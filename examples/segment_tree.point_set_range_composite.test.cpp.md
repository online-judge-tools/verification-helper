---
data:
  _extendedDependsOn:
  - icon: ':heavy_check_mark:'
    path: examples/macros.hpp
    title: examples/macros.hpp
  - icon: ':heavy_check_mark:'
    path: examples/segment_tree.hpp
    title: Segment Tree (generalized with monoids)
  _extendedRequiredBy: []
  _extendedVerifiedWith: []
  _isVerificationFailed: false
  _pathExtension: cpp
  _verificationStatusIcon: ':heavy_check_mark:'
  attributes:
    '*NOT_SPECIAL_COMMENTS*': ''
    PROBLEM: https://judge.yosupo.jp/problem/point_set_range_composite
    links:
    - https://judge.yosupo.jp/problem/point_set_range_composite
  bundledCode: "#line 1 \"examples/segment_tree.point_set_range_composite.test.cpp\"\
    \n#define PROBLEM \"https://judge.yosupo.jp/problem/point_set_range_composite\"\
    \n#include <cstdint>\n#include <iostream>\n#include <tuple>\n#include <utility>\n\
    #line 2 \"examples/segment_tree.hpp\"\n#include <cassert>\n#include <vector>\n\
    \n/**\n * @brief a Segment Tree (generalized with monoids) \n * @tparam Monoid\
    \ is a monoid; commutativity is not required\n * @see https://en.wikipedia.org/wiki/Segment_tree\n\
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
    \ racc);\n    }\n};\n#line 2 \"examples/macros.hpp\"\n#define REP(i, n) for (int\
    \ i = 0; (i) < (int)(n); ++ (i))\n#define REP3(i, m, n) for (int i = (m); (i)\
    \ < (int)(n); ++ (i))\n#define REP_R(i, n) for (int i = (int)(n) - 1; (i) >= 0;\
    \ -- (i))\n#define REP3R(i, m, n) for (int i = (int)(n) - 1; (i) >= (int)(m);\
    \ -- (i))\n#define ALL(x) begin(x), end(x)\n#line 8 \"examples/segment_tree.point_set_range_composite.test.cpp\"\
    \nusing namespace std;\n\ntemplate <int32_t MOD>\nstruct linear_function_monoid\
    \ {\n    typedef pair<int64_t, int64_t> value_type;\n    value_type unit() const\
    \ {\n        return make_pair(1, 0);\n    }\n    value_type mult(value_type g,\
    \ value_type f) const {\n        int64_t a = (f.first * g.first) % MOD;\n    \
    \    int64_t b = (f.first * g.second + f.second) % MOD;\n        return make_pair(a,\
    \ b);\n    }\n};\n\nconstexpr int32_t MOD = 998244353;\nint main() {\n    int\
    \ n, q; cin >> n >> q;\n    segment_tree<linear_function_monoid<MOD> > segtree(n);\n\
    \    REP (i, n) {\n        int64_t a, b; cin >> a >> b;\n        segtree.point_set(i,\
    \ make_pair(a, b));\n    }\n    REP (i, q) {\n        int f, x, y, z; cin >> f\
    \ >> x >> y >> z;\n        if (f == 0) {\n            segtree.point_set(x, make_pair(y,\
    \ z));\n        } else if (f == 1) {\n            int64_t a, b; tie(a, b) = segtree.range_concat(x,\
    \ y);\n            cout << (a * z + b) % MOD << endl;\n        }\n    }\n    return\
    \ 0;\n}\n"
  code: "#define PROBLEM \"https://judge.yosupo.jp/problem/point_set_range_composite\"\
    \n#include <cstdint>\n#include <iostream>\n#include <tuple>\n#include <utility>\n\
    #include \"examples/segment_tree.hpp\"\n#include \"examples/macros.hpp\"\nusing\
    \ namespace std;\n\ntemplate <int32_t MOD>\nstruct linear_function_monoid {\n\
    \    typedef pair<int64_t, int64_t> value_type;\n    value_type unit() const {\n\
    \        return make_pair(1, 0);\n    }\n    value_type mult(value_type g, value_type\
    \ f) const {\n        int64_t a = (f.first * g.first) % MOD;\n        int64_t\
    \ b = (f.first * g.second + f.second) % MOD;\n        return make_pair(a, b);\n\
    \    }\n};\n\nconstexpr int32_t MOD = 998244353;\nint main() {\n    int n, q;\
    \ cin >> n >> q;\n    segment_tree<linear_function_monoid<MOD> > segtree(n);\n\
    \    REP (i, n) {\n        int64_t a, b; cin >> a >> b;\n        segtree.point_set(i,\
    \ make_pair(a, b));\n    }\n    REP (i, q) {\n        int f, x, y, z; cin >> f\
    \ >> x >> y >> z;\n        if (f == 0) {\n            segtree.point_set(x, make_pair(y,\
    \ z));\n        } else if (f == 1) {\n            int64_t a, b; tie(a, b) = segtree.range_concat(x,\
    \ y);\n            cout << (a * z + b) % MOD << endl;\n        }\n    }\n    return\
    \ 0;\n}\n"
  dependsOn:
  - examples/segment_tree.hpp
  - examples/macros.hpp
  isVerificationFile: true
  path: examples/segment_tree.point_set_range_composite.test.cpp
  requiredBy: []
  timestamp: '2020-09-14 23:28:24+09:00'
  verificationStatus: TEST_ACCEPTED
  verifiedWith: []
documentation_of: examples/segment_tree.point_set_range_composite.test.cpp
layout: document
redirect_from:
- /verify/examples/segment_tree.point_set_range_composite.test.cpp
- /verify/examples/segment_tree.point_set_range_composite.test.cpp.html
title: examples/segment_tree.point_set_range_composite.test.cpp
---
