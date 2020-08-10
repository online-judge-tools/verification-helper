---
layout: default
---

<!-- mathjax config similar to math.stackexchange -->
<script type="text/javascript" async
  src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-MML-AM_CHTML">
</script>
<script type="text/x-mathjax-config">
  MathJax.Hub.Config({
    TeX: { equationNumbers: { autoNumber: "AMS" }},
    tex2jax: {
      inlineMath: [ ['$','$'] ],
      processEscapes: true
    },
    "HTML-CSS": { matchFontHeight: false },
    displayAlign: "left",
    displayIndent: "2em"
  });
</script>

<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/jquery-balloon-js@1.1.2/jquery.balloon.min.js" integrity="sha256-ZEYs9VrgAeNuPvs15E39OsyOJaIkXEEt10fzxJ20+2I=" crossorigin="anonymous"></script>
<script type="text/javascript" src="../../assets/js/copy-button.js"></script>
<link rel="stylesheet" href="../../assets/css/copy-button.css" />


# :warning: onlinejudge_verify/verify.py

<a href="../../index.html">Back to top page</a>

* category: <a href="../../index.html#3ae20b9c01bfbb11e942bafa45933435">onlinejudge_verify</a>
* <a href="{{ site.github.repository_url }}/blob/master/onlinejudge_verify/verify.py">View this file on GitHub</a>
    - Last commit date: 1970-01-01 00:00:00+00:00




## Code

<a id="unbundled"></a>
{% raw %}
```cpp
# Python Version: 3.x
import hashlib
import math
import os
import pathlib
import subprocess
import time
import traceback
from logging import getLogger
from typing import *

import onlinejudge_verify.languages
import onlinejudge_verify.marker

import onlinejudge

logger = getLogger(__name__)


class VerificationSummary(object):
    def __init__(self, *, failed_test_paths: List[pathlib.Path]):
        self.failed_test_paths = failed_test_paths

    def show(self) -> None:
        if self.failed_test_paths:
            logger.error('%d tests failed', len(self.failed_test_paths))
            for path in self.failed_test_paths:
                logger.error('failed: %s', str(path.resolve().relative_to(pathlib.Path.cwd())))
        else:
            logger.info('all tests succeeded')

    def succeeded(self) -> bool:
        return not self.failed_test_paths


def exec_command(command: List[str]):
    # NOTE: secrets like YUKICODER_TOKEN are masked
    logger.info('$ %s', ' '.join(command))

    cwd = pathlib.Path.cwd()
    try:

        subprocess.check_call(command)

    finally:
        # subprocess 中に Ctrl-C とかで止めるとなぜか cd しちゃったままのことがあるので戻す
        if pathlib.Path.cwd() != cwd:
            os.chdir(str(cwd))


def verify_file(path: pathlib.Path, *, compilers: List[str], tle: float, jobs: int) -> Optional[bool]:
    logger.info('verify: %s', path)

    language = onlinejudge_verify.languages.get(path)
    if language is None:
        logger.error('unsupported language')
        return False

    # analyze attributes
    try:
        attributes = language.list_attributes(path, basedir=pathlib.Path.cwd())
    except:
        traceback.print_exc()
        return False
    if 'IGNORE' in attributes:
        return None

    # recognize PROBLEM
    if 'PROBLEM' not in attributes:
        logger.error('PROBLEM is not specified')
        return False
    url = attributes['PROBLEM']
    problem = onlinejudge.dispatch.problem_from_url(url)
    logger.info('problem: %s', url)

    # download test cases
    directory = pathlib.Path('.verify-helper/cache') / hashlib.md5(url.encode()).hexdigest()
    if not (directory / 'test').exists() or not len(list((directory / 'test').iterdir())):
        directory.mkdir(parents=True, exist_ok=True)
        exec_command(['sleep', '2'])
        command = ['oj', 'download', '--system', '-d', str(directory / 'test'), '--silent', url]

        if os.environ.get('YUKICODER_TOKEN'):
            command += ['--yukicoder-token', os.environ['YUKICODER_TOKEN']]
        try:
            exec_command(command)
        except:
            traceback.print_exc()
            if isinstance(problem, onlinejudge.service.yukicoder.YukicoderProblem) and not os.environ.get('YUKICODER_TOKEN'):
                logger.warning('the $YUKICODER_TOKEN environment variable is not set')
            return False

    for environment in language.list_environments(path, basedir=pathlib.Path.cwd()):
        # compile the ./a.out
        try:
            environment.compile(path, basedir=pathlib.Path.cwd(), tempdir=directory)
            execute = ' '.join(environment.get_execute_command(path, basedir=pathlib.Path.cwd(), tempdir=directory))  # TODO: use shlex.join added in Python 3.8
        except:
            traceback.print_exc()
            return False

        # run test using oj
        command = ['oj', 'test', '-c', execute, '-d', str(directory / 'test'), '--print-input', '--tle', str(tle)]
        if isinstance(problem, onlinejudge.service.library_checker.LibraryCheckerProblem):
            command += ['--judge-command', str(problem.download_checker_binary())]
        if 'ERROR' in attributes:
            command += ['-e', attributes['ERROR']]
        if jobs != 1:
            command += ['-j', str(jobs)]
        try:
            exec_command(command)
        except:
            traceback.print_exc()
            return False

    return True


def main(paths: List[pathlib.Path], *, marker: onlinejudge_verify.marker.VerificationMarker, timeout: float = math.inf, tle: float = 60, jobs: int = 1) -> VerificationSummary:
    try:
        import resource
        _, hard = resource.getrlimit(resource.RLIMIT_STACK)
        resource.setrlimit(resource.RLIMIT_STACK, (hard, hard))
    except:
        logger.warning('failed to increase the stack size')
        print(f'::warning ::failed to ulimit')

    compilers = []
    if 'CXX' in os.environ:
        compilers.append(os.environ['CXX'])
    else:
        compilers.append('g++')
        compilers.append('clang++')

    failed_test_paths: List[pathlib.Path] = []

    start = time.time()
    for path in paths:
        if marker.is_verified(path):
            continue

        verified = verify_file(path, compilers=compilers, tle=tle, jobs=jobs)

        if verified is None:
            logger.info('ignored')
        elif verified:
            marker.mark_verified(path)
        else:
            marker.mark_failed(path)
            failed_test_paths.append(path)
            # Set an error message for GitHub Action. https://help.github.com/en/actions/reference/development-tools-for-github-actions
            print(f'::error file={str(path.resolve(strict=True).relative_to(pathlib.Path.cwd().resolve(strict=True)))}::failed to verify')

        # to prevent taking too long; we may fail to use the results of verification due to expired tokens
        if timeout is not None and time.time() - start > timeout:
            break

    return VerificationSummary(failed_test_paths=failed_test_paths)

```
{% endraw %}

<a id="bundled"></a>
{% raw %}
```cpp
Traceback (most recent call last):
  File "/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/docs.py", line 349, in write_contents
    bundled_code = language.bundle(self.file_class.file_path, basedir=pathlib.Path.cwd())
  File "/opt/hostedtoolcache/Python/3.8.5/x64/lib/python3.8/site-packages/onlinejudge_verify/languages/python.py", line 84, in bundle
    raise NotImplementedError
NotImplementedError

```
{% endraw %}

<a href="../../index.html">Back to top page</a>

