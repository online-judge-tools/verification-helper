# Design Doc

link: [DESIGN.md](https://github.com/online-judge-tools/.github/blob/master/DESIGN.md) of [online-judge-tools](https://github.com/online-judge-tools) organization


## Objective

`oj-verify` コマンドは、競技プログラミングのためのライブラリを現代的な方法で管理する機能を提供する。
特に、実際の競技プログラミングの問題を用いたテストを簡単かつ快適に実行できるようにする。

副次的な機能として、`oj-bundle` コマンドは、複数ファイルを単一ファイルにまとめて、現代的な形で書かれたソースコードをオンラインジャッジに提出できるようにする。


## Goals

-   ユーザのライブラリの信頼性を向上させること
    -   これにはドキュメントを書かせることも含む
-   競技プログラミング界隈における「ライブラリ」を「スニペットの寄せ集め」から脱却させ、それぞれの言語における標準的なライブラリに寄せていくこと


## Non-Goals

-   ユーザのライブラリの機能性を向上させること
    -   ライブラリ整備が楽しくなるような機能を追加することはあるが、あくまでバグがでにくくなる


## Background

競技プログラミング用のライブラリのテストは、実際にそれを利用する問題に提出してみて AC することを確認するという手法が一般的である。
これをすることは「ライブラリを verify する」と呼ばれている。
しかし、これはとても面倒な作業であり、大規模ライブラリになりファイル数が増えるとすべてきちんと実行するのは非現実的であった。

`oj-verify` コマンドの登場と普及の前は、ほとんどすべての競技プログラミング用のライブラリにテストは書かれていなかったことに注意したい。
そもそも、過去において、競技プログラミングの「ライブラリ」とは通常の意味のライブラリではなく、むしろ「スニペット集」と呼ばれるべきものであった。
ライブラリを `#include` 文などの標準的な機能で呼び出すことはまったく不可能で、エディタのスニペット機能の利用しての丸ごと埋め込みが通例であった。


## Overview

内部での処理は大きく分けて以下の 4 つの部分からなる。

1.  テストの実行 (`oj-verify run`)
    -   システムケースの取得
    -   テストの実行
    -   キャッシュ (`timestamps.*.json`) の管理
1.  言語個別の処理
    -   コンパイルと実行
    -   ファイル間の依存関係解析
    -   単一ファイル化 (`oj-bundle` などから使われる)
1.  ドキュメントの生成 (`oj-verify docs`)
    -   ドキュメント生成に必要なメタデータの収集
    -   ドキュメントのための Markdown ファイルの書き出し
    -   実際の HTML の生成 ([Jekyll](http://jekyllrb-ja.github.io/) による)
1.  GitHub との通信


## Detailed Design

-   テストの結果はキャッシュされる。これは速度の改善のためである。大規模なライブラリになると数百ファイルに達するため、全ファイルについて毎回テストを再実行することは快適でない。
-   ドキュメントを生成することは「ドキュメントを書くことをユーザに促す」および「カバレッジを可視化する」という働きをする。
-   言語個別の処理は [models.py](https://github.com/online-judge-tools/verification-helper/blob/master/onlinejudge_verify/languages/models.py) にある `Language` class と `LanguageEnvironment` class の sub-class として実装される。`Language` class と `LanguageEnvironment` class の区別は、ひとつの言語 (例: C++) が複数の環境 (例: G++, Clang, MSVC++ など) と関連付けられることから来る区別である。
-   競技プログラミングの文脈では end-to-end tests や integration tests と unit tests の区別が比較的曖昧である。
    通常の文脈では end-to-end tests などは unit tests と比べて「実際と似た環境で動かせる」という利点と「遅い」「不安定」「失敗の原因が分かりにくい」という欠点がある ([参考](https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html))。しかしこれは通常の end-to-end tests が「GUI の操作」「ネットワーク通信」「ファイル書き込み」などの複雑で非純粋な要素を含むからである。競技プログラミングにおいてはそのような要素はないのでテストの結果は常に「安定」しており、またファイルの依存関係が疎であることを利用して最適に差分のみテストをすることで十分に「速い」テストが可能である。このため競技プログラミングにおいては end-to-end tests の欠点とされていた特徴の多くは隠れ、unit tests との差も曖昧となる。
-   `oj-bundle` コマンドは `#include "..."` の形の include のみを展開し `#include <...>` の形の include は展開しない。この仕様は、`#include <...>` が「システムの標準のヘッダ」に使われることが意図されており、また `#include "..."` が「カレントディレクトリなどにある自作のヘッダ」に使われことが意図されている、という事情による。参考として、プリプロセッサの挙動についての説明は <https://gcc.gnu.org/onlinedocs/cpp/Search-Path.html> にある。
-   `oj-bundle` コマンドが [online-judge-tools/verification-helper](https://github.com/online-judge-tools/verification-helper) リポジトリにあるのは便宜上のものである。対応言語が増えるようなら他の新しいリポジトリに移されるだろう。


## Security Considerations

システムケースの取得にログインが必要なオンラインジャッジがある (現在は yukicoder のみ)。
その利用にはアクセストークンの設定が必要であるが、ユーザの設定ミスによりこれが公開されるとインイデントとなる。
設定方法のドキュメントで encrypted secrets を使うよう要求するようにする。


## Privacy Considerations

特になし。
ユーザが自分から公開しているコードについてのツールである。


## Metrics Considerations

GitHub 上での検索結果 <https://github.com/search?q=online-judge-verify-helper+path%3A.github> からユーザ数のほぼ正確な値が得られる。
個別の機能の利用状況についての統計は得られない。

2020/09/20 時点では利用数はおよそ 100 個である。
競技プログラミング用のライブラリを内製しているユーザの総数を取得することは難しいため、利用割合などついては不明である。


## Testing Plan

開発者による dogfooding を中心とする。
実行結果が GitHub Pages として公開されるという性質により、大まかなテストはそれで十分であろう。
