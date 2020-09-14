---
data:
  _extendedDependsOn: []
  _extendedRequiredBy: []
  _extendedVerifiedWith: []
  _pathExtension: py
  _verificationStatusIcon: ':warning:'
  attributes:
    links: []
  bundledCode: "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/documentation/build.py\"\
    , line 70, in _render_source_code_stat\n    bundled_code = language.bundle(stat.path,\
    \ basedir=basedir).decode()\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/languages/python.py\"\
    , line 84, in bundle\n    raise NotImplementedError\nNotImplementedError\n"
  code: "# Python Version: 3.x\nimport functools\nimport pathlib\nimport subprocess\n\
    from logging import getLogger\nfrom typing import *\n\nfrom onlinejudge_verify.config\
    \ import get_config\nfrom onlinejudge_verify.languages.models import Language,\
    \ LanguageEnvironment\n\nlogger = getLogger(__name__)\n\n\nclass NimLanguageEnvironment(LanguageEnvironment):\n\
    \    compile_to: str\n    NIMFLAGS: List[str]\n\n    def __init__(self, *, compile_to:\
    \ str, NIMFLAGS: List[str]):\n        self.compile_to = compile_to\n        self.NIMFLAGS\
    \ = NIMFLAGS\n\n    def compile(self, path: pathlib.Path, *, basedir: pathlib.Path,\
    \ tempdir: pathlib.Path) -> None:\n        command = [\"nim\", self.compile_to,\
    \ \"-p:.\", f\"-o:{str(tempdir /'a.out')}\", f\"--nimcache:{str(tempdir)}\"] +\
    \ self.NIMFLAGS + [str(path)]\n        logger.info('$ %s', ' '.join(command))\n\
    \        subprocess.check_call(command)\n\n    def get_execute_command(self, path:\
    \ pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> List[str]:\n\
    \        return [str(tempdir / \"a.out\")]\n\n\n@functools.lru_cache(maxsize=None)\n\
    def _list_direct_dependencies(path: pathlib.Path, *, basedir: pathlib.Path) ->\
    \ List[pathlib.Path]:\n    items: List[str] = []\n    with open(basedir / path,\
    \ 'rb') as fh:\n        for line in fh.read().decode().splitlines():\n       \
    \     line = line.strip()\n            if line.startswith('include'):\n      \
    \          items += line[7:].strip().split(',')\n            elif line.startswith('import'):\n\
    \                line = line[6:]\n                i = line.find(' except ')\n\
    \                if i >= 0:\n                    line = line[:i]\n           \
    \     items += line.split(',')\n            elif line.startswith('from'):\n  \
    \              i = line.find(' import ')\n                if i >= 0:\n       \
    \             items += line[4:i - 1]\n    dependencies = [path.resolve()]\n  \
    \  for item in items:\n        item = item.strip()\n        if item.startswith(\"\
    \\\"\"):\n            item = item[1:len(item) - 1]\n        else:\n          \
    \  item += \".nim\"\n        item_ = pathlib.Path(item)\n        if item_.exists():\n\
    \            dependencies.append(item_)\n    return list(set(dependencies))\n\n\
    \nclass NimLanguage(Language):\n    config: Dict[str, Any]\n\n    def __init__(self,\
    \ *, config: Optional[Dict[str, Any]] = None):\n        if config is None:\n \
    \           self.config = get_config().get('languages', {}).get('nim', {})\n \
    \       else:\n            self.config = config\n\n    def list_dependencies(self,\
    \ path: pathlib.Path, *, basedir: pathlib.Path) -> List[pathlib.Path]:\n     \
    \   dependencies = []\n        visited: Set[pathlib.Path] = set()\n        stk\
    \ = [path.resolve()]\n        while stk:\n            path = stk.pop()\n     \
    \       if path in visited:\n                continue\n            visited.add(path)\n\
    \            for child in _list_direct_dependencies(path, basedir=basedir):\n\
    \                dependencies.append(child)\n                stk.append(child)\n\
    \        return list(set(dependencies))\n\n    def bundle(self, path: pathlib.Path,\
    \ *, basedir: pathlib.Path) -> bytes:\n        raise NotImplementedError\n\n \
    \   def is_verification_file(self, path: pathlib.Path, *, basedir: pathlib.Path)\
    \ -> bool:\n        return path.name.endswith(\"_test.nim\")\n\n    def list_environments(self,\
    \ path: pathlib.Path, *, basedir: pathlib.Path) -> List[NimLanguageEnvironment]:\n\
    \        default_compile_to = 'cpp'\n        default_NIMFLAGS = ['-d:release',\
    \ '--opt:speed']\n        envs = []\n        if 'environments' not in self.config:\n\
    \            envs.append(NimLanguageEnvironment(compile_to=default_compile_to,\
    \ NIMFLAGS=default_NIMFLAGS))\n        else:\n            for env in self.config['environments']:\n\
    \                compile_to = env.get('compile_to', default_compile_to)\n    \
    \            NIMFLAGS: List[str] = env.get('NIMFLAGS', default_NIMFLAGS)\n   \
    \             if not isinstance(NIMFLAGS, list):\n                    raise RuntimeError('NIMFLAGS\
    \ must ba a list')\n                envs.append(NimLanguageEnvironment(compile_to=compile_to,\
    \ NIMFLAGS=NIMFLAGS))\n        return envs\n"
  dependsOn: []
  isVerificationFile: false
  path: onlinejudge_verify/languages/nim.py
  requiredBy: []
  timestamp: '1970-01-01 00:00:00+00:00'
  verificationStatus: LIBRARY_NO_TESTS
  verifiedWith: []
documentation_of: onlinejudge_verify/languages/nim.py
layout: document
redirect_from:
- /library/onlinejudge_verify/languages/nim.py
- /library/onlinejudge_verify/languages/nim.py.html
title: onlinejudge_verify/languages/nim.py
---
