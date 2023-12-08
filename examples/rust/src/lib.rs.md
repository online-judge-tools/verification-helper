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
  - icon: ':warning:'
    path: examples/rust/crates/io/scanner/src/lib.rs
    title: examples/rust/crates/io/scanner/src/lib.rs
  _extendedRequiredBy: []
  _extendedVerifiedWith: []
  _isVerificationFailed: false
  _pathExtension: rs
  _verificationStatusIcon: ':warning:'
  attributes:
    links: []
  bundledCode: "Traceback (most recent call last):\n  File \"/home/runner/.local/lib/python3.10/site-packages/onlinejudge_verify/documentation/build.py\"\
    , line 71, in _render_source_code_stat\n    bundled_code = language.bundle(stat.path,\
    \ basedir=basedir, options={'include_paths': [basedir]}).decode()\n  File \"/home/runner/.local/lib/python3.10/site-packages/onlinejudge_verify/languages/rust.py\"\
    , line 288, in bundle\n    raise NotImplementedError\nNotImplementedError\n"
  code: "//! Re-exports the crates for rustdoc.\n//!\n//! This crate itself is not\
    \ intended to be used directly.\n\n// With `custom-build` and `syn` crate, we\
    \ can expand crate-level rustdocs.\n\nmacro_rules! re_export(($($name:ident),*\
    \ $(,)?) => ($(pub mod $name { pub use ::$name::*; })*));\n\npub mod helloworld\
    \ {\n    //! Crates of \"hello\" and \"world\".\n\n    re_export!(hello, world);\n\
    }\n\npub mod io {\n    //! Crates about IO.\n\n    re_export!(input, scanner);\n\
    }\n"
  dependsOn:
  - examples/rust/crates/helloworld/hello/src/lib.rs
  - examples/rust/crates/helloworld/world/src/lib.rs
  - examples/rust/crates/io/input/src/lib.rs
  - examples/rust/crates/io/scanner/src/lib.rs
  isVerificationFile: false
  path: examples/rust/src/lib.rs
  requiredBy: []
  timestamp: '2023-12-08 10:48:14+09:00'
  verificationStatus: LIBRARY_NO_TESTS
  verifiedWith: []
documentation_of: examples/rust/src/lib.rs
layout: document
redirect_from:
- /library/examples/rust/src/lib.rs
- /library/examples/rust/src/lib.rs.html
title: examples/rust/src/lib.rs
---
