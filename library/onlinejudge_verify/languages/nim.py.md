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


# :warning: onlinejudge_verify/languages/nim.py

<a href="../../../index.html">Back to top page</a>

* category: <a href="../../../index.html#8764973beee812e26bd247e90c5ce8ff">onlinejudge_verify/languages</a>
* <a href="{{ site.github.repository_url }}/blob/master/onlinejudge_verify/languages/nim.py">View this file on GitHub</a>
    - Last commit date: 1970-01-01 00:00:00+00:00




## Code

<a id="unbundled"></a>
{% raw %}
```cpp
# Python Version: 3.x
import functools
import pathlib
import subprocess
from logging import getLogger
from typing import *

from onlinejudge_verify.config import get_config
from onlinejudge_verify.languages.models import Language, LanguageEnvironment

logger = getLogger(__name__)


class NimLanguageEnvironment(LanguageEnvironment):
    compile_to: str
    NIMFLAGS: List[str]

    def __init__(self, *, compile_to: str, NIMFLAGS: List[str]):
        self.compile_to = compile_to
        self.NIMFLAGS = NIMFLAGS

    def compile(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> None:
        command = ["nim", self.compile_to, "-p:.", f"-o:{str(tempdir /'a.out')}", f"--nimcache:{str(tempdir)}"] + self.NIMFLAGS + [str(path)]
        logger.info('$ %s', ' '.join(command))
        subprocess.check_call(command)

    def get_execute_command(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> List[str]:
        return [str(tempdir / "a.out")]


@functools.lru_cache(maxsize=None)
def _list_direct_dependencies(path: pathlib.Path, *, basedir: pathlib.Path) -> List[pathlib.Path]:
    items: List[str] = []
    with (basedir / path).open() as fh:
        for line in fh:
            line = line.strip()
            if line.startswith('include'):
                items += line[7:].strip().split(',')
            elif line.startswith('import'):
                line = line[6:]
                i = line.find(' except ')
                if i >= 0:
                    line = line[:i]
                items += line.split(',')
            elif line.startswith('from'):
                i = line.find(' import ')
                if i >= 0:
                    items += line[4:i - 1]
    dependencies = [path.resolve()]
    for item in items:
        item = item.strip()
        if item.startswith("\""):
            item = item[1:len(item) - 1]
        else:
            item += ".nim"
        item_ = pathlib.Path(item)
        if item_.exists():
            dependencies.append(item_)
    return list(set(dependencies))


class NimLanguage(Language):
    config: Dict[str, Any]

    def __init__(self, *, config: Optional[Dict[str, Any]] = None):
        if config is None:
            self.config = get_config().get('languages', {}).get('nim', {})
        else:
            self.config = config

    def list_dependencies(self, path: pathlib.Path, *, basedir: pathlib.Path) -> List[pathlib.Path]:
        dependencies = []
        visited: Set[pathlib.Path] = set()
        stk = [path.resolve()]
        while stk:
            path = stk.pop()
            if path in visited:
                continue
            visited.add(path)
            for child in _list_direct_dependencies(path, basedir=basedir):
                dependencies.append(child)
                stk.append(child)
        return list(set(dependencies))

    def bundle(self, path: pathlib.Path, *, basedir: pathlib.Path) -> bytes:
        raise NotImplementedError

    def is_verification_file(self, path: pathlib.Path, *, basedir: pathlib.Path) -> bool:
        return path.name.endswith("_test.nim")

    def list_environments(self, path: pathlib.Path, *, basedir: pathlib.Path) -> List[NimLanguageEnvironment]:
        default_compile_to = 'cpp'
        default_NIMFLAGS = ['-d:release', '--opt:speed']
        envs = []
        if 'environments' not in self.config:
            envs.append(NimLanguageEnvironment(compile_to=default_compile_to, NIMFLAGS=default_NIMFLAGS))
        else:
            for env in self.config['environments']:
                compile_to = env.get('compile_to', default_compile_to)
                NIMFLAGS: List[str] = env.get('NIMFLAGS', default_NIMFLAGS)
                if not isinstance(NIMFLAGS, list):
                    raise RuntimeError('NIMFLAGS must ba a list')
                envs.append(NimLanguageEnvironment(compile_to=compile_to, NIMFLAGS=NIMFLAGS))
        return envs

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

