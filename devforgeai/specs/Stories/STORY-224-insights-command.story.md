---
id: STORY-224
title: Create /insights Command with Query Routing
type: feature
epic: EPIC-034
sprint: Backlog
status: QA Approved
points: 3
depends_on: ["STORY-221"]
priority: High
assigned_to: TBD
created: 2025-01-02
format_version: "2.5"
---

# Story: Create /insights Command with Query Routing

## Description

**As a** Developer using DevForgeAI,
**I want** to execute insights queries via `/insights` command,
**so that** I can discover workflow patterns, errors, and decisions on-demand.

**Context:**
This is the user interface for EPIC-034 (Session Data Mining). The command routes queries to the devforgeai-insights skill which orchestrates the session-miner subagent.

## Acceptance Criteria

### AC#1: Command Parameter Support

**Given** the /insights command is invoked,
**When** parameters are provided,
**Then** the following query types are supported:
- `/insights` (dashboard overview)
- `/insights workflows` (pattern analysis)
- `/insights errors` (error mining)
- `/insights decisions [query]` (archive search)
- `/insights story STORY-XXX` (story-specific)

---

### AC#2: Query Routing to Skill

**Given** a valid query type,
**When** the command processes the request,
**Then** it invokes `devforgeai-insights` skill with appropriate parameters.

---

### AC#3: Help Documentation

**Given** the user runs `/insights --help`,
**When** help is displayed,
**Then** all query types, parameters, and examples are shown.

---

### AC#4: Error Handling

**Given** an invalid query type,
**When** the command processes the request,
**Then** a clear error message with valid options is displayed.

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Command"
      name: "insights"
      file_path: ".claude/commands/insights.md"
      interface: "Slash command"
      requirements:
        - id: "CMD-001"
          description: "Parse $ARGUMENTS for query type and parameters"
          testable: true
          priority: "Critical"
        - id: "CMD-002"
          description: "Route to devforgeai-insights skill"
          testable: true
          priority: "Critical"
        - id: "CMD-003"
          description: "Display help with --help flag"
          testable: true
          priority: "High"

  non_functional_requirements:
    - id: "NFR-CMD-001"
      category: "Performance"
      requirement: "Command initialization <2 seconds"
      metric: "<2 seconds to skill invocation"
      priority: "High"
```

---

## Definition of Done

### Implementation
- [x] Command file created at .claude/commands/insights.md
- [x] YAML frontmatter with description and argument-hint
- [x] Query type parsing logic
- [x] Skill invocation pattern
- [x] Help text

### Quality
- [x] All 4 acceptance criteria verified
- [x] Command under 500 lines (274 lines)

### Testing
- [x] Test each query type
- [x] Test help display
- [x] Test error handling

### Documentation
- [x] Command usage documented (Help section lines 156-205)
- [x] Examples provided (Quick Reference lines 16-36)

---

## Implementation Notes

- [x] Command file created at .claude/commands/insights.md - Completed: 274 lines, all 25 tests passing
- [x] YAML frontmatter with description and argument-hint - Completed: description, argument-hint, model, allowed-tools
- [x] Query type parsing logic - Completed: Supports dashboard, workflows, errors, decisions, story query types
- [x] Skill invocation pattern - Completed: Routes to devforgeai-insights skill (STORY-221 dependency)
- [x] Help text - Completed: Comprehensive help section (lines 156-205)
- [x] All 4 acceptance criteria verified - Completed: 25/25 tests passing
- [x] Command under 500 lines - Completed: 274 lines
- [x] Test each query type - Completed: Tests 8-13 in test suite
- [x] Test help display - Completed: Tests 17-20 in test suite
- [x] Test error handling - Completed: Tests 21-24 in test suite
- [x] Command usage documented - Completed: Help section lines 156-205
- [x] Examples provided - Completed: Quick Reference lines 16-36

---

## Change Log

**Current Status:** Dev Complete

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2025-01-02 | claude/story-creation-skill | Created | Story created for EPIC-034 Feature 2 | STORY-224-insights-command.story.md |
| 2025-01-03 | claude/test-automator | Red (Phase 02) | 25 tests generated for all 4 ACs + 3 CMD requirements | tests/STORY-224/test-insights-command.sh |
| 2025-01-03 | claude/backend-architect | Green (Phase 03) | Command implemented, all 25 tests passing | .claude/commands/insights.md |
| 2025-01-03 | claude/refactoring-specialist | Refactor (Phase 04) | Code reviewed: CLEAN - no refactoring needed | .claude/commands/insights.md |
| 2025-01-04 | claude/integration-tester | QA Light | Passed: Integration validation (25/25 tests), 0 violations | STORY-224-integration-test-report.md |
