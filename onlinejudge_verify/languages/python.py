# Python Version: 3.x
import functools
import pathlib
import shlex
import subprocess
import sys
from logging import getLogger
from typing import Dict, List

import importlab

from onlinejudge_verify.languages.base import Language

logger = getLogger(__name__)


@functools.lru_cache(maxsize=None)
def _python_list_depending_files(path: pathlib.Path) -> List[pathlib.Path]:
    env = importlab.environment.Environment(
        importlab.fs.Path([importlab.fs.OSFileSystem(".")]),
        (sys.version_info.major, sys.version_info.minor),
    )
    res_graph = importlab.graph.ImportGraph.create(env, [str(path)])
    res_deps = []
    for node, deps in res_graph.deps_list():
        if node == str(path.resolve()):
            res_deps = deps
            break
    return list(map(pathlib.Path, res_deps))


class PythonLanguage(Language):
    def compile(
        self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path
    ) -> None:
        command = ["echo"]
        logger.info("$ %s", " ".join(command))
        subprocess.check_call(command)

    def get_execute_command(
        self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path
    ) -> List[str]:
        return [f"PYTHONPATH={base_dir}", "python", str(path)]

    def list_attributes(
        self, path: pathlib.Path, *, basedir: pathlib.Path
    ) -> Dict[str, str]:
        command = [*shlex.split("sed 's/^# verify-helper: // ; t ; d'"), str(path)]
        text = subprocess.check_output(command)
        attributes = {}
        for line in text.splitlines():
            key, _, value = line.decode().partition(" ")
            attributes[key] = value
        return attributes

    def list_dependencies(
        self, path: pathlib.Path, *, basedir: pathlib.Path
    ) -> List[pathlib.Path]:
        return _python_list_depending_files(path.resolve())

    def bundle(self, path: pathlib.Path, *, basedir: pathlib.Path) -> bytes:
        raise NotImplementedError
