---
id: DFF-MVP-HANDOFF-01
status: planning-handoff
implementation_readiness: not-ready
updated: 2026-09-15
---

# Next session: finalize the first MVP implementation contract

## Continuation recorded

This planning prompt was followed on 2026-09-15. Its result is [DFF-WORKER-FEAS-01 v1.0.0](../specs/framework/runtime/codex-worker-feasibility-v1.md), with [verification](framework-worker-contract/20260915T151300Z/verification.md) and a new [scoped coding handoff](framework-worker-coding-handoff.md). The original prompt below remains historical context; the new handoff selects only offline implementation of the nonproduction worker harness. No runtime implementation or model trial occurred during contract finalization.

## Start here

Workspace: `C:\Projects\DevForgeAI`, native Windows. This is the continuation of the approved Adaptive Spec-Driven Engineering Framework approach. The immediate task is bounded contract finalization, not another open-ended architecture brainstorm and not implementation of the entire framework directory.

Read current `AGENTS.md`, then:

1. [Framework index](../specs/framework/index.md).
2. [MVP scope](../specs/framework/mvp/scope.md) and [acceptance scenarios](../specs/framework/mvp/acceptance.md).
3. [Runtime architecture](../specs/framework/runtime/architecture.md).
4. [Evaluation protocol](../specs/framework/evaluation/benchmark-protocol.md).
5. [Current decisions and ambiguities](../specs/framework/roadmap-and-decisions.md).

Use [discussion sections 9–12](devforgeai-adaptive-framework-enhancement-notes.md#9-continued-discussion-dedicated-terminal-versus-a-rust-engine) for reasoning and rejected alternatives. Read additional capability owners only for the chosen unit's dependencies. Do not load all historical QA artifacts or every skill package merely to resume planning.

## Decisions to preserve

- One connected framework under `docs/specs/framework/`. Rust CLI engine and Codex conversation are complementary parts; no separate terminal is selected.
- The target engine performs workflow coordination and dispatch. A command runner or Rust-assisted Codex mode has a smaller claim and cannot silently replace it.
- Supported Codex with individual Pro is the base constraint. App-server is an investigated experimental adapter, not proven production support. No secret extraction, API billing fallback, Enterprise dependency or unlimited-worker assumption.
- Persistent obligations, useful progress, project knowledge and recovery are selected needs. Physical database counts and role-per-database layouts are not selected requirements.
- Managed projects select their policy; DevForgeAI runtime remains Rust with its own mandatory >=95% line coverage and >=95% required-case pass rate. Numeric floors cannot waive mandatory failures.
- Independent QA, current-candidate evidence, permitted effects and the real protected authority boundary remain explicit. User-home SQLite is not protected acceptance.
- Compare useful delivered outcomes, integrity, recovery, adaptation and total effort. No scores, performance gains or superiority have been demonstrated.

## Bounded task for the next session

1. Inspect current Rust manifests/source organization and discover local tools. The existing package is an index application, not evidence of this workflow engine. Report drift from this handoff without reverting it.
2. Trace one complete brownfield path and the minimal upstream new-product entry check described in the scope. Select the first useful implementation unit; do not generate stories for all thirteen capabilities.
3. Resolve only the unit's essential decisions. At minimum identify exact source/test destinations, project/work/candidate identities, input/output/error protocol, state/permission ownership, persistence and recovery boundaries, and the independent expected result. Record dependent unresolved questions by AMB ID.
4. If delegated Codex execution is in that unit, first produce an exact feasibility contract: selected installed interface/version, documented support category, subscription authentication, sandbox/approval behavior, bounded disposable task, cancellation/usage handling, captured evidence, allowed effects and cleanup. Native success is not production support. Do not launch a paid/model trial or alter configuration merely because this planning prompt mentions one.
5. Produce a bounded implementation specification under the owning runtime/MVP location, with traceability to selected MVP/MC IDs, exact test fixtures/commands after discovery, and required platform/coverage scope. A ready unit may coexist with an overall not-ready framework. If an essential choice cannot be grounded, state the exact question and affected unit rather than guessing.
6. Produce the coding handoff selecting only that complete contract and its dependencies. Preserve previous evidence, current source and operational copies. Identify red/green/refactor/QA obligations and the independent retest boundary.

This handoff authorizes documentation/contract finalization. It does not authorize a runtime implementation from incomplete planning files, installation, changes under `.agents`/`.codex`, startup/systemd changes, remote source synchronization, deployment or closure of historical QA findings. The next coding request should explicitly select the finished implementation or feasibility contract. Do not use `$dev` to author this planning contract; its declared role is implementation from selected specifications.

## Completion evidence for this planning task

Return the selected unit, exact contract path/version and dependency identities, resolved/open AMB questions, concrete independent acceptance oracles, actual local discovery commands/outcomes, and the scoped coding prompt. Do not return another unbounded roadmap, invent running CLI commands, or claim tests/coverage for prose.

Current documents and prior-copy preservation are recorded in [verification](framework-mvp-planning/20260915T145455Z/verification.md) and its linked manifest. Those observations concern documentation, not implementation or framework acceptance. Read the manifest entries for the selected documents and verify current bytes before relying on them.

## Copyable next-session prompt

```text
Continue the approved DevForgeAI framework MVP planning in C:\Projects\DevForgeAI using native Windows.

Read current AGENTS.md and docs\plan\framework-mvp-next-session.md. Follow its bounded contract-finalization task and selected reading order. Verify the linked document identities; report drift without restoring older source.

Preserve the selected Rust-owned workflow-engine direction, supported Codex + individual Pro constraint, project adaptation, independent QA, and actual authority boundary. Treat database layouts and app-server integration as decisions requiring evidence, not already implemented capabilities.

Finalize one smallest useful implementation contract, or a clearly bounded nonproduction feasibility contract where the dependency is unresolved. Define exact inputs, outputs, failure paths, ownership, source/test destinations and executable acceptance oracles. Resolve only its essential decisions, retain the other ambiguity IDs, and produce the scoped coding handoff.

This session is contract finalization. Do not implement the entire framework, install components, change operational skills/startup settings, synchronize remote source, launch model trials, or claim acceptance from planning documents.
```
