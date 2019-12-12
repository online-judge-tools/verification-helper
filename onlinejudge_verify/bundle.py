# Python Version: 3.x
import pathlib
import re
from logging import getLogger
from typing import *

logger = getLogger(__name__)


class Bundler(object):
    iquote: List[pathlib.Path]
    pragma_once: Set[pathlib.Path]
    result_lines: List[bytes]

    def __init__(self, *, iquote: List[pathlib.Path] = []) -> None:
        self.iquote = iquote
        self.pragma_once = set()
        self.result_lines = []

    def _line(self, line: int, path: pathlib.Path) -> None:
        while self.result_lines and self.result_lines[-1].startswith(b'#line '):
            self.result_lines.pop()
        try:
            path = path.relative_to(pathlib.Path.cwd())
        except ValueError:
            pass
        self.result_lines.append('#line {} "{}"\n'.format(line, str(path)).encode())

    def _resolve(self, path: pathlib.Path, *, included_from: pathlib.Path) -> pathlib.Path:
        if (included_from / path).exists():
            return included_from / path
        for dir_ in self.iquote:
            if (dir_ / path).exists():
                return dir_ / path
        raise FileNotFoundError('failed to include "{}"'.format(str(path)))

    def update(self, path: pathlib.Path) -> None:
        logger.info('bundle "%s"', str(path))

        with open(str(path), "rb") as fh:
            self._line(1, path)
            for i, line in enumerate(fh.readlines()):

                # #pragma once
                if re.match(rb'#\s*pragma\s+once\s*', line):
                    if i == 0:
                        if path.resolve() in self.pragma_once:
                            return
                        else:
                            self.pragma_once.add(path.resolve())
                    else:
                        logger.warning('%s: line %s: "#pragma once" found but ignored; please put it to the first line', str(path), i + 1)
                    self._line(i + 2, path)
                    continue

                # #include "..."
                matched = re.match(rb'#\s*include\s*"(.*)"\s*', line)
                if matched:
                    included = pathlib.Path(matched.group(1).decode())
                    self.update(self._resolve(included, included_from=path))
                    self._line(i + 2, path)
                    continue

                # otherwise
                self.result_lines.append(line)

    def get(self) -> bytes:
        return b''.join(self.result_lines)
