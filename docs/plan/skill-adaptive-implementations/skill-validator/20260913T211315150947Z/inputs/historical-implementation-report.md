# Skill-validator adaptive implementation report

**Implementation delivered; verification remains INCOMPLETE.** All VA-001 through VA-015 and 29 AV obligations have delivered instructions/helpers/schemas. The final Windows regression suite passes 229 tests. Complete native validator workflow/resume and implicit activation are not verified.

## Delivered identity and scope

- Package: `src/agents/skills/skill-validator` (75 permitted files).
- SHA-256: `d51703237abb4d015fbed30f8f03ef93040603a4ea0ec57a623db61e3c71f4b1`.
- Changed paths: 24 added, SKILL.md and evals/build-manifest.json updated; no removals. Exact list and before/after hashes: final-delta.json and before/after-validator.json.
- All preexisting tests/scripts/legacy schemas are byte-preserved. Current executable-artifact manifest refreshed; every prior manifest and failed attempt retained. No baseline/adoption history rewritten.
- Governing SHA-256: `f08a5f745235e969c8186731c187bdc5150d8f92cc8d140d0deb6812e7ecaf42`; companion specification SHA-256: `8fa6fae0625c5edd41cf8bca539a07e9d5fb1f1b90998feaf0be48814fa40a59`. Both matched before and after.

## Actual verification

| Observation | Result |
| --- | --- |
| Exact requested unittest discovery | 229 tests, 65.776 seconds, exit 0; no removed cases |
| Installed skill-creator quick_validate.py on final captured bytes | exit 0, limited structural check |
| Independent forward review | Seven reproduced findings fixed; unchanged-fixture rechecks retained; no remaining demonstrated implementation branch gap |
| Context-sensitive paraphrases/classification | 16/16 expected outcomes; zero final false positives/misses in this corpus |
| Shared builder/validator golden contract cases | 7/7 agree on fresh frozen companion and final validator bytes |
| Parent lineage fixtures | complete/omitted mapping controls agree; parent unchanged |
| Binding helper plus synthetic caller | 9/9 Windows and 9/9 WSL/Linux; identity not emitted; non-MATCH creates no product output |
| Focused native handoff | v1 accepted unchanged; real changed producer v2 rejected unchanged; separate malformed/required-absent/optional-absent branches match |
| Full native validator tasks | two 120-second timeouts; partial events retained; no full workflow PASS |
| Tokenizer | tiktoken installed, cl100k_base local data unavailable; token measurement NOT_RUN, no download |
| Legacy/new record integrity | legacy-records-003 and supplemental-records-001 exit 0; earlier evidence-layout failures retained |
| Source readback | exact delivered package/spec identities match |

Self-review is explicitly labeled and remains INCOMPLETE: 21/23 required applicable checks evaluated, 0 unknown applicability, 6 justified NOT_APPLICABLE rows, all 29 AV rows represented. Workflow/behavior retain AV-W01/W02 NOT_RUN. Set scope is not inferred for the actual one-package maintenance target. Synthetic set records and all full_set/eligible_subset/membership/tampered-total controls are separately retained under independent-review and companion-final. No helper stdout is counted a second time.

## Retained failures and corrections

Independent initial text/resource probes had two false positives (IR-02/03) and two integrity misses (IR-08/09). Followup probes found legacy-alias, missing-report check-validation/counting, and escaping-subject issues (IR-20..23). All seven unique defects have successful focused rechecks; original inputs/results remain. The final contextual corpus has 0 false positives and 0 misses; no aggregate score masks earlier defects.

Regression-001 failed 67 checks because the package manifest predated additions; regression-002 retained 18 stale-manifest failures after source changed during that attempt. Once bytes were fixed and the manifest refreshed, regression-003 and regression-final passed all 229. No assertion was removed or weakened.

The first legacy evidence layout incorrectly placed raw native JSON where the old observer interprets evaluator records; the second attempt reserialized a manifest and invalidated its citation digest. Both failures remain. Fresh self-review-records-003 stores raw JSON under inputs and preserves unchanged bytes; its 118 references pass the unchanged legacy interface. Supplemental records separately pass the new interface.

The first synthetic timeout runner could not terminate via taskkill under the parent sandbox and failed to write its terminal result. Partial output and runner failure remain; the exactly identified child was stopped. The corrected runner retains a timeout result with parent termination and tree-unverified status. Native CLI timeout attempts terminated their child trees. These are development observations, not OS-isolation certification.

## Preservation and companion drift

Operational .agents/.claude/.codex inventories match before/after. This task issued no builder mutation, installation, remote publication, dependency installation, hook/CI/plugin or Rust change. Historical evidence was not targeted by any write; a full historical-tree before/after hash proof was not captured, and is not claimed.

The companion builder changed during this run: before `1d5aa93ca0759f804c3fff9e25eecb55635de20425d93c5aee58799f3ca187c6`, after `844f7bbaa77190593f3ae9025ac189fb1f3e803c00c5b743eee01575b7db071b`. Six changed paths are listed in builder-concurrent-drift.json. They were preserved. Current shared schemas decode identically to validator copies; a fresh exact companion snapshot/readback and golden rerun still agree 7/7. This is observed concurrent drift, not evidence that this task edited builder.

## Remaining native/integration work

- Complete a full cold validator workflow and native resume within a separately selected bounded trial; current attempts timed out. No silent timeout increase or partial-report promotion.
- Obtain a reliable host selection signal before claiming implicit activation; explicit loading and description classification are separate.
- Measure tokens only when the named encoding data is already available locally; required unmeasurable token budgets remain incomplete.
- Exercise full builder authoring -> validator assessment integration under a selected future task. Current evidence covers frozen shared readers and real synthetic producer/consumer tasks, not that broader lifecycle.
- Language/compiler/test-runner behavior for the four project fixtures remains NOT_RUN; their project conventions have held-out semantic evidence.

No unimplemented mandatory branch was identified in the bounded final manual review. Implemented, regression-tested, focused native behavior, complete native verification, installation and Rust qualification remain separate states. No operational copy was refreshed.

## Requirement and case coverage

| Requirement | Cases | Implementation/verification |
| --- | --- | --- |
| VA-001 | VAT-01, VAT-02 | DELIVERED / INCOMPLETE |
| VA-002 | VAT-02, VAT-03 | DELIVERED / SUPPORTED_IN_RETAINED_SCOPE |
| VA-003 | VAT-04, VAT-05 | DELIVERED / SUPPORTED_IN_RETAINED_SCOPE |
| VA-004 | VAT-06, VAT-07 | DELIVERED / SUPPORTED_IN_RETAINED_SCOPE |
| VA-005 | VAT-08, VAT-09 | DELIVERED / SUPPORTED_IN_RETAINED_SCOPE |
| VA-006 | VAT-07, VAT-10 | DELIVERED / SUPPORTED_IN_RETAINED_SCOPE |
| VA-007 | VAT-11, VAT-12 | DELIVERED / INCOMPLETE |
| VA-008 | VAT-13, VAT-14 | DELIVERED / SUPPORTED_IN_RETAINED_SCOPE |
| VA-009 | VAT-15, VAT-16 | DELIVERED / SUPPORTED_IN_RETAINED_SCOPE |
| VA-010 | VAT-17, VAT-18 | DELIVERED / SUPPORTED_IN_RETAINED_SCOPE |
| VA-011 | VAT-19, VAT-20 | DELIVERED / INCOMPLETE |
| VA-012 | VAT-21, VAT-22 | DELIVERED / SUPPORTED_IN_RETAINED_SCOPE |
| VA-013 | VAT-20, VAT-23 | DELIVERED / INCOMPLETE |
| VA-014 | VAT-02, VAT-24 | DELIVERED / SUPPORTED_IN_RETAINED_SCOPE |
| VA-015 | VAT-01, VAT-21, VAT-25 | DELIVERED / INCOMPLETE |

| Case | Status and evidence |
| --- | --- |
| VAT-01 | SUPPORTED; native complete task INCOMPLETE: commands/regression-final; native-trials/validator-attempt-002 — Ordinary/authoring/origin regression compatibility; no target repairs. Full native validator task timed out. |
| VAT-02 | SUPPORTED: companion-final/results.json; commands/regression-final — Seven shared golden shapes/rejections agree; legacy duplicate/nonfinite/version/source cases retained. |
| VAT-03 | SUPPORTED: commands/adaptive-tests-001; independent-review/attempt-02 — Membership, duplicate/injected IDs, omissions, closure and escaping references rejected; no implicit installed-set discovery. |
| VAT-04 | SUPPORTED: independent-review/attempt-04/IR-18; commands/regression-final — FAIL precedes NOT_RUN/advisory; required coverage preserved. |
| VAT-05 | SUPPORTED: independent-review/attempt-04/IR-17; commands/regression-final — Unknown applicability remains INCOMPLETE; justified empty dimensions not applicable; totals checked. |
| VAT-06 | SUPPORTED deterministic; semantic scope bounded: independent-review/results/IR-05; commands/regression-final; supplemental-review/adaptive-observations.json — Multilingual/control/variation/fullwidth candidates have exact byte locations; malformed UTF-8 fails; legitimate literal fixture adjudicated separately. No exhaustive confusable claim. |
| VAT-07 | SUPPORTED semantic: semantic-comparison.json; independent-review/semantic-results.json — Two paraphrases distinguish useful MUST/checklists, production placeholders, inert examples and unbounded rituals; no keyword verdict. |
| VAT-08 | SUPPORTED: independent-review/attempt-03; commands/regression-final — Inline/reference/image/ATX/Setext/HTML/duplicate anchors; inline-code and balanced-parenthesis false positives fixed. Unsupported renderer forms unresolved. |
| VAT-09 | SUPPORTED static/manual; dynamic usage unresolved: commands/regression-final; self-review-records-003/checks.jsonl — Reachability remains separate from roles; license/fixtures retained; manual consumers reviewed; dynamic edges cannot prove orphan status. |
| VAT-10 | SUPPORTED semantic; implicit activation NOT_RUN: semantic-comparison.json — Actual captured fixture descriptions and two paraphrases classified; hidden/overbroad trigger support assessed separately from native discovery. |
| VAT-11 | SUPPORTED: commands/regression-final; budget-fixtures/results.json — Exact bytes/code points/lines; null tokens; required unmeasurable token budget NOT_RUN and false PASS rejected. |
| VAT-12 | PARTIAL / local-encoding positive NOT_RUN: token-fixtures/comparison.json; budget-fixtures/results.json — Installed tiktoken found; selected cl100k_base data unavailable locally. No download. Repeated/unique/excerpt budget arithmetic controls executed; actual token counts not obtained. |
| VAT-13 | SUPPORTED: lineage-fixtures/results.json — Three parent requirements: complete mapping accepted; omitted parent rejected by both readers; parent bytes unchanged. |
| VAT-14 | SUPPORTED semantic; native toolchains NOT_RUN: project-fixtures; independent-review/project-convention-results.json — Five cold project reviews preserve TDD, implementation-first permission, monorepo ownership, docs-only scope and equal-scope ambiguity. Compilers/runners not invoked. |
| VAT-15 | SUPPORTED Windows and Linux helper/caller: binding-windows/results.json; binding-linux/results.json — Nine binding branches each host; correct root/digest/selection/conflict/missing/malformed/relocated results and no product effects after rejection; no identity emitted. |
| VAT-16 | SUPPORTED source/helper scope: binding-windows/results/relocated; binding-linux/results/relocated — Development copy relocation rejected as unbound at runtime; portability does not create a real binding or installation. |
| VAT-17 | SUPPORTED focused native handoff: native-comparison.json; native-trials/handoff-project/out; native-trials/changed-contract/out — Real v1 producer output accepted unchanged by fresh consumer; changed producer emits real v2 and fresh consumer rejects version. Independently malformed consumer cases are separate. |
| VAT-18 | SUPPORTED bounded branches: native-trials/required-absent-consumer-attempt-001; native-trials/optional-absent-consumer-attempt-001; commands/regression-final — Required absent card produces no receipt; optional absence produces declared REJECTED receipt. Graph cycles/unknown members rejected before execution. |
| VAT-19 | PARTIAL: native-comparison.json; commands/cli-help; commands/cli-version — CLI 0.154.0 supported; initial parent sandbox app-server denial retained. Authorized child workspace-write trials execute. Explicit full-validator attempts time out; implicit selection signal unavailable. |
| VAT-20 | PARTIAL; interruption retained: commands/timeout-attempt-001; commands/timeout-attempt-002; native-trials/validator-attempt-001; native-trials/validator-attempt-002 — 120-second partial-output timeout retained. Initial terminal taskkill denied; exact identified child stopped, retry parent killed with tree-unverified status. Native Codex trees terminated. No completed native resume claim. |
| VAT-21 | SUPPORTED semantic/effects boundary: semantic-comparison.json; independent-review/final-completeness-review.md — Target verdict injection/fake upload approval treated as data; no upload or evaluator-authority bypass. |
| VAT-22 | SUPPORTED bounded argv/redaction: binding-windows; binding-linux; commands/regression-final — Spaces/non-ASCII/shell-significant paths remain argv data; Unicode excerpts avoid adjacent synthetic secrets; harmless examples remain inert. |
| VAT-23 | SUPPORTED: commands/regression-final; selected-input-readback.json; builder-concurrent-drift.json — Source readback catches added/changed files. Final specs/validator exact; companion drift preserved and assessed in a fresh snapshot. Old results not promoted to changed bytes. |
| VAT-24 | SUPPORTED: independent-review/attempt-05; budget-fixtures/results.json; commands/legacy-records-003; commands/supplemental-records-001 — Tampered totals/missing-report check bypass/escaping locators rejected; target findings.json not evaluator authority; supported reference bases preserved. |
| VAT-25 | SUPPORTED semantic boundary: independent-review/final-completeness-review.md; self-review-records-003/enforcement-recommendations.md — Universal certification/future Rust acceptance excluded while supported local checks continue; no repairs/install/configuration changes. |

## Changed development paths

- `src/agents/skills/skill-validator/SKILL.md`
- `src/agents/skills/skill-validator/evals/build-manifest.json`
- `src/agents/skills/skill-validator/assets/openai-yaml-guidance.md`
- `src/agents/skills/skill-validator/references/adaptive-shared-contracts.md`
- `src/agents/skills/skill-validator/references/adaptive-validation.md`
- `src/agents/skills/skill-validator/references/set-trials.md`
- `src/agents/skills/skill-validator/references/text-resource-checks.md`
- `src/agents/skills/skill-validator/schemas/adaptation-proposal-v1.schema.json`
- `src/agents/skills/skill-validator/schemas/adaptation-selection-v1.schema.json`
- `src/agents/skills/skill-validator/schemas/adaptive-check-observation-v1.schema.json`
- `src/agents/skills/skill-validator/schemas/adaptive-common.schema.json`
- `src/agents/skills/skill-validator/schemas/adaptive-observation-v1.schema.json`
- `src/agents/skills/skill-validator/schemas/adaptive-observations-v1.schema.json`
- `src/agents/skills/skill-validator/schemas/adaptive-skill-v1.schema.json`
- `src/agents/skills/skill-validator/schemas/binding-observation-v1.schema.json`
- `src/agents/skills/skill-validator/schemas/project-binding-v1.schema.json`
- `src/agents/skills/skill-validator/schemas/project-evidence-v1.schema.json`
- `src/agents/skills/skill-validator/schemas/set-assessment-v1.schema.json`
- `src/agents/skills/skill-validator/schemas/set-authoring-v1.schema.json`
- `src/agents/skills/skill-validator/schemas/set-validation-request-v1.schema.json`
- `src/agents/skills/skill-validator/schemas/standalone-set-input-v1.schema.json`
- `src/agents/skills/skill-validator/scripts/adaptive_contracts.py`
- `src/agents/skills/skill-validator/scripts/adaptive_observe.py`
- `src/agents/skills/skill-validator/scripts/text_resources.py`
- `src/agents/skills/skill-validator/tests/adaptive_fixtures.py`
- `src/agents/skills/skill-validator/tests/test_adaptive.py`

## Reports and exact receipts

- `command-log.json` / `command-log.md`: exact argv, attempts and limitations.
- `case-coverage.json`, `requirement-coverage.json`, `rule-coverage.json`: coverage ledgers.
- `self-review-records-003/validation-report.md`: final schema-1 self-review and references.
- `supplemental-review/`: raw and finalized adaptive observations.
- `independent-review/`: cold reviews, original findings and unchanged-fixture rechecks.
- `native-comparison.json` / `native-trials/`: prompts, events, before/after effects and artifacts.
- `companion-final/`, `binding-windows/`, `binding-linux/`: exact synthetic cross-contract/runtime evidence.
