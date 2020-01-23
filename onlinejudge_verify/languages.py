# Python Version: 3.x
import abc
import functools
import os
import pathlib
import shlex
import subprocess
from logging import getLogger
from typing import *

import onlinejudge_verify.bundle as bundle
import toml

logger = getLogger(__name__)


class Language(object):
    @abc.abstractmethod
    def compile(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_execute_command(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> List[str]:
        raise NotImplementedError

    @abc.abstractmethod
    def list_attributes(self, path: pathlib.Path, *, basedir: pathlib.Path) -> Dict[str, str]:
        raise NotImplementedError

    @abc.abstractmethod
    def list_dependencies(self, path: pathlib.Path, *, basedir: pathlib.Path) -> List[pathlib.Path]:
        raise NotImplementedError

    @abc.abstractmethod
    def bundle(self, path: pathlib.Path, *, basedir: pathlib.Path) -> bytes:
        raise NotImplementedError


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
        bundler = bundle.Bundler(iquotes=[basedir])
        bundler.update(path)
        return bundler.get()


class OtherLanguage(Language):
    config: Dict[str, str]

    def __init__(self, *, config: Dict[str, str]):
        self.config = config

    def compile(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> None:
        command = self.config['compile'].format(path=str(path), basedir=str(basedir), tempdir=str(tempdir))
        logger.info('$ %s', command)
        subprocess.check_call(shlex.split(command))

    def get_execute_command(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> List[str]:
        command = self.config['execute'].format(path=str(path), basedir=str(basedir), tempdir=str(tempdir))
        return shlex.split(command)

    def list_attributes(self, path: pathlib.Path, *, basedir: pathlib.Path) -> Dict[str, str]:
        command = self.config['list_attributes'].format(path=str(path), basedir=str(basedir))
        text = subprocess.check_output(shlex.split(command))
        attributes = {}
        for line in text.splitlines():
            key, _, value = line.decode().partition(' ')
            attributes[key] = value
        return attributes

    def list_dependencies(self, path: pathlib.Path, *, basedir: pathlib.Path) -> List[pathlib.Path]:
        command = self.config['list_dependencies'].format(path=str(path), basedir=str(basedir))
        text = subprocess.check_output(shlex.split(command))
        dependencies = [path]
        for line in text.splitlines():
            dependencies.append(pathlib.Path(line.decode()))
        return dependencies

    def bundle(self, path: pathlib.Path, *, basedir: pathlib.Path) -> bytes:
        command = self.config['bundle'].format(path=str(path), basedir=str(basedir))
        logger.info('$ %s', command)
        return subprocess.check_output(shlex.split(command))


_dict: Dict[str, Language] = {}

_dict['.cpp'] = CPlusPlusLanguage()
_dict['.hpp'] = _dict['.cpp']

config_path = pathlib.Path('.verify-helper/config.toml')
if config_path.exists():
    for ext, config in toml.load(str(config_path)).get('languages', {}).items():
        _dict['.' + ext] = OtherLanguage(config=config)


def get(path: pathlib.Path) -> Optional[Language]:
    return _dict.get(path.suffix)
