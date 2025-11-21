# RCA-012 Phase 1 Execution Plan
## Foundation: Template Refactoring + Documentation

**Version:** 1.0
**Created:** 2025-01-21
**Estimated Duration:** 2.25 hours
**Priority:** CRITICAL
**Status:** Ready for Execution

---

## Executive Summary

**Objective:** Fix the root cause of AC header checkbox confusion by updating story template to v2.1 (remove checkbox syntax) and documenting the three-layer tracking system in CLAUDE.md.

**What Gets Fixed:**
- Story template AC headers: `### 1. [ ]` → `### AC#1:` (no checkboxes)
- Template version: 2.0 → 2.1
- CLAUDE.md: Add "Acceptance Criteria vs. Tracking Mechanisms" section
- devforgeai-story-creation skill: Add version history documentation

**Impact:**
- **Immediate:** All future stories (58+) have clear AC definition format
- **Long-term:** Zero user confusion about AC header checkboxes
- **Prevention:** Stops issue at source (template design)

**Deliverables:**
1. Template v2.1 operational
2. CLAUDE.md section documenting three-layer tracking
3. Template version history in skill documentation
4. Test story validating new format
5. User approval confirming clarity

---

## Phase 1 Overview

### Three Recommendations Combined

**REC-1 (CRITICAL):** Template Refactoring
- Remove `[ ]` checkbox syntax from AC headers
- Change format: `### 1. [ ]` → `### AC#1:`
- Update format version: 2.0 → 2.1
- Add changelog header to template
- **Effort:** 1 hour

**REC-2 (HIGH):** CLAUDE.md Documentation
- Add "Acceptance Criteria vs. Tracking Mechanisms" section
- Explain three-layer tracking (TodoWrite, AC Checklist, DoD)
- Clarify AC headers are definitions (never marked)
- Document old template format caveat (v1.0/v2.0)
- **Effort:** 45 minutes

**REC-3 (HIGH):** Template Version History
- Add "Story Template Versions" section to devforgeai-story-creation skill
- Document v1.0, v2.0, v2.1 evolution
- Explain migration path and backward compatibility
- **Effort:** 30 minutes

**Total Phase 1 Effort:** 2.25 hours (2 hours 15 minutes)

---

## Detailed Step-by-Step Execution

### Step 1: Backup Template (5 minutes)

**Objective:** Create safety backup before making changes

**Commands:**
```bash
cd /mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-story-creation/assets/templates/

# Create backup
cp story-template.md story-template.md.v2.0-backup

# Verify backup
ls -lh story-template.md*
```

**Expected Output:**
```
-rw-r--r-- 1 user user 18K ... story-template.md
-rw-r--r-- 1 user user 18K ... story-template.md.v2.0-backup
```

**Validation:**
```bash
# Verify files identical
diff story-template.md story-template.md.v2.0-backup
# Expected: No output (files identical)

echo $?
# Expected: 0 (success)
```

**Checkpoint:**
- [ ] Backup created
- [ ] Files identical (diff shows no differences)
- [ ] Backup is readable

**If Fails:**
- Check file permissions
- Verify path is correct
- Retry backup command

**Rollback:** Not needed (no changes made yet)

---

### Step 2: Update AC Header Format (15 minutes)

**Objective:** Change AC headers from `### 1. [ ]` to `### AC#1:` format

**Current State (Lines to Change):**
- Line 29: `### 1. [ ] [Criterion 1 Title]`
- Line 42: `### 2. [ ] [Criterion 2 Title]`
- Line 50: `### 3. [ ] [Criterion 3 Title]`
- Line 58: `### 4. [ ] [Criterion 4 Title]`

**Edit 1:**
```
File: /mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-story-creation/assets/templates/story-template.md

Old: ### 1. [ ] [Criterion 1 Title]
New: ### AC#1: [Criterion 1 Title]
```

**Edit 2:**
```
Old: ### 2. [ ] [Criterion 2 Title]
New: ### AC#2: [Criterion 2 Title]
```

**Edit 3:**
```
Old: ### 3. [ ] [Criterion 3 Title]
New: ### AC#3: [Criterion 3 Title]
```

**Edit 4:**
```
Old: ### 4. [ ] [Criterion 4 Title]
New: ### AC#4: [Criterion 4 Title]
```

**Validation:**
```bash
# Verify new format (should find 4 AC headers)
grep "^### AC#" story-template.md

# Expected output:
### AC#1: [Criterion 1 Title]
### AC#2: [Criterion 2 Title]
### AC#3: [Criterion 3 Title]
### AC#4: [Criterion 4 Title]

# Verify old format gone (should find 0)
grep "^### [0-9]\. \[" story-template.md
# Expected: No output, exit code 1 (no matches found)
```

**Checkpoint:**
- [ ] All 4 edits applied successfully
- [ ] New format verified (4 AC headers found)
- [ ] Old format removed (0 instances found)
- [ ] Template file readable (no corruption)

**If Fails:**
- Restore from backup: `cp story-template.md.v2.0-backup story-template.md`
- Review edit commands for typos
- Retry edits

---

### Step 3: Update Format Version (2 minutes)

**Objective:** Increment version number to reflect template changes

**Edit:**
```
File: /mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-story-creation/assets/templates/story-template.md

Old: format_version: "2.0"
New: format_version: "2.1"
```

**Validation:**
```bash
grep 'format_version:' story-template.md
# Expected: format_version: "2.1"
```

**Checkpoint:**
- [ ] Format version updated to 2.1
- [ ] YAML frontmatter still valid (no syntax errors)

---

### Step 4: Add Changelog Header (20 minutes)

**Objective:** Document template evolution with version history

**Location:** After line 1, before line 2 (before `id: STORY-XXX`)

**Content to Add:**
```markdown
# =============================================================================
# STORY TEMPLATE CHANGELOG
# =============================================================================
#
# Version: 2.1
# Last Updated: 2025-01-21
# Maintained by: devforgeai-story-creation skill
#
# Version History:
#
# v2.1 (2025-01-21) - RCA-012 Remediation
#   Changes:
#     - Removed checkbox syntax from AC headers
#     - Format change: '### 1. [ ] Title' → '### AC#1: Title'
#     - Rationale: AC headers are definitions, not completion trackers
#     - Three-layer tracking system clarified in CLAUDE.md:
#       * TodoWrite (AI phase-level monitoring)
#       * AC Verification Checklist (granular sub-item tracking)
#       * Definition of Done (official completion record)
#   Impact:
#     - Eliminates user confusion about unchecked AC headers
#     - Clarifies AC headers are static definitions
#     - All future stories (58+) benefit from clear format
#   References:
#     - RCA-012: .devforgeai/RCA/RCA-012/
#     - Root cause: Vestigial checkboxes from pre-RCA-011 design
#
# v2.0 (2025-10-30) - Structured Tech Spec (RCA-006 Phase 2)
#   Changes:
#     - Added technical_specification YAML code block
#     - Machine-readable component definitions (Service, Worker, API, etc.)
#     - Test requirements embedded in each component
#     - Improved deterministic parsing for test generation
#   Impact:
#     - Test generation accuracy improved (85% → 95%+)
#     - Validation automation enabled
#   References:
#     - .devforgeai/specs/STRUCTURED-FORMAT-SPECIFICATION.md
#
# v1.0 (Initial) - Original Template
#   Features:
#     - User story format (As a... I want... So that...)
#     - AC headers with checkbox syntax (vestigial as of v2.1)
#     - Freeform technical specification
#     - Definition of Done section
#
# Migration Paths:
#   v1.0 → v2.0: Gradual (on story update)
#   v2.0 → v2.1: Optional script available
#     Location: .claude/skills/devforgeai-story-creation/scripts/migrate-ac-headers.sh
#     Usage: bash migrate-ac-headers.sh <story-file>
#     See: .devforgeai/RCA/RCA-012/MIGRATION-SCRIPT.md
#
# Backward Compatibility:
#   All versions (v1.0, v2.0, v2.1) supported by framework
#   Old stories continue to work without migration
#   Migration is optional (for visual consistency only)
#
# =============================================================================

```

**Validation:**
```bash
# Verify changelog present
head -60 story-template.md | grep "v2.1 (2025-01-21)"
# Expected: Should find changelog entry

# Verify YAML still valid
head -80 story-template.md | grep "^---"
# Expected: 2 lines (opening --- and closing ---)
```

**Checkpoint:**
- [ ] Changelog header added
- [ ] v2.1 changes documented
- [ ] v2.0 and v1.0 history included
- [ ] Migration path explained
- [ ] YAML frontmatter still valid

---

### Step 5: Validate Template Integrity (10 minutes)

**Objective:** Comprehensive validation that template is correct and complete

**Validation Suite:**
```bash
echo "=== Template v2.1 Validation ==="

# Test 1: AC header format
ac_new=$(grep -c "^### AC#[1-4]:" story-template.md)
if [ $ac_new -eq 4 ]; then
  echo "✓ Test 1 PASS: AC headers use new format (4 found)"
else
  echo "✗ Test 1 FAIL: Expected 4 AC headers, found $ac_new"
fi

# Test 2: No old format
ac_old=$(grep -c "^### [0-9]\. \[" story-template.md 2>/dev/null || echo 0)
if [ $ac_old -eq 0 ]; then
  echo "✓ Test 2 PASS: No old format remains"
else
  echo "✗ Test 2 FAIL: Old format found ($ac_old instances)"
fi

# Test 3: Format version
if grep -q 'format_version: "2.1"' story-template.md; then
  echo "✓ Test 3 PASS: Format version is 2.1"
else
  echo "✗ Test 3 FAIL: Format version not 2.1"
fi

# Test 4: Changelog present
if grep -q "v2.1 (2025-01-21)" story-template.md; then
  echo "✓ Test 4 PASS: Changelog present"
else
  echo "✗ Test 4 FAIL: Changelog missing"
fi

# Test 5: YAML valid
yaml_markers=$(grep -c "^---$" story-template.md | head -1)
if [ $yaml_markers -ge 2 ]; then
  echo "✓ Test 5 PASS: YAML frontmatter intact"
else
  echo "✗ Test 5 FAIL: YAML frontmatter broken"
fi

# Test 6: All sections present
sections=$(grep -c "^## " story-template.md)
if [ $sections -ge 10 ]; then
  echo "✓ Test 6 PASS: All template sections present ($sections sections)"
else
  echo "✗ Test 6 FAIL: Missing sections (found $sections, expected ≥10)"
fi

echo "=== Validation Complete ==="
```

**Checkpoint:**
- [ ] Test 1: AC header format PASS
- [ ] Test 2: Old format removed PASS
- [ ] Test 3: Format version PASS
- [ ] Test 4: Changelog present PASS
- [ ] Test 5: YAML valid PASS
- [ ] Test 6: Sections intact PASS
- [ ] All 6 tests PASS

**If Any Fail:**
- Review which test failed
- Check corresponding step (2, 3, or 4)
- Fix issue
- Re-run validation
- Do NOT proceed until all 6 tests pass

---

### Step 6: Update devforgeai-story-creation Skill (30 minutes)

**Objective:** Add version history section to skill documentation

**File:** `/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-story-creation/SKILL.md`

**Action:** Find section about story template (search for "template" or "Template Format")

**Add New Section:**
```markdown
### Story Template Versions

**Current Version:** 2.1 (as of 2025-01-21)

**Version History:**

**v2.1 (2025-01-21) - AC Header Clarity Enhancement (RCA-012)**
- **Change:** Removed checkbox syntax from AC headers
  - Before: `### 1. [ ] Criterion Title`
  - After: `### AC#1: Criterion Title`
- **Rationale:** AC headers are definitions (what to test), not trackers (what's complete)
- **Impact:** Eliminates systematic user confusion about unchecked AC headers in completed stories
- **RCA Reference:** .devforgeai/RCA/RCA-012/

**v2.0 (2025-10-30) - Structured Tech Spec (RCA-006 Phase 2)**
- **Change:** Added machine-readable technical_specification YAML block
  - Component types: Service, Worker, Configuration, API, Repository, DataModel, Logging
  - Embedded test requirements for each component
  - Deterministic parsing for test generation
- **Impact:** Test generation accuracy improved from 85% to 95%+
- **Specification:** .devforgeai/specs/STRUCTURED-FORMAT-SPECIFICATION.md

**v1.0 (Initial) - Original Template**
- **Features:** User story format, AC headers with checkboxes, freeform tech spec, Definition of Done
- **Status:** Legacy format (still supported for backward compatibility)

**Migration Paths:**
- **v1.0 → v2.0:** Gradual (updated on story modification)
- **v2.0 → v2.1:** Optional automated migration
  - Script: `.claude/skills/devforgeai-story-creation/scripts/migrate-ac-headers.sh`
  - Usage: `bash migrate-ac-headers.sh <story-file>`
  - Documentation: `.devforgeai/RCA/RCA-012/MIGRATION-SCRIPT.md`
- **Backward Compatibility:** All versions supported by framework

**Template Location:** `assets/templates/story-template.md`

**See Also:** Template changelog in story-template.md header (lines 1-50)
```

**Validation:**
```bash
# Verify section added
grep -A 20 "Story Template Versions" .claude/skills/devforgeai-story-creation/SKILL.md

# Verify all 3 versions documented
grep "v2.1" .claude/skills/devforgeai-story-creation/SKILL.md
grep "v2.0" .claude/skills/devforgeai-story-creation/SKILL.md
grep "v1.0" .claude/skills/devforgeai-story-creation/SKILL.md
# Expected: All 3 versions mentioned
```

**Checkpoint:**
- [ ] Section added to skill SKILL.md
- [ ] All 3 versions documented (v1.0, v2.0, v2.1)
- [ ] Change rationale explained for each version
- [ ] Migration path documented
- [ ] Cross-reference to template changelog present

---

### Step 7: Update CLAUDE.md Documentation (45 minutes)

**Objective:** Add comprehensive section explaining three-layer tracking and AC header purpose

**File:** `/mnt/c/Projects/DevForgeAI2/src/CLAUDE.md`

**Location:** After "Story Progress Tracking (NEW - RCA-011)" section

**Search For:** `## Story Progress Tracking (NEW - RCA-011)` (around line 450-500)

**Insert After That Section:**

**Content to Add:**
```markdown
---

## Acceptance Criteria vs. Tracking Mechanisms (RCA-012 Clarification)

**IMPORTANT:** Stories contain both AC **definitions** and AC **tracking**. Understanding the distinction eliminates confusion about unchecked checkboxes.

### Three Tracking Mechanisms

| Element | Purpose | Checkbox Behavior | Updated When | Source of Truth |
|---------|---------|-------------------|--------------|-----------------|
| **AC Headers** (e.g., `### AC#1: Title`) | **Define what to test** (immutable specification) | **Never marked** (no checkboxes as of v2.1) | Never (definitions are static) | Story creation |
| **AC Verification Checklist** | **Track granular progress** (real-time sub-items) | Marked `[x]` during TDD phases | End of each TDD phase (1-5) | TDD execution |
| **Definition of Done** | **Official completion record** (quality gate) | Marked `[x]` in Phase 4.5-5 Bridge | After deferrals validated, before commit | Quality gate validation |

---

### Why AC Headers Have No Checkboxes (Template v2.1+)

**AC headers are specifications, not progress trackers.**

Acceptance Criteria define **WHAT needs to be tested/implemented**. They are static requirements that remain valid throughout the story lifecycle. Marking an AC header "complete" would incorrectly imply the requirement is no longer relevant.

**Progress tracking happens in two places:**
1. **AC Verification Checklist** - Granular sub-item tracking (20-50 items per story, updated during TDD phases)
2. **Definition of Done** - Official completion tracking (30-40 items per story, updated in Phase 4.5-5 Bridge)

**Example (STORY-052 - Documentation Story):**

**AC Header (Definition - Never Marked):**
```markdown
### AC#1: Document Completeness - Core Content Coverage

**Given** the effective prompting guide exists
**When** a user reads the guide
**Then** the document contains:
- Introduction explaining why clear input matters (≥200 words)
- Command-specific guidance for 11 commands
- 20-30 before/after examples
- Quick reference checklist
- ≥10 common pitfalls
```
↑ This is a **specification** - defines what success looks like

**DoD Items (Completion Tracker - Marked When Complete):**
```markdown
### Implementation
- [x] Document includes introduction (648 words explaining purpose and value)
- [x] All 11 commands have dedicated guidance sections
- [x] 24 before/after examples included with explanations
- [x] Quick reference checklist created (in first 500 lines)
- [x] Common pitfalls section (10 pitfalls with mitigations)
```
↑ These are **completion records** - marked [x] when work is done

**The Distinction:**
- **AC Header:** "Document must have ≥200 word introduction" (requirement definition)
- **DoD Item:** "Document includes introduction (648 words)" (completion evidence)

---

### For Older Stories (Template v2.0 and Earlier)

**Template Evolution Timeline:**
- **v1.0 stories:** AC headers have `### 1. [ ]` checkbox syntax (vestigial)
- **v2.0 stories:** AC headers have `### 1. [ ]` checkbox syntax (vestigial)
- **v2.1 stories:** AC headers have `### AC#1:` format (no checkboxes) ← NEW

**Important:** In v1.0/v2.0 stories, AC header checkboxes may or may not be marked:
- **20% of stories (e.g., STORY-007):** AC headers marked `[x]` when DoD 100% complete
- **80% of stories (e.g., STORY-014, STORY-023, STORY-030, STORY-052):** AC headers left `[ ]` regardless of completion

**No documented convention existed** for v1.0/v2.0 templates, leading to framework-wide inconsistency discovered in RCA-012.

**Guidance for Reviewing Old Stories:**

**❌ Do NOT rely on AC header checkboxes** in v1.0/v2.0 stories - they don't reliably indicate completion

**✅ Check Definition of Done section instead:**
```markdown
## Definition of Done

### Implementation
- [x] Feature implemented  ← All items [x] = Implementation complete
- [x] Code reviewed

### Quality
- [x] Tests passing        ← All items [x] = Quality validated
- [x] Coverage met

### Testing
- [x] Unit tests           ← All items [x] = Testing complete
- [x] Integration tests

### Documentation
- [x] Docs updated          ← All items [x] = Documentation complete
```

**If DoD has unchecked items `[ ]`:**
1. Check for **"Approved Deferrals"** section in Implementation Notes
2. **If section exists** with user approval timestamp → Valid deferral (story complete per agreement)
3. **If section missing** → Story incomplete (should NOT be "QA Approved" - quality gate violation)

---

### How to Determine Story Completion Status

**Single Source of Truth: Definition of Done Section**

**Decision Tree:**
```
Want to know if story is complete?
  ↓
Check DoD section
  ├─ All items [x]? → Story 100% complete ✅
  └─ Some items [ ]?
      ↓
      Check for "Approved Deferrals" section
        ├─ Section exists with user approval timestamp?
        │   → Story complete with documented deferrals ✅
        └─ Section missing?
            → Story incomplete (quality gate violation) ❌
```

**Secondary Indicator: Workflow Status**
```markdown
## Workflow Status
- [x] Architecture phase complete
- [x] Development phase complete  ← Status "Dev Complete" matches this
- [ ] QA phase complete           ← Status "QA Approved" would mark this [x]
- [ ] Released                    ← Status "Released" would mark this [x]
```

---

### Quality Gate Rule (As of RCA-012 Remediation)

**QA Validation Now Enforces (Phase 0.9):**

1. **100% AC-to-DoD traceability**
   - Every AC requirement must have corresponding DoD item
   - Validated via explicit checkbox OR test validation OR metric validation

2. **Documented deferrals**
   - Any unchecked DoD item `[ ]` requires "Approved Deferrals" section
   - Section must include:
     - User approval timestamp (e.g., "2025-01-21 10:30 UTC")
     - Blocker justification (Dependency, Toolchain, Artifact, ADR, Low-Priority)
     - Follow-up reference (story ID or completion condition)

**QA Will HALT If:**
- AC requirement has no DoD coverage (traceability <100%)
- DoD has unchecked items without "Approved Deferrals" section
- Deferral section exists but missing user approval timestamp

**See:** `.claude/skills/devforgeai-qa/references/traceability-validation-algorithm.md` (created in RCA-012 Phase 2)

---

### Migration Guidance (Optional)

**Want to update old stories (v2.0) to new format (v2.1)?**

**Use migration script:**
```bash
bash .claude/skills/devforgeai-story-creation/scripts/migrate-ac-headers.sh <story-file>
```

**What it does:**
- Changes `### 1. [ ]` → `### AC#1:`
- Updates format_version: "2.0" → "2.1"
- Creates backup (.v2.0-backup) before changes
- Validates migration success

**When to migrate:**
- Want visual consistency across all stories
- Find checkbox syntax confusing in old stories
- Preparing stories for presentation/review

**When to skip:**
- Old format doesn't bother you
- Story is archived (no active work)
- Migration risk outweighs benefit

**See:** `.devforgeai/RCA/RCA-012/MIGRATION-SCRIPT.md` for complete migration documentation

---
```

**Validation:**
```bash
# Verify section added
grep -A 10 "Acceptance Criteria vs. Tracking Mechanisms" src/CLAUDE.md

# Verify table exists
grep "| Element | Purpose | Checkbox Behavior |" src/CLAUDE.md

# Verify quality gate rule documented
grep "100% AC-to-DoD traceability" src/CLAUDE.md
```

**Checkpoint:**
- [ ] Section added after RCA-011 section
- [ ] Table comparing three mechanisms present
- [ ] "Why AC headers have no checkboxes" explained
- [ ] Old story format caveat documented
- [ ] Single source of truth guidance clear
- [ ] Quality gate rule documented
- [ ] Migration guidance provided

---

### Step 8: Sync CLAUDE.md to Operational Location (2 minutes)

**Objective:** Make updated documentation available at root level

**Command:**
```bash
cd /mnt/c/Projects/DevForgeAI2

cp src/CLAUDE.md CLAUDE.md

# Verify sync
diff src/CLAUDE.md CLAUDE.md
# Expected: No output (files identical)
```

**Checkpoint:**
- [ ] CLAUDE.md synced to root
- [ ] Files are identical
- [ ] No sync errors

---

### Step 9: Test Story Creation with Template v2.1 (15 minutes)

**Objective:** Validate new stories use updated template correctly

**Command:**
```bash
# Create test story
# Use: /create-story "Phase 1 validation test story - Will be deleted after verification completes"
```

**Wait for story creation to complete, then:**

```bash
# Find test story (most recent)
TEST_STORY=$(ls -t /mnt/c/Projects/DevForgeAI2/.ai_docs/Stories/*.story.md | head -1)

echo "Test Story: $TEST_STORY"

# Validation 1: Format version
grep "format_version:" "$TEST_STORY"
# Expected: format_version: "2.1"

# Validation 2: AC header format
grep "^### AC#" "$TEST_STORY"
# Expected: ### AC#1: through ### AC#N: (where N = number of ACs)

# Validation 3: No old format
grep "^### [0-9]\. \[" "$TEST_STORY"
# Expected: No output (exit code 1)

# Validation 4: All sections present
grep -c "^## " "$TEST_STORY"
# Expected: ~10-12 major sections

# Display first 150 lines for manual review
head -150 "$TEST_STORY"
```

**Manual Review Questions:**
- Does the story look correct?
- Are AC headers using `### AC#N:` format?
- Is there any `### N. [ ]` format present?
- Are all template sections included?
- Does the story structure make sense?

**Checkpoint:**
- [ ] Test story created successfully
- [ ] Format version is 2.1
- [ ] AC headers use new format (no checkboxes)
- [ ] No old format present
- [ ] All template sections included
- [ ] Manual review confirms quality

**Cleanup:**
```bash
# After validation, delete test story
rm "$TEST_STORY"
echo "✓ Test story deleted after successful validation"
```

---

### Step 10: User Review and Approval (15 minutes)

**Objective:** Confirm user understands documentation and approves Phase 1

**Procedure:**

**Part A: Review CLAUDE.md Section**
```
Ask user to read:
  src/CLAUDE.md - "Acceptance Criteria vs. Tracking Mechanisms" section

Time: 5-10 minutes
```

**Part B: Review Old Story (STORY-052)**
```
Ask user to open:
  .ai_docs/Stories/STORY-052-user-facing-prompting-guide.story.md

Questions:
1. Do you see AC headers with `### 1. [ ]` format?
2. Are they checked or unchecked?
3. After reading CLAUDE.md, do you now understand why they're unchecked?
4. Where is the source of truth for completion status?

Expected Answers:
1. Yes (STORY-052 has v2.0 format)
2. Unchecked (all AC headers show [ ])
3. Yes (AC headers are definitions, not trackers)
4. Definition of Done section (shows 100% complete)
```

**Part C: Review New Story**
```
Ask user to open:
  {TEST_STORY created in Step 9}

Questions:
1. Do AC headers have checkboxes?
2. Is the format clearer than old version?
3. Any confusion about what AC headers represent?

Expected Answers:
1. No (v2.1 format has no checkbox syntax)
2. Yes (clearer, no ambiguous checkboxes)
3. No (clear they're definitions)
```

**User Feedback Collection:**
```bash
# Create feedback file
cat > .devforgeai/RCA/RCA-012/phase1-user-feedback.md << 'EOF'
# Phase 1 User Feedback

**Reviewer:** {User Name}
**Date:** 2025-01-21
**Time:** {HH:MM UTC}

## Documentation Clarity

**CLAUDE.md Section Review:**
- [ ] Table comparing three mechanisms is clear
- [ ] Explanation of AC headers helps understanding
- [ ] Old story format caveat addresses my confusion
- [ ] Quality gate rule makes sense

**Rating:** {1-5 scale, where 5 = very clear}

## Template v2.1 Review

**New Story Format:**
- [ ] AC headers without checkboxes are clearer
- [ ] Format is less ambiguous than v2.0
- [ ] I understand AC headers are definitions now
- [ ] I know to check DoD section for completion status

**Rating:** {1-5 scale, where 5 = much better}

## Overall Assessment

**Remaining Questions:**
1. {Question 1 if any}
2. {Question 2 if any}

**Recommendation:**
- [ ] Approve Phase 1 - Proceed to Phase 2
- [ ] Request revisions - {What needs improvement?}

**Approval Timestamp:** {YYYY-MM-DD HH:MM UTC}
**Signature:** {User Name}
EOF

# User fills out feedback
```

**Checkpoint:**
- [ ] User reviewed CLAUDE.md section
- [ ] User reviewed STORY-052 (old format)
- [ ] User reviewed test story (new format)
- [ ] User answered all questions correctly
- [ ] User reports no remaining confusion
- [ ] User approves Phase 1 completion
- [ ] Feedback documented

**If User Confused:**
- Note specific confusion points
- Revise CLAUDE.md section for clarity
- Re-test with user
- Iterate until user approves

---

## Phase 1 Completion Checklist

**All items MUST be checked before proceeding to Phase 2:**

### Template Changes
- [ ] Step 1: Template backup created
- [ ] Step 2: AC headers updated (4 edits applied)
- [ ] Step 3: Format version updated to 2.1
- [ ] Step 4: Changelog header added
- [ ] Step 5: Template integrity validated (6/6 tests pass)

### Documentation Updates
- [ ] Step 6: devforgeai-story-creation skill updated with version history
- [ ] Step 7: CLAUDE.md updated with tracking mechanisms section
- [ ] Step 8: CLAUDE.md synced to root directory

### Validation
- [ ] Step 9: Test story created and validated
- [ ] Step 10: User review completed and approved

### Final Checks
- [ ] Template v2.1 operational (new stories use it)
- [ ] Documentation clear (user confirms understanding)
- [ ] No regressions (old stories still work)
- [ ] User approval obtained (feedback documented)

**Total:** 14 checkpoints, all must PASS

---

## Success Criteria

**Phase 1 is successful when:**

**Deliverables:**
- [x] Template v2.1 created with no AC header checkboxes
- [x] Template includes version changelog
- [x] CLAUDE.md documents three-layer tracking system
- [x] devforgeai-story-creation skill documents version history
- [x] Test story validates new format

**Validation:**
- [x] All 6 template integrity tests pass
- [x] Test story creation works without errors
- [x] User review confirms clarity (no confusion)
- [x] User approval documented

**Metrics:**
- Template changes: 4 edits + 1 version update + 1 changelog = 6 total changes
- Documentation: 2 files updated (CLAUDE.md, SKILL.md)
- Testing: 6 automated tests + 1 integration test + 1 user review
- Time: ≤2.5 hours (target: 2.25 hours)

**User Experience:**
- User creates new story → sees `### AC#1:` format
- User reads CLAUDE.md → understands three-layer tracking
- User reviews old story → knows to check DoD for completion
- User reports: "Now I understand - no more confusion"

---

## Risk Mitigation

### Risk 1: Template Breaks Story Creation

**Likelihood:** Low (simple format change)
**Mitigation:** Comprehensive validation (Step 5), test story creation (Step 9)
**Rollback:** Restore from backup (Step 1 created backup)

---

### Risk 2: User Still Confused

**Likelihood:** Low (documentation is comprehensive)
**Mitigation:** User review (Step 10), iterative refinement
**Rollback:** Revise CLAUDE.md section, re-test

---

### Risk 3: Old Stories Break

**Likelihood:** Very Low (backward compatible by design)
**Mitigation:** Regression testing (validate /dev, /qa work on old stories)
**Rollback:** Framework supports both formats, no rollback needed

---

## Rollback Procedure (If Needed)

**If Phase 1 must be rolled back:**

### Step R1: Restore Template
```bash
cd /mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-story-creation/assets/templates/

mv story-template.md story-template.md.v2.1-failed
mv story-template.md.v2.0-backup story-template.md

echo "✓ Template rolled back to v2.0"
```

### Step R2: Revert CLAUDE.md
```bash
cd /mnt/c/Projects/DevForgeAI2

# Use git to revert
git checkout src/CLAUDE.md CLAUDE.md

echo "✓ CLAUDE.md reverted"
```

### Step R3: Revert Skill Documentation
```
Edit .claude/skills/devforgeai-story-creation/SKILL.md
Remove "Story Template Versions" section
Save changes
```

### Step R4: Document Rollback Reason
```bash
cat > .devforgeai/RCA/RCA-012/PHASE1-ROLLBACK-LOG.md << 'EOF'
# Phase 1 Rollback Log

**Date:** {timestamp}
**Reason:** {Why rollback was necessary}

**Issue:**
{What went wrong}

**Impact:**
{What didn't work}

**Next Steps:**
{Revised approach}
EOF
```

---

## Timeline

### Optimistic (Everything Goes Smoothly)

| Step | Duration | Cumulative |
|------|----------|------------|
| 1. Backup template | 5 min | 5 min |
| 2. Update AC headers | 15 min | 20 min |
| 3. Update version | 2 min | 22 min |
| 4. Add changelog | 20 min | 42 min |
| 5. Validate integrity | 10 min | 52 min |
| 6. Update skill docs | 30 min | 1h 22min |
| 7. Update CLAUDE.md | 45 min | 2h 7min |
| 8. Sync CLAUDE.md | 2 min | 2h 9min |
| 9. Test story creation | 15 min | 2h 24min |
| 10. User review | 15 min | 2h 39min |
| **Total** | **2h 39min** | - |

**Buffer:** 2h 39min actual vs. 2h 15min estimated = 24 minutes over (acceptable)

---

### Realistic (With Review Cycles)

| Step | Duration | Cumulative |
|------|----------|------------|
| Steps 1-5 | 1 hour | 1 hour |
| Steps 6-8 | 1.5 hours | 2.5 hours |
| Steps 9-10 | 30 min | 3 hours |
| **Total** | **3 hours** | - |

**Buffer:** Includes time for review, iteration, and user questions

---

### Pessimistic (Issues Encountered)

| Activity | Duration | Cumulative |
|----------|----------|------------|
| Initial implementation | 2.5 hours | 2.5 hours |
| Issue discovered | - | - |
| Investigation | 30 min | 3 hours |
| Fix and re-test | 30 min | 3.5 hours |
| User review iteration | 30 min | 4 hours |
| **Total** | **4 hours** | - |

**Worst Case:** If major issue found requiring significant rework

---

## Execution Sequence Summary

```
START Phase 1
  ↓
[1] Backup template (5 min) ✓ Safety first
  ↓
[2-4] Update template (37 min) ✓ Core changes
  ↓
[5] Validate integrity (10 min) ✓ Quality check
  ↓
[6-8] Update documentation (1h 17min) ✓ User guidance
  ↓
[9] Test story creation (15 min) ✓ Integration test
  ↓
[10] User review (15 min) ✓ Acceptance test
  ↓
PHASE 1 COMPLETE (2h 39min)
  ↓
Proceed to Phase 2? (User Decision)
```

---

## Deliverables Checklist

**After Phase 1 completes, you will have:**

### Files Modified
- [ ] `.claude/skills/devforgeai-story-creation/assets/templates/story-template.md` (v2.1)
- [ ] `.claude/skills/devforgeai-story-creation/SKILL.md` (version history added)
- [ ] `src/CLAUDE.md` (tracking mechanisms section added)
- [ ] `CLAUDE.md` (synced from src/)

### Files Created
- [ ] `story-template.md.v2.0-backup` (safety backup)
- [ ] `.devforgeai/RCA/RCA-012/phase1-user-feedback.md` (approval record)

### Validation Evidence
- [ ] Template validation results (6/6 tests pass)
- [ ] Test story file (proves new format works)
- [ ] User feedback (proves documentation clarity)

### Documentation
- [ ] Template changelog documents v2.1 changes
- [ ] CLAUDE.md explains tracking mechanisms
- [ ] Skill documents version evolution

---

## Go/No-Go Decision Points

### Checkpoint 1: After Step 5 (Template Validation)

**Question:** Did all 6 template integrity tests pass?

**If YES:** Continue to Step 6 (documentation updates)
**If NO:** Stop, review failures, fix issues, re-validate before proceeding

---

### Checkpoint 2: After Step 9 (Test Story)

**Question:** Did test story creation work correctly with new template?

**If YES:** Continue to Step 10 (user review)
**If NO:** Stop, investigate template issue, fix, re-test before proceeding

---

### Checkpoint 3: After Step 10 (User Review)

**Question:** Did user approve Phase 1 completion?

**If YES:** Phase 1 COMPLETE, proceed to Phase 2 planning
**If NO:** Iterate on documentation, re-test, obtain approval before proceeding

---

## Post-Phase 1 Actions

**After Phase 1 completes successfully:**

### Immediate
1. Mark Phase 1 complete in `.devforgeai/RCA/RCA-012/INDEX.md`
2. Update Implementation Phases section (mark checkboxes [x])
3. Document actual effort vs. estimated (for future planning)

### Next Phase Preparation
1. Read IMPLEMENTATION-GUIDE.md Phase 2 section
2. Read QA-ENHANCEMENT.md (REC-5 details)
3. Allocate 2 hours for Phase 2 implementation
4. Schedule Phase 2 execution

### Optional
1. Announce template change to team (if applicable)
2. Create brief migration guide for users
3. Update any external documentation referencing template format

---

## Success Evidence Documentation

**Create success record:**
```bash
cat > .devforgeai/RCA/RCA-012/PHASE1-SUCCESS-RECORD.md << 'EOF'
# Phase 1 Success Record

**Completion Date:** 2025-01-21
**Actual Effort:** {XX hours YY minutes}
**Executor:** {Name}

## Deliverables Completed

- [x] Template v2.1 operational
- [x] CLAUDE.md updated
- [x] Skill documentation updated
- [x] Test story validated
- [x] User approval obtained

## Validation Results

**Template Integrity:** 6/6 tests PASS
**Test Story Creation:** PASS
**User Review:** APPROVED

**User Feedback:**
"{User quote about clarity improvement}"

**Evidence:**
- Template backup: story-template.md.v2.0-backup
- User feedback: phase1-user-feedback.md
- Test story: {filename} (deleted after validation)

## Next Steps

Proceed to Phase 2: QA Enhancement (REC-5)
Estimated effort: 2 hours
Target: Week 1, Days 4-7

**Sign-Off:**
Executor: {Name}
Reviewer: {Name}
Date: 2025-01-21
EOF
```

---

**PHASE 1 EXECUTION PLAN COMPLETE**

**Ready to Execute:** Yes (all steps defined, validation procedures ready)
**Estimated Time:** 2.25-3 hours (with buffer)
**Risk Level:** Low (simple changes, comprehensive validation, rollback available)
**Recommended Start:** Immediate (prevents all future AC header confusion)
