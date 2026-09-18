# DFF-WORKER-FEAS-01 v1.0.0 traceability

Implementation mapping below is complete. Current check status and candidate identity are recorded in delivery.md and final-test-inventory.json; prior passing results do not qualify changed bytes. Each row names an implemented owner and developer verification. Native qualification and protected acceptance remain separate.

| Local requirement | Source passage / obligation | Implemented owner and developer verification |
| --- | --- | --- |
| R01 | Sections 1,3 isolated foreground Rust package; exact dependencies, no authority | Manifest/lockfile, Cargo build, index hash preservation |
| R02 | Section 4 closed bounded request, identities, native paths, fixture inventory | request.rs; WF-09/17 |
| R03 | Sections 4,6 reviewed native profile and fixed adapters | request.rs/protocol.rs; synthetic review validation, no native launch |
| R04 | Section 4 fixed limits, control input and Ctrl+C | runner/process/CLI; WF-13/15/16/20 |
| R05 | Section 4 typed durable events, terminal values and exit precedence | journal/runner; WF-01..20 |
| R06 | Sections 4,7 read-only inspection, corruption, pagination, missing references | journal.rs; WF-09..12 |
| R07 | Section 5 handshake, account/model/rate preflight, exact outbound wire | protocol/peer; WF-01..03 |
| R08 | Section 5 thread effective policy, one turn, bounded reconciliation | protocol/runner; WF-02/04/05 |
| R09 | Section 5 typed events, final-message selection and deduplication | protocol/oracle; WF-04/05/07/08/18 |
| R10 | Section 5 approval/unknown request refusals | protocol/peer; WF-06 |
| R11 | Sections 5,6 cancellation ordering, one interrupt, verified teardown | runner/process; WF-13..16/20 |
| R12 | Section 6 atomic job membership, inheritance, crash containment | process_windows.rs; WF-13/14 |
| R13 | Sections 6,7 latest usage, sanitized observations, no secret capture | protocol/journal/process; WF-03/07/08/16 |
| R14 | Section 7 exclusive evidence, durable intents, no replay | journal/runner; WF-09..12 |
| R15 | Sections 7,8 unchanged exact fixture, independent strict oracle | request/oracle/runner; WF-18/19 |
| R16 | Section 8 external peer, required test file/name mapping and all subfixtures | WF-01..20; developer verification separate from independent QA |
| R17 | Section 9 TDD, Windows QA, all src line denominator >=95%, cases >=95% with every mandatory pass | execution records and full llvm-cov JSON |
| R18 | Handoff fresh absolute evidence, frozen identities, independent QA retest handoff | context binding, candidate-readback.json, output-readback.json, final-source-test-manifest.json, independent-qa-handoff.md |

WN-01/WN-02 NOT_RUN by explicit selection boundary. Their separate native inventory has 0/2 demonstrated passes. Protected acceptance NOT_EVALUATED. Parent framework, production engine, OrderDesk, index fixes, deployment, installation and operational skills are unselected deliverables.

## Subfixture accounting

| Case | Executed stimulus inventory in required test |
| --- | --- |
| WF-01 | Exact outbound handshake/policy/one-turn and independent final oracle |
| WF-02 | on-request approval and workspaceWrite sandbox |
| WF-03 | no account, API account, Plus account, absent model, absent effort |
| WF-04 | wrong thread, wrong turn, malformed JSON, conflicting response, unknown response ID |
| WF-05 | Started/completed before response, exact duplicate response; supplemental duplicate-completion tests |
| WF-06 | command approval, file approval, unknown server request |
| WF-07 | failed turn with usageLimitExceeded category |
| WF-08 | repeated cumulative usage and separate absent usage |
| WF-09 | existing run with exact and changed request, preserved journal |
| WF-10 | abrupt process exit after spawn intent and turn intent |
| WF-11 | discarded terminal stdout, repeated inspect, pagination boundaries |
| WF-12 | partial tail, corrupt complete record, sequence gap, missing input |
| WF-13 | real hidden-console Ctrl+C and stdin cancel, independently held peer/descendant handles |
| WF-14 | forced harness kill and independent peer/descendant handle waits |
| WF-15 | ignored interrupt, cancellation at server_started/thread_bound/turn_bound; supplemental cooperative EOF and lost transport |
| WF-16 | unanswered RPC, >1MiB stdout line, >8MiB stderr, production 120-second watchdog |
| WF-17 | IDs/hash/traversal, overlapping roots, actual junction, outside sentinel |
| WF-18 | wrong, missing and extra-key results |
| WF-19 | actual fixture change and injected durable evidence failure |
| WF-20 | completion first, cancellation first, cleanup unknown override |

Source test functions wf_01..wf_20 remain in the four contract-prescribed files. Supplemental negative/profile/admission/oracle/process tests do not inflate this 20-case denominator. final-test-inventory.json enumerates actual test names and retained fixture roots for the final campaigns. Developer checks do not establish independent QA.
