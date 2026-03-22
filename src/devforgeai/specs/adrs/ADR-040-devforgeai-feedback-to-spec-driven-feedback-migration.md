# ADR-040: DevForgeAI-Feedback to Spec-Driven-Feedback Migration

## Status

**Accepted** (2026-03-18)

## Context

The `devforgeai-feedback` skill was the original feedback/retrospective system. After the introduction of `spec-driven-feedback`, which provides structural anti-skip enforcement (Execute-Verify-Gate pattern), the feedback commands were updated to invoke `spec-driven-feedback`. However, `devforgeai-feedback` was retained as a **reference host** — `spec-driven-feedback` loaded all 13 reference files, 7 template files, and the HOOK-SYSTEM.md documentation from `devforgeai-feedback/` via Read() calls.

This created a dependency where:
- A deprecated skill could not be deleted because the active skill depended on its files
- Two skill directories had to be maintained despite one being deprecated
- ~46 hardcoded Read() paths in spec-driven-feedback pointed to devforgeai-feedback
- The shared-reference pattern created confusion about which skill was authoritative

## Decision

1. **Migrate all reference files** (13 references, 7 templates, 1 doc) from `devforgeai-feedback/` into `spec-driven-feedback/` to make it fully self-contained.
2. **Update all Read() paths** in spec-driven-feedback SKILL.md and phase files to use relative paths.
3. **Update all external references** across commands, memory files, config files, documentation, CLI scripts, and hooks.
4. **Archive** the `devforgeai-feedback/` directory as `_devforgeai-feedback.archive/`.
5. **Update Constitution files** to reference `spec-driven-feedback` instead of `devforgeai-feedback`.
6. **Upgrade model** from `Sonnet` to `claude-opus-4-6` for capability parity.

## Constitution File Changes

This ADR authorizes the following changes to immutable context files:

### source-tree.md
- Replace `devforgeai-feedback/` directory references with `spec-driven-feedback/`
- Add `references/`, `templates/` subdirectories under spec-driven-feedback

## Consequences

### Positive
- `spec-driven-feedback` is now fully self-contained with no external skill dependencies
- `devforgeai-feedback` can be safely deleted after verification
- Eliminates the confusing shared-reference pattern for this skill pair
- Single source of truth for feedback workflow references

### Negative
- Reference files are temporarily duplicated in the archived directory (until archive is deleted)

### Neutral
- Follows identical pattern to ADR-038 (discovering-requirements → spec-driven-ideation) and ADR-039 (implementing-stories → spec-driven-dev)

## References

- ADR-038: Discovering-Requirements to Spec-Driven-Ideation Migration
- ADR-039: Implementing-Stories to Spec-Driven-Dev Migration
- ADR-021: Configuration Layer Alignment Protocol (mutability rules for context files)
