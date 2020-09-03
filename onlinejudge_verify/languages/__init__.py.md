---
data:
  attributes: {}
  bundledCode: "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/documentation/build.py\"\
    , line 58, in _render_source_code_stat\n    bundled_code = language.bundle(stat.path,\
    \ basedir=basedir).decode()\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/languages/python.py\"\
    , line 84, in bundle\n    raise NotImplementedError\nNotImplementedError\n"
  code: "import pathlib\nfrom logging import getLogger\nfrom typing import *\n\nimport\
    \ toml\nfrom onlinejudge_verify.config import get_config\nfrom onlinejudge_verify.languages.cplusplus\
    \ import CPlusPlusLanguage\nfrom onlinejudge_verify.languages.csharpscript import\
    \ CSharpScriptLanguage\nfrom onlinejudge_verify.languages.models import Language,\
    \ LanguageEnvironment\nfrom onlinejudge_verify.languages.nim import NimLanguage\n\
    from onlinejudge_verify.languages.other import OtherLanguage\nfrom onlinejudge_verify.languages.python\
    \ import PythonLanguage\n\nlogger = getLogger(__name__)\n\n_dict: Optional[Dict[str,\
    \ Language]] = None\n\n\ndef _get_dict() -> Dict[str, Language]:\n    global _dict\n\
    \    if _dict is None:\n        _dict = {}\n        _dict['.cpp'] = CPlusPlusLanguage()\n\
    \        _dict['.hpp'] = _dict['.cpp']\n        _dict['.csx'] = CSharpScriptLanguage()\n\
    \        _dict['.nim'] = NimLanguage()\n        _dict['.py'] = PythonLanguage()\n\
    \n        for ext, config in get_config().get('languages', {}).items():\n    \
    \        if '.' + ext in _dict:\n                for key in ('compile', 'execute',\
    \ 'bundle', 'list_attributes', 'list_dependencies'):\n                    if key\
    \ in config:\n                        raise RuntimeError(\"You cannot overwrite\
    \ existing language: .{}\".format(ext))\n            else:\n                logger.warn(\"\
    config.toml: languages.%s: Adding new languages using `config.toml` is supported\
    \ but not recommended. Please consider making pull requests for your languages,\
    \ see https://github.com/kmyk/online-judge-verify-helper/issues/116\", ext)\n\
    \                _dict['.' + ext] = OtherLanguage(config=config)\n    return _dict\n\
    \n\ndef get(path: pathlib.Path) -> Optional[Language]:\n    return _get_dict().get(path.suffix)\n"
  dependsOn: []
  extendedDependsOn: []
  extendedRequiredBy: []
  extendedVerifiedWith: []
  isVerificationFile: false
  path: onlinejudge_verify/languages/__init__.py
  requiredBy: []
  timestamp: '1970-01-01 00:00:00+00:00'
  verificationStatus: LIBRARY_NO_TESTS
  verificationStatusIcon: ':warning:'
  verifiedWith: []
documentation_of: onlinejudge_verify/languages/__init__.py
layout: document
redirect_from:
- /library/onlinejudge_verify/languages/__init__.py
- /library/onlinejudge_verify/languages/__init__.py.html
title: onlinejudge_verify/languages/__init__.py
---
