# ADR-029: Source Tree Update for EPIC-074 Market Research Deliverables

**Date:** 2026-03-03
**Status:** Accepted
**Acceptance Date:** 2026-03-03
**Deciders:** Solo Developer, DevForgeAI Framework
**Tags:** source-tree, EPIC-074, STORY-535, STORY-536, STORY-537, STORY-538

## Context

EPIC-074 (Market Research & Competition) introduces 3 new framework components:

1. **`researching-market` skill** — Market sizing, competitive analysis, and customer interview workflows
2. **`market-analyst` subagent** — Research synthesis and positioning matrix generation
3. **`market-research` command** — User-facing command delegating to the skill

The custody chain audit (`devforgeai/qa/audit/custody-chain-audit-stories-535-538.md`) identified 3 CRITICAL findings (F-001, F-002, F-003): all 4 stories reference file paths not yet registered in source-tree.md. Since source-tree.md is an IMMUTABLE context file, this ADR is required before implementation can proceed.

## Decision

Add the following entries to `devforgeai/specs/context/source-tree.md`:

1. **Skill directory** under `src/claude/skills/`:
   ```
   ├── researching-market/              # Market research skill (EPIC-074)
   │   ├── SKILL.md                     # Market sizing, competitive analysis, interviews
   │   └── references/
   │       ├── market-sizing-methodology.md   # TAM/SAM/SOM estimation (STORY-535)
   │       ├── fermi-estimation.md            # Fermi estimation guidance (STORY-535)
   │       ├── competitive-analysis-framework.md  # Competitor positioning (STORY-536)
   │       └── customer-interview-guide.md    # Interview best practices (STORY-537)
   ```

2. **Subagent file** under `src/claude/agents/`:
   ```
   ├── market-analyst.md                # Research synthesis subagent (STORY-536, EPIC-074)
   ```

3. **Command file** under `src/claude/commands/`:
   ```
   ├── market-research.md               # /market-research command (STORY-538, EPIC-074)
   ```

## Rationale

1. All new framework components must be registered in source-tree.md before creation (Source: devforgeai/specs/context/architecture-constraints.md, lines 83-102 — Context File Enforcement).
2. The skill follows gerund naming (`researching-market`) per ADR-017.
3. Progressive disclosure pattern: SKILL.md < 1,000 lines with 4 reference files for deep documentation.
4. The subagent follows domain-role naming (`market-analyst`) per coding-standards.md.
5. The command follows action-object naming (`market-research`) per coding-standards.md.

## Consequences

### Positive
- Unblocks all 4 EPIC-074 stories (STORY-535, 536, 537, 538) for implementation
- QA anti-pattern-scanner will not flag structure violations for these paths
- Future stories in EPIC-074 Sprint 2 can reference these paths

### Negative
- source-tree.md grows by ~12 lines (acceptable — well within 600-line limit)

### Neutral
- No impact on existing skills, agents, or commands

## References

- Custody chain audit: `devforgeai/qa/audit/custody-chain-audit-stories-535-538.md`
- EPIC-074: `devforgeai/specs/Epics/EPIC-074-market-research-competition.epic.md`
- ADR-017: Skill gerund naming convention
