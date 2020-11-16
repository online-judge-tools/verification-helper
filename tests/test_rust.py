import json
import pathlib
import textwrap
import unittest
from typing import *

import onlinejudge_verify.marker
import onlinejudge_verify.verify as verify
import tests.utils
from onlinejudge_verify.languages.rust import RustLanguage


class TestRustListDependencies(unittest.TestCase):
    def test_success(self) -> None:
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

        with _load_files_nocheck(files) as tempdir:
            expected = sorted(tempdir / 'crates' / name / 'src' / 'lib.rs' for name in ['a', 'b', 'c'])
            actual = sorted(RustLanguage(config=None).list_dependencies(tempdir / 'crates' / 'a' / 'src' / 'lib.rs', basedir=tempdir))
            self.assertEqual(actual, expected)


class TestRustVerification(unittest.TestCase):
    def test_success(self) -> None:
        files = {
            pathlib.Path('rust-toolchain'): textwrap.dedent("""\
                1.42.0
                """).encode(),
            pathlib.Path('Cargo.toml'): textwrap.dedent("""\
                [workspace]
                members = ["crates/*", "verification/*"]
                """).encode(),
            pathlib.Path('crates', 'hello', 'Cargo.toml'): textwrap.dedent("""\
                [package]
                name = "hello"
                version = "0.0.0"
                edition = "2018"
                """).encode(),
            pathlib.Path('crates', 'hello', 'src', 'lib.rs'): textwrap.dedent("""\
                pub static HELLO: &str = "Hello";
                """).encode(),
            pathlib.Path('crates', 'world', 'Cargo.toml'): textwrap.dedent("""\
                [package]
                name = "world"
                version = "0.0.0"
                edition = "2018"
                """).encode(),
            pathlib.Path('crates', 'world', 'src', 'lib.rs'): textwrap.dedent("""\
                pub static WORLD: &str = "World";
                """).encode(),
            pathlib.Path('verification', 'yukicoder', 'Cargo.toml'): textwrap.dedent("""\
                [package]
                name = "yukicoder"
                version = "0.0.0"
                edition = "2018"

                [dependencies]
                hello = { path = "../../crates/hello" }
                world = { path = "../../crates/world" }
                """).encode(),
            pathlib.Path('verification', 'yukicoder', 'src', 'bin', '9000.rs'): textwrap.dedent("""\
                // verification-helper: PROBLEM https://yukicoder.me/problems/no/9000

                fn main() {
                    println!("{} {}!", hello::HELLO, world::WORLD);
                }
                """).encode(),
        }
        paths = [pathlib.Path('verification', 'yukicoder', 'src', 'bin', '9000.rs')]

        with _load_files_nocheck(files) as tempdir:
            with tests.utils.chdir(tempdir):
                timestamps_path = tempdir / 'timestamps.json'
                with onlinejudge_verify.marker.VerificationMarker(json_path=timestamps_path, use_git_timestamp=False) as marker:
                    self.assertEqual(verify.main(paths, marker=marker).failed_test_paths, [])
                with open(timestamps_path) as fh:
                    timestamps = json.load(fh)
                self.assertEqual(list(timestamps.keys()), [])


def _load_files_nocheck(files: Dict[pathlib.Path, bytes]) -> ContextManager[pathlib.Path]:
    return tests.utils.load_files_pathlib(files)
