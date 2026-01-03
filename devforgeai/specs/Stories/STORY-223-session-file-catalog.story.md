---
id: STORY-223
title: Catalog Session File Structure and Relationships
type: feature
epic: EPIC-034
sprint: Backlog
status: Backlog
points: 2
depends_on: ["STORY-221"]
priority: Medium
assigned_to: TBD
created: 2025-01-02
format_version: "2.5"
---

# Story: Catalog Session File Structure and Relationships

## Description

**As a** Framework Intelligence System,
**I want** to inventory session artifacts and their relationships,
**so that** the framework can understand file dependencies and session continuity.

**Context:**
Session data spans multiple file types: plans, todos, sessions, and artifacts. This story maps relationships between these files to enable comprehensive session analysis.

## Acceptance Criteria

### AC#1: Map Plans to Stories to Artifacts

**Given** the session data directories,
**When** the session-miner catalogs files,
**Then** a mapping is created: plan files → story references → associated artifacts.

---

### AC#2: Build File Dependency Graph

**Given** the cataloged files,
**When** analyzing dependencies,
**Then** a dependency graph shows which files reference or depend on others.

---

### AC#3: Track Session Continuity Markers

**Given** session files with parentUuid references,
**When** building the catalog,
**Then** session chains are identified (parent → child relationships).

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
        - id: "SM-020"
          description: "Catalog files across session directories"
          testable: true
          priority: "High"
        - id: "SM-021"
          description: "Build file dependency graph"
          testable: true
          priority: "Medium"
        - id: "SM-022"
          description: "Track parentUuid session chains"
          testable: true
          priority: "Medium"

    - type: "DataModel"
      name: "SessionCatalog"
      purpose: "Inventory of session artifacts and relationships"
      fields:
        - name: "files"
          type: "FileEntry[]"
        - name: "dependencies"
          type: "DependencyEdge[]"
        - name: "session_chains"
          type: "SessionChain[]"

  non_functional_requirements:
    - id: "NFR-020"
      category: "Performance"
      requirement: "Catalog 3000+ files within 15 seconds"
      metric: "<15 seconds for full catalog"
      priority: "Medium"
```

---

## Definition of Done

### Implementation
- [ ] File cataloging logic added to session-miner
- [ ] Dependency graph structure defined
- [ ] Session chain tracking documented

### Quality
- [ ] All 3 acceptance criteria verified
- [ ] Edge cases covered (orphaned files, circular refs)

### Testing
- [ ] Test file cataloging
- [ ] Test dependency graph building
- [ ] Test session chain detection

### Documentation
- [ ] Catalog structure documented
- [ ] Query patterns documented

---

## Implementation Notes

*Pending implementation*

---

## Change Log

**Current Status:** Backlog

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2025-01-02 | claude/story-creation-skill | Created | Story created for EPIC-034 Feature 1 | STORY-223-session-file-catalog.story.md |
