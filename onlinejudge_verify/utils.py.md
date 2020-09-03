---
data:
  attributes: {}
  bundledCode: "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/documentation/build.py\"\
    , line 58, in _render_source_code_stat\n    bundled_code = language.bundle(stat.path,\
    \ basedir=basedir).decode()\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/languages/python.py\"\
    , line 84, in bundle\n    raise NotImplementedError\nNotImplementedError\n"
  code: "# Python Version: 3.x\nimport glob\nimport os\nimport pathlib\nfrom typing\
    \ import *\n\nimport onlinejudge_verify.languages\n\n\ndef is_local_execution()\
    \ -> bool:\n    return 'GITHUB_ACTION' not in os.environ\n\n\ndef is_verification_file(path:\
    \ pathlib.Path, *, basedir: Optional[pathlib.Path] = None) -> bool:\n    \"\"\"\
    `is_verification_file` is a thin wrapper for `Languge.is_verification_file`. \
    \ This function automatically get the language.\n    \"\"\"\n\n    basedir = basedir\
    \ or pathlib.Path.cwd()  # TODO: remove this. make basedir argument always required\n\
    \    language = onlinejudge_verify.languages.get(path)\n    return language is\
    \ not None and language.is_verification_file(path, basedir=basedir)\n\n\ndef iterate_verification_files()\
    \ -> Iterator[pathlib.Path]:\n    paths = [pathlib.Path(path) for path in glob.glob('**/*',\
    \ recursive=True)]  # use glob.glob because this ignore hidden files\n    for\
    \ path in paths:\n        if is_verification_file(path):\n            yield path\n"
  dependsOn: []
  extendedDependsOn: []
  extendedRequiredBy: []
  extendedVerifiedWith: []
  isVerificationFile: false
  path: onlinejudge_verify/utils.py
  requiredBy: []
  timestamp: '1970-01-01 00:00:00+00:00'
  verificationStatus: LIBRARY_NO_TESTS
  verificationStatusIcon: ':warning:'
  verifiedWith: []
documentation_of: onlinejudge_verify/utils.py
layout: document
redirect_from:
- /library/onlinejudge_verify/utils.py
- /library/onlinejudge_verify/utils.py.html
title: onlinejudge_verify/utils.py
---
