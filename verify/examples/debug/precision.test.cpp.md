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


# :heavy_check_mark: examples/debug/precision.test.cpp

<a href="../../../index.html">Back to top page</a>

* category: <a href="../../../index.html#6ffb1fe84ae4530240b8799246bff2fd">examples/debug</a>
* <a href="{{ site.github.repository_url }}/blob/master/examples/debug/precision.test.cpp">View this file on GitHub</a>
    - Last commit date: 2020-02-28 16:21:27+09:00


* see: <a href="http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ALDS1_15_B">http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ALDS1_15_B</a>


## Code

<a id="unbundled"></a>
{% raw %}
```cpp
#define PROBLEM "http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ALDS1_15_B"

#include <iostream>
#include <iomanip>
#include <vector>
#include <algorithm>

using namespace std;

#define ERROR "1e-6"

int main() {
  using D = double;
  int n,w;
  cin>>n>>w;
  vector<D> vs(n),ws(n);
  for(int i=0;i<n;i++) cin>>vs[i]>>ws[i];

  using P = pair<D, int>;
  vector<P> vp;
  for(int i=0;i<n;i++)
    vp.emplace_back(vs[i]/ws[i],i);

  sort(vp.rbegin(),vp.rend());

  D ans=0,res=w;
  for(auto p:vp){
    D amount=min(ws[p.second],res);
    res-=amount;
    ans+=amount*p.first;
  }

  cout<<fixed<<setprecision(12)<<ans<<endl;
  return 0;
}

```
{% endraw %}

<a id="bundled"></a>
{% raw %}
```cpp
#line 1 "examples/debug/precision.test.cpp"
#define PROBLEM "http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ALDS1_15_B"

#include <iostream>
#include <iomanip>
#include <vector>
#include <algorithm>

using namespace std;

#define ERROR "1e-6"

int main() {
  using D = double;
  int n,w;
  cin>>n>>w;
  vector<D> vs(n),ws(n);
  for(int i=0;i<n;i++) cin>>vs[i]>>ws[i];

  using P = pair<D, int>;
  vector<P> vp;
  for(int i=0;i<n;i++)
    vp.emplace_back(vs[i]/ws[i],i);

  sort(vp.rbegin(),vp.rend());

  D ans=0,res=w;
  for(auto p:vp){
    D amount=min(ws[p.second],res);
    res-=amount;
    ans+=amount*p.first;
  }

  cout<<fixed<<setprecision(12)<<ans<<endl;
  return 0;
}

```
{% endraw %}

<a href="../../../index.html">Back to top page</a>

