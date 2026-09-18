# NI-T07 fixed launch-policy slice

Status: **COMPLETE for the selected fixed-policy implementation slice**. Full native-readiness QA, effective-profile qualification, Codex execution, native trials, coverage, and framework acceptance remain outside this child slice.

## Delivered behavior

- `src/restrictive-launch-policy.json` is a compiled, closed four-field record: schema version, final policy ID, pinned adapter, and fixed argv.
- The policy ID is `codex-0.154.0-readonly-no-external-tools-v2`; the exact record SHA-256 is `1dbc48c4a3627f7c5fc7a996935ec507426e4cd90adac058eb81100ac9b526b5`.
- The argument vector retains every selected proposed override and appends the selected fixed `sandbox_mode=\"read-only\"` and `approval_policy=\"never\"` settings.
- `launch_policy::args` returns the compiled vector only for adapter `codex-0.154.0-stdio`, request schema 2, the exact final policy ID, and the exact compiled-record digest. Every mismatch returns `profile_unqualified`.
- `REQUIRED_DISABLED_FEATURES` exposes exactly 35 feature names that downstream preflight logic must observe as disabled: the original fourteen, followed by 21 additional baseline-enabled effect-capable names in lexical order.
- No caller-supplied record, configuration map, argument suffix, or alternate adapter is accepted by this API.

## TDD and focused verification

| Attempt | Result | Evidence |
| --- | --- | --- |
| Red: focused integration test before module/export existed | Expected compile failure, Cargo exit 101, unresolved `launch_policy` import only | `01-red/` |
| Green: focused integration test | PASS, 2/2 | `02-green/` |
| Package rustfmt check during concurrent work | FAIL because unowned concurrent `tests/preflight_cli.rs` was not formatted; owned files had no listed diff | `03-format-check/` |
| Requested file arguments through Cargo fmt | Same concurrent unowned failure because Cargo fmt still selected the package | `04-owned-format-check/` |
| Refactor focused integration test | PASS, 2/2 | `05-refactor-test/` |
| Focused Clippy with warnings denied | PASS | `06-focused-clippy/` |
| Direct rustfmt check of the two owned Rust files | PASS | `07-owned-rustfmt/` |
| Feature-extension Red against the original fourteen-name policy | Expected FAIL, 1/2; the independent 35-name oracle observed the missing 21 entries | `08-extension-red/` |
| Feature-extension Green | PASS, 2/2 | `09-extension-green/` |
| Final owned rustfmt after the extension | PASS | `10-extension-format/` |
| Final focused Clippy after the extension | PASS with warnings denied | `11-extension-clippy/` |

All attempts retain exact argv and cwd, native process exit, UTC start/end, elapsed duration, raw `stdout.bin` and `stderr.bin`, tool digest, and a package candidate manifest. The two format failures are retained and are not represented as product failures in this slice.

The independent expected vector in `tests/launch_policy.rs` checks every positional argument and every `-c` pair, all 35 required-disabled features, the four-field record value, and the expected digest. Negative cases cover peer/unsupported adapter, schema 1, schema 3, wrong policy ID, malformed digest, and wrong valid-length digest.

## Source readback

Exact final child-slice hashes are retained in `source-readback.json`. `src/lib.rs` also contains concurrent `effective_profile` and `profile_sources` exports outside this slice; this child changed only the `launch_policy` export there.

## Remaining integration

The parent implementation must call `launch_policy::args` at the native schema-v2 launch boundary and independently qualify observed effective settings before launching a trial. This slice did not run Codex or claim policy effectiveness from the compiled argv alone.

Framework acceptance: **NOT_EVALUATED**.
