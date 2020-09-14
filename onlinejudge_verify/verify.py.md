---
data:
  _extendedDependsOn: []
  _extendedRequiredBy: []
  _extendedVerifiedWith: []
  _pathExtension: py
  _verificationStatusIcon: ':warning:'
  attributes:
    links:
    - https://help.github.com/en/actions/reference/development-tools-for-github-actions
  bundledCode: "Traceback (most recent call last):\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/documentation/build.py\"\
    , line 70, in _render_source_code_stat\n    bundled_code = language.bundle(stat.path,\
    \ basedir=basedir).decode()\n  File \"/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/languages/python.py\"\
    , line 84, in bundle\n    raise NotImplementedError\nNotImplementedError\n"
  code: "# Python Version: 3.x\nimport hashlib\nimport math\nimport os\nimport pathlib\n\
    import subprocess\nimport time\nimport traceback\nfrom logging import getLogger\n\
    from typing import *\n\nimport onlinejudge_verify.languages.list\nimport onlinejudge_verify.marker\n\
    \nimport onlinejudge\n\nlogger = getLogger(__name__)\n\n\nclass VerificationSummary(object):\n\
    \    def __init__(self, *, failed_test_paths: List[pathlib.Path]):\n        self.failed_test_paths\
    \ = failed_test_paths\n\n    def show(self) -> None:\n        if self.failed_test_paths:\n\
    \            logger.error('%d tests failed', len(self.failed_test_paths))\n  \
    \          for path in self.failed_test_paths:\n                logger.error('failed:\
    \ %s', str(path.resolve().relative_to(pathlib.Path.cwd())))\n        else:\n \
    \           logger.info('all tests succeeded')\n\n    def succeeded(self) -> bool:\n\
    \        return not self.failed_test_paths\n\n\ndef exec_command(command: List[str]):\n\
    \    # NOTE: secrets like YUKICODER_TOKEN are masked\n    logger.info('$ %s',\
    \ ' '.join(command))\n\n    cwd = pathlib.Path.cwd()\n    try:\n\n        subprocess.check_call(command)\n\
    \n    finally:\n        # subprocess \u4E2D\u306B Ctrl-C \u3068\u304B\u3067\u6B62\
    \u3081\u308B\u3068\u306A\u305C\u304B cd \u3057\u3061\u3083\u3063\u305F\u307E\u307E\
    \u306E\u3053\u3068\u304C\u3042\u308B\u306E\u3067\u623B\u3059\n        if pathlib.Path.cwd()\
    \ != cwd:\n            os.chdir(str(cwd))\n\n\ndef verify_file(path: pathlib.Path,\
    \ *, compilers: List[str], tle: float, jobs: int) -> Optional[bool]:\n    logger.info('verify:\
    \ %s', path)\n\n    language = onlinejudge_verify.languages.list.get(path)\n \
    \   if language is None:\n        logger.error('unsupported language')\n     \
    \   return False\n\n    # analyze attributes\n    try:\n        attributes = language.list_attributes(path,\
    \ basedir=pathlib.Path.cwd())\n    except:\n        traceback.print_exc()\n  \
    \      return False\n    if 'IGNORE' in attributes:\n        return None\n\n \
    \   # recognize PROBLEM\n    if 'PROBLEM' not in attributes:\n        logger.error('PROBLEM\
    \ is not specified')\n        return False\n    url = attributes['PROBLEM']\n\
    \    problem = onlinejudge.dispatch.problem_from_url(url)\n    logger.info('problem:\
    \ %s', url)\n\n    # download test cases\n    directory = pathlib.Path('.verify-helper/cache')\
    \ / hashlib.md5(url.encode()).hexdigest()\n    if not (directory / 'test').exists()\
    \ or not len(list((directory / 'test').iterdir())):\n        directory.mkdir(parents=True,\
    \ exist_ok=True)\n        exec_command(['sleep', '2'])\n        command = ['oj',\
    \ 'download', '--system', '-d', str(directory / 'test'), '--silent', url]\n\n\
    \        if os.environ.get('YUKICODER_TOKEN'):\n            command += ['--yukicoder-token',\
    \ os.environ['YUKICODER_TOKEN']]\n        try:\n            exec_command(command)\n\
    \        except:\n            traceback.print_exc()\n            if isinstance(problem,\
    \ onlinejudge.service.yukicoder.YukicoderProblem) and not os.environ.get('YUKICODER_TOKEN'):\n\
    \                logger.warning('the $YUKICODER_TOKEN environment variable is\
    \ not set')\n            return False\n\n    for environment in language.list_environments(path,\
    \ basedir=pathlib.Path.cwd()):\n        # compile the ./a.out\n        try:\n\
    \            environment.compile(path, basedir=pathlib.Path.cwd(), tempdir=directory)\n\
    \            execute = ' '.join(environment.get_execute_command(path, basedir=pathlib.Path.cwd(),\
    \ tempdir=directory))  # TODO: use shlex.join added in Python 3.8\n        except:\n\
    \            traceback.print_exc()\n            return False\n\n        # run\
    \ test using oj\n        command = ['oj', 'test', '-c', execute, '-d', str(directory\
    \ / 'test'), '--print-input', '--tle', str(tle)]\n        if isinstance(problem,\
    \ onlinejudge.service.library_checker.LibraryCheckerProblem):\n            command\
    \ += ['--judge-command', str(problem.download_checker_binary())]\n        if 'ERROR'\
    \ in attributes:\n            command += ['-e', attributes['ERROR']]\n       \
    \ if jobs != 1:\n            command += ['-j', str(jobs)]\n        try:\n    \
    \        exec_command(command)\n        except:\n            traceback.print_exc()\n\
    \            return False\n\n    return True\n\n\ndef main(paths: List[pathlib.Path],\
    \ *, marker: onlinejudge_verify.marker.VerificationMarker, timeout: float = math.inf,\
    \ tle: float = 60, jobs: int = 1) -> VerificationSummary:\n    try:\n        import\
    \ resource\n        _, hard = resource.getrlimit(resource.RLIMIT_STACK)\n    \
    \    resource.setrlimit(resource.RLIMIT_STACK, (hard, hard))\n    except:\n  \
    \      logger.warning('failed to increase the stack size')\n        print(f'::warning\
    \ ::failed to ulimit')\n\n    compilers = []\n    if 'CXX' in os.environ:\n  \
    \      compilers.append(os.environ['CXX'])\n    else:\n        compilers.append('g++')\n\
    \        compilers.append('clang++')\n\n    failed_test_paths: List[pathlib.Path]\
    \ = []\n\n    start = time.time()\n    for path in paths:\n        if marker.is_verified(path):\n\
    \            continue\n\n        verified = verify_file(path, compilers=compilers,\
    \ tle=tle, jobs=jobs)\n\n        if verified is None:\n            logger.info('ignored')\n\
    \        elif verified:\n            marker.mark_verified(path)\n        else:\n\
    \            marker.mark_failed(path)\n            failed_test_paths.append(path)\n\
    \            # Set an error message for GitHub Action. https://help.github.com/en/actions/reference/development-tools-for-github-actions\n\
    \            print(f'::error file={str(path.resolve(strict=True).relative_to(pathlib.Path.cwd().resolve(strict=True)))}::failed\
    \ to verify')\n\n        # to prevent taking too long; we may fail to use the\
    \ results of verification due to expired tokens\n        if timeout is not None\
    \ and time.time() - start > timeout:\n            break\n\n    return VerificationSummary(failed_test_paths=failed_test_paths)\n"
  dependsOn: []
  isVerificationFile: false
  path: onlinejudge_verify/verify.py
  requiredBy: []
  timestamp: '1970-01-01 00:00:00+00:00'
  verificationStatus: LIBRARY_NO_TESTS
  verifiedWith: []
documentation_of: onlinejudge_verify/verify.py
layout: document
redirect_from:
- /library/onlinejudge_verify/verify.py
- /library/onlinejudge_verify/verify.py.html
title: onlinejudge_verify/verify.py
---
