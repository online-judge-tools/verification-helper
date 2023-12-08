---
data:
  _extendedDependsOn: []
  _extendedRequiredBy: []
  _extendedVerifiedWith:
  - icon: ':heavy_check_mark:'
    path: examples/awk/circle.test.awk
    title: examples/awk/circle.test.awk
  _isVerificationFailed: false
  _pathExtension: awk
  _verificationStatusIcon: ':heavy_check_mark:'
  attributes: {}
  bundledCode: "Traceback (most recent call last):\n  File \"/home/runner/.local/lib/python3.10/site-packages/onlinejudge_verify/documentation/build.py\"\
    , line 71, in _render_source_code_stat\n    bundled_code = language.bundle(stat.path,\
    \ basedir=basedir, options={'include_paths': [basedir]}).decode()\n  File \"/home/runner/.local/lib/python3.10/site-packages/onlinejudge_verify/languages/user_defined.py\"\
    , line 71, in bundle\n    return subprocess.check_output(shlex.split(command))\n\
    \  File \"/usr/lib/python3.10/subprocess.py\", line 421, in check_output\n   \
    \ return run(*popenargs, stdout=PIPE, timeout=timeout, check=True,\n  File \"\
    /usr/lib/python3.10/subprocess.py\", line 526, in run\n    raise CalledProcessError(retcode,\
    \ process.args,\nsubprocess.CalledProcessError: Command '['false']' returned non-zero\
    \ exit status 1.\n"
  code: "function get_area(r) {\n    return 3.1415926535 * r * r;\n}\n\nfunction get_circumference(r)\
    \ {\n    return 2 * 3.1415926535 * r;\n}\n"
  dependsOn: []
  isVerificationFile: false
  path: examples/awk/circle.awk
  requiredBy: []
  timestamp: '2023-12-08 11:18:27+09:00'
  verificationStatus: LIBRARY_ALL_AC
  verifiedWith:
  - examples/awk/circle.test.awk
documentation_of: examples/awk/circle.awk
layout: document
redirect_from:
- /library/examples/awk/circle.awk
- /library/examples/awk/circle.awk.html
title: examples/awk/circle.awk
---
