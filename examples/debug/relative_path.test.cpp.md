---
data:
  _extendedDependsOn:
  - icon: ':heavy_check_mark:'
    path: examples/debug/a/b/c/foo.hpp
    title: examples/debug/a/b/c/foo.hpp
  - icon: ':heavy_check_mark:'
    path: examples/debug/d/e/f/g/foo.hpp
    title: examples/debug/d/e/f/g/foo.hpp
  - icon: ':heavy_check_mark:'
    path: examples/debug/h/i/j/k/l/foo.hpp
    title: examples/debug/h/i/j/k/l/foo.hpp
  - icon: ':heavy_check_mark:'
    path: examples/debug/relative_path.hpp
    title: examples/debug/relative_path.hpp
  _extendedRequiredBy: []
  _extendedVerifiedWith: []
  _isVerificationFailed: false
  _pathExtension: cpp
  _verificationStatusIcon: ':heavy_check_mark:'
  attributes:
    '*NOT_SPECIAL_COMMENTS*': ''
    PROBLEM: http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_1_A
    links:
    - http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_1_A
  bundledCode: "#line 1 \"examples/debug/relative_path.test.cpp\"\n#define PROBLEM\
    \ \"http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_1_A\"\n#include\
    \ <cstdio>\n#line 2 \"examples/debug/relative_path.hpp\"\nchar *hello = \"Hello\
    \ World\";\n#line 6 \"examples/debug/relative_path.test.cpp\"\n\nint main() {\n\
    \    printf(\"%s\\n\", hello);\n    return 0;\n}\n"
  code: "#define PROBLEM \"http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_1_A\"\
    \n#include <cstdio>\n#include \"./a/b/c/foo.hpp\"\n#include \"d/e/f/g/foo.hpp\"\
    \n#include \"examples/debug/h/i/j/k/l/foo.hpp\"\n\nint main() {\n    printf(\"\
    %s\\n\", hello);\n    return 0;\n}\n"
  dependsOn:
  - examples/debug/a/b/c/foo.hpp
  - examples/debug/relative_path.hpp
  - examples/debug/d/e/f/g/foo.hpp
  - examples/debug/h/i/j/k/l/foo.hpp
  isVerificationFile: true
  path: examples/debug/relative_path.test.cpp
  requiredBy: []
  timestamp: '2020-03-19 16:25:51+09:00'
  verificationStatus: TEST_ACCEPTED
  verifiedWith: []
documentation_of: examples/debug/relative_path.test.cpp
layout: document
redirect_from:
- /verify/examples/debug/relative_path.test.cpp
- /verify/examples/debug/relative_path.test.cpp.html
title: examples/debug/relative_path.test.cpp
---
