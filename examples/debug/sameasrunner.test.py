# verification-helper: PROBLEM https://onlinejudge.u-aizu.ac.jp/courses/lesson/2/ITP1/1/ITP1_1_A
import subprocess
import sys


def main():
    print('Hello World')
    r = subprocess.run(['python', '-V'], stdout=sys.stderr)
    if r.returncode != 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
