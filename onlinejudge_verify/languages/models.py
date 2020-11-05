# Python Version: 3.x
import abc
import pathlib
from typing import *

import onlinejudge_verify.languages.special_comments as special_comments


class LanguageEnvironment(object):
    @abc.abstractmethod
    def compile(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> None:
        """
        :throws Exception:
        """

        raise NotImplementedError

    @abc.abstractmethod
    def get_execute_command(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> List[str]:
        """
        Executes the specified command.

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
        raise NotImplementedError


class Language(object):
    def list_attributes(self, path: pathlib.Path, *, basedir: pathlib.Path) -> Dict[str, Any]:
        """
        :throws Exception:
        """

        attributes: Dict[str, Any] = special_comments.list_special_comments(path)
        attributes.setdefault('links', [])
        attributes['links'].extend(special_comments.list_embedded_urls(path))
        return attributes

    @abc.abstractmethod
    def list_dependencies(self, path: pathlib.Path, *, basedir: pathlib.Path) -> List[pathlib.Path]:
        """
        :throws Exception:
        """

        raise NotImplementedError

    @abc.abstractmethod
    def bundle(self, path: pathlib.Path, *, basedir: pathlib.Path, options: Dict[str, Any]) -> bytes:
        """
        :throws Exception:
        :throws NotImplementedError:
        """

        raise NotImplementedError

    def is_verification_file(self, path: pathlib.Path, *, basedir: pathlib.Path) -> bool:
        """
        Return true if path is a verification file.

        Args:
            self: (todo): write your description
            path: (str): write your description
            pathlib: (str): write your description
            Path: (str): write your description
            basedir: (str): write your description
            pathlib: (str): write your description
            Path: (str): write your description
        """
        return '.test.' in path.name

    @abc.abstractmethod
    def list_environments(self, path: pathlib.Path, *, basedir: pathlib.Path) -> Sequence[LanguageEnvironment]:
        """
        Return a list of path entries in path.

        Args:
            self: (todo): write your description
            path: (str): write your description
            pathlib: (str): write your description
            Path: (str): write your description
            basedir: (str): write your description
            pathlib: (str): write your description
            Path: (str): write your description
        """
        raise NotImplementedError
