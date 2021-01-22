---
data:
  _extendedDependsOn:
  - icon: ':heavy_check_mark:'
    path: examples/debug/relative_path.hpp
    title: examples/debug/relative_path.hpp
  _extendedRequiredBy: []
  _extendedVerifiedWith:
  - icon: ':heavy_check_mark:'
    path: examples/debug/relative_path.test.cpp
    title: examples/debug/relative_path.test.cpp
  _isVerificationFailed: false
  _pathExtension: hpp
  _verificationStatusIcon: ':heavy_check_mark:'
  attributes:
    links: []
  bundledCode: '#line 2 "examples/debug/relative_path.hpp"

    char *hello = "Hello World";

    #line 4 "examples/debug/h/i/j/k/l/foo.hpp"

    '
  code: '#pragma once

    #include "../../../../../relative_path.hpp"

    #include "../../../../../../debug/relative_path.hpp"

    '
  dependsOn:
  - examples/debug/relative_path.hpp
  isVerificationFile: false
  path: examples/debug/h/i/j/k/l/foo.hpp
  requiredBy: []
  timestamp: '2020-03-19 16:25:51+09:00'
  verificationStatus: LIBRARY_ALL_AC
  verifiedWith:
  - examples/debug/relative_path.test.cpp
documentation_of: examples/debug/h/i/j/k/l/foo.hpp
layout: document
redirect_from:
- /library/examples/debug/h/i/j/k/l/foo.hpp
- /library/examples/debug/h/i/j/k/l/foo.hpp.html
title: examples/debug/h/i/j/k/l/foo.hpp
---
