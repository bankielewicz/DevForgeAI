---
id: EPIC-003
title: Self-Improvement Automation
business-value: Enable agents to automatically learn and improve from execution without human intervention, achieving truly self-evolving agent experts
status: Backlog
priority: P2
complexity-score: 44
architecture-tier: Tier 3
created: 2025-12-16
estimated-points: 25
target-sprints: 3-4
dependencies: [EPIC-021, EPIC-022]
research_references: []
---

# Self-Improvement Automation

## Business Goal

Implement automatic learning workflows that analyze agent execution, detect patterns, and update expertise files without human intervention, transforming static agents into self-evolving domain experts.

**Success Metrics:**
- **Autonomous learning:** 95% of expertise updates happen automatically (threshold triggers, not manual /self-improve commands)
- **Learning accuracy:** 85% of auto-learned facts remain valid after 30 days (low churn rate)
- **Coverage growth:** Expertise files grow by 20-30% per month as agents accumulate knowledge

## Features

### Feature 1: Self-Improvement Workflow
**Description:** Core workflow that analyzes agent execution context, identifies new learnings, and updates expertise files automatically.

**User Stories (high-level):**
1. As an agent expert, I want to analyze my execution context after completing work, so that I can identify new learnings
2. As an agent expert, I want to extract patterns (repeated file paths, common entities, frequent user questions), so that I build mental model
3. As an agent expert, I want to validate new learnings against existing expertise, so that I don't duplicate or contradict
4. As an agent expert, I want to update expertise file with new knowledge, so that future executions leverage learnings
5. As an agent expert, I want to prune outdated learnings (if pattern no longer valid), so that expertise remains accurate

**Estimated Effort:** Large (10 story points)

### Feature 2: Threshold-Based Triggers
**Description:** Execution counter-based triggering that activates self-improvement after N agent executions, balancing learning frequency with overhead.

**User Stories (high-level):**
1. As an execution history tracker, I want to increment execution_count after each agent run, so that threshold detection works
2. As a threshold evaluator, I want to check if execution_count >= threshold (default: 10), so that self-improvement triggers automatically
3. As an agent expert, I want to configure my own threshold (5, 10, 20 executions), so that learning frequency matches domain complexity
4. As a system, I want to reset execution_count after self-improvement completes, so that cycle repeats
5. As a user, I want to see when next self-improvement will trigger (X executions remaining), so that I understand agent learning cadence

**Estimated Effort:** Small (4 story points)

### Feature 3: Hook Integration
**Description:** Integrate self-improvement with DevForgeAI post-execution hooks (post-dev, post-qa, post-release) to trigger learning after operations complete.

**User Stories (high-level):**
1. As a post-dev hook, I want to detect which domain experts were used during /dev, so that I can trigger their self-improvement
2. As a post-dev hook, I want to check execution threshold for each expert, so that only ready experts trigger learning
3. As a post-qa hook, I want to trigger self-improvement for validation-related experts, so that QA insights are captured
4. As a post-release hook, I want to trigger self-improvement for deployment experts, so that release patterns are learned
5. As a hook system, I want to invoke self-improvement asynchronously (background), so that user workflow isn't blocked

**Estimated Effort:** Medium (5 story points)

### Feature 4: Staleness Detection & Auto-Invalidation
**Description:** Detect when codebase changes significantly (schema migrations, API changes) and automatically invalidate stale expertise, triggering re-learning.

**User Stories (high-level):**
1. As an agent expert, I want to track file modification timestamps in my validation rules, so that I can detect codebase changes
2. As an agent expert, I want to compare current codebase state with mental model expectations, so that I detect staleness
3. As an agent expert, I want to mark expertise as STALE if >30% of facts are invalid, so that users see warning
4. As an agent expert, I want to trigger full re-learning workflow when marked STALE, so that mental model is rebuilt
5. As a user, I want to be notified when expert is re-learning (due to staleness), so that I understand accuracy may be temporarily reduced

**Estimated Effort:** Medium (6 story points)

### Feature 5: /self-improve Command
**Description:** Manual expertise update command for user-initiated learning (e.g., after making codebase changes not detected automatically).

**User Stories (high-level):**
1. As an engineer, I want to run /self-improve [expert-name], so that I manually trigger learning for specific expert
2. As a command, I want to analyze recent execution history for the expert, so that I have context for learning
3. As a command, I want to invoke self-improvement workflow (Feature 1), so that expertise file is updated
4. As a command, I want to display learning summary (X new patterns, Y facts pruned), so that user sees what changed
5. As an engineer, I want to run /self-improve --all, so that all experts are updated simultaneously

**Estimated Effort:** Small (3 story points)

### Feature 6: internet-sleuth Integration
**Description:** Invoke internet-sleuth agent for knowledge updates beyond LLM training cutoff (API changes, library updates, new best practices).

**User Stories (high-level):**
1. As an agent expert, I want to detect when my domain involves external APIs/libraries, so that I know research is needed
2. As an agent expert, I want to invoke internet-sleuth to research latest API documentation, so that expertise includes current info
3. As an agent expert, I want to compare research findings with my mental model, so that I can update outdated assumptions
4. As an internet-sleuth agent, I want to report back findings (API changes, deprecated methods, new features), so that expert can learn
5. As an agent expert, I want to cache research results (valid for 30 days), so that I don't research repeatedly

**Estimated Effort:** Medium (5 story points)

### Feature 7: Feedback Complement Integration
**Description:** Ensure Meta-Agentic learning complements (not replaces) devforgeai-feedback retrospective system, creating two parallel learning streams.

**User Stories (high-level):**
1. As a feedback system, I want to capture retrospective insights (what went well, challenges, improvements), so that process evolves
2. As a meta-agentic system, I want to capture runtime learnings (codebase patterns, domain knowledge), so that expertise accumulates
3. As a user, I want to see both feedback summaries AND expertise growth, so that I understand system evolution holistically
4. As a feedback hook, I want to trigger alongside meta-agentic hooks (not replace), so that both systems run
5. As a system, I want to optionally feed feedback insights into expertise updates, so that user suggestions inform agent learning

**Estimated Effort:** Small (2 story points)

## Requirements Summary

### Functional Requirements
- Self-improvement workflow (analyze execution, extract patterns, update expertise)
- Threshold-based triggers (execution counter → auto-learning)
- Hook integration (post-dev, post-qa, post-release)
- Staleness detection and auto-invalidation
- /self-improve command (manual triggering)
- internet-sleuth integration (knowledge updates)
- Feedback complement (parallel learning streams)

### Data Model

**Entities:**
- **Self-Improvement Execution** (transient, not persisted)
  - expert_id: string
  - execution_context: dict (files accessed, operations performed, outcomes)
  - extracted_learnings: list (new patterns discovered)
  - validation_results: dict (existing facts verified as still valid)
  - update_summary: dict (facts added, facts pruned, accuracy score)

- **Staleness Report** (embedded in expertise file metrics)
  - last_validation: datetime
  - validation_failures: integer (count of failed validation checks)
  - staleness_flag: boolean (true if >30% validation failures)
  - re_learning_triggered: datetime (when re-learning started)

- **Research Cache** (for internet-sleuth integration)
  - expert_id: string
  - research_topic: string (e.g., "Stripe API latest version")
  - research_date: datetime
  - findings: dict (API changes, new features, deprecations)
  - cache_expiration: datetime (research_date + 30 days)

**Relationships:**
- Self-Improvement Execution → Expertise File: one-to-one (updates specific expert)
- Staleness Report → Expertise File: embedded (part of metrics)
- Research Cache → Expertise File: one-to-many (one expert may have multiple cached research topics)

### Integration Points
1. **EPIC-001 Expertise System** - Read/write expertise files, update execution history
2. **EPIC-002 Meta-Generation Layer** - Trigger self-improvement for meta-generated experts
3. **DevForgeAI hook system** - post-dev, post-qa, post-release hooks
4. **internet-sleuth agent** - Research latest knowledge beyond LLM cutoff
5. **devforgeai-feedback skill** - Parallel learning stream (complement, not replace)

### Non-Functional Requirements

**Performance:**
- Self-improvement workflow: <30s to analyze execution and update expertise
- Threshold check: <1s to evaluate if threshold reached
- Hook invocation: <2s to trigger self-improvement asynchronously
- Staleness detection: <10s to validate mental model against codebase

**Quality:**
- Learning accuracy: 85% of auto-learned facts remain valid after 30 days
- Staleness detection recall: 95% of stale expertise is correctly detected
- Hook reliability: 99% of post-execution hooks successfully trigger
- False positive rate: <10% of staleness detections are false alarms

**Automation:**
- Autonomous learning rate: 95% of updates happen automatically (not manual /self-improve)
- Background execution: 100% of hook-triggered self-improvements run in background (non-blocking)

## Architecture Considerations

**Complexity Tier:** Tier 3 (Complex Platform, 44/60)

**Recommended Architecture:**
- Pattern: Event-Driven Architecture + Clean Architecture
- Layers:
  - **Domain Layer:** Self-improvement logic, learning algorithms, validation
  - **Application Layer:** Workflow orchestration, threshold evaluation, hook handlers
  - **Infrastructure Layer:** Hook system, file I/O, internet-sleuth invocation
  - **Presentation Layer:** /self-improve command
- Event Flow:
  1. Agent completes execution → Hook fires → Increment execution_count
  2. Check threshold → If reached → Trigger self-improvement workflow
  3. Analyze context → Extract learnings → Validate → Update expertise
  4. Optionally invoke internet-sleuth → Incorporate research → Cache results
- Database: File-based (update expertise files from EPIC-001, execution history from EPIC-001)
- Deployment: Integrated into DevForgeAI framework

**Technology Recommendations:**
- Hook System: Bash scripts in `.claude/hooks/` (already implemented)
- Background Execution: Bash `&` for async hook invocation
- Staleness Detection: File timestamp comparison + validation rule checks
- Pattern Extraction: Claude's native analysis (no external ML models)

## Risks & Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| Self-improvement corrupts expertise files | CRITICAL | Atomic writes (write to temp, rename), backup before update, rollback on validation failure |
| Learning extracts wrong patterns (false positives) | HIGH | Confidence scoring, require pattern seen 3+ times before adding to expertise |
| Threshold triggers too frequently (performance impact) | MEDIUM | Configurable thresholds (default 10), async execution prevents blocking |
| Staleness detection misses real changes | MEDIUM | Multiple validation strategies (file timestamps, content comparison, validation rules) |
| internet-sleuth research is slow | LOW | Cache research results for 30 days, trigger research asynchronously |
| Hook failures silently skip self-improvement | MEDIUM | Hook logging, alert on hook failures, retry mechanism (3 attempts) |

## Dependencies

**Prerequisites:**
- **EPIC-001 (Expertise System Foundation)** - Required for expertise file schema and execution history
- **EPIC-002 (Meta-Generation Layer)** - Required for meta-generated experts to learn from

**Dependents:**
- None (this is the final epic in Meta-Agentic MVP)

## Next Steps

1. **Story Creation:** Break features into stories via `/create-story [feature-description]`
   - Story 1: Implement core self-improvement workflow
   - Story 2: Build threshold-based trigger mechanism
   - Story 3: Integrate with post-dev, post-qa, post-release hooks
   - Story 4: Implement staleness detection algorithm
   - Story 5: Create /self-improve command
   - Story 6: Integrate internet-sleuth for knowledge updates

2. **Sprint Planning:** Add Feature 1-3 to Sprint 4, Feature 4-7 to Sprint 5

3. **Testing Strategy:**
   - Simulate agent executions to trigger thresholds
   - Test self-improvement workflow with sample expertise files
   - Validate hook integration (post-dev, post-qa, post-release)
   - Test staleness detection with intentionally outdated expertise
   - Verify internet-sleuth integration with real API research
   - Measure learning accuracy over 30-day period

4. **Release Readiness:**
   - After EPIC-003 completes, Meta-Agentic MVP is ready
   - Documentation: User guide for /create-meta-expert and /self-improve commands
   - Demo: Create database-expert, trigger self-improvement, show expertise growth
   - Feedback: Collect user feedback on autonomous learning quality
