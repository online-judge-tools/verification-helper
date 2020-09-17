# verification-helper: PROBLEM https://onlinejudge.u-aizu.ac.jp/courses/library/3/DSL/all/DSL_1_A
import sys
input = sys.stdin.buffer.readline

from examples.python.union_find import UnionFindTree


def main() -> None:
    N, Q = map(int, input().split())
    uft = UnionFindTree(N)
    for _ in range(Q):
        t, u, v = map(int, input().split())
        if t == 0:
            uft.unite(u, v)
        else:
            print(int(uft.is_same(u, v)))


if __name__ == "__main__":
    main()
