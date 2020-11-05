class UnionFindTree:
    def __init__(self, n):
        """
        Initialize the graph

        Args:
            self: (todo): write your description
            n: (int): write your description
        """
        self.par = list(range(n))  # parent
        self.rank = [0] * n  # depth of tree

    def find(self, x):
        """
        Find a value of x

        Args:
            self: (todo): write your description
            x: (todo): write your description
        """
        if self.par[x] == x:
            return x
        else:
            self.par[x] = self.find(self.par[x])
            return self.par[x]

    def unite(self, x, y):
        """
        Unite the given position.

        Args:
            self: (todo): write your description
            x: (todo): write your description
            y: (todo): write your description
        """
        x, y = self.find(x), self.find(y)
        if x == y:
            return
        if self.rank[x] < self.rank[y]:
            self.par[x] = y
        else:
            self.par[y] = x
            if self.rank[x] == self.rank[y]:
                self.rank[x] += 1

    def is_same(self, x, y):
        """
        Return true if x is the same.

        Args:
            self: (todo): write your description
            x: (array): write your description
            y: (array): write your description
        """
        return self.find(x) == self.find(y)
