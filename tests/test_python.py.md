---
data:
  _extendedDependsOn: []
  _extendedRequiredBy: []
  _extendedVerifiedWith: []
  _pathExtension: py
  _verificationStatusIcon: ':warning:'
  attributes:
    PROBLEM: http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_1_B
  bundledCode: "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/documentation/build.py\"\
    , line 67, in _render_source_code_stat\n    bundled_code = language.bundle(stat.path,\
    \ basedir=basedir).decode()\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/languages/python.py\"\
    , line 84, in bundle\n    raise NotImplementedError\nNotImplementedError\n"
  code: "import json\nimport pathlib\nimport textwrap\nimport unittest\nfrom typing\
    \ import *\n\nimport onlinejudge_verify.languages.python as python\nimport onlinejudge_verify.marker\n\
    import onlinejudge_verify.verify as verify\nimport tests.utils\n\n\nclass TestPythonListDependencies(unittest.TestCase):\n\
    \    \"\"\"TestPythonListDependencies has unit (or integrated) tests for the feature\
    \ to list dependencies of Python files.\n    \"\"\"\n    def test_one_dir(self)\
    \ -> None:\n        files = {\n            'main.py': textwrap.dedent(\"\"\"\\\
    \n                import imported\n                \"\"\").encode(),\n       \
    \     'imported.py': textwrap.dedent(\"\"\"\\\n                print(\"hello\"\
    )\n                \"\"\").encode(),\n        }\n\n        with tests.utils.load_files(files)\
    \ as tempdir:\n            with tests.utils.chdir(tempdir):\n                expected\
    \ = sorted([tempdir / 'main.py', tempdir / 'imported.py'])\n                actual\
    \ = sorted(python.PythonLanguage().list_dependencies(tempdir / 'main.py', basedir=tempdir))\n\
    \                self.assertEqual(actual, expected)\n\n    def test_separated_dir(self)\
    \ -> None:\n        files = {\n            pathlib.Path('tests', 'main.py'): textwrap.dedent(\"\
    \"\"\\\n                import library.imported\n                \"\"\").encode(),\n\
    \            pathlib.Path('library', '__init__.py'): b\"\",\n            pathlib.Path('library',\
    \ 'imported.py'): textwrap.dedent(\"\"\"\\\n                print(\"hello\")\n\
    \                \"\"\").encode(),\n        }\n\n        with tests.utils.load_files_pathlib(files)\
    \ as tempdir:\n            with tests.utils.chdir(tempdir):\n                #\
    \ TODO: Check why this doesn't include `library/__init__.py`. The lack of `library/__init__.py`\
    \ is acceptable but not so good.\n                expected = sorted([tempdir /\
    \ 'tests' / 'main.py', tempdir / 'library' / 'imported.py'])\n               \
    \ actual = sorted(python.PythonLanguage().list_dependencies(tempdir / 'tests'\
    \ / 'main.py', basedir=tempdir))\n                self.assertEqual(actual, expected)\n\
    \n\nlibrary_imported_py = rb\"\"\"\\\ndef solve(x: int) -> int:\n    return x\
    \ ** 3\n\"\"\"\n\ntests_main_py = rb\"\"\"\\\n# verify-helper: PROBLEM http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_1_B\n\
    from library.imported import solve\n\ndef main() -> None:\n    x = int(input())\n\
    \    ans = solve(x)\n    print(ans)\n\nif __name__ == \"__main__\":\n        main()\n\
    \"\"\"\n\n\nclass TestPythonVerification(unittest.TestCase):\n    \"\"\"TestPythonListDependencies\
    \ has end-to-end tests for the verification of Python files.\n    \"\"\"\n   \
    \ def test_separated_dir(self) -> None:\n        \"\"\"`test_separated_dir` is\
    \ a test for the case when the library files exist at the separate directory of\
    \ the test file.\n        \"\"\"\n\n        files = {\n            pathlib.Path('library',\
    \ '__init__.py'): b\"\",\n            pathlib.Path('library', 'imported.py'):\
    \ library_imported_py,\n            pathlib.Path('tests', 'main.py'): tests_main_py,\n\
    \        }\n        path = pathlib.Path('tests', 'main.py')\n        with tests.utils.load_files_pathlib(files)\
    \ as tempdir:\n            with tests.utils.chdir(tempdir):\n                timestamps_path\
    \ = tempdir / 'timestamps.json'\n                with onlinejudge_verify.marker.VerificationMarker(json_path=timestamps_path,\
    \ use_git_timestamp=False) as marker:\n                    self.assertEqual(verify.main([path],\
    \ marker=marker).failed_test_paths, [])\n                with open(timestamps_path)\
    \ as fh:\n                    timestamps = json.load(fh)\n                self.assertEqual(list(timestamps.keys()),\
    \ [str(pathlib.Path('tests', 'main.py'))])\n"
  dependsOn: []
  isVerificationFile: false
  path: tests/test_python.py
  requiredBy: []
  timestamp: '1970-01-01 00:00:00+00:00'
  verificationStatus: LIBRARY_NO_TESTS
  verifiedWith: []
documentation_of: tests/test_python.py
layout: document
redirect_from:
- /library/tests/test_python.py
- /library/tests/test_python.py.html
title: tests/test_python.py
---
