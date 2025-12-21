# Parallel Task Orchestration - Requirements Specification

**Version:** 1.0
**Date:** 2025-12-04
**Status:** Approved
**Author:** DevForgeAI Ideation Skill
**Epic:** EPIC-017
**Complexity Score:** 39/60 (Tier 3: Complex Platform)

---

## 1. Project Overview

### 1.1 Project Context
**Type:** Brownfield (DevForgeAI framework enhancement)
**Domain:** Developer Tools / AI Framework
**Timeline:** 2 sprints (4 weeks)
**Team:** DevForgeAI framework maintainers

### 1.2 Problem Statement
Current DevForgeAI workflows execute tasks sequentially, causing unnecessary wait times during TDD cycles (8-12 minutes per story). Research confirms that Claude Code Terminal supports parallel execution patterns that can reduce this by 35-40%, but the framework doesn't leverage them.

**Pain Points Addressed:**
- Long wait times during development workflows
- Inefficient token usage (Opus waiting idle during sequential tasks)
- Poor developer experience during long operations (builds, tests)

### 1.3 Solution Overview
Implement parallel task orchestration infrastructure enabling:
1. Multiple Task() subagent calls in single message (concurrent execution)
2. Background Bash task execution for long-running operations
3. Auto-generated subagent registry for proactive agent discovery
4. Configurable parallel limits per Anthropic subscription tier

### 1.4 Success Criteria
| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| TDD cycle time reduction | 35-40% | Before/after timing of /dev command |
| Long operation speedup | 50-80% | Build/test duration comparison |
| Token cost increase | 0% | Token counter comparison |
| Sync coordination overhead | <1 second | Measure Task() to first response |

---

## 2. User Roles & Personas

### 2.1 Primary Users

**DevForgeAI Framework Users**
- Developers using /dev, /qa, /orchestrate commands
- Benefit from faster workflow execution
- No configuration required (sensible defaults)

**DevForgeAI Framework Maintainers**
- Authors of skills, commands, subagents
- Need documentation on parallel patterns
- Benefit from auto-generated registry

### 2.2 User Personas

**Persona 1: Developer (Alex)**
- **Role:** Full-stack developer using DevForgeAI for TDD
- **Goals:** Implement features quickly with high quality
- **Needs:** Fast feedback loops, minimal wait time
- **Pain Points:** Current 8-12 minute TDD cycles feel slow
- **Success:** TDD cycles in 5-7 minutes without config changes

**Persona 2: Framework Maintainer (Jordan)**
- **Role:** DevForgeAI skill/subagent author
- **Goals:** Create efficient, reusable framework components
- **Needs:** Clear patterns for parallel orchestration, auto-discovery
- **Pain Points:** Manual CLAUDE.md updates, documentation drift
- **Success:** Add subagent → run script → registry updated automatically

---

## 3. Functional Requirements

### 3.1 User Stories by Feature

#### Feature 1: Parallel Configuration Infrastructure

**FR-1.1: Configuration Schema**
```
As a DevForgeAI user,
I want a structured configuration file for parallel execution settings,
So that I can customize parallel limits to match my Anthropic subscription tier.
```

**Acceptance Criteria:**
- Configuration file at `devforgeai/config/parallel-orchestration.yaml`
- YAML schema with: enabled flag, max_concurrent_tasks, profiles, timeouts, retry settings
- Default profile uses safe limits (4-6 concurrent tasks)
- Validation on load (reject invalid config with clear error message)

**FR-1.2: Profile Support**
```
As a DevForgeAI user,
I want preset profiles for different Anthropic plans,
So that I don't need to research optimal settings.
```

**Acceptance Criteria:**
- Three profiles: `pro` (4 concurrent), `max` (8 concurrent), `api` (10 concurrent + batch)
- Profile selected via config or auto-detected if possible
- Override individual settings within profile

**FR-1.3: Timeout Configuration**
```
As a DevForgeAI user,
I want configurable timeouts for subagents and background tasks,
So that hung operations fail gracefully instead of blocking forever.
```

**Acceptance Criteria:**
- `subagent_timeout_ms`: Default 300000 (5 minutes)
- `background_task_timeout_ms`: Default 600000 (10 minutes)
- Timeout triggers KillShell for background tasks
- Timeout triggers fallback to sequential for subagents

#### Feature 2: Subagent Registry Auto-Generation

**FR-2.1: Registry Generation Script**
```
As a framework maintainer,
I want a script that generates CLAUDE.md subagent section from agents/*.md,
So that the registry is always in sync with actual subagents.
```

**Acceptance Criteria:**
- Script at `.claude/scripts/generate-subagent-registry.sh`
- Reads all `.claude/agents/*.md` files
- Extracts YAML frontmatter: name, description, tools, proactive_triggers
- Generates markdown section for CLAUDE.md (auto-generated marker comments)
- Exit code 0 on success, non-zero on failure with error message

**FR-2.2: Proactive Triggers**
```
As Opus,
I want proactive triggers mapping task patterns to subagents,
So that I automatically invoke the right agent without hardcoded Task() calls.
```

**Acceptance Criteria:**
- Frontmatter field `proactive_triggers` added to agent template
- Registry includes table: Task Pattern | Subagent | Description
- Examples: "writing tests" → test-automator, "code review" → code-reviewer
- At least 10 agents have proactive triggers defined

**FR-2.3: Pre-Commit Hook Integration**
```
As a framework maintainer,
I want registry auto-updated on git commit,
So that CLAUDE.md never drifts from actual agents.
```

**Acceptance Criteria:**
- Pre-commit hook calls generate-subagent-registry.sh
- Hook runs only if agents/*.md files changed
- Commit blocked if registry generation fails
- Automatic staging of updated CLAUDE.md

#### Feature 3: Error Handling Patterns

**FR-3.1: Partial Failure Recovery**
```
As Opus,
I want to continue with successful subagents when one fails,
So that a single failure doesn't block 5 successful results.
```

**Acceptance Criteria:**
- Collect results from all successful subagents
- Log failed subagent with error details
- Return partial results + failure summary
- User informed which tasks succeeded/failed

**FR-3.2: Timeout Handling**
```
As Opus,
I want hung background tasks killed after configurable timeout,
So that I don't wait forever for stuck operations.
```

**Acceptance Criteria:**
- Timeout tracked per task (start time + timeout_ms)
- KillShell invoked when timeout exceeded
- Error returned: "Task {id} killed after {timeout}s"
- Subsequent tasks not blocked by killed task

**FR-3.3: Retry Logic**
```
As Opus,
I want failed subagents retried before falling back to sequential,
So that transient failures are automatically recovered.
```

**Acceptance Criteria:**
- `max_retry_attempts` configuration (default: 3)
- `backoff_multiplier` configuration (default: 1.5)
- Retry sequence: immediate → 1.5s → 2.25s → fallback
- Retry only on transient errors (timeout, network), not on hard failures

#### Feature 4: Orchestration Skill Refactor

**FR-4.1: Parallel Phase 0 Context Loading**
```
As Opus executing devforgeai-orchestration,
I want 6 context files loaded in parallel,
So that Phase 0 completes in 2-3 seconds instead of 6-8 seconds.
```

**Acceptance Criteria:**
- All 6 Read() calls in single message block
- Files: tech-stack, source-tree, dependencies, coding-standards, architecture-constraints, anti-patterns
- Result parsing after all reads complete
- Fallback to sequential if parallel fails

**FR-4.2: Parallel Feature Analysis**
```
As Opus executing devforgeai-orchestration,
I want multiple features analyzed concurrently,
So that story with 5 features is analyzed in 6 minutes instead of 25 minutes.
```

**Acceptance Criteria:**
- Up to 5 requirements-analyst Task() calls in single message
- Each analyzes one feature independently
- Results merged after all complete
- Dependency analysis runs sequentially after (uses merged results)

#### Feature 5: Development Skill Refactor

**FR-5.1: Background Test Execution**
```
As Opus executing devforgeai-development,
I want tests running in background while I implement code,
So that TDD cycle is 35-40% faster.
```

**Acceptance Criteria:**
- Tests started with `run_in_background=true` in Phase 1
- Implementation proceeds in Phase 2-3 while tests run
- BashOutput retrieves results in Phase 4
- If tests fail, implementation still saved (test fixes in Phase 5)

**FR-5.2: Parallel Subagent Invocation**
```
As Opus executing devforgeai-development,
I want multiple subagents (test-automator, code-analyzer) invoked concurrently,
So that analysis phase completes faster.
```

**Acceptance Criteria:**
- Independent subagents invoked in single message
- Example: test-automator + code-analyzer for different concerns
- Results collected and merged
- Dependencies respected (code-generator before test-automator for same file)

#### Feature 6: QA/Release Skill Updates

**FR-6.1: Parallel QA Validation**
```
As Opus executing devforgeai-qa,
I want validation subagents running concurrently,
So that QA validation completes faster.
```

**Acceptance Criteria:**
- test-automator, code-reviewer, security-auditor in parallel
- coverage-analyzer runs after tests complete (dependency)
- Results merged into single QA report
- Any CRITICAL violation blocks regardless of parallel status

**FR-6.2: Parallel Release Validation**
```
As Opus executing devforgeai-release,
I want smoke tests running concurrently with deployment validation,
So that release proceeds faster.
```

**Acceptance Criteria:**
- Smoke tests and deployment checks in parallel where independent
- Deployment to staging → parallel smoke tests → deployment to production
- Rollback triggered if any smoke test fails

#### Feature 7: Documentation & Validation

**FR-7.1: Architecture Documentation Update**
```
As a framework maintainer,
I want architecture-constraints.md updated with parallel execution rules,
So that all skills follow consistent patterns.
```

**Acceptance Criteria:**
- New section: "Parallel Execution Rules" in architecture-constraints.md
- Covers: task limits, dependency detection, timeout requirements, failure recovery
- LOCKED status (requires ADR to change)

**FR-7.2: Quick Reference Card**
```
As a DevForgeAI user,
I want a quick reference card for parallel patterns,
So that I can copy-paste working examples.
```

**Acceptance Criteria:**
- Location: `.claude/memory/parallel-orchestration-guide.md` (already exists, verify/enhance)
- Covers: Task() parallelism, background tasks, tool parallelism
- Includes anti-patterns section (what NOT to do)
- <1000 lines for quick loading

**FR-7.3: Performance Validation**
```
As a framework maintainer,
I want performance tests validating 35-40% time reduction,
So that success metrics are verified before release.
```

**Acceptance Criteria:**
- Before/after timing script for /dev command
- Run on 3+ representative stories
- Report: baseline time, optimized time, % improvement
- PASS if improvement ≥35%, WARN if 30-35%, FAIL if <30%

---

## 4. Data Requirements

### 4.1 Data Model

#### ParallelConfig Entity
**Purpose:** Store parallel execution settings

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| enabled | boolean | Yes | true | Enable/disable parallel execution |
| max_concurrent_tasks | integer | Yes | 6 | Maximum parallel subagents |
| active_profile | string | No | null | Selected profile name |

#### Profile Entity
**Purpose:** Preset configurations for subscription tiers

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| name | string | Yes | - | Profile identifier (pro/max/api) |
| max_concurrent_tasks | integer | Yes | - | Concurrent task limit |
| batch_enabled | boolean | No | false | Enable batch API mode |

#### TimeoutConfig Entity
**Purpose:** Timeout settings for tasks

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| subagent_timeout_ms | integer | Yes | 300000 | Subagent timeout (5 min) |
| background_task_timeout_ms | integer | Yes | 600000 | Background task timeout (10 min) |

#### RetryConfig Entity
**Purpose:** Retry settings for failed tasks

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| max_attempts | integer | Yes | 3 | Maximum retry attempts |
| backoff_multiplier | float | Yes | 1.5 | Exponential backoff multiplier |

#### SubagentMeta Entity
**Purpose:** Metadata extracted from agent frontmatter

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Agent identifier |
| description | string | Yes | Agent purpose |
| tools | string[] | Yes | Allowed tools |
| proactive_triggers | string[] | No | Task patterns triggering this agent |

### 4.2 Data Constraints

**Configuration Validation:**
- `max_concurrent_tasks`: 1-10 (framework limit)
- `subagent_timeout_ms`: 30000-600000 (30s to 10min)
- `background_task_timeout_ms`: 60000-600000 (1min to 10min)
- `max_attempts`: 1-5
- `backoff_multiplier`: 1.0-3.0

**Registry Validation:**
- Agent name must match filename (agent-name.md → name: agent-name)
- Tools must be from allowed list
- Proactive triggers should be lowercase, 2-50 characters

---

## 5. Integration Requirements

### 5.1 External Services

#### Claude Code Terminal
**Purpose:** Task tool parallel execution
**Protocol:** Internal tool invocation
**Data Flow:** Two-way (invoke tasks, receive results)
**Authentication:** N/A (same session)
**Error Handling:** Timeout → KillShell, Retry → Fallback sequential

#### Bash Tool
**Purpose:** Background task execution
**Protocol:** Internal tool invocation
**Data Flow:** One-way command, async result via BashOutput
**Key Parameter:** `run_in_background=true`
**Error Handling:** Timeout → KillShell

### 5.2 API Contracts

#### Task() Parallel Invocation
```yaml
# Multiple Task() in single message
# All execute concurrently, implicit sync point after
- Task:
    subagent_type: "test-automator"
    description: "Generate tests for module A"
    prompt: "..."
- Task:
    subagent_type: "code-analyzer"
    description: "Analyze complexity of module B"
    prompt: "..."
# Results available after both complete
```

#### Background Bash Execution
```yaml
# Start background task
Bash:
  command: "npm test -- --coverage"
  run_in_background: true
  timeout: 600000
# Returns immediately with task_id

# Retrieve results later
BashOutput:
  bash_id: "{task_id}"
# Returns stdout, stderr, is_complete, exit_code
```

---

## 6. Non-Functional Requirements

### 6.1 Performance

| Requirement | Target | Measurement |
|-------------|--------|-------------|
| TDD cycle time | 35-40% reduction | Before/after timing |
| Long operations | 50-80% faster | Build/test duration |
| Sync overhead | <1 second | Task() to first response |
| Context loading | 2-3 seconds (6 files) | Phase 0 duration |

### 6.2 Reliability

| Requirement | Target | Implementation |
|-------------|--------|----------------|
| Partial failure recovery | Continue with 4/5 successful | Collect partial results |
| Timeout handling | 100% of hung tasks killed | KillShell after timeout |
| Retry success rate | 80%+ transient failures recovered | 3 retries with backoff |
| Fallback availability | 100% | Sequential execution always works |

### 6.3 Cost

| Requirement | Target | Validation |
|-------------|--------|------------|
| Token consumption | 0% increase | Token counter comparison |
| Infrastructure cost | $0 | No new services |

### 6.4 Maintainability

| Requirement | Target | Implementation |
|-------------|--------|----------------|
| Documentation coverage | ≥80% | Architecture docs, quick reference |
| Registry freshness | Always current | Auto-generation script |
| Pattern consistency | 100% | All skills use same patterns |

---

## 7. Complexity Assessment

**Total Score:** 39/60 (Tier 3: Complex Platform)

### Score Breakdown

| Dimension | Score | Assessment |
|-----------|-------|------------|
| Functional | 15/20 | Multiple patterns, branching error recovery |
| Technical | 13/20 | Concurrent task coordination, timeout handling |
| Team/Org | 5/10 | Small team, existing framework knowledge |
| NFR | 6/10 | Performance targets, no compliance |

### Architecture Tier Recommendation

**Tier 3: Complex Platform** is appropriate because:
- Multiple coordinated parallel patterns (not simple sequential)
- Error handling with partial recovery (not basic try/catch)
- Configuration system with profiles (not hardcoded values)
- Registry auto-generation (not manual updates)

---

## 8. Feasibility Analysis

### 8.1 Technical Feasibility: ✅ FEASIBLE (9/10)

**Evidence:**
| Capability | Status | Source |
|------------|--------|--------|
| Native subagent parallelism | VERIFIED | Official Claude Code docs |
| Background task execution | VERIFIED | Bash tool docs, v1.0.71+ |
| Parallel tool calling | VERIFIED | Opus 4.5 release notes |
| Safe limits (4-10) | DOCUMENTED | GitHub issues #2382, #4580 |

### 8.2 Business Feasibility: ✅ FEASIBLE

**Budget:** No additional cost (framework enhancement)
**Timeline:** 2 sprints fits 4-week target
**Value:** 35-40% time savings per story × all DevForgeAI users

### 8.3 Resource Feasibility: ✅ FEASIBLE

**Team:** Existing framework maintainers have context
**Skills:** No new technologies to learn
**Dependencies:** Research complete, all patterns documented

### 8.4 Risk Register

| Risk | Category | Prob | Impact | Severity | Mitigation |
|------|----------|------|--------|----------|------------|
| Task dependency misdetection | Technical | Medium | High | HIGH | Dependency validation in config |
| JSON serialization freeze | Technical | Low | Medium | MEDIUM | Cap at 6-8 concurrent |
| Blocking behavior bug | Technical | Low | Medium | MEDIUM | Explicit parallel instruction |
| Backward compatibility | Technical | Low | High | MEDIUM | Feature flag, graceful degradation |
| Documentation drift | Process | Medium | Medium | MEDIUM | Auto-generation, pre-commit hook |

---

## 9. Constraints & Assumptions

### 9.1 Technical Constraints

**From architecture-constraints.md:**
- Three-layer architecture: Commands → Skills → Subagents
- Subagents cannot invoke Skills or Commands
- Circular dependencies forbidden
- Progressive disclosure pattern required

**Parallel-Specific Constraints:**
- Maximum 10 concurrent tasks (framework limit)
- Background tasks require explicit timeout
- Results must be retrieved before phase completion

### 9.2 Business Constraints

- No additional infrastructure cost
- Must work within existing Claude Code Terminal
- Backward compatible (existing workflows unchanged if parallel disabled)

### 9.3 Assumptions (Validated)

| Assumption | Status | Validation |
|------------|--------|------------|
| Parallel Task() supported | ✅ Validated | Official docs, GitHub issues |
| run_in_background works | ✅ Validated | Bash tool v1.0.71+ |
| 4-6 concurrent safe | ✅ Validated | Community testing |
| Auto-accept resolves blocking | ✅ Validated | GitHub issue #2382 |

---

## 10. Epic Breakdown

### Epic Roadmap

```
Sprint 1 Week 1: Infrastructure Foundation
├── F1: Parallel Config Infrastructure (5 pts)
├── F2: Subagent Registry Auto-Generation (5 pts)
└── F3: Error Handling Patterns (5 pts)

Sprint 1 Week 2: Core Skill Refactoring
├── F4: Orchestration Skill Refactor (8 pts)
└── F5: Development Skill Refactor (8 pts)

Sprint 2 Week 1: Extended Skill Updates
└── F6: QA/Release Skill Updates (5 pts)

Sprint 2 Week 2: Documentation & Validation
└── F7: Documentation & Validation (5 pts)

Total: 41 story points over 2 sprints
```

### Epic Summary

**EPIC-017: Parallel Task Orchestration for DevForgeAI**
- Business Goal: 35-40% time reduction with zero token cost
- Features: 7
- Estimated Points: 41
- Target Sprints: 2
- Priority: High
- Status: Planning

---

## 11. Next Steps

1. **Sprint Planning:** Run `/create-sprint 1` for EPIC-017
2. **Story Creation:** Break features into stories via `/create-story`
3. **Development:** Implement stories via `/dev STORY-XXX`

---

## Appendices

### A. Glossary

| Term | Definition |
|------|------------|
| Parallel Task Orchestration | Executing multiple subagent tasks concurrently |
| Background Task | Bash command running asynchronously, results retrieved later |
| Implicit Sync Point | Automatic wait for all parallel tasks to complete |
| Subagent Registry | Auto-generated index of available agents with triggers |
| Proactive Triggers | Task patterns that automatically invoke specific agents |

### B. References

- Research Report: `docs/enhancements/2025-12-04/research/parallel-orchestration-research.md`
- Implementation Guide: `docs/enhancements/2025-12-04/research/parallel-orchestration-guide.md`
- Quick Reference: `docs/enhancements/2025-12-04/research/PARALLEL-PATTERNS-QUICK-REFERENCE.md`
- Claude Code Docs: https://docs.anthropic.com/en/docs/build-with-claude/claude-code/
- GitHub Issues: #2382 (blocking), #4580 (parallel execution)

### C. Open Questions

1. **Profile Auto-Detection:** Can we detect Anthropic subscription tier automatically?
   - Current answer: No, user configures manually
   - Future: Investigate API for tier detection

2. **Batch API Integration:** Should API tier use batch processing?
   - Current answer: Optional flag `batch_enabled: true`
   - Future: Implement if significant demand

---

**Document Status:** Approved
**Review Date:** 2025-12-04
**Next Review:** After Sprint 1 completion
