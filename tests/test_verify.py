import datetime
import json
import os
import pathlib
import unittest
from typing import *

import onlinejudge_verify.marker
import onlinejudge_verify.verify as verify
import tests.utils

success_test_cpp = rb"""\
#define PROBLEM "https://judge.yosupo.jp/problem/aplusb"
#include <cstdio>
int main() {
    int a, b; scanf("%d%d", &a, &b);
    printf("%d\n", a + b);
    return 0;
}
"""

failure_test_cpp = rb"""\
#define PROBLEM "https://judge.yosupo.jp/problem/aplusb"
#include <cstdio>
int main() {
    int a, b; scanf("%d%d", &a, &b);
    printf("%d\n", a * b);
    return 0;
}
"""

timestamp_format = '%Y-%m-%d %H:%M:%S %z'


def get_timestamp_string(path: pathlib.Path) -> str:
    system_local_timezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
    epoch = path.stat().st_mtime
    timestamp = datetime.datetime.fromtimestamp(epoch, tz=system_local_timezone).replace(microsecond=0)
    return timestamp.strftime(timestamp_format)


def get_timestamp_string_of_past() -> str:
    system_local_timezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
    timestamp = datetime.datetime(year=2000, month=1, day=1, tzinfo=system_local_timezone)
    return timestamp.strftime(timestamp_format)


def set_timestamp_string(path: pathlib.Path, s: str) -> None:
    timestamp = datetime.datetime.strptime(s, timestamp_format)
    os.utime(path, times=(path.stat().st_atime, timestamp.timestamp()))


class TestStringMethods(unittest.TestCase):
    def test_success(self) -> None:
        files = {
            'example.test.cpp': success_test_cpp,
        }
        paths = [pathlib.Path('example.test.cpp')]
        with tests.utils.load_files(files) as tempdir:
            with tests.utils.chdir(tempdir):
                timestamps_path = tempdir / 'timestamps.json'
                with onlinejudge_verify.marker.VerificationMarker(json_path=timestamps_path, use_git_timestamp=False) as marker:
                    self.assertEqual(verify.main(paths, marker=marker).failed_test_paths, [])
                with open(str(timestamps_path)) as fh:
                    timestamps = json.load(fh)
                self.assertEqual(list(timestamps.keys()), ['example.test.cpp'])

    def test_failure(self) -> None:
        files = {
            'timestamps.json': json.dumps({
                "data/example.test.cpp": "2000-01-01 00:00:00 +0900",
            }).encode(),
            'example.test.cpp': failure_test_cpp,
        }
        paths = [pathlib.Path('example.test.cpp')]
        with tests.utils.load_files(files) as tempdir:
            with tests.utils.chdir(tempdir):
                timestamps_path = tempdir / 'timestamps.json'
                with onlinejudge_verify.marker.VerificationMarker(json_path=timestamps_path, use_git_timestamp=False) as marker:
                    self.assertEqual(verify.main(paths, marker=marker).failed_test_paths, paths)
                with open(str(timestamps_path)) as fh:
                    timestamps = json.load(fh)
                self.assertEqual(timestamps, {})

    def test_timestamps(self) -> None:
        files = {
            'timestamps.json': json.dumps({
                'not-updated.test.cpp': get_timestamp_string_of_past(),
                'updated-success.test.cpp': get_timestamp_string_of_past(),
                'updated-failure.test.cpp': get_timestamp_string_of_past(),
            }).encode(),
            'not-updated.test.cpp': success_test_cpp,
            'updated-success.test.cpp': success_test_cpp,
            'updated-failure.test.cpp': failure_test_cpp,
            'new-success.test.cpp': success_test_cpp,
            'new-failure.test.cpp': failure_test_cpp,
        }
        paths = [pathlib.Path(file) for file in files.keys() if file.endswith('.cpp')]
        with tests.utils.load_files(files) as tempdir:
            set_timestamp_string(tempdir / 'not-updated.test.cpp', get_timestamp_string_of_past())
            expected_return = list(map(pathlib.Path, [
                'updated-failure.test.cpp',
                'new-failure.test.cpp',
            ]))
            expected_timestamps = {
                'not-updated.test.cpp': get_timestamp_string_of_past(),
                'updated-success.test.cpp': get_timestamp_string(tempdir / 'updated-success.test.cpp'),
                'updated-failure.test.cpp': get_timestamp_string_of_past(),  # this doesn't disappear but is recognized as failure
                'new-success.test.cpp': get_timestamp_string(tempdir / 'new-success.test.cpp'),
            }
            with tests.utils.chdir(tempdir):
                timestamps_path = tempdir / 'timestamps.json'
                with onlinejudge_verify.marker.VerificationMarker(json_path=timestamps_path, use_git_timestamp=False) as marker:
                    self.assertEqual(sorted(verify.main(paths, marker=marker).failed_test_paths), sorted(expected_return))
                with open(str(timestamps_path)) as fh:
                    timestamps = json.load(fh)
                self.assertEqual(timestamps, expected_timestamps)
