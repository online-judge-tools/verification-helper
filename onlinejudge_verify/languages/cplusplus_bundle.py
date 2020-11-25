# Python Version: 3.x
import functools
import json
import os
import pathlib
import re
import shutil
import subprocess
from logging import getLogger
from typing import *

logger = getLogger(__name__)

BITS_STDCXX_H = 'bits/stdc++.h'

CXX_STANDARD_LIBS = {
    'algorithm',
    'array',
    'bitset',
    'chrono',
    'codecvt',
    'complex',
    'condition_variable',
    'deque',
    'exception',
    'forward_list',
    'fstream',
    'functional',
    'future',
    'iomanip',
    'ios',
    'iosfwd',
    'iostream',
    'istream',
    'iterator',
    'limits',
    'list',
    'locale',
    'map',
    'memory',
    'mutex',
    'new',
    'numeric',
    'ostream',
    'queue',
    'random',
    'regex',
    'set',
    'sstream',
    'stack',
    'stdexcept',
    'streambuf',
    'string',
    'thread',
    'tuple',
    'typeinfo',
    'unordered_map',
    'unordered_set',
    'utility',
    'valarray',
    'vector',
}

C_STANDARD_LIBS = {
    'assert.h',
    'complex.h',
    'ctype.h',
    'errno.h',
    'fenv.h',
    'float.h',
    'inttypes.h',
    'iso646.h',
    'limits.h',
    'locale.h',
    'math.h',
    'setjmp.h',
    'signal.h',
    'stdalign.h',
    'stdarg.h',
    'stdatomic.h',
    'stdbool.h',
    'stddef.h',
    'stdint.h',
    'stdio.h',
    'stdlib.h',
    'stdnoreturn.h',
    'string.h',
    'tgmath.h',
    'threads.h',
    'time.h',
    'uchar.h',
    'wchar.h',
    'wctype.h',
}

CXX_C_ORIGIN_LIBS = {'c' + name[:-len('.h')] for name in C_STANDARD_LIBS}

BITS_EXTCXX_H = 'bits/extc++.h'

EXT_LIBS = {
    'ext/algorithm',
    'ext/array_allocator.h',
    'ext/atomicity.h',
    'ext/bitmap_allocator.h',
    'ext/cast.h',
    'ext/concurrence.h',
    'ext/debug_allocator.h',
    'ext/extptr_allocator.h',
    'ext/functional',
    'ext/iterator',
    'ext/malloc_allocator.h',
    'ext/memory',
    'ext/mt_allocator.h',
    'ext/new_allocator.h',
    'ext/numeric',
    'ext/pod_char_traits.h',
    'ext/pointer.h',
    'ext/pool_allocator.h',
    'ext/rb_tree',
    'ext/rope',
    'ext/slist',
    'ext/stdio_filebuf.h',
    'ext/stdio_sync_filebuf.h',
    'ext/throw_allocator.h',
    'ext/typelist.h',
    'ext/type_traits.h',
    'ext/vstring.h',
    'ext/pb_ds/assoc_container.hpp',
    'ext/pb_ds/priority_queue.hpp',
    'ext/pb_ds/exception.hpp',
    'ext/pb_ds/hash_policy.hpp',
    'ext/pb_ds/list_update_policy.hpp',
    'ext/pb_ds/tree_policy.hpp',
    'ext/pb_ds/trie_policy.hpp',
}

BITS_STDTR1CXX_H = 'bits/stdtr1c++.h'

TR1_LIBS = {
    'tr1/array',
    'tr1/cctype',
    'tr1/cfenv',
    'tr1/cfloat',
    'tr1/cinttypes',
    'tr1/climits',
    'tr1/cmath',
    'tr1/complex',
    'tr1/cstdarg',
    'tr1/cstdbool',
    'tr1/cstdint',
    'tr1/cstdio',
    'tr1/cstdlib',
    'tr1/ctgmath',
    'tr1/ctime',
    'tr1/cwchar',
    'tr1/cwctype',
    'tr1/functional',
    'tr1/random',
    'tr1/tuple',
    'tr1/unordered_map',
    'tr1/unordered_set',
    'tr1/utility',
}


@functools.lru_cache(maxsize=None)
def _check_compiler(compiler: str) -> str:
    # Executables named "g++" are not always g++, due to the fake g++ of macOS
    version = subprocess.check_output([compiler, '--version']).decode()
    if 'clang' in version.lower() or 'Apple LLVM'.lower() in version.lower():
        return 'clang'
    if 'g++' in version.lower():
        return 'gcc'
    return 'unknown'  # default


@functools.lru_cache(maxsize=None)
def _get_uncommented_code(path: pathlib.Path, *, iquotes_options: Tuple[str, ...], compiler: str) -> bytes:
    # `iquotes_options` must be a tuple to use `lru_cache`

    if shutil.which(compiler) is None:
        raise BundleError(f'command not found: {compiler}')
    if _check_compiler(compiler) != 'gcc':
        if compiler == 'g++':
            raise BundleError(f'A fake g++ is detected. Please install the GNU C++ compiler.: {compiler}')
        raise BundleError(f"It's not g++. Please specify g++ with $CXX envvar.: {compiler}")
    command = [compiler, '-x', 'c++', *iquotes_options, '-fpreprocessed', '-dD', '-E', str(path)]
    return subprocess.check_output(command)


def get_uncommented_code(path: pathlib.Path, *, iquotes: List[pathlib.Path], compiler: str) -> bytes:
    iquotes_options = []
    for iquote in iquotes:
        iquotes_options.extend(['-I', str(iquote.resolve())])
    code = _get_uncommented_code(path.resolve(), iquotes_options=tuple(iquotes_options), compiler=compiler)
    lines = []  # type: List[bytes]
    for line in code.splitlines(keepends=True):
        m = re.match(rb'# (\d+) ".*"', line.rstrip())
        if m:
            lineno = int(m.group(1))
            while len(lines) + 1 < lineno:
                lines.append(b'\n')
        else:
            lines.append(line)
    return b''.join(lines)


class BundleError(Exception):
    pass


class BundleErrorAt(BundleError):
    def __init__(self, path: pathlib.Path, line: int, message: str, *args, **kwargs):
        try:
            path = path.resolve().relative_to(pathlib.Path.cwd())
        except ValueError:
            pass
        message = '{}: line {}: {}'.format(str(path), line, message)
        super().__init__(message, *args, **kwargs)  # type: ignore


class Bundler:
    iquotes: List[pathlib.Path]
    pragma_once: Set[pathlib.Path]
    pragma_once_system: Set[str]
    result_lines: List[bytes]
    path_stack: Set[pathlib.Path]
    compiler: str

    def __init__(self, *, iquotes: Optional[List[pathlib.Path]] = None, compiler: str = os.environ.get('CXX', 'g++')) -> None:
        if iquotes is None:
            iquotes = []
        self.iquotes = iquotes
        self.pragma_once = set()
        self.pragma_once_system = set()
        self.result_lines = []
        self.path_stack = set()
        self.compiler = compiler

    # これをしないと __FILE__ や __LINE__ が壊れる
    def _line(self, line: int, path: pathlib.Path) -> None:
        while self.result_lines and self.result_lines[-1].startswith(b'#line '):
            self.result_lines.pop()
        try:
            path = path.relative_to(pathlib.Path.cwd())
        except ValueError:
            pass
        # パス中の特殊文字を JSON style にエスケープしてから生成コードに記述
        # quick solution to this: https://github.com/online-judge-tools/verification-helper/issues/280
        self.result_lines.append('#line {} {}\n'.format(line, json.dumps(str(path))).encode())

    # path を解決する
    # see: https://gcc.gnu.org/onlinedocs/gcc/Directory-Options.html#Directory-Options
    def _resolve(self, path: pathlib.Path, *, included_from: pathlib.Path) -> pathlib.Path:
        if (included_from.parent / path).exists():
            return (included_from.parent / path).resolve()
        for dir_ in self.iquotes:
            if (dir_ / path).exists():
                return (dir_ / path).resolve()
        raise BundleErrorAt(path, -1, "no such header")

    def update(self, path: pathlib.Path) -> None:
        if path.resolve() in self.pragma_once:
            logger.debug('%s: skipped since this file is included once with include guard', str(path))
            return

        # 再帰的に自分自身を #include してたら諦める
        if path in self.path_stack:
            raise BundleErrorAt(path, -1, "cycle found in inclusion relations")
        self.path_stack.add(path)
        try:

            with open(str(path), "rb") as fh:
                code = fh.read()
                if not code.endswith(b"\n"):
                    # ファイルの末尾に改行がなかったら足す
                    code += b"\n"

            # include guard のまわりの変数
            # NOTE: include guard に使われたマクロがそれ以外の用途にも使われたり #undef されたりすると壊れるけど、無視します
            non_guard_line_found = False
            pragma_once_found = False
            include_guard_macro = None  # type: Optional[str]
            include_guard_define_found = False
            include_guard_endif_found = False
            preprocess_if_nest = 0

            lines = code.splitlines(keepends=True)
            uncommented_lines = get_uncommented_code(path, iquotes=self.iquotes, compiler=self.compiler).splitlines(keepends=True)
            uncommented_lines.extend([b''] * (len(lines) - len(uncommented_lines)))  # trailing comment lines are removed
            assert len(lines) == len(uncommented_lines)
            self._line(1, path)
            for i, (line, uncommented_line) in enumerate(zip(lines, uncommented_lines)):

                # nest の処理
                if re.match(rb'\s*#\s*(if|ifdef|ifndef)\s.*', uncommented_line):
                    preprocess_if_nest += 1
                if re.match(rb'\s*#\s*(else\s*|elif\s.*)', uncommented_line):
                    if preprocess_if_nest == 0:
                        raise BundleErrorAt(path, i + 1, "unmatched #else / #elif")
                if re.match(rb'\s*#\s*endif\s*', uncommented_line):
                    preprocess_if_nest -= 1
                    if preprocess_if_nest < 0:
                        raise BundleErrorAt(path, i + 1, "unmatched #endif")
                is_toplevel = preprocess_if_nest == 0 or (preprocess_if_nest == 1 and include_guard_macro is not None)

                # #pragma once
                if re.match(rb'\s*#\s*pragma\s+once\s*', line):  # #pragma once は comment 扱いで消されてしまう
                    logger.debug('%s: line %s: #pragma once', str(path), i + 1)
                    if non_guard_line_found:
                        # 先頭以外で #pragma once されてた場合は諦める
                        raise BundleErrorAt(path, i + 1, "#pragma once found in a non-first line")
                    if include_guard_macro is not None:
                        raise BundleErrorAt(path, i + 1, "#pragma once found in an include guard with #ifndef")
                    if path.resolve() in self.pragma_once:
                        return
                    pragma_once_found = True
                    self.pragma_once.add(path.resolve())
                    self._line(i + 2, path)
                    continue

                # #ifndef HOGE_H as guard
                if not pragma_once_found and not non_guard_line_found and include_guard_macro is None:
                    matched = re.match(rb'\s*#\s*ifndef\s+(\w+)\s*', uncommented_line)
                    if matched:
                        include_guard_macro = matched.group(1).decode()
                        logger.debug('%s: line %s: #ifndef %s', str(path), i + 1, include_guard_macro)
                        self.result_lines.append(b"\n")
                        continue

                # #define HOGE_H as guard
                if include_guard_macro is not None and not include_guard_define_found:
                    matched = re.match(rb'\s*#\s*define\s+(\w+)\s*', uncommented_line)
                    if matched and matched.group(1).decode() == include_guard_macro:
                        self.pragma_once.add(path.resolve())
                        logger.debug('%s: line %s: #define %s', str(path), i + 1, include_guard_macro)
                        include_guard_define_found = True
                        self.result_lines.append(b"\n")
                        continue

                # #endif as guard
                if include_guard_define_found and preprocess_if_nest == 0 and not include_guard_endif_found:
                    if re.match(rb'\s*#\s*endif\s*', uncommented_line):
                        include_guard_endif_found = True
                        self.result_lines.append(b"\n")
                        continue

                if uncommented_line:
                    non_guard_line_found = True
                    if include_guard_macro is not None and not include_guard_define_found:
                        # 先頭に #ifndef が見付かっても #define が続かないならそれは include guard ではない
                        include_guard_macro = None
                    if include_guard_endif_found:
                        # include guard の外側にコードが書かれているとまずいので検出する
                        raise BundleErrorAt(path, i + 1, "found codes out of include guard")

                # #include <...>
                matched = re.match(rb'\s*#\s*include\s*<(.*)>\s*', uncommented_line)
                if matched:
                    included = matched.group(1).decode()
                    logger.debug('%s: line %s: #include <%s>', str(path), i + 1, str(included))
                    if included in self.pragma_once_system:
                        self._line(i + 2, path)
                    elif not is_toplevel:
                        # #pragma once 系の判断ができない場合はそっとしておく
                        self.result_lines.append(line)
                    elif included in C_STANDARD_LIBS or included in CXX_STANDARD_LIBS or included in CXX_C_ORIGIN_LIBS:
                        if BITS_STDCXX_H in self.pragma_once_system:
                            self._line(i + 2, path)
                        else:
                            self.pragma_once_system.add(included)
                            self.result_lines.append(line)
                    elif included in EXT_LIBS:
                        if BITS_EXTCXX_H in self.pragma_once_system:
                            self._line(i + 2, path)
                        else:
                            self.pragma_once_system.add(included)
                            self.result_lines.append(line)
                    elif included in TR1_LIBS:
                        if BITS_STDTR1CXX_H in self.pragma_once_system:
                            self._line(i + 2, path)
                        else:
                            self.pragma_once_system.add(included)
                            self.result_lines.append(line)
                    else:
                        # possibly: bits/*, tr2/* boost/*, c-posix library, etc.
                        self.pragma_once_system.add(included)
                        self.result_lines.append(line)
                        if included in [BITS_EXTCXX_H, BITS_STDTR1CXX_H]:
                            self.pragma_once_system.add(BITS_STDCXX_H)
                    continue

                # #include "..."
                matched = re.match(rb'\s*#\s*include\s*"(.*)"\s*', uncommented_line)
                if matched:
                    included = matched.group(1).decode()
                    logger.debug('%s: line %s: #include "%s"', str(path), i + 1, included)
                    if not is_toplevel:
                        # #if の中から #include されると #pragma once 系の判断が不可能になるので諦める
                        raise BundleErrorAt(path, i + 1, "unable to process #include in #if / #ifdef / #ifndef other than include guards")
                    self.update(self._resolve(pathlib.Path(included), included_from=path))
                    self._line(i + 2, path)
                    # TODO: #include "iostream" みたいに書いたときの挙動をはっきりさせる
                    # TODO: #include <iostream> /* とかをやられた場合を落とす
                    continue

                # otherwise
                self.result_lines.append(line)

            # #if #endif の対応が壊れてたら諦める
            if preprocess_if_nest != 0:
                raise BundleErrorAt(path, i + 1, "unmatched #if / #ifdef / #ifndef")
            if include_guard_macro is not None and not include_guard_endif_found:
                raise BundleErrorAt(path, i + 1, "unmatched #ifndef")

        finally:
            # 中で return することがあるので finally 節に入れておく
            self.path_stack.remove(path)

    def get(self) -> bytes:
        return b''.join(self.result_lines)
