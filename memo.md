```
# どれかのファイルをいじる

# 成果物を作成
$ python setup.py sdist
$ pip install dist/online-judge-verify-helper-3.1.2.tar.gz
# 確認
$ oj-verify docs
```

チェック
https://github.com/kmyk/online-judge-verify-helper/blob/master/.github/workflows/format.yml
```
pip install pylint yapf mypy
pylint --disable=all --enable=unused-import onlinejudge_verify setup.py
isort --check-only --diff --recursive onlinejudge_verify setup.py
yapf -i --recursive onlinejudge_verify setup.tests
mypy onlinejudge_verify setup.py
```

# memo
- localで?依存関係うまくとれない理由
https://stackoverflow.com/questions/29555907/why-g-mm-option-ignore-current-work-dirs-include-file
