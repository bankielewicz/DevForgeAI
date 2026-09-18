# Independent dev skill validation

**PASS for the selected assessment.** All 71 applicable required checks passed; 23/23 unique required scenarios passed (100%). This comprises 16 carried historical cases with current byte/prerequisite verification and seven cases completed in this run. Assessment completed: true. Builder readiness: NO_CHANGE; proposal review: not_needed.

Validation: PERFORMED — PASS. Testing: PERFORMED — selected 23-case suite PASS, with the execution limits below. Installation: NOT_PERFORMED. Framework acceptance: NOT_EVALUATED.

## Identity, source and independence

Run: `20260914T0704028557004Z`. Target: `C:\Projects\DevForgeAI\src\agents\skills\dev`. Exact request: `docs/plan/skill-authorings/dev/20260914T0117324130584Z/validation-request.json`, SHA-256 `034887a39a8b5f12e0ca3bb27e2f87cba48b4f0f74335071ef2baf6b77d525af`. Unchanged production intake returned BOUND.

Package digest: `8ad8c94b862a2e68a1d6e3064978bb654ded484da2e8adf0317f23dd7583924c`. Frozen rule-set digest: `7efd45f8b6c62791db13084732531d6b2d5caaa752b273d9a6fb6be1ed866109`. **All applicable mandatory checks in that rule-set digest passed for that package digest.** This is an evidence-backed skill assessment, not protected framework acceptance or a guarantee of future execution.

The primary validator evaluated independently of authoring; no separate reviewer or model-independence claim. The existing original specification and revision contract remain selected, with authored custody recorded separately from schema-1 observed history. See [origin](origin-record.json), [source manifest](source-manifest.json), [final source manifest](source-after-manifest.json), [rules](rule-set.json), [workflow map](workflow-map.json), and [input/checker readback](inputs/final-input-readback.json). All 11 package files and original source/specification/rule/checker bindings match. No target or operational skill changes were made.

The original local input snapshots retain their actual prior retrieval times and were freshly hash-verified. Official OpenAI skill guidance was refreshed at 2026-09-14T07:09:59Z through OpenAI Docs and retained in [the captured page](inputs/official-build-skills.md); it corroborates the frozen rules, without silently expanding this assessment into every current standard. Token counts are NOT_RUN because the tokenizer cache was unavailable; file/byte/character/line observations and complete manual text review are retained. Optional package naming/TODO scanner candidates were manually resolved using original identity and actual passages; raw helper INCOMPLETE output is preserved, not relabeled.

## Assessment dimensions

| Dimension | Result | Evaluated / applicable required |
| --- | --- | --- |
| Standards | PASS | 11/11 |
| Workflow | PASS | 32/32 |
| Instructions | PASS | 5/5 |
| Behavior | PASS | 23/23 |
| Enforcement recommendations | Descriptive; no implemented authority claim | [Register](enforcement-recommendations.md) |

The complete 82-rule set contains 71 applicable checks and 11 explicitly inapplicable adaptive/optional checks; zero unknown applicability, failed, errored or unexecuted required checks. [Checks](checks.jsonl) and [assessment](assessment.json) retain exact reductions. All linked text resources were read, local links resolved, and workflow instructions assessed for actual inputs, action, output, recovery and observable completion; emphatic wording alone was not treated as a defect.

## Required cases and evidence provenance

| Case | Result | Execution basis |
| --- | --- | --- |
| DV-01 | PASS | Fresh cold trial |
| DV-02 | PASS | Fresh cold trial |
| DV-03 | PASS | Cold + host QA + approved warm delivery |
| DV-04 | PASS | Carried, current bindings verified |
| DV-05 | PASS | Fresh cold trial |
| DV-06 | PASS | Carried, current bindings verified |
| DV-07 | PASS | Carried, current bindings verified |
| DV-08 | PASS | Fresh cold trial |
| DV-09 | PASS | Carried, current bindings verified |
| DV-10 | PASS | Carried, current bindings verified |
| DV-11 | PASS | Carried, current bindings verified |
| DV-12 | PASS | Carried, current bindings verified |
| DV-13 | PASS | Carried, current bindings verified |
| DV-14 | PASS | Fresh cold trial |
| DV-15 | PASS | Carried, current bindings verified |
| DV-16 | PASS | Carried, current bindings verified |
| DV-17 | PASS | Carried, current bindings verified |
| DV-18 | PASS | Carried, current bindings verified |
| RV-02 | PASS | Carried, current bindings verified |
| RV-03 | PASS | Carried, current bindings verified |
| RV-04 | PASS | Fresh cold trial |
| RV-05 | PASS | Carried, current bindings verified |
| RV-06 | PASS | Carried, current bindings verified |

RV-01 aliases DV-17 and is counted once. Python/JavaScript variants, retries, host QA and warm continuation do not inflate the 23-case denominator. [Carry-forward audit](inputs/carry-forward.json) verifies each retained case's unchanged source, fixture, prior produced bytes, protected inputs, receipts and relevant runtime prerequisites. Historical executions are not represented as fresh executions. [Native decisions](inputs/native-decisions.json), [case observations](inputs/case-observations.json), and [command log](command-log.md) bind the new evidence.

New cold trials used native Windows, Codex CLI 0.154.0, inherited gpt-6-astra/high configuration without model override, and predeclared 900-second limits with at most two concurrent sessions. Initial app-server access denials are retained as attempt 001; approved host starts are attempt 002. All eight cold sessions for seven cases completed within their bounds. No WSL or additional platform qualification occurred.

DV-01 completed genuine missing-behavior red and six-method green/QA. DV-02 completed producer/consumer integration with eleven tests. DV-05 correctly blocked the underspecified slice while completing independent inventory work. DV-08 used the permitted terminal fallback and correctly left authority-dependent publication incomplete. DV-14 completed plan-only without product implementation. RV-04 rejected the stale draft's receipts/ mapping, preserved the supplied draft, executed eight-method red/green/QA, and verified delivery at the literal `custom receipts/` selection. These expected boundary outcomes are passing skill scenarios, not claims that blocked product work completed.

### JavaScript composite case

DV-03 Python completed ten unittest methods plus five integration checks. The JavaScript cold session performed genuine direct-node red/green but correctly reported the required `node --test` worker EPERM as incomplete. The exact required command was then executed on the unchanged candidate by the authorized Windows host: **6/6 PASS**, exit 0, no candidate changes. The original sandbox denial remains evidence.

The user explicitly authorized one 600-second warm continuation under the [bound proposal](inputs/javascript-continuation-proposal.md). It resumed the same session/model, inspected actual host command/streams and prerequisite hashes, completed in **193.641 seconds**, and added five evidence records plus the CLI final-message file. All 41 prior project files and four host receipts remained byte-identical; source/tests were unchanged and no passing test was rerun. [Authorization](inputs/javascript-continuation-authorization.json), [effects](trials/DV-03-javascript/attempt-003/effects.json), [independent audit](inputs/native-audits/DV-03-javascript-warm/audit.json), and [delivery](trials/DV-03-javascript/project/evidence/continuation-003-delivery.md) retain this distinction.

This supports the selected portability/development scenario through cold execution plus separately authorized host QA and warm delivery. It does not establish an entirely cold successful JavaScript delivery or Node worker execution inside the sandbox. The cold PowerShell receipt helper stated a 30-second child budget without implementing its own timeout; actual commands were short and the parent 900-second limit applied. That historical helper limitation is disclosed; no timeout-enforcement qualification is claimed.

## Evidence integrity and previous findings

The unchanged external Python JSONL runner and deterministic graders executed against independently adjudicated observations, exact fixture/expected-result/schema/runtime artifacts and a new bound manifest: **23 PASS, 0 FAIL/ERROR/NOT_RUN**, package and bundle MATCH, exit 0. See [summary](inputs/evaluation-summary.json), [results](inputs/evaluation-results.jsonl), [manifest](inputs/external-bundle-manifest.json) and [external location](inputs/external-bundle-location.json). The verifier checks evidence bindings; it does not independently infer all behavioral semantics.

The whole new schema-1 run passed the unchanged records checker with zero errors, and supplemental adaptive records passed their own checker. Foreign record families remain raw data under inputs/trials or in separate sibling roots with their own verifier. No evaluator maintenance or weakened checks were required. AV-E01 is resolved for this fresh layout. The previous 184-error whole-run result remains unchanged. An initial new bundle assembly hit a raw-manifest collision; that failed assembly and its explanation remain preserved, and a disjoint v2 capsule was used.

Both previous evidence-limitation findings are [resolved for this assessment](inputs/finding-dispositions.json); [current findings](findings.json) contains no new actionable source defect. Their historical identities and results remain intact. No skill-source repair, revision specification, builder invocation or installation is proposed. [Handoff](handoff.json) records NO_CHANGE and no approval decision needed.

## Coverage limits and next action

Required-case pass rate: 23/23 = 100%, meeting the selected 95% case floor without rounding. Executed-line and branch coverage of the instruction/template-only dev package: NOT_APPLICABLE, zero executable source files. Supporting evaluator/helper runtime coverage: NOT_RUN in this continuation. The earlier focused builder-helper coverage is separate and is not inherited as dev/framework coverage. No compiled-Rust framework denominator, acceptance service or framework qualification was evaluated.

Explicit-path cold task behavior and routing classification were exercised; native implicit activation, namespaced `$DevForgeAI:dev` invocation, installation, GUI/service behavior and non-Windows platform qualification remain outside the established claim. Model-written files and Python outputs supply evidence only. The selected independent evaluation is complete; no further action is required within this authorization.
