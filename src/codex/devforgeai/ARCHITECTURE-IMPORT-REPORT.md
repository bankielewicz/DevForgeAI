# Architecture Import Report

**Status: draft source import; full SPEC-003 qualification is not established.**

## Candidate and scope

This source import adds Architecture (SKL-003 v4) to the existing DevForgeAI Codex
plugin, version 0.3.0. It starts from main commit
969932483d301df2b9eb1ca27a166c38efe1b75b in the separate
`DevForgeAI-worktrees/architecture-codex` worktree on `codex/architecture-port`.
Brainstorm and Documents Updater remain part of the package. PRD and Epic are not
present on this base; Architecture consumes an existing PRD document.

The nine Claude source files, source fixtures, schemas, and approved specification
remain unchanged. [Source hashes](architecture-import-evidence/source-baseline.json)
bind the import to those inputs and the pre-existing Codex package.
No installation, marketplace registration, or deployment was performed.

## Provider adaptations

- Use native `request_user_input`, up to three questions and three listed answers.
  Decisions normally offer two alternatives plus **Decide later**; unavailable host
  modes use explicit text questions without assuming answers.
- Resolve assets and references relative to the loaded skill directory. Read local
  preferences from `.codex/devforgeai.local.md`.
- Use the namespaced Codex skill invocation `$devforgeai:architecture`. The final
  handoff names `$devforgeai:epic` as a planned capability, because Epic is absent.
- Record `codex` for newly authored provenance. Preserve historical Claude records.
  Unknown host model/session values remain explicitly unknown and do not count as
  verified current-run provenance.
- Add Codex skill metadata and a Codex-owned evaluation generator. Source templates
  and seeded documents preserve their original bytes.

## Comparison with SPEC-003

The [detailed comparison](architecture-import-evidence/spec-comparison.md) freezes
all 41 named obligations: 16 behaviors, six error paths, three quality requirements,
and 16 verifications. Provider adaptations do not waive the specification's
decision-specific readiness, explicit acceptance, bounded inspection, or immutable
upstream document rules.

Known source gaps include the stale SPEC-003 verification-status table and VER-07's
single-ARCH fixture, which does not exercise ERR-04's multiple-ARCH branch.
VER-12(f)'s same-package PRD reference comparison cannot be established on this
base because its Codex PRD port is on a separate branch.

## Evaluation

The frozen automated denominator is 14 cases × three repeats × two arms = **84
native Codex trials**. Case scores, actual skill loading, semantic rubric results,
and stricter artifact/provenance guards are reported separately. A score of 0.8
cannot waive a failed obligation. Missing or failed trials remain in the denominator.

All **84 v4 trials completed**, with no harness errors. The frozen runtime SHA-256 is
`002672e3f614de13d5268e6d34a71f95d52202f212f06d97de9388f9ceb3da92`;
implementation commit `5e041cced955ea817fd113a4d44353201cf55426` contains the same bytes.
The earlier v2 smoke and interrupted v3 matrix are retained separately. V3 stopped
after 24 completed trials, four interrupted trials and 56 NOT_RUN trials when an
independent review found a review-row attribution regression; v4 corrects that rule. VER-12 (eleven manual subchecks)
and VER-13 (deployed plugin immutability) remain unqualified in full.
Supplemental source probes do not establish deployment or owner acceptance.

Codex unit tests: **44 passed** (33 existing tests and eleven evaluator regressions). The generated fixture suite validates
15 fixtures against repository schemas. This validates fixtures, not model-produced
architecture artifacts.

See the [evaluation guide](evals/architecture/README.md) and
[verification plan](evals/architecture-verification-plan.json) for reproducible
commands, case mappings, and independent semantic review requirements.

## Final native results

The [machine-readable summary](architecture-import-evidence/native-evaluation-20260928-v4/evaluation-summary.json)
binds all 84 results to the candidate and evaluator hashes. The plugin source-score
mean is **0.843**, compared with **0.304** for the no-plugin baseline. Means describe
this campaign; the required 0.8 threshold applies to each repeat independently.

| Check | Result |
|---|---|
| Codex unit tests | 44/44 PASS: 33 existing tests and 11 evaluator regressions |
| Fixture schema validation | 15/15 PASS |
| Plugin source-score threshold | 36/42 repeats reach 0.8 |
| Plugin strict conformance | **7/42 PASS**; provenance and required behavior failures remain |
| Skill activation controls | 42/42 expected outcomes in each arm, including three negative-trigger runs |
| Authored/modified plugin artifact schemas | **33/33 PASS** |
| Authored/modified baseline artifact schemas | 3/52 PASS; 49 FAIL |
| Independent rubric reviews | 12/12 completed; all fail the required question or readiness rubric |
| Supplemental probes | 4/4 scoped PASS, independently reviewed |
| Full manual obligations | VER-12 and VER-13 NOT_RUN in full |

Only VER-11 and VER-16 pass every strict plugin repeat. The other twelve automated
VER obligations fail; VER-12/13 remain unqualified. A source score of 0.8 can still
include a failed mandatory grader. Strict candidate guards additionally require
actual current-run identity and preserved ownership. Baseline strict guards are
not identical, so baseline source scores provide the comparison here.

| Case | Plugin source scores (runs 1/2/3) | Baseline source scores | Plugin strict passes |
|---|---|---|---|
| VER-01 creates-arch | 0.889 / 0.889 / 0.889 | 0.000 / 0.000 / 0.000 | 0/3 |
| VER-02 org-a-policy | 0.800 / 0.800 / 0.800 | 0.000 / 0.000 / 0.000 | 0/3 |
| VER-03 org-b-policy | 1.000 / 1.000 / 1.000 | 0.000 / 0.000 / 0.000 | 0/3 |
| VER-04 unrelated-adr | 0.800 / 0.800 / 0.800 | 0.000 / 0.000 / 0.000 | 0/3 |
| VER-05 superseded-adr | 0.800 / 0.800 / 0.800 | 0.600 / 0.600 / 0.600 | 0/3 |
| VER-06 no-acceptance-without-user | 1.000 / 1.000 / 1.000 | 0.000 / 0.000 / 0.000 | 0/3 |
| VER-07 existing-arch-not-duplicated | 0.600 / 0.600 / 0.400 | 0.500 / 0.500 / 0.500 | 0/3 |
| VER-08 insufficient-evidence | 1.000 / 1.000 / 1.000 | 0.000 / 0.000 / 0.000 | 0/3 |
| VER-09 prd-change-handed-back | 0.800 / 0.800 / 0.800 | 0.400 / 0.400 / 0.400 | 0/3 |
| VER-10 hands-off-to-epic | 0.375 / 0.375 / 0.375 | 0.375 / 0.375 / 0.375 | 0/3 |
| VER-11 ignores-unrelated-request | 1.000 / 1.000 / 1.000 | 1.000 / 1.000 / 1.000 | 3/3 |
| VER-14 records-provenance | 0.800 / 0.800 / 0.800 | 0.000 / 0.000 / 0.000 | 0/3 |
| VER-15 reuse-records-review | 1.000 / 1.000 / 1.000 | 0.500 / 0.500 / 0.625 | 1/3 |
| VER-16 reuse-review-idempotent | 1.000 / 1.000 / 1.000 | 1.000 / 0.750 / 0.750 | 3/3 |

Schema counts cover ARCH/ADR files at the canonical typed paths, `docs/specs/arch/` and
`docs/specs/adr/`. Other-path writes are assessed by the source/custody graders.
Schema checks concern structure, not decision acceptance, readiness semantics or authentic provenance.
Their checker exits 1 because of the 49 baseline artifact failures; there are no plugin schema failures.

## Findings observed during native evaluation

- Exact host model identity is unavailable to the skill in the observed trials.
  Honest unknown values fail complete provenance qualification and block the
  validated readiness handoff. Nonempty-string source graders cannot waive that
  result.
- The inherited VER-07 prompt forbids questions while its grader requires a
  reuse/amend choice. The port honors the user instruction and preserves the open
  gate; that still fails the source rubric.
- V4 fixes the introduced v3 review-row attribution rule. A completed v4 repeat
  writes the correct current session while preserving historical authorship.
  Another writes unknown and labels its readback PASS without clearly disclosing
  unresolved validation. Repeat outcomes remain separate.
- An amended approved ARCH first becomes in-review with cleared approval, then
  ERR-05 restores its historical approval after three failed provenance checks.
  The trace follows the specification's failure exception and explicitly warns
  that this does not approve the amendment. The normal amendment rule and this
  failure-state restoration need owner clarification; this is inherited behavior,
  not a new provider authorization.
- All four v4 supplemental probes pass independent review: native multiple-ARCH
  selection, initial and final draft-PRD warnings, invalid-policy reporting and
  stopping, and unknown-PRD listing. The runtime candidate stays unchanged.

Detailed evidence is in the [SPEC comparison](architecture-import-evidence/spec-comparison.md),
[native trace review](architecture-import-evidence/native-trace-review.md),
[supplemental review](architecture-import-evidence/supplemental-review-v4.md),
[static validation](architecture-import-evidence/static-validation-v4.json), and
[preservation audit](architecture-import-evidence/preservation-check-v4.json).

## Manual coverage and retained attempts

[Manual coverage](architecture-import-evidence/manual-verification-v4.json) records
all eleven VER-12 subcases. Scoped c/e/g/h checks pass; f has byte parity with the
committed PRD sibling but same-package integration remains NOT_RUN. Subcases
a/b/d/i/j/k are NOT_RUN. Full VER-12 and deployed-plugin VER-13 are unqualified.

| Attempt | Retained boundary |
|---|---|
| V2 smoke | Three completed trials; pre-load root discovery and provenance/question failures retained |
| V3 matrix | 24 completed, four interrupted, 56 NOT_RUN out of 84; stopped after the review-row attribution regression |
| V3 supplemental | Two scoped passes and two failures; superseded by separate v4 probes, never overwritten |
| V4 matrix | 84/84 completed; 36/42 plugin threshold passes, 7/42 strict passes; full grades retained |
| V4 supplemental | Four scoped passes, independently assessed; no manual/deployed qualification implied |

The v3 grader missed newly authored review-row identity. Its pre-fix hashes and
the v4 correction are retained in
[v4-evaluator-correction.json](architecture-import-evidence/v4-evaluator-correction.json).
Eleven evaluator regressions now cover reuse, amendment, every new ARCH/ADR, and
stale or unknown new-row identities. V3's EOF whitespace warning is retained;
v4 removed it before freezing and passed the staged source whitespace check.

## Publication checks

The [final custody check](architecture-import-evidence/final-custody-v4.json) verifies
all 84 planned identities, all 42 runtime-copy checks, and unchanged runtime and
evaluator hashes. The independent trace audit covers 84/84 trials; source inspection,
upstream preservation and user-decision boundaries pass its bounded checks.
[Credential-pattern scans](architecture-import-evidence/publication-secret-check-final.json)
found no high-confidence matches in the retained evidence.

The final source/report whitespace check passes. The full patch retains
**3 whitespace warnings** in historical or raw evaluation evidence;
[the exact output](architecture-import-evidence/publication-whitespace-check.json) is
recorded without changing those bytes. Evidence contains no nested Git repository or symlink.

## Reproducing the evaluation

Use Python 3 with PyYAML, jsonschema and referencing, plus an authenticated Codex
CLI. The retained run used codex-cli 0.158.0 and gpt-6-astra with high reasoning.
From the repository root, choose a fresh evidence path:

```bash
python3 -B src/codex/devforgeai/tests/make_architecture_evals.py
python3 -B src/codex/devforgeai/tests/native_architecture_eval.py \
  --evidence /tmp/architecture-evaluation-new --stage matrix --jobs 4
python3 -B src/codex/devforgeai/tests/grade_architecture_eval.py \
  /tmp/architecture-evaluation-new
python3 -B src/codex/devforgeai/tests/check_architecture_artifacts.py \
  /tmp/architecture-evaluation-new --stage matrix
```

Independently assess the retained VER-05 and VER-07 traces and artifacts against
their frozen rubrics. Each trial's semantic-review.json maps its grader name
(`readiness-mapping` or `recommends-and-asks`) to a boolean `passed`, rationale
and evidence. Regrade after those reviews, then summarize:

```bash
python3 -B src/codex/devforgeai/tests/grade_architecture_eval.py \
  /tmp/architecture-evaluation-new
python3 -B src/codex/devforgeai/tests/summarize_architecture_eval.py \
  /tmp/architecture-evaluation-new
```

The summarizer rejects an incomplete 84-trial matrix or pending semantic reviews.
Use fresh evidence directories for revised candidates; preserve earlier attempts.
Native source loading does not establish installed-plugin or deployed behavior.

## 2026-09-29 — Component-kinds delta (SKL-003 v5)

Implemented only SPEC-003 v2's component-kinds change, from Claude commit `22bcfd6`,
against baseline `5074a5bf61bc0418b1ecf2404cb7fd3bb81df3f2` (approved SPEC-003 v3 is
read-only; its other changes remain outside this task). Architecture metadata and
provenance are v5, implements SPEC-003 v2; package manifest stays 0.4.0.

Static validation: **50/50 package tests PASS**, plugin/skill validators PASS,
template and valid/unknown/absent kinds schema controls PASS, and native-engine
grader controls PASS. All original generated definitions remain unchanged; only
the new `creates-arch/cmp-kinds` grader was added through its generator.

Native evaluation: **66 selected trials retained** (11 affected cases, three runs
per arm); three unchanged cases remain NOT_RUN. New kinds grader: plugin
**3/3**, baseline **0/3**. Plugin source threshold **30/33**;
strict checks **3/33**. Interactive VER-12(l): **PASS** for the
assistant-operated question/wait/answer-recording check. Full Architecture
qualification and owner acceptance are not established.

The [dated delta report](architecture-import-evidence/kinds-20260929/REPORT.md)
contains the exact worktree/branch, candidate digest, mapping, complete denominator,
failures, manual evidence, NOT_RUN reasons, and before/after preservation hashes.
The managed-worktree tool failed on WSL UNC ownership; a fresh native WSL Git
worktree was used without user-configuration changes. At evaluation completion,
no commit, push, PR, merge, installation, deployment or marketplace change had
been performed. Bryan subsequently authorized commit, push and a PR; the dated
report records its publication scope. Earlier report sections and historical
evidence remain unchanged.

Final preservation readback: **FAIL_PRIMARY_DRIFT**. During evaluation the primary
checkout advanced to `7e87cf4` (including approved SPEC-003 v4), six original
protected inputs changed there, and 19 protected-scope files were added. The task
worktree retains all 170 original protected inputs unchanged at `5074a5b`; the
runtime candidate and evaluation definitions are unchanged. The updated prompt
permits v4 and still scopes only the kinds delta; no rebase or v4 behavior port was
performed. The dated report retains the primary drift, prompt reconciliation and
unknown-origin untracked-file findings; it does not claim primary preservation.
