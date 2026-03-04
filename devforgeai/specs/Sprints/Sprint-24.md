---
id: Sprint-24
name: Market Research Foundation
epic: EPIC-074
status: Active
start_date: 2026-03-03
end_date: 2026-03-10
capacity: 11
committed_points: 11
completed_points: 0
velocity: TBD
created: 2026-03-03
---

# Sprint-24: Market Research Foundation

## Sprint Goal

Deliver the core market research skill stack for EPIC-074 (Market Research & Competition). Implement the TAM/SAM/SOM market sizing workflow, competitive landscape analysis with market-analyst subagent, customer interview question generator, and the `/market-research` command assembling the full `researching-market` skill. This sprint enables users to validate business ideas through structured market research.

## Stories

| # | Story | Title | Points | Priority | Status | Depends On |
|---|-------|-------|--------|----------|--------|------------|
| 1 | [STORY-535](../Stories/STORY-535-market-sizing-guided-workflow.story.md) | Market Sizing Guided Workflow | 3 | High | Ready for Dev | — |
| 2 | [STORY-536](../Stories/STORY-536-competitive-landscape-analysis.story.md) | Competitive Landscape Analysis | 3 | High | Ready for Dev | STORY-535 |
| 3 | [STORY-537](../Stories/STORY-537-customer-interview-question-generator.story.md) | Customer Interview Question Generator | 2 | High | Ready for Dev | STORY-535 |
| 4 | [STORY-538](../Stories/STORY-538-market-research-command-skill-assembly.story.md) | /market-research Command & Skill Assembly | 3 | High | Ready for Dev | STORY-535, STORY-536, STORY-537 |

**Total Points:** 11

## Execution Order

Based on dependency chain:

```
1. STORY-535 (Market Sizing) — no dependencies, start first
2. STORY-536 (Competitive Analysis) — after STORY-535
   STORY-537 (Customer Interviews) — after STORY-535 (parallel with 536)
3. STORY-538 (Command & Assembly) — after 535, 536, 537
```

## Key Deliverables

| Deliverable | Type | Path | Story |
|-------------|------|------|-------|
| `researching-market/SKILL.md` | Skill | `src/claude/skills/researching-market/` | STORY-535, 537, 538 |
| `market-analyst.md` | Subagent | `src/claude/agents/` | STORY-536 |
| `market-research.md` | Command | `src/claude/commands/` | STORY-538 |
| `market-sizing-methodology.md` | Reference | `src/claude/skills/researching-market/references/` | STORY-535 |
| `fermi-estimation.md` | Reference | `src/claude/skills/researching-market/references/` | STORY-535 |
| `competitive-analysis-framework.md` | Reference | `src/claude/skills/researching-market/references/` | STORY-536 |
| `customer-interview-guide.md` | Reference | `src/claude/skills/researching-market/references/` | STORY-537 |

## Capacity

| Metric | Value |
|--------|-------|
| Sprint Duration | 7 days |
| Total Capacity | 11 points |
| Committed Points | 11 points |
| Buffer | 0 points |

## Risks

1. **STORY-538 is blocked by 3 stories** — Cannot start until 535, 536, 537 complete
2. **internet-sleuth availability** — Core dependency for market data; Fermi fallback mitigates
3. **EPIC-072 not complete** — User profile integration degrades to defaults

## Daily Progress

| Day | Date | Completed | In Progress | Remaining |
|-----|------|-----------|-------------|-----------|
| 1 | 2026-03-03 | 0 pts | — | 11 pts |

---

**Sprint Template Version:** 1.0
**Last Updated:** 2026-03-03
