# ADR-039: Consolidate designing-systems into spec-driven-architecture

**Date:** 2026-03-18
**Status:** Accepted
**Deciders:** Bryan (Project Owner), DevForgeAI AI Agent
**Tags:** architecture, skill-consolidation, migration

## Context

The `designing-systems` skill was deprecated and marked "HALT - do not use" with a directive to use `spec-driven-architecture` instead. However, `designing-systems` was retained as a read-only reference library because `spec-driven-architecture` loads ALL its reference materials (31 reference files, 14 asset files, 6 validation scripts) via explicit `Read()` calls into the `designing-systems/` directory at runtime.

This creates fragile coupling:
- A deprecated skill that cannot be archived or deleted
- Every one of `spec-driven-architecture`'s 11 phase files depends on `designing-systems/` existing
- 88+ files across the `src/` tree reference `designing-systems` by name or path
- The shared-read pattern was documented in `spec-driven-architecture/references/README.md` as intentional, but it prevents the natural lifecycle of deprecation followed by removal

The `spec-driven-architecture` skill replaced `designing-systems` with structural anti-skip enforcement (Execute-Verify-Gate pattern) to prevent token optimization bias. The replacement is complete for skill invocation, but the reference material dependency was never migrated.

## Decision

We will migrate all reference materials from `designing-systems/` INTO `spec-driven-architecture/`, making it fully self-sufficient. Specifically:

1. **Copy** all 47 content files (references, assets, scripts) into `spec-driven-architecture/`
2. **Update** all internal paths (Read() calls in phase files, self-references in copied files)
3. **Update** all 88+ external references across `src/` (commands, orchestration, memory, constitution, 12+ other skills)
4. **Archive** `designing-systems/` as `_designing-systems.archive/`
5. **Retain** `spec-driven-architecture` name (no rename to gerund form)

## Rationale

- **Eliminates fragile coupling:** A deprecated skill should not be a runtime dependency for an active skill
- **Enables cleanup:** After migration, `_designing-systems.archive/` can eventually be deleted
- **Single ownership:** One skill owns its reference materials — no cross-skill file reads
- **No functional change:** The same reference content is used; only the file paths change
- **Name retention:** The `spec-driven-*` naming pattern is established (spec-driven-ideation, spec-driven-qa backups exist). Renaming to gerund form would require updating even more references with no functional benefit.

## Consequences

### Positive

- `spec-driven-architecture` becomes fully self-sufficient with zero external dependencies
- `designing-systems` can be archived and eventually deleted
- Eliminates the confusing state of a "deprecated but required" skill
- Simplifies onboarding — one skill to understand, not two
- Future reference updates only need to happen in one location

### Negative

- One-time cost of updating 88+ files across the codebase
- Temporary duplication during migration (both copies exist until archive step)
- Backup directories (`_spec-driven-architecture.backup/`, `commands/backup/`) will contain stale references (accepted — they are frozen snapshots)

### Risks and Mitigations

| Risk | Mitigation |
|------|-----------|
| Missed reference breaks a skill at runtime | Phase 10 regression scan: Grep for any remaining `designing-systems` references outside archive/backup directories |
| Constitution file drift | This ADR authorizes Constitution file updates; alignment-auditor can verify post-migration |
| Git history loss for moved files | Files are copied (not moved via git mv) — original history preserved in archive |

## Constitution Impact

This ADR authorizes updates to the following Constitution files in `src/claude/memory/Constitution/`:

| File | Nature of Change |
|------|-----------------|
| `source-tree.md` | Update directory listings and skill name references |
| `tech-stack.md` | Update pattern descriptions referencing the skill |
| `dependencies.md` | Update pattern descriptions referencing the skill |
| `architecture-constraints.md` | Update skill description in responsibility list |
| `coding-standards.md` | Replace `designing-systems` gerund naming example with `implementing-stories` |

## Alternatives Considered

1. **Keep shared-read pattern** — Rejected. Perpetuates fragile coupling indefinitely.
2. **Symlink designing-systems to spec-driven-architecture** — Rejected. Symlinks are fragile across WSL/Windows/Linux environments.
3. **Rename spec-driven-architecture to gerund form** — Rejected. The `spec-driven-*` naming pattern is already established; renaming would require even more file updates with no functional benefit.

## Related Decisions

- **ADR-017:** Skill gerund naming convention (no prefix) — `spec-driven-architecture` is an acknowledged exception to gerund naming
- **ADR-019:** Skill responsibility restructure — established the separation between `designing-systems` and `spec-driven-architecture`
- **ADR-038:** `discovering-requirements` to `spec-driven-ideation` migration — similar consolidation pattern

## Change Log

| Date | Change |
|------|--------|
| 2026-03-18 | Initial creation — Accepted |
