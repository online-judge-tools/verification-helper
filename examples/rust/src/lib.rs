//! Re-exports the crates for rustdoc.
//!
//! This crate itself is not intended to be used directly.

// With `custom-build` and `syn` crate, we can expand crate-level rustdocs.

macro_rules! re_export(($($name:ident),* $(,)?) => ($(pub mod $name { pub use ::$name::*; })*));

pub mod helloworld {
    //! Crates of "hello" and "world".

    re_export!(hello, world);
}

pub mod io {
    //! Crates about IO.

    re_export!(input, scanner);
}
