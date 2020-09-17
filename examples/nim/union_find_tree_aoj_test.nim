# verification-helper: PROBLEM https://onlinejudge.u-aizu.ac.jp/courses/library/3/DSL/all/DSL_1_A

include "examples/nim/headers.nim"
import "examples/nim/union_find_tree.nim" except hoge
include "examples/nim/union_find_tree.nim"
include "examples/nim/union_find_tree.nim"
include "examples/nim/union_find_tree.nim"
include "examples/nim/union_find_tree.nim"

let
  n, q = nextInt()
var uft = initUnionFindTree(n)
for i in 0..<q:
  let com, x, y = nextInt()
  if com == 0:
    uft.unite_trees(x, y)
  elif com == 1:
    echo if uft.is_same(x, y): 1 else: 0
