# QA remediation handoff to dev

## Selected candidate and authority

QA run: 20260917T023835Z-qa, verdict **FAIL**, execution COMPLETED. Report: `C:\Projects\DevForgeAI\docs\plan\framework-worker-logging\20260917T023835Z-qa\qa-report.md`; SHA256 is the exact `qa-report.md` entry in `C:\Projects\DevForgeAI\docs\plan\framework-worker-logging\20260917T023835Z-qa\handoff-manifest.json`. This packet's digest is its `qa-fix.md` entry. Repair is a manual next invocation; QA has not changed product source or invoked dev.

Failed candidate: `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe-logging`,67 files; candidate-manifest.json SHA256 `95a013a233fb74c168d0eb7d45a8732cdfffa3420b9bf63c1fe2b993c3351677`. Main compiled executable in `C:\Projects\DevForgeAI\docs\plan\framework-worker-logging\20260917T023835Z-qa\build-target\debug\devforgeai-codex-worker-probe.exe` has SHA256 `a91bba376364cbba4cdbeb9cf84904e401ef89f476fc965f043dc6294abb9151`. Plan SHA256 `fa4f60fb553ed7521c7091c5f10b095cceefc19ab4e3e2aa9d8e863687580263`. Exact original specification paths/hashes are in specification-bindings.json (8 contracts/clarifications), input-manifest.json (37 selected inputs; SHA256 `56f87de5a57400a376a453a540a813f24312a5d940dce8bda4d874b9fb5dd49e`), and the report table.

Project/environment: `C:\Projects\DevForgeAI`, native Windows x64 / PowerShell 7.6.6 / native C: filesystem; Rust/Cargo 1.97.1, locked offline dependencies. Evidence destination: `C:\Projects\DevForgeAI\docs\plan\framework-worker-logging\20260917T023835Z-qa`. Current AGENTS.md and applicable development skill govern any future implementation. Mandatory first-party executed-line and required unit/project-suite floors remain independently >=95%; failed mandatory behavior cannot be waived by the percentages.

Remediation owner: **dev**. Selected defects: **QA-LOG-01, QA-LOG-02**, both OPEN. Proposed manual repair output: `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe-logging-qa-fixes` (verified absent during QA handoff preparation). Preserve the failed candidate in place; create fresh corrected source/evidence without resetting, installing or overwriting existing attempts. Scope is Rust capture/inspection consistency and specification-aligned regression tests; expand only as necessary for these two demonstrated defects. No native Codex, operational configuration, PowerShell helper edits, installation, deployment, protected acceptance or automatic retest is selected.

## Shared reproduction and evidence

QA-09 is implemented at qa-harness/independent.rs:217. For each of 9 planned mutations it creates a fresh schema 3/debug successful WF-01 run, observes exit0 with stopped tree and unchanged fixture, verifies the original inspector returns completed, preserves journal-before.jsonl, changes one capture/exit/status/log condition, and records mutation-result.json. Six invalid variants return Ok/completed. The other three controls (missing capture, missing status, malformed log) correctly reject. The final test assertion fails once; it does not retry the product or inflate case counts.

Original full command/environment: attempts/16-qa09/receipt.json; raw assertion: attempts/16-qa09/stdout.txt; Cargo exit101. All records are externally bound by evidence-manifest.json. A future fresh execution must allocate its own fixture/attempt path and verify current identities first; do not rerun the existing exclusive recorder attempt.

The retained binary can reproduce the false inspector observations without any worker launch. From `C:\Projects\DevForgeAI` in PowerShell, the following exact commands were independently exercised in attempt24:

```powershell
& 'C:\Projects\DevForgeAI\docs\plan\framework-worker-logging\20260917T023835Z-qa\build-target\debug\devforgeai-codex-worker-probe.exe' inspect --run-dir 'C:\Projects\DevForgeAI\docs\plan\framework-worker-logging\20260917T023835Z-qa\attempts\16-qa09\fixtures\qa09rE4EEf\run' --after 0 --limit 100
& 'C:\Projects\DevForgeAI\docs\plan\framework-worker-logging\20260917T023835Z-qa\build-target\debug\devforgeai-codex-worker-probe.exe' inspect --run-dir 'C:\Projects\DevForgeAI\docs\plan\framework-worker-logging\20260917T023835Z-qa\attempts\16-qa09\fixtures\qa09cCNcpd\run' --after 0 --limit 100
```

Both exit0 with state completed. attempts/24-cli-confirm/receipt.json records executable hash, exact argv/cwd, elapsed time and unchanged=true for each run. This is confirmation through the compiled public CLI, not only a library assertion. Fixtures retain absolute bindings to the selected peer, source and fixture directories; preserve those bytes and paths when inspecting historical evidence.

## Defect QA-LOG-01

- State/class: OPEN, MANDATORY_PRODUCT_DEFECT, nonterminal. Mandatory conformance failure with false successful evidence; no demonstrated protected-authority or data-loss impact. Safe independent checks continued after attempt16; final verdict stayed FAIL.
- Requirements: logging-contract.md LG-02 (mandatory capture), LG-03 (digest complete only with EOF and no capture-preventing error/overflow), LG-06 (valid current completed observations), logging-design.md acceptance12; base contract inspection consistency.
- Ownership/artifact: application Rust, `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe-logging\src\capture.rs` Capture::validate lines80..100 and `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe-logging\src\journal.rs` inspect lines363..380,406..485. QA-created fixtures are the stimulus, not the defective artifact.
- Verified source mechanism: Capture::validate rejects EOF/read errors only when drain_complete is true, and does not reject byte_overflow in a claimed successful completion. inspect validates the capture shape then retains only exit_summary=true, so successful terminal checks do not enforce the required complete-capture condition. This verified explanation is limited to the demonstrated paths, not an exhaustive cause analysis.
- Preconditions: bound schema 3 inputs, debug diagnostics, valid successful peer/control, preserved binary/fixture paths; native Windows. No native Codex or external credentials.

| Fixture under attempts/16-qa09/fixtures | Changed process_exit field(s) | Expected | Observed |
| --- | --- | --- | --- |
|qa09rE4EEf|capture.drain_complete=false|Reject inconsistent completed evidence|Ok/state completed|
|qa09LmAQen|capture.stdout.eof=false and drain_complete=false|Reject incomplete capture claiming completion|Ok/state completed|
|qa09pPRBRh|capture.stdout.read_error=pipe_read_failed and drain_complete=false|Reject reader failure claiming completion|Ok/state completed|
|qa09W3tEW5|capture.stdout.byte_overflow=true|Reject overflow claiming complete capture|Ok/state completed|

Each directory has journal-before.jsonl, run/journal.jsonl, result.json and mutation-result.json. Original terminal outcome, worker code0, valid optional log/status and successful control remain otherwise unchanged. The first variant is also reproduced through CLI as above. Evidence reproduction is **CONFIRMED**; optional sink/hash checks did not catch these semantic contradictions.

Required correction: inspection must enforce completion semantics for current capture-bearing records and reject inconsistent successful completion. Retain the typed capture state through the terminal decision or use another sound equivalent. Do not merely set drain_complete/EOF true, erase error/overflow fields, suppress failed tests, or accept a byte hash as proof of complete capture. No particular speculative algorithm is required.

Compatibility: legitimate historical schemas must remain inspectable. A failed/cancelled/timed-out/cleanup-uncertain run may truthfully report incomplete capture; do not globally reject every explicit failure observation as malformed. Off still requires mandatory capture/status but no optional file. Optional diagnostics incompleteness remains nonauthoritative. Pre-stop exit remains a temporal observation, not proof of self-exit or crash.

Required regressions: preserve each independently mutated success/control pair above, include both streams and valid historical/failure controls, assert the public inspect result/code is appropriate and leaves bytes unchanged. Preserve actual reader-budget/EOF/error tests and no worker launch on inspection. Recheck affected integration, fmt/Clippy, integrity, and complete source/metric collections for the corrected bytes.

Retest condition: explicitly select the corrected candidate and this defect for independent QA; rerun the failure predicates against fresh completed evidence plus affected regressions. Only independent QA can mark VERIFIED_FIXED. No tests were stopped; QA-09's original FAIL remains. Owned child cleanup completed before evidence mutation; all test invocations ended. Dependencies: shares current capture-bearing terminal validation with QA-LOG-02; neither requires resolving a missing specification decision.

## Defect QA-LOG-02

- State/class: OPEN, MANDATORY_PRODUCT_DEFECT, nonterminal. A required exit observation is missing or conflicts with the successful terminal while inspect still reports completed. No demonstrated runtime authorization or protected framework acceptance.
- Requirements: logging-contract.md LG-02 mandatory post-stop code and LG-06 valid current completed evidence; base contract sections4/7 exit/inspection consistency.
- Ownership/artifact: application `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe-logging\src\journal.rs` inspect lines363..380 (deserialization/presence handling),432..483 (success checks). Source citations were numbered/read immediately before handoff.
- Verified mechanism: process_exit.worker_exit_code is indexed into serde_json::Value and deserialized as Option<u32>; an absent key becomes Null/None. Unlike pre_stop_exit_code, its key presence is not checked. The parsed post-stop value is discarded and never compared with terminal.worker_exit_code; successful terminal validation checks only its own zero code.
- Preconditions: same real successful schema 3/debug control and native Windows retained fixtures as above.

| Fixture under attempts/16-qa09/fixtures | Mutation | Expected | Observed |
| --- | --- | --- | --- |
|qa09cCNcpd|process_exit.worker_exit_code=29; terminal.worker_exit_code stays0|Reject contradictory mandatory exit evidence|Ok/state completed|
|qa09j98aey|Delete process_exit.worker_exit_code|Reject absent mandatory post-stop observation|Ok/state completed|

Reproduction is **CONFIRMED** by the independent mutation case; the contradictory value also reproduces through the compiled CLI command above. The same four retained artifact names apply. Exact hashes are in evidence-manifest.json; original successful result/control and unchanged diagnostic file remain available.

Required correction: enforce schema-dependent mandatory field presence and valid typed post-stop observations, then reconcile current success terminal codes with the corresponding process_exit record. A successful observation requires the independently observed successful exit that its terminal claims. Preserve appropriate nullable observations for legitimate failed cleanup/query situations rather than inventing an exit code. Do not conflate pre-stop/post-stop timing or merely copy the terminal code into missing evidence.

Required regressions: missing key versus explicit null where semantically permitted, nonzero/zero contradictions, matching successful zero and legitimate nonzero failed outcomes, both completed and preflight_checked success branches where applicable, historical-schema compatibility, read-only CLI behavior and no replay. Keep native-profile test controls synthetic; no native Codex launch is required for this repair. Run affected and full declared offline regressions/metrics with unchanged denominator policy.

Retest condition: separately select corrected identity and QA-LOG-02 for independent failure/compatibility checks; development's repair claim becomes FIX_REPORTED only, not closure. No tests remain stopped or unexecuted from this run. Cleanup is the same verified stopped child/control state; no historical PID action occurred. Dependency: QA-LOG-01 shares journal validation, so coordinated focused correction is reasonable without widening scope.

## Return contract from dev

Return a fresh corrected candidate/build identity and changed-file manifest, per-defect correction/evidence references and state FIX_REPORTED, actual red/green/refactor results, raw required-unit/project-suite counts and complete first-party line coverage, compatibility/negative-path results, and exact paths/environment for independently selected retest. Preserve all original failure records and the unchanged failed candidate. No model/Python report may issue protected framework acceptance.

## Pending prerequisites or specification decisions

None blocks scoped offline repair. QA-H01 was a resolved QA-only setup gap, not a selected dev defect. Branch coverage remains NOT_RUN with the current stable collector capability; no tool installation is implied. Native Codex/installed-profile qualification remains separately selected after offline QA passes. Current findings do not establish a need for native execution or operational changes.

## End-user remediation invocation

Open `C:\Projects\DevForgeAI` using native Windows PowerShell in Codex. The current host skill catalog exposes dev at `C:\Projects\DevForgeAI\.agents\skills\dev\SKILL.md`. Paste this into the Codex conversation input; QA does not send it or initiate the repair:

```text
$dev In C:\Projects\DevForgeAI using native Windows PowerShell, remediate QA-LOG-01 and QA-LOG-02 only.

Read current AGENTS.md and verify C:\Projects\DevForgeAI\docs\plan\framework-worker-logging\20260917T023835Z-qa\handoff-manifest.json, especially entries qa-report.md, qa-fix.md, specification-bindings.json, input-manifest.json and candidate-manifest.json. Those manifests bind the exact eight selected specifications and handoff bytes. The failed candidate is C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe-logging; candidate-manifest.json SHA256 is 95a013a233fb74c168d0eb7d45a8732cdfffa3420b9bf63c1fe2b993c3351677. Report material drift before editing; do not restore older source.

Create the corrected candidate at C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe-logging-qa-fixes, preserving the failed candidate, frozen original/snapshot, all prior evidence, unrelated changes and Start-CodexAppServerDiagnostic.ps1. Restore capture completeness and mandatory post-stop exit consistency for successful inspection, preserving legitimate failure/cancellation and historical-schema semantics. Follow red -> green -> refactor and applicable offline regression/QA checks with >=95% first-party executed-line coverage and required unit/project-suite pass rates. Retain real red evidence and independent positive/negative oracles.

Return corrected source/build identity, changed-file manifest, fresh evidence paths/raw metrics and a per-defect resolution map for separately selected independent QA retest. Do not self-close QA findings, issue framework acceptance, launch native Codex, change operational configuration, install/deploy, or auto-invoke QA.
```
