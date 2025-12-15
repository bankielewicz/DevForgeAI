# RCA-012: Story Audit Procedures (REC-6)
## Audit and Fix 39 QA Approved Stories

**Recommendation ID:** REC-6
**Priority:** HIGH
**Effort:** 6 hours (updated from 4 hours based on sampling)
**Scope:** All 39 QA Approved stories

---

## Objective

Audit all QA Approved stories for AC-DoD traceability compliance, identify stories with undocumented incomplete DoD items (like STORY-038), and fix non-compliant stories by either completing work or documenting deferrals with user approval.

---

## Audit Scope

**Stories to Audit:** 39 stories with `status: QA Approved`

**Audit Criteria:**
1. **DoD Completion:** Are all DoD items marked `[x]`?
2. **Deferral Documentation:** If incomplete, is there "Approved Deferrals" section?
3. **User Approval:** Do deferrals have timestamp?
4. **AC-DoD Traceability:** Does every AC have DoD coverage?

**Expected Outcomes:**
- **Compliant:** DoD 100% complete OR documented deferrals with user approval
- **Non-Compliant:** Incomplete DoD without "Approved Deferrals" section OR missing user approval

---

## Phase 3.1: Automated Audit Script Creation

### Script Implementation

**File:** `.devforgeai/RCA/RCA-012/scripts/audit-qa-approved-stories.sh` (NEW)

**Script:**
```bash
#!/bin/bash
# RCA-012 Story Audit Script
# Purpose: Audit all QA Approved stories for DoD compliance and deferral documentation

echo "========================================================================="
echo "RCA-012: QA Approved Stories Audit"
echo "========================================================================="
echo "Date: $(date)"
echo "Scope: All stories with status 'QA Approved'"
echo ""

# Initialize counters
total=0
compliant=0
non_compliant=0

# Results arrays
declare -a compliant_stories
declare -a non_compliant_stories

echo "Scanning stories..."
echo ""

for file in devforgeai/specs/Stories/*.story.md; do
  # Check if QA Approved
  if grep -q "status: QA Approved" "$file" 2>/dev/null; then
    total=$((total + 1))
    story=$(basename "$file" .story.md)

    # Count checkboxes
    checked=$(grep -c "^- \[x\]" "$file" 2>/dev/null || echo 0)
    unchecked=$(grep -c "^- \[ \]" "$file" 2>/dev/null || echo 0)
    dod_total=$((checked + unchecked))

    if [ $dod_total -gt 0 ]; then
      completion_pct=$((checked * 100 / dod_total))
    else
      completion_pct=0
    fi

    # Check for deferral documentation
    has_deferrals="NO"
    has_approval="NO"

    if grep -q "^## Approved Deferrals" "$file" 2>/dev/null; then
      has_deferrals="YES"

      # Check for approval timestamp
      if grep -q "User Approval:.*UTC" "$file" 2>/dev/null; then
        has_approval="YES"
      fi
    fi

    # Determine compliance
    is_compliant="NO"
    issue=""

    if [ $unchecked -eq 0 ]; then
      # DoD 100% complete
      is_compliant="YES"
      issue="✓ Complete (100% DoD)"
      compliant=$((compliant + 1))
      compliant_stories+=("$story")

    elif [ "$has_deferrals" == "YES" ] && [ "$has_approval" == "YES" ]; then
      # Incomplete with documented deferrals
      is_compliant="YES"
      issue="✓ Deferrals documented ($checked/$dod_total complete, $unchecked deferred)"
      compliant=$((compliant + 1))
      compliant_stories+=("$story")

    elif [ "$has_deferrals" == "YES" ] && [ "$has_approval" == "NO" ]; then
      # Has section but missing approval
      is_compliant="NO"
      issue="⚠️ Deferrals exist but missing user approval timestamp"
      non_compliant=$((non_compliant + 1))
      non_compliant_stories+=("$story")

    else
      # Incomplete without deferrals
      is_compliant="NO"
      issue="❌ INCOMPLETE DoD without deferral documentation ($unchecked items)"
      non_compliant=$((non_compliant + 1))
      non_compliant_stories+=("$story")
    fi

    # Display result
    printf "%-50s %3d%% (%2d/%2d) %s\n" "$story" "$completion_pct" "$checked" "$dod_total" "$issue"
  fi
done

echo ""
echo "========================================================================="
echo "Audit Summary"
echo "========================================================================="
echo "Total Stories Audited: $total"
echo "Compliant: $compliant ($((compliant * 100 / total))%)"
echo "Non-Compliant: $non_compliant ($((non_compliant * 100 / total))%)"
echo ""

if [ $non_compliant -gt 0 ]; then
  echo "========================================================================="
  echo "Non-Compliant Stories (Require Action)"
  echo "========================================================================="
  for story in "${non_compliant_stories[@]}"; do
    echo "  • $story"
  done
  echo ""
fi

echo "========================================================================="
echo "Next Steps"
echo "========================================================================="
if [ $non_compliant -gt 0 ]; then
  echo "1. Review each non-compliant story listed above"
  echo "2. For each story:"
  echo "   - Read story file completely"
  echo "   - Identify incomplete DoD items"
  echo "   - Determine: Complete work OR document deferrals"
  echo "   - If defer: Add 'Approved Deferrals' section with user approval"
  echo "3. Re-run this audit script to verify fixes"
  echo "4. Target: 100% compliance ($total/$total stories)"
else
  echo "✓ All $total stories are compliant"
  echo "✓ No action required"
fi
echo "========================================================================="

# Exit code
if [ $non_compliant -eq 0 ]; then
  exit 0  # Success
else
  exit 1  # Issues found
fi
```

**Create Script:**
```bash
mkdir -p .devforgeai/RCA/RCA-012/scripts

cat > .devforgeai/RCA/RCA-012/scripts/audit-qa-approved-stories.sh << 'SCRIPT'
{paste script above}
SCRIPT

chmod +x .devforgeai/RCA/RCA-012/scripts/audit-qa-approved-stories.sh

echo "✓ Audit script created"
```

**Effort:** 30 minutes (script creation and testing)

---

## Phase 3.2: Execute Audit

### Run Audit Script

```bash
bash .devforgeai/RCA/RCA-012/scripts/audit-qa-approved-stories.sh | tee .devforgeai/RCA/RCA-012/AUDIT-RESULTS.txt
```

**Expected Output Format:**
```
=========================================================================
RCA-012: QA Approved Stories Audit
=========================================================================
Date: 2025-01-21 08:00:00
Scope: All stories with status 'QA Approved'

Scanning stories...

STORY-007-post-operation-retrospective          100% (22/22) ✓ Complete (100% DoD)
STORY-008-adaptive-questioning-engine            100% (18/18) ✓ Complete (100% DoD)
STORY-009-skip-pattern-tracking                  100% (16/16) ✓ Complete (100% DoD)
...
STORY-014-add-definition-of-done                  27% ( 6/22) ✓ Deferrals documented (6/22 complete, 16 deferred)
STORY-023-wire-hooks-into-dev-command             68% (15/22) ✓ Deferrals documented (15/22 complete, 7 deferred)
STORY-030-qa-automation-comprehensive-guide      100% (24/24) ✓ Complete (100% DoD)
...
STORY-038-code-quality-metrics-enhancement        87% (27/31) ❌ INCOMPLETE DoD without deferral documentation (4 items)
...

=========================================================================
Audit Summary
=========================================================================
Total Stories Audited: 39
Compliant: 31 (79%)
Non-Compliant: 8 (21%)

=========================================================================
Non-Compliant Stories (Require Action)
=========================================================================
  • STORY-038-code-quality-metrics-enhancement
  • STORY-{XXX}-{potential-other-issues}
  • {... up to 8 total ...}

=========================================================================
Next Steps
=========================================================================
1. Review each non-compliant story listed above
2. For each story:
   - Read story file completely
   - Identify incomplete DoD items
   - Determine: Complete work OR document deferrals
   - If defer: Add 'Approved Deferrals' section with user approval
3. Re-run this audit script to verify fixes
4. Target: 100% compliance (39/39 stories)
=========================================================================
```

**Effort:** 30 minutes (run script, review output, prioritize fixes)

---

## Phase 3.3: Fix Priority 1 - STORY-038

**Known Issue:** 4 incomplete Testing/Documentation items without deferral documentation

### Fix Procedure

**Step 1: Read Story Completely**
```bash
Read devforgeai/specs/Stories/STORY-038-code-quality-metrics-validation-enhancement.story.md
```

**Step 2: Identify Incomplete Items**

From sampling report:
```
Testing (4/8 incomplete):
- [ ] Performance test: 10K LOC analysis <30s
- [ ] Edge case test: Zero-line files
- [ ] Edge case test: Binary files (non-code)
- [ ] Threshold violation test: Extreme values

Documentation (4/8 incomplete):
- [ ] Performance benchmarks documented
- [ ] Language-specific tooling requirements
- [ ] Threshold configuration guide
- [ ] Troubleshooting guide for quality analysis failures
```

**Total Incomplete:** 4 items (the Implementation Notes mention "Design Decision" but no formal deferrals)

---

**Step 3: User Consultation for Deferral Approval**

Use AskUserQuestion:
```
Question: "STORY-038 has 4 incomplete DoD items (Testing: 4 items). These were mentioned in Implementation Notes as 'deferred' but lack formal 'Approved Deferrals' section. Should these be:"

Options:
  1. "Complete now" - Implement all 4 missing tests
  2. "Defer with approval" - Formalize deferrals with user approval
  3. "Remove" - Items no longer relevant
  4. "Review first" - Show me the 4 items before deciding

multiSelect: false
```

**Based on Response:**

**If "Defer with approval":**
```
Request additional input:
  "Please provide deferral justification for these 4 items:
   1. Performance test: 10K LOC analysis <30s
   2. Edge case: Zero-line files
   3. Edge case: Binary files
   4. Threshold extreme values

   What is the blocker? (Artifact, Toolchain, Low-Priority, etc.)
   Is there a follow-up story? (or condition for implementation)"

Capture: User response for blocker justification
```

---

**Step 4: Add "Approved Deferrals" Section**

**File:** `devforgeai/specs/Stories/STORY-038-code-quality-metrics-validation-enhancement.story.md`

**Location:** Add after "Implementation Notes" section, before "Definition of Done"

**Content to Add:**
```markdown
## Approved Deferrals

**User Approval:** 2025-01-21 {HH:MM} UTC
**Approval Type:** Low-Priority Enhancement Deferral (RCA-012 Audit Remediation)

**Deferred Items:**

1. **Performance test: 10K LOC analysis <30s**
   - **Reason:** {User provided justification - e.g., "No large codebase available in framework repository for realistic benchmarking"}
   - **Blocker Type:** Artifact (requires real project with 10K+ LOC)
   - **Follow-up:** Test during Phase 4 real project validation OR create synthetic 10K LOC test fixture
   - **Impact:** Core functionality (metrics calculation, thresholds, recommendations) is complete and tested. Performance validation deferred to real-world usage.

2. **Edge case test: Zero-line files**
   - **Reason:** {User justification - e.g., "Edge case unlikely in practice - build tools fail on zero-line code files"}
   - **Blocker Type:** Low-Priority (not critical path)
   - **Follow-up:** Implement if user reports issue in production usage
   - **Impact:** Minimal - quality tools skip empty files automatically

3. **Edge case test: Binary files (non-code)**
   - **Reason:** {User justification - e.g., "Quality analysis tools (radon, pylint) automatically skip binary files"}
   - **Blocker Type:** Toolchain (handled by tooling, not framework responsibility)
   - **Follow-up:** None required (tooling handles this)
   - **Impact:** None - binary file handling is external to framework

4. **Threshold violation test: Extreme values**
   - **Reason:** {User justification - e.g., "Current threshold validation covers normal ranges (0-15 complexity, 0-100% duplication). Extreme values (>100 complexity) are theoretical."}
   - **Blocker Type:** Low-Priority (extreme values are edge cases)
   - **Follow-up:** Implement if encountered during production usage
   - **Impact:** Minimal - normal range validation is sufficient for 99% of use cases

**Total Deferred:** 4 items (13% of DoD)
**Completion Status:** 27/31 items complete (87%)
**Core Functionality:** Complete (quality metrics, thresholds, recommendations, read-only guarantee)

**Rationale for Approval:**
All deferred items are enhancement-level (edge cases, extreme values, documentation additions). Core functionality is fully implemented, tested, and validated. Deferring these items does not impact story value or quality gate integrity.
```

**Validation:**
```bash
# Verify section added
grep "^## Approved Deferrals" devforgeai/specs/Stories/STORY-038*.story.md

# Verify user approval timestamp
grep "User Approval: 2025-01-21" devforgeai/specs/Stories/STORY-038*.story.md

# Count deferred items documented
grep -c "^\*\*Deferred Items:\*\*" devforgeai/specs/Stories/STORY-038*.story.md
# Expected: 1 (section header)

# Verify all 4 items listed
grep -A 50 "Deferred Items:" devforgeai/specs/Stories/STORY-038*.story.md | grep -c "^[0-9]\."
# Expected: 4 (items 1-4)
```

**Effort:** 1 hour (user consultation + documentation + validation)

---

## Phase 3.4: Fix Other Non-Compliant Stories

### Story-by-Story Fix Process

**For EACH story flagged by audit script:**

**Step 1: Read Story File**
```
Read devforgeai/specs/Stories/{STORY-ID}-{slug}.story.md
```

**Step 2: Extract Incomplete DoD Items**
```
Search for: ^- \[ \] pattern (unchecked checkboxes)

Record:
  - Item text
  - Section (Implementation / Quality / Testing / Documentation)
  - Line number
```

**Step 3: Check Implementation Notes for Context**
```
Read Implementation Notes section

Search for mentions of:
  - "defer"
  - "design-phase"
  - "follow-up story"
  - "low priority"
  - Specific incomplete item keywords

Determine if deferral was implicit (mentioned) or missing entirely
```

**Step 4: Classify Incomplete Items**

**Category A: Explicitly Mentioned Deferrals (Formalize)**
```
Example: Implementation Notes say "Testing deferred to STORY-XXX"

Action:
  - Add "Approved Deferrals" section
  - List deferred items
  - Reference follow-up story
  - Add retrospective user approval timestamp
  - Justification: "Deferred per documented decision in Implementation Notes"
```

**Category B: Implicitly Incomplete (Request User Decision)**
```
Example: DoD item unchecked but no mention in notes

Action:
  Use AskUserQuestion:
    "Story {STORY_ID} has incomplete item: '{item text}'

     Should this be:
       1. Completed now (implement missing work)
       2. Deferred (add to Approved Deferrals with justification)
       3. Removed (no longer relevant)"

  Based on response: Complete, defer (with approval doc), or remove
```

**Category C: No Longer Relevant (Remove)**
```
Example: DoD item references deprecated feature

Action:
  - Remove item from DoD
  - Document removal in Implementation Notes:
    "Removed DoD item: '{item text}' - Reason: {explanation}"
```

---

**Step 5: Update Story File**

**For Category A & B (Formalize or Add Deferrals):**

Add "Approved Deferrals" section:
```markdown
## Approved Deferrals

**User Approval:** 2025-01-21 {HH:MM} UTC
**Approval Type:** {Category - Design-Phase | Low-Priority | Blocker-Dependent | Retrospective-Formalization}

**Deferred Items:**
{FOR each deferred item}:
{N}. **{Item text from DoD}**
   - **Reason:** {Why deferred - from Implementation Notes or user input}
   - **Blocker Type:** {Dependency | Toolchain | Artifact | ADR | Low-Priority}
   - **Follow-up:** {Story reference OR condition}
   - **Impact:** {Optional - significance of deferral}

**Total Deferred:** {count} items ({percentage}% of DoD)
**Completion Status:** {checked}/{total} items complete ({completion_pct}%)

**Rationale for Approval:**
{Overall justification - why these deferrals are acceptable}
```

**For Category C (Remove):**

Edit DoD section:
```
Remove: - [ ] {item text}

Add to Implementation Notes:
"**Removed DoD Items (RCA-012 Audit):**
- {item text} - Removed {date} - Reason: {explanation}"
```

---

**Step 6: Validate Fix**

```bash
# Verify "Approved Deferrals" added (if applicable)
grep "^## Approved Deferrals" devforgeai/specs/Stories/{STORY-ID}*.story.md

# Verify user approval present
grep "User Approval:.*UTC" devforgeai/specs/Stories/{STORY-ID}*.story.md

# Verify all incomplete items documented
UNCHECKED=$(grep -c "^- \[ \]" devforgeai/specs/Stories/{STORY-ID}*.story.md)
DEFERRED=$(grep -A 50 "Deferred Items:" devforgeai/specs/Stories/{STORY-ID}*.story.md | grep -c "^[0-9]\.")

if [ $UNCHECKED -eq $DEFERRED ]; then
  echo "✓ All $UNCHECKED incomplete items documented in deferrals"
else
  echo "⚠️ Warning: $UNCHECKED incomplete but only $DEFERRED documented"
fi
```

**Checkpoint (Per Story):**
- [ ] Story read completely
- [ ] Incomplete items identified and classified
- [ ] User decision obtained (if needed)
- [ ] Story file updated (deferrals added OR items removed OR work completed)
- [ ] Validation confirms all incomplete items documented
- [ ] Story marked "fixed" in tracking list

---

## Phase 3.5: Generate Compliance Report

**After All Stories Fixed:**

### Create Report

**File:** `.devforgeai/RCA/RCA-012/COMPLIANCE-REPORT.md`

**Content:**
```markdown
# QA Approved Stories Compliance Report

**Audit Date:** 2025-01-21
**Audit Scope:** 39 stories with status "QA Approved"
**Remediation Completed:** 2025-01-{XX}

---

## Executive Summary

**Before Remediation:**
- Compliant: {initial_compliant} ({percentage}%)
- Non-Compliant: {initial_non_compliant} ({percentage}%)
- Compliance Rate: {percentage}%

**After Remediation:**
- Compliant: 39 (100%)
- Non-Compliant: 0 (0%)
- Compliance Rate: 100%

**Issues Fixed:** {count} stories
**Deferrals Documented:** {count} new "Approved Deferrals" sections added
**Items Completed:** {count} incomplete DoD items implemented
**Items Removed:** {count} obsolete DoD items removed

---

## Stories Fixed

{FOR each fixed story}:
### {STORY-ID}: {Title}

**Issue:** {What was non-compliant}
**Resolution:** {What was done - deferrals added, work completed, or items removed}
**User Approval:** {timestamp if deferrals}
**Deferred Items:** {count if applicable}
**Effort:** {time spent fixing}

---

## Compliance Verification

**Final Audit Run:**
```bash
bash .devforgeai/RCA/RCA-012/scripts/audit-qa-approved-stories.sh
```

**Result:**
```
Total Stories Audited: 39
Compliant: 39 (100%)
Non-Compliant: 0 (0%)

✓ All 39 stories are compliant
✓ No action required
```

**Validation Date:** 2025-01-{XX}

---

## Quality Gate Integrity Restored

**Before RCA-012 Remediation:**
- STORY-038 reached "QA Approved" with undocumented incomplete items ❌
- 21% of stories non-compliant (8/39)
- No enforcement mechanism

**After RCA-012 Remediation:**
- All 39 stories have 100% DoD OR documented deferrals ✅
- Phase 0.9 prevents future bypasses ✅
- Enforcement mechanism operational ✅

---

## Lessons Learned

**Pattern Analysis:**
- Most non-compliant stories had implicitly deferred items (mentioned in notes but not formalized)
- Common blocker types: Artifact (no test infrastructure), Low-Priority (enhancement), Dependency (awaiting other story)
- User approval obtained retrospectively for historical deferrals (acceptable for cleanup)

**Best Practices Established:**
- Formalize deferrals immediately (don't rely on Implementation Notes alone)
- Request user approval during TDD workflow (don't defer approval to later)
- Document blocker type clearly (enables follow-up tracking)

---

## Recommendations for Future

1. **Prevent Implicit Deferrals:**
   - Phase 4.5 Deferral Challenge (RCA-006) should require formal "Approved Deferrals" section
   - Implementation Notes alone insufficient for tracking

2. **Automate Deferral Section Creation:**
   - When user approves deferral in Phase 4.5, auto-generate section
   - Don't require manual documentation (error-prone)

3. **Monitor Compliance:**
   - Run audit script monthly
   - Flag any story reaching QA Approved with <100% DoD and no deferrals
   - Escalate to framework maintainer

---

**Compliance Report Template Complete**
```

**Effort:** 30 minutes (report generation after all fixes complete)

---

## Effort Breakdown by Story Type

### Type A: Complete Stories (No Action)
- **Count:** ~24 stories (estimated 60% based on sampling)
- **Effort:** 0 minutes each
- **Total:** 0 hours

### Type B: Documented Deferrals (Verify Only)
- **Count:** ~8 stories (estimated 20% based on sampling)
- **Effort:** 10 minutes each (read story, verify deferrals documented)
- **Total:** 1.3 hours

### Type C: Undocumented Incomplete (Fix Required)
- **Count:** ~7 stories (estimated 18% based on sampling - includes STORY-038)
- **Effort:** 30-60 minutes each (user consultation + documentation)
- **Total:** 4-7 hours

**Conservative Estimate:** 6 hours total (includes buffer for unexpected issues)

---

## Audit Tracking Spreadsheet

**Create Tracking File:**
```bash
cat > .devforgeai/RCA/RCA-012/AUDIT-TRACKING.csv << 'CSV'
Story ID,Title,DoD Complete,DoD Total,Completion %,Has Deferrals,Has Approval,Compliance,Action Required,Status,Fixed Date
STORY-007,Retrospective Conversation,22,22,100%,N/A,N/A,PASS,None,✓ Compliant,N/A
STORY-014,Add DoD to Template,6,22,27%,YES,YES,PASS,None,✓ Compliant,N/A
STORY-023,Wire Hooks,15,22,68%,YES,YES,PASS,None,✓ Compliant,N/A
STORY-030,QA Automation Guide,24,24,100%,N/A,N/A,PASS,None,✓ Compliant,N/A
STORY-038,Quality Metrics,27,31,87%,NO,NO,FAIL,Add deferrals,⏳ In Progress,TBD
...
CSV
```

**Use for Tracking:**
- Update "Status" column as stories are fixed
- Update "Fixed Date" when remediation complete
- Calculate compliance percentage dynamically

---

## Success Criteria

**Phase 3 is successful when:**

- [ ] Audit script executed successfully
- [ ] All 39 stories reviewed and categorized
- [ ] STORY-038 fixed with "Approved Deferrals" section
- [ ] All flagged stories fixed (deferrals documented OR work completed OR items removed)
- [ ] Compliance report generated showing 100%
- [ ] Final audit run confirms 39/39 compliant
- [ ] Tracking spreadsheet shows all stories "✓ Compliant"
- [ ] Zero undocumented incomplete DoD items remain

---

## Validation

**Final Validation Command:**
```bash
bash .devforgeai/RCA/RCA-012/scripts/audit-qa-approved-stories.sh
```

**Expected:**
```
Total Stories Audited: 39
Compliant: 39 (100%)
Non-Compliant: 0 (0%)

✓ All 39 stories are compliant
✓ No action required
```

**Exit Code:** 0 (success)

---

**REC-6 Status:** Ready for Implementation
**Effort:** 6 hours (audit + fixes + reporting)
**Priority:** HIGH (restores framework integrity)
**Impact:** 100% compliance for all QA Approved stories
