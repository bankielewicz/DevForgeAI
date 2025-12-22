---
id: SPRINT-2
name: User Input Guidance Implementation
epic: EPIC-011
start_date: 2025-01-21
end_date: 2025-02-04
duration_days: 14
status: Active
total_points: 40
completed_points: 0
stories:
  - STORY-052
  - STORY-053
  - STORY-054
  - STORY-055
  - STORY-056
  - STORY-057
  - STORY-058
  - STORY-059
  - STORY-060
created: 2025-01-20 20:45:00
---

# Sprint 2: User Input Guidance Implementation

## Overview

**Duration:** 2025-01-21 to 2025-02-04 (14 days)
**Capacity:** 40 story points
**Epic:** [User Input Guidance System](../Epics/EPIC-011-user-input-guidance-system.epic.md) (EPIC-011)
**Status:** Active

## Sprint Goals

Implement a comprehensive user input guidance system for DevForgeAI to:
- Reduce incomplete stories by 67% (40% → 13%)
- Improve token efficiency by 9% (save 10K tokens per story)
- Reduce iteration cycles by 52% (2.5 → 1.2 subagent re-invocations)
- Establish framework-wide consistency in user interaction patterns
- Enable faster, higher-quality story creation through proven communication patterns

## Stories

### In Progress (0 points)
[Empty - will be populated during sprint]

### Ready for Dev (40 points)

#### STORY-052: User-Facing Prompting Guide Documentation
- **Points:** 8
- **Priority:** Medium
- **Epic:** EPIC-011
- **Acceptance Criteria:** 6 criteria
- **Status:** Ready for Dev
- **Description:** Create comprehensive guide teaching users how to provide clear, complete input to DevForgeAI commands, with 20-30 before/after examples and command-specific guidance for all 11 commands.

#### STORY-053: Framework-Internal Guidance Reference
- **Points:** 8
- **Priority:** Medium
- **Epic:** EPIC-011
- **Acceptance Criteria:** 6 criteria
- **Status:** Ready for Dev
- **Description:** Create internal reference for skills with 10-15 elicitation patterns, 20-30 AskUserQuestion templates, and proven patterns for requirements discovery, NFR quantification, edge case identification, and integration point discovery.

#### STORY-054: claude-code-terminal-expert Prompting Guidance Enhancement
- **Points:** 3
- **Priority:** Medium
- **Epic:** EPIC-011
- **Acceptance Criteria:** 6 criteria
- **Status:** Ready for Dev
- **Description:** Add prompting guidance section to claude-code-terminal-expert skill with cross-references to both guidance documents and 5-10 effective vs ineffective communication examples.

#### STORY-055: devforgeai-ideation Skill Integration with User Input Guidance
- **Points:** 3
- **Priority:** Medium
- **Epic:** EPIC-011
- **Acceptance Criteria:** 5 criteria
- **Status:** Ready for Dev
- **Description:** Integrate user-input-guidance.md patterns into devforgeai-ideation skill Phase 1 (Requirements Discovery) and Phase 2 (Feature Elicitation), reducing requirements-analyst subagent re-invocations by 30%.

#### STORY-056: devforgeai-story-creation Skill Integration with User Input Guidance
- **Points:** 3
- **Priority:** Medium
- **Epic:** EPIC-011
- **Acceptance Criteria:** 7 criteria
- **Status:** Ready for Dev
- **Description:** Integrate user-input-guidance.md patterns into devforgeai-story-creation skill for epic selection, sprint assignment, story priority, and acceptance criteria capture, reducing story-requirements-analyst subagent failures by 25%.

#### STORY-057: Additional Skill Integrations (architecture, ui-generator, orchestration)
- **Points:** 5
- **Priority:** Medium
- **Epic:** EPIC-011
- **Acceptance Criteria:** 4 criteria
- **Status:** Ready for Dev
- **Description:** Integrate user-input-guidance.md patterns into devforgeai-architecture (greenfield context discovery), devforgeai-ui-generator (standalone UI creation), and devforgeai-orchestration (epic creation) skills for consistent user interaction across framework.

#### STORY-058: Documentation Updates with User Input Guidance Cross-References
- **Points:** 3
- **Priority:** Medium
- **Epic:** EPIC-011
- **Acceptance Criteria:** 5 criteria
- **Status:** Ready for Dev
- **Description:** Update CLAUDE.md with "Learning DevForgeAI" section, add cross-references to all 11 commands in commands-reference.md, and update skills-reference.md with guidance integration examples.

#### STORY-059: User Input Guidance Validation & Testing Suite
- **Points:** 5
- **Priority:** Medium
- **Epic:** EPIC-011
- **Acceptance Criteria:** 6 criteria
- **Status:** Ready for Dev
- **Description:** Create comprehensive test suite with 10 baseline vs enhanced feature descriptions, success rate measurement scripts, token savings analysis, and impact reporting to validate guidance system effectiveness.

#### STORY-060: Operational Sync for User Input Guidance System
- **Points:** 2
- **Priority:** Medium
- **Epic:** EPIC-011
- **Acceptance Criteria:** 6 criteria
- **Status:** Ready for Dev
- **Description:** Create automated sync script to synchronize source files (src/) to operational directories (.claude/, root CLAUDE.md), ensuring framework uses latest guidance documentation without manual copying errors.

### Completed (0 points)
[Empty - will be populated as stories complete]

## Sprint Metrics

- **Planned Velocity:** 40 points
- **Current Velocity:** 0 points (0%)
- **Stories Planned:** 9
- **Stories Completed:** 0
- **Days Remaining:** 14
- **Capacity Status:** ✅ Optimal (40 points within 20-40 recommended range for 14-day sprint)

## Daily Progress

[Will be updated during sprint execution]

## Retrospective Notes

[To be filled at sprint end]

## Next Steps

1. Review sprint stories and prioritize execution
2. Start first story: `/dev STORY-052` (User-Facing Prompting Guide)
3. Track progress daily
4. Update story statuses as work progresses
5. Complete sprint with: `/orchestrate STORY-052` (and continue through STORY-060)
