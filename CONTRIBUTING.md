# Contribution and Hacking Guide

links:

-   [CONTRIBUTING.md](https://github.com/online-judge-tools/.github/blob/master/CONTRIBUTING.md) of [online-judge-tools](https://github.com/online-judge-tools) organization
-   [DESIGN.md](https://github.com/online-judge-tools/verification-helper/blob/master/DESIGN.md)


## How to add a new language / 新しい言語を足すには

Do the following steps:

1.  Open an issue about the support for your language
1.  Make a file `onlinejudge_verify/languages/YOUR_LANGUAGE.py`
    -   Implement a sub-class of `onlinejudge_verify.languages.models.Language`
    -   Implement a sub-class of `onlinejudge_verify.languages.models.LanguageEnvironment`
1.  Register your language at `onlinejudge_verify/languages/list.py`
1.  Add tests to `tests/` dir if possible
1.  Update documents `.verify-helper/docs/static/document.md` (or `.verify-helper/docs/static/document.ja.md`)


## CI to check format

[.github/workflows/format.yml](https://github.com/online-judge-tools/verification-helper/blob/master/.github/workflows/format.yml) defines the format checking.

You can run the format checking with the following commands. You can automatically run this with copying this script into your `.git/hooks/pre-commit`.

``` sh
#!/bin/bash
set -e

mypy onlinejudge_verify onlinejudge_bundle tests setup.py
pylint --rcfile=setup.cfg onlinejudge_verify onlinejudge_bundle tests setup.py
isort --check-only --diff onlinejudge_verify onlinejudge_bundle tests setup.py
yapf --diff --recursive onlinejudge_verify onlinejudge_bundle tests setup.py
```

You can automatically fix some errors with the following commands.

``` sh
isort onlinejudge_verify onlinejudge_bundle tests setup.py
yapf --in-place --recursive onlinejudge_verify onlinejudge_bundle tests setup.py
```
