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
  code: "\"\"\"This module collects metadata required to generate pages. This module\
    \ doesn't generate actual pages.\n\"\"\"\n\nimport pathlib\nfrom logging import\
    \ getLogger\nfrom typing import *\n\nimport onlinejudge_verify.documentation.front_matter\n\
    import onlinejudge_verify.languages.list\nimport onlinejudge_verify.utils as utils\n\
    from onlinejudge_verify.documentation.type import *\nfrom onlinejudge_verify.marker\
    \ import VerificationMarker\n\nlogger = getLogger(__name__)\n\n\ndef _find_matched_file_paths(pred:\
    \ Callable[[pathlib.Path], bool], *, basedir: pathlib.Path) -> List[pathlib.Path]:\n\
    \    found: List[pathlib.Path] = []\n\n    def dfs(x: pathlib.Path) -> None:\n\
    \        for y in x.iterdir():\n            if y.name.startswith('.'):\n     \
    \           continue\n            if y.is_dir():\n                dfs(y)\n   \
    \         else:\n                if pred(y):\n                    found.append(y)\n\
    \n    dfs(basedir)\n    return found\n\n\ndef _find_source_code_paths(*, basedir:\
    \ pathlib.Path) -> List[pathlib.Path]:\n    def pred(path: pathlib.Path) -> bool:\n\
    \        return onlinejudge_verify.languages.list.get(path) is not None\n\n  \
    \  return _find_matched_file_paths(pred, basedir=basedir)\n\n\ndef find_markdown_paths(*,\
    \ basedir: pathlib.Path) -> List[pathlib.Path]:\n    def pred(path: pathlib.Path)\
    \ -> bool:\n        return path.suffix == '.md'\n\n    return _find_matched_file_paths(pred,\
    \ basedir=basedir)\n\n\ndef _build_dependency_graph(paths: List[pathlib.Path],\
    \ *, basedir: pathlib.Path) -> Tuple[Dict[pathlib.Path, List[pathlib.Path]], Dict[pathlib.Path,\
    \ List[pathlib.Path]], Dict[pathlib.Path, List[pathlib.Path]]]:\n    \"\"\"\n\
    \    :returns: graphs from absolute paths to relative paths\n    \"\"\"\n    depends_on:\
    \ Dict[pathlib.Path, List[pathlib.Path]] = {}\n    required_by: Dict[pathlib.Path,\
    \ List[pathlib.Path]] = {}\n    verified_with: Dict[pathlib.Path, List[pathlib.Path]]\
    \ = {}\n\n    # initialize\n    for path in paths:\n        absolute_path = (basedir\
    \ / path).resolve()\n        depends_on[absolute_path] = []\n        required_by[absolute_path]\
    \ = []\n        verified_with[absolute_path] = []\n\n    # build the graph\n \
    \   for src in paths:\n        absolute_src = (basedir / src).resolve()\n    \
    \    relative_src = absolute_src.relative_to(basedir)  # all paths must be in\
    \ the git repository\n        language = onlinejudge_verify.languages.list.get(src)\n\
    \        assert language is not None\n\n        try:\n            dependencies\
    \ = language.list_dependencies(src, basedir=basedir)\n        except Exception\
    \ as e:\n            logger.exception('failed to list dependencies of %s: %s',\
    \ str(relative_src), e)\n            continue\n\n        for dst in dependencies:\n\
    \            absolute_dst = (basedir / dst).resolve()\n            relative_dst\
    \ = absolute_dst.relative_to(basedir)\n            if absolute_src == absolute_dst:\n\
    \                continue\n\n            depends_on[absolute_src].append(relative_dst)\n\
    \            if utils.is_verification_file(src, basedir=basedir):\n          \
    \      verified_with[absolute_dst].append(relative_src)\n            else:\n \
    \               required_by[absolute_dst].append(relative_src)\n\n    return depends_on,\
    \ required_by, verified_with\n\n\ndef _build_verification_status(paths: List[pathlib.Path],\
    \ *, verified_with: Dict[pathlib.Path, List[pathlib.Path]], basedir: pathlib.Path,\
    \ marker: VerificationMarker) -> Dict[pathlib.Path, VerificationStatus]:\n   \
    \ \"\"\"\n    :returns: mapping from absolute paths to verification status\n \
    \   \"\"\"\n    verification_status: Dict[pathlib.Path, VerificationStatus] =\
    \ {}\n\n    # list status for verification files\n    for path in paths:\n   \
    \     absolute_path = (basedir / path).resolve()\n        if utils.is_verification_file(path,\
    \ basedir=basedir):\n            if marker.is_verified(path):\n              \
    \  status = VerificationStatus.TEST_ACCEPTED\n            elif marker.is_failed(path):\n\
    \                status = VerificationStatus.TEST_WRONG_ANSWER\n            else:\n\
    \                status = VerificationStatus.TEST_WAITING_JUDGE\n            verification_status[absolute_path]\
    \ = status\n\n    # list status for library files\n    for path in paths:\n  \
    \      absolute_path = (basedir / path).resolve()\n        if not utils.is_verification_file(path,\
    \ basedir=basedir):\n            status_list = []\n            for verification_path\
    \ in verified_with[absolute_path]:\n                status_list.append(verification_status[(basedir\
    \ / verification_path).resolve()])\n            if not status_list:\n        \
    \        status = VerificationStatus.LIBRARY_NO_TESTS\n            elif status_list.count(VerificationStatus.TEST_ACCEPTED)\
    \ == len(status_list):\n                status = VerificationStatus.LIBRARY_ALL_AC\n\
    \            elif status_list.count(VerificationStatus.TEST_WRONG_ANSWER) == len(status_list):\n\
    \                status = VerificationStatus.LIBRARY_ALL_WA\n            elif\
    \ VerificationStatus.TEST_WRONG_ANSWER in status_list:\n                status\
    \ = VerificationStatus.LIBRARY_SOME_WA\n            else:\n                status\
    \ = VerificationStatus.LIBRARY_PARTIAL_AC\n            verification_status[absolute_path]\
    \ = status\n\n    return verification_status\n\n\ndef _get_source_code_stat(\n\
    \        path: pathlib.Path,\n        *,\n        depends_on: Dict[pathlib.Path,\
    \ List[pathlib.Path]],\n        required_by: Dict[pathlib.Path, List[pathlib.Path]],\n\
    \        verified_with: Dict[pathlib.Path, List[pathlib.Path]],\n        verification_status:\
    \ Dict[pathlib.Path, VerificationStatus],\n        marker: VerificationMarker,\n\
    \        basedir: pathlib.Path,\n) -> SourceCodeStat:\n    absolute_path = (basedir\
    \ / path).resolve()\n    relative_path = absolute_path.relative_to(basedir)\n\
    \    language = onlinejudge_verify.languages.list.get(path)\n    assert language\
    \ is not None\n\n    is_verification_file = language.is_verification_file(path,\
    \ basedir=basedir)\n    timestamp = marker.get_current_timestamp(path)\n    try:\n\
    \        attributes = language.list_attributes(path, basedir=basedir)\n    except\
    \ Exception as e:\n        logger.exception('failed to list attributes of %s:\
    \ %s', str(relative_path), e)\n        attributes = {}\n\n    return SourceCodeStat(\n\
    \        path=relative_path,\n        is_verification_file=is_verification_file,\n\
    \        verification_status=verification_status[absolute_path],\n        timestamp=timestamp,\n\
    \        depends_on=depends_on[absolute_path],\n        verified_with=verified_with[absolute_path],\n\
    \        required_by=required_by[absolute_path],\n        attributes=attributes,\n\
    \    )\n\n\ndef generate_source_code_stats(*, marker: VerificationMarker, basedir:\
    \ pathlib.Path) -> List[SourceCodeStat]:\n    source_code_paths = _find_source_code_paths(basedir=basedir)\n\
    \    depends_on, required_by, verified_with = _build_dependency_graph(source_code_paths,\
    \ basedir=basedir)\n    verification_status = _build_verification_status(source_code_paths,\
    \ verified_with=verified_with, basedir=basedir, marker=marker)\n    source_code_stats:\
    \ List[SourceCodeStat] = []\n    for path in source_code_paths:\n        stat\
    \ = _get_source_code_stat(\n            path,\n            depends_on=depends_on,\n\
    \            required_by=required_by,\n            verified_with=verified_with,\n\
    \            verification_status=verification_status,\n            marker=marker,\n\
    \            basedir=basedir,\n        )\n        source_code_stats.append(stat)\n\
    \    return sorted(source_code_stats, key=lambda stat: stat.path)\n\n\ndef is_excluded(relative_path:\
    \ pathlib.Path, *, excluded_paths: List[pathlib.Path]) -> bool:\n    for excluded\
    \ in excluded_paths:\n        if relative_path == excluded or excluded in relative_path.parents:\n\
    \            return True\n    return False\n\n\ndef apply_exclude_list_to_paths(paths:\
    \ List[pathlib.Path], *, excluded_paths: List[pathlib.Path]) -> List[pathlib.Path]:\n\
    \    return [path for path in paths if not is_excluded(path, excluded_paths=excluded_paths)]\n\
    \n\ndef apply_exclude_list_to_stats(*, excluded_paths: List[pathlib.Path], source_code_stats:\
    \ List[SourceCodeStat]) -> List[SourceCodeStat]:\n    result = []\n    for stat\
    \ in source_code_stats:\n        if is_excluded(stat.path, excluded_paths=excluded_paths):\n\
    \            continue\n        stat = SourceCodeStat(\n            path=stat.path,\n\
    \            is_verification_file=stat.is_verification_file,\n            timestamp=stat.timestamp,\n\
    \            depends_on=apply_exclude_list_to_paths(stat.depends_on, excluded_paths=excluded_paths),\n\
    \            required_by=apply_exclude_list_to_paths(stat.required_by, excluded_paths=excluded_paths),\n\
    \            verified_with=apply_exclude_list_to_paths(stat.verified_with, excluded_paths=excluded_paths),\n\
    \            verification_status=stat.verification_status,\n            attributes=stat.attributes,\n\
    \        )\n        result.append(stat)\n    return result\n\n\ndef convert_to_page_render_jobs(*,\
    \ source_code_stats: List[SourceCodeStat], markdown_paths: List[pathlib.Path],\
    \ site_render_config: SiteRenderConfig) -> List[PageRenderJob]:\n    basedir =\
    \ site_render_config.basedir\n\n    page_render_jobs: Dict[pathlib.Path, PageRenderJob]\
    \ = {}\n\n    # Markdown pages\n    for markdown_path in markdown_paths:\n   \
    \     markdown_absolute_path = (basedir / markdown_path).resolve()\n        markdown_relative_path\
    \ = markdown_absolute_path.relative_to(basedir)\n\n        with open(markdown_path,\
    \ 'rb') as fh:\n            content = fh.read()\n        front_matter, content\
    \ = onlinejudge_verify.documentation.front_matter.split_front_matter(content)\n\
    \n        # move the location if documentation_of field exists\n        path =\
    \ markdown_relative_path\n        documentation_of = front_matter.get(FrontMatterItem.documentation_of.value)\n\
    \        if documentation_of is not None:\n            if not (basedir / pathlib.Path(documentation_of)).exists():\n\
    \                logger.warning('the `documentation_of` path of %s is not found:\
    \ %s', str(path), documentation_of)\n                continue\n            documentation_of_path\
    \ = (basedir / pathlib.Path(documentation_of)).resolve().relative_to(basedir)\n\
    \            path = documentation_of_path.parent / (documentation_of_path.name\
    \ + '.md')\n\n        job = PageRenderJob(\n            path=path,\n         \
    \   front_matter=front_matter,\n            content=content,\n        )\n    \
    \    page_render_jobs[job.path] = job\n\n    # API pages\n    for stat in source_code_stats:\n\
    \        path = stat.path.parent / (stat.path.name + '.md')\n        if path in\
    \ page_render_jobs:\n            continue\n\n        front_matter = {}\n     \
    \   front_matter[FrontMatterItem.documentation_of.value] = str(stat.path)\n\n\
    \        # add redirects from old URLs\n        old_directory = 'verify' if stat.is_verification_file\
    \ else 'library'\n        front_matter[FrontMatterItem.redirect_from.value] =\
    \ [\n            '/' + str(pathlib.Path(old_directory) / stat.path),\n       \
    \     '/' + str(pathlib.Path(old_directory) / stat.path.parent / (stat.path.name\
    \ + '.html')),\n        ]\n\n        # add title specified as a attributes like\
    \ @title or @brief\n        front_matter[FrontMatterItem.title.value] = str(stat.path)\n\
    \        if 'document_title' in stat.attributes:\n            front_matter[FrontMatterItem.title.value]\
    \ = stat.attributes['document_title']\n\n        # treat @docs path/to.md directives\n\
    \        content = b''\n        if '_deprecated_at_docs' in stat.attributes:\n\
    \            at_docs_path = pathlib.Path(stat.attributes['_deprecated_at_docs'])\n\
    \            try:\n                with open(at_docs_path, 'rb') as fh:\n    \
    \                content = fh.read()\n            except FileNotFoundError as\
    \ e:\n                logger.exception('failed to read markdown file specified\
    \ by @docs in %s: %s', str(stat.path), e)\n\n        job = PageRenderJob(\n  \
    \          path=path,\n            front_matter=front_matter,\n            content=content,\n\
    \        )\n        page_render_jobs[job.path] = job\n\n    # top page\n    if\
    \ pathlib.Path('index.md') not in page_render_jobs:\n        content = b''\n \
    \       if site_render_config.index_md.exists():\n            with site_render_config.index_md.open('rb')\
    \ as fh:\n                content = fh.read()\n        job = PageRenderJob(\n\
    \            path=pathlib.Path('index.md'),\n            front_matter={\n    \
    \            'layout': 'toppage',\n            },\n            content=content,\n\
    \        )\n        page_render_jobs[job.path] = job\n\n    return list(page_render_jobs.values())\n"
  dependsOn: []
  isVerificationFile: false
  path: onlinejudge_verify/documentation/configure.py
  requiredBy: []
  timestamp: '1970-01-01 00:00:00+00:00'
  verificationStatus: LIBRARY_NO_TESTS
  verifiedWith: []
documentation_of: onlinejudge_verify/documentation/configure.py
layout: document
redirect_from:
- /library/onlinejudge_verify/documentation/configure.py
- /library/onlinejudge_verify/documentation/configure.py.html
title: onlinejudge_verify/documentation/configure.py
---
