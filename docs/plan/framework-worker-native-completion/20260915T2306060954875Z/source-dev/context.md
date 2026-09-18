# Profile-source inventory development evidence

- Owned production file: `devforgeai/experiments/codex-worker-probe/src/profile_sources.rs`
- Owned test file: `devforgeai/experiments/codex-worker-probe/tests/support/profile_sources_cases.rs`
- Scope: digest-only, fixed-root profile source inventory and freshness verification for NI-T08/NI-T10.
- Test filter: `profile_sources::cases`.
- No credential contents, operational configuration writes, or native processes are permitted in this slice.

## Retained attempts

- `01-red`: setup failure, not a valid red; another concurrently exported module did not yet exist.
- `02-red-valid`: valid red, 0/5 cases passed against the explicit not-implemented result.
- `03-green`: transitional result, 3/5 passed; existing-file normalization appended an invalid empty suffix.
- `04-green`: the initial five cases passed.
- `05-shape-red`: valid focused red for malformed deserialized entry shape.
- `06-final-green`: six cases passed after closed-shape validation was added.
- `07-clippy`: lib Clippy passed before the final formatting adjustment.
- `08-format-check`: package-wide check failed and retained concurrent formatting differences, including this slice. The two owned files were then formatted without changing behavior.
- `09-final-tests`: six cases passed with the owned file hashes matching start and readback; unrelated concurrently edited package files made the whole-package manifest differ.
- `10-clippy-final`: lib Clippy passed with `-D warnings`; the whole candidate was unchanged during this command.

Final owned source SHA-256 values at handoff:

- `src/profile_sources.rs`: `9707a9a944672e1385707fa3c8fd570c22dd85803457b61e6d7833f5c9b75fc2`
- `tests/support/profile_sources_cases.rs`: `9d13019ef4248e0031b5884b01282039a046df01a7af553fcbf5aac6ad8d8a2d`

The production collector intentionally fails closed on any reparse point within the selected plugin cache hierarchy. The observed installed cache contains `C:\Users\bryan\.codex\plugins\cache\openai-bundled\chrome\latest`, so a live collection is expected to report that exact non-secret path as a profile blocker; the collector never follows it.
