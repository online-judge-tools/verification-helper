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
  code: "# Python Version: 3.x\nimport argparse\nimport pathlib\nimport sys\nfrom\
    \ logging import DEBUG, basicConfig, getLogger\nfrom typing import *\n\nimport\
    \ colorlog\nimport onlinejudge_verify.languages\n\nlogger = getLogger(__name__)\n\
    \n\ndef main(args: Optional[List[str]] = None) -> None:\n    # configure logging\n\
    \    log_format = '%(log_color)s%(levelname)s%(reset)s:%(name)s:%(message)s'\n\
    \    handler = colorlog.StreamHandler()\n    handler.setFormatter(colorlog.ColoredFormatter(log_format))\n\
    \    basicConfig(level=DEBUG, handlers=[handler])\n\n    # parse command-line\
    \ arguments\n    parser = argparse.ArgumentParser()\n    parser.add_argument('path',\
    \ type=pathlib.Path)\n    parser.add_argument('-I', metavar='dir', type=pathlib.Path,\
    \ dest='iquote', default=pathlib.Path.cwd(), help='add the directory dir to the\
    \ list of directories to be searched for header files during preprocessing (default:\
    \ \".\")')\n    parsed = parser.parse_args(args)\n\n    language = onlinejudge_verify.languages.get(parsed.path)\n\
    \    assert language is not None\n    sys.stdout.buffer.write(language.bundle(parsed.path,\
    \ basedir=parsed.iquote))\n\n\nif __name__ == \"__main__\":\n    main()\n"
  dependsOn: []
  isVerificationFile: false
  path: onlinejudge_bundle/main.py
  requiredBy: []
  timestamp: '1970-01-01 00:00:00+00:00'
  verificationStatus: LIBRARY_NO_TESTS
  verifiedWith: []
documentation_of: onlinejudge_bundle/main.py
layout: document
redirect_from:
- /library/onlinejudge_bundle/main.py
- /library/onlinejudge_bundle/main.py.html
title: onlinejudge_bundle/main.py
---
