---
data:
  _extendedDependsOn: []
  _extendedRequiredBy: []
  _extendedVerifiedWith: []
  _pathExtension: py
  _verificationStatusIcon: ':warning:'
  attributes:
    links:
    - https://github.com/kmyk/online-judge-verify-helper
  bundledCode: "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.8.6/x64/lib/python3.8/site-packages/onlinejudge_verify/documentation/build.py\"\
    , line 71, in _render_source_code_stat\n    bundled_code = language.bundle(stat.path,\
    \ basedir=basedir).decode()\n  File \"/opt/hostedtoolcache/Python/3.8.6/x64/lib/python3.8/site-packages/onlinejudge_verify/languages/python.py\"\
    , line 85, in bundle\n    raise NotImplementedError\nNotImplementedError\n"
  code: "#!/usr/bin/env python3\nfrom setuptools import find_packages, setup\n\nsetup(\n\
    \    name='online-judge-verify-helper',\n    version='5.2.1',\n    author='Kimiyuki\
    \ Onaka',\n    author_email='kimiyuki95@gmail.com',\n    url='https://github.com/kmyk/online-judge-verify-helper',\n\
    \    license='MIT License',\n    description='',\n    python_requires='>=3.6',\n\
    \    install_requires=[\n        'colorlog',\n        'pyyaml',\n        'online-judge-tools\
    \ >= 8.0.0',\n        'setuptools',\n        'toml',\n        'importlab',\n \
    \   ],\n    packages=find_packages(exclude=('tests', 'docs')),\n    package_data={\n\
    \        'onlinejudge_verify_resources': ['*', '_layouts/*', '_includes/*', 'assets/*',\
    \ 'assets/css/*', 'assets/js/*'],\n    },\n    entry_points={\n        'console_scripts':\
    \ [\n            'oj-verify = onlinejudge_verify.main:main',\n            'oj-bundle\
    \ = onlinejudge_bundle.main:main',\n        ],\n    },\n)\n"
  dependsOn: []
  isVerificationFile: false
  path: setup.py
  requiredBy: []
  timestamp: '1970-01-01 00:00:00+00:00'
  verificationStatus: LIBRARY_NO_TESTS
  verifiedWith: []
documentation_of: setup.py
layout: document
redirect_from:
- /library/setup.py
- /library/setup.py.html
title: setup.py
---
