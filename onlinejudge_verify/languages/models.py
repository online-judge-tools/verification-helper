# Python Version: 3.x
import abc
import pathlib
from typing import *

import onlinejudge_verify.languages.special_comments as special_comments


class LanguageEnvironment:
    @abc.abstractmethod
    def compile(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> None:
        """
        :throws Exception:
        """

        raise NotImplementedError

    @abc.abstractmethod
    def get_execute_command(self, path: pathlib.Path, *, basedir: pathlib.Path, tempdir: pathlib.Path) -> List[str]:
        raise NotImplementedError


class Language:
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
        return '.test.' in path.name

    @abc.abstractmethod
    def list_environments(self, path: pathlib.Path, *, basedir: pathlib.Path) -> Sequence[LanguageEnvironment]:
        raise NotImplementedError
