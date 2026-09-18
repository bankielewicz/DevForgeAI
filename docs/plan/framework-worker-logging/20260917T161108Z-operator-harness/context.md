# Operator harness implementation context

Recorded 2026-09-17. Workspace: `C:\Projects\DevForgeAI`, native Windows PowerShell 7.6.6, Python 3.10.11, coverage.py 7.9.0, Pester 5.7.1 available. Git metadata is absent. No selected Rust probe process was running at intake.

## Selection and output destinations

The active user request is to proceed with `docs/plan/framework-worker-diagnostic-outstanding-work.md` and its five items. Its continuation selects preparation and harness implementation first; Bryan runs the native diagnostic in a separate console. Inspection and causal assessment remain pending that evidence. This implementation must not launch native Codex, including help/version. A read-only Rust `profile-sources` command is permitted preparation and cannot start Codex.

- selected_evidence_value: `C:\Projects\DevForgeAI\docs\plan\framework-worker-logging\20260917T161108Z-operator-harness`
- selection_source: the established fresh per-run `docs/plan/framework-worker-logging` evidence location, selected under the dev skill context reference and OW-01/OW-02's evidence-preservation requirements.
- resolved_evidence_root: identical to selected_evidence_value; native Windows separators only. All components were checked before first write; the directory was absent.
- Product support source: `C:\Projects\DevForgeAI\docs\plan\framework-worker-trials\20260917T122229Z-logging-diagnostic\operator-harness-001` (new; checked absent).
- Operator entrypoint: `C:\Projects\DevForgeAI\Invoke-CodexWorkerDiagnostic.ps1` (new; checked absent).
- Context, traceability, attempts, tests, checkpoint and delivery records stay below the selected evidence root. No previous executor, helper, candidate or sealed record is edited.

## Exact inputs and current observations

| Input | SHA256 / evidence |
| --- | --- |
| Root AGENTS.md | `3b8e2a112c438b536ab59db2abbcfd6e08ebdd7f41caa13cdf6d5c49866fab86` |
| Selected outstanding-work document | `98f8e0b7673da56704076dcd3b08a592414a097b67e086c6d3e211357fd94495` |
| Its documentation verification receipt | `6df48d8da211ea38e2647351895de6079f838d43eec5a077cbc4fa954c1da785` |
| QA handoff | `4ac2a9de0392e967fe65c64d782b06563cc11bd9171386b02651d4a6a545fbeb` |
| Native planning handoff | `a0341ae9f2b8431b0c8acf5e402d6c2c38f879ce5adbdff63b5fb1a0fd852891` |
| QA-built probe | `cdd7de15eece11ad4c6f8b910ddca947bcc0ca0e98cd1ed939e61ddd73975bcd` |
| Proposed 26-file source review handoff | `b69f1560dd87b23dbf0fe032c0c91d7896536c24d74d5cf2bdbc16d6035e0fa3` |
| Retained recorder supervisor.py | `bace72fafe66f9cd3b44afffc06bbc660a06a4419f86a919fd5e2fa247363990` |

At 2026-09-17T16:13:10Z, all 393 scoped bindings in the documentation receipt matched and all 26 proposed installed-file bindings matched. No material drift was found in that checked scope. The old executor still requires its 29-file inventory. The newer proposal is not yet wired into executable preparation. The selected runtime run/input/attempt/latch paths remain absent. Intake is a scoped comparison, not a whole-repository snapshot.

Bryan's D1-D3 approval, name and one-run selection persist. The user subsequently selected this continuation with the documented current inventory and stale-binding defect in view. Record that attribution with the refreshed inputs; do not re-ask unchanged model/environment/run choices. No future source drift is pre-approved. The operator command must re-collect under its actual context and stop if the source inventory differs.

## Decisions, reuse and slices

1. OW-01: preserve the old executor and write a new preparation module. Verify immutable evidence separately from currently reviewed installed sources so removal of a historical cache file does not make preservation require its restoration. Use the selected compiled `profile-sources` collector, exact raw inventory hashes, attributed source review and schema-3 request. Keep the fixture and selected Rust binary unchanged.
2. OW-02: compose the unchanged tested Python recorder with a new thin PowerShell entrypoint. Default invocation prepares/checks only; `-RunOnce` is the explicit operator dispatch mode. Python remains evidence support; compiled Rust owns admission, policy, worker containment and inspection. New support functions must retain receipt/output bytes and show progress without diagnostic backpressure delaying the recorder.
3. Keep all native process limits and restrictions: 120-second Rust total, 145-second recorder budget, cancellation at 135 seconds, one attempt, zero automatic retries, no thread/turn/model work, `gpt-6-astra/high`, `debug/closed-v1`, fixed v3 policy, four false findings, child-only omission of ANTHROPIC_API_KEY and stop on other guarded names. No raw worker pipe capture or operational configuration changes.
4. Fresh source capture/preparation may run here. Native execution remains Bryan's console step. The harness must prevent occupied-run replay, preserve every stop, and distinguish preparation, probe, worker and cleanup outcomes. Existing helper/advisor/preparation scripts remain untouched.

The existing recorder already implements literal argv, held stdin, output files, bounded cancellation, live-handle termination and receipts; reuse it. The old executor mixes immutable preservation with obsolete installed paths and cannot be reused unchanged. The direct Codex console helper bypasses the corrected Rust probe; preserve it instead of extending it into this path.

## Verification and denominator

Retain an executed red reproduction against the old executor before new preparation behavior. Continue with meaningful isolated tests and real synthetic child processes; installed Codex must never be an offline fixture. Cover stale/changed/missing bindings, exact source comparison and request rebinding, no-launch preparation, literal arguments, live output/progress, both captured streams, stdin lifetime, nonzero exits, timeout/cancellation/cleanup uncertainty and one-attempt replay protection.

Required platform: native Windows. Runtime source denominator will include every executable line of the new Python support modules, the unchanged recorder used by the operator path and the new PowerShell entrypoint; no uncovered runtime branch is excluded. Tests, synthetic fixtures and evidence-only test runners are excluded as test infrastructure. Use coverage.py for Python and Pester executed-line coverage for PowerShell, report them separately and combined, and require >=95% line coverage and >=95% required-case pass rate independently; mandatory failures still block delivery. Run the inherited recorder cases afresh. Do not rebuild/retest the unchanged Rust candidate merely for wrapper work or credit its 178/178 as new wrapper tests.

## Records and remaining work

`traceability.md` maps selected requirements to checks and pending native stages. `attempts/<unique-id>/` retains command, cwd, exit/timeout, raw outputs, source/test identities and interpretation. `checkpoint.md` will be written at meaningful boundaries; older checkpoints remain inspectable. Delivery must include real source/test/coverage identities, finalized inputs, concrete operator command and output locations. The full goal remains active until operator evidence is inspected and assessed; preparation completion alone does not close OW-03/OW-04/OW-05. Framework acceptance remains NOT_EVALUATED.
