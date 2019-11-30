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


# :warning: examples/monoids.hpp
* category: examples


[Back to top page](../../index.html)



## Verified
* :warning: [examples/segment_tree.range_minimum_query.test.cpp](../../verify/examples/segment_tree.range_minimum_query.test.cpp.html)
* :warning: [examples/segment_tree.range_sum_query.test.cpp](../../verify/examples/segment_tree.range_sum_query.test.cpp.html)


## Code
```cpp
#pragma once
#include <algorithm>
#include <cstdint>

struct plus_monoid {
    typedef int64_t value_type;
    value_type unit() const { return 0; }
    value_type mult(value_type a, value_type b) const { return a + b; }
};

struct max_monoid {
    typedef int64_t value_type;
    value_type unit() const { return INT64_MIN; }
    value_type mult(value_type a, value_type b) const { return std::max(a, b); }
};

struct min_monoid {
    typedef int64_t value_type;
    value_type unit() const { return INT64_MAX; }
    value_type mult(value_type a, value_type b) const { return std::min(a, b); }
};

```

[Back to top page](../../index.html)

