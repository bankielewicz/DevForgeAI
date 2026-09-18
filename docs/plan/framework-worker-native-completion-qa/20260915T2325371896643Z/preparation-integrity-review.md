# Preparatory integrity review

Status: provisional only. Development is still changing the candidate, so none of these observations qualifies the frozen candidate.

## Inspected scope

- Current `Cargo.toml`, README, `src/**/*.rs`, `tests/**/*.rs`, and the compiled policy JSON.
- Current test attributes/import patterns and selected new policy, source-inventory, effective-profile, review-v2, preflight protocol/CLI/recovery tests.
- QA-owned `record.py` at SHA-256 `ca6dfd8fd6d592aebd6a170ac3d722d823451f2b067277dbc640b2a5ac8c9e3c`.

## Provisional observations

- The mutable tree contained 88 physical `#[test]` attributes at the observation time. This is not the executable denominator; Cargo's frozen `--list` result will define actual unique test instances and targets.
- No `#[ignore]`, `#[should_panic]`, `mockall`, `automock`, `mock!`, common mock-decorator aliases, or Rust coverage-suppression attributes were found. Search is only a locator; frozen semantic inspection remains required.
- The only located conditional test attributes were `#[cfg(test)]` modules that bind private unit-test seams. Their referenced files and assertions must remain inside the frozen integrity inventory.
- No retry runner or ignored-test invocation was found. A scenario string containing `retry` is invalid-input data, and a process comment prohibiting retry is not a runner.
- Existing synthetic profile peers can establish compiled parsing/state-machine behavior only. They cannot qualify live Codex profile state, NI-T11 or NI-T12.
- The current fixed-policy test uses a literal ordered expected vector and digest rather than asking the product to calculate its own expected vector. Frozen QA will independently compare it with the contract and retained predecessor vector.
- A pre-freeze static concern was reported to development: a successful but unmeasurable/malformed rate-limit payload appeared able to proceed without the contract-required `not_measured` observation. Development accepted it for focused TDD before freeze. It is not a QA finding against a frozen candidate; QA will retain a separate malformed/missing/exhausted negative oracle after freeze.

## QA recorder review

- The recorder passes an argv array with `shell=False`; it does not construct a shell command.
- It creates one fresh attempt directory, byte-exact `stdout.bin` and `stderr.bin`, separate before/after complete package manifests, and a JSON receipt with argv, cwd, explicit environment overrides, executable/recorder hashes, UTC times, monotonic nanoseconds, owned PID, native exit, timeout and raw-stream sizes/hashes.
- Timeout containment targets only the recorder-owned PID and its process tree, then records the exact `taskkill.exe` argv, exit and raw streams.
- It traverses the package without following reparse points and excludes only package `target/`; QA build outputs live under this evidence root. No first-party `src` file is excluded from the planned coverage denominator.
- It uses `DEVNULL` stdin and therefore is approved only for offline noninteractive commands. It must not drive `run`, `preflight`, WN-01 or WN-02, because those operations require stdin to remain open. A separately inspected controller with the same raw receipt fields is required before any such attempt.
- The recorder records environment override values. It may receive only nonsecret QA paths such as `CARGO_TARGET_DIR` and `WF_TEST_EVIDENCE`; credential values must never be passed or retained.
- A read-only Python syntax compilation succeeded. The recorder has not launched a product command.

## Remaining frozen-candidate inspection

Re-enumerate every file from the developer manifest and independently hash it. Follow all Rust attributes, module paths, test-support binaries and assertion helpers. Confirm every WF subfixture actually executes and contributes to its parent result. Inspect the final coverage command and JSON path filters for denominator manipulation. Inspect all redaction/projection paths against byte canaries, and confirm no helper claims native behavior from synthetic peers. Any candidate drift invalidates this preparation review.

