---
data:
  attributes: {}
  bundledCode: "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/documentation/build.py\"\
    , line 58, in _render_source_code_stat\n    bundled_code = language.bundle(stat.path,\
    \ basedir=basedir).decode()\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/languages/python.py\"\
    , line 84, in bundle\n    raise NotImplementedError\nNotImplementedError\n"
  code: "# Python Version: 3.x\nimport functools\nimport os\nimport pathlib\nimport\
    \ platform\nimport shlex\nimport shutil\nimport subprocess\nimport sys\nimport\
    \ tempfile\nfrom logging import getLogger\nfrom typing import *\n\nfrom onlinejudge_verify.config\
    \ import get_config\nfrom onlinejudge_verify.languages.cplusplus_bundle import\
    \ Bundler\nfrom onlinejudge_verify.languages.models import Language, LanguageEnvironment\n\
    from onlinejudge_verify.languages.special_comments import list_doxygen_annotations,\
    \ list_special_comments\n\nlogger = getLogger(__name__)\n\n\nclass CPlusPlusLanguageEnvironment(LanguageEnvironment):\n\
    \    CXX: pathlib.Path\n    CXXFLAGS: List[str]\n\n    def __init__(self, *, CXX:\
    \ pathlib.Path, CXXFLAGS: List[str]):\n        self.CXX = CXX\n        self.CXXFLAGS\
    \ = CXXFLAGS\n\n    def compile(self, path: pathlib.Path, *, basedir: pathlib.Path,\
    \ tempdir: pathlib.Path) -> None:\n        command = [str(self.CXX), *self.CXXFLAGS,\
    \ '-I', str(basedir), '-o', str(tempdir / 'a.out'), str(path)]\n        logger.info('$\
    \ %s', ' '.join(command))\n        subprocess.check_call(command)\n\n    def get_execute_command(self,\
    \ path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> List[str]:\n\
    \        return [str(tempdir / 'a.out')]\n\n    def _is_clang(self) -> bool:\n\
    \        return 'clang++' in self.CXX.name\n\n    def _is_gcc(self) -> bool:\n\
    \        return not self._is_clang() and 'g++' in self.CXX.name\n\n\n@functools.lru_cache(maxsize=None)\n\
    def _cplusplus_list_depending_files(path: pathlib.Path, *, CXX: pathlib.Path,\
    \ joined_CXXFLAGS: str) -> List[pathlib.Path]:\n    # Using /dev/stdout is acceptable\
    \ because Library Chcker doesn't work on Windows.\n    is_windows = (platform.uname().system\
    \ == 'Windows')\n    with tempfile.TemporaryDirectory() as temp_dir:\n       \
    \ temp_file = pathlib.Path(temp_dir) / 'dependencies.txt'\n        command = [str(CXX),\
    \ *shlex.split(joined_CXXFLAGS), '-MD', '-MF', str(temp_file), '-MM', str(path)]\n\
    \        try:\n            subprocess.check_call(command)\n        except subprocess.CalledProcessError:\n\
    \            logger.error(\"failed to analyze dependencies with %s: %s  (hint:\
    \ Please check #include directives of the file and its dependencies. The paths\
    \ must exist, must not contain '\\\\', and must be case-sensitive.)\", CXX, str(path))\n\
    \            print(f'::warning file={str(path)}::failed to analyze dependencies',\
    \ file=sys.stderr)\n            raise\n        with open(temp_file, 'rb') as fp:\n\
    \            data = fp.read()\n        logger.debug('dependencies of %s: %s',\
    \ str(path), repr(data))\n        makefile_rule = shlex.split(data.decode().strip().replace('\\\
    \\\\n', '').replace('\\\\\\r\\n', ''), posix=not is_windows)\n        return [pathlib.Path(path).resolve()\
    \ for path in makefile_rule[1:]]\n\n\n@functools.lru_cache(maxsize=None)\ndef\
    \ _cplusplus_list_defined_macros(path: pathlib.Path, *, CXX: pathlib.Path, joined_CXXFLAGS:\
    \ str) -> Dict[str, str]:\n    command = [str(CXX), *shlex.split(joined_CXXFLAGS),\
    \ '-dM', '-E', str(path)]\n    data = subprocess.check_output(command)\n    define\
    \ = {}\n    for line in data.decode().splitlines():\n        assert line.startswith('#define\
    \ ')\n        a, _, b = line[len('#define '):].partition(' ')\n        if (b.startswith('\"\
    ') and b.endswith('\"')) or (b.startswith(\"'\") and b.endswith(\"'\")):\n   \
    \         b = b[1:-1]\n        define[a] = b\n    return define\n\n\n_NOT_SPECIAL_COMMENTS\
    \ = '*NOT_SPECIAL_COMMENTS*'\n_PROBLEM = 'PROBLEM'\n_IGNORE = 'IGNORE'\n_IGNORE_IF_CLANG\
    \ = 'IGNORE_IF_CLANG'\n_IGNORE_IF_GCC = 'IGNORE_IF_GCC'\n_ERROR = 'ERROR'\n\n\n\
    # config.toml example:\n#     [[languages.cpp.environments]]\n#     CXX = \"g++\"\
    \n#     CXXFALGS = [\"-std=c++17\", \"-Wall\"]\nclass CPlusPlusLanguage(Language):\n\
    \    config: Dict[str, Any]\n\n    def __init__(self, *, config: Optional[Dict[str,\
    \ Any]] = None):\n        if config is None:\n            self.config = get_config().get('languages',\
    \ {}).get('cpp', {})\n        else:\n            self.config = config\n\n    def\
    \ _list_environments(self) -> List[CPlusPlusLanguageEnvironment]:\n        default_CXXFLAGS\
    \ = ['--std=c++17', '-O2', '-Wall', '-g']\n        if platform.system() == 'Darwin':\n\
    \            default_CXXFLAGS.append('-Wl,-stack_size,0x10000000')\n        if\
    \ platform.uname().system == 'Linux' and 'Microsoft' in platform.uname().release:\n\
    \            default_CXXFLAGS.append('-fsplit-stack')\n\n        if 'CXXFLAGS'\
    \ in os.environ and 'environments' not in self.config:\n            logger.warning('Usage\
    \ of $CXXFLAGS envvar to specify options is deprecated and will be removed soon')\n\
    \            print('::warning::Usage of $CXXFLAGS envvar to specify options is\
    \ deprecated and will be removed soon')\n            default_CXXFLAGS = shlex.split(os.environ['CXXFLAGS'])\n\
    \n        envs = []\n        if 'environments' in self.config:\n            #\
    \ configured: use specified CXX & CXXFLAGS\n            for env in self.config['environments']:\n\
    \                CXX: str = env.get('CXX')\n                if CXX is None:\n\
    \                    raise RuntimeError('CXX is not specified')\n            \
    \    CXXFLAGS: List[str] = env.get('CXXFLAGS', default_CXXFLAGS)\n           \
    \     if not isinstance(CXXFLAGS, list):\n                    raise RuntimeError('CXXFLAGS\
    \ must ba a list')\n                envs.append(CPlusPlusLanguageEnvironment(CXX=pathlib.Path(CXX),\
    \ CXXFLAGS=CXXFLAGS))\n\n        elif 'CXX' in os.environ:\n            # old-style:\
    \ \u4EE5\u524D\u306F $CXX \u3092\u4F7F\u3063\u3066\u305F\u3051\u3069\u8A2D\u5B9A\
    \u30D5\u30A1\u30A4\u30EB\u306B\u79FB\u884C\u3057\u305F\u3044\n            logger.warning('Usage\
    \ of $CXX envvar to restrict compilers is deprecated and will be removed soon')\n\
    \            print('::warning::Usage of $CXX envvar to restrict compilers is deprecated\
    \ and will be removed soon')\n            envs.append(CPlusPlusLanguageEnvironment(CXX=pathlib.Path(os.environ['CXX']),\
    \ CXXFLAGS=default_CXXFLAGS))\n\n        else:\n            # default: use found\
    \ compilers\n            for name in ('g++', 'clang++'):\n                path\
    \ = shutil.which(name)\n                if path is not None:\n               \
    \     envs.append(CPlusPlusLanguageEnvironment(CXX=pathlib.Path(path), CXXFLAGS=default_CXXFLAGS))\n\
    \n        if not envs:\n            raise RuntimeError('No C++ compilers found')\n\
    \        return envs\n\n    def list_attributes(self, path: pathlib.Path, *, basedir:\
    \ pathlib.Path) -> Dict[str, str]:\n        attributes: Dict[str, str] = {}\n\
    \        attributes.update(list_doxygen_annotations(path.resolve()))\n\n     \
    \   special_comments = list_special_comments(path.resolve())\n        if special_comments:\n\
    \            attributes.update(special_comments)\n\n        else:\n          \
    \  # use old-style if special comments not found\n            # #define PROBLEM\
    \ \"https://...\" \u306E\u5F62\u5F0F\u306F\u8907\u6570 environments \u3068\u306E\
    \u76F8\u6027\u304C\u3088\u304F\u306A\u3044\u3002\u3042\u3068\u9045\u3044\n   \
    \         attributes[_NOT_SPECIAL_COMMENTS] = ''\n            all_ignored = True\n\
    \            for env in self._list_environments():\n                joined_CXXFLAGS\
    \ = ' '.join(map(shlex.quote, [*env.CXXFLAGS, '-I', str(basedir)]))\n        \
    \        macros = _cplusplus_list_defined_macros(path.resolve(), CXX=env.CXX,\
    \ joined_CXXFLAGS=joined_CXXFLAGS)\n\n                # convert macros to attributes\n\
    \                if _IGNORE not in macros:\n                    for key in [_PROBLEM,\
    \ _ERROR]:\n                        if all_ignored:\n                        \
    \    # the first non-ignored environment\n                            if key in\
    \ macros:\n                                attributes[key] = macros[key]\n   \
    \                     else:\n                            assert attributes.get(key)\
    \ == macros.get(key)\n                    all_ignored = False\n              \
    \  else:\n                    if env._is_gcc():\n                        attributes[_IGNORE_IF_GCC]\
    \ = ''\n                    elif env._is_clang():\n                        attributes[_IGNORE_IF_CLANG]\
    \ = ''\n                    else:\n                        attributes[_IGNORE]\
    \ = ''\n            if all_ignored:\n                attributes[_IGNORE] = ''\n\
    \n        return attributes\n\n    def list_dependencies(self, path: pathlib.Path,\
    \ *, basedir: pathlib.Path) -> List[pathlib.Path]:\n        env = self._list_environments()[0]\n\
    \        joined_CXXFLAGS = ' '.join(map(shlex.quote, [*env.CXXFLAGS, '-I', str(basedir)]))\n\
    \        return _cplusplus_list_depending_files(path.resolve(), CXX=env.CXX, joined_CXXFLAGS=joined_CXXFLAGS)\n\
    \n    def bundle(self, path: pathlib.Path, *, basedir: pathlib.Path) -> bytes:\n\
    \        bundler = Bundler(iquotes=[basedir])\n        bundler.update(path)\n\
    \        return bundler.get()\n\n    def list_environments(self, path: pathlib.Path,\
    \ *, basedir: pathlib.Path) -> List[CPlusPlusLanguageEnvironment]:\n        attributes\
    \ = self.list_attributes(path, basedir=basedir)\n        envs = []\n        for\
    \ env in self._list_environments():\n            if env._is_gcc() and _IGNORE_IF_GCC\
    \ in attributes:\n                continue\n            if env._is_clang() and\
    \ _IGNORE_IF_CLANG in attributes:\n                continue\n            envs.append(env)\n\
    \        return envs\n"
  dependsOn: []
  extendedDependsOn: []
  extendedRequiredBy: []
  extendedVerifiedWith: []
  isVerificationFile: false
  path: onlinejudge_verify/languages/cplusplus.py
  requiredBy: []
  timestamp: '1970-01-01 00:00:00+00:00'
  verificationStatus: LIBRARY_NO_TESTS
  verificationStatusIcon: ':warning:'
  verifiedWith: []
documentation_of: onlinejudge_verify/languages/cplusplus.py
layout: document
redirect_from:
- /library/onlinejudge_verify/languages/cplusplus.py
- /library/onlinejudge_verify/languages/cplusplus.py.html
title: onlinejudge_verify/languages/cplusplus.py
---
