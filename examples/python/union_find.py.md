---
data:
  _extendedDependsOn: []
  _extendedRequiredBy: []
  _extendedVerifiedWith:
  - icon: ':heavy_check_mark:'
    path: examples/python/union_find_aoj.test.py
    title: examples/python/union_find_aoj.test.py
  - icon: ':heavy_check_mark:'
    path: examples/python/union_find_yosupo.test.py
    title: examples/python/union_find_yosupo.test.py
  _pathExtension: py
  _verificationStatusIcon: ':heavy_check_mark:'
  attributes:
    links: []
  bundledCode: "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.9.1/x64/lib/python3.9/site-packages/onlinejudge_verify/documentation/build.py\"\
    , line 71, in _render_source_code_stat\n    bundled_code = language.bundle(stat.path,\
    \ basedir=basedir, options={'include_paths': [basedir]}).decode()\n  File \"/opt/hostedtoolcache/Python/3.9.1/x64/lib/python3.9/site-packages/onlinejudge_verify/languages/python.py\"\
    , line 85, in bundle\n    raise NotImplementedError\nNotImplementedError\n"
  code: "class UnionFindTree:\n    def __init__(self, n):\n        self.par = list(range(n))\
    \  # parent\n        self.rank = [0] * n  # depth of tree\n\n    def find(self,\
    \ x):\n        if self.par[x] == x:\n            return x\n        else:\n   \
    \         self.par[x] = self.find(self.par[x])\n            return self.par[x]\n\
    \n    def unite(self, x, y):\n        x, y = self.find(x), self.find(y)\n    \
    \    if x == y:\n            return\n        if self.rank[x] < self.rank[y]:\n\
    \            self.par[x] = y\n        else:\n            self.par[y] = x\n   \
    \         if self.rank[x] == self.rank[y]:\n                self.rank[x] += 1\n\
    \n    def is_same(self, x, y):\n        return self.find(x) == self.find(y)\n"
  dependsOn: []
  isVerificationFile: false
  path: examples/python/union_find.py
  requiredBy: []
  timestamp: '2020-08-09 17:15:45+09:00'
  verificationStatus: LIBRARY_ALL_AC
  verifiedWith:
  - examples/python/union_find_yosupo.test.py
  - examples/python/union_find_aoj.test.py
documentation_of: examples/python/union_find.py
layout: document
redirect_from:
- /library/examples/python/union_find.py
- /library/examples/python/union_find.py.html
title: examples/python/union_find.py
---
