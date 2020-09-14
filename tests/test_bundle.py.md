---
data:
  _extendedDependsOn: []
  _extendedRequiredBy: []
  _extendedVerifiedWith: []
  _pathExtension: py
  _verificationStatusIcon: ':warning:'
  attributes:
    links:
    - http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_1_A
    - http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_1_B
  bundledCode: "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/documentation/build.py\"\
    , line 70, in _render_source_code_stat\n    bundled_code = language.bundle(stat.path,\
    \ basedir=basedir).decode()\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/languages/python.py\"\
    , line 84, in bundle\n    raise NotImplementedError\nNotImplementedError\n"
  code: "\"\"\"This module has tests for the bundle feature.\n\"\"\"\n\nimport contextlib\n\
    import os\nimport pathlib\nimport platform\nimport shutil\nimport subprocess\n\
    import sys\nimport tempfile\nimport textwrap\nimport unittest\n\nimport onlinejudge_bundle.main\n\
    import onlinejudge_verify.languages.cplusplus_bundle as cplusplus_bundle\nimport\
    \ tests.utils\nfrom onlinejudge_verify.languages.cplusplus_bundle import BundleError\n\
    \n\n@unittest.skipIf(platform.system() == 'Darwin', 'We cannot use the fake g++\
    \ of macOS.')\nclass TestCPlusPlusBundlingUnit(unittest.TestCase):\n    def test_no_newline(self)\
    \ -> None:\n        # \u672B\u5C3E\u306B\u6539\u884C\u304C\u306A\u3044\u30B3\u30FC\
    \u30C9\u3092include\u3057\u305F\u6642\u306B\u6539\u884C\u304C\u8DB3\u3055\u308C\
    \u3066\u3044\u308B\u3053\u3068\u306E\u78BA\u8A8D\n\n        files = {\n      \
    \      'no_newline.cpp': b'void foo() {}',\n            'example.test.cpp': textwrap.dedent(\"\
    \"\"\\\n                #include \"no_newline.cpp\"\n                #define PROBLEM\
    \ \"http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_1_B\"\n    \
    \            \"\"\").encode(),\n        }\n        path = pathlib.Path('example.test.cpp')\n\
    \        with tests.utils.load_files(files) as tempdir:\n            with tests.utils.chdir(tempdir):\n\
    \                bundler = cplusplus_bundle.Bundler(iquotes=[tempdir])\n     \
    \           bundler.update(path)\n                self.assertIn(b'void foo() {}\\\
    n', bundler.get())\n\n    def test_uncommenting(self) -> None:\n        # prepare\
    \ files\n        files = {\n            'foo.cpp': textwrap.dedent(\"\"\"\\\n\
    \                void foo() {}\n                \"\"\").encode(),\n          \
    \  'bar.cpp': textwrap.dedent(\"\"\"\\\n                void bar() {}\n      \
    \          \"\"\").encode(),\n            'example.test.cpp': textwrap.dedent(\"\
    \"\"\\\n                #include \"foo.cpp\"\n                /*\n           \
    \     #include \"bar.cpp\"\n                */\n                // #include \"\
    bar.cpp\"\n                \"\"\").encode(),\n        }\n        path = pathlib.Path('example.test.cpp')\n\
    \        with tests.utils.load_files(files) as tempdir:\n            with tests.utils.chdir(tempdir):\n\
    \n                # check the result\n                bundler = cplusplus_bundle.Bundler(iquotes=[tempdir])\n\
    \                bundler.update(path)\n                bundled = bundler.get()\n\
    \                self.assertIn(b'void foo() {}', bundled)\n                self.assertNotIn(b'void\
    \ bar() {}', bundled)\n\n    @unittest.skipIf(shutil.which('clang++') is None,\
    \ 'clang++ is required for this test')\n    def test_reject_clang(self) -> None:\n\
    \        files = {\n            'example.test.cpp': b'',\n        }\n        path\
    \ = pathlib.Path('example.test.cpp')\n        with tests.utils.load_files(files)\
    \ as tempdir:\n            with tests.utils.chdir(tempdir):\n                bundler\
    \ = cplusplus_bundle.Bundler(iquotes=[tempdir], compiler='clang++')\n        \
    \        self.assertRaises(BundleError, lambda: bundler.update(path))\n\n\n@unittest.skipIf(platform.system()\
    \ == 'Darwin', 'We cannot use the fake g++ of macOS.')\nclass TestCPlusPlusBundlingEndToEnd(unittest.TestCase):\n\
    \    def test_smoke(self) -> None:\n        files = {\n            'library.hpp':\
    \ textwrap.dedent(\"\"\"\\\n                #pragma once\n                #include\
    \ <string>\n\n                std::string get_hello_world() {\n              \
    \      return \"Hello World\";\n                }\n                \"\"\").encode(),\n\
    \            'main.cpp': textwrap.dedent(\"\"\"\\\n                #define PROBLEM\
    \ \"http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_1_A\"\n    \
    \            #include <iostream>\n                #include \"library.hpp\"\n \
    \               using namespace std;\n\n                int main() {\n       \
    \             cout << get_hello_world() << endl;\n                    return 0;\n\
    \                }\n                \"\"\").encode(),\n        }\n\n        with\
    \ tests.utils.load_files(files) as tempdir:\n            with tests.utils.chdir(tempdir):\n\
    \                # bundle\n                with open('main.bundled.cpp', 'w')\
    \ as fh:\n                    with contextlib.redirect_stdout(fh):\n         \
    \               onlinejudge_bundle.main.main(args=['main.cpp'])\n\n          \
    \      # compile\n                subprocess.check_call(['g++', '-o', 'a.out',\
    \ 'main.bundled.cpp'], stderr=sys.stderr)\n\n                # run\n         \
    \       self.assertEqual(subprocess.check_output([str(pathlib.Path('a.out').resolve())]),\
    \ ('Hello World' + os.linesep).encode())\n\n    def test_complicated(self) ->\
    \ None:\n        library_files = {\n            pathlib.Path('library', 'macro.hpp'):\
    \ textwrap.dedent(\"\"\"\\\n                #pragma once\n                #define\
    \ REP(i, n) for (int i = 0; (i) < (int)(n); ++ (i))\n                #define REP3(i,\
    \ m, n) for (int i = (m); (i) < (int)(n); ++ (i))\n                #define REP_R(i,\
    \ n) for (int i = (int)(n) - 1; (i) >= 0; -- (i))\n                #define REP3R(i,\
    \ m, n) for (int i = (int)(n) - 1; (i) >= (int)(m); -- (i))\n                #define\
    \ ALL(x) std::begin(x), std::end(x)\n                \"\"\").encode(),\n     \
    \       pathlib.Path('library', 'fibonacci.hpp'): textwrap.dedent(\"\"\"\\\n \
    \               #pragma once\n                #include <cstdint>\n           \
    \     #include <vector>\n                #include \"library/macro.hpp\"\n\n  \
    \              int64_t calculate_fibonacci(int n) {\n                    std::vector<int64_t>\
    \ dp(n + 1);\n                    dp[0] = 0;\n                    dp[1] = 1;\n\
    \                    REP3 (i, 2, n + 1) {\n                        dp[i] = dp[i\
    \ - 1] + dp[i - 2];\n                    }\n                    return dp[n];\n\
    \                }\n                \"\"\").encode(),\n        }\n\n        test_files\
    \ = {\n            pathlib.Path('test', 'main.cpp'): textwrap.dedent(\"\"\"\\\n\
    \                #include <iostream>\n                #include \"library/macro.hpp\"\
    \n                #include \"library/fibonacci.hpp\"\n                using namespace\
    \ std;\n\n                int main() {\n                    int n; cin >> n;\n\
    \                    cout << calculate_fibonacci(n) << endl;\n               \
    \     return 0;\n                }\n                \"\"\").encode(),\n      \
    \  }\n\n        with tempfile.TemporaryDirectory() as tempdir_dst_:\n        \
    \    tempdir_dst = pathlib.Path(tempdir_dst_)\n\n            with tests.utils.load_files_pathlib(library_files)\
    \ as tempdir_src_library:\n                with tests.utils.load_files_pathlib(test_files)\
    \ as tempdir_src_test:\n                    with open(tempdir_dst / 'main.bundled.cpp',\
    \ 'w') as fh:\n                        with contextlib.redirect_stdout(fh):\n\
    \                            args = ['-I', str(tempdir_src_library), str(tempdir_src_test\
    \ / 'test' / 'main.cpp')]\n                            onlinejudge_bundle.main.main(args=args)\n\
    \n            # compile\n            subprocess.check_call(['g++', '-o', str(tempdir_dst\
    \ / 'a.out'), str(tempdir_dst / 'main.bundled.cpp')], stderr=sys.stderr)\n\n \
    \           # run\n            self.assertEqual(subprocess.check_output([str(tempdir_dst\
    \ / 'a.out')], input=b'10\\n'), ('55' + os.linesep).encode())\n            self.assertEqual(subprocess.check_output([str(tempdir_dst\
    \ / 'a.out')], input=b'20\\n'), ('6765' + os.linesep).encode())\n            self.assertEqual(subprocess.check_output([str(tempdir_dst\
    \ / 'a.out')], input=b'30\\n'), ('832040' + os.linesep).encode())\n\n    def test_standard_headers(self)\
    \ -> None:\n        test_files = {pathlib.Path('test', 'main.cpp'): textwrap.dedent(\"\
    \"\"\\\n            #include <bits/stdtr1c++.h>\n            #include <tr2/dynamic_bitset>\n\
    \            #include <bits/extc++.h>\n            #include <ext/rope>\n     \
    \       // #include <boost/multiprecision/cpp_int.hpp>\n            #include <bits/stdc++.h>\n\
    \            #include <cassert>\n            int main() {\n                __gnu_cxx::rope<int>\
    \ a;\n                using namespace std::tr1::__detail;\n                std::tr2::dynamic_bitset<unsigned>\
    \ b;\n                // using mulint = boost::multiprecision::cpp_int;\n    \
    \            using std::vector;\n                assert(1);\n                return\
    \ 0;\n            }\n            \"\"\").encode()}\n\n        with tempfile.TemporaryDirectory()\
    \ as tempdir_dst_:\n            tempdir_dst = pathlib.Path(tempdir_dst_)\n\n \
    \           # bundle\n            with tests.utils.load_files_pathlib(test_files)\
    \ as tempdir_src_test:\n                with open(tempdir_dst / 'main.bundled.cpp',\
    \ 'w') as fh:\n                    with contextlib.redirect_stdout(fh):\n    \
    \                    args = [str(tempdir_src_test / 'test' / 'main.cpp')]\n  \
    \                      onlinejudge_bundle.main.main(args=args)\n\n           \
    \ # compile\n            subprocess.check_call(['g++', str(tempdir_dst / 'main.bundled.cpp')],\
    \ stderr=sys.stderr)\n"
  dependsOn: []
  isVerificationFile: false
  path: tests/test_bundle.py
  requiredBy: []
  timestamp: '1970-01-01 00:00:00+00:00'
  verificationStatus: LIBRARY_NO_TESTS
  verifiedWith: []
documentation_of: tests/test_bundle.py
layout: document
redirect_from:
- /library/tests/test_bundle.py
- /library/tests/test_bundle.py.html
title: tests/test_bundle.py
---
