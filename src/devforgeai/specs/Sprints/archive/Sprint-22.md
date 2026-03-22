---
id: Sprint-22
name: Claude Hooks for Step-Level Phase Enforcement
epic: EPIC-086
status: Active
start_date: 2026-03-03
end_date: 2026-03-16
capacity: 24
committed_points: 24
completed_points: 0
velocity: TBD
created: 2026-03-02
---

# Sprint-22: Claude Hooks for Step-Level Phase Enforcement

## Sprint Goal

Implement the complete hook-based enforcement stack for `/dev` workflow phase compliance. Deploy 4 Claude Code hooks (SubagentStop, TaskCompleted, Stop, SessionStart) backed by a 72-step registry, providing external verification that replaces self-reported phase tracking.

## Stories

| # | Story | Title | Points | Priority | Status | Depends On |
|---|-------|-------|--------|----------|--------|------------|
| 1 | [STORY-525](../Stories/STORY-525-phase-steps-registry-step-level-tracking.story.md) | Phase Steps Registry + Step-Level Tracking | 5 | High | Ready for Dev | — |
| 2 | [STORY-526](../Stories/STORY-526-subagent-stop-hook-auto-track-invocations.story.md) | SubagentStop Hook — Auto-Track Invocations | 3 | High | Ready for Dev | STORY-525 |
| 3 | [STORY-527](../Stories/STORY-527-task-completed-hook-step-validation-gate.story.md) | TaskCompleted Hook — Step Validation Gate | 5 | High | Ready for Dev | STORY-525, STORY-526 |
| 4 | [STORY-528](../Stories/STORY-528-stop-hook-phase-completion-gate.story.md) | Stop Hook — Phase Completion Gate | 5 | High | Ready for Dev | STORY-525 |
| 5 | [STORY-529](../Stories/STORY-529-session-start-hook-context-injection.story.md) | SessionStart Hook — Context Injection | 3 | High | Ready for Dev | STORY-525 |
| 6 | [STORY-530](../Stories/STORY-530-phase-file-taskcreate-integration.story.md) | Phase File TaskCreate Integration | 3 | High | Ready for Dev | STORY-525 |

**Total Points:** 24

## Execution Order

```
Week 1: STORY-525 (foundation) → STORY-526 (SubagentStop) → STORY-527 (TaskCompleted)
Week 2: STORY-528 (Stop) + STORY-529 (SessionStart) + STORY-530 (Phase Files) [parallel]
```

### Dependency Graph

```
STORY-525 ─┬── STORY-526 ── STORY-527
            ├── STORY-528
            ├── STORY-529
            └── STORY-530
```

## Key Deliverables

- `.claude/hooks/phase-steps-registry.json` — 72-step registry (STORY-525)
- `.claude/hooks/subagent-stop-hook.sh` — Auto-track invocations (STORY-526)
- `.claude/hooks/task-completed-hook.sh` — Step validation gate (STORY-527)
- `.claude/hooks/stop-hook.sh` — Phase completion gate (STORY-528)
- `.claude/hooks/session-start-hook.sh` — Context injection (STORY-529)
- 12 updated phase files with Progressive Task Disclosure (STORY-530)
- Updated `.claude/settings.json` with 4 new hook entries

## Success Metrics

- `subagents_invoked` populated in phase-state.json: 0% → 100%
- Phases with required subagents actually invoked: unknown → 95%+
- Workflow completions with all 12 phases: ~40% → 90%+
- Phase skips caught before session end: 0 → 80%+

## Capacity

| Metric | Value |
|--------|-------|
| Total Capacity | 24 points |
| Committed | 24 points |
| Utilization | 100% |
| Buffer | 0 points |

## Burndown

| Day | Planned Remaining | Actual Remaining |
|-----|-------------------|------------------|
| Day 1 (Mar 3) | 24 | — |
| Day 5 (Mar 7) | 16 | — |
| Day 10 (Mar 14) | 0 | — |

## Retrospective

*To be completed after sprint ends*

---

**Sprint Template Version:** 1.0
**Created:** 2026-03-02
