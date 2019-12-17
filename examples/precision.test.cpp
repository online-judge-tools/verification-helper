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
