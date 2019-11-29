#define PROBLEM "https://onlinejudge.u-aizu.ac.jp/courses/library/3/DSL/all/DSL_2_B"
#include <iostream>
#include "examples/segment_tree.hpp"
#include "examples/monoids.hpp"
#include "examples/macros.hpp"
using namespace std;

int main() {
    int n, q; cin >> n >> q;
    segment_tree<plus_monoid> segtree(n);
    REP (i, n) {
        segtree.point_set(i, 0);
    }
    REP (i, q) {
        int com, x, y; cin >> com >> x >> y;
        -- x;
        if (com == 0) {
            segtree.point_set(x, segtree.range_concat(x, x + 1) + y);
        } else if (com == 1) {
            cout << segtree.range_concat(x, y) << endl;
        }
    }
    return 0;
}
