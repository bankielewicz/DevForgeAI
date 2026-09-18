# Template: Release record

**Producer:** planned core `release` (legacy `/release`)  
**Consumers:** operations; `feedback`; audit  
**Does not:** treat QA PASS as deploy permission, or fabricate native evidence for an untested platform.

## Envelope

| Field | Value |
| --- | --- |
| Release ID | REL-[utc] |
| Producer | release |
| Downstream consumer | operations / feedback |
| Failure behavior | Missing authorization or unmatched candidate → do not deploy |
| Non-claims | This record is not framework acceptance unless a live Rust receipt is attached |

## Upstream inputs

| Role | Locator | SHA-256 | Required? |
| --- | --- | --- | --- |
| QA report PASS | | | yes for this selected scope |
| Candidate identity | | | must match assessed bytes |
| Project policy delivery rules | | | |
| Release authorization | | | actual permission, not a checkbox |
| Framework acceptance receipt | | | if project requires it; else NOT_EVALUATED |

## Selected effect

- Effect requested: [publish / deploy / tag / promote]
- Target: [environment / channel]
- Authorization source: [who, when, scope]
- Excluded effects: [anything not granted]

## Preconditions actually checked

| Precondition | Evidence | Result |
| --- | --- | --- |
| Candidate matches QA-assessed hashes | | |
| Required platforms qualified | | |
| Unmet mandatory obligations | none / [list] | |
| Rollback / recovery plan | | |

If any required row fails, status is `BLOCKED`. Do not deploy.

## Execution

| Step | Command / action | Cwd | Result | Receipt |
| --- | --- | --- | --- | --- |
| | | | NOT_RUN / PASS / FAIL | |

Interrupted or partial apply: record actual state and bounded recovery. No automatic whole-project reset.

## Outcome

- Status: `RELEASED` / `PARTIAL` / `BLOCKED` / `NOT_ATTEMPTED`
- Identifiers created: [tag, artifact, URL]
- Unmet obligations remaining:
- Next action:

## Downstream handoff

**To operations:** identifiers and rollback references.  
**To feedback:** production observations start a new selected discovery or story; they do not silently rewrite policy.

**Return path:** authorization withheld, candidate drift, or missing platform returns to QA/dev/human — not a retry that ignores the gap.
