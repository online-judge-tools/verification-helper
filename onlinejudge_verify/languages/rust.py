import functools
import json
import pathlib
import shutil
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
        path = basedir.joinpath(path)
        metadata = _cargo_metadata(cwd=path.parent, no_deps=True)
        target = _find_bin_target(metadata, path)
        subprocess.run(
            ['cargo', 'build', '--release', '--bin', target['name']],
            cwd=path.parent,
            check=True,
        )

    def get_execute_command(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> List[str]:
        path = basedir.joinpath(path)
        metadata = _cargo_metadata(cwd=path.parent, no_deps=True)
        target = _find_bin_target(metadata, path)
        return [str(pathlib.Path(metadata['target_directory'], 'release', target['name']))]


class RustLanguage(Language):
    def __init__(self, *, config: Optional[Dict[str, Any]] = None):
        pass

    def list_dependencies(self, path: pathlib.Path, *, basedir: pathlib.Path) -> List[pathlib.Path]:
        path = basedir.joinpath(path)

        for parent in path.parents:
            if parent.parent.joinpath('Cargo.toml').exists() and parent.parts[-1] == 'target':
                logger.warning(f'This is a generated file!: {path}')
                return [path]

        metadata = _cargo_metadata(cwd=path.parent)
        package_and_target = _find_target(metadata, path)

        if not package_and_target:
            return list(path.parent.rglob('*.rs'))
        package, target = package_and_target

        packages_by_id = {package['id']: package for package in metadata['packages']}
        normal_build_node_deps = {normal_build_node_dep['name']: normal_build_node_dep for node in metadata['resolve']['nodes'] if node['id'] == package['id'] for normal_build_node_dep in node['deps'] if not packages_by_id[normal_build_node_dep['pkg']]['source'] and any(not dep_kind['kind'] or dep_kind['kind'] == 'build' for dep_kind in normal_build_node_dep['dep_kinds'])}

        unused_packages = set()
        if target['kind'] == ['bin']:
            renames = {dependency['rename'] for dependency in package['dependencies'] if dependency['rename']}
            if not shutil.which('cargo-udeps'):
                raise RuntimeError('`cargo-udeps` not in $PATH')
            unused_deps = json.loads(subprocess.run(
                ['rustup', 'run', 'nightly', 'cargo', 'udeps', '--output', 'json', '--manifest-path', package['manifest_path'], '--bin', target['name']],
                check=False,
                stdout=PIPE,
            ).stdout.decode())['unused_deps'].values()
            for unused_dep in unused_deps:
                if unused_dep['manifest_path'] == package['manifest_path']:
                    for name_in_toml in [*unused_dep['normal'], *unused_dep['build']]:
                        if name_in_toml in renames:
                            unused_packages.add(normal_build_node_deps[name_in_toml])
                        else:
                            for normal_build_node_dep in normal_build_node_deps.values():
                                package_id = normal_build_node_dep['pkg']
                                if packages_by_id[package_id]['name'] == name_in_toml:
                                    unused_packages.add(package_id)

        ret = [path]
        for normal_build_node_dep in normal_build_node_deps.values():
            package_id = normal_build_node_dep['pkg']
            if package_id not in unused_packages:
                for target in packages_by_id[package_id]['targets']:
                    if target['kind'] == ['lib']:
                        ret.append(pathlib.Path(target['src_path']))
        return sorted(ret)

    def bundle(self, path: pathlib.Path, *, basedir: pathlib.Path, options: Dict[str, Any]) -> bytes:
        raise NotImplementedError

    def is_verification_file(self, path: pathlib.Path, *, basedir: pathlib.Path) -> bool:
        path = basedir.joinpath(path)
        metadata = _cargo_metadata(cwd=path.parent)
        package_and_target = _find_target(metadata, path)
        if not package_and_target:
            return False
        _, target = package_and_target
        return target['kind'] == ['bin']

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


def _find_bin_target(metadata: Dict[str, Any], src_path: pathlib.Path) -> Dict[str, Any]:
    package_and_target = _find_target(metadata, src_path)
    if not package_and_target:
        raise RuntimeError(f'{src_path} is not a main source file of any target')
    _, target = package_and_target
    if target['kind'] != ['bin']:
        raise RuntimeError(f'`{target["name"]}` is not a `bin` target')
    return target
