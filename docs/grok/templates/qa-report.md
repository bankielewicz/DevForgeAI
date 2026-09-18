# Template: QA report

**Producer:** current `qa` for every completed, stopped, blocked, or planning-only invocation  
**Consumers:** `dev` on FAIL; delivery review on PASS; prerequisite owner on INCOMPLETE  
**Operational template:** `src/agents/skills/qa/assets/qa-report-template.md`  
**Does not:** repair product code, issue framework acceptance, or authorize release.

## Envelope

| Field | Value |
| --- | --- |
| QA run / mode | |
| Execution status | NOT_STARTED / IN_PROGRESS / COMPLETED / STOPPED |
| Verdict | PASS / FAIL / INCOMPLETE; planning-only uses NOT_EVALUATED |
| Producer | qa |
| Downstream consumer | [dev / release review / prerequisite owner / qa resume] |
| Failure behavior | FAIL → qa-fix; INCOMPLETE → named owner; PASS → delivery review only |
| Non-claims | COMPLETED execution is not PASS; PASS is not release authorization |

## Upstream inputs

| Role | Locator | SHA-256 |
| --- | --- | --- |
| Plan | | |
| Candidate | | |
| Specs / stories | | |
| Policy | | |

## Acceptance traceability

| Criterion | Required | Cases | Expected | Actual | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| | | | | | | |

## Integrity

- Mock-decorator result:
- Gaming assessment:
- Supplied vs independently executed evidence:

## Metrics

| Platform | Metric | Numerator | Denominator | Exact % | Floor | Result | Raw evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | line coverage / unit pass rate | | | unrounded | | | |

Unavailable platforms remain unqualified. Partial collection is not a failing percentage.

## Defects and gaps

| ID | Criterion / policy | Class | Demonstrated impact | Owner | Evidence |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

Advisory items stay out of the mandatory list.

## Stop / continuation

- Trigger ID and class:
- Tests still required (NOT_RUN with trigger):
- Independent checks that continued:
- Cleanup of QA-owned state:

## Disposition

- Product QA outcome:
- Fix packet path / hash (FAIL only):
- Framework acceptance: `NOT_EVALUATED` unless a live authority receipt is attached
- Release authorization: [separate supplied decision or not granted]

## End-user handoff

- Next owner:
- Next action:
- Paste-ready conversation prompt: [complete, resolved; no auto-send]
