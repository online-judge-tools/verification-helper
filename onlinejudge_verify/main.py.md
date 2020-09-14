---
data:
  _extendedDependsOn: []
  _extendedRequiredBy: []
  _extendedVerifiedWith: []
  _pathExtension: py
  _verificationStatusIcon: ':warning:'
  attributes:
    links:
    - '''https://{}:{}@github.com/{}.git''.format(os.environ[''GITHUB_ACTOR''],'
    - '''https://{}@github.com/{}.git''.format(os.environ[''GH_PAT''],'
    - http://127.0.0.1:4000
    - https://bundler.io/).
    - https://github.com/marketplace/actions/github-pages-deploy#secrets
    - https://github.com/maxheld83/ghpages/issues/1
    - https://help.github.com/en/actions/automating-your-workflow-with-github-actions/authenticating-with-the-github_token#about-the-github_token-secret)
  bundledCode: "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/documentation/build.py\"\
    , line 70, in _render_source_code_stat\n    bundled_code = language.bundle(stat.path,\
    \ basedir=basedir).decode()\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/languages/python.py\"\
    , line 84, in bundle\n    raise NotImplementedError\nNotImplementedError\n"
  code: "\"\"\"\nisort: skip_file\n\"\"\"\n\n# pylint: disable=unused-import,ungrouped-imports\n\
    try:\n    import onlinejudge.service\nexcept ModuleNotFoundError:\n    print(\"\
    Due to a known bug, the online-judge-tools is not yet properly installed. Please\
    \ re-run $ pip3 install --force-reinstall online-judge-api-client\")\n    exit(1)\n\
    # pylint: enable=unused-import,ungrouped-imports\n\nimport argparse\nimport glob\n\
    import math\nimport os\nimport pathlib\nimport subprocess\nimport sys\nimport\
    \ textwrap\nfrom logging import INFO, basicConfig, getLogger\nfrom typing import\
    \ *\n\nimport colorlog\nimport onlinejudge_verify.config\nimport onlinejudge_verify.documentation.main\n\
    import onlinejudge_verify.marker\nimport onlinejudge_verify.utils\nimport onlinejudge_verify.verify\n\
    \nlogger = getLogger(__name__)\n\n\ndef get_parser() -> argparse.ArgumentParser:\n\
    \    parser = argparse.ArgumentParser()\n    parser.add_argument('--config-file',\
    \ default=onlinejudge_verify.config.default_config_path, help='default: \".verify-helper/config.toml\"\
    ')\n\n    subparsers = parser.add_subparsers(dest='subcommand')\n\n    subparser\
    \ = subparsers.add_parser('all')\n    subparser.add_argument('-j', '--jobs', type=int,\
    \ default=1)\n    subparser.add_argument('--timeout', type=float, default=600)\n\
    \    subparser.add_argument('--tle', type=float, default=60)\n\n    subparser\
    \ = subparsers.add_parser('run')\n    subparser.add_argument('path', nargs='*',\
    \ type=pathlib.Path)\n    subparser.add_argument('-j', '--jobs', type=int, default=1)\n\
    \    subparser.add_argument('--timeout', type=float, default=600)\n    subparser.add_argument('--tle',\
    \ type=float, default=60)\n\n    subparser = subparsers.add_parser('docs')\n \
    \   subparser.add_argument('-j', '--jobs', type=int, default=1)\n\n    subparser\
    \ = subparsers.add_parser('stats')\n    subparser.add_argument('-j', '--jobs',\
    \ type=int, default=1)\n\n    return parser\n\n\ndef subcommand_run(paths: List[pathlib.Path],\
    \ *, timeout: float = 600, tle: float = 60, jobs: int = 1) -> onlinejudge_verify.verify.VerificationSummary:\n\
    \    \"\"\"\n    :raises Exception: if test.sh fails\n    \"\"\"\n\n    does_push\
    \ = 'GITHUB_ACTION' in os.environ and 'GITHUB_TOKEN' in os.environ and os.environ.get('GITHUB_REF',\
    \ '').startswith('refs/heads/')  # NOTE: $GITHUB_REF may be refs/pull/... or refs/tags/...\n\
    \    if does_push:\n        # checkout in advance to push\n        branch = os.environ['GITHUB_REF'][len('refs/heads/'):]\n\
    \        logger.info('$ git checkout %s', branch)\n        subprocess.check_call(['git',\
    \ 'checkout', branch])\n\n    # NOTE: the GITHUB_TOKEN expires in 60 minutes (https://help.github.com/en/actions/automating-your-workflow-with-github-actions/authenticating-with-the-github_token#about-the-github_token-secret)\n\
    \    # use 10 minutes as timeout for safety; \u7406\u7531\u306F\u3088\u304F\u5206\
    \u304B\u3063\u3066\u306A\u3044\u307D\u3044\u3051\u3069\u4EE5\u524D 20 \u5206\u3067\
    \u3084\u3063\u3066\u6B7B\u3093\u3060\u3053\u3068\u304C\u3042\u308B\u3089\u3057\
    \u3044\u306E\u3067\n    if 'GITHUB_ACTION' not in os.environ:\n        timeout\
    \ = math.inf\n\n    if not paths:\n        paths = sorted(list(onlinejudge_verify.utils.iterate_verification_files()))\n\
    \    try:\n        with onlinejudge_verify.marker.get_verification_marker() as\
    \ marker:\n            return onlinejudge_verify.verify.main(paths, marker=marker,\
    \ timeout=timeout, tle=tle, jobs=jobs)\n    finally:\n        # push results even\
    \ if some tests failed\n        if does_push:\n            push_timestamp_to_branch()\n\
    \n\ndef push_timestamp_to_branch() -> None:\n    # read config\n    logger.info('use\
    \ GITHUB_TOKEN')  # NOTE: don't use GH_PAT here, because it may cause infinite\
    \ loops with triggering GitHub Actions itself\n    url = 'https://{}:{}@github.com/{}.git'.format(os.environ['GITHUB_ACTOR'],\
    \ os.environ['GITHUB_TOKEN'], os.environ['GITHUB_REPOSITORY'])\n    logger.info('GITHUB_ACTOR\
    \ = %s', os.environ['GITHUB_ACTOR'])\n    logger.info('GITHUB_REPOSITORY = %s',\
    \ os.environ['GITHUB_REPOSITORY'])\n\n    # commit and push\n    subprocess.check_call(['git',\
    \ 'config', '--global', 'user.name', 'GitHub'])\n    subprocess.check_call(['git',\
    \ 'config', '--global', 'user.email', 'noreply@github.com'])\n    path = onlinejudge_verify.marker.get_verification_marker().json_path\n\
    \    logger.info('$ git add %s && git commit && git push', str(path))\n    if\
    \ path.exists():\n        subprocess.check_call(['git', 'add', str(path)])\n \
    \   if subprocess.run(['git', 'diff', '--quiet', '--staged']).returncode:\n  \
    \      message = '[auto-verifier] verify commit {}'.format(os.environ['GITHUB_SHA'])\n\
    \        subprocess.check_call(['git', 'commit', '-m', message])\n        subprocess.check_call(['git',\
    \ 'push', url, 'HEAD'])\n\n\ndef push_documents_to_gh_pages(*, src_dir: pathlib.Path,\
    \ dst_branch: str = 'gh-pages') -> None:\n    # read config\n    if not os.environ.get('GH_PAT'):\n\
    \        # If we push commits using GITHUB_TOKEN, the build of GitHub Pages will\
    \ not run. See https://github.com/marketplace/actions/github-pages-deploy#secrets\
    \ and https://github.com/maxheld83/ghpages/issues/1\n        logger.error(\"GH_PAT\
    \ is not available. You cannot upload the generated documents to GitHub Pages.\"\
    )\n        return\n    logger.info('use GH_PAT')\n    url = 'https://{}@github.com/{}.git'.format(os.environ['GH_PAT'],\
    \ os.environ['GITHUB_REPOSITORY'])\n    logger.info('GITHUB_REPOSITORY = %s',\
    \ os.environ['GITHUB_REPOSITORY'])\n\n    # read files before checkout\n    logger.info('read\
    \ files from %s', str(src_dir))\n    src_files = {}\n    for path in map(pathlib.Path,\
    \ glob.glob(str(src_dir) + '/**/*', recursive=True)):\n        if path.is_file():\n\
    \            logger.info('%s', str(path))\n            with open(str(path), 'rb')\
    \ as fh:\n                src_files[path.relative_to(src_dir)] = fh.read()\n\n\
    \    # checkout gh-pages\n    logger.info('$ git checkout %s', dst_branch)\n \
    \   subprocess.check_call(['rm', '.verify-helper/.gitignore'])  # required, to\
    \ remove .gitignore even if it is untracked\n    subprocess.check_call(['git',\
    \ 'stash'])\n    try:\n        subprocess.check_call(['git', 'checkout', dst_branch])\n\
    \    except subprocess.CalledProcessError:\n        subprocess.check_call(['git',\
    \ 'checkout', '--orphan', dst_branch])\n\n    # remove all non-hidden files and\
    \ write new files\n    logger.info('write files to . on %s', dst_branch)\n   \
    \ for pattern in ('**/*', '.*/**/*'):\n        for path in map(pathlib.Path, glob.glob(pattern,\
    \ recursive=True)):\n            if path.is_file() and path.parts[0] != '.git':\n\
    \                path.unlink()\n    for path, data in src_files.items():\n   \
    \     path.parent.mkdir(parents=True, exist_ok=True)\n        with open(str(path),\
    \ 'wb') as fh:\n            fh.write(data)\n\n    # commit and push\n    logger.info('$\
    \ git add . && git commit && git push')\n    subprocess.check_call(['git', 'config',\
    \ '--global', 'user.name', 'GitHub'])\n    subprocess.check_call(['git', 'config',\
    \ '--global', 'user.email', 'noreply@github.com'])\n    subprocess.check_call(['git',\
    \ 'add', '.'])\n    if subprocess.run(['git', 'diff', '--quiet', '--staged']).returncode:\n\
    \        message = '[auto-verifier] docs commit {}'.format(os.environ['GITHUB_SHA'])\n\
    \        subprocess.check_call(['git', 'commit', '-m', message])\n        subprocess.check_call(['git',\
    \ 'push', url, 'HEAD'])\n\n\ndef subcommand_docs(*, jobs: int = 1) -> None:\n\
    \    if 'GITHUB_ACTION' in os.environ and 'GITHUB_TOKEN' in os.environ:\n    \
    \    if os.environ['GITHUB_REF'] == 'refs/heads/master':\n            logger.info('generate\
    \ documents...')\n            onlinejudge_verify.documentation.main.main(jobs=jobs)\n\
    \n            logger.info('upload documents...')\n            push_documents_to_gh_pages(src_dir=pathlib.Path('.verify-helper/markdown'))\n\
    \n    else:\n        logger.info('generate documents...')\n        onlinejudge_verify.documentation.main.main(jobs=jobs)\n\
    \        logger.info('done.')\n        logger.info('%s', '\\n'.join([\n      \
    \      'To see the generated document, do the following steps:',\n           \
    \ '    1. Install Ruby with the files to build native modules. In Ubuntu, $ sudo\
    \ apt install ruby-all-dev',\n            \"    2. Install Ruby's Bundler (https://bundler.io/).\
    \ In Ubuntu, $ sudo apt install ruby-bundler\",\n            '    3. $ cd .verify-helper/markdown',\n\
    \            '    4. $ bundle install --path .vendor/bundle',\n            ' \
    \   5. $ bundle exec jekyll serve --incremental',\n            '    6. Open http://127.0.0.1:4000\
    \ on your web browser',\n        ]))\n\n\ndef subcommand_stats(*, jobs: int =\
    \ 1) -> None:\n    onlinejudge_verify.documentation.main.print_stats_json(jobs=jobs)\n\
    \n\ndef generate_gitignore() -> None:\n    path = pathlib.Path('.verify-helper/.gitignore')\n\
    \    data = textwrap.dedent(\"\"\"\\\n        .gitignore\n        cache/\n   \
    \     include/\n        markdown/\n        timestamps.local.json\n    \"\"\")\n\
    \    if path.exists():\n        with open(path) as fh:\n            if fh.read()\
    \ == data:\n                return\n    path.parent.mkdir(parents=True, exist_ok=True)\n\
    \    with open(path, 'w') as fh:\n        fh.write(data)\n\n\ndef main(args: Optional[List[str]]\
    \ = None) -> None:\n    # configure logging\n    log_format = '%(log_color)s%(levelname)s%(reset)s:%(name)s:%(message)s'\n\
    \    handler = colorlog.StreamHandler()\n    handler.setFormatter(colorlog.ColoredFormatter(log_format))\n\
    \    basicConfig(level=INFO, handlers=[handler])\n\n    # parse command-line arguments\n\
    \    parser = get_parser()\n    parsed = parser.parse_args(args)\n\n    # load\
    \ the config file as a global variable\n    onlinejudge_verify.config.set_config_path(pathlib.Path(parsed.config_file))\n\
    \n    if getattr(parsed, 'jobs', None) is not None:\n        # \u5148\u306B\u4E26\
    \u5217\u3067\u8AAD\u307F\u8FBC\u307F\u3057\u3066\u304A\u304F\n        onlinejudge_verify.marker.get_verification_marker(jobs=parsed.jobs)\n\
    \n    if parsed.subcommand == 'all':\n        generate_gitignore()\n        summary\
    \ = subcommand_run(paths=[], timeout=parsed.timeout, tle=parsed.tle, jobs=parsed.jobs)\n\
    \        subcommand_docs(jobs=parsed.jobs)\n        summary.show()\n        if\
    \ not summary.succeeded():\n            sys.exit(1)\n\n    elif parsed.subcommand\
    \ == 'run':\n        generate_gitignore()\n        summary = subcommand_run(paths=parsed.path,\
    \ timeout=parsed.timeout, tle=parsed.tle, jobs=parsed.jobs)\n        summary.show()\n\
    \        if not summary.succeeded():\n            sys.exit(1)\n\n    elif parsed.subcommand\
    \ == 'docs':\n        generate_gitignore()\n        subcommand_docs(jobs=parsed.jobs)\n\
    \n    elif parsed.subcommand == 'stats':\n        subcommand_stats(jobs=parsed.jobs)\n\
    \n    else:\n        parser.print_help()\n\n\nif __name__ == \"__main__\":\n \
    \   main()\n"
  dependsOn: []
  isVerificationFile: false
  path: onlinejudge_verify/main.py
  requiredBy: []
  timestamp: '1970-01-01 00:00:00+00:00'
  verificationStatus: LIBRARY_NO_TESTS
  verifiedWith: []
documentation_of: onlinejudge_verify/main.py
layout: document
redirect_from:
- /library/onlinejudge_verify/main.py
- /library/onlinejudge_verify/main.py.html
title: onlinejudge_verify/main.py
---
