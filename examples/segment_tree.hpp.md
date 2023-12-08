---
data:
  _extendedDependsOn: []
  _extendedRequiredBy: []
  _extendedVerifiedWith:
  - icon: ':heavy_check_mark:'
    path: examples/segment_tree.point_set_range_composite.test.cpp
    title: examples/segment_tree.point_set_range_composite.test.cpp
  - icon: ':heavy_check_mark:'
    path: examples/segment_tree.range_minimum_query.test.cpp
    title: examples/segment_tree.range_minimum_query.test.cpp
  - icon: ':heavy_check_mark:'
    path: examples/segment_tree.range_sum_query.test.cpp
    title: examples/segment_tree.range_sum_query.test.cpp
  _isVerificationFailed: false
  _pathExtension: hpp
  _verificationStatusIcon: ':heavy_check_mark:'
  attributes:
    document_title: a Segment Tree (generalized with monoids)
    links:
    - https://en.wikipedia.org/wiki/Segment_tree
  bundledCode: "#line 2 \"examples/segment_tree.hpp\"\n#include <cassert>\n#include\
    \ <vector>\n\n/**\n * @brief a Segment Tree (generalized with monoids) \n * @tparam\
    \ Monoid is a monoid; commutativity is not required\n * @see https://en.wikipedia.org/wiki/Segment_tree\n\
    \ */\ntemplate <class Monoid>\nstruct segment_tree {\n    typedef typename Monoid::value_type\
    \ value_type;\n    const Monoid mon;\n    int n;\n    std::vector<value_type>\
    \ a;\n\n    segment_tree() = default;\n    segment_tree(int n_, const Monoid &\
    \ mon_ = Monoid()) : mon(mon_) {\n        n = 1; while (n < n_) n *= 2;\n    \
    \    a.resize(2 * n - 1, mon.unit());\n    }\n\n    /**\n     * @brief set $a_i$\
    \ as b in $O(\\log n)$\n     * @arg i is 0-based\n     */\n    void point_set(int\
    \ i, value_type b) {\n        assert (0 <= i and i < n);\n        a[i + n - 1]\
    \ = b;\n        for (i = (i + n) / 2; i > 0; i /= 2) {  // 1-based\n         \
    \   a[i - 1] = mon.mult(a[2 * i - 1], a[2 * i]);\n        }\n    }\n\n    /**\n\
    \     * @brief compute $a_l \\cdot a _ {l + 1} \\cdot ... \\cdot a _ {r - 1}$\
    \ in $O(\\log n)$\n     * @arg l, r are 0-based\n     */\n    value_type range_concat(int\
    \ l, int r) {\n        assert (0 <= l and l <= r and r <= n);\n        value_type\
    \ lacc = mon.unit(), racc = mon.unit();\n        for (l += n, r += n; l < r; l\
    \ /= 2, r /= 2) {  // 1-based loop, 2x faster than recursion\n            if (l\
    \ % 2 == 1) lacc = mon.mult(lacc, a[(l ++) - 1]);\n            if (r % 2 == 1)\
    \ racc = mon.mult(a[(-- r) - 1], racc);\n        }\n        return mon.mult(lacc,\
    \ racc);\n    }\n};\n"
  code: "#pragma once\n#include <cassert>\n#include <vector>\n\n/**\n * @brief a Segment\
    \ Tree (generalized with monoids) \n * @tparam Monoid is a monoid; commutativity\
    \ is not required\n * @see https://en.wikipedia.org/wiki/Segment_tree\n */\ntemplate\
    \ <class Monoid>\nstruct segment_tree {\n    typedef typename Monoid::value_type\
    \ value_type;\n    const Monoid mon;\n    int n;\n    std::vector<value_type>\
    \ a;\n\n    segment_tree() = default;\n    segment_tree(int n_, const Monoid &\
    \ mon_ = Monoid()) : mon(mon_) {\n        n = 1; while (n < n_) n *= 2;\n    \
    \    a.resize(2 * n - 1, mon.unit());\n    }\n\n    /**\n     * @brief set $a_i$\
    \ as b in $O(\\log n)$\n     * @arg i is 0-based\n     */\n    void point_set(int\
    \ i, value_type b) {\n        assert (0 <= i and i < n);\n        a[i + n - 1]\
    \ = b;\n        for (i = (i + n) / 2; i > 0; i /= 2) {  // 1-based\n         \
    \   a[i - 1] = mon.mult(a[2 * i - 1], a[2 * i]);\n        }\n    }\n\n    /**\n\
    \     * @brief compute $a_l \\cdot a _ {l + 1} \\cdot ... \\cdot a _ {r - 1}$\
    \ in $O(\\log n)$\n     * @arg l, r are 0-based\n     */\n    value_type range_concat(int\
    \ l, int r) {\n        assert (0 <= l and l <= r and r <= n);\n        value_type\
    \ lacc = mon.unit(), racc = mon.unit();\n        for (l += n, r += n; l < r; l\
    \ /= 2, r /= 2) {  // 1-based loop, 2x faster than recursion\n            if (l\
    \ % 2 == 1) lacc = mon.mult(lacc, a[(l ++) - 1]);\n            if (r % 2 == 1)\
    \ racc = mon.mult(a[(-- r) - 1], racc);\n        }\n        return mon.mult(lacc,\
    \ racc);\n    }\n};\n"
  dependsOn: []
  isVerificationFile: false
  path: examples/segment_tree.hpp
  requiredBy: []
  timestamp: '2023-12-08 11:36:08+09:00'
  verificationStatus: LIBRARY_ALL_AC
  verifiedWith:
  - examples/segment_tree.range_sum_query.test.cpp
  - examples/segment_tree.range_minimum_query.test.cpp
  - examples/segment_tree.point_set_range_composite.test.cpp
documentation_of: examples/segment_tree.hpp
layout: document
title: Segment Tree (generalized with monoids)
---

## Operations

For a monoid $M = (M, \cdot, 1)$ and a list $a = (a_0, a_1, \dots, a _ {n - 1}) \in M^N$ of elements $M$ with the length $N$, a segment tree can process following operations with $O(\log N)$:

-   $\mathtt{point\unicode{95}set}(i, b)$: Update $a_i \gets b$
-   $\mathtt{range\unicode{95}get}(l, r)$: Calculate the product $a_l \cdot a _ {l + 1} \cdot \dots \cdot a _ {r - 1}$
