---
schema_version: "devforge.artifact/v1"
artifact_id: "CHGSPEC-PLAN-SCAFFOLD-001"
artifact_type: "skill-enhancement-spec"
project_id: "devforgeai"
revision: 1
status: draft
created_at_utc: "2026-09-10T21:40:15Z"
producer:
  skill: "devforge-evaluate-expert"
  skill_revision: "source-loaded, not installed; SKILL.md read from git commit e641797eebf04cd1e8eb9f711549e038e7745407. No installed copy exists, so no installed-file digest is claimed."
execution_ref: null
upstream:
  - artifact_id: "EVREPORT-PLAN-SCAFFOLD-001"
    revision: 1
    store: "evaluation evidence"
    path: "docs/skill-authoring/history/claude-scaffolding-20260910/devforge-plan/validation/scaffold-review/verification-results.md"
    sha256: "computed by the evaluator after that file's bytes were final and delivered in the terminal response; not written into this document"
    sections:
      - "Findings"
      - "Independent review — criteria R01-R10"
      - "Decision and coverage"
  - artifact_id: "SKILL-006"
    revision: 2
    store: project
    path: "docs/mvp/specifications/skill-006-devforge-plan.md"
    sha256: "149a66a375da1bb3447f51b657996883974fec1dac3ce92af866eba94a378e4b"
    sections:
      - "Workflow and phase exits"
      - "Validation and behavioral acceptance"
      - "Rework, stopping, and recovery"
evidence:
  - "findings.json"
  - "runner-out/pkg-source.jsonl"
  - "runner-out/pkg-installed-mode.jsonl"
  - "runner-out/fixtures-source.jsonl"
  - "runner-out/evaluator-added-source.jsonl"
  - "commands.log"
supersedes: null
decision_ref: null
missing_inputs:
  - "Tier C, B and A observations do not exist for this candidate; no change below is justified by behavioural evidence, and none claims to be."
---

# Skill repair and enhancement specification — devforge-plan (SKILL-006)

The bounded, evidence-backed change request returned for `devforge-plan` at
`03dc1a605acfb3ff80577f244d1a60f52244fb36`. It authorises no automatic edit, invocation, installation,
acceptance or release, and it carries forward the existing user authorisation without expanding it.

Every change below rests on a defect I demonstrated against the frozen bytes. Nothing here is a style
preference, a compression target, a word or line count, or a heading-sequence requirement. Where I could
not prove a cause, I have written no patch.

## Immutable intake

- **Evaluated candidate:** worktree `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-plan-20260910`,
  commit `03dc1a605acfb3ff80577f244d1a60f52244fb36`, package root
  `providers/claude/plugins/devforgeai/skills/devforge-plan/`. Thirty-file manifest in
  `verification-results.md` §"Identity and scope"; `git diff 03dc1a60… HEAD --stat -- providers/` empty.
- **Installed copy evaluated:** **not installed.** No copy exists in any Claude discovery location for
  this assignment. Every installed-mode observation is unavailable.
- **Specification:** `/home/bryan/Projects/DevForge/framework/DevForgeAI/docs/mvp/specifications/skill-006-devforge-plan.md`,
  DRAFT revision 2, sha256 `149a66a375da1bb3447f51b657996883974fec1dac3ce92af866eba94a378e4b`.
- **Evaluation report:** `verification-results.md` in this directory, `EVREPORT-PLAN-SCAFFOLD-001`
  revision 1.
- **Results record:** `findings.json` in this directory. There is no `validation-results.json`: the
  frozen validator's machine-readable half is replaced for this assignment by the packet-defined
  `findings.json`, which carries the per-criterion outcomes and the finding rows.
- **Independent review:** performed and recorded inline in `verification-results.md` §"Independent
  review — criteria R01-R10". Reviewer: a separately dispatched Claude evaluator context. Independence
  limits recorded there; in particular I read the author's `derivation.json` and `spec-mapping.md` as
  evaluation inputs, and no second reviewer was dispatched.
- **Cases and fixtures:** the candidate's own `evals/cases.jsonl`
  (`9c9938aa0e7d855c6b9ab6b8b04045b6f6e51bde176b703ceec031ae25dd77ec`), `evals/evals.json`
  (`d5627bf400a27a5bade7bb7b75790619c9e0814cb47feaeb2d11b923d9ed9ec6`),
  `evals/triggers/trigger-queries.json` (`ad23ff6470835face03b78300bde02732d38bf35136c989396bb23c17e03ed60`)
  and the 18 files under `evals/fixtures/`, all digests in `verification-results.md`. Plus the
  evaluator-added `runner-out/evaluator-added-cases.jsonl` in this directory, which is evaluator
  evidence and **not** part of the candidate.
- **Runner and graders actually used:** `scripts/run_cases.py`
  `95ca2abf77a5baf249694ad37d67a74949b567acd5164fd309724cbc576583e2` and `scripts/graders.py`
  `1b7a27a37e1fb8b2e36b1822bc23227c69e6300243e1b49b8caa848e3feca69f`, from
  `devforge-evaluate-expert` at `e641797`. These identities are self-reported by the run; no protected
  manifest binds them.
- **Prior iteration:** none. This is the first evaluation of this package. Baseline `without_skill`.

Preserve these identities exactly. Verify them before editing, and retain the old candidate bytes.

## Change decision

- **Are target changes justified by the evidence?** **Yes**, for CHG-001 through CHG-005. CHG-006 and
  CHG-007 are advisory and may be declined without affecting the disposition.
- **Next owner:** the author role for this package is `devforge-project-expert-creator` (the validator's
  named repair owner). The party actually dispatched is **the scaffold's author, under coordinator
  dispatch**, working in the same worktree and branch. Both are recorded deliberately; do not collapse
  them. Whoever takes it must verify current worktree ownership before writing, because I did not.
- **Behaviour that must be preserved unchanged:**
  - The frontmatter: `name` and `description` only, `name` equal to the folder, and all three near-miss
    exclusions naming their owning siblings. The description is 897 characters and discriminates well;
    do not rewrite it for style, and do not add `allowed-tools`, `model`, `paths`, `context`, `agent`
    or `hooks`.
  - The four phases, their order and their stated **Exit** conditions.
  - The prohibition on narrating a phase as a check, on self-issued PASS, and on writing a command
    sequence that pretends to gate; and the statement that no DevForge command inspects a planning
    artifact at this revision. These are the strongest parts of the package.
  - The prompt-injection posture in `SKILL.md` and in `references/recording-rules.md`.
  - The two-roots path rule, the absence of `scripts/`, `agents/` and `hooks/`, and the absence of any
    developer home path or `docs/mvp` runtime dependency.
  - The inherited / proposed / adopted separation, the `decision_ref` rule, the digest write order and
    the no-self-digest rule.
  - `assets/epic.md` and `assets/story.md` as byte-identical copies of the governing templates.
  - Every fixture's bytes, and the embedded digests that make the fixtures resolvable offline.
- **Forbidden scope changes:** this specification does not authorise editing `docs/mvp/**` (the
  specification, the contracts, the roster, the templates or `package-index.json`); editing any sibling
  skill or provider source; editing the `devforge-evaluate-expert` runner, graders, rubric or cases;
  editing anything in the companion DevForge repository, including its gates, policies, tests and
  `tooling_files` pins; installing, exporting, binding, or running any tier; committing on another
  session's behalf; or broadening `devforge-plan`'s scope beyond SKILL-006. If a defect appears to lie
  in a shared contract or a sibling gate, report it to that owner rather than editing around it.

## Requested changes

### CHG-001: instruct interruption and resume behaviour

- **Finding IDs:** F-001
- **Severity:** MAJOR
- **Change type:** required repair
- **Accepted requirement, or a new proposal:** accepted requirement. SKILL-006 line 46 ("On
  interruption, preserve the current phase and evidence; resume by checking their identities and the
  session assignment again") and line 85 ("If the worktree or active run changes, re-establish the
  appropriate baseline and evidence before resuming").
- **Affected revision, file and section:** `03dc1a60…`, `SKILL.md` §"Stopping" (lines 233-249), or a new
  subsection of `references/readiness-check.md` linked from §"4. Check readiness".
- **Evidence and reproduction:** `verification-results.md` §R04(a) and F-001. Reproduce with
  `grep -ni 'interrupt\|resum\|re-establish'` over `SKILL.md` and `references/*.md` — zero hits; the only
  package hit is `assets/handoff.md:90`, a section of a completed handoff document that an interrupted
  session never reaches. `diff` against `docs/mvp/templates/shared/handoff.md` shows the `Current phase`
  row was removed from the adaptation.
- **Demonstrated impact:** an interrupted planning session has no instruction to preserve the phase and
  evidence, and none to re-read the session assignment and re-check the frozen digests before resuming
  writes. That re-check is the precondition both the staleness rule and the ownership-collision rule
  depend on, so the gap reopens the two failures the rest of the package handles carefully.
- **Bounded desired behaviour:** one short paragraph stating that on interruption the session preserves
  the phase reached, the frozen input identities and any outputs already written; and that on resume it
  re-reads the session assignment and re-checks the recorded digests before writing further, treating a
  changed input as a new iteration rather than a continuation of this one.
- **Behaviour to preserve:** the rest of §"Stopping" verbatim, including the finite completion
  condition and the instruction not to add another pass of polish, a second planning document or a
  broader scope.
- **Acceptance condition:** a later evaluation finds an instruction covering both halves of SKILL-006
  line 46 — preserve on interruption, re-check identities and assignment on resume — reachable from the
  installed entrypoint without depending on the handoff step.
- **Affected reruns:** none exist. Add a tier-B case staging an interrupted session (see CHG-005).

### CHG-002: name the receiving sibling for an unscoped request in the body

- **Finding IDs:** F-002
- **Severity:** MINOR
- **Change type:** required repair
- **Accepted requirement, or a new proposal:** accepted requirement. SKILL-006 line 69, the "Out of
  scope" acceptance case: "Routes to brainstorm or define-product."
- **Affected revision, file and section:** `03dc1a60…`, `SKILL.md` §"Required inputs" missing-input
  paragraph (lines 70-73) or §"Stopping" (lines 233-249).
- **Evidence and reproduction:** `verification-results.md` §R04(b) and F-002.
  `grep -n 'brainstorm\|define-product' SKILL.md` matches line 3 (the frontmatter description) only;
  zero matches in the body or in any reference. `spec-mapping.md` line 78 claims §"Stopping" carries it;
  it does not.
- **Demonstrated impact:** the required observation for this acceptance case is that the response names
  a receiving sibling. Once the body is loaded it is the operative guidance and contains no such
  instruction, while the missing-input rule pulls toward continuing to partition a request that should
  not be partitioned. The candidate's own `evals.json` id 4 and `PL-B-005` grade exactly this.
- **Bounded desired behaviour:** one sentence: when no scope has been adopted at all, do not partition —
  name early-stage exploration as the work and route it to `devforge-brainstorm`, or to
  `devforge-define-product` where the open question is what the scope should contain, keeping what is
  suggested separate from what is installed.
- **Behaviour to preserve:** the three description exclusions exactly as written; the existing
  missing-input behaviour for the case where scope exists but one input is absent; the existing
  "check what is actually installed before naming a receiver" rule in §"Outputs".
- **Acceptance condition:** a later evaluation finds a body instruction naming at least one receiving
  sibling for a request with no adopted scope, consistent with the description's exclusions.
- **Affected reruns:** `evals.json` id 4; `PL-B-005`; trigger category `negative_unscoped_exploration`.

### CHG-003: split PL-PKG-001 so its mode-independent assertions are observable

- **Finding IDs:** F-003
- **Severity:** MINOR
- **Change type:** required repair
- **Accepted requirement, or a new proposal:** the case file's own purpose — supplying deterministic
  structural observations for this package — and the authoring contract's separately reported tiers.
- **Affected revision, file and section:** `03dc1a60…`, `evals/cases.jsonl`, case `PL-PKG-001`.
- **Evidence and reproduction:** `runner-out/pkg-source.jsonl` — `PL-PKG-001` A1-A5 all `INDETERMINATE`,
  "the case declares mode 'installed' and this run used 'source'". The frozen `run_cases.py` applies the
  case-level `mode` to every assertion in the case. `runner-out/evaluator-added-source.jsonl` —
  `EV-PKG-001` A1-A4, the same four assertions with no mode declaration, all `MATCH`.
- **Demonstrated impact:** the package's only deterministic frontmatter, name/folder and `SKILL.md`
  link-resolution observations are unobtainable in any assignment without an installed copy — which is
  every assignment so far, including this one. This evaluator had to author a replacement case.
- **Bounded desired behaviour:** `PL-PKG-001` keeps A1-A4 and drops the case-level `mode` key. A new case
  carries A5 (`path_absent` on `evals`) with `"mode": "installed"` and a title stating it is only
  observable against an installed copy.
- **Behaviour to preserve:** the assertion bodies, their `args`, and `PL-PKG-002` unchanged.
- **Acceptance condition:** a source-mode run returns real `MATCH`/`MISMATCH` rows for the four
  structural assertions, and the installed-only assertion is `SKIPPED` or `INDETERMINATE` rather than
  silently blocking them.
- **Affected reruns:** `PL-PKG-001` and its new sibling case, in both modes.

### CHG-004: make the vacuous link assertions observe something

- **Finding IDs:** F-004
- **Severity:** MINOR
- **Change type:** required repair
- **Accepted requirement, or a new proposal:** eval quality — an authored assertion must be able to
  observe the condition it names.
- **Affected revision, file and section:** `03dc1a60…`, `evals/cases.jsonl`, case `PL-PKG-002`,
  assertions A9, A10, A11.
- **Evidence and reproduction:** `runner-out/pkg-source.jsonl` and `runner-out/pkg-installed-mode.jsonl`
  — all three return `MATCH` with observed "0 local, 0 external"; the three targeted references carry no
  Markdown links. `runner-out/evaluator-added-source.jsonl` `EV-PKG-002` A1 shows
  `references/sources.md` observes "1 local, 2 external" and is covered by no candidate case.
- **Demonstrated impact:** three rows that can never fail read as link coverage the case file does not
  have, while the only reference carrying a resolvable local link is unobserved. A future edit breaking
  `sources.md`'s link to `derivation.json` would be caught by no authored case.
- **Bounded desired behaviour:** either point A9-A11 at `references/sources.md` and the three assets, or
  delete them and state in the case's `expectations.summary` that the three operative references carry
  no Markdown links by design. Either resolves it; the first also adds real coverage.
- **Behaviour to preserve:** A1-A8 and A12 unchanged.
- **Acceptance condition:** every `package_relative_links` assertion in the case file targets a file that
  either contains a link or is documented as link-free.
- **Affected reruns:** `PL-PKG-002`.

### CHG-005: repin the runner dependency and record the schema recheck

- **Finding IDs:** F-005
- **Severity:** MINOR
- **Change type:** required repair
- **Accepted requirement, or a new proposal:** the package's own `derivation.json` `dependency_status`,
  which requires a recheck against the new grader registry and case schema before the file is run.
- **Affected revision, file and section:** `03dc1a60…`, `references/derivation.json`, the `derivations[]`
  entry whose `destination` is `evals/cases.jsonl` — its four source pins and its `dependency_status`.
- **Evidence and reproduction:** the record pins `run_cases.py` `d1fb1868…` and `graders.py` `7c03e7b2…`
  at `e52ac59`; the frozen validator carries `95ca2abf…` and `1b7a27a3…` at `e641797`, with `+108`/`+55`
  changed lines including new whole-file rejection of unknown keys.
- **Demonstrated impact:** bounded. **The file is not broken.** I performed the recheck the record calls
  for: the ten-entry grader registry is byte-identical across the two revisions, every case and
  assertion key the candidate uses is inside the frozen runner's permitted sets, and the file loaded
  and produced 17 case records at exit 0 in three separate runs. The defect is that the record asserts a
  dependency at a revision no longer on the merge path and states an unsatisfied recheck condition.
- **Bounded desired behaviour:** repin the four source entries to the runner revision actually selected
  for evaluation, and replace `dependency_status` with the observed compatibility statement.
- **Behaviour to preserve:** `evals/cases.jsonl`'s own bytes. Nothing in the case file needs to change
  for this item; CHG-003 and CHG-004 are separate.
- **Acceptance condition:** the pinned digests equal the runner and graders at the selected revision, and
  the status records a performed recheck rather than a pending one.
- **Affected reruns:** none for the repin itself; this evaluation's runs already establish compatibility
  at `e641797`.

### CHG-006: route an unknown producer revision to missing_inputs (advisory)

- **Finding IDs:** F-006
- **Severity:** ADVISORY
- **Change type:** authorised enhancement
- **Accepted requirement, or a new proposal:** derived from `docs/mvp/artifact-contract.md` §"Standard
  envelope", which requires "exact installed skill revision/digest" for `producer` and defines no
  `unknown` fallback for it.
- **Affected revision, file and section:** `03dc1a60…`, `references/recording-rules.md` §"Identity and
  digests", final paragraph.
- **Evidence and reproduction:** the reference offers `unknown` as "the honest entry" and claims to
  restate the contract without extending it; `grep skill_revision docs/mvp/artifact-contract.md` returns
  no hits. `evals/fixtures/good/EPIC-001.md` carries an `unknown` producer revision.
- **Demonstrated impact:** an epic or story could carry `producer.skill_revision: unknown` with an empty
  `missing_inputs` and still be presented as a complete result.
- **Bounded desired behaviour:** state that an `unknown` producer revision is a missing required fact
  that belongs in `missing_inputs`, and mark the one-file definition explicitly as this package's
  narrowing rather than a contract restatement.
- **Behaviour to preserve:** the useful distinction between a `SKILL.md` digest, a package digest and a
  plugin version, and the existing "where the two differ the contract governs" sentence.
- **Acceptance condition:** the paragraph no longer permits a silent `unknown` in a required field.
- **Affected reruns:** none; an artifact assertion on `producer.skill_revision` could be added.

### CHG-007: disclose the removed handoff-template rows (advisory)

- **Finding IDs:** F-007
- **Severity:** ADVISORY
- **Change type:** authorised enhancement
- **Accepted requirement, or a new proposal:** the skill-authoring contract's derivation-record purpose.
- **Affected revision, file and section:** `03dc1a60…`, `references/derivation.json`, the `derivations[]`
  entry for `assets/handoff.md`, its `transformation` string.
- **Evidence and reproduction:** `diff docs/mvp/templates/shared/handoff.md assets/handoff.md` — the
  "You are here" section lost `Current phase: {{phase}}` and `Exact candidate or artifact scope`, and
  folded `Task state` into `Result`. None of the three appears in the `transformation` string.
- **Demonstrated impact:** two removals are invisible in the record whose stated purpose is to let a
  later reader tell a deliberate refresh from silent drift, and one of them is load-bearing for F-001.
- **Bounded desired behaviour:** name the removals in the `transformation` string, or restore the
  `Current phase` row — which also serves CHG-001 — and record the remaining removal.
- **Behaviour to preserve:** the rest of the transformation and `preserved` entries, both accurate.
- **Acceptance condition:** the record accounts for every difference between the shared template and the
  package copy.
- **Affected reruns:** none.

## Implementation order

CHG-001 through CHG-007 are independent and may be applied in any order, with two couplings:

- CHG-001 and CHG-007 both touch the `Current phase` row. Restoring it satisfies part of both; decide
  once and record it in both places.
- CHG-003 and CHG-004 both edit `evals/cases.jsonl`. Apply them in one pass and rerun the package group
  once, in both modes.

CHG-005 is the only item that should be applied even if every other item is declined, because the
package's own record currently states an unmet precondition for running its own cases.

## Evaluation prerequisites, not defects

None of the items below authorises a target edit, and editing `devforge-plan` will not produce any of
them.

- **Skill-package structural inspection (S001-S013) and evidence reduction are not implemented in the
  DevForge CLI.** Verified against `devforge --help` on 2026-09-10. Every structural row in the report
  is `INSPECTION_MANUAL` with `authority: none`. Owner: DevForge integration owner. Blocked claim: no
  structural observation here has gate authority, and a full set of matching runner rows does not close
  the dependency.
- **Protected-manifest custody for the evaluation runner is not implemented in the DevForge CLI.** The
  runner, grader, runtime and case identities in `runner-out/*.jsonl` are self-reported. Owner: DevForge
  integration owner.
- **No implemented decision receipt exists.** No `decision.json` was produced. The disposition was
  adjudicated by hand against the validator's results contract. Owner: DevForge integration owner.
- **Tiers C, B and A are `NOT_RUN`** — no installed copy, no fresh terminal, no isolated evaluation
  workspace, no baseline arm. Owner: the coordinator, for allocation. Blocked claims: installed-resource
  resolution, output quality against `without_skill`, and discovery/activation. Behavioural status stays
  `NOT_EVALUATED` until a real run exists. **These are the reason the disposition could never have been
  *suitable for the stated scope* in this assignment, and no repair changes that.**
- **The validator followed is itself a draft under bootstrap review** with no native evaluation. Owner:
  the `devforge-evaluate-expert` author, under coordinator dispatch. Findings graded against its rubric
  inherit that status.
- **The frozen runner does not read the assertion-level `expect` key**, so a negative-fixture case
  surfaces as a `MISMATCH` row distinguishable from a real defect only by reading
  `expectations.summary`. Owner: the `devforge-evaluate-expert` author. `PL-C-004` discloses it in
  words, which is the correct available mitigation. **No target edit** is requested for this.

**No target edit** is requested for any item in this section.

## Closure rules

- **Applied** means the source was edited. It does not close a finding.
- A changed candidate is a new identity and needs new matching evidence before any finding is closed.
  In particular, CHG-001 and CHG-002 change instruction text whose effect only a tier-B observation can
  establish; applying them closes the structural gap, not the behavioural question.
- Preserve the original failure history. Do not overwrite this report, `findings.json` or the runner
  outputs; a later iteration writes beside them.
- Never weaken an accepted expectation, delete a case or change a sibling gate to convert a recorded
  failure into a pass. A defect in a shared contract goes to its integration owner.

**Validation status:** Not performed by this document.
**Finding status:** seven findings recorded; reevaluation required after any change.
