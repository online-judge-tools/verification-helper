---
data:
  _extendedDependsOn:
  - icon: ':heavy_check_mark:'
    path: Examples2/Haskell/HelloWorld.test.hs
    title: Examples2/Haskell/HelloWorld.test.hs
  _extendedRequiredBy: []
  _extendedVerifiedWith:
  - icon: ':heavy_check_mark:'
    path: Examples2/Haskell/HelloWorld.test.hs
    title: Examples2/Haskell/HelloWorld.test.hs
  _isVerificationFailed: false
  _pathExtension: hs
  _verificationStatusIcon: ':heavy_check_mark:'
  attributes: {}
  bundledCode: "Traceback (most recent call last):\n  File \"/home/runner/.local/lib/python3.10/site-packages/onlinejudge_verify/documentation/build.py\"\
    , line 71, in _render_source_code_stat\n    bundled_code = language.bundle(stat.path,\
    \ basedir=basedir, options={'include_paths': [basedir]}).decode()\n  File \"/home/runner/.local/lib/python3.10/site-packages/onlinejudge_verify/languages/user_defined.py\"\
    , line 68, in bundle\n    raise RuntimeError('bundler is not specified: {}'.format(str(path)))\n\
    RuntimeError: bundler is not specified: Examples2/Haskell/HelloWorld.hs\n"
  code: 'module Examples2.Haskell.HelloWorld where


    helloWorld :: String

    helloWorld = "Hello World"

    '
  dependsOn:
  - Examples2/Haskell/HelloWorld.test.hs
  isVerificationFile: false
  path: Examples2/Haskell/HelloWorld.hs
  requiredBy: []
  timestamp: '2023-12-08 11:08:52+09:00'
  verificationStatus: LIBRARY_ALL_AC
  verifiedWith:
  - Examples2/Haskell/HelloWorld.test.hs
documentation_of: Examples2/Haskell/HelloWorld.hs
layout: document
redirect_from:
- /library/Examples2/Haskell/HelloWorld.hs
- /library/Examples2/Haskell/HelloWorld.hs.html
title: Examples2/Haskell/HelloWorld.hs
---
