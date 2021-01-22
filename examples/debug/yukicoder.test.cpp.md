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
    PROBLEM: https://yukicoder.me/problems/3872
    links:
    - https://yukicoder.me/problems/3872
  bundledCode: "#line 1 \"examples/debug/yukicoder.test.cpp\"\n#define PROBLEM \"\
    https://yukicoder.me/problems/3872\"\n\n#include <bits/stdc++.h>\nusing namespace\
    \ std;\n\ntemplate<typename T> void drop(const T &x){cout<<x<<endl;exit(0);}\n\
    \nint mgcd(int a,int b){\n  while(b){\n    int c=a%b;\n    a=b;\n    b=c;\n  }\n\
    \  return a;\n}\n\nsigned main(){\n  int a,b;\n  cin>>a>>b;\n  if(mgcd(a,b)!=1)\
    \ drop(-1);\n\n  const int MAX = 1e4+10;\n  vector<int> ok(MAX,1);\n  for(int\
    \ i=0;i<MAX;i++)\n    for(int j=0;j<MAX;j++)\n      if(i*a+j*b<MAX) ok[i*a+j*b]=0;\n\
    \n  int ans=0;\n  for(int i=0;i<MAX;i++)\n    ans+=ok[i];\n  cout<<ans<<endl;\n\
    \  return 0;\n}\n"
  code: "#define PROBLEM \"https://yukicoder.me/problems/3872\"\n\n#include <bits/stdc++.h>\n\
    using namespace std;\n\ntemplate<typename T> void drop(const T &x){cout<<x<<endl;exit(0);}\n\
    \nint mgcd(int a,int b){\n  while(b){\n    int c=a%b;\n    a=b;\n    b=c;\n  }\n\
    \  return a;\n}\n\nsigned main(){\n  int a,b;\n  cin>>a>>b;\n  if(mgcd(a,b)!=1)\
    \ drop(-1);\n\n  const int MAX = 1e4+10;\n  vector<int> ok(MAX,1);\n  for(int\
    \ i=0;i<MAX;i++)\n    for(int j=0;j<MAX;j++)\n      if(i*a+j*b<MAX) ok[i*a+j*b]=0;\n\
    \n  int ans=0;\n  for(int i=0;i<MAX;i++)\n    ans+=ok[i];\n  cout<<ans<<endl;\n\
    \  return 0;\n}\n"
  dependsOn: []
  isVerificationFile: true
  path: examples/debug/yukicoder.test.cpp
  requiredBy: []
  timestamp: '2020-02-28 16:21:27+09:00'
  verificationStatus: TEST_ACCEPTED
  verifiedWith: []
documentation_of: examples/debug/yukicoder.test.cpp
layout: document
redirect_from:
- /verify/examples/debug/yukicoder.test.cpp
- /verify/examples/debug/yukicoder.test.cpp.html
title: examples/debug/yukicoder.test.cpp
---
