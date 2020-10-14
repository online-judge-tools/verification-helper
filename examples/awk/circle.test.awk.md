---
data:
  _extendedDependsOn:
  - icon: ':heavy_check_mark:'
    path: examples/awk/circle.awk
    title: examples/awk/circle.awk
  _extendedRequiredBy: []
  _extendedVerifiedWith: []
  _pathExtension: awk
  _verificationStatusIcon: ':heavy_check_mark:'
  attributes:
    ERROR: 1e-5
    PROBLEM: http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_4_B
  bundledCode: "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.8.6/x64/lib/python3.8/site-packages/onlinejudge_verify/documentation/build.py\"\
    , line 71, in _render_source_code_stat\n    bundled_code = language.bundle(stat.path,\
    \ basedir=basedir).decode()\n  File \"/opt/hostedtoolcache/Python/3.8.6/x64/lib/python3.8/site-packages/onlinejudge_verify/languages/user_defined.py\"\
    , line 70, in bundle\n    return subprocess.check_output(shlex.split(command))\n\
    \  File \"/opt/hostedtoolcache/Python/3.8.6/x64/lib/python3.8/subprocess.py\"\
    , line 411, in check_output\n    return run(*popenargs, stdout=PIPE, timeout=timeout,\
    \ check=True,\n  File \"/opt/hostedtoolcache/Python/3.8.6/x64/lib/python3.8/subprocess.py\"\
    , line 512, in run\n    raise CalledProcessError(retcode, process.args,\nsubprocess.CalledProcessError:\
    \ Command '['false']' returned non-zero exit status 1.\n"
  code: "# verification-helper: PROBLEM http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_4_B\n\
    # verification-helper: ERROR 1e-5\n@include \"examples/awk/circle.awk\"\n{\n \
    \   print get_area($1), get_circumference($1);\n}\n"
  dependsOn:
  - examples/awk/circle.awk
  isVerificationFile: true
  path: examples/awk/circle.test.awk
  requiredBy: []
  timestamp: '2020-09-17 18:25:50+09:00'
  verificationStatus: TEST_ACCEPTED
  verifiedWith: []
documentation_of: examples/awk/circle.test.awk
layout: document
redirect_from:
- /verify/examples/awk/circle.test.awk
- /verify/examples/awk/circle.test.awk.html
title: examples/awk/circle.test.awk
---
