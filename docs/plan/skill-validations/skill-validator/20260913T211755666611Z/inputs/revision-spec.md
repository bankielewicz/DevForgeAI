---
id: SKILL-VALIDATOR-FOCUSED-REVISION-20260913T201813155594Z
skill_name: skill-validator
target: codex
status: proposed
---

# Proposed focused remediation contract

## Identity, purpose and ownership

Repair the four independently confirmed defects in development `C:/Projects/DevForgeAI/src/agents/skills/skill-validator`, currently 75 permitted files with package SHA-256 `d51703237abb4d015fbed30f8f03ef93040603a4ea0ec57a623db61e3c71f4b1`. Exact observed bytes and manifest are retained in this run. This proposal does not authorize changes.

Preserve the entire frozen validator specification (`inputs/skill-validator-adaptive-enhancement-spec.md`, SHA-256 `f08a5f745235e969c8186731c187bdc5150d8f92cc8d140d0deb6812e7ecaf42`) and companion shared contract (`inputs/skill-builder-adaptive-enhancement-spec.md`, SHA-256 `8fa6fae0625c5edd41cf8bca539a07e9d5fb1f1b90998feaf0be48814fa40a59`) except the precise clarified rejection/detection behavior below. Existing ordinary skill, legacy origin, authoring intake, selected-set, binding, preservation and reporting behavior remains required. This is a scoped maintenance amendment, not a replacement full acceptance campaign.

Use `$skill-creator` for a later authorized maintenance task; `$skill-validator` owns fresh independent evaluation. Do not invoke builder from validation. Approval must identify unchanged proposal and target digests and selected fixes. Inspect existing known provenance and the supported observed-scoped-edit/authoring basis before changing files; never invent generated/adopted history. A complete observed capture may support an explicitly authorized scoped edit under the newer authoring contract, but known conflicting/corrupt provenance is not absence.

## Activation, interfaces and failure behavior

Keep skill-validator's triggers, near-misses and ordinary/adaptive applicability unchanged. The affected entrypoints remain `adaptive_observe.py records --run-root <root>` and `adaptive_observe.py package --source <package>`. Preserve optional tokenizer arguments and existing legacy observer commands. No descriptor or binding becomes mandatory for ordinary skills.

Preserve closed schemas, all required fields, reference bases, raw stdout shape and exit 0/1/2 meanings. Valid assessment records with stored outcome FAIL or INCOMPLETE can still yield records exit 0: successful integrity inspection is distinct from assessment success. Invalid duplicate or contradictory applicability records yield records MISMATCH/exit 1, with a specific diagnostic; never silently rewrite records or correct claimed totals.

Input drift invalidates dependent evidence. Retain interrupted attempts; resume only against unchanged bytes, otherwise use a fresh linked run. Candidate helpers remain read-only. No remote calls, new dependencies, installations, operational-copy updates, real bindings, hooks/CI or Rust changes.

## Required corrections and acceptance

### FV-001 — Count distinct check executions once (QA-01)

Before aggregation in `scripts/adaptive_observe.py`, maintain one canonical artifact identity registry across every member checks reference and the integration checks reference, including missing-report branches. Use the existing no-follow path validation plus native Windows case normalization for identity comparison. Reject cross-role/member artifact reuse; never normalize Linux paths with Windows rules.

Also reject reuse of an identical `(run_id, check_id)` execution identity across counted check files, including copied files. Distinct checks can cite the same evidence file or equal evidence bytes. Do not deduplicate observations merely by content digest; distinct run/check identities remain distinct assertions. These checks prevent double accounting, not fabricated execution with freshly forged IDs, which remains semantic/provenance review.

Required acceptance: REPLAY-R06, D01-D03 reject; D04-D05 remain accepted. D01/D02 must not count 58 unique member rows as 87. D03 preserves exactly copied execution identities, not genuinely independent runs. Add an explicit different-run/same-check-id control and a same-member duplicate-reference case to package regressions. Do not relax reference or membership validation to accommodate new tests.

### FV-002 — Preserve immutable required handoff obligations (QA-02)

In `scripts/adaptive_observe.py`, reconcile selected handoffs against integration subjects before reduction. Each required handoff must have a required applicable observation, or a required unknown observation with NOT_RUN. A required NOT_APPLICABLE row for that obligation is contradictory and rejected even if another row passes. Missing observation coverage is invalid; the caller must emit an explicit unperformed required row when testing cannot run.

Applicable NOT_RUN or unknown/NOT_RUN keeps the set INCOMPLETE; applicable FAIL retains FAIL precedence and unperformed counts. Optional absence is tested through its declared optional branch and may produce an applicable PASS observation. Ordinary adaptive-only N/A remains valid with a concrete rationale. An explicitly selected dependency-closed subset may omit an out-of-subset handoff exactly as its immutable request declares; it cannot claim full-set completion.

Required acceptance: REPLAY-R07/H01/H06 reject; H02-H05 and H07-H11 preserve their exact expected outcomes/counts in the pre-execution files. H10 remains FAIL with 59/60 evaluated and one unknown. H11 remains an eligible-subset PASS for A only, 29/29; B and its handoff remain explicitly omitted. Add mixed applicable-PASS plus contradictory required-N/A regression coverage. These are record-integrity tests, not native producer/consumer qualification.

### FV-003 — Locate altered exact protocol values (QA-03)

In `scripts/text_resources.py`, add recognition of literal JSON `schema_version` string values as exact protocol identifier contexts, including whitespace, multiline layouts and JSONL records. Do not require the key and value to be on one physical line. Locate characters against original text, not reserialized JSON; preserve original byte offsets, line/column and original/normalized forms. Use existing `context: unknown` plus a protocol-specific explanation, unless an existing context precisely applies. Do not add a new enum value to the frozen schema.

An NFKC-changing protocol character produces an unresolved candidate and package INCOMPLETE/exit 2 when there is no unrelated required failure. It does not automatically establish a semantic FAIL. Ordinary prose remains ordinary, actual source bytes remain unchanged, and excerpts must not disclose adjacent secrets. Preserve all existing command/metadata/path/control scans. This correction does not promise exhaustive confusable detection or decoding arbitrary escaped Unicode into source characters.

Required acceptance: REPLAY-P08 and U01-U03 produce the exact expected located unresolved candidates; U04-U07 preserve existing correct behavior. U02 exercises CRLF, multibyte preceding text and a value on a separate line. U03 must satisfy both candidate presence and redaction after the fix; an empty candidate array is not evidence of working redaction. Add JSONL and equal run/source byte-preservation regression cases before implementation.

### FV-004 — Keep fenced examples literal until valid closure (QA-04)

In `scripts/text_resources.py`, distinguish opener syntax from closer syntax. A closer uses the active marker, has at least the opening marker length, starts after at most three spaces, and has only ASCII space/tab after the marker. A line with trailing text remains code content and must not toggle fence state. Preserve input line positions for both link and anchor extraction. Use the pinned CommonMark interpretation in `inputs/commonmark-notes.md`; this does not require a new Markdown dependency or full renderer implementation.

Required acceptance: REPLAY-P07/F01-F04/F09 remain free of fabricated missing-resource failures; F05-F07 report their actual outside-code links; F08 reports only the real line-5 link, never the literal line-3 example. F10 keeps supported anchors. Add tilde whitespace-tail and backtick-opener info-string counterexamples. Do not weaken the rule into ignoring entire documents containing fences.

## Implementation, TDD and delivery

Only the two identified scripts, focused regression tests and the required evaluation manifest/artifact metadata may change by default. Update a relevant reference only when needed to describe changed behavior; disclose every changed path. No companion, operational or historical-evidence edits. Four requirements map respectively to `adaptive_observe.py` (FV-001/FV-002) and `text_resources.py` (FV-003/FV-004), with tests in the existing validator test package.

Before production edits, execute focused tests demonstrating each selected failure; setup errors are not red evidence. Implement minimal changes, rerun controls, refactor only with passing affected tests, then perform fresh independent QA. Preserve all old cases and unchanged external fixtures in this run. The currently retained red results are evidence, not a substitute for checking the later selected pre-edit bytes.

Fresh QA must execute all 37 retained cases, the additional acceptance cases above, complete discovery with `python -B -X utf8 -m unittest discover -s src/agents/skills/skill-validator/tests -v`, installed quick_validate.py on exact captured delivery, and both legacy/new record interfaces. Explain differences from the previous 229 tests. Refresh required Python evaluation artifacts/digests through documented package maintenance; missing artifacts leave delivery incomplete.

Declare all first-party executable Python support scripts as the package coverage denominator before measurement; report executed-line and branch coverage separately. Report the repository's 95% requirements honestly, without excluding uncovered production paths, merging duplicate executions or rounding upward. Every selected defect acceptance case must pass even if aggregate floors are met. If coverage remains below the required floor, classify fixes independently but leave overall package acceptance incomplete/failed as applicable.

Deliver exact file delta, new package digest, red/green/refactor/QA evidence, selected finding resolution map and remaining limitations. Installation and Rust qualification remain separate. Full native workflow/resume, activation, tokenizer and broad lifecycle gaps are not closed by these fixes and are not silently bundled into implementation. No additional design decision is needed for the four corrections; execution still requires the later selected authorization and custody preflight.
