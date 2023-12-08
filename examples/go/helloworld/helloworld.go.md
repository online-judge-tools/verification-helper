---
data:
  _extendedDependsOn:
  - icon: ':heavy_check_mark:'
    path: examples/go/helloworld.go
    title: examples/go/helloworld.go
  - icon: ':heavy_check_mark:'
    path: examples/go/helloworld.test.go
    title: examples/go/helloworld.test.go
  _extendedRequiredBy:
  - icon: ':heavy_check_mark:'
    path: examples/go/helloworld.go
    title: examples/go/helloworld.go
  _extendedVerifiedWith:
  - icon: ':heavy_check_mark:'
    path: examples/go/helloworld.test.go
    title: examples/go/helloworld.test.go
  _isVerificationFailed: false
  _pathExtension: go
  _verificationStatusIcon: ':heavy_check_mark:'
  attributes: {}
  bundledCode: "Traceback (most recent call last):\n  File \"/home/runner/.local/lib/python3.10/site-packages/onlinejudge_verify/documentation/build.py\"\
    , line 71, in _render_source_code_stat\n    bundled_code = language.bundle(stat.path,\
    \ basedir=basedir, options={'include_paths': [basedir]}).decode()\n  File \"/home/runner/.local/lib/python3.10/site-packages/onlinejudge_verify/languages/user_defined.py\"\
    , line 68, in bundle\n    raise RuntimeError('bundler is not specified: {}'.format(str(path)))\n\
    RuntimeError: bundler is not specified: examples/go/helloworld/helloworld.go\n"
  code: "package helloworld\n\nfunc GetHelloWorld() string {\n    return \"Hello World\"\
    \n}\n"
  dependsOn:
  - examples/go/helloworld.go
  - examples/go/helloworld.test.go
  isVerificationFile: false
  path: examples/go/helloworld/helloworld.go
  requiredBy:
  - examples/go/helloworld.go
  timestamp: '2023-12-08 10:48:14+09:00'
  verificationStatus: LIBRARY_ALL_AC
  verifiedWith:
  - examples/go/helloworld.test.go
documentation_of: examples/go/helloworld/helloworld.go
layout: document
redirect_from:
- /library/examples/go/helloworld/helloworld.go
- /library/examples/go/helloworld/helloworld.go.html
title: examples/go/helloworld/helloworld.go
---
