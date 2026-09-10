---
schema_version: "devforge.artifact/v1"
artifact_id: "HANDOFF-CLAUDE-PLAN-SCAFFOLD-001"
artifact_type: "handoff"
project_id: "devforgeai"
revision: 1
status: draft
created_at_utc: "2026-09-10T20:06:24Z"
producer:
  skill: "none - operator-author following the source-loaded Claude devforge-project-expert-creator at commit 4999f31"
  skill_revision: "not applicable; no skill was installed or invoked. The authored candidate's own SKILL.md digest is 32d6b7da3df53ce45d9bde1e82b100b09d87192f43be2cbd1bf2c9c8fd0c73c1"
execution_ref: null
upstream:
  - artifact_id: SKILL-006
    revision: 2
    store: project
    path: docs/mvp/specifications/skill-006-devforge-plan.md
    sha256: "149a66a375da1bb3447f51b657996883974fec1dac3ce92af866eba94a378e4b"
    sections:
      - "User goal and use-case inventory"
      - "Inputs and provenance"
      - "Workflow and phase exits"
      - "Outputs and standardized templates"
      - "Validation and behavioral acceptance"
      - "Rework, stopping, and recovery"
      - "Completion handoff"
evidence: []
supersedes: null
decision_ref: null
missing_inputs:
  - "No session-record artifact exists for this assignment; the coordinator packet is the authorization and execution_ref is null."
  - "No DevForge CLI capability inspects planning artifacts; enforcement routes R1-R3 are recorded requirements with feasibility unknown."
  - "The case runner and graders this package's evals/cases.jsonl targets are unmerged at commit e52ac59, with a repair pass in progress on that branch."
---

# Authoring handoff: devforge-plan (SKILL-006), Claude scaffold

Next owner: **an independent evaluator.** This is a prepared transfer, not a receiving invocation.

## Result and next action

- **Result:** A Claude scaffold package for `devforge-plan` was created where none existed. Thirty files:
  `SKILL.md`, three `assets/` output templates, three workflow `references/` plus two provenance records,
  and `evals/` with eleven tier-B cases, seventeen runner cases, twenty-seven trigger queries and
  seventeen synthetic fixture files.
- **Why:** No `devforge-plan` exists in the searched Claude inventory, none exists in Codex to port, and
  `package-index.json` records the Claude implementation as `NOT_IMPLEMENTED` with a null source. The
  decision was **create**, against a bounded search whose unsearched locations are named.
- **Limits and blockers:** Nothing behavioural is known about these bytes. Every workflow-item
  classification is a proposed default, because the assignment prohibited asking the user. No DevForge
  command checks planning artifacts, so the three enforcement requirements the design implies are
  recorded and routed rather than implemented.
- **Next:** Evaluate this candidate independently. Tier C first, then B, then A — the required C
  observations must pass before B or A admission for this candidate. The copyable task below is scoped
  to what can actually be done today.
- **Readiness:** Prepared, not ready to run end to end. Tier C on the installed package needs an
  installation the integration owner performs; the deterministic runner needs a decision about the
  unmerged `devforge-evaluate-expert` dependency.
- **Validation status:** Not performed.
- **Behavioural status:** NOT_EVALUATED.
- **Enforcement status:** Requirements recorded; no gate implemented by this skill.

## Outputs produced

This handoff is excluded: it cannot contain its own digest and does not list itself among its own
outputs. Package file digests are not repeated here — `file-manifest.json` holds all thirty.

| Direction | Artifact | Store and path (absolute) | SHA-256 | State |
| --- | --- | --- | --- | --- |
| input | SKILL-006 rev 2 | `/home/bryan/Projects/DevForge/framework/DevForgeAI/docs/mvp/specifications/skill-006-devforge-plan.md` | `149a66a375da1bb3447f51b657996883974fec1dac3ce92af866eba94a378e4b` | governing; unmodified |
| input | Frozen builder, commit `4999f31` | `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-project-expert-creator-20260910` | SKILL.md `342b82923e64cef0c2ab77fdb8fc11b92fc68ea145642c486d2a937c5363f3d9`; other files in `authoring-notes.md` | source-loaded; draft under independent review; unmodified |
| input | Runner dependency, commit `e52ac59` | `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-evaluate-expert-20260910` | `run_cases.py` `d1fb18689eeea31f8facde4e3de1507320e74ffb349f547f9db2201395bb132d`; `graders.py` `7c03e7b2137787035c995787b232a7bf8d801c88672675bacf4359a8cdb38c13` | unmerged candidate; repair in progress; unmodified |
| output | Candidate package (30 files) | `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-plan-20260910/providers/claude/plugins/devforgeai/skills/devforge-plan/` | per-file map in `file-manifest.json`; `SKILL.md` is `32d6b7da3df53ce45d9bde1e82b100b09d87192f43be2cbd1bf2c9c8fd0c73c1` | draft; unevaluated |
| output | Working design specification | `.../authoring/design/skill-design-spec.md` | `8ac68a221ac80635c9dfc77082fefd386e56cbf66687a91b4e1628828e66a119` | draft |
| output | Authoring notes | `.../authoring/authoring-notes.md` | `f68e9f1e35ed15b250faac110e9816aab9d8f23b9a624185838dac7439adf872` | draft |
| output | Specification coverage map | `.../authoring/spec-mapping.md` | `ecfa4b70f46b783d23c9a8d20f8b129d062bf0c2c3d3f09ae893fbe43e9db55e` | draft |
| output | Package file manifest | `.../authoring/file-manifest.json` | `fef20fddc4d3d76b8328697e4bc2ee5d6b1eeab19028046a0619efcbd6755538` | draft |

Authoring directory root:
`/home/bryan/Projects/DevForge/worktrees/claude-scaffold-plan-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-plan/authoring/`

## Evidence and reading order

| Read when | Record | Purpose |
| --- | --- | --- |
| First | `file-manifest.json`, then the package's `SKILL.md` | Bind the exact candidate bytes, then read what it instructs |
| Second | `spec-mapping.md` | Every SKILL-006 row mapped to a file, a section and an eval case ID — the fastest route to an uncovered requirement |
| Before judging a design choice | `design/skill-design-spec.md` §6 (enforcement routes R1–R3), §9 (search scope, proposed defaults) | Separates what the specification required from what the author proposed |
| Before running anything | `authoring-notes.md` §"Dependency", §"Static self-checks" | The two invocation groups, the unmerged runner, and exactly what the author's own checks were and were not |
| For provenance | package `references/derivation.json`, `references/sources.md` | Where each copy came from, what makes it stale, and which external claims were actually retrieved |

## Proposed evaluation cases

Authored, not executed. They live in the package's `evals/`: eleven tier-B cases in `evals.json` (one per
SKILL-006 acceptance row, one per additional common case, plus revise-not-regenerate and the
capability-gap case), seventeen runner cases in `cases.jsonl`, and twenty-seven tier-A trigger queries in
`triggers/trigger-queries.json` with a fixed split stratified by category.

| Check | Outcome | Evidence or receipt | Cause or scope limit |
| --- | --- | --- | --- |
| Tier C — installed resources and outputs | NOT_RUN | none | No installed copy or plugin export exists |
| Tier B — output quality against eleven authored cases | NOT_RUN | none | Requires a run in a clean context with a `without_skill` baseline arm |
| Tier A — discovery and activation | NOT_RUN | none | Requires an installed package in a fresh terminal |
| Deterministic runner over `evals/cases.jsonl` | NOT_RUN | none | The runner is unmerged at `e52ac59` and under repair; the author must not produce observations about its own candidate |
| DevForge check of any planning artifact | COULD_NOT_RUN | none | No such command exists at this revision. This is the missing integration, not a scheduling problem |
| Author's static self-checks (parse, links, line count, no home paths, fixture field lists) | passed as authoring checks | `authoring-notes.md` §"Static self-checks" | Confirms the author's own writes landed. **Not** a tier result and not `PASS` for any required check |

## Copyable next task

The receiving skill `devforge-evaluate-expert` is **not installed** in this environment; it exists only
as an unmerged candidate on another branch. So this is a plain-language task with resolvable absolute
paths rather than a slash command.

```text
Goal: An independent evaluation record for the devforge-plan Claude scaffold, or a stated
      prerequisite that blocks one.
Context: Read, in this order:
  /home/bryan/Projects/DevForge/worktrees/claude-scaffold-plan-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-plan/authoring/file-manifest.json
  /home/bryan/Projects/DevForge/worktrees/claude-scaffold-plan-20260910/providers/claude/plugins/devforgeai/skills/devforge-plan/SKILL.md
  /home/bryan/Projects/DevForge/worktrees/claude-scaffold-plan-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-plan/authoring/spec-mapping.md
  /home/bryan/Projects/DevForge/worktrees/claude-scaffold-plan-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-plan/authoring/authoring-notes.md
  /home/bryan/Projects/DevForge/framework/DevForgeAI/docs/mvp/specifications/skill-006-devforge-plan.md
Task: Bind the candidate bytes against the manifest, then assess the package against SKILL-006.
      Judge the four workflow phases and their exit conditions, the description's activation
      boundary against the three named siblings, the nine acceptance cases, and whether the
      three enforcement requirements are recorded rather than simulated. Return bounded findings
      with severities and stable finding IDs.
Preserve: the proposed-default labels in design/skill-design-spec.md section 9 - they are the
      author's proposals, not user requirements, and grading them as requirements would be wrong.
      Preserve every NOT_RUN label; none of them is a defect in the candidate.
Output: an evaluation record to a destination the operator assigns, plus a handoff back to the
      author. Do not edit the candidate.
Stop at: bounded findings, or the first prerequisite that blocks the observation you need -
      naming it rather than substituting a weaker one.
```

Two prerequisites the operator owns before any run:

```text
1. Install or export the candidate so tier C has a real installed package.
   Neither was done here; installation is not the author's action.
2. Decide the devforge-evaluate-expert dependency: use the e52ac59 bytes as-is, or wait for the
   repair pass. If those scripts change, evals/cases.jsonl must be rechecked against the new
   grader registry and case schema before it is run.
```

## Retention and continuation limits

- **Output readback:** every path and digest in the outputs table was read back after the last write;
  the package manifest was re-verified against the package bytes after the final edit. Excludes this
  handoff.
- **This handoff's location:** `.../authoring/handoff.md`. No self-digest.
- **This handoff's receipt:** its digest is computed after saving and delivered in the terminal response,
  not written into this document.
- **Worktree ownership:** retained by this author until the coordinator reassigns it. Branch
  `author/claude-devforge-plan-scaffold-20260910`, base `c17e758417da64928a0f47fc2600304465ac3f3c`.
- **External gate state:** none. No DevForge command was run against any project.
- **Conditions invalidating this handoff:** SKILL-006 is revised; a governing template or contract
  changes; the `e52ac59` runner bytes change; the candidate is edited; or a DevForge planning-artifact
  capability is implemented.

Coordinator item, outside this fence: `docs/mvp/package-index.json` still records SKILL-006 as
`NOT_IMPLEMENTED` with a null Claude source. That update belongs to the integration owner and was
deliberately not made here.

**Validation status: Not performed.** A prepared transfer is not receiving execution and not acceptance.
This document authorises no evaluation, installation, activation or automatic invocation of a receiver.
