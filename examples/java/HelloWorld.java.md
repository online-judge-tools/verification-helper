---
data:
  _extendedDependsOn:
  - icon: ':heavy_check_mark:'
    path: examples/java/HelloWorld_test.java
    title: examples/java/HelloWorld_test.java
  _extendedRequiredBy: []
  _extendedVerifiedWith:
  - icon: ':heavy_check_mark:'
    path: examples/java/HelloWorld_test.java
    title: examples/java/HelloWorld_test.java
  _isVerificationFailed: false
  _pathExtension: java
  _verificationStatusIcon: ':heavy_check_mark:'
  attributes: {}
  bundledCode: "Traceback (most recent call last):\n  File \"/home/runner/.local/lib/python3.10/site-packages/onlinejudge_verify/documentation/build.py\"\
    , line 71, in _render_source_code_stat\n    bundled_code = language.bundle(stat.path,\
    \ basedir=basedir, options={'include_paths': [basedir]}).decode()\n  File \"/home/runner/.local/lib/python3.10/site-packages/onlinejudge_verify/languages/user_defined.py\"\
    , line 68, in bundle\n    raise RuntimeError('bundler is not specified: {}'.format(str(path)))\n\
    RuntimeError: bundler is not specified: examples/java/HelloWorld.java\n"
  code: "package examples.java;\n\npublic class HelloWorld {\n    public static String\
    \ getHelloWorld() {\n        return \"Hello World\";\n    }\n}\n"
  dependsOn:
  - examples/java/HelloWorld_test.java
  isVerificationFile: false
  path: examples/java/HelloWorld.java
  requiredBy: []
  timestamp: '2023-12-08 10:48:14+09:00'
  verificationStatus: LIBRARY_ALL_AC
  verifiedWith:
  - examples/java/HelloWorld_test.java
documentation_of: examples/java/HelloWorld.java
layout: document
redirect_from:
- /library/examples/java/HelloWorld.java
- /library/examples/java/HelloWorld.java.html
title: examples/java/HelloWorld.java
---
