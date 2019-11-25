# 競プロライブラリ verify 用 すごい CI script (WIP)

## 使い方

### インストール

``` console
$ pip3 install git+https://github.com/kmyk/online-judge-verify-helper
```

### 実行

まず `.test.cpp` という拡張子を持つ C++ のファイルを作って、その中で [Aizu Online Judge](http://judge.u-aizu.ac.jp/onlinejudge/) や [Library Checker](https://judge.yosupo.jp/) の問題の URL を `#define PROBLEM "URL"` のように指定しておきます  (例: [example.test.cpp](https://github.com/kmyk/online-judge-verify-helper/blob/master/example.test.cpp))。
そして `oj-verify run` を実行すると、そのようなファイルを自動で検出し、指定された問題に対し AC を得るかどうかを自動で判定してくれます。

`oj-verify init` を実行すると `.github/workflow/verify.yml` というファイルが作られます。
これを commit して GitHub に push しておくと、以後なにか push するたびに毎回自動で verify をしてくれます。
加えて readme に `[![Actions Status](https://github.com/kmyk/online-judge-verify-helper/workflows/verify/badge.svg)](https://github.com/kmyk/online-judge-verify-helper/actions)` のように書いておくと [![Actions Status](https://github.com/kmyk/online-judge-verify-helper/workflows/verify/badge.svg)](https://github.com/kmyk/online-judge-verify-helper/actions) のようなバッチが貼られ、verify に成功したかが簡単に確認できます。

まとめると、以下を実行すればよいということになります。

``` console
$ wget https://raw.githubusercontent.com/kmyk/online-judge-verify-helper/master/example.test.cpp
$ oj-verify run
$ oj-verify init
$ git add .github/workflow/verify.yml
$ git commit -m "Add .github/workflow/verify.yml"
$ git push origin master
```
