"""This module collects metadata required to generate pages. This module doesn't generate actual pages.
"""

import pathlib
from logging import getLogger
from typing import *

import onlinejudge_verify.documentation.front_matter
import onlinejudge_verify.languages.list
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


def _find_source_code_paths(*, basedir: pathlib.Path) -> List[pathlib.Path]:
    def pred(path: pathlib.Path) -> bool:
        return onlinejudge_verify.languages.list.get(path) is not None

    return _find_matched_file_paths(pred, basedir=basedir)


def find_markdown_paths(*, basedir: pathlib.Path) -> List[pathlib.Path]:
    def pred(path: pathlib.Path) -> bool:
        return path.suffix == '.md'

    return _find_matched_file_paths(pred, basedir=basedir)


def _build_dependency_graph(paths: List[pathlib.Path], *, basedir: pathlib.Path) -> Tuple[Dict[pathlib.Path, List[pathlib.Path]], Dict[pathlib.Path, List[pathlib.Path]], Dict[pathlib.Path, List[pathlib.Path]]]:
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
        language = onlinejudge_verify.languages.list.get(src)
        assert language is not None

        try:
            dependencies = language.list_dependencies(src, basedir=basedir)
        except Exception as e:
            logger.exception('failed to list dependencies of %s: %s', str(relative_src), e)
            continue

        for dst in dependencies:
            absolute_dst = (basedir / dst).resolve()
            relative_dst = absolute_dst.relative_to(basedir)
            if absolute_src == absolute_dst:
                continue
            if absolute_dst not in depends_on:
                logger.debug("The file `%s` which is depended from `%s` is ignored because it's not listed as a source code file.", relative_dst, relative_src)
                continue

            depends_on[absolute_src].append(relative_dst)
            if utils.is_verification_file(src, basedir=basedir):
                verified_with[absolute_dst].append(relative_src)
            else:
                required_by[absolute_dst].append(relative_src)

    return depends_on, required_by, verified_with


def _build_verification_status(paths: List[pathlib.Path], *, verified_with: Dict[pathlib.Path, List[pathlib.Path]], basedir: pathlib.Path, marker: VerificationMarker) -> Dict[pathlib.Path, VerificationStatus]:
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
            for verification_path in verified_with[absolute_path]:
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


def _get_source_code_stat(
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
    language = onlinejudge_verify.languages.list.get(path)
    assert language is not None

    is_verification_file = language.is_verification_file(path, basedir=basedir)
    timestamp = marker.get_current_timestamp(path)
    try:
        attributes = language.list_attributes(path, basedir=basedir)
    except Exception as e:
        logger.exception('failed to list attributes of %s: %s', str(relative_path), e)
        attributes = {}

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
    source_code_paths = _find_source_code_paths(basedir=basedir)
    depends_on, required_by, verified_with = _build_dependency_graph(source_code_paths, basedir=basedir)
    verification_status = _build_verification_status(source_code_paths, verified_with=verified_with, basedir=basedir, marker=marker)
    source_code_stats: List[SourceCodeStat] = []
    for path in source_code_paths:
        stat = _get_source_code_stat(
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


def is_excluded(relative_path: pathlib.Path, *, excluded_paths: List[pathlib.Path]) -> bool:
    for excluded in excluded_paths:
        if relative_path == excluded or excluded in relative_path.parents:
            return True
    return False


def apply_exclude_list_to_paths(paths: List[pathlib.Path], *, excluded_paths: List[pathlib.Path]) -> List[pathlib.Path]:
    return [path for path in paths if not is_excluded(path, excluded_paths=excluded_paths)]


def apply_exclude_list_to_stats(*, excluded_paths: List[pathlib.Path], source_code_stats: List[SourceCodeStat]) -> List[SourceCodeStat]:
    result = []
    for stat in source_code_stats:
        if is_excluded(stat.path, excluded_paths=excluded_paths):
            continue
        stat = SourceCodeStat(
            path=stat.path,
            is_verification_file=stat.is_verification_file,
            timestamp=stat.timestamp,
            depends_on=apply_exclude_list_to_paths(stat.depends_on, excluded_paths=excluded_paths),
            required_by=apply_exclude_list_to_paths(stat.required_by, excluded_paths=excluded_paths),
            verified_with=apply_exclude_list_to_paths(stat.verified_with, excluded_paths=excluded_paths),
            verification_status=stat.verification_status,
            attributes=stat.attributes,
        )
        result.append(stat)
    return result


def resolve_documentation_of(documentation_of: str, *, markdown_path: pathlib.Path, basedir: pathlib.Path) -> Optional[pathlib.Path]:
    if documentation_of.startswith('.'):
        # a relative path
        path = markdown_path.parent / pathlib.Path(pathlib.PurePosixPath(documentation_of))
        if path.exists() and basedir in path.resolve().parents:
            return path
    elif documentation_of.startswith('//'):
        # from the document root
        path = basedir / pathlib.Path(pathlib.PurePosixPath(documentation_of[2:]))
        if path.exists() and basedir in path.resolve().parents:
            return path

    # guessing
    logger.warning('No file at the expected path from the `documentation_of` path. The `documentation_of` path should use `/` for path separator, and start with `.` for a relative path from the path of the Markdown file, or start with `//` for a absolute path from the root of the repository.: %s', documentation_of)
    candidate_paths = [
        basedir / pathlib.Path(pathlib.PurePosixPath(documentation_of)),
        basedir / pathlib.Path(documentation_of),
        markdown_path.parent / pathlib.Path(pathlib.PurePosixPath(documentation_of)),
        markdown_path.parent / pathlib.Path(documentation_of),
    ]
    for path in candidate_paths:
        if path.exists() and basedir in path.resolve().parents:
            return path
    return None


def convert_to_page_render_jobs(*, source_code_stats: List[SourceCodeStat], markdown_paths: List[pathlib.Path], site_render_config: SiteRenderConfig) -> List[PageRenderJob]:
    basedir = site_render_config.basedir

    page_render_jobs: Dict[pathlib.Path, PageRenderJob] = {}

    # Markdown pages
    for markdown_path in markdown_paths:
        markdown_absolute_path = (basedir / markdown_path).resolve()
        markdown_relative_path = markdown_absolute_path.relative_to(basedir)

        with open(markdown_path, 'rb') as fh:
            content = fh.read()
        front_matter, content = onlinejudge_verify.documentation.front_matter.split_front_matter(content)

        # move the location if documentation_of field exists
        path = markdown_relative_path
        documentation_of = front_matter.get(FrontMatterItem.documentation_of.value)
        if documentation_of is not None:
            documentation_of_path = resolve_documentation_of(documentation_of, markdown_path=path, basedir=basedir)
            if documentation_of_path is None:
                logger.warning('the `documentation_of` path of %s is not found: %s', str(path), documentation_of)
                del front_matter[FrontMatterItem.documentation_of.value]
                continue
            documentation_of_relative_path = documentation_of_path.resolve().relative_to(basedir)
            front_matter[FrontMatterItem.documentation_of.value] = str(documentation_of_relative_path)
            path = documentation_of_relative_path.parent / (documentation_of_path.name + '.md')

        job = PageRenderJob(
            path=path,
            front_matter=front_matter,
            content=content,
        )
        page_render_jobs[job.path] = job

    # API pages
    for stat in source_code_stats:
        path = stat.path.parent / (stat.path.name + '.md')
        if path in page_render_jobs:
            continue

        front_matter = {}
        front_matter[FrontMatterItem.documentation_of.value] = str(stat.path)

        # add redirects from old URLs
        old_directory = 'verify' if stat.is_verification_file else 'library'
        front_matter[FrontMatterItem.redirect_from.value] = [
            '/' + str(pathlib.Path(old_directory) / stat.path),
            '/' + str(pathlib.Path(old_directory) / stat.path.parent / (stat.path.name + '.html')),
        ]

        # add title specified as a attributes like @title or @brief
        front_matter[FrontMatterItem.title.value] = str(stat.path)
        if 'document_title' in stat.attributes:
            front_matter[FrontMatterItem.title.value] = stat.attributes['document_title']

        # treat @docs path/to.md directives
        content = b''
        if '_deprecated_at_docs' in stat.attributes:
            at_docs_path = pathlib.Path(stat.attributes['_deprecated_at_docs'])
            try:
                with open(at_docs_path, 'rb') as fh:
                    content = fh.read()
            except FileNotFoundError as e:
                logger.exception('failed to read markdown file specified by @docs in %s: %s', str(stat.path), e)

        job = PageRenderJob(
            path=path,
            front_matter=front_matter,
            content=content,
        )
        page_render_jobs[job.path] = job

    # top page
    if pathlib.Path('index.md') not in page_render_jobs:
        content = b''
        if site_render_config.index_md.exists():
            with site_render_config.index_md.open('rb') as fh:
                content = fh.read()
        job = PageRenderJob(
            path=pathlib.Path('index.md'),
            front_matter={
                'layout': 'toppage',
            },
            content=content,
        )
        page_render_jobs[job.path] = job

    return list(page_render_jobs.values())
