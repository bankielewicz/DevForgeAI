---
schema_version: "devforge.artifact/v1"
artifact_id: "HANDOFF-devforge-design-scaffold-20260910"
artifact_type: "handoff"
project_id: "devforgeai"
revision: 2
status: draft
created_at_utc: "2026-09-10T19:28:11Z"
producer:
  skill: "devforge-project-expert-creator (source-loaded, not installed)"
  skill_revision: "342b82923e64cef0c2ab77fdb8fc11b92fc68ea145642c486d2a937c5363f3d9 (sha256 of that package's SKILL.md blob at commit 4999f3106565c5e320d1f1a7db066b437e4e94be; its bytes were read with git show, not loaded by a client)"
execution_ref: null
upstream:
  - artifact_id: "SKILL-003"
    revision: 2
    store: project
    path: "docs/mvp/specifications/skill-003-devforge-design.md"
    sha256: "4a90c0d5648217480a4986518795dedd17bf3f62a67e433ec4d9d10e4247c8fb"
    sections:
      - "User goal and use-case inventory"
      - "Inputs and provenance"
      - "Workflow and phase exits"
      - "Outputs and standardized templates"
      - "Validation and behavioral acceptance"
      - "Rework, stopping, and recovery"
evidence: []
supersedes:
  artifact_id: "HANDOFF-devforge-design-scaffold-20260910"
  revision: 1
  sha256: "3107ebbe8855f337d55a0614847c123e208d62f7a2c67a3c15bc7dddf5c273d3"
  preserved_location: "git show f3049e4423ff57a826650def1c038cf8cdefb895:docs/skill-authoring/history/claude-scaffolding-20260910/devforge-design/authoring/handoff.md"
  reason: "Revision 1 recorded created_at_utc as 2026-09-10T00:00:00Z, a date-only placeholder rather than an observed clock, and the same value appeared in references/derivation.json and file-manifest.json. All three were corrected to the observed 2026-09-10T19:28:11Z and the dependent digests recomputed. The revision-1 bytes remain reachable at that commit."
decision_ref: null
missing_inputs:
  - "Session assignment record: none exists. The authoring scope came from the operator task packet at /home/bryan/Projects/DevForge/tmp/claude-remaining-skills-scaffolding-20260910/packets/author-devforge-design.md, which is not a devforge.artifact session record, so execution_ref is null."
  - "devforge-evaluate-expert Python JSONL runner and deterministic graders: not committed at authoring time. evals/cases.jsonl is authored to a documented schema, not an observed interface."
  - "Claude Code client version: not observed; no version probe was run."
---

# Authoring handoff: devforge-design (SKILL-003), Claude scaffold

## Result and next action

- **Result:** A new Claude package was created at `providers/claude/plugins/devforgeai/skills/devforge-design/` - 23 files: `SKILL.md`, two byte-exact template copies in `assets/`, four `references/`, and an `evals/` set of 10 cases, 10 JSONL cases, 12 fixture files and 24 trigger queries. Nothing existed at that destination before; there was no collision to reconcile.
- **Why:** SKILL-003 is an accepted roster role with its own artifact type, its own template and its own place in the provenance flow, and no skill in the searched Claude inventory owns that workflow. The selection decision and its search limits are in `design/skill-design-spec.md` section 9.
- **Limits and blockers:** Four things constrain what this can be claimed to be. No `devforge` subcommand reads a design-spec, so the two enforcement routes in the design spec are recorded requirements with no implementation. The evaluation runner this package's `cases.jsonl` targets is not committed, so five schema details listed in `authoring-notes.md` need re-checking against the real interface. `devforge-define-product` is unimplemented, so this skill's required upstream normally will not exist - the `user-stated` fallback is a proposed default, not an approved one. And the non-UI "design" exclusion in the description is the author's proposal, not something SKILL-003 states.
- **Next:** An independent evaluator evaluates the package named in `file-manifest.json` against SKILL-003 and the cases in `evals/`. See the copyable task below.
- **Readiness:** Prepared, not ready to run. Tier C needs an actual installed or exported copy in a consuming project; none was generated, and generating it is the integration owner's action. Tier A needs a fresh terminal. Static review of the authored bytes can begin immediately.
- **Validation status:** Not performed.
- **Behavioural status:** NOT_EVALUATED.
- **Enforcement status:** Requirements recorded; no gate implemented, activated or executed by this skill.

## Outputs produced

This handoff is excluded from the table: it cannot contain its own digest and does not list itself among its own outputs. Its digest is delivered in the terminal report after it is saved and read back.

All paths are relative to the worktree root `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-design-20260910/`.

| Direction | Artifact | Path | SHA-256 | State |
| --- | --- | --- | --- | --- |
| output | Skill package, 23 files | `providers/claude/plugins/devforgeai/skills/devforge-design/` | per-file digests in the manifest below | authored; unevaluated |
| output | Package file manifest | `docs/skill-authoring/history/claude-scaffolding-20260910/devforge-design/authoring/file-manifest.json` | `3bee05cf053e62c2b510da756dfc553abbe1253245de46f4c792f26e9236e184` | final |
| output | Working design specification | `docs/skill-authoring/history/claude-scaffolding-20260910/devforge-design/authoring/design/skill-design-spec.md` | `3b99c9cf3dc69efb2b838c79041bd25e6c5e57058dcb0cf398aab2dd29d91655` | final |
| output | Authoring notes | `docs/skill-authoring/history/claude-scaffolding-20260910/devforge-design/authoring/authoring-notes.md` | `e2580a481589d12d4a014c7028de73c24474968cc48f9ddcf06bf98035810dd1` | final |
| output | Specification mapping | `docs/skill-authoring/history/claude-scaffolding-20260910/devforge-design/authoring/spec-mapping.md` | `9bb70be54b345a80ab40c35b2687c892bf40228755f1e81db08261cc9adc4e16` | final |
| input | SKILL-003 specification | `docs/mvp/specifications/skill-003-devforge-design.md` | `4a90c0d5648217480a4986518795dedd17bf3f62a67e433ec4d9d10e4247c8fb` | governing |
| input | design-spec template | `docs/mvp/templates/devforge-design/design-spec.md` | `5a30b17a40a52be8c1efb453415d0e77d3406c29c71674408a5506bf5e6ab661` | copied byte-exact to `assets/design-spec.md` |
| input | shared handoff template | `docs/mvp/templates/shared/handoff.md` | `abc7f8e0ca545093d3b1486d1a86cb7e51609aef17c0027b951a47da6eaed206` | copied byte-exact to `assets/handoff.md` |
| input | skill-authoring contract | `docs/mvp/skill-authoring-contract.md` | `371462385b4e32d1b347f959abb779f4be4251e357c5720a9aef039113eb4b53` | governing |

The remaining selected inputs, with their digests, are in the package's `references/derivation.json` and in `design/skill-design-spec.md` section 10.

## Evidence and reading order

| Read when | Record | Purpose |
| --- | --- | --- |
| First | `file-manifest.json`, then `providers/claude/plugins/devforgeai/skills/devforge-design/SKILL.md` | Identify the exact candidate bytes and read what the skill actually instructs |
| Before judging anything | `spec-mapping.md` | Every SKILL-003 row mapped to a file, a section and an eval case ID |
| Before treating a decision as approved | `design/skill-design-spec.md` sections 9 and 10 | The selection decision with its search limits, the seven proposed defaults, the two recorded enforcement routes, and the preserved boundaries |
| Before running anything | `authoring-notes.md` | Which builder files were loaded, what was deliberately omitted, the exact static checks that were run, and the five open schema questions against the unfinished evaluation runner |

## Proposed evaluation cases

The cases and their independently stated expectations are in `providers/claude/plugins/devforgeai/skills/devforge-design/evals/evals.json` (10 cases), with deterministic assertions in `evals/cases.jsonl` and tier-A queries in `evals/triggers/trigger-queries.json` (24 queries, fixed split). They were captured, not executed.

| Check | Outcome | Evidence | Cause or scope limit |
| --- | --- | --- | --- |
| Tier C: installed resources resolve | NOT_RUN | none | No installed copy or plugin export was generated |
| Tier B: output quality against a `without_skill` baseline | NOT_RUN | none | No baseline arm was run; no prior version of this skill exists to serve as `old_skill` |
| Tier A: discovery and activation in a fresh terminal | NOT_RUN | none | No terminal run was performed |
| Deterministic graders over `cases.jsonl` | COULD_NOT_RUN | none | The runner and graders are not committed; see `authoring-notes.md` |
| JSON validity, Markdown link resolution, absence of home paths and runtime `docs/mvp` dependencies | observed, pass | `authoring-notes.md` "Commands actually run" | Establishes only those facts about the bytes; says nothing about behaviour |

`NOT_RUN` is planned and unattempted. `COULD_NOT_RUN` is blocked with its cause. The absence of an error is not a pass.

## Copyable next task

`devforge-evaluate-expert` is **not installed** in this environment - its Claude package is an uncommitted scaffold in another worktree. So this is a plain-language task, not a slash command. All paths are absolute host paths.

```text
Goal: An independent evaluation of the devforge-design Claude package against SKILL-003.

Context, in this reading order:
  /home/bryan/Projects/DevForge/worktrees/claude-scaffold-design-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-design/authoring/file-manifest.json
  /home/bryan/Projects/DevForge/worktrees/claude-scaffold-design-20260910/providers/claude/plugins/devforgeai/skills/devforge-design/SKILL.md
  /home/bryan/Projects/DevForge/worktrees/claude-scaffold-design-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-design/authoring/spec-mapping.md
  /home/bryan/Projects/DevForge/worktrees/claude-scaffold-design-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-design/authoring/design/skill-design-spec.md
  /home/bryan/Projects/DevForge/worktrees/claude-scaffold-design-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-design/authoring/authoring-notes.md

Governing specification:
  /home/bryan/Projects/DevForge/framework/DevForgeAI/docs/mvp/specifications/skill-003-devforge-design.md
  sha256 4a90c0d5648217480a4986518795dedd17bf3f62a67e433ec4d9d10e4247c8fb

Task: Verify the manifest digests against the bytes on disk, then evaluate the package
      against SKILL-003 and the authored cases in its evals/ directory. Judge whether
      each of the seven proposed defaults in design/skill-design-spec.md section 9 is
      sound, and whether the description's activation boundary matches the trigger set.
      Record semantic findings with severities and stable finding IDs.

Preserve: the authored bytes, the recorded search limits, the NOT_RUN and COULD_NOT_RUN
      labels, and the distinction between what was suggested, what is installed, and what
      was actually invoked. Do not edit the candidate; findings go to its author.

Output: an evaluation plan and report, in your own assigned writable directory. Do not
      write inside the package or inside this authoring evidence directory.

Stop at: tier C. It needs an installed or exported copy that does not exist yet; the
      integration owner owns generating it. Report that prerequisite rather than
      substituting a changed working directory for installation isolation.
```

## Retention and continuation limits

- **Output readback:** the five output rows above were hashed after their bytes were final and re-read at those paths. This handoff is excluded.
- **Revision 2 correction:** revision 1 recorded a date-only placeholder as its creation time, and the same value sat in `references/derivation.json` and `file-manifest.json`. All three now carry the observed `2026-09-10T19:28:11Z`, and the digests that depend on them - `references/derivation.json`, then `file-manifest.json`, then `authoring-notes.md`, then the rows above - were recomputed in that write order. Revision 1's bytes are preserved at commit `f3049e4423ff57a826650def1c038cf8cdefb895` and are cited in `supersedes`; nothing was rewritten in place.
- **This handoff's location:** `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-design-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-design/authoring/handoff.md`. No self-digest.
- **This handoff's receipt:** its digest is computed after saving and reading it back, and delivered in the terminal report. It is not written into this document.
- **Worktree ownership:** retained by this authoring session at handoff time, on branch `author/claude-devforge-design-scaffold-20260910` from base `c17e758417da64928a0f47fc2600304465ac3f3c`. The commit is local; nothing was pushed.
- **External gate state:** none. No gate was invoked, and no receipt exists.
- **Conditions invalidating this handoff:** any edit to the package (the manifest digests go stale immediately); a change to SKILL-003 or to either copied template; the evaluation runner being committed with a case schema differing from what `cases.jsonl` was authored against; a new `devforge` subcommand that reads a design-spec.

A prepared transfer is not a receiving invocation. This document authorises no evaluation, installation, activation or automatic invocation of anyone. **Validation status: Not performed.**
