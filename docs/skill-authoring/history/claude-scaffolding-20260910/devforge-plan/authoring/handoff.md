---
schema_version: "devforge.artifact/v1"
artifact_id: "HANDOFF-CLAUDE-PLAN-SCAFFOLD-001"
artifact_type: "handoff"
project_id: "devforgeai"
revision: 2
status: draft
created_at_utc: "2026-09-10T22:02:19Z"
producer:
  skill: "none - operator-author following the source-loaded Claude devforge-project-expert-creator at commit 4999f31"
  skill_revision: "not applicable; no skill was installed or invoked. The authored candidate's own SKILL.md digest at this revision is 3a50ee188a84738dbe6a6a8956526f1928afd7336b5e8b20bab12552ae81f64d"
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
  - artifact_id: "SCAFFOLD-REVIEW-devforge-plan"
    revision: 1
    store: project
    path: docs/skill-authoring/history/claude-scaffolding-20260910/devforge-plan/validation/scaffold-review/findings.json
    sha256: "read-only evaluator record; digest owned by its author, not recomputed or reasserted here"
    sections:
      - "F-001"
      - "F-002"
      - "F-003"
      - "F-004"
      - "F-005"
      - "F-006"
      - "F-007"
evidence: []
supersedes:
  artifact_id: "HANDOFF-CLAUDE-PLAN-SCAFFOLD-001"
  revision: 1
  source_revision: "03dc1a605acfb3ff80577f244d1a60f52244fb36"
  note: "Revision 1's bytes remain reachable at that commit. Superseded by repair pass 1."
decision_ref: null
missing_inputs:
  - "No session-record artifact exists for this assignment; the coordinator packet is the authorization and execution_ref is null."
  - "No DevForge CLI capability inspects planning artifacts; enforcement routes R1-R3 remain recorded requirements with feasibility unknown."
  - "No eval case stages an interrupted session, so the behaviour added for F-001 is instructed but unobserved."
---

# Authoring handoff: devforge-plan (SKILL-006), Claude scaffold — revision 2

Next owner: **an independent evaluator.** This is a prepared transfer, not a receiving invocation.

Revision 2 records repair pass 1. Revision 1 handed over the scaffold at `03dc1a6`; an independent
scaffold review of those bytes returned seven findings, and all seven were applied under coordinator
dispatch. **The findings are not closed by that.** Applying a change means the source was edited; the
evaluator has to evaluate the new bytes, and observations recorded against `03dc1a6` do not transfer.

## Result and next action

- **Result:** The Claude scaffold package for `devforge-plan`, thirty files, repaired at seven of thirty
  files from the independent review. `SKILL.md` now instructs the interruption-and-resume behaviour and
  the no-adopted-scope routing that SKILL-006 requires and revision 1 omitted; the case file's
  structural assertions are observable without an installed copy; the runner dependency is repinned to
  the revision actually used.
- **Why:** Two of the findings were coverage defects against the specification, not style — R04 was FAIL
  on both. The rest were eval-quality and provenance defects that made rows unable to fail, or made a
  record assert a dependency at a superseded revision.
- **Limits and blockers:** Nothing behavioural is known about these bytes, before or after the repair.
  Every workflow-item classification is still a proposed default. No DevForge command checks planning
  artifacts. No case stages an interrupted session, so the newly added behaviour is unobserved.
- **Next:** Reevaluate the repaired bytes. The seven findings need rechecking against revision 2, and
  the new `PL-PKG-001` / `PL-PKG-003` split means the four structural assertions are now obtainable in
  source mode without any installation.
- **Readiness:** Prepared. Tier C on an installed package still needs an installation the integration
  owner performs; tiers B and A still need an allocated workspace and a fresh terminal.
- **Validation status:** Not performed.
- **Behavioural status:** NOT_EVALUATED.
- **Enforcement status:** Requirements recorded; no gate implemented by this skill.

## Repair pass 1 at a glance

| Finding | Severity | Disposition | Where |
| --- | --- | --- | --- |
| F-001 interruption/resume instructed nowhere | MAJOR | applied | `SKILL.md:255`, `references/readiness-check.md:90`, `assets/handoff.md:31` |
| F-002 out-of-scope routing only in frontmatter | MINOR | applied | `SKILL.md:77` |
| F-003 `PL-PKG-001` gated mode-independent assertions | MINOR | applied | `evals/cases.jsonl:1` and new `:3` |
| F-004 three link assertions could not fail | MINOR | applied | `evals/cases.jsonl:2` |
| F-005 runner pinned at a superseded revision | MINOR | applied | `references/derivation.json:432` |
| F-006 `skill_revision` narrowing, no `missing_inputs` routing | ADVISORY | applied | `references/recording-rules.md:85` |
| F-007 handoff derivation omitted two removed rows | ADVISORY | applied | `references/derivation.json:196` |

Nothing was declined. One cascade (CHG-R08) followed F-001: the good handoff fixture gained the restored
row, so `PL-C-003`'s forbidden self-digest string was updated. Full table with verification evidence in
`authoring-notes.md` §"Repair pass 1".

## Outputs produced

This handoff is excluded: it cannot contain its own digest and does not list itself among its own
outputs. Package file digests are not repeated here — `file-manifest.json` holds all thirty and names
the seven that changed.

| Direction | Artifact | Store and path (absolute) | SHA-256 | State |
| --- | --- | --- | --- | --- |
| input | SKILL-006 rev 2 | `/home/bryan/Projects/DevForge/framework/DevForgeAI/docs/mvp/specifications/skill-006-devforge-plan.md` | `149a66a375da1bb3447f51b657996883974fec1dac3ce92af866eba94a378e4b` | governing; unmodified |
| input | Independent scaffold review of `03dc1a6` | `.../devforge-plan/validation/scaffold-review/` | not recomputed; the evaluator owns those records and they were read read-only | frozen; unmodified by this pass |
| input | Frozen builder, commit `4999f31` | `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-project-expert-creator-20260910` | SKILL.md `342b82923e64cef0c2ab77fdb8fc11b92fc68ea145642c486d2a937c5363f3d9` | source-loaded; draft under independent review; unmodified |
| input | Runner dependency, commit `e641797` | `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-evaluate-expert-20260910` | `run_cases.py` `95ca2abf77a5baf249694ad37d67a74949b567acd5164fd309724cbc576583e2`; `graders.py` `1b7a27a37e1fb8b2e36b1822bc23227c69e6300243e1b49b8caa848e3feca69f` | unmerged candidate; repinned this pass; unmodified |
| output | Candidate package (30 files, 7 changed) | `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-plan-20260910/providers/claude/plugins/devforgeai/skills/devforge-plan/` | per-file map in `file-manifest.json`; `SKILL.md` is `3a50ee188a84738dbe6a6a8956526f1928afd7336b5e8b20bab12552ae81f64d` | draft; unevaluated |
| output | Working design specification | `.../authoring/design/skill-design-spec.md` | `8ac68a221ac80635c9dfc77082fefd386e56cbf66687a91b4e1628828e66a119` | draft; unchanged by this pass |
| output | Authoring notes, with §"Repair pass 1" | `.../authoring/authoring-notes.md` | `73976890c64271ac7d634c21b055835c4af9347cf48b33fed3d0f1ba05327f9b` | draft |
| output | Specification coverage map, corrected | `.../authoring/spec-mapping.md` | `b53175555a7ff2d903b0e5a63d477263de38135c9156a0d2ce0ed1cdb5234d8a` | draft |
| output | Package file manifest, revision 2 | `.../authoring/file-manifest.json` | `bd3b66a8b289aff296f60fdacdd9ae760894bd74f3590db940e281c07b96da26` | draft |

Authoring directory root:
`/home/bryan/Projects/DevForge/worktrees/claude-scaffold-plan-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-plan/authoring/`

## Evidence and reading order

| Read when | Record | Purpose |
| --- | --- | --- |
| First | `file-manifest.json`, then the package's `SKILL.md` | Bind the exact revision-2 bytes and see which seven files moved |
| Second | `authoring-notes.md` §"Repair pass 1" | What each finding was verified against, what changed at file:line, and what was deliberately not closed |
| Third | `spec-mapping.md` §"Repair pass 1 — coverage changes" | The three coverage rows the review showed were wrong, and where they point now |
| Before judging a design choice | `design/skill-design-spec.md` §6 and §9 | The enforcement routes and the proposed defaults — unchanged by this pass |
| For provenance | `references/derivation.json` | Each changed file now carries `prior_destination_sha256_chain` to its revision-1 digest at `03dc1a6`, plus a `repair_pass_1` note |

## Proposed evaluation cases

| Check | Outcome | Evidence or receipt | Cause or scope limit |
| --- | --- | --- | --- |
| Tier C — installed resources and outputs | NOT_RUN | none | Still no installed copy or plugin export |
| Tier B — output quality against eleven authored cases | NOT_RUN | none | Still no clean-context run or `without_skill` baseline arm |
| Tier A — discovery and activation | NOT_RUN | none | Still no installed package in a fresh terminal |
| Deterministic runner over the repaired `evals/cases.jsonl` | NOT_RUN | none | The author must not produce observations about its own candidate. The file's compatibility with the `e641797` loader was rechecked statically |
| Reevaluation of the seven applied findings | NOT_RUN | none | This is the next owner's work; edits do not close findings |
| Interrupted-session behaviour added for F-001 | NOT_RUN | none | **No case stages it.** F-001's own rerun note asks for a new tier-B case; authoring one was outside this dispatch |
| DevForge check of any planning artifact | COULD_NOT_RUN | none | No such command exists at this revision |

## Copyable next task

`devforge-evaluate-expert` is **not installed** in this environment; it exists as an unmerged candidate
at `e641797`. So this is a plain-language task with resolvable absolute paths, not a slash command.

```text
Goal: A reevaluation of the repaired devforge-plan scaffold, or a stated prerequisite that blocks one.
Context: Read, in this order:
  /home/bryan/Projects/DevForge/worktrees/claude-scaffold-plan-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-plan/authoring/file-manifest.json
  /home/bryan/Projects/DevForge/worktrees/claude-scaffold-plan-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-plan/authoring/authoring-notes.md
  /home/bryan/Projects/DevForge/worktrees/claude-scaffold-plan-20260910/providers/claude/plugins/devforgeai/skills/devforge-plan/SKILL.md
  /home/bryan/Projects/DevForge/worktrees/claude-scaffold-plan-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-plan/validation/scaffold-review/findings.json
  /home/bryan/Projects/DevForge/framework/DevForgeAI/docs/mvp/specifications/skill-006-devforge-plan.md
Task: Bind the revision-2 bytes against the manifest, then recheck F-001 through F-007 against them
      and re-adjudicate R04. Observations recorded against 03dc1a6 do not transfer. The four
      structural assertions in PL-PKG-001 are now obtainable in source mode with no installation.
Preserve: the original severities and finding IDs; the proposed-default labels in
      design/skill-design-spec.md section 9, which are proposals and not user requirements; and
      every NOT_RUN label, none of which is a defect in the candidate.
Output: an evaluation record to a destination the operator assigns, plus a handoff back to the
      author. Do not edit the candidate.
Stop at: the recheck outcome, or the first prerequisite that blocks the observation you need.
```

Prerequisites the operator still owns:

```text
1. Install or export the candidate so tier C has a real installed package. PL-PKG-003 is
   unobservable without one.
2. Allocate a fresh terminal and an isolated workspace with a without_skill baseline arm for
   tiers B and A.
3. Decide the devforge-evaluate-expert dependency. It is now pinned at e641797 and rechecked
   there; if those scripts change again, recheck evals/cases.jsonl before any run.
```

## Retention and continuation limits

- **Output readback:** every path and digest above was read back after the last write; the package
  manifest was re-verified against the package bytes after the final edit. Excludes this handoff.
- **This handoff's location:** `.../authoring/handoff.md`. No self-digest.
- **This handoff's receipt:** computed after saving and delivered in the terminal response.
- **Worktree ownership:** retained by this author until the coordinator reassigns it. Branch
  `author/claude-devforge-plan-scaffold-20260910`.
- **External gate state:** none. No DevForge command was run against any project in either pass.
- **Conditions invalidating this handoff:** SKILL-006 is revised; a governing template or contract
  changes; the `e641797` runner bytes change; the candidate is edited again; or a DevForge
  planning-artifact capability is implemented.
- **Untouched by this pass:** the evaluator's records under `validation/scaffold-review/`, `docs/mvp/**`,
  every sibling skill, every Codex source, the plugin manifest, `hooks/`, `agents/`, and the companion
  DevForge repository.

Coordinator item, outside this fence: `docs/mvp/package-index.json` still records SKILL-006 as
`NOT_IMPLEMENTED` with a null Claude source.

**Validation status: Not performed.** A prepared transfer is not receiving execution and not acceptance.
