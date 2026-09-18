# QA failure handoff — F-01, F-02 and M-01

## Candidate, contracts and ownership

QA verdict FAIL. Source `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe`. Frozen manifest `C:\Projects\DevForgeAI\docs\plan\framework-worker-qa\20260915T1800141514833Z\selected-manifest.json`, SHA-256 `177b5894a236a02c7d322df7f04d647632094a4a3f3998e7f2a150db246e1604`. Governing specification `C:\Projects\DevForgeAI\docs\specs\framework\runtime\codex-worker-feasibility-v1.md`, DFF-WORKER-FEAS-01 v1.0.0, SHA-256 `7cb5b0cb87e515bb4d59235b615922ab4ea07ef607b8111dde6cc73c8f101b23`. Read current AGENTS.md. Windows 11 Pro x64, PowerShell 7.6.6, Rust/Cargo 1.97.1 on C: NTFS. Report `C:\Projects\DevForgeAI\docs\plan\framework-worker-qa\20260915T1800141514833Z\qa-report.md`; exact report/fix/input hashes in `C:\Projects\DevForgeAI\docs\plan\framework-worker-qa\20260915T1800141514833Z\handoff-manifest.json` entries report/fix/specification.

Dev is the remediation owner. This packet proposes the next bounded development selection; it does not itself authorize QA to repair, change operational copies, amend native identity rules, inspect live profiles, run Codex, install or deploy. Preserve all prior evidence and unrelated bytes. No historical independent finding is closed.

## F-01 — Blocking write prevents deadline/cancel handling

- State OPEN; high severity; MANDATORY_PRODUCT_DEFECT. Contract sections 4–6 and IQ-02. Complete reproduction in qa-report.md and two independent-attempts/IQ-02-* directories.
- Application ownership: src/process_windows.rs::OwnedProcess::send (283–291), src/protocol.rs::Session::receive/rpc/interrupt (98/148/452 onward).
- Real peer emits 262,144-character string request ID, then does not read stdin. Injected total/RPC/grace/teardown are 750/500/200/500 ms; cancellation variant sets control at 300 ms. Expected bounded failure/timeout/cancel with stopped tree. Both still active at 3s, no terminal, requiring supervisor termination. Peer handle signals after that; no orphan after containment.
- Root cause demonstrated by source and stimulus: synchronous write on the control/deadline thread. Restore bounded write cancellation and verified termination for server replies, normal RPC and interrupt. Do not merely enlarge deadlines, drop the case or label the external kill a timeout pass.
- Original reproduction command from C:\Projects\DevForgeAI: `python -B -X utf8 docs/plan/framework-worker-qa/20260915T1800141514833Z/independent_run.py backpressure`. It is intentionally one-shot and now refuses existing attempt directories. For an authorized development Red/retest, copy the QA-only scripts and independent fixture project into a fresh sibling timestamped evidence root, preserving relative directory depth, build with independent_run.py build, then use the backpressure mode there. Verify helper/oracle bytes and candidate drift before execution; do not overwrite this run. The selected tests are data/OS observations and never authorize native Codex.
- Regression/retest: both deadline and cancellation full-pipe cases, real child/descendant handles, outbound interruption under backpressure, unchanged fixtures, deterministic terminal semantics; then affected WF-01..20, required supplemental cases and fresh all-src coverage. No automatic native trial.

## F-02 — Unknown structured error copied into retained evidence

- State OPEN; high severity, CRITICAL_PRODUCT_DEFECT under QA's security-invariant stop rule. This classification is not an observed real credential disclosure or CVSS rating.
- Contract sections 5,7; captured TurnCompletedNotification.json:54 CodexErrorInfo; IQ-05.
- Application source src/protocol.rs:419 copies untyped turn.error.codexErrorInfo to persisted/emitted error_category.
- Independent fixture: failed turn with codexErrorInfo={unexpectedPrivateField: QA_PRIVATE_SENTINEL_7159}. Expected schema rejection or sanitized summary before persistence/emission. Actual marker in run/journal.jsonl and stdout.txt, exit4/provider_failed. No real secrets involved. Peer termination verified.
- Original one-shot command: `python -B -X utf8 docs/plan/framework-worker-qa/20260915T1800141514833Z/independent_run.py privacy`; authorized reproductions require a fresh sibling evidence root as above. Evidence independent-attempts/IQ-05-private-error/.
- Restore typed error validation/sanitization before append/emit. Preserve legitimate categories and approved numeric details. Review analogous error_code retention at protocol.rs:165 as related risk, explicitly untested here. Add content-level negative controls with synthetic private markers in malformed/unknown nested error fields and verify absence from journal/stdout/diagnostics; current usage-only sanitizer tests do not prove this boundary.
- Retest must independently check exact source/binary identities, field typing, permitted category retention, negative controls and affected protocol/inspection regression. Do not self-issue QA closure.

## M-01 — Whole declared QA suite 24/26 below 95%

Both product findings explain the missing passes; restore actual behavior. No denominator inflation, threshold relaxation, replacement oracle or suppression is permitted. The frozen 20 WF cases passed their original subfixtures, but do not waive the two extra requirement failures. All-src coverage 1311/1374 (95.41484716157206%) and declared unit cases 6/6 passed before the stop; recollect after changed runtime bytes. Keep branch coverage limitations explicit.

## Stop and return contract

No further tests ran after F-02. All 26 declared offline groups reached outcomes; WN-01/WN-02 remain NOT_RUN and unselected. All owned children observed stopped, no cleanup deletion, every attempt retained. Launcher reparse identity and reviewed Pro profile remain separate owner decisions, not fixes authorized by this packet.

Return corrected candidate/build manifest, changed-file list, per-defect correction/evidence map, Red/Green/refactor results, fresh mandatory/supplemental/unit outcomes and coverage numerator/denominator/raw profiles, explicit gaps and a separate independent QA retest handoff. Only independently executed retest can close F-01/F-02. Framework acceptance remains NOT_EVALUATED.

## Copyable next assignment

Current host catalog exposes dev. Paste this into the native Windows Codex conversation only when selecting remediation:

```text
Use $dev in C:\Projects\DevForgeAI on native Windows to remediate only F-01 and F-02 in devforgeai/experiments/codex-worker-probe, then reestablish M-01 through meaningful regression checks.
Read AGENTS.md, C:\Projects\DevForgeAI\docs\specs\framework\runtime\codex-worker-feasibility-v1.md, C:\Projects\DevForgeAI\docs\plan\framework-worker-qa\20260915T1800141514833Z\qa-report.md, and C:\Projects\DevForgeAI\docs\plan\framework-worker-qa\20260915T1800141514833Z\qa-fix.md. Verify their bytes using the report, fix and specification entries in C:\Projects\DevForgeAI\docs\plan\framework-worker-qa\20260915T1800141514833Z\handoff-manifest.json before editing. Failed candidate: C:\Projects\DevForgeAI\docs\plan\framework-worker-qa\20260915T1800141514833Z\selected-manifest.json, SHA-256 177b5894a236a02c7d322df7f04d647632094a4a3f3998e7f2a150db246e1604. Verify current source against it; report drift without restoring old bytes.
Follow red -> green -> refactor -> QA. Preserve production behavior, original tests, unrelated files and every prior attempt; add meaningful regression coverage for blocked pipe writes and untyped error-payload retention. Preserve the selected 20-case inventory, all required subfixtures and >=95% coverage/pass-rate floors. Do not alter the index workspace, operational copies, launcher-identity contract or live Pro profile; do not launch Codex, install, deploy or issue framework acceptance.
Return corrected source/build identities, changed-file manifest, per-defect correction/evidence map and fresh raw regression/coverage results. Do not self-close these QA findings; a separately selected independent retest must verify closure.
```
