import pathlib
from logging import getLogger
from typing import *

import onlinejudge_verify.documentation.front_matter
import onlinejudge_verify.languages
import onlinejudge_verify.utils as utils
from onlinejudge_verify.documentation.type import *
from onlinejudge_verify.marker import VerificationMarker

logger = getLogger(__name__)


def _find_matched_file_paths(pred: Callable[[pathlib.Path], bool], *, basedir: pathlib.Path) -> List[pathlib.Path]:
    found: List[pathlib.Path] = []

    def dfs(x: pathlib.Path) -> None:
        for y in x.iterdir():
            if y.name.startswith('.'):
                continue
            if y.is_dir():
                dfs(y)
            else:
                if pred(y):
                    found.append(y)

    dfs(basedir)
    return found


def find_source_code_paths(*, basedir: pathlib.Path) -> List[pathlib.Path]:
    def pred(path: pathlib.Path) -> bool:
        return onlinejudge_verify.languages.get(path) is not None

    return _find_matched_file_paths(pred, basedir=basedir)


def find_markdown_paths(*, basedir: pathlib.Path) -> List[pathlib.Path]:
    # This list is the same to GitHub. see https://github.com/github/markup/blob/b865add2e053f8cea3d7f4d9dcba001bdfd78994/lib/github/markups.rb#L1
    markdown_suffixes = ('.md', '.mkd', '.mkdn', '.mdown', '.markdown')

    def pred(path: pathlib.Path) -> bool:
        return path.suffix in markdown_suffixes

    return _find_matched_file_paths(pred, basedir=basedir)


def build_dependency_graph(paths: List[pathlib.Path], *, basedir: pathlib.Path) -> Tuple[Dict[pathlib.Path, List[pathlib.Path]], Dict[pathlib.Path, List[pathlib.Path]], Dict[pathlib.Path, List[pathlib.Path]]]:
    """
    :returns: graphs from absolute paths to relative paths
    """
    depends_on: Dict[pathlib.Path, List[pathlib.Path]] = {}
    required_by: Dict[pathlib.Path, List[pathlib.Path]] = {}
    verified_with: Dict[pathlib.Path, List[pathlib.Path]] = {}

    # initialize
    for path in paths:
        absolute_path = (basedir / path).resolve()
        depends_on[absolute_path] = []
        required_by[absolute_path] = []
        verified_with[absolute_path] = []

    # build the graph
    for src in paths:
        absolute_src = (basedir / src).resolve()
        relative_src = absolute_src.relative_to(basedir)  # all paths must be in the git repository
        language = onlinejudge_verify.languages.get(src)
        assert language is not None

        for dst in language.list_dependencies(src, basedir=basedir):
            absolute_dst = (basedir / dst).resolve()
            relative_dst = absolute_dst.relative_to(basedir)
            if absolute_src == absolute_dst:
                continue

            depends_on[absolute_src].append(relative_dst)
            if utils.is_verification_file(absolute_dst, basedir=basedir):
                verified_with[absolute_dst].append(relative_src)
            else:
                required_by[absolute_dst].append(relative_src)

    return depends_on, required_by, verified_with


def build_verification_status(paths: List[pathlib.Path], *, depends_on: Dict[pathlib.Path, List[pathlib.Path]], basedir: pathlib.Path, marker: VerificationMarker) -> Dict[pathlib.Path, VerificationStatus]:
    """
    :returns: mapping from absolute paths to verification status
    """
    verification_status: Dict[pathlib.Path, VerificationStatus] = {}

    # list status for verification files
    for path in paths:
        absolute_path = (basedir / path).resolve()
        if utils.is_verification_file(path, basedir=basedir):
            if marker.is_verified(path):
                status = VerificationStatus.TEST_ACCEPTED
            elif marker.is_failed(path):
                status = VerificationStatus.TEST_WRONG_ANSWER
            else:
                status = VerificationStatus.TEST_WAITING_JUDGE
            verification_status[absolute_path] = status

    # list status for library files
    for path in paths:
        absolute_path = (basedir / path).resolve()
        if not utils.is_verification_file(path, basedir=basedir):
            status_list = []
            for verification_path in depends_on[absolute_path]:
                if utils.is_verification_file(verification_path, basedir=basedir):
                    status_list.append(verification_status[(basedir / verification_path).resolve()])
            if not status_list:
                status = VerificationStatus.LIBRARY_NO_TESTS
            elif status_list.count(VerificationStatus.TEST_ACCEPTED) == len(status_list):
                status = VerificationStatus.LIBRARY_ALL_AC
            elif status_list.count(VerificationStatus.TEST_WRONG_ANSWER) == len(status_list):
                status = VerificationStatus.LIBRARY_ALL_WA
            elif VerificationStatus.TEST_WRONG_ANSWER in status_list:
                status = VerificationStatus.LIBRARY_SOME_WA
            else:
                status = VerificationStatus.LIBRARY_PARTIAL_AC
            verification_status[absolute_path] = status

    return verification_status


def get_source_code_stat(
        path: pathlib.Path,
        *,
        depends_on: Dict[pathlib.Path, List[pathlib.Path]],
        required_by: Dict[pathlib.Path, List[pathlib.Path]],
        verified_with: Dict[pathlib.Path, List[pathlib.Path]],
        verification_status: Dict[pathlib.Path, VerificationStatus],
        marker: VerificationMarker,
        basedir: pathlib.Path,
) -> SourceCodeStat:
    absolute_path = (basedir / path).resolve()
    relative_path = absolute_path.relative_to(basedir)
    language = onlinejudge_verify.languages.get(path)
    assert language is not None

    is_verification_file = language.is_verification_file(path, basedir=basedir)
    timestamp = marker.get_current_timestamp(path)
    attributes = language.list_attributes(path, basedir=basedir)

    return SourceCodeStat(
        path=relative_path,
        is_verification_file=is_verification_file,
        verification_status=verification_status[absolute_path],
        timestamp=timestamp,
        depends_on=depends_on[absolute_path],
        verified_with=verified_with[absolute_path],
        required_by=required_by[absolute_path],
        attributes=attributes,
    )


def generate_source_code_stats(*, marker: VerificationMarker, basedir: pathlib.Path) -> List[SourceCodeStat]:
    source_code_paths = find_source_code_paths(basedir=basedir)
    depends_on, required_by, verified_with = build_dependency_graph(source_code_paths, basedir=basedir)
    verification_status = build_verification_status(source_code_paths, depends_on=depends_on, basedir=basedir, marker=marker)
    source_code_stats: List[SourceCodeStat] = []
    for path in source_code_paths:
        stat = get_source_code_stat(
            path,
            depends_on=depends_on,
            required_by=required_by,
            verified_with=verified_with,
            verification_status=verification_status,
            marker=marker,
            basedir=basedir,
        )
        source_code_stats.append(stat)
    return sorted(source_code_stats, key=lambda stat: stat.path)


def convert_to_page_render_jobs(*, source_code_stats: List[SourceCodeStat], markdown_paths: List[pathlib.Path], basedir: pathlib.Path) -> List[PageRenderJob]:
    page_render_jobs: List[PageRenderJob] = []

    for stat in source_code_stats:
        path = stat.path.parent / (stat.path.name + '.md')
        front_matter: Dict[str, Any] = {}
        front_matter[FrontMatterItem.title.value] = str(stat.path)
        front_matter[FrontMatterItem.documentation_of.value] = str(stat.path)
        job = PageRenderJob(
            path=path,
            front_matter=front_matter,
            content=b'',
        )
        page_render_jobs.append(job)

    for markdown_path in markdown_paths:
        markdown_absolute_path = (basedir / markdown_path).resolve()
        markdown_relative_path = markdown_absolute_path.relative_to(basedir)
        with open(markdown_path, 'rb') as fh:
            content = fh.read()
        front_matter, content = onlinejudge_verify.documentation.front_matter.split_front_matter(content)
        job = PageRenderJob(
            path=markdown_path,
            front_matter=front_matter,
            content=content,
        )
        page_render_jobs.append(job)

    if all([job.path != pathlib.Path('index.md') for job in page_render_jobs]):
        job = PageRenderJob(
            path=pathlib.Path('index.md'),
            front_matter={
                'layout': 'toppage',
            },
            content=b'',
        )
        page_render_jobs.append(job)

    return page_render_jobs
