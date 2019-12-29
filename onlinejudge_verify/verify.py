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

import onlinejudge_verify.utils as utils

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


def main(paths: List[pathlib.Path], *, marker: utils.VerificationMarker, timeout: float = math.inf, jobs: int = 1) -> None:
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

    failed_test_paths = []  # type: List[pathlib.Path]

    start = time.time()
    for path in paths:
        if marker.is_verified(path):
            continue

        logger.info('verify %s', path)
        verified = True
        for cxx in compilers:
            macros = utils.list_defined_macros(path, compiler=cxx)

            if 'IGNORE' in macros:
                continue

            assert ('PROBLEM' in macros)
            url = shlex.split(macros['PROBLEM'])[0]
            directory = pathlib.Path('.verify-helper/cache') / hashlib.md5(url.encode()).hexdigest()

            if not directory.exists():
                directory.mkdir(parents=True)
                exec_command(['sleep', '2'])
                exec_command(['oj', 'download', '--system', '-d', shlex.quote(str(directory / 'test')), url])

            # Library Checker の場合は checker.out を compile する
            if 'judge.yosupo.jp' in url:
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
                    exec_command([utils.CXX, *shlex.split(utils.CXXFLAGS), '-I', '.', '-I', str(include_directory), '-o', str(checker_out_path), str(checker_cpp_path)])

            # compile the ./a.out
            exec_command([cxx, *shlex.split(utils.CXXFLAGS), '-I', '.', '-o', shlex.quote(str(directory / 'a.out')), shlex.quote(str(path))])

            # run test using oj
            command = ['oj', 'test', '-c', shlex.quote(str(directory / 'a.out')), '-d', shlex.quote(str(directory / 'test')), '--tle', '60']
            if 'judge.yosupo.jp' in url:
                command += ['--judge-command', shlex.quote(str(directory / 'checker.out'))]
            if 'ERROR' in macros:
                command += ['-e', shlex.split(macros['ERROR'])[0]]
            if jobs != 1:
                command += ['-j', str(jobs)]
            try:
                exec_command(command)
            except:
                marker.mark_failed(path)
                verified = False
                failed_test_paths.append(path)
                # failするテストが複数ある場合に後続のテストを継続させるため、raiseして処理を終わらせるのではなくbreakする
                break

        if verified:
            marker.mark_verified(path)

        # to prevent taking too long; we may fail to use the results of verification due to expired tokens
        if timeout is not None and time.time() - start > timeout:
            break

    # failするテストがあったらraiseする
    if len(failed_test_paths) > 0:
        logger.error('%d test failed', len(failed_test_paths))
        for path in failed_test_paths:
            logger.error('failed: %s', str(path))
        raise Exception('{} test failed'.format(len(failed_test_paths)))
