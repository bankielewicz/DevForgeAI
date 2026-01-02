---
id: STORY-165
title: "RCA-012 Remove Checkbox Syntax from AC Headers"
type: enhancement
priority: Critical
points: 2
status: Backlog
epic: N/A
sprint: N/A
created: 2025-12-31
source_rca: RCA-012
source_recommendation: REC-1
tags: [rca-012, story-template, ac-headers, user-experience]
---

# STORY-165: RCA-012 Remove Checkbox Syntax from AC Headers

## User Story

**As a** DevForgeAI framework user,
**I want** Acceptance Criteria headers to use plain heading format without checkboxes,
**So that** I don't get confused thinking AC headers should be marked complete when the story is done.

## Background

RCA-012 identified that story template AC headers use checkbox syntax (`### 1. [ ] Title`) which creates false expectation that these should be marked `[x]` when the story is complete. However, AC headers are **definitions** (what to test), not **trackers** (what's complete).

The three-layer tracking system (RCA-011) provides actual completion tracking via:
1. TodoWrite (phase-level)
2. AC Verification Checklist (sub-item level)
3. Definition of Done (official completion)

AC header checkboxes are vestigial and should be removed.

## Acceptance Criteria

### AC#1: Template AC Header Format Updated
**Given** the story template `.claude/skills/devforgeai-story-creation/assets/templates/story-template.md`
**When** I review the Acceptance Criteria section
**Then** AC headers should use format `### AC#1: {Title}` instead of `### 1. [ ] {Title}`

### AC#2: New Stories Use Updated Format
**Given** the updated story template
**When** I run `/create-story "Test story"`
**Then** the generated story should have AC headers in `### AC#1:` format with no checkboxes

### AC#3: No Breaking Changes for Existing Stories
**Given** existing stories with old format (`### 1. [ ]`)
**When** the template is updated
**Then** existing stories are unchanged (no automatic migration)

### AC#4: Format Maintains Numbering Reference
**Given** the new AC header format
**When** documentation or code references acceptance criteria
**Then** references like "See AC#3" should still work logically

## Technical Specification

### File to Modify

**`.claude/skills/devforgeai-story-creation/assets/templates/story-template.md`**

### Change Pattern

**Old Format:**
```markdown
### 1. [ ] {Acceptance Criterion Title}

**Given** {precondition}
**When** {action}
**Then** {expected result}
```

**New Format:**
```markdown
### AC#1: {Acceptance Criterion Title}

**Given** {precondition}
**When** {action}
**Then** {expected result}
```

### Implementation Steps

1. Open story template file
2. Find/replace AC header pattern:
   - Search: `### 1. [ ]`
   - Replace: `### AC#1:`
   - Repeat for `### 2. [ ]` → `### AC#2:`, etc.
3. Update any template documentation referencing AC format
4. Test by generating new story

## Edge Cases

1. **Variable AC count** - Template should support 1-N acceptance criteria
2. **Existing stories** - No automatic migration (handled by STORY-168/REC-4)
3. **AC references in tech spec** - Update if template has cross-references

## Definition of Done

### Implementation
- [ ] Story template AC headers changed from `### N. [ ]` to `### AC#N:`
- [ ] Both .claude/ and src/claude/ versions updated
- [ ] Template documentation updated if needed

### Testing
- [ ] Generate new story with `/create-story`
- [ ] Verify AC headers show `### AC#1:` format
- [ ] Verify no checkboxes in AC section
- [ ] Verify Given/When/Then structure preserved

### Documentation
- [ ] RCA-012 updated with implementation status

## Non-Functional Requirements

### Consistency
- All AC headers in template should follow same format

### Clarity
- Format should clearly indicate "Acceptance Criterion #1" meaning

## Effort Estimate

- **Story Points:** 2 (1 SP = 4 hours)
- **Estimated Hours:** 1 hour
- **Complexity:** Low (find/replace in template)

## Dependencies

- None

## References

- Source RCA: `devforgeai/RCA/RCA-012/ANALYSIS.md`
- REC-1 Section: Lines 339-393
- Story Template: `.claude/skills/devforgeai-story-creation/assets/templates/story-template.md`

---

## Implementation Notes
<!-- Filled in by devforgeai-development skill -->
*To be completed during development*

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-12-31 | /create-stories-from-rca | Story created from RCA-012 REC-1 |
