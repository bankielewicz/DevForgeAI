---
artifact: idea-backlog
schema_version: "1.0"
project: "{project-name}"
created: "{ISO-8601-date}"
updated: "{ISO-8601-date}"
source_sessions:
  - "{IDEATION-NNN}"
# ---------------------------------------------------------------------------
# Idea backlog -- ideas raised but intentionally NOT in the current MVP,
# retained for later evaluation. Items use the DEF-NNN shape from
# spec-driven-brainstorming Phase 09 (the Deferred Ideas Register, ADR-065).
# This block is the machine-readable source of truth; the Markdown body below
# is the human-readable rendering of the same data.
# ---------------------------------------------------------------------------
idea_backlog:
  - id: "DEF-001"
    description: "{the idea}"
    why_deferred: "{why it is not in the current MVP}"
    business_value: "{value if built -- optional}"
    mvp_dependency: "{how it depends on or extends the MVP -- optional}"
    revisit_when: "{trigger condition for re-evaluating this idea}"
    source: "{brainstorm:BRAINSTORM-NNN:phase-NN | ideation:IDEATION-NNN:phase-NN}"
    status: "open"   # open | promoted | rejected
---

# Idea Backlog — {project-name}

> **Living artifact.** This file accumulates ideas raised during business analysis and
> ideation but intentionally **not** in the current MVP — so they survive for later
> evaluation instead of being lost. Every `/ideate` session for this project **appends**
> to it (dedupe on `id` first, then normalized `description`); it is **never
> overwritten**. Each idea carries a stable `DEF-NNN` id.

## Field Reference

| Field | Meaning |
|-------|---------|
| `id` | Stable `DEF-NNN` identifier (never reused, never renumbered) |
| `description` | The idea itself |
| `why_deferred` | Why it is not in the current MVP |
| `business_value` | Value if built (optional) |
| `mvp_dependency` | How it depends on / extends the MVP (optional) |
| `revisit_when` | Trigger condition that should re-surface this idea |
| `source` | Origin — a brainstorm phase or an ideation session |
| `status` | `open` (awaiting evaluation), `promoted` (entered an MVP/release), `rejected` (decided against — kept for the audit trail) |

## Open Ideas

_Ideas awaiting evaluation. Status `open`._

| ID | Description | Why Deferred | Revisit When | Source |
|----|-------------|--------------|--------------|--------|
| DEF-001 | {description} | {why_deferred} | {revisit_when} | {source} |

## Promoted Ideas

_Ideas that have since entered an MVP or release scope. Status `promoted`._

| ID | Description | Promoted In | Source |
|----|-------------|-------------|--------|

## Rejected Ideas

_Ideas explicitly decided against. Status `rejected`. Retained for the audit trail._

| ID | Description | Reason | Source |
|----|-------------|--------|--------|

---

**Schema:** idea-backlog 1.0 · **Produced by** spec-driven-ideation (Project Management phase) · **Consumed by** future `/ideate` re-sessions and `spec-driven-system-architecture`, `spec-driven-solution-architecture`, `spec-driven-development-architecture`
