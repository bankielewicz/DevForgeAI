---
id: DFF-MVP-01
status: planning-baseline
implementation_readiness: not-ready
updated: 2026-09-15
---

# Framework execution MVP candidate scope

[Framework index](../index.md) · [Runtime architecture](../runtime/architecture.md) · [Acceptance scenarios](acceptance.md) · [Evaluation protocol](../evaluation/benchmark-protocol.md)

## Selected outcome and limits

The user selected development of an MVP candidate from this framework baseline, with scope and evaluation defined together before implementation. The candidate must demonstrate a connected, project-adapted engineering loop: selected requirement/context, justified work scope, implementation and applicable TDD, integration/regression checks, independent QA, bounded repair/retest, and an identified candidate with truthful delivery status. Completing a phase checklist or rejecting a fabricated PASS alone is insufficient.

The framework and its Rust execution mechanism remain one product. This MVP is a selected capability subset, not a copy of every framework document or a second framework. Current foundation documents remain planning baselines. This file is a scope contract to refine; wire schemas, source destinations and qualification profiles are not ready for coding. No implementation story is created merely to fill a capability map.

## Inputs, outputs and owners

Inputs are an explicitly selected project/checkout, requirement or defect, relevant specification versions, effective project policy, grounded expertise/context, source candidate identity, required platforms/cases and permitted effects. The consumer must identify inadequate or contradictory inputs before dependent work, reusing adequate upstream artifacts instead of requiring a new PRD for a small repair.

Outputs are a preserved work identity and obligations; attributable worker/job records; inspectable progress; current-candidate evidence; independent QA findings and any repair/retest linkage; retained unresolved decisions; and a reproducible candidate/handoff whose claimed scope matches the evidence. Protected acceptance requires the actual qualified authority; an honest incomplete result is not successful product completion.

Rust owns selected workflow decisions and dispatch in the target architecture. The foreground Codex session supplies conversation/steering and reports observations. Existing project experts supply grounded knowledge. QA owns its independent assessment and expected outcomes; a named second agent alone does not establish the required independence. Governing responsibilities remain in [core workflows](../core-workflows.md), [quality](../quality-and-delivery.md) and [guardrails](../guardrails-and-rust-runtime.md).

## Required candidate capabilities

| ID | Observable outcome | Dependency / status |
| --- | --- | --- |
| MVP-01 Intake and policy | Bind the chosen work, checkout, effective standards and relevant context; expose missing/conflicting decisions | DFF-02/03/04; schema and policy conflicts unresolved |
| MVP-02 Durable obligations | Additional testing requests preserve existing repair work; amendments retain their source and prior scope | DFF-03/10; not implemented |
| MVP-03 Execution ownership | Dispatch bounded engineering work, collect results and choose the next permitted action or explicit stop reason | DFF-06/07; adapter/support and job-lifetime decision blocks implementation |
| MVP-04 Useful delivery loop | Produce a functional candidate through appropriate TDD, verification, independent QA and necessary repair/retest | DFF-02/08; cannot be replaced by gate-only fixtures |
| MVP-05 Evidence integrity | Bind observations to candidate, policy, cases, denominator and execution platform; reject unsupported promotion | DFF-07/08; protected authority profile unresolved |
| MVP-06 Progress and recovery | Retrieve bounded updates and reconstruct outstanding work after interruption without duplicate uncertain effects | DFF-10/runtime; cursor, ownership and recovery contract unresolved |
| MVP-07 Demonstrated adaptation | Run the same core loop in a second project with materially different conventions or policy, consuming grounded project context | DFF-04/05/09; exact cohort/profile and binding migration unresolved |
| MVP-08 Expert correction path | Detect a relevant stale/conflicting expert assertion and retain a scoped review/realignment handoff | DFF-05/09; no automatic operational rewrite |

MVP-03 targets Rust-owned dispatch. Rust-assisted Codex remains a separately named, reduced alternative: it can retain/check state but cannot make an ended Codex conversation call again. A prototype of that mode cannot be relabeled as delivery of MVP-03. Any scope amendment must identify the omitted capability and its effect on the evaluation claim.

## Walkthrough selection

Use the existing fictional OrderDesk change to refine one connected brownfield path: cancellation before dispatch is permitted, cancellation afterward is denied, and concurrent dispatch/cancellation must not yield contradictory states. Domain terminology, API and transaction details still need resolution; the example is not an implementation-ready product specification.

Exercise a second, separately selected project whose conventions or policy require a different grounded response. It must be more than the same fixture under a different project name. Exact language, project, acceptance oracles and expected policy differences must be fixed before trials. This pair begins to test adaptation; it does not prove support for all stacks or business domains.

Retain the original I1 new-product walkthrough as a planning check: identify how an unclear idea becomes adequate input and where a human decision is required. The MVP does not promise to automate every upstream brainstorming, business-analysis or architecture activity. These alternate entry routes must share downstream work/policy/evidence definitions.

## Host, subscription and authority boundary

The earlier Windows-first runtime direction remains the planning input. The first qualified execution profile must name the Windows host, native filesystem, Codex version/interface, subscription mode, tools, effective permissions and engine build. Separate managed-product Windows/WSL/Linux test targets are not the same as qualifying the engine on each host. Prior index-service findings and platform gaps remain unchanged historical work; this MVP does not close them.

Base operation must fit supported Codex with an individual Pro subscription. Experimental app-server use may be investigated in a separately specified disposable prototype, but no native test converts an unsupported production interface into a supported release dependency. No API billing or other paid account may be silently introduced. Model/effort, usage and concurrency are observed profile properties, not universal constants.

The protected acceptance boundary remains mandatory wherever claimed. Ordinary user-writable SQLite does not satisfy it. A local coordination prototype can provide useful evidence but cannot supply protected acceptance. Resolve AMB-03 and the selected profile before claiming a qualified protected path; do not silently lower the claim to avoid the dependency.

## Explicitly outside this candidate

No custom terminal, replacement model runtime, universal multi-host engine, hosted autonomous CI worker, production deployment automation, automatic expert generation for every role, general-purpose memory learning service, fixed agent-per-phase pipeline or mandatory database-per-role architecture is selected. The index/query service is optional context infrastructure with separate contracts. Installation/operational updates and the old index repair are not authorized by this documentation task.

Reuse existing skills and expertise where their current contracts are compatible. Reuse does not waive MIG-01/02 project-policy and QA stop differences, MIG-03 closed schemas, or AMB-12 operational binding requirements. Resolve each selected dependency before relying on it. Do not copy old shell/Python authority into the Rust runtime.

## What must be settled before coding

1. Select one bounded first implementation unit and exact Rust package/source/test destinations after inspecting the index workspace. State how it connects to this candidate; do not overwrite the index implementation.
2. Resolve that unit's governing identifiers, inputs, outputs, errors, state transitions, permission boundaries and recovery behavior. Identify remaining independent candidate blockers rather than requiring every future capability first.
3. If the unit uses a Codex worker, resolve interface maturity, Pro authentication, sandbox/approval handling, cancellation, worker lifetime and available usage observations. A feasibility unit must clearly name its experimental/nonproduction claim.
4. Finalize the relevant [acceptance cases](acceptance.md) with executable oracles, fixtures, declared platforms and resource bounds; select red/green/refactor/QA commands after tool discovery.
5. Bind the selected contract version and dependencies in a handoff. A ready unit does not promote the entire framework baseline to ready.

Framework implementation retains AGENTS.md requirements: >=95% executed-line coverage of declared first-party executable framework code and >=95% required-case pass rate, independently and per required platform; failed mandatory scenarios still fail. Managed projects use their selected policy. Benchmark success neither replaces these requirements nor establishes framework superiority.

The immediate next session finalizes that first unit, not a large story backlog. See the [handoff](../../../plan/framework-mvp-next-session.md). Evaluation proceeds from harness-validity pilot to a frozen comparison; no competitive rank or improvement is claimed yet.
