#define PROBLEM "https://judge.yosupo.jp/problem/unionfind"
#include <iostream>
#include "examples/union_find_tree.hpp"
#include "examples/macros.hpp"
using namespace std;

int main() {
    int n, q; cin >> n >> q;
    union_find_tree uft(n);
    REP (i, q) {
        int t, u, v; cin >> t >> u >> v;
        if (t == 0) {
            uft.unite_trees(u, v);
        } else if (t == 1) {
            cout << uft.is_same(u, v) << endl;
        }
    }
    return 0;
}
