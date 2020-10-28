# Python Version: 3.x
import argparse
import pathlib
import sys
from logging import DEBUG, basicConfig, getLogger
from typing import *

import colorlog

import onlinejudge_verify.languages.list

logger = getLogger(__name__)


def main(args: Optional[List[str]] = None) -> None:
    # configure logging
    log_format = '%(log_color)s%(levelname)s%(reset)s:%(name)s:%(message)s'
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(log_format))
    basicConfig(level=DEBUG, handlers=[handler])

    # parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=pathlib.Path)
    parser.add_argument('-I', metavar='dir', action='append', type=pathlib.Path, dest='iquote', default=[pathlib.Path.cwd()], help='add the directory dir to the list of directories to be searched for header files during preprocessing (default: ".")')
    parsed = parser.parse_args(args)

    language = onlinejudge_verify.languages.list.get(parsed.path)
    assert language is not None
    sys.stdout.buffer.write(language.bundle(parsed.path, basedir=parsed.iquote[0], options={'include_paths': parsed.iquote}))


if __name__ == "__main__":
    main()
