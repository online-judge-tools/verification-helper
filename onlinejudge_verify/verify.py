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
            exec_command(['oj', 'download', '--system', '-d', shlex.quote(str(directory / 'test')), url])

        # Library Checker の場合は checker.out を compile する
        if isinstance(problem, onlinejudge.service.library_checker.LibraryCheckerProblem):
            # TODO: Library Checker の generate.py に compile してもらってその結果を使うようにする
            checker_out_path = directory / 'checker.out'
            checker_cpp_path = directory / 'checker.cpp'

            # 再 compile が必要か確認
            is_checker_modified = False
            checker = onlinejudge.dispatch.problem_from_url(url).download_checker_cpp()
            if not checker_out_path.exists():
                is_checker_modified = True
            else:
                with open(checker_cpp_path, "rb") as fh:
                    if fh.read() != checker:
                        is_checker_modified = True

            if is_checker_modified:
                # compile する
                with open(checker_cpp_path, "wb") as f:
                    f.write(checker)
                include_directory = pathlib.Path('.verify-helper/include')
                include_directory.mkdir(parents=True, exist_ok=True)
                if not (include_directory / 'testlib.h').exists():
                    with open(include_directory / 'testlib.h', 'wb') as f:
                        subprocess.call(['curl', 'https://raw.githubusercontent.com/MikeMirzayanov/testlib/master/testlib.h'], stdout=f)
                CXX = os.environ.get('CXX', 'g++')
                CXXFLAGS = os.environ.get('CXXFLAGS', '--std=c++17 -O2 -Wall -g')
                exec_command([CXX, *shlex.split(CXXFLAGS), '-I', '.', '-I', str(include_directory), '-o', str(checker_out_path), str(checker_cpp_path)])

        # compile the ./a.out
        language.compile(path, basedir=pathlib.Path.cwd(), tempdir=directory)
        execute = ' '.join(language.get_execute_command(path, basedir=pathlib.Path.cwd(), tempdir=directory))  # TODO: use shlex.join added in Python 3.8

        # run test using oj
        command = ['oj', 'test', '-c', execute, '-d', shlex.quote(str(directory / 'test')), '--tle', '60']
        if isinstance(problem, onlinejudge.service.library_checker.LibraryCheckerProblem):
            command += ['--judge-command', shlex.quote(str(directory / 'checker.out'))]
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
