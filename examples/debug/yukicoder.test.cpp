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
