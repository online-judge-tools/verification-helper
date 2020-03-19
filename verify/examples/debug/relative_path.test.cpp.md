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


# :heavy_check_mark: examples/debug/relative_path.test.cpp

<a href="../../../index.html">Back to top page</a>

* category: <a href="../../../index.html#6ffb1fe84ae4530240b8799246bff2fd">examples/debug</a>
* <a href="{{ site.github.repository_url }}/blob/master/examples/debug/relative_path.test.cpp">View this file on GitHub</a>
    - Last commit date: 2020-03-19 16:25:51+09:00


* see: <a href="http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_1_A">http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_1_A</a>


## Depends on

* :heavy_check_mark: <a href="../../../library/examples/debug/a/b/c/foo.hpp.html">examples/debug/a/b/c/foo.hpp</a>
* :heavy_check_mark: <a href="../../../library/examples/debug/d/e/f/g/foo.hpp.html">examples/debug/d/e/f/g/foo.hpp</a>
* :heavy_check_mark: <a href="../../../library/examples/debug/h/i/j/k/l/foo.hpp.html">examples/debug/h/i/j/k/l/foo.hpp</a>
* :heavy_check_mark: <a href="../../../library/examples/debug/relative_path.hpp.html">examples/debug/relative_path.hpp</a>


## Code

<a id="unbundled"></a>
{% raw %}
```cpp
#define PROBLEM "http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_1_A"
#include <cstdio>
#include "./a/b/c/foo.hpp"
#include "d/e/f/g/foo.hpp"
#include "examples/debug/h/i/j/k/l/foo.hpp"

int main() {
    printf("%s\n", hello);
    return 0;
}

```
{% endraw %}

<a id="bundled"></a>
{% raw %}
```cpp
#line 1 "examples/debug/relative_path.test.cpp"
#define PROBLEM "http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_1_A"
#include <cstdio>
#line 2 "examples/debug/relative_path.hpp"
char *hello = "Hello World";
#line 6 "examples/debug/relative_path.test.cpp"

int main() {
    printf("%s\n", hello);
    return 0;
}

```
{% endraw %}

<a href="../../../index.html">Back to top page</a>

