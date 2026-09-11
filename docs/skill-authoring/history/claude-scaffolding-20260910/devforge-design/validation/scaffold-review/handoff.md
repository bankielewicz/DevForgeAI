---
schema_version: "devforge.artifact/v1"
artifact_id: "HANDOFF-devforge-design-scaffold-review-20260910"
artifact_type: "handoff"
project_id: "devforgeai"
revision: 1
status: draft
created_at_utc: "2026-09-10T20:18:54Z"
producer:
  skill: "devforge-evaluate-expert (source-loaded, not installed)"
  skill_revision: "bdf665c7e18061395c0762de7a377fdc5f6ed48d66245df5623c5c32b90cf2ac (sha256 of the SKILL.md blob at claude-scaffold-evaluate-expert-20260910 commit e641797eebf04cd1e8eb9f711549e038e7745407; read with git show and by absolute path, not loaded by a client)"
execution_ref: null
upstream:
  - artifact_id: "EVREPORT-devforge-design-scaffold-20260910"
    revision: 1
    store: project
    path: "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-design/validation/scaffold-review/verification-results.md"
    sha256: "cdbf6022ab557e35a0a3df9898da2d4d58a7442fbfd0a640b26f55578f38ea4c"
    sections:
      - "Findings"
      - "Decision and coverage"
  - artifact_id: "CHGSPEC-devforge-design-scaffold-20260910"
    revision: 1
    store: project
    path: "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-design/validation/scaffold-review/skill-enhancement-spec.md"
    sha256: "04603be875ea2a788fe8ce23ec6d48a0014a3f1ee6dd9db2dbcbfc5927488c1e"
    sections:
      - "Change decision"
      - "Requested changes"
      - "Implementation order"
  - artifact_id: "SKILL-003"
    revision: 2
    store: project
    path: "docs/mvp/specifications/skill-003-devforge-design.md"
    sha256: "4a90c0d5648217480a4986518795dedd17bf3f62a67e433ec4d9d10e4247c8fb"
    sections:
      - "Workflow and phase exits"
      - "Rework, stopping, and recovery"
evidence:
  - path: "validation-results.json"
    sha256: "30ec3e3827773ff2e0aa42d4eccaa71cfd38caa6dfd105818851d577c9cc4a85"
  - path: "ai-review.json"
    sha256: "56d7d52474bbf05202ded00d46136c0ead6114a2c85bf07a4ae84f486e1218a1"
  - path: "findings.json"
    sha256: "d274779599f18e4aa24becffc7967c8bb9ff4a8a9f6517be2e83aa5d10dc5030"
  - path: "validation-plan.json"
    sha256: "3670bdb08f9a4fafaa4e875ab84e87d5c7a71c90da5769c441d7eaf0916b94d7"
supersedes: null
decision_ref: null
missing_inputs:
  - "Session assignment record: none exists. Scope came from the operator task packet at /home/bryan/Projects/DevForge/tmp/claude-remaining-skills-scaffolding-20260910/packets/evaluator-devforge-design.md, which is not a devforge.artifact session record."
  - "Installed or exported copy of the candidate: not generated. Blocks tier C."
  - "Fresh terminal, isolated workspace, per-attempt client-state isolation: not allocated. Blocks tiers A and B."
  - "Claude Code client version and model configuration: not observable from inside this session."
---

# Evaluator handoff: devforge-design (SKILL-003) scaffold review

## You are here

- **Skill and use case:** independent scaffold evaluation of the Claude `devforge-design` package against SKILL-003, returning evidence-bound results and a bounded repair specification to its author.
- **Current phase:** P6 complete. P1, P2, P3, P5 and P6 finished; P4 (tiers C, B, A) `NOT_RUN` with its cause.
- **Task state:** **complete as an evaluation, with three required evidence groups unobserved.** The evaluation itself finished; the candidate did not pass. Those are separate facts.
- **Session/worktree assignment:** none as a `devforge.artifact` record. Writes were confined to `docs/skill-authoring/history/claude-scaffolding-20260910/devforge-design/validation/scaffold-review/` inside worktree `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-design-20260910`. Nothing was committed. Nothing outside the fence was written, moved, reset, stashed or cleaned.
- **Exact candidate scope:** commit `9ad38de25a9941eb8ed67e9650430879f62032e4`, package `providers/claude/plugins/devforgeai/skills/devforge-design`, 23 files, `SKILL.md` sha256 `65dbb586ab78a43fa2b83a7e9c35f20272b3d4181ba08e6cc7519876de0e4c83`.
- **Existing authorisation carried forward:** none beyond the packet. This handoff authorises no edit, install, run or acceptance. Preparing it is not invoking anyone.

## Inputs consumed and outputs produced

This handoff is excluded from the table: it cannot contain its own complete-byte digest and does not list itself among its own outputs. Its digest is computed after saving and reading it back, and delivered in the terminal report.

Output paths are relative to `docs/skill-authoring/history/claude-scaffolding-20260910/devforge-design/validation/scaffold-review/` in worktree `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-design-20260910`.

| Direction | Artifact ID/revision | Store/path | SHA-256 | Relevant sections | Decision/freshness state |
| --- | --- | --- | --- | --- | --- |
| input | SKILL-003 @2 | `docs/mvp/specifications/skill-003-devforge-design.md` | `4a90c0d5648217480a4986518795dedd17bf3f62a67e433ec4d9d10e4247c8fb` | all eight sections | draft specification; current; matches the packet's declared digest |
| input | CANDIDATE-devforge-design @`9ad38de` | `providers/claude/plugins/devforgeai/skills/devforge-design/` | `SKILL.md` `65dbb586…`; full 23-file manifest in `commands.log` | whole package | frozen; unchanged during the evaluation |
| input | devforge-evaluate-expert @`e641797` | `providers/claude/plugins/devforgeai/skills/devforge-evaluate-expert/` in worktree `claude-scaffold-evaluate-expert-20260910` | `SKILL.md` `bdf665c7e18061395c0762de7a377fdc5f6ed48d66245df5623c5c32b90cf2ac` | SKILL.md; rubric; runner interface; missing-capabilities; results contract; assets templates | source-loaded, not installed; **draft under bootstrap review** (E2 → `e101e76` → recheck pending) |
| output | EVPLAN-devforge-design-scaffold-20260910 @1 | `validation-plan.json` | `3670bdb08f9a4fafaa4e875ab84e87d5c7a71c90da5769c441d7eaf0916b94d7` | frozen inputs; planned checks | draft; records a sequencing deviation |
| output | AIR-devforge-design-scaffold-20260910 @1 | `ai-review.json` | `56d7d52474bbf05202ded00d46136c0ead6114a2c85bf07a4ae84f486e1218a1` | criteria R01–R10; independence limits | draft |
| output | EVRESULTS-devforge-design-scaffold-20260910 @1 | `validation-results.json` | `30ec3e3827773ff2e0aa42d4eccaa71cfd38caa6dfd105818851d577c9cc4a85` | results; coverage; adjudication | draft |
| output | FINDINGS-devforge-design-scaffold-20260910 @1 | `findings.json` | `d274779599f18e4aa24becffc7967c8bb9ff4a8a9f6517be2e83aa5d10dc5030` | F-001 … F-013 | draft |
| output | EVREPORT-devforge-design-scaffold-20260910 @1 | `verification-results.md` | `cdbf6022ab557e35a0a3df9898da2d4d58a7442fbfd0a640b26f55578f38ea4c` | evidence groups; runner observations; findings; decision | draft |
| output | CHGSPEC-devforge-design-scaffold-20260910 @1 | `skill-enhancement-spec.md` | `04603be875ea2a788fe8ce23ec6d48a0014a3f1ee6dd9db2dbcbfc5927488c1e` | CHG-001 … CHG-011 | draft |
| output | raw runner observations and evaluator-added cases | `runner-out/` (7 files) | per-file digests in `verification-results.md` `evidence` | five runs, two case files | frozen |
| output | command log | `commands.log` | hashed after this evaluation closes; delivered in the terminal report | every command and its output | frozen |

## What changed and what remains open

**Nothing in the candidate changed.** The evaluator made no edit to the package, its specification, its cases or its expectations, and no gate was changed to let anything pass.

**Disposition: revise.** One applicable `FAIL` — rubric criterion R04 and specification-coverage check `CHK-SPEC-01`, both driven by F-001 — and the results contract gives *revise* for any applicable `FAIL`.

**Candidate findings:** BLOCKER 0, **MAJOR 1**, MINOR 6, ADVISORY 4. Two further findings (F-012, F-013) are evaluation gaps owned elsewhere and are excluded from those counts.

The one MAJOR: SKILL-003's rework rule *"Product-scope conflicts return to define-product via change"* has no transition anywhere in the package. The companion clause about routing uncertainty to a bounded prototype is implemented; this one is not, and the author's `spec-mapping.md` marks it addressed by citing the frontmatter exclusion line and four `should_trigger:false` trigger negatives — activation scope, not an in-workflow route.

**The package is substantially sound otherwise.** Nine of ten rubric criteria pass, nine of ten structural checks pass, all four template derivations verify byte-for-byte at the pinned revision, all 23 of the author's declared digests match an independently computed manifest, the DevForge command surface claim matches the binary's own help exactly, and all seven Claude client facts in `references/sources.md` match the page re-fetched on 2026-09-10. `verification-results.md` has a "What this evaluation found good" section naming the behaviour that must survive the repair.

**Still open, and not the author's to close:** tiers C, B and A are `NOT_RUN`; behavioural status is `NOT_EVALUATED`. Applying every requested change still leaves this candidate at *insufficient evidence* rather than *suitable for the stated scope*.

**One thing this evaluation closed for free:** the author recorded the evaluation runner as a PENDING dependency because it was uncommitted at authoring time. It is committed now at `e641797`, and all five of the author's open schema questions were settled by running it — including that the flag is `expect_equal` (not `expect_name_matches_folder`), that `candidate_subpath: "."` is accepted, and that a nested envelope key is addressable by its leaf name but not by a dotted path. CHG-007 and CHG-008 carry the answers.

## Observed verification

| Check | Outcome | Raw evidence / external receipt | Cause or scope limit |
| --- | --- | --- | --- |
| Candidate frozen identity | PASS | `commands.log`; 23-file manifest | HEAD equals the packet's commit; `git diff 9ad38de HEAD -- providers/` empty |
| Structure (10 manual checks) | 9 PASS, 1 FAIL | `validation-results.json` | Method `INSPECTION_MANUAL`; authority: none. The FAIL is `CHK-SPEC-01` |
| Independent review R01–R10 | 9 PASS, 1 FAIL | `ai-review.json` | Static reading; a static PASS does not establish that a session follows the instructions |
| Candidate case file runs | 5 runs, all exit 0 | `runner-out/run1…run5` | Local, non-isolated. Exit status describes the program, never the candidate |
| Tier C installed resources | NOT_RUN | — | No installed or exported copy; none to be generated under this assignment |
| Tier B output quality | NOT_RUN | — | No native run; the `without_skill` arm was not executed |
| Tier A discovery and activation | NOT_RUN | — | No fresh terminal, no installed package to discover, no per-attempt client-state isolation |
| Behavioural status | NOT_EVALUATED | — | Stays there until a real terminal evaluation is recorded |
| DevForge decision receipt | none produced | — | Evidence reduction is not implemented in the DevForge CLI; adjudicated by hand |

## Continuation directory

| Order | Task | Owner / skill | Prerequisites | Completion evidence |
| --- | --- | --- | --- | --- |
| 1 | Apply CHG-001 and CHG-003 — the two required repairs that close the specification-coverage `FAIL` and the resume gap | `devforge-design` scaffold author, under coordinator dispatch | `skill-enhancement-spec.md` at the digest above; the frozen candidate at `9ad38de`; the write fence for the package source | A new candidate revision with a new `SKILL.md` digest and an updated `file-manifest.json` |
| 2 | Apply CHG-002, CHG-004, CHG-005, CHG-006, then CHG-007, then CHG-008 through CHG-010 in the stated order | same | Order 1 landed; CHG-004 depends on both repairs; CHG-008 and CHG-009 depend on CHG-006 and CHG-007 | Updated package and authoring records |
| 3 | Decide CHG-011 — whether to add a `negative_change` trigger category, which re-cuts a fixed stratified split | coordinator | None; nothing is blocked on it | Recorded decision |
| 4 | Re-evaluate the new candidate revision statically and close findings only against new matching evidence | a fresh independent evaluator | Order 1 and 2 landed; the new candidate identity | A new EVREPORT that preserves this one's `FAIL` history |
| 5 | Allocate a native evaluation: export or install the exact candidate, then tier C, then B, then A | coordinator, with the DevForgeAI integration owner for install/export | An isolated workspace, a fresh terminal, per-attempt client-state isolation, subscription sign-in | Run manifests and case grades per attempt and arm; this is the only route out of `NOT_EVALUATED` |
| 6 | Decide whether a `devforge` subcommand should read a design-spec, resolve its upstream references and verify a mockup digest | DevForge integration owner | None | A Rust implementation decision; nothing in the candidate can supply it |

## Copyable next-session prompt

Goal: apply the two required repairs to the Claude devforge-design package so that SKILL-003's product-scope-conflict rework route and its interruption-and-resume rule are both carried in SKILL.md.

Context: read, in this order —
  /home/bryan/Projects/DevForge/worktrees/claude-scaffold-design-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-design/validation/scaffold-review/skill-enhancement-spec.md
    (sections "Change decision", then CHG-001 and CHG-003, then "Forbidden scope changes")
  /home/bryan/Projects/DevForge/worktrees/claude-scaffold-design-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-design/validation/scaffold-review/verification-results.md
    (sections "Findings" and "What this evaluation found good")
  /home/bryan/Projects/DevForge/framework/DevForgeAI/docs/mvp/specifications/skill-003-devforge-design.md
    (sections "Workflow and phase exits" and "Rework, stopping, and recovery")
  /home/bryan/Projects/DevForge/worktrees/claude-scaffold-design-20260910/providers/claude/plugins/devforgeai/skills/devforge-design/SKILL.md
    (sections "4. Iterate", "When something is missing or a check cannot run", "Stopping")

Output: edited SKILL.md in place at
  /home/bryan/Projects/DevForge/worktrees/claude-scaffold-design-20260910/providers/claude/plugins/devforgeai/skills/devforge-design/SKILL.md
plus an updated
  /home/bryan/Projects/DevForge/worktrees/claude-scaffold-design-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-design/authoring/file-manifest.json
recording the new digests.

Boundaries: write only inside the devforge-design package and its authoring evidence directory in that worktree. Do not edit SKILL-003, any docs/mvp contract or template, either assets/ file (both are byte-exact template copies), any fixture, or anything in the scaffold-review directory. Do not add a scripts/ directory. Do not install, export, run or evaluate anything. Keep SKILL.md well inside 500 lines. Preserve the behaviour listed under "Behaviour that must be preserved unchanged".

Verify: SKILL.md carries a product-scope-conflict route naming devforge-change and devforge-define-product with the not-installed caveat the package already applies to downstream siblings; SKILL.md carries an interruption-and-resume bullet; both assets/ files still hash to 5a30b17a40a52be8c1efb453415d0e77d3406c29c71674408a5506bf5e6ab661 and abc7f8e0ca545093d3b1486d1a86cb7e51609aef17c0027b951a47da6eaed206; the frontmatter still carries only name and description; no docs/mvp path, home path or backtick-bang syntax appears anywhere in the package.

No slash command is given here on purpose: neither `devforge-design` nor `devforge-project-expert-creator` is installed as a Claude skill, so this is a plain-language task for a dispatched author, not an invocation. `devforge` has no subcommand that reads or checks a design-spec, so no CLI verification step is offered either — the verify line above is what a person or a session can actually observe by reading bytes.

## Resume and custody

- **Task output readback:** all eight output records listed above were written, read back and hashed in this session; the digests in the table are those readback values. `runner-out/` holds five observations files and two evaluator-authored case files. This handoff is excluded.
- **This handoff's location:** `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-design-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-design/validation/scaffold-review/handoff.md`. No self-digest.
- **This handoff's external receipt:** its digest is computed after saving and reading it back and delivered in the terminal report. It is not inserted into this document, and this document is not modified to record it.
- **Worktree ownership disposition:** released. No worktree, branch or lock was created or held. The candidate worktree is untouched apart from this untracked evidence directory, and nothing was committed. Committing or discarding this directory is the coordinator's call.
- **External gate state:** none. No `devforge` command was run against this candidate, because none exists that applies to a skill package or a design-spec. Both missing-capability statements are recorded in `verification-results.md`.
- **Conditions invalidating this handoff:** any change to the candidate package bytes or a new candidate revision; a change to SKILL-003 or to any of the ten governing inputs; a change to the `devforge-evaluate-expert` package at `e641797`, including the pending `e101e76` recheck, which would rebind the rubric anchors and the runner interface this evaluation used; a DevForge CLI revision that adds skill-package structural inspection or evidence reduction; and the first native run of any tier, which supersedes the corresponding `NOT_RUN` row.
