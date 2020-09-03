---
data:
  attributes: {}
  bundledCode: "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/documentation/build.py\"\
    , line 64, in _render_source_code_stat\n    bundled_code = language.bundle(stat.path,\
    \ basedir=basedir).decode()\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/languages/python.py\"\
    , line 84, in bundle\n    raise NotImplementedError\nNotImplementedError\n"
  code: "# Python Version: 3.x\nimport pathlib\nfrom logging import getLogger\nfrom\
    \ typing import *\n\nimport toml\n\nlogger = getLogger(__name__)\n\ndefault_config_path\
    \ = pathlib.Path('.verify-helper/config.toml')\n\n_loaded_config: Optional[Dict[str,\
    \ Any]] = None\n\n\ndef set_config_path(config_path: pathlib.Path) -> None:\n\
    \    global _loaded_config\n    assert _loaded_config is None\n    if not config_path.exists():\n\
    \        _loaded_config = {}\n        logger.info('no config file')\n    else:\n\
    \        _loaded_config = dict(toml.load(str(config_path)))\n        logger.info('config\
    \ file loaded: %s: %s', str(config_path), _loaded_config)\n\n\ndef get_config()\
    \ -> Dict[str, Any]:\n    if _loaded_config is None:\n        set_config_path(default_config_path)\n\
    \    assert _loaded_config is not None\n    return _loaded_config\n"
  dependsOn: []
  extendedDependsOn: []
  extendedRequiredBy: []
  extendedVerifiedWith: []
  isVerificationFile: false
  path: onlinejudge_verify/config.py
  requiredBy: []
  timestamp: '1970-01-01 00:00:00+00:00'
  verificationStatus: LIBRARY_NO_TESTS
  verificationStatusIcon: ':warning:'
  verifiedWith: []
documentation_of: onlinejudge_verify/config.py
layout: document
redirect_from:
- /library/onlinejudge_verify/config.py
- /library/onlinejudge_verify/config.py.html
title: onlinejudge_verify/config.py
---
