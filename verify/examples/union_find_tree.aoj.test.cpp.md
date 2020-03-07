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


# :heavy_check_mark: examples/union_find_tree.aoj.test.cpp

<a href="../../index.html">Back to top page</a>

* category: <a href="../../index.html#bfebe34154a0dfd9fc7b447fc9ed74e9">examples</a>
* <a href="{{ site.github.repository_url }}/blob/master/examples/union_find_tree.aoj.test.cpp">View this file on GitHub</a>
    - Last commit date: 2019-12-16 05:18:36+09:00


* see: <a href="https://onlinejudge.u-aizu.ac.jp/courses/library/3/DSL/all/DSL_1_A">https://onlinejudge.u-aizu.ac.jp/courses/library/3/DSL/all/DSL_1_A</a>


## Depends on

* :heavy_check_mark: <a href="../../library/examples/macros.hpp.html">examples/macros.hpp</a>
* :heavy_check_mark: <a href="../../library/examples/union_find_tree.hpp.html">a Union-Find Tree <small>(examples/union_find_tree.hpp)</small></a>


## Code

<a id="unbundled"></a>
{% raw %}
```cpp
#define PROBLEM "https://onlinejudge.u-aizu.ac.jp/courses/library/3/DSL/all/DSL_1_A"
#include <iostream>
#include "examples/union_find_tree.hpp"
#include "examples/union_find_tree.hpp"
#include "examples/union_find_tree.hpp"
#include "examples/union_find_tree.hpp"
#include "examples/union_find_tree.hpp"
#include "examples/macros.hpp"
using namespace std;

int main() {
    int n, q; cin >> n >> q;
    union_find_tree uft(n);
    REP (i, q) {
        int com, x, y; cin >> com >> x >> y;
        if (com == 0) {
            uft.unite_trees(x, y);
        } else if (com == 1) {
            cout << uft.is_same(x, y) << endl;
        }
    }
    return 0;
}

```
{% endraw %}

<a id="bundled"></a>
{% raw %}
```cpp
#line 1 "examples/union_find_tree.aoj.test.cpp"
#define PROBLEM "https://onlinejudge.u-aizu.ac.jp/courses/library/3/DSL/all/DSL_1_A"
#include <iostream>
#line 1 "examples/union_find_tree.hpp"


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


#line 2 "examples/macros.hpp"
#define REP(i, n) for (int i = 0; (i) < (int)(n); ++ (i))
#define REP3(i, m, n) for (int i = (m); (i) < (int)(n); ++ (i))
#define REP_R(i, n) for (int i = (int)(n) - 1; (i) >= 0; -- (i))
#define REP3R(i, m, n) for (int i = (int)(n) - 1; (i) >= (int)(m); -- (i))
#define ALL(x) begin(x), end(x)
#line 9 "examples/union_find_tree.aoj.test.cpp"
using namespace std;

int main() {
    int n, q; cin >> n >> q;
    union_find_tree uft(n);
    REP (i, q) {
        int com, x, y; cin >> com >> x >> y;
        if (com == 0) {
            uft.unite_trees(x, y);
        } else if (com == 1) {
            cout << uft.is_same(x, y) << endl;
        }
    }
    return 0;
}

```
{% endraw %}

<a href="../../index.html">Back to top page</a>

