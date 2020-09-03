---
data:
  attributes:
    ERROR: 1e-5
    PROBLEM: http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_4_B
  bundledCode: "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/documentation/build.py\"\
    , line 64, in _render_source_code_stat\n    bundled_code = language.bundle(stat.path,\
    \ basedir=basedir).decode()\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/languages/other.py\"\
    , line 64, in bundle\n    return subprocess.check_output(shlex.split(command))\n\
    \  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/subprocess.py\"\
    , line 411, in check_output\n    return run(*popenargs, stdout=PIPE, timeout=timeout,\
    \ check=True,\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/subprocess.py\"\
    , line 512, in run\n    raise CalledProcessError(retcode, process.args,\nsubprocess.CalledProcessError:\
    \ Command '['false']' returned non-zero exit status 1.\n"
  code: "# verify-helper: PROBLEM http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_4_B\n\
    # verify-helper: ERROR 1e-5\n@include \"examples/awk/circle.awk\"\n{\n    print\
    \ get_area($1), get_circumference($1);\n}\n"
  dependsOn:
  - examples/awk/circle.awk
  extendedDependsOn:
  - icon: ':warning:'
    path: examples/awk/circle.awk
    title: examples/awk/circle.awk
  extendedRequiredBy: []
  extendedVerifiedWith: []
  isVerificationFile: true
  path: examples/awk/circle.test.awk
  requiredBy: []
  timestamp: '2020-02-28 16:10:41+09:00'
  verificationStatus: TEST_ACCEPTED
  verificationStatusIcon: ':heavy_check_mark:'
  verifiedWith: []
documentation_of: examples/awk/circle.test.awk
layout: document
redirect_from:
- /verify/examples/awk/circle.test.awk
- /verify/examples/awk/circle.test.awk.html
title: examples/awk/circle.test.awk
---
