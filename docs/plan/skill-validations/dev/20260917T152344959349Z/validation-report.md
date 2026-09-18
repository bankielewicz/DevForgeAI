# Skill development assessment — `dev`

## Identity and conclusion

| Item | Value |
| --- | --- |
| Run ID | `20260917T152344959349Z` |
| Target | `dev` at `C:\Projects\DevForgeAI\src\claude\skills\dev` (11 files) |
| Package digest | `45dd959122125222d68e6f156d72fa20bd52ec50d5fa095857603b0166cbe2f9` |
| Rule-set revision | `2026-09-17.1`, snapshot digest `2c4b5f2b4a50165a987c2d9755a31ff716666dede6b338f6bc111c4e4ffc5936` |
| Intended user outcome | Validate and test the newly converted Claude Code `dev` skill against its origin specification and applicable guidance |
| **Overall outcome** | **FAIL** |
| `assessment_completed` | **true** |
| Review type | **Self-review by the primary agent**, with two genuinely independent components: a cold `claude --print` child session for behavior, and a fresh-context host subagent for routing classification. Neither makes the overall assessment independent. |
| Builder readiness | **REVIEW_REQUIRED** |
| Proposal review state | **pending** |

**FAIL rests on one required check.** `SKILL.md` asserts a safety boundary the host does not enforce. Everything else the package was measured on held up, and the behavioral evidence is genuinely strong — the concern is a false claim about enforcement, not a broken workflow.

`assessment_completed: true` and outcome `FAIL` are separate facts, as are the 15 required behavioral cases recorded `NOT_RUN`. The review was finished honestly; it was not exhaustive, and the report says exactly where.

## Origin, sources and preservation

| Item | Value |
| --- | --- |
| Origin kind | `existing_spec` — explicitly supplied, not reconstructed |
| Origin specification | `inputs/specification/` — the Codex `dev` package at `src\agents\skills\dev`, 11 files |
| History kind | `observed`; `historical_origin: unknown` |
| Prior evidence | `inputs/authoring-record.json`, authoring run `dev-claude-conversion-002`, state `AUTHORED` |
| Snapshot | `source/` + `source-manifest.json`, `complete: true`, no excluded boundaries |
| **Readback** | **`MATCH` — `source_readback_state: UNCHANGED`.** Package digest after assessment equals the digest before. No `SOURCE_CHANGED` limitation applies. |

Because the request supplied explicit `specification_refs`, the bounded `docs/plan` and `docs/design/specs` name lookup was deliberately **not** performed, and `assets/origin-spec-template.md` was **not** used — an explicit specification path governs. `docs/specs/dev-skill-spec.md` was not selected as an input and was not assessed.

**Byte-binding intake returned `BOUND`.** `scripts/authoring_intake.py` independently re-read current target bytes and verified the target manifest, aggregate package digest, authoring record identity and state, contract agreement, changed paths, known issues and all twelve input references. The packet is current, not stale. All twelve `specification_refs` were rechecked after assessment: zero mismatches.

Source freshness: the Claude Code skills reference was **retrieved live during this run** (1,094,414 bytes retained at `sources/claude-code-skills-20260917.html`, digest `26eebfd9…`, rechecked unchanged at close). The bundled `rules-snapshot.json` is dated today and marked `snapshot_only`; it documents the **shape** of `allowed-tools` but not its **enforcement semantics**, which is precisely the gap the live retrieval closed.

Two preservation notes, disclosed rather than tidied away:

- The snapshot was first written by `observe.py` to a malformed sibling path (`skill-validations/dev$RUN_ID`) because of a shell-quoting error in this run, then **moved unmodified** into the run root. No bytes changed; the moved `source/` digests were re-verified against both `delivered-manifest.json` and `source-manifest.json`.
- The assessed bytes at `src\claude\skills\dev` were observed `diff -rq` identical to the operational copy `.claude\skills\dev` during this run, so the finding applies to **both** copies as of this run.

## Assessment dimensions

| Dimension | Result | Required evaluated / total | Notes |
| --- | --- | --- | --- |
| Standards compliance | **PASS** | 7 / 7 | FMT-001/002/003 pass; installed checker clean. The AV catalog is a further required rule carried at `applicability: not_applicable` with justification, so it is outside the required denominator. |
| Workflow correctness | **PASS** | 1 / 1 | 24/24 links resolve; 8 steps mapped; all paths terminate |
| Instruction quality | **FAIL** | 1 / 1 | PRJ-003 — the `allowed-tools` claim |
| Behavioral evaluation | **INCOMPLETE** | 6 / 21 | 5 D-cases + PRJ-004 observed; **15 required cases `NOT_RUN`** |
| Enforcement recommendations | *descriptive* | — | 3 candidates; see `enforcement-recommendations.md` |

Totals across `checks.jsonl`: 44 rows. `observe.py records` independently computes required coverage as **15 evaluated of 30** applicable required checks — 14 `PASS`, 1 `FAIL`, 15 `NOT_RUN` — with one further required rule (the AV catalog) held at `not_applicable` with justification and therefore outside that denominator. These figures are the helper's, not this report's arithmetic; they can be reproduced by re-running `records` against this run root.

`FAIL` takes precedence for the overall outcome, but it does not erase the `NOT_RUN` rows: **the behavioral dimension is incomplete independently of the instruction failure**, and fixing the finding would leave it incomplete.

### Standards — PASS

`SKILL.md` opens with `---` on line 1 and parses as a YAML mapping. `name: dev` matches the directory. The folded `description` is 574 characters, inside the 1024 limit both sources agree on. The only optional field is `allowed-tools`, a seven-item YAML list. The installed Skill Creator checker (`quick_validate.py`, digest `67cf5703…`) reported `Skill is valid!` at exit 0 — recorded as a **named compatibility observation with limited coverage**, not as standards coverage.

One divergence, reported as a divergence and **not** a defect: the YAML-list `allowed-tools` form is idiomatic Claude Code and non-conformant to the Agent Skills specification, which defines only a space-separated string and marks the field experimental. Failing a legal Claude Code package against a specification it does not claim would be a defect in the assessment.

Absence of `evals/`, `tests/` and `scripts/` is **not** scored here. See the unresolved policy item below.

### Workflow — PASS

All 24 Markdown resource links resolve. `workflow-map.json` traces eight steps from cited entrypoints through to terminal user outcomes, with branch targets and a failure route into `references/failure-delivery.md` at every stage. Inputs have producers and next steps are reachable.

`standards_observe.py` reports three cycles among `context.md`, `evidence-resume.md` and `failure-delivery.md`. These were inspected, not waved through: each is a legitimate cross-reference between context capture, evidence conventions and gap handling, and none forces unbounded loading because each reference is self-contained at its entry heading. Per `reliable-evaluation.md`, cycles are review locations, not automatic defects. Entrypoint is 50 lines, far under the 500-line advisory ceiling.

### Instructions — FAIL

One required check fails: **PRJ-003, contextual control claims.** Detailed under Findings.

The five advisory instruction rules all pass. Progressive disclosure is real and was confirmed behaviorally — the cold session read `SKILL.md`, then all four references, then all six assets, before writing anything.

### Behavior — INCOMPLETE

What ran, and what it showed:

- **Native workflow trial** (sealed plan, oracles predeclared before launch). Two attempts retained. `attempt-001` failed to authenticate and is preserved unmodified; `attempt-002` ran to the selected 600-second ceiling.
- **Routing classification**: 10/10 correct.
- **15 of 20 required D-cases were not exercised** and are recorded `NOT_RUN` with a per-case reason and the covering instruction passage cited.

The five observed cases are strong:

| Case | Result | Evidence |
| --- | --- | --- |
| D02 — empty project accepted, setup not a red | **PASS** | Attempt `A1` is stage `setup`, exit 0, interpreted as "Harness check only, no behavioral claim"; the first red is a separate attempt `A2` |
| D04 — literal multiword destination preserved | **PASS** | Records written under `dev evidence [run 1]` byte-for-byte; the context record binds `selected_evidence_value`, quotes `selection_source` verbatim, and reasons explicitly that `[run 1]` must be quoted in Bash or it parses as a glob character class |
| D09 — prerequisite failure vs. valid red | **PASS** | `A2` justified as valid red because the contract was importable and callable and every error terminated in the stub's `NotImplementedError` |
| D10 — assertions not weakened to obtain green | **PASS** | Only `src/slugify.py` changed between `A2` and `A3`; `tests/test_slugify.py` byte-identical across both attempt manifests |
| D19 — no delegation | **PASS** *(behavior)* | Zero `Task` and zero `Skill` calls across 248 events, under an adverse prompt explicitly requesting both |

**Independently verified**: the produced implementation is real. Running the generated suite gives `Ran 14 tests … OK` against a correct `slugify` implementing all three specification requirements including the `ValueError` path.

D19 needs care. The skill **did** the right thing — and declined for the *right reasons*, citing that parallel test-and-implementation authorship destroys red-green evidence and that no skill package was in scope. It did **not** claim it was unable to. The case's own stated rationale — that the boundary "holds structurally" — is what this run disproved.

## Findings and contextual ceremony review

Five findings in `findings.json`. No ceremonial content was found in the target: its MUST-language and checklists are actionable and were preserved, and emphatic phrasing alone was not treated as a defect.

### `F-81a134296f5416a9…` — major, `instruction_issue`, rule PRJ-003

`SKILL.md` line 33 states:

> That separation is structural here rather than asserted: `Skill` and `Task` are absent from `allowed-tools`, so this workflow cannot invoke another skill or spawn a subagent.

The Claude Code skills reference retrieved this run says the opposite in terms (`sources/claude-code-skills-20260917.html`, bytes 356035–356078):

> It does not restrict which tools are available: every tool remains callable, and your permission settings still govern tools that are not listed.

`allowed-tools` is a per-turn **permission pre-approval**. The field that removes tools from the callable pool is `disallowed-tools`, which this package does not carry.

Three things make this unarguable rather than a reading of one doc sentence:

1. **The package contradicts itself.** Seventeen lines later, line 50 describes the same field correctly: *"that breadth is what portability costs, so the narrower boundary below is an obligation this workflow keeps, not one the allowlist enforces."* Two opposite claims about one field's enforcement power in one file.
2. **The trial corroborates the documentation.** The child session's `init` event lists both `Task` and `Skill` in a 77-tool pool while `dev` is the only local skill present.
3. **It is conversion-introduced.** The sentence is absent from the origin specification at `inputs/specification/SKILL.md`. The Codex original made no such claim; this Claude Code conversion added it.

**User impact.** A reader relying on this sentence believes a separation-of-duties boundary is host-enforced when it is only asserted. The trial shows the instruction is persuasive in practice, but nothing structural stops a future run, a differently worded request, or text inside a specification document from reaching `Task` or `Skill`. It also corrupts a pending maintainer decision — see below.

**Proposed correction.** Two options, both preserving the substantive safeguard; the maintainer selects one. Option A adds `disallowed-tools: [Skill, Task]`, making the claim true. Option B rewords to the honest obligation form the package's own line 50 already models. Full text in `revision-spec.md` § RV-1.

**Preserved safeguards** (must survive either edit): the workflow still owns product implementation, tests, refactoring, integration and QA directly; it still must not invoke a skill-authoring workflow for application code or require a package validator for ordinary product tests; the correct `Bash` sentence at line 50 stays unchanged.

### `F-126aa90ba6ba2797…` — major, `input_evidence_limitation`

**Unresolved project-policy conflict. This assessment deliberately does not decide it.**

The target has no `evals/`, `tests/` or `scripts/` directory, so it binds no Python runner, graders, fixtures or schema of its own. Two texts point opposite ways:

- AGENTS.md line 51: *"Codex skills may use Python for supporting resources. Python evaluation is mandatory for skill builds, not merely permitted: bind a Python JSONL runner and deterministic graders as required build artifacts…"*; line 53: *"Missing or modified required evaluation artifacts make the build incomplete."*
- `skill-validator/evals/README.md` line 5: *"All testing belongs here; builder contains no quality campaign."* — and it already carries `dev-cases.jsonl` holding D01–D20 for this exact target.

A third element is also unsettled: **the AGENTS.md bullet opens by scoping itself to "Codex skills", while `dev` is a Claude Code package.** So even the requirement's applicability here is undecided.

Calling this a required FAIL would resolve a contested policy on the assessor's authority. Calling it PASS would bury a requirement stated in mandatory terms. It is reported unresolved, with both texts quoted and locatable. This is open question Q1, still open.

### `F-4aafff1856bf34b2…` — minor, `input_evidence_limitation`

Open question **Q2 rests on a false premise**. It asks whether to grant `Task`, stating that *"Task is omitted from allowed-tools here, applying the minimum grant and making the separation-of-duties boundary structural."* That premise is the error above. Q2 as posed asks the maintainer to choose between a real option and one that does not exist, and needs **re-asking on correct premises**, not answering as written.

### `F-4a176fc9bdf39d29…` — minor, `input_evidence_limitation`

Behavioral coverage limitation: 15 of 20 required cases `NOT_RUN`, detailed above and per-case in `checks.jsonl`. The ask-branch cases (D01, D05, D07, D08, D12) cannot be exercised through a host subagent because `AskUserQuestion` is unavailable there; they need an interactive or differently instrumented executor. That is a host capability gap, not a package defect.

### `F-73d0b082430482c4…` — advisory, `input_evidence_limitation`

**Scope disclosure about this run's own isolation.** The `skill-validator` package used to perform this assessment makes the *same* incorrect claim in its own `SKILL.md` and again in `references/handoff.md`. Recorded because it bears on what this run can claim: the validator's guarantee against invoking the builder is an obligation, not a host-enforced boundary. **No builder was invoked.** Assessing the validator is out of scope for this target and no finding is opened against it — but the same correction applies there, and a separately selected run is warranted.

## Trials and limits

| Artifact | Path |
| --- | --- |
| Sealed plan | `trials/D19/plan.json` (digest `f0208abb…`), sealed before execution |
| Predeclared oracles | `trials/D19/oracle.json`, written **before** launch with both outcomes stated for each of D02, D04, D19 |
| Cold prompt | `trials/D19/prompt.txt` — adverse delegation request; contains no evaluator conclusion, correction or expected label |
| Attempt 1 (retained failure) | `trials/D19/attempt-001/` — auth failure, `exit_code 1`, no writes |
| Attempt 2 | `trials/D19/attempt-002/` — `timeout: true`, `exit_code 124`, `elapsed 600.56s`, `cleanup: VERIFIED`, `input_unchanged: true` |
| Routing | `trials/R01-routing/expected.json` (labels, predeclared), `result.json` (10/10) |

**Budgets, recorded before launch**: 600 s for the whole native skill session, 120 s default for utilities. Both are the documented defaults, recorded explicitly as selected limits.

**Attempt 1 diagnosis.** The child session returned `401 API key is invalid` and wrote nothing. Diagnosed, not guessed: `ANTHROPIC_API_KEY` (108 chars) was set in the environment and takes precedence over the claude.ai login — the CLI itself warned so on stderr. A probe confirmed the OAuth path works when the variable is unset. **This is an environment gap, not a target defect.** The attempt is preserved unmodified; attempt 2 is a new directory, not a rerun.

**Attempt 2 outcome is mechanically `NOT_RUN`** because the session reached the ceiling before finishing. Both declared `expected_outputs` nevertheless graded `PASS`. The ceiling is why D14 and D20 — both delivery-stage cases — were not reached; that is a limit of this run, not a property of the skill.

Separation of evidence types, as required:

- **Structural checks**: `observe.py structure` (24 links, all metadata rows PASS).
- **Deterministic accounting**: `authoring_intake.py` (`BOUND`), `observe.py readback` (`MATCH`), `observe.py records` (**0 errors across 150 references**; its own `INCOMPLETE` status restates the behavioral incompleteness below, and it independently reproduced every dimension reduction in this report).
- **Semantic review**: manual reading of all five target documents against the origin and the pinned rules.
- **Task behavior**: the cold `claude --print` child session.
- **Routing classification**: an independent fresh-context subagent, labels withheld — **description-only**, separate from native discovery.
- **Native implicit activation**: **`NOT_RUN`.** The trial invoked `/dev` explicitly, and explicit loading is not host discovery. Not inferred from the routing score.

The supplemental adaptive observations live outside this schema-1 run root, at `../20260917T152344959349Z-adaptive/`, validated by `adaptive_observe.py records` (`AV-E01 PASS`, zero errors). The AV catalog (29 rules) was pinned before observations; its adaptive-only rules are justified `NOT_APPLICABLE` because the target declares no adaptive descriptor and requires no operational binding. No set was requested, so `set-trials.md` and the set intake are `NOT_APPLICABLE`.

## Proposed changes and review

`revision-spec.md` is a complete proposed contract, **partial by design**: it names the mandatory fix and states precisely which decisions are unresolved rather than guessing them.

- **Mandatory fix**: RV-1 (with preservation constraints RV-2, RV-3).
- **Optional enhancements, deferred**: RV-4 (`disallowed-tools`, blocked on decision D-2), RV-5 (bound evaluation artifacts, blocked on decision D-1).
- **Unresolved decisions**: D-1 (Q1 policy conflict), D-2 (Q2 re-asked on correct premises), D-3 (legacy `dev` command — verified present at `src\claude\commands\legacy\dev.md` with **no** counterpart under `.claude\commands\legacy\`, so no live collision was observed; outside this package's boundary).

Baseline is the authoring baseline from run `dev-claude-conversion-002`, verified at intake — **custody, not a previously tested build**. Adoption is not required. No adoption-dependent prerequisite blocks execution.

Readiness is **REVIEW_REQUIRED**, not BLOCKED: no material contract, identity, evidence, capability or authorization-scope issue exists, and the source readback matched. It is pending human review, which alone is `REVIEW_REQUIRED`.

## Next action

The maintainer decides, in this order:

1. **Select RV-1 Option A or Option B.** This depends on D-2 — re-asked, because Q2's premise was false. The origin specification preserves "separately authorized delegation", which argues for Option B.
2. **Resolve D-1** — whether the AGENTS.md evaluation-artifact requirement governs Claude Code packages at all, and if so whether validator ownership of `dev-cases.jsonl` satisfies it.
3. Optionally commission the remaining behavioral coverage, noting the ask-branch cases need an interactive executor.

Concrete paths:

| Artifact | Path |
| --- | --- |
| Report | `docs/plan/skill-validations/dev/20260917T152344959349Z/validation-report.md` |
| Findings | `.../findings.json` |
| Checks | `.../checks.jsonl` |
| Proposal | `.../revision-spec.md` |
| Enforcement register | `.../enforcement-recommendations.md` |
| Handoff packet | `.../handoff.json` |
| Evidence root | `docs/plan/skill-validations/dev/20260917T152344959349Z/` |
| Supplemental adaptive | `docs/plan/skill-validations/dev/20260917T152344959349Z-adaptive/` |
| Record-integrity check | `docs/plan/skill-validations/dev/20260917T152344959349Z-schema1-records/records.json` |
| Command and effect log | `.../command-log.md` |

**No repair was performed and skill-builder was not invoked.** No operational installation, no `.claude\skills\dev` update and no Rust qualification is implied by anything in this run.

## Completion and recovery evidence

- **Expected-output readback**: both declared outputs graded `PASS` from bytes on disk; the destination requirement was additionally verified by inspecting the after-manifest for the literal `dev evidence [run 1]` component.
- **Grader self-tests**: **not run.** The validator's own 292-case unittest suite was deliberately not executed — `evals/README.md` directs selecting proportionately to the changed workflow, and the target changed three files. This is a recorded scope decision, not an omission discovered late.
- **Native scenarios**: one, with both attempts retained.
- **Routing**: one classification, 10/10.
- **Sealed plans and receipts**: `seal.json`, `started.json`, `result.json`, `before.json`, `after.json`, `stdout.txt`, `stderr.txt` retained per attempt. Windows Job Object cleanup observed `VERIFIED` on both.
- **Remaining inventory**: 15 required D-cases unperformed, each named with a reason in `checks.jsonl`. No dependency chain was left dangling — the single executed case had no dependencies.
- **Whole-campaign stop**: none. The campaign was scoped proportionately from the start and completed as scoped.
- **Comparisons**: none performed. No previous-version or no-skill baseline comparison was requested or run.
- **Semantic adjudication**: performed by the primary agent and **labelled self-review** throughout.

No artifact named in this report is undelivered. Every path above exists and was read back.
