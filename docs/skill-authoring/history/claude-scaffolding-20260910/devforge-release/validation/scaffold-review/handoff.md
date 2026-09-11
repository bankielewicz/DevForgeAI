---
schema_version: "devforge.artifact/v1"
artifact_id: "HANDOFF-REL-SCAFFOLD-EVAL-001"
artifact_type: "handoff"
project_id: "devforgeai"
revision: 1
status: draft
created_at_utc: "2026-09-10T22:02:58Z"
producer:
  skill: "devforge-evaluate-expert (source-loaded at e641797eebf04cd1e8eb9f711549e038e7745407; not installed and not invoked as a skill)"
  skill_revision: "unknown - no installed SKILL.md exists to hash. The workflow was read with `git show e641797:.../devforge-evaluate-expert/SKILL.md`; the commit is the identity, and no digest of an installed copy is claimed."
execution_ref: null
upstream:
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
      - "Open decisions for the coordinator"
  - artifact_id: SKILL-011
    revision: 2
    store: project
    path: framework/DevForgeAI/docs/mvp/specifications/skill-011-devforge-release.md
    sha256: "f94261d7af37d8c68510e88d4b8705447b06ce396ead5776c28c7502cf60585d"
    sections:
      - "User goal and use-case inventory"
      - "Validation and behavioral acceptance"
evidence:
  - "findings.json, sha256 c3221dcf9e2c27a1b288453cf5f150a72a8659a13cfb596a91ee7408c6b768a2"
  - "runner-out/observations-source.jsonl, sha256 f5914fd038f9fbb2f58562021f5048e9b49cd8dd83c03d7e8f73ef77a4b55506"
  - "runner-out/observations-evaluator.jsonl, sha256 eddedf971d497feaadbadf388233407678718a7b637c4f09af2f9f7317f6152f"
  - "runner-out/evaluator-cases.jsonl, sha256 3f1e787cb295c54164693221395d212ff67d7dd1407633df00c7f4b481e0d618"
  - "commands.log - every command run for this review, with observed UTC timestamps and observed output"
supersedes: null
decision_ref: null
missing_inputs:
  - "No session-record artifact was supplied for this evaluation assignment. The scope came from the coordinator packet. A worker-authored session ID would not be proof of ownership, so execution_ref stays null."
  - "No installed copy, fresh terminal or isolated workspace was allocated. Tiers C, B and A are NOT_RUN; behaviour is NOT_EVALUATED."
  - "No Claude Code client version was observed; every client-behaviour statement comes from documentation fetched 2026-09-10."
---

# Evaluation handoff: devforge-release (Claude, SKILL-011) scaffold review

## You are here

- **Skill and use case:** independent scaffold evaluation of the Claude `devforge-release` package against SKILL-011 revision 2. Structure, requirement coverage, instruction quality, authority boundaries, provider correctness and eval quality.
- **Current phase:** P6 complete. Results, repair specification and this handoff are written to the assigned fence.
- **Task state:** complete as an evaluation of what could be observed; the behavioural half was never in scope for this allocation.
- **Session/worktree assignment:** no session record exists; `execution_ref` is `null` with the reason above. The write fence was `.../devforge-release/validation/scaffold-review/` and nothing outside it was written. Nothing was committed.
- **Exact candidate scope:** `providers/claude/plugins/devforgeai/skills/devforge-release` at commit `dd1ae32b12ea209e71dbe338ab76bcbabd721e2e`, 24 files; the observed manifest is in the report.
- **Existing authorization carried forward:** the coordinator's evaluation dispatch. This document authorises no edit, install, export, run or acceptance.

## Result and next action

- **Result: insufficient evidence.** 0 BLOCKER, 0 MAJOR, 3 MINOR, 5 ADVISORY. All ten rubric criteria R01-R10 returned `PASS`.
- **Why:** no applicable criterion returned `FAIL`, so *revise* is not indicated on the rubric evidence; but tiers C, B and A were not run, so *suitable for the stated scope* is not supported either. The middle branch of the results contract applies. This is a coverage statement, not a criticism: on everything observable the package is unusually strong - complete specification coverage, provenance that verifies against bytes at every point checked, correct authority boundaries, and negative eval discriminators that actually discriminate.
- **Limits and blockers:** behaviour is `NOT_EVALUATED`; the validator followed is itself an unqualified draft; my independent review was not blind to the deterministic runs or to the author's evidence; one interpretation (F-001) is unresolved and is the only judgement that would change the headline.
- **Next:** the coordinator settles the F-001 interpretation, then dispatches the scaffold's author to apply CHG-001 through CHG-005. The copyable task is below.
- **Behavioural status:** NOT_EVALUATED.
- **Enforcement status:** no gate was implemented or claimed by this evaluation; findings recorded, adjudication performed by hand.
- **Published:** nothing published, nothing installed, nothing exported, nothing committed, no candidate byte changed.

## Inputs consumed and outputs produced

This handoff is excluded: it cannot contain its own digest and does not list itself among its outputs.

| Direction | Artifact ID and revision | Store and path | SHA-256 | Relevant sections | State |
| --- | --- | --- | --- | --- | --- |
| input | SKILL-011 @2 | project, `framework/DevForgeAI/docs/mvp/specifications/skill-011-devforge-release.md` | `f94261d7af37d8c68510e88d4b8705447b06ce396ead5776c28c7502cf60585d` | use-case inventory; inputs; phases; outputs; validation; rework | frozen, observed matching |
| input | candidate `devforge-release` @`dd1ae32` | worktree, `providers/claude/plugins/devforgeai/skills/devforge-release` | 24-file manifest in the report | whole package | frozen, unmodified |
| input | validator `devforge-evaluate-expert` @`e641797` | worktree, `worktrees/claude-scaffold-evaluate-expert-20260910` | `SKILL.md` read at that commit; runner `95ca2abf...`; graders `1b7a27a3...` | P1-P6, R01-R10, runner interface, results contract | source-loaded, draft, unqualified |
| input | author evidence (untrusted, informational) | worktree, `.../devforge-release/authoring/` | `file-manifest.json` verified 24/24 against bytes | design spec, notes, spec-mapping, manifest, handoff | read; no preferred verdict asserted by the author |
| output | EVREPORT-REL-SCAFFOLD-001 @1 | worktree, `.../validation/scaffold-review/verification-results.md` | `6bf0d875ac08ffdec392f1fb4a325a94c7ba107d612823c5c5f805cdbe77343e` | Findings; R01-R10; Decision and coverage | draft, complete |
| output | CHGSPEC-REL-SCAFFOLD-001 @1 | worktree, `.../validation/scaffold-review/skill-enhancement-spec.md` | `c5048e3143470ee8596a9498b677bdb12730794f0a1d0ea4708c9ee4011f4f17` | Requested changes; Open decisions | draft, complete |
| output | findings record | worktree, `.../validation/scaffold-review/findings.json` | `c3221dcf9e2c27a1b288453cf5f150a72a8659a13cfb596a91ee7408c6b768a2` | findings F-001..F-008 | draft, complete |
| output | runner observations, candidate cases | worktree, `.../scaffold-review/runner-out/observations-source.jsonl` | `f5914fd038f9fbb2f58562021f5048e9b49cd8dd83c03d7e8f73ef77a4b55506` | header; 10 case records | raw evidence, preserved |
| output | runner observations, evaluator cases | worktree, `.../scaffold-review/runner-out/observations-evaluator.jsonl` | `eddedf971d497feaadbadf388233407678718a7b637c4f09af2f9f7317f6152f` | header; 7 case records | raw evidence, preserved |
| output | evaluator case file | worktree, `.../scaffold-review/runner-out/evaluator-cases.jsonl` | `3f1e787cb295c54164693221395d212ff67d7dd1407633df00c7f4b481e0d618` | EVAL-C-101..107 | raw input, preserved |
| output | command log | worktree, `.../scaffold-review/commands.log` | hashed with this handoff's receipt | whole file | raw evidence, preserved |

## Observed verification

| Check | Outcome | Raw evidence / external receipt | Cause or scope limit |
| --- | --- | --- | --- |
| Candidate identity and drift | observed: HEAD == `dd1ae32`, empty diff over `providers/` | `commands.log` 21:47:11Z | a byte comparison, nothing about behaviour |
| Structural observation (manual + runner) | observed; 17 cases COMPLETED across two runs; 3 MISMATCH rows, all deliberate negative discriminators | `runner-out/*.jsonl` | `INSPECTION_MANUAL`, authority `none`; the DevForge CLI implements no structural-inspection capability |
| Provenance verification | observed: 5/5 derivation destinations, 8/8 selected inputs, 24/24 author manifest entries, builder pin exact | `commands.log` 21:47-21:52Z | proves which inputs were referenced, never that the result is correct |
| DevForge CLI surface | observed: 10 subcommands, leaf flags accepted, no publish/deploy path | `commands.log` 21:49:38Z | describes the binary at that path on that date; its digest was recorded, not pinned by a protected manifest |
| Independent review R01-R10 | observed: 10 PASS, 0 FAIL | `verification-results.md` P3 | not blind to the runner rows or the author's evidence; single reviewer |
| Tier C installed resources | **NOT_RUN** | none | no installed copy; installation forbidden by the packet |
| Tier B output quality vs `without_skill` | **NOT_RUN** | none | no execution allocation; both arms unexecuted, so no comparison exists |
| Tier A discovery and activation | **NOT_RUN** | none | no installed package, no fresh terminal, no consultation trace |
| Protected custody of runner identities | **COULD_NOT_RUN** | header `custody_note` in both observations files | not implemented in the DevForge CLI; owner: integration owner |

## Continuation directory

| Order | Task | Owner / skill | Prerequisites | Completion evidence |
| --- | --- | --- | --- | --- |
| 1 | Settle the F-001 interpretation: does the Agent Skills 1,024-character `description` maximum bind a Claude-provider package? | the DevForge integration owner, via the coordinator | `skill-enhancement-spec.md` "Open decisions for the coordinator", item 1 | a recorded owner decision |
| 2 | Apply CHG-001..CHG-005 to the candidate | the scaffold's author, under coordinator dispatch, following `devforge-project-expert-creator` at `4999f31` | this handoff, the report and the enhancement spec at the digests above; the decision from step 1 | a new candidate identity and an updated `file-manifest.json` |
| 3 | Re-run both case files against the repaired candidate | the author, or a re-dispatched evaluator | the new candidate identity | new observations files; no finding closes without them |
| 4 | Allocate an execution environment and run tiers C, then B, then A | the DevForge integration owner | a disposable consuming project, an installed or exported copy, a fresh terminal | run manifests, transcripts and separate per-tier results |
| 5 | Route the shared-template Codex wording question | the shared template owner | F-005 | a template owner decision; no edit inside this package's fence |

## Copyable next task

Addressed to the scaffold's author under coordinator dispatch. It names no slash command, because this package is installed nowhere and `devforge-change` has no implementation in either provider.

```text
Goal: Apply the bounded repairs CHG-001 through CHG-005 to the Claude devforge-release
      scaffold, producing a new candidate identity with matching evidence.
Context: /home/bryan/Projects/DevForge/worktrees/claude-scaffold-release-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-release/validation/scaffold-review/
         Read in this order: handoff.md, then skill-enhancement-spec.md
         (sha256 c5048e3143470ee8596a9498b677bdb12730794f0a1d0ea4708c9ee4011f4f17),
         then verification-results.md
         (sha256 6bf0d875ac08ffdec392f1fb4a325a94c7ba107d612823c5c5f805cdbe77343e)
         for the evidence behind each change, then findings.json.
Task: Edit only /home/bryan/Projects/DevForge/worktrees/claude-scaffold-release-20260910/providers/claude/plugins/devforgeai/skills/devforge-release/
      Verify the candidate is still dd1ae32b12ea209e71dbe338ab76bcbabd721e2e before editing.
      Apply CHG-002, CHG-003, CHG-004 and CHG-005 as specified. Apply CHG-001 only after
      the coordinator records the F-001 decision; the edit is safe either way, but whether
      it is required is that decision's to make.
Preserve: every item under "Behaviour that must be preserved unchanged" in the enhancement
      spec; the byte-exact equality of assets/release-record.md with the governing template
      (90b8e58f...); the equality of evals/fixtures/stale/preserved/QA-014.r1.md with
      evals/fixtures/QA-014.md (1284c83c...); this evidence directory, unmodified.
Output: the edited package, a recomputed 24-file SHA-256 manifest, updated
      authoring/file-manifest.json and the affected derivation.json digests, and a new
      authoring handoff recording the changed files and the new candidate identity.
Stop at: the edits and the new identity. Do not install, export, bind or run any tier;
      do not claim a finding closed - closure needs new matching evidence from a
      re-dispatched evaluation, and behaviour stays NOT_EVALUATED until an execution
      allocation exists.
```

## Retention and continuation limits

- **Output readback:** the six paths and digests in the outputs table above were written and hashed after their bytes were final. This handoff is excluded from that table.
- **This handoff's location:** `.../devforge-release/validation/scaffold-review/handoff.md`. No self-digest.
- **This handoff's receipt:** its digest is computed after saving and delivered with the terminal response. It is not written into this document, and this document is not edited later to record it.
- **Worktree ownership:** none taken. No worktree or branch was created, switched, committed, rebased, reset, stashed or cleaned. The candidate worktree carries only this untracked evidence directory.
- **External gate state:** none. No DevForge gate was run against this candidate, and no receipt exists. `devforge verify`, `check` and `status` were inspected via `--help` only.
- **Conditions invalidating this handoff:** any change to the candidate bytes; a new revision of SKILL-011 or of any contract digest recorded in the report; a change to the validator's runner or graders; an installation or export of this package; or an owner ruling on F-001.

Preserve the referenced bytes and both observations files, including the deliberate `MISMATCH` rows - a digest cannot recover a missing source, and a negative discriminator's raw result is the evidence that it discriminated. Record an identity change as a new revision rather than rewriting this one.

A recommendation of *insufficient evidence* is a statement about what was observed. It is not acceptance, not adoption, not release, and not a refusal. This document authorises no edit, install, export, run or invocation of any receiver.
