# ADR-039: Implementing-Stories to Spec-Driven-Dev Migration

## Status

**Accepted** (2026-03-18)

## Context

The `implementing-stories` skill was the original TDD implementation workflow. After the introduction of `spec-driven-dev`, which provides structural anti-skip enforcement (Execute-Verify-Gate pattern), the `/dev` command was updated to invoke `spec-driven-dev`. However, `implementing-stories` was retained as a **reference host** — `spec-driven-dev` loaded all 65 reference files, 18 preflight references, and 2 asset templates from `implementing-stories/references/` and `implementing-stories/assets/` via Read() calls. The `/resume-dev` command also still invoked `implementing-stories` directly.

This created a dependency where:
- A legacy skill could not be deleted because the active skill depended on its files
- Two skill directories had to be maintained despite one being deprecated for primary invocation
- The shared-reference pattern created confusion about which skill was authoritative
- 157 files across the src/ tree still referenced `implementing-stories` despite `/dev` invoking `spec-driven-dev`

## Decision

1. **Migrate all reference files** (47 core references, 18 preflight references, 2 asset templates) from `implementing-stories/` into `spec-driven-dev/` to make it fully self-contained.
2. **Update all Read() paths** in spec-driven-dev SKILL.md and phase files to use relative paths (e.g., `references/X.md`).
3. **Update all external references** across commands, memory files, agent files, orchestration references, other skills, rules, scripts, and documentation — replacing `implementing-stories` with `spec-driven-dev`.
4. **Update `/resume-dev` command** to invoke `spec-driven-dev` instead of `implementing-stories`.
5. **Archive** the `implementing-stories/` directory as `_implementing-stories.archive/`.
6. **Update Constitution files** (source-tree.md, anti-patterns.md, coding-standards.md, architecture-constraints.md, tech-stack.md) to reference `spec-driven-dev` instead of `implementing-stories`.
7. **Enhance spec-driven-dev SKILL.md** with unique sections from implementing-stories (Task-Gate Integration, Treelint integration, expanded session state).
8. **Change model** from `Sonnet` to `claude-opus-4-6` for capability parity.

## Constitution File Changes

This ADR authorizes the following changes to immutable context files:

### source-tree.md (9 references)
- Replace `implementing-stories/` directory references with `spec-driven-dev/` in directory listings
- Update naming examples to use `spec-driven-dev` instead of `implementing-stories`
- Add `references/`, `references/preflight/`, `assets/templates/` subdirectories under spec-driven-dev

### anti-patterns.md (6 references)
- Update directory structure examples to show `spec-driven-dev/` instead of `implementing-stories/`
- Update skill interaction descriptions (e.g., "spec-driven-dev calls validating-quality")

### coding-standards.md (3 references)
- Update gerund naming examples from `implementing-stories` to `spec-driven-dev`
- Update path references

### architecture-constraints.md (1 reference)
- Update Single Responsibility Principle entry:
  - FROM: "implementing-stories: TDD implementation only (ADR-017 naming)"
  - TO: "spec-driven-dev: TDD implementation only (ADR-017 naming, ADR-039 migration)"

### tech-stack.md (1 reference)
- Update phase file path reference from `implementing-stories/phases/` to `spec-driven-dev/phases/`

## Consequences

### Positive
- `spec-driven-dev` is now fully self-contained with no external skill dependencies
- `implementing-stories` can be safely deleted after verification
- Eliminates the confusing shared-reference pattern
- Single source of truth for TDD workflow references
- `/resume-dev` now uses the same skill as `/dev` (consistency)
- Model upgrade to claude-opus-4-6 provides capability parity

### Negative
- Reference files are temporarily duplicated in the archived directory (until archive is deleted)
- Large migration scope (~200 files) requires careful verification

### Neutral
- The spec-driven-dev phase files (EVG pattern) remain unchanged — only reference paths are updated
- Other spec-driven-* skills (spec-driven-feedback, etc.) follow the same migration pattern per ADR-038

## References

- ADR-017: Skill Gerund Naming Convention
- ADR-019: Skill Responsibility Restructure
- ADR-021: Configuration Layer Alignment Protocol (mutability rules for context files)
- ADR-038: Discovering-Requirements to Spec-Driven-Ideation Migration (identical pattern)
