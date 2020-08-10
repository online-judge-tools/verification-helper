# Python Version: 3.x
import base64
import functools
import pathlib
import sys
from logging import getLogger
from typing import List, Sequence, Tuple

import importlab.environment
import importlab.fs
import importlab.graph
from onlinejudge_verify.languages.models import Language, LanguageEnvironment

logger = getLogger(__name__)


class PythonLanguageEnvironment(LanguageEnvironment):
    def compile(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> None:
        pass

    def get_execute_command(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> List[str]:
        # MEMO:
        # -   We use `base64` to avoid problems about quoting. e.g. for a file whose path contains whitespace ' ', quote '\'', doublequote '"', etc.
        # -   We use `os.execve` instead of `subprocess` because spawning subprocess sometimes cause troubles around signaling.
        # -   We set PYTHONPATH to import library files in a separated directory, e.g. to import `library/imported.py` from `tests/main.py` as `import library.imported`. Please take care about the case PYTHONPATH is already set.
        # -   We use `sys.executable` because `python` command may not exist or may not be Python 3.x.
        script = '; '.join([
            "'" + 'import base64, os, sys',
            f'path = base64.b64decode(b"{base64.b64encode(str(path.resolve()).encode()).decode()}").decode()',
            f'basedir = base64.b64decode(b"{base64.b64encode(str(basedir.resolve()).encode()).decode()}").decode()',
            'env = dict(os.environ)',
            'env["PYTHONPATH"] = (basedir + os.pathsep + env["PYTHONPATH"] if "PYTHONPATH" in env else basedir)',
            'os.execve(sys.executable, [sys.executable, path], env=env)' + "'",
        ])
        return [sys.executable, '-c', script]


@functools.lru_cache(maxsize=None)
def _python_list_depending_files(path: pathlib.Path, basedir: pathlib.Path) -> List[pathlib.Path]:
    # compute the dependency graph of the `path`
    env = importlab.environment.Environment(
        importlab.fs.Path([importlab.fs.OSFileSystem(str(basedir.resolve()))]),
        (sys.version_info.major, sys.version_info.minor),
    )
    res_graph = importlab.graph.ImportGraph.create(env, [str(path)])
    try:
        node_deps_pairs = res_graph.deps_list()  # type: List[Tuple[str, List[str]]]
    except Exception:
        raise RuntimeError(f"Failed to analyze the dependency graph (circular imports?): {path}")
    logger.debug('the dependency graph of %s: %s', str(path), node_deps_pairs)

    # collect Python files which are depended by the `path` and under `basedir`
    res_deps = []  # type: List[pathlib.Path]
    res_deps.append(path.resolve())
    for node_, deps_ in node_deps_pairs:
        node = pathlib.Path(node_)
        deps = list(map(pathlib.Path, deps_))
        if node.resolve() == path.resolve():
            for dep in deps:
                if basedir.resolve() in dep.resolve().parents:
                    res_deps.append(dep.resolve())
            break
    return list(set(res_deps))


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
