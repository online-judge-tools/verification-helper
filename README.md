# 競プロライブラリ verify 用 すごい CI script (WIP)

[![Actions Status](https://github.com/kmyk/online-judge-verify-helper/workflows/verify/badge.svg)](https://github.com/kmyk/online-judge-verify-helper/actions)
[![GitHub Pages](https://img.shields.io/static/v1?label=GitHub+Pages&message=+&color=brightgreen&logo=github)](https://kmyk.github.io/online-judge-verify-helper/)
[![PyPI](https://img.shields.io/pypi/v/online-judge-verify-helper)](https://pypi.org/project/online-judge-verify-helper/)
[![LICENSE](https://img.shields.io/pypi/l/online-judge-verify-helper.svg)](https://github.com/kmyk/online-judge-verify-helper/blob/master/LICENSE)

## 使い方

### 競プロライブラリのリポジトリに設定する

これ読んで: <https://kmyk.github.io/online-judge-verify-helper/installer.html>

### 手元で実行する

#### インストール

``` console
$ pip3 install online-judge-verify-helper
```

#### 実行

まず `.test.cpp` という拡張子の名前のファイルに `#define PROBLEM "https://judge.yosupo.jp/problem/unionfind"` のような形で verify 用問題の URL を書いておきます。このとき、次のコマンドで verify できているかを確認してくれます。

``` console
$ oj-verify run
```

#### ドキュメント生成

以下のコマンドを実行すると、ドキュメントが生成されます。例: <https://kmyk.github.io/online-judge-verify-helper/>

``` console
$ oj-verify docs
```

## License

MIT License

## Authors

-   committer: [@kmyk](https://github.com/kmyk) (AtCoder: [kimiyuki](https://atcoder.jp/users/kimiyuki)): pip での配布や [online-judge-tools](https://github.com/kmyk/online-judge-tools) などその他の諸々の担当
-   committer: [@beet-aizu](https://github.com/beet-aizu) (AtCoder: [beet](https://atcoder.jp/users/beet)): verify 機能担当
-   committer: [@tsutaj](https://github.com/tsutaj) (AtCoder: [Tsuta_J](https://atcoder.jp/users/Tsuta_J)): documents 生成担当
-   special thanks: [@yosupo06](http://github.com/yosupo06) (AtCoder: [yosupo](https://atcoder.jp/users/yosupo)): verify のためのオンラインジャッジ [Library Checker](https://judge.yosupo.jp/) を管理運用してくれている
