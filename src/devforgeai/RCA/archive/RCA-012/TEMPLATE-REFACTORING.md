# RCA-012: Template Refactoring (REC-1)
## Remove Vestigial AC Header Checkboxes

**Recommendation ID:** REC-1
**Priority:** CRITICAL
**Effort:** 1 hour
**Target:** Template v2.0 → v2.1

---

## Objective

Remove checkbox syntax `[ ]` from Acceptance Criteria headers in the story template, replacing with clear identifier format `AC#N:` to eliminate user confusion between definitions (what to test) and trackers (what's complete).

---

## Current State (Template v2.0)

**File:** `.claude/skills/devforgeai-story-creation/assets/templates/story-template.md`

**Lines 29, 42, 50, 58:**
```markdown
### 1. [ ] [Criterion 1 Title]

**Given** [initial context/state],
**When** [action/event occurs],
**Then** [expected outcome].

---

### 2. [ ] [Criterion 2 Title]

**Given** [initial context/state],
**When** [action/event occurs],
**Then** [expected outcome].

---

### 3. [ ] [Criterion 3 Title]

**Given** [initial context/state],
**When** [action/event occurs],
**Then** [expected outcome].

---

### 4. [ ] [Criterion 4 Title]

**Given** [initial context/state],
**When** [action/event occurs],
**Then** [expected outcome].
```

**Problem:** Checkbox syntax `[ ]` creates false expectation that headers should be marked complete

---

## Desired State (Template v2.1)

**Lines 29, 42, 50, 58 (after refactoring):**
```markdown
### AC#1: [Criterion 1 Title]

**Given** [initial context/state],
**When** [action/event occurs],
**Then** [expected outcome].

---

### AC#2: [Criterion 2 Title]

**Given** [initial context/state],
**When** [action/event occurs],
**Then** [expected outcome].

---

### AC#3: [Criterion 3 Title]

**Given** [initial context/state],
**When** [action/event occurs],
**Then** [expected outcome].

---

### AC#4: [Criterion 4 Title]

**Given** [initial context/state],
**When** [action/event occurs],
**Then** [expected outcome].
```

**Benefit:** Clear identifier (`AC#1`) with no checkbox, eliminating ambiguity

---

## Implementation Steps

### Step 1: Backup Template (5 minutes)

**Command:**
```bash
cd .claude/skills/devforgeai-story-creation/assets/templates/

cp story-template.md story-template.md.v2.0-backup

ls -lh story-template.md*
```

**Expected Output:**
```
-rw-r--r-- 1 user user 18K Jan 21 08:00 story-template.md
-rw-r--r-- 1 user user 18K Jan 21 08:00 story-template.md.v2.0-backup
```

**Validation:**
- [ ] Backup file exists
- [ ] File sizes match
- [ ] Backup is readable

---

### Step 2: Update AC Header Format (15 minutes)

**Use Edit tool for precise replacement:**

**Edit 1: Line 29**
```
File: .claude/skills/devforgeai-story-creation/assets/templates/story-template.md

Old: ### 1. [ ] [Criterion 1 Title]
New: ### AC#1: [Criterion 1 Title]
```

**Edit 2: Line 42**
```
File: .claude/skills/devforgeai-story-creation/assets/templates/story-template.md

Old: ### 2. [ ] [Criterion 2 Title]
New: ### AC#2: [Criterion 2 Title]
```

**Edit 3: Line 50**
```
File: .claude/skills/devforgeai-story-creation/assets/templates/story-template.md

Old: ### 3. [ ] [Criterion 3 Title]
New: ### AC#3: [Criterion 3 Title]
```

**Edit 4: Line 58**
```
File: .claude/skills/devforgeai-story-creation/assets/templates/story-template.md

Old: ### 4. [ ] [Criterion 4 Title]
New: ### AC#4: [Criterion 4 Title]
```

**Validation:**
```bash
# Verify new format
grep "^### AC#" .claude/skills/devforgeai-story-creation/assets/templates/story-template.md

# Expected output:
### AC#1: [Criterion 1 Title]
### AC#2: [Criterion 2 Title]
### AC#3: [Criterion 3 Title]
### AC#4: [Criterion 4 Title]

# Verify old format is gone
grep "^### [0-9]\. \[" .claude/skills/devforgeai-story-creation/assets/templates/story-template.md
# Expected: No matches (exit code 1)
```

**Checkpoint:**
- [ ] All 4 AC headers updated
- [ ] New format uses `AC#N:` syntax
- [ ] No checkbox syntax remains
- [ ] Numbering preserved (AC#1 through AC#4)

---

### Step 3: Update Format Version (2 minutes)

**Edit Line 11:**
```
File: .claude/skills/devforgeai-story-creation/assets/templates/story-template.md

Old: format_version: "2.0"
New: format_version: "2.1"
```

**Validation:**
```bash
grep "format_version" .claude/skills/devforgeai-story-creation/assets/templates/story-template.md
# Expected: format_version: "2.1"
```

**Checkpoint:**
- [ ] Format version updated to 2.1
- [ ] YAML frontmatter still valid

---

### Step 4: Add Template Changelog Header (15 minutes)

**Location:** After line 1 (after first `---`), before line 2 (`id: STORY-XXX`)

**Add Comment Block:**
```
File: .claude/skills/devforgeai-story-creation/assets/templates/story-template.md

Insert after line 1:
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
#     - Three-layer tracking system: TodoWrite (phase-level), AC Checklist
#       (sub-item granular), DoD (official completion record)
#   Impact:
#     - Eliminates user confusion about unchecked AC headers
#     - Clarifies AC headers are static definitions
#     - All future stories (58+) benefit
#
# v2.0 (2025-10-30) - Structured Tech Spec (RCA-006 Phase 2)
#   Changes:
#     - Added technical_specification YAML code block
#     - Machine-readable component definitions (Service, Worker, API, etc.)
#     - Test requirements embedded in each component
#   Impact:
#     - Improved test generation accuracy (85% → 95%+)
#     - Deterministic parsing for validation
#
# v1.0 (Initial) - Original Template
#   Features:
#     - User story format (As a... I want... So that...)
#     - AC headers with checkbox syntax (vestigial as of v2.1)
#     - Freeform technical specification
#     - Definition of Done section
#
# Migration:
#   v1.0 → v2.0: Gradual (on story update)
#   v2.0 → v2.1: Optional script available (RCA-012/MIGRATION-SCRIPT.md)
#   Backward compatibility: All versions supported by framework
#
# =============================================================================

---
id: STORY-XXX
...
```

**Validation:**
```bash
head -50 .claude/skills/devforgeai-story-creation/assets/templates/story-template.md
# Expected: Changelog visible before YAML frontmatter
```

**Checkpoint:**
- [ ] Changelog header added
- [ ] v2.1 changes documented
- [ ] v2.0 and v1.0 history preserved
- [ ] Migration path explained

---

### Step 5: Validate Template Integrity (10 minutes)

**Comprehensive Validation:**

```bash
# Check template structure
echo "=== Template Validation ==="

# 1. YAML frontmatter valid
head -15 .claude/skills/devforgeai-story-creation/assets/templates/story-template.md | grep "^---"
# Expected: 2 lines (opening and closing YAML)

# 2. AC headers correct format
grep -c "^### AC#[1-4]:" .claude/skills/devforgeai-story-creation/assets/templates/story-template.md
# Expected: 4 (AC#1 through AC#4)

# 3. No old format remains
grep "^### [0-9]\. \[" .claude/skills/devforgeai-story-creation/assets/templates/story-template.md
# Expected: No matches (exit code 1 = success)

# 4. Format version correct
grep "format_version: \"2.1\"" .claude/skills/devforgeai-story-creation/assets/templates/story-template.md
# Expected: 1 match

# 5. Changelog present
grep "v2.1 (2025-01-21)" .claude/skills/devforgeai-story-creation/assets/templates/story-template.md
# Expected: 1 match

# 6. Template sections intact
grep -c "^## " .claude/skills/devforgeai-story-creation/assets/templates/story-template.md
# Expected: ~10-12 sections (Description, AC, Tech Spec, NFRs, Dependencies, etc.)

echo "=== Validation Complete ==="
```

**Checkpoint:**
- [ ] YAML frontmatter valid
- [ ] AC headers use new format (4 headers)
- [ ] No old format remains
- [ ] Format version is 2.1
- [ ] Changelog present and complete
- [ ] All template sections intact

---

### Step 6: Test Story Creation with Updated Template (15 minutes)

**Create Test Story:**
```bash
# Invoke story creation
/create-story "Test story to validate template v2.1 format - This is a test and will be deleted after verification"
```

**Expected Behavior:**
- Story created in `devforgeai/specs/Stories/STORY-{NNN}-test-story-*.story.md`
- Story uses template v2.1
- AC headers show `### AC#1:` format (no checkboxes)
- All other sections present

**Validation:**
```bash
# Find the test story (most recent)
TEST_STORY=$(ls -t devforgeai/specs/Stories/*.story.md | head -1)

echo "Test Story: $TEST_STORY"

# 1. Check format version
grep "format_version" "$TEST_STORY"
# Expected: format_version: "2.1"

# 2. Check AC header format
grep "^### AC#" "$TEST_STORY"
# Expected: ### AC#1: through ### AC#{N}: (based on story ACs)

# 3. Verify NO old format
grep "^### [0-9]\. \[" "$TEST_STORY"
# Expected: No matches (exit code 1 = success)

# 4. Verify story structure complete
grep -c "^## " "$TEST_STORY"
# Expected: ~10-12 major sections

# 5. Display story for manual review
cat "$TEST_STORY" | head -100
```

**Manual Review Questions:**
- Does the story look correct?
- Are AC headers clear (no ambiguous checkboxes)?
- Is the format consistent?
- Would you be confused about completion status?

**Checkpoint:**
- [ ] Test story created successfully
- [ ] Format version is 2.1
- [ ] AC headers use `### AC#N:` format
- [ ] No checkbox syntax in AC headers
- [ ] Story structure complete and valid
- [ ] Manual review confirms clarity

**Cleanup:**
```bash
# After validation, delete test story
rm "$TEST_STORY"
echo "✓ Test story deleted after successful validation"
```

---

## Detailed Specification

### AC Header Format Specification

**Before (v2.0):**
```markdown
### 1. [ ] [Criterion 1 Title]
     │   │   └── Placeholder for criterion title
     │   └────── Checkbox syntax (creates false expectation)
     └────────── Numeric identifier
```

**After (v2.1):**
```markdown
### AC#1: [Criterion 1 Title]
     │  │   └── Placeholder for criterion title
     │  └────── Separator (no checkbox)
     └───────── Clear identifier (AC = Acceptance Criterion, #1 = first)
```

**Rationale for `AC#N:` Format:**
- **AC** prefix clearly identifies as "Acceptance Criterion" (not arbitrary section)
- **#N** numbering maintains sequence (AC#1, AC#2, etc.)
- **Colon** separator is standard markdown heading convention
- **No checkbox** eliminates false expectation of marking complete

**Alternative Formats Considered:**
- `### Acceptance Criterion 1:` (too verbose)
- `### Criterion 1:` (ambiguous, could be any criterion)
- `### 1:` (too terse, loses AC context)
- `### AC 1:` (space breaks searchability, # symbol better)

**Selected:** `### AC#1:` - Balances clarity, brevity, and searchability

---

## Impact Analysis

### Positive Impacts

**For New Stories (STORY-058+):**
- Zero user confusion about AC header purpose
- Clear visual distinction between definitions and trackers
- Consistent format across all new work
- Easier to reference (e.g., "See AC#3 for performance criteria")

**For Framework Users:**
- Reduced cognitive load (one less thing to worry about)
- Clear guidance in CLAUDE.md (no more "should I mark these?")
- Confidence in DoD as source of truth

**For Framework Maintainers:**
- Consistent story format going forward
- Template evolution documented (changelog)
- Easier code reviews (no "why aren't AC headers marked?" questions)

### Potential Negative Impacts

**Old Stories Still Have Checkbox Syntax:**
- 57 existing stories have v1.0/v2.0 format
- Users may notice inconsistency between old and new
- **Mitigation:** CLAUDE.md documents this, explains old format
- **Optional:** Migration script available (REC-4, Phase 4)

**Breaking Change for Automated Tooling:**
- If any scripts parse `### N. [ ]` format, they'll break
- **Likelihood:** Low (no known tooling parses AC headers)
- **Mitigation:** Search codebase for regex patterns matching old format
- **Prevention:** Document format change in changelog

**User Habituation:**
- Users accustomed to v2.0 may expect checkboxes
- **Mitigation:** Clear documentation in CLAUDE.md
- **Timeline:** 1-2 stories for adjustment

---

## Backward Compatibility

### Template Version Support

**Framework Supports:**
- ✅ v1.0 stories (original format)
- ✅ v2.0 stories (structured tech spec with AC checkboxes)
- ✅ v2.1 stories (no AC checkboxes) ← NEW

**Migration Required:** No (all versions work)

**Migration Optional:** Yes (script available in Phase 4 for consistency)

### AC Header Parsing

**If any code parses AC headers, update regex:**

**Old Pattern (v2.0):**
```python
# Python
pattern = r'^### (\d+)\. \[(x| )\] (.+)$'

# Bash
grep '^### [0-9]\. \[' story.md
```

**New Pattern (v2.1):**
```python
# Python
pattern = r'^### AC#(\d+): (.+)$'

# Bash
grep '^### AC#[0-9]:' story.md
```

**Combined Pattern (supports both):**
```python
# Python
pattern = r'^### (?:(\d+)\. \[(x| )\] |AC#(\d+): )(.+)$'
# Captures: group 1 or 3 = number, group 4 = title

# Bash
grep -E '^### (AC#)?[0-9]' story.md
```

**Action Required:**
- Search codebase for AC header parsing
- Update regex patterns to support v2.1
- Maintain v2.0 compatibility (framework supports both)

---

## Rollback Procedure

**If template v2.1 causes issues:**

### Immediate Rollback (5 minutes)

```bash
cd .claude/skills/devforgeai-story-creation/assets/templates/

# Restore v2.0 from backup
mv story-template.md story-template.md.v2.1-failed
mv story-template.md.v2.0-backup story-template.md

echo "✓ Template rolled back to v2.0"
```

**Validation:**
```bash
grep "^### [0-9]\. \[" story-template.md
# Expected: 4 matches (old format restored)

grep "format_version" story-template.md
# Expected: format_version: "2.0"
```

### Document Rollback Reason

```bash
cat > devforgeai/RCA/RCA-012/ROLLBACK-LOG.md << 'EOF'
# REC-1 Rollback Log

**Date:** YYYY-MM-DD HH:MM UTC
**Reason:** {Why rollback was needed}

**Issue Encountered:**
{Describe what went wrong}

**Diagnosis:**
{What caused the issue}

**Resolution:**
{How to fix the root cause}

**Next Steps:**
{Revised approach or plan}
EOF
```

### Restore Confidence

- Review what broke
- Fix root cause
- Test fix in isolation
- Retry template update with fix applied

---

## Testing Strategy

### Unit Testing (Template Structure)

**Test 1: AC Header Format**
```bash
# Count AC headers with new format
ac_count=$(grep -c "^### AC#[0-9]:" story-template.md)

if [ $ac_count -eq 4 ]; then
  echo "✓ PASS: AC headers use new format (4 found)"
else
  echo "✗ FAIL: Expected 4 AC headers, found $ac_count"
fi
```

**Test 2: No Old Format Remains**
```bash
# Search for old format
old_format=$(grep -c "^### [0-9]\. \[" story-template.md)

if [ $old_format -eq 0 ]; then
  echo "✓ PASS: No old checkbox syntax found"
else
  echo "✗ FAIL: Old format still present ($old_format instances)"
fi
```

**Test 3: Format Version Correct**
```bash
# Check version
version=$(grep "format_version:" story-template.md | grep -o '"[0-9.]*"')

if [ "$version" == '"2.1"' ]; then
  echo "✓ PASS: Format version is 2.1"
else
  echo "✗ FAIL: Format version is $version (expected 2.1)"
fi
```

**Test 4: Changelog Present**
```bash
# Check for changelog
has_changelog=$(grep -c "v2.1 (2025-01-21)" story-template.md)

if [ $has_changelog -eq 1 ]; then
  echo "✓ PASS: Changelog present for v2.1"
else
  echo "✗ FAIL: Changelog missing or malformed"
fi
```

### Integration Testing (Story Creation)

**Test 5: Create Story with New Template**
```bash
# Create story
/create-story "Integration test for template v2.1 validation"

# Verify format
TEST_STORY=$(ls -t devforgeai/specs/Stories/*.story.md | head -1)
new_format=$(grep -c "^### AC#" "$TEST_STORY")

if [ $new_format -ge 1 ]; then
  echo "✓ PASS: New story uses AC#N format ($new_format ACs)"
else
  echo "✗ FAIL: New story doesn't use new format"
fi

# Cleanup
rm "$TEST_STORY"
```

### Regression Testing

**Test 6: Existing Stories Still Work**
```bash
# Verify old stories readable
/dev STORY-007
# Expected: Should work (backward compatible)

/qa STORY-007 light
# Expected: Should work (reads both formats)
```

**Test 7: Template Sections Intact**
```bash
# Verify all major sections present
sections=("Description" "Acceptance Criteria" "Technical Specification" "Dependencies" "Test Strategy" "Definition of Done")

for section in "${sections[@]}"; do
  if grep -q "^## $section" story-template.md; then
    echo "✓ Section present: $section"
  else
    echo "✗ Section missing: $section"
  fi
done
```

---

## Validation Checklist

**Pre-Implementation:**
- [ ] Backup created
- [ ] Current template reviewed
- [ ] Change scope understood (4 line edits + version + changelog)

**Implementation:**
- [ ] All 4 AC headers updated (Step 2)
- [ ] Format version updated (Step 3)
- [ ] Changelog added (Step 4)
- [ ] No syntax errors introduced

**Post-Implementation:**
- [ ] Unit tests pass (7/7)
- [ ] Integration test passes (story creation works)
- [ ] Regression tests pass (old stories still work)
- [ ] User review approved
- [ ] No rollback needed

**Final Validation:**
- [ ] Template v2.1 operational
- [ ] Next story created uses new format
- [ ] Framework integrity maintained
- [ ] User confusion eliminated

---

## Effort Breakdown

| Task | Estimated | Actual | Variance |
|------|-----------|--------|----------|
| Backup template | 5 min | ___ min | ___ |
| Update AC headers | 15 min | ___ min | ___ |
| Update version | 2 min | ___ min | ___ |
| Add changelog | 15 min | ___ min | ___ |
| Validate integrity | 10 min | ___ min | ___ |
| Test story creation | 15 min | ___ min | ___ |
| **Total** | **62 min** | ___ min | ___ |

**Budget:** 1 hour
**Buffer:** None (tasks are sequential and precise)

---

## Success Criteria

**REC-1 is successful when:**

- [ ] Template v2.1 created with no AC header checkboxes
- [ ] Format version updated to 2.1
- [ ] Changelog documents v2.1 changes
- [ ] Test story created with new format validates correctly
- [ ] User review confirms no confusion
- [ ] Backward compatibility maintained (old stories still work)
- [ ] No regressions detected
- [ ] All validation tests pass

**Evidence of Success:**
- New stories have clear AC definitions (no checkboxes)
- User feedback: "Now I understand AC headers are definitions"
- Zero questions about "should I mark AC headers?"
- Framework integrity maintained

---

## Related Documents

- **INDEX.md** - RCA-012 overview and navigation
- **ANALYSIS.md** - Root cause and 5 Whys
- **REMEDIATION-PLAN.md** - Complete 4-phase strategy
- **IMPLEMENTATION-GUIDE.md** - Step-by-step execution (this is Step 1.2)
- **VALIDATION-PROCEDURES.md** - Testing procedures
- **CONVENTIONS.md** - AC checkbox usage conventions (established by this fix)

---

**REC-1 Status:** Ready for Implementation
**Estimated Duration:** 1 hour
**Priority:** CRITICAL (implements immediately, prevents all future confusion)
