#ifndef EXAMPLES_UNION_FIND_TREE_HPP
#define EXAMPLES_UNION_FIND_TREE_HPP
#include <algorithm>
#include <vector>

/**
 * @brief a Union-Find Tree
 * @note most operations in $O(\alpha(n))$ where $\alpha(n)$ is the inverse of Ackermann function
 * @note implemented with union-by-size + path-compression
 */
struct union_find_tree {
    std::vector<int> data;
    union_find_tree() = default;
    explicit union_find_tree(int n) : data(n, -1) {}
    bool is_root(int i) { return data[i] < 0; }
    int find_root(int i) { return is_root(i) ? i : (data[i] = find_root(data[i])); }
    int tree_size(int i) { return - data[find_root(i)]; }
    int unite_trees(int i, int j) {
        i = find_root(i); j = find_root(j);
        if (i != j) {
            if (tree_size(i) < tree_size(j)) std::swap(i, j);
            data[i] += data[j];
            data[j] = i;
        }
        return i;
    }
    bool is_same(int i, int j) { return find_root(i) == find_root(j); }
};

#endif
