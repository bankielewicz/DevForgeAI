# Migration Notes: devforgeai-release -> spec-driven-release

**Migration Date:** 2026-03-18
**Source Skill:** `.claude/skills/devforgeai-release/` (754 lines, 13 phases)
**Target Skill:** `.claude/skills/spec-driven-release/` (8 phases, Execute-Verify-Gate)
**Precedent:** ADR-039 (implementing-stories -> spec-driven-dev migration)

---

## Why This Migration

The `devforgeai-release` skill suffered from **token optimization bias** - Claude would skip phases/steps during execution because the skill lacked structural anti-skip enforcement. This created rework for the user and undermined framework integrity.

The spec-driven-* pattern (Execute-Verify-Gate) prevents this through 4 independent anti-skip layers that ALL must fail before any step can be skipped.

---

## Phase Consolidation (13 -> 8)

| New Phase | Name | Old Phases Absorbed |
|-----------|------|---------------------|
| 01 | Setup & Classification | 0.1 + 0.3 + Phase 1 pre-flight |
| 02 | Build & Package | 0.2 + 0.5 |
| 03 | Pre-Release Validation | 1 |
| 04 | Staging Deployment | 2 + 2.5 (hooks as step) |
| 05 | Production Deployment | 3 + 3.5 (hooks as step) |
| 06 | Post-Deployment Validation | 4 |
| 07 | Release Documentation | 5 |
| 08 | Monitoring, Cleanup & Closure | 6 + 7 |

---

## Self-Sufficiency

This skill is **fully self-sufficient**. All references, templates, and scripts have been migrated locally:

- 22 reference files in `references/`
- 8 script files in `scripts/`
- 3 template files in `assets/templates/`

**Zero cross-references** to `.claude/skills/devforgeai-release/`.

---

## Key Structural Changes

1. **Execute-Verify-Record triplets** - Every step has mandatory EXECUTE, VERIFY, RECORD parts
2. **Binary CLI gates** - `devforgeai-validate phase-check/phase-complete/phase-record --workflow=release`
3. **Phase files** - Separated into `phases/phase-XX-*.md` (one file per phase)
4. **Checkpoint persistence** - JSON state file at `devforgeai/workflows/${STORY_ID}-release-phase-state.json`
5. **Self-check boxes** - 8 violation detection checks in Execution Model section
6. **Token optimization bias prohibition** - Explicit prohibition statement with RCA references

---

## Archive Plan

After validation:
1. Rename `devforgeai-release/` to `_devforgeai-release.archive/`
2. Add HALT directive to archived SKILL.md
3. Update skill inventory to reflect archived status
