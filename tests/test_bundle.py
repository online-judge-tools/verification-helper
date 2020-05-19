import pathlib
import platform
import shutil
import textwrap
import unittest

import onlinejudge_verify.languages.cplusplus_bundle as cplusplus_bundle
import tests.utils
from onlinejudge_verify.languages.cplusplus_bundle import BundleError


@unittest.skipIf(platform.system() == 'Darwin', 'We cannot use the fake g++ of macOS.')
class TestStringMethods(unittest.TestCase):
    def test_no_newline(self) -> None:
        # 末尾に改行がないコードをincludeした時に改行が足されていることの確認

        files = {
            'no_newline.cpp': b'void foo() {}',
            'example.test.cpp': textwrap.dedent("""\
                #include "no_newline.cpp"
                #define PROBLEM "http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_1_B"
                """).encode(),
        }
        path = pathlib.Path('example.test.cpp')
        with tests.utils.load_files(files) as tempdir:
            with tests.utils.chdir(tempdir):
                bundler = cplusplus_bundle.Bundler(iquotes=[tempdir])
                bundler.update(path)
                self.assertIn(b'void foo() {}\n', bundler.get())

    def test_uncommenting(self) -> None:
        # prepare files
        files = {
            'foo.cpp': textwrap.dedent("""\
                void foo() {}
                """).encode(),
            'bar.cpp': textwrap.dedent("""\
                void bar() {}
                """).encode(),
            'example.test.cpp': textwrap.dedent("""\
                #include "foo.cpp"
                /*
                #include "bar.cpp"
                */
                // #include "bar.cpp"
                """).encode(),
        }
        path = pathlib.Path('example.test.cpp')
        with tests.utils.load_files(files) as tempdir:
            with tests.utils.chdir(tempdir):

                # check the result
                bundler = cplusplus_bundle.Bundler(iquotes=[tempdir])
                bundler.update(path)
                bundled = bundler.get()
                self.assertIn(b'void foo() {}', bundled)
                self.assertNotIn(b'void bar() {}', bundled)

    @unittest.skipIf(shutil.which('clang++') is None, 'clang++ is required for this test')
    def test_reject_clang(self) -> None:
        files = {
            'example.test.cpp': b'',
        }
        path = pathlib.Path('example.test.cpp')
        with tests.utils.load_files(files) as tempdir:
            with tests.utils.chdir(tempdir):
                bundler = cplusplus_bundle.Bundler(iquotes=[tempdir], compiler='clang++')
                self.assertRaises(BundleError, lambda: bundler.update(path))
