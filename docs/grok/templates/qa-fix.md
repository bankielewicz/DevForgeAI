# Template: QA fix packet

**Producer:** current `qa` on FAIL  
**Consumers:** `dev` (repair owner); later `qa` `retest`  
**Operational template:** `src/agents/skills/qa/assets/qa-fix-template.md`  
**Does not:** close the finding, edit product source, or auto-invoke `dev`.

## Envelope

| Field | Value |
| --- | --- |
| Packet identity | |
| FAIL report locator / hash | |
| Producer | qa |
| Downstream consumer | dev |
| Failure behavior | Missing reproduction or oracle blocks that defect's repair claim |
| Non-claims | Root cause may be unknown; do not invent a design |

## Upstream inputs

| Role | Locator | SHA-256 |
| --- | --- | --- |
| QA report | | |
| Candidate that failed | | |
| Specs / stories | | |
| Policy floors | | |

## Selected defects

Repeat per stable defect ID.

### Defect [ID]

- Violated criterion / policy and locator:
- Class: INTEGRITY_FAILURE / METRIC_FAILURE / CRITICAL_PRODUCT_DEFECT / MANDATORY_PRODUCT_DEFECT
- Terminal vs nonterminal:
- Exact artifact ownership and paths:
- Reproduction procedure (commands, cwd) or confirmed static finding:
- Expected vs actual:
- Evidence (case/attempt IDs, hashes):
- Root cause: confirmed / not established
- Required correction (behavior to restore, not a speculative patch):
- Compatibility constraints:
- Regression oracles:
- QA retest conditions (new candidate, exact observations, invalidated metrics):
- Remaining NOT_RUN cases with trigger IDs:

## Return contract from dev

`dev` must supply: new candidate identity and changed-file manifest; per-defect correction evidence; red/green/refactor and regression receipts; current coverage and unit counts with denominators; remaining gaps. `dev` cannot self-issue QA closure.

## End-user remediation invocation

- Required project / environment:
- `dev` availability observation:
- Paste into the conversation input: [complete resolved `dev` prompt]

## Downstream handoff

**To dev:** this packet is the selected repair scope.  
**To qa retest:** only after a **new** candidate is delivered. Closure requires independent retest, not a developer claim.
