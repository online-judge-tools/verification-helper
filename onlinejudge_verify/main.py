# Python Version: 3.x
import argparse
import glob
import os
import pathlib
import subprocess
import sys
import tempfile
from logging import DEBUG, basicConfig, getLogger
from typing import *

import onlinejudge_verify.docs
import pkg_resources

package = 'onlinejudge_verify.data'
bash_script = pkg_resources.resource_string(package, 'test.sh')
verify_yml = pkg_resources.resource_string(package, 'verify.yml')

logger = getLogger(__name__)


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
        fh.write(verify_yml.replace(b'git+https://github.com/kmyk/online-judge-verify-helper.git@master', b'"online-judge-verify-helper==2.*"'))


def push_documents_to_gh_pages(*, src_dir: pathlib.Path, dst_branch: str = 'gh-pages') -> None:
    # read config
    username, reponame = os.environ['GITHUB_REPOSITORY'].split('/')
    url = 'https://{}:{}@github.com/{}/{}'.format(username, os.environ['GITHUB_TOKEN'], username, reponame)
    logger.info('username = %s', username)
    logger.info('reponame = %s', reponame)

    # read files before checkout
    logger.info('read files from %s', str(src_dir))
    src_files = {}
    for path in map(pathlib.Path, glob.glob(str(src_dir) + '/**/*', recursive=True)):
        if path.is_file():
            logger.info('%s', str(path))
            with open(str(path), 'rb') as fh:
                src_files[path.relative_to(src_dir)] = fh.read()

    # checkout gh-pages
    logger.info('$ git checkout %s', dst_branch)
    subprocess.check_call(['git', 'stash'])
    subprocess.check_call(['git', 'checkout', dst_branch])

    # remove all non-hidden files and write new files
    logger.info('write files to . on %s', dst_branch)
    for path in map(pathlib.Path, glob.glob('**/*', recursive=True)):
        if path.is_file():
            path.unlink()
    for path, data in src_files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(str(path), 'wb') as fh:
            fh.write(data)

    # commit and push
    logger.info('$ git add . && git commit && git push')
    author = '{} <online-judge-verify-helper@example.com>'.format(username)
    message = '[auto-verifier] docs commit {}'.format(os.environ['GITHUB_SHA'])
    subprocess.check_call(['git', 'add', '.'])
    subprocess.check_call(['git', 'commit', '--author', author, '-m', message])
    subprocess.check_call(['git', 'push', url, 'HEAD'])


def subcommand_docs() -> None:
    logger.info('generate documents...')
    onlinejudge_verify.docs.main()

    if 'GITHUB_ACTION' in os.environ and os.environ['GITHUB_REF'] == 'refs/heads/master':
        logger.info('upload documents...')
        push_documents_to_gh_pages(src_dir=pathlib.Path('md-output'))


def main(args: Optional[List[str]] = None) -> None:
    basicConfig(level=DEBUG)
    parser = get_parser()
    parsed = parser.parse_args(args)

    if parsed.subcommand == 'all':
        subcommand_run(paths=[])
        subcommand_docs()

    elif parsed.subcommand == 'run':
        subcommand_run(paths=parsed.path)

    elif parsed.subcommand == 'init':
        subcommand_init()

    elif parsed.subcommand == 'export':
        raise NotImplementedError('#include "hoge.hpp" みたいなやつをいい感じに展開してそのまま提出できる形コードを出力してほしい')

    elif parsed.subcommand == 'docs':
        subcommand_docs()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
