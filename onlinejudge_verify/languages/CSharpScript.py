
# Python Version: 3.x
import pathlib
from typing import *

from onlinejudge_verify.languages.base import Language


class CSharpScriptLanguage(Language):
    def compile(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> None:
        raise NotImplementedError

    def get_execute_command(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> List[str]:
        raise NotImplementedError

    def list_attributes(self, path: pathlib.Path, *, basedir: pathlib.Path) -> Dict[str, str]:
        raise NotImplementedError

    def list_dependencies(self, path: pathlib.Path, *, basedir: pathlib.Path) -> List[pathlib.Path]:
        raise NotImplementedError

    def bundle(self, path: pathlib.Path, *, basedir: pathlib.Path) -> bytes:
        raise NotImplementedError
