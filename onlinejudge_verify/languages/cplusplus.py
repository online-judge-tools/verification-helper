# Python Version: 3.x
import functools
import os
import pathlib
import platform
import shlex
import shutil
import subprocess
import sys
from logging import getLogger
from typing import *

import onlinejudge_verify.languages.special_comments as special_comments
from onlinejudge_verify.config import get_config
from onlinejudge_verify.languages.cplusplus_bundle import Bundler
from onlinejudge_verify.languages.models import Language, LanguageEnvironment

logger = getLogger(__name__)


class CPlusPlusLanguageEnvironment(LanguageEnvironment):
    CXX: pathlib.Path
    CXXFLAGS: List[str]

    def __init__(self, *, CXX: pathlib.Path, CXXFLAGS: List[str]):
        self.CXX = CXX
        self.CXXFLAGS = CXXFLAGS

    def compile(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> None:
        command = [str(self.CXX), *self.CXXFLAGS, '-I', str(basedir), '-o', str(tempdir / 'a.out'), str(path)]
        logger.info('$ %s', ' '.join(command))
        subprocess.check_call(command)

    def get_execute_command(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> List[str]:
        return [str(tempdir / 'a.out')]

    def _is_clang(self) -> bool:
        return 'clang++' in self.CXX.name

    def _is_gcc(self) -> bool:
        return not self._is_clang() and 'g++' in self.CXX.name


@functools.lru_cache(maxsize=None)
def _cplusplus_list_depending_files(path: pathlib.Path, *, CXX: pathlib.Path, joined_CXXFLAGS: str) -> List[pathlib.Path]:
    is_windows = (platform.uname().system == 'Windows')
    command = [str(CXX), *shlex.split(joined_CXXFLAGS), '-MM', str(path)]
    try:
        data = subprocess.check_output(command)
    except subprocess.CalledProcessError:
        logger.error("failed to analyze dependencies with %s: %s  (hint: Please check #include directives of the file and its dependencies. The paths must exist, must not contain '\\', and must be case-sensitive.)", CXX, str(path))
        print(f'::warning file={str(path)}::failed to analyze dependencies', file=sys.stderr)
        raise
    logger.debug('dependencies of %s: %s', str(path), repr(data))
    makefile_rule = shlex.split(data.decode().strip().replace('\\\n', '').replace('\\\r\n', ''), posix=not is_windows)
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


_NOT_SPECIAL_COMMENTS = '*NOT_SPECIAL_COMMENTS*'
_PROBLEM = 'PROBLEM'
_IGNORE = 'IGNORE'
_IGNORE_IF_CLANG = 'IGNORE_IF_CLANG'
_IGNORE_IF_GCC = 'IGNORE_IF_GCC'
_ERROR = 'ERROR'


# config.toml example:
#     [[languages.cpp.environments]]
#     CXX = "g++"
#     CXXFALGS = ["-std=c++17", "-Wall"]
class CPlusPlusLanguage(Language):
    config: Dict[str, Any]

    def __init__(self, *, config: Optional[Dict[str, Any]] = None):
        if config is None:
            self.config = get_config().get('languages', {}).get('cpp', {})
        else:
            self.config = config

    def _list_environments(self) -> List[CPlusPlusLanguageEnvironment]:
        default_CXXFLAGS = ['--std=c++17', '-O2', '-Wall', '-g']
        if platform.system() == 'Windows' or 'CYGWIN' in platform.system():
            default_CXXFLAGS.append('-Wl,-stack,0x10000000')
        if platform.system() == 'Darwin':
            default_CXXFLAGS.append('-Wl,-stack_size,0x10000000')
        if platform.uname().system == 'Linux' and 'Microsoft' in platform.uname().release:
            default_CXXFLAGS.append('-fsplit-stack')

        if 'CXXFLAGS' in os.environ and 'environments' not in self.config:
            logger.warning('Usage of $CXXFLAGS envvar to specify options is deprecated and will be removed soon')
            print('::warning::Usage of $CXXFLAGS envvar to specify options is deprecated and will be removed soon')
            default_CXXFLAGS = shlex.split(os.environ['CXXFLAGS'])

        envs = []
        if 'environments' in self.config:
            # configured: use specified CXX & CXXFLAGS
            for env in self.config['environments']:
                CXX: str = env.get('CXX')
                if CXX is None:
                    raise RuntimeError('CXX is not specified')
                CXXFLAGS: List[str] = env.get('CXXFLAGS', default_CXXFLAGS)
                if not isinstance(CXXFLAGS, list):
                    raise RuntimeError('CXXFLAGS must ba a list')
                envs.append(CPlusPlusLanguageEnvironment(CXX=pathlib.Path(CXX), CXXFLAGS=CXXFLAGS))

        elif 'CXX' in os.environ:
            # old-style: 以前は $CXX を使ってたけど設定ファイルに移行したい
            logger.warning('Usage of $CXX envvar to restrict compilers is deprecated and will be removed soon')
            print('::warning::Usage of $CXX envvar to restrict compilers is deprecated and will be removed soon')
            envs.append(CPlusPlusLanguageEnvironment(CXX=pathlib.Path(os.environ['CXX']), CXXFLAGS=default_CXXFLAGS))

        else:
            # default: use found compilers
            for name in ('g++', 'clang++'):
                path = shutil.which(name)
                if path is not None:
                    envs.append(CPlusPlusLanguageEnvironment(CXX=pathlib.Path(path), CXXFLAGS=default_CXXFLAGS))

        if not envs:
            raise RuntimeError('No C++ compilers found')
        return envs

    def list_attributes(self, path: pathlib.Path, *, basedir: pathlib.Path) -> Dict[str, Any]:
        attributes: Dict[str, Any] = {}
        attributes.update(special_comments.list_doxygen_annotations(path.resolve()))

        comments = special_comments.list_special_comments(path.resolve())
        if comments:
            attributes.update(comments)

        elif super().is_verification_file(path, basedir=basedir):
            # use old-style if special comments not found
            # #define PROBLEM "https://..." の形式は複数 environments との相性がよくない。あと遅い
            attributes[_NOT_SPECIAL_COMMENTS] = ''
            all_ignored = True
            for env in self._list_environments():
                joined_CXXFLAGS = ' '.join(map(shlex.quote, [*env.CXXFLAGS, '-I', str(basedir)]))
                macros = _cplusplus_list_defined_macros(path.resolve(), CXX=env.CXX, joined_CXXFLAGS=joined_CXXFLAGS)

                # convert macros to attributes
                if _IGNORE not in macros:
                    for key in [_PROBLEM, _ERROR]:
                        if all_ignored:
                            # the first non-ignored environment
                            if key in macros:
                                attributes[key] = macros[key]
                        else:
                            assert attributes.get(key) == macros.get(key)
                    all_ignored = False
                else:
                    if env._is_gcc():
                        attributes[_IGNORE_IF_GCC] = ''
                    elif env._is_clang():
                        attributes[_IGNORE_IF_CLANG] = ''
                    else:
                        attributes[_IGNORE] = ''
            if all_ignored:
                attributes[_IGNORE] = ''

        attributes.setdefault('links', [])
        attributes['links'].extend(special_comments.list_embedded_urls(path))
        return attributes

    def list_dependencies(self, path: pathlib.Path, *, basedir: pathlib.Path) -> List[pathlib.Path]:
        env = self._list_environments()[0]
        joined_CXXFLAGS = ' '.join(map(shlex.quote, [*env.CXXFLAGS, '-I', str(basedir)]))
        return _cplusplus_list_depending_files(path.resolve(), CXX=env.CXX, joined_CXXFLAGS=joined_CXXFLAGS)

    def bundle(self, path: pathlib.Path, *, basedir: pathlib.Path = pathlib.Path.cwd(), options: Dict[str, Any]) -> bytes:
        include_paths: List[pathlib.Path] = options['include_paths']
        assert isinstance(include_paths, list)
        bundler = Bundler(iquotes=include_paths)
        bundler.update(path)
        return bundler.get()

    def list_environments(self, path: pathlib.Path, *, basedir: pathlib.Path) -> List[CPlusPlusLanguageEnvironment]:
        attributes = self.list_attributes(path, basedir=basedir)
        envs = []
        for env in self._list_environments():
            if env._is_gcc() and _IGNORE_IF_GCC in attributes:
                continue
            if env._is_clang() and _IGNORE_IF_CLANG in attributes:
                continue
            envs.append(env)
        return envs
