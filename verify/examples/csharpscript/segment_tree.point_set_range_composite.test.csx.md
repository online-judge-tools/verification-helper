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


# :heavy_check_mark: examples/csharpscript/segment_tree.point_set_range_composite.test.csx

<a href="../../../index.html">Back to top page</a>

* category: <a href="../../../index.html#441c1a781d23a6e65db56eaa313dbebd">examples/csharpscript</a>
* <a href="{{ site.github.repository_url }}/blob/master/examples/csharpscript/segment_tree.point_set_range_composite.test.csx">View this file on GitHub</a>
    - Last commit date: 2020-02-16 04:32:52+09:00


* see: <a href="https://judge.yosupo.jp/problem/point_set_range_composite">https://judge.yosupo.jp/problem/point_set_range_composite</a>


## Depends on

* :heavy_check_mark: <a href="../../../library/examples/csharpscript/segment_tree.csx.html">examples/csharpscript/segment_tree.csx</a>


## Code

<a id="unbundled"></a>
{% raw %}
```cpp
#load "./segment_tree.csx"
#pragma PROBLEM https://judge.yosupo.jp/problem/point_set_range_composite

using System;
using System.Linq;

struct Linear
{
    const int MOD = 998244353;
    public long A;
    public long B;
    public Linear(long a, long b) { A = a; B = b; }
    public static Linear Merge(Linear a, Linear b) => new Linear(a.A * b.A % MOD, (a.B * b.A + b.B) % MOD);
    public long EvalWith(int x) => (A * x + B) % MOD;
    public override string ToString() => $"{A} {B}";
}

var nq = Console.ReadLine().Split().Select(int.Parse).ToArray();
var (n, q) = (nq[0], nq[1]);
SegmentTree<Linear> segTree = new SegmentTree<Linear>(n, new Linear(1, 0), Linear.Merge);

for (int i = 0; i < n; i++)
{
    var ab = Console.ReadLine().Split().Select(int.Parse).ToArray();
    segTree[i] = new Linear(ab[0], ab[1]);
}

for (int i = 0; i < q; i++)
{
    var query = Console.ReadLine().Split().Select(int.Parse).ToArray();
    if (query[0] == 0)
    {
        segTree[query[1]] = new Linear(query[2], query[3]);
    }
    else
    {
        Console.WriteLine(segTree[query[1]..query[2]].EvalWith(query[3]));
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

