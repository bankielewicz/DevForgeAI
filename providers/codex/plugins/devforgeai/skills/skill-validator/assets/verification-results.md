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

## Workspace preparation and native continuation

- Selected environment and carried authorization: {{actual choice and source}}.
- Frozen workspace allocation references/count/paths: {{saved path and SHA-256, or non-Git reason}}.
- Preparation observations: {{saved setup references; actual retained paths and statuses}}.
- Remaining native inputs/readiness: {{model/auth/budgets/observations/boundaries still missing; no inference from creation}}.
- Complete experiment plan and attempt/workspace/client-state bindings: {{saved refs, or explicit pending cause}}.
- Additional workspaces: {{new bounded allocation or none; no silent independent-attempt reuse}}.
- Protected runtime admission/integration status: {{actual evidence or unavailable; no active-enforcement claim from templates}}.

Prepared workspaces can be delivered with native execution NOT_RUN and dependent observations COULD_NOT_RUN. Preserve all old allocations, setup records, plans and attempts. No cleanup, acceptance or release follows from preparation.

## VPR-2 selection and outcome accounting

For an externally selected VPR-2 validator assignment, populate the following from the frozen v2 plan and actual evidence. Other-provider and legacy reports retain their original governing policy and native obligations. The artifact envelope remains devforge.artifact/v1; it is not a protected admission or acceptance receipt.

- Policy/mode and owner acceptance pin: {{VPR-2; Routine or Full; exact source/acceptance hashes, or legacy policy}}
- Actual requested claim: {{exact wording and whether its release/support contract requires Full}}
- Owner-accepted baseline/scope and destination: {{exact identities and authority, or missing}}
- Immediate and cumulative impact: {{both diff pins, fixed anchor, affected requirement/dependency union, CI-01–CI-09 union}}
- Compatibility: {{CP-01–CP-04 dispositions and used-capability evidence; unresolved changed components remain explicit}}
- Independent T04 review: {{actual selected producer, frozen plan/review pins, selection judgment and separate R01–R10 outcomes}}
- Current routinely accepted candidate/environment: {{actual owner record identity, or none}}
- Last fully qualified candidate/environment: {{exact anchor and Full evidence, ABSENT or UNKNOWN; Routine does not move it}}
- Accepted unqualified anchor/acceptance chain: {{actual source when no qualified anchor exists; never silently reset}}

- Enforced task accounting: {{all T01–T12, with separate selection/disposition and observation outcome; every P1–P6 remains Enforced}}
- Assertion coverage: {{complete original catalog/variant/arm mapping, D/S/N evidence kinds, gaps and genuine scope exclusions}}
- Shared observations/batched grades: {{conditions, exact raw-output pins, separate arm/assertion judgments and correlation/sample limits}}
- Target receiving transfer before T09: {{eligible actual target output, receiver load and required action/negative disposition, or missing/unselected}}

- Run manifests/transcripts/grades: {{paths and hashes}}
- Human feedback: {{actual feedback or not obtained}}
- Resource measurements: {{observed values or unavailable}}
- Proposed disposition: {{revise / suitable for stated scope / insufficient evidence}}
- Report completion: {{COMPLETE / PARTIAL / BLOCKED; completeness is not validation PASS}}
- Validation disposition: {{ROUTINE_PASS / FULL_PASS / FAIL / INSUFFICIENT_EVIDENCE under v2, or actual legacy outcome}}
- Routine adoption eligibility: {{true/false with exact authority, byte, scope and required post-install check basis; not human approval}}
- Qualification claim and limits: {{exact current Full evidence scope or no current qualification for these bytes}}
- Behavioral status: NOT_EVALUATED
- Unavailable or excluded observations: {{cause and effect on scope}}
- Required refresh and next owner: {{bounded task}}
- Adoption reference: null
- Prepared evaluator handoff: {{path/hash and next owner; no recursive qualification or receiving invocation implied}}
