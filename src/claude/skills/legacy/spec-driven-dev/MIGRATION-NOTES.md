# spec-driven-dev Migration Notes

## 2026-03-18: Absorbed spec-driven-dev (ADR-039)

**What changed:**
- 47 core reference files migrated from `spec-driven-dev/references/` to `spec-driven-dev/references/`
- 19 preflight reference files migrated to `spec-driven-dev/references/preflight/`
- 2 asset templates migrated to `spec-driven-dev/assets/templates/`
- All internal paths updated to relative format (e.g., `references/X.md`)
- Model changed from `Sonnet` to `opus`
- Added Treelint integration section and Reference Files inventory to SKILL.md
- `/resume-dev` command updated to invoke `spec-driven-dev` instead of `spec-driven-dev`
- ~157 cross-references across src/ tree updated
- 5 Constitution files updated (source-tree.md, anti-patterns.md, coding-standards.md, architecture-constraints.md, tech-stack.md)
- `spec-driven-dev` archived as `_spec-driven-dev.archive/`

**Why:**
- Eliminate cross-skill path fragility (spec-driven-dev depended on spec-driven-dev for all reference files)
- Single source of truth for TDD workflow references
- Enable eventual deletion of spec-driven-dev
- Consistent skill invocation (`/dev` and `/resume-dev` both invoke `spec-driven-dev`)

**Pattern:** Identical to ADR-038 (spec-driven-brainstorming → spec-driven-ideation migration)

**ADR:** `devforgeai/specs/adrs/ADR-039-spec-driven-dev-to-spec-driven-dev-migration.md`
