---
id: DFF-07
status: planning-baseline
implementation_readiness: not-ready
updated: 2026-09-15
---

# Guardrails and Rust runtime

[Framework index](index.md) · [Foundation](foundation.md)

## Purpose and ownership

One compiled Rust implementation owns protected framework state, validators, transitions, mutation decisions and acceptance. CLI and host adapters invoke that same implementation. Skills, agent messages, Python evidence tools and editable reports cannot duplicate or replace it. This is the boundary specified by the [existing authority design](../../plan/devforgeai-codex-rust-enforcement-design.md); the inspected Rust application is an index service, not evidence that this protected workflow service is installed.

The framework supplies guardrails for scoped effects and truthful progress. It does not need to prescribe every investigation, turn or draft edit. Phase guidance and phase enforcement are different capabilities. A stopped model can leave useful work incomplete; an authority can prevent an invalid transition but cannot guarantee that the implementation will succeed.

## Inputs, outputs and dependencies

The [Codex/Pro operating boundary](foundation.md#codex-and-chatgpt-pro-operating-boundary) applies to every proposed control. The Rust service performs deterministic local checks; it is not an independently authenticated LLM backend. OS provisioning, protected reviewer identity and any hook-driven continuation must be feasible under the supported local host and subscription. Until that is demonstrated, report the specific unavailable control rather than portraying it as installed or essential to ordinary advisory work.

Inputs are authenticated requests, selected work identities, approved workflow/policy versions, candidate snapshots, evaluation definitions and attributed observations. Outputs are inspectable state, allowed/rejected operations, unmet predicates with concrete remediation, and bound receipts where acceptance is authorized. Work identity comes from [DFF-03](work-items-and-dependencies.md), policy from [DFF-04](project-context-and-policy.md), and evidence meaning from [DFF-08](quality-and-delivery.md).

The existing design proposes run-start/status, artifact submission, phase requests, evaluation requests and acceptance requests. Those names are design interfaces, not commands this baseline installs. The concrete protocol, workflow definition and protection profile must be completed together before runtime implementation is called ready.

## Protected behavior to carry forward

| Boundary | Required behavior | Observable failure |
| --- | --- | --- |
| Selected scope | Preserve selected requirements/platforms and amendment history | A follow-up testing request cannot silently remove a repair obligation |
| Request/state identity | Authenticate peer outside payload; check run/revision and request identity | Stale, conflicting or replayed requests cannot double-apply or advance another run |
| Candidate/evidence identity | Evaluate immutable captured bytes; bind cases, tools and policy | A current source edit cannot be qualified using an unrelated old report |
| Evidence completeness | Apply selected denominators and mandatory conditions | Missing cases or platforms cannot become passing percentages |
| State/receipt persistence | Commit state and audit/receipt consequences consistently | A crash cannot leave accepted status without the supporting committed record |
| Approval | Establish the required principal through an actual protected boundary | A workspace approval.json or named QA agent cannot manufacture approval |
| Availability | Return explicit unavailable protection | A disabled hook or missing service cannot mint acceptance |

These are protection requirements, not claims that workspace documents enforce them. The earlier proposal chose phase-transition control rather than brokering every draft source edit. Its relation to a lightweight installation and the first core workflow remains an explicit expansion decision.

## Host adapters and execution freedom

Codex, Git and GitHub integration translates supported host events into the common Rust decision path. Hook feedback has incomplete interception coverage and post-tool checks cannot undo completed effects. Local Git hooks can be bypassed; protected downstream delivery requires its actual server/repository controls. Declarative configuration dispatches Rust rather than reimplementing policy.

The earlier Windows-first authority selection applies to a bounded first implementation proposal. Windows/WSL/Linux evidence targets remain separate from hosts on which the authority itself is qualified. It is not a universal Windows requirement for every future installation. Installation and native protection tests are separately scoped under [DFF-11](installation-and-integrations.md).

The selected bounded-continuation idea remains a proposal requiring budget, progress, cancellation and retry semantics. A model claiming progress is insufficient. No default endless loop, automatic four-agent cycle, or repeated native test attempt is introduced here. A user pause ends activity without converting unfinished work into completion.

## Verification scenarios

- OrderDesk's business rule and race scenario share one work identity; one passing unit case cannot hide the unresolved race.
- Windows coverage passes while selected Linux/WSL coverage fails: readiness remains unsatisfied with exact missing predicates.
- Disabled hooks and an existing interactive shell allow candidate activity but cannot write protected state or forge a valid receipt.
- Two transitions target the same revision: serialize or reject consistently, retaining both attempts.
- A candidate changes after snapshot creation: prior observations remain about their captured bytes, and current readiness is recalculated.
- An operator-approved scope amendment removes a deliverable: the revised scope is explicit; prior incomplete scope is not relabeled as historically complete.

## Existing assets, open decisions and next expansion

Reuse the current design's Windows service identity/named-pipe boundary and one-authority principle as selected design inputs. The proposed future client is not added to the index CLI by assumption. Python JSONL runners/graders remain evidence-producing build artifacts where skill contracts require them.

Resolve the first concrete workflow, policy/protocol schemas, role authentication, authority bootstrap, remote evidence producer trust, supported host profiles, execution limits and status/receipt consumers. Next expansion specifies one complete repair-to-independent-QA path plus rejection cases; it must demonstrate how guidance remains useful without representing unavailable protection as active enforcement.
