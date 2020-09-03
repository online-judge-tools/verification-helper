import json
import pathlib
from logging import getLogger
from typing import *

import onlinejudge_verify.documentation.build as build
import onlinejudge_verify.documentation.configure as configure
import onlinejudge_verify.marker
from onlinejudge_verify.documentation.type import *

logger = getLogger(__name__)


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
    return SiteRenderConfig(
        basedir=basedir,
        static_dir=pathlib.Path('.verify-helper', 'docs', 'static').resolve(),
        config_yml=pathlib.Path('.verify-helper', 'docs', '_config.yml').resolve(),
        destination_dir=pathlib.Path('.verify-helper', 'markdown').resolve(),
    )


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
    render_jobs = configure.convert_to_page_render_jobs(source_code_stats=source_code_stats, markdown_paths=markdown_paths, basedir=basedir)

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
