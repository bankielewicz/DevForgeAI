# Requirement and BAT traceability

Target `338c70995e72637e0ce84991be110d6a371ab6965faf4009d570156ea0e13cf2`. PASS below applies only to the named observation. A parent requirement passes only if all required subcases do. NOT_RUN is incomplete, not a pass.

| Requirement | Status | Required behavior | BAT mapping |
|---|---|---|---|
| BA-001 | NOT_RUN | Preserve authoring-only and manual handoff boundaries. | BAT-01, BAT-12 |
| BA-002 | NOT_RUN | Discover project evidence within scope and limits without executing project code. | BAT-02, BAT-03 |
| BA-003 | NOT_RUN | Propose evidence-grounded roles and identify unresolved requirements. | BAT-04, BAT-05 |
| BA-004 | FAIL | Preserve source/operational project identity separation. | BAT-06, BAT-07 |
| BA-005 | FAIL | Implement exact shared record schemas, digests, and references. | BAT-08, BAT-09 |
| BA-006 | FAIL | Author selected sets sequentially with dependencies and per-member results. | BAT-10, BAT-11 |
| BA-007 | NOT_RUN | Preserve core and record complete variant lineage. | BAT-05, BAT-13 |
| BA-008 | NOT_RUN | Ground expertise and preserve project development conventions. | BAT-04, BAT-14 |
| BA-009 | FAIL | Produce portable descriptors and binding helper. | BAT-06, BAT-07, BAT-15 |
| BA-010 | NOT_RUN | Propose explicit updates without automatic rebasing/repair. | BAT-13, BAT-16 |
| BA-011 | FAIL | Preserve legacy history, existing schemas, and custody conflict behavior. | BAT-09, BAT-11, BAT-17 |
| BA-012 | FAIL | Keep all authoring terminal-local with honest capability failures. | BAT-03, BAT-15 |
| BA-013 | NOT_RUN | Deliver discriminating routing and progressive resources. | BAT-12, BAT-14 |
| BA-014 | FAIL | Report exact authoring state without testing or enforcement claims. | BAT-01, BAT-10, BAT-17 |

| Subcase | Status | Independent oracle / required behavior | Evidence and limitation |
|---|---|---|---|
| BAT-01.01 | PASS | ordinary helper create/edit and exact manual request | v2-author-create-publish, v2-author-edit-publish; followup-results.json |
| BAT-01.02 | NOT_RUN | cold ordinary create and focused edit with no quality process | cold-create-01 host failure; cold-create-02 timeout before delivery; edit dependent on complete create |
| BAT-02.01 | PASS | junction/link refusal by runtime helper | windows-symlink, linux-symlink |
| BAT-02.02 | NOT_RUN | monorepo facts, unknown manifest, exclusions, no project execution and citations in completed proposal | cold-propose-typescript timed out; raw inputs preserved |
| BAT-02.03 | NOT_RUN | default discovery aggregate budgets and secret exclusions in autonomous discovery | No completed bounded discovery result |
| BAT-03.01 | PASS | Windows independent count and byte capture ceiling and exact boundary values | binding-file-limit, binding-byte-limit, windows-exact-files, windows-over-files, windows-exact-bytes, windows-over-bytes |
| BAT-03.02 | PASS | Linux byte ceilings | linux-exact-bytes, linux-over-bytes |
| BAT-03.03 | NOT_RUN | Linux count ceilings | linux-exact-files and linux-over-files timed out at 120 seconds on /mnt/c; no output |
| BAT-03.04 | PASS | missing Python isolated child and required unavailable Rust capability preflight | missing-python-child, selection-missing-capability |
| BAT-03.05 | NOT_RUN | independent prose retained and dependent authoring blocked after unavailable capability; shared-original discovery accounting | No cold capability-failure proposal or explicit shared-original boundary fixture |
| BAT-04.01 | NOT_RUN | HTTP retained and storage justified with actual supporting sources | Cold TypeScript/domain fixture included existing HTTP skill; proposal not completed |
| BAT-05.01 | PASS | three-parent full inventory, missing row, unauthorized removal linkage; LF/CRLF and older Markdown resource | lineage-fence-lf, lineage-fence-crlf, lineage-table-other-resource and associated negatives |
| BAT-05.02 | NOT_RUN | semantic equivalence and real current authorization adjudication in authored variant | Helpers check shape/linkage; no completed cold variant/removal case |
| BAT-06.01 | PASS | portable template and source identity review, synthetic relocation | source-text-inventory.json; windows-relocated, linux-relocated; generated fixture copies generic helper |
| BAT-06.02 | NOT_RUN | cold adaptive authoring and relocated package completion | No completed native adaptive authoring; scripted C publication is separate evidence |
| BAT-07.01 | PASS | correct/missing/root/inactive/changed/duplicate/role/unbound/unknown-version/descriptor/core-variant/two-variant results | binding-* ordinary matrix; initial-suite-results.json |
| BAT-07.02 | FAIL | excluded private-key filenames rejected | F-03 |
| BAT-07.03 | PASS | no UUID output, no helper writes, unsafe junctions and POSIX I/O failure | binding-* effects; windows-symlink, linux-symlink, linux-io-error |
| BAT-07.04 | NOT_RUN | actual generated-skill no-product-write/no-downstream behavior on rejection and resume | Independent controller and read-only helper do not prove agent enforcement |
| BAT-08.01 | PASS | new evidence/proposal/selection/descriptor/set shapes; duplicate keys/nonfinite/extra fields/invalid IDs/stale refs/locator bounds | record-*, proposal-*, selection-*, descriptor-valid; ordinary positives and negatives |
| BAT-08.02 | FAIL | strict linked legacy records and target bindings | F-01, F-02 |
| BAT-08.03 | NOT_RUN | all new record families complete positive/negative semantic cross-reference grid | No exhaustive per-field matrix for project-binding/adaptive-observation/binding-observation inspect dispatch, or every misleading citation |
| BAT-09.01 | PASS | legacy schema bytes unchanged; valid arbitrary legacy requirement objects and manual requests | legacy-byte-comparison.json; v2-author-*; author-request-readback |
| BAT-09.02 | FAIL | closed legacy top-level interpretation | F-02; F-01 linked reader |
| BAT-10.01 | PASS | A occupied preflight, B blocked, real C publication; PARTIAL and eligible subset omissions | v2-set-A-preflight-fails, v2-set-C-publish, v2-set-partial-result-valid, v2-set-subset-valid and omission negatives |
| BAT-10.02 | FAIL | exact linked per-member custody | F-01 |
| BAT-10.03 | NOT_RUN | autonomous continuation, all retained/full-set/handoff omission permutations and interrupted C writes | Auditor scripted controller; no new cold set trial or complete fault-injection/full-set grid |
| BAT-11.01 | PASS | cycles, missing/unselected dependency, occupied destination, user-edited obsolete file, divergent B/C/N, shared input stale ref | proposal-cycle, selection-*, v2-bcn-*, record-stale-reference |
| BAT-11.02 | FAIL | conflicting known adoption pointer identity | F-04 |
| BAT-11.03 | PASS | concurrent drift no overwrite | v2-author-drift-publish retains changed user.txt with applied_paths empty; status ambiguity D-01 |
| BAT-11.04 | NOT_RUN | destination ancestor overlaps, unowned collision, per-path interruption and all handoff-cycle variants | Source branches reviewed; no complete fresh executed grid |
| BAT-12.01 | PASS | description semantic classification and progressive routing | source-review.md routing table; description-only manual analysis |
| BAT-12.02 | NOT_RUN | completed native mode invocation/implicit selection and handoff stopping | All applicable cold attempts timed out; implicit activation not executed |
| BAT-13.01 | PASS | unchanged/equivalent-byte-changed review, false NO_CHANGE rejection and missing parent reference | ext2-update-* |
| BAT-13.02 | NOT_RUN | materially removed core requirement and native revision-impact proposal | No completed cold update review; no executed material-removal proposal |
| BAT-14.01 | PASS | all four convention fixtures specified and cold attempts retained | proposal_trials.py; cold-propose-*-plan.json |
| BAT-14.02 | NOT_RUN | completed four-project adaptation and contradictory same-scope convention | All four proposals timed out; ambiguous-convention cold variant not run |
| BAT-15.01 | PASS | Windows/POSIX hostile paths and offline standard-library helper; isolated missing executable | binding-hostile-path, windows-valid, linux-valid, missing-python-child; source call review |
| BAT-15.02 | FAIL | private-key exclusion in portable helper | F-03 |
| BAT-15.03 | NOT_RUN | cold missing-interpreter reporting and OS network isolation qualification | Only child launch failure and source-local network-free execution observed |
| BAT-16.01 | PASS | stale input digest rejection | record-stale-reference; ext2-update-missing-history |
| BAT-16.02 | NOT_RUN | native resume with changed original evidence and fresh linked proposal; runtime match invalidation | No native resume trial; instructions reviewed, no cached-authority claim credited |
| BAT-17.01 | PASS | ordinary import/spec-build, observed edit, authored baseline, explicit new adoption, legacy generated/adopted baseline, corrupt baseline | v2-author-*; ext2-legacy-generated, ext2-legacy-adopted, ext2-legacy-corrupt-generated |
| BAT-17.02 | FAIL | wrong known legacy pointer | F-04 |
| BAT-17.03 | NOT_RUN | complete Claude conversion dispositions and schema-2 generated-after-adoption lineage/retry histories | Import helper operation is not a complete semantic conversion or all legacy ancestry modes |
