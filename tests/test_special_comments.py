import textwrap
import unittest
from typing import *

import onlinejudge_verify.languages.special_comments as special_comments
import tests.utils


class TestSpecialComments(unittest.TestCase):
    """Unit tests for languages/special_comments.py
    """
    def test_list_embedded_urls(self) -> None:
        files = {
            'main.cpp': textwrap.dedent("""\
                // URL with quotes
                #define PROBLEM "http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_1_A"
                // url='https://atcoder.jp/'
                // `https://atcoder.jp/contests/abc001`
                //
                // URL without quotes
                // @see https://atcoder.jp/contests/abc002
                //
                // URL with quotes and extra characters
                // {"url": "https://atcoder.jp/contests/abc003"}
                // ('https://atcoder.jp/contests/abc004')
                //
                // URL with opening quote and without closing quote
                // "https://atcoder.jp/contests/abc005
                """).encode(),
        }
        expected = [
            'http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_1_A',
            'https://atcoder.jp/',
            'https://atcoder.jp/contests/abc001',
            'https://atcoder.jp/contests/abc002',
            'https://atcoder.jp/contests/abc003',
            'https://atcoder.jp/contests/abc004',
            'https://atcoder.jp/contests/abc005',
        ]

        with tests.utils.load_files(files) as tempdir:
            with tests.utils.chdir(tempdir):
                file_path = tempdir / 'main.cpp'
                actual = sorted(special_comments.list_embedded_urls(file_path))
                self.assertEqual(actual, expected)
