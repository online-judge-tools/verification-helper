# Python Version: 3.x
import pathlib
import shlex
import subprocess
from logging import getLogger
from typing import *

from onlinejudge_verify.config import get_config
from onlinejudge_verify.languages.models import Language, LanguageEnvironment
from onlinejudge_verify.languages.special_comments import list_special_comments

logger = getLogger(__name__)


class NimLanguageEnvironment(LanguageEnvironment):
    NIMFLAGS: List[str]
    CompileTo: str

    def __init__(self, *, NIMFLAGS, CompileTo):
        self.NIMFLAGS = NIMFLAGS
        self.CompileTo = CompileTo

    def compile(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> None:
        command = compile = ["nim", self.CompileTo, "-p:.", "-d:release", "-o:{tempdir}/a.out".format(tempdir=str(tempdir)), ' '.join(self.NIMFLAGS), "{path}".format(path=str(path))]
        command = ' '.join(command)
        logger.info('$ %s', command)
        subprocess.check_call(shlex.split(command))

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


    def list_attributes(self, path: pathlib.Path, *, basedir: pathlib.Path) -> Dict[str, str]:
        command = "sed 's/^# verify-helper: // ; t ; d' {path}".format(path=str(path), basedir=str(basedir))
        text = subprocess.check_output(shlex.split(command))
        attributes = {}
        for line in text.splitlines():
            key, _, value = line.decode().partition(' ')
            attributes[key] = value
        return attributes

    def list_dependencies(self, path: pathlib.Path, *, basedir: pathlib.Path) -> List[pathlib.Path]:
        command = "sed 's/^include \"\\(.*\\)\"$/\\1/ ; t ; d' {path}".format(path=str(path), basedir=str(basedir))
        text = subprocess.check_output(shlex.split(command))
        dependencies = [path]
        for line in text.splitlines():
            dependencies.append(pathlib.Path(line.decode()))
        return dependencies

    def bundle(self, path: pathlib.Path, *, basedir: pathlib.Path) -> bytes:
        raise NotImplementedError 

    def is_verification_file(self, path: pathlib.Path, *, basedir: pathlib.Path) -> bool:
        suffix = "_test.nim"
        if suffix is not None:
            return path.name.endswith(suffix)
        return super().is_verification_file(path, basedir=basedir)

    def list_environments(self, path: pathlib.Path, *, basedir: pathlib.Path) -> Sequence[NimLanguageEnvironment]:
        CompileTo = "cpp"
        if "CompileTo" in self.config:
            CompileTo = self.config["CompileTo"]
        NIMFLAGS = ""
        if "NIMFLAGS" in self.config:
            NIMFLAGS = self.config["NIMFLAGS"].split()
        return [NimLanguageEnvironment(NIMFLAGS=NIMFLAGS, CompileTo=CompileTo)]
#        return [NimLanguageEnvironment(NIMFLAGS=[])]
