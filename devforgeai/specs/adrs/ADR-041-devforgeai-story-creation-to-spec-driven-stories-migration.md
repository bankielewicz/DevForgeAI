# ADR-041: DevForgeAI-Story-Creation to Spec-Driven-Stories Migration

## Status

**Accepted** (2026-03-18)

## Context

The `devforgeai-story-creation` skill is the 8-phase story creation workflow that generates user stories with acceptance criteria, technical specifications, and UI specifications. While functionally complete, it lacks the structural anti-skip enforcement (Execute-Verify-Gate pattern) that the other 6 spec-driven-* skills use to prevent token optimization bias.

This causes:
- Claude skipping phases/steps to save tokens, creating double work
- No checkpoint persistence for session resumption
- No per-phase reference loading (references loaded ad-hoc, easily skipped)
- No binary gate enforcement at phase boundaries
- Inconsistent execution quality depending on context window pressure

All 6 other SDLC skill families have been successfully migrated:
- ADR-038: discovering-requirements -> spec-driven-ideation
- ADR-039: designing-systems -> spec-driven-architecture
- ADR-039: implementing-stories -> spec-driven-dev
- ADR-040: devforgeai-feedback -> spec-driven-feedback
- brainstorming -> spec-driven-brainstorming
- devforgeai-qa -> spec-driven-qa

## Decision

1. **Create `spec-driven-stories`** as a new skill with full anti-skip enforcement:
   - 4-layer enforcement: per-phase reference loading, binary CLI gates, checkpoint state tracking, artifact verification
   - Execute-Verify-Record pattern on every mandatory step
   - 8 separate phase files (one per workflow phase)
   - Checkpoint JSON for session resumption
   - Token Optimization Bias prohibition statement

2. **Migrate all files** from `devforgeai-story-creation/` into `spec-driven-stories/` to make it fully self-contained:
   - 22 reference files + 2 new (parameter-extraction, checkpoint-schema)
   - 2 subagent contracts (requirements-analyst, api-designer)
   - 1 story template (v2.8)
   - Scripts directory (migration, validation, tests)

3. **Rewire slash commands:**
   - `/create-story` -> invoke `spec-driven-stories`
   - `/create-stories-from-rca` -> invoke `spec-driven-stories`
   - Backup old command to `backup/create-story.md`

4. **Update all external references** across commands, memory files, agent files, rules, and other skills.

5. **Archive** `devforgeai-story-creation/` as `_devforgeai-story-creation.archive/`.

6. **Absorb inter-phase gates** (2-3, 5-6, 7-8) into Exit Verification Checklists of their preceding phase files rather than keeping them as standalone sections.

## Constitution File Changes

This ADR authorizes the following changes to immutable context files:

### source-tree.md
- Replace `devforgeai-story-creation/` directory references with `spec-driven-stories/`
- Add `phases/`, `references/`, `contracts/`, `assets/templates/` subdirectories under spec-driven-stories

## Consequences

### Positive
- `spec-driven-stories` has full anti-skip enforcement preventing token optimization bias
- Checkpoint JSON enables session resumption after context window clears
- Self-contained skill with zero cross-references to old skill
- 7th and final SDLC skill migration complete (all 7 families now use spec-driven-* pattern)
- Per-phase reference loading prevents "already covered" rationalization

### Negative
- Reference files temporarily duplicated in archive directory (until archive is deleted)
- Larger SKILL.md due to anti-skip enforcement boilerplate (~200 additional lines)

### Neutral
- Follows identical pattern to ADR-038, ADR-039, and ADR-040

## References

- ADR-038: Discovering-Requirements to Spec-Driven-Ideation Migration
- ADR-039: Implementing-Stories to Spec-Driven-Dev Migration
- ADR-039: Designing-Systems Consolidation into Spec-Driven-Architecture
- ADR-040: DevForgeAI-Feedback to Spec-Driven-Feedback Migration
- ADR-021: Configuration Layer Alignment Protocol (mutability rules for context files)
