---
data:
  _extendedDependsOn: []
  _extendedRequiredBy:
  - icon: ':heavy_check_mark:'
    path: examples/debug/a/b/c/foo.hpp
    title: examples/debug/a/b/c/foo.hpp
  - icon: ':heavy_check_mark:'
    path: examples/debug/d/e/f/g/foo.hpp
    title: examples/debug/d/e/f/g/foo.hpp
  - icon: ':heavy_check_mark:'
    path: examples/debug/h/i/j/k/l/foo.hpp
    title: examples/debug/h/i/j/k/l/foo.hpp
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

    '
  code: '#pragma once

    char *hello = "Hello World";

    '
  dependsOn: []
  isVerificationFile: false
  path: examples/debug/relative_path.hpp
  requiredBy:
  - examples/debug/h/i/j/k/l/foo.hpp
  - examples/debug/d/e/f/g/foo.hpp
  - examples/debug/a/b/c/foo.hpp
  timestamp: '2020-03-19 16:25:51+09:00'
  verificationStatus: LIBRARY_ALL_AC
  verifiedWith:
  - examples/debug/relative_path.test.cpp
documentation_of: examples/debug/relative_path.hpp
layout: document
redirect_from:
- /library/examples/debug/relative_path.hpp
- /library/examples/debug/relative_path.hpp.html
title: examples/debug/relative_path.hpp
---
