# Batch authoring and dependency ownership

## Select outcomes and decompose

Consume the explicitly selected epic/features, requirements, coverage-gap records or outcome set, together with canonical shared contracts and project policy. Verify a reported coverage gap against those sources and existing stories; a missing filename alone does not prove an uncovered outcome.

Inventory every selected normative clause and acceptance scenario with a stable source locator. Group clauses by independently observable outcome. Coalesce changes that must ship together to preserve an interface, invariant or state transition. Split only when each result is independently assessable and the split provides a concrete dependency, delivery or verification benefit. Merge groups that merely duplicate the same unfinished behavior and setup.

Do not split by source paragraph, function, file, command flag, platform, agent role or TDD phase alone. There is no universal number of stories or ACs. For example, allowing cancellation before dispatch and denying it afterward usually belongs to one state-transition story, including the race. An independent notification contract may justify a separate outcome; a second platform test does not automatically do so.

For each group record:

| Property | Required content |
| --- | --- |
| Outcome/scope | Observable result plus exclusions |
| Clause ownership | Exact source clauses owned here; referenced shared constraints keep their canonical owner |
| Acceptance mapping | Each selected scenario's story and AC, plus epic-wide integration obligations |
| Dependencies | Producer, artifact/interface/decision/evidence needed, consumer behavior and reason |
| Split/merge rationale | Concrete independence or coupling, including rejected excessive fragmentation |
| Open decisions | Question, affected work and decision owner |

Challenge the grouping for duplicate owners, omitted clauses, artificial stubs and hidden integration work before presenting it as ready. This is the author's adversarial review unless a separate reviewer actually performed it; do not call it independent QA. If the request only asks for a proposal, return the work set and stop at that selected scope.

## Dependencies

Use actual story IDs in `depends_on`. For every edge explain what the consumer needs, where it is defined and what observation will satisfy it. Read the dependency's current contract and relevant evidence; a Done label alone cannot prove that a required interface is qualified. Distinguish a contract decision from implementation or platform evidence.

Detect self-dependencies, missing/ambiguous IDs and cycles across the selected reachable graph, including relevant archived work. A future story may describe a planned producer, but a nonexistent ID cannot be presented as resolved. An external or still-undecided prerequisite remains explicit in Dependencies and Notes, and dependent readiness remains unresolved. Do not select the implementation of a referenced story merely because it supplies context.

Keep epic-wide scenarios and shared requirements visible at their canonical owner. Story creation changes planned coverage only; it does not establish implemented or tested coverage. Archived requirements still need applicable current facts, not automatic acceptance based on location.

## Execute the selected batch

Collect shared metadata once, keeping per-story exceptions. Prepare collision-free IDs and a producer-first order from actual dependencies. Stable source material may be reused while its bytes are unchanged. Reread mutable story, epic, sprint, source-link and evidence records before using them after edits.

Run the same substantive requirements, technical/UI assembly and delivery work for every selected member. Do not omit review because a batch is large. Store a result per selected outcome in the [session record](../assets/templates/session-record.md): delivered path and content identity, unresolved decisions, failure and actual link effects. Record duplicates intentionally retained and omitted/unselected outcomes with reasons.

When one story fails, preserve completed outputs and continue independent selected stories. Block dependent work that requires its missing input; do not cascade an assumed success. If an already complete producer contract is available, dependent authoring may describe that planned interface while making implementation prerequisites explicit. Stop the batch if shared identity, authority or write-scope integrity is uncertain.

At the end, read all written stories back against the selected clause/acceptance map. Report delivered, partial, blocked and omitted members separately, with unresolved epic-wide obligations. A successful subset is not full batch or epic completion. Do not close the epic, start implementation or schedule a sprint automatically.
