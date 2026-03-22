---
id: EPIC-001
title: Expertise System Foundation
business-value: Enable agents to accumulate and reuse domain knowledge, reducing repeated codebase searching by 70% and improving agent accuracy by 50%
status: Backlog
priority: P0
complexity-score: 44
architecture-tier: Tier 3
created: 2025-12-16
estimated-points: 30
target-sprints: 4
dependencies: []
research_references: []
---

# Expertise System Foundation

## Business Goal

Build infrastructure for expertise files, mental models, and domain knowledge accumulation that enables DevForgeAI agents to learn from execution and maintain working memory across sessions.

**Success Metrics:**
- **Agent search reduction:** 70% fewer file searches per execution (agents validate mental models instead of searching)
- **Accuracy improvement:** 50% higher accuracy when agents use expertise files vs. searching from scratch
- **Expertise coverage:** 80% of DevForgeAI projects have at least 3 domain experts created within 2 months

## Features

### Feature 1: Expertise File Schema & Management
**Description:** Define YAML schema for expertise files and implement CRUD operations for mental model storage in `devforgeai/meta/expertise/`.

**User Stories (high-level):**
1. As a Meta-Agentic system, I want to define expertise file schema, so that all experts follow consistent structure (domain, knowledge, learnings, validation_rules, metrics)
2. As an agent, I want to create new expertise files, so that I can start accumulating domain knowledge
3. As an agent, I want to read existing expertise files, so that I can leverage accumulated mental models
4. As an agent, I want to update expertise files, so that I can refine mental models based on new learnings
5. As a system administrator, I want to list all expertise files, so that I can audit what domains have experts

**Estimated Effort:** Medium (8 story points)

### Feature 2: Mental Model Validation
**Description:** Implement validation workflow that compares expertise mental model against actual codebase to detect staleness and accuracy.

**User Stories (high-level):**
1. As an agent expert, I want to validate my mental model against codebase, so that I know if expertise is stale
2. As an agent expert, I want to detect codebase changes (schema migrations, API changes), so that I can trigger re-learning
3. As an agent expert, I want to calculate mental model accuracy score, so that users know confidence level
4. As a user, I want to see validation status of expertise files, so that I know which experts are trustworthy

**Estimated Effort:** Medium (6 story points)

### Feature 3: Execution History Tracking
**Description:** Track agent execution history in separate per-expert files to enable threshold-based self-improvement triggers.

**User Stories (high-level):**
1. As a Meta-Agentic system, I want to create execution history file when expert first used, so that I can track usage
2. As an agent expert, I want to increment execution counter after each use, so that threshold triggers work
3. As an agent expert, I want to record last_executed timestamp, so that staleness detection works
4. As a system, I want to read execution history to determine if self-improvement threshold reached, so that learning triggers automatically

**Estimated Effort:** Small (4 story points)

### Feature 4: Domain Mapping Configuration
**Description:** Create and maintain domain mappings configuration that maps file path glob patterns to relevant domain experts.

**User Stories (high-level):**
1. As a Meta-Agentic system, I want to define domain mappings YAML schema, so that file patterns map to experts
2. As a user, I want to configure domain mappings (e.g., `src/db/**` → database-expert), so that agents know which expert to use
3. As a workflow (e.g., /dev), I want to detect which files changed, so that I can invoke relevant experts automatically
4. As an agent expert, I want to register my domain patterns, so that I'm invoked for relevant work

**Estimated Effort:** Small (3 story points)

### Feature 5: File Locking & Concurrency
**Description:** Implement file locking mechanism to prevent simultaneous writes to expertise files and provide merge strategies for concurrent updates.

**User Stories (high-level):**
1. As an agent expert, I want to acquire file lock before writing expertise, so that concurrent updates don't corrupt data
2. As an agent expert, I want to wait for lock if unavailable, so that updates are serialized
3. As an agent expert, I want to merge changes if another agent updated expertise while I waited, so that no learning is lost
4. As a system administrator, I want to detect stale locks (timeout after 5 minutes), so that stuck processes don't block forever

**Estimated Effort:** Medium (5 story points)

### Feature 6: Ideation Integration
**Description:** Detect ambiguities and missing framework capabilities during `/ideate` workflow, auto-generate meta-file specifications in first epic for project-specific customization.

**User Stories (high-level):**
1. As an ideation workflow, I want to detect when project requires capabilities not in DevForgeAI framework, so that I can propose meta-generation
2. As an ideation workflow, I want to create Epic 0 (if needed) for meta-file creation, so that project-specific experts are built first
3. As a user, I want to review proposed meta-files during ideation, so that I approve project-specific agents/skills/prompts
4. As an ideation workflow, I want to invoke internet-sleuth for knowledge updates (APIs, libraries post-LLM-cutoff), so that expertise is current

**Estimated Effort:** Medium (4 story points)

## Requirements Summary

### Functional Requirements
- Expertise file CRUD operations (create, read, update, list)
- Mental model validation against codebase
- Execution history tracking (counter, timestamps)
- Domain mapping configuration (glob patterns → experts)
- File locking for concurrent writes
- Ideation integration (detect ambiguities, propose meta-files)

### Data Model

**Entities:**
- **Expertise File** (`devforgeai/meta/expertise/{domain}-expert.yaml`)
  - domain: string (e.g., "database", "api", "websocket")
  - knowledge: dict (codebase patterns, architecture, entities)
  - learnings: list (historical insights from N executions)
  - validation_rules: list (tests to verify mental model accuracy)
  - metrics: dict (execution_count, last_executed, last_updated, accuracy_score, staleness_flag)

- **Execution History** (`devforgeai/meta/history/{domain}-expert-history.json`)
  - expert_id: string
  - execution_log: list (timestamp, operation, outcome, tokens_used)
  - execution_count: integer
  - last_executed: datetime
  - last_updated: datetime

- **Domain Mapping** (`devforgeai/meta/domain-mappings.yaml`)
  - mappings: dict (glob_pattern → expert_id)
  - Example: `{"src/db/**": "database-expert", "src/api/**": "api-expert"}`

**Relationships:**
- Expertise File ↔ Execution History: one-to-one (each expert has one history file)
- Domain Mapping → Expertise File: one-to-many (one mapping can reference multiple experts)

### Integration Points
1. **DevForgeAI hook system** - Read hook configuration, trigger expertise updates via hooks
2. **File system** - Read/Write YAML and JSON files in `devforgeai/meta/` directory
3. **Ideation workflow** - Integrate with devforgeai-ideation skill to propose meta-files
4. **internet-sleuth agent** - Invoke for knowledge updates beyond LLM training cutoff

### Non-Functional Requirements

**Performance:**
- Expertise file I/O: <100ms per read/write operation
- Validation workflow: <30s to validate mental model against codebase
- File locking: <1s wait time for lock acquisition (typical)

**Quality:**
- Expertise file size: <100KB per file (enforce pruning/summarization if exceeded)
- Mental model accuracy: >80% facts correct when validated against codebase
- Backward compatibility: 100% of existing DevForgeAI workflows continue working (opt-in enhancement)

**Scalability:**
- Support 10-20 expertise files per project (database, api, websocket, frontend, auth, etc.)
- Support 100+ executions tracked per expert
- Handle 5 concurrent expertise file updates (file locking prevents corruption)

## Architecture Considerations

**Complexity Tier:** Tier 3 (Complex Platform, 44/60)

**Recommended Architecture:**
- Pattern: Clean Architecture with domain separation
- Layers:
  - **Domain Layer:** Expertise entity, validation rules, mental model logic
  - **Application Layer:** File operations, locking orchestration, history tracking
  - **Infrastructure Layer:** File I/O, YAML/JSON parsing, hook integration
  - **Presentation Layer:** CLI commands (/create-meta-expert, /self-improve)
- Database: File-based (YAML for expertise, JSON for history/mappings)
- Deployment: Integrated into DevForgeAI framework (no separate deployment)

**Technology Recommendations:**
- File Format: YAML (expertise files - human-readable), JSON (execution history, domain mappings - parseable)
- File Locking: `flock` (Linux/WSL2) or Python `filelock` library (if CLI uses Python)
- Validation: Read tool + Grep tool + file comparison
- Hooks: Bash scripts in `.claude/hooks/` (already implemented in STORY-018)

## Risks & Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| File locking fails in WSL2 environment | HIGH | Test `flock` early in Feature 5, fallback to last-write-wins if locking unreliable |
| Expertise files grow unbounded | MEDIUM | Implement size limits (<100KB), auto-pruning/summarization when exceeded |
| Mental model validation too slow | MEDIUM | Cache validation results, incremental validation (only check changed files) |
| Concurrent writes corrupt expertise files | HIGH | Mandatory file locking (Feature 5), atomic writes (write to temp file, rename) |
| Ideation integration breaks existing flow | MEDIUM | Make meta-file generation optional (AskUserQuestion), user can skip if not needed |

## Dependencies

**Prerequisites:**
- None (this is foundation epic)

**Dependents:**
- EPIC-002 (Meta-Generation Layer) - requires expertise file schema
- EPIC-003 (Self-Improvement Automation) - requires execution history and validation

## Next Steps

1. **Architecture Phase:** Create 6 context files via `/create-context meta-agentic-system`
   - tech-stack.md: Lock file formats (YAML, JSON), file locking mechanism
   - source-tree.md: Define `devforgeai/meta/` directory structure
   - dependencies.md: No external dependencies (use Claude Code native tools)
   - coding-standards.md: YAML schema standards, error handling patterns
   - architecture-constraints.md: Clean architecture layers, file locking requirements
   - anti-patterns.md: No unbounded file growth, no concurrent writes without locking

2. **Sprint Planning:** Create Sprint 1 via `/create-sprint 1`
   - Focus: Feature 1 (Expertise File Schema & Management) + Feature 2 (Mental Model Validation)

3. **Story Creation:** Break features into stories via `/create-story [feature-description]`
   - Story 1: Define YAML schema for expertise files
   - Story 2: Implement create/read/update operations
   - Story 3: Build mental model validation workflow
