---
id: DFF-RUNTIME-01
status: planning-baseline
implementation_readiness: not-ready
updated: 2026-09-15
---

# Rust workflow engine architecture

[Framework index](../index.md) · [MVP scope](../mvp/scope.md) · [Open decisions](../roadmap-and-decisions.md#ambiguity-register)

## Purpose, status and contract ownership

The selected direction is a headless engineering workflow engine implemented in Rust and invoked through the existing Codex CLI conversation. The engine performs coordination and work dispatch; it is not merely a wrapper around a coverage command. No custom terminal is selected. This document records architecture and required boundaries, not an installed engine, a finalized protocol or permission to implement all framework capabilities.

The existing [guardrail contract](../guardrails-and-rust-runtime.md) owns protected decisions. [Work items](../work-items-and-dependencies.md) owns requirements and work identities; [project policy](../project-context-and-policy.md) owns effective standards; [quality](../quality-and-delivery.md) owns evidence meaning; [continuity](../knowledge-and-continuity.md) owns recoverable context. This runtime must consume those definitions rather than create another policy engine. The existing index application remains a distinct source-observation component.

## Responsibilities and inputs

| Component | Input and responsibility | Output and limit |
| --- | --- | --- |
| Foreground Codex conversation | User requests, steering and cancellation; submits selected work and reads status | Explains observed progress; does not independently advance protected phases |
| Rust workflow engine | Bound project/work/policy/context, execution profile and permitted effects | Durable obligations, job dispatch, results, next permitted action or an explicit stopping condition |
| Codex worker adapter | A bounded task, relevant context, model/effort selection and effective permissions | Worker events, proposed artifacts and attributed results; worker completion is not work acceptance |
| Build/test/evidence runners | Identified candidate, declared cases/tools/platform and denominator | Executed observations and artifacts; no runner-authored permission or acceptance |
| Rust authority | Authenticated requests, selected policy and validated evidence | Protected decisions under the actually qualified OS boundary |
| Persistence and query interface | Committed runtime records and retained artifacts | Bounded status/history/context responses; a summary is not proof of correctness |

There is one orchestration owner per run. For the selected engine direction, Rust owns dispatch. Foreground Codex polling is a way to retrieve updates, not the mechanism on which Rust depends to remember every pending assignment. Workers do not start a competing top-level workflow or recursively create unbounded workers. Any supported delegation must remain attributable to the run and its aggregate resource limits.

## Execution alternatives and the compatibility decision

Rust-assisted Codex is a useful alternative: Codex chooses each next call while Rust retains state and checks evidence. It does not supply Rust-owned continuation after Codex stops. Selecting that reduced mode would require an explicit scope disposition; it cannot silently satisfy the selected dispatch capability.

Codex app-server is an investigated adapter, not a mandatory approved dependency. Official documentation describes custom clients, threads, turns, approvals, streamed output and Codex-managed ChatGPT authentication. It also labels the app-server command and WebSocket transport experimental and unsupported for production workloads. Native success cannot change that documented support classification. A disposable feasibility prototype may investigate it; a supported production baseline cannot be claimed until the dependency/support decision is resolved. A different documented Codex execution interface may be evaluated against the same requirements. [Official app-server documentation](https://learn.chatgpt.com/docs/app-server)

The [Codex/Pro boundary](../foundation.md#codex-and-chatgpt-pro-operating-boundary) applies. No extracted tokens, direct undocumented model endpoint, implicit API-key fallback, credit purchase or Enterprise dependency is permitted. Codex manages subscription authentication. A deterministic status read or local test runner needs no LLM authentication. Effective tool permissions must be preserved: app-server `process/*` is documented as outside the Codex sandbox and must not be adopted as an interchangeable safe substitute for sandboxed execution. Host selection and privilege requirements need their own reviewed contract.

## Progress and lifetime

Required behavior is prompt acknowledgement of an accepted request, a stable run identity, bounded incremental event retrieval, and a current state snapshot. The actual command grammar, JSON schema, exit codes, wait limits and cursor rules remain open under AMB-05/09/16. Earlier conversational examples of `devforgeai run updates` and `run context` are sketches, not implemented or selected command names.

Responses must distinguish admitted work, running work, a worker finishing, required checks finishing, unsatisfied requirements, cancellation and acceptance. Report the active operation, elapsed time, last meaningful event, concrete results and missing prerequisites. Heartbeats show liveness. They cannot manufacture a percentage or establish progress. A flush to stdout does not guarantee immediate model commentary; qualify the actual terminal/tool return path.

Update retrieval must not restart a job. Repeating a submission after a timeout must not duplicate work. User interruption and cancellation need explicit semantics for child processes, pending approvals and retained results. A crashed engine must reconcile uncertain external effects before retrying. Neither a SQLite commit nor a persisted PID proves what a child process accomplished. The process owner, lifetime after a CLI call returns, restart authority and orphan handling are implementation blockers, not implied installation of a daemon.

## Persistence and project knowledge

The proposed user data root is the current user's `.devforgeai` directory; `C:\Users\bryan\.devforgeai` is this user's example, not a hardcoded path. No directory or database is created by this planning work. Host-specific defaults and overrides require an explicit contract.

Keep three logical record classes distinct: history of what was said/done, attributed project knowledge, and current workflow obligations/state. A model-authored statement is not an observed fact merely because it is stored. Effective requirements and policies remain bound to selected versions; mutable memory cannot retroactively change them. Shared project specifications remain canonical project artifacts, with the store retaining source references and necessary snapshots.

SQLite is a candidate for local durable storage. Project isolation and transaction boundaries come before file counts. A small project-scoped store with separate tables is the current recommendation to evaluate. A database per role/phase and the earlier fixed two-databases-per-project layout are not selected requirements. Shared business facts and a run's state should not fragment into competing developer/QA copies.

Keep state mutations and their required events in the same transaction. Separate larger transcripts, diagnostics and artifacts with explicit references, retention and missing-file behavior. A split into additional stores requires different protection/lifecycle needs, independent recovery requirements, or measured contention that the split actually addresses. Cross-store revision/snapshot semantics must be specified first. SQLite WAL allows one writer per database and does not provide a single atomic transaction across multiple database files; more files do not prove lower total I/O. [SQLite WAL documentation](https://www.sqlite.org/wal.html)

The initial design should use one native owner for each store. Windows, WSL and remote Linux must not be assumed safe concurrent readers/writers of one file across filesystem boundaries. Identified remote observations cross an interface, not an implicit shared database. Project, checkout, host and candidate identities must remain distinct.

## Protection and implementation readiness

User-home storage supports continuity; it is not a protected authority when the worker can edit it. Separate filenames, hashes, role names and `accepted` columns do not create a trusted principal. The [existing authority design](../../../plan/devforgeai-codex-rust-enforcement-design.md) still governs the protected boundary. Location, OS identity, IPC, trusted policy and provisioned effects remain AMB-03 dependencies. A prototype without that boundary reports coordination observations only.

Resolve the adapter/support profile, dispatch lifetime and limits, protocol/error semantics, storage/recovery/protection design, effective policy/QA compatibility, and Rust package/source destination before the dependent implementation contract is ready. [Next-session instructions](../../../plan/framework-mvp-next-session.md) select that bounded contract work. Runtime code, operational skills, installation and remote source changes are not part of this document delivery.
