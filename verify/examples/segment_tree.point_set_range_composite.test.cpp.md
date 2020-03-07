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

* category: <a href="../../index.html#bfebe34154a0dfd9fc7b447fc9ed74e9">examples</a>
* <a href="{{ site.github.repository_url }}/blob/master/examples/segment_tree.point_set_range_composite.test.cpp">View this file on GitHub</a>
    - Last commit date: 2020-02-28 16:00:02+09:00


* see: <a href="https://judge.yosupo.jp/problem/point_set_range_composite">https://judge.yosupo.jp/problem/point_set_range_composite</a>


## Depends on

* :heavy_check_mark: <a href="../../library/examples/macros.hpp.html">examples/macros.hpp</a>
* :heavy_check_mark: <a href="../../library/examples/segment_tree.hpp.html">a Segment Tree (generalized with monoids) <small>(examples/segment_tree.hpp)</small></a>


## Code

<a id="unbundled"></a>
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

<a id="bundled"></a>
{% raw %}
```cpp
#line 1 "examples/segment_tree.point_set_range_composite.test.cpp"
#define PROBLEM "https://judge.yosupo.jp/problem/point_set_range_composite"
#include <cstdint>
#include <iostream>
#include <tuple>
#include <utility>
#line 2 "examples/segment_tree.hpp"
#include <cassert>
#include <vector>

/**
 * @brief a Segment Tree (generalized with monoids) 
 * @docs examples/segment_tree.md
 * @tparam Monoid is a monoid; commutativity is not required
 * @see https://en.wikipedia.org/wiki/Segment_tree
 */
template <class Monoid>
struct segment_tree {
    typedef typename Monoid::value_type value_type;
    const Monoid mon;
    int n;
    std::vector<value_type> a;

    segment_tree() = default;
    segment_tree(int n_, const Monoid & mon_ = Monoid()) : mon(mon_) {
        n = 1; while (n < n_) n *= 2;
        a.resize(2 * n - 1, mon.unit());
    }

    /**
     * @brief set $a_i$ as b in $O(\log n)$
     * @arg i is 0-based
     */
    void point_set(int i, value_type b) {
        assert (0 <= i and i < n);
        a[i + n - 1] = b;
        for (i = (i + n) / 2; i > 0; i /= 2) {  // 1-based
            a[i - 1] = mon.mult(a[2 * i - 1], a[2 * i]);
        }
    }

    /**
     * @brief compute $a_l \cdot a _ {l + 1} \cdot ... \cdot a _ {r - 1}$ in $O(\log n)$
     * @arg l, r are 0-based
     */
    value_type range_concat(int l, int r) {
        assert (0 <= l and l <= r and r <= n);
        value_type lacc = mon.unit(), racc = mon.unit();
        for (l += n, r += n; l < r; l /= 2, r /= 2) {  // 1-based loop, 2x faster than recursion
            if (l % 2 == 1) lacc = mon.mult(lacc, a[(l ++) - 1]);
            if (r % 2 == 1) racc = mon.mult(a[(-- r) - 1], racc);
        }
        return mon.mult(lacc, racc);
    }
};
#line 2 "examples/macros.hpp"
#define REP(i, n) for (int i = 0; (i) < (int)(n); ++ (i))
#define REP3(i, m, n) for (int i = (m); (i) < (int)(n); ++ (i))
#define REP_R(i, n) for (int i = (int)(n) - 1; (i) >= 0; -- (i))
#define REP3R(i, m, n) for (int i = (int)(n) - 1; (i) >= (int)(m); -- (i))
#define ALL(x) begin(x), end(x)
#line 8 "examples/segment_tree.point_set_range_composite.test.cpp"
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

