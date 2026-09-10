---
schema_version: "devforge.artifact/v1"
artifact_id: "CHGSPEC-002"
artifact_type: "skill-enhancement-spec"
project_id: "devforgeai-claude-scaffolding-20260910"
revision: 1
status: draft
created_at_utc: "2026-09-10T21:16:13Z"
producer:
  skill: "devforge-evaluate-expert"
  skill_revision: "bdf665c7e18061395c0762de7a377fdc5f6ed48d66245df5623c5c32b90cf2ac (SHA-256 of the SKILL.md file bytes at commit e641797eebf04cd1e8eb9f711549e038e7745407; source-loaded, never installed, never invoked)"
execution_ref: null
upstream:
  - artifact_id: "SKILL-002"
    revision: 2
    store: project
    path: "docs/mvp/specifications/skill-002-devforge-define-product.md"
    sha256: "3e48f93f200499083a062e200f71ad4a3659fad098ef6658fb4b4a34bea6ddbf"
    sections:
      - "Workflow and phase exits"
      - "Validation and behavioral acceptance"
      - "Rework, stopping, and recovery"
      - "User goal and use-case inventory"
evidence:
  - kind: evaluation-report
    path: "verification-results.md"
  - kind: findings
    path: "findings.json"
  - kind: runner-observations
    path: "runner-out/observations-author-cases-source.jsonl"
  - kind: runner-observations
    path: "runner-out/observations-evaluator-cases-source.jsonl"
supersedes: null
decision_ref: null
missing_inputs:
  - "No installed copy of the candidate, so no tier C, B or A observation exists to motivate or to bound any change below. Every CHG here rests on source reading and on non-authoritative runner rows."
---

# Skill repair and enhancement specification - devforge-define-product

The bounded, evidence-backed change request returned for this scaffold. It authorises no automatic
edit, invocation, installation, acceptance or release, and it carries forward the existing user
authorisation without expanding it.

Each change below names the finding it closes, the exact target, the evidence, the bounded desired
behaviour, the behaviour to preserve and the reruns. Nothing here is a fabricated patch: where the
cause is a judgement rather than a demonstrated fault, the change is written as an option with its
cost stated.

## Immutable intake

- **Evaluated candidate:** worktree
  `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-define-product-20260910`, commit
  `05ed112a5a46495041651183493e28c4eae00fed`, package
  `providers/claude/plugins/devforgeai/skills/devforge-define-product/`.
  `SKILL.md` sha256 `c93065fc82750ed9df1ad8bdfd8d34b1005af03e49879b13b2f0442800c0083f`.
  The complete 20-file manifest is in `verification-results.md`.
- **Installed copy evaluated:** none. Not installed, not exported, no consuming project.
- **Specification:** `docs/mvp/specifications/skill-002-devforge-define-product.md`, revision 2,
  sha256 `3e48f93f200499083a062e200f71ad4a3659fad098ef6658fb4b4a34bea6ddbf`.
- **Evaluation report:** `verification-results.md` in this directory (EVREPORT-002).
- **Results record:** `findings.json` in this directory. No separate `validation-results.json` was
  produced; the coordinator packet folds the per-check outcomes into `verification-results.md` and
  `findings.json`.
- **Independent review:** performed by this evaluator as a separately dispatched context. Its
  per-criterion records are the R01-R10 table in `verification-results.md`; no separate
  `ai-review.json` was produced, by the same packet direction. Independence limits are recorded
  there and in `findings.json`.
- **Cases and fixtures:** the candidate's own `evals/` at the digests in the report's manifest,
  plus `runner-out/evaluator-added-cases.jsonl` in this directory.
- **Prior iteration:** none. This is the first evaluation of the first revision of this package.
- **Runner and graders:** `scripts/run_cases.py` sha256
  `95ca2abf77a5baf249694ad37d67a74949b567acd5164fd309724cbc576583e2` and `scripts/graders.py`
  sha256 `1b7a27a37e1fb8b2e36b1822bc23227c69e6300243e1b49b8caa848e3feca69f`, source-loaded from
  `devforge-evaluate-expert` at `e641797eebf04cd1e8eb9f711549e038e7745407`. Both identities are
  self-reported by the run; no protected manifest bound them.

Preserve these identities exactly. Verify them before editing and retain the old candidate.

## Change decision

- **Are target changes justified by the evidence?** **Yes**, for CHG-001 through CHG-010.
  One is a required repair (CHG-001, closing a MAJOR requirement omission). Three are required
  repairs of contained defects (CHG-002, CHG-003, CHG-004). Six are authorised enhancements whose
  demonstrated consequence is small (CHG-005 through CHG-010), and a decision to defer any of them
  with the finding left open is legitimate.
- **Next owner:** the scaffold's author for `devforge-define-product`, under coordinator dispatch.
  The validator's own template names `devforge-project-expert-creator` as the standing next owner;
  the coordinator packet governs this assignment and names the scaffold's author instead. Both are
  recorded so neither is silently substituted. This evaluator does not repair what it measured.
- **Behaviour that must be preserved unchanged:** the frontmatter contract of exactly `name` and
  `description` with `name` equal to the folder; the four-phase structure and every existing
  **Exit when** line; the two-roots resolution rule; the prompt-injection boundary; the
  proposal-versus-adoption separation and the `decision_ref` rule; the missing-integration
  statement and the accuracy of every named `devforge` subcommand; the write-then-hash-then-read-back
  digest ordering; the fixed result vocabulary; the absence of `scripts/`, `agents/`, `hooks/` and
  of any `!`-prefixed dynamic-context injection; and the byte-identity of `assets/product-brief.md`
  and `assets/handoff.md` with their `docs/mvp` sources.
- **Forbidden scope changes:** do not edit SKILL-002 or any shared contract or template to
  accommodate a finding - a defect in a shared document goes to its integration owner. Do not
  install, export or run the candidate to close a finding. Do not delete or weaken any eval case,
  fixture or expectation to convert a recorded observation into a pass. Do not add a `scripts/`
  directory, a helper, or any frontmatter field beyond `name` and `description`. Do not restructure
  the four phases or rewrite the package; every change below is local.

## Requested changes

### CHG-001: A session that is interrupted preserves its phase and evidence, and re-verifies identities before resuming

- **Finding IDs:** F-001
- **Severity:** MAJOR
- **Change type:** required repair
- **Accepted requirement, or a new proposal:** accepted requirement. SKILL-002 rev 2, "Workflow and
  phase exits" closing paragraph ("On interruption, preserve the current phase and evidence; resume
  by checking their identities and the session assignment again") and "Rework, stopping, and
  recovery" ("If the worktree or active run changes, re-establish the appropriate baseline and
  evidence before resuming").
- **Affected revision, file and section:** `05ed112a...`;
  `SKILL.md`, section "Stopping" or the bullet list under "When something is missing or a check
  cannot run"; procedural detail into `references/recording-rules.md` beside "Resolving a reference
  before you use it".
- **Evidence and reproduction:** `grep -rn -i -e interrupt -e resume -e resuming -e 'baseline and
  evidence'` over `SKILL.md`, `references/` and `assets/` returns exactly one hit,
  `assets/handoff.md:67 "## Resume and custody"`, which is the shared handoff template's
  receipt-custody heading and not workflow guidance. Both cited `recording-rules.md` sections were
  read in full and carry neither requirement.
- **Demonstrated impact:** a session interrupted mid-brief has no instruction to preserve the
  current phase and the evidence gathered, and none to re-verify the upstream identities and the
  session assignment before continuing. The staleness procedure is reactive and the reference
  readback fires only at completion, so a scope decision taken in phase 3 against pre-interruption
  bytes is never rechecked before it is written into the brief.
- **Bounded desired behaviour:** after the change, `SKILL.md` states that on an interruption the
  session preserves the phase it had reached, the brief as far as it exists, and the evidence
  already recorded; and that on resuming it re-reads and re-hashes the upstream references and
  re-checks the session assignment before continuing, treating a changed identity as the start of a
  new iteration rather than a continuation of this one. `references/recording-rules.md` carries the
  procedure. Add roughly a paragraph in each; do not expand into a new phase or a fifth section.
- **Behaviour to preserve:** the existing four **Exit when** lines; the existing staleness
  procedure under "When the upstream has moved on", which this must reference rather than duplicate;
  the narrowness of the existing stop condition, which blocks dependent requirements and not
  unrelated evidence gathering.
- **Acceptance condition:** a later evaluation greps the same terms and finds the instruction in
  `SKILL.md`, resolves the reference into `references/recording-rules.md`, and confirms the new
  text neither contradicts the existing staleness rule nor widens the stop condition.
- **Affected reruns:** DP-B-006 and DP-B-007 are the natural regressions and neither currently
  observes interruption or resume, so a new graded observation or a new case is needed. Re-run
  DP-C-001 A4 to confirm any new local link still resolves in-package.

### CHG-002: Correct the two spec-mapping rows that claim uncarried coverage

- **Finding IDs:** F-002
- **Severity:** MINOR
- **Change type:** required repair
- **Accepted requirement, or a new proposal:** accepted requirement - the coverage map must reflect
  the bytes it cites.
- **Affected revision, file and section:** `05ed112a...`;
  `docs/skill-authoring/history/claude-scaffolding-20260910/devforge-define-product/authoring/spec-mapping.md`,
  the "Workflow and phase exits" table row for interruption, the "Rework, stopping, and recovery"
  table row for re-establishing a baseline, and the "Coverage summary" list.
  **This target is the authoring evidence tree, not the skill package.**
- **Evidence and reproduction:** the map cites `references/recording-rules.md` "Resolving a
  reference before you use it" and "Ownership and concurrent writers" for both rows. Reading both
  sections in full shows a four-step digest-comparison procedure and a collision-handling section
  respectively; neither mentions interruption, phase preservation, resuming, or re-establishing a
  baseline.
- **Demonstrated impact:** the map is the artifact a dispatcher uses to decide that SKILL-002 needs
  no further work on this row. Recording a requirement as carried when the cited sections do not
  carry it turns F-001 from a visible gap into an invisible one.
- **Bounded desired behaviour:** if CHG-001 is applied first, re-cite both rows at the new section
  and leave the summary intact. If CHG-001 is deferred, change both rows to state the requirement is
  not carried and adjust the coverage summary accordingly.
- **Behaviour to preserve:** every other row of the map, which was spot-checked against bytes and
  found accurate; the map's existing and correct statement that every eval status is NOT_RUN.
- **Acceptance condition:** each of the two rows resolves to a section that actually contains the
  requirement, or states plainly that it is not carried.
- **Affected reruns:** none. This is an evidence document, not a runtime file.

### CHG-003: Declare which fixture digests are resolvable, and anticipate the staleness signal the others create

- **Finding IDs:** F-003
- **Severity:** MINOR
- **Change type:** required repair
- **Accepted requirement, or a new proposal:** accepted requirement. skill-authoring-contract rev 3
  requires reproducible fixtures and cases derived from requirements; the demonstrated problem is a
  grading contradiction, not a style preference.
- **Affected revision, file and section:** `05ed112a...`;
  `evals/fixtures/README.md` digest table and a new note; `evals/evals.json` DP-B-010
  `graded_observations` and DP-B-001 / DP-B-008 notes. Optionally the frontmatter of
  `evals/fixtures/new-product/IDEAS-001.md`, `existing-product/PROD-001.md` and
  `existing-product/CHANGE-011.md`.
- **Evidence and reproduction:** `IDEAS-001.md` `supersedes.sha256` is `0000...0000` pointing at an
  absent `IDEAS-001.r1.md`; `PROD-001.md` carries `1111...1111` and `2222...2222`, the latter
  pointing at an absent `PROD-001.r1.md`; `CHANGE-011.md` carries `3333...3333`. The `stale/`
  fixtures instead carry real, independently verified digests, because resolution is DP-B-007's
  subject.
- **Demonstrated impact:** in DP-B-001 through DP-B-005, DP-B-008 and DP-B-010 the skill's own
  reference-resolution procedure fires against digests that can never match and paths that are not
  staged, so a correct worker emits a staleness or missing-input report that none of those cases
  anticipates. DP-B-010's DELIVERY observation "every reference written resolves after the last
  write" would mark a faithfully carried-forward `PROD-001` upstream as a delivery failure - a false
  FAIL against correct behaviour. The fixtures also model, unlabelled, the shape `SKILL.md`
  explicitly forbids.
- **Bounded desired behaviour:** either (a) add a row to `evals/fixtures/README.md` naming which
  digests are real and which are non-resolvable scaffolding, and add a graded observation to
  DP-B-010 - with a note on DP-B-001 and DP-B-008 - stating that reporting the unresolvable upstream
  is expected behaviour and not a delivery failure; or (b) replace the filler digests with the
  actual sha256 of the staged fixture bytes and stage the referenced files. Option (a) is smaller
  and does not disturb any pinned digest; option (b) removes the condition rather than documenting
  it, at the cost of new fixture files. Pick one; do not do half of each.
- **Behaviour to preserve:** DP-B-007's real digests and its two staging variants, which are correct
  and are the case where resolution is deliberately under test; the fixtures README's existing
  synthetic-data declaration and its source-inventory-versus-worker-visible staging note; the three
  sentinel digests pinned in `cases.jsonl`.
- **Acceptance condition:** a later evaluation reading the fixtures README can tell, for every
  fixture digest, whether it is expected to resolve; and DP-B-010's graded observations no longer
  score a correct staleness report as a delivery failure.
- **Affected reruns:** DP-B-001, DP-B-002, DP-B-003, DP-B-004, DP-B-005, DP-B-008, DP-B-010. If
  option (b) is taken, also re-run DP-B-007 A1 and re-verify every digest recorded in
  `references/derivation.json`.

### CHG-004: Restore independent evidence to the positive validation trigger split

- **Finding IDs:** F-004
- **Severity:** MINOR
- **Change type:** required repair
- **Accepted requirement, or a new proposal:** accepted requirement. skill-authoring-contract rev 3:
  "preserve a fixed train/validation split and fresh final queries".
- **Affected revision, file and section:** `05ed112a...`; `evals/triggers/trigger-queries.json`,
  the `leakage_note` field and the `queries` array.
- **Evidence and reproduction:** P2c, P3c and P3d each paraphrase a description clause - "accepted
  brief ... change request" against "amending the scope of a product that already has an accepted
  brief"; "grown into something we cannot build ... what to cut" against "cut a scope that has grown
  past what they can deliver"; "how would I tell ... whether this thing was worth building" against
  "how they would know it helped". `leakage_note` claims only that no validation query *text*
  appears in `SKILL.md`, and discloses conceptual coupling only for the train-split P2a and P3a.
- **Demonstrated impact:** all three implicit positive validation queries restate situations the
  description enumerates, so a tier-A run over this split would largely measure whether the
  description matches its own examples rather than whether the skill is discovered from a request
  phrased outside them. A high positive rate would overstate discovery.
- **Bounded desired behaviour:** extend `leakage_note` to disclose concept-level coupling, not only
  verbatim text, and name P2c, P3c and P3d as coupled. Add at least two fresh positive validation
  queries describing situations the description does not enumerate - a request that never uses
  "MVP", "scope", "requirements" or "release", for example someone saying the team keeps arguing
  about what goes in the first version and wanting it settled and written down. Keep the split fixed
  once assigned and do not re-randomise it per run.
- **Behaviour to preserve:** the existing negatives, which are genuinely strong near-misses and
  should not be altered; the stratification of one train and one validation entry per negative
  category; the existing and correct rule that `explicit_invocation` entries are never counted as
  implicit activation evidence; the existing and accurate sibling-inventory note.
- **Acceptance condition:** at least two positive validation queries exist whose phrasing maps to no
  enumerated description clause, and `leakage_note` states the coupling of the remaining ones.
- **Affected reruns:** all tier-A positive queries once a terminal is available. No tier-B or tier-C
  case is affected.

### CHG-005: Make DP-C-001 A10 an assertion that can fail, or record why it cannot

- **Finding IDs:** F-005
- **Severity:** ADVISORY
- **Change type:** authorised enhancement
- **Accepted requirement, or a new proposal:** accepted requirement, narrowly - grader assertions
  should observe something.
- **Affected revision, file and section:** `05ed112a...`; `evals/cases.jsonl`, case DP-C-001,
  assertion A10 and `expectations.summary`.
- **Evidence and reproduction:** the runner observed "0 local, 0 external" for
  `references/sources.md`; evaluator case EV-C-101 confirms the other three non-`SKILL.md` Markdown
  files are equally link-free.
- **Demonstrated impact:** contained. The assertion cannot MISMATCH under any edit that does not
  first add a link, so it adds apparent breadth without adding an observation.
- **Bounded desired behaviour:** either drop A10, or keep it as a guard against future edits and say
  so in `expectations.summary` - that `SKILL.md` is currently the only link-bearing file.
- **Behaviour to preserve:** A1 through A9, which are load-bearing and all matched.
- **Acceptance condition:** DP-C-001 contains no assertion whose inability to fail is undocumented.
- **Affected reruns:** DP-C-001.

### CHG-006: Say which list in a case is the worker-visible one

- **Finding IDs:** F-006
- **Severity:** ADVISORY
- **Change type:** authorised enhancement
- **Accepted requirement, or a new proposal:** accepted requirement. skill-authoring-contract rev 3:
  a fixture manifest must distinguish source inventory from files actually visible to a worker.
- **Affected revision, file and section:** `05ed112a...`; `evals/cases.jsonl`, the `notes` field of
  DP-B-007 and DP-B-008.
- **Evidence and reproduction:** DP-B-008 `files[]` includes `existing-product/PROD-001.md`, staged
  by `evals.json` only as the grader-only positive control; DP-B-007 `files[]` includes
  `stale/preserved/IDEAS-002.r1.md`, which `evals.json` says is never visible to the worker in the
  unavailable-bytes variant.
- **Demonstrated impact:** the contract requirement is already met, in `evals.json`
  `fixture_staging` and the fixtures README staging note, and the frozen runner ignores `files[]`
  entirely. The residual risk is a run harness that reads `files[]` as the staging list and leaks an
  operator-only input, silently invalidating DP-B-007's unavailable variant and DP-B-008's control.
- **Bounded desired behaviour:** add one line to each case's `notes` stating that `files[]` is the
  case's source inventory and that `evals.json` `fixture_staging` is authoritative for worker
  visibility. `notes` is already a permitted case key in the runner's schema, so this does not
  change how the file loads.
- **Behaviour to preserve:** the existing `fixture_staging` text and the fixtures README staging
  note, which are correct and are the authority; the two-variant design of DP-B-007.
- **Acceptance condition:** a run harness reading only `cases.jsonl` cannot mistake `files[]` for
  the staging list.
- **Affected reruns:** none deterministic. Confirm the file still loads under the runner (exit 0).

### CHG-007: Repair the malformed IDEA-012 row, or record the defect and defer

- **Finding IDs:** F-007
- **Severity:** ADVISORY
- **Change type:** authorised enhancement, or a documented deferral
- **Accepted requirement, or a new proposal:** accepted requirement - fixtures must be reproducible
  and must say what they mean.
- **Affected revision, file and section:** `05ed112a...`;
  `evals/fixtures/stale/IDEAS-002.md`, the Ideas table, IDEA-012 row.
- **Evidence and reproduction:** the row carries 5 cells against a 6-column header, so "AI proposal"
  lands under "Who is affected" and "proposed" under "Origin", leaving "State" empty. `diff` against
  `stale/preserved/IDEAS-002.r1.md` shows revision 1 has the correct 6 cells including the
  "Members." cell revision 2 lost.
- **Demonstrated impact:** contained. A worker reading revision 2 in DP-B-007 reads IDEA-012's
  affected users as "AI proposal". DP-B-007 grades DEC-002 and IDEA-013, not IDEA-012, so no current
  graded observation is distorted.
- **Bounded desired behaviour:** restore the missing cell, then update all three places recording
  `300f1c7872ce1f8121f2554e4a3daf0b60754f3ee3e79bea24db20c8778c4e1d` - `cases.jsonl` DP-B-007
  assertion A1, the `evals/fixtures/README.md` digest table, and the evals digest map in
  `references/derivation.json` - to the new digest, in that order, hashing after the fixture's bytes
  are final. **Because the repair costs three coordinated digest updates on a pinned sentinel,
  leaving the defect recorded and unrepaired is a legitimate choice**; if it is deferred, note it in
  the fixtures README so the next reader does not treat it as an authored fact about IDEA-012.
- **Behaviour to preserve:** every other difference between the two ledger revisions, especially the
  widened DEC-002 and the added IDEA-013, which are the substance of DP-B-007.
- **Acceptance condition:** either the row has 6 cells and all three recorded digests match the new
  bytes, or the fixtures README records the known defect.
- **Affected reruns:** DP-B-007 A1 if repaired.

### CHG-008: Record the source for the devforge check characterisation

- **Finding IDs:** F-008
- **Severity:** ADVISORY
- **Change type:** authorised enhancement
- **Accepted requirement, or a new proposal:** accepted requirement. skill-authoring-contract rev 3
  requires the derivation record to state where package content came from.
- **Affected revision, file and section:** `05ed112a...`; `references/sources.md`, "DevForge CLI
  command surface"; `references/derivation.json`, the `observed_runtime_input` block; optionally the
  sentence in `SKILL.md` "What this skill owns, and what it does not" and its twin in
  `references/recording-rules.md`.
- **Evidence and reproduction:** `SKILL.md` and `references/recording-rules.md` state that
  `devforge check` "checks a project candidate's dependencies, layout, tooling pins and expert
  provenance". `devforge check --help` prints only "Check structural policy and provenance; does not
  certify semantic behavior", and `references/sources.md` scopes its `--help` observation to the
  "no command covers this workflow" statement.
- **Demonstrated impact:** the statement is **factually accurate**, verified against the
  repository's policy schema. This is a provenance gap, not an error: a later reader cannot check
  the more specific half against any source the package records.
- **Bounded desired behaviour:** either soften both sentences to the `--help` wording, or add the
  actual source - the policy schema - to `references/sources.md` with its identity and to the
  `derivation.json` observed-input block. Prefer adding the source: the specific description is more
  useful to a session than the generic one, and it is correct.
- **Behaviour to preserve:** the accuracy of the ten named subcommands and the missing-integration
  statement, both verified correct against the binary; the existing and correct `--help` limit note.
- **Acceptance condition:** every factual claim about `devforge check` in the package resolves to a
  source the package records.
- **Affected reruns:** none.

### CHG-009: Name feasibility in phase 2

- **Finding IDs:** F-009
- **Severity:** ADVISORY
- **Change type:** authorised enhancement
- **Accepted requirement, or a new proposal:** accepted requirement. SKILL-002 rev 2, "MVP support
  decision": "includes proportionate discovery and feasibility research".
- **Affected revision, file and section:** `05ed112a...`; `SKILL.md`, "## 2. Investigate", the
  proportionality paragraph.
- **Evidence and reproduction:** `grep -rn -i feasibility` over `SKILL.md` and `references/` returns
  nothing.
- **Demonstrated impact:** low. A session is never told that checking whether the scope is
  deliverable under the stated constraints belongs to phase 2.
- **Bounded desired behaviour:** extend the existing proportionality sentence so feasibility - can
  this be built inside the constraints the user actually stated - is named as a second kind of
  research subject to the same proportionality rule. One clause, not a new subsection.
- **Behaviour to preserve:** the read-only research boundary and the prohibition on contacting
  customers, signing up or spending money; the existing proportionality rule itself.
- **Acceptance condition:** phase 2 names feasibility and keeps it proportionate.
- **Affected reruns:** DP-B-002.

### CHG-010: Give the consumer table the release boundary

- **Finding IDs:** F-010
- **Severity:** ADVISORY
- **Change type:** authorised enhancement
- **Accepted requirement, or a new proposal:** accepted requirement. SKILL-002 rev 2, acceptance
  case "Out of scope".
- **Affected revision, file and section:** `05ed112a...`; `SKILL.md`, "What downstream reads".
- **Evidence and reproduction:** the routing instruction appears only in the frontmatter description
  and in the "Stopping" paragraph. The table has six consumer rows and no `devforge-release` row.
- **Demonstrated impact:** low; the behaviour is instructed and the description loads with the body.
  The concern is placement: the table is the phase-local artifact a session consults when choosing a
  continuation in phase 4.
- **Bounded desired behaviour:** add a `devforge-release` row, or one sentence beneath the table,
  stating that a request to ship an already-accepted build belongs to `devforge-release` and is not
  scope work.
- **Behaviour to preserve:** the six existing consumer rows, which match the specification's
  consumer-coverage line exactly; the existing and important paragraph that naming a consumer is not
  evidence it is installed.
- **Acceptance condition:** the release boundary is reachable from the phase-4 section without
  relying on the frontmatter.
- **Affected reruns:** DP-B-005.

## Implementation order

- **CHG-001 before CHG-002.** CHG-002's preferred form re-cites the section CHG-001 creates. If
  CHG-001 is deferred, CHG-002 takes its alternative form and states the requirement is not carried.
- **CHG-007 last, if taken at all.** It changes a pinned sentinel digest recorded in three files, so
  applying it after every other fixture edit avoids hashing the same bytes twice.
- **CHG-003 before any tier-B run.** Running DP-B-010 against the current grading text risks
  recording a false FAIL against correct behaviour.
- All other changes are independent of each other and may be applied in any order.

Whatever subset is applied, re-hash every changed file after its bytes are final and reconcile
`references/derivation.json` destination digests and the author's `file-manifest.json`, which this
evaluation verified as exact at the current revision and which will otherwise become stale.

## Evaluation prerequisites, not defects

None of these authorises a target edit, and editing the candidate will not produce any of them.

- **Skill-package structural inspection (S001-S013) and evidence reduction are not implemented in
  the DevForge CLI.** Verified against `devforge --help`, `check --help`, `expert --help` and
  `delivery --help` on the binary at sha256
  `835c32639c0a7df270fe1b9182580f14fc7d0874d3aad1b4037ba7cf420b2b07`. Every structural row in this
  evaluation is a manual observation with `authority: none`, and the complete set of matching runner
  rows does not close the dependency. Owner: DevForge integration owner.
- **Protected-manifest custody for the evaluation runner is not implemented in the DevForge CLI.**
  Runner, grader, runtime and case identities are self-reported by the run. Owner: DevForge
  integration owner.
- **No installed or exported copy of the candidate.** Blocks tier C entirely and the installed-mode
  half of DP-C-002. Owner: coordinator.
- **No isolated evaluation workspace and no fresh terminal.** Blocks tiers B and A, and therefore
  every claim about output quality, discovery and activation. Owner: coordinator.
- **The validator followed here is itself a draft under an unfinished bootstrap review** (E2:
  revise, repaired at `e101e76`, recheck outstanding). Owner: the `devforge-evaluate-expert` author
  under coordinator dispatch.

## Closure rules

- **Applied** means the source was edited. It does not close a finding.
- A changed candidate is a new identity and needs new matching evidence before any finding is closed.
- Preserve the original failure history; never overwrite an earlier `FAIL`. F-001's `FAIL` stands in
  this report whatever a later revision does.
- Never weaken an accepted expectation, delete a case or change a sibling gate to convert a recorded
  failure into a pass. A defect in a shared contract goes to its integration owner.
- Repairing every change above would move the disposition from *revise* to *insufficient evidence*,
  **not** to *suitable for the stated scope*. That step needs tiers C, B and A, which no edit
  produces.

**Validation status:** Not performed by this document.
**Finding status:** ten findings recorded, none closed; reevaluation required after any change.
