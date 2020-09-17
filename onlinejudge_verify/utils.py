# Python Version: 3.x
import glob
import os
import pathlib
from typing import *

import onlinejudge_verify.languages.list


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
