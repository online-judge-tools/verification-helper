---
data:
  _extendedDependsOn:
  - icon: ':heavy_check_mark:'
    path: examples/nim/union_find_tree.nim
    title: examples/nim/union_find_tree.nim
  - icon: ':heavy_check_mark:'
    path: examples/nim/hoge.nim
    title: examples/nim/hoge.nim
  - icon: ':heavy_check_mark:'
    path: examples/nim/headers.nim
    title: examples/nim/headers.nim
  - icon: ':heavy_check_mark:'
    path: examples/nim/union_find_tree.nim
    title: examples/nim/union_find_tree.nim
  - icon: ':heavy_check_mark:'
    path: examples/nim/hoge.nim
    title: examples/nim/hoge.nim
  - icon: ':heavy_check_mark:'
    path: examples/nim/headers.nim
    title: examples/nim/headers.nim
  _extendedRequiredBy: []
  _extendedVerifiedWith: []
  _pathExtension: nim
  _verificationStatusIcon: ':heavy_check_mark:'
  attributes:
    PROBLEM: https://onlinejudge.u-aizu.ac.jp/courses/library/3/DSL/all/DSL_1_A
    links:
    - https://onlinejudge.u-aizu.ac.jp/courses/library/3/DSL/all/DSL_1_A
  bundledCode: "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/documentation/build.py\"\
    , line 70, in _render_source_code_stat\n    bundled_code = language.bundle(stat.path,\
    \ basedir=basedir).decode()\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/languages/nim.py\"\
    , line 86, in bundle\n    raise NotImplementedError\nNotImplementedError\n"
  code: "# verification-helper: PROBLEM https://onlinejudge.u-aizu.ac.jp/courses/library/3/DSL/all/DSL_1_A\n\
    \ninclude \"examples/nim/headers.nim\"\nimport \"examples/nim/union_find_tree.nim\"\
    \ except hoge\ninclude \"examples/nim/union_find_tree.nim\"\ninclude \"examples/nim/union_find_tree.nim\"\
    \ninclude \"examples/nim/union_find_tree.nim\"\ninclude \"examples/nim/union_find_tree.nim\"\
    \n\nlet\n  n, q = nextInt()\nvar uft = initUnionFindTree(n)\nfor i in 0..<q:\n\
    \  let com, x, y = nextInt()\n  if com == 0:\n    uft.unite_trees(x, y)\n  elif\
    \ com == 1:\n    echo if uft.is_same(x, y): 1 else: 0\n"
  dependsOn:
  - examples/nim/union_find_tree.nim
  - examples/nim/hoge.nim
  - examples/nim/headers.nim
  - examples/nim/union_find_tree.nim
  - examples/nim/hoge.nim
  - examples/nim/headers.nim
  isVerificationFile: true
  path: examples/nim/union_find_tree_aoj_test.nim
  requiredBy: []
  timestamp: '2020-09-17 18:25:50+09:00'
  verificationStatus: TEST_ACCEPTED
  verifiedWith: []
documentation_of: examples/nim/union_find_tree_aoj_test.nim
layout: document
redirect_from:
- /verify/examples/nim/union_find_tree_aoj_test.nim
- /verify/examples/nim/union_find_tree_aoj_test.nim.html
title: examples/nim/union_find_tree_aoj_test.nim
---
