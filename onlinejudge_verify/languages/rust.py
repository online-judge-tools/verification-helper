import abc
import enum
import functools
import itertools
import json
import pathlib
import shutil
import subprocess
from collections import defaultdict
from enum import Enum
from logging import getLogger
from subprocess import PIPE
from typing import *

from onlinejudge_verify.config import get_config
from onlinejudge_verify.languages import special_comments
from onlinejudge_verify.languages.models import Language, LanguageEnvironment

logger = getLogger(__name__)
_metadata_by_manifest_path: Dict[pathlib.Path, Dict[str, Any]] = {}
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
    common_result = set(_source_files_in_same_targets(path, _related_source_files(basedir, metadata)))

    main_package_and_target = _find_target(metadata, path)
    if not main_package_and_target:
        return sorted(common_result)
    main_package, main_target = main_package_and_target

    packages_by_id = {p['id']: p for p in metadata['packages']}

    class DependencyNamespace(Enum):
        NORMAL_DEVELOPMENT = enum.auto()
        BUILD = enum.auto()

        @classmethod
        def from_dep_kind(cls, kind: str):
            if kind == 'build':
                return cls.BUILD
            return cls.NORMAL_DEVELOPMENT

    # Collect the `(|dev-|build-)dependencies` into a <is a `build-dependency`> → (<"extern crate name"> → <package>) dictionary.
    dependencies: DefaultDict[DependencyNamespace, Dict[str, Dict[str, Any]]] = defaultdict(dict)
    for dep in next(n['deps'] for n in metadata['resolve']['nodes'] if n['id'] == main_package['id']):
        if _need_dev_deps(main_target) or any(k['kind'] is None for k in dep['dep_kinds']):
            dependencies[DependencyNamespace.NORMAL_DEVELOPMENT][dep['name']] = packages_by_id[dep['pkg']]
        if any(k['kind'] == 'build' for k in dep['dep_kinds']):
            dependencies[DependencyNamespace.BUILD][dep['name']] = packages_by_id[dep['pkg']]

    # If `cargo_udeps_toolchain` is present, collects packages that are "unused" by `target`.
    unused_packages = defaultdict(set)
    if cargo_udeps_toolchain is not None:
        explicit_names_in_toml = {(DependencyNamespace.from_dep_kind(d['kind']), d['rename']) for d in main_package['dependencies'] if d['rename']}
        if not shutil.which('cargo-udeps'):
            raise RuntimeError('`cargo-udeps` not in $PATH')
        unused_deps = json.loads(subprocess.run(
            ['rustup', 'run', cargo_udeps_toolchain, 'cargo', 'udeps', '--output', 'json', '--manifest-path', main_package['manifest_path'], *_target_option(main_target)],
            cwd=metadata['workspace_root'],
            check=False,
            stdout=PIPE,
        ).stdout.decode())['unused_deps'].values()
        unused_dep = next((u for u in unused_deps if u['manifest_path'] == main_package['manifest_path']), None)
        if unused_dep:
            names_in_toml = [(DependencyNamespace.NORMAL_DEVELOPMENT, name_in_toml) for name_in_toml in [*unused_dep['normal'], *unused_dep['development']]]
            names_in_toml.extend((DependencyNamespace.BUILD, name_in_toml) for name_in_toml in unused_dep['build'])
            for dependency_namespace, name_in_toml in names_in_toml:
                if (dependency_namespace, name_in_toml) in explicit_names_in_toml:
                    # If the `name_in_toml` is explicitly renamed one, it equals to the `extern_crate_name`.
                    unused_package = dependencies[dependency_namespace][name_in_toml]['id']
                else:
                    # Otherwise, it equals to the `package.name`.
                    unused_package = next(p['id'] for p in dependencies[dependency_namespace].values() if p['name'] == name_in_toml)
                unused_packages[dependency_namespace].add(unused_package)

    # Finally, adds source files related to the depended crates except:
    #
    # - those detected by cargo-udeps
    # - those come from Crates.io or Git repositories (e.g. `proconio`, other people's libraries including `ac-library-rs`)

    # `main_package` should always be included.
    # Note that cargo-udeps does not detect it if it is unused.
    # https://github.com/est31/cargo-udeps/pull/35
    depended_packages = [main_package]
    for dependency_namespace, values in dependencies.items():
        for depended_package in values.values():
            if depended_package['id'] not in unused_packages[dependency_namespace] and not depended_package['source']:
                depended_packages.append(depended_package)

    ret = common_result

    for depended_package in depended_packages:
        depended_targets = [t for t in depended_package['targets'] if t != main_target and (_is_build(t) or _is_lib_or_proc_macro(t))]
        assert len(depended_targets) <= 2
        for depended_target in depended_targets:
            related_source_files = _related_source_files(basedir, _cargo_metadata_by_manifest_path(pathlib.Path(depended_package["manifest_path"])))
            ret |= _source_files_in_same_targets(pathlib.Path(depended_target['src_path']).resolve(strict=True), related_source_files)
    return sorted(ret)


def _related_source_files(basedir: pathlib.Path, metadata: Dict[str, Any]) -> Dict[pathlib.Path, FrozenSet[pathlib.Path]]:
    """Collects all of the `.rs` files recognized by a workspace.

    :param basedir: A parameter from `Language.list_dependencies`.
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
        # Finds the **latest** "dep-info" file that contains a line in the following format, and parses the line.
        #
        # ```
        # <relative/absolute path to the `.d` file itself>: <relative/absolute path to the root source file> <relative/aboslute paths to the other related files>...
        # ```
        #
        # - https://github.com/rust-lang/cargo/blob/rust-1.49.0/src/cargo/core/compiler/fingerprint.rs#L1979-L1997
        # - https://github.com/rust-lang/cargo/blob/rust-1.49.0/src/cargo/core/compiler/fingerprint.rs#L1824-L1830
        if _is_build(target):
            dep_info_paths = pathlib.Path(metadata['target_directory'], 'debug', 'build').rglob(f'{_crate_name(target)}-*.d')
        elif _is_example(target):
            dep_info_paths = pathlib.Path(metadata['target_directory'], 'debug', 'examples').glob(f'{_crate_name(target)}-*.d')
        else:
            dep_info_paths = pathlib.Path(metadata['target_directory'], 'debug', 'deps').glob(f'{_crate_name(target)}-*.d')
        for dep_info_path in sorted(dep_info_paths, key=lambda p: p.stat().st_mtime_ns, reverse=True):
            with open(dep_info_path) as file:
                dep_info = file.read()
            for line in dep_info.splitlines():
                ss = line.split(': ')
                if len(ss) == 2 and pathlib.Path(metadata['workspace_root'], ss[0]) == dep_info_path:
                    paths = []
                    it = iter(ss[1].split())
                    for s in it:
                        while s.endswith('\\'):
                            s = s.rstrip('\\')
                            s += ' '
                            s += next(it)
                        path = pathlib.Path(metadata['workspace_root'], s).resolve(strict=True)
                        # Ignores paths that don't start with the `basedir`. (e.g. `/dev/null`, `/usr/local/share/foo/bar`)
                        try:
                            # `PurePath.is_relative_to` is since Python 3.9.
                            _ = path.relative_to(basedir)
                            paths.append(path)
                        except ValueError:
                            pass
                    if paths[:1] == [pathlib.Path(target['src_path']).resolve(strict=True)]:
                        ret[paths[0]] = frozenset(paths[1:])
                        break
            else:
                continue
            break
        else:
            logger.error('no `.d` file for `%s`', target["name"])

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
        return _is_bin_or_example_bin(target) and 'PROBLEM' in special_comments.list_special_comments(path)

    def list_environments(self, path: pathlib.Path, *, basedir: pathlib.Path) -> Sequence[RustLanguageEnvironment]:
        return [RustLanguageEnvironment()]


def _cargo_metadata(cwd: pathlib.Path) -> Dict[str, Any]:
    """Returns "metadata" for a Cargo.toml file in `cwd` or its parent directories.

    :raises ValueError: if `cwd` is not absolute or contains `..`
    :returns: Output of `cargo metadata` command
    """
    if not cwd.is_absolute() or '..' in cwd.parts:
        raise ValueError(f'the `cwd` parameter must be absolute and must not contain `..`: {cwd}')

    # https://docs.rs/cargo/0.49.0/src/cargo/util/important_paths.rs.html#6-20
    for directory in [cwd, *cwd.parents]:
        manifest_path = directory / 'Cargo.toml'
        if manifest_path.exists():
            return _cargo_metadata_by_manifest_path(manifest_path)
    raise RuntimeError(f'could not find `Cargo.toml` in `{cwd}` or any parent directory')


def _cargo_metadata_by_manifest_path(manifest_path: pathlib.Path) -> Dict[str, Any]:
    """Returns "metadata" for a certain `Cargo.toml`.

    :returns: Output of `cargo metadata` command
    """
    if manifest_path in _metadata_by_manifest_path:
        return _metadata_by_manifest_path[manifest_path]

    metadata = _run_cargo_metadata(manifest_path)
    root_manifest_path = pathlib.Path(metadata['workspace_root'], 'Cargo.toml')
    if root_manifest_path != manifest_path:
        metadata = _run_cargo_metadata(root_manifest_path)

    for key in [root_manifest_path, *(pathlib.Path(p['manifest_path']) for p in metadata['packages'] if p['id'] in metadata['workspace_members'])]:
        _metadata_by_manifest_path[key] = metadata

    return metadata


def _run_cargo_metadata(manifest_path: pathlib.Path) -> Dict[str, Any]:
    """Runs `cargo metadata` for a certain `Cargo.toml`.

    This function is considered to be executed just once for every Cargo.toml in the repository.
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
            # A `src_path` may contain `..`
            # The path may not actually exist by being excluded from the package.
            if pathlib.Path(target['src_path']).resolve() == src_path:
                return package, target
    return None


def _ensure_target(metadata: Dict[str, Any], src_path: pathlib.Path) -> Dict[str, Any]:
    package_and_target = _find_target(metadata, src_path)
    if not package_and_target:
        raise RuntimeError(f'{src_path} is not a main source file of any target')
    _, target = package_and_target
    return target


def _crate_name(target: Dict[str, Any]) -> bool:
    return target['name'].replace('-', '_')


def _is_build(target: Dict[str, Any]) -> bool:
    return target['kind'] == ['custom-build']


def _is_lib_or_proc_macro(target: Dict[str, Any]) -> bool:
    return target['kind'] in [['lib'], ['proc-macro']]


def _is_bin(target: Dict[str, Any]) -> bool:
    return target['kind'] == ['bin']


def _is_example(target: Dict[str, Any]) -> bool:
    return target['kind'] == ['example']


def _is_bin_or_example_bin(target: Dict[str, Any]) -> bool:
    return _is_bin(target) or _is_example(target) and target['crate_types'] == ['bin']


def _need_dev_deps(target: Dict[str, Any]) -> bool:
    # Comes from https://docs.rs/cargo/0.49.0/cargo/ops/enum.CompileFilter.html#method.need_dev_deps
    return not (_is_lib_or_proc_macro(target) or _is_bin(target))


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
