# Python Version: 3.x
import argparse
import os
import pathlib
import subprocess
import sys
import tempfile
from typing import *

import onlinejudge_verify.docs
import pkg_resources

package = 'onlinejudge_verify.data'
bash_script = pkg_resources.resource_string(package, 'test.sh')
verify_yml = pkg_resources.resource_string(package, 'verify.yml')


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subcommand')

    subparser = subparsers.add_parser('all')

    subparser = subparsers.add_parser('run')
    subparser.add_argument('path', nargs='*', type=pathlib.Path)

    subparser = subparsers.add_parser('init')

    subparser = subparsers.add_parser('export')
    subparser.add_argument('path', type=pathlib.Path)

    subparser = subparsers.add_parser('docs')

    return parser


def subcommand_run(paths: List[str]) -> None:
    """
    :raises Exception: if test.sh fails
    """

    script = tempfile.NamedTemporaryFile(delete=False)
    script.write(bash_script)
    script.close()
    try:
        subprocess.check_call(['/bin/bash', script.name] + list(map(str, paths)), stdout=sys.stdout, stderr=sys.stderr)
    finally:
        os.remove(script.name)


def subcommand_init() -> None:
    path = pathlib.Path('.github/workflows/verify.yml')
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(str(path), 'wb') as fh:
        fh.write(verify_yml)


def main(args: Optional[List[str]] = None) -> None:
    parser = get_parser()
    parsed = parser.parse_args(args)

    if parsed.subcommand == 'all':
        subcommand_run(paths=[])
        onlinejudge_verify.docs.main()

    elif parsed.subcommand == 'run':
        subcommand_run(paths=parsed.path)

    elif parsed.subcommand == 'init':
        subcommand_init()

    elif parsed.subcommand == 'export':
        raise NotImplementedError('#include "hoge.hpp" みたいなやつをいい感じに展開してそのまま提出できる形コードを出力してほしい')

    elif parsed.subcommand == 'docs':
        onlinejudge_verify.docs.main()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
