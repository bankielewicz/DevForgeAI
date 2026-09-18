# Independent Rust logging QA report

QA verdict: **FAIL**. Execution: **COMPLETED**. The unchanged candidate passes the declared numeric floors but its inspector accepts six inconsistent successful-run records, producing two OPEN mandatory defects. These are diagnostic evidence-validation defects; no protected-authority decision or unauthorized dispatch was demonstrated.

## Identity and scope

- Run/mode: 20260917T023835Z-qa / run. Plan readiness READY; no blocked required offline cases remain.
- Project: `C:\Projects\DevForgeAI`. Native Windows x64, OS reports Microsoft Windows 10.0.26200, native C: filesystem; PowerShell 7.6.6 at `C:\Program Files\PowerShell\7\pwsh.exe`. No Git metadata.
- Candidate: `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe-logging`;67 files bound in [candidate-manifest.json](candidate-manifest.json), SHA256 `95a013a233fb74c168d0eb7d45a8732cdfffa3420b9bf63c1fe2b993c3351677`. All match the delivered development candidate and final readback.
- Plan: `C:\Projects\DevForgeAI\docs\plan\framework-worker-logging\20260917T023835Z-qa\plan.md`, SHA256 `fa4f60fb553ed7521c7091c5f10b095cceefc19ab4e3e2aa9d8e863687580263`; [plan-binding.json](plan-binding.json). Initial plan/inventory remain historical NOT_STARTED/NOT_RUN records; final state is in checkpoint/case-results.
- Selected inputs: [input-manifest.json](input-manifest.json), SHA256 `56f87de5a57400a376a453a540a813f24312a5d940dce8bda4d874b9fb5dd49e`;37 paths. Governing current AGENTS.md and installed `.agents/skills/qa` are included. No relevant saved-memory claim was used.
- Build identity: [binary-manifest.json](binary-manifest.json). Main compiled probe SHA256 `a91bba376364cbba4cdbeb9cf84904e401ef89f476fc965f043dc6294abb9151`; independent test binary SHA256 `3860be55202ec3298d5e027bcd089e738e19848d6702506736c13b179cfc8d23` in [independent-binary-v2.json](independent-binary-v2.json).
- Development delivery: `C:\Projects\DevForgeAI\docs\plan\framework-worker-logging\20260917T014842Z-dev\delivery.md` and sibling qa-handoff.md; bound in input-manifest. The supplied 153/153 claim was independently rerun as 152 package cases plus 1 supplemental case, then 13 fresh acceptance cases were added before execution.
- Effects: isolated offline builds, instrumentation, real synthetic Windows child processes/junctions, independent fixtures and retained evidence only. No product/developer-test edits, native Codex, installed-profile collection, installation, operational changes, deployment, framework acceptance or release decision.

The selected contract amendments control schema 3, policy v3 and logging. Exact specifications are also indexed by [specification-bindings.json](specification-bindings.json):

| Selected source | SHA256 |
| --- | --- |
| `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe-logging\logging-contract.md` | `39bd2fe1b7743e816bef16e28818c8a6ed0d61df5e8dcd61092593dbf65a1a19` |
| `C:\Projects\DevForgeAI\docs\plan\framework-worker-diagnostics\20260916T181820Z-dev\diagnostic-contract.md` | `a1c35642f3c4c5a2bf4102495cca48f791877cc9d67416cbd1179dc831ac9779` |
| `C:\Projects\DevForgeAI\docs\plan\framework-worker-startup-investigation\20260916T204555Z\logging-design.md` | `ef48a57d46e535e3311b2a468657ae4729b9cc77b541cc5778493f0a00530389` |
| `C:\Projects\DevForgeAI\docs\plan\framework-worker-startup-investigation\20260916T204555Z\investigation-report.md` | `415663379d3782afd45a49dd13e976421f1bcafe03355aacd25b46143f08052d` |
| `C:\Projects\DevForgeAI\docs\specs\framework\runtime\codex-worker-feasibility-v1.md` | `7cb5b0cb87e515bb4d59235b615922ab4ea07ef607b8111dde6cc73c8f101b23` |
| `C:\Projects\DevForgeAI\docs\specs\framework\runtime\codex-worker-native-readiness-v1.md` | `c3c0673cbf95ae7aa056d9fd0009ce89947309b943013fd7838438d6ee66b06d` |
| `C:\Projects\DevForgeAI\docs\specs\framework\runtime\codex-worker-preflight-v1.md` | `6e781f23f221d1033896716512e9162579653b529d107e0040d49c499574afd1` |
| `C:\Projects\DevForgeAI\docs\specs\framework\runtime\codex-worker-source-identity-v1.md` | `34160ff675f886aeeebd3a7d131fd973b86a375fb64def7604db419c79db1f8c` |

## Acceptance traceability

LD-01..12 are local locators for the logging design's numbered acceptance cases. Grouped criterion rows retain every selected ID; [criterion-results.json](criterion-results.json) is the machine-readable map and [case-results.json](case-results.json) contains all 166 unique cases. PASS rows are bounded to their stated offline behavior. Broader native/authority deliverables were not selected.

| Criterion/source | Required behavior | Case IDs | Expected | Actual | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| LG-01; LD-09 | Closed schema, literal config paths, <=4096 bytes, digest copy and final check | PKG-070..072,079..081; QA-01,02 | Invalid intake never spawns; exact boundary and legacy composition work | All predicates passed, including real junction denial and copied-byte digest | PASS | 08-qa01,09-qa02,03-coverage |
| LG-02; LD-01,02,05 | Mandatory ordered pre/post exit and joined-reader capture | PKG-074,093,143; SUP-01; QA-03,04,09 | Complete temporal exit/capture evidence; inspector enforces it | Real exits/readers passed; missing or contradictory post-stop evidence still inspects completed | FAIL | 10-qa03,11-qa04,16-qa09,24-cli-confirm; QA-LOG-01,02 |
| LG-03; LD-03,04,06,11 capture slice | Bounded independent pumps, full-byte hashes and explicit incomplete capture | PKG-001..004,073,097,126; SUP-01; QA-04,05,09 | Exact hashes/limits; incomplete capture cannot qualify a complete observation | Real pumping/limits passed; inspector accepts drain false/read error/overflow on completed evidence | FAIL | 11-qa04,12-qa05,16-qa09,21-supplement; QA-LOG-01 |
| LG-04; LD-06,07,08,11 sink slice | Four levels, closed data, fixed optional file and caps; mandatory failure precedence | PKG-005,006,038..041,069,077; QA-06,07,08 | No canaries; optional failures nonauthoritative; required writes still fail and clean up | All assertions passed, including real file and accounting failures | PASS | 13-qa06,14-qa07,15-qa08,03-coverage |
| LG-05; LD-01,02,08 classification slice | Only two known startup Error patterns, explicit truncation | PKG-001..004,074; QA-03..05 | Known patterns classify; lookalikes stay unclassified; exact byte accounting | Positive/negative byte oracles passed; no inferred crash diagnosis | PASS | 10-qa03,11-qa04,12-qa05 |
| LG-06; LD-12 | Bound current capture/status/log evidence; preserve legacy and interrupted prefixes | PKG-006,075,076,084,092,144; QA-09,10 | Reject missing/inconsistent evidence; preserve sound historical interpretation | 6 of 9 planned mutations falsely accepted;3 rejected; legacy/interrupted checks passed | FAIL | 16-qa09,17-qa10,24-cli-confirm; QA-LOG-01,02 |
| LG-07 | Only 15 policy key quote pairs change;116 argv positions/values and review binding | PKG-045,067,068,078..081; QA-11 | Exact permitted byte differences and schema 3/v2 composition | Independent old/new vector comparison and denials passed without native launch | PASS | 18-qa11,03-coverage |
| LG-08 | Inherited and independent verification, real query_failed, floors, fmt/Clippy | PKG-001..152; SUP-01; QA-01..13; BUILD/FMT/CLIPPY | Every mandatory case and both numeric floors pass | Numeric floors/static checks pass; mandatory QA-09 fails | FAIL | case-results.json,metrics.json,attempt-index.json |
| DFF-WORKER-FEAS-01 sections3..7; WF-01..08; LD-10 | Strict wire subset, gates, correlation, single turn, independent oracle | PKG-050,057..068,086,088..091,098..125; QA-08,11,12 | Only admitted/qualified work; exact trace and specification result | All applicable offline trace/denial/oracle assertions passed | PASS | 03-coverage,15-qa08,18-qa11,19-qa12 |
| WF-09..12; F-01/F-02 recovery regressions; base section7 | Exclusive persistence, intent before effect, no replay, honest inspection | PKG-082,084,128..144,149; QA-09,10,12 | No mutation/replay; sound records inspect; inconsistent success rejected | Inherited cases pass, but new capture/exit inconsistency is accepted | FAIL | 03-coverage,16-qa09,17-qa10,24-cli-confirm |
| WF-13..16 | Native Windows ownership, Ctrl+C/EOF/owner death, descendants and production watchdog | PKG-085,093..097,132,133,135,137,142; QA-03..05 | Owned trees stop; pipes drain; fixed 120-second watchdog fires | Complete actual Windows campaign passed, including production watchdog | PASS | 03-coverage,10-qa03,11-qa04,12-qa05 |
| WF-17..20 | Unsafe inputs, oracle mismatch, fixture mutation and evidence/cleanup precedence | PKG-052..055,087,145,147..151; QA-01,02,07,12 | Closed rejection/explicit failure; no success from child claim alone | Executed failure-path and preservation assertions passed | PASS | 03-coverage,08-qa01,09-qa02,14-qa07,19-qa12 |
| NI-T01..10 offline; preflight companion | Exact launcher junctions/digests, fixed policy, review and no-work preflight | PKG-007..015,042..048,067,068,079..081,090..092,098..115,138; QA-11,12 | Synthetic identity/review denials and exact preflight gates | Applicable offline assertions passed; no installed/native qualification inferred | PASS | 03-coverage,18-qa11,19-qa12 |
| SI-T01..08 | Single allowed source junction, complete source inventory, freshness/final check | PKG-016..035,042,044,046,049,152; QA-11,13 | Real synthetic Windows junctions; stale/malformed sources reject before spawn | All selected assertions passed against synthetic roots | PASS | 03-coverage,18-qa11,20-qa13 |
| SI-T09 | Existing source limits, credentials, identity/policy and WF/F-01/F-02 remain valid | PKG-007..049,098,128..152; QA-09,11..13 | Inherited behavior remains valid including current inspection | Source restrictions passed; expanded inspection semantics fail QA-09 | FAIL | 03-coverage,16-qa09; QA-LOG-01,02 |
| SI-T10 offline preservation slice; OUT-01 | Candidate, original, snapshot, bound inputs and console helper unchanged | QA-13; PRESERVE | All selected before/after bytes identical | 67 candidate,116 original/snapshot,37 inputs verified; no installed mapping mutation | PASS | 20-qa13,final-identity-check.json |
| Diagnostic v1 all stages; query_failed addendum | Same held-job query/1-1 guard; null counts on error; no RPC/private fields; closed category order | PKG-036..041,056,101..106; QA-08,12 | Real restricted handle fails actual API; closed observations/precedence | Actual QueryInformationJobObject error5, null counts/no work and cleanup asserted | PASS | 03-coverage,15-qa08,19-qa12; integrity.md |
| Documentation review | Factual native/authority boundaries, selected references and schema 3 description | QA-13; DOCS | Local references resolve; no acceptance inferred from prose | 12 documents / 49 local links reviewed; implementation completeness reduced by findings | PASS | documentation-review.json |
| NI-T11,NI-T12; WN-01,WN-02; installed-profile qualification | Separate native launch/installed source collection and operator evidence | Excluded from selected offline 166-case denominator | No native launch in this invocation | NOT_RUN; prerequisite independent offline QA has failed | NOT_APPLICABLE | plan.md; no native launch receipt |

LD-01..11's exercised runtime stimuli passed, including original exit1 cases and additional independent exit29 cases. The new failures are in interpreting completed historical evidence (LD-12/LG-06), not an observed live stream-pump failure. LG-02/03 and inherited inspection aggregates are reduced where their evidence invariants are not enforced.

## Test integrity

[integrity.md](integrity.md) records the bounded source/attribute/assertion inspection. All 67 selected files and the supplemental harness were inventoried; detailed semantics concentrated on changed runtime/test paths, WF bodies and shared helpers. Inherited attribute/import/assertion locations were inspected. No confirmed first-party mocking decorator/attribute, ignored test, coverage exclusion or result gaming was found. Serialization derives and explicit private fault seams were distinguished from mocks. This is not an exhaustive repository security review.

The real query_failed test duplicates the held Job handle without query permission and invokes the production QueryInformationJobObject mapping; it does not substitute a canned error. The full 120-second watchdog and actual Windows child/descendant tests ran. No native Codex qualification follows from them.

All supplied package/supplemental results were freshly executed. QA independently authored 13 conjunctive cases and literal byte/hash oracles, reviewed/read back helpers before use, and retained negative controls. QA-09 starts nine fresh real successful runs, confirms each unmodified control, then applies one planned mutation. It retains all observations and fails once if any invalid observation is accepted. Six were accepted; missing capture, missing status and malformed log controls were correctly rejected. This prevents inherited green tests from hiding the defect.

One QA-only preparation error occurred in attempt06-qa01 (junction command returned exit1). Its raw output and old helper/binary remain under that attempt. The documented one-attempt correction changed only QA command selection; attempt08-qa01 passed after rebuilt-helper binding. [harness-gap-01.md](harness-gap-01.md) records QA-H01. Root cause of the initial command syntax failure was not established; it is not a product defect. The same case counts once, and no product failure was retried or removed. The latest helper bindings are qa-helper-manifest-v2.json and independent-binary-v2.json; earlier manifests bind the retained earlier helper versions.

## Metrics and environments

Windows is the only selected platform, so its exact integer ratios are also the overall ratios. Threshold decisions compare counts without rounding; displayed decimals below are expansions of the exact ratios.

| Platform | Metric | Numerator | Denominator | Exact ratio / decimal percent | Floor | Result | Raw evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Windows/overall | Executed-line coverage |3858|4041|100*3858/4041 =95.47141796585003711952487008...|95%|PASS|coverage.json, coverage-analysis.json|
| Windows/overall | Required unit cases |49|49|100%|95%|PASS|03-coverage/stdout.txt, package-results.json|
| Windows/overall | Declared project suite |165|166|100*165/166 =99.39759036144578313253012048...|95%|PASS numerical floor only|case-results.json, metrics.json|
| Windows/overall | Package integration |103|103|100%|Included in project suite|PASS|03-coverage/stdout.txt|
| Windows/overall | Supplemental integration |1|1|100%|Included in project suite|PASS|21-supplement/stdout.txt|
| Windows/overall | Independent acceptance |12|13|100*12/13 =92.30769230769230769230769231...|No separate category floor; every case mandatory|FAIL conformance|08..20 attempts; QA-09 FAIL|

Coverage denominator: all 15 `src/*.rs` files declared before execution;14 have executable lines, declaration-only lib.rs has none. No executable first-party file was excluded. Test/support fixtures and dependencies are excluded. The complete unfiltered 152-case package campaign alone contributes coverage; SUP-01 and the 13 independent cases do not. Collection completed once with exit0, no skipped cases and usable LLVM JSON. Raw coverage SHA256 `610db5cec92d19f6f8e3571f9bcb45e86631c397345930bb1ad48241cf0c813d`. This reproduces the reported 95.47% without treating it as acceptance.

Tools: native Rust/Cargo 1.97.1, rustfmt 1.9.0, Clippy 0.1.97, cargo-llvm-cov 0.8.4, LLVM 22.1.6; Cargo/Rust at `C:\Users\bryan\.cargo\bin`; Python 3.10 at `C:\Program Files\Python310\python.exe`. Exact executable vectors, cwd, environment overrides, times and exits are in [attempt-index.json](attempt-index.json) and per-attempt receipts. Cargo used existing offline locked dependencies; no installation.

BUILD, FMT and Clippy all-targets with `-D warnings`: PASS (01,22,23). Full coverage command completed in 200.234 seconds according to its receipt, including the production watchdog. Branch coverage: NOT_RUN; discovered collector advertises unstable branch collection and no nightly toolchain is installed. Linux, native Codex and native rendered UI are unqualified/not selected. No partial measurement was used to trigger or avoid a stop; complete unit, line and project-suite floors pass.

## Defects and unresolved work

| ID | Requirement | Issue class / impact | Failure | Ownership | Evidence |
| --- | --- | --- | --- | --- | --- |
| QA-LOG-01 OPEN | LG-02/03/06, LD-12, base inspection | MANDATORY_PRODUCT_DEFECT; false complete diagnostic evidence | drain=false, missing EOF, reader error or byte overflow still returns completed | dev; capture.rs::Capture::validate and journal.rs::inspect |16-qa09,24-cli-confirm; qa-fix.md|
| QA-LOG-02 OPEN | LG-02/06, base exit/inspection | MANDATORY_PRODUCT_DEFECT; missing/contradictory mandatory exit accepted | absent process_exit.worker_exit_code or29 versus terminal0 still returns completed | dev; journal.rs::inspect |16-qa09,24-cli-confirm; qa-fix.md|
| QA-H01 resolved harness gap | QA fixture preparation | QA-owned setup ERROR, not product failure | initial junction creation syntax error; retained, corrected once and passed | QA helper only; already resolved |06-qa01,07-helper-rebuild,08-qa01; harness-gap-01.md|

No advisory repair scope or unresolved specification decision was added. No mandatory offline case remains NOT_RUN. Native NI-T11/12 and WN-01/02, installed-profile qualification and branch measurement remain explicitly unperformed outside this selected offline case inventory; independent offline QA must pass before downstream native qualification under the contract.

## Continuation, stopping and remaining obligations

Attempt03 finished complete metrics before independent cases. Attempt06 produced a local harness gap;07 rebuilt the QA helper and08 completed that case. Attempt16 (2026-09-17T02:56:51.415399Z to02:56:52.819452Z) confirmed both ordinary mandatory defects. The decision retained final FAIL and continued ready, safe independent QA-10..13, supplemental, formatting and Clippy checks. Attempt24 used only the already-built CLI's read-only inspect command and confirmed both findings, exit0/state completed, with unchanged run bytes.

There was no terminal integrity, metric, critical authorization/security/data-loss, identity or ownership stop. The inspector false-success result did not demonstrate protected framework acceptance, unauthorized dispatch or unintended mutation of preserved data. No issue was downgraded from a terminal class and no speculative authority capability was assumed. Remaining cases were safe, source-bound and independent of the failed consistency predicates.

All 24 command/confirmation receipts are terminal and none timed out. Actual test-held handles, stopped-tree results and joined readers provide process cleanup evidence; no historical PID was killed. No live tool session or pending owned invocation remains. QA fixture/junction directories and all target outputs are intentionally retained under this evidence root, including failed attempts. No assertion of repository-wide process absence or unobserved cleanup is made. There are no partially collected mandatory metrics or blocked dependents.

## Disposition

Product QA outcome: **FAIL**, because QA-LOG-01/02 violate mandatory criteria despite passing numeric floors. Repair owner: **dev**. [qa-fix.md](qa-fix.md) is the bound correction/retest packet; its final SHA256 is the `qa-fix.md` entry in handoff-manifest.json. Only an explicitly selected independent retest can close these OPEN findings after a corrected candidate is supplied.

Final identity readback: all 67 candidate files,116 original/snapshot files,37 input files and current helper/build identities match; see final-identity-check.json. PowerShell helper remains unchanged. External framework acceptance: **NOT_EVALUATED**. Release/deployment authorization: not granted.

## Artifact delivery

Original selection: `C:\Projects\DevForgeAI\docs\plan\framework-worker-logging`. Literal fresh destination: `C:\Projects\DevForgeAI\docs\plan\framework-worker-logging\20260917T023835Z-qa`. Required artifacts are plan.md, qa-report.md, qa-fix.md, checkpoint.json, input/candidate/specification manifests, criterion-results.json, case-results.json, raw attempts and final external bindings. All are published at these paths; final publication readback is recorded by final-readback.json after hashing.

The external `C:\Projects\DevForgeAI\docs\plan\framework-worker-logging\20260917T023835Z-qa\handoff-manifest.json` records required and actual absolute paths, byte lengths and SHA256. Exact cross-reference entry keys include `qa-report.md`, `qa-fix.md`, `checkpoint.json`, `plan.md`, `candidate-manifest.json`, `input-manifest.json`, `specification-bindings.json`, `evidence-manifest.json` and `dev-prompt.txt`. It does not hash itself. evidence-manifest.json binds regular retained evidence while excluding Cargo target intermediates; produced binaries are separately bound. Junctions are recorded without traversing them. Any final write/readback error prevents a delivered claim and must be repaired only at this original destination; see final-readback.json for actual completion.

## End-user handoff

Open `C:\Projects\DevForgeAI` in Codex on native Windows. Next owner/action: dev repairs the two selected defects in a fresh sibling candidate, then returns a candidate for separately selected QA retest. Current host skill catalog exposes `dev` at `C:\Projects\DevForgeAI\.agents\skills\dev\SKILL.md`; it was not invoked or installed by QA. No additional approval or skill-installation prerequisite blocks the manual handoff.

Paste into the Codex conversation input (not PowerShell); final conversation also supplies the external manifest's SHA256:

```text
$dev In C:\Projects\DevForgeAI using native Windows PowerShell, remediate QA-LOG-01 and QA-LOG-02 only.

Read current AGENTS.md and verify C:\Projects\DevForgeAI\docs\plan\framework-worker-logging\20260917T023835Z-qa\handoff-manifest.json, especially entries qa-report.md, qa-fix.md, specification-bindings.json, input-manifest.json and candidate-manifest.json. Those manifests bind the exact eight selected specifications and handoff bytes. The failed candidate is C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe-logging; candidate-manifest.json SHA256 is 95a013a233fb74c168d0eb7d45a8732cdfffa3420b9bf63c1fe2b993c3351677. Report material drift before editing; do not restore older source.

Create the corrected candidate at C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe-logging-qa-fixes, preserving the failed candidate, frozen original/snapshot, all prior evidence, unrelated changes and Start-CodexAppServerDiagnostic.ps1. Restore capture completeness and mandatory post-stop exit consistency for successful inspection, preserving legitimate failure/cancellation and historical-schema semantics. Follow red -> green -> refactor and applicable offline regression/QA checks with >=95% first-party executed-line coverage and required unit/project-suite pass rates. Retain real red evidence and independent positive/negative oracles.

Return corrected source/build identity, changed-file manifest, fresh evidence paths/raw metrics and a per-defect resolution map for separately selected independent QA retest. Do not self-close QA findings, issue framework acceptance, launch native Codex, change operational configuration, install/deploy, or auto-invoke QA.
```
