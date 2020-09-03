---
data:
  attributes:
    '*NOT_SPECIAL_COMMENTS*': ''
  bundledCode: '#line 2 "examples/debug/relative_path.hpp"

    char *hello = "Hello World";

    '
  code: '#pragma once

    char *hello = "Hello World";

    '
  dependsOn: []
  extendedDependsOn: []
  extendedRequiredBy:
  - icon: ':warning:'
    path: examples/debug/a/b/c/foo.hpp
    title: examples/debug/a/b/c/foo.hpp
  - icon: ':warning:'
    path: examples/debug/d/e/f/g/foo.hpp
    title: examples/debug/d/e/f/g/foo.hpp
  - icon: ':heavy_check_mark:'
    path: examples/debug/relative_path.test.cpp
    title: examples/debug/relative_path.test.cpp
  - icon: ':warning:'
    path: examples/debug/h/i/j/k/l/foo.hpp
    title: examples/debug/h/i/j/k/l/foo.hpp
  extendedVerifiedWith: []
  isVerificationFile: false
  path: examples/debug/relative_path.hpp
  requiredBy:
  - examples/debug/a/b/c/foo.hpp
  - examples/debug/d/e/f/g/foo.hpp
  - examples/debug/relative_path.test.cpp
  - examples/debug/h/i/j/k/l/foo.hpp
  timestamp: '2020-03-19 16:25:51+09:00'
  verificationStatus: LIBRARY_NO_TESTS
  verificationStatusIcon: ':warning:'
  verifiedWith: []
documentation_of: examples/debug/relative_path.hpp
layout: document
redirect_from:
- /library/examples/debug/relative_path.hpp
- /library/examples/debug/relative_path.hpp.html
title: examples/debug/relative_path.hpp
---
