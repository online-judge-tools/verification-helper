# Online Judge Verify Helper

[![Actions Status](https://github.com/kmyk/online-judge-verify-helper/workflows/verify/badge.svg)](https://github.com/kmyk/online-judge-verify-helper/actions)
[![GitHub Pages](https://img.shields.io/static/v1?label=GitHub+Pages&message=+&color=brightgreen&logo=github)](https://kmyk.github.io/online-judge-verify-helper/)
[![PyPI](https://img.shields.io/pypi/v/online-judge-verify-helper)](https://pypi.org/project/online-judge-verify-helper/)
[![LICENSE](https://img.shields.io/pypi/l/online-judge-verify-helper.svg)](https://github.com/kmyk/online-judge-verify-helper/blob/master/LICENSE)

[README in English](README.md)

## なにこれ

競プロライブラリの verify をお手軽に自動化するためのツールです。

## 使い方

### 競プロライブラリのリポジトリに設定する

これ読んで: <https://kmyk.github.io/online-judge-verify-helper/installer.html>

### 手元で実行する

#### インストール

``` console
$ pip3 install online-judge-verify-helper
```

Python のバージョンは 3.6 以上が必要です。

#### verify 自動実行

まず `.test.cpp` という拡張子の名前のファイルに `#define PROBLEM "https://judge.yosupo.jp/problem/unionfind"` のような形で verify 用問題の URL を書いておきます。このとき、次のコマンドで verify できているかを確認してくれます。

``` console
$ oj-verify run
```

利用できる問題は主に [Library Checker](https://judge.yosupo.jp/) の問題と [Aizu Online Judge](https://onlinejudge.u-aizu.ac.jp/home) の問題です。
[HackerRank](https://www.hackerrank.com/) の問題もたぶん動きますが保証はしません。
その他サービスについてはテストケースが利用できる形で公開されていないために対応していません。

#### `#include` の自動展開

与えられたファイル中の `#include "foo.hpp"` の形の include 文を展開して出力します。
JavaScript で言うところの [webpack](https://webpack.js.org/) のような機能であり、ファイル分割をしても実際のオンラインジャッジへの提出が困難にならないようにするために存在しています。
以下のように実行します。

``` console
$ oj-bundle main.cpp
```

競プロライブラリのディレクトリの外側にいる状態で実行する場合は `-I path/to/your/library` のように指定してください。`alias oj-bundle='\oj-bundle -I path/to/your/library'` のようなシェルのエイリアスを貼っておくのがおすすめです。

`#pragma once` などの [include guard](https://ja.wikibooks.org/wiki/More_C%2B%2B_Idioms/%E3%82%A4%E3%83%B3%E3%82%AF%E3%83%AB%E3%83%BC%E3%83%89%E3%82%AC%E3%83%BC%E3%83%89%E3%83%9E%E3%82%AF%E3%83%AD%28Include_Guard_Macro%29) に部分的に対応しています。複数回の include の対象になっているが出力には一度のみ含まれてほしいようなファイルがあれば、その 1 行目に `#pragma once` と書いておいてください。

#### ドキュメント生成

以下のコマンドを実行すると `.verify-helper/markdown/` にドキュメントが生成されます。例: [https://kmyk.github.io/online-judge-verify-helper/ ![GitHub Pages](https://img.shields.io/static/v1?label=GitHub+Pages&message=+&color=brightgreen&logo=github)](https://kmyk.github.io/online-judge-verify-helper/)

``` console
$ oj-verify docs
```

ドキュメント生成時に [Doxygen](http://www.doxygen.jp/) 風のコメントが見つかれば、それらは自動で利用されます。詳しくは以下の表をご覧ください。

|タグ名|説明|備考|
|---|---|---|
|`@title`|タイトルとして使用されます。|`@title` が指定されていないとき、`@brief` が存在するならば、最初に登場する `@brief` 要素がタイトルとして使用されます。`@brief` も存在しないならば、ファイル名がタイトルになります。|
|`@category`|そのライブラリが属するカテゴリとして使用されます。|指定されていない場合、ディレクトリ名がカテゴリになります。|
|`@brief`|ライブラリの説明文として使用されます。|`@title` が指定されていないときは、最初に登場する `@brief` は説明文ではなくタイトルとして使用されます。|
|`@see`, `@sa`|このタグの直後に記載された文字列に対してリンクを張ります。参考にした Web ページなどがあるときに活用するとよいでしょう。|例: `@see https://example.com/`|
|`@docs`|説明文が長く `@brief` タグで対応することが難しい場合、説明文が書かれた Markdown ファイルへのパスを記載すると、説明文がドキュメントに反映されます。|例: `@docs path/to/markdown.md`|
|`@depends`|そのライブラリが依存している他のファイルをタグで明示的に記載したい場合に使用します。|C++ など一部の言語ではソフトウェア側で依存関係を自動で判定するため、記載する必要がない場合があります。|
|`@ignore`|ドキュメント生成の対象から除外します。||

また、TeX 記法の数式 (例: `$O(N \sum_i A_i)$`) の [MathJax](https://www.mathjax.org/) による表示にも対応しています。

## Tips

-   ライブラリを verify するための問題が見つからないときは他の人のライブラリを参考にするとよいでしょう。`online-judge-verify-helper` のユーザの一覧は <https://github.com/search?q=online-judge-verify-helper+path%3A.github> から見ることができます
-   ライブラリを verify するための問題がそれでも見つからないときは [Library Checker](https://judge.yosupo.jp/) に問題を追加してください
-   高速化したい場合は頑張れば全体で 100 倍速ぐらいにできます: <https://kmyk.github.io/online-judge-verify-helper/speedup.html>
-   GitHub Actions から online-judge-verify-helper を呼び出すといった通常想定される利用法においては MIT License に関する著作権表示は要求されません ([詳細](https://github.com/kmyk/online-judge-verify-helper/issues/34))
-   これはライブラリを効率良く verify するためのツールであり、コードの検査や整形をするためのツールではありません。必要なら [clang-format](https://clang.llvm.org/docs/ClangFormat.html) などの formatter や [cppcheck](http://cppcheck.sourceforge.net/) などの linter を利用してください
-   言語は C++ 以外でも利用可能です (例: [examples/circle.test.awk](https://github.com/kmyk/online-judge-verify-helper/tree/master/examples/circle.test.awk))。`.verify-helper/config.toml` というファイルを作ってコンパイルや実行のためのコマンドを書いてください (例: [.verify-helper/config.toml](https://github.com/kmyk/online-judge-verify-helper/blob/master/.verify-helper/config.toml))

## Authors

-   committer: [@kmyk](https://github.com/kmyk) (AtCoder: [kimiyuki](https://atcoder.jp/users/kimiyuki)): pip での配布や [online-judge-tools](https://github.com/kmyk/online-judge-tools) などその他の諸々の担当
-   committer: [@beet-aizu](https://github.com/beet-aizu) (AtCoder: [beet](https://atcoder.jp/users/beet)): verify 機能担当
-   committer: [@tsutaj](https://github.com/tsutaj) (AtCoder: [tsutaj](https://atcoder.jp/users/tsutaj)): documents 生成担当
