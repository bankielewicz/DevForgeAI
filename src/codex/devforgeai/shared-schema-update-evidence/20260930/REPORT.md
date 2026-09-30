# Shared-schema update — 2026-09-30

PRD SKL-002 v3 implements SPEC-002 v3; Architecture SKL-003 v7 still implements SPEC-003 v4. Both remain draft. Package version 0.6.0 follows the earlier Codex contract-update minor-version convention.

Evaluated source commit: `4453a84bfba09c19b30a7f514e32bf79fa69a5d9`. Baseline: `c2e67516d66f6786ea9d038480d8e488c8950dd2`.

Frozen runtime SHA-256: `5dd5dfbba3b12b6c641645ce9523ea61e0b2c72fa65552294720b4af74d7078a`. This report and the README update are documentation added after that runtime freeze; they do not represent a new native evaluation.

| Area | Status | Evidence / limit |
|---|---|---|
| Source authored | PASS | Pinned shared scripts/schemas copied; Codex adaptations retained; new testing keys, SV-08, date format, and ID prefixes ported |
| Package tests | PASS | 187 tests on the clean committed candidate; baseline had 156 tests and six expected byte-identity subtest failures |
| Additional static behavior probe | FAIL | Both pinned Claude and Codex validators accept YAML `.nan` as a coverage threshold; the 0–100 percentage contract remains violated |
| Available static checks | PASS | Skill validation, manifest JSON, generator consistency, copied-file identity, provenance/prefix controls, and whitespace |
| Plugin Creator plugin validator | NOT_RUN | Validator script unavailable; the other checks are not substitutes |
| Native policy behavior | FAIL | 90/90 completed; 42/45 plugin source repetitions and 14/15 cases meet the binary criterion |
| Exact identity qualification | BLOCKED | 24 plugin trials retain unavailable or nonmatching identity; disclosure is not a pass |
| Full workflow/manual qualification | NOT_RUN | This focused campaign does not waive prior failures or manual obligations |
| Git delivery at evaluation close | NOT_RUN | Historical snapshot before the subsequently authorized push and PR; current delivery is shown by the hosting PR |
| Installation / deployment | NOT_RUN | Remains outside this change |
| Owner acceptance | NOT_RUN | SKL-002 v3 and SKL-003 v7 await Bryan |

## Native results

Three binary repetitions require 3/3 to meet the 0.8 per-case threshold. The table reports selected source policy checks, separately from identity and full qualification. Every failure and original attempt remains in the external packet.

| Skill / case | Plugin source | Baseline source | Plugin identity gaps |
|---|---|---|---|
| prd / `invalid-policy-stops` | 3/3 PASS | 0/3 FAIL | 0 |
| prd / `no-policy-defaults` | 3/3 PASS | 0/3 FAIL | 3 |
| prd / `none-does-not-waive-policy` | 3/3 PASS | 0/3 FAIL | 3 |
| prd / `policy-applied` | 3/3 PASS | 0/3 FAIL | 3 |
| prd / `policy-bad-authors` | 3/3 PASS | 0/3 FAIL | 0 |
| prd / `policy-bad-date` | 3/3 PASS | 0/3 FAIL | 0 |
| prd / `policy-bad-link` | 3/3 PASS | 0/3 FAIL | 0 |
| prd / `policy-bad-type` | 3/3 PASS | 0/3 FAIL | 0 |
| prd / `project-override-forbidden` | 3/3 PASS | 0/3 FAIL | 0 |
| prd / `project-override-permitted` | 3/3 PASS | 0/3 FAIL | 3 |
| prd / `retired-setting-ignored` | 3/3 PASS | 2/3 FAIL | 3 |
| prd / `unknown-context-failsafe` | 3/3 PASS | 0/3 FAIL | 3 |
| architecture / `org-a-policy` | 0/3 FAIL | 0/3 FAIL | 3 |
| architecture / `org-b-policy` | 3/3 PASS | 0/3 FAIL | 3 |
| architecture / `policy-bad-date` | 3/3 PASS | 0/3 FAIL | 0 |

## Findings and evidence

- **Shared NaN validation defect:** the pinned validator accepts `.nan` with exit 0. Controls accept 90 and reject 101 and signed infinities. Correct the shared validation boundary and add a regression upstream, then authorize fresh pins before changing the mandatory byte copies.
- **Architecture handoff:** `org-a-policy` failures omit the required blocked-requirement handoff after unavailable model identity leaves validation unresolved. The partial grader score of 0.8 is retained as a failed binary repetition. Supply exact identity through a supported host contract; do not fabricate it or weaken the grader.
- **Grader defect:** the inherited file-exists check missed files under a terminal recursive glob. Original scoring is preserved alongside a separate corrected scorer backed by six controls; actors were not retried. The repository grader remains unchanged.
- **Coverage boundary:** the 15 selected native fixtures contain no testing settings. Package tests exercise the new keys and SV-08; these native trials cover the requested policy regressions and date-label behavior.
- **D7 process deviation:** one full suite ran before the checkpoint commit after sandbox-denied staging. That attempt remains recorded; the separate clean committed 187-test run is the verification receipt.
- **Historical evidence:** the owner approved preserving the two old-label matches in the previous contract report. All read-only inputs and historical evidence remain unchanged.

The retired-setting baseline retains a 2/3 frozen result. Its third reply explicitly rejects the retired platform, but the document mentions its name and therefore fails the textual grader. That failure is preserved; it does not by itself establish adoption of the retired mandate.

The native host was pinned to Codex CLI 0.159.2, with `gpt-6-astra` recorded per thread. Each actor used a separate temporary parent; catalog and process-local controls disabled other skills/plugins/MCP and memories. This is not an OS-hermetic read boundary. Semantic reviews were made by the coordinating Codex assistant, not by a human approver.

## Published evidence

The committed packet contains this report, the [evaluation summary](evaluation-summary.json),
[failure categories](failure-categories.json), and the [whole-folder SHA-256 manifest](evidence-sha256-manifest.json).
The summary preserves every case result for both arms. Failure categories keep behavior, identity,
platform, harness, grader, process and missing-evidence outcomes separate.

The complete 2,302-file evidence folder remains local, outside Git, under
`/tmp/devforgeai-shared-schema-20260930-evidence/`; its archive also remains local. The run protocols,
seeded workspaces, output snapshots and detailed receipts stay local. Versioned case definitions and
generators remain part of the source change.
The manifest includes every regular file in that folder, including its original `EVIDENCE-SHA256SUMS`
and `SEAL.json`. Paths are relative to the local evidence root; they are inventory entries, not
repository links. The full local `REPORT.md` is distinct from this compact publication report.
A checksum establishes byte identity, not acceptance or qualification.

The evaluation's pre-publication closing revision was `1e1513a1c4de9537aeeff7eae2864d3091c8bba6`;
it passed 187 package tests and the available static gates. This documentation commit was then amended
only to prepare the four-file publication packet. The evaluated runtime remains
`4453a84bfba09c19b30a7f514e32bf79fa69a5d9`; no actor trial was repeated. The primary checkout's
pre-existing edits and the complete sealed local packet are preserved.

The [previous contract report](../../contract-update-evidence/20260929/REPORT.md) and all import evidence retain their original candidates, failures, and qualification limits.
