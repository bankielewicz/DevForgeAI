---
id: EPIC-032
title: RCA-to-Story Automation
business-value: Automate story creation from RCA recommendations to improve traceability and reduce manual effort
status: Planning
priority: High
complexity-score: 20
architecture-tier: Tier 2
created: 2025-12-24
estimated-points: 21-34
target-sprints: 1-2
epic: EPIC-032
---

# RCA-to-Story Automation

## Business Goal

Automate the generation of user stories from Root Cause Analysis (RCA) recommendations, providing:
- **Time Savings:** Reduce RCA→Story creation from 15-30 minutes to 2-5 minutes
- **Traceability:** 100% of RCA recommendations linkable to implementation stories
- **Consistency:** Stories from RCA match quality of epic-generated stories

**Success Metrics:**
- Time to create stories from RCA: <5 minutes (vs 15-30 minutes manual)
- Traceability: RCA documents updated with story references
- Story quality: Pass devforgeai-qa validation identical to epic-generated stories

## Problem Statement

Currently, RCA recommendations require manual story creation, creating three pain points:
1. Manual effort is tedious and error-prone
2. No traceability from RCA recommendations to story completion
3. Inconsistent process compared to epic→story decomposition

## User Personas

1. **Developer:** Uses DevForgeAI to build software, wants to track RCA fixes
2. **Framework Maintainer:** Maintains DevForgeAI framework, creates RCAs for process improvements

## Features

### Feature 1.1: RCA Document Parsing
**Description:** Parse RCA markdown files from `devforgeai/RCA/` and extract recommendations with priority, title, effort estimate, and success criteria.
**User Stories (high-level):**
1. Parse RCA frontmatter (date, severity, status)
2. Extract recommendations by priority (CRITICAL/HIGH/MEDIUM/LOW)
3. Filter recommendations by effort threshold (>2 hours)

**Estimated Effort:** Medium (5-8 story points)

### Feature 1.2: Interactive Recommendation Selection
**Description:** Display parsed recommendations and let user interactively select which to convert to stories.
**User Stories (high-level):**
1. Display recommendation summary table
2. AskUserQuestion for multi-select of recommendations

**Estimated Effort:** Small (3-5 story points)

### Feature 1.3: Batch Story Creation
**Description:** Create stories via devforgeai-story-creation skill in batch mode, similar to `/create-missing-stories`.
**User Stories (high-level):**
1. Map recommendation fields to story-creation batch markers
2. Invoke devforgeai-story-creation skill in batch mode

**Estimated Effort:** Medium (5-8 story points)

### Feature 1.4: RCA-Story Linking
**Description:** Update RCA document with created story references for traceability.
**User Stories (high-level):**
1. Update RCA Implementation Checklist with story references
2. Add story IDs to recommendation sections

**Estimated Effort:** Small (3-5 story points)

### Feature 1.5: Command Shell
**Description:** Create lean `/create-stories-from-rca` command following orchestration pattern.
**User Stories (high-level):**
1. Create command file in `.claude/commands/`
2. Implement argument parsing and validation
3. Add help text and error handling

**Estimated Effort:** Medium (5-8 story points)

## Requirements Summary

### Functional Requirements
- Parse RCA documents and extract recommendations
- Filter recommendations by effort (>2 hours suitable for stories)
- Interactive selection of recommendations to convert
- Batch story creation via devforgeai-story-creation skill
- Update RCA documents with story references
- Stories comply with constitutional context files

### Data Model
**Entities:**
- RCA Document: path, id, title, severity, status, recommendations[]
- Recommendation: id (REC-N), priority, title, description, effort_hours, success_criteria
- Story File: Generated via devforgeai-story-creation, STORY-NNN format

### Non-Functional Requirements

**Architecture:**
- Lean orchestration: Command <15K characters
- Delegates to devforgeai-story-creation skill
- No business logic in command

**Compliance:**
- Stories must validate against tech-stack.md
- Stories must validate against architecture-constraints.md

**Error Handling:**
- Best-effort parsing + interactive recovery for ambiguous sections

## Architecture Considerations

**Complexity Tier:** 2 (Moderate Application)

**Recommended Architecture:**
- Pattern: Lean orchestration (command → skill delegation)
- Layers: 2 (Command Layer, Skill Layer)
- Database: N/A (file-based markdown parsing)
- Deployment: N/A (CLI tool, runs in Claude Code terminal)

## Risks & Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| RCA format variance | LOW | Best-effort parsing + interactive recovery |
| Story-creation skill changes | LOW | Batch mode is stable, follow existing pattern |

## Dependencies

**Prerequisites:**
- devforgeai-story-creation skill (exists)
- RCA document structure (established)

**Dependents:**
- None (standalone feature)

## Next Steps

1. **Story Creation:** Break features into stories via `/create-story`
2. **Sprint Planning:** Assign stories to sprint via `/create-sprint`
3. **Implementation:** Start TDD workflow via `/dev STORY-XXX`

## Stories

| Story ID | Title | Status | Points |
|----------|-------|--------|--------|
| STORY-155 | RCA Document Parsing | Backlog | 5 |
| STORY-156 | Interactive Recommendation Selection | Backlog | 4 |
| STORY-157 | Batch Story Creation | Backlog | 5 |
| STORY-158 | RCA-Story Linking | Backlog | 4 |
| STORY-159 | Command Shell | Backlog | 5 |

**Total Points:** 23

## Change Log

| Date | Version | Change |
|------|---------|--------|
| 2025-12-25 | 1.1 | Stories created via /create-missing-stories |
| 2025-12-24 | 1.0 | Epic created via /ideate command |
