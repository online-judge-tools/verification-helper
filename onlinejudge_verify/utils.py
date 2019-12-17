# Python Version: 3.x
import functools
import json
import os
import pathlib
import shlex
import subprocess
from typing import *

CXX = os.environ.get('CXX', 'g++')
CXXFLAGS = os.environ.get('CXXFLAGS', '--std=c++17 -O2 -Wall -g')


class VerificationMarker(object):
    json_path: pathlib.Path
    old_timestamps: Dict[pathlib.Path, str]  # TODO: make this Dict[pathlib.Path, datetime.datetime]
    new_timestamps: Dict[pathlib.Path, str]

    def __init__(self, *, json_path: pathlib.Path) -> None:
        self.json_path = json_path
        self.load_timestamps()

    def is_verified(self, path: pathlib.Path) -> bool:
        return get_last_commit_time_to_verify(path, compiler=CXX) == self.old_timestamps.get(path)

    def mark_verified(self, path: pathlib.Path):
        self.new_timestamps[path] = get_last_commit_time_to_verify(path, compiler=CXX)

    def load_timestamps(self) -> None:
        self.old_timestamps = {}
        if self.json_path.exists():
            with open(str(self.json_path)) as fh:
                data = json.load(fh)
            for path, timestamp in data.items():
                if path == '~' and timestamp == 'dummy':
                    continue
                self.old_timestamps[pathlib.Path(path)] = timestamp
        self.new_timestamps = {}
        for path in self.old_timestamps.keys():
            if path.exists() and self.is_verified(path):
                self.mark_verified(path)

    def save_timestamps(self) -> None:
        if self.old_timestamps == self.new_timestamps:
            return
        data = {'~': 'dummy'}
        for path, timestamp in self.new_timestamps.items():
            data[str(path)] = timestamp
        with open(str(self.json_path), 'w') as fh:
            json.dump(data, fh, sort_keys=True, indent=0)

    def __enter__(self) -> 'VerificationMarker':
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.save_timestamps()


@functools.lru_cache(maxsize=None)
def _list_depending_files(path: pathlib.Path, *, compiler: str) -> List[pathlib.Path]:
    code = r"""{} {} -I . -MD -MF /dev/stdout -MM {} | sed '1s/[^:].*: // ; s/\\$//' | xargs -n 1""".format(compiler, CXXFLAGS, shlex.quote(str(path)))
    data = subprocess.check_output(code, shell=True)
    return list(map(pathlib.Path, data.decode().splitlines()))


def list_depending_files(path: pathlib.Path, *, compiler: str = CXX) -> List[pathlib.Path]:
    return _list_depending_files(path.resolve(), compiler=compiler)


@functools.lru_cache(maxsize=None)
def _list_defined_macros(path: pathlib.Path, *, compiler: str) -> Dict[str, str]:
    code = r"""{} {} -I . -dM -E {}""".format(compiler, CXXFLAGS, shlex.quote(str(path)))
    data = subprocess.check_output(code, shell=True)
    define = {}
    for line in data.decode().splitlines():
        assert line.startswith('#define ')
        a, _, b = line[len('#define '):].partition(' ')
        define[a] = b
    return define


def list_defined_macros(path: pathlib.Path, *, compiler: str = CXX) -> Dict[str, str]:
    return _list_defined_macros(path.resolve(), compiler=compiler)


@functools.lru_cache(maxsize=None)
def _get_last_commit_time_to_verify(path: pathlib.Path, *, compiler: str) -> str:
    depending_files = list_depending_files(path, compiler=compiler)
    code = ['git', 'log', '-1', '--date=iso', '--pretty=%ad', '--'] + list(map(lambda x: shlex.quote(str(x)), depending_files))
    return subprocess.check_output(code).decode().strip()


def get_last_commit_time_to_verify(path: pathlib.Path, *, compiler: str = CXX) -> str:
    return _get_last_commit_time_to_verify(path.resolve(), compiler=compiler)


@functools.lru_cache(maxsize=None)
def _get_uncommented_code(path: pathlib.Path, *, iquotes_options: str, compiler: str) -> bytes:
    command = """{} {} -fpreprocessed -dD -E {} | tail -n +2""".format(compiler, iquotes_options, shlex.quote(str(path)))
    return subprocess.check_output(command, shell=True)


def get_uncommented_code(path: pathlib.Path, *, iquotes: List[pathlib.Path], compiler: str = CXX) -> bytes:
    iquotes_options = ' '.join(map(lambda iquote: '-I {}'.format(shlex.quote(str(iquote.resolve()))), iquotes))
    return _get_uncommented_code(path.resolve(), iquotes_options=iquotes_options, compiler=compiler)
