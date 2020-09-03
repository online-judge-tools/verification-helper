---
data:
  attributes:
    '*NOT_SPECIAL_COMMENTS*': ''
  bundledCode: '#line 2 "examples/debug/relative_path.hpp"

    char *hello = "Hello World";

    #line 4 "examples/debug/d/e/f/g/foo.hpp"

    '
  code: '#pragma once

    #include "../../../../relative_path.hpp"

    #include "./../../../.././a/b/../../relative_path.hpp"

    '
  dependsOn:
  - examples/debug/relative_path.hpp
  extendedDependsOn:
  - icon: ':heavy_check_mark:'
    path: examples/debug/relative_path.hpp
    title: examples/debug/relative_path.hpp
  extendedRequiredBy: []
  extendedVerifiedWith:
  - icon: ':heavy_check_mark:'
    path: examples/debug/relative_path.test.cpp
    title: examples/debug/relative_path.test.cpp
  isVerificationFile: false
  path: examples/debug/d/e/f/g/foo.hpp
  requiredBy: []
  timestamp: '2020-03-19 16:25:51+09:00'
  verificationStatus: LIBRARY_ALL_AC
  verificationStatusIcon: ':heavy_check_mark:'
  verifiedWith:
  - examples/debug/relative_path.test.cpp
documentation_of: examples/debug/d/e/f/g/foo.hpp
layout: document
redirect_from:
- /library/examples/debug/d/e/f/g/foo.hpp
- /library/examples/debug/d/e/f/g/foo.hpp.html
title: examples/debug/d/e/f/g/foo.hpp
---
