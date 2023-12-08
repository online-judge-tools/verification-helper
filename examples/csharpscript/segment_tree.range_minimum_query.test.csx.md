---
data:
  _extendedDependsOn:
  - icon: ':heavy_check_mark:'
    path: examples/csharpscript/segment_tree.csx
    title: examples/csharpscript/segment_tree.csx
  _extendedRequiredBy: []
  _extendedVerifiedWith: []
  _isVerificationFailed: false
  _pathExtension: csx
  _verificationStatusIcon: ':heavy_check_mark:'
  attributes:
    PROBLEM: https://onlinejudge.u-aizu.ac.jp/courses/library/3/DSL/all/DSL_2_A
    links:
    - https://onlinejudge.u-aizu.ac.jp/courses/library/3/DSL/all/DSL_2_A
    - https://onlinejudge.u-aizu.ac.jp/courses/library/3/DSL/all/DSL_2_A
  bundledCode: "Traceback (most recent call last):\n  File \"/home/runner/.local/lib/python3.10/site-packages/onlinejudge_verify/documentation/build.py\"\
    , line 71, in _render_source_code_stat\n    bundled_code = language.bundle(stat.path,\
    \ basedir=basedir, options={'include_paths': [basedir]}).decode()\n  File \"/home/runner/.local/lib/python3.10/site-packages/onlinejudge_verify/languages/csharpscript.py\"\
    , line 113, in bundle\n    raise NotImplementedError\nNotImplementedError\n"
  code: "#load \"./segment_tree.csx\"\n#pragma PROBLEM https://onlinejudge.u-aizu.ac.jp/courses/library/3/DSL/all/DSL_2_A\n\
    \nusing System;\nusing System.Linq;\n\nvar nq = Console.ReadLine().Split().Select(int.Parse).ToArray();\n\
    var (n, q) = (nq[0], nq[1]);\nSegmentTree<int> segTree = new SegmentTree<int>(n,\
    \ int.MaxValue, Math.Min);\n\nfor (int i = 0; i < q; i++)\n{\n    var query =\
    \ Console.ReadLine().Split().Select(int.Parse).ToArray();\n    if (query[0] ==\
    \ 0)\n    {\n        segTree[query[1]] = query[2];\n    }\n    else\n    {\n \
    \       Console.WriteLine(segTree[query[1]..(query[2] + 1)]);\n    }\n}\n"
  dependsOn:
  - examples/csharpscript/segment_tree.csx
  isVerificationFile: true
  path: examples/csharpscript/segment_tree.range_minimum_query.test.csx
  requiredBy: []
  timestamp: '2023-12-08 10:48:14+09:00'
  verificationStatus: TEST_ACCEPTED
  verifiedWith: []
documentation_of: examples/csharpscript/segment_tree.range_minimum_query.test.csx
layout: document
redirect_from:
- /verify/examples/csharpscript/segment_tree.range_minimum_query.test.csx
- /verify/examples/csharpscript/segment_tree.range_minimum_query.test.csx.html
title: examples/csharpscript/segment_tree.range_minimum_query.test.csx
---
