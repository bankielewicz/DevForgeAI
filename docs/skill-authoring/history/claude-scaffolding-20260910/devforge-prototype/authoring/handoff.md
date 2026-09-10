---
schema_version: "devforge.artifact/v1"
artifact_id: "HANDOFF-CLAUDE-PROTOTYPE-SCAFFOLD-20260910"
artifact_type: "handoff"
project_id: "devforgeai"
revision: 1
status: draft
created_at_utc: "2026-09-10T19:38:44Z"
producer:
  skill: "not a skill run - operator-author following devforge-project-expert-creator at 4999f3106565c5e320d1f1a7db066b437e4e94be as source-loaded instructions"
  skill_revision: "not applicable - no skill was loaded or invoked"
execution_ref: null
upstream:
  - artifact_id: "SKILL-004"
    revision: 2
    store: "project"
    path: "docs/mvp/specifications/skill-004-devforge-prototype.md"
    sha256: "e4f61c35220641f053a828615df1bc3415c707fde26fcf8b0cdece6cdb1ba54c"
    sections_used: ["User goal and use-case inventory", "Inputs and provenance", "Workflow and phase exits", "Outputs and standardized templates", "Validation and behavioral acceptance", "Additional common cases", "Rework, stopping, and recovery", "Native creator authoring prompt", "Completion handoff"]
evidence: []
supersedes: null
decision_ref: null
missing_inputs:
  - "No session record exists for this scaffold pass, so execution_ref is null. The assignment came from a coordinator packet, which is not a session artifact."
  - "No client observation of discovery, loading or activation. Tier A is unobserved, not negative."
---

# Authoring handoff: devforge-prototype (SKILL-004), Claude scaffold

Next owner: **an independent evaluator**. This document prepares a transfer. It invokes nothing and accepts nothing.

## Result and next action

- **Result:** A new Claude `devforge-prototype` package was created from SKILL-004 revision 2. 31 files: `SKILL.md`, three assets, five references, and a source-only `evals/` tree with 11 tier-B cases, 9 deterministic runner cases, 22 trigger queries and 19 synthetic fixtures. No prior package existed and nothing was overwritten.
- **Why it matters for what happens next:** the deterministic eval arm is authored against a runner in the Claude `devforge-evaluate-expert` package at `e52ac596cbf790dfa156d883852d392c512fdbcc`, which is source-only, not installed, and itself under independent review. An evaluator planning the C and structural arms needs that package staged first, or has to record those observations as `COULD_NOT_RUN`.
- **Limits and blockers:** every decision SKILL-004 leaves silent is recorded as a **proposal** awaiting a decision (destinations, default fence path, the three near-miss exclusions beyond develop). Four DevForge CLI integrations this workflow would need do not exist and are recorded as open requirements. Nothing in the package claims otherwise.
- **Next:** an independent evaluator plans and runs tiers C, B and A against this candidate, reports them separately, and returns a bounded repair specification. The copyable task is below.
- **Readiness:** prepared, not ready. Tier C needs an installation or export that this pass did not perform; tier A needs a fresh terminal; the deterministic arm needs the runner package staged. Each is a named prerequisite with an owner, not a missing step in this handoff.
- **Validation status:** Not performed.
- **Behavioural status:** NOT_EVALUATED.
- **Enforcement status:** requirements recorded; no gate implemented by this skill.

## Inputs consumed and outputs produced

This handoff is excluded from the table: it cannot contain its own digest and does not list itself among its own outputs. Every digest below was taken after the referenced file's last write. Paths are repository-relative to the worktree named under *Retention*.

| Direction | Artifact | Store and path | SHA-256 | Sections relied on | State |
| --- | --- | --- | --- | --- | --- |
| input | SKILL-004 rev 2 | project / `docs/mvp/specifications/skill-004-devforge-prototype.md` | `e4f61c35220641f053a828615df1bc3415c707fde26fcf8b0cdece6cdb1ba54c` | all | accepted-as-governing draft specification |
| input | skill-authoring-contract rev 3 | project / `docs/mvp/skill-authoring-contract.md` | `371462385b4e32d1b347f959abb779f4be4251e357c5720a9aef039113eb4b53` | packaging, tiers, fixtures | current |
| input | experiment-plan template | project / `docs/mvp/templates/devforge-prototype/experiment-plan.md` | `70af539ce5e32ef8cbdb1648f13b1e0b3ca31f829387f159875a41f64db20564` | whole file | copied byte-identically |
| input | prototype-report template | project / `docs/mvp/templates/devforge-prototype/prototype-report.md` | `9cf2c9d3b54c69ae735036f97ba898891b04247e8a1f613413a2d8b70c213252` | whole file | copied byte-identically |
| input | shared handoff template | project / `docs/mvp/templates/shared/handoff.md` | `abc7f8e0ca545093d3b1486d1a86cb7e51609aef17c0027b951a47da6eaed206` | whole file | bounded adaptation |
| input | builder `SKILL.md` at `4999f31` | git / `providers/claude/plugins/devforgeai/skills/devforge-project-expert-creator/SKILL.md` | `342b82923e64cef0c2ab77fdb8fc11b92fc68ea145642c486d2a937c5363f3d9` | all five phases | draft under independent review |
| input | evaluate-expert `scripts/run_cases.py` at `e52ac59` | git / `providers/claude/plugins/devforgeai/skills/devforge-evaluate-expert/scripts/run_cases.py` | `d1fb18689eeea31f8facde4e3de1507320e74ffb349f547f9db2201395bb132d` | `--help`, case schema | source-only, unevaluated |
| output | candidate package (31 files) | project / `providers/claude/plugins/devforgeai/skills/devforge-prototype/` | see the manifest | authored, unevaluated |
| output | package file manifest | project / `docs/skill-authoring/history/claude-scaffolding-20260910/devforge-prototype/authoring/file-manifest.json` | `8373cca56f69423c9265f3d1e483f83971608c0d53a93796334f458b7bd480a7` | all | frozen |
| output | working design specification | project / `.../authoring/design/skill-design-spec.md` | `0a4f91fdaec82fa459caa360fb32034226a244b1b841836c1159745e49e8293c` | §2, §6 routes, §7, §9 | frozen |
| output | requirement mapping | project / `.../authoring/spec-mapping.md` | `a74a3097cdcae41df9010ec05821e1b806d0b3f6b4cce34277f7c299d13181f7` | all | frozen |
| output | authoring notes | project / `.../authoring/authoring-notes.md` | `ba2e0a36e8e7afbd05ac3d83ae3e42a3ee69fd558604559ba1e786b66a8e9447` | commands run; decisions flagged | frozen |

The candidate's `SKILL.md` hashes to `1c348077723e693e0a5a4bba997c501f3ed683f1ef834e9538e069cb193a00e2`. That is the source file's digest. An installed copy's `producer.skill_revision` must be the digest of the **installed** `SKILL.md`, which is the same bytes only if installation copies them unchanged — verify rather than assume.

## Evidence and reading order

| Read when | Record | Purpose |
| --- | --- | --- |
| First | `file-manifest.json`, then the candidate's `references/derivation.json` | Identify the exact candidate bytes and where every copied or distilled file came from |
| Before planning | `spec-mapping.md` | Every SKILL-004 row mapped to a file, a section and a case id, so the plan can be built against requirements rather than against the candidate's headings |
| Before planning | `design/skill-design-spec.md` §7 and §9 | The acceptance cases as captured *before* the candidate was written, and every proposal still awaiting a decision |
| Before acting on a gap | `authoring-notes.md` | Which commands were actually run and what they do and do not establish; the five decisions flagged for a reviewer |
| For enforcement questions | `design/skill-design-spec.md` §6 routes R1–R3, and the candidate's `references/framework-context.md` | The four missing CLI integrations, recorded as requirements with owners and unknown feasibility |

## Proposed evaluation cases

The cases and their independently stated expectations live in the candidate's `evals/` tree — `evals.json` (11 tier-B), `cases.jsonl` (9 deterministic), `triggers/trigger-queries.json` (22 tier-A queries, fixed stratified split). They were captured, not executed.

| Check | Outcome | Evidence or receipt | Cause or scope limit |
| --- | --- | --- | --- |
| Tier A — discovery and activation, fresh terminal, installed package | NOT_RUN | none | No installation was generated and no client was observed. Unobserved, not negative. |
| Tier B — output quality and boundaries, skill path supplied | NOT_RUN | none | Ten of eleven cases have no `old_skill` baseline because no prior candidate exists; those arms are `without_skill`. |
| Tier C — installed resources and outputs, `docs/mvp` absent | NOT_RUN | none | Requires an export or project-local installation that this pass did not perform. |
| Deterministic assertions in `cases.jsonl` | NOT_RUN against this skill | none | Authored against a runner in a package that is source-only and unevaluated. |
| Case-file loadability and fixture discrimination | Completed during authoring | `authoring-notes.md`, "Commands actually run" | **Authoring hygiene over this author's own fixtures. It establishes that the case file parses and the fixtures discriminate. It is not an evaluation of this skill and no row of it may be cited as one.** |

`NOT_RUN` means planned and unattempted. `COULD_NOT_RUN` with an actual cause is what a blocked required observation gets. The absence of an error is not a pass.

## Copyable next task

The receiving capability is **not installed**: the Claude `devforge-evaluate-expert` package exists as source at `e52ac59` and has not been installed, exported or evaluated anywhere. No slash command is named here, because none has been confirmed. The task below is plain language with resolvable absolute paths.

```text
Goal: An independent evaluation of the Claude devforge-prototype candidate against SKILL-004,
      with tiers A, B and C reported separately, plus a bounded repair specification.

Candidate (read-only; do not edit):
  /home/bryan/Projects/DevForge/worktrees/claude-scaffold-prototype-20260910/providers/claude/plugins/devforgeai/skills/devforge-prototype/

Governing specification:
  /home/bryan/Projects/DevForge/framework/DevForgeAI/docs/mvp/specifications/skill-004-devforge-prototype.md
  sha256 e4f61c35220641f053a828615df1bc3415c707fde26fcf8b0cdece6cdb1ba54c

Authoring evidence, in reading order:
  /home/bryan/Projects/DevForge/worktrees/claude-scaffold-prototype-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-prototype/authoring/file-manifest.json
  .../authoring/spec-mapping.md
  .../authoring/design/skill-design-spec.md
  .../authoring/authoring-notes.md

Deterministic runner and graders (source-only, unevaluated, not installed):
  /home/bryan/Projects/DevForge/worktrees/claude-scaffold-evaluate-expert-20260910/providers/claude/plugins/devforgeai/skills/devforge-evaluate-expert/scripts/run_cases.py
  ... /scripts/graders.py
  at commit e52ac596cbf790dfa156d883852d392c512fdbcc
  Invoke as: python3 <run_cases.py> --cases <candidate>/evals/cases.jsonl
             --candidate <candidate>/evals/fixtures --out <your workspace>/observations.jsonl
  Its MATCH / MISMATCH / INDETERMINATE rows are observations. Do not copy one into a results
  record as a PASS, and do not read its exit status as a verdict about anything.

Task: Freeze the candidate and the specification, plan the evaluation against the requirement
      rows in spec-mapping.md, then run what can actually be run. Report tier C, then B, then A,
      separately and unblended. Record COULD_NOT_RUN with an actual cause for anything blocked -
      an unavailable installation, an unstaged runner, an unobservable client.

Preserve: the frozen candidate bytes, the proposed-default labels in the design spec, the
      recorded-but-unimplemented status of routes R1-R3, and the distinction between this
      author's fixture-discrimination check and an evaluation of the skill.

Do not: edit the candidate, its specification, its cases or its expectations; install anything
      into the author's worktree; or treat a structural observation as evidence about behaviour.

Output: an evaluation plan, an evaluation report with its evidence, and a bounded repair
      specification, in your own assigned workspace. Do not write inside the candidate package
      or inside this authoring directory.

Stop at: a report whose every stated outcome is bound to an actual observation, with the
      unobserved parts named and caused.
```

**Prerequisites this task does not resolve, with owners:**

1. Tier C needs an export or project-local installation of the candidate — integration owner.
2. Tier A needs a fresh terminal with the package actually installed and no competing copy — integration owner, then the evaluator.
3. The deterministic arm needs the `devforge-evaluate-expert` runner staged and readable — whoever owns that worktree.

## Retention and continuation limits

- **Output readback:** the 31 candidate files and the four authoring records above, at the digests listed. Excludes this handoff.
- **This handoff's location:** `docs/skill-authoring/history/claude-scaffolding-20260910/devforge-prototype/authoring/handoff.md` in the worktree `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-prototype-20260910`, branch `author/claude-devforge-prototype-scaffold-20260910`, base `c17e758417da64928a0f47fc2600304465ac3f3c`. No self-digest.
- **This handoff's receipt:** its digest is computed after saving and read back, then delivered in the terminal response. It is not written into this document.
- **Worktree ownership:** retained by this author until the coordinator reassigns it. An evaluator works read-only against the paths above and writes only in its own workspace.
- **External gate state:** none. No DevForge command was run against any project, and no gate, policy, test or pin was read for modification or modified.
- **Conditions invalidating this handoff:** SKILL-004 revising past revision 2; either output template or the shared handoff template changing; the candidate bytes changing (any manifest digest ceasing to match); the `devforge-evaluate-expert` runner interface changing; the DevForge CLI gaining any of the four missing integrations.

A prepared transfer is not receiving execution and not acceptance. This document authorises no evaluation, installation, activation or automatic invocation of a receiver, and no observation recorded during authoring transfers to the evaluation that has not happened.
