#!/bin/bash
set -e

which oj > /dev/null || { echo 'ERROR: please install `oj'\'' with: $ pip3 install --user -U online-judge-tools' >& 1 ; exit 1 ; }

if [ -n "$CXX" ] ; then
    CXX_LIST="$CXX"
else
    CXX_LIST="g++ clang++"
fi
CXXFLAGS="${CXXFLAGS:--std=c++17 -O2 -Wall -g}"
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

get-last-commit-date() {
    file="$1"
    list-dependencies "$file" | xargs git log -1 --date=iso --pretty=%ad
}

get-error() {
    file="$1"
    list-defined "$file" | grep '^#define ERROR ' | sed 's/^#define ERROR "\(.*\)"$/\1/'
}

is-verified() {
    file="$1"
    cache=.verify-helper/timestamp/$(echo -n "$CXX/$file" | md5sum | sed 's/ .*//')
    timestamp="$(get-last-commit-date "$file")"
    [[ -e $cache ]] && [[ $timestamp = $(cat $cache) ]]
}

mark-verified() {
    file="$1"
    cache=.verify-helper/timestamp/$(echo -n "$CXX/$file" | md5sum | sed 's/ .*//')
    mkdir -p .verify-helper/timestamp
    timestamp="$(get-last-commit-date "$file")"
    echo $timestamp > $cache
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
    echo "$ CXX=$CXX ./test.sh $file"

    url="$(get-url "$file")"
    dir=.verify-helper/$(echo -n "$url" | md5sum | sed 's/ .*//')
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
            if [[ -z ${url%%*judge.yosupo.jp*} ]]; then
                python3 -c "$(echo "import onlinejudge, sys ; open(\"${dir}/checker.cpp\", \"wb\").write(onlinejudge.dispatch.problem_from_url(\"${url}\").download_checker_cpp())")"
                curl https://raw.githubusercontent.com/MikeMirzayanov/testlib/master/testlib.h > ${dir}/testlib.h
                $CXX $CXXFLAGS -I ${dir} -o ${dir}/checker.out ${dir}/checker.cpp
                oj test --judge-command ${dir}/checker.out -c ${dir}/a.out -d ${dir}/test
            elif list-defined "$file" | grep '^#define ERROR ' > /dev/null ; then
                error=$(get-error "$file")
                oj test -e ${error} -c ${dir}/a.out -d ${dir}/test
            else
                oj test -c ${dir}/a.out -d ${dir}/test
            fi
        else
            # run
            echo "$ ./a.out"
            time ${dir}/a.out
        fi
        mark-verified "$file"
    fi
}


if [[ $# -eq 0 ]] ; then
    if [[ $GITHUB_ACTIONS ]] ; then
        for f in $(find . -name \*.test.cpp) ; do
            for CXX in $CXX_LIST ; do
                run $f
            done            
            if [[ $SECONDS -gt 600 ]] ; then
                break
            fi
        done

    else
        # local
        for f in $(find . -name \*.test.cpp) ; do
            for CXX in $CXX_LIST ; do
                run $f
            done
        done
    fi
else
    # specified
    for f in "$@" ; do
        for CXX in $CXX_LIST ; do
            run $f
        done
    done
fi
