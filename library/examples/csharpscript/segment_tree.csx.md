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


# :heavy_check_mark: examples/csharpscript/segment_tree.csx

<a href="../../../index.html">Back to top page</a>

* category: <a href="../../../index.html#441c1a781d23a6e65db56eaa313dbebd">examples/csharpscript</a>
* <a href="{{ site.github.repository_url }}/blob/master/examples/csharpscript/segment_tree.csx">View this file on GitHub</a>
    - Last commit date: 2020-02-16 04:32:52+09:00




## Verified with

* :heavy_check_mark: <a href="../../../verify/examples/csharpscript/segment_tree.point_set_range_composite.test.csx.html">examples/csharpscript/segment_tree.point_set_range_composite.test.csx</a>
* :heavy_check_mark: <a href="../../../verify/examples/csharpscript/segment_tree.range_minimum_query.test.csx.html">examples/csharpscript/segment_tree.range_minimum_query.test.csx</a>
* :heavy_check_mark: <a href="../../../verify/examples/csharpscript/segment_tree.range_sum_query.test.csx.html">examples/csharpscript/segment_tree.range_sum_query.test.csx</a>


## Code

<a id="unbundled"></a>
{% raw %}
```cpp
class SegmentTree<T>
{
    public int Count { get; private set; }
    T Identity;
    T[] Data;
    Func<T, T, T> Merge;
    int LeafCount;
    public SegmentTree(int count, T identity, Func<T, T, T> merge)
    {
        Count = count;
        Identity = identity;
        Merge = merge;
        LeafCount = 1;
        while (LeafCount < count) LeafCount <<= 1;
        Data = new T[LeafCount << 1];
        for (int i = 1; i < Data.Length; i++) Data[i] = identity;
    }
    public T this[int index]
    {
        get { return Data[LeafCount + index]; }
        set { Assign(index, value); }
    }
    public void Assign(int i, T x) { Data[i += LeafCount] = x; while (0 < (i >>= 1)) Data[i] = Merge(Data[i << 1], Data[(i << 1) | 1]); }
    public void Operate(int i, T x) { Data[i += LeafCount] = Merge(Data[i], x); while (0 < (i >>= 1)) Data[i] = Merge(Data[i << 1], Data[(i << 1) | 1]); }
    public T Slice(int l, int length) => Fold(l, l + length);
    public T Fold(int l, int r)
    {
        T lRes = Identity, rRes = Identity;
        for (l += LeafCount, r += LeafCount - 1; l <= r; l = (l + 1) >> 1, r = (r - 1) >> 1)
        {
            if ((l & 1) == 1) lRes = Merge(lRes, Data[l]);
            if ((r & 1) == 0) rRes = Merge(Data[r], rRes);
        }
        return Merge(lRes, rRes);
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

