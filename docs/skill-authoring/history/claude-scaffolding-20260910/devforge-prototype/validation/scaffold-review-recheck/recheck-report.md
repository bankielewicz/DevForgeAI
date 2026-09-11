---
schema_version: "devforge.artifact/v1"
artifact_id: "EVREPORT-004-SCAFFOLD-02"
artifact_type: "expert-evaluation-report"
project_id: "DevForgeAI"
revision: 1
status: draft
created_at_utc: "2026-09-10T21:54:50Z"
producer:
  skill: "devforge-evaluate-expert"
  skill_revision: "bdf665c7e18061395c0762de7a377fdc5f6ed48d66245df5623c5c32b90cf2ac"
  skill_revision_note: "sha256 of the one SKILL.md file source-loaded from commit e641797eebf04cd1e8eb9f711549e038e7745407. Unchanged from the first pass."
execution_ref: null
supersedes:
  artifact_id: "EVREPORT-004-SCAFFOLD-01"
  revision: 1
  store: "project"
  path: "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-prototype/validation/scaffold-review/verification-results.md"
  sha256: "2939cfc197b8f47abd61158b7b8e7ce390f578203e4b60bc2014215f6001d309"
  note: "The prior report's bytes are retained unmodified at that path and were committed at d12edbb. This record supersedes its disposition only. Its FAIL rows and its findings are history and are not rewritten."
upstream:
  - artifact: "SKILL-004"
    revision: 2
    store: "project"
    path: "/home/bryan/Projects/DevForge/framework/DevForgeAI/docs/mvp/specifications/skill-004-devforge-prototype.md"
    sha256: "e4f61c35220641f053a828615df1bc3415c707fde26fcf8b0cdece6cdb1ba54c"
  - artifact: "devforge-prototype candidate package"
    revision: "a80d39e75b9b5fa89826a544b4527feefc215813"
    store: "worktree /home/bryan/Projects/DevForge/worktrees/claude-scaffold-prototype-20260910"
    path: "providers/claude/plugins/devforgeai/skills/devforge-prototype/"
    manifest: "candidate-manifest-a80d39e.txt"
    sha256: "639e1c04dfb3baac4d00343b71dcd5cf7ef935eae98c440ffea472779aebdb19"
  - artifact: "CHGSPEC-004-SCAFFOLD-01"
    store: "project"
    path: "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-prototype/validation/scaffold-review/skill-enhancement-spec.md"
    sha256: "1e076a070b129a1cd9f0e3e542adf3989817113723d6d5dc85cd41c974def294"
evidence:
  - path: "runner-out/fixtures.observations.jsonl"
    sha256: "ab0140ca87d5599a4cdffd04f8f8d75e0b86f924f51c7df018c98c7b7c2c2439"
  - path: "runner-out/package.observations.jsonl"
    sha256: "f552fcc56c412e295aec864040d45b26ca18c3016d79ef38b4c2ec41413d8dc8"
  - path: "runner-out/installed-mode-against-source.observations.jsonl"
    sha256: "0801b57f3d7cd2b729058d04134ee1f2f08cece5e559f3b0d75c517f307683f8"
  - path: "candidate-manifest-a80d39e.txt"
    sha256: "639e1c04dfb3baac4d00343b71dcd5cf7ef935eae98c440ffea472779aebdb19"
  - path: "commands.log"
    sha256: "0420f8cd6d5c89efa8eaf2b8923038c15c8b416751663c7f1b39db85e5487b2f"
decision_ref: null
missing_inputs:
  - "An installed or exported copy of the candidate. Still not allocated; tier C stays NOT_RUN and XP-PKG-005 stays unobservable."
  - "A fresh terminal and a permitted isolated workspace. Still not allocated; tiers B and A stay NOT_RUN."
  - "A session record for this evaluation. execution_ref is null; its absence establishes no ownership."
---

# Focused re-evaluation — devforge-prototype repair pass 1

**Scope, as authorized:** recheck only F-001..F-006 and rubric criterion R08 against the new revision.
Unchanged broad checks were **not** rerun; their first-pass results stand at
`../scaffold-review/` and are cited rather than recomputed. This is a focused recheck, not a second full
evaluation.

## Identity

- **New candidate:** `a80d39e75b9b5fa89826a544b4527feefc215813` (HEAD), preceded by `d12edbb`, which committed
  the first-pass review directory. Worktree clean before this fence was created.
- **Prior candidate:** `e199230858d871926fff2d55de8b015fa0ce335e`. Retained; not modified.
- **Package manifest at `a80d39e`:** 31 files, `candidate-manifest-a80d39e.txt`
  (`639e1c04dfb3baac4d00343b71dcd5cf7ef935eae98c440ffea472779aebdb19`). File count unchanged — the repair
  edited six files and added none.
- **Validator:** unchanged. `devforge-evaluate-expert` at `e641797`, source-loaded, never installed; runner
  `95ca2abf…`, graders `1b7a27a3…`, re-verified against the frozen commit. Still a draft under bootstrap
  review (E2: *revise* at `e52ac59` → repaired `e101e76` → rechecked `6916b60`, MINOR F-R01 open) and still
  unqualified.
- **Author change record (untrusted, informational):** `authoring/authoring-notes.md` "Repair pass 1",
  `authoring/file-manifest.json`, `authoring/handoff.md` revision 2, and a new `repair_pass_1` block in the
  package's own `references/derivation.json`. Every claim in them was verified against bytes before being
  credited; none was adopted.

### Changed files and their digests at `a80d39e`

| File | sha256 at `a80d39e` | Finding it serves |
| --- | --- | --- |
| `SKILL.md` | `127ded6c18429e87de34fec216f0d6389c4d3bd5dfb6db4b316507de40a3085d` | F-003 |
| `references/experiment-boundaries.md` | `7c0163534f27ae31f3dc6a9294637579025173353d08a957f8ab4934396867a0` | F-003 |
| `evals/cases.jsonl` | `f71168da5718d7ac12f823df9c3dd407575ce325c8a43eba650addc33e1e5d8b` | F-001, F-005 |
| `evals/evals.json` | `e364ec174524a06634c1ff634812d8e5bbca4a6f4d9c26bc4f9e933f6dc6d1e6` | F-002, F-004, F-005 |
| `evals/fixtures/README.md` | `8b9e8ba432d10a8e0439b9af5699e08bead70eb83400f30fc54077912774e650` | F-005, F-006 |
| `references/derivation.json` | `ad6f43b1411ffe041a60d247a9c9ac7300bc98cfd7d5cb1761e8b64132a85dfb` | provenance for all six |

## Preserved behaviour — no regression found

The enhancement spec listed what must not change. Every item was checked by byte-identity against `e199230`:

| Preserved item | Result |
| --- | --- |
| `assets/experiment-plan.md`, `assets/prototype-report.md`, `assets/handoff.md` | **UNCHANGED**, all three |
| `references/framework-context.md` (including line 33, the sentence the F-003 fix had to agree with) | **UNCHANGED** |
| `references/recording-rules.md` (including the already-correct line 60) | **UNCHANGED** |
| `references/sources.md` | **UNCHANGED** |
| `evals/triggers/trigger-queries.json` — the fixed, stratified 22-query split | **UNCHANGED** |
| All 19 files under `evals/fixtures/` except `README.md` | **UNCHANGED**, 0 of 19 differ |
| XP-C-006's sentinel binding | still `f9138601783d24d2a3dd8170db7b510c557ec22d906b76afc7707aa5be8e223f` on both the live good-fixture source and the preserved baseline |
| `SKILL.md` beyond the one repaired sentence | **1 insertion, 1 deletion** total — line 50 only |
| Frontmatter field set and description budget | still `name` + `description` only; description line still 1,143 bytes, inside the 1,536-character budget |
| The nine pre-existing deterministic cases | `candidate_subpath`, assertions and expectations intact; **all nine rows reproduce identically** (below) |
| `references/derivation.json` destination digests | **11 of 11** match the new bytes; provenance re-derived rather than left stale |

## Runner observations

Three invocations, all `/usr/bin/python3 -B`, all `--out` inside this fence, all exit 0 — which describes the
program, never the candidate. `cases.jsonl` now opens with `//` comment lines; the runner skips those, and the
file loaded cleanly at 14 cases.

### The two documented invocations

**Run 1 — fixture-backed root** (`--candidate <pkg>/evals/fixtures --mode source`):

| Case | tier | status | assertions |
| --- | --- | --- | --- |
| XP-C-001 | B | COMPLETED | A1 MATCH, A2 MATCH, A3 MATCH |
| XP-C-002 | B | COMPLETED | A1 MATCH |
| XP-C-003 | B | COMPLETED | A1 MATCH |
| XP-A-001 | B | COMPLETED | A1 MATCH |
| XP-C-004 | B | COMPLETED | A1 MISMATCH *(defect fixture, as authored)* |
| XP-C-005 | B | COMPLETED | A1 MISMATCH *(defect fixture, as authored)* |
| XP-C-006 | B | COMPLETED | A1 MISMATCH *(defect fixture)*, A2 MATCH |
| XP-A-002 | B | COULD_NOT_RUN | A1 INDETERMINATE *(truncated transcript, as authored)* |
| XP-B-001 | B | COMPLETED | A1 MATCH, A2 INDETERMINATE *(routed to review, as authored)* |
| XP-PKG-001 | C | COMPLETED | 3 × MISMATCH — wrong root for this group |
| XP-PKG-002 | C | COMPLETED | 5 × MISMATCH — wrong root |
| XP-PKG-003 | C | COMPLETED | 8 × MISMATCH — wrong root |
| XP-PKG-004 | C | COMPLETED | **2 × MATCH** — wrong root, but the absence assertions pass vacuously. See **F-007** |
| XP-PKG-005 | C | COMPLETED | 4 × INDETERMINATE, reason `the case declares mode 'installed' and this run used 'source'` |

**Run 2 — package root** (`--candidate <pkg> --mode source`):

| Case | tier | status | assertions |
| --- | --- | --- | --- |
| XP-C-001 … XP-B-001 (all nine fixture-backed) | B | COULD_NOT_RUN | `candidate_subpath … does not resolve` — by design, and now documented |
| XP-PKG-001 | C | COMPLETED | A1 MATCH (frontmatter present), A2 MATCH (`name`,`description` populated), A3 MATCH (`name='devforge-prototype' folder='devforge-prototype'`) |
| XP-PKG-002 | C | COMPLETED | 5 × MATCH — every local link in `SKILL.md` and all four references resolves in-package |
| XP-PKG-003 | C | COMPLETED | 8 × MATCH — three assets, three references and both maintenance records present |
| XP-PKG-004 | C | COMPLETED | 2 × MATCH — no `scripts/`, no `agents/` |
| XP-PKG-005 | C | COMPLETED | 4 × INDETERMINATE (mode mismatch) — the honest result with no installed copy |

### Run 3 — deliberate misuse probe for XP-PKG-005

No installed copy exists, so `--mode installed` was run against the **authoring source** with
`--case-id XP-PKG-005` (13 rows correctly `SKIPPED`, so a partial run cannot be misread as full coverage):

```
XP-PKG-005 COMPLETED
  A1 path_absent    => MISMATCH  "evals is present but the case required it to be absent"
  A2 path_present   => MATCH     assets/handoff.md exists
  A3 path_present   => MATCH     references/recording-rules.md exists
  A4 frontmatter_fields => MATCH every required field is a populated scalar
```

This establishes that **XP-PKG-005 discriminates** — it is not an assertion that can only ever return
`INDETERMINATE`, and it would catch an installed copy that shipped its eval tree. It establishes **nothing
about tier C**: the authoring source is not an installed copy, and the `MISMATCH` here is the probe working,
not a defect. Tier C remains `NOT_RUN`.

### Regression: the nine prior rows

Field-level comparison against the first pass's
`../scaffold-review/runner-out/candidate-cases.observations.jsonl`, over `execution_status`, `result`,
`observed` **and** `reason`:

> **All nine prior rows reproduce identically. 9 of 9, no drift in any field.**

The repair added coverage without disturbing a single existing observation.

## Per-finding closure

### F-001 — MINOR — **CLOSED**

*Was:* every case set `candidate_subpath` into `evals/fixtures/`, so none observed the package or an installed
copy; the four `tier: "C"` cases covered only the outputs half of the contract's tier C, and the `tier: "A"`
cases observed synthetic transcripts.

*Verified at the diff:* `evals/cases.jsonl` adds **XP-PKG-001..005**, which omit `candidate_subpath` and read
`--candidate` directly — frontmatter presence and fields, `name_folder_relation` with `expect_equal` (its
`expectations` states equality is asserted *as the DevForgeAI convention*, since Claude's own naming rules make
a difference legitimate), `package_relative_links` on `SKILL.md` and all four references, presence of the six
routed resources plus both maintenance records, absence of `scripts/` and `agents/`, and **XP-PKG-005 with
`"mode": "installed"`** asserting `evals` absent while `assets/` and `references/` ship. That last case is the
"templates and references resolve inside the installed package" half that was missing.

The eight simulated-tier cases are relabelled `tier: "B"`, and **every** case gained a `notes` field stating
what its tier refers to and that the case_id letter is historical. `evals.json`'s `tier_note` was rewritten to
describe the two groups.

*Observed:* Run 2 — XP-PKG-001..004 complete with 18 of 18 assertions MATCH against the package root;
XP-PKG-005 INDETERMINATE on mode, as its own notes predict. Run 3 shows XP-PKG-005 discriminating.

*Regression:* none. Nine prior rows identical.

*A counting caution for whoever reads the tier fields next:* `cases.jsonl` now holds nine `tier: "B"` cases
and five `tier: "C"` cases, and `evals.json` separately holds eleven `tier: "B"` cases. **These are two
different kinds of B and must not be added together into "twenty tier-B cases."** The nine in `cases.jsonl`
are deterministic observations of synthetic artifacts and transcripts; the eleven in `evals.json` are
behavioural output-quality cases needing a session. Each file's `notes` and `tier_note` say so. Note also that
**no case in `cases.jsonl` is tier A**, which is correct — the file states that tier A needs a fresh terminal
and lives in `evals/triggers/trigger-queries.json`.

**Residual, recorded not charged:** XP-PKG-005 cannot be *observed* until an installed or exported copy exists.
That is prerequisite PREREQ-003, owned by the coordinator / integration owner — it is not a defect in the
candidate, and authoring the case now was the correct move.

### F-002 — MAJOR — **CLOSED**

*Was:* `evals.json` case 8 declared `baseline_comparison: "old_skill"` when no previous revision of this skill
exists at base `c17e758`.

*Verified at the diff:* `"baseline_comparison": "without_skill"`, matching the other ten cases. A new
`fixture_note` states the distinction precisely — the fixture is a prior *report artifact* supplied **to** the
case, an input, not a baseline arm — which is exactly the conflation the finding identified. The
`NOT_APPLICABLE` fallback previously proposed in the authoring notes is explicitly **withdrawn**, on the
correct ground that the word is reserved for a stated scope exclusion and an absent baseline is not one. The
package's `spec-mapping.md` / `evals.json` contradiction is gone.

*Regression:* the case's `prompt`, `files`, `expected_output` and all five `graded_observations` are
byte-unchanged. Every one of the eleven tier-B cases now declares a baseline arm that resolves.

This was the finding driving the `revise`. It is resolved by bytes, and its fix corrects the reasoning, not
just the token.

### F-003 — MINOR (R08) — **CLOSED**

*Was:* `SKILL.md:50` claimed a self-computed hash lets a later reader tell the plan preceded the evidence —
contradicting `references/framework-context.md:33` — and routed the reader for the limitation to
`references/experiment-boundaries.md`, which contained no such statement.

*Verified at the diff:*

- `SKILL.md:50` now reads, in the operative part: *"A hash you computed yourself records which bytes you had;
  whether anything outside your own reach holds it is a separate fact, and one no current DevForge command
  supplies."* The ordering claim is gone. It links `recording-rules.md` for the field that distinguishes the
  two cases, and `experiment-boundaries.md` for why ordering still matters when nothing external attests.
- `references/experiment-boundaries.md:21` is new and carries the limit explicitly, including *"It does not
  establish to anyone else that those bytes preceded the evidence, because nothing stopped you computing it
  afterwards"*, and routes to the open integration requirement in `framework-context.md`. The dead pointer is
  no longer dead.
- Both link targets resolve in-package.

*Independent check:* `grep -rno "preceded the evidence"` over the package returns **four** literal
occurrences, verified by extraction rather than by eye:

| Location | What it is |
| --- | --- |
| `references/experiment-boundaries.md:21` | prose — **denies** the claim |
| `references/framework-context.md:33` | prose — **denies** the claim |
| `references/derivation.json:686` | the repair record's `verified` field, quoting the *old* SKILL.md text as history |
| `references/derivation.json:689` | the repair record's `acceptance_check` field, quoting its own grep *pattern* |

The two substantive prose occurrences both deny the claim, and no sentence anywhere now asserts it. The
paragraph also gets the balance right: it keeps the freeze instruction and says why a self-recorded freeze is
still worth doing, rather than over-correcting into "freezing is pointless".

*Regression:* `framework-context.md` and `recording-rules.md` byte-unchanged; `SKILL.md` changed by exactly one
line.

**R08 recheck: `PASS`.** No material contradiction remains, and the routes lead to text that addresses what
they promise. (Only R08 was rechecked, as authorized. R01–R07, R09 and R10 stand from the first pass at
`../scaffold-review/ai-review.json`; the six changed files touch none of the evidence those criteria cited,
except that the F-003 fix strengthens R08's own subject matter.)

### F-004 — MINOR — **CLOSED**

*Was:* `runner_dependency.commit` pinned `e52ac59`, a revision a bootstrap review found defective and that had
since been repaired twice.

*Verified at the diff:* the pin is now `e641797eebf04cd1e8eb9f711549e038e7745407`. A `scripts_sha256` block
declares `run_cases.py` `95ca2abf…` and `graders.py` `1b7a27a3…` — **both re-hashed here against the actual
frozen validator files and equal**, so the repin is verifiable rather than asserted, which is what the change
asked for. A `superseded_pin` field preserves the old value with the full review chain
(`b6a4bf7` → `e101e76` → `6916b60` → `e641797`) and notes that both scripts changed across the range. The
`status` sentence now carries the real condition including the open MINOR F-R01, and — correctly — tells the
reader to *confirm the revision the next evaluation will actually be given rather than assuming this pin,
because that package is still moving*. That was the open coordinator decision, and the record now defers to it
instead of hard-asserting a future.

*Regression:* `runner_dependency.boundary` — the sentence forbidding a runner row from being copied into a
results record — is byte-unchanged, as required.

### F-005 — MINOR — **CLOSED**

*Was:* the `--candidate` root the cases require was recorded nowhere, and the natural wrong value produced nine
`COULD_NOT_RUN` rows at exit 0.

*Verified at the diff:* documented in **three** places, each aimed at a different reader —
`evals.json` gains `runner_dependency.invocation` with full commands for the fixture-backed, package-observing
and installed-only groups plus a `why_this_matters` paragraph naming the silent-failure mode and the `--out`
constraints; `evals/fixtures/README.md` gains a "Running the cases against these fixtures" section with the
exact command and the same warning; and `cases.jsonl` opens with a comment header stating the two roots and
*"Check the execution_status of every row before reading a run as coverage."* The sibling gap is carried
forward honestly under `sibling_gap_reported_not_fixed` rather than being edited around.

*Observed:* both documented invocations were run exactly as written and behaved exactly as documented — Run 1
and Run 2 above.

### F-006 — ADVISORY — **CLOSED**

*Was:* fixture filenames and their internal `artifact_id` values use different numbers.

*Verified at the diff:* the author took the lower-risk option the spec offered — a "Fixture filenames versus
artifact IDs" section in `evals/fixtures/README.md` with a four-row mapping table and the rule that references
use `artifact_id` while case `files` and assertion `args` use paths, plus the rationale (stable fixture slots).
No fixture was renamed, so no `files` entry or assertion argument had to move and the sentinel bindings are
untouched — which is what made this the safer of the two options.

### F-007 — ADVISORY — **NEW**

**The wrong-root guidance is wrong for one of the five package-observing cases.**

`evals.json` `runner_dependency.invocation.fixture_backed.note` says: *"Under this root the XP-PKG-\* cases
correctly MISMATCH, because the fixtures root has no SKILL.md."* `evals/fixtures/README.md` says the same.

Observed under the fixtures root (Run 1): XP-PKG-001, -002 and -003 do MISMATCH; **XP-PKG-004 reports
`COMPLETED` with 2 × MATCH**, because its assertions are `path_absent` on `scripts` and `agents`, which are
trivially absent from the fixtures root too; and XP-PKG-005 is INDETERMINATE, not MISMATCH. So the guidance is
accurate for three of five cases and wrong for two.

*Demonstrated impact:* narrow but real, and it is the same class of hazard the rest of the file works hard to
close. The file's own advice — *"check the `execution_status` of every row"* — does not catch this one, because
XP-PKG-004's status under the wrong root is `COMPLETED`, not `COULD_NOT_RUN`. A reader who ran only the
fixtures invocation could count XP-PKG-004 as passing coverage of the no-`scripts/` policy check when it
observed the wrong tree entirely. An absence assertion passes vacuously anywhere the thing is absent.

*Smallest repair:* one clause. Amend both notes to something like: *"XP-PKG-001..003 mismatch here because
there is no `SKILL.md`; XP-PKG-004's absence assertions pass vacuously against any tree and prove nothing under
this root; XP-PKG-005 is INDETERMINATE on mode. None of the five is coverage under this root."* Optionally add
a `path_present` anchor assertion (for example on `SKILL.md`) to XP-PKG-004 so the case cannot complete against
a tree that is not the package.

*Not a regression:* this text did not exist before the repair; it arrived with the F-005 fix. It is a new,
lower-severity defect in new material, correctly caught by rerunning the documented invocation rather than
assuming it.

## The author's decision not to author EV-S-007 — I agree

My first-pass evaluator case **EV-S-007** asserted `required_report_fields` against
`assets/experiment-plan.md` and `assets/prototype-report.md` and observed `MISMATCH placeholder`. The author
declined to carry it into the package, arguing in `XP-PKG-003`'s `notes` and in `derivation.json`'s
`not_copied` field that unfilled templates *correctly* hold placeholders, so authoring that assertion would
record a healthy package as defective; `XP-PKG-003` asserts the templates are **present** instead, and
placeholder detection stays on a produced artifact where `XP-C-004` already covers it.

**I agree, and I think the author is right on a point my own case got wrong.** EV-S-007 was an evaluator-side
probe with its expected result declared in prose — I recorded the `MISMATCH` as the *expected* observation
confirming the shipped asset had not been pre-filled. That reasoning is defensible for a one-off probe I
interpret myself. It is a poor thing to ship in a durable case file: the runner emits no expected-vs-observed
comparison, so a standing assertion whose healthy-package result is `MISMATCH` inverts the file's own reading
convention and would train a later reader to skim past mismatches. Separating "the template is present"
(package check) from "a produced report has no placeholders" (artifact check) is the cleaner split, and it is
the one the contract's own distinction between package and outputs implies.

**Residual gap, recorded as an observation and not charged as a finding:** nothing now detects an
`assets/` template that was accidentally shipped *pre-filled* — the exact inverse defect. It is narrow: the
templates are byte-identical to the governing `docs/mvp` sources, `derivation.json` records those digests, and
this recheck verified all 11 destination digests, so drift would be caught by the provenance record rather than
by a case. If the author ever wants a case for it, the right shape is a digest-equality assertion against the
recorded derivation digest, not a placeholder assertion. No change requested.

## Disposition

| | First pass (`e199230`) | This recheck (`a80d39e`) |
| --- | --- | --- |
| Disposition | `revise` | **`insufficient evidence`** |
| BLOCKER | 0 | 0 |
| MAJOR | 1 (F-002) | **0** |
| MINOR | 4 (F-001, F-003, F-004, F-005) | **0** |
| ADVISORY | 1 (F-006) | **1 (F-007, new)** |
| Structure group | FAIL | **PASS** |
| `ai_review` R08 | FAIL | **PASS** |
| Tiers C / B / A | NOT_RUN | NOT_RUN |
| Behaviour | NOT_EVALUATED | NOT_EVALUATED |

**Updated disposition: `insufficient evidence`.**

Adjudicated by hand against the validator's results contract, because evidence reduction is still not
implemented in the DevForge CLI and no decision receipt exists. The rule applied: *any applicable `FAIL` gives
revise; otherwise a missing required observation gives insufficient evidence; every required observation
passing supports only suitable for the stated scope.*

- No applicable `FAIL` remains — both first-pass FAILs are closed by bytes, so `revise` no longer holds.
- `suitable for the stated scope` is **not** reachable: tiers C, B and A are all still `NOT_RUN` for want of an
  installed copy, a fresh terminal and an isolated workspace. That is a missing required observation.
- F-007 is `ADVISORY` and by the contract's own definition does not by itself fail an accepted requirement, so
  it does not restore `revise`. It is a real defect that should be fixed, and it is not a blocker on anything.

**This is the ceiling static evidence can reach.** The movement from `revise` to `insufficient evidence` is the
whole distance the repair could travel; the remaining gap is not the author's to close. Behavioural status stays
`NOT_EVALUATED`, and nothing here observes a session finding, loading or following this skill.

## Missing capabilities and prerequisites — unchanged

Both statements are recorded again, whatever the observations turned out to be.

> **Skill-package structural inspection (S001–S013) and evidence reduction are not implemented in the DevForge CLI.**

> **Protected-manifest custody for the evaluation runner — binding the selected runner and grader files, the Python and dependency selection, the case inputs and the grading criteria outside evaluated-agent write access, and verifying those identities before acceptance criteria are applied — is not implemented in the DevForge CLI.**

Every structural row in this recheck is `method: INSPECTION_MANUAL`, `authority: none`. The runner, grader and
case identities are self-reported by the run; this evaluation re-hashed the two scripts against the frozen
commit, which is stronger than the header alone and is still not protected-manifest custody. Both are
evaluation prerequisites owned by the DevForge integration owner and neither is a defect in this candidate.

Still outstanding, unchanged and not the author's to resolve: no installed or exported copy (PREREQ-003 — blocks
tier C and XP-PKG-005), no fresh terminal or isolated workspace (PREREQ-004 — blocks tiers A and B), no session
record (PREREQ-005).

## Limits of this recheck

1. **Focused scope by instruction.** Only F-001..F-006 and R08 were rechecked. R01–R07, R09 and R10, the
   requirement-coverage table, the trigger-split analysis, the provider-correctness checks and the CLI-help
   verification stand from the first pass; the six changed files touch none of the evidence those cited, and
   `trigger-queries.json` and the four unchanged references are byte-identical.
2. **Reading is still not running.** Every closure above is a statement about bytes and about deterministic
   observations of bytes. None of it establishes that a Claude session will find, load or follow this skill.
3. **The runner evidence is local and non-isolated**, with self-reported identities, and its
   `MATCH`/`MISMATCH`/`INDETERMINATE` vocabulary was again kept out of every outcome column.
4. **Independence is weaker than the first pass.** This recheck ran in the same context that produced the
   original findings, so I am checking my own prior conclusions. I mitigated by re-verifying each finding
   against the diff at the cited file and line rather than against my own summary of it, and by rerunning the
   documented invocations rather than trusting the author's recorded results — which is how F-007 surfaced.
   The exposure is real and is not `COULD_NOT_RUN`-worthy; it is a limit on the weight of these closures.
5. **The author's records were read as untrusted evidence.** `derivation.json`'s `repair_pass_1` block,
   `authoring-notes.md` and `handoff.md` were used to locate claims and were then checked against bytes. One
   miscount was noticed and not charged: the repair record's `acceptance_check` states that a grep for
   "preceded the evidence" returns "exactly two occurrences", and the literal count is four (table above).
   The claim is **self-referentially wrong** — writing it introduced a third occurrence, and the `verified`
   field beside it a fourth, so the sentence falsified its own count at the moment it was written. Its
   substance is correct and is what matters: exactly two *prose* occurrences remain and both deny the claim.
   Recorded because a reader who runs the grep will see four and should not mistake that for an unresolved
   contradiction. Not charged as a finding — it is a self-check in a provenance record, not an instruction to
   a session, and the underlying repair is sound.
6. **The validator remains unqualified** and its own MINOR F-R01 is still open.
7. **No repair was applied by this evaluator.** The candidate was not edited, `../scaffold-review/` was not
   modified, and nothing was committed.

## Recovery and continuation

- **Last completed phase:** focused recheck complete; results and findings written.
- **Frozen inputs still matching:** candidate `a80d39e` (31-file manifest above), specification `e4f61c35…`,
  validator worktree clean at `e641797` with both scripts at their recorded digests.
- **Owned processes and workspace:** none. No background process, no workspace allocation, no worktree created,
  switched, reset or released.
- **Next owner:** the coordinator, for the two decisions below. The scaffold's author has one optional
  ADVISORY (F-007) and no required repair.
- **Conditions invalidating this report:** any change to the candidate's 31-file manifest at `a80d39e`, to the
  specification, to the frozen validator or its two scripts, or the appearance of an installed or exported
  copy — which would make tiers C, B and A observable and would supersede their `NOT_RUN` rows rather than
  confirming them.
