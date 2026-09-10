---
schema_version: "devforge.artifact/v1"
artifact_id: "CHGSPEC-E3-001"
artifact_type: "skill-enhancement-spec"
project_id: "DevForgeAI"
revision: 1
status: draft
created_at_utc: "2026-09-10T21:21:51Z"
producer:
  skill: "devforge-evaluate-expert"
  skill_revision: "bdf665c7e18061395c0762de7a377fdc5f6ed48d66245df5623c5c32b90cf2ac"
execution_ref: null
upstream:
  - artifact_id: "EVREPORT-E3-001"
    revision: 1
    store: "project"
    path: "verification-results.md"
    sections_used: ["Findings", "IR-1 … IR-10 Criterion records", "S-02 Deterministic case run", "S-04 Derivation record versus actual bytes", "Missing capabilities and evaluation prerequisites"]
  - artifact_id: "SKILL-007"
    revision: 3
    store: "project"
    path: "/home/bryan/Projects/DevForge/framework/DevForgeAI/docs/mvp/specifications/skill-007-devforge-project-expert-creator.md"
    sha256: "983b5714a8285a10873f9d43861349b4b792a779aed1d7e5e6fd4af4e3efac1c"
evidence:
  - kind: "runner observations"
    path: "runner-out/observations.jsonl"
    sha256: "d75c603fe34dd49531191682f659dfe40d12108e5ae4cd65603197d3f48dc2a6"
  - kind: "authored case file"
    path: "runner-out/cases.jsonl"
    sha256: "3a8cc1952adebf05dd0eee2cd17330b23adf0ea94a3c53f99129ec4509c9e06e"
  - kind: "grader self-check"
    path: "runner-out/validator-graders-selfcheck.jsonl"
    sha256: "764e07d8957b9167e2d7c969182a39cedb3a0b645a9ff731194b034c2c22565f"
supersedes: null
decision_ref: null
missing_inputs:
  - "No installed copy, fresh terminal or isolated workspace: tiers C, B and A are NOT_RUN and no change below rests on a native observation."
  - "No execution_ref/SESSION record was supplied to this worker."
---

# Skill repair and enhancement specification

The bounded, evidence-backed change request returned to `devforge-project-expert-creator`. It authorises no automatic edit,
invocation, installation, acceptance or release, and it carries forward the existing user authorisation without expanding it.

## Immutable intake

- **Evaluated candidate:**
  `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-project-expert-creator-20260910/providers/claude/plugins/devforgeai/skills/devforge-project-expert-creator`
  at commit `4999f3106565c5e320d1f1a7db066b437e4e94be`; worktree HEAD `8c0bdd0d86c7330d2f7910d63b3511e8df43d20b` with
  `git diff 4999f31 HEAD --stat -- providers/` empty. 25 files; complete manifest in `verification-results.md` section S-01.
  `SKILL.md` `342b82923e64cef0c2ab77fdb8fc11b92fc68ea145642c486d2a937c5363f3d9`;
  `references/derivation.json` `f64e558ee69307054372a890042b228c207a3b545a3491bdd8b75aea128038a7`.
- **Installed copy evaluated:** not installed. No project-local `.claude/skills` copy and no exported plugin exists.
- **Specification:** SKILL-007 revision 3,
  `/home/bryan/Projects/DevForge/framework/DevForgeAI/docs/mvp/specifications/skill-007-devforge-project-expert-creator.md`,
  sha256 `983b5714a8285a10873f9d43861349b4b792a779aed1d7e5e6fd4af4e3efac1c`.
- **Evaluation report:** `EVREPORT-E3-001` — `verification-results.md` in this directory. Its digest is delivered in
  `handoff.md` rather than here, because it is written after this file.
- **Results record:** `findings.json` in this directory (the machine-readable half; see its `note` field for the fence deviation).
- **Independent review:** `verification-results.md` sections IR-0 … IR-10 and `findings.json` `ai_review`. Performed;
  the independence limits, including one declared contamination, are recorded in IR-0 and must be read with the outcomes.
- **Cases and fixtures:** the candidate's own eval inputs were **not** used to grade behaviour and were only inspected
  (`evals/evals.json` `64de1a96…`, `evals/triggers/trigger-queries.json` `29a4fe7f…`, nine fixtures per S-01). The
  deterministic cases this evaluation ran were authored in its own fence: `runner-out/cases.jsonl` `3a8cc195…`.
- **Prior iteration:** candidate `69b6090bde458f48cae0f5751035be65fdb4593c` (`SKILL.md` `1e9929a5…`), reviewed by E1 as
  `SEVAL-E1-001` and rechecked at `4999f31` as `SEVAL-E1-002`. Retained, not superseded by this report.
- **Baseline:** `old_skill` at `c17e758417da64928a0f47fc2600304465ac3f3c`, three files, frozen by digest, **not executed**.

Preserve these identities exactly. Verify them before editing and retain the old candidate.

## Change decision

- **Are target changes justified by the evidence?** **Partly — yes for two MINOR contained defects, no for the rest.**
  - **Yes:** F-002 and F-003 are demonstrated factual defects in shipped bytes, each with a one-place bounded correction
    (CHG-001, CHG-002).
  - **No:** F-001 and F-007 are unresolved interpretations that belong to the integration owner; editing the candidate on
    this evidence would settle a contract question the evaluator has no authority to settle (CHG-003 is a bounded
    investigation, not a patch). F-006 is an evaluation prerequisite — no edit produces a missing observation. F-004 is an
    optional proposal that no accepted requirement supports.
  - **CHG-004 (from F-005) is an authorised enhancement, not a required repair** — apply it only if the author agrees the
    point-of-use note is worth one sentence.
- **Next owner:** `devforge-project-expert-creator`
- **Behaviour that must be preserved unchanged:** the five-phase workflow and its exits; the authoring-only boundary and the
  author/evaluator separation; search-before-create with recorded search limits; specification-before-candidate; the
  one-to-three-questions-per-round rule and the do-not-reopen-settled-decisions rule; the supplied-material-is-data rule at
  `SKILL.md:42`; the fixed result vocabulary and "the absence of an error is not a pass"; "Validation status: Not performed."
  and behavioural `NOT_EVALUATED`; the no-self-digest rules; the byte-identity of `assets/expert-spec.md`,
  `assets/expert-package.md` and `assets/expert-skill.md` with their `docs/mvp` sources; every `evals/` case, expectation,
  fixture, trigger query, id, category and split assignment; the package's identity, frontmatter and invocation policy.
- **Forbidden scope changes:** do not edit `assets/expert-spec.md`, `assets/expert-package.md` or `assets/expert-skill.md`
  (byte-identity with `docs/mvp` is verified evidence — PEC-C-012); do not edit any shared contract, template, sibling gate,
  installer policy, the roster, or the DevForge CLI, its policy or its tests; do not weaken, delete or renumber any eval case,
  graded observation, trigger query or expectation; do not add a `scripts/` directory or any framework logic in Python or
  shell; do not add `agents/openai.yaml` or any Codex member; do not rewrite E1's findings, severities or IDs; do not edit
  the candidate to compensate for a missing observation; do not treat any change below as closing a finding.

## Requested changes

### CHG-001: the unavailable-evaluator-helper row names the right cause and the right owner

- **Finding IDs:** F-002
- **Severity:** MINOR
- **Change type:** required repair
- **Accepted requirement, or a new proposal:** accepted requirement — SKILL-007 "Rework, stopping, and recovery"
  ("Report missing observations precisely"), and the package's own `references/derivation.json` `refresh_conditions[4]`,
  which already names this row as the thing to revisit when the paired evaluator package lands.
- **Affected revision, file and section:** `4999f31`; `references/manual-operation.md`, "Command boundaries" table,
  final row (line 40).
- **Evidence and reproduction:** the row attributes the missing package inspector and evidence reducer to a pending Claude
  port. The frozen Claude `devforge-evaluate-expert` package at `e641797` explicitly declines to port them
  (`references/missing-rust-capabilities.md:9-19`: both are unimplemented **DevForge CLI** capabilities, and porting the
  Codex helpers would move framework authority into Python under a new name). Independently confirmed against the binary:
  `devforge --help` on `835c3263…` lists `delivery, expert, check, init, red, green, accept, verify, status, isolate` —
  no skill-package inspector, no evidence reducer. See `verification-results.md` S-06.
- **Demonstrated impact:** the reported outcome ("not available") is true, but the cause, the owner and the unblock
  condition are all wrong. A creator following this row tells a user the gap closes when the evaluator package lands. It
  does not, and no evaluator package can close it. The user is sent to the wrong owner for a prerequisite that blocks a
  structural claim.
- **Bounded desired behaviour:** the row's reason names the two unimplemented DevForge CLI capabilities — skill-package
  structural inspection (S001–S013) and evidence reduction — and the DevForge integration owner as their owner, and states
  that the paired evaluator package deliberately does not supply them. Add the matching entry to `references/derivation.json`
  recording the refresh and its trigger.
- **Behaviour to preserve:** the row's `Not available in this environment` outcome; the rule "do not name a path for a helper
  you have not confirmed exists"; every other row in the table; the surrounding owner assignments; the "Historical identities"
  section. Do not add a path, a command or a helper name.
- **Acceptance condition:** a later evaluation reading `references/manual-operation.md:40` finds the cause attributed to the
  two unimplemented DevForge CLI capabilities with the DevForge integration owner named, no helper path asserted, and a
  corresponding `derivation.json` entry whose destination digest matches the edited file.
- **Affected reruns:** `evals.json` case 9 (`requested-check-could-not-run`) — re-observe after the change. All ten cases
  remain `NOT_RUN` regardless; this names what to re-observe when they are eventually run.

### CHG-002: the eval runner dependency states what executing tier-B cases actually requires

- **Finding IDs:** F-003
- **Severity:** MINOR
- **Change type:** required repair
- **Accepted requirement, or a new proposal:** accepted requirement — SKILL-007 "Validation and behavioral acceptance"
  and the skill-authoring contract's "Three separately reported evaluation tiers".
- **Affected revision, file and section:** `4999f31`; `evals/evals.json`, `runner_dependency` object (lines 7–12),
  fields `detail` and `consequence`.
- **Evidence and reproduction:** `runner_dependency.detail` says executing the cases "requires the Python JSONL runner and
  deterministic graders supplied by the Claude devforge-evaluate-expert package". `tier_note` at line 5 declares all ten
  cases tier B. The validator's `references/runner-interface.md:119` states: "Nothing here observes discovery, activation,
  loading or output quality." This evaluation ran that runner against this package and obtained 44 structural assertions and
  zero output-quality observations (`runner-out/observations.jsonl`).
- **Demonstrated impact:** an owner scoping the evaluation reads "port the runner, then the ten cases run" and
  under-allocates. What the ten cases need is a measured native run per case with the declared `old_skill` baseline arm,
  per-attempt context isolation and separate writable outputs — a different size and kind of allocation. An unobserved
  evidence group looks cheaper to close than it is.
- **Bounded desired behaviour:** `runner_dependency` states that the JSONL runner and deterministic graders cover
  deterministic assertions only; that these ten cases are tier B and require a measured native run per attempt with the
  declared `old_skill` baseline arm and per-attempt isolation; and that an evaluation allocation, not only a ported runner,
  is the unblock condition. `status` and `owner` stay as they are.
- **Behaviour to preserve:** every case, id, name, tier, `spec_case`, prompt, `expected_output`, `graded_observation`,
  `fixture_staging`, `baseline_comparison` and `files` entry, byte-unchanged; `schema_note`, `tier_note`, `fixture_note`,
  `specification`, `grading_axes_note` and `authoring_status`; the `NOT_RUN` status of every case. Weakening or removing a
  case to make the dependency statement true is explicitly forbidden.
- **Acceptance condition:** a later evaluation reading `evals/evals.json` finds the dependency distinguishing deterministic
  assertions from tier-B measured runs and naming the baseline arm and isolation requirement, with all ten cases unchanged
  and still `NOT_RUN`, and `references/derivation.json`'s destination digest for `evals/evals.json` updated to match.
- **Affected reruns:** `evals.json` cases 1–10 (the statement governs how all ten are allocated). No case content changes,
  so no expectation is re-derived.

### CHG-003: bounded investigation — which evaluator record identity does this package receive?

- **Finding IDs:** F-001 (and, for the owner, F-007)
- **Severity:** ADVISORY
- **Change type:** bounded investigation
- **Accepted requirement, or a new proposal:** an unresolved conflict between accepted sources, not a new proposal.
- **Affected revision, file and section:** `4999f31`; `references/validator-handoff.md` lines 9–11 ("What the handoff should
  contain") and `assets/skill-design-spec.md:271` (Evaluator repair intake, Evaluation report row).
- **Evidence and reproduction:** the candidate expects `artifact_type: skill-evaluation-report` with a `SEVAL` identity,
  which `artifact-contract.md:107` and `skill-authoring-contract.md:115` both support. The frozen Claude
  `devforge-evaluate-expert` at `e641797` emits `expert-evaluation-report` / `EVREPORT-###`,
  `skill-enhancement-spec` / `CHGSPEC-###` and `handoff` / `HANDOFF-###`. The package's own copied governing template
  (`assets/expert-spec.md`, "Promoted Codex content mapping") maps EVREPORT to `verification-results.md`, so both identities
  already appear inside the candidate.
- **Demonstrated impact:** a rework session recovering a frozen evaluator handoff looks for a record the paired evaluator
  never produces and logs an intake gap instead of recognising the correct one. The candidate's existing hedge at
  `references/validator-handoff.md:18` is the correct behaviour under this ambiguity and currently contains the damage.
- **The question, and the evidence target:** *which envelope identity is canonical for a Claude skill-evaluation report —
  `skill-evaluation-report`/SEVAL per the artifact and authoring contracts, or `expert-evaluation-report`/EVREPORT per
  SKILL-008 and the `devforge-evaluate-expert` package?* Evidence target: a decision from the DevForgeAI integration owner,
  or a contract revision that says so unambiguously.
- **Bounded desired behaviour now:** **no target edit.** Record the open decision and its owner; keep the existing hedge.
  When `devforge-evaluate-expert` merges — the trigger `references/derivation.json` `refresh_conditions` already names — apply
  the owner's answer as a one-paragraph refresh of `references/validator-handoff.md`, naming both accepted identity sets if
  both survive, and preserving the "stated minimum, not a settled contract" rule.
- **Behaviour to preserve:** the hedge at line 18; the frozen-baseline recovery list; severity preservation; the four change
  types; the evaluation-prerequisite rule; the change-record field list.
- **Acceptance condition:** the owner's decision is recorded and, if it required a package change, a later evaluation finds
  `references/validator-handoff.md` consistent with the records the paired evaluator actually emits.
- **Affected reruns:** `evals.json` case 10 (`rework-from-evaluator-findings`).

### CHG-004: name the inherited Codex section as NOT_APPLICABLE where the author meets it

- **Finding IDs:** F-005
- **Severity:** ADVISORY
- **Change type:** authorised enhancement
- **Accepted requirement, or a new proposal:** a bounded clarification serving the artifact mapping already stated in
  `references/manual-operation.md:5-12`; not a new requirement.
- **Affected revision, file and section:** `4999f31`; `SKILL.md` §3 (line 70) and §5 (line 90) where the author is routed to
  `assets/expert-spec.md` and `assets/expert-package.md`, **or** `references/framework-context.md` "The artifact envelope".
  Author's choice of the single location.
- **Evidence and reproduction:** both assets end with an identical inherited "Promoted Codex content mapping" paragraph that
  maps EVREPORT to a `decision.json` the paired Claude evaluator explicitly does not produce (its `SKILL.md:133`), and names
  Routine/Full lineage fields the package marks `NOT_APPLICABLE` at `assets/skill-design-spec.md:350`. The disposition is
  recorded only in `references/derivation.json` (`carried_inapplicable_section`), a maintenance record an author filling
  XSPEC has no reason to open.
- **Demonstrated impact:** an author meets Codex-side guidance at the point of use with nothing in the reading path marking
  it inapplicable, and may produce or request a `decision.json` no Claude evaluator emits, or reopen Routine/Full fields the
  package has already dispositioned.
- **Bounded desired behaviour:** one sentence, in one place, stating that the "Promoted Codex content mapping" section
  carried verbatim in `assets/expert-spec.md` and `assets/expert-package.md` is Codex-side inherited template text,
  `NOT_APPLICABLE` to a Claude package, and that its disposition belongs to the integration owner.
- **Behaviour to preserve:** **the byte-identity of `assets/expert-spec.md` and `assets/expert-package.md` with their
  `docs/mvp` sources.** Do not edit either file. The prior review's reasoning for declining a template edit (E1/F-005) is
  sound and is preserved; this change deliberately routes around it. Also preserve the existing brevity of `SKILL.md` — one
  sentence, not a new section or reference file.
- **Acceptance condition:** a later evaluation reading `SKILL.md` (or `references/framework-context.md`) finds the note,
  and PEC-C-012 still reports both templates byte-identical to their `docs/mvp` sources.
- **Affected reruns:** `evals.json` case 1 (`direct-activation`).

### Not requested: F-004, F-006, F-007

- **F-004 (`evals/cases.jsonl` absent)** — no accepted requirement asks for it; the contract-mandated eval inputs are all
  present and well formed. Raised as an optional proposal for an **owner** to accept or decline, not as work for the author.
  Do not add it as an unrequested package member. `runner-out/cases.jsonl` in this directory is a working reference if it is
  ever accepted.
- **F-006 (tiers A, B, C `NOT_RUN`)** — an evaluation prerequisite for the evaluation owner. No edit produces a missing
  observation, and no edit should be made to compensate for one.
- **F-007 (Routine/Full applicability)** — an open decision for the DevForgeAI integration owner. The candidate's recorded
  disposition stands until that owner rules.

## Implementation order

CHG-001 and CHG-002 are independent of each other and of everything else; either may be applied alone. CHG-004 is
independent. CHG-003 is an investigation with **no edit now**; if it later authorises a refresh of
`references/validator-handoff.md`, that refresh should follow the owner's decision, not precede it. Any applied change
requires the matching `references/derivation.json` destination-digest update in the same pass — the record's own
`refresh_conditions` treat a stale destination digest as drift, and this evaluation verified all 24 currently match.

## Evaluation prerequisites, not defects

- **Skill-package structural inspection (S001–S013) and evidence reduction are not implemented in the DevForge CLI.**
  Verified against the binary's own help. Every structural row in the report is `INSPECTION_MANUAL` with `authority: none`;
  42 matching runner rows do not close this. Owner: DevForge integration owner.
- **Protected-manifest custody for the evaluation runner is not implemented in the DevForge CLI.** The runner, grader,
  runtime and case identities in the observations header are self-reported by the run. Owner: DevForge integration owner.
- **No installed copy, fresh terminal or isolated workspace was allocated**, so tiers C, B and A are `NOT_RUN` and the
  `old_skill` baseline arm was never executed. Owner: the coordinator / evaluation owner.
- **The paired evaluator package is not merged or installed** — it exists only as canonical source at `e641797` on branch
  `author/claude-devforge-evaluate-expert-scaffold-20260910` and is absent from the main working tree's provider skills
  directory. F-001 and F-002 therefore describe a refresh trigger that has partially fired, not a landed change the
  candidate failed to absorb.
- **No `execution_ref`/SESSION record was supplied to this worker.** Recorded as `null` with the reason.

None of these authorises a target edit, and editing the candidate will not produce them.

## Closure rules

- **Applied** means the source was edited. It does not close a finding.
- A changed candidate is a new identity and needs new matching evidence before any finding is closed. Every deterministic
  row, criterion record and manifest digest in `EVREPORT-E3-001` is bound to `4999f31` and does not transfer to changed bytes.
- Preserve the original failure history; never overwrite an earlier `FAIL`. E1's `F-001…F-006` keep their IDs, severities and
  original text; this report's `F-001…F-007` are a separate namespace and supersede nothing.
- Never weaken an accepted expectation, delete a case or change a sibling gate to convert a recorded failure into a pass. A
  defect in a shared contract goes to its integration owner.

**Validation status:** Not performed by this document.
**Finding status:** findings recorded; reevaluation required after any change.
