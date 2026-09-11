---
schema_version: "devforge.artifact/v1"
artifact_id: "CHGSPEC-004-SCAFFOLD-01"
artifact_type: "skill-enhancement-spec"
project_id: "DevForgeAI"
revision: 1
status: draft
created_at_utc: "2026-09-10T21:23:19Z"
producer:
  skill: "devforge-evaluate-expert"
  skill_revision: "bdf665c7e18061395c0762de7a377fdc5f6ed48d66245df5623c5c32b90cf2ac"
  skill_revision_note: "sha256 of the one SKILL.md source-loaded from e641797eebf04cd1e8eb9f711549e038e7745407"
execution_ref: null
upstream:
  - artifact: "EVREPORT-004-SCAFFOLD-01"
    store: "this directory"
    path: "verification-results.md"
  - artifact: "SKILL-004"
    revision: 2
    path: "/home/bryan/Projects/DevForge/framework/DevForgeAI/docs/mvp/specifications/skill-004-devforge-prototype.md"
    sha256: "e4f61c35220641f053a828615df1bc3415c707fde26fcf8b0cdece6cdb1ba54c"
evidence:
  - path: "findings.json"
  - path: "runner-out/candidate-cases.observations.jsonl"
    sha256: "f0e57b1298931e41dcff55dff46f761bc5cb1ff4f16a934f2d9c017b9733ed24"
  - path: "runner-out/evaluator-structural-cases.jsonl"
    sha256: "e539c5f6d2987d203897f812e583061d362bfda49f79ea7245edf412190258a9"
  - path: "runner-out/evaluator-structural.observations.jsonl"
    sha256: "ee64109c2bbd87bd9dad2a9d2e57ca8c817c0bb1f845e85537f9d23abaccca97"
  - path: "runner-out/probe-candidate-root-is-package.observations.jsonl"
    sha256: "2452d3923e7ac8d6c879ede110194c31b41f5e53c38a631f11c2a9b319761237"
supersedes: null
decision_ref: null
missing_inputs:
  - "The revision of the devforge-evaluate-expert package the next evaluation will be given. CHG-004 records the value to write rather than guessing a future pin."
---

# Skill repair and enhancement specification — devforge-prototype (SKILL-004)

The bounded, evidence-backed change request returned for the Claude `devforge-prototype` scaffold. It
authorises no automatic edit, invocation, installation, acceptance or release, and it expands no existing user
authorisation.

Every change below is traceable to a finding that was demonstrated against bytes or against a run recorded in
this directory. No change is proposed for anything unobserved.

## Immutable intake

- **Evaluated candidate:**
  `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-prototype-20260910/providers/claude/plugins/devforgeai/skills/devforge-prototype/`
  at commit `e199230858d871926fff2d55de8b015fa0ce335e`; 31 files; manifest `candidate-manifest.txt`
  (`6bd15a3ead18037682c70168752c66e838b2d536c2130462d8842acc5eb4ee6f`).
- **Installed copy evaluated:** none. No export and no project-local installation was allocated or attempted.
- **Specification:** `docs/mvp/specifications/skill-004-devforge-prototype.md`, revision 2,
  `e4f61c35220641f053a828615df1bc3415c707fde26fcf8b0cdece6cdb1ba54c`.
- **Evaluation report:** `verification-results.md` in this directory (EVREPORT-004-SCAFFOLD-01).
- **Results record:** `validation-results.json` in this directory.
- **Independent review:** `ai-review.json` in this directory. **Not fully independent** — P2 and P3 shared a
  context and the author's records were read before the per-criterion records were completed. Recorded as a
  limit, not as `COULD_NOT_RUN`.
- **Cases and fixtures:** the candidate's `evals/` at the commit above; plus the evaluator-added
  `runner-out/evaluator-structural-cases.jsonl` (`e539c5f6…`), which is evidence in this directory and is
  **not** part of the candidate.
- **Prior iteration:** none. This is the first evaluation of this package, and the baseline is
  `without_skill`.

Preserve these identities exactly. Verify them before editing and retain the old candidate; a changed
candidate is a new identity.

## Change decision

- **Are target changes justified by the evidence?** **Yes** — six, all demonstrated. Five touch `evals/`
  metadata and fixtures; one touches two sentences of `SKILL.md` and one paragraph of a reference.
- **Next owner:** the **author of this scaffold**, under coordinator dispatch. *(The validator's own default
  next owner is `devforge-project-expert-creator`; the assignment overrides it, because the repairs are
  edits to this scaffold rather than a generated-expert repair cycle. Recorded so the substitution is
  visible rather than silent.)*
- **Behaviour that must be preserved unchanged:**
  - The whole of `SKILL.md` other than the two sentences named in CHG-003 — in particular the three framing
    failure modes, the ownership prohibition at line 20, the two-roots rule, the required-inputs table, the
    supplied-material-is-not-instructions paragraph at line 40, the four phase bodies and their exits, the
    destination-selection rule, the five common-case bullets, the fixed vocabulary paragraph and the
    stopping section.
  - All three `assets/` templates, byte-for-byte. Two are byte-identical copies of the governing templates
    and the third is a recorded bounded adaptation; all three verified against `references/derivation.json`.
  - Every `references/` file other than the one paragraph named in CHG-003.
  - Every fixture's **bytes** except where CHG-006 is taken, and in particular the sentinel digest
    `f9138601783d24d2a3dd8170db7b510c557ec22d906b76afc7707aa5be8e223f` and the preserved
    `defect-fence-breach/preserved/service-notes.baseline.md`, on which case XP-C-006's verifiability depends.
  - Every existing `cases.jsonl` case, its `candidate_subpath`, its assertions and its authored expectations.
    CHG-001 **adds**; it changes no existing observation.
  - The 22 trigger queries, their `should_trigger` values and their fixed train/validation split. The split
    was assigned once at authoring time and must not be re-randomised.
  - The frontmatter field set (`name` and `description` only) and the `name` == folder-name equality.
- **Forbidden scope changes:** do not add a `scripts/` directory or any Python, shell or other executable
  implementation to this package; do not add framework logic in any language (the development language policy
  assigns it to compiled Rust in the DevForge CLI). Do not edit the specification, the `docs/mvp` templates,
  the shared contracts, the roster, the installer, a sibling skill, or the DevForge CLI, its policy, its
  tests or its `tooling_files` pins. Do not weaken or delete an eval case, a fixture or an authored
  expectation to convert a recorded observation into a passing one. Do not implement any of the four missing
  CLI integrations inside this package. Do not claim, in any edited file, that a tier ran.

## Requested changes

### CHG-001: Add deterministic cases that observe the candidate package, and make each `tier` label say what it observes

- **Finding IDs:** F-001
- **Severity:** MINOR
- **Change type:** required repair
- **Accepted requirement:** the skill-authoring contract's tier C, "installed resources **and** outputs —
  Templates/references/helper resolve inside the installed package; outputs land in the consuming project's
  map". The candidate's tier-C cases carry only the second half.
- **Affected revision, file and section:** `e199230`, `evals/cases.jsonl`, every line (the `tier` field);
  and the file as a whole (new cases).
- **Evidence and reproduction:** `runner-out/candidate-cases.observations.jsonl` — all 9 cases resolve inside
  `evals/fixtures/`. `runner-out/probe-mode-installed.observations.jsonl` — `--mode installed` yields
  byte-identical results, because no case declares a `mode`. Contrast
  `runner-out/evaluator-structural.observations.jsonl`, where 10 evaluator-added cases observe the package
  itself and complete cleanly, which demonstrates the graders for this exist and are currently unused.
- **Demonstrated impact:** no authored deterministic case observes the package or an installed copy, and the
  `tier` labels name the tier the fixture simulates rather than an observation of it, so a completed run of
  this file can be read as tier-C and tier-A coverage that does not exist.
- **Bounded desired behaviour:** afterwards, `evals/cases.jsonl` additionally contains cases that observe the
  candidate package — at minimum `frontmatter_present` and `frontmatter_fields` on `SKILL.md`,
  `name_folder_relation` with `expect_equal` (asserting equality **as the DevForgeAI convention**, with a
  `notes` line saying so, because Claude's own naming rules make a difference legitimate),
  `package_relative_links` on `SKILL.md` and on each `references/*.md`, `path_present` for each of the six
  routed resources, and one case with `"mode": "installed"` asserting `path_absent` on `evals` so an
  installed copy's stripped eval tree is actually observed. These cases must **omit** `candidate_subpath`, so
  they read `--candidate` directly. Each existing case keeps a short `notes` value stating what its `tier`
  refers to (the tier its fixture simulates) so a reader cannot mistake it for tier coverage.
  `runner-out/evaluator-structural-cases.jsonl` in this directory is a working, already-executed starting
  point; **copy from it, do not reference it** — it is evaluation evidence and must not become a package
  dependency.
- **Behaviour to preserve:** all nine existing cases unchanged, including their `candidate_subpath` values,
  assertions and expectations. Adding a case must not change an existing observation.
- **Acceptance condition:** running `evals/cases.jsonl` with `--candidate <package root>` `--mode installed`
  against a genuine installed copy produces the package-observing rows, and running it with
  `--candidate <package>/evals/fixtures` still reproduces all nine existing rows exactly as recorded in
  `runner-out/candidate-cases.observations.jsonl`. Note the two roots differ; CHG-005 is what makes that
  statable.
- **Affected reruns:** every case in `evals/cases.jsonl`, plus the new ones.

### CHG-002: Correct XB-8's baseline arm to `without_skill`

- **Finding IDs:** F-002
- **Severity:** MAJOR
- **Change type:** required repair
- **Accepted requirement:** SKILL-004 "Additional common cases" — a template placeholder remains in a
  required result field; and the skill-authoring contract's tier B, which needs a real second arm.
- **Affected revision, file and section:** `e199230`, `evals/evals.json`, `evals[7]` (id 8,
  `placeholder-in-required-field-stays-a-draft`), key `baseline_comparison`.
- **Evidence and reproduction:**
  `git -C <candidate-wt> ls-tree -r --name-only c17e758417da64928a0f47fc2600304465ac3f3c providers/claude/plugins/devforgeai/skills/`
  returns four skills and no `devforge-prototype`; the only `devforge-prototype` paths at base are the
  specification and the two `docs/mvp` templates. The package's own `spec-mapping.md` says "No baseline
  existed", and `handoff.md` line 81 says ten of eleven cases have no `old_skill` baseline — both contradict
  `evals.json` case 8.
- **Demonstrated impact:** one of the specification's four required common cases declares a preserved
  previous revision that does not exist, so its tier-B comparison has no second arm and supports no
  improvement claim. The rationale recorded at `authoring-notes.md:107` — that "a prior report artifact is the
  fixture" — conflates a fixture supplied *to* a case with a baseline *arm of the comparison*, and the
  fallback it proposes (`NOT_APPLICABLE`) would misuse the fixed vocabulary, which reserves that word for a
  stated scope exclusion.
- **Bounded desired behaviour:** `"baseline_comparison": "without_skill"`, matching the other ten cases. If
  the author still wants to record that the case's *fixture* is a prior report artifact, that belongs in the
  case's prose (`expected_output` or a note), never in `baseline_comparison`.
- **Behaviour to preserve:** the case's `prompt`, `files`, `expected_output` and all five
  `graded_observations` unchanged — the case itself is well constructed, and the user's "tell the team it is
  ready to circulate" framing is exactly the pressure the case should apply.
- **Acceptance condition:** every case in `evals/evals.json` declares a baseline arm that resolves to
  something that exists at the recorded base, and no case declares `old_skill` while no previous revision of
  this skill exists.
- **Affected reruns:** XB-8. Also correct `authoring-notes.md:107` and `handoff.md:81` if those author
  records are being maintained, so the contradiction does not survive the repair.

### CHG-003: Say what a self-computed plan freeze does and does not establish, and point at the file that says it

- **Finding IDs:** F-003
- **Severity:** MINOR
- **Change type:** required repair
- **Accepted requirement:** rubric criterion R08 (a material contradiction with a decision impact); SKILL-004
  phase 1 exit condition.
- **Affected revision, file and section:** `e199230`, `SKILL.md` line 50 (phase 1 `**Exit:**`), and
  `references/experiment-boundaries.md` section "Measurement before result".
- **Evidence and reproduction:** `SKILL.md:50` asserts the freeze exists "so that a later reader can tell the
  plan preceded the evidence"; `references/framework-context.md:33` states the opposite — "Hashing the plan
  yourself records which bytes you had; it does not establish that they preceded the evidence to anyone who
  does not already trust you." Grepping `references/experiment-boundaries.md` for `preced`,
  `does not establish`, `self-recorded` and `outside the evaluated` returns nothing, so the file `SKILL.md`
  routes the reader to for the limitation does not carry it.
- **Demonstrated impact:** the always-loaded entrypoint tells a session that a self-computed hash establishes
  temporal ordering, in the one place the skill says its whole value lives (`SKILL.md:10`), and the pointer
  that would correct it is a dead end.
- **Bounded desired behaviour:** two edits, both small.
  1. `SKILL.md:50` — keep the instruction to freeze, drop the claim it establishes ordering to a third party.
     Something with the shape of: *"Freeze it — hash the bytes and record the identity, and record where that
     identity is held. A hash you computed yourself records which bytes you had; whether anything outside your
     reach holds it is a separate fact, and [Recording rules](references/recording-rules.md) has the field that
     says which you have."* The exact wording is the author's; the requirement is that the sentence no longer
     asserts what `framework-context.md:33` denies, and that the link resolves to text that actually addresses
     it.
  2. `references/experiment-boundaries.md`, "Measurement before result" — add one sentence carrying the limit,
     so the file that phase 1 currently names is not empty on the subject even if the link is repointed.
- **Behaviour to preserve:** the freeze instruction itself, the write ordering in
  `references/recording-rules.md` (unchanged), the "Plan identity frozen before execution" guidance at
  `recording-rules.md:60` (already correct), and the open-integration row at `framework-context.md:33`
  (already correct — it is the sentence the other two must agree with).
- **Acceptance condition:** no sentence in the package asserts that a self-computed digest establishes that
  the plan preceded the evidence, and every link offered as the explanation of a freeze's limits resolves to
  text that states them.
- **Affected reruns:** XB-1 and XB-10 (both turn on what the plan's frozen identity is taken to mean).

### CHG-004: Repin and restate the recorded runner dependency

- **Finding IDs:** F-004
- **Severity:** MINOR
- **Change type:** required repair
- **Accepted requirement:** the skill-authoring contract's rule that a recorded dependency identifies the
  exact bytes it means, and refreshes when the source changes.
- **Affected revision, file and section:** `e199230`, `evals/evals.json`, `runner_dependency.commit` and
  `runner_dependency.status`.
- **Evidence and reproduction:** the pin is `e52ac596cbf790dfa156d883852d392c512fdbcc`.
  `git log --oneline e52ac59..e641797` in the validator worktree shows `b6a4bf7` (E2 independent bootstrap
  review at `e52ac59`, revise), `e101e76` (repair pass 1, F-001..F-009), `6916b60` (focused recheck, new MINOR
  F-R01), `e641797` (derivation digests regenerated). `git diff e52ac59 e641797 --stat` over that package's
  `scripts/` shows both `run_cases.py` and `graders.py` changed, 147 insertions and 16 deletions.
- **Demonstrated impact:** the deterministic arm names a runner revision a bootstrap review found defective
  and that has since been repaired twice. It is not breakage — this evaluation ran the cases against the
  `e641797` runner and all thirteen assertions agreed with their authored expectations — but the recorded
  identity and its status sentence no longer describe the runner an evaluator would be handed.
- **Bounded desired behaviour:** `runner_dependency.commit` names the revision the next evaluation will
  actually be given (`e641797eebf04cd1e8eb9f711549e038e7745407` as of this report; confirm with the
  coordinator rather than assuming, since that package is still moving), and `runner_dependency.status`
  states its real condition: source-only, not installed, its own evaluation `NOT_RUN`, and *its bootstrap
  review history* (revise at `e52ac59` → repaired at `e101e76` → rechecked, one MINOR open). Add the digests
  of `run_cases.py` and `graders.py` at the pinned revision, so a later reader can tell a repin from a drift.
- **Behaviour to preserve:** `runner_dependency.boundary` verbatim — its statement that a runner row must
  never be copied into a results record as an outcome is correct and load-bearing. Also preserve
  `runner_dependency.supplies` and `source_location`.
- **Acceptance condition:** the pinned revision's `run_cases.py` and `graders.py` hash to the digests
  recorded beside it, and the status sentence is true of that revision.
- **Affected reruns:** all nine cases in `evals/cases.jsonl`.

### CHG-005: Record the `--candidate` root the authored cases require

- **Finding IDs:** F-005
- **Severity:** MINOR
- **Change type:** required repair
- **Accepted requirement:** the runner interface — `--candidate` selects the root that every
  `candidate_subpath` resolves against; the skill-authoring contract's resource-path rule that a documented
  resource must be locatable.
- **Affected revision, file and section:** `e199230`, `evals/evals.json` (`runner_dependency`), with the same
  statement optionally echoed in `evals/fixtures/README.md`.
- **Evidence and reproduction:** `runner-out/probe-candidate-root-is-package.observations.jsonl` — invoking
  with `--candidate <package root>` exits 0, writes a complete observations file, and reports all nine cases
  `COULD_NOT_RUN` with cause `candidate_subpath 'good' does not resolve to a directory inside the candidate
  root`. Zero assertions observed.
- **Demonstrated impact:** the natural reading of "candidate root" produces a clean-looking run that observes
  nothing. That is the silent coverage loss the runner's whole-file rejection is designed to prevent,
  reintroduced through the invocation.
- **Bounded desired behaviour:** `runner_dependency` gains an explicit invocation record — the required
  `--candidate` value for the fixture-backed cases
  (`<package>/evals/fixtures`), the `--mode` to use, and, once CHG-001 lands, the *different* `--candidate`
  value the package-observing cases need (`<package root>`, or the installed root). State plainly that a
  wrong `--candidate` produces `COULD_NOT_RUN` rows at exit 0 rather than an error.
- **Behaviour to preserve:** every case's existing `candidate_subpath` value; do not restructure the fixture
  tree to make one root serve both.
- **Acceptance condition:** an evaluator who has read only `evals/evals.json` can invoke the runner correctly
  on the first attempt for both case groups.
- **Affected reruns:** all nine cases in `evals/cases.jsonl`.
- **Not in scope here:** the same convention is undocumented in the `devforge-evaluate-expert` package's own
  cases. That is a defect in a sibling package and belongs to its owner. Report it; do not edit that package
  to close this finding.

### CHG-006: Reconcile fixture filenames with the artifact IDs inside them, or say why they differ

- **Finding IDs:** F-006
- **Severity:** ADVISORY
- **Change type:** unapproved proposal — take it or record why not; it fails no accepted requirement.
- **Accepted requirement:** none. Readability of the provenance chain only.
- **Affected revision, file and section:** `e199230`, `evals/fixtures/good/experiments/XPLAN-001.md:3` and
  `XREPORT-001.md:3`; `evals/fixtures/defect-moved-threshold/experiments/XPLAN-004.md:3` and
  `XREPORT-004.md:3`; or, alternatively, `evals/fixtures/README.md`.
- **Evidence and reproduction:** the four files are named `…-001` / `…-004` and carry `artifact_id`
  `XPLAN-006` / `XREPORT-006` / `XPLAN-010` / `XREPORT-010`. Everything referring to them is internally
  consistent: XP-B-001's `routed_to` cites `XPLAN-010@1`/`XREPORT-010@1`, and
  `good/claims/disposition-claim.json` cites `XPLAN-006@1`.
- **Demonstrated impact:** a reader matching a case's `files` list to a `routed_to` reference has to
  translate between two numbering schemes. No assertion and no behaviour depends on it.
- **Bounded desired behaviour:** either align the two, or add one sentence to `evals/fixtures/README.md`
  saying the filenames are stable fixture slots while the `artifact_id` values are realistic project
  allocations, and that references use the `artifact_id`.
- **Behaviour to preserve:** if filenames change, every `files` entry in `evals/evals.json` and
  `evals/cases.jsonl` and every `args.file` / `args.path` in an assertion must be updated in the same change,
  and the XP-C-002 / XP-C-006 sentinel digests must still resolve. The lower-risk option is the README
  sentence.
- **Acceptance condition:** a reader can move between a filename and an artifact ID without inferring the
  mapping.
- **Affected reruns:** XP-C-001, XP-C-003, XP-B-001 if filenames change; none if the README sentence is taken.

## Implementation order

CHG-002, CHG-003, CHG-004, CHG-005 and CHG-006 are independent of one another and of CHG-001.

CHG-001 should follow CHG-005, because the package-observing cases need a `--candidate` root that differs from
the fixture root, and CHG-005 is where that distinction gets written down. CHG-004 is worth settling with the
coordinator before CHG-001, since the runner revision the new cases will be validated against is the one
CHG-004 pins.

Nothing here depends on any tier being run.

## Evaluation prerequisites, not defects

None of the following authorises a target edit, and editing the candidate will not produce any of them.

- **Skill-package structural inspection (S001–S013) and evidence reduction are not implemented in the
  DevForge CLI.** Owner: DevForge integration owner. Blocked claim: that a structural gate ran. Every
  structural row in the report is `INSPECTION_MANUAL`, `authority: none`.
- **Protected-manifest custody for the evaluation runner is not implemented in the DevForge CLI.** Owner:
  DevForge integration owner. Blocked claim: that the runner, grader, runtime and case identities were bound
  rather than self-reported.
- **No installed or exported copy of the candidate was allocated.** Owner: coordinator / DevForge integration
  owner. Blocks tier C entirely, the installed-mode `evals/` absence observation, and the installed-identity
  half of every structural row. This is why CHG-001's installed-mode case can be *authored* now but not
  *observed* now.
- **No fresh terminal and no permitted isolated workspace were allocated.** Owner: coordinator. Blocks tiers
  A and B.
- **The `--candidate` convention is also undocumented in the `devforge-evaluate-expert` package.** Owner: that
  package's owner. Reported, not edited around.
- **Four DevForge CLI integrations this workflow would need do not exist** — a sub-project experiment fence, a
  pre-execution plan freeze, a promotion check, and threshold immutability. Owner: DevForge integration owner.
  The candidate records all four correctly as open requirements in `references/framework-context.md` and
  implements none of them, which is the right behaviour; they are listed here so nobody mistakes them for
  work this specification asks the author to do.

## Closure rules

- **Applied** means the source was edited. It does not close a finding.
- A changed candidate is a new identity and needs new matching evidence before any finding is closed.
- Preserve the original failure history. Do not overwrite the `FAIL` rows in `validation-results.json` or the
  findings in `findings.json`; a later evaluation adds a new record.
- Never weaken an accepted expectation, delete a case or change a sibling gate to convert a recorded
  observation into a pass. A defect in a shared contract or a sibling package goes to its owner.
- Tiers C, B and A stay `NOT_RUN` and behaviour stays `NOT_EVALUATED` until someone actually observes them.
  Applying every change above changes none of those labels.

**Validation status:** Not performed by this document.
**Finding status:** six findings recorded; reevaluation required after any change.
