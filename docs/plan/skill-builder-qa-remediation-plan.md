# Skill-builder QA remediation and acceptance plan

Approved for implementation by the user's “Implement the plan” request on 2026-09-13. Maintenance owner: `$skill-creator`. Target: development-source `src/agents/skills/skill-builder` only.

## Verified baseline and decisions

Focused pre-implementation investigation independently reproduced the 43-file package manifest and SHA-256 `338c70995e72637e0ce84991be110d6a371ab6965faf4009d570156ea0e13cf2`. Governing builder specification SHA-256: `8fa6fae0625c5edd41cf8bca539a07e9d5fb1f1b90998feaf0be48814fa40a59`; companion specification SHA-256: `f08a5f745235e969c8186731c187bdc5150d8f92cc8d140d0deb6812e7ecaf42`.

Original audit: [QA report](https://github.com/bankielewicz/DevForgeAI/blob/87fd32de0b35793f4891ec9139d50764bdddd568/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z/qa-report.md), [findings](https://github.com/bankielewicz/DevForgeAI/blob/87fd32de0b35793f4891ec9139d50764bdddd568/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z/findings-ledger.md), [traceability](https://github.com/bankielewicz/DevForgeAI/blob/87fd32de0b35793f4891ec9139d50764bdddd568/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z/traceability-matrix.md). Governing contracts: [builder adaptive specification](skill-builder-adaptive-enhancement-spec.md), [authoring specification](skill-builder-authoring-enhancement-spec.md), [companion shared interface](skill-validator-adaptive-enhancement-spec.md), [independent QA workflow](skill-builder-independent-qa-prompt.md).

| Finding | Focused verification | Decision |
|---|---|---|
| F-01 | Five malformed linked set packets returned VALID/exit 0 on current source. | Repair schema checks and semantic cross-bindings. |
| F-02 | Unknown contract field reached intercepted first staging mkdir; schema forbids it. | Repair inherited parser defect; preserve schemas. |
| F-03 | Current Windows runtime returned MATCH/BOUND for synthetic id_rsa and identity.pfx packages. | Repair shared filename exclusions before content reads. |
| F-04 | Wrong adopted-pointer skill/run identities reached intercepted staging mkdir. | Invoke existing pointer validation before accepting history. |
| F-05, discovered during independent retest | Windows `.ENV` bypassed the existing `.env` prefix exclusion; three mixed-case maintenance tests reproduced the failure before repair. | Casefold the environment-file prefix before inventory reads; preserve the failed predecessor snapshot and retest final bytes on Windows/Linux. |
| D-01 | External concurrent edits preserved with PARTIAL and empty applied_paths. | Status ambiguity, not proven overwrite defect; leave production semantics unchanged. |
| E-01 | Missing pre-execution receipts, fixture/instrumentation errors, inherited cold context. | Improve evidence collection; do not patch production for harness errors. |

F-02/F-04 are inherited defects. Their pre-plan verification stopped before writes, rather than recreating the historical STAGED result. Linux F-03 was not rerun in that investigation. This is focused verification, not fresh complete acceptance.

## Comparison with the audit workflow

The audit mapped all BA/BAT entries, preserved evidence, excluded skill-validator, and separated helpers, native trials and acceptance. Its 7 FAIL / 10 NOT_RUN verdict is supported. Audit delivery is not complete acceptance: native tasks timed out, some pre-execution manifests/effect receipts were absent, cold tasks inherited context, and measured Windows line coverage was 58.19%. Setup and instrumentation failures are not valid product failures or TDD red tests. No defect is inferred solely from timeout or uncovered code. Actual builder-to-validator integration remains outside this independent audit.

## Execution and ownership

1. Allocate a fresh UTC run under `docs/plan/skill-builder-remediation/`; preserve original source bytes, manifests, specifications, tool identities and exact commands. Review unexpected drift without restoring historical bytes.
2. Retain focused tests with observable oracles. Execute red before production edits, then minimum green changes, refactor and affected regression checks. Keep setup failures separate from valid red results.
3. Use `$skill-creator` for maintenance testing. Resulting builder remains authoring-only, never runs generated-skill quality checks or automatically invokes validator.
4. Independent forward-testing owns a separate fresh audit directory. Do not modify operational copies, either validator package, historical schemas, specifications or old evidence. No installation, real binding setup, hooks/CI, remote publication or Rust implementation.

## Repairs

### F-01 and F-02: existing record contracts

Add a standard-library builder-local schema helper shared by authoring/adaptive intake without circular imports. Support the vocabulary actually used by shipped schemas, honoring unconstrained arrays/objects and omitted additionalProperties. Preserve legacy schema bytes and unrestricted legacy requirement objects.

Validate authoring contracts before staging; validate linked authoring records and requests recursively against existing schemas. Bind request run/project/target identity, authoring reference, delivered manifest rows/digest and changed paths to the published member. Recompute row digests; do not trust claimed package digests alone. Retain publication-readback checks.

Tests: five F-01 mutations with refreshed hashes, wrong run/project/paths, malformed optional references, unknown contract fields, valid optional fields and unrestricted array/object contents, valid published packets. Invalid adaptive packets yield INVALID/1; invalid authoring intake yields BLOCKED/2 before staging or target writes.

### F-04: adopted pointers

Use `custody.pointer_record` on the adopted-pointer intake branch before adoption, target, ownership and snapshot verification. Test wrong run/name separately, extra/missing fields, duplicate baseline paths, origin digest and baseline mismatch, plus valid adopted and generated-after-adoption controls. Preserve schema-1/schema-2 history and bytes. Never infer adoption from a current snapshot.

### F-03: private-key paths

Extend shared runtime exclusion, case-insensitively, for basenames id_rsa, id_dsa, id_ecdsa, id_ed25519, id_ecdsa_sk, id_ed25519_sk and suffixes .pfx, .p12, .ppk. Preserve existing exclusions. Ordinary .pub/.crt/.cer files remain permitted unless another existing rule excludes them. This is filename exclusion, not comprehensive secret detection.

Reject before content access. Exact runtime binding yields MISMATCH/UNSAFE_PATH/1 rather than silently omitting a file. Test every pattern, nesting, mixed case, existing exclusions and permitted controls; instrument reads to prove no excluded-file open. Test copied helper portability and refresh only required current artifact digests.

## QA campaign and acceptance

Retain Python JSONL runner, deterministic graders, fixtures, expected results, schema, runtime/dependency information and artifact manifests in new evidence. Do not recreate obsolete builder evaluation ownership or modify validator resources.

Independently retest fixes, rebuild full-spec/BA-001–014/BAT-01–17 traceability against repaired bytes, and complete native create/edit; monorepo discovery; four conventions; HTTP/storage preservation; variants; autonomous A/B/C continuation; update review; resume; non-MATCH/no-product-effects; complete legacy histories; interruption; set handoffs; binding/capture/hostile-path matrices. Windows and Linux results remain separate; native Linux filesystem for count-limit fixtures.

Discover current CLI flags/context. Disposable scopes only, 120 seconds per attempt including children, no bypass flags/configuration changes. Preserve attempts and justify fresh retries. Keep helper, semantic, explicit invocation, implicit discovery and native results distinct. Run Skill Creator quick_validate as limited structural evidence, plus syntax, local links, schema and regression checks.

Declare coverage denominator before runs: every first-party executable line in the repaired builder, including new helpers; no first-party exclusions. Report branch coverage separately. Required-case pass rate and line coverage each >=95%, per platform and overall. Complete BAT acceptance requires 17/17 parents (16/17=94.12%). No failed mandatory invariant is waived by percentages.

Final outputs: repair report, exact red/green/QA logs, independent QA report and mappings, final package manifest/digest, changed-file review, specification readback and evidence manifest. Missing required execution is BLOCKED/NOT_RUN and incomplete coverage, never PASS. Skill acceptance, operational installation and compiled-Rust framework qualification remain distinct.

## Implementation readback

The confirmed repairs are implemented using `$skill-creator`. See the [maintenance report](https://github.com/bankielewicz/DevForgeAI/blob/87fd32de0b35793f4891ec9139d50764bdddd568/docs/plan/skill-builder-remediation/20260913T190249336501Z/REPORT.md) and [fresh independent audit](https://github.com/bankielewicz/DevForgeAI/blob/87fd32de0b35793f4891ec9139d50764bdddd568/docs/plan/skill-independent-qa/skill-builder/20260913T190357053555Z/qa-report.md). Final development package: 44 files, SHA-256 `7715f8b80a9b089a4349f6bbb3b502a52d55a03bb2eb2ec65f861ea4be77ff3a`. Exactly six source-package paths changed; all existing schema files and four pinned specification/workflow documents remain byte-identical.

All 52 focused defect tests pass. Windows maintenance line coverage is 2,028/2,133 (95.0773558368495%), with zero first-party exclusions. Independent final-byte helper replay passes 59/59 on Windows and 59/59 on Linux using native WSL temporary fixtures. Full acceptance remains incomplete because required native scenarios timed out or were unexecuted and Linux full-source coverage was not measured. Follow the audit's explicit remaining-case matrix; the repairs and numeric Windows floor do not waive those gaps. Operational installation and Rust qualification were not performed.
