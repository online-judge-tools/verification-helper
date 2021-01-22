# online-judge-tools/verification-helper

[![Actions Status](https://github.com/online-judge-tools/verification-helper/workflows/verify/badge.svg)](https://github.com/kmyk/online-judge-verify-helper/actions)
[![GitHub Pages](https://img.shields.io/static/v1?label=GitHub+Pages&message=+&color=brightgreen&logo=github)](https://online-judge-tools.github.io/verification-helper/)
[![PyPI](https://img.shields.io/pypi/v/online-judge-verify-helper)](https://pypi.org/project/online-judge-verify-helper/)
[![LICENSE](https://img.shields.io/pypi/l/online-judge-verify-helper.svg)](https://github.com/online-judge-tools/verification-helper/blob/master/LICENSE)

[README 日本語バージョン](README.ja.md)

## What is this?

This is a tool to easily automate the verify process of your code library for competitive programming.

## How to use

### Set up the repository for the library

Please read this: <https://online-judge-tools.github.io/verification-helper/installer.html>

### Running the program

#### Installation

``` console
$ pip3 install online-judge-verify-helper
```

Python 3.6 or above is required.

#### Automating the verification

First, specify the problem URL to be used to verify the library in the file including `.test.` in its path (e.g. for C++, write `#define PROBLEM "https://judge.yosupo.jp/problem/unionfind"` in a file like `example.test.cpp`; see [the reference](https://online-judge-tools.github.io/verification-helper/document.html) for other languages). Then, run the following command to check if the verification can be performed.

``` console
$ oj-verify run
```

Currently, problems on [Library Checker](https://judge.yosupo.jp/) and [Aizu Online Judge](https://onlinejudge.u-aizu.ac.jp/home) are supported.
For the details, see [the reference](https://online-judge-tools.github.io/verification-helper/document.html).

#### Autoexpansion of `#include`s

The `include` statements in your files in the form of `#include "foo.hpp"` can be expanded,
similar to the functionality provided by [webpack](https://webpack.js.org) for JavaScript. This is to solve the problems that most online judges do not support submitting multiple files.
The function can be used by running the following command:

``` console
$ oj-bundle main.cpp
```

If your competitive programming library resides outside the current directory, please specify the flag in the form of `-I path/to/your/library`. I recommend make shell aliases like `alias oj-bundle='\oj-bundle -I path/to/your/library'`.

[Include guards](https://ja.wikibooks.org/wiki/More_C%2B%2B_Idioms/%E3%82%A4%E3%83%B3%E3%82%AF%E3%83%AB%E3%83%BC%E3%83%89%E3%82%AC%E3%83%BC%E3%83%89%E3%83%9E%E3%82%AF%E3%83%AD%28Include_Guard_Macro%29) like `#pragma once` are partially supported. If you have files that will be included multiple times but you only want them to appear once in the generated code, add `#pragma once` to the first line of the files.

#### Generating Documentation

Run the following command to generate documentation in `.verify-helper/markdown/`. Example: [https://online-judge-tools.github.io/verification-helper/ ![GitHub Pages](https://img.shields.io/static/v1?label=GitHub+Pages&message=+&color=brightgreen&logo=github)](https://online-judge-tools.github.io/verification-helper/)

``` console
$ oj-verify docs
```

If documentation generators like [Doxygen](http://www.doxygen.jp) are found when generating documentation, they will be automatically used.
TeX expressions like `$(N \sum_i A_i)$` are also supported by the [MathJax](https://www.mathjax.org/) library.
For the details, see [the reference](https://online-judge-tools.github.io/verification-helper/document.html).

## Tips

-   If you cannot find problems to verify your library, you can refer to other users' libraries. You can find all users of `online-judge-verify-helper` at <https://github.com/search?q=online-judge-verify-helper+path%3A.github>.
-   If you cannot find problems to verify your library anywhere, we suggest that you add a problem to [Library Checker](https://judge.yosupo.jp/). You can use [Hello World](http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_1_A) as a dummy problem to run your own stress tests.
-   You do not need to display the MIT License if you call `online-judge-verify-helper` from GitHub Actions ([Details, in Japanese](https://github.com/online-judge-tools/verification-helper/issues/34)).
-   This is tool to efficiently verify your library, not to check or prettify your code. If you need such functions, you can try formatters like [clang-format](https://clang.llvm.org/docs/ClangFormat.html) or linters like [cppcheck](http://cppcheck.sourceforge.net/).

## Authors

-   committer: [@kmyk](https://github.com/kmyk) (AtCoder: [kimiyuki](https://atcoder.jp/users/kimiyuki)): distribution on `pip` and miscellaneous tasks on [online-judge-tools](https://github.com/kmyk/online-judge-tools)
-   committer: [@beet-aizu](https://github.com/beet-aizu) (AtCoder: [beet](https://atcoder.jp/users/beet)): verify function
-   committer: [@tsutaj](https://github.com/tsutaj) (AtCoder: [tsutaj](https://atcoder.jp/users/tsutaj)): documents generation
