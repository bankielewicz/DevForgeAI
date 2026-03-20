# Migration Notes: claude-code-terminal-expert -> spec-driven-cc-guide

**Migration Date:** 2026-03-19
**Migrated By:** DevForgeAI AI Agent
**Source Skill:** claude-code-terminal-expert v4.0.0
**Target Skill:** spec-driven-cc-guide v5.0.0

---

## Motivation

The `claude-code-terminal-expert` skill (v4.0.0) used a progressive disclosure pattern with NO execution phases and NO enforcement. Claude's token optimization bias caused it to routinely skip loading reference files, answering from SKILL.md summaries alone. This resulted in incomplete, inaccurate, or outdated answers despite ~18,000 lines of comprehensive reference content being available.

## What Changed

| Aspect | Before (v4.0) | After (v5.0) |
|--------|---------------|--------------|
| **Name** | claude-code-terminal-expert | spec-driven-cc-guide |
| **Phase enforcement** | None (progressive disclosure) | 4 phases with Execute-Verify-Gate |
| **Reference loading** | Optional ("load as needed") | Mandatory (HALT if not loaded) |
| **Anti-skip layers** | 0 | 3 (reference verification, artifact check, step registry) |
| **Model** | (default) | Sonnet (cost-efficient for knowledge retrieval) |
| **Content** | Identical | Identical (all reference files migrated as-is) |
| **Trigger mechanism** | Auto-trigger via description keywords | Auto-trigger via description keywords (same) |

## Files Migrated As-Is (No Content Changes)

### Core References (7 files)
- `references/core-features.md` (2,428 lines)
- `references/configuration-guide.md` (1,513 lines)
- `references/integration-patterns.md` (2,790 lines)
- `references/troubleshooting-guide.md` (2,128 lines)
- `references/advanced-features.md` (3,553 lines)
- `references/best-practices.md` (1,230 lines)
- `references/documentation-urls.md` (73 lines)

### Prompt Engineering (14 files)
- `references/prompt-engineering/*.md`

### Skills Specification (6 files)
- `references/skills/*.md`

### Assets (2 files)
- `assets/quick-reference.md` (797 lines)
- `assets/comparison-matrix.md` (651 lines)

## New Files Created

- `SKILL.md` — Rewritten with EVG enforcement pattern
- `phases/phase-01-question-classification.md`
- `phases/phase-02-reference-loading.md`
- `phases/phase-03-answer-synthesis.md`
- `phases/phase-04-self-update-check.md`
- `references/domain-routing-table.md`
- `MIGRATION-NOTES.md` (this file)

## Files NOT Migrated (Archived with Old Skill)

- `README.md` — Skill-specific documentation
- `INTEGRATION_GUIDE.md` — Superseded by EVG pattern
- `SKILL-TESTING-REPORT.md` — Historical testing data
- `SKILL-VERIFICATION.md` — Historical verification data

## Archive Location

Old skill archived at: `src/claude/skills/backup/_claude-code-terminal-expert.archive/`
