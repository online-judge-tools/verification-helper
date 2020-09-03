---
data:
  attributes: {}
  bundledCode: "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/documentation/build.py\"\
    , line 58, in _render_source_code_stat\n    bundled_code = language.bundle(stat.path,\
    \ basedir=basedir).decode()\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/languages/python.py\"\
    , line 84, in bundle\n    raise NotImplementedError\nNotImplementedError\n"
  code: "\"\"\"This module has end-to-end tests to ensure that basic features of oj-verify\
    \ command work.\n\nTo test for each language, use other modules.\n\"\"\"\n\nimport\
    \ datetime\nimport json\nimport pathlib\nimport unittest\nfrom typing import *\n\
    \nimport onlinejudge_verify.marker\nimport onlinejudge_verify.verify as verify\n\
    import tests.utils\n\nsuccess_test_cpp = rb\"\"\"\\\n#define PROBLEM \"http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_1_B\"\
    \n#include <cstdio>\nint main() {\n    int x; scanf(\"%d\", &x);\n    printf(\"\
    %d\\n\", x * x * x);\n    return 0;\n}\n\"\"\"\n\nfailure_test_cpp = rb\"\"\"\\\
    \n#define PROBLEM \"http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_1_B\"\
    \n#include <cstdio>\nint main() {\n    int x; scanf(\"%d\", &x);\n    printf(\"\
    %d\\n\", x + x + x);\n    return 0;\n}\n\"\"\"\n\ntimestamp_format = '%Y-%m-%d\
    \ %H:%M:%S %z'\n\n\ndef get_timestamp_string(path: pathlib.Path) -> str:\n   \
    \ system_local_timezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo\n\
    \    epoch = path.stat().st_mtime\n    timestamp = datetime.datetime.fromtimestamp(epoch,\
    \ tz=system_local_timezone).replace(microsecond=0)\n    return timestamp.strftime(timestamp_format)\n\
    \n\ndef get_timestamp_string_of_past() -> str:\n    system_local_timezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo\n\
    \    timestamp = datetime.datetime(year=2000, month=1, day=1, tzinfo=system_local_timezone)\n\
    \    return timestamp.strftime(timestamp_format)\n\n\nclass TestVerification(unittest.TestCase):\n\
    \    def test_success(self) -> None:\n        \"\"\"\n        `test_success` is\
    \ a simple test for the case when the `.test.cpp` gets AC.\n        \"\"\"\n\n\
    \        files = {\n            'example.test.cpp': success_test_cpp,\n      \
    \  }\n        paths = [pathlib.Path('example.test.cpp')]\n        with tests.utils.load_files(files)\
    \ as tempdir:\n            with tests.utils.chdir(tempdir):\n                timestamps_path\
    \ = tempdir / 'timestamps.json'\n                with onlinejudge_verify.marker.VerificationMarker(json_path=timestamps_path,\
    \ use_git_timestamp=False) as marker:\n                    self.assertEqual(verify.main(paths,\
    \ marker=marker).failed_test_paths, [])\n                with open(timestamps_path)\
    \ as fh:\n                    timestamps = json.load(fh)\n                self.assertEqual(list(timestamps.keys()),\
    \ ['example.test.cpp'])\n\n    def test_failure(self) -> None:\n        \"\"\"\
    \n        `test_failure` is a simple test for the case when the `.test.cpp` gets\
    \ WA.\n        \"\"\"\n\n        files = {\n            'timestamps.json': json.dumps({\n\
    \                'example.test.cpp': get_timestamp_string_of_past(),\n       \
    \     }).encode(),\n            'example.test.cpp': failure_test_cpp,\n      \
    \  }\n        paths = [pathlib.Path('example.test.cpp')]\n        with tests.utils.load_files(files)\
    \ as tempdir:\n            with tests.utils.chdir(tempdir):\n                timestamps_path\
    \ = tempdir / 'timestamps.json'\n                with onlinejudge_verify.marker.VerificationMarker(json_path=timestamps_path,\
    \ use_git_timestamp=False) as marker:\n                    self.assertEqual(verify.main(paths,\
    \ marker=marker).failed_test_paths, paths)\n                with open(timestamps_path)\
    \ as fh:\n                    timestamps = json.load(fh)\n                self.assertEqual(timestamps,\
    \ {})\n\n    def test_timestamps(self) -> None:\n        \"\"\"\n        `test_timestamps`\
    \ checks whether `timestamps.json` is properly updated for all cases which files\
    \ have no dependencies.\n        \"\"\"\n\n        # prepare files\n        files\
    \ = {\n            'not-updated.test.cpp': success_test_cpp,\n            'updated-success.test.cpp':\
    \ success_test_cpp,\n            'updated-failure.test.cpp': failure_test_cpp,\n\
    \            'new-success.test.cpp': success_test_cpp,\n            'new-failure.test.cpp':\
    \ failure_test_cpp,\n        }\n        paths = list(map(pathlib.Path, files.keys()))\n\
    \n        with tests.utils.load_files(files) as tempdir:\n            timestamps_path\
    \ = tempdir / 'timestamps.json'\n            with open(timestamps_path, 'w') as\
    \ fh:\n                json.dump(\n                    {\n                   \
    \     'not-updated.test.cpp': get_timestamp_string(tempdir / 'not-updated.test.cpp'),\
    \  # NOTE: os.utime doesn't work as expected on Windows\n                    \
    \    'updated-success.test.cpp': get_timestamp_string_of_past(),\n           \
    \             'updated-failure.test.cpp': get_timestamp_string_of_past(),\n  \
    \                      'removed.test.cpp': get_timestamp_string_of_past(),\n \
    \                   },\n                    fh)\n\n            # prepare expected\
    \ values\n            expected_return = list(map(pathlib.Path, [\n           \
    \     'updated-failure.test.cpp',\n                'new-failure.test.cpp',\n \
    \           ]))\n            expected_timestamps = {\n                'not-updated.test.cpp':\
    \ get_timestamp_string(tempdir / 'not-updated.test.cpp'),\n                'updated-success.test.cpp':\
    \ get_timestamp_string(tempdir / 'updated-success.test.cpp'),\n              \
    \  'new-success.test.cpp': get_timestamp_string(tempdir / 'new-success.test.cpp'),\n\
    \            }\n\n            # check actual values\n            with tests.utils.chdir(tempdir):\n\
    \                with onlinejudge_verify.marker.VerificationMarker(json_path=timestamps_path,\
    \ use_git_timestamp=False) as marker:\n                    self.assertEqual(sorted(verify.main(paths,\
    \ marker=marker).failed_test_paths), sorted(expected_return))\n              \
    \  with open(str(timestamps_path)) as fh:\n                    timestamps = json.load(fh)\n\
    \                self.assertEqual(timestamps, expected_timestamps)\n"
  dependsOn: []
  extendedDependsOn: []
  extendedRequiredBy: []
  extendedVerifiedWith: []
  isVerificationFile: false
  path: tests/test_verify.py
  requiredBy: []
  timestamp: '1970-01-01 00:00:00+00:00'
  verificationStatus: LIBRARY_NO_TESTS
  verificationStatusIcon: ':warning:'
  verifiedWith: []
documentation_of: tests/test_verify.py
layout: document
redirect_from:
- /library/tests/test_verify.py
- /library/tests/test_verify.py.html
title: tests/test_verify.py
---
