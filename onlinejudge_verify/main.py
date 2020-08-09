"""
isort: skip_file
"""

# pylint: disable=unused-import,ungrouped-imports
try:
    import onlinejudge.service
except ModuleNotFoundError:
    print("Due to a known bug, the online-judge-tools is not yet properly installed. Please re-run $ pip3 install --force-reinstall online-judge-api-client")
    exit(1)
# pylint: enable=unused-import,ungrouped-imports

import argparse
import glob
import math
import os
import pathlib
import subprocess
import sys
import textwrap
from logging import INFO, basicConfig, getLogger
from typing import *

import onlinejudge_verify.config
import onlinejudge_verify.docs
import onlinejudge_verify.marker
import onlinejudge_verify.utils
import onlinejudge_verify.verify

logger = getLogger(__name__)


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('--config-file', default=onlinejudge_verify.config.default_config_path, help='default: ".verify-helper/config.toml"')

    subparsers = parser.add_subparsers(dest='subcommand')

    subparser = subparsers.add_parser('all')
    subparser.add_argument('-j', '--jobs', type=int, default=1)
    subparser.add_argument('--timeout', type=float, default=600)
    subparser.add_argument('--tle', type=float, default=60)

    subparser = subparsers.add_parser('run')
    subparser.add_argument('path', nargs='*', type=pathlib.Path)
    subparser.add_argument('-j', '--jobs', type=int, default=1)
    subparser.add_argument('--timeout', type=float, default=600)
    subparser.add_argument('--tle', type=float, default=60)

    subparser = subparsers.add_parser('docs')

    return parser


def subcommand_run(paths: List[pathlib.Path], *, timeout: float = 600, tle: float = 60, jobs: int = 1) -> onlinejudge_verify.verify.VerificationSummary:
    """
    :raises Exception: if test.sh fails
    """

    does_push = 'GITHUB_ACTION' in os.environ and 'GITHUB_TOKEN' in os.environ and os.environ.get('GITHUB_REF', '').startswith('refs/heads/')  # NOTE: $GITHUB_REF may be refs/pull/... or refs/tags/...
    if does_push:
        # checkout in advance to push
        branch = os.environ['GITHUB_REF'][len('refs/heads/'):]
        logger.info('$ git checkout %s', branch)
        subprocess.check_call(['git', 'checkout', branch])

    # NOTE: the GITHUB_TOKEN expires in 60 minutes (https://help.github.com/en/actions/automating-your-workflow-with-github-actions/authenticating-with-the-github_token#about-the-github_token-secret)
    # use 10 minutes as timeout for safety; 理由はよく分かってないぽいけど以前 20 分でやって死んだことがあるらしいので
    if 'GITHUB_ACTION' not in os.environ:
        timeout = math.inf

    if not paths:
        paths = sorted(list(onlinejudge_verify.utils.iterate_verification_files()))
    try:
        with onlinejudge_verify.marker.get_verification_marker() as marker:
            return onlinejudge_verify.verify.main(paths, marker=marker, timeout=timeout, tle=tle, jobs=jobs)
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
    subprocess.check_call(['git', 'config', '--global', 'user.name', 'GitHub'])
    subprocess.check_call(['git', 'config', '--global', 'user.email', 'noreply@github.com'])
    path = onlinejudge_verify.marker.get_verification_marker().json_path
    logger.info('$ git add %s && git commit && git push', str(path))
    if path.exists():
        subprocess.check_call(['git', 'add', str(path)])
    if subprocess.run(['git', 'diff', '--quiet', '--staged']).returncode:
        message = '[auto-verifier] verify commit {}'.format(os.environ['GITHUB_SHA'])
        subprocess.check_call(['git', 'commit', '-m', message])
        subprocess.check_call(['git', 'push', url, 'HEAD'])


def push_documents_to_gh_pages(*, src_dir: pathlib.Path, dst_branch: str = 'gh-pages') -> None:
    # read config
    if not os.environ.get('GH_PAT'):
        # If we push commits using GITHUB_TOKEN, the build of GitHub Pages will not run. See https://github.com/marketplace/actions/github-pages-deploy#secrets and https://github.com/maxheld83/ghpages/issues/1
        logger.error("GH_PAT is not available. You cannot upload the generated documents to GitHub Pages.")
        return
    logger.info('use GH_PAT')
    url = 'https://{}@github.com/{}.git'.format(os.environ['GH_PAT'], os.environ['GITHUB_REPOSITORY'])
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
    subprocess.check_call(['rm', '.verify-helper/.gitignore'])  # required, to remove .gitignore even if it is untracked
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
    if 'GITHUB_ACTION' in os.environ and 'GITHUB_TOKEN' in os.environ:
        if os.environ['GITHUB_REF'] == 'refs/heads/master':
            logger.info('generate documents...')
            onlinejudge_verify.docs.main()

            logger.info('upload documents...')
            push_documents_to_gh_pages(src_dir=pathlib.Path('.verify-helper/markdown'))

    else:
        logger.info('generate documents...')
        onlinejudge_verify.docs.main()
        logger.info('done.')
        logger.info('%s', '\n'.join([
            'To see the generated document, do the following steps:',
            '    1. Install Ruby with the files to build native modules. In Ubuntu, $ sudo apt install ruby-all-dev',
            "    2. Install Ruby's Bundler (https://bundler.io/). In Ubuntu, $ sudo apt install ruby-bundler",
            '    3. $ cd .verify-helper/markdown',
            '    4. $ bundle install --path .vendor/bundle',
            '    5. $ bundle exec jekyll serve --incremental',
            '    6. Open http://127.0.0.1:4000 on your web browser',
        ]))


def generate_gitignore() -> None:
    path = pathlib.Path('.verify-helper/.gitignore')
    data = textwrap.dedent("""\
        .gitignore
        cache/
        include/
        markdown/
        timestamps.local.json
    """)
    if path.exists():
        with open(path) as fh:
            if fh.read() == data:
                return
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as fh:
        fh.write(data)


def main(args: Optional[List[str]] = None) -> None:
    basicConfig(level=INFO)
    parser = get_parser()
    parsed = parser.parse_args(args)

    # load the config file as a global variable
    onlinejudge_verify.config.set_config_path(pathlib.Path(parsed.config_file))

    if getattr(parsed, 'jobs', None) is not None:
        # 先に並列で読み込みしておく
        onlinejudge_verify.marker.get_verification_marker(jobs=parsed.jobs)

    if parsed.subcommand == 'all':
        generate_gitignore()
        summary = subcommand_run(paths=[], timeout=parsed.timeout, tle=parsed.tle, jobs=parsed.jobs)
        subcommand_docs()
        summary.show()
        if not summary.succeeded():
            sys.exit(1)

    elif parsed.subcommand == 'run':
        generate_gitignore()
        summary = subcommand_run(paths=parsed.path, timeout=parsed.timeout, tle=parsed.tle, jobs=parsed.jobs)
        summary.show()
        if not summary.succeeded():
            sys.exit(1)

    elif parsed.subcommand == 'docs':
        generate_gitignore()
        subcommand_docs()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
