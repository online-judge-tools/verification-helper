# Online Judge Verify Helper の細かい仕様

[English Version](https://kmyk.github.io/online-judge-verify-helper/document.html)

## 対応している言語

一覧表:

| 言語 | コンパイラ | 対応機能 (verify / bundle / doc) | 例 |
|---|---|---|---|---|
| C++ | GCC / Clang | :heavy_check_mark: / :heavy_check_mark: / :heavy_check_mark: | [examples/segment_tree.range_sum_query.test.cpp](https://github.com/kmyk/online-judge-verify-helper/blob/master/examples/segment_tree.range_sum_query.test.cpp) |
| C# script | .NET Core | :heavy_check_mark: / :x: / :warning: | [examples/csharpscript/segment_tree.range_sum_query.test.csx](https://github.com/kmyk/online-judge-verify-helper/blob/master/examples/csharpscript/segment_tree.range_sum_query.test.csx) |

### C++ の設定

`.verify-helper/config.toml` というファイルを作って以下のように設定を設定を書くと、コンパイラやそのオプションを指定できます。
設定がない場合は、自動でコンパイラ (`g++` と `clang++`) を検出し、おすすめのオプションを用いて実行されます。

``` toml
[[languages.cpp.environments]]
CXX = "g++"

[[languages.cpp.environments]]
CXX = "clang++"
CXXFLAGS = ["-std=c++17", "-Wall", "-g", "-fsanitize=undefined", "-D_GLIBCXX_DEBUG"]
```

### C# script の設定

設定項目はありません。

### その他の言語の設定

上記以外の言語でも実行可能です (例: [examples/awk/circle.test.awk](https://github.com/kmyk/online-judge-verify-helper/blob/master/examples/awk/circle.test.awk))。
`.verify-helper/config.toml` というファイルを作って、以下のようにコンパイルや実行のためのコマンドを書いてください (例: [.verify-helper/config.toml](https://github.com/kmyk/online-judge-verify-helper/blob/master/.verify-helper/config.toml))。

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

### Doxygen 風マークアップで利用可能なタグ

|タグ名|説明|備考|
|---|---|---|
| `@title` | タイトルとして使用されます。 | `@title` が指定されていないとき、`@brief` が存在するならば、最初に登場する `@brief` 要素がタイトルとして使用されます。`@brief` も存在しないならば、ファイル名がタイトルになります。 |
| `@category` | そのライブラリが属するカテゴリとして使用されます。 | 指定されていない場合、ディレクトリ名がカテゴリになります。 |
| `@brief` | ライブラリの説明文として使用されます。 | `@title` が指定されていないときは、最初に登場する `@brief` は説明文ではなくタイトルとして使用されます。 |
| `@see`, `@sa` | このタグの直後に記載された文字列に対してリンクを張ります。参考にした Web ページなどがあるときに活用するとよいでしょう。 | 例: `@see https://example.com/` |
| `@docs` | 説明文が長く `@brief` タグで対応することが難しい場合、説明文が書かれた Markdown ファイルへのパスを記載すると、説明文がドキュメントに反映されます。 | 例: `@docs path/to/markdown.md` |
| `@depends` | そのライブラリが依存している他のファイルをタグで明示的に記載したい場合に使用します。 | C++ など一部の言語ではソフトウェア側で依存関係を自動で判定するため、記載する必要がない場合があります。 |
| `@ignore` | ドキュメント生成の対象から除外します。 |  |

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
