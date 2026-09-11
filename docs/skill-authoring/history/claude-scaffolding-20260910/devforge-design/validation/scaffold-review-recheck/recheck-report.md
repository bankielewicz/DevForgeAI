---
schema_version: "devforge.artifact/v1"
artifact_id: "EVREPORT-devforge-design-scaffold-20260910"
artifact_type: "expert-evaluation-report"
project_id: "devforgeai"
revision: 2
status: draft
created_at_utc: "2026-09-10T21:24:58Z"
producer:
  skill: "devforge-evaluate-expert (source-loaded, not installed)"
  skill_revision: "bdf665c7e18061395c0762de7a377fdc5f6ed48d66245df5623c5c32b90cf2ac (sha256 of the SKILL.md blob at claude-scaffold-evaluate-expert-20260910 commit e641797eebf04cd1e8eb9f711549e038e7745407)"
execution_ref: null
supersedes:
  artifact_id: "EVREPORT-devforge-design-scaffold-20260910"
  revision: 1
  path: "../scaffold-review/verification-results.md"
  sha256: "cdbf6022ab557e35a0a3df9898da2d4d58a7442fbfd0a640b26f55578f38ea4c"
  preserved_location: "committed at 60803e9; re-verified byte-identical at b2827ce"
  reason: "Focused re-evaluation of the repaired candidate. Revision 1 evaluated commit 9ad38de and recorded disposition revise. This revision evaluates commit b2827ce and covers only the changed requirements F-001..F-011 plus rubric criterion R04 and structural check CHK-SPEC-01. Revision 1's records are unchanged and its FAIL history is preserved, not overwritten."
upstream:
  - artifact_id: "SKILL-003"
    revision: 2
    store: project
    path: "docs/mvp/specifications/skill-003-devforge-design.md"
    sha256: "4a90c0d5648217480a4986518795dedd17bf3f62a67e433ec4d9d10e4247c8fb"
    sections:
      - "Workflow and phase exits"
      - "Rework, stopping, and recovery"
      - "Validation and behavioral acceptance"
  - artifact_id: "CANDIDATE-devforge-design"
    revision: "b2827cebf29398f6a63b2a3fd3140cd30483bf70"
    store: project
    path: "providers/claude/plugins/devforgeai/skills/devforge-design/SKILL.md"
    sha256: "90698266b028a8abad3ba113eb8e14d85212e89b41c9b0e75e8c7cdd58d082a1"
    sections:
      - "4. Iterate"
      - "When something is missing or a check cannot run"
  - artifact_id: "CHGSPEC-devforge-design-scaffold-20260910"
    revision: 1
    store: project
    path: "../scaffold-review/skill-enhancement-spec.md"
    sha256: "04603be875ea2a788fe8ce23ec6d48a0014a3f1ee6dd9db2dbcbfc5927488c1e"
    sections:
      - "Requested changes"
      - "Change decision"
evidence:
  - path: "findings-recheck.json"
    sha256: "24b729e0a32c1f561be752f891420632e16b93c3479e255d51b23345d0c51090"
  - path: "runner-out/rc1-package-installedmode.jsonl"
    sha256: "1cee7f50a3f5cde0599c9789171c9ddd8424b94c13426123f7db307df4c29638"
  - path: "runner-out/rc2-fixtures-source.jsonl"
    sha256: "b49b92fc25531aeb2d5312534e2c844dac5df20c3639f8c4b552249a8a391862"
  - path: "runner-out/rc3-fixtures-source-full.jsonl"
    sha256: "9e48ac5db784dd2d6b9a0c83215e68563e8586f81bfccae6b4b7b024e137ff07"
  - path: "commands.log"
    note: "every command this recheck ran, with its output; hashed after the recheck closes"
decision_ref: null
missing_inputs:
  - "Session assignment record: none exists; execution_ref is null."
  - "Installed or exported copy of the candidate: still not generated. Blocks tier C."
  - "Fresh terminal, isolated workspace, per-attempt client-state isolation: still not allocated. Blocks tiers A and B."
---

# Recheck: devforge-design (SKILL-003) repair pass 1

Focused re-evaluation authorized by the coordinator. **Scope: F-001 through F-011 closure, rubric criterion R04, and structural check CHK-SPEC-01 only.** Unchanged broad checks were not rerun; where a check is not named here, revision 1's outcome stands. F-012 and F-013 remain no-target-edit and are unchanged.

The candidate's own change record — `authoring/authoring-notes.md` "Repair pass 1", `authoring/file-manifest.json`, `authoring/handoff.md` revision 3 — was read as untrusted evidence. No claim in it was adopted without checking the bytes.

## Identity

- **New candidate:** commit `b2827cebf29398f6a63b2a3fd3140cd30483bf70` (HEAD), preceded by `60803e9` which committed revision 1 of this evaluation. Prior candidate `9ad38de`.
- **Package:** `providers/claude/plugins/devforgeai/skills/devforge-design`, still 23 files. No file added or deleted.
- **Seven changed package files:**

| File | sha256 at b2827ce |
| --- | --- |
| `SKILL.md` | `90698266b028a8abad3ba113eb8e14d85212e89b41c9b0e75e8c7cdd58d082a1` |
| `evals/cases.jsonl` | `0e6d95413e3864db21378a6e81b9094aaa1d33bbdce1101d07d779a8ab6eb77d` |
| `evals/evals.json` | `11b27a97554edd97c00f1f6bfe9887b4d2e49e98caacdc5cbffe1183212331f8` |
| `evals/fixtures/README.md` | `bc9ff21852b45f7bb331e3b6610bfbbb44facc7928d8dc60c3a1c243aff3fabc` |
| `evals/triggers/trigger-queries.json` | `671ea375af729a8e9be7c1f94bbcdb4415b2d33f1d0a8c833b60a654772de0f6` |
| `references/derivation.json` | `c77fc2c08c8686346f135fd56c116019405060e014469371fe5ade8cc67f8cff` |
| `references/recording-rules.md` | `282fe411fc1a9c56193a1ea4cdce5804a69228bc5efe437d5f44db08c482424b` |

- **Revision 1 of this evaluation is intact.** All eight files under `../scaffold-review/` hash at `b2827ce` exactly as delivered, including `verification-results.md` `cdbf6022…` and `commands.log` `c328658c…`. The author committed them without repinning anything.
- **Runner:** the same validator package, source-loaded at `e641797`. Still a draft under bootstrap review (E2 → `e101e76` → recheck pending).

## Preserved behaviour — regression checks

Every item the repair specification listed as must-not-change was verified.

| Preserved item | Result | Evidence |
| --- | --- | --- |
| Frontmatter is `name` and `description` only | PASS | keys = `['name','description']` |
| Description bytes unchanged | PASS | line 3 identical to `9ad38de`; 950 chars |
| `SKILL.md` well inside 500 lines | PASS | 139 lines, up from 132 |
| No shell-injection syntax, no `docs/mvp` path, no home path in `SKILL.md` | PASS | `grep -c` for ``!` ``, ```` ```! ````, `docs/mvp/`, `/home/` all 0 |
| Both `assets/` files still byte-exact template copies | PASS | `5a30b17a…`, `abc7f8e0…` unchanged |
| All 12 fixtures unchanged, both hard-coded sentinels valid | PASS | `cf0e9f8d…`, `b863996b…` unchanged; DX-B-007 A1 and DX-B-008 A2 observed MATCH |
| Inspection-versus-existence, authority boundary, upstream resolution untouched | PASS | `references/mockups-and-preview.md` unchanged; `SKILL.md` diff is additive; `recording-rules.md` diff is one table row |
| No `scripts/` added | PASS | still 23 files |
| Revision 1 of this evaluation not modified | PASS | eight digests identical at `b2827ce` |

## Per-finding closure

| ID | Sev | Status | Evidence at `b2827ce` |
| --- | --- | --- | --- |
| **F-001** | MAJOR | **CLOSED** | `SKILL.md:91-95` adds "When the design would need an accepted requirement to change": names the condition, requires recording it as a change request against the owning product artifact, names the affected requirement and flow rows, holds the dependent rows at `proposed` with the blocked requirement in `missing_inputs`, lets independent work continue, names `devforge-change` and `devforge-define-product` as owners, states neither is installed, requires a plain-language next task rather than a slash command, and blocks the missing-brief fallback from absorbing the conflict. `:97` extends the exit line to carry both rework routes. New case DX-B-011 / evals id 11 exercises it. |
| **F-002** | MINOR | **CLOSED** | `recording-rules.md:17` now requires the unobservable `skill_revision` to be recorded in `missing_inputs` naming what it blocks, with the reason. The one-file narrowing is preserved verbatim. |
| **F-003** | MINOR | **CLOSED** | `SKILL.md:122` adds a fifth bullet: preserve the phase, the frozen upstream digests and the evidence paths; on resuming re-check those identities *and the session assignment* before dependent work; a changed input, base commit or assignment starts a new iteration with prior evidence retained. Lead-in updated "Four cases" → "Five cases", so no stale count remains. |
| **F-004** | MINOR | **CLOSED** | All four wrong claims corrected and recomputed here: the interruption row cites the new bullet; the rework row is split so the product-scope clause cites the new subsection and case 11 (the previous misuse of `should_trigger:false` triggers A7a/A7b as rework evidence is gone) and the prototype clause cites case 8 and A5a/A5b; "24 trigger queries" → 23 across three positive and six negative categories; "Five of the eleven carry at least one deterministic grader assertion; six route entirely to independent review" — independently confirmed. The document states plainly that revision 1's counts were wrong and that those bytes remain at `9ad38de`. |
| **F-005** | MINOR | **CLOSED** | `evals/fixtures/README.md` gains a "Running `evals/cases.jsonl`" section with both exact invocations, the two-root reason, the note to take DX-C-001's result from the first run, and the explanation that its `path_absent` on `evals` is expected to mismatch against a source tree. **Confirmed by running the documented commands verbatim:** `rc3` returned 11 of 11 cases COMPLETED with zero COULD_NOT_RUN, against 9 of 10 COULD_NOT_RUN for the equivalent single-root run on the old revision. |
| **F-006** | MINOR | **CLOSED** | evals id 9 tier C → B, `deterministic_cases` → `DX-B-009`; `DX-C-009` renamed `DX-B-009` with tier B. `tier_note` gains the invariant that any case with a baseline arm is tier B and the only tier C case is the installed-resource one — which now holds: DX-C-001 is the sole tier C case and its `baseline_comparison` is `not_applicable`. Prompt, fixture, expectations, assertions and baseline all preserved. |
| **F-007** | MINOR | **CLOSED** | `derivation.json derivations[4]` repointed to `e641797` with per-file digests. **Both recomputed from the git objects and identical:** `run_cases.py` `95ca2abf…`, `graders.py` `1b7a27a3…`. The two schema facts readable from `run_cases.py` were re-verified (`routed_to` in `ASSERTION_KEYS`; `notes` in both `CASE_KEYS` and `ASSERTION_KEYS`). The refresh condition names the pending `e101e76` recheck and requires re-pinning. A `repair_passes` record was added stating what was applied, what was declined, what stays no-target-edit, and that changing source bytes closes no evaluation finding. |
| **F-008** | ADVISORY | **NOT APPLIED — declined** | `DX-C-001` now holds A1, A2, A3, A4, A6, A7, A8: A5 removed, nothing added. `DX-B-009` fields remain `[created_at_utc, execution_ref]`. `derivation.json` records the decline and its reason ("the repair spec records 'Demonstrated impact: no defect'"). **Acceptable** — CHG-008 was an authorised enhancement with no demonstrated defect, and declining an ADVISORY with the reason recorded is the author's call. Consequence unchanged: name-versus-folder, links in the shipped assets, the provenance files' presence, absence of injection syntax and the two template digests remain facts an evaluator supplies by hand. |
| **F-009** | ADVISORY | **CLOSED** | `DX-B-009` A1 `expect` "complete" → "placeholder", matching both its own summary and the grader's observed value. Observed: `MISMATCH`, `placeholder`. |
| **F-010** | ADVISORY | **CLOSED** | `DX-C-001` A5 removed, with a `notes` field explaining that it could only observe "0 local, 0 external" and that IDs deliberately skip A5 so earlier recorded rows still line up — preserving comparability rather than renumbering over history. Observed: six MATCH, one MISMATCH, no A5. |
| **F-011** | ADVISORY | **CLOSED**, with a disclosed limit — see N-002 | `trigger-queries.json` gains `revision: 2` and a `revision_note`. **Entry-by-entry diff of both revisions:** 23 queries before and after, no id added or removed, and across all 23 common ids the only field difference in the whole set is A7b's category (`negative_define_product` → `negative_change`). Every query text, `should_trigger` and `split` is unchanged. Totals unchanged at 13 train / 10 validation, 12 negative / 11 positive, no duplicate ids. `negative_design_note` corrected for the now-six negative categories. |

## Rechecked outcomes

| Check | Revision 1 | Revision 2 | Basis |
| --- | --- | --- | --- |
| **AI-R04** Workflow decisions and failure paths | **FAIL** | **PASS** | The FAIL rested entirely on the absent product-scope-conflict transition. `SKILL.md:91-97` supplies it with a stated condition, a stated action, a named owner for each half and an exit condition distinguishing it from the prototype route; `:122` supplies the interruption transition the same criterion's anchors reach. No conflicting instruction was introduced — the new blocks agree with the missing-product-brief procedure, the decisions-versus-proposals section and the stopping conditions, and no branch now prescribes two incompatible actions for one condition. Every other R04 anchor that passed at `9ad38de` rests on text that did not change. |
| **CHK-SPEC-01** Requirement coverage vs SKILL-003 | **FAIL** | **PASS** | Both previously unaddressed rows are addressed: the Rework product-scope clause at `SKILL.md:91-97`, the Workflow-and-phase-exits interruption clause at `SKILL.md:122`. `spec-mapping.md`'s claims for both were re-verified against the bytes they cite and now resolve. No previously addressed row lost support — the only prose edits in the package are those two additions plus the one `recording-rules.md` row. Method `INSPECTION_MANUAL`, authority: none. |

Not rerun, per the authorized scope: R01, R02, R03, R05, R06, R07, R08, R09, R10 and CHK-STRUCT-01 … CHK-AUTH-01. Revision 1's outcomes stand for those, supported by the regression table above showing the inputs they rested on are unchanged.

## Runner observations

Three runs, all `exit 0`. `/usr/bin/python3 -B` 3.12.3, validator runner at `e641797`, `--out` inside this fence. Local, non-isolated evidence; exit status describes the program, never the candidate.

| Run | Invocation | Result |
| --- | --- | --- |
| `rc1` | package root, `--mode installed`, `--case-id DX-C-001` | COMPLETED. A1 MATCH, A2 MATCH, A3 MATCH (4 local links), A4 MATCH (1 local), A6/A7 MATCH, **A8 MISMATCH** (`evals` present — the expected source-tree condition, not a defect). No A5. |
| `rc2` | fixtures root, `--mode source`, `--case-id DX-B-009 --case-id DX-B-011` | Both COMPLETED. `DX-B-009` A1 **MISMATCH** `placeholder` (the intended discriminating result, now matching its corrected `expect`), A2 INDETERMINATE routed to review. `DX-B-011` A1 INDETERMINATE routed to review — correct, since no grader can read routed-versus-absorbed from bytes. |
| `rc3` | fixtures root, `--mode source`, no `--case-id` — **exactly the command the candidate's own README documents** | **11 of 11 cases COMPLETED, zero COULD_NOT_RUN.** `DX-C-001` shows seven INDETERMINATE mode-mismatch rows, exactly as the README says it will. `DX-B-004` MISMATCH and `DX-B-007` / `DX-B-008` MATCH rows reproduce revision 1's observations unchanged. |

## New findings

Both ADVISORY. Neither blocks anything, and neither is a regression of preserved behaviour.

| ID | Sev | Finding | Smallest repair |
| --- | --- | --- | --- |
| **N-001** | ADVISORY | The new case DX-B-011 / evals id 11 grades on "the contradiction with REQ-004", asserting that revision 2 "accepts an account only for served postcodes and requires an immediate out-of-area rejection". The bytes the worker can see say only that a neighbour "is told immediately when the postcode is outside the served area" — notification, not refusal. The rejection reading is established in `fixtures/stale/PROD-001.md`'s revision-3 note ("Immediate rejection is no longer the accepted behaviour"), a fixture DX-B-011's `files` and `candidate_subpath` exclude. A worker that reads r2 carefully, concludes REQ-004 does not settle the question, and routes it as an uncovered scope question is behaving correctly and would still miss the stated expectation. | Widen the expectation in `cases.jsonl` DX-B-011 and `evals.json` id 11 to accept either reading — contradicting REQ-004, **or** a scope question REQ-004 does not settle — while still requiring it be recorded as a change request against PROD-001 rather than drawn as though permitted. **Do not edit `fixtures/shared/PROD-001.md`:** its bytes are identical to `fixtures/stale/preserved/PROD-001.r2.md` (`b863996b…`), the sentinel DX-B-008 A2 hard-codes. |
| **N-002** | ADVISORY | The trigger re-cut left **two** categories single-sided, not one: `negative_change` has one validation entry and no train entry, and `negative_define_product` now has one train entry (A7a) and no validation entry. The `revision_note` discloses only the first; `split_policy` still claims stratification by category without qualification, now true of six categories rather than eight. | Extend the `revision_note`'s known-limit sentence to name both categories and qualify `split_policy`, **or** add one query to each side to restore full stratification. Single-file edit either way. |

## Missing capabilities and evaluation prerequisites — unchanged

- **Skill-package structural inspection (S001–S013) and evidence reduction are not implemented in the DevForge CLI.** Every structural row in this recheck is `INSPECTION_MANUAL` with `authority: none`, and no decision receipt exists. Owner: DevForge integration owner.
- **Protected-manifest custody for the evaluation runner is not implemented in the DevForge CLI.** The runner, grader, runtime and case identities in every observations header are self-reported by the run. Owner: DevForge integration owner.
- **No installed or exported copy, no fresh terminal, no isolated workspace** was allocated for this recheck either. Tiers C, B and A remain `NOT_RUN` (F-012). Owner: coordinator and DevForgeAI integration owner.
- **The validator followed is itself unqualified** — a draft under bootstrap review, source-loaded, with no native evaluation of its own.

None of these is a defect in the candidate, and no edit to the candidate produces any of them.

## Decision and coverage

- **Disposition: insufficient evidence** — changed from **revise**.
- **Basis:** adjudicated by hand against the results contract; no implemented decision receipt exists. No applicable `FAIL` remains: the one FAIL that produced *revise* is resolved on both its criterion (R04) and its structural check (CHK-SPEC-01). What remains is missing observation, not observed failure.
- **Why not *suitable for the stated scope*:** tiers C, B and A are still `NOT_RUN` and behavioural status is still `NOT_EVALUATED`. No amount of source repair reaches that recommendation; it needs an allocated native evaluation.
- **Behavioural status:** `NOT_EVALUATED`.
- **Coverage:** intake, structure and independent review complete — structure now all PASS. C, B and A incomplete. Not blended into any figure.
- **Findings standing:** 1 MAJOR, 6 MINOR and 3 ADVISORY closed; 1 ADVISORY not applied and deliberately declined with the reason recorded; 2 new ADVISORY; 2 evaluation gaps unchanged. No BLOCKER at either revision.
- **Quality of the repair pass:** every applied change stayed inside the bounded scope, no forbidden target was touched, the counts and digests the author asserted were recomputed here and are correct, revision-1 error history was preserved rather than overwritten, and the one declined finding was declined explicitly with its reason.

## Recovery and continuation

- **Last completed phase:** P6 for this recheck.
- **Frozen input digests still matching:** yes. Candidate `b2827ce`, specification `4a90c0d5…`, validator `SKILL.md` `bdf665c7…`, runner `95ca2abf…` and graders `1b7a27a3…` all re-verified during this recheck.
- **Owned processes and workspace:** three `python3` runs completed and exited; no long-running process, no worktree created or held. Nothing was committed; the only untracked path is this recheck directory.
- **Next actions, in order:** (1) N-001 and N-002 are optional ADVISORY edits — the coordinator decides whether to spend another pass. (2) The only route out of `NOT_EVALUATED` is an allocated native evaluation: export or install the exact `b2827ce` candidate, then tier C, then B, then A. (3) The DevForge integration owner still owns both missing CLI capabilities and the question of whether a `devforge` subcommand should read a design-spec.
- **Conditions invalidating this report:** any change to the candidate package bytes or a new candidate revision; a change to SKILL-003 or the governing contracts; a change to the `devforge-evaluate-expert` package at `e641797`, including the pending `e101e76` recheck; a DevForge CLI revision adding structural inspection or evidence reduction; and the first native run of any tier.
