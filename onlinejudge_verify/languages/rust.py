import abc
import functools
import itertools
import json
import pathlib
import shutil
import subprocess
from logging import getLogger
from subprocess import PIPE
from typing import *

from onlinejudge_verify.config import get_config
from onlinejudge_verify.languages import special_comments
from onlinejudge_verify.languages.models import Language, LanguageEnvironment

logger = getLogger(__name__)
_cargo_checked_workspaces: Set[pathlib.Path] = set()
_related_source_files_by_workspace: Dict[pathlib.Path, Dict[pathlib.Path, FrozenSet[pathlib.Path]]] = {}


class _ListDependenciesBackend:
    @abc.abstractmethod
    def list_dependencies(self, path: pathlib.Path, *, basedir: pathlib.Path) -> List[pathlib.Path]:
        raise NotImplementedError


class _NoBackend(_ListDependenciesBackend):
    def list_dependencies(self, path: pathlib.Path, *, basedir: pathlib.Path) -> List[pathlib.Path]:
        return _list_dependencies_by_crate(path, basedir=basedir, cargo_udeps_toolchain=None)


class _CargoUdeps(_ListDependenciesBackend):
    toolchain: str = 'nightly'

    def __init__(self, *, toolchain: Optional[str]):
        if toolchain is not None:
            self.toolchain = toolchain

    def list_dependencies(self, path: pathlib.Path, *, basedir: pathlib.Path) -> List[pathlib.Path]:
        return _list_dependencies_by_crate(path, basedir=basedir, cargo_udeps_toolchain=self.toolchain)


@functools.lru_cache(maxsize=None)
def _list_dependencies_by_crate(path: pathlib.Path, *, basedir: pathlib.Path, cargo_udeps_toolchain: Optional[str]) -> List[pathlib.Path]:
    """The `list_dependencies` implementation for `_NoBackend` and `CargoUdeps`.

    :param path: A parameter in `Language.list_dependencies`.
    :param basedir: A parameter in `Language.list_dependencies`.
    :param cargo_udeps_toolchain: A Rust toolchain name for cargo-udeps. If it is `None`, we don't run cargo-udeps.
    :returns: Paths to the `.rs` files for `Language.list_dependencies`.
    """
    path = basedir / path

    # We regard that a generated file does not depend on any files.
    for parent in path.parents:
        if (parent.parent / 'Cargo.toml').exists() and parent.parts[-1] == 'target':
            logger.warning('This is a generated file!: %s', path)
            return [path]

    metadata = _cargo_metadata(cwd=path.parent)

    # First, collects source files in the same crate.
    common_result = set(_source_files_in_same_targets(path, _related_source_files(metadata)))

    package_and_target = _find_target(metadata, path)
    if not package_and_target:
        return sorted(common_result)
    package, target = package_and_target

    packages_by_id = {package['id']: package for package in metadata['packages']}

    # Collect `normal`/`build` dependent crate from filesystem paths into a <"extern crate name"> → <package ID> map.
    non_dev_path_dependencies = {}
    node = [node for node in metadata['resolve']['nodes'] if node['id'] == package['id']][0]
    for dep in node['deps']:
        if packages_by_id[dep['pkg']]['source']:
            continue
        if all(dep_kind['kind'] == ['dev'] for dep_kind in dep['dep_kinds']):
            continue
        non_dev_path_dependencies[dep['name']] = dep['pkg']
    if not _is_lib_or_proc_macro(target) and any(map(_is_lib_or_proc_macro, package['targets'])):
        non_dev_path_dependencies[package['name']] = package['id']

    # If `cargo_udeps_toolchain` is present, collects packages that are "unused" by `target`.
    unused_packages = set()
    if cargo_udeps_toolchain is not None:
        explicit_names_in_toml = {d['rename'] for d in package['dependencies'] if d['rename']}
        if not shutil.which('cargo-udeps'):
            raise RuntimeError('`cargo-udeps` not in $PATH')
        unused_deps = json.loads(subprocess.run(
            ['rustup', 'run', cargo_udeps_toolchain, 'cargo', 'udeps', '--output', 'json', '--manifest-path', package['manifest_path'], *_target_option(target)],
            check=False,
            stdout=PIPE,
        ).stdout.decode())['unused_deps'].values()
        for unused_dep in unused_deps:
            if unused_dep['manifest_path'] != package['manifest_path']:
                continue
            for name_in_toml in [*unused_dep['normal'], *unused_dep['development'], *unused_dep['build']]:
                if name_in_toml in explicit_names_in_toml:
                    # If the `name_in_toml` is explicitly renamed one, it equals to the `extern_crate_name`.
                    unused_packages.add(non_dev_path_dependencies[name_in_toml])
                else:
                    # Otherwise, it equals to the `package.name`.
                    package_id = next((i for i in non_dev_path_dependencies.values() if packages_by_id[i]['name'] == name_in_toml), None)
                    if package_id:
                        unused_packages.add(package_id)
                    else:
                        logger.error('could not resolve `%s`', name_in_toml)

    ret = common_result
    for package_id in non_dev_path_dependencies.values():
        if package_id in unused_packages:
            continue
        package = packages_by_id[package_id]
        related_source_files = _related_source_files(_cargo_metadata_by_manifest_path(pathlib.Path(package["manifest_path"])))
        for target in package['targets']:
            if _is_lib_or_proc_macro(target):
                ret |= _source_files_in_same_targets(pathlib.Path(target['src_path']), related_source_files)
    return sorted(ret)


def _related_source_files(metadata: Dict[str, Any]) -> Dict[pathlib.Path, FrozenSet[pathlib.Path]]:
    """Collects all of the `.rs` files recognized by a workspace.

    :param metadata: Output of `cargo metadata`
    :returns: A (main source file) → (other related files) map
    """
    if pathlib.Path(metadata['workspace_root']) in _related_source_files_by_workspace:
        return _related_source_files_by_workspace[pathlib.Path(metadata['workspace_root'])]

    # Runs `cargo check` to generate `$target_directory/debug/deps/*.d`.
    if pathlib.Path(metadata['workspace_root']) not in _cargo_checked_workspaces:
        subprocess.run(
            ['cargo', 'check', '--manifest-path', str(pathlib.Path(metadata['workspace_root'], 'Cargo.toml')), '--workspace', '--all-targets'],
            cwd=metadata['workspace_root'],
            check=True,
        )
        _cargo_checked_workspaces.add(pathlib.Path(metadata['workspace_root']))

    ret: Dict[pathlib.Path, FrozenSet[pathlib.Path]] = dict()

    targets_in_workspace = itertools.chain.from_iterable(p['targets'] for p in metadata['packages'] if p['id'] in metadata['workspace_members'])
    for target in targets_in_workspace:
        # Finds a **latest** `.d` file that contains a line in the following format, and parses the line.
        #
        # ```
        # <absolute path to the `.d` file itself>: <relative path to the root source file> <relative/aboslute paths to the other related files>...
        # ```
        d_file_paths = sorted(
            pathlib.Path(metadata['target_directory'], 'debug', 'deps').glob(f'{target["name"].replace("-", "_")}-*.d'),
            key=lambda p: p.stat().st_mtime_ns,
            reverse=True,
        )
        for d_file_path in d_file_paths:
            with open(d_file_path) as d_file:
                d = d_file.read()
            found = False
            for line in d.splitlines():
                words = line.split(':')
                if len(words) == 2 and pathlib.Path(words[0]) == d_file_path:
                    # Ignores paths like `/dev/null` or `/usr/share/foo/bar` (if any).
                    paths = [pathlib.Path(metadata['workspace_root'], s) for s in words[1].split() if not pathlib.Path(s).is_absolute()]
                    if paths[:1] == [pathlib.Path(target['src_path'])]:
                        ret[paths[0]] = frozenset(paths[1:])
                        found = True
                        break
            if found:
                break
        else:
            logger.warning('no `.d` file for `%s`', target["name"])

    _related_source_files_by_workspace[pathlib.Path(metadata['workspace_root'])] = ret
    return ret


def _source_files_in_same_targets(path: pathlib.Path, related_source_files: Dict[pathlib.Path, FrozenSet[pathlib.Path]]) -> FrozenSet[pathlib.Path]:
    """Returns `.rs` file paths relating to `path`.

    :param path: Path to a `.rs` file
    :param related_source_files: Output of `_related_source_files`
    :returns: Relating `.rs` file paths
    """
    # If `p` is `src_path` of a target, it does not belong to any other target unless it's weirdly symlinked,
    if path in related_source_files:
        return frozenset({path, *related_source_files[path]})

    # Otherwise, it may be used by multiple targets with `#[path = ".."] mod foo;` or something.
    return frozenset(itertools.chain.from_iterable({k, *v} for (k, v) in related_source_files.items() if path in v)) or frozenset({path})


class RustLanguageEnvironment(LanguageEnvironment):
    def compile(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> None:
        path = basedir / path
        metadata = _cargo_metadata(cwd=path.parent)
        target = _ensure_target(metadata, path)
        subprocess.run(
            ['cargo', 'build', '--release', *_target_option(target)],
            cwd=path.parent,
            check=True,
        )

    def get_execute_command(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> List[str]:
        path = basedir / path
        metadata = _cargo_metadata(cwd=path.parent)
        target = _ensure_target(metadata, path)
        return [str(pathlib.Path(metadata['target_directory'], 'release', *([] if _is_bin(target) else ['examples']), target['name']))]


class RustLanguage(Language):
    _list_dependencies_backend: _ListDependenciesBackend

    def __init__(self, *, config: Optional[Dict[str, Any]] = None):
        if config is None:
            config = get_config().get('languages', {}).get('rust', {})

        # Parses `languages.rust.list_dependencies_backend`.
        if 'list_dependencies_backend' in config:
            list_dependencies_backend = config['list_dependencies_backend']

            if not isinstance(list_dependencies_backend, dict):
                raise RuntimeError('`languages.rust.list_dependencies_backend` must be `dict`')
            if 'kind' not in list_dependencies_backend:
                raise RuntimeError('missing `languages.rust.list_dependencies_backend.kind`')

            list_dependencies_backend_kind = list_dependencies_backend['kind']

            if not isinstance(list_dependencies_backend_kind, str):
                raise RuntimeError('`languages.rust.list_dependencies_backend.kind` must be `str`')

            if list_dependencies_backend_kind == 'none':
                self._list_dependencies_backend = _NoBackend()
            elif list_dependencies_backend_kind == 'cargo-udeps':
                if 'toolchain' not in list_dependencies_backend:
                    toolchain = None
                elif isinstance(list_dependencies_backend['toolchain'], str):
                    toolchain = list_dependencies_backend['toolchain']
                else:
                    raise RuntimeError('`languages.rust.list_dependencies_backend.toolchain` must be `str`')
                self._list_dependencies_backend = _CargoUdeps(toolchain=toolchain)
            else:
                raise RuntimeError("expected 'none' or 'cargo-udeps' for `languages.rust.list_dependencies_backend.kind`")
        else:
            self._list_dependencies_backend = _NoBackend()

    def list_dependencies(self, path: pathlib.Path, *, basedir: pathlib.Path) -> List[pathlib.Path]:
        return self._list_dependencies_backend.list_dependencies(path, basedir=basedir)

    def bundle(self, path: pathlib.Path, *, basedir: pathlib.Path, options: Dict[str, Any]) -> bytes:
        raise NotImplementedError

    def is_verification_file(self, path: pathlib.Path, *, basedir: pathlib.Path) -> bool:
        path = basedir / path
        metadata = _cargo_metadata(cwd=path.parent)
        package_and_target = _find_target(metadata, path)
        if not package_and_target:
            return False
        _, target = package_and_target
        return _is_bin_or_example_bin(target) and 'PROBLEM' in special_comments.list_special_comments(pathlib.Path(target['src_path']))

    def list_environments(self, path: pathlib.Path, *, basedir: pathlib.Path) -> Sequence[RustLanguageEnvironment]:
        return [RustLanguageEnvironment()]


def _cargo_metadata(cwd: pathlib.Path) -> Dict[str, Any]:
    """Runs `cargo metadata` for a Cargo.toml file in `cwd` or its parent directories.

    :raises ValueError: if `cwd` is not absolute
    """
    if not cwd.is_absolute():
        raise ValueError(f'the `cwd` parameter must be absolute: {cwd}')

    def find_root_manifest_for_wd() -> pathlib.Path:
        # https://docs.rs/cargo/0.48.0/cargo/util/important_paths/fn.find_root_manifest_for_wd.html
        for directory in [cwd, *cwd.parents]:
            manifest_path = directory / 'Cargo.toml'
            if manifest_path.exists():
                return manifest_path
        raise RuntimeError(f'Could not find `Cargo.toml` in `{cwd}` or any parent directory')

    return _cargo_metadata_by_manifest_path(find_root_manifest_for_wd())


@functools.lru_cache(maxsize=None)
def _cargo_metadata_by_manifest_path(manifest_path: pathlib.Path) -> Dict[str, Any]:
    """Runs `cargo metadata` for a certain `Cargo.toml`.

    This function is considered to be executed for every Cargo.toml in the repository.
    For detailed information about `cargo metadata`, see:

    - <https://doc.rust-lang.org/cargo/commands/cargo-metadata.html#output-format>
    - <https://docs.rs/cargo_metadata>

    :param manifest_path: Path to a `Cargo.toml`
    :returns: Output of `cargo metadata` command
    """
    return json.loads(subprocess.run(
        ['cargo', 'metadata', '--format-version', '1', '--manifest-path', str(manifest_path)],
        stdout=PIPE,
        cwd=manifest_path.parent,
        check=True,
    ).stdout.decode())


def _find_target(
    metadata: Dict[str, Any],
    src_path: pathlib.Path,
) -> Optional[Tuple[Dict[str, Any], Dict[str, Any]]]:
    for package in metadata['packages']:
        for target in package['targets']:
            if pathlib.Path(target['src_path']) == src_path:
                return package, target
    return None


def _ensure_target(metadata: Dict[str, Any], src_path: pathlib.Path) -> Dict[str, Any]:
    package_and_target = _find_target(metadata, src_path)
    if not package_and_target:
        raise RuntimeError(f'{src_path} is not a main source file of any target')
    _, target = package_and_target
    return target


def _is_lib_or_proc_macro(target: Dict[str, Any]) -> bool:
    return target['kind'] in [['lib'], ['proc-macro']]


def _is_bin(target: Dict[str, Any]) -> bool:
    return target['kind'] == ['bin']


def _is_bin_or_example_bin(target: Dict[str, Any]) -> bool:
    return _is_bin(target) or target['kind'] == ['example'] and target['crate_types'] == ['bin']


def _target_option(target: Dict[str, Any]) -> List[str]:
    if target['kind'] == ['bin']:
        return ['--bin', target['name']]
    if target['kind'] == ['example']:
        return ['--example', target['name']]
    if target['kind'] == ['test']:
        return ['--test', target['name']]
    if target['kind'] == ['bench']:
        return ['--bench', target['name']]
    return ['--lib']
