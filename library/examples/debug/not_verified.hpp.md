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
<script type="text/javascript" src="../../../assets/js/copy-button.js"></script>
<link rel="stylesheet" href="../../../assets/css/copy-button.css" />


# :warning: examples/debug/not_verified.hpp

<a href="../../../index.html">Back to top page</a>

* category: <a href="../../../index.html#6ffb1fe84ae4530240b8799246bff2fd">examples/debug</a>
* <a href="{{ site.github.repository_url }}/blob/master/examples/debug/not_verified.hpp">View this file on GitHub</a>
    - Last commit date: 2020-02-28 16:19:20+09:00




## Code

<a id="unbundled"></a>
{% raw %}
```cpp
#pragma once

inline string get_the_proof_of_P_equal_NP() {
    while (true) {
    }
}

```
{% endraw %}

<a id="bundled"></a>
{% raw %}
```cpp
#line 2 "examples/debug/not_verified.hpp"

inline string get_the_proof_of_P_equal_NP() {
    while (true) {
    }
}

```
{% endraw %}

<a href="../../../index.html">Back to top page</a>

