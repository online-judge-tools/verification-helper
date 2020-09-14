# Python Version: 3.x
import functools
import pathlib
import re
from logging import getLogger
from typing import *

logger = getLogger(__name__)


# special comments like Vim and Python: see https://www.python.org/dev/peps/pep-0263/
@functools.lru_cache(maxsize=None)
def list_special_comments(path: pathlib.Path) -> Dict[str, str]:
    pattern = re.compile(r'\bverify-helper:\s*([0-9A-Z_]+)(?:\s(.*))?$')
    failure_pattern = re.compile(r'\bverify-helper:')
    attributes = {}
    with open(path, 'rb') as fh:
        for line in fh.read().decode().splitlines():
            matched = pattern.search(line)
            if matched:
                key = matched.group(1)
                value = (matched.group(2) or '').strip()
                attributes[key] = value
            elif failure_pattern.search(line):
                logger.warning('broken verify-helper special comment found: %s', line)
    return attributes


@functools.lru_cache(maxsize=None)
def list_doxygen_annotations(path: pathlib.Path) -> Dict[str, str]:
    pattern = re.compile(r'@(title|category|brief|docs|see|sa|ignore) (.*)')
    attributes = {}
    with open(path, 'rb') as fh:
        for line in fh.read().decode().splitlines():
            matched = pattern.search(line)
            if matched:
                key = matched.group(1)
                value = matched.group(2).strip()
                if key == 'docs':
                    attributes['_deprecated_at_docs'] = value
                    logger.warning('deprecated annotation: "@%s %s" in %s.  use front-matter style instead', key, value, str(path))
                elif key in ('title', 'brief'):
                    if 'document_title' in attributes:
                        continue
                    attributes['document_title'] = value
                elif key in ('category', 'see', 'sa', 'ignore'):
                    logger.debug('ignored annotation: "@%s %s" in %s', key, value, str(path))
                    if key == 'ignore':
                        logger.warning('Now `@ignore` has no effect. Please write as `exlucde: ["%s"]` at `.verify-helper/docs/_config.yml` instead.', value)
                else:
                    assert False
    return attributes


@functools.lru_cache(maxsize=None)
def list_embedded_urls(path: pathlib.Path) -> List[str]:
    pattern = re.compile(r"""['"`]?https?://\S*""")  # use a broad pattern. There are no needs to make match strict.
    with open(path, 'rb') as fh:
        content = fh.read().decode()
    urls = []
    for url in pattern.findall(content):
        # The URL may be written like `"https://atcoder.jp/"`. In this case, we need to remove `"`s around the URL.
        for quote in ("'", '"', '`'):
            if len(url) >= 2 and url.startswith(quote) and url.endswith(quote):
                url = url[1:-1]
                break
        urls.append(url)
    return sorted(set(urls))
