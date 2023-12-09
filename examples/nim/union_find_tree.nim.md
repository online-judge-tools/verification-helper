---
data:
  _extendedDependsOn:
  - icon: ':heavy_check_mark:'
    path: examples/nim/hoge.nim
    title: examples/nim/hoge.nim
  - icon: ':heavy_check_mark:'
    path: examples/nim/hoge.nim
    title: examples/nim/hoge.nim
  _extendedRequiredBy: []
  _extendedVerifiedWith:
  - icon: ':heavy_check_mark:'
    path: examples/nim/union_find_tree_aoj_test.nim
    title: examples/nim/union_find_tree_aoj_test.nim
  - icon: ':heavy_check_mark:'
    path: examples/nim/union_find_tree_aoj_test.nim
    title: examples/nim/union_find_tree_aoj_test.nim
  _isVerificationFailed: false
  _pathExtension: nim
  _verificationStatusIcon: ':heavy_check_mark:'
  attributes:
    links: []
  bundledCode: "Traceback (most recent call last):\n  File \"/home/runner/.local/lib/python3.10/site-packages/onlinejudge_verify/documentation/build.py\"\
    , line 71, in _render_source_code_stat\n    bundled_code = language.bundle(stat.path,\
    \ basedir=basedir, options={'include_paths': [basedir]}).decode()\n  File \"/home/runner/.local/lib/python3.10/site-packages/onlinejudge_verify/languages/nim.py\"\
    , line 86, in bundle\n    raise NotImplementedError\nNotImplementedError\n"
  code: "when not declared(EXAMPLES_UNION_FIND_TREE_NIM):\n  const EXAMPLES_UNION_FIND_TREE_NIM\
    \ = true\n  import sequtils\n  import \"examples/nim/hoge.nim\"\n  \n  # @brief\
    \ a Union-Find Tree\n  # @note most operations in $O(\\alpha(n))$ where $\\alpha(n)$\
    \ is the inverse of Ackermann function\n  # @note implemented with union-by-size\
    \ + path-compression\n  \n  type UnionFindTree = object\n    data:seq[int]\n \
    \ \n  proc initUnionFindTree*(n:int):UnionFindTree = UnionFindTree(data:newSeqWith(n,\
    \ -1))\n  \n  proc isRoot*(self: UnionFindTree, i:int):bool = return self.data[i]\
    \ < 0\n  proc findRoot*(self: var UnionFindTree, i:int):int =\n    if self.is_root(i):\n\
    \      return i\n    else:\n      self.data[i] = self.findRoot(self.data[i])\n\
    \      return self.data[i]\n  proc treeSize*(self: var UnionFindTree, i:int):int\
    \ = - self.data[self.findRoot(i)]\n  proc uniteTrees*(self: var UnionFindTree,\
    \ i, j:int):int {.discardable.} =\n    var \n      i = self.findRoot(i)\n    \
    \  j = self.findRoot(j)\n    if i != j:\n      if self.tree_size(i) < self.tree_size(j):\
    \ swap(i, j)\n      self.data[i] += self.data[j]\n      self.data[j] = i\n   \
    \ return i\n  \n  proc isSame*(self: var UnionFindTree, i, j:int):bool = self.find_root(i)\
    \ == self.find_root(j)\n\n  proc hoge*() = echo \"Hello World\"\n"
  dependsOn:
  - examples/nim/hoge.nim
  - examples/nim/hoge.nim
  isVerificationFile: false
  path: examples/nim/union_find_tree.nim
  requiredBy: []
  timestamp: '2023-12-09 20:36:27+09:00'
  verificationStatus: LIBRARY_ALL_AC
  verifiedWith:
  - examples/nim/union_find_tree_aoj_test.nim
  - examples/nim/union_find_tree_aoj_test.nim
documentation_of: examples/nim/union_find_tree.nim
layout: document
redirect_from:
- /library/examples/nim/union_find_tree.nim
- /library/examples/nim/union_find_tree.nim.html
title: examples/nim/union_find_tree.nim
---
