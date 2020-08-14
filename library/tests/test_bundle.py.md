---
layout: default
---

<!-- mathjax config similar to math.stackexchange -->
<script type="text/javascript" async
  src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-MML-AM_CHTML">
</script>
<script type="text/x-mathjax-config">
  MathJax.Hub.Config({
    TeX: { equationNumbers: { autoNumber: "AMS" }},
    tex2jax: {
      inlineMath: [ ['$','$'] ],
      processEscapes: true
    },
    "HTML-CSS": { matchFontHeight: false },
    displayAlign: "left",
    displayIndent: "2em"
  });
</script>

<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/jquery-balloon-js@1.1.2/jquery.balloon.min.js" integrity="sha256-ZEYs9VrgAeNuPvs15E39OsyOJaIkXEEt10fzxJ20+2I=" crossorigin="anonymous"></script>
<script type="text/javascript" src="../../assets/js/copy-button.js"></script>
<link rel="stylesheet" href="../../assets/css/copy-button.css" />


# :warning: tests/test_bundle.py

<a href="../../index.html">Back to top page</a>

* category: <a href="../../index.html#b61a6d542f9036550ba9c401c80f00ef">tests</a>
* <a href="{{ site.github.repository_url }}/blob/master/tests/test_bundle.py">View this file on GitHub</a>
    - Last commit date: 1970-01-01 00:00:00+00:00




## Code

<a id="unbundled"></a>
{% raw %}
```cpp
"""This module has tests for the bundle feature.
"""

import contextlib
import os
import pathlib
import platform
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest

import onlinejudge_bundle.main
import onlinejudge_verify.languages.cplusplus_bundle as cplusplus_bundle
import tests.utils
from onlinejudge_verify.languages.cplusplus_bundle import BundleError


@unittest.skipIf(platform.system() == 'Darwin', 'We cannot use the fake g++ of macOS.')
class TestCPlusPlusBundlingUnit(unittest.TestCase):
    def test_no_newline(self) -> None:
        # 末尾に改行がないコードをincludeした時に改行が足されていることの確認

        files = {
            'no_newline.cpp': b'void foo() {}',
            'example.test.cpp': textwrap.dedent("""\
                #include "no_newline.cpp"
                #define PROBLEM "http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_1_B"
                """).encode(),
        }
        path = pathlib.Path('example.test.cpp')
        with tests.utils.load_files(files) as tempdir:
            with tests.utils.chdir(tempdir):
                bundler = cplusplus_bundle.Bundler(iquotes=[tempdir])
                bundler.update(path)
                self.assertIn(b'void foo() {}\n', bundler.get())

    def test_uncommenting(self) -> None:
        # prepare files
        files = {
            'foo.cpp': textwrap.dedent("""\
                void foo() {}
                """).encode(),
            'bar.cpp': textwrap.dedent("""\
                void bar() {}
                """).encode(),
            'example.test.cpp': textwrap.dedent("""\
                #include "foo.cpp"
                /*
                #include "bar.cpp"
                */
                // #include "bar.cpp"
                """).encode(),
        }
        path = pathlib.Path('example.test.cpp')
        with tests.utils.load_files(files) as tempdir:
            with tests.utils.chdir(tempdir):

                # check the result
                bundler = cplusplus_bundle.Bundler(iquotes=[tempdir])
                bundler.update(path)
                bundled = bundler.get()
                self.assertIn(b'void foo() {}', bundled)
                self.assertNotIn(b'void bar() {}', bundled)

    @unittest.skipIf(shutil.which('clang++') is None, 'clang++ is required for this test')
    def test_reject_clang(self) -> None:
        files = {
            'example.test.cpp': b'',
        }
        path = pathlib.Path('example.test.cpp')
        with tests.utils.load_files(files) as tempdir:
            with tests.utils.chdir(tempdir):
                bundler = cplusplus_bundle.Bundler(iquotes=[tempdir], compiler='clang++')
                self.assertRaises(BundleError, lambda: bundler.update(path))


@unittest.skipIf(platform.system() == 'Darwin', 'We cannot use the fake g++ of macOS.')
class TestCPlusPlusBundlingEndToEnd(unittest.TestCase):
    def test_smoke(self) -> None:
        files = {
            'library.hpp': textwrap.dedent("""\
                #pragma once
                #include <string>

                std::string get_hello_world() {
                    return "Hello World";
                }
                """).encode(),
            'main.cpp': textwrap.dedent("""\
                #define PROBLEM "http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_1_A"
                #include <iostream>
                #include "library.hpp"
                using namespace std;

                int main() {
                    cout << get_hello_world() << endl;
                    return 0;
                }
                """).encode(),
        }

        with tests.utils.load_files(files) as tempdir:
            with tests.utils.chdir(tempdir):
                # bundle
                with open('main.bundled.cpp', 'w') as fh:
                    with contextlib.redirect_stdout(fh):
                        onlinejudge_bundle.main.main(args=['main.cpp'])

                # compile
                subprocess.check_call(['g++', '-o', 'a.out', 'main.bundled.cpp'], stderr=sys.stderr)

                # run
                self.assertEqual(subprocess.check_output([str(pathlib.Path('a.out').resolve())]), ('Hello World' + os.linesep).encode())

    def test_complicated(self) -> None:
        library_files = {
            pathlib.Path('library', 'macro.hpp'): textwrap.dedent("""\
                #pragma once
                #define REP(i, n) for (int i = 0; (i) < (int)(n); ++ (i))
                #define REP3(i, m, n) for (int i = (m); (i) < (int)(n); ++ (i))
                #define REP_R(i, n) for (int i = (int)(n) - 1; (i) >= 0; -- (i))
                #define REP3R(i, m, n) for (int i = (int)(n) - 1; (i) >= (int)(m); -- (i))
                #define ALL(x) std::begin(x), std::end(x)
                """).encode(),
            pathlib.Path('library', 'fibonacci.hpp'): textwrap.dedent("""\
                #pragma once
                #include <cstdint>
                #include <vector>
                #include "library/macro.hpp"

                int64_t calculate_fibonacci(int n) {
                    std::vector<int64_t> dp(n + 1);
                    dp[0] = 0;
                    dp[1] = 1;
                    REP3 (i, 2, n + 1) {
                        dp[i] = dp[i - 1] + dp[i - 2];
                    }
                    return dp[n];
                }
                """).encode(),
        }

        test_files = {
            pathlib.Path('test', 'main.cpp'): textwrap.dedent("""\
                #include <iostream>
                #include "library/macro.hpp"
                #include "library/fibonacci.hpp"
                using namespace std;

                int main() {
                    int n; cin >> n;
                    cout << calculate_fibonacci(n) << endl;
                    return 0;
                }
                """).encode(),
        }

        with tempfile.TemporaryDirectory() as tempdir_dst_:
            tempdir_dst = pathlib.Path(tempdir_dst_)

            # bundle
            with tests.utils.load_files_pathlib(library_files) as tempdir_src_library:
                with tests.utils.load_files_pathlib(test_files) as tempdir_src_test:
                    with open(tempdir_dst / 'main.bundled.cpp', 'w') as fh:
                        with contextlib.redirect_stdout(fh):
                            args = ['-I', str(tempdir_src_library), str(tempdir_src_test / 'test' / 'main.cpp')]
                            onlinejudge_bundle.main.main(args=args)

            # compile
            subprocess.check_call(['g++', '-o', str(tempdir_dst / 'a.out'), str(tempdir_dst / 'main.bundled.cpp')], stderr=sys.stderr)

            # run
            self.assertEqual(subprocess.check_output([str(tempdir_dst / 'a.out')], input=b'10\n'), ('55' + os.linesep).encode())
            self.assertEqual(subprocess.check_output([str(tempdir_dst / 'a.out')], input=b'20\n'), ('6765' + os.linesep).encode())
            self.assertEqual(subprocess.check_output([str(tempdir_dst / 'a.out')], input=b'30\n'), ('832040' + os.linesep).encode())

```
{% endraw %}

<a id="bundled"></a>
{% raw %}
```cpp
Traceback (most recent call last):
  File "/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/docs.py", line 349, in write_contents
    bundled_code = language.bundle(self.file_class.file_path, basedir=pathlib.Path.cwd())
  File "/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/languages/python.py", line 84, in bundle
    raise NotImplementedError
NotImplementedError

```
{% endraw %}

<a href="../../index.html">Back to top page</a>

