---
data:
  _extendedDependsOn:
  - icon: ':heavy_check_mark:'
    path: examples/python/hello_world.py
    title: examples/python/hello_world.py
  _extendedRequiredBy: []
  _extendedVerifiedWith: []
  _isVerificationFailed: false
  _pathExtension: py
  _verificationStatusIcon: ':heavy_check_mark:'
  attributes:
    PROBLEM: https://onlinejudge.u-aizu.ac.jp/courses/lesson/2/ITP1/1/ITP1_1_A
    links:
    - https://onlinejudge.u-aizu.ac.jp/courses/lesson/2/ITP1/1/ITP1_1_A
  bundledCode: "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.9.2/x64/lib/python3.9/site-packages/onlinejudge_verify/documentation/build.py\"\
    , line 71, in _render_source_code_stat\n    bundled_code = language.bundle(stat.path,\
    \ basedir=basedir, options={'include_paths': [basedir]}).decode()\n  File \"/opt/hostedtoolcache/Python/3.9.2/x64/lib/python3.9/site-packages/onlinejudge_verify/languages/python.py\"\
    , line 96, in bundle\n    raise NotImplementedError\nNotImplementedError\n"
  code: "# verification-helper: PROBLEM https://onlinejudge.u-aizu.ac.jp/courses/lesson/2/ITP1/1/ITP1_1_A\n\
    import examples.python.hello_world\n\ndef main():\n    print(examples.python.hello_world.get_hello_world())\n\
    \nif __name__ == '__main__':\n    main()\n"
  dependsOn:
  - examples/python/hello_world.py
  isVerificationFile: true
  path: examples/python/hello_world.test.py
  requiredBy: []
  timestamp: '2020-09-17 18:25:50+09:00'
  verificationStatus: TEST_ACCEPTED
  verifiedWith: []
documentation_of: examples/python/hello_world.test.py
layout: document
redirect_from:
- /verify/examples/python/hello_world.test.py
- /verify/examples/python/hello_world.test.py.html
title: examples/python/hello_world.test.py
---
