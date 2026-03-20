# ADR-044: DevForgeAI-Subagent-Creation to Spec-Driven-Agents Migration

## Status

**Accepted** (2026-03-19)

## Context

The `devforgeai-subagent-creation` skill is the 6-phase agent creation workflow that orchestrates the `agent-generator` subagent to produce DevForgeAI-aware Claude Code subagents. While functionally complete, it has **zero anti-skip enforcement** — all 6 phases are purely informational ("here's what we do") rather than mandatory ("you MUST do this").

This causes:
- Claude skipping phases/steps to save tokens, creating double work
- No checkpoint persistence for session resumption
- No per-phase reference loading (references loaded ad-hoc, easily skipped)
- No Execute-Verify-Record enforcement at step boundaries
- Requirements gathering collapsed into agent-generator invocation, preventing incomplete specs from being caught early
- Validation bundled inside generation, invisible to the skill's enforcement layer

All 17 other SDLC skill families have been successfully migrated to the `spec-driven-*` pattern:
- ADR-038: discovering-requirements -> spec-driven-ideation
- ADR-039: designing-systems -> spec-driven-architecture
- ADR-039: implementing-stories -> spec-driven-dev
- ADR-040: devforgeai-feedback -> spec-driven-feedback
- ADR-041: devforgeai-story-creation -> spec-driven-stories
- ADR-042: devforgeai-documentation -> spec-driven-documentation
- ADR-043: devforgeai-ui-generator -> spec-driven-ui
- brainstorming -> spec-driven-brainstorming
- devforgeai-qa -> spec-driven-qa
- devforgeai-release -> spec-driven-release
- story-remediation -> spec-driven-remediation
- devforgeai-qa-remediation -> spec-driven-qa-remediation
- validating-epic-coverage -> spec-driven-coverage
- root-cause-diagnosis + devforgeai-rca -> spec-driven-rca
- auditing-w3-compliance -> spec-driven-w3-compliance
- devforgeai-research -> spec-driven-research
- devforgeai-github-actions -> spec-driven-ci

`devforgeai-subagent-creation` was the **last remaining un-migrated active SDLC skill**.

## Decision

1. **Create `spec-driven-agents`** as a new skill with full anti-skip enforcement:
   - 4-layer enforcement: per-phase reference loading, checkpoint-based state tracking, artifact verification, step registry with data key completion
   - Execute-Verify-Record pattern on every mandatory step
   - 6 separate phase files (one per workflow phase)
   - Checkpoint JSON for session resumption (`--resume AGENT-NNN`)
   - Token Optimization Bias prohibition statement
   - Self-check violation boxes (7 items)

2. **Migrate all files** from `devforgeai-subagent-creation/` into `spec-driven-agents/` to make it fully self-contained:
   - 5 migrated reference files + 3 new (checkpoint-schema, error-handling, user-interaction-patterns)
   - 7 template files (code-reviewer, test-automator, documentation-writer, deployment-coordinator, requirements-analyst, skill-template, command-template-lean-orchestration)
   - 6 phase files (framework-context, requirements-gathering, specification-assembly, agent-generation, validation, result-handoff)

3. **Restructure phases** for better enforcement:
   - Phase 00 (inline): Initialization with checkpoint bootstrapping
   - Phase 01: Framework Context Loading (was Phase 2)
   - Phase 02: Requirements Gathering (NEW — was implicit inside agent-generator)
   - Phase 03: Specification Assembly (was Phase 4)
   - Phase 04: Agent Generation via agent-generator subagent (was Phase 5)
   - Phase 05: Validation — SEPARATED from generation (was bundled in Phase 5)
   - Phase 06: Result Processing & Handoff (was Phase 6)

4. **Rewire slash command:**
   - `/create-agent` -> invoke `spec-driven-agents`
   - Backup old command to `src/claude/commands/backup/create-agent.md`

5. **Update all external references** across commands, memory files, and documentation.

6. **Archive** `devforgeai-subagent-creation/` as `backup/_devforgeai-subagent-creation.archive/`.

## Constitution File Changes

This ADR authorizes the following changes to constitutional/immutable files:

### source-tree.md
- Replace `devforgeai-subagent-creation/` directory entry with `spec-driven-agents/`
- Update subdirectory structure to reflect new layout: `phases/`, `references/`, `assets/templates/`

### skills-reference.md
- Replace `devforgeai-subagent-creation` skill entry with `spec-driven-agents`
- Update skill catalog listing from `devforgeai-subagent-creation/SKILL.md` to `spec-driven-agents/SKILL.md`
- Update invocation example from `Skill(command="devforgeai-subagent-creation")` to `Skill(command="spec-driven-agents")`

## Consequences

### Positive
- All SDLC skills now follow the `spec-driven-*` pattern with anti-skip enforcement
- Session resume support via checkpoint JSON prevents lost work on context window clears
- Explicit Requirements Gathering phase (Phase 02) catches incomplete specifications before agent-generator invocation
- Separated Validation phase (Phase 05) makes compliance checking visible to enforcement layer
- Self-sufficient skill with all references, templates, and assets local

### Negative
- Increased token cost per execution due to mandatory reference loading at each phase
- Agent-generator subagent references in `src/claude/agents/agent-generator/` still reference old paths (low impact — the agent-generator receives its spec via Task prompt, not file paths)

### Neutral
- The `agent-generator` subagent itself is unchanged — only the orchestration layer was migrated
- Template files are identical to the old skill (no content changes)
