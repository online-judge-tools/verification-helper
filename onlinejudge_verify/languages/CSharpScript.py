# Python Version: 3.x
import functools
import os
import pathlib
import re
from typing import *

from onlinejudge_verify.languages.base import Language


@functools.lru_cache(maxsize=None)
def _get_csx_dependencies(path: pathlib.Path) -> Set[pathlib.Path]:
    def _resolve_dependencies(path: pathlib.Path, deps: Set[pathlib.Path]) -> None:
        path = path.resolve()
        if path in deps:
            return
        deps.add(path)
        content = path.read_text()
        matchobj = re.search(r'^\s*#load\s*"\s*(.+)\s*"', content, flags=re.MULTILINE)
        if matchobj is None:
            return
        for match in matchobj.groups():
            if match.startswith("nuget:"):
                continue

            if os.path.isabs(match):
                _resolve_dependencies(pathlib.Path(match), deps)
            else:
                _resolve_dependencies(path.parent / match, deps)\

    res: Set[pathlib.Path] = Set()
    _resolve_dependencies(path.resolve(), res)
    return res


def _get_csx_pragmas(path: pathlib.Path) -> Dict[str, str]:
    content = path.read_text()
    print(content)
    matchobj = re.search(r'^\s*#pragma\s*(.+)\s+(.+)\s*$', content, flags=re.MULTILINE)
    print(matchobj)
    res: Dict[str, str] = {}
    if matchobj is None:
        return res
    matches = matchobj.groups()
    for kvpair in [matches[i:i + 2] for i in range(0, len(matches), 2)]:
        res[kvpair[0]] = kvpair[1]
    return res


class CSharpScriptLanguage(Language):
    def compile(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> None:
        pass

    def get_execute_command(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> List[str]:
        return ['dotnet-script', str(path), '-c', 'Release']

    def list_attributes(self, path: pathlib.Path, *, basedir: pathlib.Path) -> Dict[str, str]:
        return _get_csx_pragmas(path.resolve())

    def list_dependencies(self, path: pathlib.Path, *, basedir: pathlib.Path) -> List[pathlib.Path]:
        return List(_get_csx_dependencies(path.resolve()))

    def bundle(self, path: pathlib.Path, *, basedir: pathlib.Path) -> bytes:
        raise NotImplementedError
