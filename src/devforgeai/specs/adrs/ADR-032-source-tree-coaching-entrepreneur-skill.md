# ADR-032: Source Tree Update for coaching-entrepreneur Skill and business-coach Agent

**Status:** Accepted
**Date:** 2026-03-04
**Decision Makers:** Bryan (Product Owner)
**Epic:** EPIC-072 (Assessment & Coaching Core)

## Context

STORY-469 (Confidence-Building Patterns) created three new framework components:

1. `src/claude/skills/coaching-entrepreneur/references/confidence-building-patterns.md`
2. `src/claude/skills/coaching-entrepreneur/references/imposter-syndrome-interventions.md`
3. `src/claude/agents/business-coach.md`

These paths are not registered in `devforgeai/specs/context/source-tree.md`. The pre-flight validation (Phase 01) flagged the missing paths and required user approval to proceed.

## Decision

Update `devforgeai/specs/context/source-tree.md` to:

1. Add `coaching-entrepreneur/` skill entry in the skills section (alphabetical order, after `brainstorming/`)
2. Add `business-coach.md` agent entry in the agents section (alphabetical order, after `backend-architect.md`)
3. Update agent count from "33 agents" to "34 agents"
4. Update version from 5.2 to 5.3

## Rationale

- All skills and subagents must be registered in source-tree.md for constraint enforcement
- STORY-469 created these files as part of EPIC-072 coaching capabilities
- Prevents future pre-flight validation warnings for stories extending the coaching-entrepreneur skill

## Consequences

- Source-tree.md accurately reflects the new skill and agent
- Future EPIC-072 stories (STORY-470, STORY-471) can reference these paths without validation warnings
- Agent count reflects actual inventory

## References

- STORY-469: Confidence-Building Patterns
- EPIC-072: Assessment & Coaching Core
