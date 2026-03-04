---
id: Sprint-23
name: Business Planning Foundation
epic: EPIC-073
status: Active
start_date: 2026-03-03
end_date: 2026-03-16
capacity: 16
committed_points: 16
completed_points: 0
velocity: TBD
created: 2026-03-03
---

# Sprint-23: Business Planning Foundation

## Sprint Goal

Deliver the complete business planning skill stack for EPIC-073 (Business Planning & Viability). Implement the Lean Canvas guided workflow, milestone-based plan generator, business model pattern matching with viability scoring, and the dual-mode `/business-plan` command. This sprint covers all 4 features enabling users to create structured, milestone-based business plans through guided AI workflows.

## Stories

| # | Story | Title | Points | Priority | Status | Depends On |
|---|-------|-------|--------|----------|--------|------------|
| 1 | [STORY-534](../Stories/STORY-534-dual-mode-business-plan-command.story.md) | Dual-Mode /business-plan Command | 3 | High | Ready for Dev | — |
| 2 | [STORY-531](../Stories/STORY-531-lean-canvas-guided-workflow.story.md) | Lean Canvas Guided Workflow | 5 | High | Ready for Dev | STORY-534 |
| 3 | [STORY-532](../Stories/STORY-532-milestone-based-plan-generator.story.md) | Milestone-Based Plan Generator | 5 | High | Ready for Dev | STORY-531 |
| 4 | [STORY-533](../Stories/STORY-533-business-model-pattern-matching.story.md) | Business Model Pattern Matching | 3 | Medium | Ready for Dev | STORY-531 |

**Total Points:** 16

## Execution Order

```
Week 1: STORY-534 (command) → STORY-531 (Lean Canvas core skill)
Week 2: STORY-532 (Milestones) + STORY-533 (Business Model) [parallel after STORY-531]
```

## Capacity Analysis

| Metric | Value |
|--------|-------|
| Total Capacity | 16 points |
| Committed | 16 points |
| Utilization | 100% |
| Risk Level | Medium (new skill domain) |

## Key Deliverables

- `src/claude/skills/planning-business/SKILL.md` — Core planning skill
- `src/claude/skills/planning-business/references/` — 5 reference files
- `src/claude/commands/business-plan.md` — User-facing command
- `devforgeai/specs/business/business-plan/` — Output templates

## Risks

1. **EPIC-072 dependency** — User adaptive profile may not exist yet; fallback to intermediate depth
2. **New domain** — Business planning is new territory; may need iteration on question quality
3. **Scope** — 16 points in 2 weeks is aggressive for a new skill domain

## Definition of Done (Sprint Level)

- [ ] All 4 stories QA Approved
- [ ] `/business-plan` command functional in both modes
- [ ] Lean Canvas generates complete 9-block output
- [ ] Milestone generator produces valid YAML
- [ ] Business model detection with viability scoring
- [ ] All stories have passing tests
