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


# :heavy_check_mark: examples/union_find_tree.yosupo.test.cpp


[Back to top page](../../index.html)

* see: [https://judge.yosupo.jp/problem/unionfind](https://judge.yosupo.jp/problem/unionfind)


## Dependencies
* :heavy_check_mark: [examples/macros.hpp](../../library/examples/macros.hpp.html)
* :heavy_check_mark: [a Union-Find Tree](../../library/examples/union_find_tree.hpp.html)


## Code
{% raw %}
```cpp
#define PROBLEM "https://judge.yosupo.jp/problem/unionfind"
#include <iostream>
#include "examples/union_find_tree.hpp"
#include "examples/macros.hpp"
using namespace std;

int main() {
    int n, q; cin >> n >> q;
    union_find_tree uft(n);
    REP (i, q) {
        int t, u, v; cin >> t >> u >> v;
        if (t == 0) {
            uft.unite_trees(u, v);
        } else if (t == 1) {
            cout << uft.is_same(u, v) << endl;
        }
    }
    return 0;
}

```
{% endraw %}

[Back to top page](../../index.html)

