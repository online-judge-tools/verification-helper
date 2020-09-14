---
data:
  _extendedDependsOn: []
  _extendedRequiredBy: []
  _extendedVerifiedWith: []
  _pathExtension: py
  _verificationStatusIcon: ':warning:'
  attributes: {}
  bundledCode: "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/documentation/build.py\"\
    , line 67, in _render_source_code_stat\n    bundled_code = language.bundle(stat.path,\
    \ basedir=basedir).decode()\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/languages/python.py\"\
    , line 84, in bundle\n    raise NotImplementedError\nNotImplementedError\n"
  code: "# Python Version: 3.x\nimport pathlib\nimport shlex\nimport subprocess\n\
    from logging import getLogger\nfrom typing import *\n\nfrom onlinejudge_verify.languages.models\
    \ import Language, LanguageEnvironment\nfrom onlinejudge_verify.languages.special_comments\
    \ import list_special_comments\n\nlogger = getLogger(__name__)\n\n\nclass OtherLanguageEnvironment(LanguageEnvironment):\n\
    \    config: Dict[str, str]\n\n    def __init__(self, *, config: Dict[str, str]):\n\
    \        self.config = config\n\n    def compile(self, path: pathlib.Path, *,\
    \ basedir: pathlib.Path, tempdir: pathlib.Path) -> None:\n        assert 'compile'\
    \ in self.config\n        command = self.config['compile'].format(path=str(path),\
    \ basedir=str(basedir), tempdir=str(tempdir))\n        logger.info('$ %s', command)\n\
    \        subprocess.check_call(shlex.split(command))\n\n    def get_execute_command(self,\
    \ path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> List[str]:\n\
    \        assert 'execute' in self.config\n        command = self.config['execute'].format(path=str(path),\
    \ basedir=str(basedir), tempdir=str(tempdir))\n        return shlex.split(command)\n\
    \n\nclass OtherLanguage(Language):\n    config: Dict[str, str]\n\n    def __init__(self,\
    \ *, config: Dict[str, str]):\n        self.config = config\n\n    def list_attributes(self,\
    \ path: pathlib.Path, *, basedir: pathlib.Path) -> Dict[str, str]:\n        if\
    \ 'list_attributes' not in self.config:\n            return list_special_comments(path)\n\
    \        logger.warning('\"languages.*.list_attributes\" field in .verify-helper/config.toml\
    \ is now obsoleted')\n\n        command = self.config['list_attributes'].format(path=str(path),\
    \ basedir=str(basedir))\n        text = subprocess.check_output(shlex.split(command))\n\
    \        attributes = {}\n        for line in text.splitlines():\n           \
    \ key, _, value = line.decode().partition(' ')\n            attributes[key] =\
    \ value\n        return attributes\n\n    def list_dependencies(self, path: pathlib.Path,\
    \ *, basedir: pathlib.Path) -> List[pathlib.Path]:\n        assert 'list_dependencies'\
    \ in self.config\n        command = self.config['list_dependencies'].format(path=str(path),\
    \ basedir=str(basedir))\n        text = subprocess.check_output(shlex.split(command))\n\
    \        dependencies = [path]\n        for line in text.splitlines():\n     \
    \       dependencies.append(pathlib.Path(line.decode()))\n        return dependencies\n\
    \n    def bundle(self, path: pathlib.Path, *, basedir: pathlib.Path) -> bytes:\n\
    \        assert 'bundle' in self.config\n        command = self.config['bundle'].format(path=str(path),\
    \ basedir=str(basedir))\n        logger.info('$ %s', command)\n        return\
    \ subprocess.check_output(shlex.split(command))\n\n    def is_verification_file(self,\
    \ path: pathlib.Path, *, basedir: pathlib.Path) -> bool:\n        suffix = self.config.get('verification_file_suffix')\n\
    \        if suffix is not None:\n            return path.name.endswith(suffix)\n\
    \        return super().is_verification_file(path, basedir=basedir)\n\n    def\
    \ list_environments(self, path: pathlib.Path, *, basedir: pathlib.Path) -> Sequence[OtherLanguageEnvironment]:\n\
    \        return [OtherLanguageEnvironment(config=self.config)]\n"
  dependsOn: []
  isVerificationFile: false
  path: onlinejudge_verify/languages/other.py
  requiredBy: []
  timestamp: '1970-01-01 00:00:00+00:00'
  verificationStatus: LIBRARY_NO_TESTS
  verifiedWith: []
documentation_of: onlinejudge_verify/languages/other.py
layout: document
redirect_from:
- /library/onlinejudge_verify/languages/other.py
- /library/onlinejudge_verify/languages/other.py.html
title: onlinejudge_verify/languages/other.py
---
