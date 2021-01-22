---
data:
  _extendedDependsOn:
  - icon: ':heavy_check_mark:'
    path: examples/macros.hpp
    title: examples/macros.hpp
  _extendedRequiredBy: []
  _extendedVerifiedWith: []
  _isVerificationFailed: false
  _pathExtension: cpp
  _verificationStatusIcon: ':heavy_check_mark:'
  attributes:
    '*NOT_SPECIAL_COMMENTS*': ''
    PROBLEM: http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_3_A
    links:
    - http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_3_A
  bundledCode: "#line 1 \"examples/debug/include_relative.test.cpp\"\n#define PROBLEM\
    \ \"http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_3_A\"\n#include\
    \ <cstdio>\n#line 2 \"examples/macros.hpp\"\n#define REP(i, n) for (int i = 0;\
    \ (i) < (int)(n); ++ (i))\n#define REP3(i, m, n) for (int i = (m); (i) < (int)(n);\
    \ ++ (i))\n#define REP_R(i, n) for (int i = (int)(n) - 1; (i) >= 0; -- (i))\n\
    #define REP3R(i, m, n) for (int i = (int)(n) - 1; (i) >= (int)(m); -- (i))\n#define\
    \ ALL(x) begin(x), end(x)\n#line 4 \"examples/debug/include_relative.test.cpp\"\
    \n\nint main() {\n    REP (i, 1000) {\n        printf(\"Hello World\\n\");\n \
    \   }\n    return 0;\n}\n"
  code: "#define PROBLEM \"http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_3_A\"\
    \n#include <cstdio>\n#include \"../macros.hpp\"\n\nint main() {\n    REP (i, 1000)\
    \ {\n        printf(\"Hello World\\n\");\n    }\n    return 0;\n}\n"
  dependsOn:
  - examples/macros.hpp
  isVerificationFile: true
  path: examples/debug/include_relative.test.cpp
  requiredBy: []
  timestamp: '2020-02-28 16:21:27+09:00'
  verificationStatus: TEST_ACCEPTED
  verifiedWith: []
documentation_of: examples/debug/include_relative.test.cpp
layout: document
redirect_from:
- /verify/examples/debug/include_relative.test.cpp
- /verify/examples/debug/include_relative.test.cpp.html
title: examples/debug/include_relative.test.cpp
---
