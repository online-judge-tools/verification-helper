//! Re-exports the crates for rustdoc.

pub mod hello {
    //! A re-export of `verification-helper-rust-example-hello`.

    pub use hello::*;
}

pub mod world {
    //! A re-export of `verification-helper-rust-example-world`.

    pub use world::*;
}
