import pathlib
import subprocess
import sys
from logging import getLogger
from typing import *

from onlinejudge_verify.config import get_config
from onlinejudge_verify.languages.models import LanguageEnvironment
from onlinejudge_verify.languages.user_defined import UserDefinedLanguage

logger = getLogger(__name__)


class JavaLanguageEnvironment(LanguageEnvironment):
    def compile(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> None:
        command = ['javac', str(basedir / path)]
        logger.info('$ %s', command)
        subprocess.check_call(command, stdout=sys.stdout, stderr=sys.stderr)

    def get_execute_command(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> List[str]:
        relative_path = (basedir / path).relative_to(basedir)
        class_path = '.'.join([*relative_path.parent.parts, relative_path.stem])
        return ['java', class_path]


# TODO: stop using UserDefinedLanguage
class JavaLanguage(UserDefinedLanguage):
    config: Dict[str, Any]

    def __init__(self, *, config: Optional[Dict[str, Any]] = None):
        if config is None:
            config = get_config().get('languages', {}).get('java', {})
        if 'compile' in config:
            raise RuntimeError('You cannot overwrite "compile" for Java language')
        if 'execute' in config:
            raise RuntimeError('You cannot overwrite "execute" for Java language')
        super().__init__(extension='java', config=config)

    def list_environments(self, path: pathlib.Path, *, basedir: pathlib.Path) -> Sequence[LanguageEnvironment]:
        return [JavaLanguageEnvironment()]

    def is_verification_file(self, path: pathlib.Path, *, basedir: pathlib.Path) -> bool:
        return path.name.endswith("_test.java")
