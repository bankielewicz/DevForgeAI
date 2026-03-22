---
id: EPIC-058
title: Treelint Advanced Features
status: Planning
start_date: 2026-03-08
target_date: 2026-03-21
total_points: 21-34
created: 2026-01-30
updated: 2026-01-30
source_brainstorm: BRAINSTORM-009
source_requirements: treelint-integration-requirements.md
parent_initiative: Treelint AST-Aware Code Search Integration
related_epics: [EPIC-055, EPIC-056, EPIC-057, EPIC-059]
depends_on: [EPIC-057]
---

# Epic: Treelint Advanced Features

## Business Goal

Leverage Treelint's full capabilities beyond basic symbol search, including dependency graph analysis, code quality metrics extraction, test coverage mapping, and repository map generation. These advanced features enable deeper code understanding and more sophisticated analysis workflows.

## Success Metrics

- **Metric 1:** Dependency graph integration working (`treelint deps --calls`)
- **Metric 2:** Code quality metrics extracted (function length, nesting depth)
- **Metric 3:** Test-to-function coverage mapping implemented
- **Metric 4:** Repository map generation for context (`treelint map --ranked`)
- **Metric 5:** Daemon auto-start logic functional when daemon is stopped

## Scope

### Overview

This epic implements advanced Treelint features that go beyond simple symbol search. These features enable sophisticated analysis patterns like call chain traversal, impact analysis, and semantic coverage mapping.

### Features

1. **Dependency Graph Integration**
   - Description: Integrate `treelint deps --calls` for call chain analysis
   - User Value: Understand function relationships, identify impact of changes
   - Estimated Points: 5-8 story points

2. **Code Quality Metrics Extraction**
   - Description: Extract function length, nesting depth, and complexity from AST
   - User Value: Data-driven code quality assessment beyond line counting
   - Estimated Points: 5-8 story points

3. **Test Coverage Mapping**
   - Description: Semantic correlation between test files and source functions
   - User Value: Know which functions are tested vs untested at semantic level
   - Estimated Points: 5-8 story points

4. **Repository Map Generation**
   - Description: Use `treelint map --ranked` for context-efficient codebase overview
   - User Value: Provide AI agents with ranked symbol importance for context
   - Estimated Points: 3-5 story points

5. **Daemon Auto-Start Logic**
   - Description: Claude helps start daemon when status is stopped
   - User Value: Fast queries (<5ms) without manual daemon management
   - Estimated Points: 3-5 story points

### Out of Scope

- ❌ MCP server integration (explicitly out of scope per requirements)
- ❌ Additional language support beyond Treelint v0.12.0
- ❌ Modifications to Treelint itself
- ❌ Real-time streaming (JSON batch responses sufficient)

## Target Sprints

**Estimated Duration:** 2 sprints / 2 weeks

**Sprint Breakdown:**
- **Sprint 5:** Dependency graph + Code quality metrics (10-16 pts)
- **Sprint 6:** Test coverage mapping + Repo map + Daemon auto-start (11-18 pts)

## Dependencies

### External Dependencies

- **Treelint v0.12.0:** Must support `deps`, `map`, and daemon commands
- **SQLite index:** Must be generated for advanced queries

### Internal Dependencies

- **EPIC-057 (Subagent Integration):** Basic Treelint usage must be working
- **Reference files:** Patterns from EPIC-057 extended for advanced features

### Blocking Issues

- None identified - all features are incremental on top of EPIC-057

## Stakeholders

- **Product Owner:** Framework Architect (You)
- **Tech Lead:** Framework Architect (You)
- **Other Stakeholders:**
  - Subagents using advanced features
  - Skills (devforgeai-development, devforgeai-qa, devforgeai-rca, designing-systems)

## Requirements

### Functional Requirements

#### User Stories

**User Story 1: Dependency Graph Integration**
```
As an AI Agent,
I want to query function call relationships,
So that I can understand code dependencies and impact of changes.
```

**Acceptance Criteria:**
- [ ] `treelint deps --calls --symbol <name>` returns callers and callees
- [ ] JSON output parsed correctly
- [ ] Results used in refactoring-specialist for impact analysis
- [ ] Results used in code-reviewer for dependency validation
- [ ] Performance <200ms for typical queries

**User Story 2: Code Quality Metrics Extraction**
```
As a code-quality-auditor Subagent,
I want AST-based quality metrics,
So that I can assess code quality with structural accuracy.
```

**Acceptance Criteria:**
- [ ] Function length extracted from AST (lines of code)
- [ ] Nesting depth calculated from AST structure
- [ ] Metrics integrated into code quality analysis
- [ ] Results compared against thresholds (e.g., >50 lines = warning)
- [ ] JSON output format documented

**User Story 3: Test Coverage Mapping**
```
As a coverage-analyzer Subagent,
I want semantic test-to-function mapping,
So that I know which functions are tested at a semantic level.
```

**Acceptance Criteria:**
- [ ] Test functions correlated with source functions by name patterns
- [ ] Coverage gaps identified at function level (not just file level)
- [ ] Results integrated into coverage reports
- [ ] Mapping handles multiple test files per source file

**User Story 4: Repository Map Generation**
```
As an AI Agent,
I want a ranked codebase overview,
So that I can prioritize which symbols to include in my context.
```

**Acceptance Criteria:**
- [ ] `treelint map --ranked` returns symbols ranked by importance
- [ ] JSON output parsed correctly
- [ ] Rankings used to filter context (top N symbols)
- [ ] Integration with designing-systems for brownfield analysis

**User Story 5: Daemon Auto-Start Logic**
```
As a User,
I want Claude to help start the daemon when stopped,
So that I get fast queries without manual daemon management.
```

**Acceptance Criteria:**
- [ ] Daemon status checked before queries
- [ ] If stopped, Claude offers to start daemon
- [ ] Graceful handling if user declines
- [ ] Fallback to CLI mode if daemon unavailable
- [ ] No orphan daemon processes

### Non-Functional Requirements (NFRs)

#### Performance
- **Dependency Query:** <200ms for typical call chain
- **Map Generation:** <10 seconds for 100K file codebase
- **Daemon Queries:** <5ms when daemon running

#### Reliability
- **Error Recovery:** Graceful fallback if advanced features fail
- **Daemon Lifecycle:** No orphan processes, clean shutdown

### Integration Requirements

#### API Contracts

**Dependency Graph Command:**
```bash
treelint deps --calls --symbol handleRequest --format json
```

**Response:**
```json
{
  "symbol": "handleRequest",
  "callers": [
    {"name": "routeRequest", "file": "src/router.py", "line": 45}
  ],
  "callees": [
    {"name": "validateInput", "file": "src/validator.py", "line": 12},
    {"name": "processData", "file": "src/processor.py", "line": 78}
  ]
}
```

**Repository Map Command:**
```bash
treelint map --ranked --format json
```

**Response:**
```json
{
  "symbols": [
    {"name": "handleRequest", "type": "function", "rank": 1, "references": 45},
    {"name": "User", "type": "class", "rank": 2, "references": 38}
  ],
  "total_symbols": 1250,
  "total_files": 156
}
```

## Architecture Considerations

### Complexity Tier
**Tier 2: Enhancement Package (16-30 points)**
- **Score:** 21-34 points
- **Rationale:** Advanced features building on established patterns

### Technology Constraints

- **Constraint 1:** Must use existing Treelint v0.12.0 capabilities
- **Constraint 2:** No modifications to Treelint source code
- **Constraint 3:** Daemon lifecycle managed by user (Claude assists but doesn't auto-start)

## Risks & Constraints

### Technical Risks

**Risk 1: Dependency Graph Accuracy**
- **Description:** Call relationships may be incomplete for dynamic languages
- **Probability:** Medium
- **Impact:** Low
- **Mitigation:** Document limitations, provide manual verification guidance

**Risk 2: Test Coverage Mapping Complexity**
- **Description:** Correlating tests to functions may have false positives
- **Probability:** Medium
- **Impact:** Medium
- **Mitigation:** Use naming conventions, allow manual overrides

### Constraints

**Constraint 1: Treelint Capabilities**
- **Description:** Limited to what Treelint v0.12.0 provides
- **Impact:** Cannot add new analysis types
- **Mitigation:** Document capability boundaries

## Assumptions

1. EPIC-057 complete with basic Treelint usage working
2. Treelint v0.12.0 `deps` and `map` commands are stable
3. Daemon lifecycle is user-managed (not auto-started by framework)

## Stories

| Story ID | Title | Points | Status | Sprint |
|----------|-------|--------|--------|--------|
| STORY-370 | Integrate Dependency Graph Analysis via Treelint deps | 5 | Backlog | Backlog |
| STORY-371 | Implement Code Quality Metrics Extraction via Treelint AST | 5 | Backlog | Backlog |
| STORY-372 | Implement Semantic Test Coverage Mapping via Treelint | 5 | Backlog | Backlog |
| STORY-373 | Integrate Repository Map Generation via Treelint map | 5 | Backlog | Backlog |
| STORY-374 | Implement Daemon Auto-Start Logic for Treelint | 5 | Backlog | Backlog |

## Notes

- This is the **fourth of 5 epics** in the Treelint integration initiative
- Builds on EPIC-057's basic Treelint integration
- EPIC-059 (Validation & Rollout) depends on this epic
- Features are incremental - can be prioritized based on value

---

**Epic Status:**
- ⚪ **Planning** - Requirements being defined

**Last Updated:** 2026-01-30 by DevForgeAI
