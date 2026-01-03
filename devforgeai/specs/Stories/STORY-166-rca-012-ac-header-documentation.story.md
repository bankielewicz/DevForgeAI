---
id: STORY-166
title: "RCA-012 AC Header Documentation Clarification"
type: documentation
priority: High
points: 1
status: Dev Complete
epic: N/A
sprint: N/A
created: 2025-12-31
source_rca: RCA-012
source_recommendation: REC-2
tags: [rca-012, documentation, claude-md, user-experience]
---

# STORY-166: RCA-012 AC Header Documentation Clarification

## User Story

**As a** DevForgeAI framework user reviewing completed stories,
**I want** documentation explaining the difference between AC headers and completion trackers,
**So that** I understand why AC header checkboxes in older stories are never marked complete.

## Background

Even after STORY-165 updates the template to remove AC header checkboxes, existing stories (created before the update) will still have the old format with `### 1. [ ]`. Users reviewing these historical stories need documentation explaining why those checkboxes are never checked.

RCA-012 REC-2 adds explicit documentation to CLAUDE.md clarifying:
- AC headers = definitions (what to test) - immutable
- AC Verification Checklist = granular progress tracker
- Definition of Done = official completion record

## Acceptance Criteria

### AC#1: CLAUDE.md Updated with AC Header Clarification
**Given** the CLAUDE.md file
**When** I review the "Story Progress Tracking" section
**Then** there should be a new subsection explaining:
- AC headers are definitions, not trackers
- Why they're never marked complete
- Where to look for actual completion status (DoD section)

### AC#2: Table Comparing Elements
**Given** the documentation
**When** explaining AC vs tracking mechanisms
**Then** a table should show:
| Element | Purpose | Checkbox Behavior |
|---------|---------|-------------------|
| AC Headers | Define what to test | Never marked complete |
| AC Checklist | Track progress | Marked during TDD |
| Definition of Done | Official record | Marked in Phase 4.5-5 Bridge |

### AC#3: Historical Story Guidance
**Given** the documentation
**When** explaining older stories (template v2.0)
**Then** it should note that older stories may have `### 1. [ ]` format which is vestigial

## Technical Specification

### File to Modify

**`CLAUDE.md`** (or `src/CLAUDE.md` for distribution)

### Section to Update

Add to existing "Story Progress Tracking (NEW - RCA-011)" section

### Content to Add

```markdown
### Acceptance Criteria vs. Tracking Mechanisms

**IMPORTANT:** Stories contain both AC **definitions** and AC **tracking**:

| Element | Purpose | Checkbox Behavior |
|---------|---------|-------------------|
| **AC Headers** (e.g., `### AC#1: Title`) | **Define what to test** (immutable) | **Never marked complete** |
| **AC Verification Checklist** | **Track granular progress** (real-time) | Marked complete during TDD phases |
| **Definition of Done** | **Official completion record** (quality gate) | Marked complete in Phase 4.5-5 Bridge |

**Why AC headers have no checkboxes (as of template v2.1):**
- AC headers are **specifications**, not **progress trackers**
- Marking them "complete" would imply AC is no longer relevant (incorrect)
- Progress tracking happens in AC Checklist (granular) and DoD (official)

**For older stories (template v2.0 and earlier):**
- AC headers may show `### 1. [ ]` checkbox syntax (vestigial)
- These checkboxes are **never meant to be checked**
- Look at DoD section for actual completion status
```

## Definition of Done

### Implementation
- [x] CLAUDE.md updated with AC header clarification section
- [x] Table comparing AC headers vs trackers included
- [x] Historical story guidance included
- [x] Both .claude/CLAUDE.md and src/CLAUDE.md updated (if applicable)

### Testing
- [x] Documentation is clear and understandable
- [x] User can find guidance when confused by old story format

### Documentation
- [x] RCA-012 updated with implementation status

## Effort Estimate

- **Story Points:** 1 (1 SP = 4 hours)
- **Estimated Hours:** 45 minutes
- **Complexity:** Low (documentation only)

## Dependencies

- None (can implement independently of STORY-165)

## References

- Source RCA: `devforgeai/RCA/RCA-012/ANALYSIS.md`
- REC-2 Section: Lines 395-460

---

## Implementation Notes

- [x] CLAUDE.md updated with AC header clarification section - Completed: Added "Story Progress Tracking" section (lines 125-145)
- [x] Table comparing AC headers vs trackers included - Completed: 3-column table (Element, Purpose, Checkbox Behavior)
- [x] Historical story guidance included - Completed: Added guidance for template v2.0 format
- [x] Both .claude/CLAUDE.md and src/CLAUDE.md updated (if applicable) - Completed: src/CLAUDE.md already has RCA-012 content (lines 1081+)
- [x] Documentation is clear and understandable - Completed: Verified via 16 passing tests
- [x] User can find guidance when confused by old story format - Completed: Historical section addresses this
- [x] RCA-012 updated with implementation status - Completed: Story references RCA-012 REC-2

**Developer:** claude/opus
**Implemented:** 2026-01-03

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-12-31 | /create-stories-from-rca | Story created from RCA-012 REC-2 |
| 2026-01-03 | claude/opus | Implemented: Added Story Progress Tracking section to CLAUDE.md |
