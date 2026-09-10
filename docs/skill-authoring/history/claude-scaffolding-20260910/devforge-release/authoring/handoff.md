---
schema_version: "devforge.artifact/v1"
artifact_id: "HANDOFF-REL-SCAFFOLD-001"
artifact_type: "handoff"
project_id: "devforgeai"
revision: 1
status: draft
created_at_utc: "2026-09-10T20:06:37Z"
producer:
  skill: "devforge-project-expert-creator (source-loaded at 4999f3106565c5e320d1f1a7db066b437e4e94be; not installed and not invoked as a skill)"
  skill_revision: "342b82923e64cef0c2ab77fdb8fc11b92fc68ea145642c486d2a937c5363f3d9 (SHA-256 of that package's SKILL.md file bytes at that commit)"
execution_ref: null
upstream:
  - artifact_id: SKILL-011
    revision: 2
    store: project
    path: docs/mvp/specifications/skill-011-devforge-release.md
    sha256: "f94261d7af37d8c68510e88d4b8705447b06ce396ead5776c28c7502cf60585d"
    sections:
      - "User goal and use-case inventory"
      - "Inputs and provenance"
      - "Workflow and phase exits"
      - "Outputs and standardized templates"
      - "Validation and behavioral acceptance"
      - "Rework, stopping, and recovery"
  - artifact_id: skill-authoring-contract
    revision: 3
    store: project
    path: docs/mvp/skill-authoring-contract.md
    sha256: "371462385b4e32d1b347f959abb779f4be4251e357c5720a9aef039113eb4b53"
    sections:
      - "Per-skill structure and distribution"
      - "Three separately reported evaluation tiers"
evidence:
  - "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-release/authoring/file-manifest.json"
  - "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-release/authoring/authoring-notes.md"
  - "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-release/authoring/spec-mapping.md"
  - "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-release/authoring/design/skill-design-spec.md"
supersedes: null
decision_ref: null
missing_inputs:
  - "execution_ref: no session-record artifact was supplied for this authoring assignment. The scope came from the coordinator packet. A worker-authored session ID would not be proof of ownership, so this stays null."
  - "The Python JSONL runner and deterministic graders that evals/cases.jsonl targets are pinned at commit e52ac596cbf790dfa156d883852d392c512fdbcc in the devforge-evaluate-expert worktree and are installed nowhere. A repair pass is in progress on that branch."
  - "No Claude Code client version was observed. Every client-behaviour claim in the package comes from the published documentation retrieved 2026-09-10 and is labelled as such."
---

# Authoring handoff: devforge-release (Claude, SKILL-011 scaffold)

## Result and next action

- **Result:** A new Claude skill package, `providers/claude/plugins/devforgeai/skills/devforge-release`, authored from SKILL-011 revision 2. 24 files: `SKILL.md`, two assets, four references, and an `evals/` tree of authored cases, fixtures and trigger queries. Complete as a scaffold. Its exact identity is `file-manifest.json`, in the evidence table below.
- **Why:** No `devforge-release` existed in either provider's inventory at base `c17e758417da64928a0f47fc2600304465ac3f3c`, so this is original authoring rather than a port, and the selection decision was **create**. The search scope and its limits are in the design document section 9 - the honest result is "no suitable skill found in the searched inventory", not "no such skill exists".
- **Limits and blockers:** Every proposed default is a proposal nobody approved. Four enforcement requirements (R1-R4) are recorded with no implementation. `devforge-change`, the specification's named consumer, does not exist. The evaluation runner this package's `cases.jsonl` targets is a draft under repair and is installed nowhere. Two acceptance behaviours - interruption-and-resume, post-release operational failure - have no eval case, for reasons recorded in `spec-mapping.md`.
- **Next:** An independent evaluator evaluates this candidate. The copyable task is below. The author cannot supply that judgement of its own candidate.
- **Readiness:** Prepared, not ready to run. The prerequisite is an execution allocation: a disposable consuming project, an installed or exported copy of this package, and a fresh terminal. Owner: the integration owner. Tier C requires an actual installation, so it cannot start from this source tree.
- **Validation status: Not performed.**
- **Behavioural status:** NOT_EVALUATED.
- **Enforcement status:** Requirements recorded; no gate implemented by this skill.
- **Installation mode:** none - source only. Not installed, not exported, not bound, not activated.

## Outputs produced

This handoff is excluded: it cannot contain its own digest and does not list itself among its own outputs. Every digest below was computed after that file's bytes were final and read back afterwards.

| Direction | Artifact ID and revision | Store and path | SHA-256 | Relevant sections | State |
| --- | --- | --- | --- | --- | --- |
| input | SKILL-011@2 | project, `docs/mvp/specifications/skill-011-devforge-release.md` | `f94261d7af37d8c68510e88d4b8705447b06ce396ead5776c28c7502cf60585d` | the six sections in `upstream` | governing; unchanged at base and in the working checkout |
| input | release-record template | project, `docs/mvp/templates/devforge-release/release-record.md` | `90b8e58f54eec19bb809a2aad5fb670b4616a32e3543815221818f66308e67eb` | whole file | copied byte-exact into the package |
| input | shared handoff template | project, `docs/mvp/templates/shared/handoff.md` | `abc7f8e0ca545093d3b1486d1a86cb7e51609aef17c0027b951a47da6eaed206` | whole file | adapted; transformation recorded in `references/derivation.json` |
| input | builder `SKILL.md` at `4999f31` | git, `providers/claude/plugins/devforgeai/skills/devforge-project-expert-creator/SKILL.md` | `342b82923e64cef0c2ab77fdb8fc11b92fc68ea145642c486d2a937c5363f3d9` | all five phases | source-loaded; draft under independent review |
| output | devforge-release package, 24 files | worktree, `providers/claude/plugins/devforgeai/skills/devforge-release/` | see `file-manifest.json` | — | authored candidate; NOT_EVALUATED |
| output | working design specification, revision 1 | worktree, `.../devforge-release/authoring/design/skill-design-spec.md` | `81cffb23d176008c929f0648094aecafd841376f2efca4042b5654671e476c17` | sections 5, 7, 9, 10, 12 | filled; expectations written before the candidate |
| output | package file manifest | worktree, `.../devforge-release/authoring/file-manifest.json` | `dd1c22ccb1cf1a64d07a70747b780702e034744d1b5bb7ab0cb07bf85bc68ac3` | `files_sha256` | complete; excludes its own digest |
| output | authoring notes | worktree, `.../devforge-release/authoring/authoring-notes.md` | `7c4ee6ba863105118514bf2f70c664c601f10584de7cac909c1f93b8506a144e` | "Commands actually run", "Unresolved items" | complete |
| output | specification mapping | worktree, `.../devforge-release/authoring/spec-mapping.md` | `599a6eba6d910385145f3dbf844b32c6ab1d4c0a2c364352d9cf165e816fb1bb` | "Validation and behavioral acceptance", "Gaps in this mapping" | complete |

The package's own `SKILL.md` digest is `7b7796d4cfef18f9c7734f6cb8219d627c61abd7f5ce1fab0da642919411a51f`. That is the value an artifact this skill later produces would carry as `producer.skill_revision` - the digest of one file, not of the package and not a plugin version.

## Evidence and reading order

| Read when | Record and relevant sections | Purpose |
| --- | --- | --- |
| First | `file-manifest.json`, then `providers/claude/plugins/devforgeai/skills/devforge-release/SKILL.md` | Bind the exact candidate bytes, then read what it actually instructs. |
| Second | `design/skill-design-spec.md` sections 7 and 9 | The acceptance cases as they were stated before the candidate was written, and the proposed defaults that are still only proposals. |
| Before grading | `spec-mapping.md` | Every SKILL-011 row mapped to a file, a section and an eval case ID - including the four rows with no eval coverage and why. |
| Before trusting any digest or command claim | `authoring-notes.md`, "Commands actually run" | The complete list of what was executed, including the one runner invocation and exactly what it does and does not establish. |
| For an authority or enforcement question | `design/skill-design-spec.md` section 5, routes R1-R4 | Each recorded requirement with its evidence, intended allow/refuse behaviour, owner and feasibility. None is implemented. |

## Proposed evaluation cases

The cases, with their independently stated expectations, are in `evals/evals.json` (nine tier-B cases: the five SKILL-011 acceptance rows and the four common cases), `evals/cases.jsonl` (ten deterministic and routed cases) and `evals/triggers/trigger-queries.json` (21 tier-A queries, fixed split stratified by `should_trigger` and category). They were captured, not executed.

| Check | Outcome | Evidence or receipt | Cause or scope limit |
| --- | --- | --- | --- |
| Tier C: installed resources and outputs | NOT_RUN | none | Requires an actual installation or export in a consuming project where the source docs are unreachable. Nothing was installed. |
| Tier B: output quality and boundaries | NOT_RUN | none | Requires an execution allocation, two clean contexts, and the `without_skill` baseline arm. Nothing was executed. |
| Tier A: discovery and activation | NOT_RUN | none | Requires the installed package in a fresh terminal and a real consultation trace. Nothing was observed. |
| Case-file schema load | Completed, exit 0 | `authoring-notes.md`, "The one execution" | Establishes only that `evals/cases.jsonl` loads against the pinned runner: valid JSONL, no duplicate `case_id`, no unknown grader, every `candidate_subpath` resolving. Not an evaluation; no row adopted as an outcome; tier C remains NOT_RUN. |
| Structural conformance of the package | NOT_RUN as a check | — | The schema-load run's deterministic rows are observations about bytes, not a structural gate. No DevForge command checks this package. |
| Independent semantic review | NOT_RUN | none | This is the next owner's job. An author cannot supply it. |

`NOT_RUN` is planned and unattempted. `COULD_NOT_RUN` is a required observation that was blocked, with its cause. `NOT_APPLICABLE` is a stated scope exclusion. The absence of an error is not a pass.

## Copyable next task

`devforge-evaluate-expert` exists as a Claude package only in an uncommitted-to-main worktree at `e52ac59`, is a draft under repair, and is installed nowhere. So this is a plain-language task, not a slash command. Every path is a host path, absolute.

```text
Goal: An independent evaluation of the Claude devforge-release scaffold against SKILL-011,
reporting tiers C, B and A separately and in that order.

Context: Read, in this order:
  /home/bryan/Projects/DevForge/worktrees/claude-scaffold-release-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-release/authoring/handoff.md
  .../authoring/file-manifest.json
  /home/bryan/Projects/DevForge/worktrees/claude-scaffold-release-20260910/providers/claude/plugins/devforgeai/skills/devforge-release/SKILL.md
  .../authoring/design/skill-design-spec.md   (sections 7 and 9)
  .../authoring/spec-mapping.md
  .../authoring/authoring-notes.md
Governing specification: /home/bryan/Projects/DevForge/framework/DevForgeAI/docs/mvp/specifications/skill-011-devforge-release.md
  at sha256 f94261d7af37d8c68510e88d4b8705447b06ce396ead5776c28c7502cf60585d.

Task: Bind the candidate to file-manifest.json before reading anything else, and re-verify
those digests. Evaluate the nine authored tier-B cases in evals/evals.json and the tier-A
queries in evals/triggers/trigger-queries.json. Run the deterministic cases in
evals/cases.jsonl with the runner and graders committed at
e52ac596cbf790dfa156d883852d392c512fdbcc, treating its rows as observations and never as
outcomes. Judge the proposed defaults listed in authoring-notes.md on their merits;
none was approved.

Preserve: the authored expectations exactly as written - do not weaken a case to convert a
failure into a pass. Keep the fixed trigger split; keep validation queries and their
should_trigger values out of any author-loop context. Preserve every recorded gap and
NOT_RUN rather than closing it by inspection.

Output: an evaluation plan and report with tiers C, B and A reported separately, binding the
exact candidate and baseline identities and the observed installation mode, plus a handoff
back to the author, to an evaluation output root you are assigned. Do not write inside
providers/claude/plugins/devforgeai/skills/devforge-release.

Stop at: completion, or at the first missing prerequisite - name it and its owner.
Prerequisites known to be unresolved: no execution allocation exists; no installed or
exported copy of this package exists; the runner package is a draft under repair.
```

## Retention and continuation limits

- **Output readback:** every digest in the outputs table was computed after that file's bytes were final and read back afterwards. Excludes this handoff.
- **This handoff's location:** `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-release-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-release/authoring/handoff.md`.
- **This handoff's receipt:** compute its digest after saving and reading it back, and deliver the path and digest in the terminal response to the coordinator. It is not written into this document, and this document is not edited later to record it.
- **Worktree ownership:** retained by this author until the coordinator releases it. Branch `author/claude-devforge-release-scaffold-20260910`, base `c17e758417da64928a0f47fc2600304465ac3f3c`. The fenced paths are committed on that branch by this author after these bytes were final; nothing is pushed, and the commit identity is delivered in the terminal response rather than written back into this document.
- **External gate state:** none. No DevForge command was run against this package, and none checks it.
- **Conditions invalidating this handoff:** any change to the package bytes; a revision of SKILL-011 past revision 2; a change to either copied template; a repair to the runner or graders that changes the case schema, the grader names or the `expect` handling; a change to the assigned worktree, branch or fence.

Retain the exact referenced bytes and any earlier failures; a digest cannot recover a missing source. Record an identity change as a new revision rather than rewriting prior evidence.

A prepared transfer is not receiving execution. This document authorises no evaluation, installation, activation or automatic invocation of a receiver, and the package it hands over describes deployments and external actions that this authoring session did not perform and did not simulate: nothing was tagged, published, merged, deployed or communicated. No self-digest, and no circular receipt reference.
