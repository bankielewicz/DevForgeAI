---
id: EPIC-080
title: Revisitation & Framework Evolution (Business Skills Cross-Cutting)
status: Planning
start_date: 2026-02-21
target_date: TBD
total_points: 6
completed_points: 0
created: 2026-02-21
owner: DevForgeAI
tech_lead: DevForgeAI AI Agent
team: DevForgeAI
source_brainstorm: BRAINSTORM-011-business-skills-framework
source_requirements: devforgeai/specs/requirements/business-skills-framework-requirements.md
plan_file: /home/bryan/.claude/plans/jiggly-launching-backus.md
---

# Epic: Revisitation & Framework Evolution (Business Skills Cross-Cutting)

## Business Goal

Ensure that each new business skills epic integrates coherently with previously implemented skills by establishing a structured post-epic revisitation loop. As the business skills framework grows from EPIC-072 through EPIC-079, skills must work together seamlessly — the coaching engine must adapt as new domains come online, cross-skill data flows must be validated, and the original brainstorm vision (BRAINSTORM-011) must be re-evaluated against actual implementation to catch drift.

Without revisitation, epics accumulate integration debt: skills that work in isolation but fail to compose into a coherent user experience. This epic formalizes the "re-brainstorm after each epic" pattern proposed in BRAINSTORM-011 (user decision #11).

## Success Metrics

- **Metric 1:** Post-epic revisitation checklist is triggered after each epic's QA approval
- **Metric 2:** Integration review identifies cross-skill data flow gaps before they reach users
- **Metric 3:** Brainstorm-to-implementation drift is documented and addressed per revisitation cycle
- **Metric 4:** User feedback from coaching sessions is synthesized into actionable skill improvements

**Measurement Plan:**
- Revisitation reports generated after each epic completion in `devforgeai/specs/business/revisitation/`
- Integration test results validated per revisitation cycle
- Review frequency: After each epic's QA approval

## Scope

### In Scope

1. **Feature 1: Post-Epic Revisitation Checklist** (2 pts) — Priority: P1
   - Structured checklist triggered after each epic's QA approval
   - Re-reads BRAINSTORM-011 and compares current state to original vision
   - Evaluates: skill integration quality, data flow correctness, user experience coherence
   - Generates revisitation report to `devforgeai/specs/business/revisitation/post-{epic-id}-review.md`
   - Maps to: FR-023

2. **Feature 2: Cross-Skill Integration Audit** (2 pts) — Priority: P1
   - Validates data flows between business skills (e.g., assessment profile → coaching → business plan → market research)
   - Checks artifact consistency (YAML schema compatibility across skills)
   - Identifies orphaned references or broken cross-skill dependencies
   - Generates integration health report
   - Maps to: FR-023

3. **Feature 3: Brainstorm Resumption Pattern** (1 pt) — Priority: P1
   - Implements `/brainstorm --resume BRAINSTORM-011` pattern for revisitation
   - Pre-populates context with: implemented epics, current skill inventory, pending epics
   - Generates "what changed since last revisitation" diff summary
   - Maps to: FR-023

4. **Feature 4: Coaching Feedback Synthesis** (1 pt) — Priority: P2
   - Aggregates user feedback from coaching sessions (EPIC-072 session logs)
   - Synthesizes patterns: common struggles, feature requests, adaptation effectiveness
   - Feeds recommendations into next epic's planning phase
   - Output to `devforgeai/specs/business/revisitation/feedback-synthesis.md`

### Out of Scope

- ❌ Automated code refactoring based on revisitation findings (manual via `/dev`)
- ❌ User-facing revisitation UI (internal framework process only)
- ❌ Cross-project revisitation (scoped to business skills framework only)
- ❌ Automated epic creation from revisitation findings (recommendations only)

## Target Sprints

### Sprint 1: Revisitation Core
**Goal:** Deliver post-epic checklist, integration audit, and brainstorm resumption
**Estimated Points:** 5
**Features:**
- Feature 1: Post-Epic Revisitation Checklist (STORY-A, STORY-B)
- Feature 2: Cross-Skill Integration Audit (STORY-C)
- Feature 3: Brainstorm Resumption Pattern (STORY-D)

**Key Deliverables:**
- Revisitation checklist template
- Integration audit workflow
- Brainstorm resumption context loader

### Sprint 2: Feedback Loop
**Goal:** Deliver coaching feedback synthesis
**Estimated Points:** 1
**Features:**
- Feature 4: Coaching Feedback Synthesis (STORY-E)

**Key Deliverables:**
- Feedback aggregation workflow
- Synthesis report template

## User Stories

1. **As a** framework maintainer, **I want** an automated revisitation process after each epic **so that** new skills integrate well with existing ones
2. **As a** framework maintainer, **I want** cross-skill integration audits **so that** data flows correctly between business skills
3. **As a** framework maintainer, **I want** to resume BRAINSTORM-011 with current context **so that** I can evaluate drift from original vision
4. **As a** framework maintainer, **I want** coaching session feedback synthesized **so that** user patterns inform future skill improvements

## Technical Considerations

### Architecture Impact
- **No new skills** — revisitation is a workflow pattern, not a user-facing skill
- **No new commands** — uses existing `/brainstorm --resume` pattern
- **No new subagents** — leverages existing framework capabilities
- **New artifact directory:** `devforgeai/specs/business/revisitation/`

### Technology Decisions
- **Data format:** Markdown for revisitation reports; YAML for integration audit results
- **Trigger mechanism:** Manual trigger after epic QA approval (framework hook candidate for future automation)
- **Context loading:** Reads all implemented business skill SKILL.md files + artifact directories to assess current state

### Constraints (From Context Files)
- Development in `src/` tree; tests in `tests/`; operational `.claude/` after QA
- All workflows must read 6 context files before processing
- Revisitation reports are documentation artifacts, not executable code

### Integration Points
- **Reads from:** All business skill artifacts (EPIC-072 through EPIC-079)
- **Reads from:** BRAINSTORM-011 (source of truth for vision)
- **Reads from:** Coaching session logs (`devforgeai/specs/business/coaching/session-log.yaml`)
- **Writes to:** `devforgeai/specs/business/revisitation/` (reports)

## Dependencies

### Internal Dependencies
- [x] **6 context files exist** in `devforgeai/specs/context/`
  - **Status:** Complete

- [x] **BRAINSTORM-011** exists
  - **Status:** Complete

- [ ] **EPIC-072 (Assessment & Coaching Core)** — First epic to trigger revisitation
  - **Status:** Planning
  - **Impact if delayed:** Revisitation checklist can be designed but not executed until first epic completes

### External Dependencies
- None

### Epic Dependencies
- **This epic depends on:** None (can be designed in parallel; execution requires at least one epic complete)
- **This epic blocks:** None
- **Cross-cutting:** Triggered after each of EPIC-072 through EPIC-079

## Risks & Mitigation

### Risk 1: Revisitation becomes perfunctory checkbox exercise
- **Probability:** Medium
- **Impact:** High — defeats the purpose of integration quality
- **Mitigation:** Checklist requires specific evidence for each item (file paths, test results); cannot mark complete without artifacts
- **Contingency:** Add mandatory integration test requirement per revisitation

### Risk 2: Brainstorm drift accumulates undetected
- **Probability:** Low (with revisitation)
- **Impact:** Medium — final product diverges from user vision
- **Mitigation:** Each revisitation explicitly compares current state to BRAINSTORM-011 decisions; drift documented with rationale
- **Contingency:** User review of drift report with AskUserQuestion for course correction

## Stakeholders

### Primary Stakeholders
- **Product Owner:** User (Bryan)
- **Tech Lead:** DevForgeAI AI Agent
- **Framework:** DevForgeAI (quality assurance)

### Target Users
- Framework maintainers (DevForgeAI AI Agent)
- Product owner reviewing integration quality

## Deliverable Inventory

| Deliverable | Type | Dev Path | Feature |
|-------------|------|----------|---------|
| Revisitation checklist template | Template | `src/claude/skills/designing-systems/assets/templates/` | F1 |
| Integration audit workflow | Documentation | `devforgeai/specs/business/revisitation/` | F2 |
| Brainstorm resumption context | Workflow | Integrated into `/brainstorm --resume` | F3 |
| Feedback synthesis template | Template | `devforgeai/specs/business/revisitation/` | F4 |

**Total: 4 workflow deliverables** (templates + documentation, no new skills/commands)

## Feature Dependency Chain

```
Feature 1 (Post-Epic Revisitation Checklist)
  ├── Feature 2 (Cross-Skill Integration Audit)
  └── Feature 3 (Brainstorm Resumption Pattern)
        └── Feature 4 (Coaching Feedback Synthesis)
```

## Complexity Assessment

**Score: 3.0 / 10**

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Artifact count | 2/10 | Templates and docs only; no new skills/commands/agents |
| State management | 3/10 | Reads existing artifacts; writes reports |
| Scope clarity | 7/10 | Well-defined: checklist + audit + resume + feedback |
| Framework integration | 4/10 | Uses existing patterns (brainstorm resume, feedback) |
| Testing strategy | 3/10 | Template validation + checklist completeness |
| Cross-epic coordination | 5/10 | Must understand all business skill data flows |

## Timeline

```
Epic Timeline:
================================
Sprint 1: Revisitation Core (5 pts)
Sprint 2: Feedback Loop (1 pt)
================================
Total Duration: 1-2 sprints
Total Points: 6
Stories: 5
```

### Key Milestones
- [ ] **Sprint 1 Complete:** Post-epic revisitation checklist and integration audit operational
- [ ] **Sprint 2 Complete:** Coaching feedback synthesis available
- [ ] **First Execution:** Revisitation triggered after EPIC-072 QA approval

## Progress Tracking

### Sprint Summary

| Sprint | Status | Points | Stories | Completed | In Progress | Blocked |
|--------|--------|--------|---------|-----------|-------------|---------|
| Sprint 1 | Not Started | 5 | 4 | 0 | 0 | 0 |
| Sprint 2 | Not Started | 1 | 1 | 0 | 0 | 0 |
| **Total** | **0%** | **6** | **5** | **0** | **0** | **0** |

## Source Documents

- **Brainstorm:** `devforgeai/specs/brainstorms/BRAINSTORM-011-business-skills-framework.brainstorm.md`
- **Requirements:** `devforgeai/specs/requirements/business-skills-framework-requirements.md`
- **Plan:** `/home/bryan/.claude/plans/jiggly-launching-backus.md`

---

**Epic Template Version:** 1.0
**Last Updated:** 2026-02-21
