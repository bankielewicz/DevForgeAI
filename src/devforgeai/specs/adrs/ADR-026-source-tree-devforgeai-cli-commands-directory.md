# ADR-026: Add devforgeai_cli/commands/ Directory to Source Tree

**Date:** 2026-02-28
**Status:** Accepted
**Acceptance Date:** 2026-02-28
**Deciders:** Solo Developer, DevForgeAI Framework
**Tags:** source-tree, cli, spec-drift, commands

## Context

The `devforgeai-validate` CLI tool has a `commands/` subdirectory at `.claude/scripts/devforgeai_cli/commands/` containing 4 command modules (`phase_commands.py`, `check_hooks.py`, `invoke_hooks.py`, `validate_installation.py`) plus an `__init__.py`. This directory exists on disk and is actively used by the CLI but was never documented in `source-tree.md`.

A `/validate-stories` custody chain audit (STORY-517 through STORY-521) identified this as a MEDIUM spec drift finding: stories referencing `.claude/scripts/devforgeai_cli/commands/phase_commands.py` cannot be fully validated against source-tree.md because the `commands/` subdirectory is absent from the canonical tree.

Context files are immutable without an ADR (Rule 4 in critical-rules.md), so this ADR authorizes the update.

## Decision

Add the `commands/` subdirectory and its 4 modules to `source-tree.md` under the existing `.claude/scripts/devforgeai_cli/` entry, alongside the already-documented `validators/` subdirectory.

## Rationale

1. **Spec-truth alignment:** The canonical source tree must reflect actual project structure. The `commands/` directory has existed since EPIC-015 but was omitted from the tree definition.
2. **Story validation:** STORY-517 (RCA-045 REC-1) targets `phase_commands.py` — without this ADR, context validation flags a MEDIUM finding for every story referencing this path.
3. **Pattern consistency:** The sibling `validators/` directory is already fully enumerated in source-tree.md. The `commands/` directory should follow the same pattern.

## Consequences

### Positive
- Source-tree.md accurately reflects the CLI module structure
- Story validation passes without MEDIUM findings for `commands/` paths
- Future stories targeting CLI commands have validated file paths

### Negative
- Source-tree.md grows by ~5 lines (negligible)

### Risks
- None identified — this documents existing reality, no behavioral change

## Alternatives Considered

1. **Leave undocumented** — Rejected. Creates persistent MEDIUM findings in every audit touching CLI commands. Contradicts spec-driven development principle.
2. **Flatten commands into devforgeai_cli/ root** — Rejected. The `commands/` subdirectory provides clean separation between CLI command definitions and validators. Restructuring would break existing imports.

## Enforcement

### Context File Updates Required

| File | Change | Type |
|------|--------|------|
| `devforgeai/specs/context/source-tree.md` | Add `commands/` subdirectory under `devforgeai_cli/` | Structure update |
| `devforgeai/specs/context/source-tree.md` | Bump version 4.2 → 4.3, update date | Metadata update |

### Affected Skills

| Skill | Change |
|-------|--------|
| devforgeai-story-creation | Context validation now recognizes `commands/` paths |
| implementing-stories | Pre-flight validation includes `commands/` paths |

### New Artifacts

| Artifact | Location |
|----------|----------|
| This ADR | `devforgeai/specs/adrs/ADR-026-source-tree-devforgeai-cli-commands-directory.md` |
