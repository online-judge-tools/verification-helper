"""This module has end-to-end tests to ensure that basic features of oj-verify command work.

To test for each language, use other modules.
"""

import datetime
import json
import os
import pathlib
import unittest
from typing import *

import onlinejudge_verify.marker
import onlinejudge_verify.verify as verify
import tests.utils

SUCCESS_TEST_CPP = rb"""\
#define PROBLEM "http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_1_B"
#include <cstdio>
int main() {
    int x; scanf("%d", &x);
    printf("%d\n", x * x * x);
    return 0;
}
"""

FAILURE_TEST_CPP = rb"""\
#define PROBLEM "http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_1_B"
#include <cstdio>
int main() {
    int x; scanf("%d", &x);
    printf("%d\n", x + x + x);
    return 0;
}
"""

EXTERNAL_FAILURE_FLAG_TEST_CPP = rb"""\
#define EXTERNAL_FAILURE_FLAG EXT_FAILURE_TEST
int main() {
    return 0;
}
"""

TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S %z'


def get_timestamp_string(path: pathlib.Path) -> str:
    system_local_timezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
    epoch = path.stat().st_mtime
    timestamp = datetime.datetime.fromtimestamp(epoch, tz=system_local_timezone).replace(microsecond=0)
    return timestamp.strftime(TIMESTAMP_FORMAT)


def get_timestamp_string_of_past() -> str:
    system_local_timezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
    timestamp = datetime.datetime(year=2000, month=1, day=1, tzinfo=system_local_timezone)
    return timestamp.strftime(TIMESTAMP_FORMAT)


class TestVerification(unittest.TestCase):
    def test_success(self) -> None:
        """
        `test_success` is a simple test for the case when the `.test.cpp` gets AC.
        """

        files = {
            'example.test.cpp': SUCCESS_TEST_CPP,
        }
        paths = [pathlib.Path('example.test.cpp')]
        with tests.utils.load_files(files) as tempdir:
            with tests.utils.chdir(tempdir):
                timestamps_path = tempdir / 'timestamps.json'
                with onlinejudge_verify.marker.VerificationMarker(json_path=timestamps_path, use_git_timestamp=False) as marker:
                    self.assertEqual(verify.main(paths, marker=marker).failed_test_paths, [])
                with open(timestamps_path) as fh:
                    timestamps = json.load(fh)
                self.assertEqual(list(timestamps.keys()), ['example.test.cpp'])

    def test_failure(self) -> None:
        """
        `test_failure` is a simple test for the case when the `.test.cpp` gets WA.
        """

        files = {
            'timestamps.json': json.dumps({
                'example.test.cpp': get_timestamp_string_of_past(),
            }).encode(),
            'example.test.cpp': FAILURE_TEST_CPP,
        }
        paths = [pathlib.Path('example.test.cpp')]
        with tests.utils.load_files(files) as tempdir:
            with tests.utils.chdir(tempdir):
                timestamps_path = tempdir / 'timestamps.json'
                with onlinejudge_verify.marker.VerificationMarker(json_path=timestamps_path, use_git_timestamp=False) as marker:
                    self.assertEqual(verify.main(paths, marker=marker).failed_test_paths, paths)
                with open(timestamps_path) as fh:
                    timestamps = json.load(fh)
                self.assertEqual(timestamps, {})

    def test_success_with_external_failure_flag(self) -> None:
        """
        `test_success_with_external_failure_flag` is a simple test for the case when the `.test.cpp` has `EXTERNAL_FAILURE_FLAG` attribute.
        """

        files = {
            'example.test.cpp': EXTERNAL_FAILURE_FLAG_TEST_CPP,
        }
        paths = [pathlib.Path('example.test.cpp')]
        with tests.utils.load_files(files) as tempdir:
            with tests.utils.chdir(tempdir):
                timestamps_path = tempdir / 'timestamps.json'
                del os.environ['EXT_FAILURE_TEST']
                with onlinejudge_verify.marker.VerificationMarker(json_path=timestamps_path, use_git_timestamp=False) as marker:
                    self.assertEqual(verify.main(paths, marker=marker).failed_test_paths, [])
                with open(timestamps_path) as fh:
                    timestamps = json.load(fh)
                self.assertEqual(list(timestamps.keys()), ['example.test.cpp'])

    def test_failure_with_external_failure_flag(self) -> None:
        """
        `test_failure_with_external_failure_flag` is a simple test for the case when the `.test.cpp` has `EXTERNAL_FAILURE_FLAG` attribute.
        """

        files = {
            'example.test.cpp': EXTERNAL_FAILURE_FLAG_TEST_CPP,
        }
        paths = [pathlib.Path('example.test.cpp')]
        with tests.utils.load_files(files) as tempdir:
            with tests.utils.chdir(tempdir):
                os.environ['EXT_FAILURE_TEST'] = '1'
                timestamps_path = tempdir / 'timestamps.json'
                with onlinejudge_verify.marker.VerificationMarker(json_path=timestamps_path, use_git_timestamp=False) as marker:
                    self.assertEqual(verify.main(paths, marker=marker).failed_test_paths, paths)
                with open(timestamps_path) as fh:
                    timestamps = json.load(fh)
                self.assertEqual(timestamps, {})

    def test_timestamps(self) -> None:
        """
        `test_timestamps` checks whether `timestamps.json` is properly updated for all cases which files have no dependencies.
        """

        # prepare files
        files = {
            'not-updated.test.cpp': SUCCESS_TEST_CPP,
            'updated-success.test.cpp': SUCCESS_TEST_CPP,
            'updated-failure.test.cpp': FAILURE_TEST_CPP,
            'new-success.test.cpp': SUCCESS_TEST_CPP,
            'new-failure.test.cpp': FAILURE_TEST_CPP,
        }
        paths = list(map(pathlib.Path, files.keys()))

        with tests.utils.load_files(files) as tempdir:
            timestamps_path = tempdir / 'timestamps.json'
            with open(timestamps_path, 'w') as fh:
                json.dump(
                    {
                        'not-updated.test.cpp': get_timestamp_string(tempdir / 'not-updated.test.cpp'),  # NOTE: os.utime doesn't work as expected on Windows
                        'updated-success.test.cpp': get_timestamp_string_of_past(),
                        'updated-failure.test.cpp': get_timestamp_string_of_past(),
                        'removed.test.cpp': get_timestamp_string_of_past(),
                    },
                    fh)

            # prepare expected values
            expected_return = list(map(pathlib.Path, [
                'updated-failure.test.cpp',
                'new-failure.test.cpp',
            ]))
            expected_timestamps = {
                'not-updated.test.cpp': get_timestamp_string(tempdir / 'not-updated.test.cpp'),
                'updated-success.test.cpp': get_timestamp_string(tempdir / 'updated-success.test.cpp'),
                'new-success.test.cpp': get_timestamp_string(tempdir / 'new-success.test.cpp'),
            }

            # check actual values
            with tests.utils.chdir(tempdir):
                with onlinejudge_verify.marker.VerificationMarker(json_path=timestamps_path, use_git_timestamp=False) as marker:
                    self.assertEqual(sorted(verify.main(paths, marker=marker).failed_test_paths), sorted(expected_return))
                with open(str(timestamps_path)) as fh:
                    timestamps = json.load(fh)
                self.assertEqual(timestamps, expected_timestamps)
