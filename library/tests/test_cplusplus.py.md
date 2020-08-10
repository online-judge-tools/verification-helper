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


# :warning: tests/test_cplusplus.py

<a href="../../index.html">Back to top page</a>

* category: <a href="../../index.html#b61a6d542f9036550ba9c401c80f00ef">tests</a>
* <a href="{{ site.github.repository_url }}/blob/master/tests/test_cplusplus.py">View this file on GitHub</a>
    - Last commit date: 1970-01-01 00:00:00+00:00




## Code

<a id="unbundled"></a>
{% raw %}
```cpp
import platform
import textwrap
import unittest
from typing import *

import onlinejudge_verify.languages.cplusplus as cplusplus
import tests.utils


class TestCPlusPlusListDependencies(unittest.TestCase):
    """TestCPlusPlusListDependencies has unit tests for the feature to list dependencies of C++ files.
    """
    def test_success(self) -> None:
        files = {
            'main.cpp': textwrap.dedent("""\
                #include "included.hpp"
                """).encode(),
            'included.hpp': textwrap.dedent("""\
                int main() {}
                """).encode(),
        }

        with tests.utils.load_files(files) as tempdir:
            with tests.utils.chdir(tempdir):
                expected = sorted([tempdir / 'main.cpp', tempdir / 'included.hpp'])
                actual = sorted(cplusplus.CPlusPlusLanguage().list_dependencies(tempdir / 'main.cpp', basedir=tempdir))
                self.assertEqual(actual, expected)

    @unittest.skipIf(platform.system() == 'Windows', "The path separator should be '/' for this test.")
    def test_failure_with_backslash(self) -> None:
        files = {
            'main.cpp': textwrap.dedent("""\
                #include ".\\included.hpp"
                """).encode(),
            'included.hpp': textwrap.dedent("""\
                int main() {}
                """).encode(),
        }

        with tests.utils.load_files(files={}) as tempdir:
            with tests.utils.chdir(tempdir):
                self.assertRaises(Exception, lambda: cplusplus.CPlusPlusLanguage().list_dependencies(tempdir / 'main.cpp', basedir=tempdir))

    @unittest.skipIf(platform.system() in ('Windows', 'Darwin'), "The filesystem should be case-sensitive for this test.")
    def test_failure_with_case_insensitive(self) -> None:
        files = {
            'main.cpp': textwrap.dedent("""\
                #include "INCLUDED.HPP"
                """).encode(),
            'included.hpp': textwrap.dedent("""\
                int main() {}
                """).encode(),
        }

        with tests.utils.load_files(files={}) as tempdir:
            with tests.utils.chdir(tempdir):
                self.assertRaises(Exception, lambda: cplusplus.CPlusPlusLanguage().list_dependencies(tempdir / 'main.cpp', basedir=tempdir))

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

