# 競プロライブラリに自動で verify をしてくれる CI を簡単に設定できる Web ページ

[English Version](installer.html)

## verify を自動でしてくれるように設定するには

手順:

1.  <form>
        <label>競プロライブラリの GitHub のレポジトリの URL を右の textbox に入力: </label>
        <input type="text" id="input" placeholder="https://github.com/beet-aizu/library" value="https://github.com/beet-aizu/library" size="48">
    </form>

1.  ページ <a id="output" target="_blank"></a> を開き、下の方にある緑の `Commit new file` ボタンを押す
1.  [example.test.cpp](https://github.com/kmyk/online-judge-verify-helper/blob/master/example.test.cpp) のように `#define PROBLEM "https://..."` が書かれている `hoge.test.cpp` のようなファイル名の C++ コードを追加する (<a id="output2" target="_blank">例を自動で追加するリンク</a>)
1.  <a id="output3" target="_blank">GitHub Actions <img id="output7"></a> のページから結果を確認する
1.  (おまけ) `README.md` に <code id="output4"></code> と書き足す (バッチ <a id="output5" target="_blank"><img id="output6"></a> が貼られる)

## ドキュメントが自動生成されるように設定するには

手順:

1.  verify を自動でしてくれるように設定する
1.  [コマンドライン用の個人アクセストークンを作成する - GitHub ヘルプ](https://help.github.com/ja/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line) に従い、権限 `repo` を持った Personal Access Token を生成する
1.  [暗号化されたシークレットの作成と利用 - GitHub ヘルプ](https://help.github.com/ja/actions/automating-your-workflow-with-github-actions/creating-and-using-encrypted-secrets#creating-encrypted-secrets) に従い、作成した Personal Access Token を `GH_PAT` という名前の secret として保存する
1.  なんでもよいのでなにか commit を push し、しばらく待つ (<a id="output13"><code>gh-pages</code> branch</a> の commit に緑のチェックマークが付けばよい)
1.  <a id="output8" target="_blank">GitHub Pages <img id="output9"></a> のページから結果を確認する
1.  (おまけ) `README.md` に <code id="output10"></code> と書き足す (バッチ <a id="output11" target="_blank"><img id="output12"></a> が貼られる)
1.  (おまけ) リポジトリの説明部分にドキュメントの URL を設定する (参考: [How do you change a repository description on GitHub? - Stack Overflow](https://stackoverflow.com/questions/7757751/how-do-you-change-a-repository-description-on-github))

(注意: この設定がなくてもドキュメントのデータ自体は自動で生成され `gh-pages` branch へ push されます。しかし GitHub Actions の制約のために GitHub Pages の更新までは行われません。その場合は `gh-pages` branch へ手動で空の commit などを push すれば GitHub Pages の更新が行われます。この制約はおそらくは GitHub Actions の設定ミスによる無限ループを抑制するためのものです。)


<script src="installer.js"></script>
