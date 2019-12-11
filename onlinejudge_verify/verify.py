# Python Version: 3.x
import os
import pathlib
import subprocess
import sys
import tempfile
from logging import getLogger
from typing import *

import pkg_resources

package = 'onlinejudge_verify.data'
bash_script = pkg_resources.resource_string(package, 'test.sh')

logger = getLogger(__name__)


def main(paths: List[pathlib.Path]) -> None:
    script = tempfile.NamedTemporaryFile(delete=False)
    script.write(bash_script)
    script.close()
    try:
        for path in paths:
            logger.info('verify %s', path)
            subprocess.check_call(['/bin/bash', script.name, path], stdout=sys.stdout, stderr=sys.stderr)
    finally:
        os.remove(script.name)
