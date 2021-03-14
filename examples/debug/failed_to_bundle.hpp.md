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
  bundledCode: "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.9.2/x64/lib/python3.9/site-packages/onlinejudge_verify/documentation/build.py\"\
    , line 71, in _render_source_code_stat\n    bundled_code = language.bundle(stat.path,\
    \ basedir=basedir, options={'include_paths': [basedir]}).decode()\n  File \"/opt/hostedtoolcache/Python/3.9.2/x64/lib/python3.9/site-packages/onlinejudge_verify/languages/cplusplus.py\"\
    , line 187, in bundle\n    bundler.update(path)\n  File \"/opt/hostedtoolcache/Python/3.9.2/x64/lib/python3.9/site-packages/onlinejudge_verify/languages/cplusplus_bundle.py\"\
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
  timestamp: '2020-02-28 16:19:20+09:00'
  verificationStatus: LIBRARY_NO_TESTS
  verifiedWith: []
documentation_of: examples/debug/failed_to_bundle.hpp
layout: document
redirect_from:
- /library/examples/debug/failed_to_bundle.hpp
- /library/examples/debug/failed_to_bundle.hpp.html
title: examples/debug/failed_to_bundle.hpp
---
