# Online Judge Verify Helper

[![Actions Status](https://github.com/kmyk/online-judge-verify-helper/workflows/verify/badge.svg)](https://github.com/kmyk/online-judge-verify-helper/actions)
[![GitHub Pages](https://img.shields.io/static/v1?label=GitHub+Pages&message=+&color=brightgreen&logo=github)](https://kmyk.github.io/online-judge-verify-helper/)
[![PyPI](https://img.shields.io/pypi/v/online-judge-verify-helper)](https://pypi.org/project/online-judge-verify-helper/)
[![LICENSE](https://img.shields.io/pypi/l/online-judge-verify-helper.svg)](https://github.com/kmyk/online-judge-verify-helper/blob/master/LICENSE)

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

#### verify 自動実行

まず `.test.cpp` という拡張子の名前のファイルに `#define PROBLEM "https://judge.yosupo.jp/problem/unionfind"` のような形で verify 用問題の URL を書いておきます。このとき、次のコマンドで verify できているかを確認してくれます。

``` console
$ oj-verify run
```

利用できる問題は主に [Library Checker](https://judge.yosupo.jp/) の問題と [Aizu Online Judge](https://onlinejudge.u-aizu.ac.jp/home) の問題です。
[HackerRank](https://www.hackerrank.com/) の問題もたぶん動きますが保証はしません。
その他サービスについてはテストケースが利用できる形で公開されていないために対応していません。

#### ドキュメント生成

以下のコマンドを実行すると、ドキュメントが生成されます。例: <https://kmyk.github.io/online-judge-verify-helper/> [![GitHub Pages](https://img.shields.io/static/v1?label=GitHub+Pages&message=+&color=brightgreen&logo=github)](https://kmyk.github.io/online-judge-verify-helper/)

``` console
$ oj-verify docs
```

ドキュメント生成時に [Doxygen](http://www.doxygen.jp/) 風のコメントが見つかれば、それらは自動で利用されます。
TeX 記法の数式 (例: `$O(N \sum_i A_i)$`) の MathJax による表示にも対応しています。
(TODO: どのようなコメントが認識されるかについてのドキュメントを書く)

## License

MIT License

## Authors

-   committer: [@kmyk](https://github.com/kmyk) (AtCoder: [kimiyuki](https://atcoder.jp/users/kimiyuki)): pip での配布や [online-judge-tools](https://github.com/kmyk/online-judge-tools) などその他の諸々の担当
-   committer: [@beet-aizu](https://github.com/beet-aizu) (AtCoder: [beet](https://atcoder.jp/users/beet)): verify 機能担当
-   committer: [@tsutaj](https://github.com/tsutaj) (AtCoder: [Tsuta_J](https://atcoder.jp/users/Tsuta_J)): documents 生成担当
-   special thanks: [@yosupo06](http://github.com/yosupo06) (AtCoder: [yosupo](https://atcoder.jp/users/yosupo)): verify のためのオンラインジャッジ [Library Checker](https://judge.yosupo.jp/) を管理運用してくれている
