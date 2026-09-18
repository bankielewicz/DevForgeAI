# Worker harness implementation context

- Selection: user requested `read and follow C:/Projects/DevForgeAI/docs/plan/framework-worker-coding-handoff.md`; its copyable coding prompt selects DFF-WORKER-FEAS-01 version 1.0.0 and the operational dev skill.
- Project: `C:\Projects\DevForgeAI`, native Windows / PowerShell, Windows filesystem. No `.git` exists. Target package does not exist at intake.
- selected_evidence_value: `C:\Projects\DevForgeAI\docs\plan\framework-worker-implementation\20260915T1544548240203Z`
- selection_source: handoff copyable coding prompt, "Use a new absolute evidence directory under docs/plan/framework-worker-implementation/ and bind it before writing."
- resolved_evidence_root: `C:\Projects\DevForgeAI\docs\plan\framework-worker-implementation\20260915T1544548240203Z`
- Pre-write binding: chosen fresh timestamp child, absolute Windows path under the required parent; no component renaming or checkout substitution.
- Output mapping: this root owns context.md, input-checks.json, traceability.md, slices.md, executions.jsonl, attempt directories, checkpoint documents, delivery.md and independent-qa-handoff.md. Package source/tests/manifest/README belong only to `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe`.
- Input check: all 30 delivery entries and all 305 schema entries matched their byte lengths and SHA-256 on intake. A retained repeat follows in input-checks.json.
- Scope: offline Rust harness and external deterministic Rust peer, captured native adapter implementation, Windows containment, journal, inspection and oracle. No native Codex launch, live account/config/credential inspection, network installation, operational changes, index package changes, startup changes, historical finding closure or protected acceptance.
- Tool discovery: Rust 1.97.1, Cargo 1.97.1, cargo-llvm-cov 0.8.4; Cargo/Rust binaries resolve under `C:\Users\bryan\.cargo\bin`. Offline resolution/build availability still to be checked.
- Reuse search: scoped `rg` for JobObject, PROC_THREAD_ATTRIBUTE_JOB_LIST, journal, tokenUsage and app-server in index src/tests found only SQLite journal configuration in storage.rs. Index Cargo.toml was read; it is a separate package with no compatible worker boundary to reuse. New isolated implementation is required by section 3; no imports or edits to the index package.
- Rules: root AGENTS.md and operational dev skill references read. No more-specific AGENTS.md exists in the destination ancestors. All first-party executable src lines, including CLI and Windows errors, remain the coverage denominator; threshold >=95%. WF-01..20 count once, all subfixtures mandatory. WN-01/WN-02 remain NOT_RUN; framework acceptance NOT_EVALUATED.
- Capture excludes credentials, live Codex account/configuration and unrelated histories. Referenced parent documents constrain this experiment without selecting their deliverables.
