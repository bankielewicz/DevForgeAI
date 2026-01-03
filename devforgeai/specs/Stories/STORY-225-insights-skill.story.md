---
id: STORY-225
title: Implement devforgeai-insights Skill for Mining Orchestration
type: feature
epic: EPIC-034
sprint: Backlog
status: Backlog
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
- [ ] Skill directory created at .claude/skills/devforgeai-insights/
- [ ] SKILL.md with phases (Argument Parsing, Subagent Invocation, Result Aggregation, User Display)
- [ ] Subagent invocation patterns
- [ ] Output formatting templates
- [ ] Cache mechanism documented

### Quality
- [ ] All 4 acceptance criteria verified
- [ ] Skill under 1000 lines
- [ ] Progressive disclosure with references/

### Testing
- [ ] Test each query mode
- [ ] Test subagent invocation
- [ ] Test caching behavior

### Documentation
- [ ] Skill phases documented
- [ ] Output formats documented

---

## Implementation Notes

*Pending implementation*

---

## Change Log

**Current Status:** Backlog

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2025-01-02 | claude/story-creation-skill | Created | Story created for EPIC-034 Feature 2 | STORY-225-insights-skill.story.md |
