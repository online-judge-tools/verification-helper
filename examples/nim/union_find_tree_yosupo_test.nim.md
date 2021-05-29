---
data:
  _extendedDependsOn:
  - icon: ':heavy_check_mark:'
    path: examples/nim/headers.nim
    title: examples/nim/headers.nim
  - icon: ':heavy_check_mark:'
    path: examples/nim/headers.nim
    title: examples/nim/headers.nim
  _extendedRequiredBy: []
  _extendedVerifiedWith: []
  _isVerificationFailed: false
  _pathExtension: nim
  _verificationStatusIcon: ':heavy_check_mark:'
  attributes:
    PROBLEM: https://judge.yosupo.jp/problem/unionfind
    links:
    - https://judge.yosupo.jp/problem/unionfind
  bundledCode: "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.9.5/x64/lib/python3.9/site-packages/onlinejudge_verify/documentation/build.py\"\
    , line 71, in _render_source_code_stat\n    bundled_code = language.bundle(stat.path,\
    \ basedir=basedir, options={'include_paths': [basedir]}).decode()\n  File \"/opt/hostedtoolcache/Python/3.9.5/x64/lib/python3.9/site-packages/onlinejudge_verify/languages/nim.py\"\
    , line 86, in bundle\n    raise NotImplementedError\nNotImplementedError\n"
  code: "# verification-helper: PROBLEM https://judge.yosupo.jp/problem/unionfind\n\
    \ninclude \"examples/nim/headers.nim\"\nfrom examples/nim/union_find_tree import\
    \ unite_trees, initUnionFindTree, is_same\n\nlet \n  n,q = nextInt()\nvar uft\
    \ = initUnionFindTree(n)\n\nfor i in 0..<q:\n  let t, u, v = nextInt()\n  if t\
    \ == 0:\n    uft.unite_trees(u, v)\n  elif t == 1:\n    echo if uft.is_same(u,\
    \ v): 1 else: 0\n"
  dependsOn:
  - examples/nim/headers.nim
  - examples/nim/headers.nim
  isVerificationFile: true
  path: examples/nim/union_find_tree_yosupo_test.nim
  requiredBy: []
  timestamp: '2020-09-17 18:25:50+09:00'
  verificationStatus: TEST_ACCEPTED
  verifiedWith: []
documentation_of: examples/nim/union_find_tree_yosupo_test.nim
layout: document
redirect_from:
- /verify/examples/nim/union_find_tree_yosupo_test.nim
- /verify/examples/nim/union_find_tree_yosupo_test.nim.html
title: examples/nim/union_find_tree_yosupo_test.nim
---
