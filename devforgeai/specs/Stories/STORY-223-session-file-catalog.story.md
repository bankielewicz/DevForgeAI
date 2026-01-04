---
id: STORY-223
title: Catalog Session File Structure and Relationships
type: feature
epic: EPIC-034
sprint: Backlog
status: Dev Complete
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
- [x] File cataloging logic added to session-miner - Completed: catalog_session_files() function in .claude/scripts/session_catalog.sh
- [x] Dependency graph structure defined - Completed: build_dependency_graph() with DependencyEdge model
- [x] Session chain tracking documented - Completed: track_session_chains() with SessionChain model

### Quality
- [x] All 3 acceptance criteria verified - Completed: 47/47 tests passing (AC#1: 15, AC#2: 14, AC#3: 18)
- [x] Edge cases covered (orphaned files, circular refs) - Completed: Tests for orphans, circular deps, empty dirs

### Testing
- [x] Test file cataloging - Completed: tests/STORY-223/test-ac1-map-plans-to-stories.sh (15 tests)
- [x] Test dependency graph building - Completed: tests/STORY-223/test-ac2-build-dependency-graph.sh (14 tests)
- [x] Test session chain detection - Completed: tests/STORY-223/test-ac3-track-session-continuity.sh (18 tests)

### Documentation
- [x] Catalog structure documented - Completed: JSON schema documented in session_catalog.sh header
- [x] Query patterns documented - Completed: Usage examples in function docstrings

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-01-03
**Branch:** refactor/devforgeai-migration

- [x] File cataloging logic added to session-miner - Completed: catalog_session_files() function in .claude/scripts/session_catalog.sh
- [x] Dependency graph structure defined - Completed: build_dependency_graph() with DependencyEdge model
- [x] Session chain tracking documented - Completed: track_session_chains() with SessionChain model
- [x] All 3 acceptance criteria verified - Completed: 47/47 tests passing (AC#1: 15, AC#2: 14, AC#3: 18)
- [x] Edge cases covered (orphaned files, circular refs) - Completed: Tests for orphans, circular deps, empty dirs
- [x] Test file cataloging - Completed: tests/STORY-223/test-ac1-map-plans-to-stories.sh (15 tests)
- [x] Test dependency graph building - Completed: tests/STORY-223/test-ac2-build-dependency-graph.sh (14 tests)
- [x] Test session chain detection - Completed: tests/STORY-223/test-ac3-track-session-continuity.sh (18 tests)
- [x] Catalog structure documented - Completed: JSON schema documented in session_catalog.sh header
- [x] Query patterns documented - Completed: Usage examples in function docstrings

### TDD Workflow Summary

**Phase 02 (Red): Test-First Design**
- Generated 47 comprehensive tests covering all 3 acceptance criteria
- Tests placed in tests/STORY-223/
- Test framework: Bash shell scripts with custom assertion library

**Phase 03 (Green): Implementation**
- Implemented session_catalog.sh with 3 main functions via backend-architect subagent
- All 47 tests passing (100% pass rate)

**Phase 04 (Refactor): Code Quality**
- Refactored to extract 12 helper functions
- Performance optimized with O(1) lookups using associative arrays
- JSON escaping security fix applied
- Code reviewer approved

**Phase 05 (Integration): Full Validation**
- Cross-component integration verified
- Anti-gaming validation passed (no skip decorators, empty tests, or excessive mocking)

### Files Created/Modified

**Created:**
- .claude/scripts/session_catalog.sh (540 lines, 3 main functions + 12 helpers)
- tests/STORY-223/test-lib.sh (test library)
- tests/STORY-223/test-ac1-map-plans-to-stories.sh (AC#1 tests)
- tests/STORY-223/test-ac2-build-dependency-graph.sh (AC#2 tests)
- tests/STORY-223/test-ac3-track-session-continuity.sh (AC#3 tests)
- tests/STORY-223/test-nfr-020-performance.sh (NFR tests)

---

## Change Log

**Current Status:** Dev Complete

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2025-01-02 | claude/story-creation-skill | Created | Story created for EPIC-034 Feature 1 | STORY-223-session-file-catalog.story.md |
| 2026-01-03 | claude/test-automator | Red (Phase 02) | Tests generated | tests/STORY-223/*.sh |
| 2026-01-03 | claude/backend-architect | Green (Phase 03) | Implementation complete | .claude/scripts/session_catalog.sh |
| 2026-01-03 | claude/refactoring-specialist | Refactor (Phase 04) | Code refactored, security fix | .claude/scripts/session_catalog.sh |
| 2026-01-03 | claude/opus | DoD Update (Phase 07) | Development complete, DoD validated | STORY-223-session-file-catalog.story.md |
