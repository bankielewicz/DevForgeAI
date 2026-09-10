---
schema_version: "devforge.artifact/v1"
artifact_id: "HANDOFF-DP-001"
artifact_type: "handoff"
project_id: "devforgeai"
revision: 1
status: draft
created_at_utc: "2026-09-10T19:33:41Z"
producer:
  skill: "devforge-project-expert-creator"
  skill_revision: "342b82923e64cef0c2ab77fdb8fc11b92fc68ea145642c486d2a937c5363f3d9 (SHA-256 of that skill's SKILL.md file bytes at commit 4999f3106565c5e320d1f1a7db066b437e4e94be; source-loaded, never installed or invoked)"
execution_ref: null
upstream:
  - artifact_id: "SKILL-002"
    revision: 2
    store: project
    path: "docs/mvp/specifications/skill-002-devforge-define-product.md"
    sha256: "3e48f93f200499083a062e200f71ad4a3659fad098ef6658fb4b4a34bea6ddbf"
    sections:
      - "User goal and use-case inventory"
      - "Inputs and provenance"
      - "Workflow and phase exits"
      - "Outputs and standardized templates"
      - "Validation and behavioral acceptance"
      - "Rework, stopping, and recovery"
      - "Native creator authoring prompt"
evidence:
  - id: "PACKAGE-MANIFEST"
    store: project
    path: "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-define-product/authoring/file-manifest.json"
    sha256: "2f59575a791a41d2d90eaa8e18639b1ff35a91ce04fd5f0a5d88b140f49fda24"
    note: "Twenty package-relative paths with SHA-256, taken after the last write to each."
  - id: "DESIGN"
    store: project
    path: "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-define-product/authoring/design/skill-design-spec.md"
    sha256: "945564f5520715d56fd0d8f523fc5f82d50e78bca42cb5f8fc2f9fbc06a0bc3d"
  - id: "SPEC-MAPPING"
    store: project
    path: "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-define-product/authoring/spec-mapping.md"
    sha256: "acfb370699716586742035985379134806f4284aca266ee2706bc703a02d4ca6"
  - id: "AUTHORING-NOTES"
    store: project
    path: "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-define-product/authoring/authoring-notes.md"
    sha256: "aa469dffbd1383b1c51d9471f26829131eb00e58b0525239e805a53786ffbe65"
supersedes: null
decision_ref: null
missing_inputs:
  - "No authority-store session record was supplied for this assignment; the coordinator's task packet is the authorisation and a packet is not a session record."
  - "The Claude Code client version was not recorded by this session, so a tier-A run manifest cannot yet name the terminal version."
  - "The DevForge binary used for the --help observation was not digest-pinned."
---

# Authoring handoff: devforge-define-product (SKILL-002 scaffold)

## Result and next action

- **Result:** A new Claude package at `providers/claude/plugins/devforgeai/skills/devforge-define-product/` - twenty files: `SKILL.md`, two byte-identical template copies in `assets/`, two distilled workflow references plus a sources record and a derivation record in `references/`, and an authoring-only `evals/` tree with ten requirement-derived cases, twelve deterministic case lines, twenty trigger queries and ten synthetic fixtures. No `scripts/`. Complete as a scaffold; unevaluated as a skill.
- **Why:** The selection decision was **create**. No skill in the searched inventory owns the release-scope workflow, the roster reserves SKILL-002 for it, and the artifact contract assigns the `product-brief` type to this skill alone. Enhancing `devforge-brainstorm` would blur two activations its own description deliberately separates. Search scope and its limits are in the design document, section 9.
- **Limits and blockers:** Nothing observed. The R1 enforcement requirement has no implementation and no DevForge command performs it. The JSONL runner `evals/cases.jsonl` targets is uncommitted in a sibling worktree, so its schema binding is provisional. Two search locations were unreachable. Fifteen proposed defaults await an owner's answer.
- **Next:** An independent evaluator plans and runs tier C, then B, then A against this candidate, and returns bounded findings. The author cannot supply that judgement. A copyable task is below.
- **Readiness:** **Prepared, not ready.** Three prerequisites are missing and each has an owner: an allocated evaluation workspace and disposable consuming projects (integration owner); a committed runner interface for `cases.jsonl` (the `devforge-evaluate-expert` author); an installed or exported copy of this package (integration owner). Static review of the authored bytes needs none of them and can start now.
- **Validation status:** Not performed.
- **Behavioural status:** NOT_EVALUATED.
- **Enforcement status:** Requirements recorded; no gate implemented by this skill.

## Outputs produced

This handoff is excluded: it cannot contain its own digest and does not list itself among its own outputs. Every digest below was taken after the last write to that path.

| Direction | Artifact ID and revision | Store and path | SHA-256 | Relevant sections | State |
| --- | --- | --- | --- | --- | --- |
| input | SKILL-002 @ 2 | project, `docs/mvp/specifications/skill-002-devforge-define-product.md` | `3e48f93f200499083a062e200f71ad4a3659fad098ef6658fb4b4a34bea6ddbf` | all seven listed in `upstream` | accepted governing input, unchanged |
| input | devforge-project-expert-creator SKILL.md @ `4999f31` | sibling worktree, `providers/claude/plugins/devforgeai/skills/devforge-project-expert-creator/SKILL.md` | `342b82923e64cef0c2ab77fdb8fc11b92fc68ea145642c486d2a937c5363f3d9` | Intake, Selection, Design, Authoring, Prepared transfer | draft under independent review; source-loaded, never installed |
| output | devforge-define-product package, revision 1 | project, `providers/claude/plugins/devforgeai/skills/devforge-define-product/` | 20 paths, each digested in `file-manifest.json` | - | authored candidate; NOT_EVALUATED |
| output | package manifest | project, `.../authoring/file-manifest.json` | `2f59575a791a41d2d90eaa8e18639b1ff35a91ce04fd5f0a5d88b140f49fda24` | `package_files` | final |
| output | working design document | project, `.../authoring/design/skill-design-spec.md` | `945564f5520715d56fd0d8f523fc5f82d50e78bca42cb5f8fc2f9fbc06a0bc3d` | sections 1-10, 12 | final |
| output | specification coverage map | project, `.../authoring/spec-mapping.md` | `acfb370699716586742035985379134806f4284aca266ee2706bc703a02d4ca6` | all | final |
| output | authoring notes | project, `.../authoring/authoring-notes.md` | `aa469dffbd1383b1c51d9471f26829131eb00e58b0525239e805a53786ffbe65` | sections 1-8 | final |

No evaluation plan, report, run manifest or transcript was produced. None was authorised, and none exists.

## Evidence and reading order

| Read when | Record and relevant sections | Purpose |
| --- | --- | --- |
| First | `file-manifest.json`, then `providers/claude/plugins/devforgeai/skills/devforge-define-product/SKILL.md` | Identify the exact candidate bytes and read the instructions being evaluated. |
| Before acting | `design/skill-design-spec.md` sections 3, 4, 6, 9 and 10 | The inputs, the phase/task classifications and their **proposed** status, the R1 enforcement requirement, the search scope and its limits, and the preserved boundaries. |
| Before grading anything | `spec-mapping.md` | Which specification row each file and eval case answers, and the coverage summary. |
| For the eval design | `.../devforge-define-product/evals/evals.json`, `evals/cases.jsonl`, `evals/triggers/trigger-queries.json`, `evals/fixtures/README.md` | The ten cases with graded observations and staging, the deterministic slices, the fixed trigger split, and the fixture inventory with its source-inventory-versus-worker-visible warning. |
| For an affected question | `authoring-notes.md` sections 4, 6 and 8; `.../references/derivation.json` | The proposed defaults and their basis, the pending runner dependency, the open items, and the package provenance with its refresh conditions. |

## Proposed evaluation cases

The cases proposed for this candidate, with their independently stated expectations, live in `providers/claude/plugins/devforgeai/skills/devforge-define-product/evals/evals.json` (behavioural) and `evals/cases.jsonl` (deterministic slices). They were captured, not executed.

| Check | Outcome | Evidence or receipt | Cause or scope limit |
| --- | --- | --- | --- |
| Tier C: installed resources resolve (DP-C-001, DP-C-002) | NOT_RUN | none | Requires an actual installed or exported copy in a consuming project where `docs/mvp` is unreachable. Not installed. |
| Tier B: ten output-quality cases against a `without_skill` baseline | NOT_RUN | none | Requires an evaluation allocation, disposable consuming projects and per-case fixture staging. `old_skill` is unavailable: no previous version exists. |
| Tier A: twenty trigger queries, fresh terminal | NOT_RUN | none | Requires an installed package and a fresh client context. Explicit-invocation queries are recorded separately and never count as implicit activation. |
| Deterministic grader run over `cases.jsonl` | NOT_RUN | none | The runner and graders are uncommitted in a sibling worktree; the schema binding is provisional until that interface is committed. |
| Independent semantic review of the authored bytes | NOT_RUN | none | Not attempted. Can start immediately; it needs no allocation. |

`NOT_RUN` means planned and unattempted. Nothing here was blocked mid-attempt, so no `COULD_NOT_RUN` appears. The absence of an error is not a pass.

## Copyable next task

`devforge-evaluate-expert` is **not installed** in this environment and its Claude package is uncommitted in a sibling worktree, so this is a plain-language task with resolvable absolute paths rather than a slash command. Do not substitute a command for a skill you have not confirmed is installed.

```text
Goal: An independent evaluation of the authored devforge-define-product candidate against SKILL-002,
      reporting tiers C, B and A separately and never blended.
Context: /home/bryan/Projects/DevForge/worktrees/claude-scaffold-define-product-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-define-product/authoring/handoff.md
      and the reading order it gives. The candidate is at
      /home/bryan/Projects/DevForge/worktrees/claude-scaffold-define-product-20260910/providers/claude/plugins/devforgeai/skills/devforge-define-product/
      at the digests in that directory's sibling file-manifest.json.
Task: Verify the candidate bytes against file-manifest.json before reading anything else. Then plan the
      evaluation from evals/evals.json, evals/cases.jsonl and evals/triggers/trigger-queries.json, and
      review the authored instructions against SKILL-002 rev 2
      (sha256 3e48f93f200499083a062e200f71ad4a3659fad098ef6658fb4b4a34bea6ddbf). Report findings with
      stable IDs and severities. Run tier C first; B and A only after the required C observations pass.
Preserve: the fifteen proposed defaults in authoring-notes.md section 4 - each is the author's proposal,
      not a user decision, and a severity label is not authority to change SKILL-002. Preserve the R1
      enforcement requirement as recorded rather than treating it as implemented, and preserve every
      digest in file-manifest.json.
Output: an evaluation plan and report with the exact candidate identity, the observations actually made,
      and every unavailable check recorded as COULD_NOT_RUN with its real cause, written to an assigned
      output directory outside the candidate.
Stop at: the report, or the first missing prerequisite - no installed copy, no evaluation allocation, or
      no committed JSONL runner interface. A prerequisite that is missing is COULD_NOT_RUN, never a pass.
```

If evaluation cannot be allocated yet, the useful smaller task is a static independent review of the authored bytes against SKILL-002 and the shared contracts, with findings returned as a bounded repair specification. That needs no allocation and no installation, and it is honest about being static: it observes instructions, never behaviour.

## Retention and continuation limits

- **Output readback:** the six paths in the outputs table, each read back and hashed after its last write. Excludes this handoff.
- **This handoff's location:** `docs/skill-authoring/history/claude-scaffolding-20260910/devforge-define-product/authoring/handoff.md` in the worktree `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-define-product-20260910`. No self-digest.
- **This handoff's receipt:** compute its digest after saving and reading it back, then deliver the path and digest in the terminal response. It is not written into this document.
- **Worktree ownership:** retained by this author until the coordinator reassigns it. Branch `author/claude-devforge-define-product-scaffold-20260910`, base `c17e758417da64928a0f47fc2600304465ac3f3c`. One commit adds the two fenced paths and nothing else; it was not pushed.
- **External gate state:** none. No gate was run and no receipt exists.
- **Conditions invalidating this handoff:** any change to a package digest in `file-manifest.json`; a new SKILL-002 revision; a change to a contract or template digest recorded in `references/derivation.json`; a committed `devforge-evaluate-expert` runner interface that differs from the schema `cases.jsonl` was written to; a DevForge CLI release that adds an artifact-reference or brief-admission command.

A prepared transfer is not receiving execution and not acceptance. This document authorises no evaluation, installation, activation or automatic invocation of a receiver. No self-digest, and no circular receipt reference.
