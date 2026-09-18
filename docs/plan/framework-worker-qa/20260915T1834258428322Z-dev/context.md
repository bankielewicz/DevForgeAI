# Bounded development context — 2026-09-15

User selected native Windows remediation of F-01/F-02 and restoration of M-01 from handoff.md in ../20260915T1800141514833Z. Project: C:\Projects\DevForgeAI; no root Git metadata. All 31 selected candidate entries and all 35 handoff entries matched SHA-256 before edits; handoff manifest matched b40d23c3f5751881ca563bbd47c8ce82330420aed3e0e273c13f67f54017daf6. No source drift observed. Memory search found no relevant worker entry; requirements come from current inputs.

## Output binding before production changes

selected_evidence_value: C:\Projects\DevForgeAI\docs\plan\framework-worker-qa\20260915T1834258428322Z-dev

selection_source: qa-fix.md requires a fresh sibling timestamped evidence root with the same relative depth; dev context reference permits selecting an established suitable project evidence location. This root holds context.md, selected-manifest.json (original candidate), independent fixture copy, environment/contract-readback.json, red attempt directories and receipts. Green and QA outputs are bound to sibling C:\Projects\DevForgeAI\docs\plan\framework-worker-qa\20260915T1834258428322Z-green so one-shot reproduction paths never overwrite Red. Final delivery.md, traceability.md, candidate-manifest.json, changed-files.json, build-identities.json, handoff.md and delivery-manifest.json will be under the -dev root. Separator normalization only; both absolute roots have the same parent as the selected handoff. No operational or index edits.

## Decisions and slices

Architecture/technology/source: DFF-WORKER-FEAS-01 sections 3–7. Existing Rust Session owns protocol/deadlines; OwnedProcess owns pipes and Job Object. Extend these responsibilities, preserve public send compatibility and the wire contract. No runtime dependency changes planned. Existing reader threads/channels and job teardown are reused; a bounded writer must permit the control thread to continue polling. Inspect existing send call sites and real-process tests before implementation.

1. F-01: reproduce unchanged IQ-02 deadline/cancel full pipe stimuli; add durable real-process tests for server replies, ordinary RPC and interrupt backpressure including descendant signalling. Keep deadlines active during writes and share one grace budget with interrupt. No write retries after uncertain delivery.
2. F-02: reproduce unchanged IQ-05 synthetic marker; validate CodexErrorInfo against captured schema before record/emit. Add malformed/nested category and RPC code controls plus approved-category retention checks.
3. M-01: preserve WF-01..20 and all original supplemental cases. Fresh normal and instrumented all-target tests, format, Clippy, original IQ groups with developer execution attribution. Source denominator: every executable src line, no runtime exclusions; tests/support/vendor excluded. >=95% executed-line coverage and >=95% pass rate independently; every mandatory case/subfixture must pass. Native WN-01/02 and branch coverage remain separately NOT_RUN unless available without changed toolchain; native execution is prohibited by this assignment.

## Inputs and evidence

Original handoff-manifest.json binds report/fix/specification/candidate and independent fixture hashes. Copies of record.py, independent_run.py and independent/{peer.rs,driver.rs,Cargo.toml,Cargo.lock} retain original bytes. Environment capture will verify all 335 contract/schema identities and collect exact native tools. AGENTS.md and .agents/skills/dev plus referenced context/implementation/evidence/failure guidance govern development. Selected specification and complete report/fix read. Runtime architecture is reference-only; other parent contracts supply authority fences, not additional implementation. Live profile/credential inspection, Codex launch, install/deploy, launcher amendment, unrelated source and independent finding closure are excluded.

Each execution uses a distinct retained receipt directory with exact argv, cwd, tool/candidate hashes, timestamps, exit/timeout and stream hashes. Python only records evidence and holds live process handles. It has no framework authority. Final source/build identities and per-defect map require literal-path readback. Findings remain OPEN pending independent retest; framework acceptance NOT_EVALUATED.
