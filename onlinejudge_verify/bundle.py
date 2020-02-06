# Python Version: 3.x
import argparse
import pathlib
import sys
from logging import DEBUG, basicConfig, getLogger
from typing import *

import onlinejudge_verify.languages

logger = getLogger(__name__)


def main(args: Optional[List[str]] = None) -> None:
    basicConfig(level=DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=pathlib.Path)
    parser.add_argument('-I', metavar='dir', type=pathlib.Path, dest='iquote', default=pathlib.Path.cwd(), help='add the directory dir to the list of directories to be searched for header files during preprocessing (default: ".")')
    parsed = parser.parse_args(args)

    language = onlinejudge_verify.languages.get(parsed.path)
    assert language is not None
    sys.stdout.buffer.write(language.bundle(parsed.path, basedir=parsed.iquote))


if __name__ == "__main__":
    main()
