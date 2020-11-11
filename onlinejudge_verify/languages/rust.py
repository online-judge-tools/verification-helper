import functools
import itertools
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
        metadata = _cargo_metadata(cwd=path.parent, no_deps=True)
        package_and_target = _find_target(metadata, path)
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
        metadata = _cargo_metadata(cwd=path.parent, no_deps=True)
        package_and_target = _find_target(metadata, path)
        if not package_and_target:
            raise Exception(f'{path} is not a main source file of any target')
        _, target = package_and_target
        if target['kind'] != ['bin']:
            raise RuntimeError(f'`{target["name"]}` is not a `bin` target')
        return [str(pathlib.Path(metadata['target_directory'], 'release', target['name']))]


class RustLanguage(Language):
    def __init__(self, *, config: Optional[Dict[str, Any]] = None):
        pass

    def list_dependencies(self, path: pathlib.Path, *, basedir: pathlib.Path) -> List[pathlib.Path]:
        for parent in path.parents:
            if parent.parent.joinpath('Cargo.toml').exists() and \
                    parent.parts[-1] == 'target':
                logger.warning(f'This is a generated file!: {path}')
                return []

        metadata = _cargo_metadata(cwd=path.parent)
        package_and_target = _find_target(metadata, path)

        if not package_and_target:
            return [other for other in path.parent.rglob('*.rs') if other != path]
        package, target = package_and_target

        packages_by_id = {package['id']: package for package in metadata['packages']}
        normal_build_node_deps = {normal_build_node_dep['name']: normal_build_node_dep for node in metadata['resolve']['nodes'] if node['id'] == package['id'] for normal_build_node_dep in node['deps'] if not packages_by_id[normal_build_node_dep['pkg']]['source'] and any(not dep_kind['kind'] or dep_kind['kind'] == 'build' for dep_kind in normal_build_node_dep['dep_kinds'])}

        if target['kind'] == ['bin']:
            renames = {dependency['rename'] for dependency in package['dependencies'] if dependency['rename']}
            unused_packages = {package_id
                               for unused_dep in json.loads(subprocess.run(
                                   ['rustup', 'run', 'nightly', 'cargo', 'udeps', '--output', 'json', '--manifest-path', package['manifest_path'], '--bin', target['name']],
                                   check=False,
                                   stdout=PIPE,
                               ).stdout.decode())['unused_deps'].values() if unused_dep['manifest_path'] == package['manifest_path'] for name_in_toml in itertools.chain(unused_dep['normal'], unused_dep['build']) for package_id in ([normal_build_node_deps[name_in_toml]] if name_in_toml in renames else [normal_build_node_dep['pkg'] for normal_build_node_dep in normal_build_node_deps.values() if packages_by_id[normal_build_node_dep['pkg']]['name'] == name_in_toml][:1])}
        else:
            unused_packages = set()

        return sorted(pathlib.Path(target['src_path']) for normal_build_node_dep in normal_build_node_deps.values() if normal_build_node_dep['pkg'] not in unused_packages for target in packages_by_id[normal_build_node_dep['pkg']]['targets'] if target['kind'] == ['lib'] and pathlib.Path(target['src_path']) != path)

    def bundle(self, path: pathlib.Path, *, basedir: pathlib.Path, options: Dict[str, Any]) -> bytes:
        raise NotImplementedError

    def is_verification_file(self, path: pathlib.Path, *, basedir: pathlib.Path) -> bool:
        parts = path.parts
        return len(parts) >= 3 and parts[-3] == 'src' and parts[-2] == 'bin' and pathlib.Path(parts[-1]).suffix == '.rs'

    def list_environments(self, path: pathlib.Path, *, basedir: pathlib.Path) -> Sequence[RustLanguageEnvironment]:
        return [RustLanguageEnvironment()]


def _cargo_metadata(cwd: pathlib.Path, no_deps: bool = False) -> Dict[str, Any]:
    def find_root_manifest_for_wd() -> pathlib.Path:
        # https://docs.rs/cargo/0.48.0/cargo/util/important_paths/fn.find_root_manifest_for_wd.html
        for directory in [cwd, *cwd.parents]:
            manifest_path = directory.joinpath('Cargo.toml')
            if manifest_path.exists():
                return manifest_path
        raise RuntimeError(f'Could not find `Cargo.toml` in `{cwd}` or any parent directory')

    @functools.lru_cache(maxsize=None)
    def cargo_metadata(manifest_path: pathlib.Path, no_deps: bool) -> Dict[str, Any]:
        args = ['cargo', 'metadata', '--format-version', '1', '--manifest-path', str(manifest_path)]
        if no_deps:
            args.append('--no-deps')
        return json.loads(subprocess.run(
            args,
            stdout=PIPE,
            cwd=manifest_path.parent,
            check=True,
        ).stdout.decode())

    return cargo_metadata(find_root_manifest_for_wd(), no_deps)


def _find_target(
    metadata: Dict[str, Any],
    src_path: pathlib.Path,
) -> Optional[Tuple[Dict[str, Any], Dict[str, Any]]]:
    for package in metadata['packages']:
        for target in package['targets']:
            if pathlib.Path(target['src_path']) == src_path:
                return package, target
    return None
