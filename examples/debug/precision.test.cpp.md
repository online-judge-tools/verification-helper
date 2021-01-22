---
data:
  _extendedDependsOn: []
  _extendedRequiredBy: []
  _extendedVerifiedWith: []
  _isVerificationFailed: false
  _pathExtension: cpp
  _verificationStatusIcon: ':heavy_check_mark:'
  attributes:
    '*NOT_SPECIAL_COMMENTS*': ''
    ERROR: 1e-6
    PROBLEM: http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ALDS1_15_B
    links:
    - http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ALDS1_15_B
  bundledCode: "#line 1 \"examples/debug/precision.test.cpp\"\n#define PROBLEM \"\
    http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ALDS1_15_B\"\n\n#include\
    \ <iostream>\n#include <iomanip>\n#include <vector>\n#include <algorithm>\n\n\
    using namespace std;\n\n#define ERROR \"1e-6\"\n\nint main() {\n  using D = double;\n\
    \  int n,w;\n  cin>>n>>w;\n  vector<D> vs(n),ws(n);\n  for(int i=0;i<n;i++) cin>>vs[i]>>ws[i];\n\
    \n  using P = pair<D, int>;\n  vector<P> vp;\n  for(int i=0;i<n;i++)\n    vp.emplace_back(vs[i]/ws[i],i);\n\
    \n  sort(vp.rbegin(),vp.rend());\n\n  D ans=0,res=w;\n  for(auto p:vp){\n    D\
    \ amount=min(ws[p.second],res);\n    res-=amount;\n    ans+=amount*p.first;\n\
    \  }\n\n  cout<<fixed<<setprecision(12)<<ans<<endl;\n  return 0;\n}\n"
  code: "#define PROBLEM \"http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ALDS1_15_B\"\
    \n\n#include <iostream>\n#include <iomanip>\n#include <vector>\n#include <algorithm>\n\
    \nusing namespace std;\n\n#define ERROR \"1e-6\"\n\nint main() {\n  using D =\
    \ double;\n  int n,w;\n  cin>>n>>w;\n  vector<D> vs(n),ws(n);\n  for(int i=0;i<n;i++)\
    \ cin>>vs[i]>>ws[i];\n\n  using P = pair<D, int>;\n  vector<P> vp;\n  for(int\
    \ i=0;i<n;i++)\n    vp.emplace_back(vs[i]/ws[i],i);\n\n  sort(vp.rbegin(),vp.rend());\n\
    \n  D ans=0,res=w;\n  for(auto p:vp){\n    D amount=min(ws[p.second],res);\n \
    \   res-=amount;\n    ans+=amount*p.first;\n  }\n\n  cout<<fixed<<setprecision(12)<<ans<<endl;\n\
    \  return 0;\n}\n"
  dependsOn: []
  isVerificationFile: true
  path: examples/debug/precision.test.cpp
  requiredBy: []
  timestamp: '2020-02-28 16:21:27+09:00'
  verificationStatus: TEST_ACCEPTED
  verifiedWith: []
documentation_of: examples/debug/precision.test.cpp
layout: document
redirect_from:
- /verify/examples/debug/precision.test.cpp
- /verify/examples/debug/precision.test.cpp.html
title: examples/debug/precision.test.cpp
---
