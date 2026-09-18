# Template: RCA

**Producer:** planned `rca` (legacy `/rca`)  
**Consumers:** `story-create` (recommendations), `project-policy` realignment, human  
**Does not:** replace the first red test, rewrite oracles to obtain a pass, or auto-repair.

Use after repeated or systemic failure (TDD loops, integration, QA, workflow breakdown), not as a default after one failing test.

## Envelope

| Field | Value |
| --- | --- |
| RCA ID | RCA-[utc] |
| Mode | tactical (fix prescription) / strategic (multi-why document) |
| Producer | rca |
| Downstream consumer | story-create / human / policy owner |
| Failure behavior | Insufficient evidence → INCOMPLETE analysis, not a guessed cause |
| Non-claims | Recommendations are not requirements until selected |

## Upstream inputs

| Role | Locator | SHA-256 |
| --- | --- | --- |
| Failing attempts / QA report / delivery | | |
| Specs / stories / policy | | |
| Candidate identities across attempts | | |

Preserve chronology. A later pass does not erase earlier failures.

## Problem statement

- What failed, when, on which candidate:
- What was expected (spec locator):
- How many distinct attempts and what changed between them:

## Causal chain

| Depth | Question | Answer | Evidence | Remaining uncertainty |
| --- | --- | --- | --- | --- |
| 1 | Why did the observed failure occur? | | | |
| 2 | Why was that condition present? | | | |
| … | stop when the next why is speculation | | | |

Do not force five whys. Do not skip a missing evidence step with a narrative.

## Distinctions

- Product defect vs spec defect vs test-oracle defect vs environment vs framework-control gap:
- What the passing unit tests actually proved:
- What they did not prove: [e.g. race between cancellation and dispatch]

## Recommendations

| ID | Change | Owner skill | Required new artifact | Risk if ignored |
| --- | --- | --- | --- | --- |
| RCA-R1 | | story-create / specify / architect / skill-builder | | |

## Downstream handoff

**To story-create:** selected RCA-R IDs with evidence files. Story provenance records `source_rca` and whether the story addresses a why vs a symptom.

**To policy:** only a requested new policy revision; experts still cannot lower floors to dismiss the failure.

**Return path:** implementing a symptom fix without the cited why remaining visible is a review finding, not closure of this RCA.
