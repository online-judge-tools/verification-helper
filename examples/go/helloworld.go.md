---
data:
  _extendedDependsOn:
  - icon: ':heavy_check_mark:'
    path: examples/go/helloworld.test.go
    title: examples/go/helloworld.test.go
  - icon: ':heavy_check_mark:'
    path: examples/go/helloworld/helloworld.go
    title: examples/go/helloworld/helloworld.go
  _extendedRequiredBy:
  - icon: ':heavy_check_mark:'
    path: examples/go/helloworld/helloworld.go
    title: examples/go/helloworld/helloworld.go
  _extendedVerifiedWith:
  - icon: ':heavy_check_mark:'
    path: examples/go/helloworld.test.go
    title: examples/go/helloworld.test.go
  _pathExtension: go
  _verificationStatusIcon: ':heavy_check_mark:'
  attributes: {}
  bundledCode: "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.9.0/x64/lib/python3.9/site-packages/onlinejudge_verify/documentation/build.py\"\
    , line 71, in _render_source_code_stat\n    bundled_code = language.bundle(stat.path,\
    \ basedir=basedir).decode()\n  File \"/opt/hostedtoolcache/Python/3.9.0/x64/lib/python3.9/site-packages/onlinejudge_verify/languages/user_defined.py\"\
    , line 67, in bundle\n    assert 'bundle' in self.config\nAssertionError\n"
  code: "package helloworld\n\nfunc GetHelloWorld() string {\n    return \"Hello World\"\
    \n}\n"
  dependsOn:
  - examples/go/helloworld/helloworld.go
  - examples/go/helloworld.test.go
  isVerificationFile: false
  path: examples/go/helloworld.go
  requiredBy:
  - examples/go/helloworld/helloworld.go
  timestamp: '2020-09-17 19:04:09+09:00'
  verificationStatus: LIBRARY_ALL_AC
  verifiedWith:
  - examples/go/helloworld.test.go
documentation_of: examples/go/helloworld.go
layout: document
redirect_from:
- /library/examples/go/helloworld.go
- /library/examples/go/helloworld.go.html
title: examples/go/helloworld.go
---
