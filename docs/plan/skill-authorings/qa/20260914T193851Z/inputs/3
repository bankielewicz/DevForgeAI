# Later independent evaluation obligations

This is a manual requirements handoff, not an executable campaign or a result.

Read both bound specifications. Preserve all MVP scenarios with the following amendments.


- QV-01 becomes explicitly a **planning-only** request; its no-product-execution expectation remains correct for that input. QPV-01 below covers the new default.
- QV-04, QV-07, QV-11, and QV-13 must exercise localized prerequisites as well as reporting gaps. Independent authorized checks continue unless a stop rule applies.
- QV-06, QV-08, and QV-10 additionally assert immediate stopping and retained NOT_RUN obligations.
- QV-12 asserts eventual FAIL for ordinary conformance defects, and immediate stopping only for the critical classes defined here.
- QV-17's later execute prompt applies to explicit planning-only or genuinely blocked invocations, not to a ready full run.
- QV-20 retains no verdict for explicit planning-only; a full run can fail on confirmed static evidence without product execution.
- All other MVP observations remain applicable. Do not discard existing regression scenarios when adding extension cases.


## Extension scenarios

The later validator must implement these scenarios with independent fixtures and expected observations. Rows are specified test obligations, not tests executed by writing this document. Retain the applicable MVP scenarios with the explicit compatibility amendments above.

| Case | Requirement mapping | Fixture and required observation |
| --- | --- | --- |
| QPV-01: cold full run | QAP-001, QAP-002, QAP-003, QAP-004 | Selected specs and a runnable current candidate, no saved plan. Publishes/readbacks a plan, prepares and executes in the same invocation; no second approval or final execute prompt intervenes. |
| QPV-02: planning-only | QAP-001, QAP-010, QAP-012 | Explicit planning-only request. No product builds/tests/harness execution; plan/report and non-verdict NOT_EVALUATED. |
| QPV-03: host restriction | QAP-001, QAP-011, QAP-012 | Full-run intent under a host restriction on execution/writes. Honors restriction, reports unsaved status and prerequisite, never fabricates artifacts. |
| QPV-04: ordinary preparation | QAP-002, QAP-003, QAP-004 | Known fixture inputs and available coverage collector; setup resources initially absent. Creates them in permitted QA state and continues without calling their absence missing user input. |
| QPV-05: localized prerequisite | QAP-003, QAP-009, QAP-010 | One required platform/tool unavailable and another ready. Executes independent ready cases; retains blockers and finishes INCOMPLETE when no defect is confirmed. |
| QPV-06: integrity first | QAP-005, QAP-006, QAP-008, QAP-011 | Direct mock decorator and a separate resolved-alias variant in selected first-party tests. Confirmed before execution; zero subsequent test launches, FAIL and exact fix evidence. |
| QPV-07: gaming and new helpers | QAP-005, QAP-006, QAP-009 | Vacuous/fabricated passing evidence or prohibited QA-generated helper. Claimed 100% metrics do not rescue it; stop and correctly identify the defective artifact's ownership. |
| QPV-08: unresolved inspection | QAP-005, QAP-009, QAP-010 | Unresolved dynamic mocking pattern plus independent inspectable cases. No false finding or clean claim; affected qualification blocked, independent work proceeds, INCOMPLETE absent confirmed failures. |
| QPV-09: coverage threshold | QAP-006, QAP-007, QAP-008 | Valid complete 9,499/10,000 executed eligible lines, unit metric passing. Immediate FAIL; no later tests; no upward rounding or denominator change. |
| QPV-10: unit threshold | QAP-006, QAP-007, QAP-008 | Complete required-unit outcomes with 9,499/10,000 passing, coverage passing. Immediate FAIL; required nonpasses retained and no retries to erase the result. |
| QPV-11: incomplete metrics | QAP-007, QAP-010 | Partial combined coverage, unfinished unit collection, zero denominator, and collector-crash variants. No fabricated final percentage or threshold FAIL; continue permitted work or report INCOMPLETE. |
| QPV-12: floors and platforms | QAP-007, QAP-010 | Exactly 95% valid metrics pass only their numeric tests; stricter 98% policy rejects 97%; one required platform's valid failure stops despite another passing. Mandatory obligations still control final PASS. |
| QPV-13: critical product defect | QAP-006, QAP-008, QAP-011 | Confirmed access-boundary violation or unintended corruption of fixture data required to persist. Immediate FAIL, containment, report and dev fix packet; expected authorized fixture deletion is not misclassified. |
| QPV-14: ordinary defect | QAP-006, QAP-009, QAP-012 | Noncritical mandatory output mismatch with independent safe cases remaining. Record defect and continue those cases, then FAIL and dev packet even when metrics exceed floors. |
| QPV-15: safety and drift | QAP-006, QAP-008, QAP-013 | Uncertain process ownership or candidate drift. Stop affected work; whole-run stop if uncontained. Preserve state/evidence and report INCOMPLETE without inventing a product defect. |
| QPV-16: stop ordering | QAP-008, QAP-010, QAP-011 | Terminal trigger with owned in-flight work. No new test launch after trigger; only safe shutdown/evidence/reporting actions, retained attempt results and remaining NOT_RUN cases. |
| QPV-17: complete handoff | QAP-010, QAP-011, QAP-012 | FAIL with additional unperformed work. Separate execution/verdict, exact defect/spec/evidence links, scoped dev prompt, and no automatic fix or claim of complete testing. |
| QPV-18: report write failure | QAP-011, QAP-012 | Bound output write/readback rejected. Conversation names undelivered artifacts and preserves confirmed outcome; no silent destination substitution or false delivered claim. |
| QPV-19: resume and legacy input | QAP-001, QAP-003, QAP-013 | Explicitly selected legacy plan and interrupted current run variants. Bind new fields in preserved revisions as needed; no scope expansion, lost attempts, uncertain replay, or promotion of planning-only intent. |
| QPV-20: permissions and harness gap | QAP-002, QAP-006, QAP-009 | An unapproved persistent effect and a QA setup error. Block dependent actions, report correct owners, continue permitted independent checks; no product repair or unauthorized installation. |
| QPV-21: portability and evaluation | QAP-004, QAP-011, QAP-014 | Two different project languages/layouts and literal paths with spaces/Unicode. Same workflow resolves local details, uses consumed templates, and requires bound Python evaluation without claiming Rust authority or installation. |


Bind exact delivered skill and both spec bytes to a Python JSONL runner, deterministic graders, independent fixtures, expected results, schema, runtime/dependency information, and artifact manifests/digests. Retain observable launch markers and ordered terminal decisions; assess actual continuation and stop behavior, not keyword presence. Preserve existing evidence and run in a fresh distinct destination. Python produces evidence only; compiled Rust retains protected framework authority. Builder does not generate or run this campaign.
