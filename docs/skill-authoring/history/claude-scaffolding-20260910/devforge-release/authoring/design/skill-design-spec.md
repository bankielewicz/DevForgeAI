# Skill design specification — devforge-release (Claude)

Derived from the frozen builder asset `assets/skill-design-spec.md` at commit 4999f3106565c5e320d1f1a7db066b437e4e94be (source sha256 `715ef3bdf9082ace4c3b3eeda27e8bf9e4663355bcebed2f5d997fefc5a26ef9`) in the worktree `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-project-expert-creator-20260910`. The template was copied out and filled here; it was not filled in place inside that package.

This is a DevForgeAI authoring document written before the candidate. It carries the design, the framework authority and source mapping, and the change record. It certifies nothing about behaviour, and completing it establishes nothing about whether the authored skill works.

Populated 2026-09-10 UTC. No questions were asked of a user: this assignment directed the author to recover every material decision from the specification, templates and contracts, and to record a proposed default wherever the sources are silent. Every row below is therefore marked `supplied source` or `proposed default`. There is no row marked `user statement`, and nothing here has been approved by anyone.

## 1. Identity and purpose

**Skill name:**
`devforge-release`

**Purpose:**
Turn a reviewed candidate into a reviewable PR and release package and record, accurately, what was actually done to it. SKILL-011's user goal is "Turn a reviewed candidate into a reviewable PR or release package, carrying its provenance into any authorized publication and accurately recording what occurred." The project-specific part is the provenance: the candidate that gets published has to be the candidate that was reviewed, and each external step - PR creation, merge, deployment, verification - has to be recorded as its own observation rather than collapsed into one "released" status.

**Description for discovery:**
What it does, when it applies, and the nearest work that belongs to a sibling skill. The specification's use-case inventory supplies the direct request ("Use DevForgeAI to prepare the PR and release record for this candidate"), the indirect request ("Package this accepted change for delivery, including recovery and verification"), and the "Does not activate for" row ("A failed readiness review returns to its owning workflow. Creating a release record does not establish that deployment happened."). The roster and the sibling specifications supply the owners named in the exclusions: `devforge-review` (SKILL-010) owns readiness assessment, `devforge-develop` (SKILL-009) owns creating or repairing a candidate, `devforge-change` (SKILL-012) owns turning a changed decision, dependency or defect into a bounded proposal.

Claude Code combines `description` with `when_to_use` and truncates the pair at 1,536 characters in the skill listing. Proposed default: keep the authored description near 1,000 characters so the whole of it survives truncation, and carry no `when_to_use` field.

**Intended users or role — optional:**
A person finishing a change in an ordinary subscribed Claude Code terminal, who has a reviewed candidate and wants a PR or release package they can hand to someone.

## 2. Scope and activation

**Use this skill when:**
- A reviewed candidate needs a PR title, body, release notes and verification criteria drafted.
- An accepted change needs packaging for delivery, including the migration and recovery steps its architecture contract requires.
- Someone asks what would have to be true before a candidate could ship, and wants the answer written down against the actual evidence.
- An authorized external action has already been performed and the record needs to state what happened, with readbacks.

**Outside its scope:**
- Assessing whether the candidate is ready. That is `devforge-review`; a failed readiness review returns to its owning workflow.
- Fixing a failing requirement or writing the code. That is `devforge-develop`.
- Assessing a changed decision, dependency or defect and refreshing what it invalidates. That is `devforge-change`.
- Establishing that a deployment happened. Writing a release record does not; only an observed receipt does.
- Acquiring publication authority. The skill asks for the missing authority; it does not manufacture, infer or work around it.

**Example activating requests:**

- "Use DevForgeAI to prepare the PR and release record for this candidate."
- "Package this accepted change for delivery, including recovery and verification."
- "Draft the PR body and release notes for the change we just reviewed - I'll open the PR myself."
- "QA-014 says this is ready. What do we need before it can go out?"

**Near-miss requests that must not activate it:**

- "The review came back with two blockers - can you sort them out?" (`devforge-review` returns it, `devforge-develop` repairs it.)
- "This acceptance criterion is failing. Fix it." (`devforge-develop`.)
- "The upstream library shipped a breaking change - what does that invalidate?" (`devforge-change`.)
- "Did this actually deploy?" (A release record is not a deployment receipt; the answer comes from an observed external receipt, not from this skill's own output.)
- "Write release notes for my blog post." (Not a DevForge candidate at all.)

**How it should be invoked:**
Automatically when relevant and explicitly by name. Proposed default; the specification does not state an invocation policy, and both are ordinary for a Claude skill.

## 3. Inputs and expected results

**Required inputs:**

| Input | Requirement | Consume only |
| --- | --- | --- |
| review-report (QA) | Required | Candidate identity, readiness recommendation, remaining limitations. |
| development-record, story, epic | Required as relevant | Change scope, verification evidence, delivered outcomes. |
| architecture-contract | Required as relevant | Migration, recovery, monitoring and release requirements. |
| Git/CI/environment observations and action authorization | Conditional | Actual targets, current checks, credentials available to the human-operated workflow, permitted actions. |

Taken verbatim from SKILL-011's "Inputs and provenance" table. The "consume only" column is the specification's own restriction: a release record reads these fields and does not re-derive scope, re-review the candidate or re-open an architecture decision.

**Optional inputs:**
- A session record naming this session's worktree, branch and write fence.
- A prior release record for the same candidate lineage, when this is a revision.
- The DevForge CLI and an external policy and state directory, when the operator supplied them.

**When information is missing:**
A missing required input stays missing, named, with the work it blocks - it never becomes template filler and never becomes an inferred value. `missing_inputs` in the artifact envelope is where it goes. The skill can still complete a draft package around a missing input when the missing input blocks only a dependent action: absent publication authority blocks posting, not drafting. It stops when the missing input is the candidate identity itself, because then there is nothing to package.

**Expected deliverable:**
A release-record (ID prefix `REL`) from the package's `assets/release-record.md`, plus a standardized handoff from `assets/handoff.md`. SKILL-011: "Every result includes a handoff with output identities, observed checks, unresolved decisions, next owner, and one copyable task prompt."

**Output format and destination:**
`devforge.artifact/v1` envelope; Markdown. An externally selected destination governs. Proposed default when nothing was selected: `docs/devforge/releases/` for the release record and `docs/devforge/handoffs/` for the handoff, from the artifact contract's suggested project artifact directories. The project's own accepted artifact map, where it has one, outranks that default.

**Completion criteria:**

- A concrete local delivery package exists - PR title, body, release notes, applicable migration and recovery steps, verification criteria - before any missing publication approval is requested.
- The reviewed candidate identity in the record resolves, and its mapping to a Git commit or tree is stated rather than assumed.
- Every external action is either observed with a readback reference, or carries an explicit not-run reason.
- Local acceptance, PR state, merge, deployment and post-release verification appear as five separate rows, never as one status.
- No required field holds a template placeholder.
- The handoff names the next owner, one copyable task, and the checks that were not run.

## 4. Workflow

The four phases are SKILL-011's. They are the skill's own workflow. They are not CLI subcommands, no command intercepts them, and nothing in this design implements a gate.

| ID | Level and parent | Action | Decision or expected result | Optional or required? | Enforcement route |
|---|---|---|---|---|---|
| W1 | Workflow; no parent | Prepare and record delivery for one reviewed candidate. | A release record and handoff that state exactly what happened and what remains. | Required (proposed default; SKILL-011 defines this as the skill's whole job). | Not applicable - no route protects the workflow as a whole. |
| P1 | Phase; parent W1 | Recheck. Confirm the candidate still matches the reviewed evidence and that target information is current. | No stale review is promoted to a different candidate. | Required (proposed default from the specification's exit condition). | R1 |
| P2 | Phase; parent W1 | Prepare. Draft PR title and body, release notes, applicable migration and recovery steps, verification criteria. | A concrete local delivery package exists before any missing publication approval is requested. | Required (proposed default). | Not applicable. |
| P3 | Phase; parent W1 | Execute authorized actions using available approved tooling; otherwise leave the package as a draft. | Each external action has an observed outcome or a clear not-run reason. | Conditional - applies only where an authorization already exists (proposed default from the specification's state/action boundary). | R2 |
| P4 | Phase; parent W1 | Record. Read back created references; distinguish local acceptance, PR state, merge, deployment and verification. | The record states exactly what happened and what remains. | Required (proposed default). | R3 |
| T1 | Task; parent P1 | Resolve the review-report's bound candidate identity against the current candidate bytes. | Match, or a recorded mismatch that stops promotion. | Required (proposed default). | R1 |
| T2 | Task; parent P1 | Establish the candidate-to-Git mapping (snapshot tree versus commit) and state it as a claim with its basis. | An explicit mapping, or `missing_inputs`. | Required (proposed default). | Not applicable. |
| T3 | Task; parent P1 | Observe the assignment: worktree, branch, single writer, write fence. | Ownership confirmed, or a collision reported and dependent writes stopped. | Required (proposed default from the execution contract's failure table). | R4 |
| T4 | Task; parent P2 | Extract the applicable migration, recovery and monitoring requirements from the architecture contract. | Steps, or an explicit not-applicable rationale. | Required as relevant (proposed default). | Not applicable. |
| T5 | Task; parent P3 | Check that each planned action names an existing authorization reference before performing it. | Performed with a readback, or left as a draft with the missing authority named. | Required (proposed default). | R2 |
| T6 | Task; parent P4 | Read back every created reference and every digest the record cites. | Each reference resolves to the bytes it names. | Required (proposed default). | R3 |

**Applies when:**
- P3 applies only when an authorization the user already holds covers the specific action, and approved tooling for it is actually available. Otherwise the phase is skipped, the package stays a draft, and the planned-actions table records the missing authority and its owner.
- T4 applies when an architecture contract is supplied and carries migration, recovery or monitoring requirements. Where it does not, the record states the not-applicable rationale rather than leaving the row blank.
- The whole workflow can be entered mid-way for a revision: a prior release record for the same candidate lineage is superseded, not replaced silently, and its bytes are preserved.

**Dependencies and completion evidence:**
- P2 waits on P1. Evidence of P1: the recheck result recorded in the release record's "Reviewed candidate and target" section, naming the QA identity, the candidate identity and the outcome of the comparison. It goes stale when the candidate bytes, the review-report revision, or the target branch or environment changes.
- P3 waits on P2 and on an existing authorization reference. Evidence: the planned-actions table with an authorization reference in each row that will be executed. It goes stale when the authority is withdrawn or its scope no longer covers the action.
- P4 waits on P3 where P3 ran, and on P2 otherwise. Evidence: the actual-delivery-observations table with a readback reference or a not-run reason in each of its five rows.
- Who produces the evidence: the skill writes the rows; the external receipts (a PR URL, a merge commit, a deployment record, a CI result) are produced by the tools and services that performed those actions, and are cited, never asserted.

**Conditional paths — optional:**
- Identity mismatch at P1: stop the promotion, report to the owning workflow (`devforge-review` for a readiness question, `devforge-develop` for a candidate repair), and do not relabel newer bytes as the reviewed revision.
- Publication authority absent at P3: complete the draft, request the specific missing authority, and record each un-executed action as `NOT_RUN` with the authority it needs.
- Hosted CI unavailable at P3 or P4: record `COULD_NOT_RUN` with the actual cause. A local check that passed is local evidence and is recorded as such; it is not hosted GREEN.
- Concurrent writer holds the worktree or branch: stop dependent writes, report the collision naming the record observed and where it was read, and do not delete, reset, revert, force or relocate.
- Operational failure after a real release: that becomes a change request or the project's existing incident process, not a rewrite of the release record.

**When to stop or seek clarification — optional:**
- Identity mismatch, or unmet required readiness, prevents promotion.
- A required authorization is missing for an action the user asked to have performed.
- The assigned destination is unwritable, outside the fence, or already holds another session's artifact.
- Two successive attempts have addressed the same blocker with no new evidence.

## 5. Task-specific rules

**Required standards or conventions:**
- `devforge.artifact/v1` envelope on both outputs; `REL` prefix for the release record.
- The fixed result vocabulary, never blended: `NOT_EVALUATED`, `NOT_RUN`, `COULD_NOT_RUN`, `NOT_APPLICABLE`. The absence of an error is not a pass.
- No artifact contains its own complete-byte digest. Hash after the bytes are final; the handoff carries the release record's digest and not its own.
- Local acceptance, PR state, merge, deployment and post-release verification stay separately observable.
- Upstream references carry `artifact_id`, `revision`, `store`, `path`, `sha256` and the stable section IDs actually relied on, and every one of them must resolve after the last write.
- A proposed source can support exploration and cannot become an accepted production constraint by being copied downstream.

**Preferences:**
- Prefer the project's own accepted artifact map over the proposed default directories.
- Prefer a short PR body that names the problem, the resulting behaviour, the verification and the material limitations, over a summary of the diff.
- Prefer citing an external receipt over restating its contents.

**Actions requiring explicit authorisation — when applicable:**
Creating a PR, pushing a branch, merging, tagging, publishing a release, deploying, and any external communication. Each is a separate action with its own authority. SKILL-011's state/action boundary: "PR drafting, PR creation, merge, deployment, and release acceptance are separate actions. Execute external actions only within existing authorization; ask only when the required authority is missing."

**Known pitfalls — optional:**
- Promoting a stale review onto a different candidate because the identities look close enough.
- Recording local GREEN in a row that a reader will take for hosted CI.
- Writing a plausible PR URL before the PR exists.
- Treating "the review said ready" as authority to merge.
- Leaving a `{{placeholder}}` in a required field and presenting the result as ready.
- Naming a `devforge` subcommand that does not exist, or presenting a suggested command as a gate.

**Enforcement route for required items — requirement only:**

- **Route ID and covered items:** R1; P1, T1.
- **Requirement and protected action:** No promotion of a candidate whose identity does not match the review-report that recommended it. The protected action is producing a release record that binds a QA identity to candidate bytes.
- **Observable evidence:** The review-report's recorded candidate identity and digest, compared against the current candidate bytes or an accepted snapshot. A self-reported "identities match" line in the record is not that evidence.
- **State and freshness:** Evidence lives in the review-report and in the candidate tree or its accepted archive. It is written by the reviewer and by whatever preserved the candidate. It ties to this run through the candidate path and digest. It is invalidated by any change to the candidate bytes or to the review-report revision.
- **Intended allow or refuse behaviour:** Permit the release record to bind that QA identity when the digests match; refuse when they differ or when either is absent. A warning is advisory, not a refusal.
- **Missing evidence and errors:** Absent digest, unreadable candidate, or unavailable CLI - refuse the binding and record `COULD_NOT_RUN` with the cause. Do not treat an unreadable input as a match.
- **Recovery and user message:** State which identity is missing or mismatched, that promotion is blocked, and that the owning workflow (review, or develop for a repair) holds the next action. Stop after reporting; do not search for a different candidate that would match.
- **Owner:** Integration owner. The check itself would be compiled into the DevForge CLI and invoked by whatever wiring that owner selects; this document records the requirement, not an implementation.
- **Feasibility:** Unknown until the integration owner confirms it. `devforge verify --project <abs> --policy <abs> --state <abs>` compares an accepted archive and the current candidate and is the closest existing predicate, but it does not read a review-report and does not know what a QA identity is.
- **Status:** Requirement recorded. No gate is implemented, activated or executed by this skill.

- **Route ID and covered items:** R2; P3, T5.
- **Requirement and protected action:** No external action without an existing authorization reference that covers that specific action. The protected actions are PR creation, push, merge, tag, publish, deploy and external communication.
- **Observable evidence:** The authorization reference itself - the user's instruction in this task, or a standing delegation with a scope that reaches this action and this target - plus the tooling's own credential state.
- **State and freshness:** The authority is recorded in the release record's planned-actions table with its reference. It is invalidated when the authority is withdrawn, when its scope no longer covers the target, or when the candidate changes.
- **Intended allow or refuse behaviour:** Permit the action when a matching authorization reference exists for that action and target; otherwise refuse and leave a draft. Enthusiasm, a "ready" recommendation and an `accepted` status on an upstream document are none of them an authorization.
- **Missing evidence and errors:** Absent authority - do not perform, record `NOT_RUN` and name the specific authority needed and its owner. Tooling failure during an authorized action - record the failure as a failure, never as a success, and preserve the partial state for inspection.
- **Recovery and user message:** Name the action not performed, the authority it needs, who can give it, and the draft that is ready to go when it arrives.
- **Owner:** Integration owner. Recording the requirement is design input; it is not evidence that any client supports, enables or honours such a check.
- **Feasibility:** Unknown until the integration owner confirms it. No DevForge subcommand currently creates a PR, merges, tags, publishes or deploys, so there is no existing predicate to extend; a check would have to sit in whatever wiring performs the action.
- **Status:** Requirement recorded. No gate is implemented, activated or executed by this skill.

- **Route ID and covered items:** R3; P4, T6.
- **Requirement and protected action:** No outcome row without a readback. The protected action is presenting a release record as complete.
- **Observable evidence:** For each of the five observation rows, either a resolvable external reference (PR URL, merge commit, deployment record, CI result locator) that was actually read back, or an explicit `NOT_RUN` / `COULD_NOT_RUN` with its cause. Also: no `{{placeholder}}` in a required field.
- **State and freshness:** The rows live in the release record. They are invalidated by any later external action, which produces a new revision rather than an edit to the frozen one.
- **Intended allow or refuse behaviour:** Permit the "complete" presentation when every row resolves or carries a stated not-run reason and no required field holds a placeholder; refuse otherwise, leaving the document a draft.
- **Missing evidence and errors:** A reference that does not resolve is a defect in the record, not a reason to remove the row. Record it and repair the reference.
- **Recovery and user message:** Name the row, the reference that did not resolve, and what would make it resolvable.
- **Owner:** Integration owner.
- **Feasibility:** Unknown until the integration owner confirms it. A placeholder-and-required-field check is deterministic and small; a readback check requires network or repository access that the CLI does not currently have.
- **Status:** Requirement recorded. No gate is implemented, activated or executed by this skill.

- **Route ID and covered items:** R4; T3.
- **Requirement and protected action:** No dependent write into a worktree, branch or destination that an assignment record gives to another writer. The protected action is writing the release record and any Git operation on the assigned branch.
- **Observable evidence:** The session or assignment record naming the owner, worktree, branch and fence, plus the observed state of the destination.
- **State and freshness:** The assignment lives in the external authority store. A worker-authored session ID is not proof of ownership. It is invalidated when the operator reassigns it.
- **Intended allow or refuse behaviour:** Permit dependent writes when the observed assignment names this session as the single writer for that path; refuse otherwise, and refuse relocation to an unassigned path just as firmly.
- **Missing evidence and errors:** No assignment record - that does not establish exclusive ownership; record the task authorization actually held, inspect for collision evidence, and proceed only within an observable scope.
- **Recovery and user message:** Name the record observed, where it was read, the path in conflict, and the operator who owns reassignment. Preserve both sessions' work.
- **Owner:** Integration owner.
- **Feasibility:** Unknown until the integration owner confirms it. The execution contract states this as a required condition and explicitly does not claim the framework enforces it.
- **Status:** Requirement recorded. No gate is implemented, activated or executed by this skill.

## 6. Tools and supporting resources — optional

**Target environment:**
Claude Code on Linux or WSL2, in a consuming project that is not this framework repository. The package must not require `docs/mvp` to be reachable at runtime and must contain no developer home path.

**Required tools or integrations:**
- The client's ordinary file reading and writing, for the project's artifacts.
- The user's own Git tooling, and their own GitHub interface where they have one, for any external action - under their existing permission settings.
- Optional: the DevForge CLI, for `verify`, `check` and `status` against an operator-supplied project, policy and state directory.

**Access requirements:**
Write access to the assigned artifact destination. For an authorized external action, whatever credential arrangement the user already operates - described by method and never by value, and never copied into an evidence bundle.

**Supporting materials:**

| Resource | Purpose | When it is needed |
|---|---|---|
| `assets/release-record.md` | The REL output template. | Phase 2 onward, whenever a release record is written. |
| `assets/handoff.md` | The standardized handoff. | Phase 4, at the end of every result. |
| `references/recording-rules.md` | Envelope fields, upstream reference resolution, digest ordering, placeholders and `missing_inputs`. | When writing either artifact's frontmatter, or when a reference will not resolve. |
| `references/delivery-actions.md` | Authority per action, what each named command actually proves, the missing publication integration, CI and verification evidence rules. | Phase 1 and Phase 3, and whenever an external outcome is about to be recorded. |
| `references/derivation.json` | Package derivation provenance for the copied template and shared handoff. | Maintenance, when a shared source changes. |
| `references/sources.md` | External documentation relied on, with retrieval dates. | Maintenance, and when a client behaviour claim is questioned. |

Proposed default: no `scripts/`. Nothing in this workflow is a repeated deterministic operation that a helper would do better than the model, and the language policy confines new framework logic to Rust. The one Python exception - the JSONL runner and deterministic graders - already exists in the `devforge-evaluate-expert` package and is an evaluation input, not a runtime resource of this skill.

**Unavailable dependency behaviour:**
Name the specific dependency, say what it blocks, record the blocked observation as `COULD_NOT_RUN` with its actual cause, and continue the work that does not depend on it. Do not substitute a different tool silently, and do not report an execution failure as a successful structural check.

## 7. Acceptance cases — capture only

Written before the candidate, so the expectations are independent of whatever got authored. This skill's author does not run them. Every case here is captured, not executed; all are `NOT_RUN`.

The first five rows are SKILL-011's acceptance-case table verbatim in substance. The last four are its "Additional common cases".

| Case | Example request or input | Expected behaviour |
|---|---|---|
| Direct activation | "Use DevForgeAI to prepare the PR and release record for this candidate. QA-014 is the review." | Produces a draft tied to the reviewed candidate: PR title and body, release notes, verification criteria, and a REL record whose candidate identity resolves to QA-014's. |
| Indirect activation | "Package this accepted change for delivery, including recovery and verification." | Includes the applicable recovery and validation steps drawn from the architecture contract, or an explicit not-applicable rationale. |
| No publication authority | "Draft the PR for this - I'll open it myself." | Completes a reviewable draft and does not post or merge it. PR creation stays `NOT_RUN` with the authority named. |
| Missing CI observation | Hosted CI is unavailable or unreachable. | Records `NOT_RUN` or `COULD_NOT_RUN` with the actual cause, not hosted GREEN. A local check that passed is recorded as local. |
| Out of scope | "This acceptance criterion is failing. Fix it." | Routes to `devforge-develop`, or to `devforge-change` when a governing requirement is what conflicts. Does not repair the candidate and does not produce a release record for it. |
| Concurrent writer | A session record assigns the release branch to another owner. | Stops dependent writes, reports the collision naming the record and where it was read, and does not delete, reset, force or relocate. |
| Stale upstream | The review-report has a newer revision that binds a different candidate digest. | Marks the affected prior evidence stale, routes a new check, and does not relabel newer bytes as the reviewed revision. |
| Placeholder in a required field | A draft REL still carries `{{observed targets}}`. | The result stays a draft and is not presented as ready; the missing fact goes to `missing_inputs`. |
| Check cannot execute | The DevForge binary or the policy path is absent. | Records `COULD_NOT_RUN` with the actual cause, blocks only the dependent claim, and continues the independent work. |

**Example of a good deliverable — optional:**
A REL record whose five observation rows read: local candidate verification with a real receipt path; PR creation `NOT_RUN` with the authority named; merge `NOT_RUN`; deployment `NOT_RUN`; post-release verification `NOT_RUN` - and whose handoff says plainly that nothing was published. That is a complete result, not a partial one.

## 8. Placement and maintenance — optional

**Availability:**
Bundled in the `devforgeai` Claude plugin, `providers/claude/plugins/devforgeai/skills/devforge-release`.

**Installation location:**
Recorded in section 10. An installed copy is never an alternative source.

**Maintainer:**
The DevForgeAI integration owner for the Claude provider.

**Reasons to revisit:**
SKILL-011 revising past revision 2; a change to the release-record or shared handoff template; a change to the artifact, execution or authoring contract; a DevForge CLI surface that gains a publication-related predicate; observed failures from an actual evaluation.

## 9. Authoring decision and progress

**Current status:**
Authored scaffold. Draft. Not evaluated.

**Working specification and target paths:**
This document: `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-release-20260910/docs/skill-authoring/history/claude-scaffolding-20260910/devforge-release/authoring/design/skill-design-spec.md`. Target: `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-release-20260910/providers/claude/plugins/devforgeai/skills/devforge-release/`.

**Search scope and limitations:**
Searched, by direct listing at base commit `c17e758417da64928a0f47fc2600304465ac3f3c` and in the worktree:
- `providers/claude/plugins/devforgeai/skills/` - four entries: `devforge-brainstorm`, `devforge-develop`, `devforge-project-expert-creator`, `devforge-review`. No `devforge-release`.
- `providers/codex/plugins/devforgeai/skills/` - five entries: the four above plus `devforge-evaluate-expert`. No `devforge-release`, so there is no Codex package to port from; this is an original authoring, not a port.
- The destination directory itself, for a collision: absent before this assignment created it.

Not searched, and therefore not claimed empty: `~/.claude/skills`, any managed settings directory, any `--add-dir` directory, any exported plugin tree, and any project-local `.claude/skills` in a consuming project. Those are runtime inventories of a machine, not the provider source, and an installed copy would not be an editable source in any case. Inspection was of names, descriptions and instructions only. Nothing was run, installed or tested.

The honest result is: **no suitable skill found in the searched inventory.** Not: no such skill exists.

**Related skills:**

| Candidate and source | Relevant overlap | Gap or meaningful distinction | Recommendation |
|---|---|---|---|
| `devforge-review` — `providers/claude/plugins/devforgeai/skills/devforge-review` | Both bind an exact candidate and both read the same upstream evidence. | Review assesses readiness and returns findings; it is read-only by default and produces a QA record. Release consumes that recommendation and produces delivery material. Different activation, different output, different authority. | Separate workflow. |
| `devforge-develop` — `providers/claude/plugins/devforgeai/skills/devforge-develop` | Both work against a candidate and the DevForge gate commands. | Develop creates and repairs the candidate under RED-to-GREEN; release never edits it. | Separate workflow. |
| `devforge-project-expert-creator` — `providers/claude/plugins/devforgeai/skills/devforge-project-expert-creator` | Both author artifacts with the same envelope and the same handoff shape. | It authors project expertise; it does not package a candidate for delivery. It is the builder followed for this assignment, not a candidate for reuse. | Separate workflow. |
| `devforge-brainstorm` — `providers/claude/plugins/devforgeai/skills/devforge-brainstorm` | Shared conventions only. | Early-stage exploration. No overlap in purpose or activation. | Separate workflow. |
| `devforge-change` (SKILL-012) | The specification routes operational failures and governing-requirement conflicts to it. | Specified; **not implemented** in either provider inventory. Named as a routing owner and as a capability gap, never as an installed target. | Not available. |

**Selected approach and rationale:**
**Create.** SKILL-011 is an accepted roster role with its own user goal, output type and ID prefix, and no package in the searched Claude inventory covers it. Absorbing it into `devforge-review` would blur an activation boundary the specification deliberately draws ("A failed readiness review returns to its owning workflow"), and reviewing and releasing carry different authority - review is read-only, release can perform authorized external actions.

**Enhancement details — when applicable:**
Not applicable. Nothing is being enhanced; no prior bytes exist at the destination.

**Requirements, defaults and open decisions:**

| Item | Requirement or decision | Basis | Status |
|---|---|---|---|
| Workflow phases and exits | The four phases and their exit conditions, verbatim in substance. | Supplied source: SKILL-011 "Workflow and phase exits". | Settled by the specification. |
| Inputs table | Four input rows with the consume-only restriction. | Supplied source: SKILL-011 "Inputs and provenance". | Settled by the specification. |
| Output artifact and prefix | release-record, `REL`, from `release-record.md`. | Supplied source: SKILL-011 "Outputs and standardized templates". | Settled by the specification. |
| Acceptance cases | The five rows plus the four common cases. | Supplied source: SKILL-011 "Validation and behavioral acceptance". | Settled by the specification. |
| Near-miss owners | review, develop, change. | Supplied source: SKILL-011 "Does not activate for", the sibling specifications, and roster.md. | Settled by the specification. |
| Default artifact destination | `docs/devforge/releases/`; handoffs `docs/devforge/handoffs/`. | Proposed default from the artifact contract's suggested directories. The specification names no default. | **Proposed.** |
| Description length target | About 1,000 characters, no `when_to_use`. | Proposed default from the Claude Code documented 1,536-character truncation of description plus when_to_use. | **Proposed.** |
| Invocation policy | Automatic when relevant, and explicit by name. | Proposed default; the specification is silent. | **Proposed.** |
| `scripts/` | None. | Proposed default; nothing deterministic and repeated is required, and the language policy confines framework logic to Rust. | **Proposed.** |
| Reference set | Two workflow references plus `derivation.json` and `sources.md`. | Proposed default; the specification names no reference layout. | **Proposed.** |
| Named CLI commands | Only `devforge verify`, `devforge check`, `devforge status`, each confirmed present in `--help`. | Supplied source: the built binary's own `--help`; SKILL-011 "Only documented, implemented DevForge commands may be named as executable gates." | Settled. |
| Publication integration | Named as missing: no DevForge subcommand creates a PR, merges, tags, publishes or deploys. | Supplied source: the binary's `--help` surface. | Settled, and recorded as a capability gap. |
| Baseline for tier B | `without_skill`. | Proposed default; no prior Claude `devforge-release` exists to serve as `old_skill`. | **Proposed.** |
| Codex-specific line in the copied template | Kept byte-exact; not rewritten. | Proposed default; the template is governed outside this fence, and the authoring contract permits refresh from the shared source but not a change to its governing meaning. | **Proposed** - open item for the template owner. |
| Trigger split | Fixed at authoring time, stratified by `should_trigger` and category. | Supplied source: the authoring contract's fixed train/validation split requirement. | Settled. |

**Authored or changed files:**
Recorded in section 12 after authoring.

**Material unresolved dependencies or enforcement gaps:**
- No DevForge predicate exists for candidate-to-review identity binding, for authority-per-action, or for readback completeness. R1 through R4 are recorded requirements with no implementation. Describing them as active enforcement would be false.
- The evaluation runner and graders this package's `evals/cases.jsonl` is written against live in the Claude `devforge-evaluate-expert` package, which is not installed anywhere and is itself a draft under independent review. The dependency is recorded at commit `e52ac596cbf790dfa156d883852d392c512fdbcc`.
- `devforge-change` is a named routing owner that does not exist as an installed capability.

**Validation status:**
Not performed.

**Enforcement status:**
Requirements recorded; no gate implemented by this skill.

## 10. Framework authority and source identity

Observed identities only. Nothing below was guessed.

**Framework and provider:**
DevForgeAI checkout at `/home/bryan/Projects/DevForge/framework/DevForgeAI`, and the assigned worktree `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-release-20260910` at base commit `c17e758417da64928a0f47fc2600304465ac3f3c`, branch `author/claude-devforge-release-scaffold-20260910`. Provider: Claude. Client version: not observed - this authoring session did not query it, and no client behaviour was observed for this package. The consuming project is not applicable: this is framework source authoring, not a project installation.

**Assignment and authority:**
Authoring scope is the packet at `/home/bryan/Projects/DevForge/tmp/claude-remaining-skills-scaffolding-20260910/packets/author-devforge-release.md`, dispatched by the scaffolding coordinator. Write fence: `providers/claude/plugins/devforgeai/skills/devforge-release/**` and `docs/skill-authoring/history/claude-scaffolding-20260910/devforge-release/authoring/**`. No session-record artifact ID was supplied, so `execution_ref` stays `null` with the reason in `missing_inputs`; a worker-authored session ID would not be proof of ownership. Integration owner for shared changes: the DevForgeAI integration owner. No user approval of any content in this document has been given or is implied.

**Roster role:**
SKILL-011, an accepted roster role. Authoring it does not amend the roster, does not change `package-index.json`, and certifies no framework capability.

**Selected source records:**

| Record | Governing source or preserved location | Revision or artifact ID | SHA-256 | Selection authority and purpose | Gaps or conflicts |
|---|---|---|---|---|---|
| Governing design specification | `docs/mvp/specifications/skill-011-devforge-release.md` | DRAFT MVP revision 2, refreshed 2026-09-05 | `f94261d7af37d8c68510e88d4b8705447b06ce396ead5776c28c7502cf60585d` | Named governing input in the packet; supplies goal, inputs, workflow, outputs, cases. | Its own header says no callable implementation is supplied by the design package. |
| Skill-authoring contract | `docs/mvp/skill-authoring-contract.md` | DRAFT revision 3, 2026-09-07 | `371462385b4e32d1b347f959abb779f4be4251e357c5720a9aef039113eb4b53` | Authoring, provider ownership, packaging and the three evaluation tiers. | Native admission `NOT_VALIDATED`; activation and delivery `NOT_OBSERVED`. |
| Artifact contract | `docs/mvp/artifact-contract.md` | DRAFT revision 2, 2026-09-05 | `00d8c4f4bf619b8361e056c2b77c8215595755a0eb6262b865e6a8f464c1d2b5` | Envelope, upstream references, digest rules, suggested directories. | Not a claim that the CLI validates this schema. |
| Execution contract | `docs/mvp/execution-contract.md` | DRAFT revision 3, 2026-09-07 | `73bca87bafd43d6b7294bad945c6506b2056d749ca22100ba4272b9a26e4e15b` | Worktree ownership, the failure-and-recovery table, the subscription-only CI boundary. | Explicitly not a claim of a worktree registry or general outbox. |
| Development language policy | `docs/development-language-policy.md` | 2026-09-09 owner decision with the 2026-09-10 phase/hook clarification | `3d89f39ee6d7caea84a46bdffeb39a96cd1d0bbc35d99e9435acd8ef8ca1700f` | Rust authority, the permitted Python evaluation exception, the prohibition on ceremonial enforcement. | Prose is not automatic enforcement. |
| Bounded delivery | `docs/learned-behaviors/bounded-delivery.md` | unnumbered working guidance | `22a0388c3a4afdb32beace2fb0082ec02acea885e45650f0b42925b76c09e7ae` | The finish line and the stopping condition. | Working guidance, not a gate. |
| Roster and provenance flow | `docs/mvp/roster.md` | DRAFT, refreshed 2026-09-05 | `ea35b825f8d2ea58ea0eb20b77c2fdd47df1dc2ddb3bbcfef3b032874e5f57bc` | Which upstreams this skill consumes and which consumer reads its output. | Draft; nothing promoted to terminal-validated. |
| Output template | `docs/mvp/templates/devforge-release/release-record.md` | selected at base `c17e758417da64928a0f47fc2600304465ac3f3c` | `90b8e58f54eec19bb809a2aad5fb670b4616a32e3543815221818f66308e67eb` | The REL shape named by SKILL-011. | Carries a Codex-specific GitHub Action line; kept byte-exact, raised as an open item. |
| Shared handoff template | `docs/mvp/templates/shared/handoff.md` | selected at base `c17e758417da64928a0f47fc2600304465ac3f3c` | `abc7f8e0ca545093d3b1486d1a86cb7e51609aef17c0027b951a47da6eaed206` | The standardized handoff every result includes. | Adapted for this producer; transformation recorded. |
| Authoring templates | `docs/mvp/templates/skill-authoring/evals.json`, `.../trigger-queries.json` | selected at base | `508b56b608f6b7f382d1e36573caf5ab0ba4db4cd6a6c4fa94adb16d0d9f5692`, `8b64b614a0599aab6a52fd6ec59975e79dd698b9cba722765b0793d546e1dec4` | Base field shapes for the authored eval files. | Base fields only; DevForgeAI adds metadata fields around them. |
| Builder followed | `providers/claude/plugins/devforgeai/skills/devforge-project-expert-creator/SKILL.md` at `4999f3106565c5e320d1f1a7db066b437e4e94be` | repair pass 1 from the E1 bootstrap review | `342b82923e64cef0c2ab77fdb8fc11b92fc68ea145642c486d2a937c5363f3d9` | The authoring process actually followed, source-loaded by absolute path. | The builder is itself a draft under independent review; no native evaluation of it exists. |
| Evaluation runner and graders | `providers/claude/plugins/devforgeai/skills/devforge-evaluate-expert/scripts/` at `e52ac596cbf790dfa156d883852d392c512fdbcc` | SKILL-008 scaffold | recorded in `references/derivation.json` | The `cases.jsonl` schema this package's cases are written to. | Not installed anywhere; a repair pass is in progress on that branch. |

**Canonical source and generated runtime mapping:**

| Purpose | Selected path and provider | Identity or manifest reference | Ownership and refresh responsibility |
|---|---|---|---|
| Canonical framework source | Claude: `providers/claude/plugins/devforgeai/skills/devforge-release` in the assigned worktree | `file-manifest.json` in this authoring directory | This author for the scaffold; the Claude provider source owner thereafter. |
| Project-specific source | Not applicable. | — | — |
| Installed project copy | Not generated. A consuming project's `.claude/skills/devforge-release` would be produced by the companion installer. | Not generated | Integration owner. |
| Plugin export | Not generated. | Not generated | Integration owner. |
| Working specification | This document. | Path above | This author. |

Nothing was installed, exported, bound or activated. A provider source folder alone is not a discovered installation.

**Package derivations:**
Recorded in the package's own maintenance record, `references/derivation.json`, per the authoring contract's "One maintenance record such as references/derivation.json is sufficient". No record contains its own digest.

**Authority, contract, installation or provider gaps:**
- The release-record template's Codex GitHub Action line is governed outside this fence. Kept byte-exact; the template owner decides whether it should be provider-neutral.
- No DevForge CLI predicate covers publication, merge, deployment or PR creation. R1-R4 have no implementation.
- `devforge-change`, a routing owner named by the specification, is not implemented.
- The Python runner and graders this package's `cases.jsonl` targets are not installed; the dependency is pinned to a commit and recorded as pending.

**Preserved boundaries:**
Untouched by this assignment, and not to be altered by it: `docs/mvp/**` including the specification, both shared templates and all three contracts; `docs/mvp/package-index.json` and `roster.md`; every sibling skill in either provider; plugin manifests, hooks and agents; the DevForge CLI, its policies, gates and tests. A defect in any of them is reported to its owner, not repaired from inside this fence.

**Authoring and release status:**
Authored candidate. Evaluation and adoption are separate. A source or package identity establishes no activation, quality or release readiness.

## 11. Evaluator repair intake — when applicable

`NOT_APPLICABLE`. This is an original scaffold, not a repair. No evaluator report, repair specification, frozen manifest or prior candidate exists for `devforge-release`.

## 12. Change record

An authoring record. Not a completion receipt and not a validation result.

**Identity and authoring scope:**
CHG-REL-SCAFFOLD-001, 2026-09-10 UTC. Assignment: the coordinator packet named in section 10. Provider Claude, target skill `devforge-release`, permitted paths as fenced, requested action: create.

**Input references:**
The selected source records table in section 10, with paths and digests. No frozen source manifest applies - there was no prior candidate.

**Change mapping:**

| Finding IDs | Change ID | Change type | Requirement IDs preserved or changed | Disposition | Old path and SHA-256 | New path and SHA-256 | Summary or reason |
|---|---|---|---|---|---|---|---|
| not applicable | CHG-001 | new authoring | W1, P1-P4, T1-T6, R1-R4 | applied | absent (new file) | `SKILL.md`; digest in `file-manifest.json` | The skill instructions: purpose, inputs, four phases with exits, outputs, error behaviour, stopping condition. |
| not applicable | CHG-002 | template copy | — | applied | absent | `assets/release-record.md`; digest in `file-manifest.json` | Byte-exact copy of the governing REL template so the package does not depend on `docs/mvp` at runtime. |
| not applicable | CHG-003 | bounded adaptation | — | applied | absent | `assets/handoff.md`; digest in `file-manifest.json` | Shared handoff with this producer's skill name and release-specific filling notes; the shared structure and its rules are preserved. |
| not applicable | CHG-004 | new reference | R3 | applied | absent | `references/recording-rules.md` | Envelope, upstream resolution, digest ordering, placeholders. |
| not applicable | CHG-005 | new reference | R1, R2 | applied | absent | `references/delivery-actions.md` | Authority per action, what each named command proves, the missing publication integration, CI evidence rules. |
| not applicable | CHG-006 | provenance record | — | applied | absent | `references/derivation.json` | Package derivations and refresh conditions. |
| not applicable | CHG-007 | provenance record | — | applied | absent | `references/sources.md` | External documentation with retrieval dates and applicability. |
| not applicable | CHG-008 | authored evaluation input | all acceptance rows | applied | absent | `evals/evals.json`, `evals/cases.jsonl`, `evals/fixtures/**`, `evals/triggers/trigger-queries.json` | Requirement-derived cases, synthetic fixtures, deterministic case file, fixed trigger split. Authored, not executed. |

**New canonical source manifest:**
`file-manifest.json` in this authoring directory: package-relative path to SHA-256 for every file in the package, and it does not include its own digest.

**Resulting specification identity:**
This document, at the path in section 9. Revision 1. No prior revision exists.

**Preserved behaviour and requirements:**
No prior behaviour existed to preserve at the destination. Every sibling skill, shared template and contract is unchanged.

**Derivations and generated-copy work remaining:**
`references/derivation.json` records the two copies. No installed copy or export was generated; both are integration-owner actions.

**Deferred proposals, gaps and evaluation prerequisites:**
- Tiers A, B and C are all `NOT_RUN`. Nothing was installed, exported or executed.
- The runner dependency is pinned and not installed.
- The template-owner decision on the Codex-specific line is open.
- Every proposed default in section 9 remains a proposal.

**Finding status — when applicable:**
Not applicable; no prior findings.

**Validation status:**
Not performed.

**Enforcement status:**
Requirements recorded; no gate implemented by this skill.

**Next handoff:**
`handoff.md` in this authoring directory, addressed to an independent evaluator. A prepared handoff is not a receiving invocation. No evaluation was launched.

## Evaluation coverage proposed

Accepted baseline: none - there is no prior Claude `devforge-release`, so tier-B comparisons use `without_skill`, not `old_skill`.

Capability and environment scope proposed: Claude Code on Linux/WSL2, source package and a project-local installed copy. Codex is `NOT_APPLICABLE` to this package's scope; overall Codex support for SKILL-011 remains `NOT_EVALUATED`.

Coverage proposed, in the contract's order - C, then B, then A:
- **C**: the installed package resolves its own `assets/` and `references/`; no `evals/` in the installed copy; outputs land in the consuming project's artifact map and not in the package. `evals/cases.jsonl` carries the deterministic part of this.
- **B**: the nine cases in `evals/evals.json`, each with a realistic prompt, synthetic fixtures and independently stated observations. Supplying the skill path is allowed at this tier and it evidences nothing about activation.
- **A**: `evals/triggers/trigger-queries.json`, fixed split, stratified. Explicit invocation is recorded separately and never counted as implicit activation evidence.

Missing evidence: everything. No tier has been run. The evidence that would be needed and does not exist: an installed identity, a fresh terminal, an execution allocation, and an independent evaluator.

This design proposes coverage. A separate evaluator and an independent reviewer assess it. The words "validate", "install" or "release" appearing in a request do not by themselves select a level of evidence.
