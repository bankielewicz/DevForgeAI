# Progressive disclosure authoring record

## Selection and ownership

User request: enhance only the Codex devforge-project-expert-creator, preserve five Enforced phases, support phased authoring and concise completion, preserve author-only/runtime boundaries, prepare seven focused cases, obtain one independent read-only patch review, and finish with one draft PR to main. No merge, installation, native campaign, other skill conversion, shared contract or Claude changes.

Selected DevForgeAI baseline: 8d2f22b82a08a25731c1be05e91f55247d1026ad, verified equal to local main and fetched origin/main on 2026-09-11; shared checkout was clean. Task branch: author/codex-creator-phases-20260911. Worktree: /home/bryan/Projects/DevForge/worktrees/codex-creator-phases-20260911. Exclusive changed source: providers/codex/plugins/devforgeai/skills/devforge-project-expert-creator/**. This session owns only this candidate and draft PR; repository integration/merge remains with the user-designated integration owner. Claude has independent ownership and is untouched.

Governing sources at the selected baseline: AGENTS.md; docs/mvp/skill-authoring-contract.md; docs/mvp/specifications/skill-007-devforge-project-expert-creator.md; docs/development-language-policy.md; package-local contract derivatives and assets. System skill-creator guidance was read for progressive disclosure and Codex metadata; no Claude-only metadata rules applied. No hook events or provider behavior newly asserted.

Selection: enhance the explicitly assigned canonical Codex workflow. It already owns creator behavior and the five required actions. Installed/exported sources were not edited; no duplicate skill was created. This narrow assignment does not reopen the accepted target choice or classifications.

## Requirement and change specification

| ID | Accepted change / finish condition | Candidate locations |
| --- | --- | --- |
| PD01 | Creator uses its five Enforced phases with direct links, essential entrypoint boundaries and conditional detail loading; target workflows use meaningful phases without a forced count. | SKILL.md; phases/; assets/phase.md |
| PD02 | Enhance inline instructions with an old-to-new obligation map; preserve accepted behavior, IDs, decisions and scope; isolate proposed behavior changes. | phases/03-design.md; phases/04-authoring.md; assets/skill-design-spec.md section 13 |
| PD03 | Compare purpose, activation, provider, inputs, outputs and behavior; same-provider reuse and provider separation. | phases/02-selection.md; references/existing-skill-selection.md |
| PD04 | Use relevant framework or project inputs; simple reference experts need no ceremonial phases. | phases/01-intake.md; phases/03-design.md; template section 13 |
| PD05 | Preserve Optional/Enforced choices, conditional applicability, dependencies and actual Rust enforcement owner; no invented gate. | phases/03-design.md; assets/phase.md; template section 13 |
| PD06 | Full retained evidence and evaluator handoff; terminal outcome/result/primary links/material blocker/one next action-owner; 60–120 words when practical. | phases/05-prepared-transfer.md; assets/handoff.md; assets/completion-summary.md |
| PD07 | Missing inputs/support remain explicit; authoring, independent review, execution and acceptance remain distinct. | SKILL.md; all phase exits; seven added eval cases |

Stop after scoped correction, source checks, one independent read-only review and one draft PR. No additional infrastructure or conversion tranche is implied.

## Preservation and five-phase action mapping

The original SKILL.md is retained exactly by the baseline commit above. Section-level relocation below preserves all paragraphs unless a specific authorized adaptation is noted. References in moved sections now resolve via ../references or ../assets from phases/.

| Original section / obligation | New location | Disposition |
| --- | --- | --- |
| Identity, purpose, author-only prohibition including delegated target execution, observed file identity limits | SKILL.md Scope and authority | Preserved; activation now explicitly includes workflow skills. |
| Hook design only; no handlers/configuration/activation or enforcement claims | SKILL.md Scope and authority; phases/03-design.md | Preserved; Rust authority and Python evaluation-only boundary made explicit. |
| Manual invocation, implicit discovery, legacy skill-builder/skill-validator IDs, no managed fallback/scheduling | SKILL.md Invocation, completion and stops | Preserved. |
| Enforced workflow table: Intake authority/source/write-fence; Selection discovery/collisions; Design Q&A/spec/classifications; Authoring canonical/grounded files; PreparedTransfer exact artifacts/handoff | SKILL.md phase map and respective numbered files | All five names, classifications and required actions preserved; no CLI commands invented. |
| Recover framework authority and target: source identities, contract pins, unknowns, accepted versions, canonical mapping, sibling boundaries | phases/01-intake.md | Preserved; application architecture/code required only when relevant to target expertise. |
| Choose entry path: use supplied context, no blanket approval, conditional frozen-remediation intake | phases/01-intake.md | Preserved. |
| Search existing owner: catalog/source search, aliases, comparison, justified reuse/enhance/create, limits, collisions, retained remediation decision | phases/02-selection.md | Preserved; explicit independent provider comparison added. |
| Populate specification: selected template identity, separate working document, resumed Q&A, expected cases without execution, no inferred approval | phases/03-design.md | Preserved; phase/preservation/display fields added through section 13. |
| Classify: stable IDs/parents, only new unresolved items, named groups, no parent inheritance, applicability/skips, pending dependent design | phases/03-design.md | Preserved. |
| Propose hooks: every enforced item traceable, evidence/freshness/owners, official provider support, feasibility distinct from requirement, design-only status | phases/03-design.md | Preserved; reuse accepted proposals and design only missing enforced mechanisms. |
| Author canonical: settled inputs, system skill-creator without helpers/tests, precise frontmatter/discovery, necessary resources, implicit policy, preserve prior bytes/collisions, derivations, separate install | phases/04-authoring.md | Preserved; phased target authoring and explicit implementation-language boundary added. |
| Deliver content: handoff at completion/transfer/recovery only, concise links to full rationale/pins/change dispositions, F/CHG mapping, retain former bytes | phases/05-prepared-transfer.md | Preserved; terminal display template added. |
| Managed final identity/receipt/readback ownership, no self digest, creation-time observations immutable; no automatic evaluator, validation not performed | phases/05-prepared-transfer.md; SKILL.md | Preserved. |
| Owner-selected local unqualified baseline path, no Full qualification inference | phases/05-prepared-transfer.md; unchanged manual reference | Preserved. |

No existing cases or historical results were removed. PD01–PD07 cases are authored inputs, not observations. The new synthetic fixture labels its facts and assigns materialization to a separate evaluator; no target behavior was executed during authoring.

## Packaging inspection and limits

Read-only inspection of companion DevForge at 8719300b0084edb37aa7f22a0cab7e93c74dd967 found recursive runtime resource selection in src/install.rs: authoring_only (line 3833), regular_files (3848), runtime_skill_files (3877), project planning (4457) and manual expert planning (4686). The selection excludes evals/history/cache/provenance files, not phases/. Thus ordinary regular phase Markdown files are selected by this source logic. No installer/export operation or native loading was executed; source inspection is not successful installation.

Existing package manual command references include legacy Python tools. Their migration belongs to DevForge; this assignment neither extends them nor refreshes their command contracts. Rust owns authoritative framework decisions. No new runtime feature is needed to deliver this authoring refactor.

## Verification and next ownership

Source inspection covers the five-phase mapping, relative link routing, template fields, existing case retention and resource selection. Execution/check and independent review results are recorded in the draft PR against its exact candidate commit. This record makes no prior claim that those checks passed.

Behavior evaluation: NOT_RUN. Native activation/resource loading: NOT_RUN. Installation/export: NOT_RUN. Runtime admission/acceptance: not claimed. Independent patch review is separate from creator self-validation.

Next: the independent read-only reviewer examines the frozen candidate patch and reports findings; after scoped corrections, the author opens one draft PR. Any later native evaluation, integration or installation requires its separate owner/assignment.
