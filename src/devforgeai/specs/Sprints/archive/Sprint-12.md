---
id: SPRINT-12
name: Treelint Advanced Features & Validation Rollout
epic: Multiple (EPIC-058, EPIC-059)
start_date: 2026-02-09
end_date: 2026-03-02
duration_days: 21
status: Active
total_points: 47
completed_points: 0
stories:
  - STORY-370
  - STORY-371
  - STORY-372
  - STORY-373
  - STORY-374
  - STORY-375
  - STORY-376
  - STORY-377
  - STORY-378
  - STORY-379
created: 2026-02-06
---

# Sprint 12: Treelint Advanced Features & Validation Rollout

## Overview

**Duration:** 2026-02-09 to 2026-03-02 (21 days / 3 weeks)
**Capacity:** 47 story points
**Epics:** EPIC-058 (Treelint Advanced Features) + EPIC-059 (Treelint Validation & Rollout)
**Status:** Active

This is a cross-epic sprint that delivers the remaining Treelint advanced features (dependency graph, code quality metrics, test coverage mapping, repository map, daemon auto-start) and validates the entire Treelint integration initiative with token measurement, integration testing, skill updates, and user documentation. Completing this sprint finalizes EPIC-058 and EPIC-059, concluding the Treelint AST-aware code search integration initiative (EPIC-055 through EPIC-059).

## Sprint Goals

### Primary Goals

1. **EPIC-058 Completion** - Deliver all 5 advanced Treelint features: dependency graph analysis, code quality metrics extraction, semantic test coverage mapping, repository map generation, and daemon auto-start logic
2. **Token Reduction Validation** - Build and execute the token measurement framework to validate the claimed 40-80% token reduction with quantified evidence (STORY-375)
3. **Integration Test Confidence** - Create comprehensive integration test suite covering all 7 updated subagents, hybrid fallback logic, advanced features, and error scenarios (STORY-376)
4. **Skill Integration** - Update devforgeai-development and devforgeai-qa skills with Treelint context for TDD and QA workflows (STORY-377, STORY-378)
5. **User Documentation** - Create comprehensive Treelint user documentation and troubleshooting guide (STORY-379)

### Success Metrics

- All 10 stories completed and QA approved
- Token reduction validated >= 40% in controlled workflow tests
- Integration test suite passing with 100% success rate
- devforgeai-development and devforgeai-qa skills updated with Treelint context
- User documentation complete with troubleshooting guide
- Zero workflow regressions (existing functionality preserved)

## Stories

### EPIC-058: Treelint Advanced Features (25 points)

#### STORY-370: Integrate Dependency Graph Analysis via Treelint deps
- **Points:** 5
- **Priority:** High
- **Epic:** EPIC-058
- **Dependencies:** None
- **Status:** Ready for Dev
- **Description:** Query function call relationships via `treelint deps --calls` for impact analysis in refactoring-specialist and code-reviewer subagents. 3-tier fallback: daemon -> CLI -> Grep.

#### STORY-371: Implement Code Quality Metrics Extraction via Treelint AST
- **Points:** 5
- **Priority:** High
- **Epic:** EPIC-058
- **Dependencies:** None
- **Status:** Ready for Dev
- **Description:** Extract function length, nesting depth, and cyclomatic complexity from Treelint AST for code-quality-auditor. Supplements (not replaces) existing language-specific tools.

#### STORY-372: Implement Semantic Test Coverage Mapping via Treelint
- **Points:** 5
- **Priority:** High
- **Epic:** EPIC-058
- **Dependencies:** None
- **Status:** Ready for Dev
- **Description:** Semantically correlate test functions with source functions using Treelint AST search and naming convention pattern matching for function-level coverage gap identification.

#### STORY-373: Integrate Repository Map Generation via Treelint map
- **Points:** 5
- **Priority:** Medium
- **Epic:** EPIC-058
- **Dependencies:** None
- **Status:** Ready for Dev
- **Description:** Query ranked codebase symbol map via `treelint map --ranked` for context-efficient brownfield analysis in designing-systems skill. Top-N filtering for context window optimization.

#### STORY-374: Implement Daemon Auto-Start Logic for Treelint
- **Points:** 5
- **Priority:** Medium
- **Epic:** EPIC-058
- **Dependencies:** None
- **Status:** Ready for Dev
- **Description:** Detect when Treelint daemon is stopped and offer to start it via AskUserQuestion (user-managed lifecycle). Stale PID cleanup, session-level "don't ask again" suppression.

### EPIC-059: Treelint Validation & Rollout (22 points)

#### STORY-375: Build Token Measurement Framework
- **Points:** 5
- **Priority:** High
- **Epic:** EPIC-059
- **Dependencies:** None
- **Status:** Ready for Dev
- **Description:** Token measurement framework comparing Grep-only vs Treelint-enabled workflows with minimum 5 standardized test queries. Validates 40-80% token reduction claim with quantified evidence.

#### STORY-376: Create Integration Test Suite for Treelint
- **Points:** 8
- **Priority:** High
- **Epic:** EPIC-059
- **Dependencies:** None
- **Status:** Ready for Dev
- **Description:** Comprehensive integration test suite validating all 7 Treelint-enabled subagents, hybrid fallback logic, advanced features, error scenarios, and platform compatibility. Largest story in sprint.

#### STORY-377: Update devforgeai-development Skill for Treelint
- **Points:** 3
- **Priority:** High
- **Epic:** EPIC-059
- **Dependencies:** None
- **Status:** Ready for Dev
- **Description:** Add Treelint context notes to TDD Phase 02 (test-automator), Phase 03 (backend-architect), and Phase 04 (refactoring-specialist, code-reviewer) subagent invocations. Additive-only changes.

#### STORY-378: Update devforgeai-qa Skill for Treelint
- **Points:** 3
- **Priority:** Medium
- **Epic:** EPIC-059
- **Dependencies:** None
- **Status:** Ready for Dev
- **Description:** Add Treelint context notes to QA Phase 2 subagent invocations (anti-pattern-scanner, test-automator, code-reviewer, security-auditor, coverage-analyzer). Excludes non-enabled subagents.

#### STORY-379: Create Treelint User Documentation
- **Points:** 3
- **Priority:** Medium
- **Epic:** EPIC-059
- **Dependencies:** None
- **Status:** Ready for Dev
- **Description:** Comprehensive user documentation at docs/guides/treelint-integration-guide.md covering overview, supported languages, fallback behavior, troubleshooting (5+ issues), performance expectations, daemon mode, and installation.

## Sprint Metrics

- **Planned Velocity:** 47 points
- **Current Velocity:** 0 points (0%)
- **Stories Planned:** 10
- **Stories Completed:** 0
- **Days Remaining:** 21
- **Burn-down Status:** Not started (sprint Active)

## Capacity Analysis

**Capacity:** 47 points for 3-week sprint
- **Status:** Over optimal range (47 > 40 for 2-week sprint, but 3-week duration provides adequate buffer)
- **Adjusted Assessment:** 47 points / 21 days = 2.24 points/day, within sustainable range for extended sprint
- **Story Size Mix:**
  - 3-point stories: 3 (30%) - STORY-377, STORY-378, STORY-379
  - 5-point stories: 6 (60%) - STORY-370, STORY-371, STORY-372, STORY-373, STORY-374, STORY-375
  - 8-point stories: 1 (10%) - STORY-376
  - Total: Good size distribution with majority mid-range

**Priority Distribution:**
- **High Priority:** 6 stories (35 points) - STORY-370, STORY-371, STORY-372, STORY-375, STORY-376, STORY-377
- **Medium Priority:** 4 stories (12 points) - STORY-373, STORY-374, STORY-378, STORY-379

**Risk Assessment:**
- **Cross-Epic Coordination:** Stories from EPIC-058 and EPIC-059 are independent; no cross-epic blocking dependencies
- **Largest Story:** STORY-376 (8 points) is the largest; schedule early for risk mitigation
- **Parallel Tracks:** All 10 stories are independent and can run in any order
- **Buffer:** 3-week duration provides 50% more time than standard 2-week sprint

## Development Strategy

### Recommended Execution Order

**Week 1 (Feb 9-15): High Priority - Advanced Features**
1. `/dev STORY-370` - Dependency graph analysis (5 pts, High)
2. `/dev STORY-371` - Code quality metrics (5 pts, High)
3. `/dev STORY-372` - Test coverage mapping (5 pts, High)

**Week 2 (Feb 16-22): High Priority - Validation**
4. `/dev STORY-375` - Token measurement framework (5 pts, High)
5. `/dev STORY-376` - Integration test suite (8 pts, High)
6. `/dev STORY-377` - Development skill update (3 pts, High)

**Week 3 (Feb 23-Mar 2): Medium Priority - Completion**
7. `/dev STORY-373` - Repository map generation (5 pts, Medium)
8. `/dev STORY-374` - Daemon auto-start logic (5 pts, Medium)
9. `/dev STORY-378` - QA skill update (3 pts, Medium)
10. `/dev STORY-379` - User documentation (3 pts, Medium)

### Parallel Opportunities
- STORY-370, STORY-371, STORY-372 can run fully in parallel (independent advanced features)
- STORY-377 and STORY-378 can run in parallel (independent skill updates)
- STORY-373 and STORY-374 can run in parallel (independent advanced features)

## Retrospective Notes

*To be filled at sprint end*

### What Went Well
- [To be documented]

### What Could Be Improved
- [To be documented]

### Velocity Analysis
- Planned: 47 points
- Completed: [To be calculated]
- Variance: [+/- points]

### Action Items for Next Sprint
- [To be documented]

## Next Steps

1. Review sprint goals and story priorities
2. Start first High priority story: `/dev STORY-370`
3. Track progress daily
4. After EPIC-058 stories complete, focus on EPIC-059 validation
5. Complete sprint with: `/close-sprint`
