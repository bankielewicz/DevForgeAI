---
id: DFF-WORKER-HANDOFF-01
version: 1.0.0
status: scoped-coding-handoff
updated: 2026-09-15
---

# Coding handoff: one Codex worker feasibility harness

Select [DFF-WORKER-FEAS-01 version 1.0.0](../specs/framework/runtime/codex-worker-feasibility-v1.md), with exact dependency hashes in the [delivery manifest](framework-worker-contract/20260915T151300Z/delivery-manifest.json), captured [Codex schema identities](framework-worker-contract/20260915T151300Z/schema-manifest.json), and [discovery/verification](framework-worker-contract/20260915T151300Z/verification.md).

The contract is ready for offline harness implementation. Native Pro trials, production support, protected acceptance and the complete MVP remain unqualified. This file prepares the next request; it does not initiate implementation or authorize model execution.

## Copyable coding prompt

```text
Use $dev to implement only DFF-WORKER-FEAS-01 version 1.0.0:
docs/specs/framework/runtime/codex-worker-feasibility-v1.md
in C:\Projects\DevForgeAI using native Windows.

Read current AGENTS.md, this contract and docs/plan/framework-worker-coding-handoff.md.
Verify contract/dependency bytes against docs/plan/framework-worker-contract/20260915T151300Z/delivery-manifest.json and schema-manifest.json. Report drift; preserve old evidence.

Implement the isolated package at devforgeai/experiments/codex-worker-probe with its own Cargo workspace/lockfile. Selected scope is the offline Rust harness, its deterministic external protocol peer, Windows process containment, evidence journal, inspection and independent fixture comparison. Implement the native adapter path against the captured protocol, but do not start Codex, authenticate, inspect live account capability or launch model trials.

Follow red -> green -> refactor -> QA. A compiler/setup failure is not Red. Execute WF-01 through WF-20 and all their subfixtures. Declare and measure all first-party src executable lines, including Windows/error paths; require >=95% line coverage and >=95% required-case pass rate with every mandatory case passing. Report raw counts, per-scope gaps and branch measurement separately.

Use a new absolute evidence directory under docs/plan/framework-worker-implementation/ and bind it before writing. Retain failures, source/test/dependency identities, exact commands/exit codes and reports. Do not replace the index package, edit its manifest/lockfile, modify operational skills/configuration, install dependencies or services, change startup, synchronize remote source, or close historical findings.

Keep WN-01/WN-02 NOT_RUN unless I separately select the native trial and its reviewed Pro profile. Never substitute API billing, extracted tokens, another model, relaxed permissions or production-support claims. Finish with the identified candidate, offline QA evidence, unresolved native/protection dependencies and an independent QA retest handoff. Do not report framework acceptance.
```

## Independent assessment boundary

After implementation, a separate QA selection names this contract, the frozen source/test manifest and the fresh implementation evidence directory. Independent QA writes protocol-trace, process-handle and invalid-result checks from the requirements, verifies all WF cases/subfixtures, and retains findings for development. The developer cannot self-close independent findings. Native Codex behavior needs its own explicitly selected WN-01/WN-02 profile; passing the peer does not replace those observations.

## Exact remaining native decision

Can the installed 0.154.0 profile, retaining supported Codex-managed Pro authentication, expose the selected model/effort while meeting read-only tool execution, no external tool/hook effects and owned Windows process teardown? No native launch or configuration review was performed in planning. A future trial request must name its model/effort, sanitized profile review and resource bound. If the profile cannot meet the contract, retain AMB-01/02/16 and revise only that dependency before execution. Production dispatch remains unresolved even if the experimental trial succeeds.
