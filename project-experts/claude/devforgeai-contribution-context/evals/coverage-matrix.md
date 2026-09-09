# Coverage matrix for the authored cases

Every provider, role, variant, mode and arm is counted separately here, because the case
catalogue's eight rows are not eight executions. Nothing in this file has been run: SESSION-004
allocates exactly 0 model calls, concurrency 0 and retries 0.

## Two provider facts, kept apart

| Fact | Meaning here |
| --- | --- |
| Scenario provider | What the synthetic assignment inside a fixture says about the session it describes. A fixture stating "scenario provider Codex" is a fact about the record, not about the client reading it. |
| Runtime provider under test | The client actually executing the case. For this candidate that is Claude. |

Executing these cases on the Claude runtime observes nothing about Codex support. Codex-runtime
execution is NOT_APPLICABLE to this candidate's declared scope; overall Codex support remains
NOT_EVALUATED and belongs to the separately assigned Codex package.

The distinction is also the subject of two cases: CCX-02 fails if a worker infers its role from
the runtime it happens to be running on.

## Case rows and arms

Baseline for every row is `without_skill`: the same core workflow, the same raw records, the
same tool access, without this package. The starting candidate state was ABSENT, so no
`old_skill` baseline exists for a first iteration.

| Eval id | Case | Variant | Declared mode | Mode fixed by | Scenario role | Scenario provider | Runtime provider | Baseline arm | Candidate arm |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | CCX-01 | single | checkpoint/transfer | catalogue | architect/integration operator | codex | claude | NOT_RUN | NOT_RUN |
| 2 | CCX-02 | A | orient/resume | catalogue | contributor worker | codex | claude | NOT_RUN | NOT_RUN |
| 3 | CCX-02 | B | orient/resume | catalogue | contributor worker | claude | claude | NOT_RUN | NOT_RUN |
| 4 | CCX-03 | single | orient/resume | XSPEC-004 | contributor worker | unspecified in fixture | claude | NOT_RUN | NOT_RUN |
| 5 | CCX-04 | A missing owner | checkpoint/transfer | catalogue | unassigned session with independent reporting authority | unspecified in fixture | claude | NOT_RUN | NOT_RUN |
| 6 | CCX-04 | B conflicting owner | checkpoint/transfer | catalogue | unassigned session with independent reporting authority | unspecified in fixture | claude | NOT_RUN | NOT_RUN |
| 7 | CCX-05 | A delegation present | orient/resume | XSPEC-004 | contributor worker | unspecified in fixture | claude | NOT_RUN | NOT_RUN |
| 8 | CCX-05 | B control | orient/resume | XSPEC-004 | contributor worker | unspecified in fixture | claude | NOT_RUN | NOT_RUN |
| 9 | CCX-06 | single | orient/resume | XSPEC-004 | contributor worker | unspecified in fixture | claude | NOT_RUN | NOT_RUN |
| 10 | CCX-07 | single | checkpoint/transfer | XSPEC-004 | architect/integration operator | unspecified in fixture | claude | NOT_RUN | NOT_RUN |
| 11 | CCX-08 | A routine resume | orient/resume | XSPEC-004 | contributor worker | unspecified in fixture | claude | NOT_RUN | NOT_RUN |
| 12 | CCX-08 | B explicit transfer | checkpoint/transfer | XSPEC-004 | contributor worker | unspecified in fixture | claude | NOT_RUN | NOT_RUN |
| 13 | CCX-04 | C authorized bootstrap | checkpoint/transfer | catalogue | session holding a scoped target authorization and a separate reporting authority | unspecified in fixture | claude | NOT_RUN | NOT_RUN |

**Arm count:** 13 rows x 2 arms = 26 planned arms, all NOT_RUN. This is an authored plan value,
not an execution allocation. A future allocation owner sets the actual counts, timeouts,
concurrency, retries and deadline.

Where a fixture leaves the scenario provider unspecified, the case does not depend on it, and a
future fixture owner may pin one. Recording it as unspecified is deliberate: inventing a provider
would create a distinction the case does not actually test.

## Requirement coverage

| Requirement | Cases exercising it |
| --- | --- |
| CCR-001 establish the recovery task | all 13 |
| CCR-002 resolve the selected context | 1, 2, 3, 4, 9, 10, 11, 12 |
| CCR-003 preserve authority | 1, 5, 6, 7, 8, 13 |
| CCR-004 reconstruct state from evidence | 1, 10, 11, 12 |
| CCR-005 select bounded context | 2, 3, 9 |
| CCR-006 preserve uncertainty and ownership | 5, 6, 9, 13 |
| CCR-007 return one continuation | all 13 |
| CCR-008 deliver the required mode output | 1, 5, 6, 10, 12, 13 (checkpoint delivery); 2, 3, 4, 7, 8, 9, 11 (orientation without unnecessary writes) |

## Mode coverage

| Declared mode | Eval ids | Count |
| --- | --- | --- |
| orient/resume | 2, 3, 4, 7, 8, 9, 11 | 7 |
| checkpoint/transfer | 1, 5, 6, 10, 12, 13 | 6 |

Eval 11 is the orient-only arm of the CCX-08 pair. It is counted under orientation and appears in
no checkpoint-delivery coverage claim; its orientation assertions are unchanged.

Every row declares its mode before execution. CCX-01, CCX-02 and CCX-04 take theirs from the
case catalogue; the rest were declared in XSPEC-004 before any candidate file was written. A mode
may not be reassigned after observing a result - in particular, a failed checkpoint case may not
be reclassified as orientation because its artifact turned out to be missing.

## Paired contrasts

| Pair | Discriminating difference | Why the pair is the measurement |
| --- | --- | --- |
| CCX-02 A/B | Which provider source, fence and finding belong to this worker | A candidate that returns the same answer for both has not selected anything |
| CCX-04 A/B/C | No ownership record, versus two conflicting active claims, versus a current scoped target authorization with a recorded collision observation and no session record | A and B stop the dependent target work for different reasons; C's target continuation is authorized and outstanding. A candidate returning the same target disposition for all three has not read the authorizations, and a case set with only A and B would reward stopping unconditionally |
| CCX-05 A/B | Recorded delegation present versus absent, identical request wording | Proceeding in both, or refusing in both, demonstrates nothing |
| CCX-08 A/B | Same records, different declared mode | The failure modes are opposite: churn in resume, omission in transfer |

## Tier coverage for this stage

| Tier | State | Reason |
| --- | --- | --- |
| A discovery and activation | NOT_RUN | No installed package, no fresh target terminal, no allocation. Trigger queries authored and frozen in triggers/triggers.json; their selection is authored, not observed. |
| B recovery behavior | NOT_RUN | No model calls allocated. Cases and expectations authored only. |
| C installed resources | NOT_RUN | No installation performed; no installer supports this source mapping yet. |

## What these cases are not

They are author-provided cases, written by the same session that authored the candidate. They
are not held-out independent evaluation, and passing them would not establish independent
acceptance. An improvement claim requires the paired baseline difference, and no arm has run.
