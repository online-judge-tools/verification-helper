when not declared(EXAMPLES_UNION_FIND_TREE_NIM):
  const EXAMPLES_UNION_FIND_TREE_NIM = true
  import sequtils
  import "examples/nim/hoge.nim"
  
  # @brief a Union-Find Tree
  # @note most operations in $O(\alpha(n))$ where $\alpha(n)$ is the inverse of Ackermann function
  # @note implemented with union-by-size + path-compression
  
  type UnionFindTree = object
    data:seq[int]
  
  proc initUnionFindTree*(n:int):UnionFindTree = UnionFindTree(data:newSeqWith(n, -1))
  
  proc isRoot*(self: UnionFindTree, i:int):bool = return self.data[i] < 0
  proc findRoot*(self: var UnionFindTree, i:int):int =
    if self.is_root(i):
      return i
    else:
      self.data[i] = self.findRoot(self.data[i])
      return self.data[i]
  proc treeSize*(self: var UnionFindTree, i:int):int = - self.data[self.findRoot(i)]
  proc uniteTrees*(self: var UnionFindTree, i, j:int):int {.discardable.} =
    var 
      i = self.findRoot(i)
      j = self.findRoot(j)
    if i != j:
      if self.tree_size(i) < self.tree_size(j): swap(i, j)
      self.data[i] += self.data[j]
      self.data[j] = i
    return i
  
  proc isSame*(self: var UnionFindTree, i, j:int):bool = self.find_root(i) == self.find_root(j)

  proc hoge*() = echo "Hello World"
