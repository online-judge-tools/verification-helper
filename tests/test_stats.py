"""This module has tests for the stats subcommand.
"""

import unittest

import onlinejudge_verify.main


class TestStatsSubcommandSmoke(unittest.TestCase):
    """TestStatsSubcommandSmoke is a smoke tests of `stats` subcommand.
    """
    def test_run(self) -> None:
        onlinejudge_verify.main.subcommand_stats()
