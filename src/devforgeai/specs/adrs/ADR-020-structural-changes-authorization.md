# ADR-020: Structural Changes Authorization for EPIC-071 Lean Orchestration Refactoring

**Status:** Accepted
**Date:** 2026-02-20 (Amended: 2026-02-21)
**Story:** STORY-457, STORY-462

---

## Context

EPIC-071 stories require creating new framework artifacts (skills, subagents) and updating
a LOCKED context file (source-tree.md). Per Critical Rule #4, context files are
immutable without ADR authorization. STORY-457 created the initial authorization;
STORY-462 amends it to include the `auditing-w3-compliance` skill.

## Decision

Authorize the following structural changes:

1. **New Skill:** `validating-epic-coverage` at `.claude/skills/validating-epic-coverage/`
   - Extracts shared gap-detection pipeline from two commands
   - Gerund naming per ADR-017
   - Progressive disclosure with `references/` directory

2. **New Subagent:** `epic-coverage-result-interpreter` at `.claude/agents/epic-coverage-result-interpreter.md`
   - Display formatting for coverage reports
   - Read/Grep/Glob tools only (read-only)

3. **source-tree.md Update:** Add entries for new skill and subagent
   - Skill directory entry under `.claude/skills/`
   - Subagent file entry under `.claude/agents/`

4. **Command Refactoring (STORY-457):** Lean orchestration pattern applied to:
   - `.claude/commands/validate-epic-coverage.md` (463 → ~110 lines)
   - `.claude/commands/create-missing-stories.md` (483 → ~100 lines)

5. **New Skill (STORY-462):** `auditing-w3-compliance` at `.claude/skills/auditing-w3-compliance/`
   - Encapsulates W3 violation scanning logic (4 severity categories with Grep patterns)
   - Gerund naming per ADR-017
   - Extracted from `audit-w3.md` command (240 → 110 lines)

6. **Command Refactoring (STORY-462):** Lean orchestration pattern applied to:
   - `.claude/commands/audit-w3.md` (240 → 110 lines)
   - `.claude/commands/orchestrate.md` (535 → 295 lines)
   - `.claude/commands/create-stories-from-rca.md` (263 → 148 lines)
   - `.claude/commands/dev.backup.md` (DELETED — confirmed duplicate)

7. **source-tree.md Update (STORY-462):** Add entry for `auditing-w3-compliance` skill

## Rationale

- Eliminates 800+ lines of duplicated pipeline logic across two commands
- Reduces token consumption by 40-60% per command invocation
- Follows lean orchestration pattern (commands validate + invoke, skills implement)
- Single Responsibility: each component has one job

## Consequences

- New skill must be maintained alongside existing commands
- Dual-path sync required (src/ and .claude/ trees)
- CLAUDE.md Subagent Registry must be updated with new subagent

## References

- EPIC-071: Hybrid Command Lean Orchestration Refactoring
- ADR-017: Skill Gerund Naming Convention
- Lean Orchestration Protocol: `devforgeai/protocols/lean-orchestration-pattern.md`
