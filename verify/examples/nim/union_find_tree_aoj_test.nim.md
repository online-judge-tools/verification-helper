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


# :heavy_check_mark: examples/nim/union_find_tree_aoj_test.nim

<a href="../../../index.html">Back to top page</a>

* category: <a href="../../../index.html#26e849903ad505103514429c8edaff70">examples/nim</a>
* <a href="{{ site.github.repository_url }}/blob/master/examples/nim/union_find_tree_aoj_test.nim">View this file on GitHub</a>
    - Last commit date: 2020-05-05 19:43:22+09:00


* see: <a href="https://onlinejudge.u-aizu.ac.jp/courses/library/3/DSL/all/DSL_1_A">https://onlinejudge.u-aizu.ac.jp/courses/library/3/DSL/all/DSL_1_A</a>


## Depends on

* :heavy_check_mark: <a href="../../../library/examples/nim/headers.nim.html">examples/nim/headers.nim</a>
* :heavy_check_mark: <a href="../../../library/examples/nim/hoge.nim.html">examples/nim/hoge.nim</a>
* :heavy_check_mark: <a href="../../../library/examples/nim/union_find_tree.nim.html">a Union-Find Tree <small>(examples/nim/union_find_tree.nim)</small></a>


## Code

<a id="unbundled"></a>
{% raw %}
```cpp
# verify-helper: PROBLEM https://onlinejudge.u-aizu.ac.jp/courses/library/3/DSL/all/DSL_1_A

include "examples/nim/headers.nim"
import "examples/nim/union_find_tree.nim" except hoge
include "examples/nim/union_find_tree.nim"
include "examples/nim/union_find_tree.nim"
include "examples/nim/union_find_tree.nim"
include "examples/nim/union_find_tree.nim"

let
  n, q = nextInt()
var uft = initUnionFindTree(n)
for i in 0..<q:
  let com, x, y = nextInt()
  if com == 0:
    uft.unite_trees(x, y)
  elif com == 1:
    echo if uft.is_same(x, y): 1 else: 0

```
{% endraw %}

<a id="bundled"></a>
{% raw %}
```cpp
Traceback (most recent call last):
  File "/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/docs.py", line 349, in write_contents
    bundled_code = language.bundle(self.file_class.file_path, basedir=pathlib.Path.cwd())
  File "/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/languages/nim.py", line 86, in bundle
    raise NotImplementedError
NotImplementedError

```
{% endraw %}

<a href="../../../index.html">Back to top page</a>

