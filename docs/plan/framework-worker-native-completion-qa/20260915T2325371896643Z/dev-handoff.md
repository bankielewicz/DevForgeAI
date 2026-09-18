# QA remediation handoff to dev

## Selected candidate and authority

- **QA report:** `qa-report.md` in this directory.
- **Frozen candidate:** 48-entry manifest SHA-256 `809a8beb50f8b57198a963725fd0d2ccd5e586a1243e177284bff3d6dfa471dd`.
- **Contracts:** feasibility `7cb5b0cb87e515bb4d59235b615922ab4ea07ef607b8111dde6cc73c8f101b23`; native readiness `c3c0673cbf95ae7aa056d9fd0009ce89947309b943013fd7838438d6ee66b06d`; preflight `6e781f23f221d1033896716512e9162579653b529d107e0040d49c499574afd1`.
- **Confirmed defect:** `QA-F-COV-01`, `METRIC_FAILURE` under the mandatory 95% first-party executed-line floor.
- **Remediation owner:** dev. Product, developer-test and test-fixture changes must follow red/green/refactor/QA. This handoff does not authorize installation, operational configuration changes, threshold changes, source exclusions or native trials.

## QA-F-COV-01

- **Observed result:** `2,852/3,103 = 91.91105381888495004834031582%` from a complete exit-zero `cargo llvm-cov --locked --offline --all-targets --json` collection. The current denominator needs at least `2,948` covered lines, a shortfall of `96`.
- **Evidence:** `08a-coverage/coverage.json` SHA-256 `271212ab24ab2939f4a595103c9978c2d451dc826fecfe341da06d5d4c3dc3b8`; `08a-coverage/receipt.json`; `09-coverage-analysis/stdout.bin`; retained `target-coverage/llvm-cov-target/*.profraw` inventory and hashes.
- **Largest per-file gaps:** `effective_profile.rs` 485/573; `runner.rs` 145/178; `profile_sources.rs` 420/462; `main.rs` 122/132. Root cause is not established by line counts alone.
- **Expected correction:** add meaningful requirements-derived tests and, only where justified by a product defect, correct behavior so at least 95% of every declared first-party executable line is exercised. Do not exclude source, duplicate/retry cases, weaken assertions, alter thresholds or copy implementation logic into the oracle.
- **Preservation:** keep all existing WF, NI, F-01 and F-02 behavior passing; preserve typed-field redaction, fail-closed policy, source immutability, process cleanup and native-attempt counters.
- **Required dev return:** corrected source manifest, changed-file manifest, red/green/refactor receipts, exact full-suite counts, raw coverage JSON/profraw and known remaining gaps. Developer evidence does not close this independent finding.
- **Independent retest:** verify the new manifest and test integrity; run the complete locked all-target suite, rustfmt, Clippy and one fresh full-source coverage collection. Coverage must be at least 95% at full precision. Rerun affected negative/regression cases. Do not reuse the old metric for changed bytes.

## Work stopped and still required

- Frozen-candidate live `profile-sources`: NOT_RUN after the terminal metric stop.
- NI-T05 actual pre-launch recheck and NI-T09/NI-T10 installed-profile/live portions: BLOCKED.
- WN-01 and WN-02: NOT_RUN, zero attempts consumed.
- QA-owned supplemental F-02 and retained-evidence helpers: NOT_RUN after the stop; the required compiled regression function itself passed.
- Framework acceptance authority: deferred and NOT_EVALUATED.

Once corrected-candidate offline QA passes, resolve the installed source/profile prerequisite through the compiled collector, perform the live preflight, and only then select the two bounded native trials under their zero-retry rules.

