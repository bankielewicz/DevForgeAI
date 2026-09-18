# Template: Development slice plan

**Producer:** current `dev`  
**Consumers:** per-slice TDD execution; traceability; delivery  
**Operational template:** `src/agents/skills/dev/assets/slice-plan.md`  
**Does not:** count as execution evidence. The plan is not a passing test.

## Envelope

| Field | Value |
| --- | --- |
| Plan identity | |
| Producer | dev |
| Downstream consumer | red/green/refactor/QA cycle, then delivery |
| Failure behavior | Slice with unresolved prerequisite stays blocked; independent slices continue |
| Non-claims | File-count progress is not completion |

Repeat the following section per slice in **dependency order**. Shared protocol ownership precedes dependent clients.

## Slice: [identity and observable outcome]

- Requirements: [source-qualified IDs]
- Dependencies / build order: [prior slices, required inputs]
- Consumed / provided contracts: [interfaces and single owner]
- Existing components / proposed additions: [paths]
- Allowed effects: [source/test/config/evidence boundaries]
- Verification: [focused red case; integration/negative/recovery/QA as applicable]
- Prerequisites / gaps: [tool, authority, input, decision]
- Current state: planned / in progress / verified / blocked / stale

### Reuse assessment

| Search scope and limits | Candidate | Decision | Evidence |
| --- | --- | --- | --- |
| | | reuse / extend / compose / new | |

Absence of search matches is not proof of absence.

### Execution lineage

| Step | Intended | Observed attempt | Receipt |
| --- | --- | --- | --- |
| Harness / characterization | | label passing characterization honestly | |
| Red | fail because behavior is absent/wrong | setup errors are not valid red | |
| Green | same assertions, real behavior | no hardcoded expected output | |
| Refactor | preserve contracts | rerun affected tests | |
| Integration / developer QA | | | |

Next safe action: [concrete].

## Downstream handoff

Verified slices feed traceability and delivery. A blocked slice names the upstream document that must change (`product-requirements`, `system-architecture`, `story`, or `qa-fix`) rather than weakening the test.
