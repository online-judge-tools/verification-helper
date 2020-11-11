import pathlib
from logging import getLogger
from typing import *

from onlinejudge_verify.languages.models import Language, LanguageEnvironment

logger = getLogger(__name__)


class RustLanguageEnvironment(LanguageEnvironment):
    def __init__(self):
        raise NotImplementedError

    def compile(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> None:
        raise NotImplementedError

    def get_execute_command(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> List[str]:
        raise NotImplementedError


class RustLanguage(Language):
    def __init__(self, *, config: Optional[Dict[str, Any]] = None):
        raise NotImplementedError

    def list_dependencies(self, path: pathlib.Path, *, basedir: pathlib.Path) -> List[pathlib.Path]:
        raise NotImplementedError

    def bundle(self, path: pathlib.Path, *, basedir: pathlib.Path, options: Dict[str, Any]) -> bytes:
        raise NotImplementedError

    def is_verification_file(self, path: pathlib.Path, *, basedir: pathlib.Path) -> bool:
        raise NotImplementedError

    def list_environments(self, path: pathlib.Path, *, basedir: pathlib.Path) -> Sequence[RustLanguageEnvironment]:
        raise NotImplementedError
