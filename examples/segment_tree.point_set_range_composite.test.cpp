#define PROBLEM "https://judge.yosupo.jp/problem/point_set_range_composite"
#include <cstdint>
#include <iostream>
#include <tuple>
#include <utility>
#include "examples/segment_tree.hpp"
#include "examples/macros.hpp"
using namespace std;

template <int32_t MOD>
struct linear_function_monoid {
    typedef pair<int64_t, int64_t> value_type;
    value_type unit() const {
        return make_pair(1, 0);
    }
    value_type mult(value_type g, value_type f) const {
        int64_t a = (f.first * g.first) % MOD;
        int64_t b = (f.first * g.second + f.second) % MOD;
        return make_pair(a, b);
    }
};

constexpr int32_t MOD = 998244353;
int main() {
    int n, q; cin >> n >> q;
    segment_tree<linear_function_monoid<MOD> > segtree(n);
    REP (i, n) {
        int64_t a, b; cin >> a >> b;
        segtree.point_set(i, make_pair(a, b));
    }
    REP (i, q) {
        int f, x, y, z; cin >> f >> x >> y >> z;
        if (f == 0) {
            segtree.point_set(x, make_pair(y, z));
        } else if (f == 1) {
            int64_t a, b; tie(a, b) = segtree.range_concat(x, y);
            cout << (a * z + b) % MOD << endl;
        }
    }
    return 0;
}
