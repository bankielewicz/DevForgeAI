---
id: EPIC-017
title: Parallel Task Orchestration for DevForgeAI
business-value: 35-40% reduction in story development cycle time with zero additional token cost
status: Planning
priority: High
complexity-score: 39
architecture-tier: Tier 3 (Complex Platform)
created: 2025-12-04
estimated-points: 41
target-sprints: 2
research-reference: docs/enhancements/2025-12-04/
---

# Parallel Task Orchestration for DevForgeAI

## Business Goal

Enable Opus to orchestrate multiple parallel subagents to reduce wait time for complex workflows. Cut story development cycle time by **35-40%** with **zero additional token cost**.

**Success Metrics:**
- Time reduction: 35-40% faster TDD cycles (8-12 min → 5-7 min per story)
- Long operations: 50-80% faster builds/tests via background execution
- Token cost: Zero increase (same work, concurrent execution)
- Sync overhead: <1 second coordination latency

## Features

### Feature 1: Parallel Configuration Infrastructure (Sprint 1, Week 1)
**Description:** Create `devforgeai/config/parallel-orchestration.yaml` with profile support, timeout settings, and retry configuration. Foundation for all parallel patterns.

**User Stories (high-level):**
1. As a DevForgeAI user, I want to configure maximum concurrent tasks so I can match my Anthropic subscription tier
2. As a DevForgeAI user, I want configurable timeouts so long-running operations fail gracefully
3. As a DevForgeAI user, I want profile presets (Pro/Max/API) so I don't need to research optimal settings

**Estimated Effort:** Medium (5 story points)

### Feature 2: Subagent Registry Auto-Generation (Sprint 1, Week 1)
**Description:** Script that reads `.claude/agents/*.md` frontmatter and generates CLAUDE.md section with proactive triggers. Single source of truth for subagent discovery.

**User Stories (high-level):**
1. As Opus, I want proactive triggers mapping task patterns to subagents so I automatically use the right agent
2. As a framework maintainer, I want auto-generated registry so CLAUDE.md never drifts from actual agents
3. As a DevForgeAI user, I want agents/frontmatter extended with proactive_triggers field

**Estimated Effort:** Medium (5 story points)

### Feature 3: Error Handling Patterns (Sprint 1, Week 1)
**Description:** Implement partial failure recovery, timeout handling, and retry logic patterns for parallel orchestration.

**User Stories (high-level):**
1. As Opus, I want partial failure recovery so 1 failed subagent doesn't block 5 successful ones
2. As Opus, I want timeout handling to kill hung background tasks after configurable limit
3. As Opus, I want retry logic (max N attempts with backoff) before fallback to sequential

**Estimated Effort:** Medium (5 story points)

### Feature 4: Orchestration Skill Refactor (Sprint 1, Week 2)
**Description:** Refactor devforgeai-orchestration skill to use parallel subagent invocation for story analysis and feature decomposition.

**User Stories (high-level):**
1. As Opus, I want to invoke multiple Task() calls in single message for concurrent analysis
2. As Opus, I want Phase 0 context loading (6 files) to execute in parallel
3. As Opus, I want feature analysis to run concurrently (3-5 features simultaneously)

**Estimated Effort:** Large (8 story points)

### Feature 5: Development Skill Refactor (Sprint 1, Week 2)
**Description:** Refactor devforgeai-development skill to use background task execution for tests/builds and parallel Phase 0 loading.

**User Stories (high-level):**
1. As Opus, I want tests to run in background via `run_in_background=true` while I implement code
2. As Opus, I want Phase 0 context files to load in parallel (6 files simultaneously)
3. As Opus, I want background task results retrieved via BashOutput before proceeding

**Estimated Effort:** Large (8 story points)

### Feature 6: QA/Release Skill Updates (Sprint 2, Week 1)
**Description:** Apply parallel patterns to devforgeai-qa and devforgeai-release skills for parallel validation subagents.

**User Stories (high-level):**
1. As Opus, I want QA validation subagents (test-automator, code-reviewer, security-auditor) to run in parallel
2. As Opus, I want release smoke tests to run concurrently with deployment validation
3. As Opus, I want consistent error handling patterns across all skills

**Estimated Effort:** Medium (5 story points)

### Feature 7: Documentation & Validation (Sprint 2, Week 2)
**Description:** Update architecture documentation, enhance implementation guide, create quick reference, update CLAUDE.md, and validate all NFRs.

**User Stories (high-level):**
1. As a framework maintainer, I want architecture-constraints.md updated with parallel execution rules
2. As a DevForgeAI user, I want quick reference card for copy-paste parallel patterns
3. As a framework maintainer, I want performance tests validating 35-40% time reduction

**Estimated Effort:** Medium (5 story points)

## Requirements Summary

### Functional Requirements
- Multiple Task() calls in single message (4-6 concurrent subagents with implicit sync)
- Background Bash execution via `run_in_background=true` for long operations
- Subagent registry auto-discovery via generated CLAUDE.md section
- Configurable parallel limits via `devforgeai/config/parallel-orchestration.yaml`

### Data Model
**Entities:**
- ParallelConfig: Profile settings, timeouts, retry configuration
- SubagentMeta: Name, description, tools, proactive_triggers from frontmatter
- TaskContext: Task ID, status, start time, timeout, retry count

**Relationships:**
- ParallelConfig → Profiles (one-to-many)
- SubagentMeta → ProactiveTriggers (one-to-many)

### Integration Points
1. Claude Code Terminal: Task tool parallel invocation
2. Bash tool: `run_in_background=true` parameter
3. BashOutput tool: Retrieve background task results
4. KillShell tool: Timeout handling

### Non-Functional Requirements

**Performance:**
- 35-40% reduction in TDD cycle time (validated via before/after timing)
- 50-80% faster long operations via background execution
- Sub-second (<1s) sync overhead for parallel coordination

**Reliability:**
- Partial failure recovery (continue with successful subagents)
- Graceful degradation (fallback to sequential on parallel failure)
- Configurable timeouts with kill-switch for hung tasks

**Cost:**
- Zero additional token consumption
- Same work, concurrent execution only

## Architecture Considerations

**Complexity Tier:** 3 (Complex Platform) - Score: 39/60

**Recommended Architecture:**
- Pattern: Infrastructure-first (config → patterns → skill refactoring)
- Layers: Config layer → Pattern library → Skill integration
- Deployment: Framework enhancement (no new infrastructure)

**Technology Stack:**
- Configuration: YAML (parallel-orchestration.yaml)
- Auto-generation: Shell script (generate-subagent-registry.sh)
- Documentation: Markdown (CLAUDE.md, architecture-constraints.md)

## Risks & Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| Task dependency misdetection | HIGH | Dependency validation in config, explicit sequencing rules |
| JSON serialization freeze (50+ tasks) | MEDIUM | Cap at 6-8 concurrent, batch larger workloads |
| Blocking behavior bug (#2382) | MEDIUM | Explicit "run in parallel" instruction, auto-accept |
| Backward compatibility | MEDIUM | Feature flag in config, graceful degradation |
| Documentation drift (registry) | MEDIUM | Auto-generation script, pre-commit hook |

## Dependencies

**Prerequisites:**
- Research complete (docs/enhancements/2025-12-04/) - DONE
- Claude Code Terminal v1.0.71+ (background tasks) - VERIFIED

**Dependents:**
- All future skills benefit from parallel patterns
- EPIC-010 (Parallel Story Development CI/CD) can leverage this infrastructure

## Implementation Roadmap

**Sprint 1 (Week 1): Infrastructure Foundation**
- STORY-XXX: Parallel configuration schema + validation
- STORY-XXX: Subagent registry auto-generation script
- STORY-XXX: Error handling patterns (partial, timeout, retry)

**Sprint 1 (Week 2): Core Skill Refactoring**
- STORY-XXX: devforgeai-orchestration parallel refactor
- STORY-XXX: devforgeai-development parallel refactor

**Sprint 2 (Week 1): Extended Skill Updates**
- STORY-XXX: devforgeai-qa parallel validation
- STORY-XXX: devforgeai-release parallel deployment

**Sprint 2 (Week 2): Documentation & Validation**
- STORY-XXX: Architecture documentation updates
- STORY-XXX: Performance validation (NFR compliance)

## Next Steps

1. **Sprint Planning:** Create Sprint via `/create-sprint` for EPIC-017
2. **Story Creation:** Break features into stories via `/create-story`
3. **Development:** Implement stories via `/dev STORY-XXX`

## References

### Primary Sources (Official Anthropic)
- [Introducing Claude Opus 4.5](https://www.anthropic.com/news/claude-opus-4-6) - "Very effective at managing a team of subagents"
- [Introducing advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use) - 37% token reduction evidence

### Research Artifacts
- Research Report: `docs/enhancements/2025-12-04/research/parallel-orchestration-research.md`
- Executive Summary: `docs/enhancements/2025-12-04/research/RESEARCH-074-EXECUTIVE-SUMMARY.md`
- Implementation Guide: `docs/enhancements/2025-12-04/research/parallel-orchestration-guide.md`
- Quick Reference: `docs/enhancements/2025-12-04/research/PARALLEL-PATTERNS-QUICK-REFERENCE.md`
- Extensibility Analysis: `docs/enhancements/2025-12-04/EXTENSIBILITY-ANALYSIS-REPORT.md`
