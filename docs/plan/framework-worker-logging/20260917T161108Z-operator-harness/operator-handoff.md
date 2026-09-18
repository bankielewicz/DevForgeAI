# Operator harness handoff — preparation review required

Development status: **PARTIAL**. OW-02's implementation and offline behavior checks are complete. OW-01's refreshed proposal exists, but activating its changed configuration requires Bryan's review. OW-03, OW-04 and OW-05 have not run. Native Codex: **NOT_RUN**. Framework acceptance: **NOT_EVALUATED**. No independent QA was invoked and no existing QA finding was self-closed.

## Concrete decision

Approve preparing the already-selected diagnostic with the configuration currently on this computer, including the newly added experimental context-management setting. Keep the stopped preparation as evidence and use a fresh reservation for the single native run that has not happened yet. This approval does not launch Codex or edit installed configuration.

The [review proposal](current-source-review/operator-selection.proposed.md), [exact configuration difference](config-drift.json), [inventory comparison](current-source-review/comparison.json), [proposed configuration](current-source-review/configuration.proposed.json), and [bound draft inputs](current-source-review/prepared-proposal/inputs/input-manifest.json) make that decision concrete. The draft review has a null reviewer and is not an approved native request. The active harness configuration remains unchanged and stops on the retained reservation. No ready native command is issued before finalization.

This review is required by the selected [outstanding-work contract](../../framework-worker-diagnostic-outstanding-work.md), which says to preserve existing approvals and review new material source differences. The already-approved host permission addition for the offline test runner is separately proven in [permission-rule-addition.json](current-source-review/permission-rule-addition.json); it does not need another approval.

## What changed

- Added the root [Invoke-CodexWorkerDiagnostic.ps1](../../../../Invoke-CodexWorkerDiagnostic.ps1). Its default mode prepares only; `-RunOnce` is the explicit later operator dispatch. It verifies the runtime seal, passes literal arguments, displays stages and retains the child exit status.
- Added the versioned [support package](../../framework-worker-trials/20260917T122229Z-logging-diagnostic/operator-harness-001/diagnostic.py). It separates immutable evidence from current installed sources, recollects with the selected compiled Rust collector, stops on uncovered inventory changes, creates exact-byte review/request bindings and prevents repeated dispatch.
- Derived [recorder.py](../../framework-worker-trials/20260917T122229Z-logging-diagnostic/operator-harness-001/recorder.py) from the preserved recorder. Repeated polling on the held process handle avoids the reproduced Python 3.10 Ctrl+C wait hang. Output files, cancellation bytes, stdin lifetime, ownership and deadlines remain intact. The original recorder is unchanged.
- Console output is bounded and independent of raw capture. The harness reports probe exit, observed worker exit, timeout and uncertain cleanup separately. Reading a journal field for display is explicitly not Rust inspection or acceptance.
- The optional resumed-preparation input requires exact hashes of a prior reservation and a zero-dispatch preparation stop. It preserves those files and uses a new exclusive reservation. An earlier native dispatch, changed prior record, occupied native run or second reservation remains a stop. This path has not been selected in the active configuration.

The corrected Rust source, QA build, failed candidate, snapshots, original evidence and all three older PowerShell helpers remain unchanged. Source/build identities and changed-file hashes are in [source-identities.json](source-identities.json) and [changed-file-manifest.json](changed-file-manifest.json).

## Executed verification

| Check | Current evidence and result |
| --- | --- |
| Python offline suite | [42/42 passed](attempts/15-python-final/test-results.json), including all 17 inherited recorder cases against the derived copy. Real synthetic Windows processes cover literal arguments, both streams, stdin, cancellation, timeout, denied termination and occupied-attempt prevention. |
| Python executed-line coverage | [295/296 lines, 99.662162%](attempts/15-python-final/coverage.json); 68/68 measured branches. No runtime exclusions. |
| PowerShell suite | [9/9 passed](attempts/16-powershell-final/test-results.json); mocked explicit dispatch boundary, synthetic Python argument/exit integration and a real preparation-stop check. |
| PowerShell executed-line coverage | [30/30 lines, 100%](attempts/16-powershell-final/coverage.xml); 37/37 commands. Separate branch coverage is not reported by this collector. |
| Combined source scope | 325/326 executed lines = 99.693252%. Scope is diagnostic.py, derived recorder.py and the root PowerShell entrypoint. Original supervisor.py is retained evidence and no longer imported by operator runtime. Tests, fixtures and evidence-only runners are excluded. |
| Required-case denominator | 53 distinct required cases: 51 passed, two live readiness cases blocked by the unapproved changed inputs/retained reservation. Overall 51/53 = 96.226415%; executed offline cases 51/51 = 100%. The mandatory readiness blockers prevent completion despite the numeric floors. |
| Syntax/static review | Python parse/compile succeeded. PowerShell parser reported zero errors. PSScriptAnalyzer 1.25.0 reported zero errors and four Write-Host advisories; these are intentional operator-console stage messages required by OW-02, not unattended library output. All advisories remain visible in [the report](static-checks/powershell-analysis-attempt-02.json). |
| Preservation | [393/393 original scoped bindings unchanged](preservation-final.json). The proposed-input preparation also hashed 21,828 unique files, including the 26 proposed current source files; that comparison does not claim operator approval. |
| Rust build/format/Clippy/coverage | Not rerun: this task does not modify or rebuild the selected Rust candidate. Its prior independent QA remains bound to the unchanged source/build, not counted as fresh wrapper evidence. |

All checks used native Windows, PowerShell 7.6.6 and Python 3.10.11. The Python collector is coverage.py 7.9.0; PowerShell tests use Pester 5.7.1. No tools were installed. Pester needed the host access approved in this conversation for temporary test registry fixtures and environment discovery.

## Retained failures and interpretation

- Attempts 01/03: the old executor reproduced the removed-Sites requirement; the new verification passed the same focused regression. Attempt 02's wrong optional manifest selector is retained as a setup error.
- Attempts 04/05: the initially silent preparation CLI failed the bound-packet assertion, then generated a concrete packet without native dispatch.
- Attempts 06/07: empty synthetic environments were rejected by Windows; this fixture error was corrected. Separately, the retained recorder's Ctrl+C case exceeded its 2.9-second budget. A stack trace showed Python 3.10 waiting inside its interrupt handling; bounded attempt 07 stopped the test. The derived recorder passes that case and the other inherited tests in attempts 08/15.
- Attempt 09: Pester's registry/environment access was denied; its null result is not a pass even though the first evidence runner returned zero. The runner now treats missing/incomplete Pester results as failure.
- Attempts 10/11: a mock scoping error and failure to intercept the fully qualified Python path are retained. At 16:53:26Z, a test reached actual preparation and reserved a slot; it stopped on configuration drift with zero native preflight invocations. The latch and stop are preserved. No source collector, native preflight or Codex worker ran in that stopped invocation.
- Attempts 12/13/16: explicit function mocking repaired test isolation; a singleton-array assertion in the test was corrected without changing literal argument behavior. The final PowerShell suite passes, including a separate synthetic external-process case.
- Attempts 14/15: a focused red/green check covers preserving a zero-dispatch preparation stop while retaining the one-native-dispatch limit. The optional resumed selection remains inactive pending review.

These harness observations do not establish the cause of the historical Codex exit. QA-LOG-01/02 retain the earlier independent QA disposition; this work does not reopen or self-close them.

## Continuation after the decision

If Bryan approves this specific proposal, record his actual approval in a fresh selection file. Recollect current sources, verify that only the two documented differences remain, bind that selection and the preserved zero-dispatch stop into the active preparation configuration, refresh its runtime seal, and execute the two live readiness checks. Preserve the former active configuration and seal. Any further source difference requires review; do not restore source or silently relax a check.

Once those checks pass, supply the concrete root PowerShell command for Bryan's separate-console run. Keep the exact QA probe and native worker, gpt-6-astra/high, debug/closed-v1, four false findings, v3 compiled policy, child-only ANTHROPIC_API_KEY omission, one preflight, zero retries, no model task, and 120/145-second bounds. After Bryan's run, use the selected Rust inspector across all evidence pages, recheck preservation, and assess OW-04/OW-05 without claiming a cause beyond the records.

PowerShell requires the call operator `&` before a quoted executable path. The record_powershell_checks.py command shown during testing is a single-use evidence runner, not the operator's native diagnostic command.
