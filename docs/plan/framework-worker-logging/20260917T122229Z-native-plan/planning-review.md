# Planning verification and custody record

This task produced a diagnostic plan, operator worksheet, deliberately incomplete request/review templates, exact task/config bytes, bounded command descriptions and a separately selectable native-trial prompt. It made no product or operational changes. Native Codex, Rust source-inventory execution, operator findings and new native qualification remain unperformed. Framework acceptance is `NOT_EVALUATED`.

## Executed checks

All commands ran in `C:\Projects\DevForgeAI` using `C:\Program Files\PowerShell\7\pwsh.exe` (7.6.6), native Windows x64, NT 10.0.26200.0 and C: NTFS. No Git metadata is present. The executed supporting commands were:

```powershell
& 'C:\Projects\DevForgeAI\docs\plan\framework-worker-logging\20260917T122229Z-native-plan\collect-planning-evidence.ps1' -Phase intake
& 'C:\Projects\DevForgeAI\docs\plan\framework-worker-logging\20260917T122229Z-native-plan\collect-planning-evidence-v2.ps1' -Phase intake
& 'C:\Projects\DevForgeAI\docs\plan\framework-worker-logging\20260917T122229Z-native-plan\prepare-planning-inputs.ps1'
& 'C:\Projects\DevForgeAI\docs\plan\framework-worker-logging\20260917T122229Z-native-plan\verify-planning-documents.ps1'
& 'C:\Projects\DevForgeAI\docs\plan\framework-worker-logging\20260917T122229Z-native-plan\collect-planning-evidence-v2.ps1' -Phase readback
```

| Check | Actual result and retained evidence |
| --- | --- |
| Initial preservation collector | Exit 1; file bytes matched, but five reparse display-prefix comparisons falsely reported drift. [Original receipt](intake-verification.json) and original collector retained. See PLAN-H01 below. |
| Corrected preservation intake | Exit 0, 21,535 unique file identities checked, no mismatch. [Intake](intake-v2-verification.json). |
| Planning input preparation | Exit 0; five task/config/template/command files created and indexed by [input manifest](planning-input-manifest.json). No future trial root created. |
| Documentation consistency | Exit 0; 15 checks passed, including 27 local Markdown links, exact task/config hashes, declared template fields, deliberate unresolved placeholders, fixed policy/probe identities and command/deadline consistency. [Checks](planning-checks.json). No runtime admission test is claimed. |
| Preservation after preparation | Exit 0, 21,535 unique identities checked, no mismatch and future trial root still absent. [Readback](readback-v2-verification.json). |

The preservation groups include all 39 QA handoff entries, 68 candidate files, eight specifications, 108 QA inputs, 183 failed/original/snapshot source files, 7,672 current QA evidence files and 92 executable bindings, 9,691 development evidence files, and 3,689 prior QA evidence files and 90 executable bindings. Groups overlap; 21,535 is the de-duplicated collector count, not a test denominator. Five retained evidence junctions were observed without traversal. Native executable and two launcher/one plugin junction display targets also match the compiled records. Raw Windows reparse tags and full live source completeness remain for unchanged Rust to verify during separately selected preparation/execution.

Root AGENTS.md and `Start-CodexAppServerDiagnostic.ps1` match their QA-bound bytes. The helper SHA256 is `f69da72fb44737127dcfde3607fb0e027e4afeb2463a78ac8f844bc3abfc58a0`. The checked preservation scope is explicit in the receipts; it excludes unindexed build intermediates and makes no full-repository snapshot claim. All task writes are confined to this fresh planning directory. No prior evidence was repaired or overwritten.

## PLAN-H01: evidence checker display mismatch

The original collector compared PowerShell `Target` strings directly with targets recorded by the earlier Python evidence collector. For five retained synthetic junctions, the older records have a leading `\\?\`; PowerShell displays the same target without it. All underlying regular-file hashes matched. The literal target readback established this representational difference, not a candidate or retained-evidence change.

The v2 collector removes only the four-character extended-path display prefix for this comparison, preserves both observed strings, still requires the reparse attribute and exact remaining target, and never resolves/traverses/modifies the junction. The original script/receipt remain. Corrected intake and final preservation both passed. This is a resolved planning-recorder issue, not a reopened or self-closed product QA finding. No repeated native attempt occurred.

## Factual review against current source

The current `src/request.rs` defines Request fields at lines 15-36 and ReviewV2 at 116-129; review validation at 341-447 distinguishes false-allowed preflight findings from work qualification. Lines 524-566 require a nonexistent sibling run directory and the exact native trial layout. The templates use these field names with explicit null placeholders for unknown strings/booleans/file bindings; they are intentionally invalid runtime requests until separately finalized.

`src/main.rs` supplies the selected `profile-sources`, `preflight` and `inspect` command shapes; `src/runner.rs` lines 25-28 retain the 120/10/5/5-second bounds and line 99 defines the guarded environment names. `src/profile_sources.rs` lines 113-134 derive roots; lines 284-310 enumerate source families. `src/launch_policy.rs` and its compiled JSON fix the v3 policy, 116 arguments and 35 required feature disables.

`src/capture.rs` lines 14-17 establish stream/detail/classifier limits, and lines 32-45 define the actual emitted classifier categories and narrow patterns. `src/logging.rs` fixes diagnostics at 512 events/1 MiB. `src/journal.rs` lines 363-450 validate mandatory capture/exit evidence and the complete-success requirements while retaining legitimate failed-run behavior; lines 519-523 define inspection pagination. The plan uses these observed interfaces and the eight sealed companion contracts. No newer online behavior or unverified installed CLI command was substituted.

The offline QA metrics and VERIFIED_FIXED lifecycle are reused from the sealed independent QA report, with their candidate/build bindings intact. No new build, Clippy, formatting, regression, coverage, sandbox qualification, native run or framework acceptance is claimed for prose planning. The 15 documentation checks do not replace the 178-case independent QA denominator.

## Unresolved prerequisites

Separate trial selection and model/effort confirmation, named operator review, fresh compiled source inventory for the proposed fixture, finalized review/request hashes, child-only environment selection, and a reviewed/tested evidence supervisor remain pending. The one-attempt diagnostic must establish its own current startup, effective profile, account/model, capture and cleanup observations. Neither an inventory digest nor a prior offline PASS fills those gaps. Use the [next trial prompt](next-native-trial-prompt.txt) only as a new selection.
