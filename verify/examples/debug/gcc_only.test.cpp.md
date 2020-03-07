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


# :heavy_check_mark: examples/debug/gcc_only.test.cpp

<a href="../../../index.html">Back to top page</a>

* category: <a href="../../../index.html#6ffb1fe84ae4530240b8799246bff2fd">examples/debug</a>
* <a href="{{ site.github.repository_url }}/blob/master/examples/debug/gcc_only.test.cpp">View this file on GitHub</a>
    - Last commit date: 2020-02-28 16:21:27+09:00


* see: <a href="https://onlinejudge.u-aizu.ac.jp/courses/lesson/2/ITP1/1/ITP1_1_A">https://onlinejudge.u-aizu.ac.jp/courses/lesson/2/ITP1/1/ITP1_1_A</a>


## Code

<a id="unbundled"></a>
{% raw %}
```cpp
#ifdef __clang__
#define IGNORE
#else

#define PROBLEM "https://onlinejudge.u-aizu.ac.jp/courses/lesson/2/ITP1/1/ITP1_1_A"
#include <cstdio>

// clang++ says "error: C++ requires a type specifier for all declarations", but g++ doesn't
main() {
    printf("Hello World\n");
}

#endif

```
{% endraw %}

<a id="bundled"></a>
{% raw %}
```cpp
#line 1 "examples/debug/gcc_only.test.cpp"
#ifdef __clang__
#define IGNORE
#else

#define PROBLEM "https://onlinejudge.u-aizu.ac.jp/courses/lesson/2/ITP1/1/ITP1_1_A"
#include <cstdio>

// clang++ says "error: C++ requires a type specifier for all declarations", but g++ doesn't
main() {
    printf("Hello World\n");
}

#endif

```
{% endraw %}

<a href="../../../index.html">Back to top page</a>

