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


# :warning: a Union-Find Tree <small>(examples/nim/union_find_tree.nim)</small>

<a href="../../../index.html">Back to top page</a>

* category: <a href="../../../index.html#26e849903ad505103514429c8edaff70">examples/nim</a>
* <a href="{{ site.github.repository_url }}/blob/master/examples/nim/union_find_tree.nim">View this file on GitHub</a>
    - Last commit date: 2020-05-05 19:42:40+09:00




## Code

<a id="unbundled"></a>
{% raw %}
```cpp
when not declared(EXAMPLES_UNION_FIND_TREE_NIM):
  const EXAMPLES_UNION_FIND_TREE_NIM = true
  import sequtils
  import "examples/nim/hoge.nim"
  
  # @brief a Union-Find Tree
  # @note most operations in $O(\alpha(n))$ where $\alpha(n)$ is the inverse of Ackermann function
  # @note implemented with union-by-size + path-compression
  
  type UnionFindTree = object
    data:seq[int]
  
  proc initUnionFindTree*(n:int):UnionFindTree = UnionFindTree(data:newSeqWith(n, -1))
  
  proc isRoot*(self: UnionFindTree, i:int):bool = return self.data[i] < 0
  proc findRoot*(self: var UnionFindTree, i:int):int =
    if self.is_root(i):
      return i
    else:
      self.data[i] = self.findRoot(self.data[i])
      return self.data[i]
  proc treeSize*(self: var UnionFindTree, i:int):int = - self.data[self.findRoot(i)]
  proc uniteTrees*(self: var UnionFindTree, i, j:int):int {.discardable.} =
    var 
      i = self.findRoot(i)
      j = self.findRoot(j)
    if i != j:
      if self.tree_size(i) < self.tree_size(j): swap(i, j)
      self.data[i] += self.data[j]
      self.data[j] = i
    return i
  
  proc isSame*(self: var UnionFindTree, i, j:int):bool = self.find_root(i) == self.find_root(j)

  proc hoge*() = echo "Hello World"

```
{% endraw %}

<a id="bundled"></a>
{% raw %}
```cpp
Traceback (most recent call last):
  File "/opt/hostedtoolcache/Python/3.8.2/x64/lib/python3.8/site-packages/onlinejudge_verify/docs.py", line 349, in write_contents
    bundled_code = language.bundle(self.file_class.file_path, basedir=pathlib.Path.cwd())
  File "/opt/hostedtoolcache/Python/3.8.2/x64/lib/python3.8/site-packages/onlinejudge_verify/languages/nim.py", line 86, in bundle
    raise NotImplementedError
NotImplementedError

```
{% endraw %}

<a href="../../../index.html">Back to top page</a>

