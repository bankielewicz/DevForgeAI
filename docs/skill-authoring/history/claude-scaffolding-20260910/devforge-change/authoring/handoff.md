---
schema_version: "devforge.artifact/v1"
artifact_id: "HANDOFF-devforge-change-scaffold-20260910"
artifact_type: "handoff"
project_id: "DevForgeAI"
revision: 1
status: draft
created_at_utc: "2026-09-10T20:23:16Z"
producer:
  skill: "devforge-project-expert-creator"
  skill_revision: "342b82923e64cef0c2ab77fdb8fc11b92fc68ea145642c486d2a937c5363f3d9 (SHA-256 of the builder SKILL.md file's bytes at 4999f3106565c5e320d1f1a7db066b437e4e94be; source-loaded from git object storage, not installed)"
execution_ref: null
upstream:
  - artifact_id: "SKILL-012"
    revision: 2
    store: "project"
    path: "docs/mvp/specifications/skill-012-devforge-change.md"
    sha256: "b47d49ada93bf5612ea64d5c31d94e31807869316925c53b828deb9e5cbe6774"
    sections: ["User goal and use-case inventory", "Inputs and provenance", "Workflow and phase exits", "Outputs and standardized templates", "Validation and behavioral acceptance", "Rework, stopping, and recovery"]
evidence:
  - kind: "authoring evidence"
    store: "project"
    path: "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-change/authoring/file-manifest.json"
    sha256: "8cc1c747417ead19d872072c38ed1dabdb9579e4c64c4f24db26d4bcee260c87"
supersedes: null
decision_ref: null
missing_inputs:
  - "No session record artifact was supplied for this assignment, so execution_ref is null. The coordinator packet at tmp/claude-remaining-skills-scaffolding-20260910/packets/author-devforge-change.md is the assignment; its absence as a devforge.artifact/v1 record does not establish ownership."
  - "artifact_id above is a locally derived descriptive identity. No authority allocated a HANDOFF number for this work."
---

# Authoring handoff: devforge-change (SKILL-012), Claude package

## Result and next action

- **Result:** A new Claude package was created at
  `providers/claude/plugins/devforgeai/skills/devforge-change/` — 26 files: `SKILL.md`, two
  byte-identical output template copies in `assets/`, four references plus a derivation record,
  nine tier-B eval cases, twelve runner cases, thirty trigger queries, and fifteen synthetic
  fixtures. Complete as a scaffold. The candidate identity is the manifest in the evidence
  table below. Package revision 2 repaired four eval defects found in review — the fixture
  reference digests are now a real hash chain and the runner sentinels are computed from
  those bytes; `authoring-notes.md` § Corrections has the detail. No instruction, asset or
  reference byte changed between revisions 1 and 2: nineteen of the twenty-six files are
  byte-identical, and the seven that changed are all under `evals/`.
- **Why:** The selection decision was **create**, from a bounded search of the Claude provider
  inventory at base `c17e758417da64928a0f47fc2600304465ac3f3c`: four skills exist and none
  activates on "what does this change invalidate" or owns the impact graph and the routing
  decision. The search limits are recorded in `design/skill-design-spec.md` § 9 and are part of
  the result — "no suitable skill found in the searched inventory" is what happened, not "no
  such skill exists".
- **Limits and blockers:** Two enforcement requirements (R1, R2) have no implemented check and
  are routed to the integration owner with feasibility unknown; five specific missing
  integrations are enumerated in the package's `references/cli-boundaries.md`. Six of the nine
  consumers the specification names are not implemented in this provider. The runner this
  package's `evals/cases.jsonl` targets is itself an unevaluated scaffold at a pinned revision
  in another worktree. Three coverage gaps in the specification mapping are stated rather than
  closed.
- **Next:** An independent evaluator evaluates this candidate. Owner: not this author — an
  author cannot supply the independent judgement of its own candidate. Permitted writes: an
  evaluation workspace the evaluator is assigned; nothing inside the candidate package.
  Expected deliverable: an evaluation plan and report binding the exact manifest digests below.
- **Readiness:** **Prepared, not ready.** Tier C requires an actual installed copy in a
  consuming project where this repository's `docs/mvp` is unreachable; no installation was
  performed and none is implied. Tier B requires a run workspace and a `without_skill` baseline
  arm. Tier A requires a fresh terminal with the installed package. The prerequisite is an
  installation or export by the integration owner.
- **Validation status:** Not performed.
- **Behavioural status:** NOT_EVALUATED.
- **Enforcement status:** Requirements recorded; no gate implemented by this skill.

## Outputs produced

This handoff is excluded from the table: it cannot contain its own digest and does not list
itself among its own outputs. Each file below was hashed after its bytes were final.

| Direction | Artifact ID and revision | Store and path | SHA-256 | Relevant sections | State |
| --- | --- | --- | --- | --- | --- |
| input | SKILL-012 @ 2 | project · `docs/mvp/specifications/skill-012-devforge-change.md` | `b47d49ada93bf5612ea64d5c31d94e31807869316925c53b828deb9e5cbe6774` | all six | governing; unchanged |
| input | change-request template | project · `docs/mvp/templates/devforge-change/change-request.md` | `1b6d4198065153934368079833fa853fc271aacbf7266444765cda7cde7e5b43` | whole file | unchanged |
| input | shared handoff template | project · `docs/mvp/templates/shared/handoff.md` | `abc7f8e0ca545093d3b1486d1a86cb7e51609aef17c0027b951a47da6eaed206` | whole file | unchanged |
| input | skill-authoring-contract @ 3 | project · `docs/mvp/skill-authoring-contract.md` | `371462385b4e32d1b347f959abb779f4be4251e357c5720a9aef039113eb4b53` | packaging, tiers | unchanged |
| input | builder package | project · `providers/claude/.../devforge-project-expert-creator/SKILL.md` @ `4999f31` | `342b82923e64cef0c2ab77fdb8fc11b92fc68ea145642c486d2a937c5363f3d9` | five phases | draft under independent review; source-loaded |
| output | devforge-change package @ 2 | project · `providers/claude/plugins/devforgeai/skills/devforge-change/` | see `file-manifest.json` (26 entries) | whole package | authored; NOT_EVALUATED |
| output | package manifest | project · `.../devforge-change/authoring/file-manifest.json` | `8cc1c747417ead19d872072c38ed1dabdb9579e4c64c4f24db26d4bcee260c87` | `files` | final |
| output | skill design specification @ 1 | project · `.../devforge-change/authoring/design/skill-design-spec.md` | `6cd09714a75f4027bb0f69d0bb32282ad639b8d1867cd2bc8bd5be95490ab25a` | §§ 1–12 | draft |
| output | authoring notes | project · `.../devforge-change/authoring/authoring-notes.md` | `1b88f0441c8690858c09c4dce93e2fc54fb093ba18662c1e5d09c780c7bf1671` | whole file | final |
| output | specification mapping | project · `.../devforge-change/authoring/spec-mapping.md` | `a3c60ce1b51a70752783fbf35d68cd35b891e44c81f006012f03edaf6f87c760` | whole file | final |

Package-relative digests are in `file-manifest.json` rather than repeated here; a digest
repeated in two records is a digest that can go stale in one of them. The package's own
`references/derivation.json` carries the destination digests of the six derived files, and
those were verified against the actual bytes after the last write to each.

## Evidence and reading order

| Read when | Record and relevant sections | Purpose |
| --- | --- | --- |
| First | `file-manifest.json`, then the package's `SKILL.md` | Bind the exact 26 candidate files, then read the entrypoint you are evaluating |
| Before acting | `design/skill-design-spec.md` §§ 2, 3, 4, 7, 9 | The independently stated expectations, the search scope and its limits, and every proposed default — written before the candidate, so they are not a description of what got written |
| Before grading a requirement | `spec-mapping.md` | Every specification row mapped to a file, a section and an eval ID, plus the four coverage gaps this author could not close |
| For method, dependencies and repairs | `authoring-notes.md` | Which builder files were loaded and from where, every command actually run, and the three corrections made during authoring |
| Before running any case | the package's `evals/cases.jsonl` `notes` fields, and `references/runner-interface.md` in the `devforge-evaluate-expert` package at `e641797eebf04cd1e8eb9f711549e038e7745407` | What `--candidate` must point at differs per tier and is carried in each case's `notes`, not in the schema |

## Proposed evaluation cases

The cases proposed for this candidate, with their independently stated expectations, live in
the package's `evals/evals.json` (nine tier-B cases), `evals/cases.jsonl` (twelve runner cases,
three tier C and nine tier B) and `evals/triggers/trigger-queries.json` (thirty tier-A queries
on a fixed stratified split). They were captured, not executed.

| Check | Outcome | Evidence or receipt | Cause or scope limit |
| --- | --- | --- | --- |
| Tier C: installed resources resolve | NOT_RUN | none | Requires an actual installed copy in a project where `docs/mvp` is unreachable. Nothing was installed |
| Tier B: output quality against a `without_skill` baseline | NOT_RUN | none | Requires a run workspace, separate clean contexts and a baseline arm. None was arranged |
| Tier A: discovery and activation | NOT_RUN | none | Requires a fresh terminal with the installed package. Discovery and activation are NOT_OBSERVED |
| Deterministic case runner over `evals/cases.jsonl` | NOT_RUN | none | Deliberate: producing observations is the evaluator's work. An author running it would be self-grading |
| `evals/cases.jsonl` schema conformance | Observed | author-side stdlib check; method in `authoring-notes.md` § Commands actually run | Establishes the file would be accepted as runner input. Establishes nothing about the candidate |
| Package link resolution and hygiene | Observed | author-side stdlib check | Eleven local links resolve; no developer home path; no `docs/mvp` prose dependency; no shell-injection token. A structural fact, not a behavioural one |
| Governing input pin verification | Observed | eleven paths hashed and compared against base | Establishes which bytes were referenced. Never that behaviour is correct |
| `devforge` subcommand existence | Observed | `--help` output of a local `devforge 0.1.0` build | Establishes which subcommands that build exposes. No command was run against any project |

`NOT_RUN` means planned and unattempted. The absence of an error is not a pass, and a hash
binding proves which inputs were referenced, never that behaviour is correct.

## Copyable next task

The receiving capability, `devforge-evaluate-expert`, is **not installed in this environment**
and does not exist in the Claude provider source at base — it is being scaffolded separately.
So this is a plain-language task with resolvable absolute host paths, not a slash command for a
skill nobody has confirmed.

```text
Goal: Produce an independent evaluation plan and report for the authored
devforge-change candidate. You are the evaluator; you did not author it.

Context: Read, in this order:
  /home/bryan/Projects/DevForge/worktrees/claude-scaffold-change-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-change/authoring/file-manifest.json
  /home/bryan/Projects/DevForge/worktrees/claude-scaffold-change-20260910/providers/claude/plugins/devforgeai/skills/devforge-change/SKILL.md
  /home/bryan/Projects/DevForge/worktrees/claude-scaffold-change-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-change/authoring/design/skill-design-spec.md
  /home/bryan/Projects/DevForge/worktrees/claude-scaffold-change-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-change/authoring/spec-mapping.md
  /home/bryan/Projects/DevForge/worktrees/claude-scaffold-change-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-change/authoring/authoring-notes.md
Governing specification (do not edit):
  /home/bryan/Projects/DevForge/framework/DevForgeAI/docs/mvp/specifications/skill-012-devforge-change.md
Runner and graders, pinned at e641797eebf04cd1e8eb9f711549e038e7745407 in:
  /home/bryan/Projects/DevForge/worktrees/claude-scaffold-evaluate-expert-20260910

Task: Verify the 26 candidate files still hash to the manifest before anything else;
if they do not, stop and report the drift. Then judge the candidate against the
specification and against the design spec's independently stated expectations.
Run tier C first, then B, then A, and report the three separately. Where a tier
cannot be run, record COULD_NOT_RUN with the actual cause.

Preserve: this handoff and every record it names, byte for byte. Keep the author's
proposed defaults labelled as proposals. Do not edit the candidate, the governing
specification, the shared templates, the contracts, the roster, package-index.json,
any sibling skill, or the DevForge repository's gates and policies.

Output: an evaluation plan and an evaluation report binding the exact manifest
digests above, to your own assigned evaluation workspace. Not into this directory.

Stop at: the report, or at the stated missing prerequisite - no installed copy
exists yet, so tier C and tier A need an integration owner to install or export
the package first.
```

A prerequisite task for the integration owner, if the evaluator cannot proceed: generate an
installed copy or a plugin export of this exact candidate, record the installation mode and
path, and confirm that `evals/` was stripped — which is what case `CHG-C-002` asserts.

## Retention and continuation limits

- **Output readback:** the six output rows above were hashed after their final writes and read
  back. Excludes this handoff.
- **This handoff's location:**
  `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-change-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-change/authoring/handoff.md`.
  No self-digest.
- **This handoff's receipt:** its digest is computed after saving and reading it back, and
  delivered in the authoring session's terminal response. It is not written into this document,
  and this document is not modified to record it later.
- **Worktree ownership:** retained by the authoring session at
  `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-change-20260910`, branch
  `author/claude-devforge-change-scaffold-20260910`. Not pushed. The evaluator works from its
  own workspace and does not need this branch checked out to read the bytes.
- **External gate state:** none. No `devforge` command was run against any project, no receipt
  exists, and no phase was advanced. `devforge --help` was read to establish which subcommands a
  local build exposes; that is not a gate result.
- **Conditions invalidating this handoff:** any change to the 26 candidate files; a new
  revision of SKILL-012, the change-request template or the shared handoff template; a change to
  the `devforge-evaluate-expert` runner interface at a revision after `e641797`; an integration
  owner implementing any of the five missing checks; another Claude skill being added, which
  dates the installed-inventory statement in `references/impact-tracing.md`.

Retain the exact referenced bytes and any earlier failures; a digest cannot recover a missing
source. Record an identity change as a new revision rather than rewriting prior evidence.

A prepared transfer is not receiving execution and not acceptance. This document authorises no
evaluation, installation, activation or automatic invocation of a receiver. No self-digest, and
no circular receipt reference.
