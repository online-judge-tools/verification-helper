# Python Version: 3.x
import functools
import pathlib
import subprocess
import sys
from logging import getLogger
from typing import List, Sequence

import importlab.environment
import importlab.fs
import importlab.graph
from onlinejudge_verify.languages.models import Language, LanguageEnvironment

logger = getLogger(__name__)


class PythonLanguageEnvironment(LanguageEnvironment):
    def compile(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> None:
        command = ["echo"]
        logger.info("$ %s", " ".join(command))
        subprocess.check_call(command)

    def get_execute_command(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> List[str]:
        # Adding basedir to PYTHONPATH for importing library files
        return ["python", "-c", f"\"import sys, pathlib, subprocess;subprocess.run('PYTHONPATH={basedir} python {path}', shell=True)\""]


@functools.lru_cache(maxsize=None)
def _python_list_depending_files(path: pathlib.Path, basedir: pathlib.Path) -> List[pathlib.Path]:
    env = importlab.environment.Environment(
        importlab.fs.Path([importlab.fs.OSFileSystem(str(basedir.resolve()))]),
        (sys.version_info.major, sys.version_info.minor),
    )
    res_graph = importlab.graph.ImportGraph.create(env, [str(path)])
    res_deps = []
    try:
        node_deps_pairs = res_graph.deps_list()
    except Exception:
        raise RuntimeError(f"Detect circular imports in {path}")

    for node, deps in node_deps_pairs:
        if node == str(path.resolve()):
            for dep in deps:
                if not isinstance(dep, str):
                    continue
                if dep.startswith(str(basedir)):
                    res_deps.append(dep)
            break
    return list(map(pathlib.Path, res_deps))


class PythonLanguage(Language):
    def list_dependencies(self, path: pathlib.Path, *, basedir: pathlib.Path) -> List[pathlib.Path]:
        return _python_list_depending_files(path.resolve(), basedir)

    def bundle(self, path: pathlib.Path, *, basedir: pathlib.Path) -> bytes:
        """
        :throws NotImplementedError:
        """
        raise NotImplementedError

    def is_verification_file(self, path: pathlib.Path, *, basedir: pathlib.Path) -> bool:
        return '.test.py' in path.name

    def list_environments(self, path: pathlib.Path, *, basedir: pathlib.Path) -> Sequence[PythonLanguageEnvironment]:
        # TODO add another environment (e.g. pypy)
        return [PythonLanguageEnvironment()]
