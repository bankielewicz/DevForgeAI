# Selected remediation traceability

Authority: user-selected handoff ../20260915T1800141514833Z/handoff.md, DFF-WORKER-FEAS-01 v1.0.0. All paths below are relative to this evidence root unless stated. `G` means ../20260915T1834258428322Z-green. This is developer evidence; findings remain OPEN.

| Selected obligation | Implementation / verification | Result and boundary |
| --- | --- | --- |
| Handoff intake and candidate drift | User-pinned manifest hash; 35 bound entries; original 31-file candidate; 335 contract/schema entries; input-readback.json, contract-readback-final.json | PASS, no intake drift or restored source |
| F-01; spec §§4–6: blocked write deadlines/cancel and tree stop | src/process_windows.rs::send_until, writer thread and wait_stopped; src/protocol.rs RPC/receive/initialized/interrupt. Red IQ-02-* here; Green G/independent-attempts/IQ-02-*; tests/remediation.rs first three tests | Repair implemented, behavioral checks PASS; original IQ-02 deadline boolean remains FAIL solely for expected 4 versus actual contract exit 6. Independent retest required |
| F-02; spec §§5,7: typed error retention | src/protocol.rs::error_category and numeric RPC code; tests/remediation.rs::malformed_error_payloads_never_reach_journal_or_stdout; original IQ-05 Red here and Green under G | PASS developer evidence: unknown data omitted/rejected, approved categories/details retained, marker absent. No finding closure |
| M-01; spec §§8–9: WF-01..20 with all required subfixtures | Unchanged original mandatory tests, G/01-tests and G/04-coverage | 20/20 PASS on each run; each case counted once |
| Original supplemental/unit obligations | test-inventory.json, metrics.json, same normal/instrumented receipts | 26/26 original supplemental and declared 6/6 unit cases PASS |
| Added meaningful regression | Four groups in tests/remediation.rs, peer branches added without replacing originals | 4/4 PASS normal and instrumented; not added to the original 26-group denominator |
| Original IQ-01..06 requirement groups | G/independent-attempts, copied-iq-results.json, ownership-review.md | IQ-01/03/04/05/06 PASS as developer-run evidence; IQ-02 raw FAIL, with bounded timeout/cancel observed. Original group metric 25/26 = 96.15384615384616%, numeric floor PASS; all-checks result remains qualified |
| Executed-line coverage >=95%, all src | G/coverage.json, metrics.json and raw-profile-identities.json | 1420/1487 = 95.49428379287156%, PASS; no runtime exclusions; branch NOT_RUN |
| Formatting/static analysis | G/02-format, G/03-clippy | PASS, -D warnings; locked/offline all-target builds executed by tests |
| Preserve original evidence, fixture/oracle, source fences | input-readback.json, contract-readback-final.json, changed-files.json | Original evidence entries and contract/schema bytes unchanged; only two production files, one extended peer and one new test file changed/added. Index manifest/lock and selected operational QA instructions unchanged |
| Return corrected identities and exact output paths | candidate-manifest.json (32 entries), candidate-snapshot/, changed-files.json, build-identities.json (54), raw-profile-identities.json (147), delivery-manifest.json | Literal-path readback required before final delivery; readback receipt is output-readback.json |
| Separate independent closure and authority | handoff.md | F-01/F-02 OPEN; native WN-01/WN-02 NOT_RUN, framework acceptance NOT_EVALUATED |

All selected implementation/evidence obligations are represented above. Overall development status PARTIAL solely because the unchanged IQ-02 deadline assertion remains failed pending independent expectation review. The numeric floors and product regression suite are passing. Native profile review, launcher identity changes, native trials, installation, deployment, protected enforcement and other parent-document deliverables were not selected.
