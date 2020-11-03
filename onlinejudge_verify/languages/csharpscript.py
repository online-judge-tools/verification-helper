# Python Version: 3.x
import functools
import os
import pathlib
import re
import subprocess
import uuid
from logging import getLogger
from typing import *

import onlinejudge_verify.languages.special_comments as special_comments
from onlinejudge_verify.languages.models import Language, LanguageEnvironment

logger = getLogger(__name__)

dotnet_dll_caches_dir = pathlib.Path('.verify-helper/cache') / 'dotnet-script'

pragma_line_caches: Dict[pathlib.Path, Set[int]] = {}


@functools.lru_cache(maxsize=None)
def _publish_csx(path: pathlib.Path) -> pathlib.Path:
    path = path.resolve()
    if path not in pragma_line_caches:
        pragma_line_caches[path] = set()
    filename = str(uuid.uuid4())
    command = [
        'dotnet-script',
        'publish',
        str(path),
        '--dll',
        '-n',
        filename,
        '-o',
        str(dotnet_dll_caches_dir),
        '-c',
        'Release',
    ]
    logger.info('$ %s', ' '.join(command))
    res = subprocess.check_output(command).decode().strip().splitlines()
    for warning in res[:-1]:
        matchobj = re.match(r'^(?P<file>.*)\((?P<line>\d+),\d+\): warning CS1633:', warning)
        if matchobj is None:
            continue
        file = pathlib.Path(matchobj.group('file'))
        line = int(matchobj.group('line'))
        if file not in pragma_line_caches:
            pragma_line_caches[file] = set()
        pragma_line_caches[file].add(line)
    return dotnet_dll_caches_dir / f'{filename}.dll'


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

    res: Set[pathlib.Path] = set()
    _resolve_dependencies(path.resolve(), res)
    return res


@functools.lru_cache(maxsize=None)
def _get_csx_pragmas(path: pathlib.Path) -> Dict[str, str]:
    path = path.resolve()
    if path not in pragma_line_caches:
        _publish_csx(path)
    lines = path.read_text().splitlines()
    res: Dict[str, str] = {}
    for line in pragma_line_caches[path]:
        matchobj = re.search(r'^\s*#pragma\s+(?P<key>[^\s]+)\s*(?P<value>.*)\s*', lines[line - 1])
        if matchobj is None:
            continue
        key = matchobj.group('key')
        value = matchobj.group('value')
        res[key] = value
    return res


class CSharpScriptLanguageEnvironment(LanguageEnvironment):
    def compile(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> None:
        _publish_csx(path)

    def get_execute_command(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> List[str]:
        return ['dotnet-script', 'exec', str(_publish_csx(path))]


class CSharpScriptLanguage(Language):
    def list_attributes(self, path: pathlib.Path, *, basedir: pathlib.Path) -> Dict[str, Any]:
        attributes: Dict[str, Any] = special_comments.list_special_comments(path.resolve()) or _get_csx_pragmas(path.resolve())
        attributes.setdefault('links', [])
        attributes['links'].extend(special_comments.list_embedded_urls(path))
        return attributes

    def list_dependencies(self, path: pathlib.Path, *, basedir: pathlib.Path) -> List[pathlib.Path]:
        return list(_get_csx_dependencies(path.resolve()))

    def bundle(self, path: pathlib.Path, *, basedir: pathlib.Path, options: Dict[str, Any]) -> bytes:
        raise NotImplementedError

    def list_environments(self, path: pathlib.Path, *, basedir: pathlib.Path) -> Sequence[CSharpScriptLanguageEnvironment]:
        return [CSharpScriptLanguageEnvironment()]
