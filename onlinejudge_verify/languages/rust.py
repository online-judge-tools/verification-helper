import json
import pathlib
import subprocess
from logging import getLogger
from subprocess import PIPE
from typing import *

from onlinejudge_verify.languages.models import Language, LanguageEnvironment

logger = getLogger(__name__)


class RustLanguageEnvironment(LanguageEnvironment):
    def __init__(self):
        pass

    def compile(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> None:
        metadata = cargo_metadata(cwd=path.parent, no_deps=True)
        package_and_target = find_target(metadata, path)
        if not package_and_target:
            raise Exception(f'{path} is not a main source file of any target')
        _, target = package_and_target
        if target['kind'] != ['bin']:
            raise RuntimeError(f'`{target["name"]}` is not a `bin` target')
        subprocess.run(
            ['cargo', 'build', '--release', '--bin', target['name']],
            cwd=path.parent,
            check=True,
        )

    def get_execute_command(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> List[str]:
        raise NotImplementedError


class RustLanguage(Language):
    def __init__(self, *, config: Optional[Dict[str, Any]] = None):
        pass

    def list_dependencies(self, path: pathlib.Path, *, basedir: pathlib.Path) -> List[pathlib.Path]:
        raise NotImplementedError

    def bundle(self, path: pathlib.Path, *, basedir: pathlib.Path, options: Dict[str, Any]) -> bytes:
        raise NotImplementedError

    def is_verification_file(self, path: pathlib.Path, *, basedir: pathlib.Path) -> bool:
        raise NotImplementedError

    def list_environments(self, path: pathlib.Path, *, basedir: pathlib.Path) -> Sequence[RustLanguageEnvironment]:
        return [RustLanguageEnvironment()]


def cargo_metadata(cwd: pathlib.Path, no_deps: bool = False) -> Dict[str, Any]:
    args = ['cargo', 'metadata', '--format-version', '1']
    if no_deps:
        args.append('--no-deps')
    return json.loads(subprocess.run(
        args,
        stdout=PIPE,
        cwd=cwd,
        check=True,
    ).stdout.decode())


def find_target(
    metadata: Dict[str, Any],
    src_path: pathlib.Path,
) -> Optional[Tuple[Dict[str, Any], Dict[str, Any]]]:
    for package in metadata['packages']:
        for target in package['targets']:
            if pathlib.Path(target['src_path']) == src_path:
                return package, target
    return None
