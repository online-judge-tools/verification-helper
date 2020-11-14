# Online Judge Verification Helper の細かい仕様

[English Version](https://online-judge-tools.github.io/verification-helper/document.html)

## 対応している言語

一覧表:

| 言語 | 認識される拡張子 | テストファイルだと認識されるパターン | 属性の指定方法 | 対応機能 (verify / bundle / doc) | ファイル例 |
|---|---|---|---|---|---|
| C++ | `.cpp` `.hpp` | `.test.cpp` | `#define [KEY] [VALUE]` | :heavy_check_mark: / :heavy_check_mark: / :heavy_check_mark: | [segment_tree.range_sum_query.test.cpp](https://github.com/online-judge-tools/verification-helper/blob/master/examples/segment_tree.range_sum_query.test.cpp) |
| C# script | `.csx` | `.test.csx` | `// verification-helper: [KEY] [VALUE]` | :heavy_check_mark: / :x: / :heavy_check_mark: | [segment_tree.range_sum_query.test.csx](https://github.com/online-judge-tools/verification-helper/blob/master/examples/csharpscript/segment_tree.range_sum_query.test.csx) |
| Nim | `.nim` | `_test.nim` | `# verification-helper: [KEY] [VALUE]` | :heavy_check_mark: / :x: / :heavy_check_mark: | [union_find_tree_yosupo_test.nim](https://github.com/online-judge-tools/verification-helper/blob/master/examples/nim/union_find_tree_yosupo_test.nim) |
| Python 3 | `.py` | `.test.py` | `# verification-helper: [KEY] [VALUE]` | :heavy_check_mark: / :x: / :heavy_check_mark: | [union_find_yosupo.test.py](https://github.com/online-judge-tools/verification-helper/blob/master/examples/python/union_find_yosupo.test.py) |
| Haskell | `.hs` | `.test.hs` | `-- verification-helper: [KEY] [VALUE]` | :heavy_check_mark: / :x: / :warning: | [HelloWorld.test.hs](https://github.com/online-judge-tools/verification-helper/blob/master/Examples2/Haskell/HelloWorld.test.hs) |
| Ruby | `.rb` | `.test.rb` | `# verification-helper: [KEY] [VALUE]` | :heavy_check_mark: / :x: / :warning: | [hello_world.test.rb](https://github.com/online-judge-tools/verification-helper/blob/master/examples/ruby/hello_world.test.rb) |
| Go | `.go` | `.test.go` | `// verification-helper: [KEY] [VALUE]` | :heavy_check_mark: / :x: / :warning: | [helloworld.test.go](https://github.com/online-judge-tools/verification-helper/blob/master/examples/go/helloworld.test.go) |
| Java | `.java` | `_test.java` | `// verification-helper: [KEY] [VALUE]` | :heavy_check_mark: / :x: / :warning: | [HelloWorld_test.java](https://github.com/online-judge-tools/verification-helper/blob/master/examples/java/HelloWorld_test.java) |

### C++ の設定

`.verify-helper/config.toml` というファイルを作って以下のように設定を書くと、コンパイラやそのオプションを指定できます。
設定がない場合は、自動でコンパイラ (`g++` と `clang++`) を検出し、おすすめのオプションを用いて実行されます。

``` toml
[[languages.cpp.environments]]
CXX = "g++"

[[languages.cpp.environments]]
CXX = "clang++"
CXXFLAGS = ["-std=c++17", "-Wall", "-g", "-fsanitize=undefined", "-D_GLIBCXX_DEBUG"]
```

-   [`ulimit`](https://linux.die.net/man/3/ulimit) が動作しないような環境では、自分で `CXXFLAGS` を設定する場合はスタックサイズに注意してください。
-   認識される拡張子は `.cpp` `.hpp` `.cc` `.h` のみです。`.c` や `.h++` のような拡張子のファイルや拡張子なしのファイルは認識されないことに注意してください。

### C# script の設定

設定項目はありません。
コンパイラには .NET Core が使われます。

-   いまのところ `.cs` という拡張子が認識されないことに注意してください ([#248](https://github.com/online-judge-tools/verification-helper/issues/248))。

### Nim の設定

`.verify-helper/config.toml` というファイルを作って以下のように設定を書くと、コンパイルの際に変換する言語 (例: `c`, `cpp`) やそのオプションを指定できます。
設定がない場合は AtCoder でのオプションに近いおすすめのオプションが指定されます。

``` toml
[[languages.nim.environments]]
compile_to = "c"

[[languages.nim.environments]]
compile_to = "cpp"
NIMFLAGS = ["--warning:on", "--opt:none"]
```

### Python 3 の設定

設定項目は特にありません。

### その他の言語の設定

上記以外の言語でも実行可能です (例: [examples/awk/circle.test.awk](https://github.com/online-judge-tools/verification-helper/blob/master/examples/awk/circle.test.awk))。
`.verify-helper/config.toml` というファイルを作って、以下のようにコンパイルや実行のためのコマンドを書いてください (例: [.verify-helper/config.toml](https://github.com/online-judge-tools/verification-helper/blob/master/.verify-helper/config.toml))。

``` toml
[languages.awk]
compile = "bash -c 'echo hello > {tempdir}/hello'"
execute = "env AWKPATH={basedir} awk -f {path}"
bundle = "false"
list_dependencies = "sed 's/^@include \"\\(.*\\)\"$/\\1/ ; t ; d' {path}"
```

## verify 自動実行

### 対応サービス一覧

|サービス名|備考|
|---|---|
| [Library Checker](https://judge.yosupo.jp/) | |
| [Aizu Online Judge](https://onlinejudge.u-aizu.ac.jp/home) | |
| [HackerRank](https://www.hackerrank.com/) | たぶん動きますが保証はしません。 |
| [yukicoder](https://yukicoder.me) | 環境変数 `YUKICODER_TOKEN` の設定が必要です。[ヘルプ - yukicoder](https://yukicoder.me/help) の「ログインしてないと使えない機能をAPIとして使いたい」の節や [暗号化されたシークレットの作成と利用 - GitHub ヘルプ](https://help.github.com/ja/actions/configuring-and-managing-workflows/creating-and-storing-encrypted-secrets#creating-encrypted-secrets) 参考にして設定してください。 |

これらの他サービスはテストケースを利用できる形で公開してくれていないため利用できません。

### 利用可能な属性

|変数名|説明|備考|
|---|---|---|
| `PROBLEM` | 提出する問題の URL を指定します | 必須 |
| `IGNORE` | これが定義されていれば verify は実行されません | `#ifdef __clang__` などで囲った中で指定することで特定の状況下でのみ実行を抑制することができます |
| `ERROR` | 許容誤差を指定します | |

## ドキュメント生成

### ソースコードのページへの Markdown の埋め込み

リポジトリ内に Markdown ファイルを置いておくと自動で認識されます。
[Front Matter](http://jekyllrb-ja.github.io/docs/front-matter/) 形式で `documentation_of` という項目にファイルを指定しておくと、指定したファイルについての生成されたドキュメント中に、Markdown ファイルの中身が挿入されます。

たとえば、`path/to/segment_tree.hpp` というファイルに説明を Markdown で追加したいときは `for/bar.md` などに次のように書きます。

```
---
title: Segment Tree
documentation_of: ./path/to/segment_tree.hpp
---

## 説明

このファイルでは、……
```

`documentation_of` 文字列は、`./` あるいは `..` から始まる場合は Markdown ファイルのパスからの相対パスであると認識されます。また、`//` から初まる場合は `.verify-helper` ディレクトリがある場所をルートとする絶対パスであると認識されます。
また、ディレクトリ区切り文字には `/` を使い、大文字小文字を正しく入力してください。


### トップページへの Markdown の埋め込み

`.verify-helper/docs/index.md` というファイルを作って、そこに Markdown で書いてください。

### ローカル実行

`.verify-helper/markdown/` ディレクトリ内で以下のようにコマンドを実行すると、生成されたドキュメントが <http://localhost:4000/> から確認できます。

``` console
$ bundle install --path .vendor/bundle
$ bundle exec jekyll serve
```

ただし Ruby の [Bundler](https://bundler.io/) が必要です。
これは Ubuntu であれば `sudo apt install ruby-bundler` などでインストールできます。

### その他の仕様

-   ファイル `.verify-helper/docs/_config.yml` を作成しておくと、いくつかの修正をした上で出力先ディレクトリにコピーされます。
-   ディレクトリ `.verify-helper/docs/static/` 以下にファイルを作成しておくと、ドキュメント出力先ディレクトリにそのままコピーされます。
