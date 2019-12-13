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

import onlinejudge
import onlinejudge_verify.utils as utils

logger = getLogger(__name__)

def exec_command(command: List[str]):
    subprocess.check_call(shlex.split(' '.join(command)))

def main(paths: List[pathlib.Path], *, timeout: float = math.inf) -> None:
    try:
        resource.setrlimit(resource.RLIMIT_STACK, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))
    except OSError:
        logger.warning('failed to make the stack size unlimited')

    compilers = []
    if 'CXX' in os.environ:
        compilers.append(os.environ.get('CXX'))
    else:
        compilers.append('g++')
        compilers.append('clang++')

    cxxflags = os.environ.get('CXXFLAGS', '-std=c++17 -O2 -Wall -g')

    start = time.time()
    for path in paths:
        if utils.is_verified(path, compiler=compilers[0]):
            continue

        verified = False
        logger.info('verify %s', path)
        for cxx in compilers:
            macros = utils.list_defined_macros(path, compiler=cxx)

            if 'IGNORE' in macros:
                continue

            assert ('PROBLEM' in macros)
            url = shlex.split(macros['PROBLEM'])[0]
            directory = pathlib.Path('.verify-helper') / hashlib.md5(
                url.encode()).hexdigest()

            if not directory.exists():
                directory.mkdir()
                exec_command(['sleep', '2'])
                exec_command([
                    'oj', 'download', '--system', url, '-d',
                    str(directory / 'test')
                ])

            print("$ $CXX $CXXFLAGS -I . $file")
            exec_command([
                cxx, cxxflags, '-I', '.', '-o',
                str(directory / 'a.out'),
                str(path)
            ])

            if 'judge.yosupo.jp' in url:
                checker = onlinejudge.dispatch.problem_from_url(
                    url).download_checker_cpp()
                with open(directory / "checker.cpp", "wb") as f:
                    f.write(checker)

                with open(directory / 'testlib.h', 'w') as f:
                    subprocess.call([
                        'curl',
                        'https://raw.githubusercontent.com/MikeMirzayanov/testlib/master/testlib.h'
                    ],
                                    stdout=f)

                exec_command([
                    cxx, cxxflags, '-I', '.', '-o',
                    str(directory / 'checker.out'),
                    str(directory / 'checker.cpp')
                ])

                exec_command([
                    'oj', 'test', '--judge-command',
                    str(directory / 'checker.out'), '-c',
                    str(directory / 'a.out'), '-d',
                    str(directory / 'test')
                ])
            elif 'ERROR' in macros:
                error = shlex.split(macros['ERROR'])[0]
                exec_command([
                    'oj', 'test', '-e', error, '-c',
                    str(directory / 'a.out'), '-d',
                    str(directory / 'test')
                ])
            else:
                exec_command([
                    'oj', 'test', '-c',
                    str(directory / 'a.out'), '-d',
                    str(directory / 'test')
                ])
            verified = True

        if verified:
            utils.mark_verified(path, compilers[0])

        # to prevent taking too long; we may fail to use the results of verification due to expired tokens
        if timeout is not None and time.time() - start > timeout:
            break

    utils.save_timestamps()
