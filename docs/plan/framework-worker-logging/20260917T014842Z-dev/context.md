# Rust logging development context

Selected scope: user said "Implement logging here in a fresh candidate", then "rust logging". This continues the startup investigation. New Rust development and offline verification are authorized. Native Codex remains separately selected after independent QA. No operational installation or config edits are included.

Original selected evidence value: docs/plan/framework-worker-diagnostics/20260916T181820Z-dev/qa-handoff.md; clarification: docs/plan/advisor-runs/20260916T185825Z-diagnostic-handoff/qa-handoff-addendum.md. Those are preserved reference inputs, not new output destinations. New output selection follows the user's fresh-directory requirement.

Resolved candidate: C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe-logging. Resolved evidence root: C:\Projects\DevForgeAI\docs\plan\framework-worker-logging\20260917T014842Z-dev. Component comparison against the paths announced to the user passed before candidate creation. No path relocation, checkout switch, or Git initialization. No Git metadata exists. Windows native NTFS workspace, PowerShell host; Rust x64 MSVC tools from C:\Users\bryan\.cargo\bin. Cargo.lock pinned; dependencies available offline. Exact versions retained separately.

Input hashes: input-bindings.json. All 58 source and all 58 frozen snapshot files verified before copying. Candidate starts as an exact copy of those 58 selected files, with no target output copied. Old evidence is read-only input. This is development evidence, not independent QA or framework acceptance.

Reuse: extend OwnedProcess pipe ownership and Session error checks, Journal evidence and inspector, Request admission, compiled launch policy. Add Rust capture and logging modules where those responsibilities are absent. No general logging dependency required: fixed typed JSON records avoid arbitrary text and inherited environment filters. No raw child/config/env logging.

Plan: (1) executed red tests for lost early stderr, mandatory exit summary and level selection; (2) own readers, nonblocking bounded queues, stream summaries, strict config/sink and classifier; (3) regression-preserving refactor, policy key repair in this candidate only; (4) Windows tests, fmt, Clippy, full-source line coverage and runtime query_failed check, then delivery and independent QA handoff.

Required suite initially contains all 133 inherited cases plus logging cases declared in tests/logging.rs and tests/support/capture_cases.rs, logging_cases.rs. Each test once, with conjunctive subfixtures; no skip of WF-16. Coverage denominator is every src/*.rs executable line, including new capture/logging modules and CLI. Exclusions: only tests, fixture binaries, dependencies. Branch measurement reported separately. Required paths and package manifest will be read back at delivery.
