import contextlib
import json
import os
import pathlib
import tempfile
import unittest
from typing import *

import onlinejudge_verify.utils as utils
import onlinejudge_verify.verify as verify


@contextlib.contextmanager
def load_files(files: Dict[str, bytes]) -> Iterator[pathlib.Path]:
    with tempfile.TemporaryDirectory() as tempdir_:
        tempdir = pathlib.Path(tempdir_)
        for relpath, data in files.items():
            path = tempdir / relpath
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(str(path), "wb") as fh:
                fh.write(data)
        yield tempdir


@contextlib.contextmanager
def chdir(path: pathlib.Path) -> Iterator[None]:
    cwd = os.getcwd()
    try:
        os.chdir(str(path))
        yield
    finally:
        os.chdir(cwd)


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
        with load_files(files) as tempdir:
            with chdir(tempdir):
                timestamps_path = tempdir / 'timestamps.json'
                with utils.VerificationMarker(json_path=timestamps_path, use_git_timestamp=False) as marker:
                    verify.main(paths, marker=marker)
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
        with load_files(files) as tempdir:
            with chdir(tempdir):
                timestamps_path = tempdir / 'timestamps.json'
                with utils.VerificationMarker(json_path=timestamps_path, use_git_timestamp=False) as marker:
                    self.assertRaises(Exception, lambda: verify.main(paths, marker=marker))
                with open(str(timestamps_path)) as fh:
                    timestamps = json.load(fh)
                self.assertEqual(timestamps, {})
