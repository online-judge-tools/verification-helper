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
<script type="text/javascript" src="../../../assets/js/copy-button.js"></script>
<link rel="stylesheet" href="../../../assets/css/copy-button.css" />


# :warning: onlinejudge_verify/languages/python.py

<a href="../../../index.html">Back to top page</a>

* category: <a href="../../../index.html#8764973beee812e26bd247e90c5ce8ff">onlinejudge_verify/languages</a>
* <a href="{{ site.github.repository_url }}/blob/master/onlinejudge_verify/languages/python.py">View this file on GitHub</a>
    - Last commit date: 1970-01-01 00:00:00+00:00




## Code

<a id="unbundled"></a>
{% raw %}
```cpp
# Python Version: 3.x
import functools
import pathlib
import sys
import textwrap
from logging import getLogger
from typing import List, Sequence, Tuple

import importlab.environment
import importlab.fs
import importlab.graph
from onlinejudge_verify.languages.models import Language, LanguageEnvironment

logger = getLogger(__name__)


class PythonLanguageEnvironment(LanguageEnvironment):
    def compile(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> None:
        code = textwrap.dedent(f"""\
            #!{sys.executable}
            \"\"\"This is a helper script to run the target Python code.

            We need this script to set PYTHONPATH portably. The env command, quoting something, etc. are not portable or difficult to implement.
            \"\"\"

            import os
            import sys

            # arguments
            path = {repr(str(path.resolve()))}
            basedir = {repr(str(basedir.resolve()))}

            # run {str(path)}
            env = dict(os.environ)
            if "PYTHONPATH" in env:
                env["PYTHONPATH"] = basedir + os.pathsep + env["PYTHONPATH"] 
            else:
                env["PYTHONPATH"] = basedir  # set `PYTHONPATH` to import files relative to the root directory
            os.execve(sys.executable, [sys.executable, path], env=env)  # use `os.execve` to avoid making an unnecessary parent process
        """)
        with open(str(tempdir / 'compiled.py'), 'w') as fh:
            fh.write(code)

    def get_execute_command(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> List[str]:
        return [sys.executable, str(tempdir / 'compiled.py')]


@functools.lru_cache(maxsize=None)
def _python_list_depending_files(path: pathlib.Path, basedir: pathlib.Path) -> List[pathlib.Path]:
    # compute the dependency graph of the `path`
    env = importlab.environment.Environment(
        importlab.fs.Path([importlab.fs.OSFileSystem(str(basedir.resolve()))]),
        (sys.version_info.major, sys.version_info.minor),
    )
    res_graph = importlab.graph.ImportGraph.create(env, [str(path)])
    try:
        node_deps_pairs = res_graph.deps_list()  # type: List[Tuple[str, List[str]]]
    except Exception:
        raise RuntimeError(f"Failed to analyze the dependency graph (circular imports?): {path}")
    logger.debug('the dependency graph of %s: %s', str(path), node_deps_pairs)

    # collect Python files which are depended by the `path` and under `basedir`
    res_deps = []  # type: List[pathlib.Path]
    res_deps.append(path.resolve())
    for node_, deps_ in node_deps_pairs:
        node = pathlib.Path(node_)
        deps = list(map(pathlib.Path, deps_))
        if node.resolve() == path.resolve():
            for dep in deps:
                if basedir.resolve() in dep.resolve().parents:
                    res_deps.append(dep.resolve())
            break
    return list(set(res_deps))


class PythonLanguage(Language):
    def list_dependencies(self, path: pathlib.Path, *, basedir: pathlib.Path) -> List[pathlib.Path]:
        return _python_list_depending_files(path.resolve(), basedir)

    def bundle(self, path: pathlib.Path, *, basedir: pathlib.Path) -> bytes:
        """
        :throws NotImplementedError:
        """
        raise NotImplementedError

    def is_verification_file(self, path: pathlib.Path, *, basedir: pathlib.Path) -> bool:
        return '.test.py' in path.name

    def list_environments(self, path: pathlib.Path, *, basedir: pathlib.Path) -> Sequence[PythonLanguageEnvironment]:
        # TODO add another environment (e.g. pypy)
        return [PythonLanguageEnvironment()]

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

<a href="../../../index.html">Back to top page</a>

