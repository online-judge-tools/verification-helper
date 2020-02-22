import json
import pathlib
import unittest
from typing import *

import onlinejudge_verify.marker
import onlinejudge_verify.verify as verify
import tests.utils


class TestStringMethods(unittest.TestCase):
    def test_success(self) -> None:
        files = {
            'example.test.cpp': '\n'.join([
                '#define PROBLEM "https://judge.yosupo.jp/problem/aplusb"',
                '#include <cstdio>',
                'int main() {',
                '    int a, b; scanf("%d%d", &a, &b);',
                '    printf("%d\\n", a + b);',
                '    return 0;',
                '}',
            ]).encode(),
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
            'timestamps.json': b"""{"data/example.test.cpp": "2000-01-01 00:00:00 +0900"}""",
            'example.test.cpp': '\n'.join([
                '#define PROBLEM "https://judge.yosupo.jp/problem/aplusb"',
                '#include <cstdio>',
                'int main() {',
                '    int a, b; scanf("%d%d", &a, &b);',
                '    printf("%d\\n", a ^ b);',
                '    return 0;',
                '}',
            ]).encode(),
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
