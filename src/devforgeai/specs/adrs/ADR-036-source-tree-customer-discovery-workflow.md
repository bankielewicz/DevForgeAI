# ADR-036: Source Tree Update - Customer Discovery Workflow Reference

**Status:** Accepted
**Date:** 2026-03-06
**Story:** STORY-542
**Epic:** EPIC-075

## Context

STORY-542 (Customer Discovery Workflow) requires a new reference file `customer-discovery-workflow.md` under the `marketing-business/references/` directory. The current source-tree.md only lists 3 reference files for this skill: `go-to-market-framework.md`, `channel-selection-matrix.md`, and `positioning-strategy.md`.

## Decision

Add `customer-discovery-workflow.md` to the approved source tree under `marketing-business/references/`.

## Change

```
marketing-business/
    references/
        go-to-market-framework.md
        channel-selection-matrix.md
        positioning-strategy.md
+       customer-discovery-workflow.md    # STORY-542, EPIC-075
```

## Rationale

- STORY-542 explicitly specifies this file path in its technical specification (component `customer-discovery-workflow.md`, file_path `src/claude/skills/marketing-business/references/customer-discovery-workflow.md`)
- EPIC-075 Feature 4 requires customer discovery capabilities within the marketing skill
- Follows the established `references/` progressive disclosure pattern

## Consequences

- source-tree.md must be updated to include the new file
- No other files or directories affected
