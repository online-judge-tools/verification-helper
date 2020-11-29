import json
import pathlib
from logging import getLogger
from typing import *

import pkg_resources
import yaml

import onlinejudge_verify.documentation.build as build
import onlinejudge_verify.documentation.configure as configure
import onlinejudge_verify.marker
from onlinejudge_verify.documentation.type import *

logger = getLogger(__name__)

_RESOURCE_PACKAGE = 'onlinejudge_verify_resources'
_CONFIG_YML_PATH: str = '_config.yml'


def print_stats_json(*, jobs: int = 1) -> None:
    basedir = pathlib.Path.cwd()
    logger.info('load verification status...')
    marker = onlinejudge_verify.marker.get_verification_marker(jobs=jobs)

    logger.info('collect source code statistics...')
    source_code_stats = configure.generate_source_code_stats(basedir=basedir, marker=marker)
    logger.info('dump to json...')
    data = build.render_source_code_stats(source_code_stats=source_code_stats, basedir=basedir)
    print(json.dumps(data))


def load_render_config(*, basedir: pathlib.Path) -> SiteRenderConfig:
    # load default _config.yml
    default_config_yml = yaml.safe_load(pkg_resources.resource_string(_RESOURCE_PACKAGE, _CONFIG_YML_PATH))
    assert default_config_yml is not None
    config_yml = default_config_yml

    # merge user's _config.yml
    user_config_yml_path = pathlib.Path('.verify-helper', 'docs', '_config.yml')
    if user_config_yml_path.exists():
        try:
            with open(user_config_yml_path, 'rb') as fh:
                user_config_yml = yaml.safe_load(fh.read())
            assert user_config_yml is not None
        except Exception as e:
            logger.exception('failed to parse .verify-helper/docs/_config.yml: %s', e)
        else:
            config_yml.update(user_config_yml)

    return SiteRenderConfig(
        basedir=basedir,
        static_dir=pathlib.Path('.verify-helper', 'docs', 'static').resolve(),
        config_yml=config_yml,
        index_md=pathlib.Path('.verify-helper', 'docs', 'index.md').resolve(),
        destination_dir=pathlib.Path('.verify-helper', 'markdown').resolve(),
    )


# TODO: この configure.py + build.py というファイル分割そこまでうまくはいってなくないか？ もうすこし整理したい
def main(*, jobs: int = 1) -> None:
    basedir = pathlib.Path.cwd()
    config = load_render_config(basedir=basedir)
    logger.info('load verification status...')
    marker = onlinejudge_verify.marker.get_verification_marker(jobs=jobs)

    # configure
    logger.info('collect source code statistics...')
    source_code_stats = configure.generate_source_code_stats(basedir=basedir, marker=marker)
    logger.info('list markdown files...')
    markdown_paths = configure.find_markdown_paths(basedir=basedir)
    logger.info('list rendering jobs...')
    excluded_paths = list(map(pathlib.Path, config.config_yml.get('exclude', [])))
    source_code_stats = configure.apply_exclude_list_to_stats(excluded_paths=excluded_paths, source_code_stats=source_code_stats)
    markdown_paths = configure.apply_exclude_list_to_paths(markdown_paths, excluded_paths=excluded_paths)
    render_jobs = configure.convert_to_page_render_jobs(source_code_stats=source_code_stats, markdown_paths=markdown_paths, site_render_config=config)

    # make build
    logger.info('render %s files...', len(render_jobs))
    rendered_pages = build.render_pages(page_render_jobs=render_jobs, source_code_stats=source_code_stats, site_render_config=config)
    logger.info('list static files...')
    static_files = build.load_static_files(site_render_config=config)

    # make install
    logger.info('writing %s files...', len(rendered_pages))
    for path, content in rendered_pages.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'wb') as fh:
            fh.write(content)
    logger.info('writing %s static files...', len(static_files))
    for path, content in static_files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'wb') as fh:
            fh.write(content)
