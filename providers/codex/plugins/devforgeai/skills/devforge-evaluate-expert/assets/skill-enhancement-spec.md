---
schema_version: "devforge.artifact/v1"
artifact_id: "SENH-{{number}}"
artifact_type: "skill-enhancement-spec"
project_id: "{{project-id}}"
revision: 1
status: draft
created_at_utc: "{{actual-UTC-time}}"
producer:
  skill: "devforge-evaluate-expert"
  skill_revision: "{{exact-loaded-validator-revision-or-digest}}"
execution_ref: null
upstream: []
evidence: []
supersedes: null
decision_ref: null
missing_inputs: []
---

# Skill repair and enhancement specification

This paired-utility artifact is consumed by devforge-project-expert-creator. It is not a DevForge CLI acceptance schema. The validator evaluates and writes this document; it does not apply the changes.

## Immutable intake

| Input | Identity / path / SHA-256 |
| --- | --- |
| Evaluated skill | {{canonical source; provider; complete source manifest}} |
| Installed skill | {{separate mode/path/manifest}} |
| Original design specification | {{revision, exact file and requirement IDs}} |
| Verification report / decision | {{completed paths and hashes; unavailable receipt explained}} |
| Validation plan / cases / rubric | {{frozen references}} |
| Previous change specification | {{reference or none}} |
| Existing authorization | {{user task or authority record; scope limits}} |

Next implementation owner: devforge-project-expert-creator.
Validation owner after authoring: devforge-evaluate-expert.
External acceptance owner: {{actual owner or missing_inputs}}.

## Change decision

Target changes justified: {{yes/no}}.
Reason: {{supported defects, authorized enhancements, or no demonstrated target defect}}.
Evaluation prerequisites only: {{runtime, authentication, boundary, missing evidence, or none}}.

Missing observations alone do not justify rewriting the target. If no change is justified, keep the change list empty and provide only the evaluation continuation.

## Allowed scope and invariants

- Canonical provider/source write fence: {{specific files/directories}}.
- Preserved behavior and public inputs/outputs: {{requirement IDs and examples}}.
- Protected evaluator, policy, fixtures and unrelated skills: {{paths and governing identities}}.
- Existing Optional/Enforced choices: {{item IDs, user decision source, exceptions}}.
- New unresolved choices: {{only material new requirements, otherwise none}}.
- Compatibility and resource mapping: {{packaged assets, runtime dependencies, installed-generation scope}}.
- This specification does not activate hooks, alter global settings, publish, or grant adoption.

## Requested changes

Repeat for each CHG-###. An advisory proposal requires applicable authorization before it becomes an implementation requirement.

### CHG-{{number}}: {{concrete desired behavior}}

- Classification: {{required repair / authorized enhancement / unapproved proposal / bounded investigation}}.
- Findings and severity: {{F-###; impact-based severity}}.
- Accepted requirement or proposal source: {{exact reference, requirement IDs}}.
- Target identity and locations: {{frozen source manifest; file/section}}.
- Reproduction evidence: {{case/attempt; raw file/transcript references and SHA-256}}.
- Current behavior and demonstrated consequence: {{observed facts}}.
- Required resulting behavior: {{specific inputs, action, output, failure behavior}}.
- Implementation constraints: {{scope, supported runtime, dependency constraints}}.
- Preserve: {{invariants and regression cases}}.
- Do not change: {{governing requirements, evaluator expectations, unrelated workflows}}.
- Acceptance observations: {{observable assertions; not "improve quality"}}.
- Affected reruns: {{deterministic check IDs; AI criteria; C/B/A cases; baseline and repeat treatment}}.
- Uncertainty: {{known cause, or bounded investigation question and evidence needed}}.
- Enforcement treatment: {{reuse settled classifications; new Optional/Enforced choices if needed; hook proposal reference}}.

## Implementation order and dependency map

| Order | Change ID | Depends on | Owner | Completion record |
| --- | --- | --- | --- | --- |
| {{n}} | {{CHG-###}} | {{IDs or none}} | devforge-project-expert-creator | {{authored files and change receipt}} |

## Builder return record

The builder authors the changes and a separate return record. It does not mark them validated.

| Finding / change | Applied, deferred or declined with reason | Old path / digest | New path / digest | Preserved requirement IDs |
| --- | --- | --- | --- | --- |
| {{F / CHG}} | {{state and authority}} | {{identity}} | {{identity}} | {{IDs}} |

- New complete candidate manifest: {{path and SHA-256}}.
- Updated design specification: {{path, revision, SHA-256}}.
- Generated installation mapping: {{named source-to-installed files; collision decisions}}.
- Validation status: Not performed by devforge-project-expert-creator.
- Hook status: {{Design only unless separately authorized and actually implemented outside builder}}.
- Unresolved questions / prerequisites: {{bounded items and owners}}.

## Validator retest and closure

| Finding / preserved requirement | New revision | Required checks / cases | Evidence required to close | Closure owner |
| --- | --- | --- | --- | --- |
| {{F / requirement}} | {{new manifest}} | {{IDs and affected tiers}} | {{matching observed outcome, exact evidence}} | devforge-evaluate-expert |

Retain the old FAIL and old candidate. A builder statement that a fix was applied does not close a finding. Reevaluate affected dependencies; keep unrelated prior evidence only when its frozen inputs still match. External acceptance remains a separate authority decision.
