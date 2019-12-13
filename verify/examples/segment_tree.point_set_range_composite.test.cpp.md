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


# :heavy_check_mark: examples/segment_tree.point_set_range_composite.test.cpp
<a href="../../index.html">Back to top page</a>

* <a href="{{ site.github.repository_url }}/blob/master/examples/segment_tree.point_set_range_composite.test.cpp">View this file on GitHub</a>
    - Last commit date: 2019-12-09 18:30:56 +0900


* see: <a href="https://judge.yosupo.jp/problem/point_set_range_composite">https://judge.yosupo.jp/problem/point_set_range_composite</a>


## Depends On
* :heavy_check_mark: <a href="../../library/examples/macros.hpp.html">examples/macros.hpp</a>
* :heavy_check_mark: <a href="../../library/examples/segment_tree.hpp.html">a Segment Tree (generalized with monoids)</a>


## Code
{% raw %}
```cpp
#define PROBLEM "https://judge.yosupo.jp/problem/point_set_range_composite"
#include <cstdint>
#include <iostream>
#include <tuple>
#include <utility>
#include "examples/segment_tree.hpp"
#include "examples/macros.hpp"
using namespace std;

template <int32_t MOD>
struct linear_function_monoid {
    typedef pair<int64_t, int64_t> value_type;
    value_type unit() const {
        return make_pair(1, 0);
    }
    value_type mult(value_type g, value_type f) const {
        int64_t a = (f.first * g.first) % MOD;
        int64_t b = (f.first * g.second + f.second) % MOD;
        return make_pair(a, b);
    }
};

constexpr int32_t MOD = 998244353;
int main() {
    int n, q; cin >> n >> q;
    segment_tree<linear_function_monoid<MOD> > segtree(n);
    REP (i, n) {
        int64_t a, b; cin >> a >> b;
        segtree.point_set(i, make_pair(a, b));
    }
    REP (i, q) {
        int f, x, y, z; cin >> f >> x >> y >> z;
        if (f == 0) {
            segtree.point_set(x, make_pair(y, z));
        } else if (f == 1) {
            int64_t a, b; tie(a, b) = segtree.range_concat(x, y);
            cout << (a * z + b) % MOD << endl;
        }
    }
    return 0;
}

```
{% endraw %}

<a href="../../index.html">Back to top page</a>

