---
id: STORY-225
title: Implement devforgeai-insights Skill for Mining Orchestration
type: feature
epic: EPIC-034
sprint: Backlog
status: QA Approved
points: 5
depends_on: ["STORY-221", "STORY-222", "STORY-223"]
priority: High
assigned_to: TBD
created: 2025-01-02
format_version: "2.5"
---

# Story: Implement devforgeai-insights Skill for Mining Orchestration

## Description

**As a** DevForgeAI Framework,
**I want** a skill that orchestrates session data mining operations,
**so that** the /insights command can deliver formatted, actionable insights.

**Context:**
This is the orchestration layer for EPIC-034. The skill coordinates the session-miner subagent, aggregates results, formats output, and manages caching for frequently accessed patterns.

## Acceptance Criteria

### AC#1: Subagent Orchestration

**Given** a query request from /insights command,
**When** the skill processes the query,
**Then** it invokes session-miner subagent with appropriate prompts.

---

### AC#2: Result Aggregation

**Given** raw data from session-miner,
**When** the skill processes results,
**Then** data is aggregated, filtered, and ranked by relevance.

---

### AC#3: Output Formatting

**Given** aggregated results,
**When** the skill prepares output,
**Then** results are formatted as user-friendly markdown with tables, summaries, and recommendations.

---

### AC#4: Result Caching

**Given** a query that was recently executed,
**When** the same query is requested within 1 hour,
**Then** cached results are returned without re-mining.

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Skill"
      name: "devforgeai-insights"
      file_path: ".claude/skills/devforgeai-insights/SKILL.md"
      interface: "Skill invocation"
      requirements:
        - id: "SKL-001"
          description: "Invoke session-miner subagent via Task tool"
          testable: true
          priority: "Critical"
        - id: "SKL-002"
          description: "Aggregate and filter results"
          testable: true
          priority: "High"
        - id: "SKL-003"
          description: "Format output as markdown"
          testable: true
          priority: "High"
        - id: "SKL-004"
          description: "Cache results with 1-hour TTL"
          testable: true
          priority: "Medium"

  non_functional_requirements:
    - id: "NFR-SKL-001"
      category: "Performance"
      requirement: "Query execution <10 seconds (cached)"
      metric: "<10 seconds for cached queries"
      priority: "High"
    - id: "NFR-SKL-002"
      category: "Performance"
      requirement: "Skill under 1000 lines"
      metric: "<1000 lines SKILL.md"
      priority: "High"
```

---

## Definition of Done

### Implementation
- [x] Skill directory created at .claude/skills/devforgeai-insights/
- [x] SKILL.md with phases (Argument Parsing, Subagent Invocation, Result Aggregation, User Display)
- [x] Subagent invocation patterns
- [x] Output formatting templates
- [x] Cache mechanism documented

### Quality
- [x] All 4 acceptance criteria verified
- [x] Skill under 1000 lines
- [x] Progressive disclosure with references/ (N/A: skill is 388 lines, under threshold)

### Testing
- [x] Test each query mode
- [x] Test subagent invocation
- [x] Test caching behavior

### Documentation
- [x] Skill phases documented
- [x] Output formats documented

---

## Implementation Notes

- [x] Skill directory created at .claude/skills/devforgeai-insights/ - Completed: directory created with SKILL.md
- [x] SKILL.md with phases (Argument Parsing, Subagent Invocation, Result Aggregation, User Display) - Completed: 4-phase workflow implemented
- [x] Subagent invocation patterns - Completed: Task() patterns for session-miner with 5 query types
- [x] Output formatting templates - Completed: markdown tables, summaries, recommendations for all query types
- [x] Cache mechanism documented - Completed: 1-hour TTL cache with hit/miss behavior
- [x] All 4 acceptance criteria verified - Completed: 66 tests passing across 5 test suites
- [x] Skill under 1000 lines - Completed: 388 lines (within 500-800 target)
- [x] Progressive disclosure with references/ - N/A: skill is 388 lines, under threshold (User approved: 2026-01-04)
- [x] Test each query mode - Completed: test-ac1 covers all 5 query types
- [x] Test subagent invocation - Completed: test-ac1 validates Task() patterns
- [x] Test caching behavior - Completed: test-ac4 validates 1-hour TTL cache
- [x] Skill phases documented - Completed: Phase 1-4 documented in SKILL.md
- [x] Output formats documented - Completed: Output Templates section in SKILL.md

**Developer:** claude/opus
**Implemented:** 2026-01-04

### TDD Workflow Summary
- **Red Phase:** 66 tests generated across 5 test suites (test-ac1 through test-ac4 + test-nfr)
- **Green Phase:** SKILL.md implemented to pass all tests
- **Refactor Phase:** Reduced from 481 to 388 lines (19% reduction) via DRY consolidation
- **Integration Phase:** Validated integration with /insights command and session-miner subagent

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2025-01-02 | claude/story-creation-skill | Created | Story created for EPIC-034 Feature 2 | STORY-225-insights-skill.story.md |
| 2026-01-04 | claude/opus | Dev Complete | Implemented devforgeai-insights skill with 4-phase workflow, 66 tests passing | .claude/skills/devforgeai-insights/SKILL.md, tests/STORY-225/*.sh |
| 2026-01-04 | claude/qa-result-interpreter | QA Deep | Passed: Coverage 100%, 0 violations, 66 tests passing | devforgeai/qa/reports/STORY-225-qa-report.md |
