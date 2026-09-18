# Architect Reviewer - Structured Output Mode (Phase 07)

## Structured Output Mode (for epic-creation Phase 07)

When this subagent is invoked by **Phase 07** of the `spec-driven-solution-architecture` skill (i.e., during `/create-solution-architecture` feature-decomposition technical assessment), the response MUST include both:

1. The standard prose-narrative report (sections above), AND
2. A **structured JSON block** with per-feature feasibility data, formatted as below.

Other invocations (general architecture review, ADR validation, etc.) continue using prose-only output. The structured block is additive -- it does NOT replace the narrative report; it supplements it for downstream programmatic consumption.

### Required JSON Shape

```json
{
  "verdict": "PROCEED | PROCEED_WITH_CONDITIONS | HALT",
  "feasibility_per_feature": {
    "F-01": {
      "feasibility": "FEASIBLE | NEEDS_ADR | INFEASIBLE",
      "risk": "LOW | MEDIUM | HIGH",
      "notes": "<short technical notes -- one sentence>"
    },
    "F-02": {
      "feasibility": "FEASIBLE | NEEDS_ADR | INFEASIBLE",
      "risk": "LOW | MEDIUM | HIGH",
      "notes": "<short technical notes -- one sentence>"
    }
  },
  "preimplementation_conditions": [
    "<condition 1 -- one sentence>",
    "<condition 2 -- one sentence>"
  ],
  "rejected_alternatives": [
    "<alternative 1 with one-sentence reason for rejection>"
  ]
}
```

### Field Contracts

| Field | Required | Type | Constraints |
|-------|----------|------|-------------|
| `verdict` | Yes | string | One of: `PROCEED`, `PROCEED_WITH_CONDITIONS`, `HALT` |
| `feasibility_per_feature` | Yes | object | One key per feature ID (F-01, F-02, ...) -- must cover every feature in the request |
| `feasibility_per_feature[F-NN].feasibility` | Yes | string | One of: `FEASIBLE`, `NEEDS_ADR`, `INFEASIBLE` |
| `feasibility_per_feature[F-NN].risk` | Yes | string | One of: `LOW`, `MEDIUM`, `HIGH` |
| `feasibility_per_feature[F-NN].notes` | Yes | string | One-sentence technical rationale |
| `preimplementation_conditions` | Conditional | array | Required when `verdict == "PROCEED_WITH_CONDITIONS"`; otherwise `[]` |
| `rejected_alternatives` | Optional | array | Architectural alternatives considered and rejected |

### Coverage Requirement

The `feasibility_per_feature` map MUST include an entry for **every** feature ID present in the orchestrator's Phase 07 input. If a feature is missing, the orchestrator will HALT and re-invoke this subagent for the missing feature(s). Aggregate counts (e.g., "5 feasible, 2 need ADR") are NOT a substitute -- Phase 08 reads the per-feature map directly to populate the Scope-table `Risk` column.

### Provenance

Field values MUST be GROUNDED in the context files cited in the input prompt (`tech-stack.md`, `architecture-constraints.md`, `dependencies.md`, `anti-patterns.md`). DERIVED feasibility/risk classifications require a one-sentence justification in the `notes` field.
