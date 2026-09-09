# Contributor context workflow: skill specification draft

Status: DRAFT FOR REVIEW, revision 1, 2026-09-05. This operator-authored proposal uses the existing expert-spec content model. No native expert creator was invoked, no expert package exists, and this document does not allocate a worker or approve production expertise.

## Concrete capability

- Proposed capability: CAP-CCR-001, repeatedly orient or resume a bounded DevForgeAI contribution from shared records, producing a durable handoff at the relevant checkpoint.
- Proposed native skill name: `devforgeai-contribution-context`.
- Consuming project: DevForgeAI; companion DevForge references are included only where the selected assignment makes them relevant.
- Target runtimes: Codex and Claude, with separate native package identities and observations before either support claim.
- Initial roles: architect/integration operator, Codex contributor worker, and Claude contributor worker. Runtime does not determine role or authority.
- Motivation: the current operator repeatedly selects governing inputs, reconciles assignment and evidence state, and translates findings into resumable tasks. The [contributor proposal](20260905-contributor-expertise-proposal.md) identifies the risk of relying on the architect's conversation for that knowledge.
- Reuse decision: first provide the required records through a bounded context packet. A new standing expert is justified only if it improves recurring interpretation or handoff work beyond the same core instructions and records without that expert.

The intended deliverable is a reusable native skill, not a bespoke handoff prompt for every worker invocation. Its repeatable workflow is: identify the assigned task -> resolve selected records -> assess readiness for the next action -> return control to the authorized workflow, or persist a checkpoint when required.

The capability ends with context recovery and the appropriate mode's output. It does not perform the underlying code/skill repair, independently certify that repair, take over another assignment, integrate Git changes, launch evaluation campaigns, or change external policy. The calling session may continue an already authorized task without another permission round merely because context was recovered.

## Invocation and modes

The project/session setup supplies a stable task/assignment locator and the selected authority roots. Once those are supplied, a normal request such as “Resume my assigned DevForgeAI contribution” can use the installed skill to retrieve the applicable records. This is a proposed natural-language use case, not a claim of current discovery or an invented command. The skill cannot recover facts that were never persisted or read records its runtime cannot access.

| Mode | Trigger | Result |
| --- | --- | --- |
| Orient / resume | Start a session, resume the same assigned work, or check whether the next action has its required context | Concise in-session readiness, relevant record references, unresolved prerequisites and the next already authorized action; no new HANDOFF for an ordinary read-only check |
| Checkpoint / transfer | Explicit handoff request, work transfer, a pause needing durable recovery, ownership release, or completion of work whose governing workflow requires recorded delivery | A finalized HANDOFF and externally delivered full path/SHA-256 using the existing contract |

Reuse current records instead of generating successive handoffs that merely restate unchanged state. A user-requested new checkpoint is still honored. A routine orientation response does not replace an authoring, evaluation, release, or other workflow's required closeout evidence.

The generated [native expert template](../mvp/templates/devforge-project-expert-creator/expert-skill.md) leaves deliverables and handoff behavior to the capability specification. The creator's own required authoring handoff remains distinct from each later invocation of the created expert. No shared-contract amendment is proposed for these two modes.

## Activation boundary

| Request or condition | Intended behavior |
| --- | --- |
| Explicit request to recover contribution context or prepare its handoff | Load the capability, select the requested mode, and recover the selected records |
| Fresh/replacement terminal asks what contribution it is assigned and what it may do next | Recover the applicable assignment and inputs; distinguish known facts from missing prerequisites |
| A returned contribution needs a continuation assembled from preserved records | Recover the next action from recorded outcomes and unresolved findings; persist a handoff when a checkpoint trigger applies |
| Assignment is absent, contradictory, or inaccessible | Diagnose the gap in-session; if checkpoint mode is requested, persist only to an independently authorized outbox; do not invent ownership |
| Ordinary implementation with complete usable context | Continue the actual implementation workflow; this expertise is not mandatory merely because the repository is DevForgeAI |
| General application brainstorming, arbitrary code explanation, or final semantic QA | Use the relevant workflow; this capability does not become a universal router or reviewer |

## Inputs and source selection

The caller or prior project/session setup supplies a bounded task, the selected project/authority roots and actual execution assignment. Checkpoint mode additionally needs a permitted output location. An existing handoff is optional input; it is not a prerequisite to every invocation. Other optional inputs include a relevant finding report and candidate/evaluation records. The capability may follow their in-scope references; it must not search for a more permissive owner, policy, or root.

Required facts, when applicable to the selected task:

| Fact | Source and treatment |
| --- | --- |
| Role, owner, authorization and assignment state | Actual selected SESSION/authorization record; distinguish runtime provider from task role |
| Worktree, branch/base and write fence | Recorded assignment plus permitted observations; an old producer field does not establish a current owner |
| Applicable decisions | Exact adopted decision or valid prior delegation, including scope; current task wording need not repeat a still-applicable delegation |
| Governing rules and task excerpts | Selected revisions, hashes and sections with resolvable source bytes; newer main-branch text is not an automatic replacement |
| Required expertise | Needed capability, selected package and relevant evaluation; absent/non-required expertise is disclosed without inventing an installed package |
| Candidate and evidence state | Exact candidate/export/run identity, recorded checks, open findings and limitations; a report's PASS is a claim to attribute, not independent acceptance |
| Current phase and continuation | Actual preserved observations and prerequisites; gaps and contradictions remain explicit |

The [execution contract](../mvp/execution-contract.md), [artifact contract](../mvp/artifact-contract.md), [authoring contract](../mvp/skill-authoring-contract.md), and selected [session](../mvp/templates/shared/session-record.md) and [handoff](../mvp/templates/shared/handoff.md) templates supply the existing rules. The [expert creator specification](../mvp/specifications/skill-007-devforge-project-expert-creator.md) supplies the reuse, specification, evaluation, and refresh model. Exact reviewed bytes are preserved through the companion custody receipt; these references do not amend the inputs selected for active author sessions.

## Required behavior

| Requirement | Observable behavior |
| --- | --- |
| CCR-001 — Establish the recovery task | Identify the actual task, mode, role, provider, owner, selected assignment and permitted output when required. State what is unknown. |
| CCR-002 — Resolve the selected context | Read the required accessible records; match relevant identities, locators, digests and sections. Keep selected older revisions distinct from newly observed versions. |
| CCR-003 — Preserve authority | Carry applicable prior authorization with its scope. Accepted-looking labels, stale producer metadata or suggested next steps do not grant authority. |
| CCR-004 — Reconstruct state from evidence | Distinguish context-recovery progress, underlying contribution state, recorded check outcomes and acceptance. Attribute unverified claims and identify contradictions. |
| CCR-005 — Select bounded context | Include the rules and source references needed for this task. Follow necessary dependencies; exclude irrelevant project history and another author's private deliberation. |
| CCR-006 — Preserve uncertainty and ownership | Report missing or contradictory prerequisites and stop dependent target actions. Continue only the independently authorized recovery/reporting work. |
| CCR-007 — Return one continuation | Identify the next action, owner or unresolved-owner gap, prerequisites, output and completion evidence. Return control to the calling workflow; do not independently start unrelated or unassigned work. |
| CCR-008 — Deliver the required mode output | Orient/resume returns a concise, accurate in-session result without unnecessary file writes. Checkpoint mode finalizes and reads back the handoff, then delivers its permitted path and complete 64-character SHA-256 externally; no self-digest inside the handoff. |

Successful recovery can correctly conclude that the underlying contribution is blocked. It can also correctly conclude that previously delegated work may proceed. Neither result follows merely from the provider, role name, or absence of an error.

The worker checks the validity of references it consumes and delivers. It may identify an obvious contradiction between referenced records. Full regrading of native transcripts, deciding whether an implementation meets its specification, or repairing a general validator belongs to separately assigned evaluation/review/tooling work.

## Output contract

For orient/resume, return only the context needed to continue: identified task and role, the selected record references, readiness for the specific next action, and material gaps. A short response may point to an already pinned manifest rather than dump every source digest. It must not present a hash abbreviation as an exact receipt. Repeated invocation with unchanged facts should neither rewrite task records nor manufacture new ownership or completion state.

For checkpoint/transfer, produce one handoff using the selected shared template, with its inputs table serving as the recovered context inventory. Keep the original records authoritative; the handoff is a derived view, not a replacement registry.

The handoff must make these facts directly recoverable:

1. The recovery task and the underlying contribution task, with their states distinguished.
2. Role/provider/owner, assignment reference, worktree/base/fence and applicable authorization.
3. Required input/package/candidate/evidence identities, verification performed, and explicit unavailable facts.
4. Relevant open finding identities, conflicting observations and the affected continuation.
5. One next task with prerequisites, owner, output destination and completion checks.
6. Ownership disposition, actual observed checks, and changes that would invalidate this recovered view.

When reporting check outcomes, use exactly the existing vocabulary: PASS, FAIL, NOT_RUN, COULD_NOT_RUN, NOT_APPLICABLE. Readiness for an identified next action is a separate assessment, not acceptance or certification. Scope labels correctly: a recovery behavior test may PASS because it honestly identifies unavailable required input; the failed/unavailable underlying check must retain its own outcome. Do not classify an unrecognized required record as inapplicable.

When a required input is inaccessible, record its known expected identity and the failed resolution without claiming to have verified its contents. Do not copy author-private state or credentials into the handoff. In checkpoint mode, when no authorized writable delivery path exists, report that specific limitation through the permitted terminal channel; do not invent a substitute outbox. Ordinary orientation does not require such a path.

## Role-specific application

| Role in the selected assignment | Required recovered perspective |
| --- | --- |
| Architect/integration operator | Relevant author assignments, selected common rules, candidate/evidence identities, unresolved integration dependencies and next review/integration task; authority remains explicit |
| Codex contributor worker | Its own assignment, Codex source/package selection, scoped findings, protected shared/Claude/companion paths, and next permitted contribution step |
| Claude contributor worker | Its own assignment, Claude source/package selection, scoped findings, protected shared/Codex/companion paths, and next permitted contribution step |

Information about a peer is limited to what the selected task needs for dependencies and collision detection. A fresh architect is not entitled to inherit every worker's private reasoning. Current author sessions do not become independent reviewers by changing labels.

## Candidate-independent acceptance

The companion [evaluation plan](20260905-contributor-context-evaluation-plan.md) defines the cases and comparison. It is a prospective companion, not an upstream authority for this specification. Requirement and case IDs are local identifiers in these draft documents; no runtime artifact registry is claimed.

The candidate must satisfy CCR-001 through CCR-008 in applicable cases, including truthful blocked outcomes, valid prior delegation, mode selection, and complete required delivery. No invented authority, silent input substitution, cross-fence mutation, forged verification, or incomplete required receipt is acceptable. Acknowledging a context packet is not sufficient: the in-session result or handoff must support the correct next action. Checkpoint-only assertions are excluded from ordinary orientation by the mode defined before execution, not because a required artifact happened to be missing.

Measured value must be assessed against the same core workflow, facts, tool access and runtime setup without the contributor expert. If that baseline already meets the need and the expert provides no demonstrated benefit, retaining the packet alone is a valid disposition.

## Permissions, packaging and refresh

The initial pilot needs read access to selected fixture records. Orient/resume needs no project write permission; checkpoint mode gets only its fresh report outbox. Candidate repositories, control records, peer outputs, real Git metadata, external policy/runner and expected-answer files remain outside the evaluated worker's write authority. Tools may inspect and hash authorized inputs; no network or subscription-state mutation is part of this recovery task.

Keep stable decision guidance in the candidate SKILL.md and focused references. Dynamic session IDs, live owners, current grades, project paths and handoff status remain in supplied records. Runtime resources must be package-local and evaluated in the actual installation mode.

Provider source/install mappings must be explicit in the future authoring assignment. The proposed name is not a discovered installation or a new CLI command. Existing portable example support does not settle arbitrary project-expert packaging.

Refresh only when relevant governing rules, package/provider behavior, selected source layout or observed failures warrant it. Changed skill bytes receive a new package identity and affected evaluation; changing assignment facts updates the external records and recovered handoff rather than hard-coding them into the skill.

## Readiness and continuation

This specification is ready for design review. Native authoring and evaluation are not assigned by it. Before that work, an owner must select the exact specification/cases, source/install mapping, isolated runtime and synthetic fixtures, actual author/evaluator assignments, budgets and preserved outputs.

The creator specification requires an architecture contract for production expertise. No production architecture contract for this contributor capability has been selected here. A bounded bootstrap experiment must declare its limited source basis, and its results cannot be promoted to production suitability without resolving that requirement.

The first implementation decision is whether a bounded context packet already meets the need. Any later skill authoring must preserve the active SESSION-001 and SESSION-002 assignments and use its own explicitly allocated source and evaluation scope.

Exact document/source identities and creation time are recorded in the [external receipt](20260905-contributor-context-specification.receipt.json). Behavioral evaluation: NOT_RUN. Skill authoring: NOT_RUN. Production adoption: NOT_RECORDED.
