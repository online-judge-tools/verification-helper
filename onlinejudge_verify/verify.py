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

    cxxflags = shlex.split(os.environ.get('CXXFLAGS', '-std=c++17 -O2 -Wall -g'))

    start = time.time()
    for path in paths:
        if marker.is_verified(path):
            continue

        verified = False
        logger.info('verify %s', path)
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

            exec_command([cxx, *cxxflags, '-I', '.', '-o', shlex.quote(str(directory / 'a.out')), shlex.quote(str(path))])

            command = ['oj', 'test', '-c', shlex.quote(str(directory / 'a.out')), '-d', shlex.quote(str(directory / 'test'))]
            if 'judge.yosupo.jp' in url:
                checker = onlinejudge.dispatch.problem_from_url(url).download_checker_cpp()
                with open(directory / "checker.cpp", "wb") as f:
                    f.write(checker)

                with open(directory / 'testlib.h', 'wb') as f:
                    subprocess.call(['curl', 'https://raw.githubusercontent.com/MikeMirzayanov/testlib/master/testlib.h'], stdout=f)

                exec_command([cxx, *cxxflags, '-I', '.', '-o', str(directory / 'checker.out'), str(directory / 'checker.cpp')])
                command += ['--judge-command', shlex.quote(str(directory / 'checker.out'))]

            if 'ERROR' in macros:
                command += ['-e', shlex.split(macros['ERROR'])[0]]
            if jobs != 1:
                command += ['-j', str(jobs)]
            exec_command(command)
            verified = True

        if verified:
            marker.mark_verified(path)

        # to prevent taking too long; we may fail to use the results of verification due to expired tokens
        if timeout is not None and time.time() - start > timeout:
            break
