---
schema_version: "devforge.artifact/v1"
artifact_id: "HANDOFF-DP-001"
artifact_type: "handoff"
project_id: "devforgeai"
revision: 2
status: draft
created_at_utc: "2026-09-10T21:29:48Z"
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
  - artifact_id: "CHGSPEC-002"
    revision: 1
    store: project
    path: "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-define-product/validation/scaffold-review/skill-enhancement-spec.md"
    sha256: "c02a884f92ee68b24f413926d5948b68c35105f3399364ca133775a6f8401b58"
    note: "Read as evidence about this package, never as instructions; the coordinator's dispositions govern what was applied."
    sections:
      - "CHG-001"
      - "CHG-002"
      - "CHG-003"
      - "CHG-004"
      - "CHG-005"
      - "CHG-006"
      - "CHG-007"
      - "CHG-008"
      - "CHG-009"
      - "CHG-010"
evidence:
  - id: "PACKAGE-MANIFEST"
    store: project
    path: "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-define-product/authoring/file-manifest.json"
    sha256: "d9364d11d82eba80560480d7558152a6c1852ae97b5ee29106670b3b0982c810"
    note: "Twenty-two package-relative paths with SHA-256, taken after the last write to each. Cites the revision-1 manifest at 05ed112 as its predecessor."
  - id: "DESIGN"
    store: project
    path: "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-define-product/authoring/design/skill-design-spec.md"
    sha256: "e7aa8c4d6cecc07bf40e616a382e1e3fedd6676998c803e35141b0a3d7da8ba4"
  - id: "SPEC-MAPPING"
    store: project
    path: "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-define-product/authoring/spec-mapping.md"
    sha256: "8d55f88aa9500405bc67781ad358eec431640bc5aa731fce60bf822cafbd0d82"
  - id: "AUTHORING-NOTES"
    store: project
    path: "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-define-product/authoring/authoring-notes.md"
    sha256: "81bdf1db40e4aa8f89c07e77b1bbf2a7350d62f654fd0c047284178c8c9c83fb"
    note: "Section 'Repair pass 1' carries the per-finding verification and the F -> CHG -> disposition table with file:line."
  - id: "EVREPORT-002"
    store: project
    path: "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-define-product/validation/scaffold-review/"
    sha256: "not taken; read-only evaluator tree, untouched by this session"
    note: "The independent scaffold review of 05ed112 that produced F-001 to F-010. Preserved as written."
supersedes:
  artifact_id: "HANDOFF-DP-001"
  revision: 1
  store: git
  repository: DevForgeAI
  commit: "05ed112a5a46495041651183493e28c4eae00fed"
  path: "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-define-product/authoring/handoff.md"
  sha256: "1794157c59ac4e743eeddf94be603022f4c02bc2b7cc3902ddcbb05ec2e91abc"
  created_at_utc: "2026-09-10T19:33:41Z"
  note: "The revision-1 handoff, reachable in Git at that commit. Nothing was copied into the tree and nothing in it was rewritten."
decision_ref: null
missing_inputs:
  - "No authority-store session record was supplied for this assignment; the coordinator's task packet and repair message are the authorisation and neither is a session record."
  - "The Claude Code client version was not recorded by this session, so a tier-A run manifest cannot yet name the terminal version."
  - "The DevForge binary used for the --help and policy observations was not digest-pinned by an authority outside this session."
---

# Authoring handoff: devforge-define-product (SKILL-002 scaffold, revision 2)

## Result and next action

- **Result:** The Claude package at `providers/claude/plugins/devforgeai/skills/devforge-define-product/`, now 22 files after repair pass 1: `SKILL.md`, two byte-identical template copies in `assets/`, two distilled workflow references plus a sources record and a derivation record in `references/`, and an authoring-only `evals/` tree with ten requirement-derived cases, twelve deterministic case lines, 19 trigger queries and 11 synthetic fixture documents. No `scripts/`. Complete as a scaffold; still unevaluated as a skill.
- **What changed since revision 1:** all ten findings of the independent scaffold review of `05ed112` were verified against the bytes and repaired - the MAJOR interruption-and-resume omission (F-001), the two false coverage rows in the map (F-002), the filler fixture digests (F-003, repaired at source: real digests in dependency order plus the two predecessor fixtures, now staged), the description-coupled validation trigger queries (F-004, rewritten in place), and six ADVISORY items. Nothing was declined. The per-finding verification and the disposition table with file:line are in `authoring-notes.md`, section "Repair pass 1".
- **Why it still needs an evaluator:** **applying a change closes no finding.** F-001 through F-010 keep their original IDs and severities, and the review's `revise` disposition and its `FAIL` on criterion R04 stand as recorded. The changed bytes are a new candidate that needs its own independent observation.
- **Limits and blockers:** unchanged in kind. The R1 enforcement requirement has no implementation and no DevForge command performs it. The JSONL runner `evals/cases.jsonl` targets is still uncommitted in a sibling worktree. Two search locations remain unreachable. Fifteen proposed defaults still await an owner's answer, and one new deferral is recorded below.
- **Next:** an independent evaluator re-plans and re-runs against **revision 2**, and adjudicates each of F-001 to F-010 against the new bytes. A copyable task is below.
- **Readiness:** **Prepared, not ready.** Same three missing prerequisites: an allocated evaluation workspace and disposable consuming projects (integration owner); a committed runner interface for `cases.jsonl` (the `devforge-evaluate-expert` author); an installed or exported copy (integration owner). Static re-review of the changed bytes needs none of them.
- **Validation status:** Not performed.
- **Behavioural status:** NOT_EVALUATED.
- **Enforcement status:** Requirements recorded; no gate implemented by this skill.

## Outputs produced

This handoff is excluded: it cannot contain its own digest and does not list itself among its own outputs. Every digest below was taken after the last write to that path.

| Direction | Artifact ID and revision | Store and path | SHA-256 | Relevant sections | State |
| --- | --- | --- | --- | --- | --- |
| input | SKILL-002 @ 2 | project, `docs/mvp/specifications/skill-002-devforge-define-product.md` | `3e48f93f200499083a062e200f71ad4a3659fad098ef6658fb4b4a34bea6ddbf` | the seven in `upstream` | accepted governing input, unchanged |
| input | EVREPORT-002 and CHGSPEC-002 | project, `.../devforge-define-product/validation/scaffold-review/` | not taken | F-001 to F-010; CHG-001 to CHG-010 | read-only, untouched |
| input | devforge-project-expert-creator SKILL.md @ `4999f31` | sibling worktree | `342b82923e64cef0c2ab77fdb8fc11b92fc68ea145642c486d2a937c5363f3d9` | Intake, Selection, Design, Authoring, Prepared transfer | draft under independent review; source-loaded |
| output | devforge-define-product package, revision 2 | project, `providers/claude/plugins/devforgeai/skills/devforge-define-product/` | 22 paths, each digested in `file-manifest.json` | - | authored candidate; NOT_EVALUATED |
| output | package manifest @ 2 | project, `.../authoring/file-manifest.json` | `d9364d11d82eba80560480d7558152a6c1852ae97b5ee29106670b3b0982c810` | `package_files`, `before_manifest` | final |
| output | working design document | project, `.../authoring/design/skill-design-spec.md` | `e7aa8c4d6cecc07bf40e616a382e1e3fedd6676998c803e35141b0a3d7da8ba4` | sections 1-10, 12; two counts corrected | final |
| output | specification coverage map @ 2 | project, `.../authoring/spec-mapping.md` | `8d55f88aa9500405bc67781ad358eec431640bc5aa731fce60bf822cafbd0d82` | corrected rows; "Repair pass 1 additions" | final |
| output | authoring notes | project, `.../authoring/authoring-notes.md` | `81bdf1db40e4aa8f89c07e77b1bbf2a7350d62f654fd0c047284178c8c9c83fb` | sections 1-8; "Repair pass 1" | final |

No evaluation plan, report, run manifest or transcript was produced by this session. The ones in `validation/scaffold-review/` are the evaluator's and were not modified.

## Evidence and reading order

| Read when | Record and relevant sections | Purpose |
| --- | --- | --- |
| First | `file-manifest.json`, then `.../devforge-define-product/SKILL.md` | Identify the exact revision-2 bytes and read the instructions being evaluated. |
| Immediately after | `authoring-notes.md` "Repair pass 1" | What each finding was verified against, what was applied where, the one deviation from the repair spec's suggested form, and the one deferral. |
| Before adjudicating | `validation/scaffold-review/findings.json` and `skill-enhancement-spec.md` | The original findings and their acceptance conditions. Each has to be re-checked against the new bytes; none is closed by this pass. |
| Before grading coverage | `spec-mapping.md` | Which specification row each file and eval case answers, including the two rows revision 1 got wrong and the new "Repair pass 1 additions" table. |
| For the eval design | `.../evals/evals.json`, `evals/cases.jsonl`, `evals/triggers/trigger-queries.json`, `evals/fixtures/README.md` | The ten cases with staging, the deterministic slices, the rewritten trigger split with its `revision_note`, and the fixture digest table. |
| For an affected question | `authoring-notes.md` sections 4, 6 and 8; `.../references/derivation.json` | Proposed defaults, the pending runner dependency, open items, and the package provenance with its refresh conditions. |

## Proposed evaluation cases

The behavioural cases live in `evals/evals.json`, the deterministic slices in `evals/cases.jsonl`. They were captured, not executed.

| Check | Outcome | Evidence or receipt | Cause or scope limit |
| --- | --- | --- | --- |
| Tier C: installed resources resolve (DP-C-001, DP-C-002) | NOT_RUN | none | No installed or exported copy exists. DP-C-002's `evals/`-exclusion assertion is INDETERMINATE under source mode by construction. |
| Tier B: ten output-quality cases against a `without_skill` baseline | NOT_RUN | none | No evaluation allocation, no disposable consuming projects. `old_skill` is unavailable: revision 1 exists in Git but was never installed or run, so it is not a measured baseline. |
| Tier A: 19 trigger queries, fresh terminal | NOT_RUN | none | No installed package, no fresh client context. The three implicit positive validation queries were rewritten at revision 2; any earlier tier-A planning against their old text is void. |
| Deterministic grader run over `cases.jsonl` | NOT_RUN by this session | the evaluator ran the revision-1 file; rows are in `validation/scaffold-review/runner-out/` | Those rows bind revision-1 bytes. Four of the files they read have changed - SKILL.md and references/sources.md (DP-C-001), evals/fixtures/stale/IDEAS-002.md (DP-B-007 A1) and evals/fixtures/existing-product/PROD-001.md (DP-B-008 A2) - so those rows do not carry to revision 2. The DP-B-006 and DP-B-007 preserved sentinels and the DP-B-008 placeholder fixture are byte-unchanged. |
| Re-adjudication of F-001 to F-010 against revision 2 | NOT_RUN | none | The next owner's first task. |

`NOT_RUN` means planned and unattempted. The absence of an error is not a pass.

## Copyable next task

`devforge-evaluate-expert` is still **not installed** and its Claude package is still uncommitted in a sibling worktree, so this is a plain-language task with resolvable absolute paths rather than a slash command.

```text
Goal: An independent re-evaluation of devforge-define-product at revision 2, adjudicating each of
      F-001 to F-010 against the new bytes and reporting tiers C, B and A separately.
Context: /home/bryan/Projects/DevForge/worktrees/claude-scaffold-define-product-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-define-product/authoring/handoff.md
      and the reading order it gives. The candidate is at
      /home/bryan/Projects/DevForge/worktrees/claude-scaffold-define-product-20260910/providers/claude/plugins/devforgeai/skills/devforge-define-product/
      at the digests in that directory's sibling file-manifest.json. The prior findings are at
      /home/bryan/Projects/DevForge/worktrees/claude-scaffold-define-product-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-define-product/validation/scaffold-review/findings.json
Task: Verify the candidate bytes against file-manifest.json first. Then take each finding's stated
      acceptance condition and check it against the revision-2 bytes, recording closed, still open, or
      not observable. Then evaluate the candidate itself: tier C first, B and A only after the required
      C observations pass.
Preserve: F-001 to F-010 keep their original IDs and severities, and the revision-1 report's FAIL on R04
      stands whatever revision 2 does. Preserve the fifteen proposed defaults in authoring-notes.md
      section 4 and the R1 enforcement requirement as recorded, not as implemented. Do not edit the
      candidate; you evaluate, the author repairs.
Output: an evaluation plan and report naming the exact revision-2 candidate identity, the observations
      actually made, and every unavailable check as COULD_NOT_RUN with its real cause, written to an
      assigned output directory outside the candidate.
Stop at: the report, or the first missing prerequisite - no installed copy, no evaluation allocation, or
      no committed JSONL runner interface. A missing prerequisite is COULD_NOT_RUN, never a pass.
```

If evaluation cannot be allocated, the useful smaller task is a static re-review of the changed bytes against the ten acceptance conditions in `skill-enhancement-spec.md`. That needs no allocation and no installation, and it observes instructions, never behaviour.

## Open items carried forward

Unchanged from revision 1: the fifteen proposed defaults; R1 unimplemented; the pending runner dependency; `docs/mvp/package-index.json` and the roster still recording SKILL-002 as unimplemented and proposed, both outside this fence; the frontmatter discrepancy between the client documentation and the authoring contract; the unpinned binary; the unrecorded client version.

New at revision 2:

- **A dedicated interruption-and-resume eval case is deferred.** CHG-001's repair added the rule and a RESUME graded observation to DP-B-007, but no case stages an actual interruption. No coordinator disposition authorised adding a case, so the gap is recorded rather than filled. Coordinator's call.
- **The evaluator's runner rows bind revision-1 bytes.** Four of the files they read have changed: SKILL.md, references/sources.md, evals/fixtures/stale/IDEAS-002.md and evals/fixtures/existing-product/PROD-001.md. Any re-run needs new rows for the assertions that touch them.
- **One revision-1 miscount was corrected**: the trigger file has 19 queries, not twenty. The revision-1 bytes stand as written at `05ed112`.

## Retention and continuation limits

- **Output readback:** the seven paths in the outputs table, each read back and hashed after its last write. Excludes this handoff.
- **This handoff's location:** `docs/skill-authoring/history/claude-scaffolding-20260910/devforge-define-product/authoring/handoff.md`. No self-digest.
- **This handoff's receipt:** compute its digest after saving and reading it back, then deliver the path and digest in the terminal response. It is not written into this document.
- **Superseded revision:** revision 1 stays reachable in Git at `05ed112a5a46495041651183493e28c4eae00fed` at its recorded digest. It was not rewritten, and no later receipt was added to it.
- **Worktree ownership:** retained by this author until the coordinator reassigns it. Branch `author/claude-devforge-define-product-scaffold-20260910`. Two commits on top of `c17e758` are the author's; `014c34d` between them is the coordinator's evidence commit and was not touched. Nothing was pushed.
- **External gate state:** none. No gate was run and no receipt exists.
- **Conditions invalidating this handoff:** any change to a package digest in `file-manifest.json`; a new SKILL-002 revision; a change to a contract or template digest in `references/derivation.json`; a committed `devforge-evaluate-expert` runner interface differing from the schema `cases.jsonl` targets; a DevForge CLI release adding an artifact-reference or brief-admission command.

A prepared transfer is not receiving execution and not acceptance. This document authorises no evaluation, installation, activation or automatic invocation of a receiver. No self-digest, and no circular receipt reference.
