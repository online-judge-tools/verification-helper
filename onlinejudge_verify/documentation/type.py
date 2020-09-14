import datetime
import enum
import pathlib
from typing import *


class VerificationStatus(enum.Enum):
    LIBRARY_ALL_AC = 'LIBRARY_ALL_AC'
    LIBRARY_PARTIAL_AC = 'LIBRARY_PARTIAL_AC'
    LIBRARY_SOME_WA = 'LIBRARY_SOME_WA'
    LIBRARY_ALL_WA = 'LIBRARY_ALL_WA'
    LIBRARY_NO_TESTS = 'LIBRARY_NO_TESTS'
    TEST_ACCEPTED = 'TEST_ACCEPTED'
    TEST_WRONG_ANSWER = 'TEST_WRONG_ANSWER'
    TEST_WAITING_JUDGE = 'TEST_WAITING_JUDGE'


class SourceCodeStat(NamedTuple):
    """A tuple represents a code file.
    """
    path: pathlib.Path  # a relative path from basedir
    is_verification_file: bool
    verification_status: VerificationStatus
    timestamp: datetime.datetime  # the same format to timestamps.*.json
    depends_on: List[pathlib.Path]  # relative paths from basedir
    required_by: List[pathlib.Path]  # relative paths from basedir
    verified_with: List[pathlib.Path]  # relative paths from basedir
    attributes: Dict[str, Any]


class FrontMatterItem(enum.Enum):
    title = 'title'
    layout = 'layout'
    documentation_of = 'documentation_of'
    data = 'data'
    redirect_from = 'redirect_from'  # for jekyll-redirect-from plugin


class PageRenderJob(NamedTuple):
    path: pathlib.Path  # a relative path from basedir
    front_matter: Dict[str, Any]
    content: bytes


class SiteRenderConfig(NamedTuple):
    basedir: pathlib.Path  # an absolute path
    config_yml: Dict[str, Any]
    static_dir: pathlib.Path  # an absolute path
    index_md: pathlib.Path  # an absolute path
    destination_dir: pathlib.Path  # an absolute path
