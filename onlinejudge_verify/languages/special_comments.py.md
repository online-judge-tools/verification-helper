---
data:
  _extendedDependsOn: []
  _extendedRequiredBy: []
  _extendedVerifiedWith: []
  _pathExtension: py
  _verificationStatusIcon: ':warning:'
  attributes:
    links:
    - '"https://atcoder.jp/"`.'
    - https://www.python.org/dev/peps/pep-0263/
  bundledCode: "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/documentation/build.py\"\
    , line 70, in _render_source_code_stat\n    bundled_code = language.bundle(stat.path,\
    \ basedir=basedir).decode()\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/languages/python.py\"\
    , line 84, in bundle\n    raise NotImplementedError\nNotImplementedError\n"
  code: "# Python Version: 3.x\nimport functools\nimport pathlib\nimport re\nfrom\
    \ logging import getLogger\nfrom typing import *\n\nlogger = getLogger(__name__)\n\
    \n\n# special comments like Vim and Python: see https://www.python.org/dev/peps/pep-0263/\n\
    @functools.lru_cache(maxsize=None)\ndef list_special_comments(path: pathlib.Path)\
    \ -> Dict[str, str]:\n    pattern = re.compile(r'\\bverify-helper:\\s*([0-9A-Z_]+)(?:\\\
    s(.*))?$')\n    failure_pattern = re.compile(r'\\bverify-helper:')\n    attributes\
    \ = {}\n    with open(path, 'rb') as fh:\n        for line in fh.read().decode().splitlines():\n\
    \            matched = pattern.search(line)\n            if matched:\n       \
    \         key = matched.group(1)\n                value = (matched.group(2) or\
    \ '').strip()\n                attributes[key] = value\n            elif failure_pattern.search(line):\n\
    \                logger.warning('broken verify-helper special comment found: %s',\
    \ line)\n    return attributes\n\n\n@functools.lru_cache(maxsize=None)\ndef list_doxygen_annotations(path:\
    \ pathlib.Path) -> Dict[str, str]:\n    pattern = re.compile(r'@(title|category|brief|docs|see|sa|ignore)\
    \ (.*)')\n    attributes = {}\n    with open(path, 'rb') as fh:\n        for line\
    \ in fh.read().decode().splitlines():\n            matched = pattern.search(line)\n\
    \            if matched:\n                key = matched.group(1)\n           \
    \     value = matched.group(2).strip()\n                if key == 'docs':\n  \
    \                  attributes['_deprecated_at_docs'] = value\n               \
    \     logger.warning('deprecated annotation: \"@%s %s\" in %s.  use front-matter\
    \ style instead', key, value, str(path))\n                elif key in ('title',\
    \ 'brief'):\n                    if 'document_title' in attributes:\n        \
    \                continue\n                    attributes['document_title'] =\
    \ value\n                elif key in ('category', 'see', 'sa', 'ignore'):\n  \
    \                  logger.debug('ignored annotation: \"@%s %s\" in %s', key, value,\
    \ str(path))\n                    if key == 'ignore':\n                      \
    \  logger.warning('Now `@ignore` has no effect. Please write as `exlucde: [\"\
    %s\"]` at `.verify-helper/docs/_config.yml` instead.', value)\n              \
    \  else:\n                    assert False\n    return attributes\n\n\n@functools.lru_cache(maxsize=None)\n\
    def list_embedded_urls(path: pathlib.Path) -> List[str]:\n    pattern = re.compile(r\"\
    \"\"['\"`]?https?://\\S*\"\"\")  # use a broad pattern. There are no needs to\
    \ make match strict.\n    with open(path, 'rb') as fh:\n        content = fh.read().decode()\n\
    \    urls = []\n    for url in pattern.findall(content):\n        # The URL may\
    \ be written like `\"https://atcoder.jp/\"`. In this case, we need to remove `\"\
    `s around the URL.\n        for quote in (\"'\", '\"', '`'):\n            if len(url)\
    \ >= 2 and url.startswith(quote) and url.endswith(quote):\n                url\
    \ = url[1:-1]\n                break\n        urls.append(url)\n    return sorted(set(urls))\n"
  dependsOn: []
  isVerificationFile: false
  path: onlinejudge_verify/languages/special_comments.py
  requiredBy: []
  timestamp: '1970-01-01 00:00:00+00:00'
  verificationStatus: LIBRARY_NO_TESTS
  verifiedWith: []
documentation_of: onlinejudge_verify/languages/special_comments.py
layout: document
redirect_from:
- /library/onlinejudge_verify/languages/special_comments.py
- /library/onlinejudge_verify/languages/special_comments.py.html
title: onlinejudge_verify/languages/special_comments.py
---
