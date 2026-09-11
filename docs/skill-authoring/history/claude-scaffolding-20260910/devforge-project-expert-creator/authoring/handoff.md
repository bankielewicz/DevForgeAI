---
schema_version: "devforge.artifact/v1"
artifact_id: "HANDOFF-CLAUDE-SKILL007-20260910"
artifact_type: "handoff"
project_id: "DevForgeAI"
revision: 2
status: draft
created_at_utc: "2026-09-10T18:33:02Z"
producer:
  skill: "operator-author bootstrap; no builder skill was invoked"
  skill_revision: "unknown; no producing skill was installed or loaded. The authored candidate's own SKILL.md digest is an output identity, not a producer identity, and is recorded in file-manifest.json."
execution_ref: null
upstream:
  - artifact_id: "SKILL-007"
    revision: 3
    store: project
    path: "docs/mvp/specifications/skill-007-devforge-project-expert-creator.md"
    sha256: "983b5714a8285a10873f9d43861349b4b792a779aed1d7e5e6fd4af4e3efac1c"
    sections:
      - "User goal and use-case inventory"
      - "Inputs and provenance"
      - "Workflow and phase exits"
      - "Outputs and standardized templates"
      - "Validation and behavioural acceptance"
      - "Rework, stopping, and recovery"
  - artifact_id: "skill-authoring-contract"
    revision: 3
    store: project
    path: "docs/mvp/skill-authoring-contract.md"
    sha256: "371462385b4e32d1b347f959abb779f4be4251e357c5720a9aef039113eb4b53"
    sections:
      - "Scope and sources"
      - "Sources, ownership, and runtime copies"
      - "Per-skill structure and distribution"
      - "Three separately reported evaluation tiers"
evidence:
  - kind: "candidate file manifest"
    store: project
    path: "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-project-expert-creator/authoring/file-manifest.json"
    sha256: "4b3f13faca72187a10e08d2359b796d9173c7a82306e26a4f8c8c769b513712c"
    description: "25 package-relative paths and digests for the authored candidate."
  - kind: "authoring record"
    store: project
    path: "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-project-expert-creator/authoring/authoring-notes.md"
    sha256: "bbf59c955f8f6f69614e51dba76e476da87d15720a4926a120a9eec98488253a"
    description: "Bootstrap route, Codex source revision, preserved baseline behaviours, provider transformations, commands actually run, unresolved questions."
  - kind: "requirement mapping"
    store: project
    path: "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-project-expert-creator/authoring/spec-mapping.md"
    sha256: "6bb979ca85884530aa60b9d243419e75df48187aaff6cb8294d888e1d8dce48b"
    description: "Every SKILL-007 row mapped to a package file and section and an eval case ID, including rows recorded NOT_APPLICABLE."
  - kind: "package derivation record"
    store: project
    path: "providers/claude/plugins/devforgeai/skills/devforge-project-expert-creator/references/derivation.json"
    sha256: "f64e558ee69307054372a890042b228c207a3b545a3491bdd8b75aea128038a7"
    description: "Source paths, revisions and digests for every copied and adapted file; superseded baseline; what was deliberately not carried from the Codex source. See file-manifest.json for the authoritative current digest of this file."
supersedes: "HANDOFF-CLAUDE-SKILL007-20260910@1, candidate commit 69b6090bde458f48cae0f5751035be65fdb4593c; prior bytes reachable at that commit"
decision_ref: null
missing_inputs:
  - "Tier A discovery and activation observations for this candidate: not obtained."
  - "Tier B output-quality observations against an old_skill baseline: not obtained."
  - "Tier C installed-resource observations: not obtained."
  - "The Claude devforge-evaluate-expert package, which supplies the Python JSONL runner and deterministic graders these evals depend on: not present at this revision."
  - "Authority-selected session record (execution_ref): none was supplied by the task packet, so execution_ref is null. The worktree, branch and base commit actually assigned are recorded in authoring-notes.md; their presence does not establish an authority-selected session record."
---

# Authoring handoff: Claude devforge-project-expert-creator

## Result and next action

- **Result:** The Claude `devforge-project-expert-creator` package was enhanced from a three-file draft to a complete 25-file candidate, adapted from the Codex creator at base `c17e758417da64928a0f47fc2600304465ac3f3c`. This is **revision 2**, after repair pass 1 against the independent E1 bootstrap review; it supersedes candidate commit `69b6090bde458f48cae0f5751035be65fdb4593c`, whose bytes stay reachable at that commit. Two files changed in the pass (`SKILL.md`, `references/derivation.json`); the other twenty-three are byte-exact. Authoring is complete for the assigned scope.
- **Why:** The one decision that shapes what happens next is the reassignment of `devforge expert bind` and `devforge check` from the creator to the operator and integration owner, per SKILL-007 revision 3's Authoring exit ("no target tests, binding or installation by creator"). The commands were retained in the package's knowledge with their owners named, not deleted. See `authoring-notes.md`, "Claude baseline preserved".
- **Limits and blockers:** Nothing in this package has been evaluated, installed, exported, bound or executed. The open items needing a coordinator or integration-owner decision are listed in `authoring-notes.md` under "Unresolved questions"; F-005 and F-006 from the E1 review join them there.
- **Next:** An independent evaluator performs tiers C, then B, then A against this exact candidate. The runner dependency below must be resolved first.
- **Readiness:** **Prepared, not ready.** The Claude `devforge-evaluate-expert` package does not exist at this revision, so the harness that would execute `evals/evals.json` and the trigger queries is unavailable. That prerequisite is owned by the parallel port and the evaluation owner.
- **Validation status:** Not performed.
- **Behavioural status:** NOT_EVALUATED.
- **Enforcement status:** requirements recorded; no gate implemented by this skill.
- **Finding status:** source changes recorded; reevaluation required. Repair pass 1 applied F-001 through F-004 from the independent E1 bootstrap review; F-005 and F-006 were declined as no-target-edit by both the evaluator and the coordinator. An applied change closes no finding.

## Outputs produced

This handoff is excluded from the table: it does not carry its own digest and does not list itself.

| Direction | Artifact | Store and path | SHA-256 | State |
| --- | --- | --- | --- | --- |
| output | Candidate package, 25 files, revision 2 | project, `providers/claude/plugins/devforgeai/skills/devforge-project-expert-creator/` | see `file-manifest.json` | authored, unevaluated |
| input | E1 bootstrap review (SEVAL-E1-001) | project, `.../validation/bootstrap-review-e1/` | findings.json `e6c133d3c5dad5d58a73d97db0447b4c408616dc792690489e43a857cbc8d7af`; repair-spec.md `23a98aa48f93c29aae49e57dd59f0a0b748049795372b71e2b363d5d7cdfef54` | read-only, unmodified |
| output | Candidate file manifest | project, `.../authoring/file-manifest.json` | `4b3f13faca72187a10e08d2359b796d9173c7a82306e26a4f8c8c769b513712c` | complete |
| output | Authoring record | project, `.../authoring/authoring-notes.md` | `bbf59c955f8f6f69614e51dba76e476da87d15720a4926a120a9eec98488253a` | complete |
| output | Requirement mapping | project, `.../authoring/spec-mapping.md` | `6bb979ca85884530aa60b9d243419e75df48187aaff6cb8294d888e1d8dce48b` | complete |
| input | SKILL-007 revision 3 | project, `docs/mvp/specifications/skill-007-devforge-project-expert-creator.md` | `983b5714a8285a10873f9d43861349b4b792a779aed1d7e5e6fd4af4e3efac1c` | governing, unchanged |
| input | Codex creator package, 18 files | project, `providers/codex/plugins/devforgeai/skills/devforge-project-expert-creator/` | see `references/derivation.json` `port_source` | read-only, unchanged |
| input | Claude baseline, 3 files | git, commit `c17e758417da64928a0f47fc2600304465ac3f3c` | see `references/derivation.json` `claude_baseline_superseded` | superseded, bytes reachable |

Every digest above was computed after the referenced file's bytes were final, and the package digests in `file-manifest.json` were verified against the files on disk after the last write.

## Evidence and reading order

| Read when | Record and relevant sections | Purpose |
| --- | --- | --- |
| First | `file-manifest.json`; the candidate's `SKILL.md` and `references/framework-context.md` | Bind the exact candidate bytes, then see what the skill claims to do and what it explicitly does not own. |
| Before acting | `authoring-notes.md`, "Repair pass 1 - E1 bootstrap review" | See which findings were applied, where, and which were declined and why. |
| Before acting | `spec-mapping.md`, coverage summary and the "Validation and behavioural acceptance" table | See which SKILL-007 row each package section serves and which eval case covers it, including the five rows recorded `NOT_APPLICABLE`. |
| Before judging provenance | `references/derivation.json`, `derivations` and `not_carried_from_port_source` | Confirm each copy's source and transformation, and why three Codex references and the `contracts/` copies were deliberately not carried. |
| For an affected question | `authoring-notes.md`, "Provider transformations" and "Unresolved questions" | Recover the rationale for a specific departure from the Codex package shape, and the open decisions. |
| Before running anything | `evals/evals.json` `runner_dependency`; `evals/triggers/trigger-queries.json` `runner_dependency` | Understand why no case has been executed and what must exist first. |

## Observed checks

| Check | Outcome | Evidence | Cause or scope limit |
| --- | --- | --- | --- |
| Assignment verified before writing | OBSERVED | `git rev-parse HEAD` = `c17e758417da...`, expected branch, clean tree | Recorded in `authoring-notes.md`, "Commands actually run". |
| Every DevForge command named in the package exists | OBSERVED | `devforge --help`, `expert --help`, `check --help`, `expert prepare\|bind\|status --help` | Existence and flag placement only. No command was run against a project. |
| JSON files parse | OBSERVED | `evals.json`, `trigger-queries.json`, `derivation.json` all load | Syntax only; says nothing about content correctness. |
| Recorded destination digests match the files on disk | OBSERVED | Programmatic comparison of every `destination_sha256` in `derivation.json` | No mismatches, and `derivation.json` carries no self-digest. |
| Forbidden-pattern scrub | OBSERVED | grep for `.agents/skills`, `$devforge-`, `agents/openai.yaml`, OpenAI hosts, absolute home paths, `.poc/` | No hits. Remaining "Codex" occurrences are labelled `NOT_APPLICABLE` or historical, plus two verbatim shared-template sections noted below. |
| Tier C: installed resources resolve | NOT_RUN | none | No installation or export was performed. |
| Tier B: output quality against an `old_skill` baseline | NOT_RUN | none | Runner unavailable; see the readiness note. |
| Tier A: discovery and activation | NOT_RUN | none | Requires an installed package in a fresh terminal. |
| Semantic review of the authored content | NOT_RUN | none | An author cannot supply the independent judgement of its own candidate. |

No check above establishes that the skill behaves correctly. A package or digest check proves which bytes exist and were referenced, and nothing more.

## For the evaluator

The candidate's own tests are ten tier-B cases in `evals/evals.json` and twenty-one tier-A trigger queries, with nine synthetic fixtures. Points worth knowing before planning:

- Cases 1-5 are the SKILL-007 acceptance rows; 6-9 are the four additional common cases; 10 covers the rework path.
- Case 7's staleness mismatch is bound to real digests: `fixtures/stale/XPKG-001.md` cites ARCH-001 revision 1 at `65d99ab5...`, the true digest of `fixtures/stale/preserved/ARCH-001.r1.md`, while the file at the cited path is revision 2 at `d30ce790...`. Changing either fixture invalidates that case.
- Case 6 needs the operator to supply the worker identity and a permitted outbox outside the fence, and to hash the protected tree before and after.
- Case 9 requires deliberately *not* staging a policy file or executable at the named paths.
- The trigger split is fixed and stratified at authoring time. Validation entries and their `should_trigger` values must not enter an author-loop or task-worker context.
- Every case declares `baseline_comparison: old_skill`. The baseline is the three-file package at commit `c17e758417da64928a0f47fc2600304465ac3f3c`, whose digests are in `references/derivation.json`.

## Copyable next task

The Claude `devforge-evaluate-expert` skill is not installed in this environment, so this is a plain-language task rather than a slash invocation. Do not substitute a slash command for a skill whose installation has not been confirmed.

```text
Goal: an independent evaluation of the authored Claude devforge-project-expert-creator
candidate, reported as separate tier C, B and A results.

Context:
  Candidate package:
    /home/bryan/Projects/DevForge/worktrees/claude-scaffold-project-expert-creator-20260910/providers/claude/plugins/devforgeai/skills/devforge-project-expert-creator
  Bind these exact bytes using the manifest at:
    /home/bryan/Projects/DevForge/worktrees/claude-scaffold-project-expert-creator-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-project-expert-creator/authoring/file-manifest.json
  Then follow the reading order in:
    /home/bryan/Projects/DevForge/worktrees/claude-scaffold-project-expert-creator-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-project-expert-creator/authoring/handoff.md
  Governing specification: docs/mvp/specifications/skill-007-devforge-project-expert-creator.md
    revision 3, sha256 983b5714a8285a10873f9d43861349b4b792a779aed1d7e5e6fd4af4e3efac1c
  Baseline for output-quality comparison: the three-file package at commit
    c17e758417da64928a0f47fc2600304465ac3f3c (old_skill).

Prerequisite, owned by the evaluation owner and the parallel devforge-evaluate-expert port:
  the Python JSONL runner and deterministic graders. Until those exist, record every
  case COULD_NOT_RUN with that cause rather than reporting an unexecuted case as passing.

Task: install or export the exact candidate under a separate execution allocation,
then run tier C first, then tier B, then tier A, per the authoring contract's ordering.
Do not blend the tiers into one figure.

Preserve: the candidate bytes unchanged; the fixed trigger train/validation split;
the original severities and IDs of anything you find; and this handoff's frozen content.

Output: a validation plan, results, a decision record and a bounded repair specification,
plus a prepared creator handoff, in the assigned evaluation output root. Do not edit the
candidate - the evaluator evaluates and the creator edits.

Stop at: completed tier results, or the stated missing prerequisite with its owner named.
```

## Retention and continuation limits

- **Output readback:** the four output rows above were written, then hashed, then their digests recorded here. The package digests in `file-manifest.json` were verified against the files on disk after the last write.
- **This handoff's location:** `docs/skill-authoring/history/claude-scaffolding-20260910/devforge-project-expert-creator/authoring/handoff.md`. It carries no self-digest.
- **This handoff's receipt:** compute its digest after saving and reading it back, and deliver the path and digest in the terminal response or the permitted outbox. Do not write that digest into this document.
- **Worktree ownership:** retained by worker A1 on branch `author/claude-devforge-project-expert-creator-scaffold-20260910`. No other worktree was touched. Nothing was pushed.
- **External gate state:** none. No `devforge` gate command was run against any project; no state directory, binding or acceptance record was created.
- **Conditions invalidating this handoff:** any change to a candidate file digest in `file-manifest.json`; a new selected revision of SKILL-007 or the authoring contract; a change to `docs/mvp/templates/devforge-project-expert-creator/*` or `docs/mvp/templates/shared/handoff.md`; arrival of the Claude `devforge-evaluate-expert` package, which may supersede the record shapes stated in `references/validator-handoff.md`.

Two dispositions belong to the integration owner, not to this author: the "Promoted Codex content mapping" sections carried verbatim inside `assets/expert-spec.md` and `assets/expert-package.md`, which are `NOT_APPLICABLE` to a Claude package but could not be edited without changing a shared template's governing meaning; and whether the omission of `references/contracts/` copies, in favour of the distilled `references/framework-context.md`, is acceptable divergence from the Codex package shape.

A prepared transfer is not receiving execution and not acceptance. This document authorises no evaluation, installation, activation, binding or automatic invocation of a receiver. Preparing it neither invokes the evaluator nor grants an allocation.
