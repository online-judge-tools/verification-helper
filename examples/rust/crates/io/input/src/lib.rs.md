---
data:
  _extendedDependsOn:
  - icon: ':warning:'
    path: examples/rust/crates/io/scanner/src/lib.rs
    title: examples/rust/crates/io/scanner/src/lib.rs
  _extendedRequiredBy:
  - icon: ':warning:'
    path: examples/rust/src/lib.rs
    title: examples/rust/src/lib.rs
  _extendedVerifiedWith:
  - icon: ':heavy_check_mark:'
    path: examples/rust/verification/src/bin/aizu-online-judge-itp1-1-a.rs
    title: examples/rust/verification/src/bin/aizu-online-judge-itp1-1-a.rs
  - icon: ':heavy_check_mark:'
    path: examples/rust/verification/src/bin/library-checker-aplusb.rs
    title: examples/rust/verification/src/bin/library-checker-aplusb.rs
  _isVerificationFailed: false
  _pathExtension: rs
  _verificationStatusIcon: ':heavy_check_mark:'
  attributes:
    links: []
  bundledCode: "Traceback (most recent call last):\n  File \"/home/runner/.local/lib/python3.10/site-packages/onlinejudge_verify/documentation/build.py\"\
    , line 71, in _render_source_code_stat\n    bundled_code = language.bundle(stat.path,\
    \ basedir=basedir, options={'include_paths': [basedir]}).decode()\n  File \"/home/runner/.local/lib/python3.10/site-packages/onlinejudge_verify/languages/rust.py\"\
    , line 288, in bundle\n    raise NotImplementedError\nNotImplementedError\n"
  code: "//! A limited `input!` macro.\n//!\n//! ```no_run\n//! use input::input;\n\
    //!\n//! input! {\n//!     a: u32,\n//!     b: u32,\n//! }\n//! ```\n\npub use\
    \ scanner::Scanner;\n\n/// A limited `input!` macro.\n#[macro_export]\nmacro_rules!\
    \ input {\n    ($($var:ident : $ty:ty),* $(,)?) => {\n        let mut __scanner\
    \ = $crate::Scanner::from_stdin();\n        $(\n            let $var = __scanner.read::<$ty>();\n\
    \        )*\n    };\n}\n"
  dependsOn:
  - examples/rust/crates/io/scanner/src/lib.rs
  isVerificationFile: false
  path: examples/rust/crates/io/input/src/lib.rs
  requiredBy:
  - examples/rust/src/lib.rs
  timestamp: '2023-12-09 20:36:27+09:00'
  verificationStatus: LIBRARY_ALL_AC
  verifiedWith:
  - examples/rust/verification/src/bin/library-checker-aplusb.rs
  - examples/rust/verification/src/bin/aizu-online-judge-itp1-1-a.rs
documentation_of: examples/rust/crates/io/input/src/lib.rs
layout: document
redirect_from:
- /library/examples/rust/crates/io/input/src/lib.rs
- /library/examples/rust/crates/io/input/src/lib.rs.html
title: examples/rust/crates/io/input/src/lib.rs
---
