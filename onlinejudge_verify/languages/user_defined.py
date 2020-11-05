# Python Version: 3.x
import pathlib
import shlex
import subprocess
from logging import getLogger
from typing import *

import onlinejudge_verify.utils as utils
from onlinejudge_verify.languages.models import Language, LanguageEnvironment
from onlinejudge_verify.languages.special_comments import list_special_comments

logger = getLogger(__name__)


class UserDefinedLanguageEnvironment(LanguageEnvironment):
    config: Dict[str, str]

    def __init__(self, *, config: Dict[str, str]):
        """
        Initialize the configuration.

        Args:
            self: (todo): write your description
            config: (todo): write your description
        """
        self.config = config

    def compile(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> None:
        """
        Compile the given directory.

        Args:
            self: (todo): write your description
            path: (str): write your description
            pathlib: (str): write your description
            Path: (str): write your description
            basedir: (str): write your description
            pathlib: (str): write your description
            Path: (str): write your description
            tempdir: (str): write your description
            pathlib: (str): write your description
            Path: (str): write your description
        """
        assert 'compile' in self.config
        command = self.config['compile'].format(path=str(path), basedir=str(basedir), tempdir=str(tempdir))
        logger.info('$ %s', command)
        subprocess.check_call(shlex.split(command))

    def get_execute_command(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> List[str]:
        """
        Execute a command on the given path.

        Args:
            self: (todo): write your description
            path: (str): write your description
            pathlib: (str): write your description
            Path: (str): write your description
            basedir: (str): write your description
            pathlib: (str): write your description
            Path: (str): write your description
            tempdir: (str): write your description
            pathlib: (str): write your description
            Path: (str): write your description
        """
        assert 'execute' in self.config
        command = self.config['execute'].format(path=str(path), basedir=str(basedir), tempdir=str(tempdir))
        return shlex.split(command)


class UserDefinedLanguage(Language):
    extension: str
    config: Dict[str, str]

    def __init__(self, *, extension: str, config: Dict[str, str]):
        """
        Initialize extension.

        Args:
            self: (todo): write your description
            extension: (todo): write your description
            config: (todo): write your description
        """
        self.extension = extension
        self.config = config

    def list_attributes(self, path: pathlib.Path, *, basedir: pathlib.Path) -> Dict[str, str]:
        """
        Returns a list of path.

        Args:
            self: (todo): write your description
            path: (str): write your description
            pathlib: (str): write your description
            Path: (str): write your description
            basedir: (str): write your description
            pathlib: (str): write your description
            Path: (str): write your description
        """
        if 'list_attributes' not in self.config:
            return list_special_comments(path)
        logger.warning('"languages.*.list_attributes" field in .verify-helper/config.toml is now obsoleted')

        command = self.config['list_attributes'].format(path=str(path), basedir=str(basedir))
        text = subprocess.check_output(shlex.split(command))
        attributes = {}
        for line in text.splitlines():
            key, _, value = line.decode().partition(' ')
            attributes[key] = value
        return attributes

    def list_dependencies(self, path: pathlib.Path, *, basedir: pathlib.Path) -> List[pathlib.Path]:
        """
        Return a list of files.

        Args:
            self: (todo): write your description
            path: (str): write your description
            pathlib: (str): write your description
            Path: (str): write your description
            basedir: (str): write your description
            pathlib: (str): write your description
            Path: (str): write your description
        """
        if 'list_dependencies' not in self.config:
            logger.warning('The functionality to list dependencies of .%s file is not implemented yet.', self.extension)
            return list(utils.glob_with_predicate(lambda path: path.suffix == '.' + self.extension))

        command = self.config['list_dependencies'].format(path=str(path), basedir=str(basedir))
        text = subprocess.check_output(shlex.split(command))
        dependencies = [path]
        for line in text.splitlines():
            dependencies.append(pathlib.Path(line.decode()))
        return dependencies

    def bundle(self, path: pathlib.Path, *, basedir: pathlib.Path, options: Dict[str, Any]) -> bytes:
        """
        Bundle command.

        Args:
            self: (todo): write your description
            path: (str): write your description
            pathlib: (str): write your description
            Path: (str): write your description
            basedir: (str): write your description
            pathlib: (str): write your description
            Path: (str): write your description
            options: (dict): write your description
        """
        assert 'bundle' in self.config
        command = self.config['bundle'].format(path=str(path), basedir=str(basedir))
        logger.info('$ %s', command)
        return subprocess.check_output(shlex.split(command))

    def is_verification_file(self, path: pathlib.Path, *, basedir: pathlib.Path) -> bool:
        """
        Return true if path is_verification is_file.

        Args:
            self: (todo): write your description
            path: (str): write your description
            pathlib: (str): write your description
            Path: (str): write your description
            basedir: (str): write your description
            pathlib: (str): write your description
            Path: (str): write your description
        """
        suffix = self.config.get('verification_file_suffix')
        if suffix is not None:
            return path.name.endswith(suffix)
        return super().is_verification_file(path, basedir=basedir)

    def list_environments(self, path: pathlib.Path, *, basedir: pathlib.Path) -> Sequence[LanguageEnvironment]:
        """
        Return a list of environments.

        Args:
            self: (todo): write your description
            path: (str): write your description
            pathlib: (str): write your description
            Path: (str): write your description
            basedir: (str): write your description
            pathlib: (str): write your description
            Path: (str): write your description
        """
        return [UserDefinedLanguageEnvironment(config=self.config)]
