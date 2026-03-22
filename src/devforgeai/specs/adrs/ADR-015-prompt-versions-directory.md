---
id: ADR-015
title: "Add Prompt Versions Directory to Source Tree"
status: APPROVED
created: 2026-02-12
updated: 2026-02-12
author: DevForgeAI Framework
source_story: STORY-390
source_epic: EPIC-061
---

# ADR-015: Add Prompt Versions Directory to Source Tree

## Status

**APPROVED** - 2026-02-12

## Context

STORY-390 (Implement Prompt Versioning System for Template Migration Safety) requires a structured directory to store version snapshots of prompt templates (agents, skills, commands). The system captures before/after states of prompt files during template migrations, stores SHA-256 verified snapshots, and enables rollback within minutes.

The versioning data is documentation-only (Markdown snapshot files and VERSION-HISTORY.md audit trails), making `devforgeai/specs/` the appropriate parent directory per the existing "NO code in devforgeai/specs/" rule.

## Decision

Add `devforgeai/specs/prompt-versions/` to source-tree.md as a valid directory location for prompt version snapshots.

### Directory Structure

```
devforgeai/specs/prompt-versions/
├── {component_id}/
│   ├── VERSION-HISTORY.md              # Audit trail (Markdown table)
│   ├── {timestamp}-{hash}.snapshot.md  # Version snapshots
│   └── ...
```

### Rules
- Each component gets its own subdirectory (flat structure)
- Snapshot files contain YAML frontmatter + full file content (before/after)
- VERSION-HISTORY.md tracks all versions per component
- Documentation only (no executable code)
- Component IDs must match `^[a-z][a-z0-9-]{1,63}$`

## Consequences

### Positive
- Clear location for version data within existing specs hierarchy
- Consistent with "documentation only" rule for devforgeai/specs/
- Enables EPIC-062 template migration safety with structured audit trail
- Supports up to 100 components x 50 versions (< 500MB total)

### Negative
- Adds storage overhead (~100KB per component per version)
- Directory will grow with each template migration

### Neutral
- No impact on existing directory structure
- No code changes required for existing components

## References

- STORY-390: Implement Prompt Versioning System for Template Migration Safety
- EPIC-061: Unified Template Standardization & Enforcement
- EPIC-062: Pilot Evaluation & Rollout (consumer of versioning system)
