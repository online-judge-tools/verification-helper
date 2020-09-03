---
data:
  attributes:
    PROBLEM: https://judge.yosupo.jp/problem/unionfind
  bundledCode: "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/documentation/build.py\"\
    , line 58, in _render_source_code_stat\n    bundled_code = language.bundle(stat.path,\
    \ basedir=basedir).decode()\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/languages/nim.py\"\
    , line 86, in bundle\n    raise NotImplementedError\nNotImplementedError\n"
  code: "# verify-helper: PROBLEM https://judge.yosupo.jp/problem/unionfind\n\ninclude\
    \ \"examples/nim/headers.nim\"\nfrom examples/nim/union_find_tree import unite_trees,\
    \ initUnionFindTree, is_same\n\nlet \n  n,q = nextInt()\nvar uft = initUnionFindTree(n)\n\
    \nfor i in 0..<q:\n  let t, u, v = nextInt()\n  if t == 0:\n    uft.unite_trees(u,\
    \ v)\n  elif t == 1:\n    echo if uft.is_same(u, v): 1 else: 0\n"
  dependsOn:
  - examples/nim/headers.nim
  - examples/nim/headers.nim
  extendedDependsOn:
  - icon: ':warning:'
    path: examples/nim/headers.nim
    title: examples/nim/headers.nim
  - icon: ':warning:'
    path: examples/nim/headers.nim
    title: examples/nim/headers.nim
  extendedRequiredBy: []
  extendedVerifiedWith: []
  isVerificationFile: true
  path: examples/nim/union_find_tree_yosupo_test.nim
  requiredBy: []
  timestamp: '2020-05-05 19:19:11+09:00'
  verificationStatus: TEST_ACCEPTED
  verificationStatusIcon: ':heavy_check_mark:'
  verifiedWith: []
documentation_of: examples/nim/union_find_tree_yosupo_test.nim
layout: document
redirect_from:
- /verify/examples/nim/union_find_tree_yosupo_test.nim
- /verify/examples/nim/union_find_tree_yosupo_test.nim.html
title: examples/nim/union_find_tree_yosupo_test.nim
---
