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
<script type="text/javascript" src="../../assets/js/copy-button.js"></script>
<link rel="stylesheet" href="../../assets/css/copy-button.css" />


# :warning: examples/macros.hpp
* category: examples


[Back to top page](../../index.html)



## Verified
* :warning: [examples/segment_tree.point_set_range_composite.test.cpp](../../verify/examples/segment_tree.point_set_range_composite.test.cpp.html)
* :warning: [examples/segment_tree.range_minimum_query.test.cpp](../../verify/examples/segment_tree.range_minimum_query.test.cpp.html)
* :warning: [examples/segment_tree.range_sum_query.test.cpp](../../verify/examples/segment_tree.range_sum_query.test.cpp.html)
* :warning: [examples/union_find_tree.aoj.test.cpp](../../verify/examples/union_find_tree.aoj.test.cpp.html)
* :warning: [examples/union_find_tree.yosupo.test.cpp](../../verify/examples/union_find_tree.yosupo.test.cpp.html)


## Code
```cpp
#pragma once
#define REP(i, n) for (int i = 0; (i) < (int)(n); ++ (i))
#define REP3(i, m, n) for (int i = (m); (i) < (int)(n); ++ (i))
#define REP_R(i, n) for (int i = (int)(n) - 1; (i) >= 0; -- (i))
#define REP3R(i, m, n) for (int i = (int)(n) - 1; (i) >= (int)(m); -- (i))
#define ALL(x) begin(x), end(x)

```

[Back to top page](../../index.html)

