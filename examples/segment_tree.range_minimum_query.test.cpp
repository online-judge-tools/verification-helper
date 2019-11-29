#define PROBLEM "https://onlinejudge.u-aizu.ac.jp/courses/library/3/DSL/all/DSL_2_A"
#include <iostream>
#include "examples/segment_tree.hpp"
#include "examples/monoids.hpp"
#include "examples/macros.hpp"
using namespace std;

int main() {
    int n, q; cin >> n >> q;
    segment_tree<min_monoid> segtree(n);
    REP (i, n) {
        segtree.point_set(i, (1u << 31) - 1);
    }
    REP (i, q) {
        int com, x, y; cin >> com >> x >> y;
        if (com == 0) {
            segtree.point_set(x, y);
        } else if (com == 1) {
            cout << segtree.range_concat(x, y + 1) << endl;
        }
    }
    return 0;
}
