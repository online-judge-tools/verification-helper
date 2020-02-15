#load "./segment_tree.csx"
#pragma PROBLEM https://judge.yosupo.jp/problem/point_set_range_composite

using System;
using System.Linq;

struct Linear
{
    const int MOD = 998244353;
    public long A;
    public long B;
    public Linear(long a, long b) { A = a; B = b; }
    public static Linear Merge(Linear a, Linear b) => new Linear(a.A * b.A % MOD, (a.B * b.A + b.B) % MOD);
    public long EvalWith(int x) => (A * x + B) % MOD;
    public override string ToString() => $"{A} {B}";
}

var nq = Console.ReadLine().Split().Select(int.Parse).ToArray();
var (n, q) = (nq[0], nq[1]);
SegmentTree<Linear> segTree = new SegmentTree<Linear>(n, new Linear(1, 0), Linear.Merge);

for (int i = 0; i < n; i++)
{
    var ab = Console.ReadLine().Split().Select(int.Parse).ToArray();
    segTree[i] = new Linear(ab[0], ab[1]);
}

for (int i = 0; i < q; i++)
{
    var query = Console.ReadLine().Split().Select(int.Parse).ToArray();
    if (query[0] == 0)
    {
        segTree[query[1]] = new Linear(query[2], query[3]);
    }
    else
    {
        Console.WriteLine(segTree[query[1]..query[2]].EvalWith(query[3]));
    }
}

