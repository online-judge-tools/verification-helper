# verification-helper: PROBLEM https://judge.yosupo.jp/problem/unionfind

include "examples/nim/headers.nim"
from examples/nim/union_find_tree import unite_trees, initUnionFindTree, is_same

let 
  n,q = nextInt()
var uft = initUnionFindTree(n)

for i in 0..<q:
  let t, u, v = nextInt()
  if t == 0:
    uft.unite_trees(u, v)
  elif t == 1:
    echo if uft.is_same(u, v): 1 else: 0
