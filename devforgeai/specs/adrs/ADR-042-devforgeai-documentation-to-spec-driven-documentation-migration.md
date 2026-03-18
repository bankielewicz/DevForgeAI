# ADR-042: DevForgeAI-Documentation to Spec-Driven-Documentation Migration

## Status

**Accepted** (2026-03-18)

## Context

The `devforgeai-documentation` skill (v1.1.0, 1,167 lines) is the documentation generation, auditing, and remediation workflow. It supports 3 workflow paths: Generation (greenfield/brownfield, Phases 0-7), Audit (4-dimension DevEx scoring, Phases A.0-A.4), and Fix (automated/interactive remediation, Phases B.0-B.5). While functionally complete, it lacks the structural anti-skip enforcement (Execute-Verify-Gate pattern) that the other 8 spec-driven-* skills use to prevent token optimization bias.

This causes:
- Claude skipping phases/steps to save tokens, creating double work
- No checkpoint persistence for session resumption
- No per-phase reference loading (references loaded ad-hoc, easily skipped)
- No binary gate enforcement at phase boundaries
- Inconsistent execution quality depending on context window pressure

All 8 other SDLC skill families have been successfully migrated:
- ADR-038: discovering-requirements -> spec-driven-ideation
- ADR-039: designing-systems -> spec-driven-architecture
- ADR-039: implementing-stories -> spec-driven-dev
- ADR-040: devforgeai-feedback -> spec-driven-feedback
- ADR-041: devforgeai-story-creation -> spec-driven-stories
- brainstorming -> spec-driven-brainstorming
- devforgeai-qa -> spec-driven-qa
- devforgeai-release -> spec-driven-release

## Decision

1. **Create `spec-driven-documentation`** as a new skill with full anti-skip enforcement:
   - 4-layer enforcement: per-phase reference loading, binary CLI gates, checkpoint state tracking, artifact verification
   - Execute-Verify-Record pattern on every mandatory step (69 EVG triplets total)
   - 21 separate phase files across 3 workflow paths
   - Checkpoint JSON for session resumption with per-workflow state
   - Token Optimization Bias prohibition statement

2. **Architecture: Single skill with conditional phase dispatch** (Option C, matching spec-driven-feedback precedent):
   - Three workflow paths share Phase 01 (Preflight) and Phase 02 (Dispatch), then diverge:
     - **Generation** (greenfield/brownfield): Phases G03-G10 (10 total phases)
     - **Audit** (`--audit=dryrun`): Phases A03-A07 (7 total phases)
     - **Fix** (`--audit-fix`): Phases F03-F08 (8 total phases)
   - Prefixed phase IDs (G03, A03, F03) prevent cross-workflow confusion
   - Separate CLI `--workflow=` flags (doc-gen, doc-audit, doc-fix) for state isolation

3. **Migrate all files** from `devforgeai-documentation/` into `spec-driven-documentation/` to make it fully self-contained:
   - 8 reference files copied (with internal path updates)
   - 3 new reference files created (parameter-extraction.md, audit-workflow.md, audit-fix-catalog.md)
   - 8 template files copied unchanged
   - Monolithic 1,167-line SKILL.md decomposed into ~280-line lean orchestrator + 21 phase files

4. **Rewire slash command:**
   - `/document` -> invoke `spec-driven-documentation`
   - Backup old command to `src/claude/commands/backup/document.md`

5. **Update all external references** across memory files (skills-reference.md, commands-reference.md, documentation-command-guide.md, skill-execution-troubleshooting.md) and agent files (documentation-writer.md, code-analyzer.md).

6. **Archive** `devforgeai-documentation/` as `backup/_devforgeai-documentation.archive/` with HALT header.

7. **Model upgrade** from `claude-sonnet-4-6` to `claude-opus-4-6` (consistent with all spec-driven migrations).

## Constitution File Changes

This ADR authorizes the following changes to immutable context files:

### source-tree.md
- Replace `devforgeai-documentation/` directory references with `spec-driven-documentation/`
- Add `phases/`, `references/`, `assets/templates/` subdirectories under spec-driven-documentation
- Document 21 phase files (2 shared + 8 generation + 5 audit + 6 fix)

## Consequences

### Positive
- `spec-driven-documentation` has full anti-skip enforcement preventing token optimization bias
- 21 phase files with 69 EVG triplets ensure every step is executed, verified, and recorded
- Checkpoint JSON enables session resumption after context window clears
- Self-contained skill with zero active references to old skill
- 9th and final core SDLC skill migration complete (all 9 families now use spec-driven-* pattern)
- Per-phase reference loading prevents "already covered" rationalization
- 3 new reference files (audit-workflow.md, audit-fix-catalog.md, parameter-extraction.md) fill documentation gaps that existed in the original skill
- Prefixed phase IDs (G/A/F) make multi-workflow skill self-documenting

### Negative
- Reference files temporarily duplicated in archive directory (until archive is deleted)
- 21 phase files increase total file count (but each is independently loadable, reducing context pressure)
- Larger combined content due to EVG boilerplate across 21 files

### Neutral
- Follows identical pattern to ADR-038 through ADR-041
- `/document` command syntax unchanged (backward compatible)
- Subagent contracts (documentation-writer, code-analyzer) unchanged

## References

- ADR-038: Discovering-Requirements to Spec-Driven-Ideation Migration
- ADR-039: Implementing-Stories to Spec-Driven-Dev Migration
- ADR-039: Designing-Systems Consolidation into Spec-Driven-Architecture
- ADR-040: DevForgeAI-Feedback to Spec-Driven-Feedback Migration
- ADR-041: DevForgeAI-Story-Creation to Spec-Driven-Stories Migration
- ADR-021: Configuration Layer Alignment Protocol (mutability rules for context files)
