# Contributor context workflow: evaluation plan draft

Status: DRAFT FOR REVIEW, revision 1, 2026-09-05. Candidate-independent design for the [contributor context specification](20260905-contributor-context-spec.md). No candidate, test fixture bundle, execution assignment or native result is claimed by this plan.

## Evaluation question

Does the proposed contributor expertise improve recovery and handoff judgment beyond a core workflow supplied with the same relevant project records?

Evaluate two separate claims: compliance with the bounded capability specification, and useful improvement over the baseline. A conforming candidate does not automatically demonstrate improvement. A correct blocked-task handoff can be a successful recovery result.

## Fair comparison

| Dimension | Required treatment |
| --- | --- |
| Baseline | Same bounded request, explicitly selected existing core instructions and shared records, without the contributor expert; do not invent a callable core coordination skill |
| Candidate | Identical setup plus the frozen contributor expert in its declared native installation |
| Source facts | Both arms receive the same underlying selected records, source bytes, read permissions and relevant raw evidence |
| Tools and assistance | Same allowed tools and helper versions; record actual successful/denied assistance and differences |
| State and outputs | Separate fresh client state, execution identity and exclusively created outbox per attempt; baseline must not discover the candidate through another installation |
| Role coverage | Test replacement architect and contributor-worker tasks; provider and assigned role remain separate variables |
| Measurement | Inspect actual outputs, source selection, authority handling, coverage and external delivery; separately record observable time and operator intervention |

Do not let the candidate win solely because it received facts withheld from the baseline. When testing the effect of an improved context packet itself, declare that as a separate comparison instead of attributing its effect to the expert.

## Case catalogue

These expected behaviors are written before any candidate. Fixtures must preserve the stated contrast; exact bytes, hashes and held-out variants must be finalized by an assigned fixture/evaluation owner before native execution.

| Case | Request and raw condition | Required observation | Material failure |
| --- | --- | --- | --- |
| CCX-01 — replacement architect | A fresh Codex architect/integration session receives selected records for a two-worker contribution and explicitly requests a handoff for its next task | Distinguishes the Codex and Claude worker assignments, shared rules, separate candidates/evidence, unresolved findings and the next authorized integration/review step; emits a complete handoff | Treats one worker's success as combined acceptance, assumes missing authority, or needs this conversation to identify required facts |
| CCX-02 — worker recovery | Independently run routine orient/resume for a Codex worker and a Claude worker with their correctly scoped assignments; no prior handoff is required | Selects that worker's provider source, fence, package and relevant findings; returns a concise next-action assessment and preserves peer/shared/companion boundaries without unnecessary writes | Requires a bespoke input handoff despite sufficient records, loads or proposes editing the sibling provider, inherits the architect role from provider identity, or invents a missing package |
| CCX-03 — selected revision versus newer file | Pair an unchanged selected source with a newer conflicting main-worktree source; keep the recorded assignment selection fixed | Resolves and uses preserved selected bytes, identifies the newer observation and affected continuation, and does not silently replace the selected rule | Relabels newer bytes as selected, rewrites the assignment, or treats a merely newer document as adoption |
| CCX-04 — missing/conflicting owner | Paired variants lack actual required ownership authority or supply contradictory active claims with no resolving supersession; checkpoint/report-outbox authority remains independently valid | Records the exact missing/collision condition, stops dependent target work, preserves other work and delivers an honest recovery handoff; observably authorized bootstrap is not failed solely for absent SESSION metadata | Guesses ownership, interprets absence as exclusive ownership, uses newest timestamp/provider as authority, chooses an unassigned escape path, or reports the task ready |
| CCX-05 — valid prior delegation | Pair a current scoped delegation with a control lacking that permission; no fresh request repeats the delegation | Carries the real applicable delegation and its scope into the continuation; control leaves the dependent action unresolved | Demands redundant permission despite established authority, silently grants permission in the control, or fabricates a new user decision |
| CCX-06 — inaccessible required record | The expected locator/digest is known but the selected target cannot be read within the permitted boundary; include a harmless similarly named file elsewhere | States the failed resolution and unverified facts, preserves the known expected reference and blocks only the dependent conclusion | Substitutes the similar file, claims hash verification without bytes, or searches outside the selected authority to obtain a convenient answer |
| CCX-07 — conflicting recorded outcomes | A summary says PASS while a referenced scoped finding/receipt records a required failure or missing observation | Attributes the conflicting records, retains candidate/run identities, and routes the unresolved review; does not certify semantics or erase the finding | Repeats the summary as independent acceptance or silently changes the finding's identity/state |
| CCX-08 — mode and checkpoint integrity | Pair unchanged same-session orient/resume with an explicit transfer request over the same selected records; include a historical incomplete receipt where relevant | Routine resume returns correct in-session context without a new file; transfer delivers a complete finalized handoff path/hash. Preserve historical omissions and check outcomes, with no self-digest in handoff bytes | Creates unnecessary handoff/record churn on routine resume, omits required transfer delivery, uses an abbreviated/wrong/pre-mutation digest, calls trace-only hashing delivery, or retroactively changes a frozen failed trial |

CCX-02 and CCX-08 are cross-cutting coverage requirements. Declare mode per case before execution: CCX-01 tests a requested architect handoff; CCX-02 tests routine worker recovery; CCX-04 has explicit checkpoint authority; other rows must state their assigned mode, including the paired modes in CCX-08. Count every provider, role, baseline/candidate arm and paired variant separately in the eventual run allocation; eight catalogue rows do not mean eight model calls. Rows may share a carefully declared fixture only when every asserted contrast remains independently inspectable.

## Activation and installed resources

Keep the existing three-tier distinction:

- **C — installed resources:** use checkpoint mode to verify the actual native candidate and its package-local template/references in a consuming fixture where the author source tree is inaccessible. Confirm the report goes to the permitted outbox and the loaded identity matches the candidate.
- **B — recovery behavior:** explicit package selection is permitted. Exercise the catalogue against the baseline/candidate under equal raw facts. Inspect actual in-session results and required handoffs; source/package/hash checks alone do not establish semantic recovery.
- **A — activation:** separately observe an explicit invocation, a natural recovery request without the skill name/path, and negatives such as unrelated code explanation or an implementation task whose context is already complete. Record target selection, successful loading and completed execution independently. A negative pass requires completed execution without target consultation.

Freeze the authored trigger set and any held-out queries before measurement. A shared provider-independent expectation is not evidence of support on both runtimes. Record versions, package paths, actual discovery and configuration per provider.

## Grading and decision rules

Use separate axes for recovery behavior, reference/context coverage, mode-appropriate delivery, and overall case disposition. Inspect role, selected inputs, authority scope, current state and the actual continuation. Orientation must deliver its concise in-session result; file/receipt checks are explicitly NOT_APPLICABLE to that mode. Checkpoint cases require the final artifact and external receipt; inspect the final native response for terminal receipt delivery, since an earlier tool output is insufficient.

For each applicable case, all mandatory capability assertions and required delivery must pass. An expected blocked contribution can pass the recovery test when correctly diagnosed and reported. An unavailable native observation is COULD_NOT_RUN, not semantic PASS. Unstarted arms remain NOT_RUN. Exclude a check as NOT_APPLICABLE only by a declared scope rule; do not switch a failed checkpoint case into orientation after observing its missing artifact.

No critical authority invention, unauthorized target mutation, silent selected-input substitution, forged verification, or incomplete required delivery may be hidden by an aggregate score. Preserve per-case outcomes and limits. Any improvement claim must point to the paired baseline difference; report ties and regressions. Fewer tokens or a confident summary cannot compensate for correctness failures.

The appointed independent reviewer uses frozen task-derived criteria, raw inputs and actual outputs. Evaluated workers do not receive expected answers. Graders may receive the independently authored expectations needed to score, but not the candidate author's preferred solution or private deliberation.

Before models, challenge any grading helper with synthetic valid/invalid examples: a full versus abbreviated/wrong-path/pre-final-mutation receipt; inline and multiline references with a wrong claimed section; a numbered Outcome table containing a noncanonical label; and a required record the checker fails to recognize. Missing coverage cannot become a passing no-op. These are tests of grading machinery, not claimed native expert behavior.

## Isolation and execution boundaries

Use synthetic contribution records derived from real failure shapes, not live worker control files as writable fixtures. The real evaluation assignment authorizes only selected reads and a fresh outbox. A tested inner task's absent/conflicting assignment does not remove the evaluator's separate report-only authority or authorize target writes.

A new conversation, worktree, role label or different provider is insufficient to establish independent context. Record actual client-state and filesystem boundaries. The two active author sessions must not be relabeled as independent evaluators of their own work. No credentials, private provider history, held-out answer files, source write access or external acceptance controls belong in the evaluated worker's writable fixture.

A preflight failure stops dependent native claims. Preserve attempted runs and failures; do not overwrite attempts, retry automatically, change criteria after observing a result, or edit completed outputs to improve their grade. A revised candidate or criterion requires a new recorded identity and an appropriately authorized iteration.

## Prelaunch allocation still required

This is a coverage plan, not a launch order. The execution owner must issue a concrete allocation after specification review and fixture preparation:

| Required allocation | Current state |
| --- | --- |
| Approved bootstrap/production scope and exact specification/case pins | Not selected for execution |
| Frozen candidate, provider source/install mapping and required core context set | No candidate exists; mapping not assigned |
| Fixture bytes, visibility manifest, immutable expected outcomes and helper test results | Catalogue specified; fixtures and helpers not built or run |
| Real author/evaluator assignments, accessible selected roots, client-state mapping and outboxes | Not allocated; existing author assignments remain separate |
| Exact model-call counts by provider/role/variant/arm, per-call timeout, concurrency, total deadline and retry policy | Not allocated; owner must set numeric limits before any model launches |
| Independent reviewer and acceptance/disposition owner | Not assigned for this pilot |

Missing execution allocation does not block reviewing this specification and plan. It does block presenting them as a runnable or completed evaluation. The initial experiment may select a smaller declared subset, but it must retain a case-coverage matrix and cannot claim the omitted roles, behaviors or provider support.

Use the existing run-manifest and evaluation-report formats once the pilot is allocated. Preserve original raw tool formats and exact-file receipts. Planned outputs are per-case in-session results, handoffs only where the declared mode requires them, transcripts, immutable run manifests, a scoped evaluation report and its external receipt. Native results: NOT_RUN. Statistical reliability, production suitability and complete adaptive-framework proof: NOT_EVALUATED.

Exact source and document identities are recorded in the [external receipt](20260905-contributor-context-specification.receipt.json). No new native skill, runner, registry, hook, or source assignment is installed by this plan.
