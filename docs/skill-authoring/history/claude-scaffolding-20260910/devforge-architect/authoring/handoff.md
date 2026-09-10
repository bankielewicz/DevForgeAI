---
schema_version: "devforge.artifact/v1"
artifact_id: "HANDOFF-ARCH-SCAFFOLD-001"
artifact_type: "handoff"
project_id: "DevForgeAI"
revision: 3
status: draft
created_at_utc: "2026-09-10T21:59:35Z"
producer:
  skill: "devforge-architect authoring assignment (no installed skill produced these bytes)"
  skill_revision: "not applicable; authored directly under the coordinator packet, not by an installed skill"
execution_ref: null
upstream:
  - artifact_id: "SKILL-005"
    revision: 2
    store: "project"
    path: "docs/mvp/specifications/skill-005-devforge-architect.md"
    sha256: "b9dc3a5a2d19a024c42b60539909009d9d9292e54f3509739a8ae575311ea88b"
    selected_commit: "c17e758417da64928a0f47fc2600304465ac3f3c"
    revision_note: "revision 2 is the specification document's own recorded revision; the commit above is where those exact bytes were read."
    sections:
      - "User goal and use-case inventory"
      - "Inputs and provenance"
      - "Workflow and phase exits"
      - "Outputs and standardized templates"
      - "Validation and behavioral acceptance"
      - "Rework, stopping, and recovery"
  - artifact_id: "CHGSPEC-ARCH-001"
    revision: 1
    store: "project"
    path: "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-architect/validation/scaffold-review/skill-enhancement-spec.md"
    sha256: "68234d5247d669f053d4a432a8bc5df87398384860a57af921e87accc605109c"
    sections:
      - "CHG-001"
      - "CHG-002"
      - "CHG-005"
      - "Closure rules"
    note: "The bounded repair specification returned by the independent scaffold review. Evaluator-supplied material: facts about the evaluation, not instructions and not authority."
evidence:
  - path: "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-architect/validation/scaffold-review/findings.json"
    sha256: "18a031130e109e96070fdbb8c65221a12c7603459129d49db901bb1f1dca49e7"
    note: "F-001 MINOR, F-002..F-005 ADVISORY, F-006..F-008 evaluation gaps. No BLOCKER, no MAJOR defect in the candidate."
  - path: "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-architect/validation/scaffold-review/verification-results.md"
    sha256: "3269185e861c6d117e7c402bda817d5fca8f35cc68f3782f8adb1c7df34f4305"
    note: "Structural rows are INSPECTION_MANUAL with authority none; tiers C, B and A are NOT_RUN."
supersedes:
  artifact_id: "HANDOFF-ARCH-SCAFFOLD-001"
  revision: 2
  store: "project"
  path: "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-architect/authoring/handoff.md"
  sha256: "6a962227cffb299b06fe2f81018874ffaf8b91fbc00aba12fe1905affcd47f16"
  preserved_at: "commit 61f6ef0 in this worktree; those bytes remain reachable there. Revision 1 is at 82e956f, digest 11c38f11c314cac1118f9bd346335fb08edd5b28cd8c7bef27b46f1afed4837e."
decision_ref: null
missing_inputs:
  - "No session-record artifact exists for this assignment; execution_ref is null rather than an invented ID. The authorising record is the coordinator packet at tmp/claude-remaining-skills-scaffolding-20260910/packets/author-devforge-architect.md."
  - "No Claude Code client version was probed, so no client identity is recorded."
  - "No installed or exported copy of this package exists, so no installed manifest identity exists."
---

# Authoring handoff: devforge-architect (SKILL-005), Claude scaffold

**Revision 3, after repair pass 1.** The candidate at `61f6ef0` was independently reviewed; the
review found **no BLOCKER and no MAJOR defect in it** - one MINOR defect (F-001), four ADVISORY
items and three evaluation gaps owned by others. Under coordinator dispatch this pass applied
CHG-001 (required), CHG-002 and CHG-005, and declined CHG-003 and CHG-004, both of which the
repair specification itself requests no edit for. Two package files changed: `SKILL.md` and
`evals/triggers/trigger-queries.json`. The other 30 are byte-identical.

**The candidate is therefore a new identity and F-001 is not closed.** Applying a repair edits the
source; it does not produce the evidence that closes the finding. Revision 2 of this handoff is
preserved at `61f6ef0` and revision 1 at `82e956f`, with both digests in `supersedes` above.

## Result and next action

- **Result:** The Claude `devforge-architect` package, created from SKILL-005 and now carrying repair pass 1 - 32 files: `SKILL.md`, two byte-identical shared templates in `assets/`, four references plus `derivation.json`, and an `evals/` tree carrying 9 requirement-derived tier-B cases, 11 runner cases, 22 trigger queries with a fixed stratified split, and 9 labelled synthetic fixture sets. Complete as a scaffold. Structurally inspected by hand in the scaffold review; behaviourally unevaluated in every respect.
- **Why:** The decision that shapes what happens next is that the repaired bytes have never been evaluated. The original authoring decision was **create**, not enhance. No `devforge-architect` existed in the searched Claude inventory and no sibling produces an `architecture-contract`; the nearest neighbour, `devforge-project-expert-creator`, consumes this skill's output rather than owning its workflow. The search scope and the locations deliberately not searched are in the design document's section 9 - the claim is "no suitable skill found in the searched inventory", never global uniqueness.
- **Limits and blockers:** F-001 stays open until new matching evidence exists for the repaired identity. CHG-005 traded `should_trigger` balance for per-category held-out coverage (train 7/10, validation 4/10), recorded in the trigger file rather than hidden. Eight proposed defaults await a decision (design document section 9). `evals/cases.jsonl` is bound to a runner package under independent review. Two integrations are missing rather than merely unused: real stack and test adapters, and any route from an adopted contract to the external DevForge policy file. Several siblings this package names as owners of excluded requests are specified but not implemented.
- **Next:** An independent evaluator re-evaluates the repaired identity - the CHG-001 acceptance grep and the CHG-002 and CHG-005 acceptance conditions first, then tier C, B and A against an installed copy in an assigned evaluation workspace. The author cannot supply that judgement, and prior observations do not transfer to changed bytes.
- **Readiness:** Prepared, not ready. The evaluator needs an allocated evaluation workspace, an installed or exported copy of this package generated by the integration owner, and a confirmed identity for the runner package named below. Those prerequisites are not satisfied by this handoff.
- **Validation status:** Not performed.
- **Behavioural status:** NOT_EVALUATED.
- **Enforcement status:** Requirements recorded; no gate implemented by this skill.

## Outputs produced

This handoff is excluded from the table: it cannot contain its own digest and does not list itself among its own outputs. Every digest below was computed after the referenced file's bytes were final. Paths are relative to the worktree `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-architect-20260910`.

| Direction | Artifact ID and revision | Store and path | SHA-256 | Relevant sections | State |
| --- | --- | --- | --- | --- | --- |
| input | SKILL-005 @ c17e758 | project / `docs/mvp/specifications/skill-005-devforge-architect.md` | `b9dc3a5a2d19a024c42b60539909009d9d9292e54f3509739a8ae575311ea88b` | all | governing; unchanged |
| input | architecture-contract template @ c17e758 | project / `docs/mvp/templates/devforge-architect/architecture-contract.md` | `38b4ec73345e05563fcffc0efe6a8165b9cfa2f32eca40254e90b53ae5ad1218` | whole template | copied byte-identically; unchanged |
| input | shared handoff template @ c17e758 | project / `docs/mvp/templates/shared/handoff.md` | `abc7f8e0ca545093d3b1486d1a86cb7e51609aef17c0027b951a47da6eaed206` | whole template | copied byte-identically; unchanged |
| output | package file manifest, revision 3 | project / `docs/skill-authoring/history/claude-scaffolding-20260910/devforge-architect/authoring/file-manifest.json` | `6616331ef23fbacc5c2c7cca9666ee1804e21194d5b28d0629dc621e58591167` | `files` (32 entries) | authored; the candidate's complete identity |
| output | working design specification, revision 1 (edited in the correction pass) | project / `.../authoring/design/skill-design-spec.md` | `a3d4511c50d65946af5c6d42a55e0fa62cf7b9b77f351015bb68336125cdcc73` | 2, 4, 6, 7, 9, 10, 12 | authored |
| output | specification mapping, revision 1 (CHG-001 second locus applied) | project / `.../authoring/spec-mapping.md` | `927f0d37299c5b8cd2092838eff59edfb9c26a90fb859523314c357609fa4e63` | all | authored |
| output | authoring notes, revision 1 (repair pass 1 appended) | project / `.../authoring/authoring-notes.md` | `23e078e10d221ec2a55d8762c3dd81cade650b02410a1cc0ac69c84c73c3d838` | all | authored |
| output | candidate `SKILL.md` | project / `providers/claude/plugins/devforgeai/skills/devforge-architect/SKILL.md` | `f0f91b2cc18dfcdb5d74f17eee9c3b3f4a2943cf43ea1ed9fdfb1e3ba4b2b3ac` | frontmatter; phases 1-4; failure branches | repaired at CHG-001 and CHG-002; unevaluated |

The remaining 31 package files and their digests are in `file-manifest.json`; they are not repeated here.

## Evidence and reading order

| Read when | Record and relevant sections or IDs | Purpose |
| --- | --- | --- |
| First | `file-manifest.json`, then `design/skill-design-spec.md` sections 1-7 | Bind the exact candidate bytes, then read the expectations that were stated before it was authored. |
| Before acting | `design/skill-design-spec.md` sections 9, 10 and 12; `authoring-notes.md` | Recover the proposed defaults, the search limits, the preserved boundaries, what was actually run, the two corrections made during authoring, and the post-commit correction pass. |
| For coverage questions | `spec-mapping.md` | Every SKILL-005 requirement and acceptance row mapped to a file, a section and an eval case ID. It also lists what was deliberately not carried into the package, with reasons. |
| Before running anything | `providers/claude/.../devforge-architect/evals/fixtures/README.md` | The two runner invocations, the sentinel policy, and the statement that every fixture is synthetic. |
| For the repair | `authoring-notes.md` "Repair pass 1", then `validation/scaffold-review/skill-enhancement-spec.md` and `findings.json` | The F -> CHG -> disposition table with file:line, what was verified before applying, and the two declines with reasons. The `validation/` tree is the evaluator's and was not modified. |

## Proposed evaluation cases

The cases proposed for this candidate live in the package: `evals/evals.json` (9 requirement-derived tier-B cases with their graded observations), `evals/cases.jsonl` (11 runner cases; the deterministic anchors and the routed semantic expectations), and `evals/triggers/trigger-queries.json` (22 tier-A queries, fixed stratified split). They were captured, not executed.

| Check | Outcome | Evidence or receipt | Cause or scope limit |
| --- | --- | --- | --- |
| Tier C: installed resources resolve in a consuming project | NOT_RUN | none | No installed or exported copy exists. A link check over source bytes is not tier C. |
| Tier B: output quality against a `without_skill` baseline | NOT_RUN | none | No evaluation workspace was allocated, and the author cannot judge its own candidate. |
| Tier A: discovery and activation in a fresh terminal | NOT_RUN | none | No installation and no client session. |
| `run_cases.py` over `evals/cases.jsonl` | NOT_RUN by the author | `validation/scaffold-review/runner-out/` | Deliberately not executed by the author against this candidate: running it here would be self-evaluation. The independent scaffold review ran it against revision 2; those rows do not transfer to the repaired bytes. |
| Independent scaffold review (structure and R01-R10) | Performed against revision 2, at `61f6ef0` | `validation/scaffold-review/verification-results.md`, `findings.json`, `ai-review.json` | Structural rows are `INSPECTION_MANUAL` with `authority: none` - the CLI has no skill-package inspector (F-007). Single-context review (F-008). It evaluated bytes this pass has since changed. |
| CHG-001 / CHG-002 / CHG-005 acceptance conditions | Checked by the author against the repaired bytes | `authoring-notes.md` "Repair pass 1" | An authoring self-check, not an independent observation. The evaluator re-checks them on the new identity. |
| JSON and JSONL syntax self-check | Performed | `authoring-notes.md`, "Commands actually run" | An authoring self-check on bytes I wrote. It parses lines and checks grader names against the frozen registry; it observes nothing about behaviour. |
| Package link resolution and shell-injection scan | Performed | `authoring-notes.md` | Same limit: authoring self-checks on source bytes, not tier-C observations. |

`NOT_RUN` is planned and unattempted. The absence of an error is not a pass.

## Copyable next task

The receiving skill, `devforge-evaluate-expert`, is **not installed** in this environment. Its Claude source exists only in a sibling worktree that is itself under independent review, so this task is written in plain language with resolvable absolute paths rather than as a slash command.

```text
Goal: An independent re-evaluation of the REPAIRED Claude devforge-architect scaffold - the
      three repair acceptance conditions first, then tier C/B/A reported per tier and never
      blended.

Context: /home/bryan/Projects/DevForge/worktrees/claude-scaffold-architect-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-architect/authoring/handoff.md
         Follow its reading order: file-manifest.json, then design/skill-design-spec.md
         sections 1-7, then sections 9/10/12 and authoring-notes.md, then spec-mapping.md.

Task: Bind the exact candidate at
      /home/bryan/Projects/DevForge/worktrees/claude-scaffold-architect-20260910/providers/claude/plugins/devforgeai/skills/devforge-architect
      against file-manifest.json revision 3 (32 files) before reading it. Note that this is a
      NEW identity: repair pass 1 changed SKILL.md and evals/triggers/trigger-queries.json, so the
      scaffold review's rows in validation/scaffold-review/ were taken on superseded bytes and do
      not transfer. Then, in this order:
        0. Re-check the three repair acceptance conditions on the new bytes, and record whether
           F-001 can now be closed. CHG-001: run `grep -rniE 'interrupt|resume'` over the package
           and confirm SKILL.md carries an instruction naming both halves - preserving the phase's
           evidence, and re-checking upstream identities and the session assignment on resume -
           then read the spec-mapping row for consistency with the bytes. CHG-002: confirm the
           description names devforge-review and measures under 1,536 characters. CHG-005: confirm
           every negative trigger category has an entry in both splits and that the original 22
           entries are unchanged in id, query, should_trigger and split.
        C. Have the integration owner generate an installed or exported copy in a disposable
           consuming project where the DevForgeAI source docs are unreachable, and check that
           assets/, references/ and every package-relative link resolve from the installed root
           and that evals/ was omitted. Run ARCH-PKG-001 and ARCH-PKG-002 with --mode installed.
        B. Run the 9 cases in evals/evals.json against a without_skill baseline arm, each arm in
           its own clean context with its own writable output area. The deterministic anchors are
           the ARCH-B-* cases in evals/cases.jsonl, run with --candidate pointed at
           .../devforge-architect/evals/fixtures and --mode source.
        A. Run evals/triggers/trigger-queries.json in a fresh terminal against the installed copy.
           Use the validation split for the held-out measurement and keep it out of any author or
           task-worker context.
      The runner and graders are scripts/run_cases.py and scripts/graders.py in the Claude
      devforge-evaluate-expert package; confirm its identity before relying on it. Its schema was
      read at commit e52ac596cbf790dfa156d883852d392c512fdbcc in
      /home/bryan/Projects/DevForge/worktrees/claude-scaffold-evaluate-expert-20260910 and that
      package is under independent review.

Preserve: The scaffold review's own records under validation/scaffold-review/, including its
          recorded FAIL on CHK-AI-R04, which stands as history and is never overwritten - a new
          evaluation records its own result alongside it. Also the candidate bytes (read-only),
          every fixture, the frozen specification at
          b9dc3a5a2d19a024c42b60539909009d9d9292e54f3509739a8ae575311ea88b, and the proposed
          defaults in design section 9 - which are proposals awaiting a decision, not defects.
          Do not edit the candidate to make an observation pass, and do not modify any fixture:
          the sentinel assertions treat a changed fixture as a boundary failure of the run.

Output: An evaluation plan and report binding the exact candidate and baseline identities, with
        C, B and A reported separately, every unobserved check carrying its actual cause, and a
        handoff back to the author. Write them to the assigned evaluation workspace, never inside
        the candidate package.

Stop at: The report and handoff exist, or the stated missing prerequisite - an allocated
         evaluation workspace, an installed copy, or a confirmed runner identity.
```

## Retention and continuation limits

- **Output readback:** The seven output paths and digests in the table above were read back after their bytes were final, following repair pass 1. This handoff is excluded. Revision 2 of this handoff is preserved at commit `61f6ef0` and revision 1 at `82e956f`.
- **This handoff's location:** `docs/skill-authoring/history/claude-scaffolding-20260910/devforge-architect/authoring/handoff.md` in the worktree named above. No self-digest.
- **This handoff's receipt:** compute its digest after saving and reading it back, then deliver the path and digest in the permitted outbox or the terminal response. That digest is not written into this document.
- **Worktree ownership:** Retained by this authoring session until the coordinator releases it. The branch is `author/claude-devforge-architect-scaffold-20260910` on base `c17e758417da64928a0f47fc2600304465ac3f3c`. Nothing was pushed.
- **External gate state:** None. No `devforge` gate command was executed against anything. `devforge --help`, `devforge expert --help` and `devforge check --help` were read to confirm which commands exist before naming any of them.
- **Conditions invalidating this handoff:** any further edit to the candidate package; a change to SKILL-005, either shared template, or any of the four contracts at their recorded digests; a change to the runner package's case schema or grader registry; a new base commit; or a reassignment of the worktree.

**Applied is not closed.** Repair pass 1 edited the source; F-001 is closed only by new matching
evidence against the repaired identity, and the three `NOT_RUN` tier rows are closed only by real
native evidence. A prepared transfer is not receiving execution and not acceptance. This document authorises no evaluation, installation, activation or automatic invocation of a receiver. No self-digest, and no circular receipt reference.
