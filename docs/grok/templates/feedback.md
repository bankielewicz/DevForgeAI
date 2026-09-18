# Template: Feedback

**Producer:** planned `feedback` (legacy `/feedback`)  
**Consumers:** `discover` / `specify`, `story-create`, `skill-builder` propose (framework gaps only)  
**Does not:** become a requirement until selected; change quality policy; auto-create incidents.

## Envelope

| Field | Value |
| --- | --- |
| Feedback ID | FB-[utc] |
| Trigger | post-dev / post-qa / post-release / retrospective / manual |
| Producer | feedback |
| Downstream consumer | [discover / story-create / skill-builder / none] |
| Failure behavior | Incomplete item (no observable behavior) is not handed downstream |
| Non-claims | Not an RCA; not a story; not a skill defect unless evidenced |

## Upstream inputs

| Role | Locator | SHA-256 |
| --- | --- | --- |
| Release / QA / delivery record | | |
| User statements | | |
| Related prior feedback | | |

## Item

- Observation: [what happened, with evidence]
- Expected (if known): [spec ID or “unspecified”]
- Impact: [user / process / framework]
- Classification: product defect / spec gap / process friction / framework gap / praise
- Recommendation: [proposed work, not a requirement]
- Observable acceptance if adopted: [or “insufficient — needs specify”]

## Disposition

| Path | Selected? | Target template |
| --- | --- | --- |
| New discovery / spec change | | business-analysis / product-requirements |
| New story | | story |
| Policy realignment request | | project-policy (new revision) |
| Framework adaptation | | adaptation-proposal |
| No action | | reason |

## Downstream handoff

Hand off only **selected** recommendations with locators. `story-create` treats this as a recommendation source, not as already-approved scope.

**Return path:** a story authored from this item must keep provenance (`from_recommendations`). Rejecting the recommendation does not delete this record.
