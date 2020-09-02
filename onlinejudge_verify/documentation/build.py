import copy
import pathlib
import traceback
from logging import getLogger
from typing import *

import onlinejudge_verify.documentation.front_matter
import onlinejudge_verify.utils as utils
import pkg_resources
from onlinejudge_verify.documentation.type import *

logger = getLogger(__name__)

package = 'onlinejudge_verify_resources'
_static_files: List[Dict[str, Any]] = [
    {
        'path': pathlib.Path('_config.yml'),
        'data': pkg_resources.resource_string(package, '_config.yml'),
    },
    {
        'path': pathlib.Path('_layouts/document.html'),
        'data': pkg_resources.resource_string(package, '_layouts/document.html'),
    },
    {
        'path': pathlib.Path('_layouts/toppage.html'),
        'data': pkg_resources.resource_string(package, '_layouts/toppage.html'),
    },
    {
        'path': pathlib.Path('assets/css/copy-button.css'),
        'data': pkg_resources.resource_string(package, 'assets/css/copy-button.css'),
    },
    {
        'path': pathlib.Path('assets/js/copy-button.js'),
        'data': pkg_resources.resource_string(package, 'assets/js/copy-button.js'),
    },
    {
        'path': pathlib.Path('Gemfile'),
        'data': pkg_resources.resource_string(package, 'Gemfile'),
    },
]


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
    with open(basedir / stat.path) as fh:
        code = fh.read()
    try:
        language = onlinejudge_verify.languages.get(stat.path)
        assert language is not None
        bundled_code = language.bundle(stat.path, basedir=basedir).decode()
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


def _render_source_code_stat_for_page(path: pathlib.Path, *, source_code_stats_dict: Dict[pathlib.Path, SourceCodeStat], basedir: pathlib.Path) -> Dict[str, Any]:
    stat = source_code_stats_dict[(basedir / path).resolve()]
    data = _render_source_code_stat(stat, basedir=basedir)
    data['verificationStatusIcon'] = _get_verification_status_icon(stat.verification_status)

    def ext(path: pathlib.Path) -> Dict[str, Any]:
        stat = source_code_stats_dict[(basedir / path).resolve()]
        return {
            'path': str(path),
            'title': stat.attributes.get('document_title', str(stat.path)),
            'icon': _get_verification_status_icon(stat.verification_status),
        }

    data['extendedDependsOn'] = [ext(path) for path in stat.depends_on]
    data['extendedRequiredBy'] = [ext(path) for path in stat.required_by]
    data['extendedVerifiedWith'] = [ext(path) for path in stat.verified_with]

    return data


def _render_source_code_stats_for_top_page(*, source_code_stats: List[SourceCodeStat], basedir: pathlib.Path) -> Dict[str, Any]:
    libraryCategories: Dict[str, List[Dict[str, str]]] = {}
    verificationCategories: Dict[str, List[Dict[str, str]]] = {}
    for stat in source_code_stats:
        if utils.is_verification_file(stat.path, basedir=basedir):
            categories = verificationCategories
        else:
            categories = libraryCategories
        category = str(stat.path.parent)
        if category not in categories:
            categories[category] = []
        categories[category].append({
            'path': str(stat.path),
            'title': stat.attributes.get('document_title', str(stat.path)),
            'icon': _get_verification_status_icon(stat.verification_status),
        })

    data: Dict[str, Any] = {}
    data['libraryCategories'] = []
    for category, pages in libraryCategories.items():
        data['libraryCategories'].append({
            'name': category,
            'pages': pages,
        })
    data['verificationCategories'] = []
    for category, pages in verificationCategories.items():
        data['verificationCategories'].append({
            'name': category,
            'pages': pages,
        })
    return data


def render_pages(*, page_render_jobs: List[PageRenderJob], source_code_stats: List[SourceCodeStat], site_render_config: SiteRenderConfig) -> Dict[pathlib.Path, bytes]:
    """
    :returns: mapping from absolute paths to file contents
    """

    source_code_stats_dict = {(site_render_config.basedir / stat.path).resolve(): stat for stat in source_code_stats}

    rendered_pages: Dict[pathlib.Path, bytes] = {}
    for job in page_render_jobs:
        documentation_of = job.front_matter.get(FrontMatterItem.documentation_of.value)

        front_matter = copy.deepcopy(job.front_matter)
        if front_matter.get(FrontMatterItem.layout.value) == 'toppage':
            data = _render_source_code_stats_for_top_page(source_code_stats=source_code_stats, basedir=site_render_config.basedir)
            front_matter[FrontMatterItem.data.value] = data

        elif documentation_of is not None:
            front_matter.setdefault(FrontMatterItem.layout.value, 'document')
            data = _render_source_code_stat_for_page(pathlib.Path(documentation_of), source_code_stats_dict=source_code_stats_dict, basedir=site_render_config.basedir)
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


def list_static_files(*, site_render_config: SiteRenderConfig) -> Dict[pathlib.Path, bytes]:
    files: Dict[pathlib.Path, bytes] = {}
    for asset in _static_files:
        files[site_render_config.destination_dir / asset['path']] = asset['data']
    for src in site_render_config.static_dir.glob('**/*'):
        dst = site_render_config.destination_dir / src.relative_to(site_render_config.static_dir)
        with open(src, 'rb') as fh:
            files[dst] = fh.read()
    return files
