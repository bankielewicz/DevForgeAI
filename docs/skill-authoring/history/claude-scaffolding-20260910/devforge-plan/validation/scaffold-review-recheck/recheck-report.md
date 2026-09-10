---
schema_version: "devforge.artifact/v1"
artifact_id: "EVREPORT-PLAN-SCAFFOLD-001"
artifact_type: "expert-evaluation-report"
project_id: "devforgeai"
revision: 2
status: draft
created_at_utc: "2026-09-10T22:10:48Z"
producer:
  skill: "devforge-evaluate-expert"
  skill_revision: "source-loaded, not installed; SKILL.md read from git commit e641797eebf04cd1e8eb9f711549e038e7745407. No installed copy exists, so no installed-file digest is claimed."
execution_ref: null
upstream:
  - artifact_id: "SKILL-006"
    revision: 2
    store: project
    path: "docs/mvp/specifications/skill-006-devforge-plan.md"
    sha256: "149a66a375da1bb3447f51b657996883974fec1dac3ce92af866eba94a378e4b"
    sections:
      - "Workflow and phase exits"
      - "Validation and behavioral acceptance"
      - "Rework, stopping, and recovery"
  - artifact_id: "devforge-plan candidate package"
    revision: "git f8709e84272ba1d642387d86c476cf37c8cad81f"
    store: "git worktree, read-only"
    path: "providers/claude/plugins/devforgeai/skills/devforge-plan/"
    sha256: "30-file manifest; the seven changed files are listed in Candidate identity below"
    sections:
      - "SKILL.md"
      - "references/"
      - "assets/"
      - "evals/"
  - artifact_id: "artifact-contract"
    revision: 2
    store: project
    path: "docs/mvp/artifact-contract.md"
    sha256: "00d8c4f4bf619b8361e056c2b77c8215595755a0eb6262b865e6a8f464c1d2b5"
    sections:
      - "Standard envelope"
evidence:
  - "runner-out/recheck-pkg-source.jsonl"
  - "runner-out/recheck-pkg003-installed.jsonl"
  - "runner-out/recheck-pkg003-source.jsonl"
  - "runner-out/recheck-plc003.jsonl"
  - "commands.log"
  - "findings-recheck.json"
supersedes:
  artifact_id: "EVREPORT-PLAN-SCAFFOLD-001"
  revision: 1
  store: "evaluation evidence, committed at 68b5f0d"
  path: "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-plan/validation/scaffold-review/verification-results.md"
  sha256: "fc784022665fe9b18cc56bd0c3270c86076fa5f628b802736ac908c5e9f4d9d7"
  note: "Revision 1's bytes stay reachable and unmodified at that path and at commit 68b5f0d. This revision supersedes it for the disposition; it does not replace its observations of the 03dc1a6 bytes."
decision_ref: null
missing_inputs:
  - "No installed copy of devforge-plan exists in any Claude discovery location; tier C cannot be observed."
  - "No fresh terminal and no isolated evaluation workspace were allocated; tiers B and A cannot be observed."
  - "No eval case stages an interrupted session, so F-001's closure is structural and not behavioural."
  - "No session record was supplied for this evaluation; execution_ref is null and its absence does not establish ownership."
---

# Focused recheck — devforge-plan repair pass 1

Scope, as dispatched: recheck only the changed requirements F-001 through F-007 against the new
revision, and recheck R04 only. Unchanged broad checks were **not** rerun; their first-pass evidence
still stands for the bytes it observed. I recommend; I do not accept, adopt, install or release
anything, and nothing here authorises an edit.

## Candidate identity

- **New candidate:** worktree `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-plan-20260910`
  at `f8709e84272ba1d642387d86c476cf37c8cad81f` (HEAD), package
  `providers/claude/plugins/devforgeai/skills/devforge-plan/`, 30 files.
- **Prior candidate:** `03dc1a605acfb3ff80577f244d1a60f52244fb36`, whose bytes remain reachable at that
  commit. `68b5f0d` committed my first-pass review directory; `git diff 68b5f0d HEAD --stat` over
  `validation/` is empty, so the repair commit did not touch it.
- **Validator:** unchanged — `devforge-evaluate-expert` at `e641797`, source-loaded, still a draft under
  bootstrap review with no native evaluation.

Seven package files changed. Their digests at `f8709e8`, recomputed by me at 2026-09-10T22:06Z:

| sha256 | changed file |
| --- | --- |
| `3a50ee188a84738dbe6a6a8956526f1928afd7336b5e8b20bab12552ae81f64d` | `SKILL.md` |
| `a1b4fcec6bb800dbacb4d6c6e658cb5aae992dd98adff277119a7017122ae49b` | `assets/handoff.md` |
| `d68c5536ad3f058f75149253f866f5a652f95cdf20105186923d2b574ab19c77` | `evals/cases.jsonl` |
| `e37ec74ec62f29e0e314026266450d2467d025f44404bedb1724e3ba9348051b` | `evals/fixtures/good/HANDOFF-001.md` |
| `7d84ab90564063a95451a4140b48fdc907d95f994306adb23a922b13c872f5d6` | `references/derivation.json` |
| `78cc43630a963a7a8c324c78f082bbbbb0e12f97466caa08f8aff80ff4352e82` | `references/readiness-check.md` |
| `1100fa1b8463a696add721fcf3649ea4c61364dab3dd995bbd6e5b465455f204` | `references/recording-rules.md` |

Unchanged and therefore not re-observed: `assets/epic.md` `48f8b069…`, `assets/story.md` `a19ccd7f…`,
`references/sources.md` `7238dacc…`, `references/upstream-resolution.md` `604b9cd9…`,
`evals/evals.json` `d5627bf4…`, `evals/triggers/trigger-queries.json` `ad23ff64…`, and every fixture
except `good/HANDOFF-001.md`.

## Per-finding closure

| Finding | Severity at rev 1 | Verdict | Evidence |
| --- | --- | --- | --- |
| F-001 | MAJOR | **Closed, structurally** | Three locations now carry what one location was claimed to carry and did not. `SKILL.md` §"Stopping" gains a paragraph opening "Stopping deliberately is not the same as being interrupted", instructing preservation of the phase reached, the frozen input identities and any outputs already written, and requiring a re-read of the session assignment and a re-check of the recorded digests before any further write, with a changed input treated as a new iteration. It links `references/readiness-check.md`, which gains §"Resuming after an interruption": preserve first, a three-step re-check (assignment, digests, base or run identity), an outcome table saying what each result blocks, and an instruction to record the resume itself. `assets/handoff.md` §"You are here" regains the **Current phase** row removed at revision 1, adapted to name the four phases. Both halves of SKILL-006 line 46 and the line-85 requirement are now instructed at the point of use. **Closure is structural: the instruction exists. No behavioural observation establishes that a session follows it** — see the eval-case note below. |
| F-002 | MINOR | **Closed** | `SKILL.md` §"Required inputs" gains a paragraph opening "A missing input is not the same as no adopted scope at all", naming `devforge-brainstorm` for which problem is worth solving and `devforge-define-product` for what the scope should contain, and repeating the suggested/installed/invoked separation. The routing is now the operative body instruction, not only a frontmatter exclusion, and the paragraph states its own precedence against the neighbouring missing-input rule. |
| F-003 | MINOR | **Closed** | `PL-PKG-001` drops its case-level `mode` and its A5; new `PL-PKG-003` carries A5 with `"mode": "installed"`. `runner-out/recheck-pkg-source.jsonl`: `PL-PKG-001` A1-A4 are now four real `MATCH` rows in source mode — frontmatter present, `name`/`description` populated scalars, `name` == folder, and 8 local links all resolving. `runner-out/recheck-pkg003-source.jsonl`: `PL-PKG-003` A5 is `INDETERMINATE` with the mode reason, so the gate is isolated to the one installation-dependent assertion instead of blocking four others. |
| F-004 | MINOR | **Closed** | `PL-PKG-002` A9 is retargeted from `references/recording-rules.md` to `references/sources.md`; A10 and A11 are removed. `runner-out/recheck-pkg-source.jsonl`: A9 now observes "1 local, 2 external" — a row that can fail. The case's `expectations.summary` states why the other three references carry no Markdown links and that `SKILL.md`'s links are covered by `PL-PKG-001` A4, so the removal is documented rather than silent. |
| F-005 | MINOR | **Closed** | All four sources in the `evals/cases.jsonl` derivation entry are repinned from `e52ac59` to `e641797`, and I verified each digest against the validator bytes: `run_cases.py` `95ca2abf…`, `graders.py` `1b7a27a3…`, `runner-interface.md` `87c8942f…`, `evals/cases.jsonl` `c31a7cb0…`. `dependency_status` now records the recheck as performed and states what it established — registry byte-identical, every key permitted, all 18 cases loaded — and says how it was obtained, and that a further script change requires another recheck. |
| F-006 | MINOR (recorded ADVISORY at rev 1) | **Closed** | `references/recording-rules.md` rewrites the paragraph to say where the restatement stops and the narrowing begins: the contract requires the exact installed revision or digest, this package narrows that to the SHA-256 of the installed `SKILL.md`, and the contract still governs. It adds that the contract supplies a `null`-plus-`missing_inputs` fallback for `execution_ref` and none for `producer`, so an unrecoverable value is a missing required fact — write `unknown` with what is known **and** record it in `missing_inputs`, because `unknown` with an empty `missing_inputs` is a draft presented as complete. |
| F-007 | ADVISORY | **Closed** | The `assets/handoff.md` derivation entry's `transformation` now names all three departures from the shared template: the removed `Exact candidate or artifact scope` row with its reason, the `Task state` fold into `Result`, and the `Current phase` removal explicitly labelled a defect (F-001, F-007) with the note that the row is restored at revision 2. A `repair_pass_1` key is present on each of the five changed derivation destinations. |

**No finding is still open. No new finding.**

## Regression checks

Each of these was chosen because a repair could plausibly have broken it.

| Check | Result |
| --- | --- |
| `description` byte-identical | Yes. `sed -n '3p'` hashes to `64b9772dbf2298de3039a181c07684adc34e6ad1c8136b16593a36a859ae0601` at both `03dc1a6` and `f8709e8`; the whole frontmatter block (lines 1-5) hashes to `d47e317920c97f86d1be2e68cb006287454472be3167defa6d6dc07a3fae8cf6` at both. Every diff hunk starts below line 74. The discovery surface is untouched, so the first pass's trigger-split and no-leakage findings still hold. |
| Restored `Current phase` row present in the good HANDOFF fixture, not only in the template | Yes. `evals/fixtures/good/HANDOFF-001.md` gains `- **Current phase:** Check readiness, completed for the authored story; Specify not started for the four allocated stories.` — a populated value consistent with that fixture's `Result: partial`, not a copied placeholder. The template and the conforming example agree. |
| Sentinel updated consistently | Yes. The fixture's new digest is `e37ec74ec62f29e0e314026266450d2467d025f44404bedb1724e3ba9348051b`, and `PL-C-003` A2's `forbidden_strings` entry is exactly that string. `grep` for the superseded `e85fb43b…` across the whole package returns no match, so no stale digest survives. `runner-out/recheck-plc003.jsonl` A2 is `MATCH`, "2 sentinel(s) unchanged", confirming the no-self-digest check is live against the new bytes and that `EPIC-001` and `STORY-001` still hash to the values the fixture cites. |
| Fixture does not contain its own digest | Yes. Zero occurrences of its own digest in its own bytes. |
| `PL-C-003` A1 still complete after a field was added to the fixture | Yes. `MATCH`, "12 fields". |
| `SKILL.md` links still resolve after a link was added | Yes. `PL-PKG-001` A4 observes 8 local links (was 7), all resolving inside the package. |
| `SKILL.md` size | 265 lines, up from 249; still inside the documented 500-line guidance. |
| Case file still loads against the frozen runner | Yes. 18 cases, 59 assertions (61 minus A10 and A11; A5 moved rather than removed). No duplicate `case_id`, no key outside the frozen runner's permitted sets, exit 0 on all four runs. |
| All `derivation.json` destination digests | 11 of 11 correct against the file bytes; `evals/fixtures/` still null by design. |
| Author evidence at revision 2 | `authoring/file-manifest.json` is revision 2, supersedes revision 1 at `03dc1a6`, records 30 entries with **0 mismatches** against the actual bytes, and its `repair_pass_1_changed_files` list is exactly the seven files the git diff shows. The new fixture digest is recorded and the old one is absent. |
| `spec-mapping.md` claims the first pass falsified | Both corrected. Line 58 now cites the three real locations; line 78 now cites the `SKILL.md` §"Required inputs" paragraph as the operative body instruction. A correction table names the original false claims and the finding each belongs to, rather than quietly overwriting them. |
| Untouched files | `evals/evals.json` and `evals/triggers/` are byte-identical, so the 11 tier-B cases and the 27 stratified trigger queries are unchanged. |

## R04 recheck

Rechecked alone, as dispatched. R01-R03 and R05-R10 were `PASS` at revision 1 and are not re-adjudicated
here; the changed bytes do not touch what they cite, except that R07's F-006 note is now resolved.

**R04 Workflow decisions and failure paths — `PASS`.**

Both branches that produced the `FAIL` are now instructed. The FAIL anchors were "an essential action has
no usable transition" (interruption had none) and the absence of the routing the acceptance table
requires. Both are addressed at the point of use, with the reference routed from the phase that needs it.

I checked specifically for the anchor a repair of this shape most easily trips — "two instructions
prescribe incompatible actions for the same condition with no precedence" — and it does not apply. Each
new paragraph opens by naming the neighbouring rule it must not be confused with and stating which
condition it governs: "A missing input is not the same as no adopted scope at all" separates the routing
rule from the missing-input rule, and "Stopping deliberately is not the same as being interrupted"
separates the resume rule from the stop conditions. The `readiness-check.md` outcome table is consistent
with `upstream-resolution.md` (a moved digest is a new iteration needing authorisation, not a silent
substitution) and with the collision rule it cross-references (a reassigned destination stops dependent
writes). No conflicting duplicate rule was introduced.

## Does SKILL-006 require a dedicated interruption eval case?

**No.** The specification's §"Validation and behavioral acceptance" enumerates five acceptance cases —
Direct activation, Indirect activation, Missing behavior, Traceability, Out of scope — plus four
additional common cases: concurrent writer, upstream change, surviving placeholder, and a check that
cannot execute. Interruption and resume appears in §"Workflow and phase exits" (line 46) and
§"Rework, stopping, and recovery" (line 85) as **required behaviour**, and in neither enumerated list.
The candidate carries a case for all nine enumerated cases.

So the author's deferral is consistent with the specification, and it is recorded honestly rather than
hidden: `authoring-notes.md` names it as a known gap not closed by this pass, and `spec-mapping.md`
line 58 marks the eval column "none authored — see the gap note below". The "add a tier-B case" line in
my revision-1 CHG-001 was my own rerun recommendation, not a specification requirement, and I record
that distinction rather than converting my suggestion into an obligation.

What follows is narrower and stands: **F-001's closure is structural, not behavioural.** The instruction
exists and is reachable; nothing observes whether a session follows it. Adding such a case would be a
discretionary enhancement that strengthens future evidence. Its absence is an evaluation gap for the
coordinator's allocation decision, not a defect in the candidate, and it does not reopen F-001.

## Runner observations

Local, non-isolated evidence. `MATCH` / `MISMATCH` / `INDETERMINATE` are observations about single
assertions, never outcomes; no aggregate is computed. Exit status describes the program. Runner identity
is self-reported by the run, because protected-manifest custody is still not implemented.

| Run | Selection | `--candidate` | `--mode` | Exit | Rows |
| --- | --- | --- | --- | --- | --- |
| 1 | `PL-PKG-001`, `PL-PKG-002` | package root | `source` | 0 | `PL-PKG-001` A1-A4 `MATCH` (frontmatter; `description,name`; `name='devforge-plan' folder='devforge-plan'`; 8 local links resolve). `PL-PKG-002` A1-A8 `MATCH` present, A9 `MATCH` "1 local, 2 external", A12 `MATCH` absent |
| 2 | `PL-PKG-003` | package root | `installed` | 0 | A5 `MISMATCH` "evals is present but the case required it to be absent" — the expected artefact of running an installed-mode assertion against source bytes. Not a candidate defect and not tier C evidence; no installed copy exists |
| 3 | `PL-PKG-003` | package root | `source` | 0 | A5 `INDETERMINATE` "the case declares mode 'installed' and this run used 'source'" — confirms the mode gate now covers only the installation-dependent assertion |
| 4 | `PL-C-003` | `evals/fixtures` | `source` | 0 | A1 `MATCH` "12 fields"; A2 `MATCH` "2 sentinel(s) unchanged"; A3 `INDETERMINATE` (routed to independent review, as authored) |

Not rerun, deliberately: `PL-C-001`, `PL-C-002`, `PL-C-004`, `PL-C-005`, `PL-C-006` and
`PL-B-001`..`PL-B-009`. None of the files they observe changed, and the pass was scoped to the changed
requirements. Their revision-1 rows in `../scaffold-review/runner-out/` remain the evidence for them.

## Missing capabilities and evaluation prerequisites

Unchanged by this pass and recorded again in full, whatever the observations were.

- **Skill-package structural inspection (S001-S013) and evidence reduction are not implemented in the
  DevForge CLI.** Every structural row here is `INSPECTION_MANUAL` with `authority: none`. A complete set
  of matching runner rows does not close this. Owner: DevForge integration owner.
- **Protected-manifest custody for the evaluation runner is not implemented in the DevForge CLI.** The
  runner, grader, runtime and case identities in `runner-out/*.jsonl` are self-reported by the run.
  Owner: DevForge integration owner.
- **No implemented decision receipt exists.** No `decision.json` was produced; the disposition below was
  adjudicated by hand against the validator's results contract.
- **Tiers C, B and A remain `NOT_RUN`** — no installed copy, no fresh terminal, no isolated workspace, no
  baseline arm. Owner: the coordinator, for allocation.
- **The validator followed is itself a draft under bootstrap review** with no native evaluation.
- **No eval case stages an interrupted session**, so F-001's closure cannot be behavioural. Owner: the
  coordinator, for the allocation decision; not a defect in the candidate.

None of these is a defect in `devforge-plan`, and no edit to it produces any of them.

## Disposition

- **Updated disposition: insufficient evidence.** Adjudicated by hand against the validator's results
  contract. The revision-1 `revise` rested on one applicable `FAIL` at R04; that `FAIL` is resolved, and
  no applicable `FAIL` remains. The contract's next clause then governs: *otherwise a missing required
  observation gives insufficient evidence*. Tiers C, B and A are `NOT_RUN`, so *suitable for the stated
  scope* — which requires every required observation passing — is not reachable and **would not have been
  reachable however good the repair was**. This is a change of cause, not a grade: the candidate no
  longer has a demonstrated defect blocking it; it has never been observed running.
- **Behavioural status: `NOT_EVALUATED`.** Unchanged. No session has run this skill.
- **Findings at this revision:** 0 BLOCKER, 0 MAJOR, 0 MINOR, 0 ADVISORY open. Seven closed.
- **Repair quality:** each of the seven repairs is bounded to what the finding demonstrated. Nothing was
  weakened to pass: no case was deleted to remove a failing row, no expectation was relaxed, no sibling
  gate was touched, and the two corrected `spec-mapping.md` rows record what the original claim said
  rather than quietly replacing it. The three of my seven findings that were closest to judgement calls
  (F-002, F-006, F-007) were addressed on their substance rather than argued with.

*Insufficient evidence* is a recommendation about what is known, not a rejection and not acceptance.

## Limits

- **This is a focused recheck, not a re-evaluation.** Only the changed requirements and R04 were
  examined. R01-R03 and R05-R10 rest on the revision-1 reading of the revision-1 bytes; I verified the
  changed bytes do not touch what those criteria cite, but I did not re-derive them.
- **Every observation is about bytes.** Nothing here establishes that a Claude session finds, loads or
  follows this skill.
- **Same reviewer as revision 1.** I know the findings I wrote and what a closing repair would look
  like, which is the opposite of independence for a closure judgement. A reviewer who had not written
  F-001..F-007 might read the same repairs differently.
- **Structural evidence obtained by reading**, in the same filesystem and process space as the candidate,
  under a self-reported runner identity with no protected custody.
- **F-001's closure is structural only**, as stated above.

## Recovery and continuation

- **Last completed phase:** P6 — recheck results written to the assigned recheck fence.
- **Frozen input digests still matching:** yes at 2026-09-10T22:10:48Z. Candidate HEAD `f8709e8`;
  specification `149a66a3…`; validator worktree HEAD `e641797`.
- **Owned processes and workspace disposition:** none retained. Four `python3 -B` runner invocations
  completed and exited. No worktree or branch held, no commit made.
- **First-pass evidence:** `../scaffold-review/` is unmodified. Its five documents and five runner
  outputs stand as the record of the `03dc1a6` bytes; this report supersedes it for the disposition only.
- **Conditions invalidating this report:** the package changes again; SKILL-006 or a governing contract
  is revised; the frozen validator's rubric, runner or graders change; or an installed copy, terminal or
  isolated workspace becomes available, which would make the three `NOT_RUN` tiers observable and start a
  new iteration rather than continuing this one.
