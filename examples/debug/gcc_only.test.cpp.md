---
data:
  _extendedDependsOn: []
  _extendedRequiredBy: []
  _extendedVerifiedWith: []
  _isVerificationFailed: false
  _pathExtension: cpp
  _verificationStatusIcon: ':heavy_check_mark:'
  attributes:
    '*NOT_SPECIAL_COMMENTS*': ''
    IGNORE_IF_CLANG: ''
    PROBLEM: https://onlinejudge.u-aizu.ac.jp/courses/lesson/2/ITP1/1/ITP1_1_A
    links:
    - https://onlinejudge.u-aizu.ac.jp/courses/lesson/2/ITP1/1/ITP1_1_A
  bundledCode: "#line 1 \"examples/debug/gcc_only.test.cpp\"\n#ifdef __clang__\n#define\
    \ IGNORE\n#else\n\n#define PROBLEM \"https://onlinejudge.u-aizu.ac.jp/courses/lesson/2/ITP1/1/ITP1_1_A\"\
    \n#include <cstdio>\n\n// clang++ says \"error: C++ requires a type specifier\
    \ for all declarations\", but g++ doesn't\nmain() {\n    printf(\"Hello World\\\
    n\");\n}\n\n#endif\n"
  code: "#ifdef __clang__\n#define IGNORE\n#else\n\n#define PROBLEM \"https://onlinejudge.u-aizu.ac.jp/courses/lesson/2/ITP1/1/ITP1_1_A\"\
    \n#include <cstdio>\n\n// clang++ says \"error: C++ requires a type specifier\
    \ for all declarations\", but g++ doesn't\nmain() {\n    printf(\"Hello World\\\
    n\");\n}\n\n#endif\n"
  dependsOn: []
  isVerificationFile: true
  path: examples/debug/gcc_only.test.cpp
  requiredBy: []
  timestamp: '2020-02-28 16:21:27+09:00'
  verificationStatus: TEST_ACCEPTED
  verifiedWith: []
documentation_of: examples/debug/gcc_only.test.cpp
layout: document
redirect_from:
- /verify/examples/debug/gcc_only.test.cpp
- /verify/examples/debug/gcc_only.test.cpp.html
title: examples/debug/gcc_only.test.cpp
---
