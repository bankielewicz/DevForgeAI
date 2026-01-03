---
id: STORY-222
title: Extract Plan File Knowledge Base for Decision Archive
type: feature
epic: EPIC-034
sprint: Backlog
status: Backlog
points: 3
depends_on: ["STORY-221"]
priority: High
assigned_to: TBD
created: 2025-01-02
format_version: "2.5"
---

# Story: Extract Plan File Knowledge Base for Decision Archive

## Description

**As a** Framework Intelligence System,
**I want** to mine decision context from .claude/plans/*.md files,
**so that** developers can search past architectural decisions and learn from historical approaches.

**Context:**
The project contains 350+ plan files with embedded decision rationales. This story extracts structured knowledge to build a searchable decision archive.

## Acceptance Criteria

### AC#1: YAML Frontmatter Parsing

**Given** a plan file with YAML frontmatter,
**When** the session-miner extracts metadata,
**Then** status, created, author, and related_stories fields are parsed.

---

### AC#2: Story ID Pattern Extraction

**Given** a plan file containing story references,
**When** the session-miner scans content,
**Then** all STORY-NNN patterns are extracted with surrounding context.

---

### AC#3: Decision Archive Mapping

**Given** extracted plan file data,
**When** building the decision archive,
**Then** a bidirectional story→decision mapping is created.

---

### AC#4: Cross-Reference Support

**Given** a story ID query,
**When** searching the decision archive,
**Then** all related plan files are returned with decision context.

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Subagent"
      name: "session-miner"
      file_path: ".claude/agents/session-miner.md"
      requirements:
        - id: "SM-010"
          description: "Parse YAML frontmatter from plan files"
          testable: true
          priority: "Critical"
        - id: "SM-011"
          description: "Extract STORY-NNN patterns with regex"
          testable: true
          priority: "High"
        - id: "SM-012"
          description: "Build story→decision bidirectional mapping"
          testable: true
          priority: "High"

    - type: "DataModel"
      name: "DecisionArchive"
      purpose: "Bidirectional mapping of stories to plans"
      fields:
        - name: "story_to_plans"
          type: "Map<String, String[]>"
        - name: "plan_to_stories"
          type: "Map<String, String[]>"

  non_functional_requirements:
    - id: "NFR-010"
      category: "Performance"
      requirement: "Index 350+ plan files within 10 seconds"
      metric: "<10 seconds for full index"
      priority: "High"
```

---

## Definition of Done

### Implementation
- [ ] Plan file parsing logic added to session-miner
- [ ] YAML frontmatter extraction documented
- [ ] Story ID regex pattern documented
- [ ] Decision archive data structures defined

### Quality
- [ ] All 4 acceptance criteria verified
- [ ] Edge cases covered (malformed YAML, missing sections)
- [ ] Performance target met (<10 seconds)

### Testing
- [ ] Test frontmatter parsing
- [ ] Test story ID extraction
- [ ] Integration test with real plan files

### Documentation
- [ ] Query interface documented
- [ ] Output schema documented

---

## Implementation Notes

*Pending implementation*

---

## Change Log

**Current Status:** Backlog

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2025-01-02 | claude/story-creation-skill | Created | Story created for EPIC-034 Feature 1 | STORY-222-plan-file-knowledge-base.story.md |
