# Python Version: 3.x
import argparse
import glob
import math
import os
import pathlib
import subprocess
import sys
from logging import DEBUG, basicConfig, getLogger
from typing import *

import onlinejudge_verify.docs
import onlinejudge_verify.languages
import onlinejudge_verify.marker
import onlinejudge_verify.verify

logger = getLogger(__name__)


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subcommand')

    subparser = subparsers.add_parser('all')
    subparser.add_argument('-j', '--jobs', type=int, default=1)

    subparser = subparsers.add_parser('run')
    subparser.add_argument('path', nargs='*', type=pathlib.Path)
    subparser.add_argument('-j', '--jobs', type=int, default=1)

    subparser = subparsers.add_parser('init')

    subparser = subparsers.add_parser('bundle')
    subparser.add_argument('path', type=pathlib.Path)
    subparser.add_argument('-I', metavar='dir', type=pathlib.Path, dest='iquote', default=pathlib.Path.cwd(), help='add the directory dir to the list of directories to be searched for header files during preprocessing (default: ".")')

    subparser = subparsers.add_parser('docs')

    return parser


def subcommand_run(paths: List[pathlib.Path], *, jobs: int = 1) -> None:
    """
    :raises Exception: if test.sh fails
    """

    does_push = 'GITHUB_ACTION' in os.environ and os.environ.get('GITHUB_REF', '').startswith('refs/heads/')  # NOTE: $GITHUB_REF may be refs/pull/... or refs/tags/...
    if does_push:
        # checkout in advance to push
        branch = os.environ['GITHUB_REF'][len('refs/heads/'):]
        logger.info('$ git checkout %s', branch)
        subprocess.check_call(['git', 'checkout', branch])

    # NOTE: the GITHUB_TOKEN expires in 60 minutes (https://help.github.com/en/actions/automating-your-workflow-with-github-actions/authenticating-with-the-github_token#about-the-github_token-secret)
    # use 10 minutes as timeout for safety; 理由はよく分かってないぽいけど以前 20 分でやって死んだことがあるらしいので
    timeout = 10 * 60 if 'GITHUB_ACTION' in os.environ else math.inf

    if not paths:
        for path in pathlib.Path.cwd().glob('**/*.test.*'):
            if onlinejudge_verify.languages.get(path):
                paths.append(path)
        paths = sorted(paths)
    try:
        with onlinejudge_verify.marker.get_verification_marker() as marker:
            onlinejudge_verify.verify.main(paths, marker=marker, timeout=timeout, jobs=jobs)
    finally:
        # push results even if some tests failed
        if does_push:
            push_timestamp_to_branch()


def push_timestamp_to_branch() -> None:
    # read config
    logger.info('use GITHUB_TOKEN')  # NOTE: don't use GH_PAT here, because it may cause infinite loops with triggering GitHub Actions itself
    url = 'https://{}:{}@github.com/{}.git'.format(os.environ['GITHUB_ACTOR'], os.environ['GITHUB_TOKEN'], os.environ['GITHUB_REPOSITORY'])
    logger.info('GITHUB_ACTOR = %s', os.environ['GITHUB_ACTOR'])
    logger.info('GITHUB_REPOSITORY = %s', os.environ['GITHUB_REPOSITORY'])

    # commit and push
    logger.info('$ git add .verify-helper && git commit && git push')
    subprocess.check_call(['git', 'config', '--global', 'user.name', 'GitHub'])
    subprocess.check_call(['git', 'config', '--global', 'user.email', 'noreply@github.com'])
    subprocess.check_call(['git', 'add', onlinejudge_verify.marker.get_verification_marker().json_path])
    if subprocess.run(['git', 'diff', '--quiet', '--staged']).returncode:
        message = '[auto-verifier] verify commit {}'.format(os.environ['GITHUB_SHA'])
        subprocess.check_call(['git', 'commit', '-m', message])
        subprocess.check_call(['git', 'push', url, 'HEAD'])


def push_documents_to_gh_pages(*, src_dir: pathlib.Path, dst_branch: str = 'gh-pages') -> None:
    # read config
    if os.environ.get('GH_PAT', None):
        logger.info('use GH_PAT')
        # see https://github.com/marketplace/actions/github-pages-deploy#secrets and https://github.com/maxheld83/ghpages/issues/1
        url = 'https://{}@github.com/{}.git'.format(os.environ['GH_PAT'], os.environ['GITHUB_REPOSITORY'])
    else:
        logger.info('use GITHUB_TOKEN')
        url = 'https://{}:{}@github.com/{}.git'.format(os.environ['GITHUB_ACTOR'], os.environ['GITHUB_TOKEN'], os.environ['GITHUB_REPOSITORY'])
    logger.info('GITHUB_ACTOR = %s', os.environ['GITHUB_ACTOR'])
    logger.info('GITHUB_REPOSITORY = %s', os.environ['GITHUB_REPOSITORY'])

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
    try:
        subprocess.check_call(['git', 'checkout', dst_branch])
    except subprocess.CalledProcessError:
        subprocess.check_call(['git', 'checkout', '--orphan', dst_branch])

    # remove all non-hidden files and write new files
    logger.info('write files to . on %s', dst_branch)
    for pattern in ('**/*', '.*/**/*'):
        for path in map(pathlib.Path, glob.glob(pattern, recursive=True)):
            if path.is_file() and path.parts[0] != '.git':
                path.unlink()
    for path, data in src_files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(str(path), 'wb') as fh:
            fh.write(data)

    # commit and push
    logger.info('$ git add . && git commit && git push')
    subprocess.check_call(['git', 'config', '--global', 'user.name', 'GitHub'])
    subprocess.check_call(['git', 'config', '--global', 'user.email', 'noreply@github.com'])
    subprocess.check_call(['git', 'add', '.'])
    if subprocess.run(['git', 'diff', '--quiet', '--staged']).returncode:
        message = '[auto-verifier] docs commit {}'.format(os.environ['GITHUB_SHA'])
        subprocess.check_call(['git', 'commit', '-m', message])
        subprocess.check_call(['git', 'push', url, 'HEAD'])


def subcommand_docs() -> None:
    if 'GITHUB_ACTION' in os.environ:
        if os.environ['GITHUB_REF'] == 'refs/heads/master':
            logger.info('generate documents...')
            onlinejudge_verify.docs.main(html=False, force=True)

            logger.info('upload documents...')
            push_documents_to_gh_pages(src_dir=pathlib.Path('.verify-helper/markdown'))

    else:
        logger.info('generate documents...')
        onlinejudge_verify.docs.main(html=False, force=True)


def subcommand_bundle(path: pathlib.Path, *, iquote: pathlib.Path) -> None:
    language = onlinejudge_verify.languages.get(path)
    assert language is not None
    sys.stdout.buffer.write(language.bundle(path, basedir=iquote))


def main(args: Optional[List[str]] = None) -> None:
    basicConfig(level=DEBUG)
    parser = get_parser()
    parsed = parser.parse_args(args)

    if getattr(parsed, 'jobs', None) is not None:
        # 先に並列で読み込みしておく
        onlinejudge_verify.marker.get_verification_marker(jobs=parsed.jobs)

    if parsed.subcommand == 'all':
        try:
            subcommand_run(paths=[], jobs=parsed.jobs)
        finally:
            # generate documents even if some tests failed
            subcommand_docs()

    elif parsed.subcommand == 'run':
        subcommand_run(paths=parsed.path, jobs=parsed.jobs)

    elif parsed.subcommand == 'bundle':
        subcommand_bundle(parsed.path, iquote=parsed.iquote)

    elif parsed.subcommand == 'docs':
        subcommand_docs()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
