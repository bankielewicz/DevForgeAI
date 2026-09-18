# Requirements-to-tests matrix (pre-freeze)

Every executable row is `BLOCKED` only on the explicit candidate freeze. Evidence paths and frozen test names will be added after Cargo enumeration. All subfixtures named in a row are conjunctive.

## Source-identity amendment — denominator 10

| ID | Expected observable behavior | Level / independent oracle | Planned evidence |
| --- | --- | --- | --- |
| SI-T01 | The exact reviewed directory junction admits; schema-2 inventory records the normalized mapping, physical file hashes, `j` membership, and one physical binding per file. | Real Windows junction through the candidate's private collector seam plus QA-owned disposable-copy assertion; compare output structure and independent hashes. | Setup proof, mapping metadata, inventory JSON, duplicate-path count. |
| SI-T02 | Same bytes at another target, changed target, escaping target, and missing target each reject. | Real junction targets under owned roots; each negative expected independently from SI-01 absolute/sibling rules. | Per-stimulus outcome and unchanged sentinels. |
| SI-T03 | Directory symlink, wrong tag/reparse type, ordinary-directory substitution, and missing junction each reject. | Real Windows symlink/junction/ordinary/missing fixtures; inspect OS attributes/tag separately from product outcome. | Native metadata plus rejection records. |
| SI-T04 | Unlisted alias, loop, target/ancestor/control-source reparse, and alias outside selector depth reject. | Owned real reparse graph and sentinels; no installed paths. | Per-negative trace and fixture manifest. |
| SI-T05 | Physical byte or complete indexed membership drift invalidates a retained inventory. | Collect once, mutate one owned byte/member at a time, verify stale inventory rejection; restore only QA-owned fixtures between distinct cases. | Before/after hashes/member encodings and rejection. |
| SI-T06 | Schema 1, stale/forged identity digest, omitted/extra mapping, and unknown/duplicate/malformed fields reject. | Byte-level JSON mutations from a valid closed record; use an independent JSON duplicate-key writer and exact expected error class. | Input bytes/hashes and outcomes. |
| SI-T07 | Review binds only physical sources; stale review/inventory and any review path through alias reject. | Review/inventory byte and path mutations; compare file bindings against independently enumerated physical paths. | Review/inventory pairs and rejection. |
| SI-T08 | Drift after initial qualification is rejected after durable spawn intent and argument preparation, before any child process creation. | Inspect private callback ordering and public fixed-check wiring; focused compiled test uses real child path but a callback-induced source drift and independently verifies no server-start/PID/child evidence. | Ordered journal kinds, callback count, null worker exit, process count. |
| SI-T09 | Source limits, credential exclusions, strict non-plugin paths, executable/policy checks, all WF, NI offline, F-01 and F-02 regressions remain valid. | Complete locked/offline suite plus independent focused controls. | Full suite, policy oracle, privacy/process evidence. |
| SI-T10 | Final candidate/specification bytes are unchanged and installed mapping metadata is only the selected mapping; old evidence remains untouched. | Fresh literal-path manifests and nonmutating `Get-Item`/reparse metadata readback only; no installed collection. | Final manifests, mapping metadata, old-evidence existence/hash comparisons. |

The finalized SI-01/SI-03 clarification is mandatory: under a disjoint derived `USERPROFILE`, public `profile-sources` succeeds with an empty applicable `junctions` set when no reparse exists, and an identically shaped relative `openai-bundled/chrome/latest` junction rejects. The compiled absolute record cannot relocate through environment/root derivation.

## Base WF regression — denominator 20

| ID | Required observation |
| --- | --- |
| WF-01 | Exact handshake/method/field order and one turn produce the strict expected result, exit 0. |
| WF-02 | `on-request` approval and `workspaceWrite` sandbox variants both stop before turn, exit 3. |
| WF-03 | No account, API account, Plus account, and absent model/effort all stop without fallback, exit 3. |
| WF-04 | Wrong IDs, malformed JSON, conflicting duplicate, and unknown response ID fail with exit 4 and no redispatch. |
| WF-05 | Early completion/started plus an exact duplicate reconcile to one correlated result and one terminal. |
| WF-06 | Command/file approvals and unknown request are denied/cancelled, never grant or write a rule, and exit 4. |
| WF-07 | Usage-limit failure retains only approved typed category/open work, exit 4, one spawn. |
| WF-08 | Latest cumulative usage is retained once; absent usage stays null. |
| WF-09 | Existing exact/changed run directories reject before spawn and preserve every old byte. |
| WF-10 | Crashes after spawn/turn intent remain unknown/incomplete, with zero redispatch or PID-only kill. |
| WF-11 | Durable terminal survives lost stdout; repeated paginated inspection stays identical and complete. |
| WF-12 | Partial tail, corrupt interior, sequence gap, and missing input classify distinctly with zero mutation. |
| WF-13 | Ctrl+C and stdin cancel stop peer/descendant, empty Job, and return exit 5 within bounds. |
| WF-14 | Forced harness termination signals held peer/grandchild handles within five seconds; no orphan/PID inference. |
| WF-15 | Ignored interrupt and cancel-before-IDs both force teardown, suppress late start, and return exit 5. |
| WF-16 | No response, oversized line, and stderr flood produce correct bounded failures with no live child. |
| WF-17 | Invalid IDs/hash, traversal/reparse, and root overlap reject before launch and preserve sentinels. |
| WF-18 | Wrong, missing, and extra output keys fail the strict oracle with exit 4. |
| WF-19 | Fixture mutation and injected evidence failure preserve actual failure, never success, and stop the tree. |
| WF-20 | Completion/cancel order follows the journal; unknown cleanup always exits 7. |

## Native-readiness selected offline portions — denominator 10

Every NI row below is limited to behavior that can be established without installed-profile collection or native Codex execution. Passing these rows does not establish full NI-T01..NI-T10 readiness. NI-T05's actual immediately-prelaunch observation and the actual effective-profile/runtime portions of NI-T07..NI-T10 remain pending outside this campaign.

| ID | Required offline observation |
| --- | --- |
| NI-T01 | Exact two-junction launcher mapping admits only the physical executable. |
| NI-T02 | Changed target/type and same bytes elsewhere reject before spawn. |
| NI-T03 | Digest mismatch, missing physical file, and unsupported adapter reject without PATH fallback. |
| NI-T04 | Fixture/run/review/profile reparses reject, including paths through approved launcher junctions. |
| NI-T05 | Offline alias/byte drift at final recheck rejects before spawn and preserves evidence; no live-Codex credit. |
| NI-T06 | Peer admission, all WF cases/subfixtures, and F-01/F-02 remain valid. |
| NI-T07 | Exact shell-free native-only argv/policy is enforced; injection and mismatch reject. |
| NI-T08 | Legacy/unknown/mismatched review-policy/inventory and incomplete source coverage block readiness. |
| NI-T09 | Synthetic protocol proves strict RPC order, inactive effects, complete pagination, one-worker accounting, and no work RPC; no installed-profile credit. |
| NI-T10 | Synthetic source/environment/provider/auth/model/effort/sandbox/rate-limit conflicts block work; no installed-profile credit. |

NI-T11/WN-01 and NI-T12/WN-02 remain a separate `0/2 BLOCKED/NOT_RUN` native denominator and will not execute. This run will not recalculate or improve any aggregate full-readiness percentage from offline evidence alone.

## Focused defect regressions — denominator 2

| ID | Required observation |
| --- | --- |
| F-01 | Full stdin-pipe pressure cannot defeat deadline/cancel handling; deadline exits 6, cancel exits 5, and the owned process tree stops. |
| F-02 | Only approved typed error fields survive; private canaries and unknown nested provider fields are absent from journal/stdout/stderr while required category/code fields remain. |

## Cross-cutting checks

| ID | Required observation |
| --- | --- |
| QA-INTEGRITY | No prohibited mock decorator, result gaming, ignored required case, fake native claim, source exclusion, or denominator manipulation in frozen product/tests or QA helpers. |
| QA-BUILD | `cargo build --locked --offline --bins` succeeds before SI-T08 unit checks and produces the required peer under the QA-owned target. |
| QA-UNIT | Complete frozen unit inventory reaches at least 95%; every mandatory unit invariant passes. |
| QA-SUITE | Complete frozen all-target inventory reaches at least 95%; every mandatory group and subfixture passes. |
| QA-FMT | `cargo fmt --all -- --check` exits 0. |
| QA-CLIPPY | Locked/offline all-target Clippy with `-D warnings` exits 0. |
| QA-DOC | Documentation tests are discovered and executed; zero discovered is reported as zero, not omitted. |
| QA-COVERAGE | One complete full-source LLVM collection reaches at least 95% with all 12 `src/*.rs` files accounted for and no first-party exclusion. |

## Final execution accounting

All statuses below apply only to the selected offline scope. One executable observation can satisfy overlapping requirement groups; these 42 groups are not added to the unique Rust-test denominator.

| Criterion groups | Count | Final status | Qualifying evidence |
| --- | ---: | --- | --- |
| SI-T01..SI-T06 | 6/6 | PASS | Original-package focused collector campaign `09-focused-collector`, complete original-package suite `12-full-all-targets`, and independently authored real-junction mapping/tag/target/member/schema matrix `38-independent-negative-matrix-corrected`. |
| SI-T07 | 1/1 | PASS | Original-package focused review campaign `10-focused-review`; attempt 38 independently rejects stale inventory/source, legacy review schema, missing inventory reference, and omitted/extra physical source bindings. |
| SI-T08 | 1/1 | PASS | Original-package final-boundary campaign `11-focused-final-boundary`; attempt 38 verifies durable intent followed by rejection with no spawn; mutant sensitivity attempt 44 makes the same assertion fail when the final-check error is deliberately ignored. |
| SI-T09 | 1/1 | PASS | Complete original-package suite `12-full-all-targets` (123/123), static checks `16-fmt`, `17-clippy`, and complete coverage `20-coverage`/`22-coverage-analysis`. |
| SI-T10 | 1/1 | PASS | `50-final-readback`: candidate 56/56 and all four specifications unchanged; exact installed junction/tag/target metadata observed without collection; historical failed attempts retained. |
| WF-01..WF-20 | 20/20 | PASS | Frozen inventory and complete original-package suite `12-full-all-targets`; retained process/protocol fixtures and assertions were reviewed under `test-integrity.md`. |
| NI-T01..NI-T10, selected offline portions only | 10/10 | PASS | Frozen inventory and complete original-package suite `12-full-all-targets`, focused attempts 09..11, and attempt 38. No installed-profile or native-Codex credit is assigned. |
| F-01..F-02 | 2/2 | PASS | Complete original-package suite `12-full-all-targets`, including `tests/remediation.rs`; no skipped cases. |
| **Selected offline total** | **42/42** | **PASS** | Overlapping traceability groups, with every subfixture conjunctive. |
| WN-01..WN-02 | 0/2 | BLOCKED / NOT_RUN | Separate native denominator; Codex was not launched and installed-profile collection was not performed. |

Cross-cutting outcomes: QA-BUILD PASS (`05-build-bins`); QA-UNIT PASS 37/37; QA-SUITE PASS 123/123; QA-FMT PASS (`16-fmt`); QA-CLIPPY PASS (`17-clippy`); QA-DOC PASS with 0 discovered (`18-doc-tests`); QA-COVERAGE PASS at 3191/3339 lines, 95.56753519017669961066%, all 12 source files and zero first-party exclusions (`22-coverage-analysis`).
