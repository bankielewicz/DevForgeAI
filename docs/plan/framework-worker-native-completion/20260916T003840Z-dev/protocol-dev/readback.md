# Output readback

Required evidence root and actual evidence root are both exactly `C:\Projects\DevForgeAI\docs\plan\framework-worker-native-completion\20260916T003840Z-dev\protocol-dev`.

Read back at delivery:

- `context.md`: present, SHA-256 `62bd81c66aff8aa10bae40763d0ac6da2c20a15370e6f22d450bb18018fbfa1b` before final delivery records.
- `declared-cases.md`: present, SHA-256 `40dd88f8ff8b815829c9dc5a9c83d7407c7b18ab5a2af2bf93addeffd27d3f512`.
- `traceability.md`, `slice-plan.md`, `delivery.md`, and `checkpoint.md`: present beneath the exact selected evidence root.
- `record.py`: present, SHA-256 `ca6dfd8fd6d592aebd6a170ac3d722d823451f2b067277dbc640b2a5ac8c9e3c`.
- Final focused test receipt and raw stdout/stderr: present under `08-focused-integrity-green/`.
- Final focused Clippy receipt and raw stdout/stderr: present under `09-focused-clippy-final/`.
- Final owned rustfmt receipt and raw stdout/stderr: present under `10-owned-format-final/`.
- Nine retained final fixture roots: each contains `input.json`, `protocol-edges-trace.jsonl`, `run/journal.jsonl`, and `fixture/task.json` under `fixtures-integrity/`.
- Owned test files: present at the selected package paths with hashes stated in `delivery.md`.

Earlier characterization, formatting failure and formatter/refactor attempts remain preserved. No evidence directory was relocated or overwritten.
