import pathlib
import unittest

import onlinejudge_verify.bundle as bundle
import tests.utils


class TestStringMethods(unittest.TestCase):
    def test_no_newline(self) -> None:
        # 末尾に改行がないコードをincludeした時に改行が足されていることの確認
        files = {'no_newline.cpp': b'void foo() {}', 'example.test.cpp': b'#include "no_newline.cpp"'}
        path = pathlib.Path('example.test.cpp')
        with tests.utils.load_files(files) as tempdir:
            with tests.utils.chdir(tempdir):
                bundler = bundle.Bundler(iquotes=[tempdir])
                bundler.update(path)
                self.assertIn(b'void foo() {}\n', bundler.get())