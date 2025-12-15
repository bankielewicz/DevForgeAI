# RCA-012 Implementation Guide
## Step-by-Step Remediation Execution

**Version:** 1.0
**Created:** 2025-01-21
**Audience:** Framework developers implementing RCA-012 recommendations

---

## Overview

This guide provides detailed, executable steps for implementing all RCA-012 recommendations across 4 phases.

**Prerequisites:**
- Read INDEX.md (navigation and overview)
- Read ANALYSIS.md (understand root cause)
- Read SAMPLING-REPORT.md (understand extent of problem)
- Read REMEDIATION-PLAN.md (understand strategy)

**Execution Approach:**
- Sequential phases (Phase 1 → 2 → 3 → 4)
- Validate each phase before proceeding
- Rollback procedures documented for each step
- Checkpoints for user review/approval

---

## Phase 1: Foundation (Template + Documentation)

**Duration:** 3 days (Days 1-3)
**Effort:** 2.25 hours
**Priority:** CRITICAL/HIGH
**Deliverables:** Template v2.1, CLAUDE.md update, version tracking

---

### Step 1.1: Backup Current Template (5 minutes)

**Command:**
```bash
cp .claude/skills/devforgeai-story-creation/assets/templates/story-template.md \
   .claude/skills/devforgeai-story-creation/assets/templates/story-template.md.v2.0-backup

echo "✓ Backup created"
ls -lh .claude/skills/devforgeai-story-creation/assets/templates/story-template.md*
```

**Validation:**
- [ ] Backup file exists
- [ ] Backup file size matches original (566 bytes)

**Rollback:** If issues found later, restore with:
```bash
mv .claude/skills/devforgeai-story-creation/assets/templates/story-template.md.v2.0-backup \
   .claude/skills/devforgeai-story-creation/assets/templates/story-template.md
```

---

### Step 1.2: Update Template AC Headers (15 minutes)

**File:** `.claude/skills/devforgeai-story-creation/assets/templates/story-template.md`

**Change 1: Remove checkbox syntax from AC headers (Lines 29, 42, 50, 58)**

Use Edit tool:
```
Old: ### 1. [ ] [Criterion 1 Title]
New: ### AC#1: [Criterion 1 Title]

Old: ### 2. [ ] [Criterion 2 Title]
New: ### AC#2: [Criterion 2 Title]

Old: ### 3. [ ] [Criterion 3 Title]
New: ### AC#3: [Criterion 3 Title]

Old: ### 4. [ ] [Criterion 4 Title]
New: ### AC#4: [Criterion 4 Title]
```

**Change 2: Update format version (Line 11)**
```
Old: format_version: "2.0"
New: format_version: "2.1"
```

**Change 3: Add changelog header (after line 1, before current YAML frontmatter)**

Add:
```yaml
# Story Template Changelog
# Version: 2.1
# Last Updated: 2025-01-21
#
# Changelog:
#   v2.1 (2025-01-21):
#     - Removed checkbox syntax from AC headers (RCA-012)
#     - Changed format: '### 1. [ ]' → '### AC#1:'
#     - Rationale: AC headers are definitions, not trackers
#     - Three-layer tracking: TodoWrite (phases), AC Checklist (sub-items), DoD (official)
#
#   v2.0 (2025-10-30):
#     - Added format_version to story YAML frontmatter
#     - Structured technical specification in YAML format
#
#   v1.0 (Initial):
#     - Original template format
#
```

**Validation:**
```bash
# Verify changes
grep "^### AC#" .claude/skills/devforgeai-story-creation/assets/templates/story-template.md
# Expected: 4 lines showing AC#1: through AC#4:

grep "format_version" .claude/skills/devforgeai-story-creation/assets/templates/story-template.md
# Expected: format_version: "2.1"

head -20 .claude/skills/devforgeai-story-creation/assets/templates/story-template.md
# Expected: Changelog visible in header
```

**Checkpoint:**
- [ ] AC headers use `### AC#N:` format (no checkboxes)
- [ ] Format version updated to 2.1
- [ ] Changelog header added with v2.1 entry
- [ ] Template still valid (no syntax errors)

---

### Step 1.3: Update devforgeai-story-creation Skill Documentation (15 minutes)

**File:** `.claude/skills/devforgeai-story-creation/SKILL.md`

**Location:** Find section about story template (search for "story template" or "template.md")

**Add New Section: "Story Template Versions"**

Insert after template description:
```markdown
### Story Template Versions

**Current Version:** 2.1 (as of 2025-01-21)

**Version History:**
- **v2.1** (2025-01-21): Removed AC header checkboxes, added changelog (RCA-012)
  - **Change:** `### 1. [ ] Title` → `### AC#1: Title`
  - **Rationale:** AC headers are definitions (what to test), not trackers (what's complete)
  - **Impact:** Eliminates user confusion about unchecked AC headers in completed stories

- **v2.0** (2025-10-30): Structured tech spec YAML format (RCA-006 Phase 2)
  - **Change:** Added `technical_specification` YAML code block
  - **Rationale:** Machine-readable specs for deterministic parsing
  - **Impact:** Improved test generation accuracy (85% → 95%+)

- **v1.0** (Initial): Original template format
  - **Format:** Freeform tech spec, AC headers with checkboxes

**Migration Path:**
- **v1.0 → v2.0:** Gradual (on story update)
- **v2.0 → v2.1:** Optional migration script available (see RCA-012/MIGRATION-SCRIPT.md)
- **Backward Compatibility:** All versions supported

**See:** Template changelog in `assets/templates/story-template.md` header
```

**Validation:**
```bash
grep -A 10 "Story Template Versions" .claude/skills/devforgeai-story-creation/SKILL.md
# Expected: Version history section visible
```

**Checkpoint:**
- [ ] Version history section added to skill documentation
- [ ] All 3 versions documented (v1.0, v2.0, v2.1)
- [ ] Migration path explained
- [ ] Backward compatibility noted

---

### Step 1.4: Update CLAUDE.md with Tracking Mechanisms Clarification (45 minutes)

**File:** `src/CLAUDE.md` (distribution source)

**Location:** After "Story Progress Tracking (NEW - RCA-011)" section (~line 470-500)

**Add New Section:**

```markdown
### Acceptance Criteria vs. Tracking Mechanisms (RCA-012 Clarification)

**IMPORTANT:** Stories contain both AC **definitions** and AC **tracking**:

| Element | Purpose | Checkbox Behavior | Updated When | Source of Truth |
|---------|---------|-------------------|--------------|-----------------|
| **AC Headers** (e.g., `### AC#1: Title`) | **Define what to test** (immutable) | **Never marked** (no checkboxes as of v2.1) | Never (definitions are static) | Story creation |
| **AC Verification Checklist** | **Track granular progress** (real-time) | Marked complete during TDD phases | End of each TDD phase (1-5) | TDD execution |
| **Definition of Done** | **Official completion record** (quality gate) | Marked complete in Phase 4.5-5 Bridge | After deferrals validated, before commit | Quality gate validation |

#### Why AC Headers Have No Checkboxes (Template v2.1+)

**AC headers are specifications, not progress trackers.**

Marking an AC header "complete" would imply the acceptance criterion is no longer relevant, which is incorrect. Acceptance criteria remain valid throughout the story lifecycle—they define what success looks like.

Progress tracking happens in:
1. **AC Verification Checklist** - Granular sub-item tracking (20-50 items per story)
2. **Definition of Done** - Official completion tracking (30-40 items per story)

**Example (STORY-052):**
- **AC Header:** `### AC#1: Document Completeness - Core Content Coverage` (definition, never marked)
- **AC Checklist:** 16 sub-items tracking granular progress (marked as phases complete)
- **DoD:** 8 items tracking official completion (marked in Phase 4.5-5 Bridge)

#### For Older Stories (Template v2.0 and Earlier)

**Template Evolution:**
- **v1.0 stories:** AC headers have `### 1. [ ]` checkbox syntax (vestigial)
- **v2.0 stories:** AC headers have `### 1. [ ]` checkbox syntax (vestigial)
- **v2.1 stories:** AC headers have `### AC#1:` format (no checkboxes)

**Important:** In v1.0/v2.0 stories, AC header checkboxes may or may not be marked:
- **Some stories** (e.g., STORY-007): AC headers marked `[x]` when DoD 100% complete
- **Most stories** (e.g., STORY-014, STORY-023, STORY-030): AC headers left `[ ]` regardless of completion

**No documented convention existed** for v1.0/v2.0 templates, leading to 80% inconsistency.

#### How to Determine Story Completion Status

**Single Source of Truth: Definition of Done Section**

```markdown
## Definition of Done

### Implementation
- [x] Feature implemented  ← If all marked [x], implementation complete
- [x] Code reviewed

### Quality
- [x] Tests passing        ← If all marked [x], quality validated
- [x] Coverage met

### Testing
- [x] Unit tests           ← If all marked [x], testing complete
- [x] Integration tests

### Documentation
- [x] Docs updated          ← If all marked [x], documentation complete
```

**If DoD has unchecked items `[ ]`:**
1. Check for "Approved Deferrals" section in Implementation Notes
2. If section exists with user approval timestamp → Valid deferral (work complete per agreement)
3. If section missing → Work incomplete (story should not be "QA Approved")

**Workflow Status Section (Secondary Indicator):**
```markdown
## Workflow Status
- [x] Architecture phase complete
- [x] Development phase complete  ← Story is "Dev Complete" when marked
- [ ] QA phase complete           ← Story is "QA Approved" when marked
- [ ] Released                    ← Story is "Released" when marked
```

**Ignore AC header checkboxes** in old stories (v1.0/v2.0) - they don't reliably indicate completion.

#### Quality Gate Rule (As of RCA-012 Remediation)

**QA Validation Now Requires:**
1. **100% AC-to-DoD traceability** - Every AC requirement must have corresponding DoD item (explicit checkbox OR test validation)
2. **Documented deferrals** - Any incomplete DoD item requires "Approved Deferrals" section with:
   - User approval timestamp
   - Blocker justification (dependency, toolchain, artifact, ADR)
   - Follow-up story reference (if deferring to future implementation)

**QA will FAIL if:**
- AC requirement has no DoD coverage (traceability <100%)
- DoD item incomplete without deferral documentation
- Deferral missing user approval timestamp

**See:** `.claude/skills/devforgeai-qa/references/traceability-validation-algorithm.md` (created in Phase 2)
```

**Validation:**
```bash
# Check section was added
grep -A 20 "Acceptance Criteria vs. Tracking Mechanisms" src/CLAUDE.md

# Verify table visible
grep "AC Headers.*Purpose.*Checkbox Behavior" src/CLAUDE.md
```

**Checkpoint:**
- [ ] New section added to CLAUDE.md
- [ ] Table clearly documents three tracking mechanisms
- [ ] v1.0/v2.0 template caveat explained
- [ ] Quality gate rule documented
- [ ] "Single Source of Truth" guidance clear

---

### Step 1.5: Sync CLAUDE.md to Operational Location (2 minutes)

**Command:**
```bash
cp src/CLAUDE.md CLAUDE.md

echo "✓ CLAUDE.md synced to root"
```

**Validation:**
```bash
diff src/CLAUDE.md CLAUDE.md
# Expected: No differences
```

**Checkpoint:**
- [ ] CLAUDE.md synced to root directory
- [ ] Both files identical
- [ ] Users see updated documentation

---

### Step 1.6: Test Template v2.1 with New Story Creation (20 minutes)

**Command:**
```bash
# Create test story to validate template format
/create-story "Test story for template v2.1 validation - Delete after verification"
```

**Expected Behavior:**
- Story created successfully
- AC headers show `### AC#1:` format (no checkbox syntax)
- Format version is "2.1" in YAML frontmatter
- All other template sections unchanged

**Validation:**
```bash
# Find the test story
TEST_STORY=$(ls -t devforgeai/specs/Stories/*.story.md | head -1)

echo "Test story: $TEST_STORY"

# Check AC header format
grep "^### AC#" "$TEST_STORY"
# Expected: ### AC#1: through ### AC#4: (or however many ACs)

# Check NO old format remains
grep "^### [0-9]\. \[" "$TEST_STORY"
# Expected: No matches (exit code 1)

# Check format version
grep "format_version" "$TEST_STORY"
# Expected: format_version: "2.1"
```

**Checkpoint:**
- [ ] Test story created successfully
- [ ] AC headers use `### AC#N:` format (no checkboxes)
- [ ] Format version is "2.1"
- [ ] No old `### N. [ ]` format present
- [ ] Template sections all present and correct

**Cleanup:**
```bash
# After validation, remove test story
rm "$TEST_STORY"
echo "✓ Test story removed"
```

---

### Step 1.7: User Review of Documentation (15 minutes)

**Request User Review:**

Ask user to:
1. Read CLAUDE.md new section: "Acceptance Criteria vs. Tracking Mechanisms"
2. Review STORY-052 (has old v2.0 format with unchecked AC headers)
3. Confirm understanding: DoD is source of truth, AC headers are definitions
4. Provide feedback: Is the explanation clear?

**Questions for User:**
- Does the CLAUDE.md section clarify the confusion?
- Is the "Single Source of Truth" guidance helpful?
- Any remaining questions about story completion tracking?

**Document Feedback:**
```bash
cat > .devforgeai/RCA/RCA-012/user-feedback-phase1.md << 'EOF'
# Phase 1 User Feedback

**Date:** 2025-01-XX
**Reviewer:** [User name]

**Documentation Clarity:**
- [ ] CLAUDE.md section is clear and helpful
- [ ] Table is easy to understand
- [ ] Examples clarify the distinction
- [ ] Quality gate rule makes sense

**Remaining Questions:**
1. [Question 1 if any]
2. [Question 2 if any]

**Approval:**
- [ ] Approve Phase 1 - Proceed to Phase 2
- [ ] Request revisions - [What needs improvement?]

**Timestamp:** YYYY-MM-DD HH:MM UTC
EOF

# User fills out feedback
```

**Checkpoint:**
- [ ] User reviewed CLAUDE.md documentation
- [ ] User confirms clarity (no confusion)
- [ ] User approved Phase 1 completion
- [ ] Feedback documented

---

### Phase 1 Completion Criteria

**All checkpoints MUST pass before Phase 2:**

- [ ] Template backup created (Step 1.1)
- [ ] AC headers updated to `### AC#N:` format (Step 1.2)
- [ ] Format version updated to 2.1 (Step 1.2)
- [ ] Changelog added to template (Step 1.2)
- [ ] devforgeai-story-creation skill updated with version history (Step 1.3)
- [ ] CLAUDE.md updated with tracking mechanisms section (Step 1.4)
- [ ] CLAUDE.md synced to root (Step 1.5)
- [ ] Test story validated new format (Step 1.6)
- [ ] User review completed and approved (Step 1.7)

**Validation Command:**
```bash
bash .devforgeai/RCA/RCA-012/scripts/validate-phase1.sh
```

**If All Pass:**
```
✓ Phase 1 COMPLETE
  - Template v2.1: Operational
  - Documentation: Updated
  - User Review: Approved
  - Ready for Phase 2
```

**If Any Fail:**
```
Review failures, address issues, re-validate
Do NOT proceed to Phase 2 until all checkpoints pass
```

---

## Phase 2: Quality Gate Enhancement (Days 4-7)

**Duration:** 4 days
**Effort:** 2 hours
**Priority:** HIGH
**Deliverables:** QA traceability validation (Phase 0.9)

---

### Step 2.1: Read QA Skill Current Implementation (10 minutes)

**Command:**
```bash
Read(.claude/skills/devforgeai-qa/SKILL.md)
```

**Purpose:** Understand current Phase 0 structure and where to insert Phase 0.9

**Note:** Find Phase 0 (Parameter Extraction) and Phase 1 (Validation Mode Selection) - Phase 0.9 goes between them

---

### Step 2.2: Create Traceability Validation Algorithm Reference (30 minutes)

**File:** `.claude/skills/devforgeai-qa/references/traceability-validation-algorithm.md` (NEW)

**Content:** See QA-ENHANCEMENT.md for complete algorithm

**Summary:**
- Extracts AC count and granular requirements
- Extracts DoD items (total, checked, unchecked)
- Maps AC requirements to DoD coverage
- Calculates traceability score (target: 100%)
- Validates incomplete items have "Approved Deferrals" section
- HALTS QA if traceability <100% or deferrals undocumented

**Testing:**
```bash
# Verify file created
ls -lh .claude/skills/devforgeai-qa/references/traceability-validation-algorithm.md

# Verify content complete
wc -l .claude/skills/devforgeai-qa/references/traceability-validation-algorithm.md
# Expected: ~200-300 lines
```

---

### Step 2.3: Add Phase 0.9 to devforgeai-qa Skill (45 minutes)

**File:** `.claude/skills/devforgeai-qa/SKILL.md`

**Location:** After Phase 0 (Parameter Extraction), before Phase 1 (Validation Mode Selection)

**Insert Phase 0.9:**
```markdown
---

## Phase 0.9: AC-DoD Traceability Validation (NEW - RCA-012)

**Purpose:** Verify every Acceptance Criterion requirement has corresponding Definition of Done coverage. Prevents quality gate bypass and ensures complete work.

**Reference:** See `references/traceability-validation-algorithm.md` for complete algorithm

**Execution:**

### Step 0.9.1: Load Traceability Algorithm
```
Read(file_path=".claude/skills/devforgeai-qa/references/traceability-validation-algorithm.md")
```

### Step 0.9.2: Extract and Validate
```
Execute algorithm from reference file:
  1. Count AC headers and granular requirements
  2. Count DoD items (total, checked, unchecked)
  3. Map AC requirements to DoD items
  4. Calculate traceability score
  5. Validate deferrals if DoD incomplete
  6. Apply quality gate rules
```

### Step 0.9.3: Display Traceability Report
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Phase 0.9: AC-DoD Traceability Validation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Acceptance Criteria Analysis:
  • Total ACs: {ac_count}
  • Total AC requirements (granular): {ac_req_count}
  • DoD items: {dod_total}

Traceability Mapping:
  • AC#1 ({req_count} requirements) → {dod_count} DoD items {status}
  • AC#2 ({req_count} requirements) → {dod_count} DoD items {status}
  [... for all ACs ...]

Traceability Score: {score}% {PASS/FAIL}

DoD Completion Status:
  • Total items: {dod_total}
  • Complete [x]: {dod_checked}
  • Incomplete [ ]: {dod_unchecked}
  • Completion: {completion_pct}%

{If incomplete items present}:
Deferral Documentation: {VALID/INVALID}
  • Approved Deferrals section: {EXISTS/MISSING}
  • User approval timestamp: {PRESENT/MISSING}
  • Deferred items documented: {count}/{unchecked_count}

{PASS/FAIL message}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 0.9.4: Quality Gate Decision
```
IF traceability_score < 100:
  HALT QA workflow (display remediation guidance)
  EXIT

IF dod_unchecked > 0 AND deferral_status == "INVALID":
  HALT QA workflow (display deferral documentation requirements)
  EXIT

IF all checks PASS:
  Proceed to Phase 1 (Validation Mode Selection)
```

**Checkpoint:**
- [ ] Traceability validation executed
- [ ] All AC requirements mapped to DoD items
- [ ] Incomplete items validated (approved deferrals OR blocking error)
- [ ] Quality gate enforced

---
```

**Validation:**
```bash
# Verify Phase 0.9 added
grep "Phase 0.9" .claude/skills/devforgeai-qa/SKILL.md

# Verify reference file mentioned
grep "traceability-validation-algorithm.md" .claude/skills/devforgeai-qa/SKILL.md
```

**Checkpoint:**
- [ ] Phase 0.9 added to QA skill
- [ ] Algorithm reference loaded
- [ ] Quality gate rules implemented
- [ ] Display template formatted

---

### Step 2.4: Test QA Traceability Validation (30 minutes)

**Test Scenario 1: Story with 100% Traceability (Should PASS)**
```bash
/qa STORY-007 light
# Expected: Phase 0.9 shows 100% traceability, QA continues
```

**Test Scenario 2: Story with Missing DoD Item (Should FAIL)**

Create test story with intentional gap:
```markdown
## Acceptance Criteria
### AC#1: Feature works correctly
**Given** valid input, **When** user submits, **Then** feature processes successfully

## Definition of Done
### Implementation
- [x] Feature implemented
# Missing DoD item for "processes successfully" requirement
```

Run QA:
```bash
/qa TEST-STORY light
# Expected: Phase 0.9 HALTS with "Missing DoD coverage for AC#1 requirement: processes successfully"
```

**Test Scenario 3: Story with Undocumented Incomplete DoD (Should FAIL)**

```bash
# Create story with incomplete DoD, no "Approved Deferrals" section
# Run QA
/qa TEST-STORY light
# Expected: Phase 0.9 HALTS with "Incomplete DoD without approval documentation"
```

**Checkpoint:**
- [ ] Test 1: 100% traceability → PASS (QA continues)
- [ ] Test 2: Missing DoD item → FAIL (QA halts with clear guidance)
- [ ] Test 3: Undocumented incomplete → FAIL (QA enforces deferral docs)
- [ ] All 3 scenarios behave correctly

---

### Phase 2 Completion Criteria

**All checkpoints MUST pass:**

- [ ] Traceability algorithm reference file created (Step 2.2)
- [ ] Phase 0.9 added to devforgeai-qa/SKILL.md (Step 2.3)
- [ ] Algorithm integration complete (Step 2.3)
- [ ] Test scenario 1: PASS for valid story (Step 2.4)
- [ ] Test scenario 2: FAIL for missing traceability (Step 2.4)
- [ ] Test scenario 3: FAIL for undocumented deferrals (Step 2.4)

**Validation Command:**
```bash
bash .devforgeai/RCA/RCA-012/scripts/validate-phase2.sh
```

**If All Pass:**
```
✓ Phase 2 COMPLETE
  - QA skill enhanced with traceability validation
  - Quality gate bypass prevention operational
  - Ready for Phase 3 (historical cleanup)
```

---

## Phase 3: Historical Cleanup (Days 8-14)

**Duration:** 7 days
**Effort:** 6 hours (updated from 4 hours based on sampling)
**Priority:** HIGH
**Deliverables:** STORY-038 fixed, all 39 stories audited, compliance report

---

### Step 3.1: Create Automated Audit Script (30 minutes)

**File:** `.devforgeai/RCA/RCA-012/scripts/audit-qa-approved-stories.sh` (NEW)

**Script Content:** See STORY-AUDIT.md for complete script

**Summary:** Script scans all 39 QA Approved stories and reports:
- DoD completion percentage
- Deferral documentation status
- Compliance flags (complete, documented deferrals, or undocumented incomplete)

**Testing:**
```bash
chmod +x .devforgeai/RCA/RCA-012/scripts/audit-qa-approved-stories.sh

bash .devforgeai/RCA/RCA-012/scripts/audit-qa-approved-stories.sh
# Expected: Output showing all 39 stories with compliance status
```

**Checkpoint:**
- [ ] Audit script created
- [ ] Script is executable
- [ ] Script runs without errors
- [ ] Output is readable and actionable

---

### Step 3.2: Run Audit and Generate Report (30 minutes)

**Command:**
```bash
bash .devforgeai/RCA/RCA-012/scripts/audit-qa-approved-stories.sh > .devforgeai/RCA/RCA-012/AUDIT-RESULTS.txt

cat .devforgeai/RCA/RCA-012/AUDIT-RESULTS.txt
```

**Review Output:**
- Identify stories flagged: "⚠️ INCOMPLETE DoD without deferral docs"
- Count total non-compliant stories
- Prioritize fixes (STORY-038 first, then others)

**Create Summary:**
```bash
cat > .devforgeai/RCA/RCA-012/COMPLIANCE-REPORT.md << 'EOF'
# QA Approved Stories Compliance Report

**Audit Date:** 2025-01-21
**Stories Audited:** 39
**Sample Findings Applied:** Yes (based on 5-story sample)

## Summary Statistics

- **Fully Compliant:** {count} stories (100% DoD OR documented deferrals)
- **Non-Compliant:** {count} stories (incomplete DoD without deferral docs)
- **Compliance Rate:** {percentage}%

## Non-Compliant Stories (Require Immediate Fix)

{List of stories with incomplete DoD, no deferral documentation}

## Action Required

{For each non-compliant story, list required action}
EOF
```

**Checkpoint:**
- [ ] Audit results generated
- [ ] Compliance report created
- [ ] Non-compliant stories identified
- [ ] Action plan created for each

---

### Step 3.3: Fix STORY-038 (Priority 1) (1 hour)

**File:** `devforgeai/specs/Stories/STORY-038-code-quality-metrics-validation-enhancement.story.md`

**Issue:** 4 incomplete DoD items without "Approved Deferrals" section

**Incomplete Items:**
1. Performance test: 10K LOC analysis <30s
2. Edge case test: Zero-line files
3. Edge case test: Binary files (non-code)
4. Threshold violation test: Extreme values

**Resolution:** Ask user for deferral approval

Use AskUserQuestion:
```
Question: "STORY-038 has 4 incomplete Testing items. Should these be:"
Options:
  1. "Completed now (implement missing tests)" - Write tests immediately
  2. "Deferred with approval (low priority enhancements)" - Document as approved deferrals
  3. "Removed (no longer relevant)" - Remove from DoD

Response determines action
```

**If user selects "Deferred with approval":**

Add to STORY-038 Implementation Notes:
```markdown
## Approved Deferrals

**User Approval:** 2025-01-21 [HH:MM] UTC
**Approval Type:** Low-Priority Enhancement Deferral

**Deferred Items:**
1. **Performance test: 10K LOC analysis <30s**
   - **Reason:** No large codebase available for benchmarking in framework itself
   - **Blocker Type:** Artifact (requires real project with 10K+ LOC)
   - **Follow-up:** Test in real project usage (Phase 4 validation)

2. **Edge case test: Zero-line files**
   - **Reason:** Edge case unlikely in practice (build fails on zero-line code files)
   - **Blocker Type:** Low priority (not critical path)
   - **Follow-up:** Implement if user reports issue

3. **Edge case test: Binary files**
   - **Reason:** Code quality tools skip binary files automatically
   - **Blocker Type:** Handled by tooling (not framework responsibility)
   - **Follow-up:** None required

4. **Threshold violation test: Extreme values**
   - **Reason:** Current threshold validation covers normal ranges
   - **Blocker Type:** Low priority (extreme values are edge cases)
   - **Follow-up:** Implement if needed during real project usage

**Impact:** Core functionality complete (quality metrics calculation, threshold validation, recommendations). Deferred items are enhancement-level, not critical path.
```

**Validation:**
```bash
# Verify section added
grep "Approved Deferrals" devforgeai/specs/Stories/STORY-038*.story.md

# Verify user approval timestamp
grep "User Approval: 2025-01-21" devforgeai/specs/Stories/STORY-038*.story.md

# Verify all 4 items documented
grep -c "Deferred Items" devforgeai/specs/Stories/STORY-038*.story.md | grep "1"
# (Should find exactly 1 "Deferred Items:" section header)
```

**Checkpoint:**
- [ ] User decision obtained (complete, defer, or remove)
- [ ] Action implemented (tests written OR deferrals documented OR items removed)
- [ ] STORY-038 updated with "Approved Deferrals" section
- [ ] User approval timestamp present
- [ ] All 4 items documented with justification

---

### Step 3.4: Fix Other Non-Compliant Stories (2-4 hours)

**Based on audit results, for EACH flagged story:**

**Process:**
1. Read story file completely
2. Identify incomplete DoD items (items marked `[ ]`)
3. Review Implementation Notes for deferral context
4. Determine if deferral was implicit (mentioned in notes) or missing
5. If implicit: Formalize with "Approved Deferrals" section
6. If missing: Ask user for approval/completion decision
7. Update story file accordingly
8. Mark story as "fixed" in audit tracking

**Template for Approved Deferrals Section:**
```markdown
## Approved Deferrals

**User Approval:** {date} {time} UTC
**Approval Type:** {Design-Phase | Low-Priority | Blocker-Dependent}

**Deferred Items:**
1. **{DoD item text}**
   - **Reason:** {Why this was deferred}
   - **Blocker Type:** {Dependency | Toolchain | Artifact | ADR | Low-Priority}
   - **Follow-up:** {What happens next - story reference or condition}

{Repeat for each deferred item}

**Impact:** {What's complete vs. what's deferred}
```

**Checkpoint (per story):**
- [ ] Story read and reviewed
- [ ] Incomplete items identified
- [ ] User approval obtained (if needed)
- [ ] "Approved Deferrals" section added
- [ ] All items documented with justification
- [ ] Story marked compliant in audit tracking

---

### Step 3.5: Generate Final Compliance Report (30 minutes)

**File:** `.devforgeai/RCA/RCA-012/COMPLIANCE-REPORT.md`

**Content:**
```markdown
# QA Approved Stories Compliance Report (Final)

**Audit Date:** 2025-01-21
**Stories Audited:** 39
**Stories Fixed:** {count}

## Compliance Status

**Before Remediation:**
- Compliant: {count} ({percentage}%)
- Non-Compliant: {count} ({percentage}%)

**After Remediation:**
- Compliant: 39 (100%)
- Non-Compliant: 0 (0%)

## Stories Fixed

{For each fixed story, document what was changed}

## Verification

All stories now have:
- [ ] 100% AC-to-DoD traceability OR
- [ ] Documented deferrals with user approval

Run verification:
```bash
bash .devforgeai/RCA/RCA-012/scripts/verify-compliance.sh
# Expected: 39/39 PASS
```
```

**Checkpoint:**
- [ ] Final compliance report generated
- [ ] All 39 stories verified compliant
- [ ] Verification script confirms 100% compliance
- [ ] Audit documentation complete

---

### Phase 3 Completion Criteria

**All checkpoints MUST pass:**

- [ ] Audit script created and executed (Step 3.1, 3.2)
- [ ] STORY-038 fixed with approved deferrals (Step 3.3)
- [ ] All flagged stories fixed (Step 3.4)
- [ ] Compliance report shows 100% (Step 3.5)
- [ ] Verification script confirms compliance (Step 3.5)

**Validation Command:**
```bash
bash .devforgeai/RCA/RCA-012/scripts/validate-phase3.sh
```

**If All Pass:**
```
✓ Phase 3 COMPLETE
  - All 39 stories audited
  - Non-compliant stories fixed
  - 100% compliance achieved
  - Ready for Phase 4 (automation)
```

---

## Phase 4: Automation & Long-Term Prevention (Days 15-21)

**Duration:** 7 days
**Effort:** 3.5 hours
**Priority:** MEDIUM
**Deliverables:** Migration script, traceability matrix template

---

### Step 4.1: Create Migration Script (1.5 hours)

**File:** `.claude/skills/devforgeai-story-creation/scripts/migrate-ac-headers.sh` (NEW)

**See:** MIGRATION-SCRIPT.md for complete implementation

**Testing:**
```bash
# Test on STORY-052 (has old format)
bash .claude/skills/devforgeai-story-creation/scripts/migrate-ac-headers.sh \
  devforgeai/specs/Stories/STORY-052-user-facing-prompting-guide.story.md

# Verify changes
grep "^### AC#" devforgeai/specs/Stories/STORY-052-user-facing-prompting-guide.story.md
# Expected: AC#1 through AC#6 (no checkbox syntax)

# Restore from backup (for now - user decides whether to keep migration)
mv devforgeai/specs/Stories/STORY-052-user-facing-prompting-guide.story.md.v2.0-backup \
   devforgeai/specs/Stories/STORY-052-user-facing-prompting-guide.story.md
```

**Checkpoint:**
- [ ] Migration script created
- [ ] Script tested on STORY-052
- [ ] Backup created before migration
- [ ] Migration successful (format updated correctly)
- [ ] Restore from backup works
- [ ] Script documented in MIGRATION-SCRIPT.md

---

### Step 4.2: Add Traceability Matrix to Template (2 hours)

**File:** `.claude/skills/devforgeai-story-creation/assets/templates/story-template.md`

**See:** TRACEABILITY-MATRIX.md for complete template section

**Summary:** Add new section showing visual mapping between AC requirements and DoD items

**Validation:**
```bash
# Create test story with new template
/create-story "Test traceability matrix template"

# Verify matrix section present
grep "AC-to-DoD Traceability Matrix" {test-story-file}

# Verify table structure
grep "| AC | Requirement | DoD Item |" {test-story-file}
```

**Checkpoint:**
- [ ] Traceability matrix section added to template
- [ ] Template v2.1 updated (includes matrix)
- [ ] Test story includes matrix
- [ ] Matrix format is clear and useful

---

### Phase 4 Completion Criteria

**All checkpoints MUST pass:**

- [ ] Migration script created and tested (Step 4.1)
- [ ] Traceability matrix added to template (Step 4.2)
- [ ] Template v2.1 fully enhanced
- [ ] All automation tools documented
- [ ] Long-term prevention mechanisms in place

**Validation Command:**
```bash
bash .devforgeai/RCA/RCA-012/scripts/validate-phase4.sh
```

**If All Pass:**
```
✓ Phase 4 COMPLETE
  - Migration script operational
  - Enhanced template available
  - Automation complete
  - RCA-012 remediation 100% complete
```

---

## Overall Implementation Checklist

### Phase 1: Foundation ✅ (Target: Day 3)
- [ ] Template v2.1 created (AC headers no checkboxes)
- [ ] CLAUDE.md updated (tracking mechanisms clarified)
- [ ] Version tracking operational
- [ ] Test story validated
- [ ] User review approved

### Phase 2: Quality Gate ✅ (Target: Day 7)
- [ ] Traceability algorithm created
- [ ] Phase 0.9 added to QA skill
- [ ] QA validation prevents bypasses
- [ ] Test scenarios all pass

### Phase 3: Historical Cleanup ✅ (Target: Day 14)
- [ ] Audit script executed
- [ ] STORY-038 fixed
- [ ] All non-compliant stories fixed
- [ ] Compliance report: 100%

### Phase 4: Automation ✅ (Target: Day 21)
- [ ] Migration script operational
- [ ] Traceability matrix in template
- [ ] Documentation complete

---

## Success Validation

**After all 4 phases complete:**

```bash
# Run comprehensive validation
bash .devforgeai/RCA/RCA-012/scripts/validate-all-phases.sh

# Expected output:
✓ Phase 1: Template v2.1 operational
✓ Phase 2: QA validation prevents bypasses
✓ Phase 3: All 39 stories compliant
✓ Phase 4: Automation tools available

✓ RCA-012 Remediation: COMPLETE
```

**User Acceptance Criteria:**
- [ ] Create new story → AC headers have no checkboxes
- [ ] Review old story → Understand DoD is source of truth
- [ ] Run /qa on incomplete story → QA halts with clear guidance
- [ ] No confusion about story completion status

**Framework Integrity Metrics:**
- AC-DoD traceability: 100%
- User confusion incidents: 0
- Quality gate bypasses: 0
- Template version tracking: Operational

---

## Rollback Procedures

**See REMEDIATION-PLAN.md for detailed rollback procedures per phase**

**Emergency Rollback (Full):**
```bash
# Restore template
mv .claude/skills/devforgeai-story-creation/assets/templates/story-template.md.v2.0-backup \
   .claude/skills/devforgeai-story-creation/assets/templates/story-template.md

# Revert CLAUDE.md (use git)
git checkout src/CLAUDE.md CLAUDE.md

# Remove Phase 0.9 from QA skill
# (Manual edit required)

echo "✓ Full rollback complete - framework restored to pre-RCA-012 state"
```

**When to Rollback:**
- Template v2.1 causes story creation failures
- User feedback indicates documentation unclear
- QA Phase 0.9 creates false positives (blocks valid stories)
- Migration script corrupts story files

---

## Timeline & Milestones

### Week 1
- **Day 1-3:** Phase 1 (Foundation)
  - Milestone: Template v2.1 operational, documentation updated
- **Day 4-7:** Phase 2 (Quality Gate)
  - Milestone: QA validation enhanced, bypass prevention active

### Week 2
- **Day 8-10:** Phase 3 Part 1 (Audit)
  - Milestone: Audit complete, non-compliant stories identified
- **Day 11-14:** Phase 3 Part 2 (Fixes)
  - Milestone: STORY-038 and all flagged stories fixed

### Week 3-4
- **Day 15-18:** Phase 4 Part 1 (Migration Script)
  - Milestone: Migration automation available
- **Day 19-21:** Phase 4 Part 2 (Template Enhancement)
  - Milestone: Traceability matrix operational

### Final Validation
- **Day 21:** Comprehensive validation
  - Milestone: All phases verified, RCA-012 remediation complete

---

## Support & Troubleshooting

### Common Issues

**Issue: Template change breaks story creation**
- **Symptom:** /create-story fails with syntax error
- **Diagnosis:** Check template YAML frontmatter format
- **Fix:** Verify changelog syntax is valid (comment format)
- **Prevention:** Test template before deployment

**Issue: QA Phase 0.9 false positive**
- **Symptom:** QA halts on story with valid traceability
- **Diagnosis:** Algorithm may miscount AC requirements
- **Fix:** Review algorithm, adjust parsing logic
- **Prevention:** Comprehensive test scenarios in Phase 2

**Issue: Migration script corrupts story**
- **Symptom:** Story file unreadable after migration
- **Diagnosis:** sed regex may have edge case
- **Fix:** Restore from backup (.v2.0-backup file)
- **Prevention:** Test on isolated stories first

### Getting Help

**If stuck during implementation:**
1. Check specific action plan document (TEMPLATE-REFACTORING.md, etc.)
2. Review validation procedures (VALIDATION-PROCEDURES.md)
3. Consult testing plan (TESTING-PLAN.md)
4. Trigger new RCA if unexpected issues emerge

---

## Completion Certification

**After implementation complete, certify:**

```markdown
# RCA-012 Implementation Certification

**Implementer:** {Name}
**Completion Date:** YYYY-MM-DD
**Total Effort:** {hours}

**Phase Completion:**
- [x] Phase 1: Foundation (Template v2.1, documentation)
- [x] Phase 2: Quality Gate (QA traceability validation)
- [x] Phase 3: Historical Cleanup (39 stories audited and fixed)
- [x] Phase 4: Automation (migration script, enhanced template)

**Validation Results:**
- [x] All phase validation scripts PASS
- [x] User acceptance criteria met
- [x] Framework integrity metrics achieved
- [x] No regressions detected

**Sign-off:**
Implementer: {Signature/Name}
Reviewer: {Signature/Name}
Date: YYYY-MM-DD

**RCA-012 Status:** RESOLVED
```

Save to: `.devforgeai/RCA/RCA-012/IMPLEMENTATION-CERTIFICATION.md`

---

**Implementation Guide Complete**
**Next:** Begin Phase 1 Step 1.1 (backup template) or read action plan documents for detailed implementation specs
