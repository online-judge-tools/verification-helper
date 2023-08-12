import json
import pathlib
import textwrap
import unittest
from typing import *

import onlinejudge_verify.languages.python as python
import onlinejudge_verify.marker
import onlinejudge_verify.verify as verify
import tests.utils


class TestPythonListDependencies(unittest.TestCase):
    """TestPythonListDependencies has unit (or integrated) tests for the feature to list dependencies of Python files.
    """
    def test_one_dir(self) -> None:
        files = {
            'main.py': textwrap.dedent("""\
                import imported
                """).encode(),
            'imported.py': textwrap.dedent("""\
                print("hello")
                """).encode(),
        }

        with tests.utils.load_files(files) as tempdir:
            with tests.utils.chdir(tempdir):
                expected = sorted([tempdir / 'main.py', tempdir / 'imported.py'])
                actual = sorted(python.PythonLanguage().list_dependencies(tempdir / 'main.py', basedir=tempdir))
                self.assertEqual(actual, expected)

    def test_separated_dir(self) -> None:
        files = {
            pathlib.Path('tests', 'main.py'): textwrap.dedent("""\
                import library.imported
                """).encode(),
            pathlib.Path('library', '__init__.py'): b"",
            pathlib.Path('library', 'imported.py'): textwrap.dedent("""\
                print("hello")
                """).encode(),
        }

        with tests.utils.load_files_pathlib(files) as tempdir:
            with tests.utils.chdir(tempdir):
                # TODO: Check why this doesn't include `library/__init__.py`. The lack of `library/__init__.py` is acceptable but not so good.
                expected = sorted([tempdir / 'tests' / 'main.py', tempdir / 'library' / 'imported.py'])
                actual = sorted(python.PythonLanguage().list_dependencies(tempdir / 'tests' / 'main.py', basedir=tempdir))
                self.assertEqual(actual, expected)


LIBRARY_IMPORTED_PY = rb"""\
def solve(x: int) -> int:
    return x ** 3
"""

TESTS_MAIN_PY = rb"""\
# verify-helper: PROBLEM http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_1_B
from library.imported import solve

def main() -> None:
    x = int(input())
    ans = solve(x)
    print(ans)

if __name__ == "__main__":
        main()
"""

TESTS_MAIN_PY_WITH_STDLIB = rb"""\
# verify-helper: PROBLEM http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_1_B
from library.imported import solve
import os

def main() -> None:
    x = int(input())
    ans = solve(x)
    print(ans)

if __name__ == "__main__":
        main()
"""


class TestPythonVerification(unittest.TestCase):
    """TestPythonListDependencies has end-to-end tests for the verification of Python files.
    """
    def test_separated_dir(self) -> None:
        """`test_separated_dir` is a test for the case when the library files exist at the separate directory of the test file.
        """

        files = {
            pathlib.Path('library', '__init__.py'): b"",
            pathlib.Path('library', 'imported.py'): LIBRARY_IMPORTED_PY,
            pathlib.Path('tests', 'main.py'): TESTS_MAIN_PY,
        }
        path = pathlib.Path('tests', 'main.py')
        with tests.utils.load_files_pathlib(files) as tempdir:
            with tests.utils.chdir(tempdir):
                timestamps_path = tempdir / 'timestamps.json'
                with onlinejudge_verify.marker.VerificationMarker(json_path=timestamps_path, use_git_timestamp=False) as marker:
                    self.assertEqual(verify.main([path], marker=marker).failed_test_paths, [])
                with open(timestamps_path) as fh:
                    timestamps = json.load(fh)
                self.assertEqual(list(timestamps.keys()), [str(pathlib.Path('tests', 'main.py'))])

    def test_separated_dir_with_stdlib(self) -> None:
        """`test_separated_dir_with_stdlib` is a test for the case when the library files exist at the separate directory of the test file.
        In this test, main.py has an import of a module in stdlib.
        """

        files = {
            pathlib.Path('library', '__init__.py'): b"",
            pathlib.Path('library', 'imported.py'): LIBRARY_IMPORTED_PY,
            pathlib.Path('tests', 'main.py'): TESTS_MAIN_PY_WITH_STDLIB,
        }
        path = pathlib.Path('tests', 'main.py')
        with tests.utils.load_files_pathlib(files) as tempdir:
            with tests.utils.chdir(tempdir):
                timestamps_path = tempdir / 'timestamps.json'
                with onlinejudge_verify.marker.VerificationMarker(json_path=timestamps_path, use_git_timestamp=False) as marker:
                    self.assertEqual(verify.main([path], marker=marker).failed_test_paths, [])
                with open(timestamps_path) as fh:
                    timestamps = json.load(fh)
                self.assertEqual(list(timestamps.keys()), [str(pathlib.Path('tests', 'main.py'))])
