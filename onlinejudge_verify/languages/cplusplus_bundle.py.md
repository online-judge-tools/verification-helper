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
  code: "# Python Version: 3.x\nimport functools\nimport json\nimport os\nimport pathlib\n\
    import re\nimport shutil\nimport subprocess\nfrom logging import getLogger\nfrom\
    \ typing import *\n\nlogger = getLogger(__name__)\n\nbits_stdcxx_h = 'bits/stdc++.h'\n\
    \ncxx_standard_libs = {\n    'algorithm',\n    'array',\n    'bitset',\n    'chrono',\n\
    \    'codecvt',\n    'complex',\n    'condition_variable',\n    'deque',\n   \
    \ 'exception',\n    'forward_list',\n    'fstream',\n    'functional',\n    'future',\n\
    \    'iomanip',\n    'ios',\n    'iosfwd',\n    'iostream',\n    'istream',\n\
    \    'iterator',\n    'limits',\n    'list',\n    'locale',\n    'map',\n    'memory',\n\
    \    'mutex',\n    'new',\n    'numeric',\n    'ostream',\n    'queue',\n    'random',\n\
    \    'regex',\n    'set',\n    'sstream',\n    'stack',\n    'stdexcept',\n  \
    \  'streambuf',\n    'string',\n    'thread',\n    'tuple',\n    'typeinfo',\n\
    \    'unordered_map',\n    'unordered_set',\n    'utility',\n    'valarray',\n\
    \    'vector',\n}\n\nc_standard_libs = {\n    'assert.h',\n    'complex.h',\n\
    \    'ctype.h',\n    'errno.h',\n    'fenv.h',\n    'float.h',\n    'inttypes.h',\n\
    \    'iso646.h',\n    'limits.h',\n    'locale.h',\n    'math.h',\n    'setjmp.h',\n\
    \    'signal.h',\n    'stdalign.h',\n    'stdarg.h',\n    'stdatomic.h',\n   \
    \ 'stdbool.h',\n    'stddef.h',\n    'stdint.h',\n    'stdio.h',\n    'stdlib.h',\n\
    \    'stdnoreturn.h',\n    'string.h',\n    'tgmath.h',\n    'threads.h',\n  \
    \  'time.h',\n    'uchar.h',\n    'wchar.h',\n    'wctype.h',\n}\n\ncxx_c_origin_libs\
    \ = {'c' + name[:-len('.h')] for name in c_standard_libs}\n\nbits_extcxx_h = 'bits/extc++.h'\n\
    \next_libs = {\n    'ext/algorithm',\n    'ext/array_allocator.h',\n    'ext/atomicity.h',\n\
    \    'ext/bitmap_allocator.h',\n    'ext/cast.h',\n    'ext/concurrence.h',\n\
    \    'ext/debug_allocator.h',\n    'ext/extptr_allocator.h',\n    'ext/functional',\n\
    \    'ext/iterator',\n    'ext/malloc_allocator.h',\n    'ext/memory',\n    'ext/mt_allocator.h',\n\
    \    'ext/new_allocator.h',\n    'ext/numeric',\n    'ext/pod_char_traits.h',\n\
    \    'ext/pointer.h',\n    'ext/pool_allocator.h',\n    'ext/rb_tree',\n    'ext/rope',\n\
    \    'ext/slist',\n    'ext/stdio_filebuf.h',\n    'ext/stdio_sync_filebuf.h',\n\
    \    'ext/throw_allocator.h',\n    'ext/typelist.h',\n    'ext/type_traits.h',\n\
    \    'ext/vstring.h',\n    'ext/pb_ds/assoc_container.hpp',\n    'ext/pb_ds/priority_queue.hpp',\n\
    \    'ext/pb_ds/exception.hpp',\n    'ext/pb_ds/hash_policy.hpp',\n    'ext/pb_ds/list_update_policy.hpp',\n\
    \    'ext/pb_ds/tree_policy.hpp',\n    'ext/pb_ds/trie_policy.hpp',\n}\n\nbits_stdtr1cxx_h\
    \ = 'bits/stdtr1c++.h'\n\ntr1_libs = {\n    'tr1/array',\n    'tr1/cctype',\n\
    \    'tr1/cfenv',\n    'tr1/cfloat',\n    'tr1/cinttypes',\n    'tr1/climits',\n\
    \    'tr1/cmath',\n    'tr1/complex',\n    'tr1/cstdarg',\n    'tr1/cstdbool',\n\
    \    'tr1/cstdint',\n    'tr1/cstdio',\n    'tr1/cstdlib',\n    'tr1/ctgmath',\n\
    \    'tr1/ctime',\n    'tr1/cwchar',\n    'tr1/cwctype',\n    'tr1/functional',\n\
    \    'tr1/random',\n    'tr1/tuple',\n    'tr1/unordered_map',\n    'tr1/unordered_set',\n\
    \    'tr1/utility',\n}\n\n\n@functools.lru_cache(maxsize=None)\ndef _check_compiler(compiler:\
    \ str) -> str:\n    # Executables named \"g++\" are not always g++, due to the\
    \ fake g++ of macOS\n    version = subprocess.check_output([compiler, '--version']).decode()\n\
    \    if 'clang' in version.lower() or 'Apple LLVM'.lower() in version.lower():\n\
    \        return 'clang'\n    if 'g++' in version.lower():\n        return 'gcc'\n\
    \    return 'unknown'  # default\n\n\n@functools.lru_cache(maxsize=None)\ndef\
    \ _get_uncommented_code(path: pathlib.Path, *, iquotes_options: Tuple[str, ...],\
    \ compiler: str) -> bytes:\n    # `iquotes_options` must be a tuple to use `lru_cache`\n\
    \n    if shutil.which(compiler) is None:\n        raise BundleError(f'command\
    \ not found: {compiler}')\n    if _check_compiler(compiler) != 'gcc':\n      \
    \  if compiler == 'g++':\n            raise BundleError(f'A fake g++ is detected.\
    \ Please install the GNU C++ compiler.: {compiler}')\n        raise BundleError(f\"\
    It's not g++. Please specify g++ with $CXX envvar.: {compiler}\")\n    command\
    \ = [compiler, *iquotes_options, '-fpreprocessed', '-dD', '-E', str(path)]\n \
    \   return subprocess.check_output(command)\n\n\ndef get_uncommented_code(path:\
    \ pathlib.Path, *, iquotes: List[pathlib.Path], compiler: str) -> bytes:\n   \
    \ iquotes_options = []\n    for iquote in iquotes:\n        iquotes_options.extend(['-I',\
    \ str(iquote.resolve())])\n    code = _get_uncommented_code(path.resolve(), iquotes_options=tuple(iquotes_options),\
    \ compiler=compiler)\n    lines = []  # type: List[bytes]\n    for line in code.splitlines(keepends=True):\n\
    \        m = re.match(rb'# (\\d+) \".*\"', line.rstrip())\n        if m:\n   \
    \         lineno = int(m.group(1))\n            while len(lines) + 1 < lineno:\n\
    \                lines.append(b'\\n')\n        else:\n            lines.append(line)\n\
    \    return b''.join(lines)\n\n\nclass BundleError(Exception):\n    pass\n\n\n\
    class BundleErrorAt(BundleError):\n    def __init__(self, path: pathlib.Path,\
    \ line: int, message: str, *args, **kwargs):\n        try:\n            path =\
    \ path.resolve().relative_to(pathlib.Path.cwd())\n        except ValueError:\n\
    \            pass\n        message = '{}: line {}: {}'.format(str(path), line,\
    \ message)\n        super().__init__(message, *args, **kwargs)  # type: ignore\n\
    \n\nclass Bundler(object):\n    iquotes: List[pathlib.Path]\n    pragma_once:\
    \ Set[pathlib.Path]\n    pragma_once_system: Set[str]\n    result_lines: List[bytes]\n\
    \    path_stack: Set[pathlib.Path]\n    compiler: str\n\n    def __init__(self,\
    \ *, iquotes: List[pathlib.Path] = [], compiler: str = os.environ.get('CXX', 'g++'))\
    \ -> None:\n        self.iquotes = iquotes\n        self.pragma_once = set()\n\
    \        self.pragma_once_system = set()\n        self.result_lines = []\n   \
    \     self.path_stack = set()\n        self.compiler = compiler\n\n    # \u3053\
    \u308C\u3092\u3057\u306A\u3044\u3068 __FILE__ \u3084 __LINE__ \u304C\u58CA\u308C\
    \u308B\n    def _line(self, line: int, path: pathlib.Path) -> None:\n        while\
    \ self.result_lines and self.result_lines[-1].startswith(b'#line '):\n       \
    \     self.result_lines.pop()\n        try:\n            path = path.relative_to(pathlib.Path.cwd())\n\
    \        except ValueError:\n            pass\n        # \u30D1\u30B9\u4E2D\u306E\
    \u7279\u6B8A\u6587\u5B57\u3092 JSON style \u306B\u30A8\u30B9\u30B1\u30FC\u30D7\
    \u3057\u3066\u304B\u3089\u751F\u6210\u30B3\u30FC\u30C9\u306B\u8A18\u8FF0\n   \
    \     # quick solution to this: https://github.com/online-judge-tools/verification-helper/issues/280\n\
    \        self.result_lines.append('#line {} {}\\n'.format(line, json.dumps(str(path))).encode())\n\
    \n    # path \u3092\u89E3\u6C7A\u3059\u308B\n    # see: https://gcc.gnu.org/onlinedocs/gcc/Directory-Options.html#Directory-Options\n\
    \    def _resolve(self, path: pathlib.Path, *, included_from: pathlib.Path) ->\
    \ pathlib.Path:\n        if (included_from.parent / path).exists():\n        \
    \    return (included_from.parent / path).resolve()\n        for dir_ in self.iquotes:\n\
    \            if (dir_ / path).exists():\n                return (dir_ / path).resolve()\n\
    \        raise BundleErrorAt(path, -1, \"no such header\")\n\n    def update(self,\
    \ path: pathlib.Path) -> None:\n        if path.resolve() in self.pragma_once:\n\
    \            logger.debug('%s: skipped since this file is included once with include\
    \ guard', str(path))\n            return\n\n        # \u518D\u5E30\u7684\u306B\
    \u81EA\u5206\u81EA\u8EAB\u3092 #include \u3057\u3066\u305F\u3089\u8AE6\u3081\u308B\
    \n        if path in self.path_stack:\n            raise BundleErrorAt(path, -1,\
    \ \"cycle found in inclusion relations\")\n        self.path_stack.add(path)\n\
    \        try:\n\n            with open(str(path), \"rb\") as fh:\n           \
    \     code = fh.read()\n                if not code.endswith(b\"\\n\"):\n    \
    \                # \u30D5\u30A1\u30A4\u30EB\u306E\u672B\u5C3E\u306B\u6539\u884C\
    \u304C\u306A\u304B\u3063\u305F\u3089\u8DB3\u3059\n                    code +=\
    \ b\"\\n\"\n\n            # include guard \u306E\u307E\u308F\u308A\u306E\u5909\
    \u6570\n            # NOTE: include guard \u306B\u4F7F\u308F\u308C\u305F\u30DE\
    \u30AF\u30ED\u304C\u305D\u308C\u4EE5\u5916\u306E\u7528\u9014\u306B\u3082\u4F7F\
    \u308F\u308C\u305F\u308A #undef \u3055\u308C\u305F\u308A\u3059\u308B\u3068\u58CA\
    \u308C\u308B\u3051\u3069\u3001\u7121\u8996\u3057\u307E\u3059\n            non_guard_line_found\
    \ = False\n            pragma_once_found = False\n            include_guard_macro\
    \ = None  # type: Optional[str]\n            include_guard_define_found = False\n\
    \            include_guard_endif_found = False\n            preprocess_if_nest\
    \ = 0\n\n            lines = code.splitlines(keepends=True)\n            uncommented_lines\
    \ = get_uncommented_code(path, iquotes=self.iquotes, compiler=self.compiler).splitlines(keepends=True)\n\
    \            uncommented_lines.extend([b''] * (len(lines) - len(uncommented_lines)))\
    \  # trailing comment lines are removed\n            assert len(lines) == len(uncommented_lines)\n\
    \            self._line(1, path)\n            for i, (line, uncommented_line)\
    \ in enumerate(zip(lines, uncommented_lines)):\n\n                # nest \u306E\
    \u51E6\u7406\n                if re.match(rb'\\s*#\\s*(if|ifdef|ifndef)\\s.*',\
    \ uncommented_line):\n                    preprocess_if_nest += 1\n          \
    \      if re.match(rb'\\s*#\\s*(else\\s*|elif\\s.*)', uncommented_line):\n   \
    \                 if preprocess_if_nest == 0:\n                        raise BundleErrorAt(path,\
    \ i + 1, \"unmatched #else / #elif\")\n                if re.match(rb'\\s*#\\\
    s*endif\\s*', uncommented_line):\n                    preprocess_if_nest -= 1\n\
    \                    if preprocess_if_nest < 0:\n                        raise\
    \ BundleErrorAt(path, i + 1, \"unmatched #endif\")\n                is_toplevel\
    \ = preprocess_if_nest == 0 or (preprocess_if_nest == 1 and include_guard_macro\
    \ is not None)\n\n                # #pragma once\n                if re.match(rb'\\\
    s*#\\s*pragma\\s+once\\s*', line):  # #pragma once \u306F comment \u6271\u3044\
    \u3067\u6D88\u3055\u308C\u3066\u3057\u307E\u3046\n                    logger.debug('%s:\
    \ line %s: #pragma once', str(path), i + 1)\n                    if non_guard_line_found:\n\
    \                        # \u5148\u982D\u4EE5\u5916\u3067 #pragma once \u3055\u308C\
    \u3066\u305F\u5834\u5408\u306F\u8AE6\u3081\u308B\n                        raise\
    \ BundleErrorAt(path, i + 1, \"#pragma once found in a non-first line\")\n   \
    \                 if include_guard_macro is not None:\n                      \
    \  raise BundleErrorAt(path, i + 1, \"#pragma once found in an include guard with\
    \ #ifndef\")\n                    if path.resolve() in self.pragma_once:\n   \
    \                     return\n                    pragma_once_found = True\n \
    \                   self.pragma_once.add(path.resolve())\n                   \
    \ self._line(i + 2, path)\n                    continue\n\n                # #ifndef\
    \ HOGE_H as guard\n                if not pragma_once_found and not non_guard_line_found\
    \ and include_guard_macro is None:\n                    matched = re.match(rb'\\\
    s*#\\s*ifndef\\s+(\\w+)\\s*', uncommented_line)\n                    if matched:\n\
    \                        include_guard_macro = matched.group(1).decode()\n   \
    \                     logger.debug('%s: line %s: #ifndef %s', str(path), i + 1,\
    \ include_guard_macro)\n                        self.result_lines.append(b\"\\\
    n\")\n                        continue\n\n                # #define HOGE_H as\
    \ guard\n                if include_guard_macro is not None and not include_guard_define_found:\n\
    \                    matched = re.match(rb'\\s*#\\s*define\\s+(\\w+)\\s*', uncommented_line)\n\
    \                    if matched and matched.group(1).decode() == include_guard_macro:\n\
    \                        self.pragma_once.add(path.resolve())\n              \
    \          logger.debug('%s: line %s: #define %s', str(path), i + 1, include_guard_macro)\n\
    \                        include_guard_define_found = True\n                 \
    \       self.result_lines.append(b\"\\n\")\n                        continue\n\
    \n                # #endif as guard\n                if include_guard_define_found\
    \ and preprocess_if_nest == 0 and not include_guard_endif_found:\n           \
    \         if re.match(rb'\\s*#\\s*endif\\s*', uncommented_line):\n           \
    \             include_guard_endif_found = True\n                        self.result_lines.append(b\"\
    \\n\")\n                        continue\n\n                if uncommented_line:\n\
    \                    non_guard_line_found = True\n                    if include_guard_macro\
    \ is not None and not include_guard_define_found:\n                        # \u5148\
    \u982D\u306B #ifndef \u304C\u898B\u4ED8\u304B\u3063\u3066\u3082 #define \u304C\
    \u7D9A\u304B\u306A\u3044\u306A\u3089\u305D\u308C\u306F include guard \u3067\u306F\
    \u306A\u3044\n                        include_guard_macro = None\n           \
    \         if include_guard_endif_found:\n                        # include guard\
    \ \u306E\u5916\u5074\u306B\u30B3\u30FC\u30C9\u304C\u66F8\u304B\u308C\u3066\u3044\
    \u308B\u3068\u307E\u305A\u3044\u306E\u3067\u691C\u51FA\u3059\u308B\n         \
    \               raise BundleErrorAt(path, i + 1, \"found codes out of include\
    \ guard\")\n\n                # #include <...>\n                matched = re.match(rb'\\\
    s*#\\s*include\\s*<(.*)>\\s*', uncommented_line)\n                if matched:\n\
    \                    included = matched.group(1).decode()\n                  \
    \  logger.debug('%s: line %s: #include <%s>', str(path), i + 1, str(included))\n\
    \                    if included in self.pragma_once_system:\n               \
    \         self._line(i + 2, path)\n                    elif not is_toplevel:\n\
    \                        # #pragma once \u7CFB\u306E\u5224\u65AD\u304C\u3067\u304D\
    \u306A\u3044\u5834\u5408\u306F\u305D\u3063\u3068\u3057\u3066\u304A\u304F\n   \
    \                     self.result_lines.append(line)\n                    elif\
    \ included in c_standard_libs or included in cxx_standard_libs or included in\
    \ cxx_c_origin_libs:\n                        if bits_stdcxx_h in self.pragma_once_system:\n\
    \                            self._line(i + 2, path)\n                       \
    \ else:\n                            self.pragma_once_system.add(included)\n \
    \                           self.result_lines.append(line)\n                 \
    \   elif included in ext_libs:\n                        if bits_extcxx_h in self.pragma_once_system:\n\
    \                            self._line(i + 2, path)\n                       \
    \ else:\n                            self.pragma_once_system.add(included)\n \
    \                           self.result_lines.append(line)\n                 \
    \   elif included in tr1_libs:\n                        if bits_stdtr1cxx_h in\
    \ self.pragma_once_system:\n                            self._line(i + 2, path)\n\
    \                        else:\n                            self.pragma_once_system.add(included)\n\
    \                            self.result_lines.append(line)\n                \
    \    else:\n                        # possibly: bits/*, tr2/* boost/*, c-posix\
    \ library, etc.\n                        self.pragma_once_system.add(included)\n\
    \                        self.result_lines.append(line)\n                    \
    \    if included in [bits_extcxx_h, bits_stdtr1cxx_h]:\n                     \
    \       self.pragma_once_system.add(bits_stdcxx_h)\n                    continue\n\
    \n                # #include \"...\"\n                matched = re.match(rb'\\\
    s*#\\s*include\\s*\"(.*)\"\\s*', uncommented_line)\n                if matched:\n\
    \                    included = matched.group(1).decode()\n                  \
    \  logger.debug('%s: line %s: #include \"%s\"', str(path), i + 1, included)\n\
    \                    if not is_toplevel:\n                        # #if \u306E\
    \u4E2D\u304B\u3089 #include \u3055\u308C\u308B\u3068 #pragma once \u7CFB\u306E\
    \u5224\u65AD\u304C\u4E0D\u53EF\u80FD\u306B\u306A\u308B\u306E\u3067\u8AE6\u3081\
    \u308B\n                        raise BundleErrorAt(path, i + 1, \"unable to process\
    \ #include in #if / #ifdef / #ifndef other than include guards\")\n          \
    \          self.update(self._resolve(pathlib.Path(included), included_from=path))\n\
    \                    self._line(i + 2, path)\n                    # TODO: #include\
    \ \"iostream\" \u307F\u305F\u3044\u306B\u66F8\u3044\u305F\u3068\u304D\u306E\u6319\
    \u52D5\u3092\u306F\u3063\u304D\u308A\u3055\u305B\u308B\n                    #\
    \ TODO: #include <iostream> /* \u3068\u304B\u3092\u3084\u3089\u308C\u305F\u5834\
    \u5408\u3092\u843D\u3068\u3059\n                    continue\n\n             \
    \   # otherwise\n                self.result_lines.append(line)\n\n          \
    \  # #if #endif \u306E\u5BFE\u5FDC\u304C\u58CA\u308C\u3066\u305F\u3089\u8AE6\u3081\
    \u308B\n            if preprocess_if_nest != 0:\n                raise BundleErrorAt(path,\
    \ i + 1, \"unmatched #if / #ifdef / #ifndef\")\n            if include_guard_macro\
    \ is not None and not include_guard_endif_found:\n                raise BundleErrorAt(path,\
    \ i + 1, \"unmatched #ifndef\")\n\n        finally:\n            # \u4E2D\u3067\
    \ return \u3059\u308B\u3053\u3068\u304C\u3042\u308B\u306E\u3067 finally \u7BC0\
    \u306B\u5165\u308C\u3066\u304A\u304F\n            self.path_stack.remove(path)\n\
    \n    def get(self) -> bytes:\n        return b''.join(self.result_lines)\n"
  dependsOn: []
  isVerificationFile: false
  path: onlinejudge_verify/languages/cplusplus_bundle.py
  requiredBy: []
  timestamp: '1970-01-01 00:00:00+00:00'
  verificationStatus: LIBRARY_NO_TESTS
  verifiedWith: []
documentation_of: onlinejudge_verify/languages/cplusplus_bundle.py
layout: document
redirect_from:
- /library/onlinejudge_verify/languages/cplusplus_bundle.py
- /library/onlinejudge_verify/languages/cplusplus_bundle.py.html
title: onlinejudge_verify/languages/cplusplus_bundle.py
---
