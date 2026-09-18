---
id: DFF-ENHANCEMENT-NOTES-001
status: retained-planning-record
updated: 2026-09-15
---

# Adaptive framework: retained enhancement discussion

This record preserves the QA-rooted proposals, user choices, objections and subsequent whole-framework direction from the 2026-09-14/15 conversation. It is not a runtime specification, skill instruction, acceptance receipt or permission to resume product repair. The [framework index](../specs/framework/index.md) is the entry point for subsequent planning; its [decision register](../specs/framework/roadmap-and-decisions.md) records current dispositions.

## 1. Incident and verified evidence

The initial request selected native-Windows remediation of QA-D01 (tray status missing current generation and last reconciliation) and QA-D02 (coverage below the 95% repository floor). Later requests added WSL/Linux testing and supplied a Linux host. Those credentials are deliberately not reproduced here. The follow-up request was then a root cause analysis of incomplete remediation.

Original [QA report](index-service-qa/20260914T184442947070Z/executions/20260914T191133863776Z/qa-report.md), [repair packet](index-service-qa/20260914T184442947070Z/executions/20260914T191133863776Z/qa-fix.md) and [dev handoff](index-service-qa/20260914T184442947070Z/executions/20260914T191133863776Z/dev-handoff.md) remain preserved. The selected identities were rechecked during this session:

| Input | SHA-256 |
| --- | --- |
| Index service MVP specification | 52d33c84435da8f3442c6b1dc4c5370113ff0eb93ee5cd2801903741900c89c4 |
| Original QA handoff-manifest.json | 7681571d0e61f71b857fb57bf1bb466f902781a52a3e2c3fbf4d8f3794a2398b |
| Original failed source-manifest.json | 43b63b5a9496b9d5374996d274cf5b852e2301ba23a87490717c786f71790343 |

The original QA measured Windows 2626/3442 executed lines and Ubuntu 2075/2786, with 16/18 declared unit cases passing on each. These are historical measurements, not new test executions in this documentation task.

The retained [remediation final delivery](index-service-remediation/20260914T1950304158791Z/final-delivery.md) reported:

| Platform | Executed-line evidence | Result scope |
| --- | --- | --- |
| Windows | 3314/3486 = 95.065978% | Developer evidence for repaired tray and Windows floor |
| SSH Linux | 2410/2830 = 85.159011% | Coverage and Clippy failures remained |
| WSL Linux | 2418/2830 = 85.441696% | Coverage and Clippy failures remained |

The selected unit cases reached 18/18, but that did not cure platform coverage or full qualification. The separate bridge scenario was 1/2, with its remaining assertions unexecuted because the configured fixture could not be used and was later found absent. The exact cause/time of its disappearance was not established. Do not claim WSL cleanup caused it. Startup/systemd and other acceptance/integrity gaps remained separate; documentation of them did not authorize broader effects.

Retained technical analysis identified missing Unix test parity, Windows-only imports producing Unix Clippy failures, and Windows behavior still represented in Unix coverage behind runtime cfg! rejection. Those are product/test issues requiring their own scoped repair, not reasons to weaken coverage denominators. See the [earlier RCA](root-cause-analyses/qa-completion/20260914T2024442802835Z/analysis.md) for incident analysis; its earlier prose-control recommendations are qualified by the later decisions below.

## 2. Root cause and the correction to the correction

The development execution stopped with repairable selected work remaining and treated a testing extension as narrowing the active repair objective. Honest PARTIAL reporting avoided false acceptance, but did not fulfill the selected repair. Evidence did not establish that unavailable native tools or build duration prevented further work.

The first proposed response added more continuation/stop rules to the dev skill. The user rejected that architectural direction: modernization is intended to remove ceremonial logic from skills and put executable safeguards in Codex/Git/GitHub hooks and compiled Rust controls. Existing skill instructions already required meaningful continuation and verification; more emphatic wording would retain model obedience as the control mechanism.

Revised systemic finding: protected workflow obligations and completion were not demonstrated as externally enforced in this run. The [existing Rust design](devforgeai-codex-rust-enforcement-design.md) already places authoritative validation/state in Rust; the inspected index service does not implement that separate authority. There was no demonstrated malfunction of an installed Rust phase gate. A gate can reject unsupported completion; it cannot guarantee an LLM successfully repairs software or force the user to continue.

## 3. Earlier bounded runtime selections

The user initially selected a foundation-plus-workflow implementation contract, a Windows authority with separate Windows/WSL/Linux evidence, phase transitions rather than brokerage of every draft mutation, and bounded continuation on premature stop. These remain traceable selections for that bounded proposal. The later whole-framework direction requires integration and does not make Windows mandatory for every managed project.

Useful candidate controls include persistent obligations across steering/resume, explicit scope amendments, current-candidate evidence, approved cases/denominators, protected state and receipts, and one decision path for CLI/hooks. Domain draft work can continue without optional infrastructure; unavailable required authority cannot be replaced with a Python flag or editable manifest. Scope, evidence and phase state remain separate from session activity.

Continuation needs an actual budget and progress definition, respects interruption and host limits, and leaves exhausted work incomplete. It must not blindly rerun uncertain effects or automatically repeat restricted native cases. No fixed retry count or automatic supervisor was implemented or selected as a universal core requirement.

## 4. Custom agents: supported capability and disputed orchestration

Official Codex documentation supports named custom subagents with role instructions and configurable model/effort. The user requested editable profiles and a complete attribute reference. The [subagent capability document](../specs/framework/subagents-and-context.md) records mandatory profile fields, common overrides, global settings, inheritance/precedence, and the full captured general configuration schema with applicability limits. The local CLI version observation was 0.154.0; profile activation was not tested and no operational profiles were created.

Initial proposed roles were Red/test builder, Green/implementer, Refactor, QA and coordinator. The Red role creates the appropriate test level, not exclusively unit tests. A native agent name is not a protected identity, skill or privilege boundary. Model/effort changes belong to invocation provenance; unchanged native test evidence does not become invalid solely because the next agent uses another model.

The user selected a new affected Red cycle for changes to accepted developer tests. Later objections concerning unnecessary iteration require this to be narrowed and tested before adoption: distinguish assertion changes, fixture corrections, formatting and unchanged dependencies. Preserve original QA oracles and all prior chronology. Replaying a baseline later cannot be represented as historical proof that a test was executed before an earlier production edit.

Fresh Red/QA contexts were proposed to reduce inherited assumptions. The user requested an adversarial viewpoint and challenged token waste from iterative phase-agent cycles. Freshness of context is not independence or adversarial reasoning. Reviews need relevant requirements, evidence and counterexamples; hiding relevant history can reduce effectiveness. One story owner plus selective adversarial review is the later recommendation, not a mandated four-agent pipeline. Actual usage/quality comparisons are needed before claiming savings.

## 5. Epic/story decomposition without fragmentation

Review covered [query CLI](devforgeai-index-query-cli-spec.md) and [authority design](devforgeai-codex-rust-enforcement-design.md). Query ownership must stay separate from protected authority. Both can be organized into epics and bounded stories while retaining shared canonical contracts.

The user clarified that the concern about 100 stories applies to unwarranted splitting of the selected documents, not a universal limit. A large MVP or brownfield enhancement can justify many stories. The proposed method inventories normative clauses, shared constraints and acceptance conditions; seeds coherent observable capabilities; merges fragments lacking independent completion; and permits splits with separate outcomes, acceptance and interface/dependency rationale. A source file, phase, platform, CLI flag or requirement row alone does not justify another story.

Rust can validate accounting, dependency closure, duplicates, cycles and declared split reasons. It cannot prove good semantic granularity just because a graph is valid. Bounded adversarial review challenges the proposed boundaries and changes only demonstrated problems. No arbitrary score or cap substitutes for that review.

Illustrative groups were approximately six query stories and eight authority stories; fourteen was not a fixed implementation commitment. Query groups: foundation/coverage, structural navigation/inspection, lexical retrieval/ranking, candidate calls, freshness/lifecycle, integrated terminal qualification. Authority groups: common contracts, protected host, durable state, concrete workflow, snapshots, restricted evaluation, evidence/receipts, client/hooks. Actual readiness and the current implementation can change these boundaries. Shared protocol/provenance/error/generation rules must not be copied into divergent mini-specifications. Platform and TDD obligations normally remain cases within a story.

Each story preserves its selected outcomes and applicable checks. Epic completion still requires one identified integrated candidate, cross-story cases, the complete selected platform/quality scope and unresolved-defect accounting. All story status files saying done cannot supply acceptance.

## 6. Whole-framework direction

The user stepped back from a defect-specific control system to the DevForgeAI Adaptive Spec-Driven Engineering Framework: portable guidance with guardrails, a core engineering lifecycle, and project experts reflecting accumulated business, architecture, development and QA knowledge. Avoid disconnected silos or a framework assembled from unrelated fixes. Large framework work itself needs bounded planning iterations and durable navigation to survive context compaction.

The resulting [foundation set](../specs/framework/index.md) distinguishes skills (methods), expertise (grounded project knowledge/responsibility), and subagents (execution contexts). A project expert can contribute across workflows without copying the same domain facts into each role. Existing adaptive core/project_variant/expertise contracts are reused as inputs, with lineage and binding limitations preserved. No automatic fine-tuning, hidden permanent memory or continuous autonomous learning is claimed.

The user chose project-selected quality policies. DevForgeAI keeps its own Rust and 95% engineering rules. Current qa's hardcoded minimums, mock-decorator prohibition and stop semantics require explicit compatibility work rather than silently becoming universal product policy or being changed by this document.

Expert slippage is a proposed capability: track grounding changes/conflicts, responsibility coverage, behavior, routing/handoff failures and observed incorrect recommendations separately. Changed bytes are a review signal, not proof of a semantic defect. No single competence score, arbitrary age threshold or automatic operational rewrite was selected. The next work is a bounded evidence-baseline and realignment contract, with actual cases and scoped dependency review.

## 7. Latest feasibility and ambiguity constraints

The user subsequently required every base capability to work within Codex plus an individual ChatGPT Pro subscription and required ambiguities to be documented. This constrains every preceding proposal. No base dependency may assume separate API billing, Enterprise controls, unsupported hooks, unlimited contexts/agents, extracted credentials or an always-on LLM backend. Official documentation distinguishes subscription sign-in from API billing and describes usage limits; actual account/model support still requires observation. See the [operating boundary](../specs/framework/foundation.md#codex-and-chatgpt-pro-operating-boundary).

Protected OS identities, hosted GitHub controls, quota telemetry, exact subagent precedence and automatic continuation have explicit unresolved dependencies. A Pro subscription does not establish OS protection or a second independent trusted principal. Local deterministic Rust tooling is compatible in principle, but the required installation, privileges and host behavior must be specified and qualified before claiming readiness. Optional external integrations remain outside base dependencies.

The [ambiguity register](../specs/framework/roadmap-and-decisions.md#ambiguity-register) records exact questions, owners, resolution evidence and blocked claims. Recording uncertainty is required; filling it with an implementable-sounding guess is not completion. The current delivery is a reviewed planning baseline, with bounded next tasks for each capability.

## 8. Preservation and follow-up

This task changes only the new framework documentation, structural reference and documentation evidence. It does not modify original source/specifications, operational skills, startup/systemd, Git/GitHub settings, remote checkouts or previous QA attempts. No product tests are newly claimed. Follow the framework index and I1 next-session task before expanding this record into an implementation-ready contract.
