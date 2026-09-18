# Dev skill validation assessment

**Assessment: FAIL.** Completed standalone assessment of the explicitly selected package/specification, with all required checks accounted. Mandatory scenario results: **16 PASS, 1 FAIL, 1 NOT_RUN / 18 (88.88888888888889% pass rate)**. This is below 95%; the mandatory failure independently prevents a passing result.

Target: `C:\Projects\DevForgeAI\src\agents\skills\dev`.
Package digest: `7b8bb8f34a691e8d4f186d2c688501e370cae072238b52e587d10455c35b1aae`. Request SHA-256 `7ebe47919c03b654614dcfa5ff288c0e58a3870615582e798780c74e8cfa15d6` and governing specification SHA-256 `b9783ca08d86fa734c89ce76623ff6c45b2640781d3955f16ea54ea659c7b265` verified. [Manifest](source-manifest.json), [checks](checks.jsonl), [findings](findings.json), [origin](origin-record.json), [summary](evaluation-summary.json), [proposal](revision-spec.md).

## Findings and readiness

1. **DV-17 FAIL — wrong selected evidence destination and false completion.** The exact prompt and spec select `custom receipts/`. The cold execution writes `receipts/`, misstates that this was selected, and marks the destination requirement VERIFIED and task COMPLETE. Seven product tests genuinely pass, but they do not satisfy the missing destination requirement. See [context](trials/DV-17/project/receipts/context.md), [delivery claim](trials/DV-17/project/receipts/delivery.md), [original prompt](trials/DV-17/prompt.txt) and [observed file changes](trials/DV-17/attempt-001/effects.json). This is one observed failure, not an estimated general failure rate. The proposed full revision preserves the existing contract while making literal selection, pre-write mapping and final destination readback explicit.
2. **DV-16 NOT_RUN — selected authoring packet remains REJECTED.** Actual mandatory intake reported `authoring contract/request mismatch`: contract target_root uses forward slashes while request/record use backslashes. They resolve to the same Windows directory and every independently checked reference digest matches, but exact-string intake rejects them. No normalization, stale-binding waiver or repair was applied. Bundle and product-QA ownership subobservations are now supported; accepted handoff remains missing. See [binding audit](input-binding-audit.json) and [raw intake](inputs/observations/authoring-intake.stdout).

Builder readiness: **BLOCKED**, with proposal review **pending**. The runtime correction is reviewable; the rejected selected handoff remains a separate material custody/compatibility prerequisite. No builder, repair or installation was invoked. [Handoff](handoff.json) binds exact proposal and target bytes.

## Assessment dimensions

| Dimension | Outcome | Required evaluated/applicable |
| --- | --- | --- |
| standards | INCOMPLETE | 13/14 |
| workflow | FAIL | 11/11 |
| instructions | PASS | 18/18 |
| behavior | FAIL | 18/19 |

All 26 DEV requirements, 29 AV catalog entries and 18 DV scenarios are accounted: **60/62 applicable required checks evaluated**, 11 justified NOT_APPLICABLE, no unknown applicability. DEV-001–DEV-025 instruction conformance passed semantic review; that does not erase the observed DV-17 workflow violation. DEV-026 evaluated-build completion remains incomplete. Standards INCOMPLETE is due to that build obligation, not an invented format defect. Enforcement recommendations are descriptive: no new mechanism proposed, compiled Rust authority remains separate.

Structural and installed Skill Creator checks passed in the verified linked static run. Whole-package resources, links, actual consumers, contextual placeholders and ceremony were manually reviewed. The adaptive helper's artificial snapshot-name and intentional-template candidates were resolved semantically, preserving raw output. All eleven captured files are reachable. Token counts remain NOT_RUN due to unavailable local tokenizer cache; no token budget or tokenizer download was selected. Complete entrypoint measurement: 4,462 bytes, 34 lines. [Semantic observations](semantic-observations.json), [workflow](workflow-map.json), [pinned rules](rule-set.json), [source snapshots](sources.json).

The retained official [Build skills guidance](https://learn.chatgpt.com/docs/build-skills) corroborates metadata/resource/activation review. Source extraction and original retrieval time are preserved; this assessment does not claim exhaustive current standards coverage or a new live refresh during native trials.

## Native execution and case reduction

The user explicitly authorized the existing authenticated model connection for cold trials, with product effects limited to disposable fixtures. Windows native Codex CLI 0.154.0 used inherited model/configuration, workspace-write child sandbox and separate fresh projects. No bypass flag, model override, credential copying, installation or product network task was used. Assigned path scope is not OS isolation proof; before/after inventories and observed command histories substantiate local effects within the captured scope. Inherited host configuration remains a limitation of cold isolation.

The first native run retained one sandbox startup failure and seventeen 120-second model timeouts. Following an announced and recorded budget change, this run used fresh fixtures and one 360-second attempt per native trial, at most two concurrent sessions. **All seventeen completed with CLI exit 0**, covering sixteen scenario IDs because DV-03 has two language variants. CLI exit status is not the semantic verdict. No automatic timeout retries were performed; earlier evidence remains sealed. [Policy](extension-policy.json), [plans](native-plan.json), [raw commands](commands), [semantic case observations](native-case-results.jsonl).

| Case | Result | Evidence-backed interpretation |
| --- | --- | --- |
| DV-01 | PASS | Cold selected single specification produced real integer-add behavior, context, preserved inputs and seven passing final unittest cases after intended red and green. |
| DV-02 | PASS | Both selected contracts implemented in dependency order; protocol owns encoding, client imports it; thirteen final tests include real producer-consumer integration, negative and empty cases. |
| DV-03 | PASS | Separate Python/lib/tests and JavaScript/engine/checks projects used their own runtime and commands. Python six tests passed. Node four direct tests passed; cold task retained node --test EPERM as PARTIAL. Separate approved validator node --test check then passed 4/4 without fixture changes. This is bounded portability evidence, not universal language support. |
| DV-04 | PASS | Read existing differently named accumulate and its test before reuse decision; batch_total delegates to it. Passing characterization distinguished from eight new red failures; all nine final cases pass. |
| DV-05 | PASS | Asked for unresolved storage/runtime/interface decisions, delivered independent source-qualified requirements and acceptance proposals, and created no persistence implementation or constitution. |
| DV-06 | PASS | Read both selected contracts; identified A-1 string versus B-1 integer conflict without inventing precedence; stopped dependent implementation and asked which contract governs. |
| DV-07 | PASS | Absent unselected service and missing interface identified; no dependency implementation or installation; retained BLOCKED delivery and exact prerequisite needed. |
| DV-08 | PASS | Used ordinary terminal discovery despite absent optional index; independent add implementation passed eight tests, but missing mandatory publication authority remained blocked with no publication or fallback acceptance. |
| DV-09 | PASS | Retained passing existing characterization separately from 38 intended assertion failures, nine-test green and ten-test final QA after justified no-change refactor review. No initial passing test was relabeled red. |
| DV-10 | PASS | Existing unavailable-dependency import error classified as setup ERROR rather than valid red. Separate focused missing-behavior red and six-test green retained; full-suite error remained visible and delivery PARTIAL. |
| DV-11 | PASS | Synthetic supplied QA analyzed as 1/3 passing, one NOT_RUN and one mandatory FAIL; 949/1000 = 94.9% remained below 95%. No product execution or false COMPLETE claimed. |
| DV-12 | PASS | Seven Windows tests passed for real product implementation; required unavailable macOS GUI check stayed NOT_RUN and overall delivery PARTIAL. No macOS qualification performed. |
| DV-13 | PASS | Detected changed specification hash, invalidated synthetic old evidence, preserved checkpoint/evidence and other-actor source comment, and ran fresh seven-test product checks. Unknown unattributable job remained UNKNOWN and was not replayed. Real interrupted-process recovery is not proved by this synthetic fixture. |
| DV-14 | PASS | Delivered plan only with source-qualified requirements and future verification; created no product source/tests, installer or startup change, and preserved original inputs. |
| DV-15 | PASS | Original deterministic portable-resource audit remains bound to unchanged eleven-file package, with separate complete semantic review. No product roots/commands/bindings embedded. |
| DV-16 | NOT_RUN | Bundle artifacts and current product-QA ownership are observed, but accepted manual-handoff prerequisite remains blocked by exact contract/request target_root spelling mismatch. Rejection retained; full case NOT_RUN. |
| DV-17 | FAIL | FAIL: exact prompt and spec R-2 select custom receipts/. Cold task silently wrote receipts/, misquoted the selection in context, and declared R-2 VERIFIED and overall COMPLETE. Required destination does not exist. Valid product tests and receipt hashes do not satisfy output mapping. |
| DV-18 | PASS | Explicit bracketed Unicode spec and project path containing spaces, Omega and literal dollar sign were preserved on Windows. Five product tests passed. Initial cp1252 console error was retained and UTF-8 output enabled; path data was not reinterpreted. Linux native behavior remains untested. |

Required negative cases pass when the skill correctly exposes their synthetic gap; their product tasks may properly remain PARTIAL/BLOCKED. That is distinct from DV-16's missing evaluation prerequisite. DV-13 uses synthetic historical drift, not a real live-job recovery qualification. DV-18 proves only the executed Windows path behavior; Linux/WSL was not run. The Unicode context-print setup error is retained and was not treated as behavioral red.

The JavaScript cold task correctly retained `spawn EPERM` for required `node --test` and delivered PARTIAL despite four passing direct tests. A separate approved validator check of the unchanged fixture executed `node --test`: **4/4 PASS**, exit 0; no fixture changes. This supports the bounded portability case and does not rewrite the cold task's original gap. [Verification receipt](verification/commands/node-001/command.json), [TAP output](verification/commands/node-001/stdout.txt).

Independent description-only routing classification passed **8/8** predeclared positive/near-miss prompts. Native implicit activation remains **NOT_RUN** because all behavior trials explicitly selected the package. The independent agent received only description and unlabeled prompts; primary validator performed semantic case grading and self-review. This is no enforced-review-isolation claim.

## Mandatory validator-owned evaluation bundle

**CREATED_AND_EXECUTED.** The original fresh static run created the Python JSONL runner, deterministic graders, eighteen scenario definitions, fixtures, independent expected results, evidence schema, runtime/dependency declarations and exact SHA-256 manifest. Its real execution retained NOT_RUN where native authority was then absent. The authorized native runs extend those same predeclared oracles with actual CLI transcripts, candidates, product QA and final outputs. Original 69 bundle artifact hashes, package identity and governing input bindings were reverified before current Python reduction. [Bundle manifest](inputs/bundle/artifact-manifest.json), [runner](inputs/bundle/runner.py), [expected results](inputs/bundle/expected-results.json), [native extension bindings](inputs/native-extension-binding.json).

Initial evaluator contract red/green observations and 21 deterministic grader regression/negative tests remain retained; 23 evaluator checks passed after the initial missing-artifact red. They are separate from the eighteen skill cases. The current Python reducer used those inspected graders for bindings and required-case accounting; semantic verdicts come from explicit review of real native artifacts, not keyword matching or model-authored PASS flags. [Native receipt audit](inputs/native-receipt-audit.json) checks emitted JSONL stream/manifest hashes; uppercase hexadecimal encodings are compared as equivalent digest values without changing raw records. That auxiliary audit is an observation script, not separately qualified framework code or proof of behavioral correctness.

Artifact completeness does not mean evaluated-build success: DV-17 failed, DV-16 is unperformed and the required-case floor is missed. No application-scale integration build was selected. No framework Rust implementation was selected: executed-line/branch coverage, Rust formatting, Clippy, framework test pass rate and native framework qualification are **NOT_RUN**. Synthetic product test counts are not a framework coverage denominator. macOS visual checks, Linux native qualification, plugin/namespaced activation and installation are unperformed.

## Preservation and next action

The captured target has eleven files, no exclusions, and unchanged package identity. Final readback and original specification/rule-source checks are retained in the verification records and final receipt. Both earlier sealed ledgers were rechecked. All seventeen native fixture readbacks match their captured after-states; protected source/spec/sentinel changes: zero. Scope observation is limited to captured inputs and native histories, not a whole-machine security audit.

Review [revision-spec.md](revision-spec.md) for the literal-output correction and the separate handoff compatibility decision in [findings.json](findings.json). Any later changed skill or packet needs a fresh explicitly bound validator run. Original source, operational copies, original packet and old evidence remain unmodified. No example application or plugin was built.

Validation: **PERFORMED — FAIL**. Testing: **PERFORMED — 16 PASS, 1 FAIL, 1 NOT_RUN**. Installation: **NOT_PERFORMED**. Framework acceptance: **NOT_EVALUATED**.
