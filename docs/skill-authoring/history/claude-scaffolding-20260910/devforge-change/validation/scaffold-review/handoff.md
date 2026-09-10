---
schema_version: "devforge.artifact/v1"
artifact_id: "HANDOFF-CHANGE-SCAFFOLD-REVIEW-001"
artifact_type: "handoff"
project_id: "DevForgeAI"
revision: 1
status: draft
created_at_utc: "2026-09-10T22:37:05Z"
producer:
  skill: "devforge-evaluate-expert"
  skill_revision: "bdf665c7e18061395c0762de7a377fdc5f6ed48d66245df5623c5c32b90cf2ac"
execution_ref: null
upstream:
  - artifact_id: "EVREPORT-CHANGE-SCAFFOLD-001"
    revision: 1
    store: "project"
    path: "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-change/validation/scaffold-review/verification-results.md"
    sha256: "7958d02db7b03fa2a400e4ef92e6c006fed67c12adf5896c0009841412b4979b"
    sections: ["Identity and scope", "Evidence groups and outcomes", "Independent review R01-R10", "Findings", "Decision and coverage", "Limits of this evaluation"]
  - artifact_id: "CHGSPEC-CHANGE-SCAFFOLD-001"
    revision: 1
    store: "project"
    path: "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-change/validation/scaffold-review/skill-enhancement-spec.md"
    sha256: "109b7c3930fad22cbb3376c63250557b92cf84f89995d3f153ce177ed13809f5"
    sections: ["Change decision", "Requested changes CHG-001..CHG-010", "Implementation order", "Closure rules"]
  - artifact_id: "SKILL-012"
    revision: "DRAFT MVP specification, revision 2, refreshed 2026-09-05 UTC"
    store: "project"
    path: "/home/bryan/Projects/DevForge/framework/DevForgeAI/docs/mvp/specifications/skill-012-devforge-change.md"
    sha256: "b47d49ada93bf5612ea64d5c31d94e31807869316925c53b828deb9e5cbe6774"
    sections: ["Workflow and phase exits", "Rework, stopping, and recovery"]
evidence:
  - kind: "runner observations"
    path: "runner-out/run1-candidate-cases-mode-installed.jsonl"
    sha256: "3ef529215fba6df690d58b5dae5b0065a81d576c8ae9d911348df05cca17b249"
  - kind: "runner observations"
    path: "runner-out/run2-candidate-cases-mode-source.jsonl"
    sha256: "67a72d5a4639f50e7b0f00e1126cbb7473366ff90a875aac42e5cfb0e5a4d36c"
  - kind: "runner observations"
    path: "runner-out/run3-evaluator-cases-mode-source.jsonl"
    sha256: "2b5ad232a7a84494a1cfe0cfd1c7fb1370fba8724ffcd66e600ad059c0117235"
supersedes: null
decision_ref: null
missing_inputs:
  - "execution_ref: no authority-selected session record exists for this evaluator assignment. The coordinator's packet at /home/bryan/Projects/DevForge/tmp/claude-remaining-skills-scaffolding-20260910/packets/evaluator-devforge-change.md is the assignment; it allocates no SESSION identity, and its absence does not establish ownership of any destination."
  - "Tier C, B and A observations: no installed copy, no fresh terminal, no isolated workspace, no without_skill arm."
  - "A second fresh reviewer context for P3."
---

# Skill handoff

## You are here

- Skill and use case: `devforge-evaluate-expert` - independent scaffold evaluation of the Claude
  `devforge-change` package against SKILL-012, returning evidence and a bounded repair
  specification. Evaluation only; no acceptance is granted and nothing was installed or run.
- Current phase: **P6 Return, complete.** P1 freeze, P2 deterministic observation, P3 independent
  review and P5 adjudication are done; P4 native tiers are `NOT_RUN` with their causes recorded.
- Task state: **complete** for the assigned scope. Distinct from the candidate's document status,
  which stays `draft`, and from its behavioural status, which stays `NOT_EVALUATED`.
- Session/worktree assignment: independent evaluator under a coordinator, packet at
  `/home/bryan/Projects/DevForge/tmp/claude-remaining-skills-scaffolding-20260910/packets/evaluator-devforge-change.md`.
  Write fence:
  `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-change-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-change/validation/scaffold-review/`.
  Nothing outside it was written; no commit was made.
- Exact candidate or artifact scope: Claude `devforge-change` at commit
  `1056b738309bb66c9b2ace9662424de5b0752190`, package root
  `providers/claude/plugins/devforgeai/skills/devforge-change`, 26 files, `SKILL.md` =
  `e36888541043a8d50cfce9980b94f8a0b7d0c11264d539c13087523f5655450f`. Candidate HEAD equalled the
  packet's frozen commit exactly. Not installed.
- Existing authorization carried forward: the coordinator's packet. This handoff authorises no
  edit, install, invocation, acceptance or release, and preparing it invokes nobody.

## Inputs consumed and outputs produced

This handoff is excluded from the rows below: it cannot contain its own complete-byte digest, and
it does not list itself among its own outputs.

| Direction | Artifact ID/revision | Store/path | SHA-256 | Relevant sections | Decision/freshness state |
| --- | --- | --- | --- | --- | --- |
| input | SKILL-012 rev 2 | `framework/DevForgeAI/docs/mvp/specifications/skill-012-devforge-change.md` | `b47d49ada93bf5612ea64d5c31d94e31807869316925c53b828deb9e5cbe6774` | Workflow and phase exits; Rework, stopping, and recovery | frozen; matches the packet's stated digest |
| input | devforge-change candidate @ `1056b73` | `providers/claude/plugins/devforgeai/skills/devforge-change` (26 files) | per-file manifest in `verification-results.md` § Identity and scope | whole package | frozen; 26/26 sentinels re-observed unchanged at the end of the evaluation |
| input | devforge-evaluate-expert @ `e641797` (validator, source-loaded) | `worktrees/claude-scaffold-evaluate-expert-20260910/providers/claude/plugins/devforgeai/skills/devforge-evaluate-expert` | `SKILL.md` `bdf665c7e18061395c0762de7a377fdc5f6ed48d66245df5623c5c32b90cf2ac`; `run_cases.py` `95ca2abf77a5baf249694ad37d67a74949b567acd5164fd309724cbc576583e2`; `graders.py` `1b7a27a37e1fb8b2e36b1822bc23227c69e6300243e1b49b8caa848e3feca69f` | P1-P6, rubric R01-R10, results contract, runner interface | **draft under bootstrap review** (E2: revise -> repaired at `e101e76` -> recheck) |
| input | author evidence (untrusted, informational) | `docs/skill-authoring/history/claude-scaffolding-20260910/devforge-change/authoring/` (5 files) | `spec-mapping.md` `a3c60ce1b51a70752783fbf35d68cd35b891e44c81f006012f03edaf6f87c760`; `file-manifest.json` `8cc1c747417ead19d872072c38ed1dabdb9579e4c64c4f24db26d4bcee260c87`; `authoring-notes.md` `1b88f0441c8690858c09c4dce93e2fc54fb093ba18662c1e5d09c780c7bf1671` | spec mapping; manifest; authoring notes | read only after the rubric pass; every cited claim verified against bytes |
| output | EVREPORT-CHANGE-SCAFFOLD-001 rev 1 | `<fence>/verification-results.md` | `7958d02db7b03fa2a400e4ef92e6c006fed67c12adf5896c0009841412b4979b` | all | draft; disposition `revise` |
| output | CHGSPEC-CHANGE-SCAFFOLD-001 rev 1 | `<fence>/skill-enhancement-spec.md` | `109b7c3930fad22cbb3376c63250557b92cf84f89995d3f153ce177ed13809f5` | CHG-001..CHG-010 | draft; not authorised, not applied |
| output | findings record | `<fence>/findings.json` | `569c9ee560fa33aabb451364794715a08247e085b53593955eed063e4a201562` | F-001..F-010 | draft |
| output | command log | `<fence>/commands.log` | `ee5c8771ecd0baf93e519bd76dca139a49660489cadcf3cf28e525e556e439d1` | all | complete |
| output | evaluator case file | `<fence>/runner-out/evaluator-cases.jsonl` | `a2bb42306db1ba761a23b8880b03242137b162a323db7aa43a7e6c91af31702a` | EVAL-S-001..EVAL-S-005 | authored by the evaluator, not the author |
| output | runner observations, run 1 | `<fence>/runner-out/run1-candidate-cases-mode-installed.jsonl` | `3ef529215fba6df690d58b5dae5b0065a81d576c8ae9d911348df05cca17b249` | 12 case records | local, non-isolated evidence |
| output | runner observations, run 2 | `<fence>/runner-out/run2-candidate-cases-mode-source.jsonl` | `67a72d5a4639f50e7b0f00e1126cbb7473366ff90a875aac42e5cfb0e5a4d36c` | 12 case records | local, non-isolated evidence |
| output | runner observations, run 3 | `<fence>/runner-out/run3-evaluator-cases-mode-source.jsonl` | `2b5ad232a7a84494a1cfe0cfd1c7fb1370fba8724ffcd66e600ad059c0117235` | 5 case records | local, non-isolated evidence |

`<fence>` is
`/home/bryan/Projects/DevForge/worktrees/claude-scaffold-change-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-change/validation/scaffold-review/`.

## What changed and what remains open

Nothing in the candidate changed. No package byte, no author-evidence byte, no governing input
and no gate was edited; no commit was made; no skill was installed, invoked or run.

**Disposition: `revise`.** One applicable rubric criterion failed. Counts: **0 BLOCKER, 1 MAJOR,
4 MINOR, 5 ADVISORY.**

- **F-001 (MAJOR, R04 FAIL)** - the interruption-and-resume behaviour SKILL-012 requires at lines
  45 and 83 has no instruction anywhere in the runtime package. The author's own mapping points at
  two table rows that do not carry it, while the same document's coverage-gap list concedes the
  requirement is covered "only indirectly". A resumed session is therefore never told to re-verify
  its trigger, its cited artifact revisions or its session assignment. CHG-001 is a one-row edit to
  `SKILL.md`; CHG-002 adds the case that would observe it.
- The four MINOR defects are contained and each has a one-line or one-clause repair: two
  provenance records disagreeing on the package revision (F-002); a third unresolvable fixture
  citation the fixtures README does not disclose (F-003); two substring forbidden-strings that can
  fire on conforming output, including for a specification acceptance case (F-004); and
  `devforge-review` missing from the description's exclusions although the package's own tier-A
  negatives assign that owner (F-005).
- Five ADVISORY items are recorded, one of which (F-010, an injection eval case) is explicitly an
  **unapproved proposal** the owner may decline without weakening conformance to SKILL-012.

**What is genuinely strong, and should be preserved rather than re-litigated:** the authority
boundaries (R03, R10) are unusually clear - the package refuses to narrate a phase as a check, to
issue itself a PASS, or to write a simulated gate, and it enumerates five requirements with no
implemented check and routes each to the integration owner as design input. Every `devforge`
command it names exists in `devforge 0.1.0 --help` and every per-command predicate matches the
leaf help. No shell-injection token, no Codex-only concept, no `docs/mvp` runtime path and no
developer home path appears anywhere. All 15 local links resolve in-package; both asset copies are
byte-identical to the governing templates; all six derivation destination digests and all nine
source digests match bytes; and the candidate's `evals/cases.jsonl` loads in the frozen runner
without rejection.

**What remains open, and is not the author's to close:** every behavioural question. Tiers C, B and
A are `NOT_RUN`, behaviour is `NOT_EVALUATED`, and no baseline arm exists, so nothing here says
whether a session finds this skill, loads it, follows it, or produces a better change-request with
it than without it.

## Observed verification

| Check | Outcome | Raw evidence / external receipt | Cause or scope limit |
| --- | --- | --- | --- |
| Candidate HEAD equals the packet's frozen commit | PASS | `commands.log`; `git rev-parse` = `1056b73` | none |
| Validator byte-pinned to `e641797`, worktree clean | PASS | `commands.log`; nine files EQUAL | the validator is itself an unevaluated draft |
| Specification digest matches the packet | PASS | `b47d49ad…` | none |
| Governing templates and contracts at `c17e758` match `references/derivation.json` | PASS | nine source digests | none |
| Both packaged assets byte-identical to their governing templates | PASS | `diff` | none |
| DevForge CLI command surface vs `references/cli-boundaries.md` | PASS | `devforge --help`, six leaf helps, `devforge 0.1.0` | `--help` only; no command run against any project |
| Claude client facts vs `references/sources.md` | PASS | `WebFetch https://code.claude.com/docs/en/skills`, fetched 2026-09-10 | documentation describes the client, not this package |
| Provider-syntax and runtime-dependency hygiene | PASS | `EVAL-S-004` A2-A8; grep scans | source tree, not an installed copy |
| Structural observation (frontmatter, name/folder, links, resources) | PASS | run1, run3 | `INSPECTION_MANUAL`; authority none |
| Fixture cross-digest resolution | 5 of 7 resolve | evaluator scan | finding F-003 |
| Author `file-manifest.json` vs bytes | PASS, 26/26 | `commands.log` | the manifest's revision and timestamp are finding F-002 |
| Frozen case runner, three runs | all exit 0 | `runner-out/*.jsonl` | exit status describes the program, never the candidate; rows carry no authority |
| Independent review R01-R10 | 9 PASS, 1 FAIL (R04) | `verification-results.md` | one context performed P2 and P3 |
| Tier C installed resources | **NOT_RUN** | none | no installed copy; the packet forbids attempting an install |
| Tier B output quality | **NOT_RUN** | none | no terminal, no run workspace, no `without_skill` arm |
| Tier A discovery and activation | **NOT_RUN** | none | no fresh terminal |
| Behavioural status | **NOT_EVALUATED** | none | no run of any kind was observed |
| Skill-package structural inspection and evidence reduction in the DevForge CLI | not implemented | - | evaluation prerequisite; owner: DevForge integration owner |
| Protected-manifest custody for the evaluation runner | not implemented | - | evaluation prerequisite; owner: DevForge integration owner |

## Continuation directory

| Order | Task | Owner / skill | Prerequisites | Completion evidence |
| --- | --- | --- | --- | --- |
| 1 | Decide whether to dispatch the repair now or to run the tiers first, and rule on the two owner-level questions below | coordinator | this handoff | a recorded decision |
| 2 | Apply CHG-001 and CHG-002 (the MAJOR pair), then CHG-003 through CHG-006 | the scaffold's author for this package, under coordinator dispatch | `skill-enhancement-spec.md`; the frozen candidate identity | changed files, the new candidate identity, and a regenerated `file-manifest.json` - reported without running validation |
| 3 | Rule on CHG-007 (`gen_cases.py`) and CHG-010's F-010 half, both of which need an owner decision before any edit | coordinator | CHG-007 and CHG-010 | a recorded decision |
| 4 | Allocate an installed copy in a consuming project where `docs/mvp` is unreachable, and run tier C | coordinator, then an evaluator | a permitted installation target | tier C run manifests and case grades |
| 5 | Allocate a fresh terminal, a per-case run workspace with `inputs/` and `outputs/`, and a `without_skill` arm; run tier B then tier A | coordinator, then an evaluator | tier C admitted; CHG-006 applied first, since a description edit invalidates any prior tier-A observation | tier B and A run manifests, transcripts and case grades |
| 6 | Re-evaluate the changed candidate and close findings only against new matching evidence | an independent evaluator | a new candidate identity | a new EVREPORT at the new identity; this one is not amended |

## Copyable next-session prompt

Goal: Apply the bounded repairs CHG-001 through CHG-006 to the Claude `devforge-change` package
and report the changed files and the new candidate identity. Do not run any validation and do not
record any tier result.

Context: The frozen candidate is
`/home/bryan/Projects/DevForge/worktrees/claude-scaffold-change-20260910/providers/claude/plugins/devforgeai/skills/devforge-change`
at commit `1056b738309bb66c9b2ace9662424de5b0752190`, 26 files, `SKILL.md` sha256
`e36888541043a8d50cfce9980b94f8a0b7d0c11264d539c13087523f5655450f`. Verify that identity before
editing anything. The governing specification is
`/home/bryan/Projects/DevForge/framework/DevForgeAI/docs/mvp/specifications/skill-012-devforge-change.md`
sha256 `b47d49ada93bf5612ea64d5c31d94e31807869316925c53b828deb9e5cbe6774`; the requirement behind
the MAJOR finding is its line 45, restated at line 83. Read
`/home/bryan/Projects/DevForge/worktrees/claude-scaffold-change-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-change/validation/scaffold-review/skill-enhancement-spec.md`
in full - it carries the evidence, the bounded desired behaviour, the behaviour to preserve and the
acceptance condition for each change - and read `verification-results.md` in the same directory for
the observations behind them.

Output: edited files inside
`providers/claude/plugins/devforgeai/skills/devforge-change/`, a regenerated
`docs/skill-authoring/history/claude-scaffolding-20260910/devforge-change/authoring/file-manifest.json`,
and `references/derivation.json` written last so its destination digests describe final bytes.

Boundaries: stay in the assigned worktree and in those two paths. Do not edit SKILL-012, any
shared template, any contract, the roster, a sibling skill package, the DevForge CLI, any policy or
any gate. Do not add a `scripts/` directory or a frontmatter field beyond `name` and `description`.
Do not renumber an existing case or query ID, and do not weaken or delete an assertion to turn a
MISMATCH into a MATCH. CHG-007 and the F-010 half of CHG-010 need a coordinator decision first -
leave them alone unless you have one. Applying a change does not close a finding.

Verify: `grep -rni interrupt` over the runtime package returns the new instruction; the new
interrupt/resume case appears in both `evals/evals.json` and `evals/cases.jsonl` and every `files`
entry resolves; the case file still loads in the frozen runner at
`/home/bryan/Projects/DevForge/worktrees/claude-scaffold-evaluate-expert-20260910/providers/claude/plugins/devforgeai/skills/devforge-evaluate-expert/scripts/run_cases.py`;
the two provenance records agree on the package revision; the conforming sentence for each repaired
forbidden-string case contains no forbidden needle; and the `description` names five sibling
exclusions and stays under 1,536 characters.

Every DevForgeAI roster skill named in this prompt is a draft, and only `devforge-brainstorm`,
`devforge-change`, `devforge-develop`, `devforge-project-expert-creator` and `devforge-review`
exist in the Claude provider source at this commit. None of them is installed here, so this is a
plain-language task with resolvable absolute paths rather than a slash command.

## Resume and custody

- Task output readback: the six deliverables and four runner files listed in the outputs table
  above, each read back and hashed after its bytes were final. This handoff is excluded.
- This handoff's location:
  `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-change-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-change/validation/scaffold-review/handoff.md`.
  No self-digest.
- This handoff's external receipt: compute its digest after saving and reading it back, and deliver
  the path and digest in the terminal response or a permitted outbox. Do not insert that digest
  into this document.
- Worktree ownership disposition: **released.** No worktree was created or modified beyond the
  untracked output fence, no branch was touched, no commit was made, and no process was left
  running.
- External gate state: no DevForge gate was run. `devforge --help` and `--version` were read from
  the build at `/home/bryan/Projects/DevForge/framework/DevForge/target/debug/devforge`
  (`devforge 0.1.0`); reading help establishes which subcommands exist and nothing more.
- Conditions invalidating this handoff: any change to the candidate package bytes, to SKILL-012, to
  the packaged or governing templates, to the `devforge-evaluate-expert` runner, graders or rubric
  at a revision after `e641797`, to the DevForge CLI's command surface, or to the Claude Code
  skills documentation retrieved on 2026-09-10. A new candidate revision is a new identity and
  starts a new evaluation iteration rather than amending this one.

## Decisions the coordinator must make

1. **Dispatch order.** CHG-006 edits the `description`. A description edit invalidates every prior
   tier-A observation. None exists yet, so applying it now costs nothing and applying it after a
   tier-A run would waste that run.
2. **CHG-007.** The authoring record cites `gen_cases.py` as a standing control; the file was never
   committed. Preserving a Python case generator would need explicit authority under the workspace
   development-language policy, which admits Python only for the skill-evaluation JSONL runner and
   the deterministic graders. Correcting the wording needs no such authority. Choose which.
3. **CHG-010 / F-010.** An eval case for the supplied-data-is-not-instructions boundary is a new
   proposal, not a SKILL-012 requirement. Accept or decline.
4. **The validator dependency.** This evaluation's method came from a draft package under its own
   bootstrap review (E2: revise -> repaired at `e101e76` -> recheck). If that package's rubric,
   results contract or runner changes at a later revision, this report's method changes with it and
   a re-evaluation would be a new iteration.
5. **Tier allocation.** Nothing behavioural is known about this package. Deciding whether the
   scaffold is adequate for its stated scope needs tiers C, B and A, and none of them can be
   arranged inside an evaluator's fence.
