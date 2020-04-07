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
    with open(path) as fh:
        for line in fh.readlines():
            matched = pattern.search(line)
            if matched:
                key = matched.group(1)
                value = (matched.group(2) or '').strip()
                attributes[key] = value
            elif failure_pattern.search(line):
                logger.warning('broken verify-helper special comment found: %s', line)
    return attributes
