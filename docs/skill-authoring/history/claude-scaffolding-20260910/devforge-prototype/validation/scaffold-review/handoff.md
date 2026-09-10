---
schema_version: "devforge.artifact/v1"
artifact_id: "HANDOFF-EVAL-004-SCAFFOLD-01"
artifact_type: "handoff"
project_id: "DevForgeAI"
revision: 1
status: draft
created_at_utc: "2026-09-10T21:23:19Z"
producer:
  skill: "devforge-evaluate-expert"
  skill_revision: "bdf665c7e18061395c0762de7a377fdc5f6ed48d66245df5623c5c32b90cf2ac"
  skill_revision_note: "sha256 of the one SKILL.md file source-loaded from commit e641797eebf04cd1e8eb9f711549e038e7745407. Not a package digest and not a plugin version."
execution_ref: null
upstream:
  - artifact: "SKILL-004"
    revision: 2
    store: "project"
    path: "/home/bryan/Projects/DevForge/framework/DevForgeAI/docs/mvp/specifications/skill-004-devforge-prototype.md"
    sha256: "e4f61c35220641f053a828615df1bc3415c707fde26fcf8b0cdece6cdb1ba54c"
  - artifact: "devforge-prototype candidate package"
    revision: "e199230858d871926fff2d55de8b015fa0ce335e"
    store: "worktree /home/bryan/Projects/DevForge/worktrees/claude-scaffold-prototype-20260910"
    path: "providers/claude/plugins/devforgeai/skills/devforge-prototype/"
evidence:
  - path: "runner-out/candidate-cases.observations.jsonl"
    sha256: "f0e57b1298931e41dcff55dff46f761bc5cb1ff4f16a934f2d9c017b9733ed24"
  - path: "runner-out/evaluator-structural.observations.jsonl"
    sha256: "ee64109c2bbd87bd9dad2a9d2e57ca8c817c0bb1f845e85537f9d23abaccca97"
  - path: "runner-out/probe-candidate-root-is-package.observations.jsonl"
    sha256: "2452d3923e7ac8d6c879ede110194c31b41f5e53c38a631f11c2a9b319761237"
  - path: "runner-out/probe-mode-installed.observations.jsonl"
    sha256: "4e9562102b5c7ef866657877d041d9759dcbc1f437cea7ca113ee8d5104e4b29"
  - path: "commands.log"
    sha256: "3e2004672cd180302e40577451a19c589f80dffe353443808bdd56057f930e85"
supersedes: null
decision_ref: null
missing_inputs:
  - "No installed or exported copy of the candidate. Blocks tier C and the installed-mode evals/ absence observation."
  - "No fresh terminal and no permitted isolated workspace. Blocks tiers A and B."
  - "No session record for this evaluation. execution_ref is null; its absence establishes no ownership."
---

# Skill handoff — scaffold evaluation of devforge-prototype (SKILL-004), returning to the author

## You are here

- **Skill and use case:** `devforge-evaluate-expert` — evaluate an existing skill package against its governing
  specification and return evidence-bound results with a bounded repair specification for its author.
- **Current phase:** P6 (return). P1–P3 and P5 completed; P4 (native tiers) `NOT_RUN` with cause.
- **Task state:** **complete as an evaluation, with named gaps.** Every observation that could be made from
  reading and from deterministic runs was made and recorded; every observation that needed an installed copy
  or a terminal was not attempted and carries its actual cause. This document's own `status` is `draft` —
  that is the document's state, not the task's, and producing this report is not accepting it.
- **Session/worktree assignment:** independent evaluator under a coordinator. No SESSION record exists;
  `execution_ref` is null and its absence establishes no ownership. Read-only on two frozen worktrees; writes
  confined to this directory.
- **Exact candidate or artifact scope:**
  `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-prototype-20260910/providers/claude/plugins/devforgeai/skills/devforge-prototype/`
  at commit `e199230858d871926fff2d55de8b015fa0ce335e`, 31 files, manifest digest
  `6bd15a3ead18037682c70168752c66e838b2d536c2130462d8842acc5eb4ee6f`. **Not installed anywhere.**
- **Existing authorization carried forward:** the coordinator's evaluation assignment only. This evaluation
  accepted, adopted, installed and released nothing, and requests no new permission.

## What changed and what remains open

**Outcome: `revise`.** One MAJOR, four MINOR, one ADVISORY, no BLOCKER. Behaviour `NOT_EVALUATED`; tiers C, B
and A all `NOT_RUN`.

The package is in good shape. Frontmatter carries exactly `name` and `description`; `name` equals the folder
name; all seven local links resolve in-package; all six routed resources are present; both output templates
are byte-identical copies of the governing `docs/mvp` templates and the handoff is a recorded bounded
adaptation; all 11 `derivation.json` destination digests and all 9 governing-input digests re-hash correctly;
no `docs/mvp`, home-directory or cross-package runtime dependency exists; the description is well inside the
1,536-character budget; there is no Codex-only concept and no Claude `!`-injection syntax; no held-out answer
leaks into the shipping files; the trigger split is fixed and stratified with every category carrying both
arms; every SKILL-004 acceptance row and common case is instructed and has a tier-B case; every DevForge
command the package names exists in the binary's own `--help`, with `isolate`'s real limit stated rather than
oversold; and the four controls the workflow would need are recorded as open requirements for the integration
owner rather than simulated.

**What drives the `revise`:**

1. **F-002 (MAJOR).** Eval case XB-8 declares `baseline_comparison: "old_skill"` when no previous revision of
   this skill exists at base `c17e758` — verified with `git ls-tree`. One of the specification's four required
   common cases therefore has no runnable comparison arm. The package's own `spec-mapping.md` says "No baseline
   existed", so the record contradicts itself. The author's proposed fallback (`NOT_APPLICABLE`) would also
   misuse the fixed vocabulary. One-token repair: `"without_skill"`.
2. **F-003 (MINOR, R08 FAIL).** `SKILL.md:50` tells a session that hashing the plan lets a later reader tell
   the plan preceded the evidence — which `references/framework-context.md:33` explicitly denies — and routes
   the reader for the limitation to `references/experiment-boundaries.md`, which contains no such statement.
   Two-sentence repair.

**Also open:** F-001 (tier labels in `cases.jsonl` name the tier the fixture simulates; no deterministic case
observes the package or an installed copy), F-004 (the recorded runner pin `e52ac59` is a superseded,
since-repaired revision), F-005 (the `--candidate` root the cases require is written down nowhere, and the
natural wrong value produces nine `COULD_NOT_RUN` rows at exit 0), F-006 (ADVISORY: fixture filenames and
their internal `artifact_id` values use different numbers).

**Unresolved and not this evaluation's to settle:** whether the coordinator wants the native arms run at all
before the repairs land, and which revision of `devforge-evaluate-expert` the next evaluation will be given
(F-004's forward pin depends on it).

## Inputs consumed and outputs produced

This handoff is excluded from the table: it cannot contain its own complete-byte digest and does not list
itself among its own outputs. Every digest below was computed after the file's bytes were final.

| Direction | Artifact ID and revision | Store and path | SHA-256 | Relevant sections | State |
| --- | --- | --- | --- | --- | --- |
| input | SKILL-004 rev 2 | `framework/DevForgeAI/docs/mvp/specifications/skill-004-devforge-prototype.md` | `e4f61c35220641f053a828615df1bc3415c707fde26fcf8b0cdece6cdb1ba54c` | all sections | draft (per its own header) |
| input | devforge-prototype candidate @ `e199230` | candidate worktree, `providers/claude/plugins/devforgeai/skills/devforge-prototype/` | manifest `6bd15a3ead18037682c70168752c66e838b2d536c2130462d8842acc5eb4ee6f` | whole package, 31 files | frozen; unchanged by this evaluation |
| input | devforge-evaluate-expert @ `e641797` (workflow, rubric, runner, templates) | validator worktree, `providers/claude/plugins/devforgeai/skills/devforge-evaluate-expert/` | `SKILL.md` `bdf665c7e18061395c0762de7a377fdc5f6ed48d66245df5623c5c32b90cf2ac`; `run_cases.py` `95ca2abf77a5baf249694ad37d67a74949b567acd5164fd309724cbc576583e2`; `graders.py` `1b7a27a37e1fb8b2e36b1822bc23227c69e6300243e1b49b8caa848e3feca69f` | P1–P6, R01–R10, runner interface, results contract, output templates | source-loaded, never installed; **draft under bootstrap review, unevaluated** |
| output | EVPLAN-004-SCAFFOLD-01 | `validation-plan.json` | `a864bc73eae707b98e5d8d1207d0d88db8371ffc1a31be32f848ca24d1e74243` | frozen inputs, planned checks, declared expectations | frozen before the runs |
| output | (P3 record) | `ai-review.json` | `706fe8a8dab924ffcd695ef40ad559d4856388989698ff1ca9c79b29d5750d5d` | R01–R10 | complete; independence limits recorded |
| output | (P5 record) | `validation-results.json` | `382b1f74a54a9eb13fc7913202acc672e2b39e3f2ccd5c0ff9b2fe177d4c92ae` | 26 planned checks, group outcomes, disposition | complete |
| output | EVREPORT-004-SCAFFOLD-01 | `verification-results.md` | `2939cfc197b8f47abd61158b7b8e7ce390f578203e4b60bc2014215f6001d309` | identity, evidence groups, runner tables, coverage, R01–R10, findings, decision, limits | draft |
| output | (findings, machine-readable) | `findings.json` | `5fb80dff124e6f21af6f9c227a308609ad6c0ab5f37406a1a8b88b2526ed5393` | F-001..F-006, prerequisites, tiers | complete |
| output | CHGSPEC-004-SCAFFOLD-01 | `skill-enhancement-spec.md` | `1e076a070b129a1cd9f0e3e542adf3989817113723d6d5dc85cd41c974def294` | CHG-001..CHG-006, preserved behaviour, forbidden scope | draft |
| output | (raw evidence) | `runner-out/candidate-cases.observations.jsonl` | `f0e57b1298931e41dcff55dff46f761bc5cb1ff4f16a934f2d9c017b9733ed24` | 9 case records | frozen |
| output | (raw evidence) | `runner-out/evaluator-structural-cases.jsonl` | `e539c5f6d2987d203897f812e583061d362bfda49f79ea7245edf412190258a9` | 10 evaluator-added cases | frozen |
| output | (raw evidence) | `runner-out/evaluator-structural.observations.jsonl` | `ee64109c2bbd87bd9dad2a9d2e57ca8c817c0bb1f845e85537f9d23abaccca97` | 10 case records | frozen |
| output | (raw evidence) | `runner-out/probe-candidate-root-is-package.observations.jsonl` | `2452d3923e7ac8d6c879ede110194c31b41f5e53c38a631f11c2a9b319761237` | F-005 evidence | frozen |
| output | (raw evidence) | `runner-out/probe-mode-installed.observations.jsonl` | `4e9562102b5c7ef866657877d041d9759dcbc1f437cea7ca113ee8d5104e4b29` | F-001 evidence | frozen |
| output | (candidate identity) | `candidate-manifest.txt` | `6bd15a3ead18037682c70168752c66e838b2d536c2130462d8842acc5eb4ee6f` | 31 `{sha256, path}` rows | frozen |
| output | (command record) | `commands.log` | `3e2004672cd180302e40577451a19c589f80dffe353443808bdd56057f930e85` | P1 orientation (reconstructed) through P6 | finalised before this handoff was written |

No copy of the candidate, no installed package and no export was produced. Nothing outside this directory was
written, and nothing was committed.

## Observed verification

| Check | Outcome | Raw evidence or external receipt | Cause or scope limit |
| --- | --- | --- | --- |
| Candidate identity frozen and unchanged | PASS | `commands.log` §P1; `candidate-manifest.txt` | Self-reported identity; no protected manifest binds it |
| Runner and graders equal the frozen commit's bytes | PASS | `commands.log` §P1 | Verified by digest against `git show`; still not protected-manifest custody |
| Structural observations (11 rows) | 10 PASS, 1 FAIL | `runner-out/evaluator-structural.observations.jsonl`; `commands.log` §P2 | Method `INSPECTION_MANUAL`, authority none. FAIL is F-002 |
| Candidate's 9 authored deterministic cases | completed; 13/13 assertions agree with their authored expectations | `runner-out/candidate-cases.observations.jsonl` | Local, non-isolated evidence. Observes fixtures, not the candidate package (F-001) |
| Evaluator-added structural cases (10) | completed; all agree with their declared expectations | `runner-out/evaluator-structural.observations.jsonl` | Authored by this evaluation after seeing the candidate; structural facts only, grades nothing |
| Independent review R01–R10 | 9 PASS, 1 FAIL (R08) | `ai-review.json` | Fresh evaluator context, but P2/P3 shared a context and author records were read before completion |
| Tier C — installed resources | NOT_RUN | none | No installed or exported copy was allocated; installation was not attempted |
| Tier B — output quality vs `without_skill` | NOT_RUN | none | No fresh terminal and no permitted isolated workspace were allocated |
| Tier A — discovery and activation | NOT_RUN | none | No fresh terminal and no installed inventory; not observable by reading |
| Behavioural conformance | NOT_EVALUATED | none | Nothing here observes a session finding, loading or following this skill |

`NOT_RUN` means planned and unattempted. `COULD_NOT_RUN` with the actual cause is what a blocked required
observation gets. `NOT_APPLICABLE` is only for a stated scope exclusion. The absence of an error is not a
pass, and no row above supports a claim about how this skill behaves.

**Enforcement status:** requirements recorded; **no gate was implemented, run or claimed by this evaluation**.
Two DevForge CLI capabilities this workflow would otherwise use do not exist, and both statements are recorded
verbatim in `verification-results.md` and `validation-results.json`: skill-package structural inspection
(S001–S013) and evidence reduction are not implemented in the DevForge CLI; and protected-manifest custody for
the evaluation runner is not implemented in the DevForge CLI. Both are evaluation prerequisites owned by the
DevForge integration owner and neither is a defect in this candidate.

**Validation status:** this is a static and deterministic evaluation. Nothing was independently checked by a
second reviewer, and a self-run measurement is not an independent check. The instrument itself
(`devforge-evaluate-expert` at `e641797`) is a draft under bootstrap review — E2 returned *revise* at
`e52ac59`, repairs landed at `e101e76`, the focused recheck closed F-001..F-009 and opened a new MINOR F-R01,
and `e641797` regenerated its derivation digests — and has never been natively evaluated. It is unqualified,
and no result here inherits authority from it.

## Continuation directory

| Order | Task | Owner or skill | Prerequisites | Completion evidence |
| --- | --- | --- | --- | --- |
| 1 | Apply CHG-002 (baseline arm) and CHG-003 (freeze claim and its pointer) — the two changes behind the `revise` | **the author of this scaffold**, under coordinator dispatch | `skill-enhancement-spec.md`; write access to the candidate's own worktree and branch | a new candidate commit and a changed 31-file manifest; the author reports the changed files and the new identity without running validation |
| 2 | Apply CHG-005, then CHG-001 (record the `--candidate` roots, then add cases that observe the package) | same | order matters: CHG-005 first | `evals/` updated; the nine existing rows still reproduce exactly |
| 3 | Confirm the forward runner pin with the coordinator, then apply CHG-004 | same, with the coordinator | which `devforge-evaluate-expert` revision the next evaluation gets | `runner_dependency` naming a revision whose script digests match |
| 4 | Decide CHG-006 (ADVISORY) — align fixture filenames with their artifact IDs, or add the README sentence | same | none | either the aligned files or the README sentence |
| 5 | Allocate an installation or export and an isolated workspace, then run tier C, then B, then A on the repaired candidate | coordinator / DevForge integration owner, then an evaluator | a fresh terminal, an installed or exported copy, a permitted workspace | run manifests and case grades per tier, reported separately and unblended |
| 6 | Report the undocumented `--candidate` convention in the `devforge-evaluate-expert` package | coordinator, to that package's owner | none | a finding filed against that package |

Most of the DevForge roster is specified but not implemented, so check what is actually installed before naming
a skill rather than reading a name off the roster. **No `devforge-prototype` is installed anywhere**, and
neither is `devforge-evaluate-expert`; both exist only as provider source. Where the natural consumer is
absent, the task above is stated in plain language rather than as a slash command.

**A note on the next owner.** The validator's own default next owner for a repair specification is
`devforge-project-expert-creator`. The assignment overrides that here: the repairs are edits to a framework
scaffold, returning to its author under coordinator dispatch, not a generated-expert repair cycle. The
substitution is recorded so it is visible rather than silent.

## Copyable next task

Plain-language, not a slash command: `devforge-prototype` is not installed, `devforge-evaluate-expert` is not
installed, and this handoff does not present a fictional command as runnable.

```text
Goal: Apply the two changes behind the revise disposition to the Claude devforge-prototype scaffold.
Context: /home/bryan/Projects/DevForge/worktrees/claude-scaffold-prototype-20260910/docs/skill-authoring/
         history/claude-scaffolding-20260910/devforge-prototype/validation/scaffold-review/
         Read skill-enhancement-spec.md (CHG-002 and CHG-003) and, for the evidence behind them,
         verification-results.md sections "Findings" and "Independent review R01-R10" (criterion R08).
Task:  CHG-002 - in evals/evals.json, case 8 (placeholder-in-required-field-stays-a-draft), change
         "baseline_comparison": "old_skill" to "without_skill". No Claude devforge-prototype exists at
         base c17e758417da64928a0f47fc2600304465ac3f3c, so no old_skill arm can exist.
       CHG-003 - in SKILL.md line 50, stop asserting that hashing the plan establishes to a later reader
         that it preceded the evidence (references/framework-context.md line 33 denies exactly that), and
         repoint the "what a freeze does and does not establish" link at text that actually says it;
         optionally add that one sentence to references/experiment-boundaries.md "Measurement before result".
Preserve: the candidate at e199230858d871926fff2d55de8b015fa0ce335e as the prior identity; all three
       assets/ templates byte-for-byte; the nine existing cases in evals/cases.jsonl with their
       candidate_subpath values and assertions; the sentinel digest
       f9138601783d24d2a3dd8170db7b510c557ec22d906b76afc7707aa5be8e223f and the preserved baseline fixture;
       the 22 trigger queries and their fixed train/validation split; frontmatter of name and description only.
Do not: edit the specification, the docs/mvp templates, the shared contracts, the roster, a sibling skill,
       or the DevForge CLI, its policy, its tests or its tooling_files pins; add scripts/ or any executable
       implementation to this package; weaken or delete an eval case or expectation; claim any tier ran.
Output: the edited candidate in its own worktree and branch, plus a report of the changed files and the new
       candidate identity. Do not run validation and do not close a finding - a changed candidate is a new
       identity and needs new matching evidence.
Stop at: those two changes applied and reported, or the first point where a preserved item would have to
       change to proceed.
```

## Retention and continuation limits

- **Output readback:** the thirteen files listed in the outputs table above — every file in this directory
  except this handoff — each read back and hashed after
  its bytes were final; every JSON and JSONL record re-parsed successfully. This handoff is excluded.
- **This handoff's location:** saved at
  `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-prototype-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-prototype/validation/scaffold-review/handoff.md`.
  No self-digest.
- **This handoff's receipt:** its digest is computed after saving and reading it back, and delivered in the
  terminal response to the coordinator. It is not written into this document.
- **Worktree ownership:** none taken. No worktree was created, switched, reset, cleaned, stashed, rebased or
  released; both frozen worktrees were read only, and both were clean at their expected commits at the start
  and at the end.
- **External gate state:** none. No `devforge` command was run against any project, policy or state
  directory; only `--help` was inspected. No phase state, no receipt, no accepted snapshot.
- **Conditions invalidating this handoff:** any change to the candidate's 31-file manifest; any change to
  `docs/mvp/specifications/skill-004-devforge-prototype.md`; any change to the frozen validator or its
  `scripts/run_cases.py` / `scripts/graders.py`; any change to the eval fixtures; or the appearance of an
  installed or exported copy — which would make tiers C, B and A observable and would supersede their
  `NOT_RUN` rows rather than confirming them.

Retain the exact referenced bytes and every recorded failure. A `FAIL` here is a finding to be repaired and
re-observed, not a record to be tidied away, and no later revision may quietly replace an expectation it was
measured against.

A prepared handoff is not a receiving invocation and it is not acceptance. This document authorises no edit to
the candidate by this evaluator, no installation, no adoption and no release. **`revise` is a recommendation
supporting someone else's decision.**
