#!/usr/bin/env bash
set -eu
set -x
pwd -P
/home/bryan/.cargo/bin/rustc --version --verbose
/home/bryan/.cargo/bin/cargo --version
/home/bryan/.cargo/bin/cargo fmt --all -- --check
/home/bryan/.cargo/bin/cargo clippy --locked --offline --all-targets -- -D warnings
/home/bryan/.cargo/bin/cargo build --locked --offline --release --bin devforgeai --bin devforgeai-indexd
sha256sum /tmp/devforgeai-index-20260914T0727264112301Z/release/devforgeai /tmp/devforgeai-index-20260914T0727264112301Z/release/devforgeai-indexd
