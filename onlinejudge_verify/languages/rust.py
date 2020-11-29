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
_source_file_sets_by_package_manifest_path: Dict[pathlib.Path, FrozenSet[FrozenSet[pathlib.Path]]] = {}


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


def _list_dependencies_by_crate(path: pathlib.Path, *, basedir: pathlib.Path, cargo_udeps_toolchain: Optional[str]) -> List[pathlib.Path]:
    path = basedir / path

    for parent in path.parents:
        if (parent.parent / 'Cargo.toml').exists() and parent.parts[-1] == 'target':
            logger.warning('This is a generated file!: %s', path)
            return [path]

    metadata = _cargo_metadata(cwd=path.parent)
    package_and_target = _find_target(metadata, path)

    source_file_sets = _source_file_sets(metadata)  # mutable

    def source_files_in_same_targets(p: pathlib.Path) -> FrozenSet[pathlib.Path]:
        # `p` may be used by multiple targets with `#[path = ".."] mod foo;` or something.
        return frozenset({p, *itertools.chain.from_iterable(s for s in source_file_sets if p in s)})

    ret = set(source_files_in_same_targets(path))

    if not package_and_target:
        return sorted(ret)
    package, target = package_and_target

    packages_by_id = {package['id']: package for package in metadata['packages']}
    normal_build_node_deps = {
        normal_build_node_dep['name']: normal_build_node_dep['pkg']
        for node in metadata['resolve']['nodes']
        if node['id'] == package['id']
        for normal_build_node_dep in node['deps']
        if not packages_by_id[normal_build_node_dep['pkg']]['source'] and any(
            not dep_kind['kind'] or dep_kind['kind'] == 'build'
            for dep_kind in normal_build_node_dep['dep_kinds']
        )
    } # yapf: disable

    if not _is_lib_or_proc_macro(target) and any(map(_is_lib_or_proc_macro, package['targets'])):
        normal_build_node_deps[package['name']] = package['id']

    unused_packages = set()
    if cargo_udeps_toolchain is not None:
        renames = {dependency['rename'] for dependency in package['dependencies'] if dependency['rename']}
        if not shutil.which('cargo-udeps'):
            raise RuntimeError('`cargo-udeps` not in $PATH')
        unused_deps = json.loads(subprocess.run(
            ['rustup', 'run', cargo_udeps_toolchain, 'cargo', 'udeps', '--output', 'json', '--manifest-path', package['manifest_path'], *_target_option(target)],
            check=False,
            stdout=PIPE,
        ).stdout.decode())['unused_deps'].values()
        for unused_dep in unused_deps:
            if unused_dep['manifest_path'] == package['manifest_path']:
                for name_in_toml in [*unused_dep['normal'], *unused_dep['development'], *unused_dep['build']]:
                    if name_in_toml in renames:
                        unused_packages.add(normal_build_node_deps[name_in_toml])
                    else:
                        for package_id in normal_build_node_deps.values():
                            if packages_by_id[package_id]['name'] == name_in_toml:
                                unused_packages.add(package_id)

    for package_id in normal_build_node_deps.values():
        if package_id not in unused_packages:
            package = packages_by_id[package_id]
            source_file_sets = _source_file_sets(_cargo_metadata(pathlib.Path(package["manifest_path"]).parent))
            for target in package['targets']:
                if _is_lib_or_proc_macro(target):
                    ret |= source_files_in_same_targets(pathlib.Path(target['src_path']))
    return sorted(ret)


def _source_file_sets(metadata: Dict[str, Any]) -> FrozenSet[FrozenSet[pathlib.Path]]:
    if pathlib.Path(metadata['workspace_root']) not in _cargo_checked_workspaces:
        subprocess.run(
            ['cargo', 'check', '--manifest-path', str(pathlib.Path(metadata['workspace_root'], 'Cargo.toml')), '--workspace', '--all-targets'],
            cwd=metadata['workspace_root'],
            check=True,
        )
        _cargo_checked_workspaces.add(pathlib.Path(metadata['workspace_root']))

    ret: Set[FrozenSet[pathlib.Path]] = set()

    for ws_member in (p for p in metadata['packages'] if p['id'] in metadata['workspace_members']):
        ws_member_manifest_path = pathlib.Path(ws_member['manifest_path'])

        if ws_member_manifest_path in _source_file_sets_by_package_manifest_path:
            ret |= _source_file_sets_by_package_manifest_path[ws_member_manifest_path]
            continue

        source_file_sets = set()

        for target in ws_member['targets']:
            d_file_paths = sorted(
                pathlib.Path(metadata['target_directory'], 'debug', 'deps').glob(f'{target["name"].replace("-", "_")}-*.d'),
                key=lambda p: p.stat().st_mtime_ns,
                reverse=True,
            )
            for d_file_path in d_file_paths:
                # Like this:
                #
                # ```
                # /home/ryo/src/github.com/rust-lang-ja/ac-library-rs/target/debug/deps/ac_library_rs-a044142420f688ff.rmeta: src/lib.rs src/convolution.rs src/dsu.rs src/fenwicktree.rs src/lazysegtree.rs src/math.rs src/maxflow.rs src/mincostflow.rs src/modint.rs src/scc.rs src/segtree.rs src/string.rs src/twosat.rs src/internal_bit.rs src/internal_math.rs src/internal_queue.rs src/internal_scc.rs src/internal_type_traits.rs
                #
                # /home/ryo/src/github.com/rust-lang-ja/ac-library-rs/target/debug/deps/ac_library_rs-a044142420f688ff.d: src/lib.rs src/convolution.rs src/dsu.rs src/fenwicktree.rs src/lazysegtree.rs src/math.rs src/maxflow.rs src/mincostflow.rs src/modint.rs src/scc.rs src/segtree.rs src/string.rs src/twosat.rs src/internal_bit.rs src/internal_math.rs src/internal_queue.rs src/internal_scc.rs src/internal_type_traits.rs
                #
                # src/lib.rs:
                # src/convolution.rs:
                # src/dsu.rs:
                # src/fenwicktree.rs:
                # src/lazysegtree.rs:
                # src/math.rs:
                # src/maxflow.rs:
                # src/mincostflow.rs:
                # src/modint.rs:
                # src/scc.rs:
                # src/segtree.rs:
                # src/string.rs:
                # src/twosat.rs:
                # src/internal_bit.rs:
                # src/internal_math.rs:
                # src/internal_queue.rs:
                # src/internal_scc.rs:
                # src/internal_type_traits.rs:
                # ```
                with open(d_file_path) as d_file:
                    d = d_file.read()
                source_file_group = None
                for line in d.splitlines():
                    words = line.split(':')
                    if len(words) == 2 and pathlib.Path(words[0]) == d_file_path:
                        paths = [pathlib.Path(metadata['workspace_root'], s) for s in words[1].split() if not pathlib.Path(s).is_absolute()]
                        if paths[:1] == [pathlib.Path(target['src_path'])]:
                            source_file_group = frozenset(paths)
                            break
                if source_file_group is not None:
                    source_file_sets.add(source_file_group)
                    break
            else:
                logger.warning('no `.d` file for `%s`', target["name"])

        _source_file_sets_by_package_manifest_path[ws_member_manifest_path] = frozenset(source_file_sets)
        ret |= source_file_sets

    return frozenset(ret)


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
    def find_root_manifest_for_wd() -> pathlib.Path:
        # https://docs.rs/cargo/0.48.0/cargo/util/important_paths/fn.find_root_manifest_for_wd.html
        assert cwd.is_absolute()
        for directory in [cwd, *cwd.parents]:
            manifest_path = directory / 'Cargo.toml'
            if manifest_path.exists():
                return manifest_path
        raise RuntimeError(f'Could not find `Cargo.toml` in `{cwd}` or any parent directory')

    return cargo_metadata_by_manifest_path(find_root_manifest_for_wd())


@functools.lru_cache(maxsize=None)
def cargo_metadata_by_manifest_path(manifest_path: pathlib.Path) -> Dict[str, Any]:
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
