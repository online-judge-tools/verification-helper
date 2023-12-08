---
data:
  _extendedDependsOn: []
  _extendedRequiredBy: []
  _extendedVerifiedWith: []
  _isVerificationFailed: false
  _pathExtension: hpp
  _verificationStatusIcon: ':warning:'
  attributes:
    links: []
  bundledCode: "Traceback (most recent call last):\n  File \"/home/runner/.local/lib/python3.10/site-packages/onlinejudge_verify/documentation/build.py\"\
    , line 71, in _render_source_code_stat\n    bundled_code = language.bundle(stat.path,\
    \ basedir=basedir, options={'include_paths': [basedir]}).decode()\n  File \"/home/runner/.local/lib/python3.10/site-packages/onlinejudge_verify/languages/cplusplus.py\"\
    , line 187, in bundle\n    bundler.update(path)\n  File \"/home/runner/.local/lib/python3.10/site-packages/onlinejudge_verify/languages/cplusplus_bundle.py\"\
    , line 400, in update\n    raise BundleErrorAt(path, i + 1, \"unable to process\
    \ #include in #if / #ifdef / #ifndef other than include guards\")\nonlinejudge_verify.languages.cplusplus_bundle.BundleErrorAt:\
    \ examples/debug/failed_to_bundle.hpp: line 3: unable to process #include in #if\
    \ / #ifdef / #ifndef other than include guards\n"
  code: '#define HOGE

    #ifndef HOGE

    #include "examples/failed_to_bundle.hpp"  // this is a self-include at a glance

    #endif

    '
  dependsOn: []
  isVerificationFile: false
  path: examples/debug/failed_to_bundle.hpp
  requiredBy: []
  timestamp: '2023-12-08 11:18:27+09:00'
  verificationStatus: LIBRARY_NO_TESTS
  verifiedWith: []
documentation_of: examples/debug/failed_to_bundle.hpp
layout: document
redirect_from:
- /library/examples/debug/failed_to_bundle.hpp
- /library/examples/debug/failed_to_bundle.hpp.html
title: examples/debug/failed_to_bundle.hpp
---
