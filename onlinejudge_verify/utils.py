# Python Version: 3.x
import os
import pathlib
from typing import *

import onlinejudge_verify.languages


def is_local_execution() -> bool:
    return 'GITHUB_ACTION' not in os.environ


def is_verification_file(path: pathlib.Path) -> bool:
    language = onlinejudge_verify.languages.get(path)
    return language is not None and language.is_verification_file(path, basedir=pathlib.Path.cwd())


def iterate_verification_files() -> Iterator[pathlib.Path]:
    for path in pathlib.Path.cwd().glob('**/*'):
        if is_verification_file(path):
            yield path
