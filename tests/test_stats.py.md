---
data:
  _extendedDependsOn: []
  _extendedRequiredBy: []
  _extendedVerifiedWith: []
  _pathExtension: py
  _verificationStatusIcon: ':warning:'
  attributes: {}
  bundledCode: "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/documentation/build.py\"\
    , line 67, in _render_source_code_stat\n    bundled_code = language.bundle(stat.path,\
    \ basedir=basedir).decode()\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/languages/python.py\"\
    , line 84, in bundle\n    raise NotImplementedError\nNotImplementedError\n"
  code: "\"\"\"This module has tests for the stats subcommand.\n\"\"\"\n\nimport unittest\n\
    \nimport onlinejudge_verify.main\n\n\nclass TestStatsSubcommandSmoke(unittest.TestCase):\n\
    \    \"\"\"TestStatsSubcommandSmoke is a smoke tests of `stats` subcommand.\n\
    \    \"\"\"\n    def test_run(self) -> None:\n        onlinejudge_verify.main.subcommand_stats()\n"
  dependsOn: []
  isVerificationFile: false
  path: tests/test_stats.py
  requiredBy: []
  timestamp: '1970-01-01 00:00:00+00:00'
  verificationStatus: LIBRARY_NO_TESTS
  verifiedWith: []
documentation_of: tests/test_stats.py
layout: document
redirect_from:
- /library/tests/test_stats.py
- /library/tests/test_stats.py.html
title: tests/test_stats.py
---
