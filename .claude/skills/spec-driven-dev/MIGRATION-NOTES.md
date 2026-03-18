# spec-driven-dev Migration Notes

## 2026-03-18: Absorbed implementing-stories (ADR-039)

**What changed:**
- 47 core reference files migrated from `implementing-stories/references/` to `spec-driven-dev/references/`
- 19 preflight reference files migrated to `spec-driven-dev/references/preflight/`
- 2 asset templates migrated to `spec-driven-dev/assets/templates/`
- All internal paths updated to relative format (e.g., `references/X.md`)
- Model changed from `Sonnet` to `claude-opus-4-6`
- Added Treelint integration section and Reference Files inventory to SKILL.md
- `/resume-dev` command updated to invoke `spec-driven-dev` instead of `implementing-stories`
- ~157 cross-references across src/ tree updated
- 5 Constitution files updated (source-tree.md, anti-patterns.md, coding-standards.md, architecture-constraints.md, tech-stack.md)
- `implementing-stories` archived as `_implementing-stories.archive/`

**Why:**
- Eliminate cross-skill path fragility (spec-driven-dev depended on implementing-stories for all reference files)
- Single source of truth for TDD workflow references
- Enable eventual deletion of implementing-stories
- Consistent skill invocation (`/dev` and `/resume-dev` both invoke `spec-driven-dev`)

**Pattern:** Identical to ADR-038 (discovering-requirements → spec-driven-ideation migration)

**ADR:** `devforgeai/specs/adrs/ADR-039-implementing-stories-to-spec-driven-dev-migration.md`
