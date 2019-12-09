---
layout: default
---

<!-- mathjax config similar to math.stackexchange -->
<script type="text/javascript" async
  src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-MML-AM_CHTML">
</script>
<script type="text/x-mathjax-config">
  MathJax.Hub.Config({
    TeX: { equationNumbers: { autoNumber: "AMS" }},
    tex2jax: {
      inlineMath: [ ['$','$'] ],
      processEscapes: true
    },
    "HTML-CSS": { matchFontHeight: false },
    displayAlign: "left",
    displayIndent: "2em"
  });
</script>

<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/jquery-balloon-js@1.1.2/jquery.balloon.min.js" integrity="sha256-ZEYs9VrgAeNuPvs15E39OsyOJaIkXEEt10fzxJ20+2I=" crossorigin="anonymous"></script>
<script type="text/javascript" src="assets/js/copy-button.js"></script>
<link rel="stylesheet" href="assets/css/copy-button.css" />


# ライブラリの HTML ビルドテスト

ここに書いた内容がトップページに足されます

* this unordered seed list will be replaced by toc as unordered list
{:toc}

## Library Files
### examples
* :heavy_check_mark: [examples/macros.hpp](library/examples/macros.hpp.html)
* :heavy_check_mark: [examples/monoids.hpp](library/examples/monoids.hpp.html)
* :warning: [examples/not_verified.hpp](library/examples/not_verified.hpp.html)
* :heavy_check_mark: [a segment tree](library/examples/segment_tree.hpp.html)
* :heavy_check_mark: [a disjoint set structure](library/examples/union_find_tree.hpp.html)


## Verify Files
* :heavy_check_mark: [example.test.cpp](verify/example.test.cpp.html)
* :heavy_check_mark: [examples/include_relative.test.cpp](verify/examples/include_relative.test.cpp.html)
* :heavy_check_mark: [examples/segment_tree.point_set_range_composite.test.cpp](verify/examples/segment_tree.point_set_range_composite.test.cpp.html)
* :heavy_check_mark: [examples/segment_tree.range_minimum_query.test.cpp](verify/examples/segment_tree.range_minimum_query.test.cpp.html)
* :heavy_check_mark: [examples/segment_tree.range_sum_query.test.cpp](verify/examples/segment_tree.range_sum_query.test.cpp.html)
* :heavy_check_mark: [examples/union_find_tree.aoj.test.cpp](verify/examples/union_find_tree.aoj.test.cpp.html)
* :heavy_check_mark: [examples/union_find_tree.yosupo.test.cpp](verify/examples/union_find_tree.yosupo.test.cpp.html)


