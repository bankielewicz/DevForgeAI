---
schema_version: "devforge.artifact/v1"
artifact_id: "EVREPORT-{{number}}"
artifact_type: "expert-evaluation-report"
project_id: "{{project_id}}"
revision: 1
status: draft
created_at_utc: "{{actual-ISO-8601-UTC-time}}"
producer:
  skill: "devforge-evaluate-expert"
  skill_revision: "{{digest of the loaded SKILL.md file, or unknown with a reason}}"
execution_ref: "{{SESSION-ID}}@{{revision}}, or null with the reason in missing_inputs"
upstream: []
evidence: []
supersedes: null
decision_ref: null
missing_inputs: []
---

# Skill verification results

Fill a copy in the assigned evidence location; never fill this template in place. This report is the human-readable EVREPORT content. `validation-results.json` holds the machine-readable per-check outcomes and is referenced from here rather than restated.

## Identity and scope

- **Evaluation plan:** {{EVPLAN identity, path and digest}}
- **Candidate source identity:** {{root and file manifest reference}}
- **Installed candidate identity:** {{installation mode, absolute path and manifest reference; or not installed, with the reason}}
- **Specification:** {{path, revision and digest}}
- **Baseline:** {{old_skill with its preserved identity, or without_skill, or NOT_RUN with the reason}}
- **Client, version and model configuration:** {{observed values, or unknown}}
- **Assignment and write fence:** {{owner, permitted writes, report destination}}
- **Independence conditions actually met:** {{what was separated, and what was not}}
- **Scope of this evaluation:** {{what it covers and explicitly does not}}

## Evidence groups and outcomes

Report each group separately. Do not merge them into a single figure.

| Group | Observations | Outcome | Evidence | Limits |
| --- | --- | --- | --- | --- |
| Intake and freeze | {{frozen identities}} | NOT_RUN | {{locator}} | {{limit}} |
| Structure (manual observation) | {{what was read}} | NOT_RUN | {{locator}} | Method: INSPECTION_MANUAL; authority: none |
| Independent review R01-R10 | {{per-criterion summary}} | NOT_RUN | {{locator}} | {{independence limits}} |
| Tier C installed resources | {{cases}} | NOT_RUN | {{run manifests and grades}} | {{limit}} |
| Tier B output quality | {{cases and arms}} | NOT_RUN | {{run manifests and grades}} | {{limit}} |
| Tier A discovery and activation | {{cases; explicit and implicit kept separate}} | NOT_RUN | {{run manifests and grades}} | {{limit}} |

## Candidate and baseline comparison

| Case ID | Candidate evidence | Candidate outcome | Baseline evidence | Baseline outcome | Constraint violations |
| --- | --- | --- | --- | --- | --- |
| {{case}} | {{artifact reference}} | NOT_RUN | {{artifact reference}} | NOT_RUN | {{findings}} |

An incomplete baseline supports no improvement claim. Disclose order sensitivity, identity leakage, effective tool assistance and sampling limits before stating any comparison.

## Findings

| Finding ID | Type | Severity | Requirement | Evidence | Demonstrated impact | Affected cases |
| --- | --- | --- | --- | --- | --- | --- |
| F-001 | {{defect/enhancement/evaluation_gap}} | {{BLOCKER/MAJOR/MINOR/ADVISORY}} | {{ID}} | {{locator}} | {{consequence}} | {{case IDs}} |

## Missing capabilities and evaluation prerequisites

Record both statements in every report, whatever the observations were.

- **Skill-package structural inspection (S001-S013) and evidence reduction are not implemented in the DevForge CLI.** Structural facts here were obtained by reading and are labelled `INSPECTION_MANUAL` with `authority: none`. Owner: DevForge integration owner.
- **Protected-manifest custody for the evaluation runner is not implemented in the DevForge CLI.** Runner, grader, runtime and case identities are self-reported by the run. Owner: DevForge integration owner.
- {{Any other prerequisite: unavailable runtime, authentication, observation channel or authority, with the claim it blocks and its owner.}}

These are prerequisites, not defects in the candidate.

## Decision and coverage

- **Disposition:** {{revise / insufficient evidence / suitable for the stated scope}}
- **Basis:** adjudicated against the results contract by hand; no implemented decision receipt exists.
- **Behavioural status:** NOT_EVALUATED
- **Coverage actually obtained:** {{which required groups are complete}}
- **Required observations not obtained:** {{each with its cause}}
- **Observed metrics:** {{values, or unavailable}}
- **Adoption reference:** null
- **Handoff reference:** {{HANDOFF identity}}

*Suitable for the stated scope* is a recommendation. It is not acceptance, adoption or release.

## Recovery and continuation

- **Last completed phase:** {{phase}}
- **Frozen input digests still matching:** {{yes, or the observed drift}}
- **Owned processes and workspace disposition:** {{retained / released, with the operator reference}}
- **Conditions invalidating this report:** {{candidate, installed copy, specification, fixture, baseline or runtime changes}}
