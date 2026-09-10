---
schema_version: "devforge.artifact/v1"
artifact_id: "HANDOFF-REL-SCAFFOLD-001"
artifact_type: "handoff"
project_id: "devforgeai"
revision: 3
status: draft
created_at_utc: "2026-09-10T22:15:48Z"
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
  - artifact_id: EVREPORT-REL-SCAFFOLD-001
    revision: 1
    store: worktree
    path: docs/skill-authoring/history/claude-scaffolding-20260910/devforge-release/validation/scaffold-review/verification-results.md
    sha256: "6bf0d875ac08ffdec392f1fb4a325a94c7ba107d612823c5c5f805cdbe77343e"
    sections:
      - "Findings"
      - "Decision and coverage"
  - artifact_id: CHGSPEC-REL-SCAFFOLD-001
    revision: 1
    store: worktree
    path: docs/skill-authoring/history/claude-scaffolding-20260910/devforge-release/validation/scaffold-review/skill-enhancement-spec.md
    sha256: "c5048e3143470ee8596a9498b677bdb12730794f0a1d0ea4708c9ee4011f4f17"
    sections:
      - "Requested changes"
      - "No target edit: F-005, F-007, F-008"
evidence:
  - "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-release/validation/scaffold-review/findings.json, sha256 c3221dcf9e2c27a1b288453cf5f150a72a8659a13cfb596a91ee7408c6b768a2 (read-only intake; not modified)"
  - "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-release/authoring/file-manifest.json"
  - "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-release/authoring/authoring-notes.md"
  - "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-release/authoring/spec-mapping.md"
  - "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-release/authoring/design/skill-design-spec.md"
supersedes:
  artifact_id: HANDOFF-REL-SCAFFOLD-001
  revision: 1
  store: git
  locator: "commit dd1ae32b12ea209e71dbe338ab76bcbabd721e2e, docs/skill-authoring/history/claude-scaffolding-20260910/devforge-release/authoring/handoff.md"
  sha256: "231845383ef2e39fb0edef37606ff2159c49bfdd1dad75b5c7a26e9c5372f215"
  numbering_note: "The bytes at ccacc96 and at dd1ae32 both carried revision 1; neither was renumbered at the time. The coordinator selected revision 3 for this repair pass, so the sequence skips 2. Both prior byte-sets remain reachable at those commits and neither was rewritten."
decision_ref: null
missing_inputs:
  - "execution_ref: no session-record artifact was supplied for this authoring assignment. The scope came from the coordinator packet. A worker-authored session ID would not be proof of ownership, so this stays null."
  - "The Python JSONL runner and deterministic graders that evals/cases.jsonl targets are pinned at commit e641797eebf04cd1e8eb9f711549e038e7745407 in the devforge-evaluate-expert worktree and are installed nowhere. That package remains a draft under its own bootstrap-review chain."
  - "No Claude Code client version was observed. Every client-behaviour claim in the package comes from the published documentation retrieved 2026-09-10 and is labelled as such."
  - "Whether the shared release-record template's Codex-named line should be made provider-neutral is an open decision for that template's owner (F-005). No target edit was made and none is available from inside this fence."
  - "Tiers C, B and A remain unobserved because no execution allocation exists (F-008). Owner: the DevForge integration owner. Editing the candidate does not produce these observations."
---

# Authoring handoff: devforge-release (Claude, SKILL-011 scaffold)

## Result and next action

- **Result:** A Claude skill package, `providers/claude/plugins/devforgeai/skills/devforge-release`, authored from SKILL-011 revision 2 and revised once by repair pass 1 against the independent scaffold review. 25 files: `SKILL.md`, two assets, four references, and an `evals/` tree of authored cases, fixtures and trigger queries. Complete as a scaffold. Its exact identity is `file-manifest.json`, in the evidence table below.
- **Why:** No `devforge-release` existed in either provider's inventory at base `c17e758417da64928a0f47fc2600304465ac3f3c`, so this is original authoring rather than a port, and the selection decision was **create**. The search scope and its limits are in the design document section 9 - the honest result is "no suitable skill found in the searched inventory", not "no such skill exists".
- **Limits and blockers:** Every proposed default is a proposal nobody approved. Four enforcement requirements (R1-R4) are recorded with no implementation. `devforge-change`, the specification's named consumer, does not exist. The evaluation runner this package's `cases.jsonl` targets is a draft under repair and is installed nowhere. Two acceptance behaviours - interruption-and-resume, post-release operational failure - have no eval case, for reasons recorded in `spec-mapping.md`. **Repair pass 1 changed the candidate, so the review that produced it no longer covers these bytes: none of its eight findings is closed and all of them need reevaluation against the new identity.**
- **Next:** An independent evaluator reevaluates the repaired candidate. The copyable task is below. The author cannot supply that judgement of its own candidate, and applying a requested change does not close the finding that requested it.
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
| input | EVREPORT-REL-SCAFFOLD-001@1 (independent scaffold review of `dd1ae32`) | worktree, `../validation/scaffold-review/verification-results.md` | `6bf0d875ac08ffdec392f1fb4a325a94c7ba107d612823c5c5f805cdbe77343e` | Findings; Decision and coverage | read-only intake; not modified |
| input | CHGSPEC-REL-SCAFFOLD-001@1 (repair specification) | worktree, `../validation/scaffold-review/skill-enhancement-spec.md` | `c5048e3143470ee8596a9498b677bdb12730794f0a1d0ea4708c9ee4011f4f17` | Requested changes; No target edit | read-only intake; not modified |
| output | devforge-release package, 25 files, repair pass 1 | worktree, `providers/claude/plugins/devforgeai/skills/devforge-release/` | see `file-manifest.json` | — | authored candidate, new identity; NOT_EVALUATED |
| output | working design specification, revision 1 | worktree, `.../devforge-release/authoring/design/skill-design-spec.md` | `81cffb23d176008c929f0648094aecafd841376f2efca4042b5654671e476c17` | sections 5, 7, 9, 10, 12 | filled; expectations written before the candidate |
| output | package file manifest | worktree, `.../devforge-release/authoring/file-manifest.json` | `dfc32d0c254bd95f65566e4117aa9f11799a86e894723c9574c06fa458c239fa` | `files_sha256` | complete; excludes its own digest |
| output | authoring notes, with the repair-pass-1 record | worktree, `.../devforge-release/authoring/authoring-notes.md` | `eacfe77786dda368407e0833ea88d5d84e283d21339d65837aed7c0ef47b204a` | "Commands actually run", "Repair pass 1", "Unresolved items" | complete |
| output | specification mapping | worktree, `.../devforge-release/authoring/spec-mapping.md` | `29031c2397523a7f928a97e80a6826b19be3c3481abf5368f0184c89c6e2abac` | "Validation and behavioral acceptance", "Gaps in this mapping" | complete |

The package's own `SKILL.md` digest is `b4ac89032c8b17ee6d201033290833c1498e06952f5885e80b331b50629112fe`; the pre-repair bytes hashed `7b7796d4cfef18f9c7734f6cb8219d627c61abd7f5ce1fab0da642919411a51f` and stay reachable at `dd1ae32`. That is the value an artifact this skill later produces would carry as `producer.skill_revision` - the digest of one file, not of the package and not a plugin version.

## Evidence and reading order

| Read when | Record and relevant sections | Purpose |
| --- | --- | --- |
| First | `file-manifest.json`, then `providers/claude/plugins/devforgeai/skills/devforge-release/SKILL.md` | Bind the exact candidate bytes, then read what it actually instructs. |
| Second | `design/skill-design-spec.md` sections 7 and 9 | The acceptance cases as they were stated before the candidate was written, and the proposed defaults that are still only proposals. |
| Before grading | `spec-mapping.md` | Every SKILL-011 row mapped to a file, a section and an eval case ID - including the four rows with no eval coverage and why. |
| Before trusting any digest or command claim | `authoring-notes.md`, "Commands actually run" | The complete list of what was executed, including the one runner invocation and exactly what it does and does not establish. |
| For an authority or enforcement question | `design/skill-design-spec.md` section 5, routes R1-R4 | Each recorded requirement with its evidence, intended allow/refuse behaviour, owner and feasibility. None is implemented. |

## Proposed evaluation cases

The cases, with their independently stated expectations, are in `evals/evals.json` (**ten** tier-B cases: the five SKILL-011 acceptance rows, the four common cases, and the untrusted-data case added in repair pass 1), `evals/cases.jsonl` (ten deterministic and routed cases) and `evals/triggers/trigger-queries.json` (21 tier-A queries, fixed split stratified by `should_trigger` and category, unchanged by the repair). They were captured, not executed.

| Check | Outcome | Evidence or receipt | Cause or scope limit |
| --- | --- | --- | --- |
| Tier C: installed resources and outputs | NOT_RUN | none | Requires an actual installation or export in a consuming project where the source docs are unreachable. Nothing was installed. |
| Tier B: output quality and boundaries | NOT_RUN | none | Requires an execution allocation, two clean contexts, and the `without_skill` baseline arm. Nothing was executed. |
| Tier A: discovery and activation | NOT_RUN | none | Requires the installed package in a fresh terminal and a real consultation trace. Nothing was observed. |
| Case-file schema load | Completed, exit 0 | `authoring-notes.md`, "The only execution" and "Verification after the repairs" | Establishes only that `evals/cases.jsonl` loads against the pinned runner: valid JSONL, no duplicate `case_id`, no unknown grader, every `candidate_subpath` resolving. Re-run after the repairs against `e641797`; all ten cases COMPLETED with every assertion matching the expectation its case states. Not an evaluation; no row adopted as an outcome; tier C remains NOT_RUN. |
| Structural conformance of the package | NOT_RUN as a check | — | The schema-load run's deterministic rows are observations about bytes, not a structural gate. No DevForge command checks this package. |
| Independent semantic review | NOT_RUN | none | This is the next owner's job. An author cannot supply it. |

`NOT_RUN` is planned and unattempted. `COULD_NOT_RUN` is a required observation that was blocked, with its cause. `NOT_APPLICABLE` is a stated scope exclusion. The absence of an error is not a pass.

## Repair pass 1

One consolidated repair against the independent scaffold review of `dd1ae32`. Three MINOR and two ADVISORY findings produced target edits; three findings produced none. The full F -> CHG -> disposition table, with file and line for each edit, is in `authoring-notes.md` under "Repair pass 1".

| Finding | Severity | Disposition |
| --- | --- | --- |
| F-001 description over the portable 1,024-character maximum | MINOR | applied - trimmed to 1,016, every discriminating clause preserved, limit and source recorded in `references/sources.md` |
| F-002 runtime worked example reuses eval fixture identifiers | MINOR | applied - two identifiers decoupled in `references/recording-rules.md`; no fixture bytes changed |
| F-003 no case discriminates the untrusted-data posture | MINOR | applied - one tier-B case and one fixture added; the trigger-query half declined, with the reason recorded |
| F-004 stale runner and grader pin | ADVISORY | applied - repinned to `e641797` with both digests recomputed; the prior pin retained, not deleted |
| F-005 Codex-named line in a byte-exact shared template copy | ADVISORY | **no target edit** - routed to the shared template owner; the existing open-item record preserved |
| F-006 worked-good fixture writes PASS in a delivery row | ADVISORY | applied - one fixture table cell reworded; every other cell unchanged |
| F-007 spec-mapping names the wrong file for `docs/mvp` | ADVISORY | applied in the authoring evidence, outside the package identity |
| F-008 tiers C, B and A not run | ADVISORY | **no target edit** - an evaluation prerequisite for the DevForge integration owner |

**Applied means the source was edited. It does not close a finding.** The candidate is a new identity and every finding needs new matching evidence. No case, graded observation or expectation was weakened or removed to accommodate a repair; the evaluator's severities and finding IDs are carried exactly as supplied.

## Copyable next task

`devforge-evaluate-expert` exists as a Claude package only in an uncommitted-to-main worktree at `e52ac59`, is a draft under repair, and is installed nowhere. So this is a plain-language task, not a slash command. Every path is a host path, absolute.

```text
Goal: An independent REevaluation of the repaired Claude devforge-release candidate against
SKILL-011, reporting tiers C, B and A separately and in that order, and readjudicating the
eight findings of the prior review against the new bytes.

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
those digests - the package is 25 files now, not the 24 the prior review froze. Evaluate the
ten authored tier-B cases in evals/evals.json and the tier-A queries in
evals/triggers/trigger-queries.json. Run the deterministic cases in evals/cases.jsonl with
the runner and graders committed at e641797eebf04cd1e8eb9f711549e038e7745407, treating its
rows as observations and never as outcomes. Readjudicate F-001 through F-008 from
../validation/scaffold-review/findings.json against the new bytes; none of them is closed by
this repair. Judge the proposed defaults listed in authoring-notes.md on their merits; none
was approved.

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
exported copy of this package exists; the runner package is still a draft. F-005 awaits the
shared template owner and F-008 awaits the integration owner; neither is the evaluator's to
close.
```

## Retention and continuation limits

- **Output readback:** every digest in the outputs table was computed after that file's bytes were final and read back afterwards. Excludes this handoff.
- **This handoff's location:** `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-release-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-release/authoring/handoff.md`.
- **This handoff's receipt:** compute its digest after saving and reading it back, and deliver the path and digest in the terminal response to the coordinator. It is not written into this document, and this document is not edited later to record it.
- **Worktree ownership:** retained by this author until the coordinator releases it. Branch `author/claude-devforge-release-scaffold-20260910`, base `c17e758417da64928a0f47fc2600304465ac3f3c`. The fenced paths are committed on that branch by this author after these bytes were final; nothing is pushed, and the commit identity is delivered in the terminal response rather than written back into this document.
- **External gate state:** none. No DevForge command was run against this package, and none checks it.
- **Conditions invalidating this handoff:** any change to the package bytes; a revision of SKILL-011 past revision 2; a change to either copied template; a move of the runner pin past `e641797`, or a repair there that changes the case schema, the grader names or the `expect` handling; a change to the assigned worktree, branch or fence.

Retain the exact referenced bytes and any earlier failures; a digest cannot recover a missing source. Record an identity change as a new revision rather than rewriting prior evidence.

A prepared transfer is not receiving execution. This document authorises no evaluation, installation, activation or automatic invocation of a receiver, and the package it hands over describes deployments and external actions that this authoring session did not perform and did not simulate: nothing was tagged, published, merged, deployed or communicated. No self-digest, and no circular receipt reference.
