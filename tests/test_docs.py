"""This module has tests for the docs subcommand.
"""

import pathlib
import random
import textwrap
import unittest
from typing import *

import onlinejudge_verify.main
import tests.utils as utils


class TestDocsSubcommandSmoke(unittest.TestCase):
    """TestDocsSubcommandSmoke is a class for smoke tests of `docs` subcommand.
    """
    def test_run(self) -> None:
        onlinejudge_verify.main.subcommand_docs()


class TestDocsSubcommand(unittest.TestCase):
    """TestDocsSubcommand is a class for end-to-end tests of `docs` subcommand.
    """
    def test_documentation_of(self) -> None:
        get_random_string = lambda: ''.join([random.choice('0123456789abcdef') for _ in range(64)])
        random_relative_hpp = get_random_string()
        random_absolute_hpp = get_random_string()
        random_unsupported_absolute_hpp = get_random_string()
        random_no_document_hpp = get_random_string()
        random_relative_md = get_random_string()
        random_absolute_md = get_random_string()
        random_unsupported_absolute_md = get_random_string()
        random_standalone_page_md = get_random_string()

        files = {
            pathlib.Path('src', 'a', 'b', 'relative.hpp'): random_relative_hpp.encode(),
            pathlib.Path('src', 'a', 'b', 'absolute.hpp'): random_absolute_hpp.encode(),
            pathlib.Path('src', 'a', 'b', 'unsupported-absolute.hpp'): random_unsupported_absolute_hpp.encode(),
            pathlib.Path('src', 'a', 'b', 'no-document.hpp'): random_no_document_hpp.encode(),
            pathlib.Path('docs', 'x', 'y', 'relative.md'): textwrap.dedent(f"""\
                ---
                title: relative.md
                documentation_of: ../../../src/a/b/relative.hpp
                ---

                {random_relative_md}
                """).encode(),
            pathlib.Path('docs', 'x', 'y', 'unsupported-absolute.md'): textwrap.dedent(f"""\
                ---
                title: unsupported-absolute.md
                documentation_of: src/a/b/unsupported-absolute.hpp
                ---

                {random_unsupported_absolute_md}
                """).encode(),
            pathlib.Path('docs', 'x', 'y', 'absolute.md'): textwrap.dedent(f"""\
                ---
                title: absolute.md
                documentation_of: //src/a/b/absolute.hpp
                ---

                {random_absolute_md}
                """).encode(),
            pathlib.Path('docs', 'x', 'y', 'standalone-page.md'): textwrap.dedent(f"""\
                ---
                title: standalone page
                ---

                {random_standalone_page_md}
                """).encode(),
        }

        destination_dir = pathlib.Path('.verify-helper', 'markdown')
        expected: Dict[pathlib.Path, List[str]] = {
            destination_dir / 'src' / 'a' / 'b' / 'relative.hpp.md': [random_relative_hpp, random_relative_md],
            destination_dir / 'src' / 'a' / 'b' / 'absolute.hpp.md': [random_absolute_hpp, random_absolute_md],
            destination_dir / 'src' / 'a' / 'b' / 'unsupported-absolute.hpp.md': [random_unsupported_absolute_hpp, random_unsupported_absolute_md],
            destination_dir / 'src' / 'a' / 'b' / 'no-document.hpp.md': [random_no_document_hpp],
            destination_dir / 'docs' / 'x' / 'y' / 'standalone-page.md': [random_standalone_page_md],
        }

        with utils.load_files_pathlib(files) as tempdir:
            with utils.chdir(tempdir):
                onlinejudge_verify.main.subcommand_docs()
                for path, keywords in expected.items():
                    self.assertTrue((tempdir / path).exists())
                    with open(tempdir / path) as fh:
                        content = fh.read()
                    for keyword in keywords:
                        self.assertIn(keyword, content)
