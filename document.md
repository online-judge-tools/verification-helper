# The reference of Online Judge Verification Helper

[日本語バージョン](https://online-judge-tools.github.io/verification-helper/document.ja.html)

## Supported languages

Summary:

| Language | Available file extensions | Pattern to detect test files | How to specify attributes | Features (verify / bundle / doc) | Example file |
|---|---|---|---|---|---|
| C++ | `.cpp` `.hpp` | `.test.cpp` | `#define [KEY] [VALUE]` | :heavy_check_mark: / :heavy_check_mark: / :heavy_check_mark: | [segment_tree.range_sum_query.test.cpp](https://github.com/online-judge-tools/verification-helper/blob/master/examples/segment_tree.range_sum_query.test.cpp) |
| C# script | `.csx` | `.test.csx` | `// verification-helper: [KEY] [VALUE]` | :heavy_check_mark: / :x: / :heavy_check_mark: | [segment_tree.range_sum_query.test.csx](https://github.com/online-judge-tools/verification-helper/blob/master/examples/csharpscript/segment_tree.range_sum_query.test.csx) |
| Nim | `.nim` | `_test.nim` | `# verification-helper: [KEY] [VALUE]` | :heavy_check_mark: / :x: / :heavy_check_mark: | [union_find_tree_yosupo_test.nim](https://github.com/online-judge-tools/verification-helper/blob/master/examples/nim/union_find_tree_yosupo_test.nim) |
| Python 3 | `.py` | `.test.py` | `# verification-helper: [KEY] [VALUE]` | :heavy_check_mark: / :x: / :heavy_check_mark: | [union_find_yosupo.test.py](https://github.com/online-judge-tools/verification-helper/blob/master/examples/python/union_find_yosupo.test.py) |
| Haskell | `.hs` | `.test.hs` | `-- verification-helper: [KEY] [VALUE]` | :heavy_check_mark: / :x: / :warning: | [HelloWorld.test.hs](https://github.com/online-judge-tools/verification-helper/blob/master/Examples2/Haskell/HelloWorld.test.hs) |
| Ruby | `.rb` | `.test.rb` | `# verification-helper: [KEY] [VALUE]` | :heavy_check_mark: / :x: / :warning: | [hello_world.test.rb](https://github.com/online-judge-tools/verification-helper/blob/master/examples/ruby/hello_world.test.rb) |
| Go | `.go` | `.test.go` | `// verification-helper: [KEY] [VALUE]` | :heavy_check_mark: / :x: / :warning: | [helloworld.test.go](https://github.com/online-judge-tools/verification-helper/blob/master/examples/go/helloworld.test.go) |
| Java | `.java` | `_test.java` | `// verification-helper: [KEY] [VALUE]` | :heavy_check_mark: / :x: / :warning: | [HelloWorld_test.java](https://github.com/online-judge-tools/verification-helper/blob/master/examples/java/HelloWorld_test.java) |
| Rust | `.rs` | special | `// verification-helper: [KEY] [VALUE]` | :heavy_check_mark: / :x: / :warning: | [itp1-1-a.rs](https://github.com/online-judge-tools/verification-helper/blob/master/examples/rust/verification/src/bin/aizu-online-judge-itp1-1-a.rs) |

### Settings for C++

You can specify compilers and options with writing `.verify-helper/config.toml` as below.
If there are no settings, online-judge-verify-helper automatically detects compilers (`g++` and `clang++` if exists) and use recommended options.

``` toml
[[languages.cpp.environments]]
CXX = "g++"

[[languages.cpp.environments]]
CXX = "clang++"
CXXFLAGS = ["-std=c++17", "-Wall", "-g", "-fsanitize=undefined", "-D_GLIBCXX_DEBUG"]
```

-   If you use environments which [`ulimit`](https://linux.die.net/man/3/ulimit) doesn't work on, and if you want to set `CXXFLAGS` by yourself, please be careful about the stack size.
-   The supported extensions are `.cpp`, `.hpp`, `.cc`, and `.h`. Please note that files with other extensions like `.c` `.h++` and files without extensions are not recognized.

### Settings for C#

There is no config now.
.NET Core is used as the compiler.

-   Note that currently the `.cs` extension is not recognized ([#248](https://github.com/online-judge-tools/verification-helper/issues/248)).

### Settings for Nim

You can specify options and targets (e.g. `c` `cpp`) with writing `.verify-helper/config.toml` as below.
If there is no settings, online-judge-verify-helper automatically use recommended options similar to options on AtCoder.

``` toml
[[languages.nim.environments]]
compile_to = "c"

[[languages.nim.environments]]
compile_to = "cpp"
NIMFLAGS = ["--warning:on", "--opt:none"]
```

### Settings for Python 3

There is no config now.

### Settings for Rust

`oj-verify` uses [root source files](https://docs.rs/cargo_metadata/0.12.0/cargo_metadata/struct.Target.html#structfield.src_path) of [binary targets](https://doc.rust-lang.org/cargo/reference/cargo-targets.html#binaries) or [example targets](https://doc.rust-lang.org/cargo/reference/cargo-targets.html#examples) (excluding targets which `crate-type` is specified) which have the [`PROBLEM`](#available-macro-definitions) attribute

You can customize the method to list depending files with `languages.rust.list_dependencies_backend` of `.verify-helper/config.toml`.

- `kind = "none"`

    This is the default behavoir.
    For each target, all `.rs` files in the target is treated as a block. The dependency relationship of files in each target are not analyzed.

    ```toml
    [languages.rust.list_dependencies_backend]
    kind = "none"
    ```

    - For a file which is a root source file of a target, the file depends all `.rs` files in its target and all depending local crates.
    - For a file which is not a root source file of any targets, the file depends all `.rs` files in its target.

- `kind = "cargo-udeps"`

    This method is similar to `kind = "none"`, but uses [cargo-udeps](https://github.com/est31/cargo-udeps) in `$PATH` to narrow down dependencies. It computes the dependency relationship of files using the dependencies relationship between crates.

    ```toml
    [languages.rust.list_dependencies_backend]
    kind = "cargo-udeps"
    toolchain = "nightly-yyyy-mm-dd" # defaults to "nightly"
    ```

### Settings for other languages

You can use languages other than above (e.g. AWK [examples/awk/circle.test.awk](https://github.com/online-judge-tools/verification-helper/blob/master/examples/awk/circle.test.awk)). Please write commands to compile and execute in the config file `.verify-helper/config.toml` (e.g. [.verify-helper/config.toml](https://github.com/kmyk/online-judge-verify-helper/blob/master/.verify-helper/config.toml)).
`compile` field and `execute` field are required, and other fields are optional.

``` toml
[languages.awk]
compile = "bash -c 'echo hello > {tempdir}/hello'"
execute = "env AWKPATH={basedir} awk -f {path}"
bundle = "false"
list_dependencies = "sed 's/^@include \"\\(.*\\)\"$/\\1/ ; t ; d' {path}"
verification_file_suffix = ".test.sed"
```

## Automating the verification

### Available judging platforms

|Name|Remarks|
|---|---|
| [Library Checker](https://judge.yosupo.jp/) | |
| [Aizu Online Judge](https://onlinejudge.u-aizu.ac.jp/home) | |
| [HackerRank](https://www.hackerrank.com/) | |
| [AtCoder](https://atcoder.jp) | You must set the `DROPBOX_TOKEN` environment variable. You can obtain the token by following the HINT message shown by `$ oj d --system https://atcoder.jp/contests/agc001/tasks/agc001_a`. |
| [yukicoder](https://yukicoder.me) | You must set the `YUKICODER_TOKEN` environment variable. See 「ログインしてないと使えない機能をAPIとして使いたい」 in [ヘルプ - yukicoder](https://yukicoder.me/help) and [Creating and using encrypted secrets - GitHub Help](https://help.github.com/en/actions/configuring-and-managing-workflows/creating-and-storing-encrypted-secrets). |

Other judging platforms do not currently publish the test cases in usable forms, and so are not currently supported.

### Available macro definitions

|Macro name|Description|Remarks|
|---|---|---|
| `PROBLEM` | specify the URL of the problem to submit | required |
| `IGNORE` | If this is defined in a file, the verification is skipped. | You can use this in a scope like `#ifdef __clang__` to ignore in a specific environment. |
| `ERROR` | specify the absolute or relative error to be considered as correct | |

## Generating Documentation

### Embedding Markdown to pages for source codes

Markdown files in the repository are automatically recognized.
When the `documentation_of` field in [Front Matter](http://jekyllrb-ja.github.io/docs/front-matter/) specifies a source code file, the content of Markdown file is inserted into the generated document page of specified code.

For example, to add description to a document of a file `path/to/segment_tree.hpp`, make a Markdown file like `foo/bar.md` and write as the following in the file.

```
---
title: Segment Tree
documentation_of: ./path/to/segment_tree.hpp
---

## Description

In this file, ...
```

The `documentation_of` string is recognized as a relative path from the Markdown file when the string starts with `./` or `..`.
The `documentation_of` string is recognized as a absolute path from the directory which has `.verify-helper` directory as the root when the string starts with `//`.
The path should use `/` as directory separator be case-sensitive.



### Embedding Markdown to the top page

Please make the file `.verify-helper/docs/index.md` and write Markdown there.


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
