---
title: Segment Tree (generalized with monoids)
documentation_of: examples/segment_tree.hpp
---

## Operations

For a monoid $M = (M, \cdot, 1)$ and a list $a = (a_0, a_1, \dots, a _ {n - 1}) \in M^N$ of elements $M$ with the length $N$, a segment tree can process following operations with $O(\log N)$:

-   $\mathtt{point\unicode{95}set}(i, b)$: Update $a_i \gets b$
-   $\mathtt{range\unicode{95}get}(l, r)$: Calculate the product $a_l \cdot a _ {l + 1} \cdot \dots \cdot a _ {r - 1}$
