# spec-driven-feedback Migration Notes

## 2026-03-18: Absorbed spec-driven-feedback (ADR-040)

**What changed:**
- 13 reference files migrated from `spec-driven-feedback/references/` to `spec-driven-feedback/references/`
- 7 template YAML files migrated from `spec-driven-feedback/templates/` to `spec-driven-feedback/templates/`
- HOOK-SYSTEM.md (979 lines) migrated to `spec-driven-feedback/HOOK-SYSTEM.md`
- All internal paths updated to relative format (e.g., `references/X.md`, `templates/X.yaml`)
- Model changed from `Sonnet` to `opus`
- ~100 cross-references across src/ tree updated
- Constitution source-tree.md updated
- `spec-driven-feedback` archived as `_spec-driven-feedback.archive/`

**Why:**
- Eliminate cross-skill path fragility (~46 Read() paths pointed to spec-driven-feedback)
- Single source of truth for feedback workflow references
- Enable eventual deletion of spec-driven-feedback
- Consistent with ADR-038 and ADR-039 migration pattern

**Pattern:** Identical to ADR-039 (spec-driven-dev → spec-driven-dev migration)

**ADR:** `devforgeai/specs/adrs/ADR-040-spec-driven-feedback-to-spec-driven-feedback-migration.md`
