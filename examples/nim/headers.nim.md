---
data:
  _extendedDependsOn: []
  _extendedRequiredBy: []
  _extendedVerifiedWith:
  - icon: ':heavy_check_mark:'
    path: examples/nim/union_find_tree_aoj_test.nim
    title: examples/nim/union_find_tree_aoj_test.nim
  - icon: ':heavy_check_mark:'
    path: examples/nim/union_find_tree_aoj_test.nim
    title: examples/nim/union_find_tree_aoj_test.nim
  - icon: ':heavy_check_mark:'
    path: examples/nim/union_find_tree_yosupo_test.nim
    title: examples/nim/union_find_tree_yosupo_test.nim
  - icon: ':heavy_check_mark:'
    path: examples/nim/union_find_tree_yosupo_test.nim
    title: examples/nim/union_find_tree_yosupo_test.nim
  _pathExtension: nim
  _verificationStatusIcon: ':heavy_check_mark:'
  attributes:
    links: []
  bundledCode: "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.9.1/x64/lib/python3.9/site-packages/onlinejudge_verify/documentation/build.py\"\
    , line 71, in _render_source_code_stat\n    bundled_code = language.bundle(stat.path,\
    \ basedir=basedir, options={'include_paths': [basedir]}).decode()\n  File \"/opt/hostedtoolcache/Python/3.9.1/x64/lib/python3.9/site-packages/onlinejudge_verify/languages/nim.py\"\
    , line 86, in bundle\n    raise NotImplementedError\nNotImplementedError\n"
  code: 'import macros


    proc scanf(formatstr: cstring){.header: "<stdio.h>", varargs.}

    proc nextInt(): int = scanf("%lld",addr result)

    '
  dependsOn: []
  isVerificationFile: false
  path: examples/nim/headers.nim
  requiredBy: []
  timestamp: '2020-05-04 17:35:34+09:00'
  verificationStatus: LIBRARY_ALL_AC
  verifiedWith:
  - examples/nim/union_find_tree_yosupo_test.nim
  - examples/nim/union_find_tree_yosupo_test.nim
  - examples/nim/union_find_tree_aoj_test.nim
  - examples/nim/union_find_tree_aoj_test.nim
documentation_of: examples/nim/headers.nim
layout: document
redirect_from:
- /library/examples/nim/headers.nim
- /library/examples/nim/headers.nim.html
title: examples/nim/headers.nim
---
