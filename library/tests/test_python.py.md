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


# :warning: tests/test_python.py

<a href="../../index.html">Back to top page</a>

* category: <a href="../../index.html#b61a6d542f9036550ba9c401c80f00ef">tests</a>
* <a href="{{ site.github.repository_url }}/blob/master/tests/test_python.py">View this file on GitHub</a>
    - Last commit date: 1970-01-01 00:00:00+00:00




## Code

<a id="unbundled"></a>
{% raw %}
```cpp
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


library_imported_py = rb"""\
def solve(x: int) -> int:
    return x ** 3
"""

tests_main_py = rb"""\
# verify-helper: PROBLEM http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_1_B
from library.imported import solve

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
            pathlib.Path('library', 'imported.py'): library_imported_py,
            pathlib.Path('tests', 'main.py'): tests_main_py,
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

