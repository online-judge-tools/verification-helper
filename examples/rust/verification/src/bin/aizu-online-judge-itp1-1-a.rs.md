---
data:
  _extendedDependsOn:
  - icon: ':heavy_check_mark:'
    path: examples/rust/crates/helloworld/hello/src/lib.rs
    title: examples/rust/crates/helloworld/hello/src/lib.rs
  - icon: ':heavy_check_mark:'
    path: examples/rust/crates/helloworld/world/src/lib.rs
    title: examples/rust/crates/helloworld/world/src/lib.rs
  - icon: ':heavy_check_mark:'
    path: examples/rust/crates/io/input/src/lib.rs
    title: examples/rust/crates/io/input/src/lib.rs
  _extendedRequiredBy: []
  _extendedVerifiedWith: []
  _pathExtension: rs
  _verificationStatusIcon: ':heavy_check_mark:'
  attributes:
    PROBLEM: http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_1_A
    links:
    - http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_1_A
  bundledCode: "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.9.1/x64/lib/python3.9/site-packages/onlinejudge_verify/documentation/build.py\"\
    , line 71, in _render_source_code_stat\n    bundled_code = language.bundle(stat.path,\
    \ basedir=basedir, options={'include_paths': [basedir]}).decode()\n  File \"/opt/hostedtoolcache/Python/3.9.1/x64/lib/python3.9/site-packages/onlinejudge_verify/languages/rust.py\"\
    , line 288, in bundle\n    raise NotImplementedError\nNotImplementedError\n"
  code: "// verification-helper: PROBLEM http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_1_A\n\
    \nfn main() {\n    println!(\"{} {}\", hello::HELLO, world::WORLD);\n}\n"
  dependsOn:
  - examples/rust/crates/helloworld/hello/src/lib.rs
  - examples/rust/crates/helloworld/world/src/lib.rs
  - examples/rust/crates/io/input/src/lib.rs
  isVerificationFile: true
  path: examples/rust/verification/src/bin/aizu-online-judge-itp1-1-a.rs
  requiredBy: []
  timestamp: '2020-11-30 13:30:54+09:00'
  verificationStatus: TEST_ACCEPTED
  verifiedWith: []
documentation_of: examples/rust/verification/src/bin/aizu-online-judge-itp1-1-a.rs
layout: document
redirect_from:
- /verify/examples/rust/verification/src/bin/aizu-online-judge-itp1-1-a.rs
- /verify/examples/rust/verification/src/bin/aizu-online-judge-itp1-1-a.rs.html
title: examples/rust/verification/src/bin/aizu-online-judge-itp1-1-a.rs
---
