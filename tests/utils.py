import contextlib
import os
import pathlib
import tempfile
from typing import *


def load_files(files: Dict[str, bytes]) -> ContextManager[pathlib.Path]:
    """
    Load files from a dictionary.

    Args:
        files: (dict): write your description
    """
    files_ = {}
    for relpath, data in files.items():
        assert '/' not in relpath and '\\' not in relpath  # we should use pathlib
        files_[pathlib.Path(relpath)] = data
    return load_files_pathlib(files_)


@contextlib.contextmanager
def load_files_pathlib(files: Dict[pathlib.Path, bytes]) -> Iterator[pathlib.Path]:
    """
    Loads a list.

    Args:
        files: (dict): write your description
        Dict: (todo): write your description
        pathlib: (str): write your description
        Path: (str): write your description
        bytes: (str): write your description
    """
    with tempfile.TemporaryDirectory() as tempdir_:
        tempdir = pathlib.Path(tempdir_).resolve()
        for relpath, data in files.items():
            path = tempdir / relpath
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(str(path), "wb") as fh:
                fh.write(data)
        yield tempdir


@contextlib.contextmanager
def chdir(path: pathlib.Path) -> Iterator[None]:
    """
    Change the working directory.

    Args:
        path: (str): write your description
        pathlib: (str): write your description
        Path: (str): write your description
    """
    cwd = os.getcwd()
    try:
        os.chdir(str(path))
        yield
    finally:
        os.chdir(cwd)
