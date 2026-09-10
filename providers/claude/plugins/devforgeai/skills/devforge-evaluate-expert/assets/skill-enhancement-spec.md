---
schema_version: "devforge.artifact/v1"
artifact_id: "CHGSPEC-{{number}}"
artifact_type: "skill-enhancement-spec"
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

# Skill repair and enhancement specification

The bounded, evidence-backed change request returned to `devforge-project-expert-creator`. It authorises no automatic edit, invocation, installation, acceptance or release, and it carries forward the existing user authorisation without expanding it.

Give enough information to implement each change without replaying the discovery conversation. Where the cause is unproven, write a bounded investigation instead of a fabricated patch.

## Immutable intake

- **Evaluated candidate:** {{exact source identity, root and manifest reference}}
- **Installed copy evaluated:** {{mode, path and manifest reference, or not installed}}
- **Specification:** {{path, revision and digest}}
- **Evaluation report:** {{EVREPORT identity, path and digest}}
- **Results record:** {{path and digest}}
- **Independent review:** {{path and digest, or COULD_NOT_RUN with its cause}}
- **Cases and fixtures:** {{paths and digests}}
- **Prior iteration:** {{retained identity, or none}}

Preserve these identities exactly. The builder verifies them before editing and retains the old candidate.

## Change decision

- **Are target changes justified by the evidence?** {{yes / no}}
- **If no:** state that explicitly and list only the missing evaluation work and its owner. Do not send an empty repair task.
- **Next owner:** `devforge-project-expert-creator`
- **Behaviour that must be preserved unchanged:** {{unrelated behaviour, resources, identity and invocation policy}}
- **Forbidden scope changes:** {{what this specification does not authorise}}

## Requested changes

Repeat for each change.

### CHG-{{number}}: {{concrete desired behaviour}}

- **Finding IDs:** {{F-###}}
- **Severity:** {{BLOCKER/MAJOR/MINOR/ADVISORY, chosen from the demonstrated consequence}}
- **Change type:** {{required repair / authorised enhancement / unapproved proposal / bounded investigation}}
- **Accepted requirement, or a new proposal:** {{which it is, and its source}}
- **Affected revision, file and section:** {{exact locators}}
- **Evidence and reproduction:** {{locator, and the observation that demonstrates it}}
- **Demonstrated impact:** {{the actual consequence, not a rubric label}}
- **Bounded desired behaviour:** {{what should be true afterwards}}
- **Behaviour to preserve:** {{explicit}}
- **Acceptance condition:** {{how a later evaluation would recognise it}}
- **Affected reruns:** {{case IDs to re-observe after the change}}

## Implementation order

{{Dependencies between changes, where any exist. Otherwise state that they are independent.}}

## Evaluation prerequisites, not defects

{{Missing activation, loading, installed-resource or runtime observations, and the two missing DevForge CLI capabilities where they blocked a claim. Each with its owner. None of these authorises a target edit, and editing the candidate will not produce them.}}

## Closure rules

- **Applied** means the source was edited. It does not close a finding.
- A changed candidate is a new identity and needs new matching evidence before any finding is closed.
- Preserve the original failure history; never overwrite an earlier `FAIL`.
- Never weaken an accepted expectation, delete a case or change a sibling gate to convert a recorded failure into a pass. A defect in a shared contract goes to its integration owner.

**Validation status:** Not performed by this document.
**Finding status:** findings recorded; reevaluation required after any change.
