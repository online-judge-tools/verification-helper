---
data:
  attributes: {}
  bundledCode: "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/documentation/build.py\"\
    , line 58, in _render_source_code_stat\n    bundled_code = language.bundle(stat.path,\
    \ basedir=basedir).decode()\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/languages/python.py\"\
    , line 84, in bundle\n    raise NotImplementedError\nNotImplementedError\n"
  code: "# Python Version: 3.x\nimport functools\nimport pathlib\nimport sys\nimport\
    \ textwrap\nfrom logging import getLogger\nfrom typing import List, Sequence,\
    \ Tuple\n\nimport importlab.environment\nimport importlab.fs\nimport importlab.graph\n\
    from onlinejudge_verify.languages.models import Language, LanguageEnvironment\n\
    \nlogger = getLogger(__name__)\n\n\nclass PythonLanguageEnvironment(LanguageEnvironment):\n\
    \    def compile(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir:\
    \ pathlib.Path) -> None:\n        code = textwrap.dedent(f\"\"\"\\\n         \
    \   #!{sys.executable}\n            \\\"\\\"\\\"This is a helper script to run\
    \ the target Python code.\n\n            We need this script to set PYTHONPATH\
    \ portably. The env command, quoting something, etc. are not portable or difficult\
    \ to implement.\n            \\\"\\\"\\\"\n\n            import os\n         \
    \   import sys\n\n            # arguments\n            path = {repr(str(path.resolve()))}\n\
    \            basedir = {repr(str(basedir.resolve()))}\n\n            # run {str(path)}\n\
    \            env = dict(os.environ)\n            if \"PYTHONPATH\" in env:\n \
    \               env[\"PYTHONPATH\"] = basedir + os.pathsep + env[\"PYTHONPATH\"\
    ] \n            else:\n                env[\"PYTHONPATH\"] = basedir  # set `PYTHONPATH`\
    \ to import files relative to the root directory\n            os.execve(sys.executable,\
    \ [sys.executable, path], env=env)  # use `os.execve` to avoid making an unnecessary\
    \ parent process\n        \"\"\")\n        with open(tempdir / 'compiled.py',\
    \ 'wb') as fh:\n            fh.write(code.encode())\n\n    def get_execute_command(self,\
    \ path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> List[str]:\n\
    \        return [sys.executable, str(tempdir / 'compiled.py')]\n\n\n@functools.lru_cache(maxsize=None)\n\
    def _python_list_depending_files(path: pathlib.Path, basedir: pathlib.Path) ->\
    \ List[pathlib.Path]:\n    # compute the dependency graph of the `path`\n    env\
    \ = importlab.environment.Environment(\n        importlab.fs.Path([importlab.fs.OSFileSystem(str(basedir.resolve()))]),\n\
    \        (sys.version_info.major, sys.version_info.minor),\n    )\n    res_graph\
    \ = importlab.graph.ImportGraph.create(env, [str(path)])\n    try:\n        node_deps_pairs\
    \ = res_graph.deps_list()  # type: List[Tuple[str, List[str]]]\n    except Exception:\n\
    \        raise RuntimeError(f\"Failed to analyze the dependency graph (circular\
    \ imports?): {path}\")\n    logger.debug('the dependency graph of %s: %s', str(path),\
    \ node_deps_pairs)\n\n    # collect Python files which are depended by the `path`\
    \ and under `basedir`\n    res_deps = []  # type: List[pathlib.Path]\n    res_deps.append(path.resolve())\n\
    \    for node_, deps_ in node_deps_pairs:\n        node = pathlib.Path(node_)\n\
    \        deps = list(map(pathlib.Path, deps_))\n        if node.resolve() == path.resolve():\n\
    \            for dep in deps:\n                if basedir.resolve() in dep.resolve().parents:\n\
    \                    res_deps.append(dep.resolve())\n            break\n    return\
    \ list(set(res_deps))\n\n\nclass PythonLanguage(Language):\n    def list_dependencies(self,\
    \ path: pathlib.Path, *, basedir: pathlib.Path) -> List[pathlib.Path]:\n     \
    \   return _python_list_depending_files(path.resolve(), basedir)\n\n    def bundle(self,\
    \ path: pathlib.Path, *, basedir: pathlib.Path) -> bytes:\n        \"\"\"\n  \
    \      :throws NotImplementedError:\n        \"\"\"\n        raise NotImplementedError\n\
    \n    def is_verification_file(self, path: pathlib.Path, *, basedir: pathlib.Path)\
    \ -> bool:\n        return '.test.py' in path.name\n\n    def list_environments(self,\
    \ path: pathlib.Path, *, basedir: pathlib.Path) -> Sequence[PythonLanguageEnvironment]:\n\
    \        # TODO add another environment (e.g. pypy)\n        return [PythonLanguageEnvironment()]\n"
  dependsOn: []
  extendedDependsOn: []
  extendedRequiredBy: []
  extendedVerifiedWith: []
  isVerificationFile: false
  path: onlinejudge_verify/languages/python.py
  requiredBy: []
  timestamp: '1970-01-01 00:00:00+00:00'
  verificationStatus: LIBRARY_NO_TESTS
  verificationStatusIcon: ':warning:'
  verifiedWith: []
documentation_of: onlinejudge_verify/languages/python.py
layout: document
redirect_from:
- /library/onlinejudge_verify/languages/python.py
- /library/onlinejudge_verify/languages/python.py.html
title: onlinejudge_verify/languages/python.py
---
