---
id: STORY-172
title: "RCA-013 Story Complexity Heuristics"
type: enhancement
priority: Low
points: 5
status: Backlog
epic: N/A
sprint: N/A
created: 2025-12-31
source_rca: RCA-013
source_recommendation: REC-6
tags: [rca-013, complexity-analysis, story-scoping, user-experience]
---

# STORY-172: RCA-013 Story Complexity Heuristics

## User Story

**As a** DevForgeAI framework user,
**I want** to be warned during Phase 0 if a story is likely to require multiple iterations,
**So that** I can consider breaking it into smaller stories before investing development time.

## Background

RCA-013 identified that stories with many DoD items or complex technical specs often require multiple TDD iterations. REC-6 adds heuristics to analyze story complexity at Phase 0 and warn users about potentially oversized stories.

This helps users make informed decisions about:
- Story scope appropriateness
- Expected development time
- Potential for iteration loops

## Acceptance Criteria

### AC#1: Analyze Story Metrics at Phase 0
**Given** Phase 0 (Pre-Flight) is executing
**When** story file is loaded
**Then** analyze and capture:
- DoD item count
- Acceptance criteria count
- Technical specification size (lines)
- File touch count (from tech spec)

### AC#2: Apply Complexity Thresholds
**Given** story metrics are captured
**When** evaluating complexity
**Then** apply thresholds:
- DoD items: >20 = High, >30 = Very High
- AC count: >5 = High, >8 = Very High
- Tech spec lines: >100 = High, >200 = Very High
- Files touched: >10 = High, >20 = Very High

### AC#3: Display Complexity Warning
**Given** story exceeds complexity thresholds
**When** Phase 0 completes
**Then** display warning:
```
⚠️ Story Complexity: HIGH
Metrics:
- DoD items: 35 (threshold: 20)
- Files to modify: 12 (threshold: 10)

This story may require multiple TDD iterations.
Consider: Break into 2-3 smaller stories?
```

### AC#4: User Decision Point
**Given** complexity warning displayed
**When** prompting user
**Then** offer options:
- "Continue - I understand this is a large story"
- "Show me what could be split out"
- "Stop - I'll break this into smaller stories first"

### AC#5: Log Complexity for Retrospective
**Given** story complexity is assessed
**When** development completes
**Then** log actual iterations vs predicted complexity for framework learning

## Technical Specification

### File to Modify

**`.claude/skills/devforgeai-development/references/preflight-validation.md`**

### Complexity Analysis Logic

```markdown
### Step 11: Story Complexity Analysis (NEW)

**Purpose:** Warn user about potentially oversized stories

**Metrics to Analyze:**
```
dod_count = count(DoD items in story)
ac_count = count(Acceptance Criteria)
tech_spec_lines = count(lines in Technical Specification section)
files_touched = count(files mentioned in tech spec)
```

**Complexity Scoring:**
```
complexity_score = 0

IF dod_count > 20: complexity_score += 1
IF dod_count > 30: complexity_score += 1

IF ac_count > 5: complexity_score += 1
IF ac_count > 8: complexity_score += 1

IF tech_spec_lines > 100: complexity_score += 1
IF tech_spec_lines > 200: complexity_score += 1

IF files_touched > 10: complexity_score += 1
IF files_touched > 20: complexity_score += 1

complexity_level =
  score >= 4: "VERY HIGH"
  score >= 2: "HIGH"
  score >= 1: "MEDIUM"
  else: "NORMAL"
```

**Warning Display (if score >= 2):**
```
Display: ""
Display: "⚠️ STORY COMPLEXITY ASSESSMENT"
Display: "================================"
Display: "Complexity Level: {complexity_level}"
Display: ""
Display: "Metrics:"
IF dod_count > 20:
  Display: "  • DoD items: {dod_count} (threshold: 20)"
IF ac_count > 5:
  Display: "  • Acceptance Criteria: {ac_count} (threshold: 5)"
IF tech_spec_lines > 100:
  Display: "  • Tech spec size: {tech_spec_lines} lines (threshold: 100)"
IF files_touched > 10:
  Display: "  • Files to modify: {files_touched} (threshold: 10)"
Display: ""
Display: "This story may require multiple TDD iterations (2-3+ passes)."
Display: ""

AskUserQuestion:
  Question: "How would you like to proceed?"
  Header: "Complexity"
  Options:
    - "Continue - I understand this is a large story"
    - "Show me what could be split out"
    - "Stop - I'll break this into smaller stories first"
  multiSelect: false
```
```

### Split Suggestion Logic

If user chooses "Show me what could be split out":
- Group DoD items by category
- Suggest logical boundaries
- Example: "Implementation items 1-5 could be STORY-A, items 6-10 could be STORY-B"

## Edge Cases

1. **Story already split** - Small stories should pass without warning
2. **Intentionally large stories** - User can proceed after acknowledgment
3. **Metrics unavailable** - Skip analysis if story format doesn't match expected structure

## Definition of Done

### Implementation
- [ ] Step 11 added to preflight-validation.md
- [ ] Complexity metrics captured (DoD, AC, tech spec, files)
- [ ] Complexity scoring implemented
- [ ] Warning display for HIGH/VERY HIGH
- [ ] User decision point with 3 options
- [ ] Split suggestion logic for option 2
- [ ] Both .claude/ and src/claude/ versions updated

### Testing
- [ ] Test with small story (should pass without warning)
- [ ] Test with medium story (MEDIUM complexity, no blocking warning)
- [ ] Test with large story (HIGH complexity, warning displayed)
- [ ] Test user can proceed after warning
- [ ] Test split suggestion provides useful guidance

### Documentation
- [ ] RCA-013 updated with implementation status
- [ ] Complexity thresholds documented

## Non-Functional Requirements

### Accuracy
- Thresholds should be calibrated based on actual story data
- May need adjustment after observing real patterns

### Non-Blocking
- Warning should inform, not force story decomposition
- User always has option to proceed

## Effort Estimate

- **Story Points:** 5 (1 SP = 4 hours)
- **Estimated Hours:** 2-3 hours
- **Complexity:** Medium (analysis logic + user interaction)

## Dependencies

- Story files must have consistent format for metric extraction

## References

- Source RCA: `devforgeai/RCA/RCA-013-development-workflow-stops-before-completion-despite-no-deferrals.md`
- REC-6 Section: Lines 646-652

---

## Implementation Notes
<!-- Filled in by devforgeai-development skill -->
*To be completed during development*

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-12-31 | /create-stories-from-rca | Story created from RCA-013 REC-6 |
