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
  _isVerificationFailed: false
  _pathExtension: hs
  _verificationStatusIcon: ':heavy_check_mark:'
  attributes:
    PROBLEM: https://onlinejudge.u-aizu.ac.jp/courses/lesson/2/ITP1/1/ITP1_1_A
  bundledCode: "Traceback (most recent call last):\n  File \"/home/runner/.local/lib/python3.10/site-packages/onlinejudge_verify/documentation/build.py\"\
    , line 71, in _render_source_code_stat\n    bundled_code = language.bundle(stat.path,\
    \ basedir=basedir, options={'include_paths': [basedir]}).decode()\n  File \"/home/runner/.local/lib/python3.10/site-packages/onlinejudge_verify/languages/user_defined.py\"\
    , line 68, in bundle\n    raise RuntimeError('bundler is not specified: {}'.format(str(path)))\n\
    RuntimeError: bundler is not specified: Examples2/Haskell/HelloWorld.test.hs\n"
  code: "{- verification-helper: PROBLEM https://onlinejudge.u-aizu.ac.jp/courses/lesson/2/ITP1/1/ITP1_1_A\n\
    \ -}\nmodule Main where\nimport Examples2.Haskell.HelloWorld (helloWorld)\n\n\
    main :: IO ()\nmain = putStrLn helloWorld\n"
  dependsOn:
  - Examples2/Haskell/HelloWorld.hs
  isVerificationFile: true
  path: Examples2/Haskell/HelloWorld.test.hs
  requiredBy:
  - Examples2/Haskell/HelloWorld.hs
  timestamp: '2023-12-08 11:08:52+09:00'
  verificationStatus: TEST_ACCEPTED
  verifiedWith: []
documentation_of: Examples2/Haskell/HelloWorld.test.hs
layout: document
redirect_from:
- /verify/Examples2/Haskell/HelloWorld.test.hs
- /verify/Examples2/Haskell/HelloWorld.test.hs.html
title: Examples2/Haskell/HelloWorld.test.hs
---
