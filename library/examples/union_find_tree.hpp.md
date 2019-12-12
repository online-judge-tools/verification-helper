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


# :heavy_check_mark: a Union-Find Tree
<a href="../../index.html">Back to top page</a>

* category: examples
* <a href="{{ site.github.repository_url }}/blob/master/examples/union_find_tree.hpp">View this file on GitHub</a>
    - Last commit date: 2019-12-09 18:30:56 +0900




## Verified With
* :heavy_check_mark: <a href="../../verify/examples/union_find_tree.aoj.test.cpp.html">examples/union_find_tree.aoj.test.cpp</a>
* :heavy_check_mark: <a href="../../verify/examples/union_find_tree.yosupo.test.cpp.html">examples/union_find_tree.yosupo.test.cpp</a>


## Code
{% raw %}
```cpp
#pragma once
#include <algorithm>
#include <vector>

/**
 * @brief a Union-Find Tree
 * @note most operations in $O(\alpha(n))$ where $\alpha(n)$ is the inverse of Ackermann function
 * @note implemented with union-by-size + path-compression
 */
struct union_find_tree {
    std::vector<int> data;
    union_find_tree() = default;
    explicit union_find_tree(int n) : data(n, -1) {}
    bool is_root(int i) { return data[i] < 0; }
    int find_root(int i) { return is_root(i) ? i : (data[i] = find_root(data[i])); }
    int tree_size(int i) { return - data[find_root(i)]; }
    int unite_trees(int i, int j) {
        i = find_root(i); j = find_root(j);
        if (i != j) {
            if (tree_size(i) < tree_size(j)) std::swap(i, j);
            data[i] += data[j];
            data[j] = i;
        }
        return i;
    }
    bool is_same(int i, int j) { return find_root(i) == find_root(j); }
};

```
{% endraw %}

<a href="../../index.html">Back to top page</a>

