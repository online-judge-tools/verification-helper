---
data:
  attributes: {}
  bundledCode: "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/documentation/build.py\"\
    , line 64, in _render_source_code_stat\n    bundled_code = language.bundle(stat.path,\
    \ basedir=basedir).decode()\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/languages/csharpscript.py\"\
    , line 110, in bundle\n    raise NotImplementedError\nNotImplementedError\n"
  code: "class SegmentTree<T>\n{\n    public int Count { get; private set; }\n   \
    \ T Identity;\n    T[] Data;\n    Func<T, T, T> Merge;\n    int LeafCount;\n \
    \   public SegmentTree(int count, T identity, Func<T, T, T> merge)\n    {\n  \
    \      Count = count;\n        Identity = identity;\n        Merge = merge;\n\
    \        LeafCount = 1;\n        while (LeafCount < count) LeafCount <<= 1;\n\
    \        Data = new T[LeafCount << 1];\n        for (int i = 1; i < Data.Length;\
    \ i++) Data[i] = identity;\n    }\n    public T this[int index]\n    {\n     \
    \   get { return Data[LeafCount + index]; }\n        set { Assign(index, value);\
    \ }\n    }\n    public void Assign(int i, T x) { Data[i += LeafCount] = x; while\
    \ (0 < (i >>= 1)) Data[i] = Merge(Data[i << 1], Data[(i << 1) | 1]); }\n    public\
    \ void Operate(int i, T x) { Data[i += LeafCount] = Merge(Data[i], x); while (0\
    \ < (i >>= 1)) Data[i] = Merge(Data[i << 1], Data[(i << 1) | 1]); }\n    public\
    \ T Slice(int l, int length) => Fold(l, l + length);\n    public T Fold(int l,\
    \ int r)\n    {\n        T lRes = Identity, rRes = Identity;\n        for (l +=\
    \ LeafCount, r += LeafCount - 1; l <= r; l = (l + 1) >> 1, r = (r - 1) >> 1)\n\
    \        {\n            if ((l & 1) == 1) lRes = Merge(lRes, Data[l]);\n     \
    \       if ((r & 1) == 0) rRes = Merge(Data[r], rRes);\n        }\n        return\
    \ Merge(lRes, rRes);\n    }\n}\n"
  dependsOn: []
  extendedDependsOn: []
  extendedRequiredBy:
  - icon: ':heavy_check_mark:'
    path: examples/csharpscript/segment_tree.point_set_range_composite.test.csx
    title: examples/csharpscript/segment_tree.point_set_range_composite.test.csx
  - icon: ':heavy_check_mark:'
    path: examples/csharpscript/segment_tree.range_sum_query.test.csx
    title: examples/csharpscript/segment_tree.range_sum_query.test.csx
  - icon: ':heavy_check_mark:'
    path: examples/csharpscript/segment_tree.range_minimum_query.test.csx
    title: examples/csharpscript/segment_tree.range_minimum_query.test.csx
  extendedVerifiedWith: []
  isVerificationFile: false
  path: examples/csharpscript/segment_tree.csx
  requiredBy:
  - examples/csharpscript/segment_tree.point_set_range_composite.test.csx
  - examples/csharpscript/segment_tree.range_sum_query.test.csx
  - examples/csharpscript/segment_tree.range_minimum_query.test.csx
  timestamp: '2020-02-16 04:32:52+09:00'
  verificationStatus: LIBRARY_NO_TESTS
  verificationStatusIcon: ':warning:'
  verifiedWith: []
documentation_of: examples/csharpscript/segment_tree.csx
layout: document
redirect_from:
- /library/examples/csharpscript/segment_tree.csx
- /library/examples/csharpscript/segment_tree.csx.html
title: examples/csharpscript/segment_tree.csx
---
