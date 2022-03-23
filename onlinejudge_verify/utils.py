# Python Version: 3.x
import glob
import os
import pathlib
from typing import *

import onlinejudge_verify.languages.list

_dependency_dict: Dict[pathlib.Path, Set[pathlib.Path]] = {}


def _get_absolute_dependency(path: pathlib.Path, *, basedir: pathlib.Path) -> Iterable[pathlib.Path]:
    language = onlinejudge_verify.languages.list.get(path)
    if language is not None:
        try:
            for p in language.list_dependencies(path, basedir=basedir):
                yield p.absolute()
        except Exception:
            pass


def init_dependencies(paths: List[pathlib.Path], *, basedir: pathlib.Path):
    for path in paths:
        if not path.is_absolute():
            path = (basedir / path).absolute()
        if path not in _dependency_dict:
            _dependency_dict[path] = set()
        language = onlinejudge_verify.languages.list.get(path)
        if language is not None:
            _dependency_dict[path].update(_get_absolute_dependency(path, basedir=basedir))
    for path in paths:
        language = onlinejudge_verify.languages.list.get(path)
        if language is None:
            continue
        try:
            sameas = language.list_attributes(path, basedir=basedir)['SAMEAS']
        except Exception:
            continue
        if not path.is_absolute():
            path = (basedir / path).absolute()
        sameas_path = pathlib.Path(sameas).absolute()
        if sameas_path in _dependency_dict:
            _dependency_dict[sameas_path].add(path)


def get_dependencies(path: pathlib.Path, *, basedir: pathlib.Path) -> List[pathlib.Path]:
    if not path.is_absolute():
        path = (basedir / path).absolute()
    if path in _dependency_dict:
        return [p.relative_to(basedir) for p in _dependency_dict[path]]

    language = onlinejudge_verify.languages.list.get(path)
    if language is None:
        return []
    _dependency_dict[path] = set(_get_absolute_dependency(path, basedir=basedir))
    return [p.relative_to(basedir) for p in _dependency_dict[path]]


def is_local_execution() -> bool:
    return 'GITHUB_ACTION' not in os.environ


def is_verification_file(path: pathlib.Path, *, basedir: Optional[pathlib.Path] = None) -> bool:
    """`is_verification_file` is a thin wrapper for `Languge.is_verification_file`.  This function automatically get the language.
    """

    basedir = basedir or pathlib.Path.cwd()  # TODO: remove this. make basedir argument always required
    language = onlinejudge_verify.languages.list.get(path)
    return language is not None and language.is_verification_file(path, basedir=basedir)


def glob_with_predicate(pred: Callable[[pathlib.Path], bool]) -> Iterator[pathlib.Path]:
    """glob_with_basename iterates files whose basenames satisfy the predicate.

    This function ignores hidden directories and hidden files, whose names start with dot `.` letter.
    """
    return filter(pred, map(pathlib.Path, glob.glob('**', recursive=True)))


def iterate_verification_files() -> Iterator[pathlib.Path]:
    return glob_with_predicate(is_verification_file)
