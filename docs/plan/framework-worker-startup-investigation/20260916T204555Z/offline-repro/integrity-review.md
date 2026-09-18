# Pre-execution harness integrity review

Review completed after the test plan and harness were written and before either Cargo command ran.

## Production bindings

- `main.rs` loads the frozen candidate modules from absolute paths. The process and protocol implementations are `include!`d byte-for-byte; the wrapper does not copy or edit their bodies.
- The selected 58-file manifest was read before authoring and its SHA256 matched `419c98b437a44ce479554170bda36b40f4b8a05b3f2307361680d44fab039540`.
- `record.py` rechecks every manifest entry before and after each Cargo command and fails on drift.
- The dependency lock was copied from the already retained offline QA harness. Both Cargo commands use `--locked --offline` and a fresh target directory under this evidence root.

## Observed source path

- `process_windows.rs:158-167` turns each raw stderr read into `Incoming::Stderr { bytes, sha256 }`; the raw block is not retained in that message.
- `protocol.rs:249-272` performs process accounting and returns `profile_unqualified` for any count other than 1/1.
- `protocol.rs:288-305` performs that guard before sending an RPC.
- `protocol.rs:141-204` is the only path that consumes `Incoming::Stderr` and appends its metadata to the journal.

This ordering predicts that a 1/0 worker can return at the pre-send guard while already queued stderr metadata remains unconsumed. The receive control distinguishes that ordering from a broken pipe reader or journal writer.

## Synthetic boundary

- `synthetic-peer.exe` is the sole child path passed to `OwnedProcess::spawn`.
- The peer has two closed modes: `early-exit` and `control`. Both write the same fixed harmless stderr bytes. Neither reads credentials, profiles, installed configuration, or the network.
- The peer asserts that no `thread/` or `turn/` method is received.
- `record.py` invokes only the provided argv with `shell=False`; it does not discover or execute a Codex binary.
- No inherited candidate tests are selected or executed. This reproduction builds normal binaries and runs one purpose-built executable.

## Oracle review

The executable asserts the real child exit code, Job Object counts, unchanged session result, emitted/persisted journal equality, stderr byte count and SHA256, diagnostic objects, no thread/turn identifiers, and bounded cleanup. The success line is written only after both cases pass. These observations are produced from the runtime values; there is no hardcoded PASS flag.

## Limits

The wrapper's Cargo manifest directory differs from the product package. It exposes one adjacent function to call the unchanged private initialize RPC for SR-02. It does not test path-sensitive public runner admission and cannot identify the cause of the prior native worker exit.
