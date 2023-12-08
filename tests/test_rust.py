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
                1.70.0
                """).encode(),
            pathlib.Path('Cargo.toml'): textwrap.dedent("""\
                [workspace]
                members = ["verification"]

                [package]
                name = "my_competitive_library"
                version = "0.0.0"
                edition = "2018"

                [dependencies]
                my-competitive-library-a = { path = "./crates/a" }
                my-competitive-library-b = { path = "./crates/b" }
                my-competitive-library-c = { path = "./crates/c" }
                """).encode(),
            pathlib.Path('src', 'lib.rs'): textwrap.dedent("""\
                macro_rules! re_export(($($name:ident),* $(,)?) => ($(pub mod $name { pub use $name::*; })*));
                re_export!(a, b, c);
                """).encode(),
            pathlib.Path('crates', 'a', 'Cargo.toml'): textwrap.dedent("""\
                [package]
                name = "my-competitive-library-a"
                version = "0.0.0"
                edition = "2018"

                [lib]
                name = "a"

                [dependencies]
                my-competitive-library-b = { path = "../b" }
                my-competitive-library-c = { path = "../c" }
                """).encode(),
            pathlib.Path('crates', 'a', 'src', 'lib.rs'): textwrap.dedent("""\
                use b::B;
                use c::C;

                pub struct A(B, C);
                """).encode(),
            pathlib.Path('crates', 'b', 'Cargo.toml'): textwrap.dedent("""\
                [package]
                name = "my-competitive-library-b"
                version = "0.0.0"
                edition = "2018"

                [lib]
                name = "b"
                """).encode(),
            pathlib.Path('crates', 'b', 'src', 'lib.rs'): textwrap.dedent("""\
                pub struct B;
                """).encode(),
            pathlib.Path('crates', 'c', 'Cargo.toml'): textwrap.dedent("""\
                [package]
                name = "my-competitive-library-c"
                version = "0.0.0"
                edition = "2018"

                [lib]
                name = "c"
                """).encode(),
            pathlib.Path('crates', 'c', 'src', 'lib.rs'): textwrap.dedent("""\
                pub struct C;
                """).encode(),
            pathlib.Path('verification', 'Cargo.toml'): textwrap.dedent("""\
                [package]
                name = "verification"
                version = "0.0.0"
                edition = "2018"

                [dependencies]
                my-competitive-library-a = { path = "../crates/a" }
                """).encode(),
            pathlib.Path('verification', 'src', 'bin', 'aizu-online-judge-itp1-1-a.rs'): textwrap.dedent("""\
                // verification-helper: PROBLEM http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_1_A

                use a as _;

                fn main() {
                    println!("Hello World");
                }
                """).encode(),
        }

        with tests.utils.load_files_pathlib(files) as tempdir:

            def sub_crate_src_path(crate_name: str) -> pathlib.Path:
                return tempdir / 'crates' / crate_name / 'src' / 'lib.rs'

            top_lib_src_path = tempdir / 'src' / 'lib.rs'
            verification_src_path = tempdir / 'verification' / 'src' / 'bin' / 'aizu-online-judge-itp1-1-a.rs'

            expected = [sub_crate_src_path('a'), sub_crate_src_path('b'), sub_crate_src_path('c'), top_lib_src_path]
            actual = sorted(RustLanguage(config=None).list_dependencies(top_lib_src_path, basedir=tempdir))
            self.assertEqual(actual, expected)

            expected = [sub_crate_src_path('a'), sub_crate_src_path('b'), sub_crate_src_path('c')]
            actual = sorted(RustLanguage(config=None).list_dependencies(sub_crate_src_path('a'), basedir=tempdir))
            self.assertEqual(actual, expected)

            for src_path in [sub_crate_src_path('b'), sub_crate_src_path('c')]:
                expected = [src_path]
                actual = sorted(RustLanguage(config=None).list_dependencies(src_path, basedir=tempdir))
                self.assertEqual(actual, expected)

            expected = [sub_crate_src_path('a'), verification_src_path]
            actual = sorted(RustLanguage(config=None).list_dependencies(verification_src_path, basedir=tempdir))
            self.assertEqual(actual, expected)

    def test_separate_workspaces(self) -> None:
        files = {
            pathlib.Path('rust-toolchain'): textwrap.dedent("""\
                1.70.0
                """).encode(),
            pathlib.Path('Cargo.toml'): textwrap.dedent("""\
                [workspace]

                [package]
                name = "my_competitive_library"
                version = "0.0.0"
                edition = "2018"

                [dependencies]
                my-competitive-library-a = { path = "./crates/a" }
                """).encode(),
            pathlib.Path('src', 'lib.rs'): textwrap.dedent("""\
                macro_rules! re_export(($($name:ident),* $(,)?) => ($(pub mod $name { pub use $name::*; })*));
                re_export!(a);
                """).encode(),
            pathlib.Path('crates', 'a', 'Cargo.toml'): textwrap.dedent("""\
                [package]
                name = "my-competitive-library-a"
                version = "0.0.0"
                edition = "2018"

                [lib]
                name = "a"
                """).encode(),
            pathlib.Path('crates', 'a', 'src', 'lib.rs'): b'',
            pathlib.Path('verification', 'aizu-online-judge', 'Cargo.toml'): textwrap.dedent("""\
                [workspace]

                [package]
                name = "aizu-online-judge"
                version = "0.0.0"
                edition = "2018"

                [dependencies]
                my-competitive-library-a = { path = "../../crates/a" }
                """).encode(),
            pathlib.Path('verification', 'aizu-online-judge', 'src', 'bin', 'itp1-1-a.rs'): textwrap.dedent("""\
                // verification-helper: PROBLEM http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_1_A

                use a as _;

                fn main() {
                    println!("Hello World");
                }
                """).encode(),
        }

        with tests.utils.load_files_pathlib(files) as tempdir:
            top_lib_src_path = tempdir / 'src' / 'lib.rs'
            sub_lib_src_path = tempdir / 'crates' / 'a' / 'src' / 'lib.rs'
            verification_src_path = tempdir / 'verification' / 'aizu-online-judge' / 'src' / 'bin' / 'itp1-1-a.rs'

            expected = [sub_lib_src_path, top_lib_src_path]
            actual = sorted(RustLanguage(config=None).list_dependencies(top_lib_src_path, basedir=tempdir))
            self.assertEqual(actual, expected)

            expected = [sub_lib_src_path]
            actual = sorted(RustLanguage(config=None).list_dependencies(sub_lib_src_path, basedir=tempdir))
            self.assertEqual(actual, expected)

            expected = [sub_lib_src_path, verification_src_path]
            actual = sorted(RustLanguage(config=None).list_dependencies(verification_src_path, basedir=tempdir))
            self.assertEqual(actual, expected)

    def test_gathered_source_files(self) -> None:
        files = {
            pathlib.Path('rust-toolchain'): textwrap.dedent("""\
                1.70.0
                """).encode(),
            pathlib.Path('Cargo.toml'): textwrap.dedent("""\
                [workspace]
                members = ["verification"]

                [package]
                name = "my_competitive_library"
                version = "0.0.0"
                edition = "2018"

                [dependencies]
                my-competitive-library-a = { path = "./crates/manifests/a" }
                my-competitive-library-b = { path = "./crates/manifests/b" }
                my-competitive-library-c = { path = "./crates/manifests/c" }
                """).encode(),
            pathlib.Path('src', 'lib.rs'): textwrap.dedent("""\
                macro_rules! re_export(($($name:ident),* $(,)?) => ($(pub mod $name { pub use $name::*; })*));
                re_export!(a, b, c);
                """).encode(),
            pathlib.Path('crates', 'manifests', 'a', 'Cargo.toml'): textwrap.dedent("""\
                [package]
                name = "my-competitive-library-a"
                version = "0.0.0"
                edition = "2018"

                [lib]
                name = "a"
                path = "../../sourcefiles/a.rs"

                [dependencies]
                my-competitive-library-b = { path = "../b" }
                my-competitive-library-c = { path = "../c" }
                """).encode(),
            pathlib.Path('crates', 'manifests', 'b', 'Cargo.toml'): textwrap.dedent("""\
                [package]
                name = "my-competitive-library-b"
                version = "0.0.0"
                edition = "2018"

                [lib]
                name = "b"
                path = "../../sourcefiles/b.rs"
                """).encode(),
            pathlib.Path('crates', 'manifests', 'c', 'Cargo.toml'): textwrap.dedent("""\
                [package]
                name = "my-competitive-library-c"
                version = "0.0.0"
                edition = "2018"

                [lib]
                name = "c"
                path = "../../sourcefiles/c.rs"
                """).encode(),
            pathlib.Path('crates', 'sourcefiles', 'a.rs'): textwrap.dedent("""\
                use b::B;
                use c::C;

                pub struct A(B, C);
                """).encode(),
            pathlib.Path('crates', 'sourcefiles', 'b.rs'): textwrap.dedent("""\
                pub struct B;
                """).encode(),
            pathlib.Path('crates', 'sourcefiles', 'c.rs'): textwrap.dedent("""\
                pub struct C;
                """).encode(),
            pathlib.Path('verification', 'Cargo.toml'): textwrap.dedent("""\
                [package]
                name = "verification"
                version = "0.0.0"
                edition = "2018"

                [dependencies]
                my-competitive-library-a = { path = "../crates/manifests/a" }
                """).encode(),
            pathlib.Path('verification', 'src', 'bin', 'aizu-online-judge-itp1-1-a.rs'): textwrap.dedent("""\
                // verification-helper: PROBLEM http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_1_A

                use a as _;

                fn main() {
                    println!("Hello World");
                }
                """).encode(),
        }

        with tests.utils.load_files_pathlib(files) as tempdir:

            def sub_lib_src_path(crate_name: str) -> pathlib.Path:
                return tempdir / 'crates' / 'sourcefiles' / f'{crate_name}.rs'

            top_lib_src_path = tempdir / 'src' / 'lib.rs'
            verification_src_path = tempdir / 'verification' / 'src' / 'bin' / 'aizu-online-judge-itp1-1-a.rs'

            expected = [*map(sub_lib_src_path, ['a', 'b', 'c']), top_lib_src_path]
            actual = sorted(RustLanguage(config=None).list_dependencies(top_lib_src_path, basedir=tempdir))
            self.assertEqual(actual, expected)

            expected = list(map(sub_lib_src_path, ['a', 'b', 'c']))
            actual = sorted(RustLanguage(config=None).list_dependencies(sub_lib_src_path('a'), basedir=tempdir))
            self.assertEqual(actual, expected)

            for src_path in map(sub_lib_src_path, ['b', 'c']):
                expected = [src_path]
                actual = sorted(RustLanguage(config=None).list_dependencies(src_path, basedir=tempdir))
                self.assertEqual(actual, expected)

            expected = [sub_lib_src_path('a'), verification_src_path]
            actual = sorted(RustLanguage(config=None).list_dependencies(verification_src_path, basedir=tempdir))
            self.assertEqual(actual, expected)

    def test_mono_package(self) -> None:
        files = {
            pathlib.Path('rust-toolchain'): textwrap.dedent("""\
                1.70.0
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
            pathlib.Path('src', 'a.rs'): b'',
            pathlib.Path('src', 'b.rs'): b'',
            pathlib.Path('src', 'c.rs'): b'',
            pathlib.Path('examples', 'aizu-online-judge-itp1-1-a.rs'): textwrap.dedent("""\
                // verification-helper: PROBLEM http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ITP1_1_A

                use my_competitive_library as _;

                fn main() {
                    println!("Hello World");
                }
                """).encode(),
        }

        with tests.utils.load_files_pathlib(files) as tempdir:
            expected = [tempdir / 'src' / f'{stem}.rs' for stem in ['a', 'b', 'c', 'lib']]

            for file_stem in ['a', 'b', 'c', 'lib']:
                actual = sorted(RustLanguage(config=None).list_dependencies(tempdir / 'src' / f'{file_stem}.rs', basedir=tempdir))
                self.assertEqual(actual, expected)

            expected = sorted([*expected, tempdir / 'examples' / 'aizu-online-judge-itp1-1-a.rs'])
            actual = sorted(RustLanguage(config=None).list_dependencies(tempdir / 'examples' / 'aizu-online-judge-itp1-1-a.rs', basedir=tempdir))
            self.assertEqual(actual, expected)

    def test_external_crates(self) -> None:
        files = {
            pathlib.Path('rust-toolchain'): textwrap.dedent("""\
                1.70.0
                """).encode(),
            pathlib.Path('Cargo.toml'): textwrap.dedent("""\
                [package]
                name = "my_competitive_library"
                version = "0.0.0"
                edition = "2018"

                [dependencies]
                ac-library-rs = { git = "https://github.com/rust-lang-ja/ac-library-rs", rev = "19509cd5103313b884f89b3001510d5155bbb4db" }
                maplit = "=1.0.2"
                """).encode(),
            pathlib.Path('src', 'lib.rs'): textwrap.dedent("""\
                use {ac_library_rs as _, maplit as _};
                """).encode(),
        }

        with tests.utils.load_files_pathlib(files) as tempdir:
            src_path = tempdir / 'src' / 'lib.rs'

            expected = [src_path]
            actual = sorted(RustLanguage(config=None).list_dependencies(src_path, basedir=tempdir))
            self.assertEqual(actual, expected)

    def test_build_dependencies(self) -> None:
        files = {
            pathlib.Path('rust-toolchain'): textwrap.dedent("""\
                1.70.0
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

                [build-dependencies]
                b = { path = "../b" }
                """).encode(),
            pathlib.Path('crates', 'a', 'build.rs'): textwrap.dedent("""\
                use std::{env, fs, path::PathBuf};

                fn main() {
                    let out_dir = PathBuf::from(env::var_os("OUT_DIR").unwrap());
                    fs::write(out_dir.join("message.txt"), b::MESSAGE).unwrap();
                }
                """).encode(),
            pathlib.Path('crates', 'a', 'src', 'lib.rs'): textwrap.dedent("""\
                pub fn print_message() {
                    println!("{}", include_str!(concat!(env!("OUT_DIR"), "/message.txt")));
                }
                """).encode(),
            pathlib.Path('crates', 'b', 'Cargo.toml'): textwrap.dedent("""\
                [package]
                name = "b"
                version = "0.0.0"
                edition = "2018"
                """).encode(),
            pathlib.Path('crates', 'b', 'src', 'lib.rs'): textwrap.dedent("""\
                pub static MESSAGE: &str = "hi";
                """).encode(),
        }

        with tests.utils.load_files_pathlib(files) as tempdir:

            def build_src_path(package_name: str) -> pathlib.Path:
                return tempdir / 'crates' / package_name / 'build.rs'

            def lib_src_path(package_name: str) -> pathlib.Path:
                return tempdir / 'crates' / package_name / 'src' / 'lib.rs'

            for src_path in [build_src_path('a'), lib_src_path('a')]:
                actual = RustLanguage(config=None).list_dependencies(src_path, basedir=tempdir)
                generated_file = next((tempdir / 'target' / 'debug' / 'build').rglob('message.txt'))
                expected = sorted([build_src_path('a'), lib_src_path('a'), lib_src_path('b'), generated_file])
                self.assertEqual(actual, expected)

            expected = [generated_file]
            actual = RustLanguage(config=None).list_dependencies(generated_file, basedir=tempdir)
            self.assertEqual(actual, expected)

            expected = [lib_src_path('b')]
            actual = sorted(RustLanguage(config=None).list_dependencies(lib_src_path('b'), basedir=tempdir))
            self.assertEqual(actual, expected)


class TestRustVerification(unittest.TestCase):
    def test_success(self) -> None:
        files = {
            pathlib.Path('rust-toolchain'): textwrap.dedent("""\
                1.70.0
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
