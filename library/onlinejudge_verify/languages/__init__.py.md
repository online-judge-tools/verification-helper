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


# :warning: onlinejudge_verify/languages/__init__.py

<a href="../../../index.html">Back to top page</a>

* category: <a href="../../../index.html#8764973beee812e26bd247e90c5ce8ff">onlinejudge_verify/languages</a>
* <a href="{{ site.github.repository_url }}/blob/master/onlinejudge_verify/languages/__init__.py">View this file on GitHub</a>
    - Last commit date: 1970-01-01 00:00:00+00:00




## Code

<a id="unbundled"></a>
{% raw %}
```cpp
import pathlib
from logging import getLogger
from typing import *

import toml
from onlinejudge_verify.config import get_config
from onlinejudge_verify.languages.cplusplus import CPlusPlusLanguage
from onlinejudge_verify.languages.csharpscript import CSharpScriptLanguage
from onlinejudge_verify.languages.models import Language, LanguageEnvironment
from onlinejudge_verify.languages.nim import NimLanguage
from onlinejudge_verify.languages.other import OtherLanguage
from onlinejudge_verify.languages.python import PythonLanguage

logger = getLogger(__name__)

_dict: Optional[Dict[str, Language]] = None


def _get_dict() -> Dict[str, Language]:
    global _dict
    if _dict is None:
        _dict = {}
        _dict['.cpp'] = CPlusPlusLanguage()
        _dict['.hpp'] = _dict['.cpp']
        _dict['.csx'] = CSharpScriptLanguage()
        _dict['.nim'] = NimLanguage()
        _dict['.py'] = PythonLanguage()

        for ext, config in get_config().get('languages', {}).items():
            if '.' + ext in _dict:
                for key in ('compile', 'execute', 'bundle', 'list_attributes', 'list_dependencies'):
                    if key in config:
                        raise RuntimeError("You cannot overwrite existing language: .{}".format(ext))
            else:
                logger.warn("config.toml: languages.%s: Adding new languages using `config.toml` is supported but not recommended. Please consider making pull requests for your languages, see https://github.com/kmyk/online-judge-verify-helper/issues/116", ext)
                _dict['.' + ext] = OtherLanguage(config=config)
    return _dict


def get(path: pathlib.Path) -> Optional[Language]:
    return _get_dict().get(path.suffix)

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

