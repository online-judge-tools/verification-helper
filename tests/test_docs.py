"""This module has tests for the docs subcommand.
"""

import unittest

import onlinejudge_verify.main


class TestDocsSubcommandSmoke(unittest.TestCase):
    """TestDocsSubcommandSmoke is a smoke tests of `docs` subcommand.
    """
    def test_run(self) -> None:
        onlinejudge_verify.main.subcommand_docs()
