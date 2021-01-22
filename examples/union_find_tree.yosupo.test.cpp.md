---
data:
  _extendedDependsOn:
  - icon: ':heavy_check_mark:'
    path: examples/macros.hpp
    title: examples/macros.hpp
  - icon: ':heavy_check_mark:'
    path: examples/union_find_tree.hpp
    title: a Union-Find Tree
  _extendedRequiredBy: []
  _extendedVerifiedWith: []
  _isVerificationFailed: false
  _pathExtension: cpp
  _verificationStatusIcon: ':heavy_check_mark:'
  attributes:
    '*NOT_SPECIAL_COMMENTS*': ''
    PROBLEM: https://judge.yosupo.jp/problem/unionfind
    links:
    - https://judge.yosupo.jp/problem/unionfind
  bundledCode: "#line 1 \"examples/union_find_tree.yosupo.test.cpp\"\n#define PROBLEM\
    \ \"https://judge.yosupo.jp/problem/unionfind\"\n#include <iostream>\n#line 1\
    \ \"examples/union_find_tree.hpp\"\n\n\n#include <algorithm>\n#include <vector>\n\
    \n/**\n * @brief a Union-Find Tree\n * @note most operations in $O(\\alpha(n))$\
    \ where $\\alpha(n)$ is the inverse of Ackermann function\n * @note implemented\
    \ with union-by-size + path-compression\n */\nstruct union_find_tree {\n    std::vector<int>\
    \ data;\n    union_find_tree() = default;\n    explicit union_find_tree(int n)\
    \ : data(n, -1) {}\n    bool is_root(int i) { return data[i] < 0; }\n    int find_root(int\
    \ i) { return is_root(i) ? i : (data[i] = find_root(data[i])); }\n    int tree_size(int\
    \ i) { return - data[find_root(i)]; }\n    int unite_trees(int i, int j) {\n \
    \       i = find_root(i); j = find_root(j);\n        if (i != j) {\n         \
    \   if (tree_size(i) < tree_size(j)) std::swap(i, j);\n            data[i] +=\
    \ data[j];\n            data[j] = i;\n        }\n        return i;\n    }\n  \
    \  bool is_same(int i, int j) { return find_root(i) == find_root(j); }\n};\n\n\
    \n#line 2 \"examples/macros.hpp\"\n#define REP(i, n) for (int i = 0; (i) < (int)(n);\
    \ ++ (i))\n#define REP3(i, m, n) for (int i = (m); (i) < (int)(n); ++ (i))\n#define\
    \ REP_R(i, n) for (int i = (int)(n) - 1; (i) >= 0; -- (i))\n#define REP3R(i, m,\
    \ n) for (int i = (int)(n) - 1; (i) >= (int)(m); -- (i))\n#define ALL(x) begin(x),\
    \ end(x)\n#line 5 \"examples/union_find_tree.yosupo.test.cpp\"\nusing namespace\
    \ std;\n\nint main() {\n    int n, q; cin >> n >> q;\n    union_find_tree uft(n);\n\
    \    REP (i, q) {\n        int t, u, v; cin >> t >> u >> v;\n        if (t ==\
    \ 0) {\n            uft.unite_trees(u, v);\n        } else if (t == 1) {\n   \
    \         cout << uft.is_same(u, v) << endl;\n        }\n    }\n    return 0;\n\
    }\n"
  code: "#define PROBLEM \"https://judge.yosupo.jp/problem/unionfind\"\n#include <iostream>\n\
    #include \"examples/union_find_tree.hpp\"\n#include \"examples/macros.hpp\"\n\
    using namespace std;\n\nint main() {\n    int n, q; cin >> n >> q;\n    union_find_tree\
    \ uft(n);\n    REP (i, q) {\n        int t, u, v; cin >> t >> u >> v;\n      \
    \  if (t == 0) {\n            uft.unite_trees(u, v);\n        } else if (t ==\
    \ 1) {\n            cout << uft.is_same(u, v) << endl;\n        }\n    }\n   \
    \ return 0;\n}\n"
  dependsOn:
  - examples/union_find_tree.hpp
  - examples/macros.hpp
  isVerificationFile: true
  path: examples/union_find_tree.yosupo.test.cpp
  requiredBy: []
  timestamp: '2019-12-16 05:18:36+09:00'
  verificationStatus: TEST_ACCEPTED
  verifiedWith: []
documentation_of: examples/union_find_tree.yosupo.test.cpp
layout: document
redirect_from:
- /verify/examples/union_find_tree.yosupo.test.cpp
- /verify/examples/union_find_tree.yosupo.test.cpp.html
title: examples/union_find_tree.yosupo.test.cpp
---
