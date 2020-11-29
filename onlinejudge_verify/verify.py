# Python Version: 3.x
import hashlib
import math
import os
import pathlib
import subprocess
import time
import traceback
from logging import getLogger
from typing import *

import onlinejudge
import onlinejudge_verify.languages.list
import onlinejudge_verify.marker

logger = getLogger(__name__)


class VerificationSummary:
    def __init__(self, *, failed_test_paths: List[pathlib.Path]):
        self.failed_test_paths = failed_test_paths

    def show(self) -> None:
        if self.failed_test_paths:
            logger.error('%d tests failed', len(self.failed_test_paths))
            for path in self.failed_test_paths:
                logger.error('failed: %s', str(path.resolve().relative_to(pathlib.Path.cwd())))
        else:
            logger.info('all tests succeeded')

    def succeeded(self) -> bool:
        return not self.failed_test_paths


def exec_command(command: List[str]):
    # NOTE: secrets like YUKICODER_TOKEN are masked
    logger.info('$ %s', ' '.join(command))

    cwd = pathlib.Path.cwd()
    try:

        subprocess.check_call(command)

    finally:
        # subprocess 中に Ctrl-C とかで止めるとなぜか cd しちゃったままのことがあるので戻す
        if pathlib.Path.cwd() != cwd:
            os.chdir(str(cwd))


def verify_file(path: pathlib.Path, *, compilers: List[str], tle: float, jobs: int) -> Optional[bool]:
    logger.info('verify: %s', path)

    language = onlinejudge_verify.languages.list.get(path)
    if language is None:
        logger.error('unsupported language')
        return False

    # analyze attributes
    try:
        attributes = language.list_attributes(path, basedir=pathlib.Path.cwd())
    except Exception:
        traceback.print_exc()
        return False
    if 'IGNORE' in attributes:
        return None

    # recognize PROBLEM
    if 'PROBLEM' not in attributes:
        logger.error('PROBLEM is not specified')
        return False
    url = attributes['PROBLEM']
    problem = onlinejudge.dispatch.problem_from_url(url)
    logger.info('problem: %s', url)

    # download test cases
    directory = pathlib.Path('.verify-helper/cache') / hashlib.md5(url.encode()).hexdigest()
    if not (directory / 'test').exists() or list((directory / 'test').iterdir()) == []:
        directory.mkdir(parents=True, exist_ok=True)
        exec_command(['sleep', '2'])
        command = ['oj', 'download', '--system', '-d', str(directory / 'test'), '--silent', url]

        if os.environ.get('YUKICODER_TOKEN'):
            command += ['--yukicoder-token', os.environ['YUKICODER_TOKEN']]
        try:
            exec_command(command)
        except Exception:
            traceback.print_exc()
            if isinstance(problem, onlinejudge.service.yukicoder.YukicoderProblem) and not os.environ.get('YUKICODER_TOKEN'):
                logger.warning('the $YUKICODER_TOKEN environment variable is not set')
            return False

    for environment in language.list_environments(path, basedir=pathlib.Path.cwd()):
        # compile the ./a.out
        try:
            environment.compile(path, basedir=pathlib.Path.cwd(), tempdir=directory)
            execute = ' '.join(environment.get_execute_command(path, basedir=pathlib.Path.cwd(), tempdir=directory))  # TODO: use shlex.join added in Python 3.8
        except Exception:
            traceback.print_exc()
            return False

        # run test using oj
        command = ['oj', 'test', '-c', execute, '-d', str(directory / 'test'), '--print-input', '--tle', str(tle)]
        if isinstance(problem, onlinejudge.service.library_checker.LibraryCheckerProblem):
            command += ['--judge-command', str(problem.download_checker_binary())]
        if 'ERROR' in attributes:
            command += ['-e', attributes['ERROR']]
        if jobs != 1:
            command += ['-j', str(jobs)]
        try:
            exec_command(command)
        except Exception:
            traceback.print_exc()
            return False

    return True


def main(paths: List[pathlib.Path], *, marker: onlinejudge_verify.marker.VerificationMarker, timeout: float = math.inf, tle: float = 60, jobs: int = 1) -> VerificationSummary:
    try:
        import resource  # pylint: disable=import-outside-toplevel
        _, hard = resource.getrlimit(resource.RLIMIT_STACK)
        resource.setrlimit(resource.RLIMIT_STACK, (hard, hard))
    except Exception:
        logger.warning('failed to increase the stack size')
        print('::warning ::failed to ulimit')

    compilers = []
    if 'CXX' in os.environ:
        compilers.append(os.environ['CXX'])
    else:
        compilers.append('g++')
        compilers.append('clang++')

    failed_test_paths: List[pathlib.Path] = []

    start = time.time()
    for path in paths:
        if marker.is_verified(path):
            continue

        verified = verify_file(path, compilers=compilers, tle=tle, jobs=jobs)

        if verified is None:
            logger.info('ignored')
        elif verified:
            marker.mark_verified(path)
        else:
            marker.mark_failed(path)
            failed_test_paths.append(path)
            # Set an error message for GitHub Action. https://help.github.com/en/actions/reference/development-tools-for-github-actions
            print(f'::error file={str(path.resolve(strict=True).relative_to(pathlib.Path.cwd().resolve(strict=True)))}::failed to verify')

        # to prevent taking too long; we may fail to use the results of verification due to expired tokens
        if timeout is not None and time.time() - start > timeout:
            break

    return VerificationSummary(failed_test_paths=failed_test_paths)
