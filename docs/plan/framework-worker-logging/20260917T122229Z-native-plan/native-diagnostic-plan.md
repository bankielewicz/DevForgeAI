# Native diagnostic plan for operator review

Planning is complete; native execution is **NOT_RUN**, operator review is **PENDING**, and framework acceptance is **NOT_EVALUATED**. This document proposes one separately selected `preflight` diagnostic. It neither authorizes a launch nor supplies operator findings. No fixture/run directory has been created for the proposed attempt.

## Verified selection and scope

The supplied [QA handoff](../20260917T105456Z-qa-retest/handoff-manifest.json) matches SHA256 `4ac2a9de0392e967fe65c64d782b06563cc11bd9171386b02651d4a6a545fbeb`. Its 39 entries, including the [bound next prompt](../20260917T105456Z-qa-retest/next-review-prompt.txt), were checked before preparation. The [QA report](../20260917T105456Z-qa-retest/qa-report.md) reports 178/178 required cases, 49/49 units, and 3,872/4,057 executed lines (95.4399802809958%). These are retained independent offline results, not measurements from this planning task. QA-LOG-01 and QA-LOG-02 remain `VERIFIED_FIXED` in the unchanged [QA lifecycle](../20260917T105456Z-qa-retest/defect-lifecycle.json).

The 68-file corrected source is `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe-logging-qa-fixes`. Its [candidate manifest](../20260917T105456Z-qa-retest/candidate-manifest.json) has SHA256 `44dcb32397b479506ae84b85fa536f40f4bf5234a7647c4e86d160507926761d`. The selected QA-built probe is:

```text
C:\Projects\DevForgeAI\docs\plan\framework-worker-logging\20260917T105456Z-qa-retest\build-target\debug\devforgeai-codex-worker-probe.exe
2,545,152 bytes
SHA256 cdd7de15eece11ad4c6f8b910ddca947bcc0ca0e98cd1ed939e61ddd73975bcd
```

All eight [specification bindings](../20260917T105456Z-qa-retest/specification-bindings.json) match. Apply the contracts together: [native readiness](../../../specs/framework/runtime/codex-worker-native-readiness-v1.md), [preflight](../../../specs/framework/runtime/codex-worker-preflight-v1.md), [source identity](../../../specs/framework/runtime/codex-worker-source-identity-v1.md), and [logging](../../../../devforgeai/experiments/codex-worker-probe-logging-qa-fixes/logging-contract.md), with the bound base, diagnostic and investigation contracts. Source identity advances the inventory to schema 2; logging advances the request to schema 3 and policy to v3. Review stays schema 2. Earlier v1/v2 examples are historical and must not replace these selected versions.

There is no material drift in the checked source, specification, binary, input and retained evidence bindings. [Intake verification](intake-v2-verification.json) records the Windows x64 / PowerShell 7.6.6 / C: NTFS host and preservation scope. Readback covers the corrected/failed/original/snapshot candidates and selected old evidence. Git metadata is absent. The unchanged root PowerShell helper is neither the launcher nor a dependency of this proposal.

## Diagnostic question and proposed selection

Determine whether this exact pinned app-server remains active through initialize and the required profile inspection, and retain complete bounded stream/exit evidence if it exits early. The [earlier attempt](../../framework-worker-native-diagnostics/20260916T202125Z/diagnostic-report.md) observed exit 1 before initialize. Its cause was unresolved. The logging repair and policy quote correction are not proof of a startup fix.

Propose exactly one `preflight --request` invocation, zero retries, no thread/start, turn/start or model work. Model `gpt-6-astra` and effort `high` are proposed profile selections for the future user decision, not observed entitlement. The operation cannot earn WN-01/WN-02 or NI-T11/NI-T12 credit. No native Codex command, including help/version, is part of this planning task.

Future trial root: `C:\Projects\DevForgeAI\docs\plan\framework-worker-trials\20260917T122229Z-logging-diagnostic`.

| Future location relative to that root | Ownership and purpose |
| --- | --- |
| `selection.md` | Exact separate user selection and any child-environment authorization. |
| `fixture/task.json` | Only fixture member; byte copy of the planned [task](inputs/task.json), 307 bytes, SHA256 `b35366b508eea199c12142a8a4a8d13a083426c35c4b9ebaf9f0ccf168eeab3a`. |
| `inputs-001/` | Fresh inventory, named operator review and rationale, diagnostics config, request and exact-byte input manifest. Preserve later versions separately if needed before launch. |
| `sources-001/`, `sources-002-prelaunch/`, `sources-003-after/` | Read-only Rust source-inventory stdout, stderr and command receipts. |
| `native-001/` | Supervisor identity, create-new launch latch, owned process handle/PID receipt, probe stdout/stderr, duration, exit/timeout/containment records. |
| `run/` | Created exclusively by Rust. Do not create during preparation. Rust writes `request.json`, `task.json`, `profile-review.json`, `diagnostics-config.json`, `inputs.json`, `journal.jsonl`, and optional `diagnostics.jsonl`. |
| `inspect-001/` and further distinct pages | Read-only compiled inspection output and exit receipts; never repair retained evidence. |
| `report.md`, manifests and readback | Observed prerequisite outcome, capture completeness, preservation and remaining limitations. |

This future root was absent during planning. Recheck immediately before preparation; a collision is a stop, not permission to reuse or erase it. The planning directory is distinct and contains templates only.

## Exact prerequisites before a launch

1. A separate user selection must name this seal, this candidate/binary, one diagnostic attempt, model/effort and the child-environment proposal. Complete the [operator-review handoff](operator-review-handoff.md). Current planning authorization does not cover launch.
2. Reverify the QA seal and all selected source/build/specification bindings. Use the QA-built executable above without rebuilding or substituting a protocol peer. Changed bytes require reporting and a new selection; never restore older source.
3. Recheck the physical native executable and its two compiled launcher junction mappings. The physical path is `C:\Users\bryan\.codex\packages\standalone\releases\0.154.0-x86_64-pc-windows-msvc\bin\codex.exe`, 298,169,136 bytes, SHA256 `be96b992178b1e467c225800da0d65f2c86d5eba1ef0b14632f65db381cbdfde`. Planning confirmed bytes and PowerShell junction metadata; complete Rust reparse/identity verification is still required immediately before spawn.
4. Use adapter `codex-0.154.0-stdio` and compiled policy `codex-0.154.0-readonly-no-external-tools-v3`, SHA256 `c8ef7b6184e20fd55833c9b8f7cd17b6dc1f0af494ca367c857953680dab1b49`, with exactly 116 arguments. Rust supplies the argv; no manually reconstructed native command or caller overrides. Preserve all 35 feature disables, read-only/never settings, disabled external integrations, OpenAI provider and ChatGPT selection.
5. Create the fresh fixture with only exact task bytes, leaving `run/` absent. Paths must be absolute, disjoint, without traversal or unsupported reparse components. The request's `candidate_sha256` binds **task bytes**, not the source-manifest digest.
6. Collect a fresh schema-2 inventory using the selected Rust probe. Bind it to the exact future fixture and reviewed source identities. Recollect after any host approval or permission-context change and immediately before launch; preserve old input versions and obtain renewed operator review of any material difference. No stale review/hash reuse.
7. Finalize an actual named operator review, schema 2, with supported values and source coverage. For `preflight`, false findings mean unqualified for work and are permitted; no all-true claim is needed. Any unsupported finding must remain unqualified. The strict [review template](review.template.json) deliberately uses null unresolved fields and is not accepted input.
8. Bind exact diagnostics bytes, inventory, review and request in that order. The [diagnostics selection](inputs/diagnostics.json) is closed schema 1 / `debug` / `closed-v1`. The [request template](request.template.json) is schema 3 with an unresolved review digest; finalize a new immutable copy, never launch the template.
9. The current parent environment contains `ANTHROPIC_API_KEY` by name. Unchanged inheritance fails the Rust credential guard. The future request proposes removing only that name from a copy passed to the child. Do this only if separately selected; leave parent and saved configuration unchanged. Stop on any other name containing `API_KEY` or `ACCESS_TOKEN`, `OPENAI_BASE_URL`, or an alternate `CODEX_HOME`. Record names only, never values. No injection, credential-file read, login/refresh or provider fallback.
10. Prepare and review a thin evidence supervisor with the controls below. Its code/bytes and offline pipe/timeout/containment checks are not supplied or claimed by this planning task. The old diagnostic recorder is historical reference only: its old package, request schema and policy bindings cannot launch this candidate unchanged. Preserve it and `Start-CodexAppServerDiagnostic.ps1`.

## Bounded command contract

[command-plan.json](command-plan.json) supplies exact executable, cwd, argv and bounds. These are planned invocations, not a runnable launcher or evidence that they were executed.

```text
<QA-built probe> profile-sources --checkout-root <future trial root>\fixture
<QA-built probe> preflight --request <future trial root>\inputs-001\request.json
<QA-built probe> inspect --run-dir <future trial root>\run --after 0 --limit 100
```

Run from `C:\Projects\DevForgeAI` through native Windows PowerShell and a reviewed shell-free process recorder. Source collection and each inspection page have proposed 30-second outer bounds and no native launch. Preserve exact UTF-8/raw stdout bytes for inventory hashing; do not parse and reserialize the file that the review references. For inspection pagination, use the returned last sequence as the next `--after` cursor and distinct receipts until all records are covered. Inspect the same immutable run only.

The native recorder must redirect and drain both probe outputs, retain exact bytes and exit codes, and hold probe stdin open with no input during normal execution. Piping empty input, closing stdin or using a helper that calls `communicate()` and closes it would request cancellation. Allowed cancellation is the closed `{"op":"cancel"}` line or the existing Ctrl+C mechanism. Bound control input to 1 KiB.

Rust retains the 120-second total, 10-second RPC capped by remaining time, 5-second grace and 5-second teardown bounds. The proposed supervisor budget is 145 seconds including containment/finalization: reserve the last 10 seconds, request cancellation by 135 seconds if still alive, then use only its retained live process ownership to contain an overrun. The recorder must specify and verify this deadline behavior before selection is executable. Never kill a process based only on a historical PID. A supervisor timeout/overrun is an errored attempt, not a passing Rust deadline test; an unproven stop is cleanup uncertainty. Do not hide cleanup/finalization time beyond the bound.

Create the launch latch before the prelaunch refresh/dispatch sequence. Stop on any unmet prerequisite or first failed invocation; preserve every input version, error and receipt. The selection allows at most one native invocation and no automatic retry, alternate binary, policy relaxation or configuration repair.

## Required observations and interpretation

The existing Rust held Job Object guard must observe exactly one created/active worker where required, including rejection of already-exited descendants. Detached child console, explicit inherited pipe list and atomic job attachment remain unchanged. Do not relax the predicate to accommodate a failing startup.

Within the same bounded app-server process, Rust performs initialize/initialized, config/read with layers, configRequirements/read, complete bounded experimentalFeature/list, hooks/list, local-only plugin/list without refetch, app/installed without refresh, disabled-state MCP inspection, account/read without token refresh, exact model/effort and rate-limit observation. Require the conjunction of the source-bound operator review and actual supported runtime state. Unknown/malformed origin, active integration, work notification/server request, auth/model/profile or process guard failure stops the diagnostic. No thread or turn follows a positive preflight.

New capture evidence must contain observed-before-stop and pre/post exit codes, complete stdout/stderr aggregates, reader/EOF/error/overflow information and valid diagnostic status. The combined stream budget remains 8 MiB; stdout lines 1 MiB. Debug detail is capped at 64 chunk summaries per stream; optional logging at 512 events/1 MiB. Only lengths, hashes and closed observations leave the logger; the classifier uses at most 64 KiB of stderr in memory. No raw worker streams, config payloads, tokens or arbitrary logger arguments are added by the recorder. Probe stdout is already the approved typed journal; do not separately tap worker pipes.

The compiled labels `strict_config_rejected` (the evidenced unknown-configuration-field pattern) and `configuration_parse_failed` (the evidenced invalid MCP transport pattern) are narrow observations. Other messages remain `unclassified`. A pre-stop observation is temporal evidence, not proof of spontaneous exit or a Rust crash. An exit code alone does not establish cause. Truncation, overflow, reader error or optional-log incompleteness must be explicit, and cannot support a complete-diagnostic claim.

Positive diagnostic evidence requires exit 0, terminal `preflight_checked`, null thread/turn, oracle `not_evaluated`, unchanged fixture, zero child exit, verified stopped tree, complete mandatory capture and valid diagnostics. Inspect must also accept the new journal and binding consistency. For a legitimate failed run, preserve its nonzero child code and terminal outcome: `inspect` exit 0 means the record is internally valid, not that startup succeeded. Inspection of malformed/incomplete evidence returns failure; do not rewrite evidence to make it pass. Historical schemas remain historical and cannot substitute for this new schema-3 attempt.

Record probe exit 2 invalid intake, 3 blocked prerequisite, 4 failure, 5 cancellation, 6 deadline or 7 cleanup uncertainty as emitted, together with the terminal reason and raw receipts. Missing terminal, setup error, timeout, failed mandatory consistency or unknown cleanup remains incomplete/unqualified. Distinguish whether the native child actually started. Do not turn a retained failure into a product defect or root-cause claim without supporting observations.

## Handoff and remaining prerequisites

Still pending: separate user selection; named operator/source review; fresh Rust inventory for the future fixture; final request/review digests; explicit child-environment selection; reviewed supervisor and offline verification; live effective profile, account/model and startup observations. PowerShell metadata checks do not establish the full runtime profile or sandbox qualification.

The [next native-trial prompt](next-native-trial-prompt.txt) is the concrete separately selectable request. Native trial evidence must stay in the proposed fresh root, and all old candidates, snapshots, QA/development/native evidence and the PowerShell helper remain preserved. Any product/source change is outside this plan and invalidates reuse of the selected binary/QA result. Build/format/Clippy/coverage are inherited QA results; none was rerun for prose planning. Compiled Rust owns runtime policy and evidence validation; no planning document or supervisor issues framework acceptance.
