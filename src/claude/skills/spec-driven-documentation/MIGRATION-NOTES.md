# spec-driven-documentation Migration Notes

## 2026-03-18: Absorbed devforgeai-documentation (v1.1.0)

### Source Skill
- **Name:** devforgeai-documentation
- **Location:** `src/claude/skills/devforgeai-documentation/`
- **Size:** 1,167 lines (monolithic SKILL.md)
- **Version:** 1.1.0 (included Phase A: Audit, Phase B: Fix)

### Migration Summary

| Aspect | Before | After |
|--------|--------|-------|
| **Skill name** | devforgeai-documentation | spec-driven-documentation |
| **SKILL.md lines** | 1,167 (monolithic) | ~280 (lean orchestrator) |
| **Phase enforcement** | None (inline phases) | Execute-Verify-Gate at every step |
| **Anti-skip layers** | 0 | 4 independent layers |
| **Phase files** | 0 (all inline) | 21 separate files |
| **Model** | claude-sonnet-4-6 | claude-opus-4-6 |
| **Workflow paths** | 3 (gen/audit/fix) | 3 (unchanged) |
| **Reference files** | 8 | 11 (8 migrated + 3 new) |
| **Template files** | 8 | 8 (unchanged) |

### What Changed

1. **Structural Anti-Skip Enforcement Added:**
   - Every phase is a separate file with Entry Gate, Contract, Mandatory Steps (EVG triplets), Exit Gate
   - CLI gates via `devforgeai-validate phase-check/record/complete`
   - Phase checkpoint persistence in `devforgeai/workflows/`

2. **Monolithic SKILL.md Decomposed:**
   - Phases 0-7 -> Phase 01-02 (shared) + G03-G10 (generation)
   - Phase A (A.0-A.4) -> Phase A03-A07 (audit)
   - Phase B (B.0-B.5) -> Phase F03-F08 (fix)

3. **Three New Reference Files Created:**
   - `references/parameter-extraction.md` (extracted from SKILL.md lines 33-51)
   - `references/audit-workflow.md` (extracted from SKILL.md Phase A.1, lines 917-950)
   - `references/audit-fix-catalog.md` (new, referenced but never existed in original)

4. **Model Upgraded:**
   - From `claude-sonnet-4-6` to `claude-opus-4-6` (consistent with all spec-driven migrations)

### Files Migrated

**Reference files (copied with path updates):**
- `anti-aspirational-guidelines.md`
- `brownfield-analysis.md`
- `diagram-generation-guide.md`
- `document-help.md`
- `documentation-standards.md`
- `greenfield-workflow.md`
- `post-generation-workflow.md`
- `template-customization.md`

**Template files (copied unchanged):**
- `readme-template.md`
- `developer-guide-template.md`
- `api-docs-template.md`
- `troubleshooting-template.md`
- `contributing-template.md`
- `changelog-template.md`
- `architecture-template.md`
- `roadmap-template.md`

### Command Updates

- `/document` command updated to invoke `spec-driven-documentation`
- Old command backed up to `src/claude/commands/backup/document.md`

### Archive

- Original skill archived to `src/claude/skills/backup/_devforgeai-documentation.archive/`
- HALT header added to archived SKILL.md
