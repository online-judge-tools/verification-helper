# Python Version: 3.x
import hashlib
import math
import os
import pathlib
import resource
import shlex
import subprocess
import time
from logging import getLogger
from typing import *

import onlinejudge_verify.languages
import onlinejudge_verify.marker

import onlinejudge

logger = getLogger(__name__)


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


def verify_file(path: pathlib.Path, *, compilers: List[str], jobs: int) -> bool:
    logger.info('verify: %s', path)

    language_ = onlinejudge_verify.languages.get(path)
    if language_ is None:
        logger.error('unsupported language')
        return False

    if isinstance(language_, onlinejudge_verify.languages.CPlusPlusLanguage) and 'CXX' not in os.environ:
        matrix: List[onlinejudge_verify.languages.Language] = [
            onlinejudge_verify.languages.CPlusPlusLanguage(CXX='g++'),
            onlinejudge_verify.languages.CPlusPlusLanguage(CXX='clang++'),
        ]
    else:
        matrix = [language_]
    for language in matrix:

        macros = language.list_attributes(path, basedir=pathlib.Path.cwd())
        if 'IGNORE' in macros:
            continue
        assert 'PROBLEM' in macros
        url = macros['PROBLEM']
        problem = onlinejudge.dispatch.problem_from_url(url)
        logger.info('problem: %s', url)

        directory = pathlib.Path('.verify-helper/cache') / hashlib.md5(url.encode()).hexdigest()
        if not (directory / 'test').exists():
            directory.mkdir(parents=True)
            exec_command(['sleep', '2'])
            command = ['oj', 'download', '--system', '-d', shlex.quote(str(directory / 'test')), url]

            if os.environ.get('YUKICODER_TOKEN'):
                command += ['--yukicoder-token', os.environ['YUKICODER_TOKEN']]
            try:
                exec_command(command)
            except:
                if isinstance(problem, onlinejudge.service.yukicoder.YukicoderProblem) and not os.environ.get('YUKICODER_TOKEN'):
                    logger.warning('the $YUKICODER_TOKEN environment variable is not set')
                raise

        # compile the ./a.out
        language.compile(path, basedir=pathlib.Path.cwd(), tempdir=directory)
        execute = ' '.join(language.get_execute_command(path, basedir=pathlib.Path.cwd(), tempdir=directory))  # TODO: use shlex.join added in Python 3.8

        # run test using oj
        command = ['oj', 'test', '-c', execute, '-d', shlex.quote(str(directory / 'test')), '--tle', '60']
        if isinstance(problem, onlinejudge.service.library_checker.LibraryCheckerProblem):
            command += ['--judge-command', str(problem.download_checker_binary())]
        if 'ERROR' in macros:
            command += ['-e', macros['ERROR']]
        if jobs != 1:
            command += ['-j', str(jobs)]
        try:
            exec_command(command)
        except:
            return False

    return True


def main(paths: List[pathlib.Path], *, marker: onlinejudge_verify.marker.VerificationMarker, timeout: float = math.inf, jobs: int = 1) -> None:
    try:
        resource.setrlimit(resource.RLIMIT_STACK, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))
    except:
        logger.warning('failed to make the stack size unlimited')

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

        verified = verify_file(path, compilers=compilers, jobs=jobs)

        if verified:
            marker.mark_verified(path)
        else:
            marker.mark_failed(path)
            failed_test_paths.append(path)

        # to prevent taking too long; we may fail to use the results of verification due to expired tokens
        if timeout is not None and time.time() - start > timeout:
            break

    # failするテストがあったらraiseする
    if len(failed_test_paths) > 0:
        logger.error('%d test failed', len(failed_test_paths))
        for path in failed_test_paths:
            logger.error('failed: %s', str(path))
        raise Exception('{} test failed'.format(len(failed_test_paths)))
