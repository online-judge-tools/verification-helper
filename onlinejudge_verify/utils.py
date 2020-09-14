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


def iterate_verification_files() -> Iterator[pathlib.Path]:
    paths = [pathlib.Path(path) for path in glob.glob('**/*', recursive=True)]  # use glob.glob because this ignore hidden files
    for path in paths:
        if is_verification_file(path):
            yield path
