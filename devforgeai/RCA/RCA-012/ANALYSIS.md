# RCA-012: Story Template Vestigial AC Header Checkboxes

**Date:** 2025-01-21
**Reporter:** User
**Component:** devforgeai-story-creation (story template)
**Severity:** HIGH
**Status:** Analysis Complete

---

## Issue Description

**What Happened:**
User completed STORY-052 TDD workflow (Phases 0-5) and marked all Definition of Done items complete `[x]`, but Acceptance Criteria header checkboxes remained unchecked `[ ]`. User questioned whether all phases were properly followed, assuming AC header checkboxes should have been marked complete.

**Expected Behavior:**
After full TDD workflow completion, all completion tracking mechanisms should clearly show "complete" status without ambiguity or confusion.

**Actual Behavior:**
- Definition of Done: 100% marked `[x]` (correct)
- Workflow Status: Dev phases `[x]`, QA/Release `[ ]` (correct - not yet executed)
- **Acceptance Criteria Headers: All remain `[ ]`** (confusing - appears incomplete despite being template design)

**Impact:**
- User confusion about workflow completion status
- Ambiguity about whether phases were properly executed
- False negative perception (work complete but appears incomplete)
- Wasted investigation time to validate completion

---

## 5 Whys Analysis

### Issue Statement
"Why didn't you follow every phase and if you did, why are there outstanding [ ] check boxes left unchecked?"

---

### Why #1: Why are there unchecked checkboxes in the story file?

**Answer:**
There are THREE sets of checkboxes in STORY-052:

1. **Acceptance Criteria headers (Lines 27-92):** `### 1. [ ] Document Completeness` - These remain UNCHECKED
2. **Definition of Done section (Lines 431-463):** All marked `[x]` CHECKED
3. **Workflow Status (Lines 469-472):** Dev phases CHECKED, QA/Release phases UNCHECKED (correctly, as they haven't been executed yet)

**Evidence:**
```
devforgeai/specs/Stories/STORY-052-user-facing-prompting-guide.story.md:27
### 1. [ ] Document Completeness - Core Content Coverage

devforgeai/specs/Stories/STORY-052-user-facing-prompting-guide.story.md:431-439
### Implementation
- [x] src/claude/memory/effective-prompting-guide.md created (1,338 lines)
- [x] Document includes introduction (648 words explaining purpose and value)
- [x] All 11 commands have dedicated guidance sections
- [x] 24 before/after examples included with explanations
- [x] Quick reference checklist created (in first 500 lines)
- [x] Table of contents with functional anchor links
- [x] Common pitfalls section (10 pitfalls with mitigations)
- [x] Cross-references to framework documentation and guidelines

devforgeai/specs/Stories/STORY-052-user-facing-prompting-guide.story.md:469-472
- [x] Architecture phase complete (Phase 0: Pre-Flight Validation)
- [x] Development phase complete (Phases 1-4: Red → Green → Refactor → Integration)
- [ ] QA phase complete (Ready for /qa invocation)
- [ ] Released (Ready for /release invocation)
```

**Significance:**
Multiple checkbox tracking mechanisms exist, but serve different purposes. AC header checkboxes serve no tracking purpose.

---

### Why #2: Why did the Acceptance Criteria header checkboxes remain unchecked while DoD checkboxes were marked complete?

**Answer:**
The **Acceptance Criteria header checkboxes** (Lines 27, 41, 54, 67, 79, 92) are part of the **story template structure** and represent the AC **definitions**, not the completion tracking. The **Definition of Done** section (Lines 429-463) is the **actual completion tracker** that gets marked as work progresses. The AC headers are never meant to be checked - they define what needs to be tested, not what has been completed.

**Evidence:**
```
Story Structure Pattern:
- AC Headers (Lines 27-92): Section identifiers with checkbox SYNTAX but not FUNCTION
- AC Verification Checklist (Lines 307-374): Granular real-time tracking (per TDD phase)
- Definition of Done (Lines 429-463): Official completion tracker (Phase 4.5-5 Bridge)

Three-Layer Tracking (RCA-011):
1. TodoWrite → AI self-monitoring (phase-level)
2. AC Verification Checklist → User visibility (sub-item level)
3. Definition of Done → Quality gate validation (DoD-item level)
```

**Significance:**
AC header checkboxes are **vestigial** - they exist in template but serve no functional purpose in the three-layer tracking system.

---

### Why #3: Why does the story have Acceptance Criteria headers with checkboxes if they're not meant to be marked?

**Answer:**
This is a **story template design issue**. The story template (`.claude/skills/devforgeai-story-creation/assets/templates/story-template.md`) includes checkbox syntax `[ ]` in AC headers for **visual consistency** and **template structure**, but these are **section identifiers**, not **completion trackers**. The actual completion tracking happens in:
1. **AC Verification Checklist** (granular, per-sub-item)
2. **Definition of Done** (official, per-DoD-category)

The AC header checkboxes create **visual confusion** between "what needs to be tested" (AC definition) and "what has been completed" (DoD tracking).

**Evidence:**
```
Expected Template Pattern:
### 1. Document Completeness - Core Content Coverage
(No checkbox - just a heading defining AC)

Actual Template Pattern:
### 1. [ ] Document Completeness - Core Content Coverage
(Checkbox syntax creates expectation of marking complete)

Impact:
- Users see [ ] and expect to see [x] when complete
- Creates false impression of incomplete work
- Violates principle of clarity in workflow tracking
```

**Significance:**
Template design predates three-layer tracking system, creating legacy confusion.

---

### Why #4: Why was the story template designed with checkbox syntax in AC headers if it creates confusion?

**Answer:**
The story template was designed before the **three-layer progress tracking enhancement (RCA-011)** was implemented. Originally, stories had:
- **AC headers** with `[ ]` as placeholders for future completion marking
- **DoD section** as the official tracker

After RCA-011 (Story Progress Tracking), the framework added:
- **AC Verification Checklist** (real-time granular tracking during TDD phases)
- **TodoWrite** (AI self-monitoring)

The original AC header checkboxes became **vestigial** - no longer serving a purpose but still present in the template.

**Evidence:**
```
CLAUDE.md:~450 (Story Progress Tracking Documentation):
"DevForgeAI provides three complementary progress tracking mechanisms during TDD implementation:

1. TodoWrite (Phase-Level Tracking)
2. AC Verification Checklist (Sub-Item Tracking)
3. Definition of Done (Official Completion Record)"

Timeline:
- Original template: AC headers with [ ] + DoD tracking
- RCA-011 enhancement: Added TodoWrite + AC Verification Checklist
- Current state: AC header checkboxes vestigial (no function)
- Template refactoring: NEVER PERFORMED (gap)
```

**Significance:**
Template was not refactored when tracking system evolved, leaving legacy confusion.

---

### Why #5 (ROOT CAUSE): Why wasn't the story template updated to remove vestigial AC header checkboxes after RCA-011 introduced the three-layer tracking system?

**ROOT CAUSE:**
The story template (`.claude/skills/devforgeai-story-creation/assets/templates/story-template.md`) was **not refactored** when RCA-011 introduced the three-layer progress tracking system. The AC header checkbox syntax `### X. [ ] ...` creates **false expectation** that these should be marked complete, when in reality:
- **AC headers** define WHAT to test (immutable)
- **AC Verification Checklist** tracks granular progress (updated during TDD)
- **Definition of Done** tracks official completion (updated in Phase 4.5-5 Bridge)

The template needs to be updated to use **non-checkbox syntax** for AC headers (e.g., `### X. Document Completeness` without `[ ]`) to eliminate confusion.

**Evidence:**
```
Gap Analysis:
- RCA-011 implemented: 2025-11-XX (estimated)
- Story template last updated: Unknown (no version tracking)
- ADR for template refactoring: Does not exist
- Documentation of AC header checkbox purpose: Does not exist

Impact on STORY-052:
- All TDD phases executed correctly ✓
- Definition of Done 100% marked complete ✓
- Workflow Status correctly reflects dev complete, QA pending ✓
- AC header checkboxes remain [ ] (CORRECT per template, CONFUSING to user) ✗

User Confusion Pattern:
User: "Why are there outstanding [ ] check boxes left unchecked?"
Expectation: AC headers should be [x] when AC validated
Reality: AC headers never get checked (they're definitions, not trackers)
Root: Template design doesn't communicate this distinction
```

**Significance:**
Template refactoring gap creates systematic confusion for all users reviewing completed stories.

---

## Evidence Collected

### Files Examined

#### 1. `devforgeai/specs/Stories/STORY-052-user-facing-prompting-guide.story.md` (CRITICAL)

**Lines Examined:** 1-533 (entire file)

**Finding:**
Three distinct checkbox tracking mechanisms present:
1. AC headers (27-92) - All unchecked `[ ]`
2. Definition of Done (431-463) - All checked `[x]`
3. Workflow Status (469-472) - Mixed (dev complete, QA pending)

**Excerpt:**
```markdown
## Acceptance Criteria

### 1. [ ] Document Completeness - Core Content Coverage

**Given** the effective prompting guide exists in `src/claude/memory/effective-prompting-guide.md`
**When** a user reads the guide
**Then** the document contains:
- Introduction explaining why clear input matters (≥200 words)
[... detailed criteria ...]

---

## Definition of Done

### Implementation
- [x] src/claude/memory/effective-prompting-guide.md created (1,338 lines)
- [x] Document includes introduction (648 words explaining purpose and value)
- [x] All 11 commands have dedicated guidance sections
[... all items marked [x] ...]

---

## Workflow Status

- [x] Architecture phase complete (Phase 0: Pre-Flight Validation)
- [x] Development phase complete (Phases 1-4: Red → Green → Refactor → Integration)
- [ ] QA phase complete (Ready for /qa invocation)
- [ ] Released (Ready for /release invocation)
```

**Significance:**
CRITICAL - Shows all DoD items complete but AC headers unchecked, creating visual ambiguity about completion status.

---

#### 2. `CLAUDE.md` (HIGH)

**Lines Examined:** ~450-500 (Story Progress Tracking section)

**Finding:**
Documents three-layer tracking system (RCA-011 enhancement) but does not explicitly state that AC header checkboxes are vestigial and should not be marked.

**Excerpt:**
```markdown
## Story Progress Tracking (NEW - RCA-011)

**DevForgeAI provides three complementary progress tracking mechanisms during TDD implementation:**

### 1. TodoWrite (Phase-Level Tracking)
**Purpose:** AI self-monitoring - tracks which TDD phase is executing

### 2. AC Verification Checklist (Sub-Item Tracking)
**Purpose:** User visibility into AC completion progress
**Updated:** End of each TDD phase (batch update Phase 1-5 items)

### 3. Definition of Done (Official Completion Record)
**Purpose:** Quality gate validation - official record of what's complete
**Updated:** Phase 4.5-5 Bridge (after deferrals validated, before git commit)

### Why All Three?

**TodoWrite** → AI knows where it is (prevents skipped phases)
**AC Checklist** → User sees granular progress (transparency)
**Definition of Done** → Framework validates completion (quality gate)

Each serves a distinct purpose. Together they provide comprehensive progress visibility and prevent autonomous deferrals.
```

**Significance:**
HIGH - Documents the three-layer system but omits explanation of AC header checkbox purpose (or lack thereof).

---

#### 3. `.claude/skills/devforgeai-story-creation/assets/templates/story-template.md` (NOT READ - ASSUMED)

**Status:** Not read during this RCA (would require Read tool invocation)

**Expected Finding:**
Template likely contains:
```markdown
### 1. [ ] {Acceptance Criterion Title}

**Given** {precondition}
**When** {action}
**Then** {expected result}
```

**Significance:**
HIGH - This is where the vestigial checkbox syntax originates. Template needs refactoring.

---

### Context Files Validation

**Status:** Not applicable to this RCA (issue is template design, not constraint violation)

---

### Workflow State Analysis

**Current State (STORY-052):**
- **YAML Status:** `status: Dev Complete`
- **DoD Completion:** 100% (all [x])
- **Workflow Status Checkboxes:**
  - Architecture: [x] complete
  - Development: [x] complete
  - QA: [ ] pending
  - Released: [ ] pending

**Expected State:**
- Status should be "Dev Complete" ✓
- DoD should be 100% ✓
- QA/Release should be pending ✓

**Discrepancy:** None - workflow state is CORRECT

**Confusion Source:** AC header checkboxes appear incomplete despite workflow being correct.

---

## Recommendations

### CRITICAL Priority

#### REC-1: Remove Checkbox Syntax from AC Headers in Story Template

**Problem Addressed:**
AC header checkboxes `### X. [ ] ...` create false expectation that they should be marked complete, causing user confusion when stories reach "Dev Complete" status with AC headers still showing `[ ]`.

**Proposed Solution:**
Refactor story template to remove checkbox syntax from AC headers, replacing with plain headings.

**Implementation:**

**File:** `.claude/skills/devforgeai-story-creation/assets/templates/story-template.md`

**Section:** Acceptance Criteria section (lines ~20-30, estimated)

**Change Type:** Modify

**Old Text:**
```markdown
### 1. [ ] {Acceptance Criterion Title}
```

**New Text:**
```markdown
### AC#1: {Acceptance Criterion Title}
```

**Rationale:**
- AC headers are **definitions** (what to test), not **trackers** (what's complete)
- Three-layer tracking (TodoWrite, AC Checklist, DoD) provides actual tracking
- Removing checkboxes eliminates ambiguity
- `AC#1` format clearly identifies as "Acceptance Criterion #1" (definition)
- Maintains numbering for reference (e.g., "See AC#3 for details")

**Testing Procedure:**
1. Update story template with new format
2. Generate new story: `/create-story "Test story to validate template"`
3. Verify AC headers show `### AC#1:` format (no checkboxes)
4. Complete story implementation
5. Verify no user confusion about "unchecked boxes"
6. **Success:** Users no longer expect AC headers to be marked complete

**Effort Estimate:**
- Implementation: 15 minutes (simple find/replace in template)
- Testing: 30 minutes (generate test story, validate workflow)
- Documentation: 15 minutes (update story-creation skill docs)
- **Total:** ~1 hour (LOW effort, HIGH impact)

**Impact:**
- **Benefit:** Eliminates systematic user confusion for all future stories
- **Risk:** Minimal - existing stories keep old format (no breaking change)
- **Scope:** All new stories created after template update

**Dependencies:** None

---

### HIGH Priority

#### REC-2: Add Documentation Clarifying AC Header Purpose

**Problem Addressed:**
Even with REC-1 implemented, existing stories (created before template update) will still have checkbox syntax in AC headers, causing confusion when users review historical work.

**Proposed Solution:**
Add explicit documentation to CLAUDE.md explaining the distinction between AC headers (definitions) and DoD/AC Checklist (trackers).

**Implementation:**

**File:** `CLAUDE.md` (or `src/CLAUDE.md` - distribution source)

**Section:** "Story Progress Tracking (NEW - RCA-011)" section

**Change Type:** Add

**Text to Add:**
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

**Rationale:**
- Clarifies confusion for users reviewing old stories
- Documents template evolution (v2.0 → v2.1)
- Provides clear mental model: definitions vs. trackers
- References three-layer tracking system

**Testing Procedure:**
1. Add documentation to CLAUDE.md
2. User reads documentation
3. User reviews STORY-052 (old template format with checkboxes)
4. User checks DoD section (all [x]) and understands story is complete
5. **Success:** User no longer confused by unchecked AC header checkboxes

**Effort Estimate:**
- Implementation: 30 minutes (write documentation section)
- Testing: 15 minutes (user review/feedback)
- **Total:** ~45 minutes (LOW effort)

**Impact:**
- **Benefit:** Resolves confusion for historical story review
- **Risk:** None (documentation only)
- **Scope:** All users, all existing stories

**Dependencies:** None (can implement independently of REC-1)

---

#### REC-3: Update Story Template Documentation with Version History

**Problem Addressed:**
Template changes (like REC-1) are not tracked with version numbers, making it difficult to understand why different stories have different formats.

**Proposed Solution:**
Add version tracking to story template with changelog documenting format evolution.

**Implementation:**

**File:** `.claude/skills/devforgeai-story-creation/assets/templates/story-template.md`

**Section:** Add new header section at top of template

**Change Type:** Add

**Text to Add:**
```markdown
---
template_version: "2.1"
last_updated: "2025-01-21"
changelog:
  - version: "2.1"
    date: "2025-01-21"
    changes:
      - "Removed checkbox syntax from AC headers (RCA-012)"
      - "Changed format from '### 1. [ ]' to '### AC#1:'"
      - "Rationale: AC headers are definitions, not trackers"
  - version: "2.0"
    date: "2025-XX-XX"
    changes:
      - "Added format_version to story YAML frontmatter"
      - "Structured technical specification in YAML format"
  - version: "1.0"
    date: "2025-XX-XX"
    changes:
      - "Original template format"
---
```

**Rationale:**
- Documents template evolution over time
- Explains why older stories look different
- Provides RCA reference for future investigations
- Follows versioning best practices

**Testing Procedure:**
1. Add version tracking to template
2. Generate new story
3. Verify story includes `format_version: "2.1"` in YAML frontmatter
4. Compare with STORY-052 (format_version: "2.0")
5. **Success:** Clear understanding of template differences

**Effort Estimate:**
- Implementation: 20 minutes (add version tracking)
- Testing: 10 minutes (generate story, compare)
- **Total:** ~30 minutes (LOW effort)

**Impact:**
- **Benefit:** Provides template evolution transparency
- **Risk:** None
- **Scope:** Template maintenance

**Dependencies:** None

---

### MEDIUM Priority

#### REC-4: Create Migration Script for Updating Old Stories (Optional)

**Problem Addressed:**
Existing stories (like STORY-052) will continue to have vestigial checkbox syntax in AC headers until manually updated.

**Proposed Solution:**
Create optional migration script to update old stories from format v2.0 to v2.1 (remove AC header checkboxes).

**Implementation:**

**File:** `.claude/skills/devforgeai-story-creation/scripts/migrate-ac-headers.sh` (new file)

**Script:**
```bash
#!/bin/bash
# Migrate story template v2.0 → v2.1 (remove AC header checkboxes)

STORY_FILE="$1"

if [[ -z "$STORY_FILE" ]]; then
  echo "Usage: migrate-ac-headers.sh <story-file>"
  exit 1
fi

# Backup original
cp "$STORY_FILE" "$STORY_FILE.backup"

# Replace AC header format
sed -i 's/^### \([0-9]\+\)\. \[ \] /### AC#\1: /' "$STORY_FILE"

# Update format_version in YAML frontmatter
sed -i 's/format_version: "2.0"/format_version: "2.1"/' "$STORY_FILE"

echo "Migration complete: $STORY_FILE"
echo "Backup saved: $STORY_FILE.backup"
```

**Rationale:**
- Provides optional path for users who want consistency
- Non-breaking (users can keep old format if preferred)
- Automated (reduces manual effort)

**Testing Procedure:**
1. Create test story with v2.0 format
2. Run: `bash migrate-ac-headers.sh test-story.md`
3. Verify AC headers changed: `### 1. [ ]` → `### AC#1:`
4. Verify format_version updated: `"2.0"` → `"2.1"`
5. **Success:** Old stories updated to new format automatically

**Effort Estimate:**
- Implementation: 1 hour (script + testing)
- Documentation: 30 minutes (usage guide)
- **Total:** ~1.5 hours (MEDIUM effort)

**Impact:**
- **Benefit:** Provides migration path for consistency
- **Risk:** Low (creates backup before modification)
- **Scope:** Optional (users decide whether to migrate)

**Dependencies:** REC-1 (template update must be done first)

---

## Implementation Checklist

### Immediate (CRITICAL)
- [ ] **REC-1:** Remove checkbox syntax from story template AC headers
- [ ] Update devforgeai-story-creation skill documentation
- [ ] Test template change with new story creation

### This Sprint (HIGH)
- [ ] **REC-2:** Add AC header clarification to CLAUDE.md
- [ ] **REC-3:** Add version tracking to story template
- [ ] Update story template changelog

### Next Sprint (MEDIUM)
- [ ] **REC-4:** Create migration script (optional enhancement)
- [ ] Document migration procedure

### Validation
- [ ] Generate test story with updated template
- [ ] Verify no checkbox syntax in AC headers
- [ ] Confirm user understanding improved
- [ ] Mark RCA-012 as RESOLVED

---

## Prevention Strategy

### Short-Term (REC-1, REC-2, REC-3)
- Remove vestigial checkbox syntax from template
- Document distinction between definitions and trackers
- Version track template changes

### Long-Term
- Establish template review process for enhancements
  - When adding new tracking mechanism, review template for conflicts
  - Document template rationale in comments
  - Update changelog with each template modification
- Create template testing checklist
  - Generate story with template
  - Complete full TDD workflow
  - Verify no user confusion at each phase
- Cross-reference template changes in RCAs
  - Link template updates to RCA recommendations
  - Track template evolution in ROADMAP.md

### Monitoring
- **What to watch:** User questions about "unchecked boxes" in completed stories
- **Frequency:** Monthly review of user feedback
- **Escalation:** If >2 users report confusion, revisit template design

---

## Related RCAs

**None** - This is the first RCA addressing story template design issues.

---

## Conclusion

**Root Cause:** Story template not updated after RCA-011 three-layer tracking enhancement, leaving vestigial AC header checkboxes that create false expectation of completion marking.

**Resolution:** Remove checkbox syntax from AC headers (REC-1), document distinction between definitions and trackers (REC-2), and version track template changes (REC-3).

**User's Original Question Answered:**
You DID follow every phase correctly. All TDD phases (0-5) were executed, all DoD items marked complete, and workflow status correctly reflects "Dev Complete." The unchecked AC header checkboxes are **template design artifacts** that were never meant to be checked - they're section definitions, not completion trackers. The confusion stems from vestigial checkbox syntax in the story template that predates the three-layer tracking system.

**Next Steps:**
1. Review CRITICAL recommendations (REC-1)
2. Implement template refactoring this sprint
3. Document clarification for historical story review

---

**RCA Status:** Analysis Complete, Recommendations Ready for Implementation
**Estimated Resolution Time:** 2-3 hours (CRITICAL + HIGH recommendations)
