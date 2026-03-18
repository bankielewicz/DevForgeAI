# spec-driven-stories Migration Notes

## 2026-03-18: Absorbed devforgeai-story-creation (ADR-041)

**What changed:**
- 22 reference files migrated from `devforgeai-story-creation/references/` to `spec-driven-stories/references/`
- 2 new reference files created: `parameter-extraction.md`, `checkpoint-schema.md`
- 8 phase files created in `phases/` (Execute-Verify-Record pattern per phase)
- 2 subagent contracts migrated to `contracts/`
- Story template (v2.8) migrated to `assets/templates/`
- Scripts directory migrated (migration, validation, tests)
- All internal paths updated to relative format (e.g., `references/X.md`)
- Added 4-layer anti-skip enforcement with Execute-Verify-Record pattern
- Added checkpoint-based state persistence for session resumability
- Inter-phase gates (2-3, 5-6, 7-8) absorbed into Exit Verification Checklists
- `/create-story` command rewired to invoke `spec-driven-stories`
- `/create-stories-from-rca` command updated to invoke `spec-driven-stories`
- Cross-references across src/ tree updated
- `devforgeai-story-creation` archived as `_devforgeai-story-creation.archive/`

**Why:**
- Add structural anti-skip enforcement (Execute-Verify-Gate pattern) to prevent token optimization bias
- Checkpoint JSON enables session resumption after context window clears
- Self-sufficient skill with zero cross-references to old skill
- 7th and final SDLC skill migration complete (all 7 families now use spec-driven-* pattern)
- Per-phase reference loading prevents "already covered" rationalization

**Pattern:** Identical to ADR-039 (implementing-stories -> spec-driven-dev) and ADR-040 (devforgeai-feedback -> spec-driven-feedback)

**ADR:** `devforgeai/specs/adrs/ADR-041-devforgeai-story-creation-to-spec-driven-stories-migration.md`
