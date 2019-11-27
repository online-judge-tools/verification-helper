# 競プロライブラリ verify 用 すごい CI script (WIP)

## 使い方

### かんたん Web 上インストール

<https://kmyk.github.io/online-judge-verify-helper/>

### ターミナル上で実行

まず `oj-verify` コマンドを使えるようにします。
これには `pip3 install git+https://github.com/kmyk/online-judge-verify-helper` を実行します。

テストを書いていきましょう。
`.test.cpp` という拡張子を持つ C++ のファイルを作って、その中で [Aizu Online Judge](http://judge.u-aizu.ac.jp/onlinejudge/) や [Library Checker](https://judge.yosupo.jp/) の問題の URL を `#define PROBLEM "URL"` のように指定しておきます  (例: [example.test.cpp](https://github.com/kmyk/online-judge-verify-helper/blob/master/example.test.cpp))。
そして `oj-verify run` を実行すると、そのようなファイルを自動で検出し、指定された問題に対し AC を得るかどうかを自動で判定してくれます。

最後に GitHub 上で自動で verify してくれるように設定しましょう。
`oj-verify init` を実行すると `.github/workflow/verify.yml` というファイルが作られます。
これを commit して GitHub に push しておけば終了です。
以後なにか push するたびに毎回自動で verify をしてくれます。

まとめると、以下を実行すればよいということになります。

``` console
$ pip3 install git+https://github.com/kmyk/online-judge-verify-helper
$ wget https://raw.githubusercontent.com/kmyk/online-judge-verify-helper/master/example.test.cpp
$ oj-verify run
$ oj-verify init
$ git add .github/workflow/verify.yml
$ git add example.test.cpp
$ git commit -m "Add .github/workflow/verify.yml and example.test.cpp"
$ git push origin master
```

加えて `README.md` に `[![Actions Status](https://github.com/kmyk/online-judge-verify-helper/workflows/verify/badge.svg)](https://github.com/kmyk/online-judge-verify-helper/actions)` のように書いておくとよいでしょう。URL は適切に書き換えてください。
[![Actions Status](https://github.com/kmyk/online-judge-verify-helper/workflows/verify/badge.svg)](https://github.com/kmyk/online-judge-verify-helper/actions) のようなバッチが貼られ、verify に成功したかが簡単に確認できます。
