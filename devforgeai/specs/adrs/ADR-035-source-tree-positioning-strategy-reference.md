# ADR-035: Source Tree Update - positioning-strategy.md Reference

**Status:** Accepted
**Date:** 2026-03-05
**Story:** STORY-540
**Epic:** EPIC-075

## Context

STORY-540 implements a Positioning & Messaging Framework as a reference file for the marketing-business skill. The file `positioning-strategy.md` needs to be added to `src/claude/skills/marketing-business/references/` but is not yet listed in source-tree.md.

## Decision

Add `positioning-strategy.md` to the marketing-business skill references in source-tree.md.

## Changes

**File:** `devforgeai/specs/context/source-tree.md`

Add under `marketing-business/references/`:
```
│   │   │       ├── positioning-strategy.md
```

## Consequences

- marketing-business skill gains positioning workflow documentation
- Downstream STORY-541 can reference this file for skill assembly
- No breaking changes to existing files
