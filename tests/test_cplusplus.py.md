---
data:
  attributes: {}
  bundledCode: "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/documentation/build.py\"\
    , line 64, in _render_source_code_stat\n    bundled_code = language.bundle(stat.path,\
    \ basedir=basedir).decode()\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/languages/python.py\"\
    , line 84, in bundle\n    raise NotImplementedError\nNotImplementedError\n"
  code: "import platform\nimport textwrap\nimport unittest\nfrom typing import *\n\
    \nimport onlinejudge_verify.languages.cplusplus as cplusplus\nimport tests.utils\n\
    \n\nclass TestCPlusPlusListDependencies(unittest.TestCase):\n    \"\"\"TestCPlusPlusListDependencies\
    \ has unit tests for the feature to list dependencies of C++ files.\n    \"\"\"\
    \n    def test_success(self) -> None:\n        files = {\n            'main.cpp':\
    \ textwrap.dedent(\"\"\"\\\n                #include \"included.hpp\"\n      \
    \          \"\"\").encode(),\n            'included.hpp': textwrap.dedent(\"\"\
    \"\\\n                int main() {}\n                \"\"\").encode(),\n     \
    \   }\n\n        with tests.utils.load_files(files) as tempdir:\n            with\
    \ tests.utils.chdir(tempdir):\n                expected = sorted([tempdir / 'main.cpp',\
    \ tempdir / 'included.hpp'])\n                actual = sorted(cplusplus.CPlusPlusLanguage().list_dependencies(tempdir\
    \ / 'main.cpp', basedir=tempdir))\n                self.assertEqual(actual, expected)\n\
    \n    @unittest.skipIf(platform.system() == 'Windows', \"The path separator should\
    \ be '/' for this test.\")\n    def test_failure_with_backslash(self) -> None:\n\
    \        files = {\n            'main.cpp': textwrap.dedent(\"\"\"\\\n       \
    \         #include \".\\\\included.hpp\"\n                \"\"\").encode(),\n\
    \            'included.hpp': textwrap.dedent(\"\"\"\\\n                int main()\
    \ {}\n                \"\"\").encode(),\n        }\n\n        with tests.utils.load_files(files={})\
    \ as tempdir:\n            with tests.utils.chdir(tempdir):\n                self.assertRaises(Exception,\
    \ lambda: cplusplus.CPlusPlusLanguage().list_dependencies(tempdir / 'main.cpp',\
    \ basedir=tempdir))\n\n    @unittest.skipIf(platform.system() in ('Windows', 'Darwin'),\
    \ \"The filesystem should be case-sensitive for this test.\")\n    def test_failure_with_case_insensitive(self)\
    \ -> None:\n        files = {\n            'main.cpp': textwrap.dedent(\"\"\"\\\
    \n                #include \"INCLUDED.HPP\"\n                \"\"\").encode(),\n\
    \            'included.hpp': textwrap.dedent(\"\"\"\\\n                int main()\
    \ {}\n                \"\"\").encode(),\n        }\n\n        with tests.utils.load_files(files={})\
    \ as tempdir:\n            with tests.utils.chdir(tempdir):\n                self.assertRaises(Exception,\
    \ lambda: cplusplus.CPlusPlusLanguage().list_dependencies(tempdir / 'main.cpp',\
    \ basedir=tempdir))\n"
  dependsOn: []
  extendedDependsOn: []
  extendedRequiredBy: []
  extendedVerifiedWith: []
  isVerificationFile: false
  path: tests/test_cplusplus.py
  requiredBy: []
  timestamp: '1970-01-01 00:00:00+00:00'
  verificationStatus: LIBRARY_NO_TESTS
  verificationStatusIcon: ':warning:'
  verifiedWith: []
documentation_of: tests/test_cplusplus.py
layout: document
redirect_from:
- /library/tests/test_cplusplus.py
- /library/tests/test_cplusplus.py.html
title: tests/test_cplusplus.py
---
