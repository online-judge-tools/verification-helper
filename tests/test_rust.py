import json
import pathlib
import textwrap
import unittest

import onlinejudge_verify.marker
import onlinejudge_verify.verify as verify
import tests.utils
from onlinejudge_verify.languages.rust import RustLanguage


class TestRustListDependencies(unittest.TestCase):
    def test_separate_crates(self) -> None:
        files = {
            pathlib.Path('rust-toolchain'): textwrap.dedent("""\
                1.42.0
                """).encode(),
            pathlib.Path('Cargo.toml'): textwrap.dedent("""\
                [workspace]
                members = ["crates/*"]
                """).encode(),
            pathlib.Path('crates', 'a', 'Cargo.toml'): textwrap.dedent("""\
                [package]
                name = "a"
                version = "0.0.0"
                edition = "2018"

                [dependencies]
                b = { path = "../b" }
                c = { path = "../c" }
                """).encode(),
            pathlib.Path('crates', 'a', 'src', 'lib.rs'): textwrap.dedent("""\
                use b::B;
                use c::C;

                pub struct A(B, C);
                """).encode(),
            pathlib.Path('crates', 'b', 'Cargo.toml'): textwrap.dedent("""\
                [package]
                name = "b"
                version = "0.0.0"
                edition = "2018"
                """).encode(),
            pathlib.Path('crates', 'b', 'src', 'lib.rs'): textwrap.dedent("""\
                pub struct B;
                """).encode(),
            pathlib.Path('crates', 'c', 'Cargo.toml'): textwrap.dedent("""\
                [package]
                name = "c"
                version = "0.0.0"
                edition = "2018"
                """).encode(),
            pathlib.Path('crates', 'c', 'src', 'lib.rs'): textwrap.dedent("""\
                pub struct C;
                """).encode(),
        }

        with tests.utils.load_files_pathlib(files) as tempdir:
            expected = sorted(tempdir / 'crates' / name / 'src' / 'lib.rs' for name in ['a', 'b', 'c'])
            actual = sorted(RustLanguage(config=None).list_dependencies(tempdir / 'crates' / 'a' / 'src' / 'lib.rs', basedir=tempdir))
            self.assertEqual(actual, expected)

    def test_mono_crate(self) -> None:
        files = {
            pathlib.Path('rust-toolchain'): textwrap.dedent("""\
                1.42.0
                """).encode(),
            pathlib.Path('Cargo.toml'): textwrap.dedent("""\
                [package]
                name = "my_competitive_library"
                version = "0.0.0"
                edition = "2018"
                """).encode(),
            pathlib.Path('src', 'lib.rs'): textwrap.dedent("""\
                pub mod a;
                pub mod b;
                pub mod c;
                """).encode(),
            pathlib.Path('src', 'a.rs'): textwrap.dedent("""\
                pub struct A;
                """).encode(),
            pathlib.Path('src', 'b.rs'): textwrap.dedent("""\
                pub struct B;
                """).encode(),
            pathlib.Path('src', 'c.rs'): textwrap.dedent("""\
                pub struct C;
                """).encode(),
        }

        with tests.utils.load_files_pathlib(files) as tempdir:
            expected = [tempdir / 'src' / f'{stem}.rs' for stem in ['a', 'b', 'c', 'lib']]

            for file_stem in ['a', 'b', 'c', 'lib']:
                actual = sorted(RustLanguage(config=None).list_dependencies(tempdir / 'src' / f'{file_stem}.rs', basedir=tempdir))
                self.assertEqual(actual, expected)


class TestRustVerification(unittest.TestCase):
    def test_success(self) -> None:
        files = {
            pathlib.Path('rust-toolchain'): textwrap.dedent("""\
                1.42.0
                """).encode(),
            pathlib.Path('Cargo.toml'): textwrap.dedent("""\
                [package]
                name = "verification"
                version = "0.0.0"
                edition = "2018"
                """).encode(),
            pathlib.Path('src', 'bin', 'library-checker-aplusb.rs'): textwrap.dedent("""\
                // verification-helper: PROBLEM https://judge.yosupo.jp/problem/aplusb

                use std::io::{self, Read as _};

                fn main() {
                    let mut input = "".to_owned();
                    io::stdin().read_to_string(&mut input).unwrap();
                    let mut input = input.split_ascii_whitespace();
                    macro_rules! read(($ty:ty) => (input.next().unwrap().parse::<$ty>().unwrap()));

                    let (a, b) = (read!(u64), read!(u64));

                    println!("{}", a + b);
                }
                """).encode(),
        }
        path = pathlib.Path('src', 'bin', 'library-checker-aplusb.rs')

        with tests.utils.load_files_pathlib(files) as tempdir:
            with tests.utils.chdir(tempdir):
                timestamps_path = tempdir / 'timestamps.json'
                with onlinejudge_verify.marker.VerificationMarker(json_path=timestamps_path, use_git_timestamp=False) as marker:
                    self.assertEqual(verify.main([path], marker=marker).failed_test_paths, [])
                with open(timestamps_path) as fh:
                    timestamps = json.load(fh)
                self.assertEqual(list(timestamps.keys()), [str(path)])
