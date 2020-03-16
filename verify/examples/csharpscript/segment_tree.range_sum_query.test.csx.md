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


# :heavy_check_mark: examples/csharpscript/segment_tree.range_sum_query.test.csx

<a href="../../../index.html">Back to top page</a>

* category: <a href="../../../index.html#441c1a781d23a6e65db56eaa313dbebd">examples/csharpscript</a>
* <a href="{{ site.github.repository_url }}/blob/master/examples/csharpscript/segment_tree.range_sum_query.test.csx">View this file on GitHub</a>
    - Last commit date: 2020-02-16 04:32:52+09:00


* see: <a href="https://onlinejudge.u-aizu.ac.jp/courses/library/3/DSL/all/DSL_2_B">https://onlinejudge.u-aizu.ac.jp/courses/library/3/DSL/all/DSL_2_B</a>


## Depends on

* :heavy_check_mark: <a href="../../../library/examples/csharpscript/segment_tree.csx.html">examples/csharpscript/segment_tree.csx</a>


## Code

<a id="unbundled"></a>
{% raw %}
```cpp
#load "./segment_tree.csx"
#pragma PROBLEM https://onlinejudge.u-aizu.ac.jp/courses/library/3/DSL/all/DSL_2_B

using System;
using System.Linq;

var nq = Console.ReadLine().Split().Select(int.Parse).ToArray();
var (n, q) = (nq[0], nq[1]);
SegmentTree<int> segTree = new SegmentTree<int>(n, 0, (x, y) => x + y);

for (int i = 0; i < q; i++)
{
    var query = Console.ReadLine().Split().Select(int.Parse).ToArray();
    if (query[0] == 0)
    {
        segTree[query[1] - 1] += query[2];
    }
    else
    {
        Console.WriteLine(segTree[(query[1] - 1)..query[2]]);
    }
}

```
{% endraw %}

<a id="bundled"></a>
{% raw %}
```cpp
Traceback (most recent call last):
  File "/opt/hostedtoolcache/Python/3.8.2/x64/lib/python3.8/site-packages/onlinejudge_verify/docs.py", line 340, in write_contents
    bundled_code = language.bundle(self.file_class.file_path, basedir=pathlib.Path.cwd())
  File "/opt/hostedtoolcache/Python/3.8.2/x64/lib/python3.8/site-packages/onlinejudge_verify/languages/csharpscript.py", line 110, in bundle
    raise NotImplementedError
NotImplementedError

```
{% endraw %}

<a href="../../../index.html">Back to top page</a>

