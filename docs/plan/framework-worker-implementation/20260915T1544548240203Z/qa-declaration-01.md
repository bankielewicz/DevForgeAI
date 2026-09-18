# Windows QA declaration, candidate 01

Candidate is the exact source/test/Cargo manifest inventory recorded by attempt 030-clippy (SHA-256 of candidate.json: 0367a068dddf0f4408df4e54259ab06fbb91f85001d41b7c2d7c81a944b69326). Each later command also captures its own candidate manifest; source changes invalidate this campaign for the changed candidate.

Required platform: native Windows, this C: checkout. Required offline cases: WF-01 through WF-20, one case each; every section 8 subfixture is mandatory. Supplemental tests do not inflate the denominator of 20. Native WN-01/WN-02 remain separately NOT_RUN (0 demonstrated passes / 2 required native cases). Framework acceptance NOT_EVALUATED.

Line denominator: every first-party executable line emitted by llvm-cov for this package's `src/` files, including main.rs, request/profile, protocol, process_windows, journal, runner and oracle. Exclude only tests/support/test fixtures, generated/vendor/dependency code. No runtime source exclusions. Enumerate all src files against the full JSON coverage export, retaining raw per-file counts. Required executed-line percentage >=95%; required-case rate >=95% AND every mandatory case/subfixture must pass.

Collector: discovered cargo-llvm-cov 0.8.4 on Rust 1.97.1, `cargo llvm-cov --locked --offline --all-targets --json --output-path <this root>/coverage-01.json`. No ignore-filename filter. This runs the full tests, including the 120-second watchdog and native Windows test peer processes. Explicit separate noninstrumented all-targets regression will also run on the frozen final candidate.

Branch coverage: NOT_RUN in this stable-toolchain campaign. Collector help labels --branch unstable; no nightly installation or claim of measured branches is made. The JSON branch fields will be reported as emitted, without interpreting a zero denominator as coverage.

No native Codex startup/authentication/account/configuration examination is part of this campaign. Synthetic review tests inspect only test-authored files.
