---
id: EPIC-034
title: Session Data Mining for Framework Intelligence
status: Planning
start_date: 2025-01-02
target_date: 2025-01-16
total_points: 31
completed_points: 0
created: 2025-01-02
owner: DevForgeAI Framework
tech_lead: Claude
team: DevForgeAI
plan_file: /home/bryan/.claude/plans/vast-sparking-shore.md
priority: Medium
complexity_score: 7
---

# Epic: Session Data Mining for Framework Intelligence

## Business Goal

Mine 86MB+ of Claude Code session data to extract workflow patterns, error analysis, and institutional knowledge that improves DevForgeAI framework effectiveness. Enable on-demand insights via `/insights` command to help developers:
- Identify successful command sequences and workflows
- Detect and prevent common errors and anti-patterns
- Access historical decisions for informed future choices
- Optimize development processes based on empirical data

## Success Metrics

- **Pattern Extraction:** Identify top 10 workflow patterns with >85% confidence
- **Error Reduction:** Track recovery success rates for top 10 error categories
- **Decision Archive:** Index 100% of plan files with <1 second search
- **Command Adoption:** /insights used successfully in 80%+ of invocations

**Measurement Plan:**
- Track command invocations via history.jsonl
- Monitor query execution times
- Survey user satisfaction with insight quality
- Review frequency: End of each sprint

## Scope

### In Scope

1. **Feature 1: Session Miner Subagent** (5 SP)
   - Foundation data extraction layer using native tools (Read, Glob, Grep)
   - Parse history.jsonl, session files, plan files, todo files
   - Return structured JSON for skill aggregation

2. **Feature 2: DevForgeAI Insights Skill + /insights Command** (8 SP)
   - User interface for invoking mining operations
   - Orchestration layer dispatching to session-miner subagent
   - Result formatting and caching

3. **Feature 3: Workflow Pattern Extraction** (5 SP)
   - Command sequence analysis and success/failure correlation
   - Phase duration estimates from timestamp analysis
   - Optimal ordering pattern identification

4. **Feature 4: Anti-Pattern & Error Mining** (5 SP)
   - Error categorization and taxonomy
   - Recovery success rate tracking
   - Constitutional anti-pattern detection

5. **Feature 5: Plan File Knowledge Base** (8 SP)
   - Full-text search across 350+ plan files
   - Decision-outcome correlation
   - Implementation pattern library

### Out of Scope

- Real-time streaming analysis (use pre-computation instead)
- External Python/Node dependencies for parsing
- Modification of session data (read-only analysis)
- Cross-project session aggregation (current project only)
- ML-based pattern recognition (rule-based only)

## Target Sprints

### Sprint 1: Foundation (13 SP)
**Goal:** Establish data extraction layer and user interface
**Estimated Points:** 13
**Features:**
- F1: Session Miner Subagent (5 SP) - 4 stories
- F2: Insights Skill + Command (8 SP) - 4 stories

**Key Deliverables:**
- `.claude/agents/session-miner.md`
- `.claude/skills/devforgeai-insights/SKILL.md`
- `.claude/commands/insights.md`
- `/insights` dashboard working

### Sprint 2: Mining Modes (10 SP)
**Goal:** Implement workflow and error mining capabilities
**Estimated Points:** 10
**Features:**
- F3: Workflow Pattern Extraction (5 SP) - 3 stories
- F4: Anti-Pattern & Error Mining (5 SP) - 3 stories

**Key Deliverables:**
- `/insights workflows` functional
- `/insights errors` functional
- Pattern detection algorithms

### Sprint 3: Knowledge Base (8 SP)
**Goal:** Complete decision archive with search
**Estimated Points:** 8
**Features:**
- F5: Plan File Knowledge Base (8 SP) - 4 stories

**Key Deliverables:**
- `/insights decisions [query]` functional
- Plan file indexing
- Outcome correlation

## User Stories

High-level user stories (18 total, decomposed in features):

1. **As a** DevForgeAI user, **I want** to see a dashboard of session insights, **so that** I understand my development patterns
2. **As a** DevForgeAI user, **I want** to discover successful workflow sequences, **so that** I can follow proven paths
3. **As a** DevForgeAI user, **I want** to identify common error categories, **so that** I can avoid repeated mistakes
4. **As a** DevForgeAI user, **I want** to search past decisions, **so that** I can learn from historical approaches
5. **As a** DevForgeAI user, **I want** story-specific insights, **so that** I can analyze individual implementations

## Technical Considerations

### Architecture Impact
- New subagent: `session-miner` (read-only, native tools)
- New skill: `devforgeai-insights` (orchestration)
- New command: `insights` (user interface)
- Cache directory: `devforgeai/cache/insights/`

### Technology Decisions
- **ADR REQUIRED:** Data processing architecture (pre-computation vs streaming)
- Native tools only (Read, Glob, Grep) per tech-stack.md
- JSONL parsing via structured Read operations
- Caching with simple TTL strategy

### Constitutional Compliance
| Constraint | Status |
|------------|--------|
| Native tools only | COMPLIANT |
| Skill < 1,000 lines | COMPLIANT (~600) |
| Command < 500 lines | COMPLIANT (~300) |
| Subagent < 500 lines | COMPLIANT (~300) |
| Zero dependencies | COMPLIANT |
| Subagent no skill invoke | COMPLIANT |

### Performance Requirements
- Index generation: < 2 minutes (one-time)
- Cached queries: < 10 seconds
- Archive search: < 1 second
- Support full history (23,995+ entries)

## Dependencies

### Internal Dependencies
- [x] **Context Files:** 6 constitutional files exist
  - **Status:** Complete
  - **Impact if missing:** Cannot validate compliance

### External Dependencies
- [ ] **ADR: Data Processing Architecture** (REQUIRED)
  - **Owner:** Tech Lead
  - **ETA:** Before Sprint 1
  - **Status:** Not Started

### Downstream Dependencies (This Epic Enables)
- **EPIC-032:** RCA Automation (uses error mining data)
- **EPIC-021:** Expertise System Foundation (uses decision archive)
- **EPIC-023:** Self-Improvement Automation (uses pattern insights)

## Risks & Mitigation

### Risk 1: 86MB Data Volume Causes Timeout
- **Probability:** HIGH
- **Impact:** HIGH
- **Mitigation:** Use pre-computation with lightweight index files instead of runtime streaming
- **Contingency:** Implement pagination with "first 1000 entries" quick mode

### Risk 2: Token Exhaustion During Parsing
- **Probability:** HIGH
- **Impact:** HIGH
- **Mitigation:** Grep pre-filtering before Read, chunked processing with offset/limit
- **Contingency:** External pre-processor script (Option B from architect review)

### Risk 3: Error Classification Inaccuracy
- **Probability:** MEDIUM
- **Impact:** MEDIUM
- **Mitigation:** Validate against 1000+ error samples before release
- **Contingency:** Manual error code registry with AskUserQuestion for unknowns

### Risk 4: Pattern Analysis Returns Obvious Results
- **Probability:** LOW
- **Impact:** LOW
- **Mitigation:** Frequency filtering (>5%) + semantic filtering
- **Contingency:** Add statistical significance thresholds

## Stakeholders

### Primary Stakeholders
- **Product Owner:** DevForgeAI Framework Team
- **Tech Lead:** Claude (AI orchestration)
- **User:** DevForgeAI developers

## Timeline

```
Epic Timeline:
════════════════════════════════════════════════════
Week 1:    Sprint 1 - Foundation (Session Miner + Skill)
Week 2:    Sprint 2 - Mining Modes (Workflows + Errors)
Week 3:    Sprint 3 - Knowledge Base (Decision Archive)
════════════════════════════════════════════════════
Total Duration: 2-3 weeks (1-2 sprints compressed)
Target Release: 2025-01-16
```

### Key Milestones
- [ ] **M1:** ADR approved for data processing architecture
- [ ] **M2:** /insights dashboard functional (end Sprint 1)
- [ ] **M3:** Workflow + Error mining complete (end Sprint 2)
- [ ] **M4:** Decision archive searchable (end Sprint 3)
- [ ] **Final Release:** All modes functional, QA approved

## Progress Tracking

### Sprint Summary

| Sprint | Status | Points | Stories | Completed | In Progress | Blocked |
|--------|--------|--------|---------|-----------|-------------|---------|
| Sprint 1 | Not Started | 13 | 8 | 0 | 0 | 0 |
| Sprint 2 | Not Started | 10 | 6 | 0 | 0 | 0 |
| Sprint 3 | Not Started | 8 | 4 | 0 | 0 | 0 |
| **Total** | **0%** | **31** | **18** | **0** | **0** | **0** |

### Burndown
- **Total Points:** 31
- **Completed:** 0
- **Remaining:** 31
- **Velocity:** TBD

## Technical Assessment Summary

**Complexity Score:** 7/10

**Assessment:** CHANGES RECOMMENDED (by architect-reviewer)

**Critical Issues to Address:**
1. Data volume streaming architecture - Requires ADR
2. Performance targets need revision (split index vs query)

**Recommended Actions:**
1. Create ADR for data processing architecture (REQUIRED)
2. Add cache location to source-tree.md
3. Define index schema before implementation

## Files to Create

| Component | Path | Size Target |
|-----------|------|-------------|
| Subagent | `.claude/agents/session-miner.md` | <500 lines |
| Skill | `.claude/skills/devforgeai-insights/SKILL.md` | <1000 lines |
| Skill Ref | `.claude/skills/devforgeai-insights/references/mining-patterns.md` | ~500 lines |
| Skill Ref | `.claude/skills/devforgeai-insights/references/output-formats.md` | ~300 lines |
| Command | `.claude/commands/insights.md` | <500 lines |

## Retrospective (Post-Epic)

*To be completed after epic completes*

---

**Epic Created:** 2025-01-02
**Plan Reference:** /home/bryan/.claude/plans/vast-sparking-shore.md
**Feature Decomposition By:** requirements-analyst (opus)
**Technical Assessment By:** architect-reviewer (opus)
