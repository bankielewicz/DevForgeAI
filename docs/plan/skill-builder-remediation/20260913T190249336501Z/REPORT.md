# Skill-builder remediation implementation

The four original QA defects were reproduced and repaired in the development builder using `$skill-creator`. Independent retesting found an additional Windows environment-file case bypass, which was also reproduced and repaired. The corrections are implemented; **complete skill acceptance remains INCOMPLETE**. Required native workflows timed out or remain unexecuted, and Linux full-source coverage is unmeasured. No installation or Rust qualification occurred.

Approved workflow: [remediation plan](../../skill-builder-qa-remediation-plan.md). Separate evaluation owner and results: [independent audit](../../skill-independent-qa/skill-builder/20260913T190357053555Z/qa-report.md). The original QA's 7 FAIL / 10 NOT_RUN verdict remains valid for its original bytes; it is not overwritten by these results.

## Qualified issues and implementation

| Finding | Correction and observable result |
| --- | --- |
| F-01: malformed/mismatched linked set custody | Adaptive intake validates full existing authoring/request schemas; cross-checks run, project, target, authorization, changed paths and authoring references; validates typed manifest rows and recomputes inventory/digest bindings. Invalid linked packets are rejected with valid controls retained. |
| F-02: unlisted authoring contract fields | Authoring intake validates the frozen contract schema before staging. The shared local schema helper preserves unconstrained legacy arrays/objects and existing schema defaults. Unknown fields and malformed optional references are rejected without changing schemas. |
| F-03: excluded private-key filenames | Shared runtime rejects private-key basenames and suffixes case-insensitively before content reads. Public certificate/key controls remain permitted unless another exclusion applies. This is filename exclusion, not comprehensive secret detection. |
| F-04: adopted pointer identities | The existing `custody.pointer_record` validation now checks pointer shape, run/skill identity and baseline/origin bindings before adoption intake accepts history. Schema-1/schema-2 controls, including generated-after-adoption history, remain covered. |
| F-05: Windows `.ENV` bypass | The environment-file prefix comparison now uses case folding. `.ENV`, `.Env.production` and `.eNv.local` are rejected before file opens. Independent Windows/Linux regressions cover uppercase and mixed-case aliases. |

D-01 remains a status-contract ambiguity, not a demonstrated overwrite bug: an external edit yields PARTIAL with empty applied_paths and preserves the external bytes. Production semantics were deliberately retained. The historical oracle still expects BLOCKED and its raw FAIL remains visible. E-01 fixture/instrumentation failures are evidence limitations, not product defects; corrected attempts are retained separately.

Exactly six package paths changed: `scripts/record_schema.py` (new), `scripts/adaptive.py`, `scripts/authoring.py`, `assets/adaptive-runtime/check_project_binding.py`, `references/project-binding.md`, and `package-manifest.json`. The bounded standard-library schema helper supports the vocabulary used by the shipped schemas; it is not a general JSON Schema engine or framework authority.

## TDD and executed verification

| Evidence | Executed outcome |
| --- | --- |
| `commands/red-03` | Original defects: 47 cases, 30 expected failures, 17 passes, zero setup errors. |
| `commands/green-01` | 47/47 pass after initial repairs. |
| `commands/red-04`, `commands/green-02` | Manifest float-byte and exact-name edge failures reproduced; 49/49 passed after strict typed manifest/exact-match correction. |
| `commands/red-05` | New `.ENV` issue: 52 cases, three expected failures, zero errors. |
| `commands/green-05-corrected`, `evaluations/release-02` | Final package: 52/52 focused cases pass, with predeclared expected results, source receipt and JSONL output. |
| `commands/release-legacy` | 31/31 history, custody, scaffolding and recovery tests pass. |
| `commands/release-edges` | 35/35 negative intake, handoff, publication and I/O cases pass. |
| `commands/contract-edges-03` | 10/10 publication preservation, deletion, malformed revision/adoption, metadata concurrency and capture-limit cases pass. |
| `commands/release-maintenance`, `regression-release/maintenance-results.json` | Historical maintenance oracle replay: 130/131 pass; D-01 remains the single raw oracle disagreement. This copied suite is not the independent audit. |
| `runtime-release-results.json` | 22/22 original-template runtime calls match their expected outcomes. These repeat existing cases for source-path measurement and are excluded from the required-case denominator. |
| Independent `reports/windows-final04-results.json`, `reports/linux-final04-results.json` | 59/59 helper cases pass per platform on final bytes, including the environment-case regression. Independent I/O and hostile-argv observations are separately identified. |
| `commands/structural-release`, `release-readback/receipt.json` | Skill Creator structural check passes; eight Python files parse; 18 JSON files parse; local Markdown links resolve; artifact map matches all 43 non-manifest files; schemas/specifications remain unchanged. |

The final declared Windows maintenance suite has 259 required cases: 52 + 31 + 35 + 10 + 131. Its raw pass rate is 258/259 = 99.61389961389962%. Earlier TDD failures and failed setup attempts remain in place; reruns do not add cases to the denominator or erase prior outcomes. The independent suite's 59 cases are a separate denominator, not added to inflate the maintenance rate. Neither rate is the full BAT pass rate.

Setup-only attempts remain explicit: red-01/red-02 contained fixture issues; green-05 could not import the local evidence module under coverage; its corrected run uses the retained coverage driver. Contract-edges attempt01 used `.git` as an excluded legacy lookup directory, but that helper's declared exclusions contain `backup`; the corrected fixture tests the actual legacy boundary. No product code changed for these harness errors.

## Coverage and acceptance limits

Denominator declared before collection: **all eight first-party executable Python files, 2,133 lines, no exclusions**. The final-byte Windows maintenance collection covers **2,028/2,133 = 95.0773558368495% lines**; branch coverage is **825/944 = 87.39406779661017%**. See [coverage report](coverage-release-03.json) and its [input/digest plan](coverage-release-03-plan.json). Missing lines remain listed; no lines were excluded to reach the threshold. The independent collector's narrower measurement remains separately reported as 852/2,133.

Linux independent helpers ran on WSL-native `/tmp` fixtures against the selected Windows source bytes; 59/59 pass. Linux full-source coverage is NOT_RUN. The earlier mounted-filesystem attempt was incomplete and is retained. Windows coverage does not qualify Linux or other untested platforms. No overall all-platform threshold or protected acceptance is claimed.

Native create and edit completed on the immediately preceding `ecb5f805...` package; the later change only folds environment-file prefixes and updates its documentation/manifest. These observations remain bound to that predecessor digest. Final-byte routing-description completed. Seven proposal/set/discovery cases and final-byte equivalent/removed-parent update reviews and import timed out at 120 seconds, including child termination. Partial artifacts and traces remain evidence, not completed workflows. Timeouts alone do not establish an implementation bug.

Continue from the independent audit's BA/BAT/clause matrix: complete native adaptation across four conventions, monorepo/capability discovery, variants and relocation, runtime no-product-write behavior, dependency failure continuation, update reviews, resume/recovery, and remaining legacy/import/set handoffs. Diagnose why native runs spend their budget in setup/read phases before selecting a new attempt and scope; preserve these attempts and do not weaken required outcomes. Enhanced-validator consumption, operational installation and compiled-Rust acceptance remain separate tasks.

## Final identity and retained evidence

Original: 43 files, `338c70995e72637e0ce84991be110d6a371ab6965faf4009d570156ea0e13cf2`.

Final: 44 files, **`7715f8b80a9b089a4349f6bbb3b502a52d55a03bb2eb2ec65f861ea4be77ff3a`**. Exact file rows, specification hashes and six reviewed diffs: [release readback](release-readback/receipt.json). Existing schema bytes, both adaptive specification hashes, authoring specification and independent QA prompt match the initial receipt. Operational copies, validator packages and old audit evidence were outside the write scope.

The Python JSONL runner, deterministic tests, schema, runtime information, expected outputs, command receipts and fixture receipts are retained in this directory. [Artifact manifest](artifact-manifest.json) binds the selected final evidence and scoped receipt manifests without self-reference. These are ordinary development observations; Python/model-written reports cannot authorize mutations or issue framework acceptance.
