# Outstanding Rust worker diagnostic work

Status checked: **2026-09-17**, using native Windows PowerShell 7.6.6 in `C:\Projects\DevForgeAI`.

**The logging implementation and independent offline QA are complete. The corrected candidate's native diagnostic has not run, and the original Codex worker's exit cause remains unresolved.** This document records the five remaining items, their dependencies, and the evidence needed to finish them. Writing this document does not execute those items or issue framework acceptance.

## 1. Origin, scope, and current evidence

The project starting point identified by Bryan is [DEVFORGEAI-INDEX-QUERY-001](devforgeai-index-query-cli-spec.md), which extends and depends on the [index service MVP specification](devforgeai-index-service-mvp-spec.md). Those contracts define the Rust index application and query CLI. This document does not audit all of their requirements or declare the index application complete.

The later [framework MVP handoff](framework-mvp-next-session.md) records the selection of [DFF-WORKER-FEAS-01](../specs/framework/runtime/codex-worker-feasibility-v1.md), a bounded worker experiment. The current diagnostic belongs to that runtime work. The [compiled-Rust enforcement design](devforgeai-codex-rust-enforcement-design.md) defines a separate authority boundary; neither a working index CLI nor a successful worker diagnostic establishes protected framework acceptance.

The [September 16 investigation](framework-worker-startup-investigation/20260916T204555Z/investigation-report.md) and [logging design](framework-worker-startup-investigation/20260916T204555Z/logging-design.md) describe the earlier startup blind spot and proposed repairs. Their historical `NOT_IMPLEMENTED` statements must remain intact. The later [logging contract](../../devforgeai/experiments/codex-worker-probe-logging-qa-fixes/logging-contract.md) and [September 17 independent QA report](framework-worker-logging/20260917T105456Z-qa-retest/qa-report.md) establish the current implementation and offline assessment.

| Area | Verified starting point |
| --- | --- |
| Selected source | `devforgeai/experiments/codex-worker-probe-logging-qa-fixes`; all 68 files match the QA candidate manifest. |
| Logging and capture | Startup capture independent of protocol receive; pre/post-stop exit observations; bounded stream draining; EOF/error/overflow/completeness evidence; `off`, `minimal`, `verbose`, and `debug` levels are implemented. |
| Selected defect retest | QA-LOG-01 and QA-LOG-02 are independently `VERIFIED_FIXED`. Their closure is inherited from QA, not issued by this document. |
| Offline quality | 178/178 required cases, including 49/49 units; executed-line coverage 3,872/4,057 = 95.4399802809958%; build, formatting, and Clippy passed in the retained QA run. |
| Existing evidence recorder | Its unchanged source matches the retained offline result: 17/17 cases, 73/73 executable lines, and 10/10 branches. This does not qualify future wrapper changes. |
| Native selection | Bryan approved the input decisions and selected one native diagnostic. Final current-source execution inputs are not ready. |
| Current preparation failure | The wrapper still checks a 29-file inventory containing removed curated Sites files. A newer 26-file inventory and draft review exist, but the wrapper does not use them. |
| Latest source observation | All 26 proposed file bindings matched at this document's check. Bundled Sites 0.1.70 is present; the separate curated Sites 0.1.65 directory is absent. These are dated observations, not fixed-version requirements. |
| Corrected-candidate native result | `NOT_RUN`: no final runtime-input directory, prelaunch-inventory directory, launch reservation, native-attempt directory, Rust run directory, or native result exists for this selected attempt. |
| Original worker exit | Exit 1 before initialize remains unexplained by the retained original evidence. The later cleanup did not cause the already-observed exit. |
| Framework acceptance | `NOT_EVALUATED`. Broader native workflow qualification remains separate work. |

The current preparation limitation is evidenced by the [execution wrapper](framework-worker-trials/20260917T122229Z-logging-diagnostic/native-execution-001/execute_once.py), [stopped preparation receipt](framework-worker-trials/20260917T122229Z-logging-diagnostic/native-execution-001/execution-stop-002.json), [newer draft review](framework-worker-trials/20260917T122229Z-logging-diagnostic/native-execution-001/source-review-002/review.proposed.json), and [Sites documentation update](framework-worker-trials/20260917T122229Z-logging-diagnostic/native-execution-001/sites-version-update.md). The draft review's reviewer is still null; do not portray it as finalized runtime input.

### Approval chronology and identities

The [approved input summary](framework-worker-trials/20260917T122229Z-logging-diagnostic/inputs-002-reviewed/approval-summary.md) records Bryan's D1-D3 decisions. It predates native selection, so its original selection-pending language is historical. The later [native selection record](framework-worker-trials/20260917T122229Z-logging-diagnostic/native-execution-001/selection-final.md) records the one-run instruction, approval of the then-current 29-file source set, and the exact host permission-rule addition. The [subsequent source review](framework-worker-trials/20260917T122229Z-logging-diagnostic/native-execution-001/source-review-002/drift-report.md) records the additional removal of curated Sites. The later request to document Sites 0.1.70 did not finalize that draft or update the wrapper.

Preserve those decisions. Do not ask again for the same model, environment treatment, or single-run selection. Finalizing the refreshed source review must reflect actual user instructions; ask only about a material difference not already covered. Neither this status document nor routine plugin updates automatically approve future changed sources.

The six selected handoff seals and their direct entries were rechecked for this document. The most important execution identities are:

| Identity | SHA256 |
| --- | --- |
| [Independent QA handoff](framework-worker-logging/20260917T105456Z-qa-retest/handoff-manifest.json) | `4ac2a9de0392e967fe65c64d782b06563cc11bd9171386b02651d4a6a545fbeb` |
| [Native diagnostic plan handoff](framework-worker-logging/20260917T122229Z-native-plan/handoff-manifest.json) | `a0341ae9f2b8431b0c8acf5e402d6c2c38f879ce5adbdff63b5fb1a0fd852891` |
| [QA candidate manifest](framework-worker-logging/20260917T105456Z-qa-retest/candidate-manifest.json) | `44dcb32397b479506ae84b85fa536f40f4bf5234a7647c4e86d160507926761d` |
| [QA-built Rust probe](framework-worker-logging/20260917T105456Z-qa-retest/build-target/debug/devforgeai-codex-worker-probe.exe) | `cdd7de15eece11ad4c6f8b910ddca947bcc0ca0e98cd1ed939e61ddd73975bcd` |
| [Proposed 26-file source review handoff](framework-worker-trials/20260917T122229Z-logging-diagnostic/native-execution-001/source-review-002/handoff-manifest.json) | `b69f1560dd87b23dbf0fe032c0c91d7896536c24d74d5cf2bdbc16d6035e0fa3` |

Use the QA-built executable without rebuilding or substituting another candidate. Its full path is `C:\Projects\DevForgeAI\docs\plan\framework-worker-logging\20260917T105456Z-qa-retest\build-target\debug\devforgeai-codex-worker-probe.exe`. The [bound specifications](framework-worker-logging/20260917T105456Z-qa-retest/specification-bindings.json) and [native diagnostic plan](framework-worker-logging/20260917T122229Z-native-plan/native-diagnostic-plan.md) supply the detailed contracts.

### What the existing scripts do

| Script/resource | Role and limitation |
| --- | --- |
| [Start-CodexAppServerDiagnostic.ps1](../../Start-CodexAppServerDiagnostic.ps1) | Manual console launcher for pinned Codex, with 15 CLI key-quoting corrections. Displays worker startup output directly, but does not run the corrected Rust probe, its Job Object/preflight checks, or its logging inspection. Preserve it. |
| [advisor-test.ps1](../../advisor-test.ps1) | Launches Claude to review the retained environment-blocker briefing. It is an advisor diagnostic, not a Codex-worker preflight. Preserve it. |
| [Test-NativeDiagnosticPreparation.ps1](../../Test-NativeDiagnosticPreparation.ps1) | Calls only the wrapper's read-only preparation check and exposes its traceback/exit code. It does not execute Rust preflight or native Codex. |
| [Existing recorder and test evidence](framework-worker-trials/20260917T122229Z-logging-diagnostic/recorder-checks/final-evidence.json) | Tested bounded process/output recording support to reuse for the future PowerShell entrypoint. Compiled Rust retains admission, launch policy, worker containment, and inspection. |

Earlier manual console diagnostics are not erased by the corrected candidate's `NOT_RUN` status. Conversely, console output from a direct Codex launch does not qualify the unexecuted corrected Rust preflight. The proposed PowerShell harness must display probe output and progress within the selected redaction contract. It must not promise to expose arbitrary child stderr that Rust deliberately excludes; direct-console or raw forensic capture is a distinct evidence path.

## 2. Five outstanding items

The dependency order is **OW-01 -> OW-02 -> OW-03 -> OW-04 -> OW-05**. OW-01 and offline harness development may overlap, but both must be ready before native execution. No item is completed merely by writing this document.

### OW-01 — Refresh and finalize preparation inputs

**State:** blocked by stale execution bindings. **Responsible:** implementing agent; Bryan for any uncovered material source-review decision.

Inspect the current wrapper and stopped receipts before changing anything. Preserve the stopped executor versions, original and newer inventories, sealed handoffs, failed/corrected candidates, frozen snapshots, and prior evidence. Write new input/executor evidence versions; never overwrite an earlier stop receipt or rerun the stale wrapper unchanged.

Collect a fresh schema-2 inventory with the selected Rust probe. Discover actual installed versions and paths rather than replacing every historical `0.1.65` string with `0.1.70`. Compare the observation with the attributed review, record material differences, and finalize the source review and schema-3 request with exact-byte hashes. The newer 26-file proposal is a starting point, not permission to omit changed files or directory-membership checks.

A collection performed inside one host permission context cannot automatically qualify a different operator console. Recollect immediately before launch under the actual execution context and child environment, including after a host permission change. Preserve valid existing approvals; record any newly required source-review decision concretely.

**Required output and completion evidence:** new inventory, source comparison, attributed review, diagnostics/request bindings and input manifest; successful preservation/consistency checks; no dependency on a removed live file; and a run-time recheck that stops on uncovered drift. Missing or changed protected candidate/build bytes require reporting, not restoration or substitution.

### OW-02 — Prepare the operator-run PowerShell harness

**State:** not ready; the recorder exists, but the root preparation script is not a native execution harness. **Responsible:** implementing agent.

Provide a native Windows PowerShell entrypoint for the exact QA-built Rust `preflight --request` operation. Reuse the reviewed recorder's bounded capture and ownership behavior. Preserve the existing console/advisor/preparation helpers. Clearly separate preparation-only behavior from explicit single-run dispatch, and deliver one concrete operator command only when its files and bindings exist.

Show the executable and request identities, current stage, elapsed progress and approved probe output. Retain exact stdout/stderr bytes and receipts independently of console rendering. Label preparation failure, probe failure, worker failure, timeout, and cleanup uncertainty distinctly. Keep probe stdin open during normal execution; an empty pipe or closed stdin can request cancellation. Do not tap worker pipes, print credential values, or bypass the Rust process guard to obtain more output.

**Required output and completion evidence:** the runnable PowerShell entrypoint, exact operator command, new source/change identities, and retained red -> green -> refactor/offline verification for behavior changes. Cover literal argument handling, stale/missing inputs, no-launch preparation, both output streams, stdin lifetime, nonzero exits, cancellation/timeout, owned-process cleanup, and prevention of repeated dispatch. Apply the repository's >=95% executed-line coverage and >=95% required-case pass-rate requirements to the declared changed executable scope; retain denominators and failures. The old recorder's 17/17 result cannot qualify modified bytes by itself. Native Codex is not a fixture for these offline checks.

### OW-03 — Run the one selected native diagnostic

**State:** not run for the corrected candidate. **Responsible:** Bryan, using the completed harness in a separate console. **Prerequisites:** OW-01 and OW-02 complete, with current source review and intact selected identities.

Carry forward `gpt-6-astra` / `high`, `debug` / `closed-v1`, the fixed v3 compiled launch policy, and all four operator findings false/unqualified for model work. Omit only `ANTHROPIC_API_KEY` from a child environment copy. Leave the parent environment and saved configuration unchanged; other guarded credential/provider names or alternate `CODEX_HOME` retain their stopping behavior.

Use one preflight, zero automatic retries, no model task, no thread/turn, and no increase in limits. Retain the 120-second Rust total and 145-second recorder budget, including cancellation/containment/finalization; the existing plan specifies the 135-second recorder cancellation point and remaining reserves. Keep the selected fixture and fresh runtime layout. A failed native attempt is still consumed.

**Required output and completion evidence:** exact command/cwd, executable and input hashes, stage and timing receipts, raw probe stdout/stderr, Rust journal/optional diagnostic records when created, process exit/timeout information, and cleanup observations. Evidence collection is complete only when the attempt's actual outcome and remaining uncertainties are recorded; success is not assumed. If it times out, preserve the attempt and provide Bryan the exact command and cleanup/input prerequisites for a separately selected console reproduction. Do not silently rerun or reuse an occupied run directory.

### OW-04 — Inspect and reconcile the resulting records

**State:** not run; depends on OW-03. **Responsible:** evidence-reviewing agent using the selected compiled Rust inspector.

Inspect the immutable run across all pages, retaining each command, output and exit receipt. Check terminal/startup outcome, stdout/stderr totals and hashes, EOF/read errors/overflow/drain completeness, pre/post-stop exit observations, mandatory exit-code consistency, optional diagnostic integrity, and stopped-tree evidence. Capture an after-run source inventory and recheck the selected protected files and fixture.

**Required output and completion evidence:** a report that distinguishes successful preflight, an internally valid failed run, and incomplete/inconsistent evidence. `inspect` exit 0 for a legitimate failed run does not mean startup succeeded. Missing run/terminal evidence, timeout or unknown cleanup must be reported explicitly; do not repair the journal, reinterpret historical schemas as current capture, or report preservation beyond the scope actually checked.

### OW-05 — Assess the cause and select any follow-up

**State:** unresolved; depends on OW-04. **Responsible:** evidence-reviewing agent; development and independent QA remain separate roles if a new repair is selected.

Separate observations, supported conclusions, and hypotheses. The current classifier's configuration categories are narrow recognized message patterns, not proof of the original run's cause. Its unclassified result is legitimate, and the original discarded pipe text cannot be recovered from the retained original artifacts.

| New evidence | Required disposition |
| --- | --- |
| Supported product defect | Describe a reproducible defect and affected contract, then hand off a scoped repair with red/green/refactor evidence and independent QA against changed bytes. Do not rebuild and reuse the old candidate's QA result or automatically invoke QA. |
| Configuration category or other startup failure without a proven product defect | Report the observed category, code, stage and limits; identify the next targeted check. Do not speculatively alter installed configuration or authentication. |
| Unclassified, incomplete or cleanup-uncertain failure | Preserve the failure and name the missing evidence and bounded next action. Do not invent a root cause or claim complete diagnosis. |
| Successful corrected-candidate startup | Record success for this attempt while leaving the historical exit unresolved unless additional evidence supports a causal conclusion. |

**Required output and completion evidence:** an evidence-backed conclusion or explicit unresolved disposition, with remaining questions and any separately selectable follow-up. Completion of this assessment does not require claiming the unknowable original cause is solved. No logging finding is reopened or self-closed without new evidence; broader native workflow qualification and framework acceptance remain separate.

## 3. Copyable continuation request for OW-01 and OW-02

```text
Work in C:\Projects\DevForgeAI using native Windows PowerShell. Read current AGENTS.md and docs\plan\framework-worker-diagnostic-outstanding-work.md.

Implement only OW-01 and OW-02: refresh/finalize the diagnostic preparation inputs and prepare a tested operator-run PowerShell entrypoint for the corrected Rust probe. Do not launch native Codex during this task. Return the concrete command for Bryan to run in a separate console after the inputs and harness are ready.

Verify the linked QA handoff (SHA256 4ac2a9de0392e967fe65c64d782b06563cc11bd9171386b02651d4a6a545fbeb), native planning handoff (SHA256 a0341ae9f2b8431b0c8acf5e402d6c2c38f879ce5adbdff63b5fb1a0fd852891), current AGENTS.md, selected candidate/build/specifications, approval chronology, and stopped preparation evidence. Report material drift before editing; do not restore old source. Use the existing QA-built probe without rebuilding it.

Preserve the previous executor/input versions, all sealed evidence, candidates and snapshots, existing PowerShell helpers, unrelated files and operational configuration. Discover current plugin versions; do not treat Sites 0.1.70 as a permanent requirement. Attribute the finalized source review to actual instructions. Preserve already-recorded approvals and ask only about new material differences not covered by them.

Reuse the reviewed evidence recorder and retain Rust ownership of admission, policy, worker containment and inspection. Preserve the selected model/effort, child-only environment treatment, four false findings, logging redaction, one-attempt/no-retry limits and 120/145-second bounds. Make preparation failures, probe outcomes and worker outcomes understandable in the console while retaining exact probe outputs and receipts. Do not replace the Rust preflight with the direct Codex console helper.

Follow red -> green -> refactor and applicable offline regression/negative-path/coverage checks for behavior changes. Retain the >=95% line-coverage and required-case pass-rate denominators and evidence. Do not count historical tests as fresh verification of modified code, launch native Codex as a test, install/deploy, change configuration, automatically invoke QA, self-close findings or issue framework acceptance.

Return changed-file/source identities, fresh executed test evidence, the new input bindings, and one ready-to-run PowerShell command with output locations and limits. If a material source-review decision remains, present its concrete file/behavior difference and withhold native dispatch. OW-03 is the operator's run; OW-04 and OW-05 follow its retained evidence.
```

## 4. Documentation verification and update rules

The [documentation verification receipt](framework-worker-logging/20260917T160006Z-outstanding-work-docs/verification.json) records the exact checks, outcomes, document hash, local links and before/after preservation bindings. The check scope is six handoff seals and their direct entries, the selected QA source/specification/build manifests, existing recorder evidence, relevant scripts, and originating documents. It is not a whole-repository snapshot or a rerun of all prior artifact trees.

This update adds documentation and its verification receipt only. No red/green execution, runtime coverage, native result or framework acceptance is claimed for prose. Future updates must date their observations, link the specific new evidence, and distinguish completed implementation, offline QA, native execution, inspection, and causal diagnosis. Preserve historical evidence instead of changing its old statuses to make them appear current.
