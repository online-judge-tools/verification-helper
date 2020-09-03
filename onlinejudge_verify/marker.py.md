---
data:
  attributes: {}
  bundledCode: "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/documentation/build.py\"\
    , line 58, in _render_source_code_stat\n    bundled_code = language.bundle(stat.path,\
    \ basedir=basedir).decode()\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/languages/python.py\"\
    , line 84, in bundle\n    raise NotImplementedError\nNotImplementedError\n"
  code: "# Python Version: 3.x\nimport concurrent.futures\nimport datetime\nimport\
    \ functools\nimport json\nimport pathlib\nimport subprocess\nimport traceback\n\
    from typing import *\n\nimport onlinejudge_verify.languages\nimport onlinejudge_verify.utils\n\
    \n_error_timestamp = datetime.datetime.fromtimestamp(0, tz=datetime.timezone(datetime.timedelta()))\n\
    \n\ndef _cwd() -> pathlib.Path:\n    # .resolve() is required for Windows on GitHub\
    \ Actions because we need to expand 8.3 filenames like `C:\\\\Users\\\\RUNNER~1\\\
    \\AppData\\\\Local\\\\Temp\\\\tmp_xxxxxxx` to `C:\\\\Users\\\\runneradmin\\\\\
    AppData\\\\Local\\\\Temp\\\\tmp_xxxxxxx`\n    return pathlib.Path.cwd().resolve(strict=True)\n\
    \n\nclass VerificationMarker(object):\n    json_path: pathlib.Path\n    use_git_timestamp:\
    \ bool\n    old_timestamps: Dict[pathlib.Path, datetime.datetime]\n    new_timestamps:\
    \ Dict[pathlib.Path, datetime.datetime]\n    verification_statuses: Dict[pathlib.Path,\
    \ str]\n\n    def __init__(self, *, json_path: pathlib.Path, use_git_timestamp:\
    \ bool, jobs: Optional[int] = None) -> None:\n        self.json_path = json_path\n\
    \        self.use_git_timestamp = use_git_timestamp\n        self.verification_statuses\
    \ = {}\n        self.load_timestamps(jobs=jobs)\n\n    def get_current_timestamp(self,\
    \ path: pathlib.Path) -> datetime.datetime:\n        if self.use_git_timestamp:\n\
    \            return get_last_commit_time_to_verify(path)\n        else:\n    \
    \        language = onlinejudge_verify.languages.get(path)\n            assert\
    \ language is not None\n            try:\n                depending_files = language.list_dependencies(path,\
    \ basedir=_cwd())\n            except Exception:\n                traceback.print_exc()\n\
    \                return _error_timestamp\n            else:\n                timestamp\
    \ = max([x.stat().st_mtime for x in depending_files])\n                system_local_timezone\
    \ = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo\n       \
    \         return datetime.datetime.fromtimestamp(timestamp, tz=system_local_timezone).replace(microsecond=0)\
    \  # microsecond=0 is required because it's erased on timestamps.*.json\n\n  \
    \  def is_verified(self, path: pathlib.Path) -> bool:\n        if not path.exists():\n\
    \            return False\n        path = path.resolve(strict=True).relative_to(_cwd())\n\
    \        return self.verification_statuses.get(path) == 'verified'\n\n    def\
    \ mark_verified(self, path: pathlib.Path) -> None:\n        \"\"\"\n        :param\
    \ path: should exist\n        \"\"\"\n\n        path = path.resolve(strict=True).relative_to(_cwd())\n\
    \        self.new_timestamps[path] = self.get_current_timestamp(path)\n      \
    \  self.verification_statuses[path] = 'verified'\n\n    def is_failed(self, path:\
    \ pathlib.Path) -> bool:\n        if not path.exists():\n            return True\n\
    \        path = path.resolve(strict=True).relative_to(_cwd())\n        if path\
    \ not in self.verification_statuses:\n            # verified\u306E\u5834\u5408\
    \u306F\u5FC5\u305Aself.verification_status[path] == 'verified'\u3068\u306A\u308B\
    \u306E\u3067\u3053\u306Eif\u306E\u4E2D\u306B\u306F\u5165\u3089\u306A\u3044\n \
    \           # \u305D\u308C\u4EE5\u5916\u306E\u5834\u5408\u306F\u300C\u305D\u3082\
    \u305D\u3082\u30C6\u30B9\u30C8\u3092\u5B9F\u884C\u3057\u3066\u3044\u306A\u3044\
    \u300D\u53EF\u80FD\u6027\u3082\u3042\u308B\u304C\u4E00\u65E6\u306Ffailed\u3068\
    \u307F\u306A\u3059\n            return True\n        return self.verification_statuses[path]\
    \ == 'failed'\n\n    def mark_failed(self, path: pathlib.Path) -> None:\n    \
    \    if not path.exists():\n            return\n        path = path.resolve(strict=True).relative_to(_cwd())\n\
    \        self.verification_statuses[path] = 'failed'\n\n    def load_timestamps(self,\
    \ *, jobs: Optional[int] = None) -> None:\n        # \u53E4\u3044\u3082\u306E\u3092\
    \u8AAD\u307F\u8FBC\u3080\n        self.old_timestamps = {}\n        if self.json_path.exists():\n\
    \            with open(self.json_path) as fh:\n                data = json.load(fh)\n\
    \            for path, timestamp in data.items():\n                if path ==\
    \ '~' and timestamp == 'dummy':  # for backward compatibility\n              \
    \      continue\n                self.old_timestamps[pathlib.Path(path)] = datetime.datetime.strptime(timestamp,\
    \ '%Y-%m-%d %H:%M:%S %z')\n\n        # \u65B0\u3057\u3044\u3082\u306E\u306B\u79FB\
    \u3059\n        self.new_timestamps = {}\n\n        def load(path, timestamp):\n\
    \            if path.exists() and _error_timestamp < self.get_current_timestamp(path)\
    \ <= timestamp:\n                self.mark_verified(path)\n                return\n\
    \            #\u300C\u305D\u3082\u305D\u3082\u30C6\u30B9\u30C8\u3092\u5B9F\u884C\
    \u3057\u3066\u3044\u306A\u3044\u300D\u306E\u304B\u300C\u5B9F\u884C\u3057\u305F\
    \u4E0A\u3067\u5931\u6557\u3057\u305F\u300D\u306E\u304B\u533A\u5225\u3067\u304D\
    \u306A\u3044\u304C\u3001verify\u3067\u304D\u3066\u306A\u3044\u4E8B\u306B\u306F\
    \u5909\u308F\u308A\u306A\u3044\u306E\u3067\u4E00\u65E6\u306Ffailed\u3068\u307F\
    \u306A\u3059\n            self.mark_failed(path)\n            if path.exists():\n\
    \                # \u904E\u53BB\u306Bverify\u3055\u308C\u305F\u3053\u3068\u304C\
    \u3042\u308B\u5834\u5408\u306F\u3001\u6700\u7D42verify\u6642\u523B\u3092\u5F15\
    \u304D\u7D99\u3050\n                self.new_timestamps[path] = timestamp\n\n\
    \        if jobs is None:\n            for path, timestamp in self.old_timestamps.items():\n\
    \                load(path, timestamp)\n        else:\n            # TODO: \u3053\
    \u3053 (\u5B9F\u8CEA VerificationMarker.__init__) \u304C\u9045\u3044\u306E\u306A\
    \u3093\u3060\u304B\u304A\u304B\u3057\u304F\u306A\u3044\u304B\uFF1F verify\u6642\
    \u523B\u304C\u53E4\u3044\u3082\u306E\u306E\u51E6\u7406\u3068\u304B\u306F\u5225\
    \u3067\u3084\u308B\u3079\u304D\u306A\u6C17\u304C\u3059\u308B\n            # \u4F9D\
    \u5B58\u5148\u30D5\u30A1\u30A4\u30EB\u306E\u89E3\u6790\u306A\u3069\u304C\u3042\
    \u3063\u3066\u9045\u3044\u306E\u3067\u4E26\u5217\u3067\u3084\u308B\n         \
    \   with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as executor:\n\
    \                for path, timestamp in self.old_timestamps.items():\n       \
    \             executor.submit(load, path, timestamp)\n\n    def save_timestamps(self)\
    \ -> None:\n        data = {}\n        for path, timestamp in self.new_timestamps.items():\n\
    \            if self.verification_statuses[path] == 'verified':\n            \
    \    data[str(path)] = timestamp.strftime('%Y-%m-%d %H:%M:%S %z')\n        with\
    \ open(self.json_path, 'w') as fh:\n            json.dump(data, fh, sort_keys=True,\
    \ indent=0)\n\n    def __enter__(self) -> 'VerificationMarker':\n        return\
    \ self\n\n    def __exit__(self, exc_type, exc_value, traceback) -> None:\n  \
    \      self.save_timestamps()\n\n\n_verification_marker = None  # type: Optional[VerificationMarker]\n\
    \n\ndef get_verification_marker(*, jobs: Optional[int] = None) -> VerificationMarker:\n\
    \    global _verification_marker\n    if _verification_marker is None:\n     \
    \   # use different files in local and in remote to avoid conflicts\n        if\
    \ onlinejudge_verify.utils.is_local_execution():\n            timestamps_json_path\
    \ = pathlib.Path('.verify-helper/timestamps.local.json')\n        else:\n    \
    \        timestamps_json_path = pathlib.Path('.verify-helper/timestamps.remote.json')\n\
    \        use_git_timestamp = not onlinejudge_verify.utils.is_local_execution()\n\
    \        _verification_marker = VerificationMarker(json_path=timestamps_json_path,\
    \ use_git_timestamp=use_git_timestamp, jobs=jobs)\n    return _verification_marker\n\
    \n\n@functools.lru_cache(maxsize=None)\ndef _get_last_commit_time_to_verify(path:\
    \ pathlib.Path) -> datetime.datetime:\n    language = onlinejudge_verify.languages.get(path)\n\
    \    assert language is not None\n    try:\n        depending_files = language.list_dependencies(path,\
    \ basedir=_cwd())\n    except Exception:\n        traceback.print_exc()\n    \
    \    return _error_timestamp\n    code = ['git', 'log', '-1', '--date=iso', '--pretty=%ad',\
    \ '--'] + list(map(str, depending_files))\n    timestamp = subprocess.check_output(code).decode().strip()\n\
    \    if not timestamp:\n        return _error_timestamp\n    return datetime.datetime.strptime(timestamp,\
    \ '%Y-%m-%d %H:%M:%S %z')\n\n\ndef get_last_commit_time_to_verify(path: pathlib.Path)\
    \ -> datetime.datetime:\n    \"\"\"\n    :param path: should exist\n    \"\"\"\
    \n\n    return _get_last_commit_time_to_verify(path.resolve(strict=True))\n"
  dependsOn: []
  extendedDependsOn: []
  extendedRequiredBy: []
  extendedVerifiedWith: []
  isVerificationFile: false
  path: onlinejudge_verify/marker.py
  requiredBy: []
  timestamp: '1970-01-01 00:00:00+00:00'
  verificationStatus: LIBRARY_NO_TESTS
  verificationStatusIcon: ':warning:'
  verifiedWith: []
documentation_of: onlinejudge_verify/marker.py
layout: document
redirect_from:
- /library/onlinejudge_verify/marker.py
- /library/onlinejudge_verify/marker.py.html
title: onlinejudge_verify/marker.py
---
