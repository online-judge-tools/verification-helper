# Python Version: 3.x
import os


def is_local_execution() -> bool:
    return 'GITHUB_ACTION' not in os.environ
