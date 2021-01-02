"""
isort: skip_file
"""

# pylint: disable=unused-import,ungrouped-imports
try:
    import onlinejudge.service
except ModuleNotFoundError:
    print("Due to a known bug, the online-judge-tools is not yet properly installed. Please re-run $ pip3 install --force-reinstall online-judge-api-client")
    exit(1)  # pylint: disable=consider-using-sys-exit
# pylint: enable=unused-import,ungrouped-imports

import argparse
import json
import glob
import math
import os
import pathlib
import urllib.request
import subprocess
import sys
import textwrap
from logging import INFO, basicConfig, getLogger
from typing import *

import colorlog
import onlinejudge_verify.config
import onlinejudge_verify.documentation.main
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
    subparser.add_argument('-j', '--jobs', type=int, default=1)

    subparser = subparsers.add_parser('stats')
    subparser.add_argument('-j', '--jobs', type=int, default=1)

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
    if subprocess.run(['git', 'diff', '--quiet', '--staged'], check=False).returncode:
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
    if subprocess.run(['git', 'diff', '--quiet', '--staged'], check=False).returncode:
        message = '[auto-verifier] docs commit {}'.format(os.environ['GITHUB_SHA'])
        subprocess.check_call(['git', 'commit', '-m', message])
        subprocess.check_call(['git', 'push', url, 'HEAD'])


def subcommand_docs(*, jobs: int = 1) -> None:
    if 'GITHUB_ACTION' in os.environ and 'GITHUB_TOKEN' in os.environ:
        # check it is kicked by "push" event
        if os.environ['GITHUB_EVENT_NAME'] != 'push':
            logger.info('This execution is not kicked from "push" event. Updating GitHub Pages is skipped.')
            return

        # check it is on the default branch.
        try:
            # /repos/{owner}/{repo} endpoint. See https://docs.github.com/en/free-pro-team@latest/rest/reference/repos#get-a-repository
            req = urllib.request.Request(os.environ['GITHUB_API_URL'] + '/repos/' + os.environ['GITHUB_REPOSITORY'])
            req.add_header('authorization', 'Bearer ' + os.environ['GITHUB_TOKEN'])
            with urllib.request.urlopen(req) as fh:
                repos = json.loads(fh.read())
            default_branch = repos['default_branch']
        except Exception as e:
            logger.exception('failed to get the default branch: %s', e)
            logger.info('Updating GitHub Pages is skipped.')
            return
        if os.environ['GITHUB_REF'] != 'refs/heads/{}'.format(default_branch):
            logger.info('This execution is not on the default branch (the default is "refs/heads/%s" but the actual is "%s"). Updating GitHub Pages is skipped.', default_branch, os.environ['GITHUB_REF'])
            return

        # updating the GitHub Pages
        logger.info('generate documents...')
        onlinejudge_verify.documentation.main.main(jobs=jobs)

        logger.info('upload documents...')
        push_documents_to_gh_pages(src_dir=pathlib.Path('.verify-helper/markdown'))

    else:
        logger.info('generate documents...')
        onlinejudge_verify.documentation.main.main(jobs=jobs)
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


def subcommand_stats(*, jobs: int = 1) -> None:
    onlinejudge_verify.documentation.main.print_stats_json(jobs=jobs)


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


# TODO: remove this function when affected people disappears. You can see the list of such people at https://github.com/search?q=%22timestamps.local.json%22+language%3Agitignore&type=Code
def _delete_gitignore() -> None:
    """A workaround for the issue https://github.com/online-judge-tools/verification-helper/issues/332
    """

    try:
        # check if it's on GitHub Action
        should_push = 'GITHUB_ACTION' in os.environ and 'GITHUB_TOKEN' in os.environ and os.environ.get('GITHUB_REF', '').startswith('refs/heads/')
        if not should_push:
            return

        # checkout the target branch
        branch = os.environ['GITHUB_REF'][len('refs/heads/'):]
        logger.info('$ git checkout %s', branch)
        subprocess.check_call(['git', 'checkout', branch])

        # check if .verify-helper/.gitignore exists
        gitignore_path = pathlib.Path('.verify-helper', '.gitignore')
        gitignore_checked_in = (subprocess.run(['git', 'ls-files', '--error-unmatch', str(gitignore_path)], check=False).returncode == 0)
        if not gitignore_checked_in:
            return
        logger.warning('file %s exists in this Git repository. It should not be checked in.', str(gitignore_path))

        # read config
        logger.info('use GITHUB_TOKEN')  # NOTE: don't use GH_PAT here, because it may cause infinite loops with triggering GitHub Actions itself
        url = 'https://{}:{}@github.com/{}.git'.format(os.environ['GITHUB_ACTOR'], os.environ['GITHUB_TOKEN'], os.environ['GITHUB_REPOSITORY'])
        logger.info('GITHUB_ACTOR = %s', os.environ['GITHUB_ACTOR'])
        logger.info('GITHUB_REPOSITORY = %s', os.environ['GITHUB_REPOSITORY'])

        # remove .verify-helper/.gitignore
        subprocess.check_call(['git', 'config', '--global', 'user.name', 'GitHub'])
        subprocess.check_call(['git', 'config', '--global', 'user.email', 'noreply@github.com'])
        logger.info('$ git rm --cached %s', str(gitignore_path))
        subprocess.check_call(['git', 'rm', '--cached', str(gitignore_path)])
        message = '[auto-verifier] remove .verify-helper/.gitignore (see https://github.com/online-judge-tools/verification-helper/issues/332)'
        logger.info('$ git commit -m ...')
        subprocess.check_call(['git', 'commit', '-m', message])
        logger.info('$ git push ... HEAD')
        subprocess.check_call(['git', 'push', url, 'HEAD'])

    except Exception:
        logger.exception('something wrong in _delete_gitignore(). ignored.')


def main(args: Optional[List[str]] = None) -> None:
    # configure logging
    log_format = '%(log_color)s%(levelname)s%(reset)s:%(name)s:%(message)s'
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(log_format))
    basicConfig(level=INFO, handlers=[handler])

    # parse command-line arguments
    parser = get_parser()
    parsed = parser.parse_args(args)

    # load the config file as a global variable
    onlinejudge_verify.config.set_config_path(pathlib.Path(parsed.config_file))

    if getattr(parsed, 'jobs', None) is not None:
        # 先に並列で読み込みしておく
        onlinejudge_verify.marker.get_verification_marker(jobs=parsed.jobs)

    if parsed.subcommand == 'all':
        _delete_gitignore()
        generate_gitignore()
        summary = subcommand_run(paths=[], timeout=parsed.timeout, tle=parsed.tle, jobs=parsed.jobs)
        subcommand_docs(jobs=parsed.jobs)
        summary.show()
        if not summary.succeeded():
            sys.exit(1)

    elif parsed.subcommand == 'run':
        _delete_gitignore()
        generate_gitignore()
        summary = subcommand_run(paths=parsed.path, timeout=parsed.timeout, tle=parsed.tle, jobs=parsed.jobs)
        summary.show()
        if not summary.succeeded():
            sys.exit(1)

    elif parsed.subcommand == 'docs':
        _delete_gitignore()
        generate_gitignore()
        subcommand_docs(jobs=parsed.jobs)

    elif parsed.subcommand == 'stats':
        subcommand_stats(jobs=parsed.jobs)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
