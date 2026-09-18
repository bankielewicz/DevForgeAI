# Template: Development traceability

**Producer:** current `dev`  
**Consumers:** `dev` delivery accounting; `qa` intake (supporting, not the QA oracle)  
**Operational template:** `src/agents/skills/dev/assets/traceability.md`  
**Does not:** close independent QA findings or substitute for missing tests.

## Envelope

| Field | Value |
| --- | --- |
| Record identity | |
| Candidate identity | [manifest / hashes; may lag if source changed — say so] |
| Producer | dev |
| Downstream consumer | development-delivery; qa inventory |
| Failure behavior | Unmapped selected requirement prevents COMPLETE |
| Non-claims | Status `verified` is developer evidence, not QA PASS |

## Upstream inputs

Selected specs/stories and their hashes: [table or reference to context record].

## Requirement map

| Source-qualified ID | Statement locator | Implementation paths / symbols | Tests / evidence | Status | Unresolved reason |
| --- | --- | --- | --- | --- | --- |
| | | | | verified / pending / blocked / excluded | |

Count each selected requirement once. Exclusions need a source-based reason. Referenced-but-unselected specs stay out of the denominator.

## Slice coverage

| Slice | Requirement IDs | Red receipt | Green receipt | Remaining |
| --- | --- | --- | --- | --- |
| | | | | |

## Downstream handoff

Delivery uses these counts. QA rebuilds its own criterion inventory from the **specifications**, then may compare this map for gaps. A row marked verified with no bound receipt is incomplete, not passing.
