# ADR-038: Discovering-Requirements to Spec-Driven-Ideation Migration

## Status

**Accepted** (2026-03-18)

## Context

The `discovering-requirements` skill was deprecated and marked "HALT - do not use" after the introduction of `spec-driven-ideation`, which provides structural anti-skip enforcement (Execute-Verify-Gate pattern). However, `discovering-requirements` was retained as a **reference host** — `spec-driven-ideation` loaded all its workflow references, templates, error handling guides, and scripts from `discovering-requirements/references/`, `discovering-requirements/assets/`, and `discovering-requirements/scripts/` via Read() calls.

This created a dependency where:
- A deprecated skill could not be deleted because an active skill depended on its files
- Two skill directories had to be maintained despite one being deprecated
- The shared-reference pattern created confusion about which skill was authoritative

## Decision

1. **Migrate all reference files** (28 references, 4 assets, 3 scripts) from `discovering-requirements/` into `spec-driven-ideation/` to make it fully self-contained.
2. **Update all Read() paths** in spec-driven-ideation phase files to point to the new locations.
3. **Update all external references** across memory files, agent files, orchestration references, validators, and documentation.
4. **Archive** the `discovering-requirements/` directory as `_discovering-requirements.archived/`.
5. **Update Constitution files** (source-tree.md, architecture-constraints.md, anti-patterns.md) to reference `spec-driven-ideation` instead of `discovering-requirements`.

## Constitution File Changes

This ADR authorizes the following changes to immutable context files:

### source-tree.md
- Replace `discovering-requirements/` directory references with `spec-driven-ideation/` (lines 28, 929, 1002)
- Add `references/`, `assets/templates/`, `scripts/` subdirectories under spec-driven-ideation

### architecture-constraints.md
- Update Single Responsibility Principle entry:
  - FROM: "discovering-requirements: Requirements discovery and elicitation only (ADR-017 naming)"
  - TO: "spec-driven-ideation: Requirements discovery and elicitation only (ADR-017 naming, ADR-038 migration)"

### anti-patterns.md
- Update directory structure example to show `spec-driven-ideation/` instead of `discovering-requirements/`

## Consequences

### Positive
- `spec-driven-ideation` is now fully self-contained with no external skill dependencies
- `discovering-requirements` can be safely deleted after verification
- Eliminates the confusing shared-reference pattern for this skill pair
- Single source of truth for ideation workflow references

### Negative
- Reference files are now duplicated in the archived directory (temporary, until archive is deleted)
- Any future updates to reference files only need to be made in `spec-driven-ideation/`

### Neutral
- The `spec-driven-brainstorming` skill uses a similar shared-reference pattern with `brainstorming/` but is not affected by this migration

## References

- ADR-017: Skill Gerund Naming Convention
- ADR-019: Skill Responsibility Restructure
- ADR-021: Configuration Layer Alignment Protocol (mutability rules for context files)
