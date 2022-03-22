# verification-helper: STANDALONE
import subprocess
import sys

def main():
    subprocess.run([sys.executable, '-V'], check=True)


if __name__ == '__main__':
    main()
