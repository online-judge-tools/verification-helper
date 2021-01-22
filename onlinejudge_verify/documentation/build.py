"""This module generate actual pages for given metadata. This module doesn't collect metadata to generate pages.
"""

import copy
import pathlib
import traceback
from logging import getLogger
from typing import *

import pkg_resources
import yaml

import onlinejudge_verify.documentation.front_matter
import onlinejudge_verify.languages.list
import onlinejudge_verify.utils as utils
from onlinejudge_verify.documentation.type import *

logger = getLogger(__name__)

_RESOURCE_PACKAGE = 'onlinejudge_verify_resources'
_COPIED_STATIC_FILE_PATHS: List[str] = [
    '_layouts/page.html',
    '_layouts/document.html',
    '_layouts/toppage.html',
    '_includes/mathjax.html',
    '_includes/theme_fix.html',
    '_includes/highlight.html',
    '_includes/document_header.html',
    '_includes/document_body.html',
    '_includes/document_footer.html',
    '_includes/toppage_header.html',
    '_includes/toppage_body.html',
    'assets/css/copy-button.css',
    'assets/js/copy-button.js',
    'Gemfile',
]


def _build_page_title_dict(*, page_render_jobs: List[PageRenderJob]) -> Dict[pathlib.Path, str]:
    page_title_dict: Dict[pathlib.Path, str] = {}
    for job in page_render_jobs:
        assert job.path.suffix == '.md'
        title = job.front_matter.get(FrontMatterItem.title.value)
        if title is None:
            title = str(job.path.parent / job.path.stem)
        page_title_dict[job.path] = title
        page_title_dict[job.path.parent / job.path.stem] = title
    return page_title_dict


def _get_verification_status_icon(verification_status: VerificationStatus) -> str:
    table = {
        VerificationStatus.LIBRARY_ALL_AC: ':heavy_check_mark:',
        VerificationStatus.LIBRARY_PARTIAL_AC: ':question:',
        VerificationStatus.LIBRARY_SOME_WA: ':question:',
        VerificationStatus.LIBRARY_ALL_WA: ':x:',
        VerificationStatus.LIBRARY_NO_TESTS: ':warning:',
        VerificationStatus.TEST_ACCEPTED: ':heavy_check_mark:',
        VerificationStatus.TEST_WRONG_ANSWER: ':x:',
        VerificationStatus.TEST_WAITING_JUDGE: ':warning:',
    }
    return table[verification_status]


def _render_source_code_stat(stat: SourceCodeStat, *, basedir: pathlib.Path) -> Dict[str, Any]:
    with open(basedir / stat.path, 'rb') as fh:
        code = fh.read().decode()
    try:
        language = onlinejudge_verify.languages.list.get(stat.path)
        assert language is not None
        bundled_code = language.bundle(stat.path, basedir=basedir, options={'include_paths': [basedir]}).decode()
    except Exception:
        logger.warning("failed to bundle: %s", str(stat.path))
        bundled_code = traceback.format_exc()
    return {
        'path': str(stat.path),
        'code': code,
        'bundledCode': bundled_code,
        'isVerificationFile': stat.is_verification_file,
        'verificationStatus': stat.verification_status.value,
        'timestamp': str(stat.timestamp),
        'dependsOn': [str(path) for path in stat.depends_on],
        'requiredBy': [str(path) for path in stat.required_by],
        'verifiedWith': [str(path) for path in stat.verified_with],
        'attributes': stat.attributes,
    }


def _render_source_code_stat_for_page(
    path: pathlib.Path,
    *,
    source_code_stats_dict: Dict[pathlib.Path, SourceCodeStat],
    page_title_dict: Dict[pathlib.Path, str],
    basedir: pathlib.Path,
) -> Dict[str, Any]:
    relative_path = (basedir / path).resolve().relative_to(basedir)
    stat = source_code_stats_dict[relative_path]
    data = _render_source_code_stat(stat, basedir=basedir)
    data['_pathExtension'] = path.suffix.lstrip('.')
    data['_verificationStatusIcon'] = _get_verification_status_icon(stat.verification_status)
    data['_isVerificationFailed'] = stat.verification_status in (VerificationStatus.LIBRARY_SOME_WA, VerificationStatus.LIBRARY_ALL_WA, VerificationStatus.TEST_WRONG_ANSWER)

    def ext(relative_path: pathlib.Path) -> Dict[str, Any]:
        stat = source_code_stats_dict[relative_path]
        return {
            'path': str(relative_path),
            'title': page_title_dict[relative_path],
            'icon': _get_verification_status_icon(stat.verification_status),
        }

    data['_extendedDependsOn'] = [ext(path) for path in sorted(stat.depends_on, key=str)]
    data['_extendedRequiredBy'] = [ext(path) for path in sorted(stat.required_by, key=str)]
    data['_extendedVerifiedWith'] = [ext(path) for path in sorted(stat.verified_with, key=str)]

    return data


def _render_source_code_stats_for_top_page(
    *,
    source_code_stats: List[SourceCodeStat],
    page_title_dict: Dict[pathlib.Path, str],
    basedir: pathlib.Path,
) -> Dict[str, Any]:
    library_categories: Dict[str, List[Dict[str, str]]] = {}
    verification_categories: Dict[str, List[Dict[str, str]]] = {}
    for stat in source_code_stats:
        if utils.is_verification_file(stat.path, basedir=basedir):
            categories = verification_categories
        else:
            categories = library_categories
        category = str(stat.path.parent)
        if category not in categories:
            categories[category] = []
        categories[category].append({
            'path': str(stat.path),
            'title': page_title_dict[stat.path],
            'icon': _get_verification_status_icon(stat.verification_status),
        })

    data: Dict[str, Any] = {}
    data['libraryCategories'] = []
    for category, pages in library_categories.items():
        data['libraryCategories'].append({
            'name': category,
            'pages': pages,
        })
    data['verificationCategories'] = []
    for category, pages in verification_categories.items():
        data['verificationCategories'].append({
            'name': category,
            'pages': pages,
        })
    return data


def render_pages(*, page_render_jobs: List[PageRenderJob], source_code_stats: List[SourceCodeStat], site_render_config: SiteRenderConfig) -> Dict[pathlib.Path, bytes]:
    """
    :returns: mapping from absolute paths to file contents
    """

    page_title_dict = _build_page_title_dict(page_render_jobs=page_render_jobs)
    source_code_stats_dict = {stat.path: stat for stat in source_code_stats}

    rendered_pages: Dict[pathlib.Path, bytes] = {}
    for job in page_render_jobs:
        documentation_of = job.front_matter.get(FrontMatterItem.documentation_of.value)

        front_matter = copy.deepcopy(job.front_matter)
        if front_matter.get(FrontMatterItem.layout.value) == 'toppage':
            data = _render_source_code_stats_for_top_page(source_code_stats=source_code_stats, page_title_dict=page_title_dict, basedir=site_render_config.basedir)
            front_matter[FrontMatterItem.data.value] = data

        elif documentation_of is not None:
            front_matter.setdefault(FrontMatterItem.layout.value, 'document')
            data = _render_source_code_stat_for_page(pathlib.Path(documentation_of), source_code_stats_dict=source_code_stats_dict, page_title_dict=page_title_dict, basedir=site_render_config.basedir)
            front_matter.setdefault(FrontMatterItem.data.value, data)

        path = site_render_config.destination_dir / job.path
        content = onlinejudge_verify.documentation.front_matter.merge_front_matter(front_matter, job.content)
        rendered_pages[path] = content

    return rendered_pages


def render_source_code_stats(*, source_code_stats: List[SourceCodeStat], basedir: pathlib.Path) -> List[Dict[str, Any]]:
    data: List[Dict[str, Any]] = []
    for stat in source_code_stats:
        data.append(_render_source_code_stat(stat, basedir=basedir))
    return data


def load_static_files(*, site_render_config: SiteRenderConfig) -> Dict[pathlib.Path, bytes]:
    files: Dict[pathlib.Path, bytes] = {}

    # write merged config.yml
    files[site_render_config.destination_dir / '_config.yml'] = yaml.safe_dump(site_render_config.config_yml).encode()

    # load files in onlinejudge_verify_resources/
    for path in _COPIED_STATIC_FILE_PATHS:
        files[site_render_config.destination_dir / pathlib.Path(path)] = pkg_resources.resource_string(_RESOURCE_PACKAGE, path)

    # overwrite with docs/static
    for src in site_render_config.static_dir.glob('**/*'):
        if src.is_file():
            dst = site_render_config.destination_dir / src.relative_to(site_render_config.static_dir)
            with open(src, 'rb') as fh:
                files[dst] = fh.read()
    return files
