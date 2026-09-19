# Skill development assessment — `dev`

## Identity and conclusion

| Item | Value |
| --- | --- |
| Run | `20260918T202845Z` |
| Target | `C:\Projects\DevForgeAI\.claude\skills\dev` (Claude Code) |
| Mirror | `C:\Projects\DevForgeAI\src\claude\skills\dev` — byte-identical |
| Package digest | `45dd959122125222d68e6f156d72fa20bd52ec50d5fa095857603b0166cbe2f9` |
| Rule set | revision `2026-09-17.1`, 16 rules selected, 9 required |
| Intended user outcome | Independent assessment of the selected `dev` skill package, with findings and a proposed revision for review |
| Review character | **Self-review by the validating agent**, with two host `Task` trials executed in their own contexts. A subagent is not an enforced permission boundary; the structural, semantic and adjudication work in this report is the primary agent's. |
| `assessment_completed` | **true** |
| **Outcome** | **FAIL** |
| Builder readiness | **REVIEW_REQUIRED** |
| Proposal review state | **pending** |

`assessment_completed: true` and outcome `FAIL` are separate axes: the review was finished with honest
observations, and it concluded that one required check fails.

**One defect drives the FAIL.** The package is otherwise in good shape — 32 structure checks pass, all 24
internal links resolve, the workflow traces cleanly end to end, and the description routes correctly. The
failure is a single sentence that claims a host-enforced boundary which does not exist.

---

## Origin, sources and preservation

**Origin.** `origin_kind: existing_spec`, `history_kind: observed`, `historical_origin: unknown`.

The governing specification is `docs/specs/dev-skill-spec.md` (`DEVFORGEAI-DEV-SKILL-001`, `skill_name: dev`),
captured byte-exact at `inputs/dev-skill-spec.md`. Three provenance facts matter:

1. **The validator's bounded lookup roots do not contain it.** `docs/design/specs` does not exist and
   `docs/plan` holds no dev specification. This was **not** treated as absence — the specification exists,
   self-identifies at its own absolute path, and explicitly records that builder name-based lookup searches
   elsewhere. No origin specification was reconstructed. (`ORG-U1`)
2. **It specifies a Codex skill.** Its authoring-metadata table names `src\agents\skills\dev` as the final
   development package. The assessed Claude Code package is a derived port that no specification governs.
   (`ORG-U2`, finding `F-7eb942c2…`)
3. **Its frontmatter is stale.** `status: proposed` / `package_status: not_authored` while three copies exist
   on disk. Repository instructions already record this as stale; it is not read as unbuilt. (`ORG-U3`)

**Port history.** The Claude Code variant differs from its Codex parent in 3 of 11 files; the other 8 are
byte-identical. The conversion is otherwise clean — no `$skill-name` syntax, no `agents/*.yaml`, no residual
Codex host references. No builder authoring record accompanied the port, so history is inferred from the byte
delta rather than verified (`ORG-U4`). The port added the `allowed-tools` list, improved the description,
renamed the host, and introduced the one defective sentence.

**Preservation.** Snapshot `COMPLETE`: 11 files, 33.0 KiB, no exclusions, no links or junctions followed,
well within the 2,000-file / 32 MiB ceiling. Exact bytes at `source/` with `source-manifest.json`.

**Source freshness.** `claude-code-skills` — **live_verified** 2026-09-18, the controlling passage retrieved
and retained at `inputs/rule-sources/claude-code-skills-allowed-tools.md` before it was cited. The retained
extract is a model-produced quotation of the live page, not a byte-exact page capture, and the digest covers
the extract. `rules-snapshot` and `claude-frontmatter-guidance` — **snapshot_only**, revision `2026-09-17.1`.
`project-spec` — exact in-repository bytes.

---

## Assessment dimensions

| Dimension | Outcome | Required evaluated / total | Notes |
| --- | --- | --- | --- |
| Standards compliance | **PASS** | 4 / 4 | One advisory divergence, not a defect |
| Workflow correctness | **PASS** | 3 / 3 | 7 steps, no gaps |
| Instruction quality | **FAIL** | 6 / 6 | One unenforced control claim |
| Behavioral evaluation | **INCOMPLETE** | 3 / 5 | Both trials passed; two native checks NOT_RUN |
| Enforcement recommendations | *descriptive* | — | 4 candidates, none implemented |

Overall required coverage: **16 of 18** required checks evaluated. FAIL precedence does not erase the
`NOT_RUN` rows — `C-BEH-002` (native implicit activation) and `C-BEH-003` (host application of
`allowed-tools`) remain unperformed with *unknown* applicability, not inapplicable.

Behavior is INCOMPLETE rather than PASS **despite both trials passing**, because two required behavioral
checks could not be performed in this session. That is the honest reduction: an unperformed check is not a
passed one.

### Standards — PASS

`SKILL.md` present with frontmatter at the first line; `name: dev` matches the directory; the description is
537 characters, inside both the 1,024 specification cap and the 1,536 Claude Code listing cap. Three
frontmatter keys, all supported. Snapshot complete with no exclusions.

**Recorded divergence, not a defect (`C-STD-004`, NOT_RUN by design):** `allowed-tools` is a YAML list, which
Claude Code accepts and the Agent Skills specification does not define. The package is valid on its declared
host and non-portable to a host implementing only the specification. Failing it here would fail a legal
Claude Code package against a specification it does not claim.

### Workflow — PASS

Seven steps traced from cited entrypoints in `workflow-map.json`. Every step has entry conditions, inputs
with a producer, an executor, outputs, completion evidence, a next or terminal target, and a cited failure
route. No input lacks a producer; no step is unreachable; no branch lacks a failure exit. Creation is
correctly separated from delivery — `failure-delivery.md:17` requires destination readback before `VERIFIED`
or `COMPLETE`, and `:29` reports external acceptance separately from development status.

All 24 internal links resolve with correct relative roots. Manual review beyond the helper's declared blind
spots (reference-style links, HTML anchors, Setext headings, fragment anchors) found none present. No orphan
resources: all six assets and all four references are reachable from the entrypoint.

### Instructions — FAIL

One required check fails; five pass.

The ceremonial review found **no** unbounded ritual, self-scoring loop, or repeat-until-perfect instruction.
Every emphatic `never` in the references attaches to an observable action with a stopping criterion — never
append an unexecuted template row, never overwrite an earlier failure, never exclude uncovered owned
behavior, missing measurement is unperformed rather than an estimated pass. Those classify as
`useful_instruction`; emphasis alone is not a defect. The six asset templates carry bracketed placeholders
only, with no pre-filled `PASS`/`COMPLETE` claim presented as an observation.

The failure is a single `unenforced_control_claim` at `SKILL.md:33`, detailed below.

---

## Findings and contextual ceremony review

### `F-c3d23eda…` — unenforced control claim · **major** · `PRJ-003` · `SKILL.md:33` (bytes 2106–2331)

> That separation is structural here rather than asserted: `Skill` and `Task` are absent from
> `allowed-tools`, so this workflow cannot invoke another skill or spawn a subagent.

The live Claude Code skills reference states the opposite:

> The `allowed-tools` field grants permission for the listed tools during the turn that invokes the skill…
> **It does not restrict which tools are available: every tool remains callable, and your permission settings
> still govern tools that are not listed.**

The field that removes tools from the pool is `disallowed-tools`, which this package does not use. Absence
from `allowed-tools` therefore produces a permission prompt for an unlisted tool under default settings — not
an inability to call it.

**The package contradicts itself twice on this point.** `SKILL.md:50`, added in the same port, describes the
unscoped `Bash` grant correctly as "an obligation this workflow keeps, **not one the allowlist enforces**."
And `references/implementation.md:13` states that "separately authorized delegation must preserve ownership
and evidence" — which presupposes delegation is possible. Lines 33 and 50 apply opposite models of the same
frontmatter field, seventeen lines apart.

The passage has **no counterpart in the Codex parent**. It was introduced by the port, in prose that no
specification governs — which is exactly the gap the companion finding describes.

**User impact.** A reader who trusts line 33 believes a host-enforced boundary exists where only an
instruction does. The risk lands precisely in the scenario the sentence was written to address: prompt
content attempting to expand scope. The skill's functional behavior is unaffected, which is why this is major
rather than a blocker.

**Preserved requirements.** The substantive instruction not to delegate product implementation, and its
resistance to later instructions asking for delegation, must survive any rewording. Only the false claim
about the mechanism is removed.

**Proposed correction.** `RR-001` offers two dispositions — state the boundary honestly as an obligation
(recommended), or make it real with `disallowed-tools: [Skill, Task]` and describe it accurately as
turn-scoped. **`OQ-1` is the maintainer's decision**; the validator recommends but does not choose, because
option (b) changes runtime tool availability.

### `F-7eb942c2…` — no governing specification for this host variant · **minor** · `PRJ-001`

The only specification naming `dev` specifies a **Codex** skill and names `src\agents\skills\dev` as its
build target. The assessed Claude Code package is a derived port with no contract of its own. Eight of its
eleven files are byte-identical to the parent; the three that differ carry every host-specific decision —
including the defective passage above. Specification conformance could not have caught it, because no
specification covers those bytes.

Two adjacent observations are recorded but are **not** package defects: the stale specification frontmatter,
and the lookup-root mismatch that the specification itself anticipates.

### Family pattern — observed, not assessed

The same claim pattern appears in four sibling packages this run **did not assess**: `qa:55`,
`skill-builder:27`, `skill-validator:32` and `advisor:27`. Each package that makes the false claim also
states the correct model elsewhere in the same paragraph, so this reads as one inconsistent mental model
replicated across the family rather than four independent errors. `advisor`'s wording is defensible — it
states design intent, not enforcement. **This came from a string search, not an assessment.** Validating
those packages requires selecting them in their own runs; `OQ-2` records the decision.

---

## Trials and limits

### `T1-routing` — **PASS**, 10/10

A cold `Task` agent classified ten predeclared prompts using only the five sibling skill descriptions, with
expected labels sealed in `expected.json` and never shown to it. All four positives routed to `dev`; all six
near-misses routed away. The three near-misses owned by siblings each went to the **correct** sibling, so the
boundary discriminates rather than merely declining. The classifier's stated reasons cite `dev`'s own
exclusion clause for the spec-drafting, deployment and review-only cases, indicating those exclusions do
observable work.

### `T2-cold-workflow` — **PASS**

A cold `Task` agent was given only the entrypoint path, a synthetic specification, a work directory and the
outcome. No expected result, no hint about the fixture's traps, and no correction were injected. It ran 20
minutes, 63 tool calls, and produced 40 files. **Every claim below was re-verified by the validating agent
against the retained bytes; the executor's own report was not accepted as evidence.**

The fixture carried two deliberate traps.

**The destination trap.** The specification named the evidence destination `build evidence/run one` — two
multiword components with spaces. `references/context.md:15` instructs at length never to shorten a
multiword directory by treating one word as descriptive prose. The evidence landed at exactly
`build evidence/run one`: no `build/` + `evidence/` word-split, no hyphenated variant, no generic default
directory. The instruction held under a cold read by an agent that had never seen it.

**The boolean trap.** Requirement R4 required rejecting a non-integer price, with booleans explicitly
included — and in Python `isinstance(True, int)` is `True`, so a naive guard silently passes. This was
caught **by a failing test, not by inspection**: `logs/A006.err` records exactly three `FAIL` lines for the
float, `True` and `False` cases before any guard existed. The implementation then tests `isinstance(…, bool)`
before the `int` check.

Verified independently:

| Claim | Verification |
| --- | --- |
| 12/12 required cases pass | Re-ran the suite: `Ran 12 tests … OK`, exit 0 |
| Candidate digests | `sha256sum` matches the reported values for both files |
| Genuine red→green cycles | 10 attempts with coherent exit codes: setup 0, red 1, green 0, red 1, green 0, red 1, green 0, refactor 0, integration 0, qa 0 |
| Refactor preserved behavior | `logs/A007.err` and `logs/A008.err` are **byte-identical** (`c49434fd…`) — corroborated, not re-asserted |
| Every requirement accounted | `traceability.md` references R1, R2, R3, R4 individually |
| Containment | 40 files, all under the permitted write root; nothing outside `docs/plan/skill-validations/`; no install, no network |

Three behaviors are worth naming because they are what the references ask for and are easy to fake:

- **Acceptance was kept separate from completion.** External framework acceptance was reported
  `NOT_EVALUATED` rather than inferred from development `COMPLETE`, as `failure-delivery.md:29` requires.
- **No threshold was imported from the enclosing repository.** The fixture declared one metric; the
  repository's ≥95% coverage floor was correctly *not* applied, matching the portability contract.
- **The executor disclosed two of its own process errors** — including a first `slice-plan.md` draft that it
  says pre-filled anticipated exit codes before any command ran, replaced before execution. What is
  verifiable here is the **disclosure and the corrected state**: the retained `execution-record.jsonl` parses
  cleanly and contains no value contradicted by the logs. No bytes of the pre-corrected draft exist, so the
  original error's contents were not independently confirmed — `attempt-001.json` records this as
  `CONFIRMED_AS_DISCLOSED` rather than `CONFIRMED`. Taken at that weight, it is still the behavior
  `evidence-resume.md:3` asks for, applied by the agent to its own work.

**Harness limitation, recorded not hidden (`C-BEH-007`, ERROR):** the plan declared a 600-second ceiling for
a whole native session; the task ran 1,178 seconds and the runner did not terminate it. The recorded limit
was not the effective limit. This is a defect in the trial harness, not in the target, and the ceiling was
retained rather than silently raised.

### Separation of evidence types

| Evidence type | Status |
| --- | --- |
| Structural checks (`observe.py structure`) | Executed — 32 checks, all PASS |
| Deterministic accounting (`observe.py records`) | Executed — 0 errors, 39 references verified |
| Manual link and anchor review | Executed — no unsupported forms present |
| Semantic review | Primary agent, self-review |
| Routing classification | Executed in a cold `Task` context — 10/10 |
| Task behavior | Executed in a cold `Task` context — trial `T2`, PASS, independently re-verified |
| **Native implicit activation** | **NOT_RUN** — the host was never observed selecting this skill through its own discovery. Explicitly loading the entrypoint is not that observation. Applicability is *unknown*, not inapplicable. |
| **Host application of `allowed-tools`** | **NOT_RUN** — trial `T2` runs as a `Task` subagent reading the entrypoint as instructions, so the host never applied this package's frontmatter grant. Finding `F-c3d23eda…` rests on the documented behavior of the field, not on an observed refusal. |

### Limits

- Self-review. Subagents supplied cold contexts for two trials but are not an enforced permission boundary
  and share this session's authentication and budget.
- Single attempt per trial; no variance estimate across repeated samples.
- `snapshot_only` freshness for the bundled rule catalog; the one controlling passage was refreshed live.
- The `T2` fixture is small and single-language. It exercises the workflow's shape, not its behavior on a
  large multi-document specification set.
- The declared trial timeout was not enforced by the runner (`C-BEH-007`).

**Source readback: `MATCH`.** `readback` against the original target returned an empty changed list, so
`source_readback_state` is `UNCHANGED` and conclusions apply to the **current** bytes, not only to the
retained snapshot. `source-after-manifest.json` records the post-assessment state. Nothing here is labelled
`SOURCE_CHANGED`, and current-byte readiness is not blocked on that ground.

---

## Proposed changes and review

`revision-spec.md` proposes three mandatory fixes (`RR-001` remove the claim, `RR-002` keep the two allowlist
passages consistent, `RR-003` apply to both mirrored paths) and one optional enhancement (`RR-004` record a
governing contract for the variant). Everything not named there is preserved unchanged — the workflow, all
six assets, all four references, the resource graph, and the `name` and `description` fields.

Two decisions are unresolved and are **not** guessed: `OQ-1` (obligation or real restriction) and `OQ-2`
(whether to open runs on the four sibling packages).

`enforcement-recommendations.md` records four candidates — detecting frontmatter-as-enforcement claims,
backing stated boundaries with `disallowed-tools`, keeping the mirrored trees identical, and binding a
specification to each host variant. **None is implemented, and none is an acceptance gate.** Each records its
own bypass and coverage limits; notably, `disallowed-tools` is turn-scoped rather than session-long, and a
local Git hook is bypassable in a way a hosted check is not.

## Next action

**Answer `OQ-1`**, then decide `OQ-2`. No builder invocation before that, because the answer determines
whether the frontmatter changes.

**Why `REVIEW_REQUIRED` and not `BLOCKED`.** One unresolved contract question exists — `ORG-U2`, no
specification governs this host variant. It is **not material to this change set**: `RR-001`'s correction is
derived from the live Claude Code reference rather than from any specification, and acceptance cases `AC-1`
through `AC-4` are verifiable against the package itself. That is why `RR-004` is an optional enhancement
rather than a prerequisite. The baseline is verified — exact bytes retained, readback `MATCH` — and no
adoption capability is needed for a scoped edit to an observed package. Review has simply not happened yet,
and pending review alone is `REVIEW_REQUIRED`.

The validator did not repair the target, install anything, or invoke `skill-builder`. All writes are confined
to this run directory — `git status` shows `docs/plan/skill-validations/` as the only untracked path and the
target package unmodified. No operational installation or Rust qualification is implied by anything here.

| Artifact | Path |
| --- | --- |
| This report | `docs/plan/skill-validations/dev/20260918T202845Z/validation-report.md` |
| Proposed revision | `…/revision-spec.md` |
| Findings | `…/findings.json` |
| Checks | `…/checks.jsonl` |
| Workflow map | `…/workflow-map.json` |
| Origin record | `…/origin-record.json` |
| Enforcement register | `…/enforcement-recommendations.md` |
| Handoff | `…/handoff.json` |
| Exact bytes assessed | `…/source/` + `…/source-manifest.json` |
| Trials | `…/trials/T1-routing/`, `…/trials/T2-cold-workflow/` |
