---
data:
  _extendedDependsOn: []
  _extendedRequiredBy: []
  _extendedVerifiedWith: []
  _pathExtension: py
  _verificationStatusIcon: ':warning:'
  attributes:
    links: []
  bundledCode: "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/documentation/build.py\"\
    , line 70, in _render_source_code_stat\n    bundled_code = language.bundle(stat.path,\
    \ basedir=basedir).decode()\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/languages/python.py\"\
    , line 84, in bundle\n    raise NotImplementedError\nNotImplementedError\n"
  code: "import json\nimport pathlib\nfrom logging import getLogger\nfrom typing import\
    \ *\n\nimport onlinejudge_verify.documentation.build as build\nimport onlinejudge_verify.documentation.configure\
    \ as configure\nimport onlinejudge_verify.marker\nimport pkg_resources\nimport\
    \ yaml\nfrom onlinejudge_verify.documentation.type import *\n\nlogger = getLogger(__name__)\n\
    \n_resource_package = 'onlinejudge_verify_resources'\n_config_yml_path: str =\
    \ '_config.yml'\n\n\ndef print_stats_json(*, jobs: int = 1) -> None:\n    basedir\
    \ = pathlib.Path.cwd()\n    logger.info('load verification status...')\n    marker\
    \ = onlinejudge_verify.marker.get_verification_marker(jobs=jobs)\n\n    logger.info('collect\
    \ source code statistics...')\n    source_code_stats = configure.generate_source_code_stats(basedir=basedir,\
    \ marker=marker)\n    logger.info('dump to json...')\n    data = build.render_source_code_stats(source_code_stats=source_code_stats,\
    \ basedir=basedir)\n    print(json.dumps(data))\n\n\ndef load_render_config(*,\
    \ basedir: pathlib.Path) -> SiteRenderConfig:\n    # load default _config.yml\n\
    \    default_config_yml = yaml.safe_load(pkg_resources.resource_string(_resource_package,\
    \ _config_yml_path))\n    assert default_config_yml is not None\n    config_yml\
    \ = default_config_yml\n\n    # merge user's _config.yml\n    user_config_yml_path\
    \ = pathlib.Path('.verify-helper', 'docs', '_config.yml')\n    if user_config_yml_path.exists():\n\
    \        try:\n            with open(user_config_yml_path, 'rb') as fh:\n    \
    \            user_config_yml = yaml.safe_load(fh.read())\n            assert user_config_yml\
    \ is not None\n        except Exception as e:\n            logger.exception('failed\
    \ to parse .verify-helper/docs/_config.yml: %s', e)\n        else:\n         \
    \   config_yml.update(user_config_yml)\n\n    return SiteRenderConfig(\n     \
    \   basedir=basedir,\n        static_dir=pathlib.Path('.verify-helper', 'docs',\
    \ 'static').resolve(),\n        config_yml=config_yml,\n        index_md=pathlib.Path('.verify-helper',\
    \ 'docs', 'index.md').resolve(),\n        destination_dir=pathlib.Path('.verify-helper',\
    \ 'markdown').resolve(),\n    )\n\n\n# TODO: \u3053\u306E configure.py + build.py\
    \ \u3068\u3044\u3046\u30D5\u30A1\u30A4\u30EB\u5206\u5272\u305D\u3053\u307E\u3067\
    \u3046\u307E\u304F\u306F\u3044\u3063\u3066\u306A\u304F\u306A\u3044\u304B\uFF1F\
    \ \u3082\u3046\u3059\u3053\u3057\u6574\u7406\u3057\u305F\u3044\ndef main(*, jobs:\
    \ int = 1) -> None:\n    basedir = pathlib.Path.cwd()\n    config = load_render_config(basedir=basedir)\n\
    \    logger.info('load verification status...')\n    marker = onlinejudge_verify.marker.get_verification_marker(jobs=jobs)\n\
    \n    # configure\n    logger.info('collect source code statistics...')\n    source_code_stats\
    \ = configure.generate_source_code_stats(basedir=basedir, marker=marker)\n   \
    \ logger.info('list markdown files...')\n    markdown_paths = configure.find_markdown_paths(basedir=basedir)\n\
    \    logger.info('list rendering jobs...')\n    excluded_paths = list(map(pathlib.Path,\
    \ config.config_yml.get('exclude', [])))\n    source_code_stats = configure.apply_exclude_list_to_stats(excluded_paths=excluded_paths,\
    \ source_code_stats=source_code_stats)\n    markdown_paths = configure.apply_exclude_list_to_paths(markdown_paths,\
    \ excluded_paths=excluded_paths)\n    render_jobs = configure.convert_to_page_render_jobs(source_code_stats=source_code_stats,\
    \ markdown_paths=markdown_paths, site_render_config=config)\n\n    # make build\n\
    \    logger.info('render %s files...', len(render_jobs))\n    rendered_pages =\
    \ build.render_pages(page_render_jobs=render_jobs, source_code_stats=source_code_stats,\
    \ site_render_config=config)\n    logger.info('list static files...')\n    static_files\
    \ = build.load_static_files(site_render_config=config)\n\n    # make install\n\
    \    logger.info('writing %s files...', len(rendered_pages))\n    for path, content\
    \ in rendered_pages.items():\n        path.parent.mkdir(parents=True, exist_ok=True)\n\
    \        with open(path, 'wb') as fh:\n            fh.write(content)\n    logger.info('writing\
    \ %s static files...', len(static_files))\n    for path, content in static_files.items():\n\
    \        path.parent.mkdir(parents=True, exist_ok=True)\n        with open(path,\
    \ 'wb') as fh:\n            fh.write(content)\n"
  dependsOn: []
  isVerificationFile: false
  path: onlinejudge_verify/documentation/main.py
  requiredBy: []
  timestamp: '1970-01-01 00:00:00+00:00'
  verificationStatus: LIBRARY_NO_TESTS
  verifiedWith: []
documentation_of: onlinejudge_verify/documentation/main.py
layout: document
redirect_from:
- /library/onlinejudge_verify/documentation/main.py
- /library/onlinejudge_verify/documentation/main.py.html
title: onlinejudge_verify/documentation/main.py
---
