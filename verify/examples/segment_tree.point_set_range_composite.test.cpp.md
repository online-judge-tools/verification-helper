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


[Back to top page](../../index.html)

* see: [https://judge.yosupo.jp/problem/point_set_range_composite](https://judge.yosupo.jp/problem/point_set_range_composite)


## Dependencies
* :heavy_check_mark: [examples/macros.hpp](../../library/examples/macros.hpp.html)
* :heavy_check_mark: [a segment tree](../../library/examples/segment_tree.hpp.html)


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

[Back to top page](../../index.html)

