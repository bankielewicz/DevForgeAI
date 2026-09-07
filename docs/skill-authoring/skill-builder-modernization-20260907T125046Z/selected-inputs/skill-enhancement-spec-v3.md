---
schema_version: devforge.artifact/v1
artifact_id: SENH-skill-builder-20260907T122152Z
artifact_type: skill-enhancement-spec
project_id: DevForge
revision: 3
status: draft
created_at_utc: '2026-09-07T12:47:23.449239+00:00'
producer:
  skill: skill-validator
  skill_revision: e8310693ad1b756f85a57ec96bab4b0fe2ea3d75c70f1fe5143b416e9122516c
execution_ref: null
upstream:
- artifact_id: SENH-skill-builder-20260907T122152Z
  revision: 1
  store: assigned-evaluation-root
  path: /home/bryan/Projects/DevForge/framework/DevForgeAI/.poc/codex/skill-builder-workspace/skill-builder-20260907T122152Z/skill-enhancement-spec.md
  sha256: 597df2dc9b986c88fa7234d74818ed7a080432b57d246d91a61d1dd530cbffed
  sections:
  - CHG-001
  - CHG-002
  - CHG-003
evidence:
- path: /home/bryan/Projects/DevForge/framework/DevForgeAI/.poc/codex/skill-builder-workspace/skill-builder-20260907T122152Z/modernization-inputs/source-record.json
  sha256: 43889f556f5917a797f9c5e54e31a13ece5d92321120dca51f0c0344394835aa
- path: /home/bryan/Projects/DevForge/framework/DevForgeAI/.poc/codex/skill-builder-workspace/skill-builder-20260907T122152Z/ai-review.json
  sha256: 01eb3318c03a9e7b2904524edcda04854f15b0617aa1de86843399b2ebdb1805
supersedes:
  artifact_id: SENH-skill-builder-20260907T122152Z
  revision: 2
  path: /home/bryan/Projects/DevForge/framework/DevForgeAI/.poc/codex/skill-builder-workspace/skill-builder-20260907T122152Z/skill-enhancement-spec-v2.md
  sha256: 155d18956d6e7af785440dfd93268bee2437d73d5b8bc85ac3c0ef944409c8f1
decision_ref: null
missing_inputs:
- Builder/validator managed runtime adapter and its separately allocated implementation/verification
- Observed native integration and delivery
---

# Skill-builder modernization amendment

This revision supersedes skill-enhancement-spec-v2.md by making the builder handoff template an explicit deliverable. It retains the modernization correction to CHG-003 and the runtime-owned receipt approach in CHG-001. It preserves the earlier measured findings, outcomes, frozen inputs and reports.

## Governing direction

The user clarified that DevForgeAI modernization removes ceremonial skill instructions in favor of Codex hooks, runtime phases and gates. Prose is guidance; a statement that a step is mandatory is not evidence that the runtime enforces it.

Use the current revision-3 authoring and execution contracts for this modernization design. Keep the earlier evaluation bound to its original selected inputs; do not rewrite it as a revision-3 conformance result.

## Responsibility boundary

| Owner | Required responsibility |
| --- | --- |
| skill-builder | Understand the user's need; search for existing skills; resolve consequential questions; capture Optional/Enforced choices; write or enhance the specification and skill; supply substantive evidence in the runtime-provided checkpoint shape. |
| Protected runtime and hooks | Select and supply the active phase, accepted inputs, output paths, evidence shape and fresh challenge; check phase prerequisites; preserve accepted state; control transition, waiting and bounded correction; check actual final files; publish/read back the authoritative receipt. |
| skill-validator | Inspect prompt quality and artifacts, run supported deterministic and behavioral evaluations, and return evidence-backed findings. A semantic judgment is a recorded gate input, not self-issued authority to pass the gate. |
| User/integration owner | Select actual task scope, governing source and required controls; own shared runtime/hook changes and external acceptance. A runtime event does not imply user adoption. |

Semantic instructions remain necessary. Keep concrete interview questions, duplicate-selection logic, domain facts, useful examples, failure interpretation and intended artifact meaning. Remove repeated status declarations, manual phase-advance rituals, self-certification and model-managed delivery verification.

A phase checkpoint must identify actual artifacts/evidence. A checkbox, prose "done" marker, phase heading, or model confidence cannot prove that the work happened. Deterministic checks establish observable predicates; human intent and semantic quality still require appropriate evidence/review.

## Revised changes

### CHG-001: Eliminate circular and model-managed completion receipts

F-001 remains a supported MINOR static defect: the inline specification receipt requests the containing specification's own hash.

Remove the circular current-document digest field. For managed operation, the runtime computes final file identities after the model saves its useful outputs, preserves the selected snapshot and supplies the authoritative external receipt. The model must not manually drive advance/resume/complete/check/verify or a receipt-helper fallback.

Keep the handoff's substantive content: decisions versus proposals, unresolved work, relevant artifact references and the next useful task. Record creation-time observations accurately; never rewrite the handoff to claim a later runtime check or receipt existed when it was written.

Acceptance: no artifact contains its own complete-byte digest; runtime-owned final checks bind actual completed bytes; changing those bytes prevents the dependent completion claim. Semantic handoff content remains recoverable.

### CHG-002: Correct selected-source identity and perform an explicit controlled refresh

F-002 remains a supported MINOR static defect: the builder's execution-contract summary says revision 2 while its pinned source is revision 3. Correct the declaration against the already-pinned source and update the destination derivation identity.

For modernization, explicitly select current revision-3 governing sources and reconcile the affected builder/validator instructions and derived resources. Preserve prior source bytes and evaluation history. Do not silently edit the shared contracts or reinterpret old results.

Acceptance: package labels, selected source bytes, resource meaning and derivation records agree. Source freshness alone grants neither runtime support nor behavioral acceptance.

### CHG-003: Replace the prior handoff-checklist recommendation with runtime integration

Do not add a longer prose checklist merely to create a heading named Handoff. The existing outgoing receipt text and incoming validator handoff guide are not proof of a controlled builder-to-validator transition.

Specify and implement the builder workflow's runtime contract before claiming enforced handoff:
1. Declare the actual allowed phase transitions and required versus optional items, using preserved user classifications.
2. Give the model the current phase, permitted outputs and concrete evidence shape.
3. Check required artifacts and selected evidence before allowing the dependent phase or completed handoff.
4. Preserve waiting state when a material user answer is missing. Arrival of a new message alone does not prove the required answer or adoption.
5. Reject stale, replayed, wrong-phase, missing or invalid evidence; bound corrections and deadlines.
6. Runtime owns final identity checks, immutable state and completion-receipt publication/readback. Keep human-readable continuation content separate from mechanical completion status.

**Required deliverable: a reusable skill-builder assets/handoff.md template.** Derive it from the same selected shared handoff contract used by skill-validator, with source/destination derivation records. Populate it at actual authoring completion, transfer, or a recovery checkpoint; do not generate a new handoff for ordinary read-only discussion.

The template must carry the current task/phase state, exact authored skill/specification references, decisions versus proposals, remaining issues, existing authorization/write scope, next owner, prerequisites, completion evidence, copyable continuation prompt, and invalidation/custody conditions. It must distinguish a prepared handoff document from an admitted runtime transition and an actually invoked receiving skill.

Keep substantive content model-authored. Runtime-controlled fields and completion receipts come from actual runtime observations; absent observations remain explicit. No current document self-digest, model-issued gate approval, manual phase-advance ritual, or claim that a template by itself enforces handoff is permitted. Reuse shared schemas and load the template only when the delivery/checkpoint condition applies.

Acceptance: skipping a required phase or supplying a marker without evidence cannot complete the workflow; unmet prerequisites remain blocked/incomplete; a valid bounded run produces the correct artifacts and an independently observed runtime receipt. No new per-phase human approval ceremony is introduced.

## Impact on skill-validator

Apply the same architecture to the validator's six phases. Keep its useful inspection, AI rubric, case definitions, evidence interpretation and repair recommendations. Runtime-owned state should control admission to dependent testing and completion.

The current validator's H1-H5 PreToolUse/Stop hook proposals belong to its older design. Do not activate them blindly alongside the modern managed-session callbacks or claim that those proposals are the framework's current implementation. An owned integration task must reconcile event coverage, schemas, protected state, failure behavior and provider configuration.

A model-produced PASS record or a reducer that checks declared evidence identities cannot independently authenticate native execution, prove semantic truth or authorize release. Required gates consume accepted evidence from the allocated producers and retain their scope limits.

## Current support and work boundary

The current documented managed runtime is specialized to brainstorm: Recover, Explore, Record, Focus, with its own session/checkpoint schema. Its current provider source declares synchronous SessionStart, UserPromptSubmit, Stop and SessionEnd hooks. That is not evidence of a generic builder/validator phase engine.

Shared contracts still report native admission not validated and native activation/rendered delivery not observed. Therefore this amendment defines required modernization work; it does not claim builder/validator runtime integration or active enforcement exists.

Skill source changes belong to skill-builder. Shared runtime adapters, schemas, hook registration and installer changes belong to their allocated integration owner. A missing adapter is an implementation gap, not a reason to substitute ceremonial prose and call it enforced.

## Validation and handoff

Retain the previous two static findings and the native COULD_NOT_RUN outcomes. The existing source/installed builder remains unchanged by this amendment.

A future implementation needs separate evidence for:
- Useful authoring behavior and artifact content, including realistic Q&A and duplicate handling.
- Deterministic transition/gate behavior with invalid, missing, stale and replayed evidence.
- Waiting, bounded correction, deadline and protected-state behavior.
- Actual native callback coverage, single effective callback handling, denial/continuation and receipt delivery.
- Builder-to-validator transfer without self-certification or lost context.

No new validation, target edits, hook activation, runtime changes or acceptance are performed by this recommendation update.
