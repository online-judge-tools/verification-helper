---
data:
  _extendedDependsOn:
  - icon: ':heavy_check_mark:'
    path: Examples2/Haskell/HelloWorld.hs
    title: Examples2/Haskell/HelloWorld.hs
  _extendedRequiredBy:
  - icon: ':heavy_check_mark:'
    path: Examples2/Haskell/HelloWorld.hs
    title: Examples2/Haskell/HelloWorld.hs
  _extendedVerifiedWith: []
  _pathExtension: hs
  _verificationStatusIcon: ':heavy_check_mark:'
  attributes:
    PROBLEM: https://onlinejudge.u-aizu.ac.jp/courses/lesson/2/ITP1/1/ITP1_1_A
  bundledCode: "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/documentation/build.py\"\
    , line 70, in _render_source_code_stat\n    bundled_code = language.bundle(stat.path,\
    \ basedir=basedir).decode()\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/languages/user_defined.py\"\
    , line 67, in bundle\n    assert 'bundle' in self.config\nAssertionError\n"
  code: "{- verification-helper: PROBLEM https://onlinejudge.u-aizu.ac.jp/courses/lesson/2/ITP1/1/ITP1_1_A\n\
    \ -}\nmodule Main where\nimport Examples2.Haskell.HelloWorld (helloWorld)\n\n\
    main :: IO ()\nmain = putStrLn helloWorld\n"
  dependsOn:
  - Examples2/Haskell/HelloWorld.hs
  isVerificationFile: true
  path: Examples2/Haskell/HelloWorld.test.hs
  requiredBy:
  - Examples2/Haskell/HelloWorld.hs
  timestamp: '2020-09-17 18:45:17+09:00'
  verificationStatus: TEST_ACCEPTED
  verifiedWith: []
documentation_of: Examples2/Haskell/HelloWorld.test.hs
layout: document
redirect_from:
- /verify/Examples2/Haskell/HelloWorld.test.hs
- /verify/Examples2/Haskell/HelloWorld.test.hs.html
title: Examples2/Haskell/HelloWorld.test.hs
---
