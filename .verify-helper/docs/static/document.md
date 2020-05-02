# The reference of Online Judge Verify Helper

[日本語バージョン](https://online-judge-tools.github.io/verification-helper/document.ja.html)

## Supported languages

Summary:

| Language | Compilers | How to specify attributes | Features (verify / bundle / doc) | Examples |
|---|---|---|---|---|
| C++ | GCC / Clang | `#define [KEY] [VALUE]` | :heavy_check_mark: / :heavy_check_mark: / :heavy_check_mark: | [examples/segment_tree.range_sum_query.test.cpp](https://github.com/online-judge-tools/verification-helper/blob/master/examples/segment_tree.range_sum_query.test.cpp) |
| C# script | .NET Core | `#pragma [KEY] [VALUE]` | :heavy_check_mark: / :x: / :warning: | [examples/csharpscript/segment_tree.range_sum_query.test.csx](https://github.com/online-judge-tools/verification-helper/blob/master/examples/csharpscript/segment_tree.range_sum_query.test.csx) |

### Settings for C++

You can specify compilers and options with writing `.verify-helper/config.toml` as below.
If there is no settings, online-judge-verify-helper automatically detects compilers (`g++` and `clang++` if exists) and use recommended options.

``` toml
[[languages.cpp.environments]]
CXX = "g++"

[[languages.cpp.environments]]
CXX = "clang++"
CXXFLAGS = ["-std=c++17", "-Wall", "-g", "-fsanitize=undefined", "-D_GLIBCXX_DEBUG"]
```

### Settings for C#

No config

### Settings for other languages

You can use languages other than above (e.g. AWK [examples/awk/circle.test.awk](https://github.com/online-judge-tools/verification-helper/blob/master/examples/awk/circle.test.awk)). Please write commands to compile and execute in the config file `.verify-helper/config.toml` (e.g. [.verify-helper/config.toml](https://github.com/kmyk/online-judge-verify-helper/blob/master/.verify-helper/config.toml)).

``` toml
[languages.awk]
compile = "bash -c 'echo hello > {tempdir}/hello'"
execute = "env AWKPATH={basedir} awk -f {path}"
bundle = "false"
list_dependencies = "sed 's/^@include \"\\(.*\\)\"$/\\1/ ; t ; d' {path}"
```

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

### Local execution

Executing following commands, you can see generated documents locally at <http://localhost:4000/>.

``` console
$ bundle install --path .vendor/bundle
$ bundle exec jekyll serve
```

To do this, Ruby's [Bundler](https://bundler.io/) is required.
If you are using Ubuntu, you can install this with `sudo apt install ruby-bundler`.


### Others

-   The file `.verify-helper/docs/_config.yml` is copied into the target directory with some modification.
-   Files under the directory `.verify-helper/docs/static/` are copied into the target directory directly.
