---
id: SPRINT-13
name: EPIC-064 Code Smell Detection Gap Closure
epic: EPIC-064
start_date: 2026-02-14
end_date: 2026-02-28
duration_days: 14
status: Active
total_points: 34
completed_points: 0
stories:
  - STORY-399
  - STORY-400
  - STORY-401
  - STORY-402
  - STORY-403
  - STORY-404
  - STORY-405
  - STORY-406
  - STORY-407
created: 2026-02-13
---

# Sprint 13: EPIC-064 Code Smell Detection Gap Closure

## Overview

**Duration:** 2026-02-14 to 2026-02-28 (14 days / 2 weeks)
**Capacity:** 31 story points
**Epic:** EPIC-064 (AI-Generated Code Smell Detection Gap Closure)
**Status:** Active

This sprint delivers 8 new code smell detections, expanding DevForgeAI's automated smell detection from 3 types to 11 types (+267%). The work spans 4 features: Tier 1 Quick Wins (anti-pattern-scanner Phase 5 extensions), Dead Code Detector (new subagent), Placeholder Detection (code-reviewer Section 8.5), and Tier 2 Detections (middle man, message chains). All detections use the proven EPIC-060/061/062 methodology — Treelint AST analysis, two-stage filtering (PE-060), and confidence scoring (PE-059).

## Sprint Goals

### Primary Goals

1. **Tier 1 Quick Wins** — Add 4 new smell detections to anti-pattern-scanner Phase 5: Data Class, Long Parameter List, Commented-Out Code, Orphaned Imports (13 pts)
2. **Dead Code Detector** — Create new subagent with Treelint call-graph analysis and entry point exclusion (8 pts)
3. **Placeholder Detection** — Extend code-reviewer Section 8 with Section 8.5 for incomplete code detection (5 pts)
4. **Tier 2 Detections** — Add Middle Man and Message Chain detection to anti-pattern-scanner Phase 5 (5 pts)

### Success Metrics

- All 8 stories completed and QA approved
- anti-pattern-scanner detects 11 smell types (up from 3)
- False positive rate < 15% for two-stage filtered detections
- Zero regressions on existing 3 smell detections (God Object, Long Method, Magic Numbers)
- dead-code-detector baseline composite score >= 4.0
- ADR-016 documented for dead-code-detector read-only constraint

## Stories

### Feature 1: Anti-Pattern-Scanner Tier 1 Quick Wins (13 points)

#### STORY-399: Add Data Class Detection to Anti-Pattern-Scanner
- **Points:** 3
- **Priority:** High
- **Epic:** EPIC-064
- **Dependencies:** None
- **Status:** Ready for Dev
- **Description:** Detect classes with properties but no behavior using Treelint AST enumeration with two-stage filtering (PE-060). Threshold: method_count < 3 AND property_count > 2.

#### STORY-400: Add Long Parameter List Detection to Anti-Pattern-Scanner
- **Points:** 2
- **Priority:** High
- **Epic:** EPIC-064
- **Dependencies:** None
- **Status:** Ready for Dev
- **Description:** Detect functions with > 4 parameters (excluding self/cls/*args/**kwargs) using Treelint function signature analysis. No two-stage filtering needed.

#### STORY-401: Add Commented-Out Code Detection to Anti-Pattern-Scanner
- **Points:** 5
- **Priority:** High
- **Epic:** EPIC-064
- **Dependencies:** None
- **Status:** Ready for Dev
- **Description:** Detect commented-out code blocks using two-stage filtering. Stage 1: Grep patterns for Python/TS/JS commented code. Stage 2: LLM with chain-of-thought (PE-005) to distinguish from documentation examples.

#### STORY-402: Add Orphaned Import Detection to Anti-Pattern-Scanner
- **Points:** 3
- **Priority:** High
- **Epic:** EPIC-064
- **Dependencies:** None
- **Status:** Ready for Dev
- **Description:** Detect unused imports by extracting symbols and searching same file for usage. Handles wildcards, re-exports, side-effect imports, type-only imports, and Python __all__.

### Feature 2: Dead Code Detector Subagent (8 points)

#### STORY-403: Create Dead-Code-Detector Subagent
- **Points:** 8
- **Priority:** High
- **Epic:** EPIC-064
- **Dependencies:** None
- **Status:** Ready for Dev
- **Description:** New Layer 2 read-only subagent with 10-element canonical template and 4-phase workflow: Context Loading → Function Discovery → Dependency Analysis → Entry Point Exclusion. ADR-016 for read-only constraint.

### Feature 3: Code-Reviewer Placeholder Detection (5 points)

#### STORY-404: Extend Anti-Gaming with Placeholder/Incomplete Code Detection
- **Points:** 5
- **Priority:** High
- **Epic:** EPIC-064
- **Dependencies:** None
- **Status:** Ready for Dev
- **Description:** Add Section 8.5 to code-reviewer for placeholder detection (pass, return null, NotImplementedError) with two-stage filtering. Excludes test directories. Severity HIGH.

### Feature 4: Anti-Pattern-Scanner Tier 2 (5 points)

#### STORY-405: Add Middle Man Detection to Anti-Pattern-Scanner
- **Points:** 3
- **Priority:** High
- **Epic:** EPIC-064
- **Dependencies:** None
- **Status:** Ready for Dev
- **Description:** Detect classes where > 80% of methods are single-line delegations (body <= 2 lines). Minimum 3 methods to prevent false positives on small utility classes.

#### STORY-406: Add Message Chain Detection to Anti-Pattern-Scanner
- **Points:** 2
- **Priority:** High
- **Epic:** EPIC-064
- **Dependencies:** None
- **Status:** Ready for Dev
- **Description:** Detect 3+ chained method calls (Law of Demeter violations) with two-stage filtering. Suppress builder patterns, promise chains, fluent APIs, jQuery chains.

## Sprint Metrics

- **Planned Velocity:** 34 points
- **Current Velocity:** 0 points (0%)
- **Stories Planned:** 8
- **Stories Completed:** 0
- **Days Remaining:** 14
- **Burn-down Status:** Not started (sprint Active)

## Capacity Analysis

**Capacity:** 34 points for 2-week sprint
- **Status:** Within optimal range (20-40 points)
- **Points/Day:** 31 / 14 = 2.21 points/day, within sustainable range
- **Story Size Mix:**
  - 2-point stories: 2 (25%) — STORY-400, STORY-406
  - 3-point stories: 3 (37.5%) — STORY-399, STORY-402, STORY-405
  - 5-point stories: 2 (25%) — STORY-401, STORY-404
  - 8-point stories: 1 (12.5%) — STORY-403
  - Total: Well-balanced distribution

**Priority Distribution:**
- **High Priority:** 8 stories (31 points) — all stories are high priority

**Risk Assessment:**
- **Largest Story:** STORY-403 (8 points, dead-code-detector subagent) — schedule mid-sprint for risk mitigation
- **Two-Stage Filter Stories:** STORY-399, STORY-401, STORY-404, STORY-406 share the two-stage filtering pattern — create reference file in STORY-401 first, then reuse
- **Parallel Tracks:** All stories are independent (no blocking dependencies)
- **Key Deliverable:** `.claude/agents/anti-pattern-scanner/references/two-stage-filter-patterns.md` created in STORY-401, used by STORY-399, STORY-404, STORY-406

## Development Strategy

### Recommended Execution Order

**Week 1 (Feb 14-21): Tier 1 Quick Wins + Foundation**
1. `/dev STORY-401` — Commented-Out Code (5 pts) — **START HERE**: Creates two-stage-filter-patterns.md reference file used by 3 other stories
2. `/dev STORY-399` — Data Class Detection (3 pts) — Uses two-stage filter reference
3. `/dev STORY-400` — Long Parameter List (2 pts) — Simple, fast win
4. `/dev STORY-402` — Orphaned Imports (3 pts) — Completes Tier 1

**Week 2 (Feb 22-28): Dead Code + Placeholder + Tier 2**
5. `/dev STORY-403` — Dead Code Detector (8 pts) — Largest story, new subagent
6. `/dev STORY-404` — Placeholder Detection (5 pts) — Uses two-stage filter reference
7. `/dev STORY-405` — Middle Man Detection (3 pts) — Tier 2
8. `/dev STORY-406` — Message Chain Detection (2 pts) — Uses two-stage filter reference

### Parallel Opportunities
- STORY-400 and STORY-402 can run in parallel (no shared dependencies)
- STORY-405 and STORY-406 can run in parallel (independent Tier 2 detections)
- STORY-403 and STORY-404 can run in parallel (different agents: dead-code-detector vs code-reviewer)

### Key Dependencies
- STORY-401 should be completed before STORY-399, STORY-404, STORY-406 (creates shared two-stage-filter-patterns.md reference)
- No external dependencies

## Retrospective Notes

*To be filled at sprint end*

### What Went Well
- [To be documented]

### What Could Be Improved
- [To be documented]

### Velocity Analysis
- Planned: 31 points
- Completed: [To be calculated]
- Variance: [+/- points]

### Action Items for Next Sprint
- [To be documented]
- Consider: STORY-407 (Documentation/ADR) for Sprint-14

## Next Steps

1. Review sprint goals and execution order
2. Start first story: `/dev STORY-401` (creates two-stage filter foundation)
3. Track progress daily
4. After Tier 1 complete, evaluate before proceeding to Tier 2
5. Complete sprint with: `/close-sprint`
