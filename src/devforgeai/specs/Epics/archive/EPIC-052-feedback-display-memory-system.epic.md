---
id: EPIC-052
title: Framework Feedback Display & Memory System
business-value: Display captured observations inline during /dev workflow and persist patterns across sessions for continuous framework improvement
status: Planning
priority: High
complexity-score: 30
architecture-tier: Tier 2
created: 2026-01-26
estimated-points: 35
target-sprints: 2
dependencies:
  - EPIC-051
brainstorm-source: BRAINSTORM-007-feedback-system-visibility.brainstorm.md
owner: Framework Owner
tech_lead: Claude (DevForgeAI)
team: DevForgeAI Core
---

# Framework Feedback Display & Memory System

## Business Goal

Display captured observations inline during /dev workflow completion and implement multi-layer memory system for cross-session pattern learning, enabling visible framework self-improvement.

**Success Metrics:**
- Framework Insights displayed in 100% of /dev completions (Phase 10)
- Users report seeing feedback during workflow (vs searching files manually)
- Cross-story patterns detected and surfaced (3+ occurrence threshold)
- Session memory files created for each story

**Measurement Plan:**
- **Tracking:** Grep for "Framework Insights" in /dev terminal output
- **Baseline:** 0% (current - no inline display)
- **Target:** 100% display rate
- **Review frequency:** After each sprint

## Problem Statement

Even when observations are captured (EPIC-051), framework owners can't see insights during workflow execution because dev-result-interpreter doesn't read Phase 09 ai-analysis output. Users must manually search files in `devforgeai/feedback/ai-analysis/` to find insights.

**Visibility Gap:** Inline display will increase feedback visibility and user engagement with framework improvement recommendations.

## Scope

### In Scope

1. **Inline Display** - Modify dev-result-interpreter to show Framework Insights at Phase 10
2. **Session Memory** - Per-story observation persistence during story lifecycle
3. **Long-Term Memory** - Cross-story pattern learning files
4. **Memory Aggregation** - Surface relevant patterns in TDD phases

### Out of Scope

- **Observation capture** - Implemented in EPIC-051 (prerequisite)
- **Real-time streaming of observations** - Only display at Phase 10 completion
- **Memory editing UI** - No user interface for modifying memory files
- **Memory export/import** - Memory files are internal-only
- **Memory search/query interface** - Simple file-based storage only
- **External memory integration** - No connection to external databases or APIs
- **Memory versioning/history** - Files are append-only, no historical views

## Prerequisites

### ADR Required: Source Tree Update

**CRITICAL:** This epic requires an ADR to update `devforgeai/specs/context/source-tree.md` before implementation.

**New directories needed:**
```
.claude/memory/
├── sessions/           # NEW: Per-story session memory
│   └── {STORY-ID}-session.md
└── learning/           # NEW: Cross-story pattern learning
    ├── tdd-patterns.md
    ├── friction-catalog.md
    └── success-patterns.md
```

**ADR Reference:** ADR-XXX (to be created in Sprint 1, Story 1)

**Rationale:** source-tree.md (lines 291-302) only shows `.claude/memory/` with reference files, not session/learning subdirectories. Constitutional compliance requires ADR approval before creating new directories.

## User Stories

1. **As a** Framework Owner, **I want** to see Framework Insights at the end of /dev workflow, **so that** I don't have to search files manually.

2. **As a** Framework Owner, **I want** each story to have a session memory file, **so that** all observations from the story lifecycle are consolidated.

3. **As a** Framework Architect (Claude), **I want** long-term memory files to accumulate patterns, **so that** I can learn from past stories.

4. **As a** Framework Architect (Claude), **I want** relevant patterns surfaced during TDD phases, **so that** I can avoid repeating mistakes.

## Features

### Feature 1: Inline Display in dev-result-interpreter

**Description:** Modify dev-result-interpreter subagent to read Phase 09 ai-analysis output and display "Framework Insights" section at Phase 10 workflow completion.

**File to Modify:** `.claude/agents/dev-result-interpreter.md`

**ai-analysis.json Schema (Phase 09 output location):**
```
devforgeai/feedback/ai-analysis/{STORY_ID}/ai-analysis.json
```

**Expected JSON Structure:**
```json
{
  "story_id": "STORY-XXX",
  "timestamp": "2026-01-26T12:00:00Z",
  "what_worked_well": [
    "TDD cycle completed in single iteration",
    "AC verification passed on first attempt"
  ],
  "areas_for_improvement": [
    "Test coverage could be higher in edge cases",
    "Phase 03 took longer than average"
  ],
  "recommendations": [
    {
      "recommendation": "Add edge case tests upfront",
      "estimated_effort": "small",
      "priority": "medium"
    }
  ],
  "patterns_observed": ["clean-tdd-cycle", "first-time-pass"],
  "anti_patterns_detected": []
}
```

**Display Template (add to dev-result-interpreter output):**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Framework Insights (Phase 09 Analysis)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

What Worked Well:
  ✓ {what_worked_well[0]}
  ✓ {what_worked_well[1]}
  ✓ {what_worked_well[2]}

Areas for Improvement:
  ⚠ {areas_for_improvement[0]}
  ⚠ {areas_for_improvement[1]}

Top Recommendations:
  1. {recommendations[0].recommendation} ({recommendations[0].estimated_effort})
  2. {recommendations[1].recommendation} ({recommendations[1].estimated_effort})

Full analysis: devforgeai/feedback/ai-analysis/{STORY_ID}/
```

**Fallback (when ai-analysis.json doesn't exist):**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Framework Insights
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
No framework insights captured for this story.
Enable Phase 09 feedback hooks for AI analysis.
```

**Acceptance Criteria (for stories):**
- AC1: dev-result-interpreter reads ai-analysis.json from `devforgeai/feedback/ai-analysis/{STORY_ID}/`
- AC2: Framework Insights section displays at Phase 10 output
- AC3: Top 3 items per category displayed (what_worked, improvements, recommendations)
- AC4: Graceful fallback when ai-analysis.json doesn't exist
- AC5: File path to full analysis shown

**Estimated Effort:** Medium (8 story points)

### Feature 2: Session Memory Layer

**Description:** Create per-story session memory that persists observations throughout story lifecycle and archives on completion.

**File Location:** `.claude/memory/sessions/{STORY_ID}-session.md`

**Session Memory Schema:**
```markdown
---
story_id: STORY-XXX
created: 2026-01-26T12:00:00Z
last_updated: 2026-01-26T14:30:00Z
status: active | archived
---

# Session Memory: STORY-XXX

## Observations

### Phase 02 (Test-First)
- [gap] Coverage gap identified in edge cases (high)
- [success] All AC tests written successfully (medium)

### Phase 03 (Implementation)
- [friction] Type mismatch required refactoring (medium)
- [pattern] Used repository pattern effectively (low)

### Phase 04 (Refactor)
- [success] Reduced cyclomatic complexity from 12 to 6 (high)

## Reflections

### Reflection 1 (Phase 03, Iteration 2)
- **What happened:** Implementation failed type check
- **Why it failed:** Misread AC#2 expected return type
- **How to improve:** Verify AC types before implementing

## Subagent Invocations

| Timestamp | Subagent | Phase | Duration |
|-----------|----------|-------|----------|
| 12:01:00 | test-automator | 02 | 45s |
| 12:05:00 | backend-architect | 03 | 120s |
| 12:10:00 | code-reviewer | 03 | 30s |

## Phase Progression

| Phase | Started | Completed | Iterations |
|-------|---------|-----------|------------|
| 02 | 12:00:00 | 12:05:00 | 1 |
| 03 | 12:05:00 | 12:15:00 | 2 |
| 04 | 12:15:00 | 12:20:00 | 1 |
```

**Lifecycle:**
1. **Create:** At Phase 01 (Preflight) completion
2. **Update:** After each phase exit (append observations)
3. **Archive:** At story completion (move to `sessions/archive/` or mark status: archived)

**Acceptance Criteria (for stories):**
- AC1: Session memory file created at Phase 01 completion
- AC2: Observations appended after each phase exit
- AC3: Session memory archived on story completion
- AC4: Schema matches specification above
- AC5: Stale session files (>7 days, no updates) cleaned up

**Estimated Effort:** Medium (8 story points)

### Feature 3: Long-Term Memory Layer

**Description:** Create cross-story pattern learning files that accumulate insights across multiple story completions.

**File Locations (require ADR for source-tree.md update):**
- `.claude/memory/learning/tdd-patterns.md`
- `.claude/memory/learning/friction-catalog.md`
- `.claude/memory/learning/success-patterns.md`

**tdd-patterns.md Schema:**
```markdown
---
last_updated: 2026-01-26T12:00:00Z
total_patterns: 15
version: 1.0
---

# TDD Patterns Learned

## Pattern: clean-tdd-cycle
**Occurrences:** 12
**Confidence:** high (>10 occurrences)
**Last Seen:** STORY-320

**Description:** TDD cycle completes with single iteration per phase

**When to Apply:**
- Story has clear, unambiguous AC
- No external dependencies
- Well-defined input/output contracts

**Examples:**
- STORY-305: Completed all phases in single iteration
- STORY-310: Zero reflections captured (no failures)

## Pattern: edge-case-gap
**Occurrences:** 8
**Confidence:** medium (5-10 occurrences)
**Last Seen:** STORY-318

**Description:** Edge case coverage gaps detected in Phase 02

**When to Apply:**
- AC mentions "all cases" or "any input"
- Data validation is involved

**Mitigation:**
- Add boundary tests explicitly
- Test null/empty/max values
```

**friction-catalog.md Schema:**
```markdown
---
last_updated: 2026-01-26T12:00:00Z
total_friction_points: 23
version: 1.0
---

# Friction Catalog

## Friction: type-mismatch-iteration
**Occurrences:** 6
**Confidence:** medium
**Avg Resolution Time:** 15 minutes

**Description:** Type mismatch between AC expectation and implementation

**Root Cause:** AC interpretation differs from implementation

**Solution:**
1. Read AC return type explicitly before implementing
2. Add type assertion in test before implementation
3. Use typed interfaces when available

**Stories Affected:**
- STORY-303: Phase 03 required 2 iterations
- STORY-315: Type error in API response
```

**Pattern Detection Algorithm:**
```
ON story_completion:
  1. Read session memory observations
  2. FOR each observation:
     a. Extract category + note keywords
     b. Hash to pattern_id (category + keyword_hash)
     c. IF pattern_id exists in long-term memory:
        - Increment occurrences
        - Update last_seen
        - Add story to examples (max 5)
     d. ELSE IF similar pattern exists (>70% keyword overlap):
        - Merge into existing pattern
        - Increment occurrences
     e. ELSE:
        - Create new pattern entry
        - Set occurrences = 1
        - Set confidence = low

  3. Update confidence levels:
     - occurrences >= 10 → high
     - occurrences >= 5 → medium
     - occurrences >= 3 → low
     - occurrences < 3 → emerging (not surfaced)
```

**Update Triggers:**
- After each story completes (QA Approved status)
- Triggered by hook: `post-qa-memory-update.sh` (to be created)

**Acceptance Criteria (for stories):**
- AC1: ADR created for source-tree.md update (prerequisite)
- AC2: tdd-patterns.md created with schema above
- AC3: friction-catalog.md created with schema above
- AC4: success-patterns.md created with schema above
- AC5: Pattern detection algorithm implemented per specification
- AC6: Patterns with <3 occurrences not surfaced (emerging only)
- AC7: Confidence levels calculated correctly (low/medium/high)

**Estimated Effort:** Large (12 story points)

### Feature 4: Memory Aggregation & Surfacing

**Description:** Combine session observations with long-term patterns to inform future TDD iterations with historical context.

**Integration Points:**

**Phase 02 (Test-First) - Surface TDD Patterns:**
```markdown
# Add to phase-02-test-first.md

### Memory Context (EPIC-052)

Before writing tests, check long-term memory:

1. Read `.claude/memory/learning/tdd-patterns.md`
2. Match story characteristics to pattern triggers
3. Surface relevant patterns:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Relevant TDD Patterns (from long-term memory)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Pattern: edge-case-gap (8 occurrences, medium confidence)
  → This story involves data validation
  → Recommendation: Add boundary tests explicitly
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
```

**Phase 03 (Implementation) - Surface Friction Warnings:**
```markdown
# Add to phase-03-implementation.md

### Friction Awareness (EPIC-052)

Before implementing, check friction catalog:

1. Read `.claude/memory/learning/friction-catalog.md`
2. Match implementation type to known friction points
3. Display warnings:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Friction Warning (from long-term memory)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Friction: type-mismatch-iteration (6 occurrences)
  → Stories with API responses often have type mismatches
  → Prevention: Verify AC return type before implementing
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
```

**Files to Modify:**
- `.claude/skills/devforgeai-development/phases/phase-02-test-first.md`
- `.claude/skills/devforgeai-development/phases/phase-03-implementation.md`

**Acceptance Criteria (for stories):**
- AC1: Phase 02 reads and surfaces relevant TDD patterns
- AC2: Phase 03 reads and surfaces friction warnings
- AC3: Pattern matching based on story characteristics (AC keywords, story type)
- AC4: Only patterns with confidence >= low (3+ occurrences) surfaced
- AC5: Display format matches specification above

**Estimated Effort:** Medium (7 story points)

## Target Sprints

### Sprint 1: Display & Session Memory (Week 3)
**Goal:** Inline display working, session memory operational
**Estimated Points:** 17

**Stories:**
- STORY-339: Create ADR for source-tree.md update (1 pt) - **PREREQUISITE** ✅ CREATED
- STORY-340: Add Framework Insights to dev-result-interpreter (8 pts) ✅ CREATED
- STORY-341: Create session memory file schema and writer (8 pts) ✅ CREATED

**Key Deliverables:**
- ADR approved for new directories
- Framework Insights visible at Phase 10
- Session memory created for each story

### Sprint 2: Long-Term Memory & Aggregation (Week 4)
**Goal:** Cross-story learning operational
**Estimated Points:** 18

**Stories:**
- STORY-342: Create long-term memory files and pattern detection (12 pts) ✅ CREATED
- STORY-343: Implement memory surfacing in phases 02-03 (6 pts) ✅ CREATED

**Key Deliverables:**
- Three long-term memory files operational
- Patterns surfaced during TDD phases
- Memory aggregation working

## Requirements Summary

### Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1 | Display Framework Insights at Phase 10 | MUST |
| FR-2 | Read Phase 09 ai-analysis output | MUST |
| FR-3 | Create session memory per story | MUST |
| FR-4 | Archive session memory on completion | MUST |
| FR-5 | Create 3 long-term memory files | MUST |
| FR-6 | Detect recurring patterns (3+ occurrences) | MUST |
| FR-7 | Surface relevant patterns in Phase 02-03 | SHOULD |

### Data Model

**Entities:**
- Session Memory: story_id, observations[], reflections[], invocations[], phases[]
- Long-Term Memory: patterns[] with pattern_id, occurrences, confidence, examples[]
- Pattern: category, description, when_to_apply, mitigation, stories_affected[]

**Relationships:**
- Story → one Session Memory
- Session Memory → aggregates to Long-Term Memory
- Long-Term Memory → informs future Stories

### Non-Functional Requirements

**Performance:**
- Memory read adds <50ms to phase startup
- Pattern aggregation runs synchronously after story completion

**Storage:**
- Session memory: ~5-20KB per story
- Long-term memory: ~50-100KB total (capped)
- Archive policy: Session files >30 days archived to `sessions/archive/`

## Architecture Considerations

**Complexity Tier:** 2 (Moderate Application)

**Recommended Architecture:**
- Pattern: Multi-layer memory (short-term + long-term)
- Storage: Markdown files in .claude/memory/
- Aggregation: Pattern detection via keyword hashing + frequency analysis

**Memory Architecture (requires ADR):**
```
.claude/memory/
├── sessions/                    # NEW (requires ADR)
│   ├── STORY-XXX-session.md    # Active session
│   └── archive/                 # Archived sessions
│       └── STORY-YYY-session.md
├── learning/                    # NEW (requires ADR)
│   ├── tdd-patterns.md
│   ├── friction-catalog.md
│   └── success-patterns.md
├── skills-reference.md          # EXISTING
├── commands-reference.md        # EXISTING
└── ...                          # Other existing files
```

## Risks & Mitigations

| Risk | Probability | Impact | Severity | Mitigation | Contingency |
|------|-------------|--------|----------|------------|-------------|
| ADR rejected | Low | High | HIGH | Pre-validate with stakeholders | Use flat files in existing .claude/memory/ |
| Memory file growth unbounded | Medium | Medium | MEDIUM | Cap long-term memory at 100KB, prune oldest | Archive to separate location |
| Pattern detection false positives | Medium | Low | MEDIUM | Require 3+ occurrences, confidence threshold | Allow manual pattern editing |
| Session memory conflicts | Low | Medium | LOW | Per-story isolation, atomic writes | Retry with file locking |
| Performance impact | Low | Low | LOW | Lazy loading, async aggregation | Cache frequently accessed patterns |

## Dependencies

### Internal Dependencies
- [x] **EPIC-051:** Framework Feedback Capture System
  - **Status:** Not Started (created same day)
  - **Impact if delayed:** Cannot display observations that don't exist

### External Dependencies
- [ ] **ADR-XXX:** Source tree update for new directories
  - **Owner:** Framework Architect
  - **ETA:** Sprint 1, Day 1
  - **Status:** Not Started

## Stakeholders

### Primary Stakeholders
- **Framework Owner (User):** Wants to see feedback inline without searching files
- **Framework Architect (Claude):** Benefits from historical patterns during TDD

### Additional Stakeholders
- **Future Users:** Will benefit from accumulated pattern knowledge

## Hypotheses to Validate

| ID | Hypothesis | Success Criteria |
|----|------------|------------------|
| H2 | Inline display will increase feedback visibility | Users report seeing feedback during /dev |
| H5 | Multi-layer memory enables learning | Cross-story patterns detected (3+ occurrences) |
| H6 | Historical context improves TDD success | Fewer repeated friction points over time |

## Market Research Integration

**From BRAINSTORM-007:**
- **Reflexion Pattern** (NeurIPS 2023): Verbal reflections improve retry success
- **TAO Cycle** (ReAct): Thought-Action-Observation loop
- **Multi-Layer Memory** (CrewAI): Short-term + long-term memory architecture
- **89% of production agents** have observability (LangChain State of AI 2026)

## Timeline

```
Epic Timeline:
════════════════════════════════════════════════════
Week 3:  Sprint 1 - Display & Session Memory
         (Prerequisite: EPIC-051 complete)
Week 4:  Sprint 2 - Long-Term Memory & Aggregation
════════════════════════════════════════════════════
Total Duration: 2 weeks
Target Release: February 23, 2026
Dependencies: EPIC-051 must complete by Feb 9, 2026
```

### Key Milestones
- [ ] **Milestone 0:** Feb 9, 2026 - EPIC-051 complete (prerequisite)
- [ ] **Milestone 1:** Feb 16, 2026 - ADR approved, inline display working
- [ ] **Milestone 2:** Feb 16, 2026 - Session memory operational
- [ ] **Milestone 3:** Feb 23, 2026 - Long-term memory and aggregation complete
- [ ] **Final Release:** Feb 23, 2026 - Full feedback visibility system operational

## Progress Tracking

### Sprint Summary

| Sprint | Status | Points | Stories | Completed | In Progress | Blocked |
|--------|--------|--------|---------|-----------|-------------|---------|
| Sprint 1 | Stories Created | 17 | 3 | 0 | 0 | 0 |
| Sprint 2 | Stories Created | 18 | 2 | 0 | 0 | 0 |
| **Total** | **100%** | **35** | **5** | **0** | **0** | **0** |

## Next Steps

1. **Wait for EPIC-051:** Must complete before starting EPIC-052
2. **Create ADR:** First story must create ADR for source-tree.md update
3. **Story Creation:** Run `/create-story` for each Feature 1-4 story
4. **Sprint Planning:** Create Sprint-N with Sprint 1 stories

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-26 | Epic created from BRAINSTORM-007 ideation | DevForgeAI Ideation |
| 2026-01-26 | Added missing sections per constitutional audit | DevForgeAI Ideation |
| 2026-01-26 | Added ADR requirement for source-tree.md update | DevForgeAI Ideation |
| 2026-01-30 | STORY-339 created (ADR for memory directories) | /create-story batch |
| 2026-01-30 | STORY-340 created (Framework Insights in dev-result-interpreter) | /create-story batch |
| 2026-01-30 | STORY-341 created (Session memory layer) | /create-story batch |
| 2026-01-30 | STORY-342 created (Long-term memory layer) | /create-story batch |
| 2026-01-30 | STORY-343 created (Memory surfacing in TDD phases) | /create-story batch |
