---
data:
  _extendedDependsOn:
  - icon: ':heavy_check_mark:'
    path: examples/java/HelloWorld.java
    title: examples/java/HelloWorld.java
  _extendedRequiredBy:
  - icon: ':heavy_check_mark:'
    path: examples/java/HelloWorld.java
    title: examples/java/HelloWorld.java
  _extendedVerifiedWith: []
  _pathExtension: java
  _verificationStatusIcon: ':heavy_check_mark:'
  attributes:
    PROBLEM: https://onlinejudge.u-aizu.ac.jp/courses/lesson/2/ITP1/1/ITP1_1_A
  bundledCode: "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/documentation/build.py\"\
    , line 71, in _render_source_code_stat\n    bundled_code = language.bundle(stat.path,\
    \ basedir=basedir).decode()\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/languages/user_defined.py\"\
    , line 67, in bundle\n    assert 'bundle' in self.config\nAssertionError\n"
  code: "// verification-helper: PROBLEM https://onlinejudge.u-aizu.ac.jp/courses/lesson/2/ITP1/1/ITP1_1_A\n\
    package examples.java;\nimport examples.java.HelloWorld;\n\npublic class HelloWorld_test\
    \ {\n    public static void main(String[] args) {\n        System.out.println(HelloWorld.getHelloWorld());\n\
    \    }\n}\n"
  dependsOn:
  - examples/java/HelloWorld.java
  isVerificationFile: true
  path: examples/java/HelloWorld_test.java
  requiredBy:
  - examples/java/HelloWorld.java
  timestamp: '2020-09-17 19:34:20+09:00'
  verificationStatus: TEST_ACCEPTED
  verifiedWith: []
documentation_of: examples/java/HelloWorld_test.java
layout: document
redirect_from:
- /verify/examples/java/HelloWorld_test.java
- /verify/examples/java/HelloWorld_test.java.html
title: examples/java/HelloWorld_test.java
---
