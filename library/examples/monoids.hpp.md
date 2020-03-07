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


# VerificationStatus.VERIFIED examples/monoids.hpp

<a href="../../index.html">Back to top page</a>

* category: <a href="../../index.html#bfebe34154a0dfd9fc7b447fc9ed74e9">examples</a>
* <a href="{{ site.github.repository_url }}/blob/master/examples/monoids.hpp">View this file on GitHub</a>
    - Last commit date: 2019-11-29 11:28:05+09:00




## Verified with

* :heavy_check_mark: <a href="../../verify/examples/segment_tree.range_minimum_query.test.cpp.html">examples/segment_tree.range_minimum_query.test.cpp</a>
* :heavy_check_mark: <a href="../../verify/examples/segment_tree.range_sum_query.test.cpp.html">examples/segment_tree.range_sum_query.test.cpp</a>


## Code

<a id="unbundled"></a>
{% raw %}
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
{% endraw %}

<a id="bundled"></a>
{% raw %}
```cpp
#line 2 "examples/monoids.hpp"
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
{% endraw %}

<a href="../../index.html">Back to top page</a>

