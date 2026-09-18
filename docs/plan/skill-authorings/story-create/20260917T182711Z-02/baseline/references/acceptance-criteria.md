# Requirements and acceptance criteria

## Preserve the source contract

Describe the actor, capability and value in a single user-story statement, followed by explicit in-scope and out-of-scope behavior. A technical infrastructure actor is valid when that is the real consumer. Do not invent a customer persona for internal work.

Build a clause-to-AC map from original selected sources. Cite project-relative document paths, headings and stable IDs; add verified line locators or a short exact excerpt when needed to disambiguate a claim. For a direct request, record the actual request/decision in Provenance or Notes rather than inventing a brainstorm document. Sources can include decisions, user research, current code and external documentation actually inspected. Do not manufacture quotes, quantified impact or citations to missing files. Mark an unsupported essential claim as an open decision.

Keep business intent, technical mechanism and verification observation distinguishable. A source reference does not silently select unrelated deliverables. Store shared rules at their canonical owner and reference them at clause level. If selected sources disagree, identify the concrete conflict and affected ACs before claiming the story is ready.

## AC form

Use stable unique IDs `AC1`, `AC2`, and so on, with headings `### AC#1: Descriptive outcome`. AC headings are definitions, not completion checkboxes. Each XML block has a nonempty `given`, `when` and `then`:

```xml
<acceptance_criteria id="AC1" implements="SVC-001">
  <given>An order has not been dispatched and the caller owns it</given>
  <when>The caller requests cancellation</when>
  <then>The order becomes cancelled exactly once and cannot subsequently dispatch</then>
</acceptance_criteria>
```

This is a fictional pattern, not a requirement to add orders to a project. Replace examples with the actual selected contract. Escape XML metacharacters and quoted attributes; code literals can use valid CDATA where appropriate. Keep each block well formed. `implements` names defined technical requirement/component IDs, never nonexistent design elements. For documentation-only outcomes without executable components, omit it with a concrete non-applicability explanation in the traceability table.

Optional `verification` may include project-relative `source_files`, `test_file` and a project-specified `coverage_threshold`. These are planned verification hints, not claims that files/tests exist or measurements have passed. Mark new paths as planned in surrounding prose. An optional `implementation` element can contain `approach`, `pseudocode` and `rationale` when that helps implement an AC; do not constrain a mechanism that the governing specification intentionally leaves open.

Cover the successful result and applicable boundaries, invalid inputs, forbidden actors/states, concurrency, idempotency, partial failure and recovery. Use as many ACs as the selected behavior requires. “Works correctly,” “fast” or “secure” is not an observable expected result. If a required performance/reliability target is unknown, ask for the decision; do not invent a numeric threshold. A denial criterion includes allowed unchanged state and side effects, not just an error message.

## Refactors and defect work

For a refactor, identify preserved interfaces, output, user-visible content, ordering, configuration behavior and permission boundaries. Include preservation ACs and applicable golden-output/regression comparisons against a named baseline. If help text, summaries, errors or prompt order matter, name their actual preservation properties; a keyword match alone is insufficient. Do not copy a historical validator's magic wording to make a rule appear satisfied.

For a bug fix, retain the demonstrated trigger, observed wrong behavior and requirement-derived expected result; unresolved diagnoses stay hypotheses. Define a regression obligation that distinguishes old and repaired behavior. Implementation still follows current project TDD and QA policy. This skill authors the obligation; it does not claim to have reproduced or repaired the defect unless separately supplied evidence actually demonstrates that fact.

## Edge cases, NFRs and DoD

Document applicable data validation (type/range/format/nullability), error responses and affected state. Separate observed constraints from proposals. Use [domain patterns](domain-patterns.md) to spot relevant omissions without importing its illustrative product choices.

Map every selected AC and NFR to a planned test/review observation in Test Strategy and the unchecked AC Verification Checklist. State required platforms and how denominators/thresholds will be measured when the project specifies them. Keep missing platform/tool capability explicit. DoD items describe concrete implementation, quality, testing and documentation outcomes and remain unchecked in a newly authored story.

Provenance, measurable requirements and an author content review are useful inputs to development/QA; they are not independent assessment or framework acceptance.
