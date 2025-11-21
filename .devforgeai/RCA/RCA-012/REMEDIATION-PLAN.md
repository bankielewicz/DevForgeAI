# RCA-012 Remediation Plan
## AC-DoD Traceability and Checkbox Convention System

**Version:** 1.0
**Created:** 2025-01-21
**Status:** Ready for Implementation

---

## Problem Statement

**Current State:**
- 80% of QA Approved stories have inconsistent AC header checkbox usage
- 20% compliance rate for AC-to-DoD traceability
- No documented convention for when/how to mark AC headers
- Quality gate bypass detected (STORY-038 reached QA Approved with 4 undocumented incomplete DoD items)
- Template design creates user confusion (checkbox syntax suggests marking, but headers are definitions not trackers)

**Desired State:**
- 100% of stories have clear, unambiguous completion tracking
- AC headers clearly identified as definitions (not trackers)
- DoD section is the single source of truth for completion status
- QA validation enforces AC-DoD traceability
- Zero user confusion about story completion

---

## Strategic Approach

### 4-Phase Sequential Implementation

**Phase 1: Foundation (Template + Documentation)**
- Fix root cause: Update template to remove vestigial checkboxes
- Document conventions: Clarify tracking mechanisms in CLAUDE.md
- Prevent future issues: All new stories use clear format

**Phase 2: Quality Gate Enhancement**
- Add validation: QA checks AC-DoD traceability
- Enforce standards: QA fails if traceability <100%
- Prevent bypasses: Catch incomplete DoD early

**Phase 3: Historical Cleanup**
- Audit existing stories: Review all 39 QA Approved stories
- Fix non-compliance: Document deferrals, update incomplete items
- Restore integrity: Framework-wide compliance verified

**Phase 4: Automation & Long-Term Prevention**
- Migration tools: Optional script for updating old stories
- Enhanced templates: Traceability matrix built into template
- Monitoring: Automated compliance tracking

---

## Phase 1: Foundation (Week 1, Days 1-3)

### Objectives
1. Eliminate vestigial AC header checkboxes from template
2. Document AC vs. tracking mechanisms distinction
3. Version track template changes
4. Prevent all future confusion

### Deliverables

#### REC-1: Template Refactoring
**File:** `.claude/skills/devforgeai-story-creation/assets/templates/story-template.md`

**Changes:**
```diff
- ### 1. [ ] [Criterion 1 Title]
+ ### AC#1: [Criterion 1 Title]

- ### 2. [ ] [Criterion 2 Title]
+ ### AC#2: [Criterion 2 Title]

- ### 3. [ ] [Criterion 3 Title]
+ ### AC#3: [Criterion 3 Title]

- ### 4. [ ] [Criterion 4 Title]
+ ### AC#4: [Criterion 4 Title]
```

**Also update at lines 29, 42, 50, 58 (4 locations)**

**Version Update:**
```diff
- format_version: "2.0"
+ format_version: "2.1"
```

**Add Changelog Header:**
```yaml
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
      - "Three-layer tracking: TodoWrite (phases), AC Checklist (sub-items), DoD (official)"
  - version: "2.0"
    date: "2025-10-30"
    changes:
      - "Added format_version to story YAML frontmatter"
      - "Structured technical specification in YAML format"
---
```

**Effort:** 1 hour (implementation + testing)
**Testing:** Create test story with /create-story, verify AC headers have no checkboxes
**Success:** New stories use `### AC#1:` format

---

#### REC-2: CLAUDE.md Documentation Update
**File:** `src/CLAUDE.md` (distribution source)

**Location:** Add new section after "Story Progress Tracking (NEW - RCA-011)" (~line 470)

**Content to Add:**
```markdown
### Acceptance Criteria vs. Tracking Mechanisms (RCA-012 Clarification)

**IMPORTANT:** Stories contain both AC **definitions** and AC **tracking**:

| Element | Purpose | Checkbox Behavior | Updated When |
|---------|---------|-------------------|--------------|
| **AC Headers** (e.g., `### AC#1: Title`) | **Define what to test** (immutable) | **Never marked** (no checkboxes as of v2.1) | Never (definitions are static) |
| **AC Verification Checklist** | **Track granular progress** (real-time) | Marked complete during TDD phases | End of each TDD phase (1-5) |
| **Definition of Done** | **Official completion record** (quality gate) | Marked complete in Phase 4.5-5 Bridge | After deferrals validated, before commit |

**Why AC headers have no checkboxes (template v2.1+):**
- AC headers are **specifications**, not **progress trackers**
- Marking them "complete" would imply AC is no longer relevant (incorrect)
- Progress tracking happens in AC Checklist (granular) and DoD (official)

**For older stories (template v2.0 and earlier):**
- AC headers may show `### 1. [ ]` checkbox syntax (vestigial from pre-RCA-011 design)
- **These checkboxes may or may not be marked** (no documented convention existed)
- **Look at Definition of Done section for actual completion status**
- **DoD is the single source of truth** for story completion

**Quality Gate Rule (as of RCA-012 remediation):**
- QA validation REQUIRES 100% AC-to-DoD traceability
- Every AC requirement must have corresponding DoD item (explicit checkbox OR test validation)
- Incomplete DoD items require "Approved Deferrals" section with user consent timestamp
- QA fails if traceability <100% without documented deferrals
```

**Effort:** 45 minutes (writing + review)
**Testing:** User reads documentation, reviews STORY-052, confirms understanding
**Success:** User no longer confused by unchecked AC header checkboxes in old stories

---

#### REC-3: Template Version Tracking Documentation
**File:** `.claude/skills/devforgeai-story-creation/SKILL.md`

**Location:** Add to "Story Template Format" section

**Content to Add:**
```markdown
### Template Version History

**Current Version:** 2.1 (as of 2025-01-21)

**Version Evolution:**
- **v2.1** (2025-01-21): Removed AC header checkboxes, added changelog (RCA-012)
- **v2.0** (2025-10-30): Structured tech spec YAML format (RCA-006 Phase 2)
- **v1.0** (2025-XX-XX): Original template format

**Migration Path:**
- Stories created with v2.0: Optional migration to v2.1 via script
- Stories created with v1.0: Gradual migration on story update
- Backward compatibility: All versions supported

**See:** Template changelog in `assets/templates/story-template.md` header
```

**Effort:** 30 minutes
**Testing:** Review skill documentation, confirm version clarity
**Success:** Template evolution transparent and documented

---

### Phase 1 Validation

**Validation Checklist:**
- [ ] Template v2.1 created with no AC header checkboxes
- [ ] Changelog added to template header
- [ ] CLAUDE.md updated with tracking mechanisms clarification
- [ ] devforgeai-story-creation skill updated with version history
- [ ] Test story created using new template
- [ ] Test story AC headers show `### AC#1:` format (no checkboxes)
- [ ] User review confirms no confusion

**Success Criteria:**
- All 7 validation items pass
- New story creation works without errors
- Documentation is clear and comprehensive

**Rollback Plan (if validation fails):**
- Revert template to v2.0
- Document issues found
- Revise approach based on findings

---

## Phase 2: Quality Gate Enhancement (Week 1-2, Days 4-7)

### Objectives
1. Add AC-DoD traceability validation to QA workflow
2. Enforce 100% traceability requirement
3. Detect incomplete DoD early
4. Prevent quality gate bypasses

### Deliverables

#### REC-5: QA Traceability Validation Enhancement
**Files to Update:**
1. `.claude/skills/devforgeai-qa/SKILL.md` - Add traceability check to workflow
2. `.claude/skills/devforgeai-qa/references/validation-procedures.md` - Document validation algorithm
3. `.claude/skills/devforgeai-qa/references/dod-protocol.md` - Update DoD validation rules

**Implementation:**

**Step 1: Add Phase 0.9 to QA Skill (Pre-Validation Traceability Check)**

**File:** `.claude/skills/devforgeai-qa/SKILL.md`
**Location:** After Phase 0 (Parameter Extraction), before Phase 1 (Validation Mode Selection)

**Content to Add:**
```markdown
### Phase 0.9: AC-DoD Traceability Validation (NEW - RCA-012)

**Purpose:** Verify every Acceptance Criterion requirement has corresponding Definition of Done coverage

**Execution:**

Step 1: Extract Acceptance Criteria Count
```
Read story file
Count AC headers: grep "^### AC#[0-9]" (for v2.1+) OR grep "^### [0-9]\." (for v2.0)
Store: ac_count
```

Step 2: Extract AC Requirements (Granular)
```
FOR each AC header:
  Extract AC title
  Read AC content (Given/When/Then scenarios)
  Parse requirements:
    - Count distinct "Then" clauses (each is a requirement)
    - Extract measurable criteria (word counts, counts, percentages)
    - Identify validation needs (tests, evidence, metrics)

Store: ac_requirements[] (list of all granular requirements)
```

Step 3: Extract DoD Items
```
Read DoD section
Count checkboxes: grep "^- \[" (both [x] and [ ])
Store: dod_total_items
Count checked: grep "^- \[x\]"
Store: dod_checked_items
```

Step 4: Map AC Requirements to DoD Coverage
```
FOR each ac_requirement in ac_requirements[]:
  Search DoD section for:
    - Explicit checkbox mentioning requirement
    - Test validation referencing AC number
    - Quality metric covering requirement

  IF found:
    traceability[ac_requirement] = {dod_item, coverage_type}
  ELSE:
    missing_traceability[ac_requirement] = true
```

Step 5: Calculate Traceability Score
```
traceability_score = (ac_requirements.length - missing_traceability.length) / ac_requirements.length * 100
```

Step 6: Validate Incomplete DoD Items
```
incomplete_items = dod_total_items - dod_checked_items

IF incomplete_items > 0:
  Search for "Approved Deferrals" section in story file

  IF section exists:
    Extract deferred items list
    Verify each has user approval timestamp
    Verify each has justification (blocker type)

    IF all deferrals documented:
      deferral_status = "VALID (user-approved)"
    ELSE:
      deferral_status = "INVALID (missing approval)"
  ELSE:
    deferral_status = "INVALID (no Approved Deferrals section)"
```

Step 7: Apply Quality Gate Rules
```
IF traceability_score < 100:
  HALT QA workflow
  Display:
  "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  "❌ QA VALIDATION FAILED - AC-DoD Traceability Insufficient"
  ""
  "Traceability Score: {traceability_score}% (100% required)"
  ""
  "Missing DoD Coverage for AC Requirements:"
  FOR each missing in missing_traceability[]:
    Display: "  • {ac_requirement}"
  ""
  "Action Required:"
  "1. Add DoD items for missing AC requirements"
  "2. OR update AC to clarify existing DoD items cover requirements"
  "3. Re-run: /qa {STORY_ID}"
  "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  EXIT QA workflow (do not proceed to validation)

IF incomplete_items > 0 AND deferral_status contains "INVALID":
  HALT QA workflow
  Display:
  "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  "❌ QA VALIDATION FAILED - Incomplete DoD Without Approval"
  ""
  "DoD Completion: {dod_checked_items}/{dod_total_items} ({completion}%)"
  ""
  "Incomplete Items: {incomplete_items}"
  "Deferral Documentation: {deferral_status}"
  ""
  "Action Required:"
  "1. Complete all incomplete DoD items"
  "2. OR create 'Approved Deferrals' section with:"
  "   - List of deferred items"
  "   - Blocker justification (dependency, toolchain, artifact, ADR)"
  "   - User approval timestamp"
  "   - Follow-up story reference (if deferring to future story)"
  "3. Re-run: /qa {STORY_ID}"
  "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  EXIT QA workflow

IF traceability_score == 100 AND (incomplete_items == 0 OR deferral_status == "VALID"):
  Display:
  "✓ Phase 0.9 Traceability Validation: PASS"
  "  - AC-DoD traceability: {traceability_score}%"
  "  - DoD completion: {dod_checked_items}/{dod_total_items}"
  "  - Deferral status: {deferral_status}"
  ""

  Proceed to Phase 1 (Validation Mode Selection)
```

**Validation Output Format:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Phase 0.9: AC-DoD Traceability Validation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Acceptance Criteria Analysis:
  • Total ACs: 6
  • Total AC requirements (granular): 30
  • DoD items: 26

Traceability Mapping:
  • AC#1 (6 requirements) → 6 DoD items ✓
  • AC#2 (5 requirements) → 1 DoD item (test validation) ✓
  • AC#3 (5 requirements) → 1 DoD item (test validation) ✓
  • AC#4 (4 requirements) → 1 DoD item (test validation) ✓
  • AC#5 (5 requirements) → 1 DoD item (test validation) ✓
  • AC#6 (5 requirements) → 2 DoD items (test validation) ✓

Traceability Score: 100% ✅

DoD Completion Status:
  • Total items: 26
  • Complete [x]: 26
  • Incomplete [ ]: 0
  • Completion: 100% ✅

✓ PASS - Traceability validated, story ready for QA validation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
```

**Effort:** 2 hours (implementation + testing)
**Testing:** Run /qa on story with missing traceability, verify HALT occurs
**Success:** QA blocks stories with <100% AC-DoD traceability

---

#### REC-2: CLAUDE.md Documentation
(See Phase 1 documentation section in INDEX.md - already defined)

**Effort:** 45 minutes
**Testing:** User review confirms clarity

---

#### REC-3: Template Versioning
(See Phase 1 template refactoring section above - included in REC-1)

**Effort:** Included in REC-1 (30 minutes)
**Testing:** Verify changelog present in template

---

### Phase 1 Success Criteria

- [ ] Template v2.1 created with `### AC#1:` format (no checkboxes)
- [ ] Template includes version changelog
- [ ] CLAUDE.md documents AC vs. tracking distinction
- [ ] devforgeai-story-creation skill references version history
- [ ] Test story created with new template validates format
- [ ] User review confirms no confusion

**Total Phase 1 Effort:** 2.25 hours
**Completion Timeline:** 3 days (with review cycles)

---

## Phase 2: Quality Gate Enhancement (Week 1-2, Days 4-7)

### Objectives
1. Add AC-DoD traceability validation to QA workflow
2. Enforce 100% traceability or documented deferrals
3. Block quality gate bypasses
4. Provide clear remediation guidance

### Deliverables

#### REC-5: QA Traceability Validation (Detailed Above)

**Additional Files:**

**File:** `.claude/skills/devforgeai-qa/references/traceability-validation-algorithm.md` (NEW)
**Content:** Complete algorithm for mapping AC requirements to DoD coverage

**File:** `.claude/skills/devforgeai-qa/assets/traceability-report-template.md` (NEW)
**Content:** Template for traceability validation output

**Effort:** 2 hours total
- Algorithm design: 30 minutes
- Implementation in QA skill: 45 minutes
- Reference documentation: 30 minutes
- Testing: 15 minutes

**Testing Scenarios:**
1. Story with 100% traceability → PASS
2. Story with missing DoD item for AC requirement → FAIL with remediation guidance
3. Story with incomplete DoD + documented deferrals → PASS
4. Story with incomplete DoD + NO deferral documentation → FAIL

**Success Criteria:**
- [ ] Phase 0.9 added to devforgeai-qa skill
- [ ] Traceability validation algorithm implemented
- [ ] Test scenarios all produce expected results
- [ ] Remediation guidance clear and actionable

---

### Phase 2 Success Criteria

- [ ] QA workflow includes Phase 0.9 traceability validation
- [ ] QA fails stories with <100% traceability
- [ ] QA provides clear remediation guidance
- [ ] Test scenarios validate correct behavior
- [ ] Documentation complete (algorithm, templates)

**Total Phase 2 Effort:** 2 hours
**Completion Timeline:** 4 days (Days 4-7)
**Dependency:** Can run parallel with Phase 1

---

## Phase 3: Historical Cleanup (Week 2-3, Days 8-14)

### Objectives
1. Audit all 39 QA Approved stories for compliance
2. Fix STORY-038 and any others with undocumented incompleteness
3. Standardize deferral documentation
4. Restore framework integrity

### Deliverables

#### REC-6: QA Approved Stories Audit

**Audit Scope:** 39 stories with status "QA Approved"

**Audit Procedure:**

**Step 1: Automated Compliance Scan**
```bash
# Create audit script
cat > .devforgeai/RCA/RCA-012/scripts/audit-qa-approved-stories.sh << 'SCRIPT'
#!/bin/bash

echo "=== QA Approved Stories Audit (RCA-012) ==="
echo "Date: $(date)"
echo ""

for file in .ai_docs/Stories/*.story.md; do
  if grep -q "status: QA Approved" "$file" 2>/dev/null; then
    story=$(basename "$file" .story.md)

    # Count checkboxes
    checked=$(grep -c "^- \[x\]" "$file" 2>/dev/null || echo 0)
    unchecked=$(grep -c "^- \[ \]" "$file" 2>/dev/null || echo 0)
    total=$((checked + unchecked))

    if [ $total -gt 0 ]; then
      pct=$((checked * 100 / total))

      # Check for deferral documentation
      has_deferrals="NO"
      if grep -q "Approved Deferrals" "$file" 2>/dev/null; then
        has_deferrals="YES"
      fi

      # Flag issues
      issue=""
      if [ $unchecked -gt 0 ] && [ "$has_deferrals" == "NO" ]; then
        issue="⚠️ INCOMPLETE DoD without deferral docs"
      elif [ $pct -lt 100 ] && [ "$has_deferrals" == "YES" ]; then
        issue="✓ Deferrals documented"
      elif [ $pct -eq 100 ]; then
        issue="✓ Complete"
      fi

      echo "$story: $checked/$total ($pct%) - Deferrals: $has_deferrals - $issue"
    fi
  fi
done

echo ""
echo "=== Audit Complete ==="
SCRIPT

chmod +x .devforgeai/RCA/RCA-012/scripts/audit-qa-approved-stories.sh
bash .devforgeai/RCA/RCA-012/scripts/audit-qa-approved-stories.sh > .devforgeai/RCA/RCA-012/AUDIT-RESULTS.txt
```

**Step 2: Manual Review of Flagged Stories**
```
Review all stories flagged: "⚠️ INCOMPLETE DoD without deferral docs"

FOR each flagged story:
  Read story file
  Identify incomplete DoD items
  Determine if items should be:
    a) Completed (implement missing work)
    b) Deferred (add "Approved Deferrals" section with user approval)
    c) Removed (no longer relevant)
```

**Step 3: Fix STORY-038 (Known Issue)**
```
Read STORY-038 fully
Identify 4 incomplete DoD items
Ask user:
  "STORY-038 has 4 incomplete DoD items:
   1. {item 1}
   2. {item 2}
   3. {item 3}
   4. {item 4}

   Should these be:
   - Completed now (implement missing work)
   - Deferred with approval (add to Approved Deferrals section)
   - Removed (no longer relevant)"

Based on response:
  - Complete items OR
  - Add "Approved Deferrals" section with user approval timestamp OR
  - Remove items from DoD
```

**Step 4: Create Compliance Report**
```
Generate: .devforgeai/RCA/RCA-012/COMPLIANCE-REPORT.md

Include:
- Total stories audited: 39
- Fully compliant: {count} ({percentage}%)
- Incomplete with documented deferrals: {count}
- Incomplete WITHOUT deferral docs: {count} ⚠️
- Action items for each non-compliant story
```

**Effort:** 4 hours
- Automated audit: 30 minutes (script creation + execution)
- Manual review: 2 hours (review flagged stories)
- STORY-038 fix: 1 hour (user consultation + implementation)
- Compliance report: 30 minutes

**Testing:**
- Run audit script on all 39 stories
- Verify flagged stories actually have issues
- Fix test story, re-run audit, verify it clears

**Success Criteria:**
- [ ] All 39 stories audited
- [ ] Compliance report generated
- [ ] STORY-038 fixed (deferrals documented OR items completed)
- [ ] All incomplete DoD items have user approval
- [ ] Zero undocumented incomplete items

---

### Phase 3 Success Criteria

- [ ] Audit script created and executed
- [ ] Compliance report shows 100% of stories have documented deferrals OR 100% DoD
- [ ] STORY-038 and other non-compliant stories fixed
- [ ] Framework integrity restored
- [ ] /audit-deferrals command shows 100% compliance

**Total Phase 3 Effort:** 4 hours
**Completion Timeline:** 7 days (Days 8-14)
**Dependency:** Should follow Phase 2 (QA enhancement) to catch future issues

---

## Phase 4: Automation & Long-Term Prevention (Week 3-4, Days 15-21)

### Objectives
1. Provide automated migration for old stories (optional)
2. Enhance template with traceability matrix
3. Establish monitoring for compliance
4. Prevent recurrence

### Deliverables

#### REC-4: Migration Script for Old Stories

**File:** `.claude/skills/devforgeai-story-creation/scripts/migrate-ac-headers.sh` (NEW)

**Script Content:**
```bash
#!/bin/bash
# Migrate story template v2.0 → v2.1 (remove AC header checkboxes)
# Usage: migrate-ac-headers.sh <story-file>

STORY_FILE="$1"

if [[ -z "$STORY_FILE" ]]; then
  echo "Usage: migrate-ac-headers.sh <story-file>"
  echo "Example: migrate-ac-headers.sh .ai_docs/Stories/STORY-052-*.story.md"
  exit 1
fi

if [[ ! -f "$STORY_FILE" ]]; then
  echo "Error: File not found: $STORY_FILE"
  exit 1
fi

echo "Migrating: $STORY_FILE"

# Backup original
BACKUP_FILE="${STORY_FILE}.v2.0-backup"
cp "$STORY_FILE" "$BACKUP_FILE"
echo "✓ Backup created: $BACKUP_FILE"

# Replace AC header format (handles both checked and unchecked)
# Pattern 1: ### 1. [ ] Title → ### AC#1: Title
# Pattern 2: ### 1. [x] Title → ### AC#1: Title
sed -i 's/^### \([0-9]\+\)\. \[\(x\| \)\] /### AC#\1: /' "$STORY_FILE"

# Update format_version in YAML frontmatter
sed -i 's/format_version: "2.0"/format_version: "2.1"/' "$STORY_FILE"

# Verify changes
AC_COUNT_BEFORE=$(grep -c "^### [0-9]\. \[" "$BACKUP_FILE" 2>/dev/null || echo 0)
AC_COUNT_AFTER=$(grep -c "^### AC#[0-9]" "$STORY_FILE" 2>/dev/null || echo 0)

if [ $AC_COUNT_AFTER -eq $AC_COUNT_BEFORE ]; then
  echo "✓ Migration successful: $AC_COUNT_AFTER AC headers updated"
  echo "✓ Format version updated: 2.0 → 2.1"
  echo ""
  echo "Review changes with: diff $BACKUP_FILE $STORY_FILE"
  echo "Restore if needed: mv $BACKUP_FILE $STORY_FILE"
else
  echo "⚠️ Warning: AC count mismatch (before: $AC_COUNT_BEFORE, after: $AC_COUNT_AFTER)"
  echo "Review manually: diff $BACKUP_FILE $STORY_FILE"
fi
```

**Effort:** 1.5 hours
- Script creation: 45 minutes
- Testing on 5 stories: 30 minutes
- Documentation: 15 minutes

**Testing:**
- Test on STORY-052 (has `### 1. [ ]` format)
- Verify output is `### AC#1:` format
- Verify format_version updated
- Verify backup created
- Restore from backup, verify original preserved

**Success:** Script successfully migrates story format without data loss

---

#### REC-7: Traceability Matrix Template Enhancement

**File:** `.claude/skills/devforgeai-story-creation/assets/templates/story-template.md`

**Location:** Add new section after "Acceptance Criteria Verification Checklist" (line ~500)

**Content to Add:**
```markdown
## AC-to-DoD Traceability Matrix

**Purpose:** Visual mapping showing how each Acceptance Criterion requirement is validated in Definition of Done

**Usage:** Populated during story creation to ensure 100% AC-DoD coverage

| AC | Requirement | DoD Item | Validation Type |
|----|-------------|----------|-----------------|
| AC#1 | [Requirement description] | Implementation: [Item #] | Explicit Checkbox |
| AC#1 | [Another requirement] | Testing: [Item #] | Test Validation |
| AC#2 | [Requirement description] | Quality: [Item #] | Test Validation |
| AC#3 | [Requirement description] | Implementation: [Item #] | Explicit Checkbox |

**Validation Types:**
- **Explicit Checkbox:** DoD item directly states requirement (e.g., "Document includes introduction ≥200 words")
- **Test Validation:** DoD item references test that validates requirement (e.g., "Example validation test (AC2 - PASS)")
- **Metric Validation:** DoD item provides measurable proof (e.g., "Code coverage >95%")

**Quality Gate:** QA validates this matrix during Phase 0.9 - all ACs must have DoD coverage
```

**Effort:** 2 hours
- Template design: 1 hour
- Update story-creation skill to populate matrix: 45 minutes
- Testing: 15 minutes

**Testing:**
- Create new story with template v2.1
- Verify matrix section present
- Populate matrix manually
- Run /qa, verify traceability validation uses matrix

**Success:** New stories include pre-populated traceability matrix

---

### Phase 4 Success Criteria

- [ ] Migration script created and tested
- [ ] Traceability matrix added to template
- [ ] Migration tested on 5 sample stories
- [ ] Documentation complete (script usage, matrix purpose)
- [ ] Template v2.1 fully enhanced

**Total Phase 4 Effort:** 3.5 hours
**Completion Timeline:** 7 days (Days 15-21)
**Dependency:** Follows Phase 3 (after audit identifies which stories need migration)

---

## Complete Remediation Timeline

### Week 1: Foundation
- **Days 1-3:** Phase 1 (Template + Documentation)
  - REC-1: Template refactoring
  - REC-2: CLAUDE.md update
  - REC-3: Template versioning
- **Days 4-7:** Phase 2 (QA Enhancement)
  - REC-5: Traceability validation in QA

### Week 2-3: Cleanup & Validation
- **Days 8-14:** Phase 3 (Historical Audit)
  - REC-6: Audit 39 QA Approved stories
  - Fix STORY-038 and non-compliant stories

### Week 3-4: Automation
- **Days 15-21:** Phase 4 (Automation)
  - REC-4: Migration script
  - REC-7: Traceability matrix template

---

## Effort Summary

| Phase | Recommendations | Effort | Priority |
|-------|----------------|--------|----------|
| **Phase 1** | REC-1, REC-2, REC-3 | 2.25 hours | CRITICAL/HIGH |
| **Phase 2** | REC-5 | 2 hours | HIGH |
| **Phase 3** | REC-6 | 4 hours | HIGH |
| **Phase 4** | REC-4, REC-7 | 3.5 hours | MEDIUM |
| **Total** | 7 recommendations | 11.75 hours | Mixed |

---

## Risk Assessment

### Implementation Risks

**Risk 1: Breaking Existing Workflows**
- **Likelihood:** Low
- **Impact:** High
- **Mitigation:** Backward compatibility (v2.0 stories still work), comprehensive testing
- **Rollback:** Template backup, revert capability

**Risk 2: User Resistance to Change**
- **Likelihood:** Medium
- **Impact:** Medium
- **Mitigation:** Clear documentation, optional migration (not forced)
- **Rollback:** Keep v2.0 template available if needed

**Risk 3: Audit Reveals More Issues**
- **Likelihood:** High
- **Impact:** Medium (more work needed)
- **Mitigation:** Expect 10-20% of stories need fixes, budget extra time
- **Contingency:** Prioritize fixes (STORY-038 first, others as time allows)

### Benefit Analysis

**Immediate Benefits (Phase 1):**
- All future stories (58+) have clear format
- User confusion eliminated for new work
- Template evolution documented

**Medium-Term Benefits (Phase 2-3):**
- Quality gate bypass prevention
- Historical stories compliance-verified
- Framework integrity restored

**Long-Term Benefits (Phase 4):**
- Automated migration available
- Enhanced traceability transparency
- Monitoring prevents recurrence

**Return on Investment:**
- 11.75 hours investment
- Prevents ~2-3 hours user confusion per story
- Prevents quality gate bypasses (immeasurable value)
- **ROI:** Positive after 4-5 stories

---

## Validation Strategy

### Phase-by-Phase Validation

**Phase 1 Validation:**
```
1. Create test story: /create-story "Test story for template v2.1 validation"
2. Verify AC headers: grep "^### AC#" (no checkbox syntax)
3. User review: Read CLAUDE.md section, confirm clarity
4. Complete story: /dev TEST-STORY
5. Verify no confusion about completion status
```

**Phase 2 Validation:**
```
1. Run /qa on story with missing AC-DoD mapping
2. Verify QA HALTS with clear remediation guidance
3. Fix traceability issue
4. Re-run /qa
5. Verify QA PASSES after fix
```

**Phase 3 Validation:**
```
1. Run audit script
2. Review compliance report
3. Verify all flagged stories actually have issues
4. Fix STORY-038
5. Re-run audit
6. Verify STORY-038 clears
```

**Phase 4 Validation:**
```
1. Test migration script on STORY-052
2. Verify AC headers updated correctly
3. Verify no data loss
4. Restore from backup
5. Verify restore works
```

### End-to-End Validation (After All Phases)

**Validation Checklist:**
- [ ] Template v2.1 in use for all new stories
- [ ] CLAUDE.md documents tracking mechanisms clearly
- [ ] QA enforces AC-DoD traceability (100% required)
- [ ] All 39 QA Approved stories compliance-verified
- [ ] Migration script available and tested
- [ ] Traceability matrix template operational
- [ ] User feedback confirms no confusion
- [ ] /audit-deferrals shows 100% compliance
- [ ] Zero quality gate bypasses detected

**Success:** All 9 items pass

---

## Rollback Procedures

### Phase 1 Rollback
```
IF template v2.1 causes issues:
  1. Revert: git checkout .claude/skills/devforgeai-story-creation/assets/templates/story-template.md
  2. Remove: CLAUDE.md documentation additions
  3. Document: Why rollback was needed
  4. Revise: Approach based on issues found
```

### Phase 2 Rollback
```
IF QA traceability validation blocks valid stories:
  1. Comment out Phase 0.9 in devforgeai-qa/SKILL.md
  2. Revert validation-procedures.md changes
  3. Document: False positive patterns
  4. Revise: Validation algorithm to fix false positives
```

### Phase 3 Rollback
```
IF audit changes break stories:
  1. Restore from backup (.story.md.backup files)
  2. Document: What broke
  3. Revise: Audit procedure to prevent issue
```

### Phase 4 Rollback
```
IF migration script corrupts stories:
  1. All stories have backups (.v2.0-backup)
  2. Restore: mv *.v2.0-backup to original
  3. Fix: Script bug
  4. Re-test: On isolated stories before batch migration
```

---

## Communication Plan

### Stakeholder Communication

**For Framework Users:**
```
Subject: Story Template Update - Improved Clarity (v2.1)

Summary:
- Story template updated to eliminate confusing checkbox syntax in AC headers
- AC headers now clearly labeled as definitions (### AC#1:)
- Completion tracking remains in Definition of Done section (no change)
- Your existing stories still work (backward compatible)
- Optional migration script available if you want consistency

Action Required: None (automatic for new stories)
Optional: Migrate old stories using provided script
```

**For Framework Maintainers:**
```
Subject: RCA-012 Remediation - 4 Phases, 11.75 Hours

Summary:
- Issue: 80% inconsistency in AC header checkbox usage
- Root cause: Template not updated after RCA-011 enhancement
- Fix: 4-phase remediation (template, QA, audit, automation)
- Effort: 11.75 hours over 3-4 weeks
- Impact: 100% traceability compliance, zero user confusion

Action Required:
- Phase 1 (CRITICAL): Implement immediately
- Phase 2-4 (HIGH/MEDIUM): Schedule in sprint
```

---

## Success Metrics

### Quantitative Metrics

**Before Remediation:**
- AC header consistency: 20%
- AC-DoD traceability: 20% compliant
- User confusion incidents: ~1 per week
- Quality gate bypasses: 1 detected (STORY-038)

**After Remediation (Target):**
- AC header consistency: 100%
- AC-DoD traceability: 100% compliant
- User confusion incidents: 0
- Quality gate bypasses: 0 (prevented by QA validation)

### Qualitative Metrics

**User Experience:**
- "I understand what's complete" (clarity)
- "DoD is the source of truth" (confidence)
- "No ambiguity about story status" (trust)

**Framework Integrity:**
- "QA catches incomplete work" (quality)
- "Deferrals are documented" (transparency)
- "Standards are enforced" (consistency)

---

## Dependencies

### Phase Dependencies
- Phase 2 can run **parallel** with Phase 1 (no dependency)
- Phase 3 **requires** Phase 2 (need QA validation to catch future issues)
- Phase 4 **requires** Phase 3 (need audit results to know what to migrate)

### External Dependencies
- User availability for STORY-038 deferral approval (~30 minutes)
- User review of CLAUDE.md documentation (~15 minutes)
- Sprint planning to allocate 11.75 hours

---

## Monitoring & Prevention

### Post-Remediation Monitoring

**Weekly (First Month):**
- Run compliance audit script
- Check for new stories with checkbox syntax
- Review user feedback for confusion

**Monthly (Ongoing):**
- Audit new QA Approved stories (spot check 5 random stories)
- Verify AC-DoD traceability validation working
- Review template changelog for unexpected changes

**Escalation Triggers:**
- Any story reaches QA Approved with <100% traceability → Immediate investigation
- User reports "unchecked boxes" confusion → Review story, update documentation
- Template modified without version update → Block and require changelog entry

### Long-Term Prevention

**Process Improvements:**
1. Template change requires:
   - Version number increment
   - Changelog entry
   - Impact analysis (what stories affected?)
   - Testing plan (validate with new story)

2. QA validation includes:
   - AC-DoD traceability check (Phase 0.9)
   - Deferral documentation validation
   - Template version compatibility check

3. User onboarding includes:
   - Clear explanation of three-layer tracking
   - AC headers = definitions (static)
   - DoD = completion record (dynamic)
   - Where to look for story status (DoD section, Workflow Status)

---

## Related Issues & Cross-References

**Related RCAs:**
- **RCA-011:** Story Progress Tracking (three-layer system) - Created the context for this issue
- **RCA-006:** Autonomous Deferrals - Deferral validation patterns referenced in Phase 3
- **RCA-009:** Skill Execution Premature Stop - Similar template/documentation clarity issue

**Related Stories:**
- **STORY-014:** First story to leave AC headers unchecked (pattern started here)
- **STORY-038:** Quality gate bypass example (incomplete DoD without deferral docs)
- **STORY-052:** Triggered this RCA (user confusion about unchecked boxes)

**Related Components:**
- Story template (primary fix target)
- devforgeai-qa skill (validation enhancement)
- devforgeai-story-creation skill (template ownership)
- CLAUDE.md (convention documentation)

---

## Document Versions

| Document | Version | Status | Purpose |
|----------|---------|--------|---------|
| **INDEX.md** (this file) | 1.0 | ✅ COMPLETE | Navigation and overview |
| **ANALYSIS.md** | 1.0 | ✅ COMPLETE | Original 5 Whys and root cause |
| **SAMPLING-REPORT.md** | 1.0 | 📝 NEXT | 5-story sample detailed analysis |
| **REMEDIATION-PLAN.md** | 1.0 | ✅ COMPLETE | 4-phase remediation strategy |
| **IMPLEMENTATION-GUIDE.md** | 1.0 | 📝 PENDING | Step-by-step execution guide |
| **TEMPLATE-REFACTORING.md** | 1.0 | 📝 PENDING | REC-1 detailed implementation |
| **DOCUMENTATION-UPDATE.md** | 1.0 | 📝 PENDING | REC-2, REC-3 implementation |
| **QA-ENHANCEMENT.md** | 1.0 | 📝 PENDING | REC-5 detailed implementation |
| **STORY-AUDIT.md** | 1.0 | 📝 PENDING | REC-6 audit procedures |
| **MIGRATION-SCRIPT.md** | 1.0 | 📝 PENDING | REC-4 script details |
| **CONVENTIONS.md** | 1.0 | 📝 PENDING | AC checkbox usage conventions |
| **TESTING-PLAN.md** | 1.0 | 📝 PENDING | Validation strategy |
| **TRACEABILITY-MATRIX.md** | 1.0 | 📝 PENDING | AC-DoD mapping examples |
| **VALIDATION-PROCEDURES.md** | 1.0 | 📝 PENDING | Testing procedures |

---

## Immediate Next Steps

**For User Decision (NOW):**
1. **Review this INDEX.md** - Approve the 4-phase remediation approach
2. **Choose execution path:**
   - **Option A:** Create all RCA-012 documents now (complete planning package) - ~2 hours
   - **Option B:** Create documents incrementally as each phase executes - ~30 min per phase
   - **Option C:** Proceed directly to Phase 1 implementation (use this INDEX + REMEDIATION-PLAN as guide) - Start now

**Recommendation:** **Option A** - Complete planning package provides:
- Full visibility into remediation scope
- Ability to review before implementation
- Reference documentation for all phases
- Coordinated approach across all fixes

**After Decision:**
- If Option A: Create remaining 11 documents (SAMPLING-REPORT.md through VALIDATION-PROCEDURES.md)
- If Option B: Create IMPLEMENTATION-GUIDE.md, begin Phase 1
- If Option C: Begin REC-1 (template refactoring) immediately

---

**RCA-012 Status:** Planning Framework Complete, Awaiting User Decision on Document Creation Strategy
**Estimated Planning Completion:** 2 hours (if Option A selected)
**Estimated Total Resolution:** 13.75 hours (11.75 implementation + 2 planning)
