# Python Version: 3.x
import concurrent.futures
import datetime
import functools
import json
import os
import pathlib
import shlex
import subprocess
from typing import *

import onlinejudge_verify.languages


class VerificationMarker(object):
    json_path: pathlib.Path
    use_git_timestamp: bool
    old_timestamps: Dict[pathlib.Path, datetime.datetime]
    new_timestamps: Dict[pathlib.Path, datetime.datetime]
    verification_statuses: Dict[pathlib.Path, str]

    def __init__(self, *, json_path: pathlib.Path, use_git_timestamp: bool, jobs: Optional[int] = None) -> None:
        self.json_path = json_path
        self.use_git_timestamp = use_git_timestamp
        self.verification_statuses = {}
        self.load_timestamps(jobs=jobs)

    def get_current_timestamp(self, path: pathlib.Path) -> datetime.datetime:
        if self.use_git_timestamp:
            return get_last_commit_time_to_verify(path)
        else:
            language = onlinejudge_verify.languages.get(path)
            assert language is not None
            timestamp = max([x.stat().st_mtime for x in language.list_dependencies(path, basedir=pathlib.Path.cwd())])
            system_local_timezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
            return datetime.datetime.fromtimestamp(timestamp, tz=system_local_timezone).replace(microsecond=0)  # microsecond=0 is required because it's erased on timestamps.*.json

    def is_verified(self, path: pathlib.Path) -> bool:
        path = path.resolve().relative_to(pathlib.Path.cwd())
        return self.verification_statuses.get(path) == 'verified'

    def mark_verified(self, path: pathlib.Path) -> None:
        path = path.resolve().relative_to(pathlib.Path.cwd())
        self.new_timestamps[path] = self.get_current_timestamp(path)
        self.verification_statuses[path] = 'verified'

    def is_failed(self, path: pathlib.Path) -> bool:
        path = path.resolve().relative_to(pathlib.Path.cwd())
        if path not in self.verification_statuses:
            # verifiedの場合は必ずself.verification_status[path] == 'verified'となるのでこのifの中には入らない
            # それ以外の場合は「そもそもテストを実行していない」可能性もあるが一旦はfailedとみなす
            return True
        return self.verification_statuses[path] == 'failed'

    def mark_failed(self, path: pathlib.Path) -> None:
        path = path.resolve().relative_to(pathlib.Path.cwd())
        self.verification_statuses[path] = 'failed'

    def load_timestamps(self, *, jobs: Optional[int] = None) -> None:
        # 古いものを読み込む
        self.old_timestamps = {}
        if self.json_path.exists():
            with open(str(self.json_path)) as fh:
                data = json.load(fh)
            for path, timestamp in data.items():
                if path == '~' and timestamp == 'dummy':  # for backward compatibility
                    continue
                self.old_timestamps[pathlib.Path(path)] = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S %z')

        # 新しいものに移す
        self.new_timestamps = {}

        def load(path, timestamp):
            if path.exists() and self.get_current_timestamp(path) <= timestamp:
                self.mark_verified(path)
                return
            #「そもそもテストを実行していない」のか「実行した上で失敗した」のか区別できないが、verifyできてない事には変わりないので一旦はfailedとみなす
            self.mark_failed(path)
            if path.exists():
                # 過去にverifyされたことがある場合は、最終verify時刻を引き継ぐ
                self.new_timestamps[path] = timestamp

        if jobs is None:
            for path, timestamp in self.old_timestamps.items():
                load(path, timestamp)
        else:
            # TODO: ここ (実質 VerificationMarker.__init__) が遅いのなんだかおかしくないか？ verify時刻が古いものの処理とかは別でやるべきな気がする
            # 依存先ファイルの解析などがあって遅いので並列でやる
            with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as executor:
                for path, timestamp in self.old_timestamps.items():
                    executor.submit(load, path, timestamp)

    def save_timestamps(self) -> None:
        if self.old_timestamps == self.new_timestamps:
            return
        data = {}
        for path, timestamp in self.new_timestamps.items():
            data[str(path)] = timestamp.strftime('%Y-%m-%d %H:%M:%S %z')
        with open(str(self.json_path), 'w') as fh:
            json.dump(data, fh, sort_keys=True, indent=0)

    def __enter__(self) -> 'VerificationMarker':
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.save_timestamps()


_verification_marker = None  # type: Optional[VerificationMarker]


def get_verification_marker(*, jobs: Optional[int] = None) -> VerificationMarker:
    global _verification_marker
    if _verification_marker is None:
        # use different files in local and in remote to avoid conflicts
        if 'GITHUB_ACTION' in os.environ:
            timestamps_json_path = pathlib.Path('.verify-helper/timestamps.remote.json')
        else:
            timestamps_json_path = pathlib.Path('.verify-helper/timestamps.local.json')
        use_git_timestamp = 'GITHUB_ACTION' in os.environ
        _verification_marker = VerificationMarker(json_path=timestamps_json_path, use_git_timestamp=use_git_timestamp, jobs=jobs)
    return _verification_marker


@functools.lru_cache(maxsize=None)
def _get_last_commit_time_to_verify(path: pathlib.Path) -> datetime.datetime:
    language = onlinejudge_verify.languages.get(path)
    assert language is not None
    depending_files = language.list_dependencies(path, basedir=pathlib.Path.cwd())
    code = ['git', 'log', '-1', '--date=iso', '--pretty=%ad', '--'] + list(map(lambda x: shlex.quote(str(x)), depending_files))
    timestamp = subprocess.check_output(code).decode().strip()
    if not timestamp:
        return datetime.datetime.fromtimestamp(0)
    return datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S %z')


def get_last_commit_time_to_verify(path: pathlib.Path) -> datetime.datetime:
    return _get_last_commit_time_to_verify(path.resolve())
