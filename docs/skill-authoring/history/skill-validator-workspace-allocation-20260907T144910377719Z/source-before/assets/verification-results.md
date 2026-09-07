---
schema_version: "devforge.artifact/v1"
artifact_id: "SEVAL-{{number}}"
artifact_type: "skill-evaluation-report"
project_id: "{{project-id}}"
revision: 1
status: draft
created_at_utc: "{{actual-UTC-time}}"
producer:
  skill: "skill-validator"
  skill_revision: "{{exact-loaded-validator-revision-or-digest}}"
execution_ref: null
upstream: []
evidence: []
supersedes: null
decision_ref: null
missing_inputs: []
---

# Skill verification results

Populate this copy from retained observations. Use null plus missing_inputs for absent authority metadata; do not invent execution or adoption references. Replace every placeholder. Apply the definitions in the packaged results contract.

## Identity and scope

| Item | Exact value / evidence locator and SHA-256 |
| --- | --- |
| Run and evaluation owner | {{run_id; actual assignment; permitted outbox}} |
| Candidate source | {{root, revision if real, complete relative-file digest manifest}} |
| Actual installed package | {{provider, installation mode, path, separate manifest}} |
| Specification and requirements | {{exact specification; selected requirement IDs}} |
| Framework and rubric | {{selected revisions, reference files, derivation freshness}} |
| Cases and fixtures | {{frozen definitions; raw facts; worker-visible versus operator-only}} |
| Baseline | {{old_skill or without_skill; preserved identity and reason}} |
| Runtime | {{client/version/model configuration; observable tool availability}} |
| Independence and boundary | {{reviewer identity; client history/memory; filesystem/source access; process probes}} |
| Budget and sampling | {{planned/actual attempts and time; unused budget; limitations}} |
| Previous iteration | {{prior report/change receipt/finding IDs, or none}} |

Scope exclusions were fixed before observation: {{each exclusion, requirement and reason; none when none}}.
Actual user feedback/adoption: {{verbatim short feedback or absent; decision source only if actual}}.

## Evidence and outcomes

| Evidence group | Planned checks / attempts | PASS | FAIL | NOT_RUN | COULD_NOT_RUN | NOT_APPLICABLE | Raw files / hashes | Scope limits |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Intake and frozen inputs | {{IDs}} | {{count}} | {{count}} | {{count}} | {{count}} | {{count}} | {{refs}} | {{limits}} |
| Deterministic structure | {{IDs}} | {{count}} | {{count}} | {{count}} | {{count}} | {{count}} | {{source and installed reports}} | {{parser/coverage limits}} |
| Independent AI review | {{R01-R10}} | {{count}} | {{count}} | {{count}} | {{count}} | {{count}} | {{review refs}} | {{independence/disagreements}} |
| C: installed resources | {{IDs}} | {{count}} | {{count}} | {{count}} | {{count}} | {{count}} | {{run and grade refs}} | {{source visibility proof}} |
| B: output quality | {{IDs and arms}} | {{count}} | {{count}} | {{count}} | {{count}} | {{count}} | {{run and grade refs}} | {{comparison limits}} |
| A: discovery / activation | {{explicit/direct/indirect/negative}} | {{count}} | {{count}} | {{count}} | {{count}} | {{count}} | {{run and grade refs}} | {{selection vs loading vs completion}} |

Do not combine these groups into a pass percentage. Counts do not replace per-case evidence. List every planned check in validation-results.json, including unrun and unavailable work.

## Candidate and baseline comparison

| Case / attempt | Candidate outcome and evidence | Baseline outcome and evidence | Required behavior / observed difference | Assistance and sampling limits |
| --- | --- | --- | --- | --- |
| {{ID}} | {{outcome; refs}} | {{outcome; refs}} | {{requirement; observation}} | {{tool use; configuration; uncertainty}} |

A completed failing baseline is comparison evidence; it does not automatically fail the candidate. Missing baseline observations remain incomplete. No causal improvement claim without support.

## Findings

Repeat this block for each finding, or state "No supported target findings" with coverage limits.

- ID / type / severity: {{F-###; defect/enhancement/evaluation_gap; BLOCKER/MAJOR/MINOR/ADVISORY}}
- Requirement or proposed addition: {{requirement IDs and selected source; mark new suggestion as proposal}}
- Affected identity and location: {{candidate manifest; exact file, section, lines where useful}}
- Evidence: {{path, exact SHA-256, relevant section or transcript event}}
- Observation and impact: {{concrete expected/actual difference and consequence}}
- Confidence and dispute: {{supported/uncertain; contrary evidence and resolution}}
- Recommended disposition: {{bounded correction, optional enhancement, investigation, or runtime prerequisite}}
- Related change and rerun cases: {{CHG-###; case IDs; preserved behaviors}}

## Decision and coverage

- Reducer inputs and receipt: {{plan/results/decision paths and SHA-256, or actual error and missing receipt}}
- Required-check outcome: {{PASS / FAIL / NOT_RUN / COULD_NOT_RUN; preserve mixed incomplete coverage}}
- Behavioral status: {{NOT_EVALUATED / supported scoped case outcomes; no global certification}}
- Coverage complete: {{true/false, with every missing item}}
- Proposed disposition: {{revise / suitable_for_stated_scope / insufficient_evidence}}
- Reason: {{findings and evidence supporting that disposition}}
- External acceptance: NOT_GRANTED unless a separately identified authority actually grants it.
- Adoption reference: null unless supported by an actual decision.
- Source freshness at handoff: {{current identity comparison and timestamp; changed inputs invalidate dependent claims}}

## Recovery and continuation

| Missing observation / remaining task | Cause | Next owner | Prerequisite | Required evidence |
| --- | --- | --- | --- | --- |
| {{ID}} | {{actual cause}} | {{operator / skill-builder / skill-validator}} | {{specific requirement}} | {{receipt / revised bytes / rerun}} |

- Builder specification: {{completed path and SHA-256}}.
- Retest scope: {{affected cases plus required regressions; no reuse across stale dependencies}}.
- Output custody: {{permitted outbox; completed files read back}}.
- Limits: {{unavailable features, unresolved AI judgment, unobserved performance or native behavior}}.
