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
    PROBLEM: https://judge.yosupo.jp/problem/point_set_range_composite
    links:
    - https://judge.yosupo.jp/problem/point_set_range_composite
  bundledCode: "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.9.1/x64/lib/python3.9/site-packages/onlinejudge_verify/documentation/build.py\"\
    , line 71, in _render_source_code_stat\n    bundled_code = language.bundle(stat.path,\
    \ basedir=basedir, options={'include_paths': [basedir]}).decode()\n  File \"/opt/hostedtoolcache/Python/3.9.1/x64/lib/python3.9/site-packages/onlinejudge_verify/languages/csharpscript.py\"\
    , line 113, in bundle\n    raise NotImplementedError\nNotImplementedError\n"
  code: "#load \"./segment_tree.csx\"\n#pragma PROBLEM https://judge.yosupo.jp/problem/point_set_range_composite\n\
    \nusing System;\nusing System.Linq;\n\nstruct Linear\n{\n    const int MOD = 998244353;\n\
    \    public long A;\n    public long B;\n    public Linear(long a, long b) { A\
    \ = a; B = b; }\n    public static Linear Merge(Linear a, Linear b) => new Linear(a.A\
    \ * b.A % MOD, (a.B * b.A + b.B) % MOD);\n    public long EvalWith(int x) => (A\
    \ * x + B) % MOD;\n    public override string ToString() => $\"{A} {B}\";\n}\n\
    \nvar nq = Console.ReadLine().Split().Select(int.Parse).ToArray();\nvar (n, q)\
    \ = (nq[0], nq[1]);\nSegmentTree<Linear> segTree = new SegmentTree<Linear>(n,\
    \ new Linear(1, 0), Linear.Merge);\n\nfor (int i = 0; i < n; i++)\n{\n    var\
    \ ab = Console.ReadLine().Split().Select(int.Parse).ToArray();\n    segTree[i]\
    \ = new Linear(ab[0], ab[1]);\n}\n\nfor (int i = 0; i < q; i++)\n{\n    var query\
    \ = Console.ReadLine().Split().Select(int.Parse).ToArray();\n    if (query[0]\
    \ == 0)\n    {\n        segTree[query[1]] = new Linear(query[2], query[3]);\n\
    \    }\n    else\n    {\n        Console.WriteLine(segTree[query[1]..query[2]].EvalWith(query[3]));\n\
    \    }\n}\n\n"
  dependsOn:
  - examples/csharpscript/segment_tree.csx
  isVerificationFile: true
  path: examples/csharpscript/segment_tree.point_set_range_composite.test.csx
  requiredBy: []
  timestamp: '2020-02-16 04:32:52+09:00'
  verificationStatus: TEST_ACCEPTED
  verifiedWith: []
documentation_of: examples/csharpscript/segment_tree.point_set_range_composite.test.csx
layout: document
redirect_from:
- /verify/examples/csharpscript/segment_tree.point_set_range_composite.test.csx
- /verify/examples/csharpscript/segment_tree.point_set_range_composite.test.csx.html
title: examples/csharpscript/segment_tree.point_set_range_composite.test.csx
---
