# Python Version: 3.x
import functools
import os
import pathlib
import shlex
import subprocess
from logging import getLogger
from typing import *

from onlinejudge_verify.languages.base import Language
from onlinejudge_verify.languages.cplusplus_bundle import Bundler

logger = getLogger(__name__)


@functools.lru_cache(maxsize=None)
def _cplusplus_list_depending_files(path: pathlib.Path, *, compiler: str) -> List[pathlib.Path]:
    code = r"""{} -MD -MF /dev/stdout -MM {} | sed '1s/[^:].*: // ; s/\\$//' | xargs -n 1""".format(compiler, shlex.quote(str(path)))
    data = subprocess.check_output(code, shell=True)
    return list(map(pathlib.Path, data.decode().splitlines()))


@functools.lru_cache(maxsize=None)
def _cplusplus_list_defined_macros(path: pathlib.Path, *, compiler: str) -> Dict[str, str]:
    command = [*shlex.split(compiler), '-dM', '-E', str(path)]
    data = subprocess.check_output(command)
    define = {}
    for line in data.decode().splitlines():
        assert line.startswith('#define ')
        a, _, b = line[len('#define '):].partition(' ')
        if (b.startswith('"') and b.endswith('"')) or (b.startswith("'") and b.endswith("'")):
            b = b[1:-1]
        define[a] = b
    return define


class CPlusPlusLanguage(Language):
    CXX: str
    CXXFLAGS: str

    def __init__(self, *, CXX: str = os.environ.get('CXX', 'g++'), CXXFLAGS: str = os.environ.get('CXXFLAGS', '--std=c++17 -O2 -Wall -g')):
        self.CXX = CXX
        self.CXXFLAGS = CXXFLAGS

    def compile(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> None:
        command = [self.CXX, *shlex.split(self.CXXFLAGS), '-I', str(basedir), '-o', str(tempdir / 'a.out'), str(path)]
        logger.info('$ %s', ' '.join(command))
        subprocess.check_call(command)

    def get_execute_command(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> List[str]:
        return [str(tempdir / 'a.out')]

    def list_attributes(self, path: pathlib.Path, *, basedir: pathlib.Path) -> Dict[str, str]:
        compiler = ' '.join([self.CXX, self.CXXFLAGS, '-I', str(basedir)])
        return _cplusplus_list_defined_macros(path.resolve(), compiler=compiler)

    def list_dependencies(self, path: pathlib.Path, *, basedir: pathlib.Path) -> List[pathlib.Path]:
        compiler = ' '.join([self.CXX, self.CXXFLAGS, '-I', str(basedir)])
        return _cplusplus_list_depending_files(path.resolve(), compiler=compiler)

    def bundle(self, path: pathlib.Path, *, basedir: pathlib.Path) -> bytes:
        bundler = Bundler(iquotes=[basedir])
        bundler.update(path)
        return bundler.get()
