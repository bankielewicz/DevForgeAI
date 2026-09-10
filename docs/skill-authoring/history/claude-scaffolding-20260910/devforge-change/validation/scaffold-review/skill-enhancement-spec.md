---
schema_version: "devforge.artifact/v1"
artifact_id: "CHGSPEC-CHANGE-SCAFFOLD-001"
artifact_type: "skill-enhancement-spec"
project_id: "DevForgeAI"
revision: 1
status: draft
created_at_utc: "2026-09-10T22:24:55Z"
producer:
  skill: "devforge-evaluate-expert"
  skill_revision: "bdf665c7e18061395c0762de7a377fdc5f6ed48d66245df5623c5c32b90cf2ac"
execution_ref: null
upstream:
  - artifact_id: "SKILL-012"
    revision: "DRAFT MVP specification, revision 2, refreshed 2026-09-05 UTC"
    store: "project"
    path: "/home/bryan/Projects/DevForge/framework/DevForgeAI/docs/mvp/specifications/skill-012-devforge-change.md"
    sha256: "b47d49ada93bf5612ea64d5c31d94e31807869316925c53b828deb9e5cbe6774"
    sections: ["Workflow and phase exits", "Validation and behavioral acceptance", "Rework, stopping, and recovery"]
evidence:
  - kind: "evaluation report"
    path: "verification-results.md"
    description: "the report this specification implements; hash it after its bytes are final"
  - kind: "findings"
    path: "findings.json"
  - kind: "runner observations"
    path: "runner-out/"
supersedes: null
decision_ref: null
missing_inputs:
  - "execution_ref: no authority-selected session record exists for this evaluator assignment. The coordinator's packet at /home/bryan/Projects/DevForge/tmp/claude-remaining-skills-scaffolding-20260910/packets/evaluator-devforge-change.md is the assignment; it allocates no SESSION identity, and its absence does not establish ownership of any destination."
  - "Tier C, B and A observations. Every one is NOT_RUN; no change below rests on an unobserved run."
---

# Skill repair and enhancement specification

The bounded, evidence-backed change request returned for the Claude `devforge-change` scaffold.
It authorises no automatic edit, invocation, installation, acceptance or release, and it carries
forward the existing user authorisation without expanding it.

Every change below is derived from a defect demonstrated against bytes. Where a cause could not
be demonstrated, no patch is written.

## Immutable intake

- **Evaluated candidate:** Claude `devforge-change`, worktree
  `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-change-20260910`, commit
  `1056b738309bb66c9b2ace9662424de5b0752190`, package root
  `providers/claude/plugins/devforgeai/skills/devforge-change`, 26 files. The evaluator's own
  per-file SHA-256 manifest is in `verification-results.md` § Identity and scope. `SKILL.md` =
  `e36888541043a8d50cfce9980b94f8a0b7d0c11264d539c13087523f5655450f`.
- **Installed copy evaluated:** none. Not installed; no installed copy exists.
- **Specification:** `/home/bryan/Projects/DevForge/framework/DevForgeAI/docs/mvp/specifications/skill-012-devforge-change.md`,
  DRAFT MVP revision 2 refreshed 2026-09-05 UTC, sha256
  `b47d49ada93bf5612ea64d5c31d94e31807869316925c53b828deb9e5cbe6774`.
- **Evaluation report:** `verification-results.md`, in this directory. Hash it after its bytes
  are final; this document deliberately does not carry that digest, because the report was
  written in the same pass.
- **Results record:** the per-check outcomes are stated in `verification-results.md` §§ Evidence
  groups, Checks actually run, Runner observations and Independent review; there is no separate
  `validation-results.json` in this assignment's deliverable list.
- **Independent review:** `verification-results.md` § Independent review R01-R10. **Independence
  limit: the same context performed P2 and P3.** The rubric reading was completed before any
  author-evidence file was opened; a second fresh reviewer was not available.
- **Cases and fixtures:** the candidate's own `evals/cases.jsonl`
  (`b332e021924b9bd09b030628801ae80df2bc6538f5258c62685ce9f9141d8da2`), `evals/evals.json`
  (`a0931d4a40b04d9169bcd1b9ca70e7d772a6092ac39e49f2d84437cce3d1d463`),
  `evals/triggers/trigger-queries.json`
  (`636d4ed1bf1c155e008b32202cc41070cc84285ece9053280fce3882a01b6a42`), and the fifteen fixture
  files at the digests in the report's manifest. The evaluator's added cases are at
  `runner-out/evaluator-cases.jsonl`.
- **Runner and rubric:** `devforge-evaluate-expert` (Claude) at
  `e641797eebf04cd1e8eb9f711549e038e7745407`, source-loaded. `scripts/run_cases.py` =
  `95ca2abf77a5baf249694ad37d67a74949b567acd5164fd309724cbc576583e2`; `scripts/graders.py` =
  `1b7a27a37e1fb8b2e36b1822bc23227c69e6300243e1b49b8caa848e3feca69f`. **That package is itself a
  draft under bootstrap review (E2: revise -> repaired at `e101e76` -> recheck).**
- **Prior iteration:** none. This is the first evaluation of this package. Package revision 1
  (commit `8e80bc5`) is retained in git history and must not be deleted.

Preserve these identities exactly. Verify them before editing, and retain the current candidate
bytes; the next revision is a new identity.

## Change decision

- **Are target changes justified by the evidence?** **Yes** - one MAJOR and four MINOR defects
  are demonstrated against bytes. CHG-006 through CHG-010 are advisory and the owner may decline
  any of them without weakening conformance to SKILL-012.
- **Next owner:** the scaffold's author for this package, under coordinator dispatch. (The
  validator's generic template names `devforge-project-expert-creator`; this assignment's packet
  names the scaffold's author, and the packet governs. The author followed
  `devforge-project-expert-creator` at `4999f3106565c5e320d1f1a7db066b437e4e94be` as a
  source-loaded builder, which is a recorded dependency and not an authority to widen scope.)
- **Behaviour that must be preserved unchanged:**
  - The four-phase workflow (Capture, Trace impact, Decide, Route and verify) and every bolded
    exit condition.
  - The two-field frontmatter form, `name: devforge-change`, and the folder name.
  - Every existing exclusion clause and trigger phrase in the `description`.
  - All six recorded destination digests and all nine recorded source digests in
    `references/derivation.json`, and both byte-identical asset copies.
  - The corrected fixture hash chain and the recomputed sentinel digests, which are
    independently verified correct.
  - The fixed, stratified trigger split: 30 queries, 14 positive and 16 negative across ten
    categories, each category carrying both a train and a validation entry.
  - Every `execution_status: NOT_RUN`, `activation_claim: NONE`, `claims_not_made` block and
    behavioural `NOT_EVALUATED` statement. None of these may be softened.
- **Forbidden scope changes:** do not add a `scripts/` directory to the package; do not add
  frontmatter fields beyond `name` and `description`; do not edit SKILL-012, any shared template,
  any contract, the roster, `package-index.json`, a sibling skill package, the DevForge CLI, any
  policy or any gate; do not renumber existing case IDs or trigger query IDs; do not weaken or
  delete an existing assertion to convert a MISMATCH into a MATCH; do not create an installed
  copy or run any tier; do not record any tier result.

## Requested changes

### CHG-001: A resumed session re-verifies its frozen identities and its assignment before continuing

- **Finding IDs:** F-001
- **Severity:** MAJOR
- **Change type:** required repair
- **Accepted requirement, or a new proposal:** accepted requirement. SKILL-012 line 45 ("On
  interruption, preserve the current phase and evidence; resume by checking their identities and
  the session assignment again") and line 83 ("If the worktree or active run changes,
  re-establish the appropriate baseline and evidence before resuming").
- **Affected revision, file and section:** package at `1056b73`;
  `providers/claude/plugins/devforgeai/skills/devforge-change/SKILL.md`, the table under
  "## When something is missing or a check cannot run" (`SKILL.md:119-127`), optionally one
  sentence in "## Stopping" (`SKILL.md:129-137`).
- **Evidence and reproduction:** `grep -rni 'interrupt'` over `SKILL.md`, `references/` and
  `assets/` returns nothing. `grep -rni 'resume'` over the same set returns one hit,
  `assets/handoff.md:67` "## Resume and custody", which is the copied shared template's
  handoff-custody section. The author's `spec-mapping.md` maps the requirement to "SKILL.md §
  When something is missing, rows 2 and 4"; those rows are `SKILL.md:122` (a moved upstream,
  installed copy, base commit or candidate) and `SKILL.md:124` (a concurrent writer), and
  neither states an interruption trigger or a resume-time recheck. The same document's own
  "Coverage gaps" section concedes the requirement is "covered only indirectly".
- **Demonstrated impact:** a session resumed after an interruption has no instruction to
  re-verify that the trigger, the cited artifact revisions and the session assignment still match
  what it recorded, so it may continue an impact graph bound to bytes that have since moved -
  which is precisely the failure `references/recording-rules.md:63` warns about ("A digest is
  only true while the bytes behind it are reachable").
- **Bounded desired behaviour:** after the change, an interrupted-and-resumed session is told to
  preserve the phase it reached and the evidence it gathered; and, before continuing, to re-read
  the trigger, the cited artifact revisions and the session assignment and confirm they still
  match the identities it recorded - with a changed identity starting a new iteration rather than
  continuing this one.
- **Suggested minimal edit (wording is the author's to choose):** one new row in the existing
  table, for example - *"The session was interrupted and is being resumed" | "Preserve the phase
  you reached and the evidence you gathered. Before continuing, re-read the trigger, each cited
  artifact revision and the session assignment, and confirm they still match the identities you
  recorded. A changed identity starts a new iteration rather than continuing this one; say which
  it is."*
- **Behaviour to preserve:** every existing row of that table in its current order and wording;
  the four phase exits; the existing Stopping conditions. No reference or asset file needs to
  change, and no reference need be added.
- **Acceptance condition:** a later evaluator greps the runtime package for an interruption or
  resumption instruction and finds one that names both the recheck of the frozen artifact
  identities and the recheck of the session assignment; and `spec-mapping.md`'s row for
  SKILL-012 line 45 points at that instruction rather than at rows 2 and 4.
- **Affected reruns:** `CHG-B-006`, `CHG-B-007`, `evals.json` cases 6 and 7, plus a new case that
  actually interrupts and resumes a run (see CHG-002).

### CHG-002: Add an eval case that interrupts and resumes a run

- **Finding IDs:** F-001
- **Severity:** MAJOR (it is the observation that would close CHG-001)
- **Change type:** required repair - the acceptance condition for CHG-001 needs an observable case
- **Accepted requirement, or a new proposal:** accepted requirement; the same SKILL-012 lines.
- **Affected revision, file and section:** package at `1056b73`; `evals/evals.json` (a tenth case)
  and `evals/cases.jsonl` (a matching deterministic case), plus one fixture directory.
- **Evidence and reproduction:** `spec-mapping.md` § Coverage gaps: "Interruption and resume is
  specified and is covered only indirectly, through the stale upstream and concurrent writer
  cases. **No case interrupts a run.**"
- **Demonstrated impact:** with no case, the repaired instruction from CHG-001 would be
  unobservable at every tier, and the finding could not be closed with matching evidence.
- **Bounded desired behaviour:** one tier-B case whose prompt resumes a partially completed
  assessment - supplying a partial working record plus an artifact set in which one cited
  revision has moved since that record was written - and whose graded observations require the
  resumed session to re-check the recorded identities and the session assignment, to state which
  identities changed, and to treat a changed identity as a new iteration.
- **Behaviour to preserve:** the nine existing `evals.json` cases and the twelve existing
  `cases.jsonl` cases, at their current IDs. Reuse the existing `shared/` and `b7/` fixtures where
  they fit rather than duplicating them.
- **Acceptance condition:** the new case appears in both files, its `files` entries all resolve,
  the file still loads in the frozen runner without rejection, and its `requirement` string quotes
  SKILL-012 line 45.
- **Affected reruns:** the new case; no existing case changes.

### CHG-003: Reconcile the two package-revision records

- **Finding IDs:** F-002
- **Severity:** MINOR
- **Change type:** required repair
- **Accepted requirement, or a new proposal:** accepted requirement - the artifact contract's
  identity-and-revision rules, and `references/derivation.json`'s own `refresh_conditions`.
- **Affected revision, file and section:** `references/derivation.json` keys `package_revision`
  (line 6) and `recorded_at_utc` (line 7);
  `docs/skill-authoring/history/claude-scaffolding-20260910/devforge-change/authoring/file-manifest.json`
  key `recorded_at_utc` (line 7).
- **Evidence and reproduction:** `derivation.json:6` `"package_revision": 1` with
  `recorded_at_utc` `2026-09-10T20:04:04Z`; `file-manifest.json:5` `"package_revision": 2` with
  `recorded_at_utc` `2026-09-10T20:23:16Z` and a `revision_2_change` note. `git log` shows commit
  `1056b73` was authored `2026-09-10T21:09:02Z` and changed seven package files without touching
  `derivation.json`, so the manifest's recorded time precedes the bytes it covers. Independent
  verification: all 26 manifest digests and all six `derivation.json` destination digests match
  actual bytes, so **no digest is stale**.
- **Demonstrated impact:** two provenance records inside one delivered package give different
  revision numbers for the same bytes, and the manifest's timestamp does not describe when its
  digests were taken. A later refresh or citation keyed on a package revision cannot tell which
  record governs.
- **Bounded desired behaviour:** `derivation.json` records `package_revision: 2` with a
  `recorded_at_utc` read from an observed `date -u`, and `file-manifest.json` records the actual
  time its revision-2 digests were computed.
- **Behaviour to preserve:** every recorded source and destination digest in `derivation.json`
  and every file digest in the manifest - none of them changes.
- **Acceptance condition:** the two records agree on the package revision, and each
  `recorded_at_utc` is at or after the commit time of the bytes it describes.
- **Affected reruns:** none; re-verify by reading both records.

### CHG-004: Disclose the third unresolvable fixture citation

- **Finding IDs:** F-003
- **Severity:** MINOR
- **Change type:** required repair
- **Accepted requirement, or a new proposal:** accepted requirement - skill-authoring contract
  line 50 (fixtures reproducible from source), and the package's own README claim.
- **Affected revision, file and section:** `evals/fixtures/README.md` § "Reference digests inside
  the fixtures", the "Two deliberate exceptions" list; alternatively
  `evals/fixtures/shared/XPKG-tide-sync.md` § "File manifest" (lines 41-42).
- **Evidence and reproduction:** the README states every fixture citation "resolves to bytes that
  actually hash to it" and names exactly two exceptions. A scan of every 64-hex string under
  `evals/fixtures/` finds seven references: five resolve; `shared/XPKG-tide-sync.md:41`
  (`a1b2c3d4e5f60718…`, for `SKILL.md`) and `:42` (`112233445566778899aabbccddeeff00…`, for
  `references/reconciliation.md`) do not, and neither is a named exception.
- **Demonstrated impact:** a tier-B worker following `references/impact-tracing.md` § "Resolve a
  reference before you trust it" hits two unresolvable digests that neither the README nor the
  graded observations for `evals.json` cases 1 and 4 anticipate, and the one edge the fixture set
  deliberately leaves unresolvable (PROD-002) stops being distinctive.
- **Bounded desired behaviour:** the reader can tell, from the fixture set itself, that XPKG-004's
  file-manifest rows are digests of notional package files that are not present in the set.
- **Behaviour to preserve:** the five resolving citations, the dependency-order hash chain, and
  both existing documented exceptions. Do **not** create the two absent files to make the digests
  resolve - the fixture is a record about a package that is deliberately not in the set.
- **Acceptance condition:** a rerun of the evaluator's digest-resolution scan finds every
  unresolvable citation accounted for by a statement in the fixture set.
- **Affected reruns:** `evals.json` cases 1 and 4; `CHG-B-001`, `CHG-B-004`.

### CHG-005: Narrow two forbidden strings that can fire on conforming output

- **Finding IDs:** F-004
- **Severity:** MINOR
- **Change type:** required repair
- **Accepted requirement, or a new proposal:** accepted requirement - skill-authoring contract
  line 74; an assertion must not report a violation for output that satisfies the requirement.
- **Affected revision, file and section:** `evals/cases.jsonl`, `CHG-B-002` assertion A1
  `args.forbidden_strings`, and `CHG-B-009` assertion A2 `args.forbidden_strings`.
- **Evidence and reproduction:** the frozen grader matches by plain case-sensitive substring
  (`scripts/graders.py`, `grade_artifact_side_effect`: `for needle in forbidden: if needle in
  text`). `CHG-B-002` A1 forbids `"upgrade applied"`, and the natural conforming sentence for that
  case's required behaviour - "No upgrade applied to dependencies.json" - contains it.
  `CHG-B-009` A2 forbids `"check passed"`, and a conforming assessment that resolved an upstream
  digest may write "the ARCH-002 digest check passed".
- **Demonstrated impact:** `CHG-B-002` observes SKILL-012's *Indirect activation* acceptance case;
  its assertion can report MISMATCH for output that satisfies the requirement, inverting the
  observation. This is the same defect class the author already repaired in this commit for
  `"status: accepted"`; two instances remain.
- **Bounded desired behaviour:** each needle fires only on silent adoption or a false success
  claim, never on a correct denial or a correct verification statement.
- **Suggested minimal edit:** drop `"upgrade applied"` (the sibling needles
  `"Decision state: accepted"` and `"Decision state: adopted"` already carry the adoption intent),
  or replace it with `"we applied the upgrade"`. Replace `"check passed"` with
  `"freshness check passed"`.
- **Behaviour to preserve:** every sentinel digest in both assertions, and every other forbidden
  string in the file. Re-run the author-side check that every `required_report_fields` name still
  exists in `assets/change-request.md`.
- **Acceptance condition:** a later evaluator constructs the conforming sentence for each case and
  observes that no forbidden needle is a substring of it.
- **Affected reruns:** `CHG-B-002`, `CHG-B-009`; `evals.json` cases 2 and 9.

### CHG-006: Name `devforge-review` in the description's exclusion clause

- **Finding IDs:** F-005
- **Severity:** MINOR
- **Change type:** required repair
- **Accepted requirement, or a new proposal:** accepted requirement - skill-authoring contract
  line 111; the measured discrimination surface must be the one the entrypoint carries.
- **Affected revision, file and section:** `SKILL.md:3`, the `description` exclusion clause.
- **Evidence and reproduction:** `SKILL.md:3` names `devforge-develop`, `devforge-brainstorm`,
  `devforge-project-expert-creator` and `devforge-evaluate-expert`; `devforge-review` is absent.
  `evals/triggers/trigger-queries.json` category `negative_review` (A8a train, A8b validation)
  assigns `"owner": "devforge-review"`. `git ls-tree c17e758
  providers/claude/plugins/devforgeai/skills/` shows `devforge-review` is one of the four Claude
  skills actually present. The description measures 1034 characters against the documented
  1,536-character listing cap, so roughly 500 characters of headroom exist.
- **Demonstrated impact:** two of the package's own tier-A negatives test a boundary the
  description never draws, so the planned measurement and the measured surface disagree.
- **Bounded desired behaviour:** the description excludes reviewing a candidate or a diff for
  correctness against its acceptance criteria and names `devforge-review` as its owner, while
  staying inside the cap.
- **Behaviour to preserve:** the two-field frontmatter, the `name`, the four existing exclusions,
  and the closing "routine work already covered by an accepted story does not need a change
  process" clause. Do not restructure the description.
- **Acceptance condition:** the description names five sibling exclusions with their owners and
  measures under 1,536 characters; and, once tier A can run, A8a and A8b are observed as
  non-activations.
- **Affected reruns:** the entire tier-A trigger set - a description edit invalidates every prior
  activation observation for these bytes. None exists yet, so nothing is lost by editing now.

### CHG-007: Correct the `gen_cases.py` claim

- **Finding IDs:** F-006
- **Severity:** ADVISORY
- **Change type:** authorised enhancement (evidence-record accuracy)
- **Accepted requirement, or a new proposal:** accepted requirement - a record must not cite a
  control artifact that is not preserved.
- **Affected revision, file and section:**
  `docs/skill-authoring/history/claude-scaffolding-20260910/devforge-change/authoring/authoring-notes.md`,
  the two sentences citing `gen_cases.py`.
- **Evidence and reproduction:** `find` over the worktree and `git log --all --diff-filter=A` show
  `gen_cases.py` was never added. Independent verification that the digests it was said to protect
  are nevertheless correct: `EVAL-S-004` A1, 26/26 sentinels unchanged; five of seven fixture
  cross-digests resolve and the other two are covered by CHG-004.
- **Demonstrated impact:** a standing anti-drift control is claimed where only a one-time
  verification exists.
- **Bounded desired behaviour:** the record says the sentinels were computed from fixture bytes
  once, by a scratch tool that was not preserved, and that re-verification is the evaluator's
  `artifact_side_effect` run.
- **Behaviour to preserve:** the corrected hash chain and the recomputed sentinels. **Do not
  create and commit `gen_cases.py` to satisfy this**: the workspace development-language policy
  admits Python only for the skill-evaluation JSONL runner and the deterministic graders, so
  preserving a case generator would need the owner's explicit authority first. That decision is
  the coordinator's, not the author's.
- **Acceptance condition:** no record in the authoring evidence cites an artifact that is not
  preserved.
- **Affected reruns:** none.

### CHG-008: Qualify the "Commands that exist" heading

- **Finding IDs:** F-007
- **Severity:** ADVISORY
- **Change type:** authorised enhancement
- **Accepted requirement, or a new proposal:** accepted requirement - SKILL-012 line 45, only
  documented implemented commands may be named; stated precisely.
- **Affected revision, file and section:** `references/cli-boundaries.md`, the heading and first
  line of "## Commands that exist".
- **Evidence and reproduction:** `devforge --help` on the build at
  `/home/bryan/Projects/DevForge/framework/DevForge/target/debug/devforge` (`devforge 0.1.0`)
  lists eleven subcommands; the table covers six. Every command the file names was verified
  present, and its per-command predicates match the leaf `--help` output.
- **Demonstrated impact:** a reader could take the heading as exhaustive and conclude that `init`,
  `red`, `green`, `accept` and `isolate` do not exist. No wrong action follows for this workflow.
- **Bounded desired behaviour:** one clause makes clear the table is the subset a change
  assessment may cite, not the binary's full surface.
- **Behaviour to preserve:** every row's predicate wording, and the "Before relying on any row
  here" instruction to read `--help` first.
- **Acceptance condition:** the heading or its first line states the table is a subset.
- **Affected reruns:** `CHG-B-009`; `evals.json` case 9.

### CHG-009: Restore A3e's independence as a held-out probe

- **Finding IDs:** F-008
- **Severity:** ADVISORY
- **Change type:** authorised enhancement
- **Accepted requirement, or a new proposal:** accepted requirement - skill-authoring contract
  line 111, and the file's own `split_policy` ("only the train split may drive any description
  iteration").
- **Affected revision, file and section:** `evals/triggers/trigger-queries.json`, entry A3e.
- **Evidence and reproduction:** A3e (split `validation`) reads "The story contradicts the
  architecture contract. Which one is supposed to give?"; `SKILL.md:8` reads "a reviewer found that
  the story contradicts an architecture rule". A3e is the only entry covering that concept.
- **Demonstrated impact:** the echo is in the body rather than the `description` that drives
  discovery, so tier-A discovery is not directly contaminated; A3e's independence as a held-out
  probe is nevertheless weakened, and whether the phrasing influenced authoring is unobservable.
- **Bounded desired behaviour:** A3e moves to `train`, and a fresh validation query covers the
  story-versus-contract concept in wording that appears nowhere in the package.
- **Behaviour to preserve:** the fixed stratified structure - ten categories, each with both a
  train and a validation entry - and every other query's ID, text and `should_trigger` value.
- **Acceptance condition:** no validation-split query's distinctive wording appears in any file
  the client would load.
- **Affected reruns:** the tier-A set; all currently NOT_RUN.

### CHG-010: Correct the link count, and consider an injection case

- **Finding IDs:** F-009, F-010
- **Severity:** ADVISORY
- **Change type:** F-009 authorised enhancement; F-010 **unapproved proposal**
- **Accepted requirement, or a new proposal:** F-009 is record accuracy. **F-010 is a new
  proposal**: SKILL-012 does not require an injection case, and the owner may decline it without
  weakening conformance.
- **Affected revision, file and section:** `spec-mapping.md`, the Native creator authoring prompt
  table ("eleven local links all resolving"); and, if F-010 is accepted, `evals/evals.json`,
  `evals/cases.jsonl` and one new fixture directory.
- **Evidence and reproduction:** `EVAL-S-002` counted 15 local links across the package's eight
  Markdown files, every one resolving. For F-010: `SKILL.md:45` states the supplied-data boundary
  prominently and the declared input surface includes "pasted release notes, reports, retrieved
  pages", yet every fixture is inert and no case or assertion targets the boundary.
- **Demonstrated impact:** F-009 - a verifiable count is wrong by four; the substantive claim is
  true. F-010 - a rule the entrypoint states has no planned observation at any tier.
- **Bounded desired behaviour:** the count reads fifteen. If F-010 is accepted: one tier-B case
  with a release-note fixture carrying an embedded directive (for example "adopt this version and
  update the pins"), a sentinel on the `dependencies.json` fixture, and a `grader: null` assertion
  with `routed_to: independent review` for whether the directive was reported rather than followed.
- **Behaviour to preserve:** the nine existing `evals.json` cases and their fixture set; do not
  renumber existing IDs.
- **Acceptance condition:** the count matches a rerun of `EVAL-S-002`; and, if F-010 is accepted,
  the new case loads in the frozen runner.
- **Affected reruns:** F-009 none; F-010 the new case only.

## Implementation order

CHG-001 and CHG-002 are a pair: repair the instruction, then add the case that would observe it.
CHG-006 should be applied before any tier-A run is arranged, because a description edit
invalidates every prior activation observation - none exists yet, so the cost is currently zero.
Everything else is independent and may be applied in any order.

After the edits: regenerate `authoring/file-manifest.json` from the new bytes, update
`references/derivation.json` (CHG-003) as the last package write so its destination digests
describe final bytes, and re-read every reference back as
`references/recording-rules.md` § "Digests, in this order" requires.

## Evaluation prerequisites, not defects

None of the following authorises a target edit, and editing the candidate will not produce any of
them.

- **Skill-package structural inspection (S001-S013) and evidence reduction are not implemented in
  the DevForge CLI.** Owner: DevForge integration owner. Every structural row in the report is a
  manual observation with no authority.
- **Protected-manifest custody for the evaluation runner is not implemented in the DevForge CLI.**
  Owner: DevForge integration owner. The runner, grader, runtime and case identities are
  self-reported by the run.
- **No installed copy exists**, so tier C is NOT_RUN and `CHG-C-002` A8 - the assertion that would
  establish `evals/` is stripped on install - has never been observed against a real installed
  copy. Owner: coordinator.
- **No terminal, run workspace, per-attempt isolation or `without_skill` arm** was allocated, so
  tiers B and A are NOT_RUN and behaviour is `NOT_EVALUATED`. Owner: coordinator.
- **No second fresh reviewer context** was available; P2 and P3 shared one context. Owner:
  coordinator.
- **The validator followed is itself a draft under bootstrap review.** Owner: coordinator. A
  defect in its rubric, results contract or runner propagates into this specification.

## Closure rules

- **Applied** means the source was edited. It does not close a finding.
- A changed candidate is a new identity and needs new matching evidence before any finding is
  closed.
- Preserve the original failure history; never overwrite an earlier `FAIL`. Package revision 1 at
  commit `8e80bc5` and the current bytes at `1056b73` both stay in history.
- Never weaken an accepted expectation, delete a case or change a sibling gate to convert a
  recorded failure into a pass. A defect in a shared contract, a shared template or the DevForge
  CLI goes to its integration owner, not into this package.
- Do not add a migration campaign, a second report or a broader refactor to close a gap that
  belongs to someone else.

**Validation status:** Not performed by this document.
**Behavioural status:** `NOT_EVALUATED`.
**Tiers A, B and C:** `NOT_RUN`.
**Finding status:** ten findings recorded; reevaluation required after any change.
