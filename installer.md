# Tool to set up automated verification CI by GitHub Actions

[日本語バージョン](installer.ja.html)

## To set up automated verification

Steps:

1.  <form>
        <label>Input the URL of the library repository in the textbox on the right: </label>
        <input type="text" id="input" placeholder="https://github.com/beet-aizu/library" value="https://github.com/beet-aizu/library" size="48">
    </form>

1.  Open <a id="output" target="_blank"></a> and click the green `Commit new file` button.
1.  Add C++ source files ending with `.test.cpp` and `#define PROBLEM "https://..."` added like [example.test.cpp](https://github.com/online-judge-tools/verification-helper/blob/master/example.test.cpp) to the repository. (<a id="output2" target="_blank">A link to add the example file to your repository</a>)
1.  Confirm the result from the <a id="output3" target="_blank">GitHub Actions <img id="output7"></a> page.
1.  (Additional) Add <code id="output4"></code> to `README.md` (The badge <a id="output5" target="_blank"><img id="output6"></a> will be added)

## To set up automated documentation generator

Steps:

1.  Set up the automated verification process.
1.  Follow the steps in [Creating a personal access token for the command line - GitHub Help](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line) and generate a personal access toen with the permission `repo`.
1.  Follow the steps in [Creating and using encrypted secrets - GitHub Help](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/creating-and-using-encrypted-secrets) and save the generated personal access token as a secret named `GH_PAT`.
1.  Push any commit, and wait for a while. (You are done when a commit in <a id="output13"><code>gh-pages</code> branch</a> has a green check mark.)
1.  Confirm the result from the <a id="output8" target="_blank">GitHub Pages <img id="output9"></a> page.
1.  (Additional) Add <code id="output10"></code> to `README.md` (The badge <a id="output11" target="_blank"><img id="output12"></a> will be added)
1.  (Additional) Set the URL of documents to the repository description (see: [How do you change a repository description on GitHub? - Stack Overflow](https://stackoverflow.com/questions/7757751/how-do-you-change-a-repository-description-on-github))

(Note: even without this setting, the documentation will be generated and pushed to the `gh-pages` branch. However, because of limitations from GitHub Actions, GitHub Pages cannot be automatically updated. This can be mitigated by pushing an empty commit to trigger an update on GitHub Pages. This limitation is probably to prevent infinite loop from wrong settings in GitHub Actions.)


<script src="installer.js"></script>
