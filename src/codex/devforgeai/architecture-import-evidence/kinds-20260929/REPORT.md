# Architecture component-kinds delta — 2026-09-29

Architecture source is authored as **SKL-003 v5**, implementing only the **SPEC-003 v2 component-kinds delta**. These results do not establish full Architecture requalification, installation, or owner acceptance. The final primary-checkout readback detected drift; the tested worktree and its protected inputs are unchanged (see the exception below).

## Evidence availability

This PR includes this report, the [evaluation summary](evaluation-summary.json),
the [failure categories](failure-categories.json), and a
[SHA-256 manifest of the whole evidence folder](evidence-sha256-manifest.json).
All other campaign evidence remains untracked in the local worktree. Paths marked
"local file" below are relative to
`src/codex/devforgeai/architecture-import-evidence/kinds-20260929/` inside the
worktree listed below; they are not links to files published in this PR.

## Candidate and baseline

- Worktree: `/home/bryan/.codex/worktrees/architecture-kinds-20260929/DevForgeAI`.
- Branch: `codex/architecture-kinds-20260929`.
- Baseline: `5074a5bf61bc0418b1ecf2404cb7fd3bb81df3f2`, verified against `origin/main` and the remote main ref after PRs #10 and #11 merged.
- Baseline SPEC-003: approved **v3**, SHA-256 `8a3f93d127fca7358250dfb6770da5c9f1408b95c866ea4eb76ac9a05a8ce681`. Approved v2 at PR #10's merge has the expected SHA-256 `7f429d44e809a576fa626512dd9fd1c8759710d9b5e2d8ad84bde06bf2392f4f`. Its kinds requirements are the authority for this delta. V3's policy-script, ERR-05 and BEH-14 changes remain outside this task.
- Native runtime digest: `b07c5b09a4f728391567bc8fca72cc0342ca9363a09cf3cb8168756c59b70254`. Frozen schedule and manifests (local file `matrix-plan.json`) bind the 11 runtime files, evaluation definitions, executable, version, and harness hashes before native execution.
- Native CLI: `codex-cli 0.159.0`; resolved executable and hash are in the frozen plan. The native host selected `gpt-6-astra` with `max` reasoning, inherited from its configuration. Recorded host settings (local file `native-host-settings.json`) preserve the actual values across attempts.
- Worktree exception: the app's managed-worktree tool failed with dubious ownership on the WSL UNC path. A fresh native WSL Git worktree was created on the requested branch. It is not app-managed; no global trust or user configuration was changed.

## Claude-to-Codex mapping and source changes

The exact reference is Claude commit `22bcfd6`; its diff is retained (local file `claude-kinds-reference.diff`). This is an additive delta, not a re-port.

| Claude change | Codex implementation |
|---|---|
| Component step lists seven kinds and asks about uncertainty | Same values, multiple kinds allowed; Codex uses the existing mode-aware `request_user_input` or plain-text-and-wait rules |
| No-user uncertainty and unchanged legacy CMPs | Only evidence-stated kinds; otherwise omit the field and add the exact CMP marker; existing components remain byte-identical |
| Output field/table, self-check, examples and ARCH template | Matching additions; template uses real `"service"`, with no invalid enum placeholder |
| Skill provenance | Metadata/provenance 4 → 5; implements SPEC-003 v2, with draft status and honest unknown authoring identity retained |
| `creates-arch/cmp-kinds` grader | Added through the Codex generator and regenerated. Uses the native harness's Python regex engine; rejects invalid later values and flow fields even when another valid value or marker is present |
| Artifact checker | Already loads canonical `src/schemas/arch.schema.json`; no enum fork or runtime schema copy was added |

The package manifest remains **0.4.0**. Its history bumps the package when skills are added; this change updates an existing skill and retains all four skills and their metadata. Native discovery (local file `catalog-preflight/result.json`) found Architecture, PRD, Brainstorm and Documents Updater. PRD source is unchanged.

## Static checks

Retained static results (local file `static-attempt-1/results.json`): plugin validator PASS; skill validator PASS; **50/50 package tests PASS** (44 existing, six new regression methods); all 15 generated fixtures validate. Template schema check PASS after replacing only date placeholders; a valid kind passes, an unknown kind is rejected, and a missing kinds field passes. Empty, duplicate and scalar kinds are also rejected by schema controls. No schema is added to the runtime package.

The same-engine grader self-tests cover valid block lists, multiple kinds, the uncertainty marker, unknown values, a valid value followed by an unknown value, empty lists, flow form, and attempts to mask invalid fields with a marker. See `test_architecture_kinds` in the test log (local file `static-attempt-1/package-tests.stderr.txt`). Existing generated prompts, fixtures and graders are byte-identical; only `cmp-kinds.md` was added. Source audit (local file `source-audit.json`) records version alignment, policy-reference parity, and the 378-line skill with a 638-character description. Source and new-source-file whitespace checks passed.

## Native results

The original prompts and fixtures were used, with three repetitions per arm. **66/66 selected attempts are retained**; run statuses: `{"completed": 65, "failed": 1}`. The complete 84-slot denominator retains 18 explicitly unrun slots for the three unchanged cases. No retries were used to seek a passing sample. Every plugin repeat must reach 0.8; failed mandatory checks are not waived by an average. Scores from a failed native turn describe retained partial output, not completed behavior; execution status and completion guards remain separate.

- New `cmp-kinds` check on `creates-arch`: plugin **3/3**, baseline **0/3**.
- Focused classification review (local file `creates-kind-review.json`): the three plugin creation artifacts were also read against their PRD. UI/hosting classifications follow explicit PRD evidence; `service` denotes the stated application/business logic, without asserting a deployment choice. Uncertain kinds retain component-specific markers. This primary-assistant review is separate from the native producer, not independent of source authorship.
- Source-score threshold: plugin **30/33**, baseline **0/33**.
- Strict checks: plugin **3/33**, baseline **0/33**. Baseline provenance guards are different, so compare source scores separately.
- Artifact schema results: `{"baseline": {"FAIL": 52, "PASS": 15}, "plugin": {"PASS": 48}}`. These count saved canonical-path artifacts, not the trial denominator.
- Component kind/legacy preservation audit: `{"baseline": {"FAIL": 13, "PASS": 5}, "plugin": {"PASS": 122}}`. This checks enum, uniqueness, block form, uncertainty markers, and legacy item bytes; it does not by itself prove semantic certainty.

| Case | Plugin scores (1 / 2 / 3) | Baseline scores | Plugin strict passes |
|---|---|---|---|
| creates-arch | 0.900 / 0.900 / 0.900 | 0.000 / 0.000 / 0.000 | 0/3 |
| org-a-policy | 0.800 / 0.800 / 0.800 | 0.000 / 0.000 / 0.000 | 0/3 |
| org-b-policy | 1.000 / 1.000 / 1.000 | 0.000 / 0.000 / 0.000 | 0/3 |
| unrelated-adr | 0.800 / 0.800 / 0.800 | 0.000 / 0.000 / 0.000 | 0/3 |
| superseded-adr | 0.800 / 0.800 / 0.800 | 0.600 / 0.600 / 0.600 | 0/3 |
| no-acceptance-without-user | 1.000 / 1.000 / 1.000 | 0.000 / 0.000 / 0.000 | 0/3 |
| insufficient-evidence | 1.000 / 1.000 / 1.000 | 0.000 / 0.000 / 0.000 | 0/3 |
| prd-change-handed-back | 0.800 / 0.800 / 0.800 | 0.400 / 0.600 / 0.600 | 0/3 |
| hands-off-to-epic | 0.375 / 0.375 / 0.375 | 0.375 / 0.375 / 0.375 | 0/3 |
| records-provenance | 1.000 / 1.000 / 1.000 | 0.000 / 0.000 / 0.000 | 0/3 |
| reuse-records-review | 1.000 / 1.000 / 1.000 | 0.500 / 0.500 (native failed) / 0.500 | 3/3 |

See [summary and full denominator](evaluation-summary.json), per-grader results (local file `matrix-grades.json`), [separate failure categories](failure-categories.json), artifact schemas (local file `artifact-schema-checks.json`), component audit (local file `component-kind-audit.json`), and each trial under `matrix/` for prompts, protocols, runtime snapshots, before/after workspaces, replies and individual grades. The original semantic rubrics remain separate from regex scores; pending reviews are marked `REVIEW_REQUIRED`. The primary assistant reviewed the retained semantic replies separately from the native trial producer; this is not independent review of the source author.

The trials use separate fixture workspaces and candidate discovery settings but share the host's temporary directory. Some producers reused top-level temporary validator filenames. The bounded temporary-path audit (local file `scratch-isolation-audit.json`) records observed command/file-change uses and any overlapping use windows; it does not establish an OS-hermetic boundary. Independent grading and schema/component audits use saved workspace artifacts, not producer-reported temporary validator results.

## Interactive VER-12(l)

**PASS for the scoped interactive behavior.** A fresh PRD named an ambiguous Coordination hub. In Default mode the native model asked which kinds apply, offered all seven, and ended its turn. The pre-answer workspace was unchanged. After the primary assistant manually inspected that question and supplied the predefined fixture answer, the next turn wrote exactly `service` and `api`. The PRD and candidate stayed unchanged. Question, answer, artifact and checks (local file `manual-VER12l/grade.json`) retain the evidence.

This was an assistant-operated native interaction, not Bryan's personal acceptance. The plain-text fallback was exercised; Plan-mode `request_user_input` was not rerun. Other VER-12 subcases and deployment VER-13 remain NOT_RUN in this delta. The inherited model-provenance limitation remains visible separately from the kinds interaction.

## Unchanged cases not rerun

- `existing-arch-not-duplicated`: **NOT_RUN** — Unchanged step-4 gate ends before component classification or output validation.
- `ignores-unrelated-request`: **NOT_RUN** — Unchanged negative-trigger path does not load the skill or reach component classification.
- `reuse-review-idempotent`: **NOT_RUN** — Confirmed current-version reuse writes nothing and skips output validation; no component classification is persisted.

Their last results remain in the unmodified v4 report and [v4 summary](../native-evaluation-20260928-v4/evaluation-summary.json): VER-07 plugin scores 0.600 / 0.600 / 0.400, strict 0/3; VER-11 1.000 / 1.000 / 1.000, strict 3/3; VER-16 1.000 / 1.000 / 1.000, strict 3/3. Those historical results are not passes for this candidate.

## Boundaries, discrepancies and acceptance

SPEC-003 BEH-13 requires “generated_by with the tool, model and session”. The frozen skill requires exact host identities and leaves validation unresolved when one is unavailable. The native host supplies its configured model to the evaluator, but model-produced ARCH files in this campaign can still record `unknown`. This proves a provenance mismatch and records the producer's report of unavailable identity; it does not alone prove that the host cannot expose identity through any supported channel. Failed handoff/source graders, provenance guards, missing evidence, and any harness failures remain distinct. No spec, source rule or grader was weakened. See detailed discrepancies (local file `discrepancies.md`) for evidence and proposed follow-up.

Preservation audit (local file `preservation-audit.json`): **FAIL_PRIMARY_DRIFT** for the overall unchanged-primary requirement; **PASS** for the 170 protected inputs in this task worktree and the frozen candidate/evaluation files. Before (local file `read-only-before.json`) and after (local file `read-only-after.json`) hashes retain both locations, including the expanded primary directory scopes. Primary before (local file `primary-before.json`) and after (local file `primary-after.json`) inventories preserve the drift evidence. See the exception below.

| Boundary | Status |
|---|---|
| Source authored | Complete, Architecture v5 kinds delta |
| Static validation | PASS, bounded checks above |
| Native `cmp-kinds` grader | Plugin 3/3; execution completion and all other failures remain separate |
| Interactive kinds check | PASS, assistant-operated; personal review separate |
| Full Architecture qualification | Not established |
| Primary unchanged readback | FAIL_PRIMARY_DRIFT; task-worktree protected inputs PASS |
| Git delivery | At evaluation completion, no delivery had occurred; see the subsequent publication note below |
| Installation / deployment / marketplaces | Not performed |
| Owner acceptance | Pending Bryan's review |

## Primary readback exception

**The unchanged-primary requirement is not met.** The primary checkout moved from
`5074a5bf61bc0418b1ecf2404cb7fd3bb81df3f2` to
`7e87cf4b4858d9184b763afad631a17ab34a972f` while this campaign ran. Its reflog records
checkouts and fast-forward pulls at 13:15:42 and 14:09:05 EDT, with PRs #14 and #16
now in main. This task did not issue those checkout, commit, or pull commands.
The readback also found 26 new untracked empty files; their origin is not
established, and they were left untouched.

Of the 170 original protected inputs, six changed in the primary checkout and 19
files were added within the protected directory scopes (189 files at readback).
**All 170 remain byte-identical in the isolated task worktree.** The task's source
candidate, all 33 plugin runtime copies, original evaluation definitions, native
executable and frozen harness files are unchanged. The primary manifests differ
at 153 paths overall; complete before/after hashes are retained rather than
presenting an unchanged-primary PASS.

Primary SPEC-003 is now approved v4, SHA-256
`8d757078c85144ff8e790e5eec89335688a9bee1025c0c81a476894115c9e4f8`.
The current prompt added that allowed hash and explicitly says v4 does not touch
component kinds. Reversing only that allowance reproduces the prompt hash captured
before implementation; the reconstructed baseline prompt is labeled as a
reconstruction. SPEC-003 section 4 is identical between the frozen v3 input and
current v4. The tested baseline remains `5074a5b`; no rebase, v4 behavior port, or
qualification claim for later main was made.

See drift reconciliation (local file `primary-drift-reconciliation.json`),
primary file differences (local file `primary-drift.json`),
Git readback (local file `primary-git-readback.json`), and the
current prompt (local file `task-prompt-after-readback.md`).

## Publication scope

The amended commit contains exactly **13 files**: the nine source, test, generated
grader and package-documentation files, plus this report, `evaluation-summary.json`,
`failure-categories.json`, and `evidence-sha256-manifest.json`. There is no
`.gitignore` change. Candidate and case snapshots, native transcripts, protocols,
trial workspaces, manual/static evidence, detailed audits and authoring helpers
remain local and untracked; no evidence file was deleted. All 66 attempts remain
retained, and the published summary preserves the full 84-slot denominator.

The manifest records each evidence file's relative path, size and SHA-256 at
publication preparation, including hidden files and the four files' supporting
local evidence. It excludes only itself to avoid a self-referential hash. Its
aggregate digest covers the ordered file records using the encoding specified
in the manifest. Prior publication receipts and report snapshots are historical
records, preserved locally and included in this manifest; the earlier broad
commit was not pushed.

The source candidate and evaluation results are unchanged. Publication does not
establish full Architecture qualification, installation, deployment, merge, or
owner acceptance. The PR provides the Git delivery record.
