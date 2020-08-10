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


# :warning: onlinejudge_verify/config.py

<a href="../../index.html">Back to top page</a>

* category: <a href="../../index.html#3ae20b9c01bfbb11e942bafa45933435">onlinejudge_verify</a>
* <a href="{{ site.github.repository_url }}/blob/master/onlinejudge_verify/config.py">View this file on GitHub</a>
    - Last commit date: 1970-01-01 00:00:00+00:00




## Code

<a id="unbundled"></a>
{% raw %}
```cpp
# Python Version: 3.x
import pathlib
from logging import getLogger
from typing import *

import toml

logger = getLogger(__name__)

default_config_path = pathlib.Path('.verify-helper/config.toml')

_loaded_config: Optional[Dict[str, Any]] = None


def set_config_path(config_path: pathlib.Path) -> None:
    global _loaded_config
    assert _loaded_config is None
    if not config_path.exists():
        _loaded_config = {}
        logger.info('no config file')
    else:
        _loaded_config = dict(toml.load(str(config_path)))
        logger.info('config file loaded: %s: %s', str(config_path), _loaded_config)


def get_config() -> Dict[str, Any]:
    if _loaded_config is None:
        set_config_path(default_config_path)
    assert _loaded_config is not None
    return _loaded_config

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

