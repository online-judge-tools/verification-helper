# Python Version: 3.x
import json
import os
import pathlib
import shlex
import subprocess
from typing import *

CXXFLAGS = os.environ.get('CXXFLAGS', '--std=c++17 -O2 -Wall -g')

timestamps = {'~': 'dummy'}

path_timestamp = pathlib.Path('.verify-helper/timestamp/timestamp.json')
if path_timestamp.exists():
    with open(path_timestamp, 'r') as f:
        timestamps = json.loads(f.read())


def list_depending_files(path: pathlib.Path, *, compiler: str) -> List[pathlib.Path]:
    code = r"""{} {} -I . -MD -MF /dev/stdout -MM {} | sed '1s/[^:].*: // ; s/\\$//' | xargs -n 1""".format(compiler, CXXFLAGS, shlex.quote(str(path)))
    data = subprocess.check_output(code, shell=True)
    return list(map(pathlib.Path, data.decode().splitlines()))


def list_defined_macros(path: pathlib.Path, *, compiler: str) -> Dict[str, str]:
    code = r"""{} {} -I . -dM -E {}""".format(compiler, CXXFLAGS, shlex.quote(str(path)))
    data = subprocess.check_output(code, shell=True)
    define = {}
    for line in data.decode().splitlines():
        assert line.startswith('#define ')
        a, _, b = line[len('#define '):].partition(' ')
        define[a] = b
    return define


def get_last_commit_time_to_verify(path: pathlib.Path, *, compiler: str) -> str:
    depending_files = list_depending_files(path, compiler=compiler)
    code = ['git', 'log', '-1', '--date=iso', '--pretty=%ad', '--'] + list(map(lambda x: shlex.quote(str(x)), depending_files))
    return subprocess.check_output(code).decode().strip()


def is_verified(path: pathlib.Path, compiler: str) -> bool:
    return get_last_commit_time_to_verify(path, compiler=compiler) == timestamps.get(str(path), None)


def mark_verified(path: pathlib.Path, compiler: str):
    timestamps[str(path)] = get_last_commit_time_to_verify(path, compiler=compiler)


def save_timestamps():
    with open(path_timestamp, 'w') as f:
        json.dump(timestamps, f, sort_keys=True, indent=0)
