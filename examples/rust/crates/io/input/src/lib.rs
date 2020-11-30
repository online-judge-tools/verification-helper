//! A limited `input!` macro.
//!
//! ```no_run
//! use input::input;
//!
//! input! {
//!     a: u32,
//!     b: u32,
//! }
//! ```

pub use scanner::Scanner;

/// A limited `input!` macro.
#[macro_export]
macro_rules! input {
    ($($var:ident : $ty:ty),* $(,)?) => {
        let mut __scanner = $crate::Scanner::from_stdin();
        $(
            let $var = __scanner.read::<$ty>();
        )*
    };
}
