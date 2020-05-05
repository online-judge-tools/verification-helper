# Python Version: 3.x
import functools
import pathlib
import re
import subprocess
from logging import getLogger
from typing import *

from onlinejudge_verify.config import get_config
from onlinejudge_verify.languages.models import Language, LanguageEnvironment

logger = getLogger(__name__)


class NimLanguageEnvironment(LanguageEnvironment):
    compile_to: str
    NIMFLAGS: List[str]

    def __init__(self, *, compile_to: str, NIMFLAGS: List[str]):
        self.compile_to = compile_to
        self.NIMFLAGS = NIMFLAGS

    def compile(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> None:
        command = ["nim", self.compile_to, "-p:.", f"-o:{str(tempdir /'a.out')}", f"--nimcache:{str(tempdir)}"] + self.NIMFLAGS + [str(path)]
        logger.info('$ %s', ' '.join(command))
        subprocess.check_call(command)

    def get_execute_command(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> List[str]:
        return [str(tempdir / "a.out")]


@functools.lru_cache(maxsize=None)
def _list_direct_dependencies(path: pathlib.Path, *, basedir: pathlib.Path) -> List[pathlib.Path]:
    dependencies = [path.resolve()]
    with (basedir / path).open() as fh:
        for line in fh:
            m = re.match(r'''^\s*include\s*"(.*)"''', line)
            if m:
                included = pathlib.Path(m.group(1))
                if included.exists():
                    dependencies.append(included.resolve())
    return dependencies


class NimLanguage(Language):
    config: Dict[str, Any]

    def __init__(self, *, config: Optional[Dict[str, Any]] = None):
        if config is None:
            self.config = get_config().get('languages', {}).get('nim', {})
        else:
            self.config = config

    def list_dependencies(self, path: pathlib.Path, *, basedir: pathlib.Path) -> List[pathlib.Path]:
        dependencies = []
        visited: Set[pathlib.Path] = set()
        stk = [path.resolve()]
        while stk:
            path = stk.pop()
            if path in visited:
                continue
            visited.add(path)
            for child in _list_direct_dependencies(path, basedir=basedir):
                dependencies.append(child)
                stk.append(child)
        return list(set(dependencies))

    def bundle(self, path: pathlib.Path, *, basedir: pathlib.Path) -> bytes:
        raise NotImplementedError

    def is_verification_file(self, path: pathlib.Path, *, basedir: pathlib.Path) -> bool:
        return path.name.endswith("_test.nim")

    def list_environments(self, path: pathlib.Path, *, basedir: pathlib.Path) -> List[NimLanguageEnvironment]:
        default_compile_to = 'cpp'
        default_NIMFLAGS = ['-d:release', '--opt:speed']
        envs = []
        if 'environments' not in self.config:
            envs.append(NimLanguageEnvironment(compile_to=default_compile_to, NIMFLAGS=default_NIMFLAGS))
        else:
            for env in self.config['environments']:
                compile_to = env.get('compile_to', default_compile_to)
                NIMFLAGS: List[str] = env.get('NIMFLAGS', default_NIMFLAGS)
                if not isinstance(NIMFLAGS, list):
                    raise RuntimeError('NIMFLAGS must ba a list')
                envs.append(NimLanguageEnvironment(compile_to=compile_to, NIMFLAGS=NIMFLAGS))
        return envs
