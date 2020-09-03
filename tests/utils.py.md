---
data:
  attributes: {}
  bundledCode: "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/documentation/build.py\"\
    , line 58, in _render_source_code_stat\n    bundled_code = language.bundle(stat.path,\
    \ basedir=basedir).decode()\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/languages/python.py\"\
    , line 84, in bundle\n    raise NotImplementedError\nNotImplementedError\n"
  code: "import contextlib\nimport os\nimport pathlib\nimport tempfile\nfrom typing\
    \ import *\n\n\ndef load_files(files: Dict[str, bytes]) -> Iterator[pathlib.Path]:\n\
    \    files_ = {}\n    for relpath, data in files.items():\n        assert '/'\
    \ not in relpath and '\\\\' not in relpath  # we should use pathlib\n        files_[pathlib.Path(relpath)]\
    \ = data\n    return load_files_pathlib(files_)\n\n\n@contextlib.contextmanager\n\
    def load_files_pathlib(files: Dict[pathlib.Path, bytes]) -> Iterator[pathlib.Path]:\n\
    \    with tempfile.TemporaryDirectory() as tempdir_:\n        tempdir = pathlib.Path(tempdir_).resolve()\n\
    \        for relpath, data in files.items():\n            path = tempdir / relpath\n\
    \            path.parent.mkdir(parents=True, exist_ok=True)\n            with\
    \ open(str(path), \"wb\") as fh:\n                fh.write(data)\n        yield\
    \ tempdir\n\n\n@contextlib.contextmanager\ndef chdir(path: pathlib.Path) -> Iterator[None]:\n\
    \    cwd = os.getcwd()\n    try:\n        os.chdir(str(path))\n        yield\n\
    \    finally:\n        os.chdir(cwd)\n"
  dependsOn: []
  extendedDependsOn: []
  extendedRequiredBy: []
  extendedVerifiedWith: []
  isVerificationFile: false
  path: tests/utils.py
  requiredBy: []
  timestamp: '1970-01-01 00:00:00+00:00'
  verificationStatus: LIBRARY_NO_TESTS
  verificationStatusIcon: ':warning:'
  verifiedWith: []
documentation_of: tests/utils.py
layout: document
redirect_from:
- /library/tests/utils.py
- /library/tests/utils.py.html
title: tests/utils.py
---
