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


# :heavy_check_mark: examples/circle.awk

<a href="../../index.html">Back to top page</a>

* category: <a href="../../index.html#bfebe34154a0dfd9fc7b447fc9ed74e9">examples</a>
* <a href="{{ site.github.repository_url }}/blob/master/examples/circle.awk">View this file on GitHub</a>
    - Last commit date: 2020-01-24 05:02:31+09:00




## Verified with

* :heavy_check_mark: <a href="../../verify/examples/circle.test.awk.html">examples/circle.test.awk</a>


## Code

<a id="unbundled"></a>
{% raw %}
```cpp
function get_area(r) {
    return 3.1415926535 * r * r;
}

function get_circumference(r) {
    return 2 * 3.1415926535 * r;
}

```
{% endraw %}

<a id="bundled"></a>
{% raw %}
```cpp
#line 1 "examples/circle.awk"
function get_area(r) {
    return 3.1415926535 * r * r;
}

function get_circumference(r) {
    return 2 * 3.1415926535 * r;
}

```
{% endraw %}

<a href="../../index.html">Back to top page</a>

