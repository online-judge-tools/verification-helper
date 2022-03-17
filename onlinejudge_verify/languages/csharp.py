# Python Version: 3.x
import distutils.version
import functools
import json
import os
import pathlib
import shutil
import subprocess
import xml.etree.ElementTree as ET
from logging import getLogger
from typing import *

import onlinejudge_verify.languages.special_comments as special_comments
from onlinejudge_verify.languages.models import Language, LanguageEnvironment

logger = getLogger(__name__)


@functools.lru_cache(maxsize=1)
def _check_dotnet_version() -> None:
    if not shutil.which('dotnet'):
        raise RuntimeError('`dotnet` not in $PATH')
    command = ['dotnet', '--version']
    logger.info('$ %s', ' '.join(command))
    res = subprocess.check_output(command).decode().strip()
    logger.info('dotnet version: %s', res)
    if distutils.version.LooseVersion(res) <= distutils.version.LooseVersion("6"):
        raise RuntimeError("oj-verify needs .NET 6 SDK or newer")


@functools.lru_cache(maxsize=1)
def _check_expander_console() -> None:
    if not shutil.which('dotnet-source-expand'):
        raise RuntimeError('`dotnet-source-expand` not in $PATH. Run `dotnet tool install -g SourceExpander.Console`')
    command = ['dotnet-source-expand', 'version']
    logger.info('$ %s', ' '.join(command))
    res = subprocess.check_output(command).decode().strip()
    logger.info('dotnet-source-expand version: %s', res)
    if distutils.version.LooseVersion(res) < distutils.version.LooseVersion("5"):
        raise RuntimeError('`dotnet-source-expand` version must be 5.0.0 or newer. Update SourceExpander.Console. `dotnet tool update -g SourceExpander.Console`')


class EmbeddedLibrary:
    def __init__(self, name: str, version: str) -> None:
        self.name = name
        self.version = version

    def __repr__(self) -> str:
        return 'EmbeddedLibrary("%s", "%s")' % (self.name, self.version)


@functools.lru_cache(maxsize=None)
def _list_embedded(csproj_path: pathlib.Path) -> List[EmbeddedLibrary]:
    _check_expander_console()
    if csproj_path is None or csproj_path.suffix != ".csproj":
        raise RuntimeError('csproj_path must be .csproj')
    command = ['dotnet-source-expand', 'library-list', str(csproj_path)]
    logger.info('$ %s', ' '.join(command))

    def enumerate_library(lines: List[str]):
        for line in lines:
            sp = line.split(',')
            if len(sp) >= 2:
                yield EmbeddedLibrary(sp[0], sp[1])

    res = list(enumerate_library(subprocess.check_output(command, encoding='utf-8').strip().splitlines()))
    logger.debug('libraries: %s', res)
    return res


@functools.lru_cache(maxsize=None)
def _check_embedded_existing(csproj_path: pathlib.Path) -> None:
    command = ['dotnet', 'build', str(csproj_path)]
    logger.info('$ %s', ' '.join(command))
    subprocess.check_output(command)
    l = _list_embedded(csproj_path)
    if len(l) == 0:
        raise RuntimeError('Library needs SourceExpander.Embedder')


def _check_env(path: pathlib.Path):
    _check_dotnet_version()
    _check_expander_console()
    _check_embedded_existing(_resolve_csproj(path))


@functools.lru_cache(maxsize=None)
def _check_no_embedder(csproj_path: pathlib.Path) -> None:
    root = ET.parse(csproj_path).getroot()
    if root.find('.//PackageReference[@Include="SourceExpander.Embedder"]'):
        logger.error(" Test project(%s) has `SourceExpander.Embedder` reference. Libraries and tests should not be in same project.", str(csproj_path))


@functools.lru_cache(maxsize=None)
def _resolve_csproj(path: pathlib.Path) -> Optional[pathlib.Path]:
    path = path.resolve()
    if path.suffix == ".csproj":
        return path

    proj = next(path.glob("*.csproj"), None)
    if proj is not None:
        return proj

    if path == path.parent:
        return None
    return _resolve_csproj(path.parent)


@functools.lru_cache(maxsize=None)
def _expand_code_dict(csproj_path: pathlib.Path) -> Dict[pathlib.Path, str]:
    _check_expander_console()
    command = ['dotnet-source-expand', 'expand-all', str(csproj_path)]
    logger.info('$ %s', ' '.join(command))
    json_res = subprocess.check_output(command)
    return {pathlib.Path(t['FilePath']): t['ExpandedCode'] for t in json.loads(json_res)}


@functools.lru_cache(maxsize=None)
def _expand_code(path: pathlib.Path) -> bytes:
    _check_expander_console()
    csproj_path = _resolve_csproj(path)
    _check_no_embedder(csproj_path)
    d = _expand_code_dict(csproj_path)
    return d[path].encode('utf-8')


class DependencyInfo:
    def __init__(self, filename: str, dependencies: List[str], typenames: Set[str]) -> None:
        self.filename = filename
        self.dependencies = dependencies
        self.defined_types = typenames

    def __repr__(self) -> str:
        return 'DependencyInfo("%s", %s, %s)' % (self.filename, self.dependencies, self.defined_types)


@functools.lru_cache(maxsize=None)
def _dependency_info_list(csproj_path: pathlib.Path) -> List[DependencyInfo]:
    _check_expander_console()
    _check_embedded_existing(csproj_path)
    if csproj_path is None or csproj_path.suffix != ".csproj":
        raise RuntimeError('csproj_path must be .csproj')

    command = ['dotnet-source-expand', 'dependency', '-p', str(csproj_path)]
    logger.info('$ %s', ' '.join(command))
    res = subprocess.check_output(command)
    return json.loads(res, object_hook=lambda d: DependencyInfo(d['FileName'], d['Dependencies'], set(d['TypeNames'])))


@functools.lru_cache(maxsize=None)
def _dependency_info_dict(csproj_path: pathlib.Path) -> Dict[pathlib.Path, DependencyInfo]:
    deps: Dict[pathlib.Path, DependencyInfo] = dict()
    for d in _dependency_info_list(csproj_path):
        p = pathlib.Path(d.filename)
        if p.exists():
            deps[p] = d
    return deps


@functools.lru_cache(maxsize=None)
def _list_dependencies(path: pathlib.Path) -> List[pathlib.Path]:
    path = path.resolve()
    depinfo = _dependency_info_dict(_resolve_csproj(path))
    return [p for p in (pathlib.Path(dep) for dep in depinfo[path].dependencies) if p.exists()]


@functools.lru_cache(maxsize=None)
def _get_target_framework(csproj_path: pathlib.Path) -> str:
    root = ET.parse(csproj_path).getroot()
    target = root.findtext('.//TargetFramework')
    if target is None:
        raise RuntimeError('<TargetFramework> is not found')
    return target


class CSharpLanguageEnvironment(LanguageEnvironment):
    @staticmethod
    def _create_runner_project(code: bytes, target_framework: str, output_dir):
        os.makedirs(str(output_dir), exist_ok=True)
        with open(output_dir / 'runner.csproj', 'w') as f:
            f.write('''<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>{}</TargetFramework>
  </PropertyGroup>
</Project>'''.format(target_framework))

        with open(output_dir / 'main.cs', 'wb') as f:
            f.write(code)

    def compile(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> None:
        path = path.resolve()
        output_dir = tempdir / 'dotnet'
        _check_env(path)
        target_framework = _get_target_framework(_resolve_csproj(path))
        logger.info('build: TargetFramework = %s', target_framework)
        self._create_runner_project(_expand_code(path), target_framework, output_dir)

        command = ['dotnet', 'build', str(output_dir / 'runner.csproj'), '-c', 'Release', '-o', str(output_dir / 'bin')]
        logger.info('$ %s', ' '.join(command))
        subprocess.check_output(command)

    def get_execute_command(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> List[str]:
        path = path.resolve()
        output_dir = tempdir / 'dotnet'
        path = path.resolve()
        _check_env(path)
        return [str(output_dir / 'bin' / 'runner')]


class CSharpLanguage(Language):
    def list_attributes(self, path: pathlib.Path, *, basedir: pathlib.Path) -> Dict[str, Any]:
        path = path.resolve()
        attributes: Dict[str, Any] = special_comments.list_special_comments(path)
        attributes.setdefault('links', [])
        attributes['links'].extend(special_comments.list_embedded_urls(path))
        return attributes

    def list_dependencies(self, path: pathlib.Path, *, basedir: pathlib.Path) -> List[pathlib.Path]:
        path = path.resolve()
        _check_env(path)
        return _list_dependencies(path)

    def bundle(self, path: pathlib.Path, *, basedir: pathlib.Path, options: Dict[str, Any]) -> bytes:
        path = path.resolve()
        _check_env(path)
        return _expand_code(path)

    def list_environments(self, path: pathlib.Path, *, basedir: pathlib.Path) -> Sequence[CSharpLanguageEnvironment]:
        return [CSharpLanguageEnvironment()]
