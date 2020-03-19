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
<script type="text/javascript" src="../../../../../../../../assets/js/copy-button.js"></script>
<link rel="stylesheet" href="../../../../../../../../assets/css/copy-button.css" />


# :heavy_check_mark: examples/debug/h/i/j/k/l/foo.hpp

<a href="../../../../../../../../index.html">Back to top page</a>

* category: <a href="../../../../../../../../index.html#0e490f8d9604c79efef385fa06283f64">examples/debug/h/i/j/k/l</a>
* <a href="{{ site.github.repository_url }}/blob/master/examples/debug/h/i/j/k/l/foo.hpp">View this file on GitHub</a>
    - Last commit date: 2020-03-19 16:25:51+09:00




## Depends on

* :heavy_check_mark: <a href="../../../../../relative_path.hpp.html">examples/debug/relative_path.hpp</a>


## Verified with

* :heavy_check_mark: <a href="../../../../../../../../verify/examples/debug/relative_path.test.cpp.html">examples/debug/relative_path.test.cpp</a>


## Code

<a id="unbundled"></a>
{% raw %}
```cpp
#pragma once
#include "../../../../../relative_path.hpp"
#include "../../../../../../debug/relative_path.hpp"

```
{% endraw %}

<a id="bundled"></a>
{% raw %}
```cpp
#line 2 "examples/debug/relative_path.hpp"
char *hello = "Hello World";
#line 4 "examples/debug/h/i/j/k/l/foo.hpp"

```
{% endraw %}

<a href="../../../../../../../../index.html">Back to top page</a>

