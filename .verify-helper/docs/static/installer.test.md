# 競プロライブラリに自動で verify をしてくれる CI を簡単に設定できる Web ページ

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
1.  [Creating and using encrypted secrets - GitHub ヘルプ](https://help.github.com/ja/actions/automating-your-workflow-with-github-actions/creating-and-using-encrypted-secrets#creating-encrypted-secrets) に従い、作成した Personal Access Token を `GH_PAT` という名前の secret として保存する

(注意: この設定がなくてもドキュメントのデータ自体は自動で生成され `gh-pages` branch へ push されます。しかし GitHub Actions の制約のために GitHub Pages の更新までは行われません。その場合は `gh-pages` branch へ手動で空の commit などを push すれば GitHub Pages の更新が行われます。この制約はおそらくは GitHub Actions の設定ミスによる無限ループを抑制するためのものです。)

<script>
    const data = {};
    data["verify.yml"] = (function () {
        let req = new XMLHttpRequest();
        req.open("GET", "https://raw.githubusercontent.com/kmyk/online-judge-verify-helper/master/.github/workflows/verify.yml", true);
        req.send();
        return req.response;
    })();
    data["example.test.cpp"] = (function () {
        let req = new XMLHttpRequest();
        req.open("GET", "https://raw.githubusercontent.com/kmyk/online-judge-verify-helper/master/example.test.cpp", true);
        req.send();
        return req.response;
    })();

    const input = document.getElementById("input");
    const output = document.getElementById("output");
    const output2 = document.getElementById("output2");
    const output3 = document.getElementById("output3");
    const output4 = document.getElementById("output4");
    const output5 = document.getElementById("output5");
    const output6 = document.getElementById("output6");
    const output7 = document.getElementById("output7");
    function update() {
        if (input.value.match(/\/github.com\/[^\/]+\/[^\/]+/)) {
            const url = input.value.replace(/\/$/, "");

            const filename = ".github%2Fworkflows%2Fverify.yml"
            const value = btoa(data["verify.yml"].replace("git+https://github.com/kmyk/online-judge-verify-helper.git@master", "online-judge-verify-helper"));
            output.href = url + "/new/master?filename=" + filename + "&value=" + value;
            output.textContent = url + "&value=...";

            const filename2 = "example.test.cpp";
            const value2 = btoa(data["example.test.cpp"]);
            output2.href = url + "/new/master?filename=" + filename2 + "&value=" + value2;

            output3.href = input.value.replace(/\/$/, "") + "/actions";
            output5.href = input.value.replace(/\/$/, "") + "/actions";

            output4.textContent = "[![Actions Status](" + url + "/workflows/verify/badge.svg)](" + url + "/actions)";
            output6.src = url + "/workflows/verify/badge.svg";
            output7.src = url + "/workflows/verify/badge.svg";
        }
    }
    input.addEventListener('change', update);
    input.addEventListener('keyup', update);
    update();

    // workaround for the Dinky theme
    output6.style.margin = 0;
    output6.style.padding = 0;
    output7.style.margin = 0;
    output7.style.padding = 0;
</script>
