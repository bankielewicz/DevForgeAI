# QA skill independent validation

## Identity and conclusion

**INCOMPLETE.** Assessment reporting is complete; behavioral evaluation and evaluated-build completeness are not. No confirmed defect in the nine runtime source files is established by this run.

- Target: `C:\Projects\DevForgeAI\src\agents\skills\qa`
- Run: `20260914T1949120508210Z`
- Package digest: `bb9b461276a959fe5278117b6687b3edce1342149ae2dd1b5ea82fb03e1d38ed` (9 files, 79946 bytes)
- Rule-set SHA-256: `1ab9ebcf4f9250bff50c320c711f721021496773f8a212826209d5da3c6855fe`
- Selected origin: [MVP specification](inputs/05-qa-skill-spec.md) plus [extension](inputs/04-qa-skill-postmvp-spec.md); extension precedence applies only to its explicit amendments.
- Independence: primary validator assessed builder-delivered bytes; a separate description-only agent supplied routing classifications. Grader implementation tests are evaluator self-tests, not independent runtime skill acceptance.
- Builder readiness: **BLOCKED** by missing required evaluation evidence. Proposal review state: **not_needed**. No runtime source revision or installation is proposed.

## Preservation and sources

The authoring request bound successfully to exact current bytes. The [source snapshot](source/), [original manifest](source-manifest.json), [source-after manifest](source-after-manifest.json) and [preservation readback](preservation-readback.json) show target, both specifications, bound authoring inputs, operational QA and loaded validator unchanged. Historical evidence was never a write destination; the complete historical tree was not recursively hashed. There were no source-capture exclusions.

Authoring-v1 custody is kept in the sibling supplemental record; it is not relabeled as an adopted or legacy generated baseline. No historical quality result qualifies these edited bytes. [OpenAI skill guidance](https://learn.chatgpt.com/docs/build-skills) was retrieved and retained, alongside the dated AV project-policy catalog. See [sources](sources.json) and the [rule binding note](rule-binding-note.md) for exact freshness and the nonsemantic source-ID correction.

## Assessment dimensions

| Dimension | Outcome | Required evaluated / total |
| --- | --- | --- |
| standards | PASS | 11 / 11 |
| workflow | INCOMPLETE | 0 / 1 |
| instructions | INCOMPLETE | 3 / 6 |
| behavior | INCOMPLETE | 0 / 43 |

Overall required checks evaluated: **14/61**; unknown applicability: 0. Ten adaptive-only rules are justified NOT_APPLICABLE for this ordinary single skill. Required unperformed checks remain in the denominator. These are development assessment checks, not compiled-Rust admission or enforcement.

Static review covers all 40 QA/QAP requirements through the [requirement map](requirement-map.json), [workflow map](workflow-map.json) and [semantic review](semantic-review.json). It found coherent continuation, localized readiness, severity stops, complete-collection metrics, literal output delivery and manual repair ownership. Static conformance does not prove those branches execute.

## Executed checks and limits

- `observe.py structure`: exit 0; supported structural observations passed.
- Actual installed Skill Creator `quick_validate.py`: exit 0.
- `adaptive_observe.py package`: exit 2 / INCOMPLETE retained unchanged. Its original-directory identity and TODO candidates were manually resolved; 20 local links resolve, all nine resources have consumers, and no specified Unicode candidate was found. Token counts are NOT_RUN because local encoding data is unavailable; bytes/characters/lines were measured.
- Description routing: **10/10 expected labels matched**. The file-backed routing plan was saved after agent launch; this chronology limitation is disclosed. Explicit source loading in CLI pilots is not native implicit activation.
- Grader TDD: initial 20-test red result retained (24 failing assertions including subtests), then green; report-field extension red retained, then **29/29 tests passed**. No gratuitous refactor was made.
- Focused grader executed-line coverage: **44/44 = 100.00000000%**. Branch coverage: **32/32 = 100.00000000%**. Denominator is only `evaluation/graders.py`; native harness, JSONL runner and orchestration coverage are unmeasured. This is not whole-bundle or framework coverage. The instruction-only target has no executable source-line denominator.
- Bound [Python JSONL bundle](evaluation/bundle-manifest.json): [runner](evaluation/runner.py), [graders](evaluation/graders.py), [independent vectors](evaluation/fixtures.json), [expected results](evaluation/expected-results.json), [schema](inputs/evaluation-result.schema.json), [runtime](evaluation/runtime.json), three concrete native fixtures and exact source/spec/artifact bindings. Execution returned exit **2**, correctly reporting **28/28 grader controls passed and 0/42 complete skill scenarios qualified**. Controls do not count toward scenario pass rate.

## Cold native trials

| Trial | Attempt 001 | Approved attempt 002 | Behavioral observation |
| --- | --- | --- | --- |
| QPV-01 full run | CLI initialization access denied | 120-second timeout | Loaded exact skill, inspected fixture/tools, announced planning; no plan/report or test-launch artifact delivered. |
| QPV-02 explicit plan | CLI initialization access denied | 120-second timeout | Loaded selected skill and inspected inputs; no plan/report delivered. No product launch observed. |
| QPV-06 integrity | CLI initialization access denied | 120-second timeout | Correctly identified direct and resolved-alias mock decorators and announced FAIL/stop before testing; no subsequent command/test launch in retained trace, but report/fix delivery unfinished. |

Each attempt retains exact prompt, inputs, command, cwd, start/end, stdout/stderr, timeout, owned-process cleanup and before/after manifest. The child used workspace-write, inherited configured model/auth, and no bypass flags. Its prompt boundary is not proof of OS isolation. Parent-owned timeout cleanup terminated the recorded process trees; no candidate/fixture bytes changed. See [native observations](native-observations.json) and [command log](command-log.md).

These are three feasibility pilots, not a completed 42-scenario campaign. **39 scenario IDs were not separately attempted; all 42 remain NOT_RUN as complete scenarios.** The full native fixtures/variants for dependency sets, localized readiness, dynamic inspection, threshold collections, in-flight stop ordering, delivery failure, resume/retest, permissions, hostile inputs and the two-language portability pair remain outstanding. No claim is made that unattempted cases cannot run. No timeout is counted as a confirmed skill defect or passing evaluation, and no failed case was silently retried with a larger budget.

## Finding and change proposal

`F-12f5195d7652975d2d28290d7aa3750599cadf14149655b5679461d9e1c8550d` is an **input/evidence limitation**, not a runtime-source bug: mandatory native coverage and delivered outputs are incomplete. The [finding](findings.json) preserves exact affected obligations. No revision specification is justified by the current evidence; `proposed_spec` is null in [handoff](handoff.json). The [enforcement register](enforcement-recommendations.md) proposes no new controls.

## Next action

The remaining work is a separately selected continuation of independent evaluation: recheck these source/spec identities, explicitly choose adequate native case budgets, complete the remaining independent fixtures and graders, and preserve all current attempts. Start a fresh linked run if any input changed. The current 120-second pilots do not authorize larger-budget retries by themselves. No builder invocation, product repair, operational update, deployment or installation was performed. **Framework acceptance: NOT_EVALUATED.**
