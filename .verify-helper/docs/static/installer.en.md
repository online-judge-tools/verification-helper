# Tool to set up automated verification CI by GitHub Actions

[日本語バージョン](installer.html)

## To set up automated verification

Steps:

1.  <form>
        <label>Input the URL of the library repository in the textbox on the right: </label>
        <input type="text" id="input" placeholder="https://github.com/beet-aizu/library" value="https://github.com/beet-aizu/library" size="48">
    </form>

1.  Open <a id="output" target="_blank"></a> and click the green `Commit new file` button.
1.  Add C++ source files ending with `.test.cpp` and `#define PROBLEM "https://..."` added like [example.test.cpp](https://github.com/kmyk/online-judge-verify-helper/blob/master/example.test.cpp) to the repository. (<a id="output2" target="_blank">A link to add the example file to your repository</a>)
1.  Confirm the result from the <a id="output3" target="_blank">GitHub Actions <img id="output7"></a> page.
1.  (Additional) Add <code id="output4"></code> to `README.md` (The badge <a id="output5" target="_blank"><img id="output6"></a> will be added)

## To set up automated documentation generator

Steps:

1.  Set up the automated verification process.
1.  Follow the steps in [Creating a personal access token for the command line - GitHub Help](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line) and generate a personal access toen with the permission `repo`.
1.  Follow the steps in [Creating and using encrypted secrets - GitHub Help](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/creating-and-using-encrypted-secrets) and save the generated personal access token as a secret named `GH_PAT`.

(Note: even without this setting, the documentation will be generated and pushed to the `gh-pages` branch. However, because of limitations from GitHub Actions, GitHub Pages cannot be automatically updated. This can be mitigated by pushing an empty commit to trigger an update on GitHub Pages. This limitation is probably to prevent infinite loop from wrong settings in GitHub Actions.)

<script>
    const data = {};
    data["verify.yml"] = (function () {
        const req = new XMLHttpRequest();
        req.open("GET", "https://raw.githubusercontent.com/kmyk/online-judge-verify-helper/master/.github/workflows/verify.yml", false);
        req.send();
        return req.responseText;
    })();
    data["example.test.cpp"] = (function () {
        const req = new XMLHttpRequest();
        req.open("GET", "https://raw.githubusercontent.com/kmyk/online-judge-verify-helper/master/example.test.cpp", false);
        req.send();
        return req.responseText;
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
            const value = encodeURIComponent(data["verify.yml"].replace("git+https://github.com/kmyk/online-judge-verify-helper.git@master", "online-judge-verify-helper"));
            output.href = url + "/new/master?filename=" + filename + "&value=" + value;
            output.textContent = url + "&value=...";

            const filename2 = "example.test.cpp";
            const value2 = encodeURIComponent(data["example.test.cpp"]);
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
