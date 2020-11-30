//! Re-exports the crates for rustdoc.
pub mod helloworld {
    //! Crates of "hello" and "world".
    pub mod hello {
        //! A re-export of `verification-helper-rust-example-hello`.
        pub use hello::*;
    }
    pub mod world {
        //! A re-export of `verification-helper-rust-example-world`.
        pub use world::*;
    }
}
pub mod io {
    //! Crates about IO.
    pub mod input {
        //! A re-export of `verification-helper-rust-example-input`.
        pub use input::*;
    }
    pub mod scanner {
        //! A re-export of `verification-helper-rust-example-scanner`.
        pub use scanner::*;
    }
}
