# Python Version: 3.x
import pathlib
import re
from logging import getLogger
from typing import *

import onlinejudge_verify.utils as utils

logger = getLogger(__name__)


class BundleError(Exception):
    def __init__(self, path: pathlib.Path, line: int, message: str, *args, **kwargs):
        try:
            path = path.resolve().relative_to(pathlib.Path.cwd())
        except ValueError:
            pass
        message = '{}: line {}: {}'.format(str(path), line, message)
        super().__init__(message, *args, **kwargs)  # type: ignore


class Bundler(object):
    iquotes: List[pathlib.Path]
    pragma_once: Set[pathlib.Path]
    result_lines: List[bytes]
    path_stack: Set[pathlib.Path]

    def __init__(self, *, iquotes: List[pathlib.Path] = []) -> None:
        self.iquotes = iquotes
        self.pragma_once = set()
        self.result_lines = []
        self.path_stack = set()

    # これをしないと __FILE__ や __LINE__ が壊れる
    def _line(self, line: int, path: pathlib.Path) -> None:
        while self.result_lines and self.result_lines[-1].startswith(b'#line '):
            self.result_lines.pop()
        try:
            path = path.relative_to(pathlib.Path.cwd())
        except ValueError:
            pass
        self.result_lines.append('#line {} "{}"\n'.format(line, str(path)).encode())

    # path を解決する
    # see: https://gcc.gnu.org/onlinedocs/gcc/Directory-Options.html#Directory-Options
    def _resolve(self, path: pathlib.Path, *, included_from: pathlib.Path) -> pathlib.Path:
        if (included_from.parent / path).exists():
            return included_from.parent / path
        for dir_ in self.iquotes:
            if (dir_ / path).exists():
                return dir_ / path
        raise BundleError(path, -1, "no such header")

    def update(self, path: pathlib.Path) -> None:
        if path in self.pragma_once:
            logger.info('%s: skipped since this file is included once with include guard', str(path))
            return

        # 再帰的に自分自身を #include してたら諦める
        if path in self.path_stack:
            raise BundleError(path, -1, "cycle found in inclusion relations")
        self.path_stack.add(path)
        try:

            with open(str(path), "rb") as fh:
                code = fh.read()

            # include guard のまわりの変数
            # NOTE: include guard に使われたマクロがそれ以外の用途にも使われたり #undef されたりすると壊れるけど、無視します
            non_guard_line_found = False
            include_guard_macro = None  # type: Optional[str]
            include_guard_endif_found = False
            preprocess_if_nest = 0

            self._line(1, path)
            for i, (line, uncommented_line) in enumerate(zip(code.splitlines(keepends=True), utils.get_uncommented_code(path, iquotes=self.iquotes).splitlines(keepends=True))):

                # #pragma once
                if re.match(rb'\s*#\s*pragma\s+once\s*', line):  # #pragma once は comment 扱いで消されてしまう
                    logger.info('%s: line %s: #pragma once', str(path), i + 1)
                    if i != 0:
                        # 先頭以外で #pragma once されてた場合は諦める
                        raise BundleError(path, i + 1, "#pragma once found in a non-first line")
                    if path.resolve() in self.pragma_once:
                        return
                    self.pragma_once.add(path.resolve())
                    self._line(i + 2, path)
                    continue

                # #ifndef HOGE_H as guard
                if not non_guard_line_found and include_guard_macro is None:
                    matched = re.match(rb'\s*#\s*ifndef\s+(\w+)\s*', uncommented_line)
                    if matched:
                        include_guard_macro = matched.group(1).decode()
                        logger.info('%s: line %s: #ifndef %s', str(path), i + 1, include_guard_macro)
                        self.result_lines.append(b"\n")
                        continue

                # #define HOGE_H as guard
                if not non_guard_line_found and include_guard_macro is not None:
                    matched = re.match(rb'\s*#\s*define\s+(\w+)\s*', uncommented_line)
                    if matched and matched.group(1).decode() == include_guard_macro:
                        self.pragma_once.add(path.resolve())
                        logger.info('%s: line %s: #define %s', str(path), i + 1, include_guard_macro)
                        self.result_lines.append(b"\n")
                        continue

                # #endif as guard
                if include_guard_macro is not None and preprocess_if_nest == 0 and not include_guard_endif_found:
                    if re.match(rb'\s*#\s*endif\s*', uncommented_line):
                        include_guard_endif_found = True
                        self.result_lines.append(b"\n")
                        continue

                if uncommented_line:
                    # include guard の外側にコードが書かれているとまずいので検出する
                    non_guard_line_found = True
                    if include_guard_endif_found:
                        raise BundleError(path, i + 1, "found codes out of include guard")

                # #if #ifdef #ifndef
                if re.match(rb'\s*#\s*(if|ifdef|ifndef)\s.*', uncommented_line):
                    preprocess_if_nest += 1
                    self.result_lines.append(line)
                    continue

                # #else #elif
                if re.match(rb'\s*#\s*(else\s*|elif\s.*)', uncommented_line):
                    if preprocess_if_nest == 0:
                        raise BundleError(path, i + 1, "unmatched #else / #elif")
                    self.result_lines.append(line)
                    continue

                # #endif
                if re.match(rb'\s*#\s*endif\s*', uncommented_line):
                    preprocess_if_nest -= 1
                    if preprocess_if_nest < 0:
                        raise BundleError(path, i + 1, "unmatched #endif")
                    self.result_lines.append(line)
                    continue

                # #include "..."
                matched = re.match(rb'\s*#\s*include\s*"(.*)"\s*', uncommented_line)
                if matched:
                    included = pathlib.Path(matched.group(1).decode())
                    logger.info('%s: line %s: include %s', str(path), i + 1, str(included))
                    if preprocess_if_nest:
                        # #if の中から #include されると #pragma once 系の判断が不可能になるので諦める
                        raise BundleError(path, i + 1, "unable to process #include in #if / #ifdef / #ifndef other than include guards")
                    self.update(self._resolve(included, included_from=path))
                    self._line(i + 2, path)
                    continue

                # otherwise
                self.result_lines.append(line)

            # #if #endif の対応が壊れてたら諦める
            if preprocess_if_nest != 0:
                raise BundleError(path, i + 1, "unmatched #if / #ifdef / #ifndef")
            if include_guard_macro is not None and not include_guard_endif_found:
                raise BundleError(path, i + 1, "unmatched #ifndef")

        finally:
            # 中で return することがあるので finally 節に入れておく
            self.path_stack.remove(path)

    def get(self) -> bytes:
        return b''.join(self.result_lines)
