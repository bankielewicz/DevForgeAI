# Migration Notes: devforgeai-development -> implementing-stories

**Migration Date:** 2026-02-16
**ADR:** ADR-017-skill-gerund-naming-no-prefix.md
**Plan:** .claude/plans/idempotent-hatching-treasure.md

---

## What Changed

| Aspect | Before | After |
|--------|--------|-------|
| Skill name | `devforgeai-development` | `implementing-stories` |
| SKILL.md size | 1,099 lines | 329 lines (70% reduction) |
| Reference depth | 3 levels (SKILL -> phase -> _index.md -> sub-file) | 2 levels (SKILL -> phase -> sub-file) |
| Top 5 reference files | 5,897 lines combined | 2,151 lines (63.5% reduction) |
| Naming convention | `devforgeai-[phase]` prefix | `[gerund-phrase]` (Anthropic-compliant) |

## Files Created

- `.claude/skills/implementing-stories/` (82 files) - New skill directory
- `.claude/skills/devforgeai-development.backup/` - Immutable backup of original
- `.claude/commands/dev.backup.md` - Backup of original /dev command
- `devforgeai/specs/adrs/ADR-017-skill-gerund-naming-no-prefix.md` - Naming convention ADR
- 3 extracted reference files:
  - `references/workflow-deviation-protocol.md`
  - `references/pre-phase-planning.md`
  - `references/phase-transition-validation.md`

## Cross-References Updated

All occurrences of `devforgeai-development` replaced with `implementing-stories` in:
- 27 agent files (`.claude/agents/`)
- 16 memory/Constitution files (`.claude/memory/`)
- 8 command files (`.claude/commands/`)
- 58 other skill files (qa, rca, orchestration, story-creation, etc.)
- 17 implementing-stories internal references
- 14 script/test files
- 2 context files (`source-tree.md`, `coding-standards.md`)
- 3 system files (settings.local.json, system-prompt-core.md, README.md)

**Exempt from replacement (backups):**
- `.claude/skills/devforgeai-development.backup/` (immutable)
- `.claude/skills/devforgeai-development/` (old operational src copy)
- `.claude/commands/dev.backup.md`
- All `.backup`, `.original-*`, `.rec3-backup` files

## Operational Sync Required (Manual)

After verifying src/ changes:

1. Copy `.claude/skills/implementing-stories/` -> `.claude/skills/implementing-stories/`
2. Update `.claude/commands/dev.md` from `.claude/commands/dev.md`
3. Sync `.claude/agents/` from `.claude/agents/`
4. Sync `.claude/memory/` from `.claude/memory/`
5. Sync `.claude/rules/` from `.claude/rules/`
6. Sync `.claude/settings.local.json` from `.claude/settings.local.json`
7. Delete `.claude/skills/devforgeai-development/` (operational copy replaced)
8. Update project root `CLAUDE.md` references

## Verification Commands

```bash
# Verify 0 active matches (backup dirs exempt)
grep -rl "devforgeai-development" .claude/ --include="*.md" | grep -v ".backup" | grep -v "devforgeai-development/"

# Verify new skill invocation
grep "implementing-stories" .claude/commands/dev.md

# Verify SKILL.md size
wc -l .claude/skills/implementing-stories/SKILL.md
# Expected: 329 lines

# Verify context files clean
grep "devforgeai-development" devforgeai/specs/context/*.md
# Expected: no output
```

## Rollback Plan

If issues arise:
1. Backup directory is at `.claude/skills/devforgeai-development.backup/`
2. Command backup at `.claude/commands/dev.backup.md`
3. Git revert to pre-migration commit

## Post-MVP: Remaining Skill Renames

ADR-017 establishes the naming table for all 14 skills. Only `devforgeai-development` was migrated in this MVP. Remaining renames follow the same pattern (mechanical rename + cross-reference update).
