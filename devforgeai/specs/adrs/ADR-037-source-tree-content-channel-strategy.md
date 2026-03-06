# ADR-037: Source Tree Update - Content Channel Strategy Reference

**Status:** Accepted
**Date:** 2026-03-06
**Story:** STORY-543
**Epic:** EPIC-075

## Context

STORY-543 (Content & Channel Strategy Outline) requires a new reference file `content-channel-strategy.md` under the `marketing-business/references/` directory. The existing `channel-selection-matrix.md` is a different file containing scoring weights for distribution channels. STORY-543 delivers a content strategy skeleton with topic ideas, posting frequency, and channel selection guidance — a distinct deliverable.

## Decision

Add `content-channel-strategy.md` to the approved source tree under `marketing-business/references/`.

## Change

```
marketing-business/
    references/
        go-to-market-framework.md
        channel-selection-matrix.md
        positioning-strategy.md
        customer-discovery-workflow.md
+       content-channel-strategy.md    # STORY-543, EPIC-075
```

## Rationale

- STORY-543 explicitly specifies this file path in its acceptance criteria and technical specification
- EPIC-075 Feature 5 requires content strategy skeleton generation
- `channel-selection-matrix.md` already exists as a separate scoring weights file — cannot reuse that filename
- Follows the established `references/` progressive disclosure pattern

## Consequences

- source-tree.md must be updated to include the new file
- No other files or directories affected
