# The reference of Online Judge Verify Helper

[日本語バージョン](https://kmyk.github.io/online-judge-verify-helper/document.ja.html)

## Automating the verification

### Available judging platforms

|Name|Remarks|
|---|---|
| [Library Checker](https://judge.yosupo.jp/) | |
| [Aizu Online Judge](https://onlinejudge.u-aizu.ac.jp/home) | |
| [HackerRank](https://www.hackerrank.com/) | |
| [yukicoder](https://yukicoder.me) | You must set the `YUKICODER_TOKEN` environment variable. See 「ログインしてないと使えない機能をAPIとして使いたい」 in [ヘルプ - yukicoder](https://yukicoder.me/help) and [Creating and using encrypted secrets - GitHub Help](https://help.github.com/en/actions/configuring-and-managing-workflows/creating-and-storing-encrypted-secrets). |

Other judging platforms do not currently publish the test cases in usable forms, and so are not currently supported.

### Available macro definitions

|Macro name|Description|Remarks|
|---|---|---|
| `PROBLEM` | specify the URL of the problem to submit | required |
| `IGNORE` | If this is defined in a file, the verification is skipped. | You can use this in a scope like `#ifdef __clang__` to ignore in a specific environment. |
| `ERROR` | specify the absolute or relative error to be considered as correct | |

## Generating Documentation

### Available tags

|Tag name|Description|Remarks|
|---|---|---|
| `@title` | Library file title | If a title was not specified, the `@brief` element which appears first is used as a title. If there was no `@brief` elements, a filename is used as a title. |
| `@category` | Category | If a category was not specified, a directory name is used as a category. |
| `@brief` | Description of library file | If a title was not specified, the `@brief` element which appears first is not used as a description, but it is used as a title. |
| `@see`, `@sa` | Create a hyperlink to an URL which is written right after this tag. We recommend to use this tag when you have some reference web pages. | Usage: `@see https://example.com/` |
| `@docs` | When a description of your library is too long to handle by using `@brief` tags, you can add a description which is written in Markdown file. | Usage: `@docs path/to/markdown.md` |
| `@depends` | You can this tag when you want to write dependencies explicitly. | This application supports the automatic recognization of dependencies for some languages such as C++, so there are some cases you need not to write this. |
| `@ignore` | This application does not generate the documentation of the library file which this tag is specified. |  |


### Others

-   The file `.verify-helper/docs/_config.yml` is copied into the target directory with some modification.
-   Files under the directory `.verify-helper/docs/static/` are copied into the target directory directly.
