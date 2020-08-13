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


# :warning: onlinejudge_bundle/main.py

<a href="../../index.html">Back to top page</a>

* category: <a href="../../index.html#7ec143aebb09797ba7c92bba4c3edc28">onlinejudge_bundle</a>
* <a href="{{ site.github.repository_url }}/blob/master/onlinejudge_bundle/main.py">View this file on GitHub</a>
    - Last commit date: 1970-01-01 00:00:00+00:00




## Code

<a id="unbundled"></a>
{% raw %}
```cpp
# Python Version: 3.x
import argparse
import pathlib
import sys
from logging import DEBUG, basicConfig, getLogger
from typing import *

import colorlog
import onlinejudge_verify.languages

logger = getLogger(__name__)


def main(args: Optional[List[str]] = None) -> None:
    # configure logging
    log_format = '%(log_color)s%(levelname)s%(reset)s:%(name)s:%(message)s'
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(log_format))
    basicConfig(level=DEBUG, handlers=[handler])

    # parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=pathlib.Path)
    parser.add_argument('-I', metavar='dir', type=pathlib.Path, dest='iquote', default=pathlib.Path.cwd(), help='add the directory dir to the list of directories to be searched for header files during preprocessing (default: ".")')
    parsed = parser.parse_args(args)

    language = onlinejudge_verify.languages.get(parsed.path)
    assert language is not None
    sys.stdout.buffer.write(language.bundle(parsed.path, basedir=parsed.iquote))


if __name__ == "__main__":
    main()

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

