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


# :warning: onlinejudge_verify/languages/other.py

<a href="../../../index.html">Back to top page</a>

* category: <a href="../../../index.html#8764973beee812e26bd247e90c5ce8ff">onlinejudge_verify/languages</a>
* <a href="{{ site.github.repository_url }}/blob/master/onlinejudge_verify/languages/other.py">View this file on GitHub</a>
    - Last commit date: 1970-01-01 00:00:00+00:00




## Code

<a id="unbundled"></a>
{% raw %}
```cpp
# Python Version: 3.x
import pathlib
import shlex
import subprocess
from logging import getLogger
from typing import *

from onlinejudge_verify.languages.models import Language, LanguageEnvironment
from onlinejudge_verify.languages.special_comments import list_special_comments

logger = getLogger(__name__)


class OtherLanguageEnvironment(LanguageEnvironment):
    config: Dict[str, str]

    def __init__(self, *, config: Dict[str, str]):
        self.config = config

    def compile(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> None:
        assert 'compile' in self.config
        command = self.config['compile'].format(path=str(path), basedir=str(basedir), tempdir=str(tempdir))
        logger.info('$ %s', command)
        subprocess.check_call(shlex.split(command))

    def get_execute_command(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> List[str]:
        assert 'execute' in self.config
        command = self.config['execute'].format(path=str(path), basedir=str(basedir), tempdir=str(tempdir))
        return shlex.split(command)


class OtherLanguage(Language):
    config: Dict[str, str]

    def __init__(self, *, config: Dict[str, str]):
        self.config = config

    def list_attributes(self, path: pathlib.Path, *, basedir: pathlib.Path) -> Dict[str, str]:
        if 'list_attributes' not in self.config:
            return list_special_comments(path)
        logger.warning('"languages.*.list_attributes" field in .verify-helper/config.toml is now obsoleted')

        command = self.config['list_attributes'].format(path=str(path), basedir=str(basedir))
        text = subprocess.check_output(shlex.split(command))
        attributes = {}
        for line in text.splitlines():
            key, _, value = line.decode().partition(' ')
            attributes[key] = value
        return attributes

    def list_dependencies(self, path: pathlib.Path, *, basedir: pathlib.Path) -> List[pathlib.Path]:
        assert 'list_dependencies' in self.config
        command = self.config['list_dependencies'].format(path=str(path), basedir=str(basedir))
        text = subprocess.check_output(shlex.split(command))
        dependencies = [path]
        for line in text.splitlines():
            dependencies.append(pathlib.Path(line.decode()))
        return dependencies

    def bundle(self, path: pathlib.Path, *, basedir: pathlib.Path) -> bytes:
        assert 'bundle' in self.config
        command = self.config['bundle'].format(path=str(path), basedir=str(basedir))
        logger.info('$ %s', command)
        return subprocess.check_output(shlex.split(command))

    def is_verification_file(self, path: pathlib.Path, *, basedir: pathlib.Path) -> bool:
        suffix = self.config.get('verification_file_suffix')
        if suffix is not None:
            return path.name.endswith(suffix)
        return super().is_verification_file(path, basedir=basedir)

    def list_environments(self, path: pathlib.Path, *, basedir: pathlib.Path) -> Sequence[OtherLanguageEnvironment]:
        return [OtherLanguageEnvironment(config=self.config)]

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

