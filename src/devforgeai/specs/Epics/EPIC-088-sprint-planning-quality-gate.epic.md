---
id: EPIC-088
title: Sprint Planning Quality Gate (Gate 0S)
status: Planning
start_date: 2026-03-22
target_date: 2026-04-19
total_points: 16
completed_points: 0
created: 2026-03-22
owner: Project Owner
tech_lead: DevForgeAI AI Agent
team: DevForgeAI
---

# Epic: Sprint Planning Quality Gate (Gate 0S)

## Business Goal

Close the quality gate gap between epic-level planning and sprint-level execution. The DevForgeAI framework has 4 quality gates (Gates 1-4) covering Architecture through Release, but zero gates covering the Planning-to-Sprint transition. Sprint creation (Phase 03S) currently validates only story existence, Backlog status, and capacity range (20-40 points). This allows sprints to be created with unresolved dependencies, circular blocking, file conflicts between parallel stories, incomplete functional areas, and multi-sprint assignment. Gate 0S validates dependency chains, file overlaps, and feature cohesion before sprint commitment, preventing defective sprints from entering the development pipeline.

## Success Metrics

- **Metric 1:** Zero sprints created with unresolved blocking dependencies (from current: no validation)
- **Metric 2:** Zero sprints created with stories already assigned to another sprint (from current: no check)
- **Metric 3:** File overlap warnings surfaced during sprint planning for 100% of overlapping stories (from current: only surfaced during /dev)
- **Metric 4:** Feature cohesion warnings for 100% of partial feature sets when epic Target Sprints section exists (from current: no check)

**Measurement Plan:**
- Tracked via sprint planning Phase 03S execution logs
- Baseline: No pre-sprint validation exists
- Target: All 4 Gate 0S checks execute on every sprint creation
- Review: After each sprint creation

## Scope

### In Scope

1. **Feature 1: Gate 0S ADR and Quality Gates Reference**
   - Create ADR-046 establishing Gate 0S as a new quality gate
   - Add Gate 0S to quality-gates.md reference document
   - Update quality-gates rule summary
   - Business value: Establishes architectural foundation for sprint validation

2. **Feature 2: Sprint Dependency Chain Validation**
   - Invoke dependency-graph-analyzer during Phase 03S Step 2.5
   - Validate all depends_on references resolve to in-sprint or completed stories
   - Detect circular dependencies via DFS
   - Business value: Prevents blocked stories from entering sprints

3. **Feature 3: Sprint File Overlap Detection**
   - Invoke file-overlap-detector during Phase 03S Step 2.6 in pre-flight mode
   - Detect stories modifying the same files
   - Recommend execution order based on dependency and overlap analysis
   - Business value: Reduces merge conflicts and parallel development hazards

4. **Feature 4: Feature Cohesion Validation + Multi-Sprint Assignment Check**
   - Parse epic Target Sprints section for feature-to-story mapping
   - Detect partial feature shipments (incomplete functional areas)
   - Prevent stories already assigned to another sprint from being re-assigned
   - Business value: Prevents incomplete feature releases and duplicate sprint assignment

### Out of Scope

- Sprint Goal concept (future enhancement, documented in plan)
- Velocity-based capacity planning (future enhancement, documented in plan)
- MVP slice identification (future enhancement, documented in plan)
- Brainstorm-to-ideation pipeline gates (future epic, documented in plan)
- Ideation-to-epic pipeline gates (future epic, documented in plan)
- Modifications to dependency-graph-analyzer or file-overlap-detector agents (reused as-is via prompt)

## Target Sprints

### Sprint 1: Foundation + Dependency Validation
**Goal:** Establish ADR-046 and implement dependency chain validation in Phase 03S
**Estimated Points:** 8
**Features:**
- Feature 1: Gate 0S ADR and quality gates reference (STORY-A, 3 pts)
- Feature 2: Sprint dependency chain validation (STORY-B, 5 pts)

**Key Deliverables:**
- ADR-046 accepted at devforgeai/specs/adrs/
- Gate 0S documented in quality-gates.md
- Step 2.5 (Dependency Chain Validation) functional in Phase 03S

### Sprint 2: Overlap Detection + Feature Cohesion
**Goal:** Complete all Gate 0S checks with file overlap detection and feature cohesion validation
**Estimated Points:** 8
**Features:**
- Feature 3: Sprint file overlap detection (STORY-C, 5 pts)
- Feature 4: Feature cohesion + multi-sprint check (STORY-D, 3 pts)

**Key Deliverables:**
- Step 2.6 (File Overlap Detection) functional in Phase 03S
- Step 2.7 (Feature Cohesion + Multi-Sprint) functional in Phase 03S
- Gate 0S fully operational

## User Stories

1. **As a** framework user, **I want** sprint planning to validate dependency chains, **so that** sprints are not created with unresolvable blocking dependencies
2. **As a** framework user, **I want** sprint planning to detect file overlaps between stories, **so that** I can sequence parallel development to avoid merge conflicts
3. **As a** framework user, **I want** sprint planning to warn about partial feature sets, **so that** I don't inadvertently ship incomplete functional areas
4. **As a** framework user, **I want** sprint planning to block multi-sprint story assignment, **so that** stories cannot be accidentally added to multiple sprints

## Technical Considerations

### Architecture Impact
- No new services or components needed
- Enhances existing Phase 03S with 3 new steps (2.5, 2.6, 2.7)
- Reuses existing subagents: dependency-graph-analyzer, file-overlap-detector
- No data model changes

### Technology Decisions
- No new technologies required (uses existing Read, Grep, Task, AskUserQuestion tools)
- No library additions needed
- All validation logic expressible in markdown section parsing + YAML frontmatter extraction

### Security & Compliance
- No security implications (read-only validation gate)
- No sensitive data exposure

### Performance Requirements
- Gate 0S adds ~20-30 seconds to sprint creation (2 subagent invocations)
- Acceptable for a planning-time operation (not runtime-critical)

## Decision Context

### Design Rationale

Gate 0S is positioned between Step 2 (Validate Selected Stories) and Step 3 (Calculate Capacity) in Phase 03S because:
1. Story files must be validated as existing and in Backlog status before dependency/overlap analysis can proceed (Step 2 provides this)
2. Capacity calculation (Step 3) is meaningless if stories will be removed due to dependency failures
3. Sprint document generation (Step 4) should incorporate overlap recommendations

### Rejected Alternatives

1. **Modifying dependency-graph-analyzer agent** — Rejected because the agent is prompt-driven and already handles all needed validation. Sprint selection list context is passed via prompt text, requiring no agent code changes.
2. **Creating a new sprint-validator agent** — Rejected because it would duplicate existing agent capabilities. Reusing dependency-graph-analyzer and file-overlap-detector follows the Single Responsibility Principle.
3. **Post-sprint validation (validating after sprint creation)** — Rejected because fixing a defective sprint after creation requires story reassignment, which is more disruptive than preventing the defect.

### Implementation Constraints

- Must not break existing sprint creation workflow (stories with no deps and no overlaps must pass transparently)
- Must follow Three-Layer Architecture (Commands > Skills > Subagents)
- Must follow Execute-Verify-Record pattern for each new step
- Feature cohesion check depends on epic Target Sprints section format — must gracefully skip for epics without this section

### Key Insights from Discovery

- RESEARCH-002 documents that corporate Agile frameworks (SAFe, LeSS, Scrum@Scale) validate dependency chains and feature cohesion before sprint commitment
- dependency-graph-analyzer and file-overlap-detector already exist and are only invoked during /dev Phase 01 (too late)
- Epic template Target Sprints section contains feature-to-story mapping that is never read by /create-sprint
- The gap-detector.sh script (Strategy 2) already parses epic Stories tables using the same Grep patterns needed for Target Sprints parsing

## Dependencies

### Internal Dependencies
- [x] **ADR-046:** Sprint Planning Quality Gate — Created 2026-03-22
  - **Status:** Accepted
  - **Impact if delayed:** Cannot proceed with Gate 0S implementation

### External Dependencies
- None

## Risks & Mitigation

### Risk 1: Epic Target Sprints format varies across epics
- **Probability:** Medium
- **Impact:** Low
- **Mitigation:** Use `STORY-\d+` regex pattern to extract story IDs regardless of prose format. Same technique as gap-detector.sh Strategy 2.
- **Contingency:** Feature cohesion check gracefully skips with info message if parsing fails

### Risk 2: file-overlap-detector filters by "In Development" status
- **Probability:** High
- **Impact:** Low
- **Mitigation:** Pass explicit instruction in prompt to analyze provided list rather than filtering by status
- **Contingency:** If agent doesn't support pre-flight mode, fall back to direct file_path extraction via Grep

### Risk 3: Multi-epic sprints have no single Target Sprints section
- **Probability:** Medium
- **Impact:** Low
- **Mitigation:** Feature cohesion check skips when EPIC_ID is "Multiple" or not set
- **Contingency:** Accept INFO-level skip message

## Stakeholders

### Primary Stakeholders
- **Product Owner:** Bryan — Decision authority on gate strictness and bypass policies
- **Tech Lead:** DevForgeAI AI Agent — Implementation and testing

## Timeline

```
Epic Timeline:
════════════════════════════════════════════════════
Week 1-2:  Sprint 1 — ADR + Dependency Validation
Week 3-4:  Sprint 2 — File Overlap + Feature Cohesion
════════════════════════════════════════════════════
Total Duration: 4 weeks
Target Completion: 2026-04-19
```

### Key Milestones
- [ ] **Milestone 1:** 2026-03-29 — ADR-046 accepted, Gate 0S documented in quality-gates.md
- [ ] **Milestone 2:** 2026-04-05 — Dependency chain validation operational (Step 2.5)
- [ ] **Milestone 3:** 2026-04-12 — File overlap detection operational (Step 2.6)
- [ ] **Final Release:** 2026-04-19 — Gate 0S fully operational (Steps 2.5 + 2.6 + 2.7)

## Progress Tracking

### Sprint Summary

| Sprint | Status | Points | Stories | Completed | In Progress | Blocked |
|--------|--------|--------|---------|-----------|-------------|---------|
| Sprint 1 | Not Started | 8 | 2 | 0 | 0 | 0 |
| Sprint 2 | Not Started | 8 | 2 | 0 | 0 | 0 |
| **Total** | **0%** | **16** | **4** | **0** | **0** | **0** |

### Burndown
- **Total Points:** 16
- **Completed:** 0
- **Remaining:** 16
- **Velocity:** TBD (after first sprint)

## Retrospective (Post-Epic)

*To be completed after epic completes*

---

**Epic Template Version:** 1.0
**Last Updated:** 2026-03-22
**Research Reference:** RESEARCH-002 (devforgeai/specs/research/shared/RESEARCH-002-epic-vs-sprint-sdlc-relationship.md)
**ADR Reference:** ADR-046 (devforgeai/specs/adrs/ADR-046-sprint-planning-quality-gate.md)
**Plan Reference:** /home/bryan/.claude/plans/delightful-bubbling-puzzle.md
