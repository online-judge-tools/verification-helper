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

    subparser = subparsers.add_parser('run')
    subparser.add_argument('path', nargs='*', type=pathlib.Path)

    subparser = subparsers.add_parser('init')
    subparser.add_argument('--target', choices=['github-actions'], default='github-actions')

    subparser = subparsers.add_parser('export')
    subparser.add_argument('path', type=pathlib.Path)

    subparser = subparsers.add_parser('docs')

    return parser


def main(args: Optional[List[str]] = None) -> None:
    parser = get_parser()
    parsed = parser.parse_args(args)

    if parsed.subcommand == 'run':
        script = tempfile.NamedTemporaryFile(delete=False)
        script.write(bash_script)
        script.close()
        try:
            subprocess.check_call(['/bin/bash', script.name] + list(map(str, parsed.path)), stdout=sys.stdout, stderr=sys.stderr)
        finally:
            os.remove(script.name)

    elif parsed.subcommand == 'init':
        if parsed.target == 'github-actions':
            path = pathlib.Path('.github/workflows/verify.yml')
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(str(path), 'wb') as fh:
                fh.write(verify_yml)
        else:
            assert False

    elif parsed.subcommand == 'export':
        raise NotImplementedError('#include "hoge.hpp" みたいなやつをいい感じに展開してそのまま提出できる形コードを出力してほしい')

    elif parsed.subcommand == 'docs':
        onlinejudge_verify.docs.main()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
