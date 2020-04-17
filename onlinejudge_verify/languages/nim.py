# Python Version: 3.x
import pathlib
import re
import shlex
import subprocess
from logging import getLogger
from typing import *

from onlinejudge_verify.config import get_config
from onlinejudge_verify.languages.models import Language, LanguageEnvironment

logger = getLogger(__name__)


class NimLanguageEnvironment(LanguageEnvironment):
    NIMFLAGS: List[str]
    compile_to: str

    def __init__(self, *, NIMFLAGS, compile_to):
        self.NIMFLAGS = NIMFLAGS
        self.compile_to = compile_to

    def compile(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> None:
        command = ["nim", self.compile_to, "-p:.", "-o:{tempdir}/a.out".format(tempdir=str(tempdir))] + self.NIMFLAGS + ["{path}".format(path=str(path))]
        logger.info('$ %s', ' '.join(command))
        subprocess.check_call(command)

    def get_execute_command(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> List[str]:
        command = execute = "{tempdir}/a.out".format(path=str(path), basedir=str(basedir), tempdir=str(tempdir))
        return shlex.split(command)


class NimLanguage(Language):
    config: Dict[str, Any]

    def __init__(self, *, config: Optional[Dict[str, Any]] = None):
        if config is None:
            self.config = get_config().get('languages', {}).get('nim', {})
        else:
            self.config = config

    def list_dependencies(self, path: pathlib.Path, *, basedir: pathlib.Path) -> List[pathlib.Path]:
        texts = []
        p = pathlib.Path("{basedir}/{path}".format(path=str(path), basedir=str(basedir)))
        with p.open(mode='r') as f:
            pattern = re.compile(r"include\s*\"(.*)\"")
            for line in f:
                line = line.strip()
                if line.startswith('include'):
                    texts += re.findall(pattern, line)
        dependencies = [path]
        for line in texts:
            dependencies.append(pathlib.Path(line))
        return dependencies

    def bundle(self, path: pathlib.Path, *, basedir: pathlib.Path) -> bytes:
        raise NotImplementedError

    def is_verification_file(self, path: pathlib.Path, *, basedir: pathlib.Path) -> bool:
        return path.name.endswith("_test.nim")

    def list_environments(self, path: pathlib.Path, *, basedir: pathlib.Path) -> List[NimLanguageEnvironment]:
        default_NIMFLAGS = ['--warning:on --opt:none']
        envs = []
        if 'environments' in self.config:
            for env in self.config['environments']:
                compile_to = "cpp"
                if 'compile_to' in env:
                    compile_to = env.get('compile_to')
                if compile_to is None:
                    raise RuntimeError('compile_to is not specified')
                NIMFLAGS: List[str] = env.get('NIMFLAGS', default_NIMFLAGS)
                if not isinstance(NIMFLAGS, list):
                    raise RuntimeError('NIMFLAGS must ba a list')
                envs.append(NimLanguageEnvironment(compile_to=compile_to, NIMFLAGS=NIMFLAGS))
        return envs
