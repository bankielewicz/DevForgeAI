---
schema_version: "devforge.artifact/v1"
artifact_id: "CHGSPEC-ARCH-001"
artifact_type: "skill-enhancement-spec"
project_id: "DevForgeAI"
revision: 1
status: draft
created_at_utc: "2026-09-10T21:48:00Z"
producer:
  skill: "devforge-evaluate-expert"
  skill_revision: "bdf665c7e18061395c0762de7a377fdc5f6ed48d66245df5623c5c32b90cf2ac"
execution_ref: null
upstream:
  - artifact_id: "EVREPORT-ARCH-001"
    revision: 1
    store: "project"
    path: "verification-results.md"
    sha256: "3269185e861c6d117e7c402bda817d5fca8f35cc68f3782f8adb1c7df34f4305"
    sections:
      - "Findings"
      - "Independent review R01-R10"
      - "Missing capabilities and evaluation prerequisites"
  - artifact_id: "SKILL-005"
    revision: "2"
    store: "project"
    path: "/home/bryan/Projects/DevForge/framework/DevForgeAI/docs/mvp/specifications/skill-005-devforge-architect.md"
    sha256: "b9dc3a5a2d19a024c42b60539909009d9d9292e54f3509739a8ae575311ea88b"
    sections:
      - "Workflow and phase exits"
      - "Rework, stopping, and recovery"
evidence:
  - path: "findings.json"
    sha256: "18a031130e109e96070fdbb8c65221a12c7603459129d49db901bb1f1dca49e7"
  - path: "ai-review.json"
    sha256: "964c0ce8c6dbf780c50469d1045329735038b812daefb56ac089aeaed85cc2bb"
  - path: "validation-results.json"
    sha256: "5c8ad6ee2a64d00643f06d9fc4ece74113a9c7cd530c3eed22dcf75dcc8bdf69"
supersedes: null
decision_ref: null
missing_inputs:
  - "Native tier C, B and A evidence. Not required to implement CHG-001, and required before any behavioural claim about this skill."
---

# Skill repair and enhancement specification: devforge-architect (SKILL-005)

The bounded, evidence-backed change request returned for this candidate. It authorises no automatic edit, invocation, installation, acceptance or release, and it expands no existing authorisation.

**One required repair, with a two-sentence fix. Four optional items, two of which explicitly recommend no target edit.** The evaluation found no BLOCKER and no MAJOR defect in the candidate.

## Immutable intake

- **Evaluated candidate:** `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-architect-20260910/providers/claude/plugins/devforgeai/skills/devforge-architect` at commit `61f6ef06fc61fa92d7a3714c54a5251cd9177a4f`. `SKILL.md` sha256 `cb51fead7d5bdd8ed6fcee17c3e6ae6a716efc0936108240e535fa0cca04b9e4`. Full 32-file manifest in `verification-results.md`, "Candidate source manifest".
- **Installed copy evaluated:** none. Nothing was installed, exported or bound.
- **Specification:** `docs/mvp/specifications/skill-005-devforge-architect.md`, revision 2, sha256 `b9dc3a5a2d19a024c42b60539909009d9d9292e54f3509739a8ae575311ea88b`.
- **Evaluation report:** `verification-results.md`, sha256 `3269185e861c6d117e7c402bda817d5fca8f35cc68f3782f8adb1c7df34f4305`.
- **Results record:** `validation-results.json` revision 2, sha256 `5c8ad6ee2a64d00643f06d9fc4ece74113a9c7cd530c3eed22dcf75dcc8bdf69`.
- **Findings record:** `findings.json`, sha256 `18a031130e109e96070fdbb8c65221a12c7603459129d49db901bb1f1dca49e7`.
- **Independent review:** `ai-review.json` revision 2, sha256 `964c0ce8c6dbf780c50469d1045329735038b812daefb56ac089aeaed85cc2bb`. Completed, single-context; limits recorded in the report. Revision 2 corrected numeric line spans only; see the report's Limits item 8.
- **Cases and fixtures:** the candidate's own `evals/cases.jsonl` sha256 `809a67baab4ed8fd7e967d750e76667761c7475d1e2fd685d98bff1cdd5a0eb1`, `evals/evals.json` sha256 `dba8dd4530ced694f2ed37d2a1ec6f0ba9d88471522e1f1cc85fd1bf9ae0c947`, `evals/triggers/trigger-queries.json` sha256 `0caa042650d002dcb5e8fe03067728cbab6842a6fadf81be0a2a42a92085aaf2`, with the twenty fixtures listed in the report's manifest. The evaluator-added cases are at `runner-out/evaluator-added-cases.jsonl` sha256 `5b2db5f9f84bd12351e93b16b9c4f4a5b87831d0b4b7e63a016dfbc61b8371ce`.
- **Prior iteration:** none. This is the first evaluation of the first revision of this package.

Verify these identities before editing, and retain the current candidate bytes.

## Change decision

- **Are target changes justified by the evidence?** **Yes — for CHG-001 only.** CHG-002 and CHG-005 are optional enhancements the coordinator may decline. CHG-003 and CHG-004 record demonstrated non-defects and request **no target edit**; they exist so a later reader can see the question was asked and answered.
- **Next owner:** `devforge-project-expert-creator` — that is the role the results contract names as the owner of every fix. Under this coordinator's dispatch the concrete recipient is **the scaffold's author for `devforge-architect`**, working in the same worktree `claude-scaffold-architect-20260910` on branch `author/claude-devforge-architect-scaffold-20260910`. Both are stated because the role and the dispatch are different facts.
- **Behaviour that must be preserved unchanged:** the frontmatter `name`; the folder name; the four phases and their `Exit when` lines; all five existing failure branches; the `Two roots` section; the trust-boundary paragraph; the enforcement-requirement record in `references/framework-context.md`; every digest, derivation and template copy; all twenty fixtures and their sentinels; the fixed trigger split; and the package's freedom from shell-injection syntax, host paths and `docs/mvp` runtime dependency. Every one of these was independently verified in this evaluation and any change to them invalidates the corresponding observation.
- **Forbidden scope changes:** no new phase; no new reference file; no change to either copied template or to `derivation.json`'s recorded digests; no change to any fixture, sentinel, eval case, expected observation or trigger split; no re-randomisation of the split; no change to the specification, to a shared contract, to a sibling skill, to the roster or to the DevForge CLI; no install, export, bind or commit as part of applying this specification; and no rewrite of the package in the course of a two-sentence repair.

## Requested changes

### CHG-001: an interrupted session preserves its phase evidence and re-establishes its assignment before resuming

- **Finding IDs:** F-001
- **Severity:** MINOR — chosen from the demonstrated consequence, which is contained, not from the criterion label.
- **Change type:** required repair
- **Accepted requirement, or a new proposal:** accepted requirement. SKILL-005 "Workflow and phase exits": *"On interruption, preserve the current phase and evidence; resume by checking their identities and the session assignment again."* And SKILL-005 "Rework, stopping, and recovery": *"If the worktree or active run changes, re-establish the appropriate baseline and evidence before resuming."*
- **Affected revision, file and section:** `61f6ef06…`, `providers/claude/plugins/devforgeai/skills/devforge-architect/SKILL.md`. Either the `## Stopping` section (lines 113–120) or a sixth bullet in `## When something is missing or a check cannot run` (lines 103–111). Second locus, outside the package: `docs/skill-authoring/history/claude-scaffolding-20260910/devforge-architect/authoring/spec-mapping.md`, the final row of its "Workflow and phase exits" table.
- **Evidence and reproduction:** run `grep -rniE 'interrupt|resume' <package-root>` over the frozen bytes. It returns exactly one hit — the `## Resume and custody` heading inside the copied `assets/handoff.md` template — and no instruction anywhere addresses an interrupted session. The two sections `spec-mapping.md` cites, `references/recording-rules.md` "Resolving an upstream reference" (lines 58–70) and "When no session record exists" (lines 80–85), were read: they carry the identity-recheck half as unconditional pre-write rules and carry the phase-and-evidence-preservation half not at all, and neither is framed as an interruption or resume path, so a resumed session has no trigger to consult them.
- **Demonstrated impact:** a session interrupted mid-contract has no instruction to preserve the current phase's partial evidence or to re-read the session assignment before continuing. It carries partial phase work forward under an assignment it has not re-established — the situation the execution contract's worktree rules exist to prevent. The consequence is contained rather than severe precisely because the unconditional pre-write identity rules still catch the highest-risk resumed-session failure, a silently stale upstream. A session that runs to completion in one pass is unaffected.
- **Bounded desired behaviour:** after the change, `SKILL.md` states that on an interruption the current phase's evidence and the identities already frozen are preserved rather than discarded; that work resumes only after re-checking the upstream identities and the session assignment; and that a changed input starts a new revision rather than continuing this one. Two sentences is the right size. Do not add a phase, a reference file or a procedure.
- **Behaviour to preserve:** everything else in `Stopping` — the completion conditions, the four stop-and-hand-back triggers, and the closing paragraph on bounded delivery and change requests. If the bullet form is chosen instead, all five existing bullets stay unchanged and in order.
- **Second locus:** correct the `spec-mapping.md` row to record the coverage as partial, distinguishing the identity-recheck half (carried, in `recording-rules.md`) from the phase-and-evidence-preservation half (now carried, in `SKILL.md`). Do not delete the original row's history.
- **Acceptance condition:** a later evaluation runs the same `interrupt|resume` grep and finds an instruction in `SKILL.md` that names both halves; and reads the `spec-mapping.md` row and finds it consistent with the bytes.
- **Affected reruns:** `ARCH-B-007` (the case whose situation is closest to a resumed session), `ARCH-PKG-001` and `EV-ADD-PKG-001` (link resolution and package structure, because `SKILL.md` bytes change), and the `SKILL.md` digest wherever it is recorded — `authoring/file-manifest.json` and any `producer.skill_revision` derived from it.

### CHG-002: name devforge-review among the description's exclusions

- **Finding IDs:** F-002
- **Severity:** ADVISORY
- **Change type:** authorised enhancement, optional
- **Accepted requirement, or a new proposal:** proposal. No specification requirement names `devforge-review` as an exclusion; the case for it comes from the candidate's own authored negative `A12a`, which routes a code-review request to that sibling.
- **Affected revision, file and section:** `61f6ef06…`, `SKILL.md` line 3, the frontmatter `description` exclusion clause.
- **Evidence and reproduction:** the description measures 1,297 characters. The live Claude Code documentation, retrieved 2026-09-10 UTC, states the `description` (with `when_to_use`) is truncated at 1,536 characters in the skill listing. That leaves 239 characters of headroom, enough for a clause such as *"to review a candidate against acceptance criteria (devforge-review)"*.
- **Demonstrated impact:** none measured — tier A did not run. This is a discrimination-margin observation: `A12a` is currently discriminated by the absence of an attractor rather than by a stated boundary.
- **Bounded desired behaviour:** one added exclusion clause naming `devforge-review`, with the total description still measurably under 1,536 characters.
- **Behaviour to preserve:** every existing exclusion and its owning skill; the `devforge-change` routing sentence, which carries the specification's "Does not activate for" row; the two-field frontmatter form.
- **Forbidden:** do not exceed the truncation limit to fit it. If it does not fit within the measured headroom, decline the change and say so.
- **Acceptance condition:** the description names `devforge-review` and measures under 1,536 characters.
- **Affected reruns:** `A12a` and every other tier-A query, since the description is the discovery surface; `ARCH-PKG-001`.

### CHG-003: no target edit — the DevForge command list

- **Finding IDs:** F-003
- **Severity:** ADVISORY
- **Change type:** recorded non-defect
- **Evidence:** `SKILL.md` line 93 says the surface *"includes"* `check`, `expert prepare|bind|status`, `init`, `red`, `green`, `accept`, `verify`, `status` and `isolate`. The operator binary (`devforge 0.1.0`, sha256 `835c3263…`) lists one further top-level command group, `delivery`. Every command the package names exists; `includes` is non-exhaustive rather than false; and the same sentence instructs the reader to run `devforge --help` on the operator's binary.
- **Decision: no target edit.** Nothing is demonstrated wrong and nothing in this skill's workflow needs `delivery`. If the author edits that sentence for another reason, adding `delivery` is acceptable; editing it solely for completeness is not justified by the evidence.

### CHG-004: no target edit — devforge-evaluate-expert as a consumer

- **Finding IDs:** F-004
- **Severity:** ADVISORY
- **Change type:** recorded non-defect
- **Evidence:** the specification's consumer-coverage line lists `evaluate-expert`; the package names it nowhere. `spec-mapping.md` discloses this as a deliberate partial with a stated reason — `evaluate-expert` consumes an expert package rather than the contract, and naming an uninstalled skill in a continuation would risk presenting it as an available next step. The bytes match the disclosure, and `SKILL.md` independently instructs checking what is actually installed before naming a skill in a continuation.
- **Decision: no target edit.** The specification line describes artifact flow across the roster, not an instruction the skill must recite. Recorded so the coordinator sees a considered decision rather than an omission.

### CHG-005: give the single-entry negative trigger categories held-out coverage

- **Finding IDs:** F-005
- **Severity:** ADVISORY
- **Change type:** authorised enhancement, optional and conditional
- **Accepted requirement, or a new proposal:** proposal, serving the authoring contract's separately reported tiers.
- **Affected revision, file and section:** `61f6ef06…`, `evals/triggers/trigger-queries.json`, `queries[]`.
- **Evidence and reproduction:** 22 queries, no duplicate IDs, split fixed and recorded once, balanced by `should_trigger` at 7/7 train and 4/4 validation, every negative category owner-mapped. Eight of thirteen categories carry exactly one query, so six negative routings appear in one split only.
- **Demonstrated impact:** none yet, because tier A did not run. If it later does, those six routings will be evidenced only from whichever split holds them, and a description change tuned on train would have no held-out check for them.
- **Bounded desired behaviour:** one added query on the thinner side of the single-entry negative categories, each naming its owning sibling in `owner_map`.
- **Behaviour to preserve:** the existing 22 entries, their IDs, their `should_trigger` values and their split assignments, exactly as they are.
- **Forbidden:** do not re-randomise or reassign the existing split; do not move an entry between splits; do not install a stub sibling to obtain a routing result.
- **Condition:** apply only if a native tier-A evaluation is actually scheduled. Otherwise leave it and record the gap.
- **Acceptance condition:** every negative category has at least one entry in each split, and the original 22 entries are unchanged.
- **Affected reruns:** the tier-A set, once it can run at all.

## Implementation order

CHG-001 is independent and is the only required item. CHG-002 and CHG-005 are independent of it and of each other; either may be applied, deferred or declined without affecting CHG-001. CHG-003 and CHG-004 request no edit and have no implementation. If CHG-001 and CHG-002 are both applied, hash `SKILL.md` once after both edits rather than between them, and update every recorded `SKILL.md` digest in the same change.

## Evaluation prerequisites, not defects

None of these authorises a target edit, and editing the candidate will not produce any of them.

| Prerequisite | Blocks | Owner | Finding |
| --- | --- | --- | --- |
| An installed or exported copy, a fresh Claude Code terminal with an observable version, and a permitted isolated workspace with per-attempt client state separation | Every tier C, B and A claim; the whole `without_skill` comparison; the specification's behavioural acceptance requirement | Coordinator / DevForge integration owner | F-006 |
| Skill-package structural inspection (S001–S013) and evidence reduction in the DevForge CLI | A gate-authoritative structural outcome and a decision receipt. Structural rows here are `INSPECTION_MANUAL` with `authority: none`, and the disposition was adjudicated by hand | DevForge integration owner | F-007 |
| Protected-manifest custody for the evaluation runner in the DevForge CLI | Verified runner, grader, runtime and case identities, which are currently self-reported by each run's own header | DevForge integration owner | F-007 |
| A second separately dispatched reviewer context | Nothing outright; it bounds the strength of R01–R10. Needed only if a criterion outcome becomes contested | Coordinator | F-008 |

## Closure rules

- **Applied** means the source was edited. It does not close a finding.
- A changed candidate is a new identity and needs new matching evidence before F-001 is closed.
- Preserve the original failure history. Never overwrite this evaluation's `FAIL` on `CHK-AI-R04`; a later evaluation records its own result alongside it.
- Never weaken an accepted expectation, delete a case, or change a sibling gate, a shared contract or the specification to convert a recorded failure into a pass. A defect in a shared contract goes to its integration owner.
- The three `NOT_RUN` tier rows are closed only by real native evidence, never by a repair to the candidate.

**Validation status:** not performed by this document.
**Finding status:** findings recorded; reevaluation required after any change.
