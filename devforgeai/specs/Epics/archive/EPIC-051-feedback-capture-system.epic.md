---
id: EPIC-051
title: Framework Feedback Capture System
business-value: Enable automatic observation capture from subagents and phases to create self-improving framework with actionable insights
status: Planning
priority: High
complexity-score: 30
architecture-tier: Tier 2
created: 2026-01-26
estimated-points: 30
target-sprints: 2
dependencies: []
brainstorm-source: BRAINSTORM-007-feedback-system-visibility.brainstorm.md
owner: Framework Owner
tech_lead: Claude (DevForgeAI)
team: DevForgeAI Core
---

# Framework Feedback Capture System

## Business Goal

Enable automatic capture of observations, patterns, and friction points from subagents and workflow phases to populate phase-state.json with actionable framework improvement insights.

**Success Metrics:**
- `observations[]` array populated for 80%+ of completed stories (vs 0% currently)
- 4 high-frequency subagents return observation data
- Reflexion data captured for all failed TDD phases
- Zero manual observation capture required

**Measurement Plan:**
- **Tracking:** Count stories with non-empty `observations[]` in phase-state.json after /dev completion
- **Baseline:** 0% (current - no observations captured)
- **Target:** 80%+ populated
- **Review frequency:** After each sprint

## Problem Statement

Framework owners experience inability to see feedback from phases/subagents/workflows because subagents don't return observation data and the feedback system (STORY-018) was added after core components existed. This results in a framework that can't self-improve, repeated friction going unaddressed, and loss of institutional knowledge.

**Root Cause (5 Whys):** Feedback system came after subagents; retrofitting has been deprioritized vs new features.

## Scope

### In Scope

1. **Subagent Observation Schema** - Add optional `observations[]` field to 4 subagent contracts
2. **Observation Extractor** - Create new subagent to mine existing outputs
3. **Phase State Integration** - Append observations to phase-state.json at phase exits
4. **Reflexion Pattern** - Capture verbal reflections when TDD phases fail

### Out of Scope

- **Inline display of observations** - Deferred to EPIC-052
- **Long-term memory persistence** - Deferred to EPIC-052
- **Pattern detection/aggregation** - Deferred to EPIC-052
- **UI dashboard for observations** - Not planned (terminal-only framework)
- **Observation editing/deletion by users** - Out of scope (write-only capture)
- **Retroactive observation capture for completed stories** - Only future stories

## User Stories

1. **As a** Framework Owner, **I want** subagents to automatically return observations during execution, **so that** I don't have to manually capture feedback.

2. **As a** Framework Architect (Claude), **I want** an observation extractor to mine existing subagent outputs, **so that** observations are captured even from subagents without explicit schema.

3. **As a** Framework Owner, **I want** phase-state.json to contain all observations from a story's lifecycle, **so that** I can review what happened in each phase.

4. **As a** Framework Architect (Claude), **I want** failed TDD phases to capture verbal reflections, **so that** retry attempts have context about what went wrong.

## Features

### Feature 1: Subagent Observation Schema

**Description:** Add optional `observations[]` field to 4 high-frequency subagent contracts enabling automatic insight capture without breaking existing invocations.

**Files to Modify:**
- `.claude/agents/test-automator.md` (lines TBD - add to Output section)
- `.claude/agents/code-reviewer.md` (lines TBD - add to Output section)
- `.claude/agents/backend-architect.md` (lines TBD - add to Output section)
- `.claude/agents/ac-compliance-verifier.md` (lines TBD - add to Output section)

**Observation Schema (add to each subagent's Output section):**
```yaml
# Optional observation output (EPIC-051)
observations:
  - category: friction | success | pattern | gap | idea | bug | warning
    note: "Human-readable observation text"
    severity: low | medium | high
    files: ["optional/file/paths.md"]  # Files related to observation
```

**Acceptance Criteria (for stories):**
- AC1: test-automator.md contains `observations:` schema in Output section
- AC2: code-reviewer.md contains `observations:` schema in Output section
- AC3: backend-architect.md contains `observations:` schema in Output section
- AC4: ac-compliance-verifier.md contains `observations:` schema in Output section
- AC5: Each schema is optional (subagents work without it)
- AC6: All 7 categories documented (friction, success, pattern, gap, idea, bug, warning)

**Estimated Effort:** Medium (8 story points)

### Feature 2: Observation Extractor Subagent

**Description:** Create new subagent that mines existing subagent outputs for observations without requiring schema changes to all subagents.

**File to Create:** `.claude/agents/observation-extractor.md`

**Extraction Rules (map existing output fields to observations):**

| Subagent | Source Field | Target Category | Condition |
|----------|--------------|-----------------|-----------|
| test-automator | `coverage_result.gaps[]` | gap | Any gap exists |
| test-automator | `test_failures[]` | friction | Any failure exists |
| code-reviewer | `issues[].severity == "high"` | friction | High severity issues |
| code-reviewer | `issues[].severity == "medium"` | warning | Medium severity issues |
| backend-architect | `pattern_compliance.violations[]` | pattern | Any violation exists |
| ac-compliance-verifier | `verification_results[].status == "FAIL"` | gap | Any AC fails |

**Note:** Source fields reference existing subagent output schemas. If field doesn't exist in subagent output, extraction skips silently.

**Invocation Pattern:**
```markdown
# Called by phase files at exit gate
Task(subagent_type="observation-extractor",
     prompt="Extract observations from phase {phase_number} subagent outputs",
     context="{subagent_output_json}")
```

**Acceptance Criteria (for stories):**
- AC1: observation-extractor.md created in `.claude/agents/`
- AC2: Extraction rules for test-automator implemented
- AC3: Extraction rules for code-reviewer implemented
- AC4: Extraction rules for backend-architect implemented
- AC5: Extraction rules for ac-compliance-verifier implemented
- AC6: Silent skip when source field doesn't exist (no errors)

**Estimated Effort:** Medium (8 story points)

### Feature 3: Phase State Integration

**Description:** Automatically append captured observations to `observations[]` array in phase-state.json at phase exit gates.

**Files to Modify:**
- `.claude/skills/devforgeai-development/phases/phase-02-test-first.md` - Add observation capture before exit
- `.claude/skills/devforgeai-development/phases/phase-03-implementation.md` - Add observation capture before exit
- `.claude/skills/devforgeai-development/phases/phase-04-refactoring.md` - Add observation capture before exit
- `.claude/skills/devforgeai-development/phases/phase-05-integration.md` - Add observation capture before exit
- `.claude/skills/devforgeai-development/phases/phase-06-deferral.md` - Add observation capture before exit
- `.claude/skills/devforgeai-development/phases/phase-07-dod-update.md` - Add observation capture before exit
- `.claude/skills/devforgeai-development/phases/phase-08-git-workflow.md` - Add observation capture before exit

**Integration Pattern (add to each phase file's exit gate):**
```markdown
### Observation Capture (EPIC-051)

Before exiting this phase:

1. Collect explicit observations from subagent returns (if observations[] present)
2. Invoke observation-extractor for implicit observations
3. Append to phase-state.json observations array:

```json
{
  "observations": [
    {
      "id": "OBS-{phase}-{timestamp}",
      "phase": "{phase_number}",
      "category": "{category}",
      "note": "{observation_text}",
      "severity": "{low|medium|high}",
      "files": [],
      "source": "explicit|extracted",
      "timestamp": "{ISO8601}"
    }
  ]
}
```

**Acceptance Criteria (for stories):**
- AC1: Phase 02 captures observations before exit
- AC2: Phase 03 captures observations before exit
- AC3: Phases 04-08 capture observations before exit
- AC4: Observations have unique IDs (OBS-{phase}-{timestamp})
- AC5: Observations persist in phase-state.json after phase completion
- AC6: Both explicit (subagent return) and extracted observations captured

**Estimated Effort:** Small (6 story points)

### Feature 4: Reflexion Pattern for TDD Retry

**Description:** Store verbal reflections when TDD phases fail, enabling improved retry success through contextual learning.

**File to Modify:** `.claude/skills/devforgeai-development/references/tdd-red-phase.md` (and green/refactor phases)

**Reflection Schema (add to phase-state.json on failure):**
```json
{
  "reflections": [
    {
      "id": "REF-{phase}-{timestamp}",
      "phase": "02",
      "failed": true,
      "iteration": 1,
      "reflection": {
        "what_happened": "Tests failed with assertion error on line 45",
        "why_it_failed": "Expected value was outdated after AC clarification",
        "how_to_improve": "Re-read AC before writing assertions"
      },
      "timestamp": "{ISO8601}"
    }
  ]
}
```

**Trigger:** When phase fails validation and triggers retry:
```markdown
# On phase failure (before retry)
IF phase_failed:
    1. Generate reflection using self-analysis
    2. Append to phase-state.json reflections[]
    3. On retry, read previous reflections for context
```

**Acceptance Criteria (for stories):**
- AC1: Reflection schema added to phase-state.json structure
- AC2: Phase 02 captures reflection on test failure
- AC3: Phase 03 captures reflection on implementation failure
- AC4: Phase 04 captures reflection on refactoring failure
- AC5: Retry workflow reads previous reflections for context
- AC6: Reflections have unique IDs (REF-{phase}-{timestamp})

**Estimated Effort:** Medium (8 story points)

## Target Sprints

### Sprint 1: Foundation (Week 1)
**Goal:** Establish observation schema and extractor
**Estimated Points:** 16

**Stories:**
- STORY-318: Add Observation Schema to High-Frequency Subagents (8 pts) ✅ CREATED
  - Covers all 4 subagents: test-automator, code-reviewer, backend-architect, ac-compliance-verifier
- STORY-319: Create Observation Extractor Subagent (8 pts) ✅ CREATED

**Key Deliverables:**
- 4 subagent contracts updated with optional observations schema
- observation-extractor subagent operational

### Sprint 2: Integration (Week 2)
**Goal:** Integrate observation capture into phase workflow
**Estimated Points:** 14

**Stories:**
- STORY-336: Add Observation Capture to Phases 02-04 (6 pts) ✅ CREATED
- STORY-337: Add Observation Capture to Phases 05-08 (4 pts) ✅ CREATED
- STORY-338: Implement Reflexion Pattern for TDD Retry (4 pts) ✅ CREATED

**Key Deliverables:**
- All phases capture observations
- Failed phases capture reflections
- phase-state.json populated with observations

## Requirements Summary

### Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1 | Subagents return optional observations[] field | MUST |
| FR-2 | Observations have 7 categories (friction, success, pattern, gap, idea, bug, warning) | MUST |
| FR-3 | Observation extractor mines existing outputs | MUST |
| FR-4 | Phase exits append observations to phase-state.json | MUST |
| FR-5 | Failed phases capture verbal reflection | MUST |
| FR-6 | Backward compatible (optional fields) | MUST |

### Data Model

**Entities:**
- Observation: id, phase, category, note, severity, files[], source, timestamp
- Reflection: id, phase, failed, iteration, reflection{what/why/how}, timestamp
- Phase State: existing structure + observations[], reflections[]

**Relationships:**
- Phase State → many Observations
- Phase State → many Reflections (on failures)

### Non-Functional Requirements

**Performance:**
- Observation capture adds <100ms per phase

**Compatibility:**
- All changes backward compatible
- Existing subagent invocations unchanged

## Architecture Considerations

**Complexity Tier:** 2 (Moderate Application)

**Recommended Architecture:**
- Pattern: Extend existing subagent contracts with optional field
- Integration: Hook into phase exit gate workflow
- Storage: JSON in phase-state.json (existing pattern)

**Technology Recommendations:**
- Markdown subagent contracts (existing)
- JSON phase state files (existing)
- Claude Code tools only (constitutional)

## Risks & Mitigations

| Risk | Probability | Impact | Severity | Mitigation | Contingency |
|------|-------------|--------|----------|------------|-------------|
| Two-hat cognitive load | High | Medium | HIGH | Move capture to subagent returns, not manual reflection | Simplify to extraction-only |
| Observation noise | Medium | Low | MEDIUM | Define 7 specific categories with severity levels | Add filtering in display |
| Incomplete extraction rules | Medium | Medium | MEDIUM | Test against historical subagent outputs | Iteratively add rules |
| Subagent output format varies | Medium | Medium | MEDIUM | Define extraction rules per subagent type | Silent skip on missing fields |

## Dependencies

### Internal Dependencies
- [ ] **None** - This is a foundational epic
  - **Status:** N/A
  - **Impact if delayed:** N/A

### External Dependencies
- [ ] **None** - Framework-internal only

## Stakeholders

### Primary Stakeholders
- **Framework Owner (User):** Wants to see what's happening during development
- **Framework Architect (Claude):** Captures observations during execution

### Additional Stakeholders
- **Future Users:** Will benefit from framework self-improvement

## Hypotheses to Validate

| ID | Hypothesis | Success Criteria |
|----|------------|------------------|
| H1 | Adding observation schema will capture data automatically | phase-state.json `observations[]` populated for 80%+ stories |
| H3 | Automatic capture is better than manual reflection | Observation count increases vs manual capture |
| H4 | Verbal reflections improve retry success | TDD iteration counts decrease over time |

## Timeline

```
Epic Timeline:
════════════════════════════════════════════════════
Week 1:  Sprint 1 - Foundation (schema + extractor)
Week 2:  Sprint 2 - Integration (phases + reflexion)
════════════════════════════════════════════════════
Total Duration: 2 weeks
Target Release: February 9, 2026
```

### Key Milestones
- [ ] **Milestone 1:** Feb 2, 2026 - All 4 subagent schemas updated
- [ ] **Milestone 2:** Feb 2, 2026 - Observation extractor operational
- [ ] **Milestone 3:** Feb 9, 2026 - Phase integration complete
- [ ] **Final Release:** Feb 9, 2026 - EPIC-051 complete, EPIC-052 unblocked

## Progress Tracking

### Sprint Summary

| Sprint | Status | Points | Stories | Completed | In Progress | Blocked |
|--------|--------|--------|---------|-----------|-------------|---------|
| Sprint 1 | Not Started | 16 | 5 | 0 | 0 | 0 |
| Sprint 2 | Not Started | 14 | 3 | 0 | 0 | 0 |
| **Total** | **0%** | **30** | **8** | **0** | **0** | **0** |

## Next Steps

1. **Story Creation:** Run `/create-story` for each Feature 1-4 story
2. **Sprint Planning:** Create Sprint-N with Sprint 1 stories
3. **Implementation:** Begin with test-automator subagent (highest frequency)

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-26 | Epic created from BRAINSTORM-007 ideation | DevForgeAI Ideation |
| 2026-01-26 | Added missing sections per constitutional audit | DevForgeAI Ideation |
| 2026-01-30 | STORY-336 created (Add Observation Capture to Phases 02-04) | /create-story batch |
| 2026-01-30 | STORY-337 created (Add Observation Capture to Phases 05-08) | /create-story batch |
| 2026-01-30 | STORY-338 created (Implement Reflexion Pattern for TDD Retry) | /create-story batch |
