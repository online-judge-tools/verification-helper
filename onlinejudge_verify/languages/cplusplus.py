# Python Version: 3.x
import functools
import pathlib
import platform
import shlex
import shutil
import subprocess
from logging import getLogger
from typing import *

from onlinejudge_verify.languages.cplusplus_bundle import Bundler
from onlinejudge_verify.languages.models import Language, LanguageEnvironment
from onlinejudge_verify.languages.special_comments import list_special_comments

logger = getLogger(__name__)


class CPlusPlusLanguageEnvironment(LanguageEnvironment):
    CXX: pathlib.Path
    CXXFLAGS: List[str]

    def __init__(self, *, CXX: pathlib.Path, CXXFLAGS: Optional[List[str]] = None):
        self.CXX = CXX
        if CXXFLAGS is not None:
            self.CXXFLAGS = CXXFLAGS
        else:
            self.CXXFLAGS = ['--std=c++17', '-O2', '-Wall', '-g']
            if platform.uname().system == 'Linux' and 'Microsoft' in platform.uname().release:
                self.CXXFLAGS.append('-fsplit-stack')

    def compile(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> None:
        command = [str(self.CXX), *self.CXXFLAGS, '-I', str(basedir), '-o', str(tempdir / 'a.out'), str(path)]
        logger.info('$ %s', ' '.join(command))
        subprocess.check_call(command)

    def get_execute_command(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> List[str]:
        return [str(tempdir / 'a.out')]


@functools.lru_cache(maxsize=None)
def _cplusplus_list_depending_files(path: pathlib.Path, *, CXX: pathlib.Path, joined_CXXFLAGS: str) -> List[pathlib.Path]:
    # Using /dev/stdout is acceptable because Library Chcker doesn't work on Windows.
    command = [str(CXX), *shlex.split(joined_CXXFLAGS), '-MD', '-MF', '/dev/stdout', '-MM', str(path)]
    data = subprocess.check_output(command)
    makefile_rule = shlex.split(data.decode().replace('\\\n', ''))
    return [pathlib.Path(path).resolve() for path in makefile_rule[1:]]


@functools.lru_cache(maxsize=None)
def _cplusplus_list_defined_macros(path: pathlib.Path, *, CXX: pathlib.Path, joined_CXXFLAGS: str) -> Dict[str, str]:
    command = [str(CXX), *shlex.split(joined_CXXFLAGS), '-dM', '-E', str(path)]
    data = subprocess.check_output(command)
    define = {}
    for line in data.decode().splitlines():
        assert line.startswith('#define ')
        a, _, b = line[len('#define '):].partition(' ')
        if (b.startswith('"') and b.endswith('"')) or (b.startswith("'") and b.endswith("'")):
            b = b[1:-1]
        define[a] = b
    return define


@functools.lru_cache(maxsize=None)
def _list_default_environments() -> List[CPlusPlusLanguageEnvironment]:
    envs = []
    for name in ('g++', 'clang++'):
        path = shutil.which(name)
        if path is not None:
            envs.append(CPlusPlusLanguageEnvironment(CXX=pathlib.Path(path)))
    return envs


def _get_default_CXX() -> pathlib.Path:
    return _list_default_environments()[0].CXX


def _get_default_CXXFLAGS() -> List[str]:
    return _list_default_environments()[0].CXXFLAGS


# 以前は #ifdef __clang__ #define IGNORE #endif をしていた
def _workaround_ignore_if_clang(path: pathlib.Path, *, clang: pathlib.Path, basedir: pathlib.Path) -> bool:
    with open(path) as fh:
        if 'IGNORE' not in fh.read():
            return False
    joined_CXXFLAGS = ' '.join(map(shlex.quote, [*_get_default_CXXFLAGS(), '-I', str(basedir)]))
    return 'IGNORE' in _cplusplus_list_defined_macros(path.resolve(), CXX=clang, joined_CXXFLAGS=joined_CXXFLAGS)


class CPlusPlusLanguage(Language):
    def list_attributes(self, path: pathlib.Path, *, basedir: pathlib.Path) -> Dict[str, str]:
        joined_CXXFLAGS = ' '.join(map(shlex.quote, [*_get_default_CXXFLAGS(), '-I', str(basedir)]))
        return list_special_comments(path.resolve()) or _cplusplus_list_defined_macros(path.resolve(), CXX=_get_default_CXX(), joined_CXXFLAGS=joined_CXXFLAGS)

    def list_dependencies(self, path: pathlib.Path, *, basedir: pathlib.Path) -> List[pathlib.Path]:
        joined_CXXFLAGS = ' '.join(map(shlex.quote, [*_get_default_CXXFLAGS(), '-I', str(basedir)]))
        return _cplusplus_list_depending_files(path.resolve(), CXX=_get_default_CXX(), joined_CXXFLAGS=joined_CXXFLAGS)

    def bundle(self, path: pathlib.Path, *, basedir: pathlib.Path) -> bytes:
        bundler = Bundler(iquotes=[basedir])
        bundler.update(path)
        return bundler.get()

    def list_environments(self, path: pathlib.Path, *, basedir: pathlib.Path) -> List[CPlusPlusLanguageEnvironment]:
        envs = []
        for env in _list_default_environments():
            # TODO: 仕様検討 このあたりどうにかする
            # if 'clang++' in env.CXX.name and 'IGNORE_IF_CLANG' in self.list_attributes(path, basedir=basedir):
            #     continue
            # if 'g++' in env.CXX.name and 'IGNORE_IF_GCC' in self.list_attributes(path, basedir=basedir):
            #     continue
            if 'clang++' in env.CXX.name and _workaround_ignore_if_clang(path, clang=env.CXX, basedir=basedir):
                # logger.warning('failed to make the stack size unlimited')
                # print(f'::warning ::use IGNORE_IF_CLANG')
                continue
            envs.append(env)
        return envs
