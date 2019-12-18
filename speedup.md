# 高速化について

デフォルトでは有効になっていない高速化の設定がいくつかあります。
これらを説明します。
なおこれらがデフォルトでない理由は、どれも基本的にすこし不安定になりがちであり、たいていのユーザにとっては速度よりも安定性の方がうれしいはずだからです。

## 単一 job 内の並列実行

遊んでいる CPU にも仕事をさせましょう。
`oj-verify all --jobs 2` などのように `--jobs` オプションを用いることでテストが $N$ 並列で実行されます。
GitHub Actions 上の環境は $2$ コアなので `--jobs 2` とするとよいです。verify の実行部分が $2$ 倍速になります。$3$ 以上を指定してもあまり効果は期待できません。

[GitHubホストランナーの仮想環境 - GitHub ヘルプ](https://help.github.com/ja/actions/automating-your-workflow-with-github-actions/virtual-environments-for-github-hosted-runners#supported-runners-and-hardware-resources)

### 設定方法

1.  `.github/workflows/verify.yml` 中の `oj-verify all` を `oj-verify all --jobs 2` で置き換える

## cache アクションの利用

テストケースの取得には時間がかかります。たとえば API を連続で叩きすぎて迷惑をかけないように適度に sleep を挟んだりしているためです。
しかしテストケースは毎回同じなので、キャッシュをしておけば取得を省略できて全体でだいたい $2$ 倍速ぐらいになると思います。

[依存関係をキャッシュしてワークフローのスピードを上げる - GitHub ヘルプ](https://help.github.com/ja/actions/automating-your-workflow-with-github-actions/caching-dependencies-to-speed-up-workflows)

### 設定方法

1.  WIP: `.github/workflows/verify.yml` に適切な設定をする。<https://github.com/beet-aizu/library/pull/9> のあたりが参考になります

## 複数 jobs の並列実行

GitHub Actions では jobs を $20$ 個まで (学生や Pro だと $40$ 個まで) 同時実行できます。
これを使えばそのまま $20$ 倍速になります。

[GitHub Actionsについて - GitHub ヘルプ](https://help.github.com/ja/actions/automating-your-workflow-with-github-actions/about-github-actions#usage-limits)

### 設定方法

1.  WIP: `oj-verify run foo.test.cpp` と `oj-verify run bar.test.cpp` を同時に実行しても `.verify-helper/timestamps.*.json` が壊れないように修正するプルリクを出す。たぶん <https://github.com/benediktschmitt/py-filelock> みたいなのを使う
1.  WIP: `.github/workflows/verify.yml` に適切な設定をする。ファイル名の hash 値 $\bmod 20$ とかで振り分けて並列実行して最後にまとめて commit して push するとかを書かないとだめ
