# Python Version: 3.x
import argparse
import os
import pathlib
import subprocess
import sys
import tempfile
from typing import *

bash_script = r"""#!/bin/bash
set -e

which oj > /dev/null || { echo 'ERROR: please install `oj'\'' with: $ pip3 install --user -U online-judge-tools=='\''6.*'\''' >& 1 ; exit 1 ; }

CXX=${CXX:-g++}
CXXFLAGS="${CXXFLAGS:--std=c++14 -O2 -Wall -g}"
ulimit -s unlimited || true


list-dependencies() {
    file="$1"
    $CXX $CXXFLAGS -I . -MD -MF /dev/stdout -MM "$file" | sed '1s/[^:].*: // ; s/\\$//' | xargs -n 1
}

list-defined() {
    file="$1"
    $CXX $CXXFLAGS -I . -dM -E "$file"
}

get-url() {
    file="$1"
    list-defined "$file" | grep '^#define PROBLEM ' | sed 's/^#define PROBLEM "\(.*\)"$/\1/'
}

is-verified() {
    file="$1"
    cache=test/timestamp/$(echo -n "$file" | md5sum | sed 's/ .*//')
    timestamp="$(list-dependencies "$file" | xargs -I '{}' find "$file" '{}' -printf "%T+\t%p\n" | sort -nr | head -n 1 | cut -f 2)"
    [[ -e $cache ]] && [[ $timestamp -ot $cache ]]
}

mark-verified() {
    file="$1"
    cache=test/timestamp/$(echo -n "$file" | md5sum | sed 's/ .*//')
    mkdir -p test/timestamp
    touch $cache
}

list-recently-updated() {
    for file in $(find . -name \*.test.cpp) ; do
        list-dependencies "$file" | xargs -n 1 | while read f ; do
            git log -1 --format="%ci	${file}" "$f"
        done | sort -nr | head -n 1
    done | sort -nr | head -n 20 | cut -f 2
}

run() {
    file="$1"
    echo "$ ./test.sh $file"

    url="$(get-url "$file")"
    dir=test/$(echo -n "$url" | md5sum | sed 's/ .*//')
    mkdir -p ${dir}

    # ignore if IGNORE is defined
    if list-defined "$file" | grep '^#define IGNORE ' > /dev/null ; then
        return
    fi

    if ! is-verified "$file" ; then
        # compile
        $CXX $CXXFLAGS -I . -o ${dir}/a.out "$file"
        if [[ -n ${url} ]] ; then
            # download
            echo "$ oj d -a $url"
            if [[ ! -e ${dir}/test ]] ; then
                sleep 2
                oj download --system "$url" -d ${dir}/test
            fi
            # test
            echo '$ oj t'
            oj test -c ${dir}/a.out -d ${dir}/test
        else
            # run
            echo "$ ./a.out"
            time ${dir}/a.out
        fi
        mark-verified "$file"
    fi
}


if [[ $# -eq 1 && ( $1 = -h || $1 = --help || $1 = -? ) ]] ; then
    echo Usage: $0 '[FILE ...]'
    echo 'Compile and Run specified C++ code.'
    echo 'If the given code contains macro like `#define PROBLEM "https://..."'\'', Download test cases of the problem and Test with them.'
    echo
    echo 'Features:'
    echo '-   glob files with "**/*.test.cpp" if no arguments given.'
    echo '-   cache results of tests, analyze "#include <...>" relations, and execute tests if and only if necessary.'
    echo '-   on CI environment (i.e. $CI is defined), only recently modified files are tested (without cache).'

elif [[ $# -eq 0 ]] ; then
    if [[ $CI ]] ; then
        # CI
        for f in $(list-recently-updated) ; do
            run $f
        done

    else
        # local
        for f in $(find . -name \*.test.cpp) ; do
            run $f
        done
    fi
else
    # specified
    for f in "$@" ; do
        run "$f"
    done
fi
"""

verify_yml = r"""name: verify

on:
  push:
    branches:
    - master

jobs:
  build:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v1

    - name: Set up Python
      uses: actions/setup-python@v1

    - name: Install dependencies
      run: pip3 install -U git+https://github.com/kmyk/online-judge-ci-script

    - name: Run tests
      run: oj-ci run
"""


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subcommand')

    subparser = subparsers.add_parser('run')
    subparser.add_argument('path', nargs='*', type=pathlib.Path)

    subparser = subparsers.add_parser('init')
    subparser.add_argument('--target', choices=['github-actions'], default='github-actions')

    subparser = subparsers.add_parser('export')
    subparser.add_argument('path', type=pathlib.Path)

    subparser = subparsers.add_parser('snippet')
    subparser.add_argument('--target', choices=['vscode'], required=True)

    return parser


def main(args: Optional[List[str]] = None) -> None:
    parser = get_parser()
    parsed = parser.parse_args(args)

    if parsed.subcommand == 'run':
        fh = tempfile.NamedTemporaryFile(delete=False)
        fh.write(bash_script.encode())
        fh.close()
        try:
            subprocess.check_call(['/bin/bash', fh.name] + list(map(str, parsed.path)), stdout=sys.stdout, stderr=sys.stderr)
        finally:
            os.remove(fh.name)

    elif parsed.subcommand == 'init':
        if parsed.target == 'github-actions':
            path = pathlib.Path('.github/workflows/verify.yml')
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(str(path), 'w') as fh:
                fh.write(verify_yml)
        else:
            assert False

    elif parsed.subcommand == 'export':
        raise NotImplementedError('#include "hoge.hpp" みたいなやつをいい感じに展開してそのまま提出できる形コードを出力してほしい')

    elif parsed.subcommand == 'snippet':
        raise NotImplementedError('ついでに VS Code 用の snippet.json みたいなやつもいい感じに出力されてほしい')

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
