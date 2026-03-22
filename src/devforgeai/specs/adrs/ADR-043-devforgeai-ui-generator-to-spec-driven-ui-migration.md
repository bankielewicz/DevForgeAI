# ADR-043: DevForgeAI-UI-Generator to Spec-Driven-UI Migration

## Status

**Accepted** (2026-03-18)

## Context

The `devforgeai-ui-generator` skill is the 7-phase UI specification and code generation workflow that produces front-end components for Web (React, Blazor, ASP.NET, HTML), Desktop GUI (WPF, Tkinter), and Terminal interfaces. While functionally complete, it uses inline expansion without structural anti-skip enforcement (Execute-Verify-Record pattern), making it vulnerable to token optimization bias.

This causes:
- Claude skipping phases/steps to save tokens, creating double work
- No checkpoint persistence for session resumption
- No per-phase reference loading (references loaded ad-hoc, easily skipped)
- No binary gate enforcement at phase boundaries
- Inconsistent execution quality depending on context window pressure

All other SDLC skill families have been successfully migrated:
- ADR-038: discovering-requirements -> spec-driven-ideation
- ADR-039: designing-systems -> spec-driven-architecture
- ADR-039: implementing-stories -> spec-driven-dev
- ADR-040: devforgeai-feedback -> spec-driven-feedback
- ADR-041: devforgeai-story-creation -> spec-driven-stories
- ADR-042: devforgeai-documentation -> spec-driven-documentation
- brainstorming -> spec-driven-brainstorming
- devforgeai-qa -> spec-driven-qa
- devforgeai-release -> spec-driven-release
- story-remediation -> spec-driven-remediation
- devforgeai-qa-remediation -> spec-driven-qa-remediation
- validating-epic-coverage -> spec-driven-coverage
- auditing-w3-compliance -> spec-driven-w3-compliance
- root-cause-diagnosis + devforgeai-rca -> spec-driven-rca

## Decision

1. **Create `spec-driven-ui`** as a new skill with full anti-skip enforcement:
   - 4-layer enforcement: per-phase reference loading, binary CLI gates, checkpoint state tracking, artifact verification
   - Execute-Verify-Record pattern on every mandatory step
   - 9 separate phase files (phases 00-08, expanding from the original 7 phases + Phase N)
   - Phase State Initialization via `devforgeai-validate phase-init ${IDENTIFIER} --workflow=ui`
   - Token Optimization Bias prohibition statement
   - Self-check violation list (8 items)

2. **Migrate all files** from `devforgeai-ui-generator/` into `spec-driven-ui/` to make it fully self-contained:
   - 19 reference files (18 migrated + 1 new `shared-protocols.md`)
   - 7 asset templates (React, Blazor, ASP.NET, HTML, WPF, Tkinter, Terminal)
   - 2 Python scripts (`validate_context.py`, `ensure_spec_dir.py`)
   - Renamed underscore files to hyphens: `web_best_practices.md` -> `web-best-practices.md`, etc.

3. **Rewire slash command:**
   - `/create-ui` -> invoke `spec-driven-ui`
   - Backup old command to `backup/create-ui.md`

4. **Update all external references** across 22 active files (commands, memory files, agent files, protocols, other skills).

5. **Archive** `devforgeai-ui-generator/` to `backup/devforgeai-ui-generator/`.

## Phase Mapping (Old -> New)

| New Phase | Old Phase | Name |
|-----------|-----------|------|
| 00 | NEW | Initialization (CWD validation, parameter extraction, phase-init) |
| 01 | Phase 1 | Context Validation (6 context files) |
| 02 | Phase 2 | Story Analysis & Mode Detection |
| 03 | Phase 3 | Interactive Discovery (AskUserQuestion flows) |
| 04 | Phase 4 | Template & Best Practices Loading |
| 05 | Phase 5 | Code Generation |
| 06 | Phase 6 | Documentation & ui-spec-formatter Subagent |
| 07 | Phase 7 | Specification Validation (user-driven resolution) |
| 08 | Phase N | Feedback & Completion (hooks + result report) |

## Constitution File Changes

This ADR authorizes the following changes to immutable context files:

### source-tree.md
- Replace `devforgeai-ui-generator/` directory references with `spec-driven-ui/`
- Add `phases/`, `references/`, `assets/`, `scripts/` subdirectories under spec-driven-ui

**Applied:** source-tree.md updated 2026-03-19.

## Consequences

### Positive
- `spec-driven-ui` has full anti-skip enforcement preventing token optimization bias
- All 9 phases execute for every invocation (no mode-conditional skipping)
- Self-contained skill with zero cross-references to old skill
- Per-phase reference loading prevents "already covered" rationalization
- 15th skill family migration complete
- Consistent with all other spec-driven-* skills

### Negative
- Reference files temporarily duplicated in archive directory (until archive is deleted)
- Slightly higher token overhead (~40K vs ~35K per component) due to EVR enforcement boilerplate

### Neutral
- Follows identical pattern to ADR-038 through ADR-042
- No change to UI generation functionality (same 7 workflow phases, same templates, same subagent)

## References

- ADR-038: Discovering-Requirements to Spec-Driven-Ideation Migration
- ADR-039: Implementing-Stories to Spec-Driven-Dev Migration
- ADR-039: Designing-Systems Consolidation into Spec-Driven-Architecture
- ADR-040: DevForgeAI-Feedback to Spec-Driven-Feedback Migration
- ADR-041: DevForgeAI-Story-Creation to Spec-Driven-Stories Migration
- ADR-042: DevForgeAI-Documentation to Spec-Driven-Documentation Migration
- ADR-021: Configuration Layer Alignment Protocol (mutability rules for context files)
