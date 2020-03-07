---
layout: default
---

<!-- mathjax config similar to math.stackexchange -->
<script type="text/javascript" async
  src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-MML-AM_CHTML">
</script>
<script type="text/x-mathjax-config">
  MathJax.Hub.Config({
    TeX: { equationNumbers: { autoNumber: "AMS" }},
    tex2jax: {
      inlineMath: [ ['$','$'] ],
      processEscapes: true
    },
    "HTML-CSS": { matchFontHeight: false },
    displayAlign: "left",
    displayIndent: "2em"
  });
</script>

<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/jquery-balloon-js@1.1.2/jquery.balloon.min.js" integrity="sha256-ZEYs9VrgAeNuPvs15E39OsyOJaIkXEEt10fzxJ20+2I=" crossorigin="anonymous"></script>
<script type="text/javascript" src="../../../assets/js/copy-button.js"></script>
<link rel="stylesheet" href="../../../assets/css/copy-button.css" />


# :heavy_check_mark: examples/debug/yukicoder.test.cpp

<a href="../../../index.html">Back to top page</a>

* category: <a href="../../../index.html#6ffb1fe84ae4530240b8799246bff2fd">examples/debug</a>
* <a href="{{ site.github.repository_url }}/blob/master/examples/debug/yukicoder.test.cpp">View this file on GitHub</a>
    - Last commit date: 2020-02-28 16:21:27+09:00


* see: <a href="https://yukicoder.me/problems/3872">https://yukicoder.me/problems/3872</a>


## Code

<a id="unbundled"></a>
{% raw %}
```cpp
#define PROBLEM "https://yukicoder.me/problems/3872"

#include <bits/stdc++.h>
using namespace std;

template<typename T> void drop(const T &x){cout<<x<<endl;exit(0);}

int mgcd(int a,int b){
  while(b){
    int c=a%b;
    a=b;
    b=c;
  }
  return a;
}

signed main(){
  int a,b;
  cin>>a>>b;
  if(mgcd(a,b)!=1) drop(-1);

  const int MAX = 1e4+10;
  vector<int> ok(MAX,1);
  for(int i=0;i<MAX;i++)
    for(int j=0;j<MAX;j++)
      if(i*a+j*b<MAX) ok[i*a+j*b]=0;

  int ans=0;
  for(int i=0;i<MAX;i++)
    ans+=ok[i];
  cout<<ans<<endl;
  return 0;
}

```
{% endraw %}

<a id="bundled"></a>
{% raw %}
```cpp
#line 1 "examples/debug/yukicoder.test.cpp"
#define PROBLEM "https://yukicoder.me/problems/3872"

#include <bits/stdc++.h>
using namespace std;

template<typename T> void drop(const T &x){cout<<x<<endl;exit(0);}

int mgcd(int a,int b){
  while(b){
    int c=a%b;
    a=b;
    b=c;
  }
  return a;
}

signed main(){
  int a,b;
  cin>>a>>b;
  if(mgcd(a,b)!=1) drop(-1);

  const int MAX = 1e4+10;
  vector<int> ok(MAX,1);
  for(int i=0;i<MAX;i++)
    for(int j=0;j<MAX;j++)
      if(i*a+j*b<MAX) ok[i*a+j*b]=0;

  int ans=0;
  for(int i=0;i<MAX;i++)
    ans+=ok[i];
  cout<<ans<<endl;
  return 0;
}

```
{% endraw %}

<a href="../../../index.html">Back to top page</a>

