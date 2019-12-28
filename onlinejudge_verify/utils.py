# Python Version: 3.x
import datetime
import functools
import json
import os
import pathlib
import re
import shlex
import subprocess
from typing import *

CXX = os.environ.get('CXX', 'g++')
CXXFLAGS = os.environ.get('CXXFLAGS', '--std=c++17 -O2 -Wall -g')


class VerificationMarker(object):
    json_path: pathlib.Path
    use_git_timestamp: bool
    old_timestamps: Dict[pathlib.Path, datetime.datetime]
    new_timestamps: Dict[pathlib.Path, datetime.datetime]
    verification_statuses: Dict[pathlib.Path, str]

    def __init__(self, *, json_path: pathlib.Path, use_git_timestamp: bool) -> None:
        self.json_path = json_path
        self.use_git_timestamp = use_git_timestamp
        self.verification_statuses = {}
        self.load_timestamps()
        self.load_test_results()

    def get_current_timestamp(self, path: pathlib.Path) -> datetime.datetime:
        if self.use_git_timestamp:
            return get_last_commit_time_to_verify(path, compiler=CXX)
        else:
            timestamp = max([x.stat().st_mtime for x in list_depending_files(path, compiler=CXX)])
            system_local_timezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
            return datetime.datetime.fromtimestamp(timestamp, tz=system_local_timezone).replace(microsecond=0)  # microsecond=0 is required because it's erased on timestamps.*.json

    def is_verified(self, path: pathlib.Path) -> bool:
        if path not in self.verification_statuses or self.verification_statuses[path] != 'verified':
            return False
        return path in self.new_timestamps and self.get_current_timestamp(path) <= self.new_timestamps[path]

    def mark_verified(self, path: pathlib.Path) -> None:
        self.new_timestamps[path] = self.get_current_timestamp(path)
        self.verification_statuses[path] = 'verified'

    def is_failed(self, path: pathlib.Path) -> bool:
        if path not in self.verification_statuses or self.verification_statuses[path] != 'failed':
            return False
        return path in self.new_timestamps and self.get_current_timestamp(path) <= self.new_timestamps[path]

    def mark_failed(self, path: pathlib.Path) -> None:
        self.new_timestamps[path] = self.get_current_timestamp(path)
        self.verification_statuses[path] = 'failed'

    def load_timestamps(self) -> None:
        self.old_timestamps = {}
        if self.json_path.exists():
            with open(str(self.json_path)) as fh:
                data = json.load(fh)
            for path, timestamp in data.items():
                if path == '~' and timestamp == 'dummy':
                    continue
                self.old_timestamps[pathlib.Path(path)] = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S %z')
        self.new_timestamps = {}
        for path, timestamp in self.old_timestamps.items():
            if path.exists() and self.get_current_timestamp(path) <= timestamp:
                self.mark_verified(path)

    def load_test_results(self) -> None:
        old_results = {}
        # convert path from 'path/to/timestamps.~.json' to 'path/to/results.~.json'
        result_json_path = pathlib.Path(str(self.json_path).replace('/timestamps.', '/results.'))
        if result_json_path.exists():
            with open(str(result_json_path)) as fh:
                data = json.load(fh)
            for path, result in data.items():
                if path == '~':
                    continue
                old_results[pathlib.Path(path)] = result
        for path, result in old_results.items():
            timestamp = datetime.datetime.strptime(result['timestamp'], '%Y-%m-%d %H:%M:%S %z')
            if path.exists() and self.get_current_timestamp(path) <= timestamp:
                if result['status'] == 'verified':
                    self.mark_verified(path)
                elif result['status'] == 'failed':
                    self.mark_failed(path)

    def save_timestamps(self) -> None:
        if self.old_timestamps == self.new_timestamps:
            return
        data = {'~': 'dummy'}
        for path, timestamp in self.new_timestamps.items():
            data[str(path)] = timestamp.strftime('%Y-%m-%d %H:%M:%S %z')
        with open(str(self.json_path), 'w') as fh:
            json.dump(data, fh, sort_keys=True, indent=0)

    def save_test_results(self) -> None:
        if self.old_timestamps == self.new_timestamps:
            return
        data = {'~': {'status': 'dummy', 'timestamp': 'dummy'}}
        for path in self.verification_statuses:
            assert (path in self.new_timestamps)
            status = self.verification_statuses[path]
            timestamp = self.new_timestamps[path].strftime('%Y-%m-%d %H:%M:%S %z')
            data[str(path)] = {'status': status, 'timestamp': timestamp}
        # convert path from 'path/to/timestamps.~.json' to 'path/to/results.~.json'
        result_json_path = str(self.json_path).replace('/timestamps.', '/results.')
        with open(result_json_path, 'w') as fh:
            json.dump(data, fh, sort_keys=True, indent=0)

    def __enter__(self) -> 'VerificationMarker':
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.save_timestamps()
        self.save_test_results()


_verification_marker = None  # type: Optional[VerificationMarker]


def get_verification_marker() -> VerificationMarker:
    global _verification_marker
    if _verification_marker is None:
        # use different files in local and in remote to avoid conflicts
        if 'GITHUB_ACTION' in os.environ:
            timestamps_json_path = pathlib.Path('.verify-helper/timestamps.remote.json')
        else:
            timestamps_json_path = pathlib.Path('.verify-helper/timestamps.local.json')
        use_git_timestamp = 'GITHUB_ACTION' in os.environ
        _verification_marker = VerificationMarker(json_path=timestamps_json_path, use_git_timestamp=use_git_timestamp)
    return _verification_marker


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
def _get_last_commit_time_to_verify(path: pathlib.Path, *, compiler: str) -> datetime.datetime:
    depending_files = list_depending_files(path, compiler=compiler)
    code = ['git', 'log', '-1', '--date=iso', '--pretty=%ad', '--'] + list(map(lambda x: shlex.quote(str(x)), depending_files))
    timestamp = subprocess.check_output(code).decode().strip()
    if not timestamp:
        return datetime.datetime.fromtimestamp(0)
    return datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S %z')


def get_last_commit_time_to_verify(path: pathlib.Path, *, compiler: str = CXX) -> datetime.datetime:
    return _get_last_commit_time_to_verify(path.resolve(), compiler=compiler)


@functools.lru_cache(maxsize=None)
def _get_uncommented_code(path: pathlib.Path, *, iquotes_options: str, compiler: str) -> bytes:
    command = """{} {} -fpreprocessed -dD -E {}""".format(compiler, iquotes_options, shlex.quote(str(path)))
    return subprocess.check_output(command, shell=True)


def get_uncommented_code(path: pathlib.Path, *, iquotes: List[pathlib.Path], compiler: str = CXX) -> bytes:
    iquotes_options = ' '.join(map(lambda iquote: '-I {}'.format(shlex.quote(str(iquote.resolve()))), iquotes))
    code = _get_uncommented_code(path.resolve(), iquotes_options=iquotes_options, compiler=compiler)
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
