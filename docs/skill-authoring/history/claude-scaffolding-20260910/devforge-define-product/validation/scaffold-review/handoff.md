---
schema_version: "devforge.artifact/v1"
artifact_id: "HANDOFF-002"
artifact_type: "handoff"
project_id: "devforgeai-claude-scaffolding-20260910"
revision: 1
status: draft
created_at_utc: "2026-09-10T21:16:13Z"
producer:
  skill: "devforge-evaluate-expert"
  skill_revision: "bdf665c7e18061395c0762de7a377fdc5f6ed48d66245df5623c5c32b90cf2ac (SHA-256 of the SKILL.md file bytes at commit e641797eebf04cd1e8eb9f711549e038e7745407; source-loaded, never installed, never invoked as a skill)"
execution_ref: null
upstream:
  - artifact_id: "EVREPORT-002"
    revision: 1
    store: project
    path: "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-define-product/validation/scaffold-review/verification-results.md"
    sha256: "38be18684b7a769bc2cf0ac82cd2e9d2b9248a1857b7888fb59d1c7a7e256c7e"
    sections:
      - "Findings"
      - "Independent review R01-R10"
      - "Decision and coverage"
  - artifact_id: "CHGSPEC-002"
    revision: 1
    store: project
    path: "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-define-product/validation/scaffold-review/skill-enhancement-spec.md"
    sha256: "c02a884f92ee68b24f413926d5948b68c35105f3399364ca133775a6f8401b58"
    sections:
      - "Change decision"
      - "Requested changes"
      - "Implementation order"
  - artifact_id: "SKILL-002"
    revision: 2
    store: project
    path: "docs/mvp/specifications/skill-002-devforge-define-product.md"
    sha256: "3e48f93f200499083a062e200f71ad4a3659fad098ef6658fb4b4a34bea6ddbf"
    sections:
      - "Workflow and phase exits"
      - "Rework, stopping, and recovery"
evidence:
  - kind: runner-observations
    path: "runner-out/observations-author-cases-source.jsonl"
    sha256: "cf4f2d30a732b2242e40f4e90d34a4a192d6ab11187365eca1201da26f60b7b6"
  - kind: runner-observations
    path: "runner-out/observations-evaluator-cases-source.jsonl"
    sha256: "bbb6c5e0db662227bc140bf42893cb6386fc289a10b4d4f7d0d8c2ac2de707a5"
  - kind: command-log
    path: "commands.log"
    sha256: "2d5164687107817dde623f84503f56e8f065e4ad00aacfc4294e17efca74bca1"
supersedes: null
decision_ref: null
missing_inputs:
  - "No installed or exported copy of the candidate. Tier C is NOT_RUN; the assignment authorised no installation."
  - "No isolated evaluation workspace and no fresh terminal. Tiers B and A are NOT_RUN."
  - "No authority-store session record. The assignment is the coordinator's task packet; a packet is not a session record, so execution_ref is null rather than an invented identifier."
---

# Skill handoff - scaffold evaluation of devforge-define-product

## You are here

- **Skill and use case:** `devforge-evaluate-expert` - evaluate an existing skill package against
  its governing specification and return evidence-bound results with a bounded repair specification.
- **Current phase:** P6 Return, complete. P1 freeze, P2 deterministic observation, P3 independent
  review, P5 adjudication all complete. P4 native tiers deliberately not attempted.
- **Task state:** **complete.** The evaluation is finished and delivered. This is distinct from the
  candidate's own status, which is a draft scaffold, and from its behavioural status, which is
  `NOT_EVALUATED`. Reporting completion and the candidate passing are separate facts.
- **Session/worktree assignment:** coordinator task packet at
  `/home/bryan/Projects/DevForge/tmp/claude-remaining-skills-scaffolding-20260910/packets/evaluator-devforge-define-product.md`.
  No authority-store session record exists; `execution_ref` is null with the reason in
  `missing_inputs`.
- **Exact candidate or artifact scope:** worktree
  `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-define-product-20260910` at commit
  `05ed112a5a46495041651183493e28c4eae00fed`, package
  `providers/claude/plugins/devforgeai/skills/devforge-define-product/`, 20 files,
  `SKILL.md` sha256 `c93065fc82750ed9df1ad8bdfd8d34b1005af03e49879b13b2f0442800c0083f`.
- **Existing authorization carried forward:** read-only on the candidate and every governing input;
  write permitted only inside this evaluation directory. Nothing outside it was created, modified or
  deleted, and nothing was committed. This handoff authorises no edit, install, run or acceptance.

## Inputs consumed and outputs produced

This handoff is excluded from the rows below: it cannot contain its own complete-byte digest.
Every listed file was hashed after its bytes were complete.

| Direction | Artifact ID/revision | Store/path | SHA-256 | Relevant sections | Decision/freshness state |
| --- | --- | --- | --- | --- | --- |
| input | SKILL-002 rev 2 | project, `docs/mvp/specifications/skill-002-devforge-define-product.md` | `3e48f93f200499083a062e200f71ad4a3659fad098ef6658fb4b4a34bea6ddbf` | all | DRAFT MVP specification; digest independently verified, equals the packet's pin and the candidate's derivation record |
| input | devforge-define-product candidate @ `05ed112a` | worktree, `providers/claude/plugins/devforgeai/skills/devforge-define-product/` | `SKILL.md` `c93065fc8275...`; full 20-file manifest in EVREPORT-002 | all | Frozen. Package bytes proved equal to the frozen commit; working tree clean |
| input | devforge-evaluate-expert @ `e641797` | worktree, `providers/claude/plugins/devforgeai/skills/devforge-evaluate-expert/SKILL.md` | `bdf665c7e18061395c0762de7a377fdc5f6ed48d66245df5623c5c32b90cf2ac` | P1-P6, rubric, runner interface, results contract, missing capabilities | The validator followed. **Draft under bootstrap review**: E2 revise, repaired at `e101e76`, recheck outstanding. Source-loaded, never installed |
| input | run_cases.py @ `e641797` | worktree, `.../devforge-evaluate-expert/scripts/run_cases.py` | `95ca2abf77a5baf249694ad37d67a74949b567acd5164fd309724cbc576583e2` | - | Self-reported identity; no protected-manifest custody exists |
| input | graders.py @ `e641797` | worktree, `.../devforge-evaluate-expert/scripts/graders.py` | `1b7a27a37e1fb8b2e36b1822bc23227c69e6300243e1b49b8caa848e3feca69f` | - | Self-reported identity |
| input | devforge binary | `framework/DevForge/target/debug/devforge` | `835c32639c0a7df270fe1b9182580f14fc7d0874d3aad1b4037ba7cf420b2b07` | `--help` for the root and for `check`, `expert`, `delivery` | Help output only; no subcommand was executed |
| input | Claude Agent Skills documentation | external, `https://code.claude.com/docs/en/skills` | none - a rendered page has no stable byte identity this session could pin | frontmatter fields, name default, 1,536-char truncation, 500-line guidance, install locations, `!` injection | Retrieved 2026-09-10 UTC. Every claim the candidate records was independently re-verified |
| output | EVREPORT-002 rev 1 | project, `.../validation/scaffold-review/verification-results.md` | `38be18684b7a769bc2cf0ac82cd2e9d2b9248a1857b7888fb59d1c7a7e256c7e` | Identity and scope; Evidence groups; Runner observations; R01-R10; Findings; Decision and coverage; Limits | draft; disposition *revise* |
| output | findings record | project, `.../validation/scaffold-review/findings.json` | `d3a2b7426917f07116e2cef6c725805f12a67f07a8f38bed807c11d0ec3593c8` | `findings` F-001..F-010; `severity_counts`; `rubric`; `tiers`; `evaluation_prerequisites` | draft; machine-readable half of EVREPORT-002 |
| output | CHGSPEC-002 rev 1 | project, `.../validation/scaffold-review/skill-enhancement-spec.md` | `c02a884f92ee68b24f413926d5948b68c35105f3399364ca133775a6f8401b58` | Immutable intake; Change decision; CHG-001..CHG-010; Implementation order; Closure rules | draft; authorises no automatic edit |
| output | runner observations, author cases | project, `.../validation/scaffold-review/runner-out/observations-author-cases-source.jsonl` | `cf4f2d30a732b2242e40f4e90d34a4a192d6ab11187365eca1201da26f60b7b6` | 1 header + 12 case records | local, non-isolated evidence; no aggregate row |
| output | runner observations, evaluator cases | project, `.../validation/scaffold-review/runner-out/observations-evaluator-cases-source.jsonl` | `bbb6c5e0db662227bc140bf42893cb6386fc289a10b4d4f7d0d8c2ac2de707a5` | 1 header + 5 case records | local, non-isolated evidence |
| output | evaluator-added case file | project, `.../validation/scaffold-review/runner-out/evaluator-added-cases.jsonl` | `7916011164a59b0cc281e3d0dd1420616e2cafdb31ae6e8784c33189d350a721` | EV-C-101..EV-C-105 | authored by this evaluator, outside the candidate |
| output | command log | project, `.../validation/scaffold-review/commands.log` | `2d5164687107817dde623f84503f56e8f065e4ad00aacfc4294e17efca74bca1` | all | every command actually run |

## What changed and what remains open

**Nothing in the candidate changed.** This evaluator measured and handed back; it did not repair
what it was measuring.

**Outcome:** disposition **revise**. Ten findings: 0 BLOCKER, 1 MAJOR, 3 MINOR, 6 ADVISORY.

**The decisive reason:** F-001. SKILL-002 revision 2 requires interruption-and-resume behaviour in
two separate sections, and it is carried nowhere in the shipped runtime files. Rubric criterion R04
is `FAIL`; every other criterion is `PASS`.

**What is newly proposed versus what is established:** CHG-001 through CHG-010 are proposals to the
next owner, not decisions. No adoption reference exists and `decision_ref` is null. The findings
themselves are observations against frozen bytes and are established.

**What remains open:**

- The three native tiers. C, B and A are all `NOT_RUN` with causes recorded, so **no claim about
  discovery, activation, installed-resource resolution or output quality is supported by anything in
  this evaluation**, and no improvement over the `without_skill` baseline is claimed.
- DP-C-002's `evals/`-exclusion assertion returned `INDETERMINATE` under source mode. The exclusion
  is unobserved, not established.
- Whether the coordinator wants CHG-007 applied at all, given it costs three coordinated digest
  updates on a pinned sentinel for a defect that distorts no current graded observation.
- Whether the two missing DevForge CLI capabilities will be supplied, or whether future evaluations
  of this package continue by manual reading with `authority: none`.

**Worth recording alongside the disposition:** the package is strong. Derivation is exact - all six
destination digests and all twelve source digests verified, both template copies byte-identical to
`docs/mvp`. The ten `devforge` subcommands it names match the binary's own `--help` exactly and no
command is invented. Every Claude client claim in `references/sources.md` was independently
re-verified as accurate. The authority boundaries, the prompt-injection posture and the
proposal-versus-adoption separation are unusually well drawn. The author's own `file-manifest.json`
is correct to the byte across all 20 files. *Revise* here means one real omission and a set of
contained eval-package repairs, not a weak package.

## Observed verification

| Check | Outcome | Raw evidence / external receipt | Cause or scope limit |
| --- | --- | --- | --- |
| Candidate identity frozen and package bytes equal the frozen commit | PASS | `commands.log`; `git diff 05ed112a HEAD --stat -- providers/` empty, `git status --porcelain` clean | Byte identity only |
| Structural observation: inventory, frontmatter, name/folder, link resolution, declarative parsing, no `!` injection, no absolute or home path | PASS | `runner-out/*.jsonl`; `commands.log` | **Method `INSPECTION_MANUAL`, authority `none`.** Obtained by reading plus a non-authoritative runner. No implemented rule catalogue was applied |
| Author case file loads under the frozen runner | PASS | `runner-out/observations-author-cases-source.jsonl`, exit 0, 12 case records | Loading is not running. Exit 0 describes the program, never the candidate |
| Derivation sources and destinations verified against bytes | PASS | `commands.log`; manifest in EVREPORT-002 | 12 source and 6 destination digests, spot-checked well beyond the required 5 |
| Requirement coverage against SKILL-002 | **FAIL** | F-001; `grep` evidence in `commands.log` | Interruption and resume carried nowhere |
| Independent static review R01-R10 | **FAIL** (R04); R01, R02, R03, R05, R06, R07, R08, R09, R10 PASS | EVREPORT-002 "Independent review R01-R10" | Static reading. A static PASS does not establish that a session will follow the instructions. Independence limits recorded |
| Author `file-manifest.json` against actual bytes | PASS | `commands.log` | 20/20 match, no omission, no phantom entry |
| Tier C installed resources | **NOT_RUN** | none | No installed or exported copy; assignment authorised no installation |
| Tier B output quality | **NOT_RUN** | none | No isolated workspace allocated; no baseline arm run |
| Tier A discovery and activation | **NOT_RUN** | none | No fresh terminal available |
| Behavioural status | **NOT_EVALUATED** | none | No session has used this skill |

## Continuation directory

| Order | Task | Owner / skill | Prerequisites | Completion evidence |
| --- | --- | --- | --- | --- |
| 1 | Apply CHG-001: add the interruption-and-resume rule to `SKILL.md` and its procedure to `references/recording-rules.md`, closing the only MAJOR finding | the scaffold's author for `devforge-define-product`, under coordinator dispatch | CHGSPEC-002 and EVREPORT-002 at the digests above; the frozen candidate at `05ed112a`; write access to that package only | A new candidate revision with a new `SKILL.md` digest, `references/derivation.json` destination digests reconciled, and the changed files reported |
| 2 | Apply CHG-002 (correct the two spec-mapping rows), then CHG-003, CHG-004 and CHG-006 | same owner | CHG-001 decided first: CHG-002's preferred form re-cites the section CHG-001 creates | Updated `spec-mapping.md`, `evals/fixtures/README.md`, `evals/evals.json`, `evals/triggers/trigger-queries.json`, `evals/cases.jsonl`; case file still loads under the runner at exit 0 |
| 3 | Decide CHG-005, CHG-007, CHG-008, CHG-009, CHG-010 - each an ADVISORY that may legitimately be deferred with its finding left open | coordinator, then the scaffold's author | The demonstrated impact and the cost note for each, in CHGSPEC-002 | A recorded decision per change; for CHG-007 specifically, either the repair with all three digests reconciled or a README note recording the deferral |
| 4 | Allocate an isolated workspace and install or export the candidate, then run tier C, then B, then A | coordinator, then a native evaluation assignment | A permitted isolated workspace, a fresh terminal, and a decision on which installation mode is under test | Run manifests and case grades per case, arm and attempt; the installed-mode half of DP-C-002 finally observed |
| 5 | Supply skill-package structural inspection and protected-manifest custody in compiled Rust | DevForge integration owner | Independent of everything above | A CLI revision whose `--help` exposes them, which retires both missing-capability statements and changes every affected report |

## Copyable next-session prompt

Goal: Close F-001 in the devforge-define-product scaffold by applying CHG-001, without touching
anything else the enhancement spec does not authorise.

Context: Read, at these exact identities:
  - Repair spec: /home/bryan/Projects/DevForge/worktrees/claude-scaffold-define-product-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-define-product/validation/scaffold-review/skill-enhancement-spec.md
    sha256 c02a884f92ee68b24f413926d5948b68c35105f3399364ca133775a6f8401b58 - sections "Change decision", "CHG-001", "Implementation order", "Closure rules".
  - Evaluation report: .../validation/scaffold-review/verification-results.md
    sha256 38be18684b7a769bc2cf0ac82cd2e9d2b9248a1857b7888fb59d1c7a7e256c7e - section "Findings", finding F-001.
  - Governing requirement: /home/bryan/Projects/DevForge/framework/DevForgeAI/docs/mvp/specifications/skill-002-devforge-define-product.md
    sha256 3e48f93f200499083a062e200f71ad4a3659fad098ef6658fb4b4a34bea6ddbf - "Workflow and phase exits" closing paragraph and "Rework, stopping, and recovery".
  - Target package: /home/bryan/Projects/DevForge/worktrees/claude-scaffold-define-product-20260910/providers/claude/plugins/devforgeai/skills/devforge-define-product/
    at commit 05ed112a5a46495041651183493e28c4eae00fed; SKILL.md sha256 c93065fc82750ed9df1ad8bdfd8d34b1005af03e49879b13b2f0442800c0083f.

Output: An edited SKILL.md carrying the interruption-and-resume rule, an edited
references/recording-rules.md carrying its procedure, and reconciled destination digests in
references/derivation.json. Report the changed files and the new candidate identity. Do not run
validation and do not claim any tier result.

Boundaries: Write only inside that package and inside the authoring evidence tree for CHG-002.
Preserve everything listed under "Behaviour that must be preserved unchanged" in CHGSPEC-002.
Do not edit SKILL-002, any shared contract or template, this evaluation directory, or any eval
expectation in order to make a finding go away. Do not add scripts/, agents/, hooks/, any frontmatter
field beyond name and description, or any `!`-prefixed dynamic-context injection.

Verify: grep -rn -i -e interrupt -e resume over SKILL.md and references/ returns the new
instruction; the four existing "Exit when" lines are unchanged; every SKILL.md link still resolves
in-package; evals/cases.jsonl still loads under the frozen runner at exit 0.

Note on invocation: no DevForgeAI skill is installed in this environment, so the next task is
ordinary editing work by a dispatched author, not a skill invocation. `devforge-define-product`,
`devforge-project-expert-creator` and `devforge-evaluate-expert` exist as provider source only. Do
not present any of them as a runnable command.

## Resume and custody

- **Task output readback:** the four documents and three runner files listed in the outputs table
  above, at the digests shown, each hashed after its bytes were complete and read back. This handoff
  is excluded from that list.
- **This handoff's location:** saved at
  `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-define-product-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-define-product/validation/scaffold-review/handoff.md`.
  It carries no digest of itself.
- **This handoff's external receipt:** its digest is computed after saving and reading it back, and
  delivered in the terminal response to the coordinator. It is not inserted into this document and
  this document is not modified to record it.
- **Worktree ownership disposition:** released. This evaluator holds no lock, no branch and no
  workspace. The candidate worktree was never modified: no commit, no rebase, no reset, no stash, no
  clean, no branch switch. Only this evaluation directory was written.
- **External gate state:** none. No DevForge gate was invoked, no phase state was created or
  advanced, and no receipt exists. The two missing CLI capabilities mean no decision receipt is
  producible; the disposition was adjudicated by hand against the results contract.
- **Conditions invalidating this handoff:** any change to the candidate package bytes; any change to
  SKILL-002 or the governing contracts and templates at their pinned digests; any change to the
  validator, the runner or the graders; an installed or exported copy becoming available, which
  makes tier C observable and supersedes the installed-mode gap; the DevForge CLI gaining a
  skill-package inspector or an evidence reducer, which retires both missing-capability statements
  and reopens every report that recorded them.
