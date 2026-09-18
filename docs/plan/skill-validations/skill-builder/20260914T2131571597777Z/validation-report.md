# Skill-builder post-MVP validation

**FAIL** for package `ecb01ece2c38443e58fe7a5b307e9d0de22a1fa9b9ec1f726b79cfa328cb9c9e` against the selected [post-MVP specification](inputs/skill-builder-postmvp-spec.md). Assessment completed: true. Source readback: **UNCHANGED**; all 47 files captured, no exclusions. No source repair or operational installation occurred.

## Confirmed finding

**Major: design-enabled publication can silently downgrade to legacy mode.** Changing `origin.json`'s mode to false, removing its capture binding/file, and altering the captured design still produced AUTHORED, a new baseline and successful publication readback. Reproduced with independent fixtures on Windows and Linux. This violates SBP-011/SBPV-11. The failure concerns local custody consistency; it is not a claim of protected security authority.

Stable finding: `F-033ab599c1554cc6262d11d921b543753874612287144ad90fd34c0dd769dc44`. See [full finding](findings.json), [Windows observations](observations/independent-tests/results.jsonl), [Linux observations](observations/linux-checks/results.jsonl), and the [actual successful publication after corruption](trials/independent/test_silent_legacy_downgrade/docs/plan/authoring/run1/publication-readback.json).

## Qualification and gaps

| Inventory | Outcome |
| --- | --- |
| Installed Skill Creator structural checker | Exit 0 |
| Validator structure observation | Exit 0 |
| Complete text/resource scan | No Unicode candidates; helper's source-directory naming uncertainty resolved against original bound path |
| Independent design custody, Windows | 34/35 supported after correcting one JSON-escaping assertion; 1 product failure |
| Retained custody regressions | 71/71 supported after correcting one copied-fixture schema path |
| Retained adaptive regressions | 21/21 passed |
| Independent design custody, Linux | 34/35 passed; same product failure |
| Required SBPV-01–18 | 5 PASS, 1 FAIL, 12 NOT_RUN/incomplete |
| Native implicit activation | NOT_RUN; explicit loading is different |
| Generated-skill execution | NOT_RUN: neither cold producer delivered a published package |

The original Windows attempts remain 33/35 and 70/71; [handoff assertion correction](observations/handoff-readback/result.json) and [schema-path correction](observations/regression-schema-correction/result.json) are separately retained. No product assertion was weakened, no failed product case was retried into a passing count, and no source was changed. The independent routing reviewer classified 12/12 intended prompts; expected labels were not separately persisted before the response, so this is advisory evidence only.

The full declared Windows first-party denominator is 2,264 executable lines across captured scripts and the generic runtime template, with zero first-party exclusions. Instrumented execution covered **835/2264 = 36.881625%**. Branches: **431/1030 = 41.844660%**. Uninstrumented execution receives no invented credit. This fails the 95% executed-line requirement. Linux line/branch coverage is NOT_RUN. See [coverage](observations/coverage-summary.json).

Windows helper cases are 126/127 (99.212598%) after separately documented harness corrections; complete SBPV scenarios are 5/18 (27.777778%). Linux targeted custody is 34/35 (97.142857%). The declared combined case inventory is 165/180 (91.666667%); [inventory definitions](observations/quality-inventories.json) keep the layers and prior attempts visible. Numeric floors do not waive the failed mandatory custody case or missing complete workflows.

## Cold trials and recovery

Each representative first attempt failed to initialize the local Codex client with Access denied, before model execution. Approved second attempts ran the installed Codex CLI with workspace-write, inherited configuration and a 120-second ceiling. [Simple](trials/native-simple-002/attempt-001.json) and [branching](trials/native-branching-002/attempt-001.json) trials both timed out; parent-owned taskkill returned 0 for each process tree. No timeout was increased and no timeout retry was performed. Exact prompts, events, stderr and before/after manifests are retained under trials.

Simple authoring retained the task capture, contract and design, but no staged/delivered package. Branching authoring retained native event observations but no authored output files. Partial discussions/designs are not completed SBPV scenarios. These ceilings are evaluation limits, not product performance requirements or proof that source caused the timeout. The next dependent action is fresh authorized cold producer execution followed by independent execution of its unmodified delivered skill. Do not fabricate consumer input from an evaluator-written package.

Linux checks ran with native Python 3.12.3 under Ubuntu at the verified `/mnt/c/Projects/DevForgeAI`, accessing the same selected Windows checkout. This bounded compatibility run did not switch to or qualify another checkout. Windows used Python 3.10.11. No tool/dependency installation occurred.

## Assessment dimensions and evidence

- standards: **INCOMPLETE**, 9/10 required checks evaluated.
- workflow: **FAIL**, 8/9 required checks evaluated.
- instructions: **FAIL**, 14/17 required checks evaluated.
- behavior: **FAIL**, 8/21 required checks evaluated.

Required coverage: 39/57; unknown applicability: 0. [Checks](checks.jsonl) retain unperformed obligations under FAIL. Semantic assessment is by the primary validator, separate from builder maintenance; description routing used an independent agent. [Workflow map](workflow-map.json), [resource consumers](observations/resource-adjudication.json), [context counts](observations/context-summary.json), and [ceremony review](observations/ceremony-review.json) retain their limits. Templates and useful MUST/review instructions were not treated as defects merely for their wording.

Rules: `a6006addde71816037bf6d215d59d08440ff4971c81bb2b4269a471f2f1fbfe3`. Official guidance was refreshed from [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills) and retained in guidance; repository and SBP requirements remain distinct project policies. No API/model parameter requirements were imposed on this instruction-based skill. [Sources](sources.json), [origin](origin-record.json), [input readback](observations/input-readback.json) and [source after manifest](source-after-manifest.json) bind the observed bytes. Maintenance claims were inspected as history, not reused as fresh passes or a generated baseline.

## Proposed revision and next action

The [complete proposed revision](revision-spec.md) addresses the single custody finding with an independently bound internal stage-integrity receipt checked before branch selection. It preserves authoring-only scope and closed packet schemas, and explicitly proposes fresh linked runs for pre-revision staged records that cannot establish the new property. That compatibility choice requires review. No timeout-driven product redesign is proposed.

[Handoff](handoff.json) preserves pending proposal review and separate execution readiness. No legacy generated/adopted baseline is asserted; the supported observed-edit/skill-creator maintenance route is documented separately and does not require invented adoption. A repair must be a newly selected, narrowly scoped task followed by a fresh validation run. [Enforcement register](enforcement-recommendations.md) keeps protected authority in future compiled Rust.

Record-check outcomes and reference-audit limitations are in [record-integrity](record-integrity.md). These are evidence integrity observations, not semantic acceptance. Framework acceptance and installation: NOT_RUN.
