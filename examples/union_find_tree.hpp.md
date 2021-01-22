---
data:
  _extendedDependsOn: []
  _extendedRequiredBy: []
  _extendedVerifiedWith:
  - icon: ':heavy_check_mark:'
    path: examples/union_find_tree.aoj.test.cpp
    title: examples/union_find_tree.aoj.test.cpp
  - icon: ':heavy_check_mark:'
    path: examples/union_find_tree.yosupo.test.cpp
    title: examples/union_find_tree.yosupo.test.cpp
  _isVerificationFailed: false
  _pathExtension: hpp
  _verificationStatusIcon: ':heavy_check_mark:'
  attributes:
    document_title: a Union-Find Tree
    links: []
  bundledCode: "#line 1 \"examples/union_find_tree.hpp\"\n\n\n#include <algorithm>\n\
    #include <vector>\n\n/**\n * @brief a Union-Find Tree\n * @note most operations\
    \ in $O(\\alpha(n))$ where $\\alpha(n)$ is the inverse of Ackermann function\n\
    \ * @note implemented with union-by-size + path-compression\n */\nstruct union_find_tree\
    \ {\n    std::vector<int> data;\n    union_find_tree() = default;\n    explicit\
    \ union_find_tree(int n) : data(n, -1) {}\n    bool is_root(int i) { return data[i]\
    \ < 0; }\n    int find_root(int i) { return is_root(i) ? i : (data[i] = find_root(data[i]));\
    \ }\n    int tree_size(int i) { return - data[find_root(i)]; }\n    int unite_trees(int\
    \ i, int j) {\n        i = find_root(i); j = find_root(j);\n        if (i != j)\
    \ {\n            if (tree_size(i) < tree_size(j)) std::swap(i, j);\n         \
    \   data[i] += data[j];\n            data[j] = i;\n        }\n        return i;\n\
    \    }\n    bool is_same(int i, int j) { return find_root(i) == find_root(j);\
    \ }\n};\n\n\n"
  code: "#ifndef EXAMPLES_UNION_FIND_TREE_HPP\n#define EXAMPLES_UNION_FIND_TREE_HPP\n\
    #include <algorithm>\n#include <vector>\n\n/**\n * @brief a Union-Find Tree\n\
    \ * @note most operations in $O(\\alpha(n))$ where $\\alpha(n)$ is the inverse\
    \ of Ackermann function\n * @note implemented with union-by-size + path-compression\n\
    \ */\nstruct union_find_tree {\n    std::vector<int> data;\n    union_find_tree()\
    \ = default;\n    explicit union_find_tree(int n) : data(n, -1) {}\n    bool is_root(int\
    \ i) { return data[i] < 0; }\n    int find_root(int i) { return is_root(i) ? i\
    \ : (data[i] = find_root(data[i])); }\n    int tree_size(int i) { return - data[find_root(i)];\
    \ }\n    int unite_trees(int i, int j) {\n        i = find_root(i); j = find_root(j);\n\
    \        if (i != j) {\n            if (tree_size(i) < tree_size(j)) std::swap(i,\
    \ j);\n            data[i] += data[j];\n            data[j] = i;\n        }\n\
    \        return i;\n    }\n    bool is_same(int i, int j) { return find_root(i)\
    \ == find_root(j); }\n};\n\n#endif\n"
  dependsOn: []
  isVerificationFile: false
  path: examples/union_find_tree.hpp
  requiredBy: []
  timestamp: '2019-12-16 05:18:36+09:00'
  verificationStatus: LIBRARY_ALL_AC
  verifiedWith:
  - examples/union_find_tree.yosupo.test.cpp
  - examples/union_find_tree.aoj.test.cpp
documentation_of: examples/union_find_tree.hpp
layout: document
redirect_from:
- /library/examples/union_find_tree.hpp
- /library/examples/union_find_tree.hpp.html
title: a Union-Find Tree
---
