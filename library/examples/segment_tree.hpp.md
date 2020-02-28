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


# :heavy_check_mark: a Segment Tree (generalized with monoids) <small>(examples/segment_tree.hpp)</small>

<a href="../../index.html">Back to top page</a>

* category: <a href="../../index.html#bfebe34154a0dfd9fc7b447fc9ed74e9">examples</a>
* <a href="{{ site.github.repository_url }}/blob/master/examples/segment_tree.hpp">View this file on GitHub</a>
    - Last commit date: 2020-02-28 16:00:02+09:00


* see: <a href="https://en.wikipedia.org/wiki/Segment_tree">https://en.wikipedia.org/wiki/Segment_tree</a>


## Operations

For a monoid $M = (M, \cdot, 1)$ and a list $a = (a_0, a_1, \dots, a _ {n - 1}) \in M^N$ of elements $M$ with the length $N$, a segment tree can process following operations with $O(\log N)$:

-   $\mathtt{point\unicode{95}set}(i, b)$: Update $a_i \gets b$
-   $\mathtt{range\unicode{95}get}(l, r)$: Calculate the product $a_l \cdot a _ {l + 1} \cdot \dots \cdot a _ {r - 1}$


## Verified with

* :heavy_check_mark: <a href="../../verify/examples/segment_tree.point_set_range_composite.test.cpp.html">examples/segment_tree.point_set_range_composite.test.cpp</a>
* :heavy_check_mark: <a href="../../verify/examples/segment_tree.range_minimum_query.test.cpp.html">examples/segment_tree.range_minimum_query.test.cpp</a>
* :heavy_check_mark: <a href="../../verify/examples/segment_tree.range_sum_query.test.cpp.html">examples/segment_tree.range_sum_query.test.cpp</a>


## Code

<a id="unbundled"></a>
{% raw %}
```cpp
#pragma once
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

```
{% endraw %}

<a id="bundled"></a>
{% raw %}
```cpp
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

```
{% endraw %}

<a href="../../index.html">Back to top page</a>

