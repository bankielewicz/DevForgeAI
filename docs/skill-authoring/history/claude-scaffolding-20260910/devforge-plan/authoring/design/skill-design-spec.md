# Skill design specification — devforge-plan (Claude)

Derived from the frozen builder's package template `assets/skill-design-spec.md` at
`/home/bryan/Projects/DevForge/worktrees/claude-scaffold-project-expert-creator-20260910`, commit
`4999f3106565c5e320d1f1a7db066b437e4e94be`, source SHA-256
`715ef3bdf9082ace4c3b3eeda27e8bf9e4663355bcebed2f5d997fefc5a26ef9`. The template was copied to this
project artifact location and filled here; the package copy was not filled in place, and no
`assets/skill-design-spec.md` is shipped inside the `devforge-plan` package (it is the builder's asset,
not this skill's runtime resource).

This is a DevForgeAI authoring document. It carries the design, the framework authority and source
mapping, and the change record. It does not certify a skill, and completing it establishes nothing
about behaviour. Section 11 (evaluator repair intake) is **NOT_APPLICABLE**: no evaluator report exists
for `devforge-plan`, and this is a first authoring pass rather than a bounded repair.

**No questions were asked of the user.** The assignment prohibits them. Every material decision below
was recovered from the governing specification, the shared templates and contracts, the roster, or the
observed CLI and client documentation. Where those sources are silent, the entry is a **proposed
default** and is labelled as such. A proposal here is a design input awaiting an owner's answer; it is
not a requirement anyone gave.

---

## 1. Identity and purpose

**Skill name:**
`devforge-plan`

**Purpose:**
Break adopted delivery scope into dependency-ordered epics and bounded, independently checkable stories,
each carrying behavioural acceptance criteria that trace back to the requirement or architecture rule
they came from, plus the expert capabilities the story will need. Project-specific guidance changes the
result because the partition has to respect *this* project's adopted requirement IDs, its accepted
architecture rules, its source roots and test policy, and the backlog that already exists — none of
which a generic decomposition can know. (SKILL-006, "User goal"; roster SKILL-006 row.)

**Description for discovery:**
Break adopted scope into dependency-ordered epics and bounded stories, each with observable acceptance
criteria, an explicit write scope, and the expert capabilities it needs, keeping every criterion
traceable to the requirement or architecture rule it came from. Use it when someone has a product brief
or an architecture contract and asks what to build first, what to implement next, what "done" means for
each change, how to split an epic into stories, or wants an adopted scope turned into work a developer
could pick up — and when an accepted amendment means the affected stories need revising rather than the
whole backlog regenerated. Do not use it to implement or execute a story that is already ready (that is
devforge-develop), to decide whether a product idea is worth building or what the scope should contain
(that is devforge-define-product), or to explore alternatives when no scope has been selected yet (that
is devforge-brainstorm).

Rationale for the exclusions: SKILL-006's "Does not activate for" row names develop and define-product;
the "Out of scope" acceptance case names brainstorm or define-product for a request to explore
alternatives without selected scope. The roster confirms each sibling's owned output.

**Intended users or role — optional:**
Whoever is turning an adopted scope into work: the person holding the product brief and architecture
contract, working in an ordinary subscribed Claude Code terminal.

## 2. Scope and activation

**Use this skill when:**
Adopted requirements exist (a product brief, an architecture contract, or both) and the next question is
what the units of delivery are, in what order, and what would count as done for each of them. Also when
an accepted amendment or a story defect means specific stories need revising, and when a partial backlog
needs coverage, cycle and readiness checking against its governing sources.

**Outside its scope:**

| Nearby request | Owner |
| --- | --- |
| Execute or implement a story that is already ready | `devforge-develop` (SKILL-009) |
| Decide what the product is for, which requirements are in scope, what value it delivers | `devforge-define-product` (SKILL-002) |
| Explore alternatives or ideas when nothing has been selected yet | `devforge-brainstorm` (SKILL-001) |
| Choose the stack, write the architecture rules, set the test policy | `devforge-architect` (SKILL-005) |
| Create or refresh the expert skill a story declares it needs | `devforge-project-expert-creator` (SKILL-007) |
| Change an adopted requirement or architecture rule | `devforge-change` (SKILL-012), routed to the owner |
| Grade or evaluate a skill package | `devforge-evaluate-expert` (SKILL-008) |
| Sprint scheduling, issue-tracker synchronisation | Out of MVP scope entirely (SKILL-006 "Plugin capability") |

**Example activating requests:**

- "Use DevForgeAI to turn this product brief into epics and stories."
- "What should we implement first, and what does done mean for each change?"
- "Split this epic into stories a developer could actually pick up."
- "CHG-004 was accepted — which stories does it affect and what has to change in them?"

**Near-miss requests that must not activate it:**

- "STORY-014 is accepted and ready. Implement it." (develop)
- "Is this feature worth building at all? Who is it even for?" (define-product / brainstorm)
- "Let's brainstorm some alternatives — I haven't decided what we're building." (brainstorm)
- "Write the architecture contract and pick the database." (architect)
- "Build me the expert skill STORY-003 says it needs." (project-expert-creator)

**How it should be invoked:**
Automatically when relevant, and explicitly by name. **Proposed default:** the package sets no
`disable-model-invocation` and no `paths` restriction; the roster describes explicit native invocation
for the MVP, but the discovery description is written to carry indirect activation as well, and
SKILL-006's acceptance table requires an indirect-activation observation. Owner may narrow this.

## 3. Inputs and expected results

**Required inputs** (SKILL-006 "Inputs and provenance"):

| Input | Requirement | Consume only |
| --- | --- | --- |
| `product-brief` (PROD) | Required | Selected requirement IDs and delivery non-goals. |
| `architecture-contract` (ARCH) | Required for production stories | Applicable rule IDs, test policy, source roots, capability requirements. |
| `design-spec` (UX) or `prototype-report` (XREPORT) | Conditional | Relevant flows, states, observations, hardening disposition. |
| Existing epics/stories and `change-request` (CHG) | Conditional | Dependencies, completed work, the accepted amendment. |
| Provider, destination and write fence | Required before writing | Where the epics and stories are written and what may be touched. |

**Optional inputs:**
An existing project artifact map (`CLAUDE.md`, `AGENTS.md`, an existing `docs/devforge/` tree); a session
assignment record; an accepted decision reference for a constraint the user has already adopted.

**When information is missing:**
A missing required input stays missing, named, with the work it blocks. The skill may proceed with the
part of the partition that does not depend on it. It may **not** invent a requirement ID, an
architecture rule, a digest, an approval, or an expert package to close the gap. An undefined behaviour
in an adopted requirement (the specification's "Missing behavior" case) produces an acceptance criterion
marked unresolved and a routed clarification, not a guessed rule. Stop only when no story can be made
implementation-ready and the blocking owner has been named.

**Expected deliverable:**
One or more `epic` documents (ID prefix EPIC) and `story` documents (ID prefix STORY), plus a
standardized `handoff`. SKILL-006 "Outputs and standardized templates".

**Output format and destination:**
`assets/epic.md`, `assets/story.md` and `assets/handoff.md`, package-local copies of the governing
templates, carrying the `devforge.artifact/v1` envelope. An externally selected destination governs.
**Proposed default** where nothing was selected: the artifact contract's suggested map —
`docs/devforge/epics/` and `docs/devforge/stories/`, handoffs in `docs/devforge/handoffs/`.

**Completion criteria:**

- Every selected requirement ID is either covered by a named story or recorded as an explicit deferral
  with its reason.
- Every story has at least one acceptance criterion whose failure is observable, an allowed write
  scope, its dependencies, and its required capability IDs.
- The dependency graph across the authored stories has no cycle, or the cycle is reported as a blocker.
- Every upstream reference resolves to the revision and digest cited.
- Ready stories are separated from blocked stories, with the actual blocker on each blocked one.
- A handoff exists naming the outputs, their digests, the unresolved decisions and one next task.
- No required field in a delivered document still holds a template placeholder.

## 4. Workflow

Four phases, taken from SKILL-006's "Workflow and phase exits" table. They are this skill's workflow,
not CLI subcommands; nothing in the DevForge CLI intercepts them.

| ID | Level and parent | Action | Decision or expected result | Optional or required? | Enforcement route |
|---|---|---|---|---|---|
| W1 | Workflow; no parent | Derive epics and implementable stories from adopted scope | Linked epics and stories with traceable criteria, plus a handoff | **Proposed: required** for the delivery slice (SKILL-006 "MVP support decision") | R1 |
| P1 | Phase; parent W1 | Select: identify the delivery outcome and the exact accepted source revisions | Scope and non-goals are traceable | **Proposed: required** | R1 |
| P2 | Phase; parent W1 | Partition: outcome-oriented epics and small, independently checkable stories | Each story has a useful outcome and explicit dependencies | **Proposed: required** | R2 |
| P3 | Phase; parent W1 | Specify: behavioural acceptance criteria, negative cases, write scope, test policy, expertise needs | A developer can identify what to change, how to verify it, and what not to infer | **Proposed: required** | R2 |
| P4 | Phase; parent W1 | Check readiness: coverage, cycles, unresolved decisions, source freshness, capability gaps | Ready stories separated from blocked stories without pretending a missing expert exists | **Proposed: required** | R3 |
| T1 | Task; parent P1 | Resolve each cited upstream reference to its stated revision and digest | Reference resolves, or staleness is reported against preserved bytes | **Proposed: required** | R3 |
| T2 | Task; parent P2 | Allocate stable EPIC/STORY IDs and record membership and dependency order | IDs allocated and never reused | **Proposed: required** | R2 |
| T3 | Task; parent P3 | Record each acceptance criterion's requirement reference, or mark it a new proposal | Traceability, or an explicit proposal label | **Proposed: required** | R2 |
| T4 | Task; parent P3 | Assemble the bounded context packet from source excerpts with section IDs and digests | Excerpts carry their source identity | **Proposed: optional** — only where an excerpt is genuinely needed | not applicable |
| T5 | Task; parent P4 | Write the handoff with outputs, observed checks, unresolved decisions, next owner and one task | Handoff exists and its references resolve | **Proposed: required** | R3 |
| T6 | Task; parent P2 | Optional sprint grouping | A user-selected grouping, or none | **Optional** (SKILL-006 "State/action boundary": sprint grouping is optional) | not applicable |

**Applies when:**
P2's design/prototype consumption applies only when a `design-spec` or `prototype-report` is supplied.
T6 applies only when the user asks for a grouping. The revise-affected-stories path (rather than a full
regeneration) applies when an existing backlog and an accepted `change-request` are both present.

**Dependencies and completion evidence:**
P2 waits on P1's resolved source identities; a partition against unresolved sources cannot be traceable.
P3 waits on P2's allocated story IDs and dependency edges. P4 waits on P3, because coverage and cycle
checking need the authored criteria and edges. The completion evidence for each is the authored
document itself plus the resolution record for its upstream references — written by this skill, and
therefore an authoring record, not an independent observation. It goes stale when a cited upstream
revision changes, when the destination is written by another owner, or when an accepted amendment lands.

**Conditional paths — optional:**
Accepted amendment present → revise only the affected stories, preserving prior acceptance criteria and
invalidating affected downstream evidence (SKILL-006 "Rework"). Product or architecture contradiction →
route through `devforge-change` to the owning skill rather than editing the governing source. Dependency
cycle, unresolved consequential acceptance behaviour, stale governing input, or required missing
expertise → stop that continuation and report (SKILL-006 "Stop the affected continuation when").

**When to stop or seek clarification — optional:**
A consequential behaviour is undefined in the adopted scope and no owner has answered; a cited upstream
revision cannot be resolved to preserved bytes; the assigned destination is claimed by another writer;
the requested work would require broadening permissions, adding requirements, or rewriting the stack.

## 5. Task-specific rules

**Required standards or conventions:**

- The `devforge.artifact/v1` envelope on every output; the governing epic and story templates; ID
  prefixes EPIC and STORY; stable IDs that are never reused.
- Acceptance criteria in Given/When/Then form with an observable failure behaviour, per the story
  template's AC table. "Works well" is not an acceptance criterion.
- Each criterion carries the requirement reference it derives from, or is explicitly labelled a new
  proposal (SKILL-006 "Traceability" case).
- Upstream references carry `artifact_id`, `revision`, `store`, `path`, `sha256` and the stable section
  IDs actually relied on (artifact contract, "Standard envelope").
- No artifact contains its own complete-byte digest; hash after the bytes are final; a handoff does not
  list itself among its own outputs (artifact contract, "Skill authoring evidence").
- Epic membership, next-step links and handoff backlinks are relationships, **not** causal upstream
  edges (artifact contract, "Provenance without circular bookkeeping"). Do not revise an accepted story
  merely to record that its expert was installed.
- The fixed result vocabulary: `NOT_EVALUATED`, `NOT_RUN`, `COULD_NOT_RUN`, `NOT_APPLICABLE`. Never
  blended, never summed into a percentage.

**Preferences:**
Small stories over large ones where the outcome stays useful; a story a developer can finish and check
independently. Outcome-oriented epics rather than layer-oriented ones. Excerpt only what the story
actually needs into the bounded context packet — the source keeps authority.

**Actions requiring explicit authorisation — when applicable:**
Adopting a newer upstream revision in place of the one already cited. Writing to a destination that
already holds another owner's artifact. Recording a user decision (`decision_ref`) — only an actual
adoption or a standing delegation that covers this change supplies one. Nothing in this skill authorises
executing a story, running a gate, installing a package, or performing an external action that a
planning document happens to describe.

**Known pitfalls — optional:**

- Inventing a requirement, rule, dependency or permission the adopted scope does not contain; downstream
  develop then implements it and review checks against it.
- Writing an unfalsifiable acceptance criterion, which makes a genuine RED observation impossible.
- Declaring a story ready when its expertise, upstream or decisions are missing — including naming an
  expert package that does not exist.
- Regenerating a whole backlog for a bounded amendment, discarding prior acceptance criteria and their
  history.
- Treating a proposed design or prototype disposition as an accepted production constraint by copying it
  downstream (SKILL-006 "Inputs and provenance").

## 6. Tools and supporting resources

**Target environment:**
Claude Code on Linux/WSL2, in a consuming project that need not contain the DevForgeAI repository. The
skill loads from wherever the client installed it.

**Required tools or integrations:**
File reading and writing in the consuming project. No network dependency. No DevForge CLI dependency for
the workflow itself — see the enforcement route below for what the CLI does and does not cover.

**Access requirements:**
Read access to the cited upstream artifacts and any preserved-bytes archive; write access to the assigned
epic/story/handoff destinations. No credentials or secrets.

**Supporting materials:**

| Resource | Purpose | When it is needed |
|---|---|---|
| `assets/epic.md` | The governing epic template, package-local | Writing an epic |
| `assets/story.md` | The governing story template, package-local | Writing a story |
| `assets/handoff.md` | The standardized handoff envelope | Closing the result |
| `references/recording-rules.md` | Envelope fields, ID and digest rules, placeholders, vocabulary | Filling any artifact's frontmatter or a required field |
| `references/upstream-resolution.md` | Resolving and verifying upstream references, staleness, bounded context packets, research/evidence rules | Select, and any time a cited revision may have moved |
| `references/readiness-check.md` | Coverage, cycles, unresolved decisions, freshness, capability gaps, ownership collision, the missing CLI integration | Check readiness, and any blocked or collided condition |
| `references/derivation.json` | Where each package-local copy came from and what makes it stale | Maintenance |
| `references/sources.md` | External documentation actually retrieved, with dates and claims | Maintenance |

**Unavailable dependency behaviour:**
A missing upstream document, an unreachable preserved revision, or an unwritable destination is reported
by name with the work it blocks; independent parts of the partition continue. A requested check that
cannot execute is `COULD_NOT_RUN` with its actual cause. The absence of an error is not a pass.

**Enforcement route for required items — requirement only:**

- **Route ID and covered items:** R1 — W1, P1.
- **Requirement and protected action:** Before an epic or story is presented as derived from adopted
  scope, every cited upstream reference resolves to the exact revision and digest recorded. Protected
  action: presenting the partition as traceable.
- **Observable evidence:** The upstream entries in the output's envelope, each resolved against bytes
  that hash to the digest cited. Distinguishable from a self-reported "checked" marker only if something
  other than the author recomputes it.
- **State and freshness:** Evidence lives in the consuming project's artifact store, written by this
  skill. It ties to the source revisions named in the envelope. Any change to a cited upstream file
  invalidates it.
- **Intended allow or refuse behaviour:** Refuse the traceability claim when a cited digest does not
  match the bytes at the cited locator; allow when every entry resolves.
- **Missing evidence and errors:** A missing or unreachable upstream is reported as a stale or missing
  input, and the dependent claim is withheld. Not a silent substitution of newer bytes.
- **Recovery and user message:** Name the reference, the expected digest, what was found, and the owner
  who can supply the preserved bytes or authorise the newer revision.
- **Owner:** Integration owner. The check itself would be compiled into the DevForge CLI and invoked by
  whatever wiring that owner selects; this document records the requirement, not an implementation.
- **Feasibility:** Unknown until the integration owner confirms it.
- **Status:** Requirement recorded. **Enforcement requested; not confirmed available.** No gate is
  implemented, activated or executed by this skill.

- **Route ID and covered items:** R2 — P2, P3, T2, T3.
- **Requirement and protected action:** Before a story is offered to `devforge-develop`, it carries at
  least one acceptance criterion with an observable failure behaviour, a declared write scope, its
  dependencies, and its required capability IDs; each criterion names its requirement reference or is
  labelled a proposal. Protected action: a development run against that story.
- **Observable evidence:** The story document's AC table, scope block and expertise table, and the
  presence or absence of a requirement reference per row.
- **State and freshness:** In the story file itself. Stale when the story is revised or a governing
  requirement changes.
- **Intended allow or refuse behaviour:** Refuse the development run for a story with an empty or
  unfalsifiable AC table, an undeclared write scope, or an unresolved consequential criterion; allow
  otherwise.
- **Missing evidence and errors:** A story that cannot be read or parsed blocks its own dependent run
  and nothing else.
- **Recovery and user message:** Name the story, the missing element and the phase that supplies it.
- **Owner:** Integration owner.
- **Feasibility:** Unknown until the integration owner confirms it.
- **Status:** Requirement recorded. **Enforcement requested; not confirmed available.**

- **Route ID and covered items:** R3 — P4, T1, T5.
- **Requirement and protected action:** Before a backlog is presented as ready, requirement coverage is
  accounted for, the dependency graph is acyclic, and no required field holds a template placeholder.
  Protected action: presenting the set as ready for delivery.
- **Observable evidence:** The epic's coverage table, the dependency edges across the authored stories,
  and a placeholder scan of every required field.
- **State and freshness:** In the epic and story files. Stale on any story revision or amendment.
- **Intended allow or refuse behaviour:** Refuse the readiness presentation on an uncovered requirement
  with no recorded deferral, on a cycle, or on a surviving placeholder; allow otherwise.
- **Missing evidence and errors:** An unreadable member story makes coverage indeterminate, which is
  `COULD_NOT_RUN`, not a pass.
- **Recovery and user message:** Name the uncovered requirement, the cycle members, or the field and
  line still holding a placeholder.
- **Owner:** Integration owner.
- **Feasibility:** Unknown until the integration owner confirms it.
- **Status:** Requirement recorded. **Enforcement requested; not confirmed available.**

**Observed CLI surface** (`/home/bryan/Projects/DevForge/framework/DevForge/target/debug/devforge --help`,
observed 2026-09-10T19:37Z): `delivery`, `expert`, `check`, `init`, `red`, `green`, `accept`, `verify`,
`status`, `isolate`. **No subcommand takes an epic, a story, a requirement graph or an artifact
envelope.** `devforge check` checks a project's structural policy and provenance against an external
policy JSON and explicitly "does not certify semantic behavior"; it is not a planning check. SKILL-006's
"Plugin capability" row states that deterministic graph and provenance checks belong to DevForge — that
capability is **not implemented at this revision**, and R1/R2/R3 above are exactly the gap.

## 7. Acceptance cases — capture only

Recorded before the candidate, from SKILL-006's "Validation and behavioral acceptance" table and its
"Additional common cases". Captured, not executed. This skill did not run any of them.

| Case | Example request or input | Expected behaviour |
|---|---|---|
| Direct activation | "Use DevForgeAI to turn this product brief into epics and stories." | Produces linked epic and story documents. |
| Indirect activation | "What should we implement next?" | Uses dependencies and readiness rather than inventing a sprint requirement. |
| Missing behavior | A requirement leaves authorization behaviour undefined. | Marks the dependent acceptance criterion unresolved and routes clarification. |
| Traceability | One supplied acceptance criterion is not supported by any requirement. | Identifies it as a new proposal, not an inherited requirement. |
| Out of scope | "Let's brainstorm alternatives" with no selected scope. | Routes to brainstorm or define-product. |
| Ownership collision | A session record assigns the target destination to another writer. | Stops dependent writes and reports the collision without deleting or resetting anyone's work. |
| Stale upstream | A cited ARCH revision has been superseded in the live tree. | Marks the applicable prior evidence stale and routes a new check or run; does not relabel newer bytes as the old revision. |
| Placeholder left in a required field | A story field still holds `{{...}}`. | The result stays a draft and cannot be presented as ready. |
| Check could not run | A requested check cannot execute. | Records `COULD_NOT_RUN` with its actual cause; absence of an error is not PASS. |

**Example of a good deliverable — optional:**
`evals/fixtures/good/EPIC-001.md` and `evals/fixtures/good/STORY-001.md` in the package, both labelled
synthetic.

## 8. Placement and maintenance

**Availability:**
Bundled in the `devforgeai` Claude plugin; canonical source
`providers/claude/plugins/devforgeai/skills/devforge-plan/`.

**Installation location:**
Recorded in section 10. An installed copy is never an alternative source.

**Maintainer:**
The assigned Claude provider author for this skill; shared templates and contracts belong to the
integration owner.

**Reasons to revisit:**
A change to SKILL-006, to `templates/devforge-plan/epic.md` or `story.md`, to `templates/shared/handoff.md`,
to the artifact or execution contracts, to the DevForge CLI's command surface (particularly if a planning
check is implemented), or to Claude Code's skill frontmatter or discovery behaviour. Also any measured
failure from an evaluation.

## 9. Authoring decision and progress

**Current status:**
Authored candidate (scaffold). Not evaluated.

**Working specification and target paths:**
This document:
`/home/bryan/Projects/DevForge/worktrees/claude-scaffold-plan-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-plan/authoring/design/skill-design-spec.md`.
Target package:
`/home/bryan/Projects/DevForge/worktrees/claude-scaffold-plan-20260910/providers/claude/plugins/devforgeai/skills/devforge-plan/`.

**Search scope and limitations:**

Searched at base revision `c17e758417da64928a0f47fc2600304465ac3f3c`, by reading directory names and
`SKILL.md` frontmatter, then the plausible candidates' instructions. Nothing was run or installed.

| Location | Result |
| --- | --- |
| `providers/claude/plugins/devforgeai/skills/` (assigned canonical inventory) | Four skills: `devforge-brainstorm`, `devforge-develop`, `devforge-project-expert-creator`, `devforge-review`. No `devforge-plan`. |
| `providers/codex/plugins/devforgeai/skills/` (read-only, for lineage only) | Five skills: the four above plus `devforge-evaluate-expert`. No `devforge-plan`. |
| `docs/mvp/package-index.json`, SKILL-006 entry | `implementations.claude.source: null`, `status: NOT_IMPLEMENTED`, `native_behavior: NOT_EVALUATED`. Codex identical. |
| `docs/mvp/roster.md`, SKILL-006 row | "Proposed" — no current source. |
| Destination `providers/claude/plugins/devforgeai/skills/devforge-plan/` | Did not exist at base. No collision. |

Locations **not** searched and therefore not claimed empty: `~/.claude/skills/`, any managed
(enterprise) settings directory, any `--add-dir` directory, any consuming project's `.claude/skills/`,
any exported plugin outside this repository, and the `.agents/skills` Codex installation tree. The
comparison is limited to instructions and metadata; no candidate was executed, and nothing here supports
a claim of global uniqueness.

**Related skills:**

| Candidate and source | Relevant overlap | Gap or meaningful distinction | Recommendation |
|---|---|---|---|
| `devforge-brainstorm` — `providers/claude/.../devforge-brainstorm` | Both produce a durable artifact from a conversation and both separate proposals from decisions | Brainstorm operates before scope is selected and produces an idea ledger; it explicitly excludes work on an accepted story. It cannot partition adopted scope. | Separate workflow |
| `devforge-develop` — `providers/claude/.../devforge-develop` | Both centre on a story | Develop consumes a ready story and drives the RED-to-GREEN run; it produces no story. Its own instructions say to read the story, not write it. | Separate workflow |
| `devforge-project-expert-creator` — `providers/claude/.../devforge-project-expert-creator` (at 4999f31) | Both take a concrete story plus accepted architecture as input, and both record capability needs | The creator authors an expert skill from a story that already exists. It is a consumer of this skill's output, per the roster edge `PL --> XC`. | Separate workflow |
| `devforge-review` — `providers/claude/.../devforge-review` | Both compare a result against upstream intent | Review inspects a candidate after development against story criteria; it does not derive stories. | Separate workflow |
| Codex `devforge-*` packages | Same roster roles | Different provider; the assignment fences this to Claude, and no Codex `devforge-plan` exists to port. | Not a candidate |

**Selected approach and rationale:**
**Create.** No `devforge-plan` exists in the searched Claude inventory, none exists in the Codex
inventory to port, and the package index records the Claude implementation as `NOT_IMPLEMENTED` with a
null source. The nearest siblings own adjacent phases with different activation, different inputs and
different outputs; absorbing epic and story derivation into any of them would blur an activation
boundary that SKILL-006 and the roster define. Honest statement of the result: *no suitable skill was
found in the searched inventory*.

**Enhancement details — when applicable:**
Not applicable. Nothing is being enhanced; nothing existed at the destination.

**Requirements, defaults and open decisions:**

| Item | Requirement or decision | Basis | Status |
|---|---|---|---|
| Output destination default | `docs/devforge/epics/`, `docs/devforge/stories/`, `docs/devforge/handoffs/` when nothing was selected | Artifact contract, "Output storage and stable candidate snapshots" | **Proposed default** |
| Invocation policy | Automatic when relevant plus explicit by name; no `paths` restriction | SKILL-006 acceptance table requires an indirect-activation observation | **Proposed default** |
| Frontmatter fields | `name` and `description` only | Assignment; matches the sibling Claude packages | Settled by assignment |
| W1/P1–P4/T1–T3/T5 classification | Required | Derived from SKILL-006's phase-exit table; the user was not asked | **Proposed** — awaiting owner |
| T4 (bounded context packet) classification | Optional, applies only where an excerpt is genuinely needed | SKILL-006 "include only relevant context excerpts" | **Proposed** — awaiting owner |
| T6 (sprint grouping) classification | Optional | SKILL-006 states sprint grouping is optional | Settled by specification |
| Package references (three) | `recording-rules`, `upstream-resolution`, `readiness-check` | Derived from the phases that need conditional detail | **Proposed** — authoring judgement |
| No `scripts/` | None authored | Assignment prefers none; no deterministic operation in this workflow justifies one | **Proposed** |
| Eval baseline label | `without_skill` for every tier-B case | No previous `devforge-plan` exists in either provider, so `old_skill` has no referent | Settled by observation |
| Runner dependency | `evals/cases.jsonl` written to the `devforge-evaluate-expert` runner schema at commit `e52ac59` | Assignment; schema read from that commit's `scripts/run_cases.py`, `scripts/graders.py` and `references/runner-interface.md` | Settled, with the dependency recorded |
| Managed-runtime section | Omitted | SKILL-006 requires no managed operation; the brainstorm package's managed-runtime section was deliberately not copied | Settled by specification |

**Authored or changed files:**
The package file list and digests are in the authoring `file-manifest.json`. This document does not
duplicate that inventory and contains no digest of itself.

**Material unresolved dependencies or enforcement gaps:**

1. No DevForge CLI command checks planning artifacts. R1, R2 and R3 are recorded requirements with
   feasibility unknown; the specification assigns deterministic graph and provenance checks to DevForge
   and that capability does not exist at this revision.
2. Seven of the eight upstream and downstream siblings named in the roster provenance flow are not
   implemented for Claude — `define-product`, `design`, `prototype`, `architect`, `release` and `change`
   have no source at all, and `evaluate-expert` exists only as a candidate on another branch. The skill
   must therefore treat named producers and consumers as artifact types, not as invocable skills.
3. The Python case runner and graders this package's `evals/cases.jsonl` targets live in a package that
   is itself an unmerged candidate under repair on another branch.
4. Workflow item classifications (W1, P1–P4, T1–T5) are proposals; no user answered the
   optional-or-required question because the assignment prohibits questions.

**Validation status:**
Not performed.

**Enforcement status:**
Requirements recorded; no gate implemented by this skill.

## 10. Framework authority and source identity

**Framework and provider:**
DevForgeAI checkout `/home/bryan/Projects/DevForge/framework/DevForgeAI`, working through the assigned
worktree `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-plan-20260910` on branch
`author/claude-devforge-plan-scaffold-20260910`, base commit
`c17e758417da64928a0f47fc2600304465ac3f3c` (verified with `git rev-parse HEAD` before writing).
Provider: Claude. Client: Claude Code. Consuming project: none — this is framework authoring.

**Assignment and authority:**
Scaffolding assignment from the coordinator packet
`/home/bryan/Projects/DevForge/tmp/claude-remaining-skills-scaffolding-20260910/packets/author-devforge-plan.md`.
Exclusive write fence: `providers/claude/plugins/devforgeai/skills/devforge-plan/**` and
`docs/skill-authoring/history/claude-scaffolding-20260910/devforge-plan/authoring/**`. Integration owner
for shared contracts, templates, roster, package index, manifests, hooks and agents: not this author. No
session-record artifact ID was supplied; `execution_ref` is `null` with the packet named in
`missing_inputs` wherever an envelope requires it.

**Roster role:**
SKILL-006, an accepted roster role, currently `NOT_IMPLEMENTED` for both providers. Authoring this
candidate does not amend the roster, does not change `package-index.json`, and certifies no framework
capability.

**Selected source records:**

| Record | Governing source or preserved location | Revision or artifact ID | SHA-256 | Selection authority and purpose | Gaps or conflicts |
|---|---|---|---|---|---|
| Governing design specification | `docs/mvp/specifications/skill-006-devforge-plan.md` | SKILL-006, DRAFT revision 2, refreshed 2026-09-05 | `149a66a375da1bb3447f51b657996883974fec1dac3ce92af866eba94a378e4b` | Named governing input in the assignment; verified by `sha256sum` | Draft status; no callable implementation supplied by the design package |
| Skill-authoring contract | `docs/mvp/skill-authoring-contract.md` | DRAFT revision 3, 2026-09-07 | `371462385b4e32d1b347f959abb779f4be4251e357c5720a9aef039113eb4b53` | Authoring, provider, packaging and evaluation-tier boundary | Native admission `NOT_VALIDATED`; activation and delivery `NOT_OBSERVED` |
| Artifact contract | `docs/mvp/artifact-contract.md` | DRAFT revision 2, 2026-09-05 | `00d8c4f4bf619b8361e056c2b77c8215595755a0eb6262b865e6a8f464c1d2b5` | Envelope, provenance, digest and storage rules | Not claimed to be validated by the CLI |
| Execution contract | `docs/mvp/execution-contract.md` | DRAFT revision 3, 2026-09-07 | `73bca87bafd43d6b7294bad945c6506b2056d749ca22100ba4272b9a26e4e15b` | Worktree ownership, collision behaviour, command-naming rule | No worktree registry exists |
| Roster | `docs/mvp/roster.md` | DRAFT, refreshed 2026-09-05 | `ea35b825f8d2ea58ea0eb20b77c2fdd47df1dc2ddb3bbcfef3b032874e5f57bc` | Provenance flow: producers and consumers of epic and story | Most siblings unimplemented |
| Package index | `docs/mvp/package-index.json` | current at base | read-only; not modified | SKILL-006 implementation status | — |
| Development language policy | `docs/development-language-policy.md` | 2026-09-09 owner decision with the 2026-09-10 clarification | `3d89f39ee6d7caea84a46bdffeb39a96cd1d0bbc35d99e9435acd8ef8ca1700f` | Rust owns gates; permitted Python evaluation runner only | — |
| Bounded delivery | `docs/learned-behaviors/bounded-delivery.md` | unnumbered working guidance | `22a0388c3a4afdb32beace2fb0082ec02acea885e45650f0b42925b76c09e7ae` | Finish line matching the request | — |
| Epic template | `docs/mvp/templates/devforge-plan/epic.md` | current at base | `48f8b069f6f57b386d0337a2ef15503dfe234a97f3d7162740b708de75dc35e3` | Named governing template | — |
| Story template | `docs/mvp/templates/devforge-plan/story.md` | current at base | `a19ccd7f332c895fe6d7713ed8ae1a7e52991c71c846557d3fb29862ebff9daf` | Named governing template | — |
| Shared handoff template | `docs/mvp/templates/shared/handoff.md` | current at base | `abc7f8e0ca545093d3b1486d1a86cb7e51609aef17c0027b951a47da6eaed206` | Named governing template | — |
| Template for this document | builder package asset `assets/skill-design-spec.md` at commit `4999f31` | `4999f3106565c5e320d1f1a7db066b437e4e94be` | `715ef3bdf9082ace4c3b3eeda27e8bf9e4663355bcebed2f5d997fefc5a26ef9` | The builder named in the assignment; `docs/mvp` has no shared skill-design-spec template | The builder is itself a draft under independent review |
| Case-runner schema | `scripts/run_cases.py`, `scripts/graders.py`, `references/runner-interface.md` at commit `e52ac59` | `e52ac596cbf790dfa156d883852d392c512fdbcc` | digests in `authoring-notes.md` | The assignment's named runner dependency | Unmerged candidate; a repair pass is in progress on that branch |

**Canonical source and generated runtime mapping:**

| Purpose | Selected path and provider | Identity or manifest reference | Ownership and refresh responsibility |
|---|---|---|---|
| Canonical framework source | `providers/claude/plugins/devforgeai/skills/devforge-plan/` (Claude) | `file-manifest.json` in this authoring directory | This author |
| Project-specific source | Not applicable | — | — |
| Installed project copy | A consuming project's `.claude/skills/devforge-plan/` | Not generated | Integration owner |
| Plugin export | Not generated | Not generated | Integration owner |
| Working specification | This document | — | This author |

A provider source folder alone is not a discovered installation. No installation, export, binding,
activation or evaluation was performed.

**Package derivations:**
Recorded in the package's `references/derivation.json`, which carries the source paths and revisions,
source and destination digests, transformations and refresh conditions. It is not duplicated here, and
no record contains its own digest.

**Authority, contract, installation or provider gaps:**
The three enforcement routes in section 6 are unimplemented. `package-index.json` still records
SKILL-006 as `NOT_IMPLEMENTED` with a null Claude source; updating it is the integration owner's change,
outside this fence, and a coordinator item. The runner dependency is an unmerged branch.

**Preserved boundaries:**
Untouched by this assignment: `docs/mvp/**` (specifications, templates, contracts, roster, package
index), the sibling Claude skills, every Codex source, the plugin manifest, `hooks/`, `agents/`, and the
companion DevForge repository's gates, policies and tests. A defect in any of them is reported to its
owner, not repaired here.

**Authoring and release status:**
Authored candidate. Evaluation and adoption are separate; source or package identity establishes no
activation, no quality and no release readiness.

## 11. Evaluator repair intake

**NOT_APPLICABLE.** No evaluator handoff, report, finding or repair specification exists for
`devforge-plan`. This is a first authoring pass.

## 12. Change record

**Identity and authoring scope:**
Record `PLAN-SCAFFOLD-001`, 2026-09-10 UTC. Coordinator packet
`.../packets/author-devforge-plan.md`. Provider Claude, target skill `devforge-plan`, permitted paths as
in section 10, requested action: **create**.

**Input references:**
The selected source records table in section 10. No prior candidate, no frozen source manifest, no
evaluator report — nothing existed at the destination.

**Change mapping:**

| Finding IDs | Change ID | Change type | Requirement IDs preserved or changed | Disposition | Old path and SHA-256 | New path and SHA-256 | Summary or reason |
|---|---|---|---|---|---|---|---|
| not applicable | CHG-001 | new package | W1, P1–P4, T1–T6 introduced | applied | absent (new) | see `file-manifest.json` | Claude scaffold of SKILL-006: SKILL.md, three references, three assets, evals with fixtures and trigger queries |

**New canonical source manifest:**
`file-manifest.json` in this authoring directory: package-relative path to SHA-256 for every file in the
candidate. It excludes its own digest. No value in it is a guess.

**Resulting specification identity:**
This document, at the path in section 9. SKILL-006 revision 2 is unchanged; nothing in this pass amends
it.

**Preserved behaviour and requirements:**
Nothing pre-existed. The governing templates' placeholders are preserved byte-for-byte in the package
copies; the derivation record states the exact transformation for each.

**Derivations and generated-copy work remaining:**
`references/derivation.json` covers the package copies. Canonical-to-installed and export mapping is not
generated and belongs to the integration owner. `package-index.json` still records SKILL-006 as
`NOT_IMPLEMENTED`; that update is outside this fence.

**Deferred proposals, gaps and evaluation prerequisites:**
Section 9's unresolved list. Tiers A, B and C are `NOT_RUN`. No installation exists to evaluate, and the
runner this package's cases target is on an unmerged branch.

**Finding status:**
Not applicable — no findings exist.

**Validation status:**
Not performed.

**Enforcement status:**
Requirements recorded; no gate implemented by this skill.

**Next handoff:**
`handoff.md` in this authoring directory, addressed to an independent evaluator. It is a prepared
document, not a receiving invocation. No evaluation is launched.

## Evaluation coverage proposed

Accepted baseline: none — no previous `devforge-plan` exists in either provider, so every tier-B case
uses `without_skill` as its baseline label and `old_skill` has no referent. Capability scope: the four
workflow phases and the nine acceptance cases in section 7. Environment scope: Claude Code on Linux/WSL2,
project-local installation and plugin export are both untested.

Proposed coverage: tier C for installed-resource resolution and artifact-field completeness (the
deterministic cases in `evals/cases.jsonl`); tier B for output quality against the nine acceptance cases
(`evals/evals.json`); tier A for discovery and activation from an installed package in a fresh terminal
(`evals/triggers/trigger-queries.json`, fixed split, stratified by category, assigned once here).

Missing evidence: everything behavioural. Tiers A, B and C are `NOT_RUN` by this author. This skill
proposes coverage; a separate evaluator and an independent reviewer assess it. The accepted Routine/Full
manual-mode policy governs the promoted Codex packages and is `NOT_APPLICABLE` to this Claude package
until an owner selects an equivalent.
