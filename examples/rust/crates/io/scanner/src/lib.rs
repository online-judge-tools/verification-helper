//! A quite simple input scanner.
//!
//! ```no_run
//! use scanner::Scanner;
//!
//! let mut sc = Scanner::from_stdin();
//! let _: u64 = sc.read();
//! ```

use std::{
    any, fmt,
    io::{self, Read as _},
    str::{FromStr, SplitAsciiWhitespace},
};

/// A quite simple input scanner.
pub struct Scanner {
    tokens: SplitAsciiWhitespace<'static>,
}

impl Scanner {
    /// Constructs a new `Self` with while input from stdin.
    ///
    /// # Panics
    ///
    /// Panics if an IO error occurred.
    pub fn from_stdin() -> Self {
        let mut input = "".to_owned();
        io::stdin().read_to_string(&mut input).unwrap();
        Self {
            tokens: Box::leak(input.into_boxed_str()).split_ascii_whitespace(),
        }
    }

    /// Consumes and parses the next token.
    ///
    /// # Panics
    ///
    /// Panics if:
    ///
    /// - no token left
    /// - failed to parse the token
    pub fn read<T>(&mut self) -> T
    where
        T: FromStr,
        T::Err: fmt::Display,
    {
        let token = self.tokens.next().expect("reached EOF");
        token.parse().unwrap_or_else(|err| {
            panic!(
                "could not parse {:?} as `{}`: {}",
                token,
                any::type_name::<T>(),
                err,
            );
        })
    }
}
