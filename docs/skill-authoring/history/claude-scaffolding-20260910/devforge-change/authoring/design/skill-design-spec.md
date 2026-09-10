# Skill design specification — devforge-change

Working design document, filled from the template at
`providers/claude/plugins/devforgeai/skills/devforge-project-expert-creator/assets/skill-design-spec.md`
at builder revision `4999f3106565c5e320d1f1a7db066b437e4e94be`. The template was read from git
object storage and filled here, at the project artifact location — never in place inside the
builder package.

This is a DevForgeAI authoring document. It carries the design, the framework authority and
source mapping, and the change record. It certifies nothing, and completing it establishes
nothing about behaviour.

**No questions were asked of a user.** This assignment directed that every material decision
be recovered from the specification, templates and contracts, and that anything they leave
silent be recorded as a labelled proposed default. Proposed defaults are marked
**PROPOSAL** throughout and are not user requirements.

## 1. Identity and purpose

**Skill name:**
`devforge-change`

**Purpose:**
Turn a change trigger — feedback, a defect, a dependency update, a decision that no longer
holds — into a bounded change proposal carrying the affected artifact revisions and the
correct return path. Project-specific guidance changes the result because the answer to
"what does this break" is entirely a function of this project's accepted artifacts, their
declared references, and which of its skills are actually installed.

**Description for discovery:**
The frontmatter `description` in the authored `SKILL.md`. It states what the skill does, the
activating conditions in direct and indirect phrasing drawn from the specification's
use-case inventory, and the near-miss exclusions each naming the sibling that owns them.
Claude uses this text to decide automatic invocation, and the combined `description` and
`when_to_use` text is truncated at 1,536 characters in the skill listing; the authored
description is 1,034 characters and carries the key use case first.

**Intended users or role:**
Anyone holding a change trigger against a project with accepted DevForgeAI artifacts. Not a
role; the skill is selected by the request.

## 2. Scope and activation

**Use this skill when:**
A concrete change trigger exists and the question is what it invalidates and who revises it
first — an amendment request against an accepted architecture rule or decision; an external
release or customer request that undermines a recorded assumption; a review or release that
surfaced a conflict with a governing decision; an expert, story or installed package that
looks stale because something upstream moved.

**Outside its scope:**

| Excluded work | Owner |
| --- | --- |
| Implementing a story that is accepted and unchanged | `devforge-develop` |
| Early exploration with no accepted artifacts to invalidate | `devforge-brainstorm` |
| Authoring or refreshing an expert package after a change is agreed | `devforge-project-expert-creator` |
| Grading a package's behaviour | `devforge-evaluate-expert` |
| Reviewing a candidate for correctness and readiness | `devforge-review` |
| Performing the revision of any affected artifact | The owning skill for that artifact |

The specification's own exclusion — "routine work already covered by an accepted story does
not need a new change process" — is the load-bearing one and appears verbatim in substance in
the description.

**Example activating requests:**

- "Use DevForgeAI to assess this change and identify what must be updated." (the
  specification's direct request)
- "A new library version or customer request changes our assumptions; what does that
  invalidate?" (the specification's indirect request)
- "We want to amend the accepted rule that conflicts are resolved server-side. What's the
  impact?"
- "The story contradicts the architecture contract. Which one is supposed to give?"

**Near-miss requests that must not activate it:**

- "The story is signed off and the criteria haven't changed. Write the query builder change
  and its tests." → `devforge-develop`
- "We agreed the expert needs updating for the new API. Go ahead and rewrite it." →
  `devforge-project-expert-creator`
- "Review this candidate for correctness and readiness." → `devforge-review`
- "Change the timeout in the config from 30 seconds to 60." → ordinary assistance; the word
  "change" is not the trigger.

**How it should be invoked:**
**PROPOSAL** — automatically when relevant and explicitly by name, the DevForgeAI default.
The specification says "the user can invoke the skill in an ordinary subscribed terminal once
it is installed and discovered" and says the MVP uses manual invocation, not scheduled
self-updating experts; it does not restrict model invocation, so the default stands. No
`disable-model-invocation` or `user-invocable` field is set: the package uses the two-field
frontmatter form.

## 3. Inputs and expected results

**Required inputs** (from the specification's inputs table, extended with the two the
execution contract makes necessary before any write):

| Input | Requirement | Consume only |
| --- | --- | --- |
| Change trigger or feedback | Required | Observed defect, user request, release feedback, or verified external update |
| Affected current artifacts | Required | Exact idea/product/design/architecture/story/expert/candidate identities |
| release-record, review-report, or expert-evaluation-report | Conditional | The evidence motivating the change |
| Declared dependency and provenance links | Required for impact | `upstream` entries, stable section IDs, recorded bindings |
| Existing decision authority | Required before a disposition | Actual adoption or a standing instruction whose scope reaches this change |
| Session assignment, worktree and write fence | Required before writing | Who owns the destination |
| Installed package copies and active runs | Optional | Generated copies and in-flight work a source change also invalidates |

**Optional inputs:**
Prior change-requests touching the same artifacts; a project artifact map in `CLAUDE.md` or
`AGENTS.md`.

**When information is missing:**
The fact stays missing, recorded in `missing_inputs` with the work it blocks, and the
analysis that does not depend on it continues. Nothing may be inferred into a revision,
digest, owner, approval or dependency edge. The skill stops only for the three conditions in
its Stopping section: an unattributable trigger, absent authority for a consequential
amendment, or a conflicting write fence.

**Expected deliverable:**
One `change-request` (ID prefix `CHG`) plus a handoff.

**Output format and destination:**
`assets/change-request.md` and `assets/handoff.md`, both package-local copies of the
governing templates. An externally selected destination governs; a project artifact map
applies only when nothing was selected. **PROPOSAL** — where neither exists, the skill
describes the project's own map as the default rather than hard-coding a path; the
specification names no default directory and inventing one would be a constraint nobody set.

**Completion criteria:**

- The trigger is attributed to a source actually read and classified as a defect against
  agreed behaviour or as new scope.
- The impact graph names direct and transitive dependents with identities, and states its own
  coverage limits.
- The disposition is recorded with its authority cited, or the missing decision is named with
  its owner.
- Routing and refresh rows name real owners and real next actions.
- The change-request and handoff exist, their declared references resolve, and no accepted
  artifact was revised and no owning skill invoked.

## 4. Workflow

| ID | Level and parent | Action | Decision or expected result | Optional or required? | Enforcement route |
|---|---|---|---|---|---|
| W1 | Workflow; no parent | Assess a change and route its dependents | A change-request and a handoff, or a recorded decline | **PROPOSAL** required — this is the skill's whole deliverable | R1 |
| P1 | Phase; parent W1 | Capture | Trigger attributable; defect distinguished from new scope | **PROPOSAL** required | R1 |
| P2 | Phase; parent W1 | Trace impact | Direct and transitive dependents listed with uncertain coverage disclosed | **PROPOSAL** required | R1 |
| P3 | Phase; parent W1 | Decide | Clear disposition without inventing approval | **PROPOSAL** required | R1 |
| P4 | Phase; parent W1 | Route and verify | Affected work stays stale or blocked until the required new evidence exists | **PROPOSAL** required | R1, R2 |
| T1 | Task; parent P1 | Record the current accepted behaviour by artifact, revision and section | An exact citation, or a recorded inability to make one | **PROPOSAL** required | R1 |
| T2 | Task; parent P2 | Resolve each declared upstream reference to actual bytes and check the digest | Resolved, mismatched, missing-with-preserved-copy, or unresolved | **PROPOSAL** required | R1 |
| T3 | Task; parent P2 | Include generated copies, bound evaluations and active runs in the graph | Rows distinct from their sources | **PROPOSAL** required | R1 |
| T4 | Task; parent P3 | Cite the authorizing decision or name the missing one and its owner | Authority recorded separately from disposition | **PROPOSAL** required | R1 |
| T5 | Task; parent P4 | Check what is actually installed before naming an owning skill | Installed / not installed / capability gap | **PROPOSAL** required | R2 |
| T6 | Task; parent P4 | Write the refresh and verification plan with every state at proposed | A plan with owners and pinned inputs | **PROPOSAL** required | R2 |

Every classification above is a proposed default. The specification states these four phases
and their exit conditions as required behaviour, which is the basis for proposing "required";
no user has classified them.

**Applies when:**
P2's installed-copy and active-run sweep applies only where such copies or runs exist and are
readable; where they are not, that is a coverage limit, recorded, not a skipped step. The
conditional input row (release-record / review-report / expert-evaluation-report) applies only
when such a record exists.

**Dependencies and completion evidence:**

- P3 waits on P2: a disposition without an impact graph is a guess. Evidence of P2 is the
  populated impact table including its coverage column. It goes stale when any listed identity
  changes.
- P4 waits on P3: routing without a disposition invents the classification. Evidence is the
  recorded classification and its authority citation.
- The refresh rows themselves produce no completion evidence in this skill. Each names the
  artifact or receipt that would show it done, written by the owner named in the row.

**Conditional paths:**
A trigger classified as an in-scope implementation repair inside unchanged criteria exits at
P3 with a short routing answer to the implementation skill; P4's full refresh plan does not
apply and a change-request may legitimately not be produced. This is the specification's
"small implementation fixes inside unchanged criteria return directly to develop".

**When to stop or seek clarification:**
An unattributable trigger; absent authority for a consequential amendment; a conflicting write
fence at the assigned destination.

## 5. Task-specific rules

**Required standards or conventions:**

- Fixed result vocabulary: `NOT_EVALUATED`, `NOT_RUN`, `COULD_NOT_RUN`, `NOT_APPLICABLE`,
  never blended.
- `devforge.artifact/v1` envelope on the change-request; no artifact carries its own digest;
  hash after bytes are final; read every repeated reference back after the last write.
- A surviving `{{placeholder}}` in a required field means draft, not ready.
- Package-relative links only; no dependency on `docs/mvp` at runtime; no developer home path
  anywhere in the package.
- Only documented, implemented DevForge commands may be named as executable gates.

**Preferences:**
Prose over checklists in `SKILL.md`; conditional detail in references loaded at the phase that
needs them.

**Actions requiring explicit authorisation:**
Adopting a proposal; revising any accepted artifact; upgrading a pinned dependency; invoking
an owning skill. None of these is performed by this skill under any circumstances.

**Known pitfalls:**
The three named at the top of `SKILL.md` — inventing approval, doing the work instead of
routing it, and a confident impact graph with a silent hole. The third is specific to this
skill and is the reason the coverage column is required rather than optional.

## 6. Tools and supporting resources

**Target environment:**
Claude Code on Linux/WSL2, in a consuming project. No model API key. The DevForge CLI may or
may not be present; the skill is written to work without it.

**Required tools or integrations:**
File reading in the consuming project. Nothing else is required. A skill grants no tool
permissions.

**Supporting materials:**

| Resource | Purpose | When it is needed |
|---|---|---|
| `assets/change-request.md` | The output template | At Output |
| `assets/handoff.md` | The handoff template | At Output |
| `references/impact-tracing.md` | Reference resolution, what belongs in the graph, ownership map, coverage limits | At Trace impact and Route |
| `references/recording-rules.md` | Envelope fields, upstream vs evidence, digest ordering, placeholders | At Output |
| `references/cli-boundaries.md` | Which commands exist and what each proves; the five missing checks | Wherever a command or a gate is about to be named |
| `references/sources.md` | External source claims and their retrieval date | On a client or packaging question |
| `references/derivation.json` | Package provenance | On a refresh |

No `scripts/`. Nothing in this workflow is a repeated deterministic operation, and a helper
here would have to either read project artifacts (judgement, not determinism) or restate a
check the Rust CLI owns.

**Unavailable dependency behaviour:**
Record `COULD_NOT_RUN` with the actual cause and what it blocks; continue the independent
work. Never report an absent error as a pass.

**Enforcement route for required items:**

- **Route ID and covered items:** R1 — W1, P1, P2, P3, T1, T2, T3, T4.
  - **Requirement and protected action:** A change-request may not be presented as complete
    unless its trigger is attributed, its impact table carries a populated coverage statement,
    and its disposition cites an authority or names a missing decision. Protected action:
    downstream consumption of the change-request as the basis for a revision.
  - **Observable evidence:** The change-request's own populated fields, and the resolvability
    of each `upstream` entry it declares. Distinguishable from a self-reported marker because
    the references either resolve or do not.
  - **State and freshness:** Lives in the change-request at its recorded destination, written
    by this skill. Invalidated when any cited identity changes.
  - **Intended allow or refuse behaviour:** Refuse to treat the change-request as a basis for
    a revision when a required field is empty, holds a placeholder, or declares an upstream
    entry that does not resolve. A warning is advisory, not a refusal.
  - **Missing evidence and errors:** Missing or unresolvable evidence refuses; an unreadable
    store is `COULD_NOT_RUN`, distinct from a refusal.
  - **Recovery and user message:** Name the unresolved field or reference and its owner; the
    change-request stays draft.
  - **Owner:** Integration owner. The check is compiled into the DevForge CLI and invoked by
    whatever wiring that owner selects.
  - **Feasibility:** Unknown until the integration owner confirms it. Nothing in the CLI reads
    a `devforge.artifact/v1` envelope today.
  - **Status:** Requirement recorded. No gate is implemented, activated or executed by this
    skill.

- **Route ID and covered items:** R2 — P4, T5, T6.
  - **Requirement and protected action:** Affected work stays stale or blocked until the
    required new evidence exists. Protected action: relying on an evaluation, installed copy
    or candidate whose governing source has changed.
  - **Observable evidence:** A comparison between an artifact's recorded upstream digest and
    the current bytes at that locator; for a generated copy, a comparison between the copy and
    the source it was generated from.
  - **State and freshness:** Would live in the consuming project, written by the CLI. Goes
    stale on any write to either side of a comparison.
  - **Intended allow or refuse behaviour:** Refuse the dependent action while a governing
    source's digest differs from what the dependent recorded.
  - **Missing evidence and errors:** No recorded upstream digest is `COULD_NOT_RUN`, not a
    pass. An unreadable installed copy is likewise.
  - **Recovery and user message:** Name the drifted pair and the refresh row that would close
    it.
  - **Owner:** Integration owner.
  - **Feasibility:** Unknown. `devforge expert status` implements the nearest thing — one bound
    expert against its own recorded binding — and its scope does not reach stories, contracts,
    reports, candidates or installed skill copies. Recorded as **Enforcement requested; not
    confirmed available.**
  - **Status:** Requirement recorded. No gate is implemented, activated or executed by this
    skill. `references/cli-boundaries.md` states this in the package itself so a worker cannot
    mistake the requirement for a check.

## 7. Acceptance cases — capture only

Written before the candidate, from the specification's acceptance table and its four
additional common cases. Captured, not executed. They are carried into `evals/evals.json`
(nine tier-B cases) and, for the deterministically observable parts, into `evals/cases.jsonl`.

| Case | Example request or input | Expected behaviour |
| --- | --- | --- |
| Direct activation | Request impact analysis for an architecture amendment | Identifies governing records and dependent stories, experts and runs |
| Indirect activation | Mention a new package release | Verifies relevant facts and proposes an upgrade without silently applying it |
| Unchanged semantics | Fix a typo outside governed behaviour | Response stays proportionate; no unrelated reevaluation is forced |
| Transitive drift | An API revision affects an expert used by a story | Marks the chain for review; records installed-copy refresh and reevaluation |
| Out of scope | Ask to implement an unchanged ready story | Routes to develop without reopening adopted decisions |
| Concurrent writer | A second session claims the same worktree and branch | Dependent writes stop; the collision is reported; nothing is deleted or reset |
| Stale upstream | A candidate cites a revision that has been superseded | Prior evidence marked stale; a new check routed; preserved bytes cited at the preserved path |
| Placeholder in a required field | The "before" behaviour cannot be recovered from any artifact | Recorded in `missing_inputs`; no placeholder survives; result stays a draft |
| Check cannot execute | No CLI, no policy, expert directory unreadable | `COULD_NOT_RUN` with the actual cause; absence of an error is not PASS |

**Example of a good deliverable:**
None supplied. A worked change-request would either be synthetic — and therefore a fixture,
which belongs in `evals/fixtures/` and is stripped from installed copies — or real, and this
package has no real project. Shipping a filled template as an asset is the specific defect the
authoring contract's placeholder rule exists to prevent.

## 8. Placement and maintenance

**Availability:** Bundled in the `devforgeai` Claude plugin.

**Installation location:** Recorded in section 10. An installed copy is never an alternative
source.

**Maintainer:** The Claude provider skill author, under the integration owner for anything
shared.

**Reasons to revisit:** A new revision of SKILL-012; a change to the change-request or shared
handoff template; a change to the artifact, execution or skill-authoring contract; a new
implemented DevForge subcommand or a newly implemented missing check; another Claude skill
being added, which dates the installed-inventory statement in `impact-tracing.md`; a change to
the `devforge-evaluate-expert` runner schema.

## 9. Authoring decision and progress

**Current status:** Authored scaffold. Draft. Not validated, not evaluated, not installed.

**Working specification and target paths:**
This document at
`docs/skill-authoring/history/claude-scaffolding-20260910/devforge-change/authoring/design/skill-design-spec.md`;
target skill directory
`providers/claude/plugins/devforgeai/skills/devforge-change/`.

**Search scope and limitations:**

Searched, at base `c17e758417da64928a0f47fc2600304465ac3f3c` in the assigned worktree:

- `providers/claude/plugins/devforgeai/skills/` — the assigned provider's canonical source
  inventory. Four entries: `devforge-brainstorm`, `devforge-develop`,
  `devforge-project-expert-creator`, `devforge-review`. No `devforge-change`.
- `docs/mvp/roster.md` — SKILL-012 is listed with current source "Proposed".
- `docs/skill-authoring/history/claude-scaffolding-20260910/` — the coordinator's evidence
  tree, for a destination collision. The `devforge-change` directory existed and was empty.

Not searched, and recorded as unreachable rather than empty: any personal `~/.claude/skills/`
inventory, enterprise managed settings, claude.ai account-synced skills, and any `--add-dir`
directory. Those are runtime discovery locations for a consuming session and are not part of
this assignment's fence; a bounded source search cannot speak for them.

Not compared: the Codex provider's inventory. Provider sources have distinct ownership and a
Codex skill is not a candidate for a Claude assignment.

**Related skills:**

| Candidate and source | Relevant overlap | Gap or meaningful distinction | Recommendation |
|---|---|---|---|
| `devforge-brainstorm` (`providers/claude/.../devforge-brainstorm`) | Both read a change-request; brainstorm consumes one as input | Brainstorm explores undeveloped intent and owns the idea ledger. It has no impact-tracing scope and no routing responsibility. Its own SKILL.md names `devforge-change` as specified and absent | Separate workflow |
| `devforge-develop` (`providers/claude/.../devforge-develop`) | Both act on a defect report | Develop implements one governed story under an unchanged criterion. The specification routes small fixes inside unchanged criteria directly to it, which is a boundary, not an overlap | Separate workflow |
| `devforge-project-expert-creator` (`providers/claude/.../devforge-project-expert-creator`) | Both handle "an expert went stale" | The creator performs the refresh and owns the expert package. This skill decides whether a refresh is warranted and routes it. Its own reference material treats an evaluator's change request as an input, not as work it originates | Separate workflow |
| `devforge-review` (`providers/claude/.../devforge-review`) | Both can surface a conflict with a governing requirement | Review judges a candidate against its criteria; the roster's dashed edge sends the governing-requirement conflict from review to change. That edge is the distinction | Separate workflow |

**Selected approach and rationale:**
**Create.** No suitable skill was found in the searched inventory. The distinction is stated in
terms of activation and scope, not subject matter: nothing installed activates on "what does
this change invalidate", and nothing installed owns the impact graph or the routing decision.
Creation is what the assignment directs and what the roster's "Proposed" status describes. This
is not a claim of global uniqueness; it is the result of the bounded search recorded above.

No destination collision: the package directory did not exist, and the evidence directory
existed and was empty.

**Requirements, defaults and open decisions:**

| Item | Requirement or decision | Basis | Status |
|---|---|---|---|
| Four phases and their exit conditions | Capture / Trace impact / Decide / Route and verify | SKILL-012 workflow table | Settled by specification |
| One output artifact, `CHG` prefix | change-request from the governing template | SKILL-012 outputs table | Settled by specification |
| Nine acceptance cases | Five specification rows plus four common cases | SKILL-012 validation section | Settled by specification |
| Two-field frontmatter | `name` and `description` only | Assignment and DevForgeAI package convention | Settled by assignment |
| No `scripts/` | Nothing deterministic and repeated to automate | Assignment prefers none; authoring contract permits when justified | **PROPOSAL** |
| Four references | impact-tracing, recording-rules, cli-boundaries, sources | Derived from what the four phases actually need | **PROPOSAL** |
| Invocation policy | Automatic when relevant and explicit by name | Client default; specification does not restrict | **PROPOSAL** |
| Default output destination | The project's own artifact map; no path hard-coded | Specification names none; inventing one would be an unset constraint | **PROPOSAL** |
| Workflow item classifications | All required | Specification states them as required behaviour; no user classified them | **PROPOSAL** |
| Trigger split | Fixed, stratified by `should_trigger` and category, ~60/40 train/validation | Authoring contract requires a fixed split; the ratio is not specified | **PROPOSAL** |
| Baseline arm | `without_skill` for every tier-B case | No previous revision of this skill exists | Settled by fact |
| Synthetic fixture project | "tidepool"; invented package `tidepool-sync` | Fixtures must be reproducible and must not imply a real project | **PROPOSAL** |

**Authored or changed files:**
Listed with digests in `../file-manifest.json`. Nothing outside the assigned fence was
written.

**Material unresolved dependencies or enforcement gaps:**
R1 and R2 are recorded requirements with no implemented check. Five specific missing
integrations are enumerated in `references/cli-boundaries.md`. The
`devforge-evaluate-expert` runner exists at `e641797eebf04cd1e8eb9f711549e038e7745407` in a
separate worktree and is itself an unevaluated scaffold; `evals/cases.jsonl` is authored
against its schema and was not executed.

**Validation status:**
Not performed.

**Enforcement status:**
Requirements recorded; no gate implemented by this skill.

## 10. Framework authority and source identity

**Framework and provider:**
DevForgeAI checkout at worktree `worktrees/claude-scaffold-change-20260910`, branch
`author/claude-devforge-change-scaffold-20260910`, base
`c17e758417da64928a0f47fc2600304465ac3f3c`. Provider: Claude. Consuming project: none — this
is framework authoring, not a project installation.

**Assignment and authority:**
Coordinator-issued scaffold packet for SKILL-012, Claude package. Exclusive fence:
`providers/claude/plugins/devforgeai/skills/devforge-change/**` and
`docs/skill-authoring/history/claude-scaffolding-20260910/devforge-change/authoring/**`.
Integration owner for anything shared: not this author. No session record artifact was
supplied, so `execution_ref` is recorded as the packet path rather than a fabricated
SESSION ID.

**Roster role:**
SKILL-012 in the accepted roster, current source "Proposed". Authoring this scaffold does not
amend the roster, change `package-index.json`, or certify a framework capability. No roster or
index file was touched.

**Selected source records:**

| Record | Governing source | Revision or artifact ID | SHA-256 | Selection authority and purpose | Gaps or conflicts |
|---|---|---|---|---|---|
| Governing design specification | `docs/mvp/specifications/skill-012-devforge-change.md` | SKILL-012, DRAFT MVP revision 2 | `b47d49ada93bf5612ea64d5c31d94e31807869316925c53b828deb9e5cbe6774` | Packet; governing | Its own header says no callable implementation is supplied |
| Skill-authoring contract | `docs/mvp/skill-authoring-contract.md` | DRAFT MVP revision 3 | `371462385b4e32d1b347f959abb779f4be4251e357c5720a9aef039113eb4b53` | Packet; authoring, provider and packaging boundary | None affecting this package |
| Artifact contract | `docs/mvp/artifact-contract.md` | selected at base | `00d8c4f4bf619b8361e056c2b77c8215595755a0eb6262b865e6a8f464c1d2b5` | Packet; envelope and reference rules | None |
| Execution contract | `docs/mvp/execution-contract.md` | selected at base | `73bca87bafd43d6b7294bad945c6506b2056d749ca22100ba4272b9a26e4e15b` | Packet; worktree and concurrency | None |
| Roster | `docs/mvp/roster.md` | selected at base | `ea35b825f8d2ea58ea0eb20b77c2fdd47df1dc2ddb3bbcfef3b032874e5f57bc` | Packet; provenance flow and consumers | Most consumers are unimplemented |
| Development language policy | `docs/development-language-policy.md` | selected at base | `3d89f39ee6d7caea84a46bdffeb39a96cd1d0bbc35d99e9435acd8ef8ca1700f` | Packet; Rust authority boundary | None |
| Bounded delivery | `docs/learned-behaviors/bounded-delivery.md` | selected at base | `22a0388c3a4afdb32beace2fb0082ec02acea885e45650f0b42925b76c09e7ae` | Packet; stopping condition | None |
| change-request template | `docs/mvp/templates/devforge-change/change-request.md` | selected at base | `1b6d4198065153934368079833fa853fc271aacbf7266444765cda7cde7e5b43` | Packet; output template | None |
| Shared handoff template | `docs/mvp/templates/shared/handoff.md` | selected at base | `abc7f8e0ca545093d3b1486d1a86cb7e51609aef17c0027b951a47da6eaed206` | Packet; handoff template | None |
| evals template | `docs/mvp/templates/skill-authoring/evals.json` | selected at base | `508b56b608f6b7f382d1e36573caf5ab0ba4db4cd6a6c4fa94adb16d0d9f5692` | Packet; base eval fields | None |
| trigger-queries template | `docs/mvp/templates/skill-authoring/trigger-queries.json` | selected at base | `8b64b614a0599aab6a52fd6ec59975e79dd698b9cba722765b0793d546e1dec4` | Packet; base trigger fields | None |
| Template for this document | builder `assets/skill-design-spec.md` at `4999f31` | `4999f3106565c5e320d1f1a7db066b437e4e94be` | `d741d4dfadbb37353f5542dbb825ab7df9bbdb7be10e4380e262f54e0f663790` is the builder's `assets/handoff.md`; this document's template was read from the same revision | Packet; builder to follow | Builder is a draft under independent review |

Every working-copy digest was verified byte-identical to the same path at
`c17e758417da64928a0f47fc2600304465ac3f3c` before any dependent write.

**Canonical source and generated runtime mapping:**

| Purpose | Selected path and provider | Identity | Ownership |
|---|---|---|---|
| Canonical framework source | `providers/claude/plugins/devforgeai/skills/devforge-change` | `../file-manifest.json` | This author |
| Installed project copy | A consuming project's `.claude/skills/devforge-change` | Not generated | Integration owner |
| Plugin export | Not generated | Not generated | Integration owner |
| Working specification | This document | — | This author |

A provider source folder by itself is not a discovered installation.

**Package derivations:**
Recorded in `providers/claude/plugins/devforgeai/skills/devforge-change/references/derivation.json`,
which is the package's maintenance record. Not duplicated here.

**Authority, contract, installation or provider gaps:**

- Six of the nine consumers the specification names for change-request output are not
  implemented in this provider. Recorded as capability gaps; not a reason to change the roster
  or to install a stub.
- No implemented check exists for R1 or R2; five specific missing integrations are enumerated
  in the package.
- The `devforge-evaluate-expert` runner is a dependency at a pinned revision in another
  worktree and is itself unevaluated.

**Preserved boundaries:**
Nothing outside the fence was written. Not touched: `docs/mvp/**` including the specification,
the templates and the contracts; `docs/mvp/package-index.json`; `docs/mvp/roster.md`; the four
sibling Claude skills; every Codex source; plugin manifests, hooks and agents; the DevForge
repository, its gates, policies, tests and `tooling_files` pins.

**Authoring and release status:**
Authored candidate. Evaluation and adoption are separate; a source identity establishes no
activation, quality or release readiness.

## 11. Evaluator repair intake

Not applicable. This is a first authoring pass, not a repair from a frozen evaluator handoff.
No evaluation report, repair specification or finding exists for this package.

## 12. Change record

**Identity and authoring scope:**
Scaffold authoring pass, 2026-09-10 UTC. Coordinator packet at
`tmp/claude-remaining-skills-scaffolding-20260910/packets/author-devforge-change.md`.
Provider: Claude. Target skill: `devforge-change`. Requested action: create.

**Input references:**
Section 10's selected source records, plus the builder package at
`4999f3106565c5e320d1f1a7db066b437e4e94be` and the runner dependency at
`e641797eebf04cd1e8eb9f711549e038e7745407`.

**Change mapping:**

| Finding IDs | Change ID | Change type | Requirement IDs | Disposition | Old path and SHA-256 | New path and SHA-256 | Summary |
|---|---|---|---|---|---|---|---|
| Not applicable | CHG-A01 | New authored package | W1, P1–P4, T1–T6, R1, R2 | applied | Absent (new package) | `../file-manifest.json` | Scaffold `devforge-change` against SKILL-012: entrypoint, two template assets, four references, nine tier-B eval cases, twelve runner cases, thirty trigger queries, fifteen synthetic fixtures |

**New canonical source manifest:**
`../file-manifest.json`. It sits outside the package so that it covers every package file
including `references/derivation.json`, and no record contains its own digest.

**Resulting specification identity:**
This document, revision 1, at the path in section 9. No prior revision exists.

**Preserved behaviour and requirements:**
No existing behaviour was changed: this is a new package. Every sibling skill, shared
template, contract and roster entry is byte-unchanged.

**Derivations and generated-copy work remaining:**
Installation and export are the integration owner's; neither was performed and neither is
implied. `evals/` must be stripped by that installation, which case `CHG-C-002` asserts.

**Deferred proposals, gaps and evaluation prerequisites:**
Every tier is `NOT_RUN`. Tier C requires an actual installed copy in a consuming project where
`docs/mvp` is unreachable. Tier B requires a run workspace and a `without_skill` baseline arm.
Tier A requires a fresh terminal and the installed package. None of these was arranged; this
assignment is authoring only.

**Finding status:**
Not applicable; no findings exist.

**Validation status:**
Not performed.

**Enforcement status:**
Requirements recorded; no gate implemented by this skill.

**Next handoff:**
`../handoff.md`. Next owner: an independent evaluator. A prepared transfer is not a receiving
invocation and authorises no evaluation, installation or activation.

## Evaluation coverage proposed

Accepted baseline: none — there is no previous revision, so every tier-B baseline arm is
`without_skill`. Capability and environment scope: Claude Code on Linux/WSL2, project-local
installation or plugin export, whichever the evaluator actually uses; the two are different
installation modes and the report must say which.

Current candidate: the package manifest in `../file-manifest.json`. Impact of this change:
the whole package is new, so no prior observation transfers to it and none exists.

Proposed coverage: tier C first, from an actual installed copy — three cases, twenty-one
deterministic assertions. Then tier B — nine cases with `without_skill` baselines and separate
clean contexts and writable outputs. Then tier A — thirty trigger queries on the fixed
stratified split, from a fresh terminal, with the skill path never supplied except in the two
`explicit_invocation` entries, which are recorded separately and never counted as implicit
activation evidence.

Missing evidence: all of it. This skill proposes evaluation coverage; a separate evaluator and
an independent reviewer assess it. No source edit closes an evaluation finding, and capturing
acceptance cases is not authorisation to run them.
