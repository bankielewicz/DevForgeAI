# spec-driven-feedback Migration Notes

## 2026-03-18: Absorbed devforgeai-feedback (ADR-040)

**What changed:**
- 13 reference files migrated from `devforgeai-feedback/references/` to `spec-driven-feedback/references/`
- 7 template YAML files migrated from `devforgeai-feedback/templates/` to `spec-driven-feedback/templates/`
- HOOK-SYSTEM.md (979 lines) migrated to `spec-driven-feedback/HOOK-SYSTEM.md`
- All internal paths updated to relative format (e.g., `references/X.md`, `templates/X.yaml`)
- Model changed from `Sonnet` to `claude-opus-4-6`
- ~100 cross-references across src/ tree updated
- Constitution source-tree.md updated
- `devforgeai-feedback` archived as `_devforgeai-feedback.archive/`

**Why:**
- Eliminate cross-skill path fragility (~46 Read() paths pointed to devforgeai-feedback)
- Single source of truth for feedback workflow references
- Enable eventual deletion of devforgeai-feedback
- Consistent with ADR-038 and ADR-039 migration pattern

**Pattern:** Identical to ADR-039 (implementing-stories → spec-driven-dev migration)

**ADR:** `devforgeai/specs/adrs/ADR-040-devforgeai-feedback-to-spec-driven-feedback-migration.md`
