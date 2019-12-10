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
<script type="text/javascript" src="../../assets/js/copy-button.js"></script>
<link rel="stylesheet" href="../../assets/css/copy-button.css" />


# :heavy_check_mark: examples/macros.hpp
<a href="../../index.html">Back to top page</a>

* category: examples
* <a href="{{ site.github.repository_url }}/blob/master/examples/macros.hpp">View this file on GitHub</a> (Last commit date: 2019-11-29 11:28:05 +0900)




## Verified
* :heavy_check_mark: <a href="../../verify/examples/include_relative.test.cpp.html">examples/include_relative.test.cpp</a>
* :heavy_check_mark: <a href="../../verify/examples/segment_tree.point_set_range_composite.test.cpp.html">examples/segment_tree.point_set_range_composite.test.cpp</a>
* :heavy_check_mark: <a href="../../verify/examples/segment_tree.range_minimum_query.test.cpp.html">examples/segment_tree.range_minimum_query.test.cpp</a>
* :heavy_check_mark: <a href="../../verify/examples/segment_tree.range_sum_query.test.cpp.html">examples/segment_tree.range_sum_query.test.cpp</a>
* :heavy_check_mark: <a href="../../verify/examples/union_find_tree.aoj.test.cpp.html">examples/union_find_tree.aoj.test.cpp</a>
* :heavy_check_mark: <a href="../../verify/examples/union_find_tree.yosupo.test.cpp.html">examples/union_find_tree.yosupo.test.cpp</a>


## Code
{% raw %}
```cpp
#pragma once
#define REP(i, n) for (int i = 0; (i) < (int)(n); ++ (i))
#define REP3(i, m, n) for (int i = (m); (i) < (int)(n); ++ (i))
#define REP_R(i, n) for (int i = (int)(n) - 1; (i) >= 0; -- (i))
#define REP3R(i, m, n) for (int i = (int)(n) - 1; (i) >= (int)(m); -- (i))
#define ALL(x) begin(x), end(x)

```
{% endraw %}

<a href="../../index.html">Back to top page</a>

