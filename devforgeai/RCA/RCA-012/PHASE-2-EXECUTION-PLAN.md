# RCA-012 Phase 2 Execution Plan
## QA Enhancement: Add AC-DoD Traceability Validation

**Version:** 1.0
**Created:** 2025-01-21
**Estimated Duration:** 2 hours
**Priority:** HIGH
**Status:** Ready for Execution

---

## Executive Summary

**Objective:** Add Phase 0.9 to devforgeai-qa skill that validates 100% AC-to-DoD traceability and enforces documented deferrals, preventing quality gate bypasses like STORY-038 (which reached "QA Approved" with 4 undocumented incomplete DoD items).

**What Gets Built:**
- New Phase 0.9 in devforgeai-qa/SKILL.md (traceability validation)
- New reference file: `traceability-validation-algorithm.md` (complete algorithm)
- New asset file: `traceability-report-template.md` (display templates)

**Impact:**
- **Prevention:** Catches incomplete DoD before expensive validations (build, tests, coverage)
- **Enforcement:** Requires 100% AC-to-DoD traceability OR documented deferrals
- **Token Savings:** ~60K tokens per caught issue (avoid Phases 2-6 if structure invalid)

**Deliverables:**
1. Phase 0.9 integrated into QA workflow
2. Traceability validation algorithm documented
3. Display templates for PASS/FAIL scenarios
4. Test scenarios validating correct behavior

---

## Phase 2 Overview

### Single Recommendation (REC-5)

**REC-5 (HIGH):** Add AC-DoD Traceability Validation to QA
- Insert Phase 0.9 between Phase 0 (Parameter Extraction) and Phase 1 (Validation Mode Selection)
- Validate every AC requirement has corresponding DoD item
- Enforce deferral documentation for incomplete DoD items
- HALT QA if traceability <100% or deferrals undocumented
- **Effort:** 2 hours

**Why HIGH Priority:**
- Prevents future STORY-038-style bypasses
- Quality gate integrity essential
- Catches structural issues before expensive validations
- Framework-wide impact (all 39+ QA Approved stories benefit)

---

## Detailed Step-by-Step Execution

### Step 1: Read Current QA Skill Structure (10 minutes)

**Objective:** Understand current QA workflow and identify Phase 0.9 insertion point

**File to Read:**
```bash
Read(.claude/skills/devforgeai-qa/SKILL.md)
# or
Read(src/claude/skills/devforgeai-qa/SKILL.md)
```

**What to Find:**
1. Phase 0: Parameter Extraction (where it ends)
2. Phase 1: Validation Mode Selection (where it begins)
3. Current phase numbering scheme
4. How phases transition (success criteria, checkpoints)

**Identify Insertion Point:**
- Phase 0.9 goes AFTER Phase 0, BEFORE Phase 1
- Should be ~line 150-200 (after parameter extraction completes)

**Checkpoint:**
- [ ] Current QA skill structure understood
- [ ] Phase 0 ending identified
- [ ] Phase 1 beginning identified
- [ ] Insertion point confirmed

---

### Step 2: Create Traceability Validation Algorithm Reference (30 minutes)

**Objective:** Document complete algorithm for mapping AC requirements to DoD coverage

**File to Create:** `src/claude/skills/devforgeai-qa/references/traceability-validation-algorithm.md`

**Content Structure:**

```markdown
# AC-to-DoD Traceability Validation Algorithm

**Purpose:** Map every Acceptance Criterion requirement to Definition of Done coverage, ensuring 100% traceability.

**Used By:** devforgeai-qa skill Phase 0.9

---

## Algorithm Overview

**5-Step Process:**
1. Extract AC count and granular requirements from story file
2. Extract DoD items (total, checked, unchecked)
3. Map AC requirements to DoD items (keyword matching)
4. Calculate traceability score (target: 100%)
5. Validate deferrals if DoD incomplete

---

## Step 1: Extract AC Requirements

### Step 1.1: Count AC Headers

**For Template v2.1+:**
```
ac_headers = grep count "^### AC#[0-9]:" story_file
```

**For Template v2.0/v1.0:**
```
ac_headers = grep count "^### [0-9]\. \[" story_file
```

**Combined (supports both):**
```
ac_headers = grep count "^### (AC#)?[0-9]" story_file
ac_count = ac_headers
```

### Step 1.2: Extract Granular Requirements

For each AC section, parse:

**1. Given/When/Then Scenarios:**
```
# Find all "Then" clauses (each is a requirement)
then_clauses = grep "^\*\*Then\*\*" in AC_section

Example:
  **Then** system processes successfully      ← Requirement 1
  **And** system returns response in <200ms   ← Requirement 2
  **And** system logs transaction             ← Requirement 3
```

**2. Bullet List Requirements:**
```
# Find bullet points after "Then" (detailed requirements)
bullet_requirements = grep "^- " in AC_section (after Then clause)

Example:
  **Then** document contains:
  - Introduction (≥200 words)                 ← Requirement 1
  - 11 command sections                       ← Requirement 2
  - 20-30 examples                            ← Requirement 3
```

**3. Measurable Criteria:**
```
# Find metrics, thresholds, ranges
metrics = grep patterns like:
  - "≥X", "≤X", "<X", ">X"
  - "X-Y range"
  - "X%" (percentages)
  - "X items", "X words", "X seconds"

Example:
  - Introduction ≥200 words                   ← Measurable requirement
  - Response time <200ms                      ← Measurable requirement
  - Coverage >95%                             ← Measurable requirement
```

**Store:**
```
ac_requirements = [
  {ac_number: 1, text: "system processes successfully", type: "functional"},
  {ac_number: 1, text: "response in <200ms", type: "performance"},
  {ac_number: 2, text: "Introduction ≥200 words", type: "content"},
  ...
]

total_ac_requirements = ac_requirements.length
```

---

## Step 2: Extract DoD Items

### Step 2.1: Count Checkboxes

```
# Find all checkbox lines in DoD section
dod_section = extract_section("^## Definition of Done", story_file)

# Count total checkboxes (both [x] and [ ])
dod_total = grep count "^- \[" in dod_section

# Count checked
dod_checked = grep count "^- \[x\]" in dod_section

# Count unchecked
dod_unchecked = grep count "^- \[ \]" in dod_section

# Calculate completion
dod_completion_pct = (dod_checked / dod_total) × 100
```

### Step 2.2: Extract DoD Item Text

```
# Parse each checkbox line
dod_items = []

FOR each line matching "^- \[(x| )\] (.+)$":
  Extract:
    - checkbox_status: x or (space)
    - item_text: full text after checkbox
    - section: Implementation / Quality / Testing / Documentation

  Store:
    dod_items.append({
      text: item_text,
      status: checkbox_status,
      section: section
    })
```

---

## Step 3: Map AC Requirements to DoD Coverage

### Step 3.1: Keyword Extraction

For each AC requirement, extract keywords:

```
requirement = "Document includes introduction (≥200 words)"

keywords = extract_keywords(requirement)
  → ["document", "introduction", "200", "words"]

# Remove stop words
keywords = remove_stop_words(keywords)
  → ["introduction", "200", "words"]

# Normalize
keywords = lowercase(keywords)
  → ["introduction", "200", "words"]
```

### Step 3.2: Search DoD for Coverage

```
FOR each ac_req in ac_requirements:
  keywords = extract_keywords(ac_req.text)

  # Search DoD items for keyword matches
  FOR each dod_item in dod_items:
    dod_keywords = extract_keywords(dod_item.text)

    # Calculate match score
    matches = count(keywords intersect dod_keywords)
    match_score = matches / keywords.length

    IF match_score ≥ 0.5:  # 50%+ keyword overlap
      # Likely coverage found
      potential_coverage = dod_item

  IF potential_coverage found:
    # Determine coverage type
    IF dod_item explicitly mentions requirement:
      coverage_type = "Explicit Checkbox"

    ELSE IF dod_item mentions "test" and AC number:
      coverage_type = "Test Validation"
      # Example: "Integration test (AC#2 - PASS)"

    ELSE IF dod_item provides metric for requirement:
      coverage_type = "Metric Validation"
      # Example: "Coverage >95%" validates AC coverage requirement

    traceability_map[ac_req] = {
      dod_item: dod_item,
      coverage_type: coverage_type,
      match_score: match_score
    }

  ELSE:
    # No coverage found
    missing_traceability.append(ac_req)
```

### Step 3.3: Calculate Traceability Score

```
covered_requirements = total_ac_requirements - missing_traceability.length
traceability_score = (covered_requirements / total_ac_requirements) × 100
```

**Example (STORY-052):**
```
Total AC requirements: 30
Covered: 30
Missing: 0
Traceability Score: 100%
```

**Example (Incomplete Story):**
```
Total AC requirements: 10
Covered: 7
Missing: 3 (AC#2 performance requirement, AC#3 error handling, AC#4 logging)
Traceability Score: 70% ❌ (100% required)
```

---

## Step 4: Validate Deferrals (If DoD Incomplete)

### Step 4.1: Check for "Approved Deferrals" Section

```
IF dod_unchecked > 0:
  # Story has incomplete DoD items

  # Search for section
  has_deferral_section = search_for("^## Approved Deferrals", story_file)

  IF has_deferral_section:
    # Extract deferral details
    deferral_section = extract_section("^## Approved Deferrals", story_file)

    Extract:
      - user_approval_timestamp = grep "User Approval:.*UTC"
      - deferred_items_list = extract_numbered_list(deferral_section)
      - blocker_justifications = grep "Blocker Type:" for each item

    # Validate each incomplete DoD item is documented
    FOR each unchecked_item in dod_unchecked_items:
      IF unchecked_item.text in deferred_items_list:
        documented_deferrals.append(unchecked_item)
      ELSE:
        undocumented_items.append(unchecked_item)

    # Determine deferral status
    IF undocumented_items.length == 0:
      deferral_status = "VALID (all {dod_unchecked} items user-approved)"
    ELSE:
      deferral_status = "INVALID ({undocumented_items.length} items lack approval)"

  ELSE:
    # No deferral section found
    deferral_status = "INVALID (no Approved Deferrals section, {dod_unchecked} items incomplete)"

ELSE:
  # DoD 100% complete
  deferral_status = "N/A (DoD 100% complete)"
```

---

## Step 5: Apply Quality Gate Rules

### Decision Logic

```
IF traceability_score < 100:
  ┌─ HALT QA Workflow ─┐
  │ Display:           │
  │ ❌ Traceability    │
  │   Insufficient     │
  │                    │
  │ Score: {score}%    │
  │ Missing:           │
  │ • {req 1}          │
  │ • {req 2}          │
  │                    │
  │ Remediation:       │
  │ Add DoD items      │
  └────────────────────┘
  EXIT (do not proceed to Phase 1)

ELSE IF dod_unchecked > 0 AND deferral_status contains "INVALID":
  ┌─ HALT QA Workflow ─┐
  │ Display:           │
  │ ❌ Incomplete DoD  │
  │   Without Approval │
  │                    │
  │ Incomplete: {N}    │
  │ Documented: {M}    │
  │                    │
  │ Remediation:       │
  │ Add "Approved      │
  │ Deferrals" section │
  └────────────────────┘
  EXIT

ELSE:
  ┌─ PASS ─────────────┐
  │ Display:           │
  │ ✓ Traceability     │
  │   Validation PASS  │
  │                    │
  │ AC-DoD: {score}%   │
  │ DoD: {pct}%        │
  │ Deferrals: {sts}   │
  └────────────────────┘
  Proceed to Phase 1 (Validation Mode Selection)
```

---

## Edge Cases Handled

### Edge Case 1: Multiple DoD Items Cover One AC Requirement

**Scenario:** AC#1 requires "User authentication with email and password"

**DoD Coverage:**
- Implementation: "Email validation implemented"
- Implementation: "Password hashing implemented (bcrypt)"
- Testing: "Auth integration test passing"

**Handling:** Count as COVERED (3 DoD items collectively validate)

---

### Edge Case 2: One DoD Item Covers Multiple AC Requirements

**Scenario:** DoD item: "All tests passing (validates AC#1, AC#2, AC#3)"

**AC Coverage:**
- AC#1: Feature works
- AC#2: Error handling
- AC#3: Performance

**Handling:** Count as COVERED for all 3 ACs (rollup validation acceptable)

---

### Edge Case 3: Test-Based Validation

**Scenario:** AC#2 has 5 granular requirements

**DoD Coverage:** Single item: "Example validation test (AC#2 - PASS)"

**Handling:**
- Test validates all 5 requirements algorithmically
- Count as COVERED (test provides comprehensive validation)
- Coverage type: "Test Validation"

---

### Edge Case 4: Design-Phase Story

**Scenario:** STORY-023 (design complete, implementation deferred to STORY-024)

**Expected:**
- Traceability: 100% (design requirements have design DoD items)
- DoD completion: 68% (implementation deferred)
- Deferrals: Documented with user approval timestamp

**Handling:** PASS (design complete, implementation properly deferred)

---
```

**Reference:** Complete algorithm specification in QA-ENHANCEMENT.md

**Effort:** 30 minutes (writing algorithm documentation)

---

### Step 3: Create Display Templates Asset File (15 minutes)

**Objective:** Standardized display templates for traceability validation results

**File to Create:** `src/claude/skills/devforgeai-qa/assets/traceability-report-template.md`

**Content Structure:**

```markdown
# AC-to-DoD Traceability Report Templates

**Used By:** devforgeai-qa skill Phase 0.9

---

## PASS Template (100% Traceability)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Phase 0.9: AC-DoD Traceability Validation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Acceptance Criteria Analysis:
  • Total ACs: {ac_count}
  • Total AC requirements (granular): {ac_req_count}
  • DoD items: {dod_total}

Traceability Mapping:
  • AC#1 ({req_count} requirements) → {dod_count} DoD items ✓
  • AC#2 ({req_count} requirements) → {dod_count} DoD items ✓
  {... for each AC ...}

Traceability Score: {score}% ✅

DoD Completion Status:
  • Total items: {dod_total}
  • Complete [x]: {dod_checked}
  • Incomplete [ ]: {dod_unchecked}
  • Completion: {completion_pct}%

{IF dod_unchecked > 0}:
Deferral Documentation: {deferral_status}
  • Approved Deferrals section: EXISTS
  • User approval timestamp: {timestamp}
  • Deferred items: {count} (100% documented)

✓ PASS - Traceability validated, story ready for QA validation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## FAIL Template: Missing Traceability

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ QA VALIDATION FAILED - AC-DoD Traceability Insufficient
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Acceptance Criteria Analysis:
  • Total ACs: {ac_count}
  • Total requirements: {ac_req_count}

Traceability Mapping:
  • AC#1 ({req_count} requirements) → {dod_count} DoD items ✓
  • AC#2 ({req_count} requirements) → NOT FOUND ✗
  • AC#3 ({req_count} requirements) → {dod_count} DoD items ✓
  {... highlighting ✗ FAIL ones ...}

Traceability Score: {score}% ❌ (100% required)

Missing DoD Coverage for AC Requirements:
  • {AC requirement 1 description}
  • {AC requirement 2 description}
  {... list all missing ...}

ACTION REQUIRED:

Option 1: Add DoD Items (Recommended)
  Add to appropriate DoD subsection:

  ### Implementation
  {FOR each missing requirement related to implementation}:
  - [ ] {requirement with measurable criteria}

  ### Testing
  {FOR each missing requirement related to testing}:
  - [ ] {requirement with measurable criteria}

  Example:
  - [ ] Performance validated: API response <200ms (p95)
  - [ ] Error handling tested for 5 failure scenarios

Option 2: Clarify Existing Coverage
  If DoD items exist but different wording prevented detection:
    1. Update DoD item text to explicitly mention AC requirement
    2. Add AC reference: "(validates AC#N: {requirement})"

  Example:
    Before: "- [x] All tests passing"
    After:  "- [x] All tests passing (AC#2: Error handling validated)"

Option 3: Update AC (If Invalid)
  If requirement is obsolete or incorrectly stated:
    1. Edit story AC section
    2. Remove or revise requirement
    3. Document decision in Implementation Notes
    4. Re-run /qa

After fixing, re-run: /qa {STORY_ID}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## FAIL Template: Undocumented Deferrals

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ QA VALIDATION FAILED - Incomplete DoD Without Approval
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DoD Completion: {completion_pct}% ({dod_checked}/{dod_total} items)

Incomplete Items: {dod_unchecked}

Deferral Documentation: {deferral_status}

{IF no deferral section}:
No "Approved Deferrals" section found in Implementation Notes.
Story has {dod_unchecked} incomplete DoD items without documented user approval.

{IF partial documentation}:
"Approved Deferrals" section exists but only documents {documented_count}/{dod_unchecked} incomplete items.

Undocumented Incomplete Items:
  • {item 1 text}
  • {item 2 text}
  {... for each undocumented ...}

ACTION REQUIRED:

Option 1: Complete All Items (Preferred)
  Implement all {dod_unchecked} incomplete items.

Option 2: Document Deferrals (If Valid Blockers)
  Add to Implementation Notes:

  ## Approved Deferrals

  **User Approval:** {timestamp} UTC
  **Approval Type:** {Design-Phase | Low-Priority | Blocker-Dependent}

  **Deferred Items:**
  {FOR each item}:
  {N}. **{item text}**
     - Reason: {Why deferred - be specific}
     - Blocker Type: {Dependency | Toolchain | Artifact | ADR | Low-Priority}
     - Follow-up: {Story ref OR completion condition}

  Then re-run: /qa {STORY_ID}

Option 3: Remove Items (If Obsolete)
  If items are no longer relevant:
    1. Edit DoD section, remove items
    2. Document removal in Implementation Notes
    3. Re-run /qa

After fixing, re-run: /qa {STORY_ID}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
```

**Effort:** 15 minutes (creating display templates)

**Checkpoint:**
- [ ] Template file created
- [ ] PASS template defined
- [ ] FAIL (traceability) template defined
- [ ] FAIL (deferrals) template defined
- [ ] Remediation guidance included

---

### Step 4: Integrate Phase 0.9 into QA Skill (45 minutes)

**Objective:** Insert Phase 0.9 into devforgeai-qa/SKILL.md workflow

**File to Edit:** `src/claude/skills/devforgeai-qa/SKILL.md`

**Location:** After Phase 0 ends, before Phase 1 begins

**Content to Insert:**

```markdown
---

## Phase 0.9: AC-DoD Traceability Validation (NEW - RCA-012)

**Purpose:** Verify every Acceptance Criterion requirement has corresponding Definition of Done coverage. Prevents quality gate bypass and ensures complete work validation.

**Reference:** See `references/traceability-validation-algorithm.md` for complete algorithm

**Display Templates:** See `assets/traceability-report-template.md` for PASS/FAIL formatting

**Execution:**

### Step 0.9.1: Load Traceability Algorithm

```
Read(file_path=".claude/skills/devforgeai-qa/references/traceability-validation-algorithm.md")
```

Algorithm loaded into context (progressive loading - ~300 lines).

---

### Step 0.9.2: Execute Algorithm

**Run 5-step validation:**

```
1. Extract AC count and granular requirements
   - Parse AC headers (v2.1 format: ### AC#N: OR v2.0 format: ### N. [ ])
   - Extract Given/When/Then scenarios
   - Extract bullet list requirements
   - Extract measurable criteria (≥, ≤, <, >, percentages)
   - Store: ac_requirements[] (all granular requirements)

2. Extract DoD items
   - Count total checkboxes in DoD section
   - Count checked [x] and unchecked [ ]
   - Calculate completion percentage
   - Store: dod_items[] (all DoD items with status)

3. Map AC requirements to DoD coverage
   - For each AC requirement, extract keywords
   - Search DoD items for keyword matches (≥50% overlap)
   - Determine coverage type (Explicit / Test / Metric)
   - Store: traceability_map{} (requirement → DoD item mapping)
   - Identify: missing_traceability[] (unmapped requirements)

4. Calculate traceability score
   - covered = total_requirements - missing.length
   - score = (covered / total) × 100
   - Target: 100%

5. Validate deferrals (if DoD incomplete)
   - Check for "Approved Deferrals" section
   - Extract user approval timestamp
   - Match unchecked DoD items to deferred items list
   - Determine: deferral_status (VALID / INVALID)
```

**Result:**
- `traceability_score`: 0-100%
- `dod_completion_pct`: 0-100%
- `deferral_status`: VALID / INVALID / N/A
- `missing_traceability[]`: List of unmapped requirements

---

### Step 0.9.3: Display Traceability Report

**Load display template:**
```
Read(file_path=".claude/skills/devforgeai-qa/assets/traceability-report-template.md")
```

**Select template based on result:**

```
IF traceability_score == 100 AND (dod_unchecked == 0 OR deferral_status == "VALID"):
  Use: PASS template
  Display: Success message with summary

ELSE IF traceability_score < 100:
  Use: FAIL template (Missing Traceability)
  Display: Error message with missing requirements list
  Display: Remediation guidance (3 options)

ELSE IF dod_unchecked > 0 AND deferral_status contains "INVALID":
  Use: FAIL template (Undocumented Deferrals)
  Display: Error message with incomplete items list
  Display: Remediation guidance (deferral template)
```

**Populate template with actual data:**
- Substitute {ac_count}, {traceability_score}, {dod_completion_pct}, etc.
- List missing requirements (if any)
- List undocumented items (if any)
- Format for terminal display (80-column width, box drawing)

**Display to user:**
```
Output: {populated_template}
```

---

### Step 0.9.4: Quality Gate Decision

**Apply gate rules:**

```
IF traceability_score < 100:
  Display: FAIL template (missing traceability)
  HALT QA workflow
  EXIT Phase 0.9 (do NOT proceed to Phase 1)

IF dod_unchecked > 0 AND deferral_status == "INVALID":
  Display: FAIL template (undocumented deferrals)
  HALT QA workflow
  EXIT Phase 0.9

IF all checks PASS:
  Display: PASS template
  Display: "Proceeding to Phase 1..."
  Continue to Phase 1 (Validation Mode Selection)
```

**Checkpoint:**
- [ ] Algorithm executed successfully
- [ ] Traceability score calculated
- [ ] Deferral status validated (if applicable)
- [ ] Display template selected and populated
- [ ] Quality gate decision made (PASS/HALT)
- [ ] Workflow proceeds or halts appropriately

---

**Phase 0.9 Pseudo-Code Summary:**

```
Phase 0.9: AC-DoD Traceability Validation
  ↓
Load algorithm (traceability-validation-algorithm.md)
  ↓
Execute 5-step validation:
  1. Extract AC requirements (parse story AC section)
  2. Extract DoD items (parse story DoD section)
  3. Map AC → DoD (keyword matching, ≥50% overlap)
  4. Calculate score (covered / total × 100)
  5. Validate deferrals (if incomplete)
  ↓
Load display templates (traceability-report-template.md)
  ↓
Select template (PASS / FAIL-traceability / FAIL-deferrals)
  ↓
Populate and display
  ↓
Quality Gate Decision:
  ├─ traceability < 100% → HALT (display remediation)
  ├─ deferrals invalid → HALT (display deferral template)
  └─ all PASS → Continue to Phase 1
```

---

**Integration Point:**
- Insert this section after Phase 0, before Phase 1 in devforgeai-qa/SKILL.md
- Phase numbering: Phase 0 → Phase 0.9 → Phase 1 → ... → Phase 6
- Token cost: ~2K in main conversation (algorithm loaded progressively)

**Effort:** 45 minutes (writing Phase 0.9 section, integrating into skill)

**Checkpoint:**
- [ ] Phase 0.9 section written
- [ ] Inserted at correct location (after Phase 0)
- [ ] Algorithm reference included
- [ ] Display template reference included
- [ ] Quality gate rules implemented
- [ ] No syntax errors

---

### Step 5: Sync QA Skill to Operational Location (2 minutes)

**Objective:** Make updated QA skill available for runtime use

**Commands:**
```bash
# Sync main skill file
cp src/claude/skills/devforgeai-qa/SKILL.md \
   .claude/skills/devforgeai-qa/SKILL.md

# Sync reference files
cp src/claude/skills/devforgeai-qa/references/traceability-validation-algorithm.md \
   .claude/skills/devforgeai-qa/references/traceability-validation-algorithm.md

# Sync asset files
mkdir -p .claude/skills/devforgeai-qa/assets
cp src/claude/skills/devforgeai-qa/assets/traceability-report-template.md \
   .claude/skills/devforgeai-qa/assets/traceability-report-template.md

echo "✓ QA skill synced: src/ → .claude/"
```

**Validation:**
```bash
# Verify sync
diff src/claude/skills/devforgeai-qa/SKILL.md \
     .claude/skills/devforgeai-qa/SKILL.md
# Expected: No output (files identical)

# Verify Phase 0.9 present
grep "Phase 0.9.*Traceability" .claude/skills/devforgeai-qa/SKILL.md
# Expected: 1 match
```

**Checkpoint:**
- [ ] SKILL.md synced
- [ ] Reference files synced
- [ ] Asset files synced
- [ ] Files identical (src/ ↔ .claude/)

---

### Step 6: Test Scenario 1 - Perfect Traceability (Should PASS) (10 minutes)

**Objective:** Verify QA allows stories with 100% traceability

**Test Story:** STORY-007 (known perfect compliance from sampling)

**Procedure:**
```bash
# Run QA validation
/qa STORY-007 light
```

**Expected Behavior:**
```
Phase 0.9: AC-DoD Traceability Validation

Traceability Score: 100% ✅
DoD Completion: 100%

✓ PASS - Traceability validated

Phase 1: Validation Mode = light
... (QA continues normally)
```

**Validation Checklist:**
- [ ] Phase 0.9 executes (output visible)
- [ ] Displays "Phase 0.9: AC-DoD Traceability Validation" header
- [ ] Shows traceability score (100%)
- [ ] Shows PASS status (✓)
- [ ] QA continues to Phase 1 (NOT halted)
- [ ] QA completes without Phase 0.9-related errors

**If Fails:**
- Review Phase 0.9 integration
- Check algorithm execution
- Verify display template used
- Debug and fix before proceeding

---

### Step 7: Test Scenario 2 - Missing Traceability (Should FAIL/HALT) (10 minutes)

**Objective:** Verify QA halts when AC requirement has no DoD coverage

**Test Story:** Create intentionally incomplete story

**Setup:**
```bash
# Create test story file
cat > devforgeai/specs/Stories/TEST-MISSING-TRACEABILITY.story.md << 'EOF'
---
id: TEST-MISSING-TRACEABILITY
title: Test Story - Missing DoD Coverage
status: Dev Complete
format_version: "2.1"
---

## Acceptance Criteria

### AC#1: Feature Works and Performs Well

**Given** valid input
**When** user submits
**Then** system processes successfully
**And** system completes in <100ms
**And** system logs transaction

## Definition of Done

### Implementation
- [x] Feature implemented

# MISSING DoD items for:
# - "<100ms" performance requirement (AC#1)
# - "logs transaction" logging requirement (AC#1)
EOF
```

**Procedure:**
```bash
/qa TEST-MISSING-TRACEABILITY light
```

**Expected Behavior:**
```
Phase 0.9: AC-DoD Traceability Validation

Traceability Score: 33% ❌ (1/3 requirements covered)

Missing DoD Coverage:
  • AC#1: completes in <100ms
  • AC#1: logs transaction

❌ QA VALIDATION FAILED - AC-DoD Traceability Insufficient
... (remediation guidance displayed)
```

**Validation Checklist:**
- [ ] QA halts at Phase 0.9 (does NOT continue to Phase 1)
- [ ] Displays FAIL status clearly
- [ ] Shows traceability score (33%)
- [ ] Lists 2 missing requirements correctly
- [ ] Provides remediation guidance (3 options)
- [ ] Exit is graceful (no errors, clean HALT)

**Cleanup:**
```bash
rm devforgeai/specs/Stories/TEST-MISSING-TRACEABILITY.story.md
```

**If Fails:**
- Algorithm may not be detecting missing coverage
- Review keyword matching logic
- Check edge case handling
- Fix and re-test

---

### Step 8: Test Scenario 3 - Undocumented Deferrals (Should FAIL/HALT) (10 minutes)

**Objective:** Verify QA halts when DoD incomplete without "Approved Deferrals" section

**Test Story:** Simulate STORY-038 issue pattern

**Setup:**
```bash
cat > devforgeai/specs/Stories/TEST-UNDOCUMENTED-DEFERRALS.story.md << 'EOF'
---
id: TEST-UNDOCUMENTED-DEFERRALS
title: Test Story - Incomplete DoD Without Deferrals
status: Dev Complete
format_version: "2.1"
---

## Acceptance Criteria

### AC#1: Feature Complete

**Given** all scenarios
**When** tested
**Then** feature works correctly

## Definition of Done

### Implementation
- [x] Feature implemented
- [x] Code reviewed

### Testing
- [x] Unit tests passing
- [ ] Performance test (10K load)
- [ ] E2E test (full workflow)

# NO "Approved Deferrals" section
# Simulates STORY-038 pattern (incomplete without documentation)
EOF
```

**Procedure:**
```bash
/qa TEST-UNDOCUMENTED-DEFERRALS light
```

**Expected Behavior:**
```
Phase 0.9: AC-DoD Traceability Validation

Traceability Score: 100% ✅

DoD Completion: 60% (3/5 items)

Deferral Documentation: INVALID (no Approved Deferrals section)

❌ QA VALIDATION FAILED - Incomplete DoD Without Approval

Incomplete Items: 2
- Performance test (10K load)
- E2E test (full workflow)

ACTION REQUIRED:
Add "Approved Deferrals" section...
... (deferral template displayed)
```

**Validation Checklist:**
- [ ] QA halts at Phase 0.9
- [ ] Traceability shows 100% (AC requirements covered)
- [ ] DoD completion shows 60% (3/5 items)
- [ ] Detects missing "Approved Deferrals" section
- [ ] Lists 2 incomplete items
- [ ] Provides deferral section template
- [ ] Does NOT proceed to Phase 1

**Cleanup:**
```bash
rm devforgeai/specs/Stories/TEST-UNDOCUMENTED-DEFERRALS.story.md
```

**If Fails:**
- Deferral detection logic may be broken
- Review Step 4 of algorithm (validate deferrals)
- Check "Approved Deferrals" section search
- Fix and re-test

---

### Step 9: Test Scenario 4 - Documented Deferrals (Should PASS) (10 minutes)

**Objective:** Verify QA allows incomplete DoD when deferrals are properly documented

**Test Story:** STORY-023 (known valid deferrals from sampling)

**Procedure:**
```bash
/qa STORY-023 light
```

**Expected Behavior:**
```
Phase 0.9: AC-DoD Traceability Validation

Traceability Score: 100% ✅

DoD Completion: 68% (15/22 items)

Deferral Documentation: VALID (7 items user-approved)
  • Approved Deferrals section: EXISTS
  • User approval: 2025-11-14 14:30 UTC
  • Deferred items: 7 (100% documented)

✓ PASS - Traceability validated, deferrals properly documented

Phase 1: Validation Mode = light
... (QA continues)
```

**Validation Checklist:**
- [ ] Phase 0.9 executes
- [ ] Traceability score: 100%
- [ ] DoD completion: 68% (detected correctly)
- [ ] Recognizes "Approved Deferrals" section
- [ ] Validates user approval timestamp
- [ ] Shows PASS status
- [ ] QA continues to Phase 1 (NOT halted)

**If Fails:**
- Deferral validation may be too strict
- Review deferral matching logic
- Check timestamp parsing
- Fix and re-test

---

### Step 10: Commit Phase 2 Changes to Git (5 minutes)

**Objective:** Commit QA enhancement with comprehensive message

**Files to Commit:**
- `src/claude/skills/devforgeai-qa/SKILL.md` (Phase 0.9 added)
- `src/claude/skills/devforgeai-qa/references/traceability-validation-algorithm.md` (new)
- `src/claude/skills/devforgeai-qa/assets/traceability-report-template.md` (new)
- Operational syncs in `.claude/skills/devforgeai-qa/`

**Commit Command:**
```bash
git add src/claude/skills/devforgeai-qa/SKILL.md
git add src/claude/skills/devforgeai-qa/references/traceability-validation-algorithm.md
git add src/claude/skills/devforgeai-qa/assets/traceability-report-template.md
git add .claude/skills/devforgeai-qa/

git commit -m "$(cat <<'EOF'
feat(RCA-012 Phase 2): QA traceability validation (Phase 0.9)

QA Enhancement (REC-5):
- Added Phase 0.9 to devforgeai-qa skill
- Validates 100% AC-to-DoD traceability before validation
- Enforces documented deferrals for incomplete DoD items
- Prevents quality gate bypass (STORY-038 pattern)

Implementation:
- New Phase 0.9 in SKILL.md (after Phase 0, before Phase 1)
- Traceability algorithm (5 steps: extract, map, score, validate)
- Display templates (PASS/FAIL scenarios with remediation)
- Quality gate rules (HALT if <100% or undocumented deferrals)

Impact:
- Catches structural issues before expensive validations
- Token savings: ~60K per caught issue (skip Phases 2-6)
- Prevents STORY-038-style bypasses (87% DoD without approval)

Test Results:
- Scenario 1: STORY-007 (100% traceability) → PASS ✓
- Scenario 2: Missing coverage → HALT with remediation ✓
- Scenario 3: Undocumented deferrals → HALT with template ✓
- Scenario 4: STORY-023 (documented deferrals) → PASS ✓

All 4 scenarios validated successfully.

Files Created:
- references/traceability-validation-algorithm.md (~300 lines)
- assets/traceability-report-template.md (~200 lines)

Files Modified:
- SKILL.md (Phase 0.9 added, ~150 lines)

Compliance: RCA-012 remediation plan, quality gate enforcement
EOF
)"
```

**Validation:**
```bash
git log -1 --stat
# Expected: Commit created with 3 files (1 modified, 2 new)
```

**Checkpoint:**
- [ ] All Phase 2 files staged
- [ ] Commit message comprehensive
- [ ] Commit successful
- [ ] No pre-commit hook failures

---

## Phase 2 Completion Checklist

**All items MUST be checked before marking Phase 2 complete:**

### Reference Files
- [ ] Step 2: traceability-validation-algorithm.md created (~300 lines)
- [ ] Algorithm includes all 5 steps (extract, map, score, validate deferrals, gate decision)
- [ ] Edge cases documented (4 cases: multiple coverage, rollup, test-based, design-phase)

### Asset Files
- [ ] Step 3: traceability-report-template.md created (~200 lines)
- [ ] PASS template defined
- [ ] FAIL (missing traceability) template defined
- [ ] FAIL (undocumented deferrals) template defined
- [ ] Remediation guidance comprehensive (3 options each)

### Skill Integration
- [ ] Step 4: Phase 0.9 added to devforgeai-qa/SKILL.md (~150 lines)
- [ ] Inserted after Phase 0, before Phase 1
- [ ] References algorithm file correctly
- [ ] References template file correctly
- [ ] Quality gate rules implemented
- [ ] No syntax errors

### Operational Sync
- [ ] Step 5: Files synced (src/ → .claude/)
- [ ] SKILL.md synced
- [ ] Reference file synced
- [ ] Asset file synced
- [ ] All files identical

### Testing
- [ ] Step 6: Test 1 - STORY-007 (perfect) → PASS ✓
- [ ] Step 7: Test 2 - Missing coverage → HALT ✓
- [ ] Step 8: Test 3 - Undocumented deferrals → HALT ✓
- [ ] Step 9: Test 4 - STORY-023 (documented) → PASS ✓

### Git Commit
- [ ] Step 10: All files committed
- [ ] Commit message comprehensive
- [ ] Commit successful

**Total:** 24 checkpoints, all must PASS

---

## Success Criteria

**Phase 2 is successful when:**

**Deliverables:**
- [ ] Phase 0.9 integrated into QA workflow
- [ ] Traceability algorithm documented (~300 lines)
- [ ] Display templates created (~200 lines)
- [ ] All files synced (src/ → operational)

**Validation:**
- [ ] All 4 test scenarios behave correctly
  - Perfect traceability (STORY-007) → PASS
  - Missing coverage → HALT with remediation
  - Undocumented deferrals → HALT with template
  - Documented deferrals (STORY-023) → PASS
- [ ] No false positives (valid stories incorrectly halted)
- [ ] No false negatives (invalid stories incorrectly passed)

**Metrics:**
- Implementation: ~500 lines total (algorithm + templates + Phase 0.9)
- Test scenarios: 4/4 pass
- Time: ≤2.5 hours (target: 2 hours)
- Token overhead: <2K per QA run

**User Experience:**
- QA catches structural issues early (before expensive validations)
- Clear remediation guidance (actionable steps)
- No confusion about quality gate (expectations clear)

---

## Timeline Breakdown

### Optimistic (No Issues)

| Step | Duration | Cumulative |
|------|----------|------------|
| 1. Read QA skill | 10 min | 10 min |
| 2. Create algorithm file | 30 min | 40 min |
| 3. Create template file | 15 min | 55 min |
| 4. Integrate Phase 0.9 | 45 min | 1h 40min |
| 5. Sync to operational | 2 min | 1h 42min |
| 6-9. Test scenarios (4) | 40 min | 2h 22min |
| 10. Commit changes | 5 min | 2h 27min |
| **Total** | **2h 27min** | - |

**Buffer:** 2h 27min vs. 2h estimate = 27 minutes over (acceptable)

---

### Realistic (With Iteration)

| Activity | Duration | Cumulative |
|----------|----------|------------|
| Steps 1-3 | 1 hour | 1 hour |
| Step 4 (with review) | 1 hour | 2 hours |
| Step 5 | 5 min | 2h 5min |
| Steps 6-9 (with fixes) | 1 hour | 3h 5min |
| Step 10 | 5 min | 3h 10min |
| **Total** | **3h 10min** | - |

**Includes:** Time for test failures, algorithm adjustments, re-testing

---

### Pessimistic (Issues Found)

| Activity | Duration | Cumulative |
|----------|----------|------------|
| Initial implementation | 2 hours | 2 hours |
| Test scenario 2 fails | - | - |
| Debug algorithm | 30 min | 2h 30min |
| Fix keyword matching | 30 min | 3 hours |
| Re-test all scenarios | 30 min | 3h 30min |
| Additional edge case | 30 min | 4 hours |
| **Total** | **4 hours** | - |

**Worst Case:** Algorithm has bugs requiring significant rework

---

## Risk Assessment

### Risk 1: Algorithm False Positives

**Description:** QA halts valid stories (claims missing coverage when DoD actually covers AC)

**Likelihood:** Medium (keyword matching may miss synonyms)
**Impact:** High (blocks valid work, user frustration)

**Mitigation:**
- Comprehensive keyword extraction (include synonyms)
- Adjust match threshold (50% may be too strict, try 40%)
- Manual review during testing (catch false positives early)

**Rollback:** Comment out Phase 0.9, fix algorithm, re-enable

---

### Risk 2: Algorithm False Negatives

**Description:** QA passes invalid stories (claims coverage when DoD actually missing)

**Likelihood:** Low (conservative matching reduces this risk)
**Impact:** High (quality gate bypass, defeats purpose)

**Mitigation:**
- Test with known incomplete stories
- Verify STORY-038 pattern would be caught
- Adjust match threshold if needed (stricter)

**Rollback:** Not needed (false negatives less critical than false positives)

---

### Risk 3: Performance Overhead

**Description:** Phase 0.9 adds excessive time/token cost to QA runs

**Likelihood:** Low (lightweight validation, story file already loaded)
**Impact:** Medium (slower QA, more tokens)

**Mitigation:**
- Measure overhead (Step 6 baseline vs. enhanced)
- Target: <30 seconds, <2K tokens
- Optimize if exceeds (cache AC/DoD extraction)

**Rollback:** Disable Phase 0.9 if overhead unacceptable

---

## Rollback Procedure

**If Phase 2 must be rolled back:**

### Step R1: Disable Phase 0.9
```bash
# Edit QA skill
vi src/claude/skills/devforgeai-qa/SKILL.md

# Comment out Phase 0.9 section
<!-- Phase 0.9 disabled - investigating false positives -->
<!--
Phase 0.9: AC-DoD Traceability Validation
...
-->

# Save changes
# Sync to operational
cp src/claude/skills/devforgeai-qa/SKILL.md .claude/skills/devforgeai-qa/SKILL.md
```

### Step R2: Document Rollback Reason
```bash
cat > .devforgeai/RCA/RCA-012/PHASE2-ROLLBACK-LOG.md << 'EOF'
# Phase 2 Rollback Log

**Date:** {timestamp}
**Reason:** {Why rollback needed}

**Issue:**
{What went wrong - false positives, performance, bugs}

**Test Failure:**
{Which test scenario failed and why}

**Next Steps:**
{How to fix - algorithm adjustment, threshold tuning, etc.}
EOF
```

### Step R3: Fix and Re-Enable
- Address root cause
- Re-test with all 4 scenarios
- Re-enable Phase 0.9 when fixed

---

## Integration with Existing QA Phases

### Phase Flow with 0.9 Inserted

**Before Phase 2 (Current QA):**
```
User: /qa STORY-001 deep
  ↓
Phase 0: Parameter Extraction
  ↓
Phase 1: Validation Mode Selection
  ↓
Phases 2-6: Expensive validations (build, test, coverage, security)
  ↓
Phase 7: Report generation
```

**After Phase 2 (Enhanced QA):**
```
User: /qa STORY-001 deep
  ↓
Phase 0: Parameter Extraction
  ↓
Phase 0.9: Traceability Validation ← NEW
  ├─ traceability < 100% → HALT
  ├─ deferrals invalid → HALT
  └─ all PASS → Continue
  ↓
Phase 1: Validation Mode Selection
  ↓
Phases 2-6: Expensive validations (only if 0.9 passed)
  ↓
Phase 7: Report generation
```

**Benefit:** Fail fast on structural issues, save tokens on invalid stories

---

## Post-Phase 2 Actions

**After Phase 2 completes:**

### Update Documentation
1. Mark Phase 2 complete in `.devforgeai/RCA/RCA-012/INDEX.md`
2. Update phase checkboxes (mark [x])
3. Document actual effort vs. estimated

### Prepare Phase 3
1. Read IMPLEMENTATION-GUIDE.md Phase 3 section
2. Read STORY-AUDIT.md (REC-6 details)
3. Allocate 6 hours for historical cleanup
4. Plan STORY-038 fix as priority 1

### Optional Announcement
1. Notify team: QA now validates traceability
2. Provide guidance: How to pass Phase 0.9
3. Reference: CLAUDE.md section on tracking mechanisms

---

## Success Evidence Documentation

**Create completion record:**
```bash
cat > .devforgeai/RCA/RCA-012/PHASE2-SUCCESS-RECORD.md << 'EOF'
# Phase 2 Success Record

**Completion Date:** 2025-01-{XX}
**Actual Effort:** {XX hours YY minutes}
**Executor:** {Name}

## Deliverables Completed

- [x] Phase 0.9 integrated into devforgeai-qa/SKILL.md
- [x] Traceability algorithm documented (~300 lines)
- [x] Display templates created (~200 lines)
- [x] All files synced (src/ → .claude/)
- [x] All 4 test scenarios passing

## Test Results

| Scenario | Expected | Actual | Status |
|----------|----------|--------|--------|
| STORY-007 (perfect) | PASS, continue | PASS | ✅ |
| Missing coverage | HALT, remediation | HALT | ✅ |
| Undocumented deferrals | HALT, template | HALT | ✅ |
| STORY-023 (documented) | PASS, continue | PASS | ✅ |

**Pass Rate:** 4/4 (100%)

## Performance Metrics

- Token overhead: {X}K tokens (target: <2K)
- Time overhead: {X} seconds (target: <30s)
- False positives: {count} (target: 0)
- False negatives: {count} (target: 0)

## Next Steps

Proceed to Phase 3: Historical Cleanup (REC-6)
- Audit 39 QA Approved stories
- Fix STORY-038 and other non-compliant stories
- Estimated effort: 6 hours

**Sign-Off:**
Executor: {Name}
Reviewer: {Name}
Date: 2025-01-{XX}
EOF
```

---

## Files That Will Be Created/Modified

### New Files (3)

**1. Algorithm Reference:**
```
src/claude/skills/devforgeai-qa/references/traceability-validation-algorithm.md
.claude/skills/devforgeai-qa/references/traceability-validation-algorithm.md
```
Size: ~300 lines
Purpose: Complete 5-step algorithm specification

**2. Display Templates:**
```
src/claude/skills/devforgeai-qa/assets/traceability-report-template.md
.claude/skills/devforgeai-qa/assets/traceability-report-template.md
```
Size: ~200 lines
Purpose: PASS/FAIL display formatting

**3. Test Stories (Temporary):**
```
devforgeai/specs/Stories/TEST-MISSING-TRACEABILITY.story.md (deleted after test)
devforgeai/specs/Stories/TEST-UNDOCUMENTED-DEFERRALS.story.md (deleted after test)
```

### Modified Files (1)

**QA Skill:**
```
src/claude/skills/devforgeai-qa/SKILL.md
.claude/skills/devforgeai-qa/SKILL.md
```
Change: Add Phase 0.9 section (~150 lines)
Location: After Phase 0, before Phase 1

---

## Validation Strategy

### Unit Testing (Algorithm Components)

**Test 1: AC Requirement Extraction**
```python
# Test with known story (STORY-052)
requirements = extract_ac_requirements("STORY-052")
assert len(requirements) == 30  # Known count
assert "Introduction ≥200 words" in requirements[0]
```

**Test 2: DoD Item Extraction**
```python
dod_items = extract_dod_items("STORY-052")
assert len(dod_items) == 26  # Known count
assert all(item['status'] == 'x' for item in dod_items)  # All checked
```

**Test 3: Keyword Matching**
```python
ac_req = "Document includes introduction (≥200 words)"
dod_item = "Document has intro (648 words)"

match_score = calculate_match(ac_req, dod_item)
assert match_score >= 0.5  # Should match (intro/introduction, words)
```

---

### Integration Testing (Phase 0.9 in QA)

**Test 1:** Full QA run on STORY-007 → Should PASS and continue
**Test 2:** QA on incomplete story → Should HALT at Phase 0.9
**Test 3:** QA on story with deferrals → Should PASS if documented
**Test 4:** QA on STORY-038 (before fix) → Should HALT (missing deferrals)

---

### Regression Testing

**Test 1: Old Stories Still Work**
```bash
# Run QA on v1.0/v2.0 stories
/qa STORY-014 light  # v2.0 format
/qa STORY-007 light  # v2.0 format

# Expected: Phase 0.9 handles both formats correctly
```

**Test 2: QA Workflow Unchanged for Valid Stories**
```bash
# Stories with 100% DoD should experience no change
/qa STORY-030 light

# Expected: Same behavior as before Phase 2 (just +Phase 0.9 output)
```

---

## Go/No-Go Decision Points

### Checkpoint 1: After Step 4 (Phase 0.9 Integration)

**Question:** Is Phase 0.9 correctly integrated without syntax errors?

**Validation:**
```bash
# Check for syntax errors
grep -A 20 "Phase 0.9" src/claude/skills/devforgeai-qa/SKILL.md

# Verify references work
grep "traceability-validation-algorithm.md" src/claude/skills/devforgeai-qa/SKILL.md
```

**If YES:** Continue to Step 5 (sync)
**If NO:** Fix syntax errors, re-validate

---

### Checkpoint 2: After Step 6-9 (All Test Scenarios)

**Question:** Did all 4 test scenarios behave as expected?

**Criteria:**
- Test 1 (STORY-007): PASS and QA continues ✓
- Test 2 (missing): HALT with remediation ✓
- Test 3 (no deferrals): HALT with template ✓
- Test 4 (STORY-023): PASS with deferrals ✓

**If ALL YES:** Proceed to Step 10 (commit)
**If ANY NO:** Debug failures, fix algorithm, re-test all

---

### Checkpoint 3: After Step 10 (Commit)

**Question:** Was commit successful? Any pre-commit issues?

**If YES:** Phase 2 COMPLETE
**If NO:** Fix pre-commit issues, retry

---

## Expected Outcomes

**When Phase 2 completes:**

### Immediate
- ✅ QA workflow enhanced with traceability validation
- ✅ Quality gate bypass prevention operational
- ✅ STORY-038 pattern would be caught (if encountered now)

### Testing Evidence
- ✅ 4/4 test scenarios pass
- ✅ No false positives detected
- ✅ STORY-007 and STORY-023 still pass QA
- ✅ Invalid stories properly halted

### Documentation
- ✅ Algorithm documented for transparency
- ✅ Display templates ensure consistency
- ✅ Integration tested and validated

### Ready for Phase 3
- ✅ Phase 0.9 operational
- ✅ Can now audit 39 stories with confidence
- ✅ Enhanced QA will catch any remaining issues

---

## Phase 2 Dependencies

### Prerequisite (MUST be complete)
- ✅ Phase 1: Template v2.1 operational (handles both old and new format)
- ✅ CLAUDE.md documents tracking mechanisms
- ✅ User understands DoD is source of truth

### No Dependencies (Can run parallel with Phase 1)
- Phase 2 doesn't depend on Phase 1 completion
- Could have been implemented before template change
- Sequential execution chosen for logical flow

### Enables (What Phase 2 makes possible)
- ✅ Phase 3: Audit with confidence (Phase 0.9 validates fixes)
- ✅ Future stories: Automatic validation (no manual review needed)
- ✅ Quality assurance: Systematic enforcement (not ad-hoc)

---

## Measurement and Monitoring

### Success Metrics to Track

**After Phase 2 implementation:**

**1. Quality Gate Effectiveness:**
- Count: Stories halted at Phase 0.9 (vs. passed)
- Target: 0 false positives, 100% true positives

**2. Token Savings:**
- Measure: Tokens saved by failing at Phase 0.9 vs. Phase 6
- Target: ~60K tokens per caught issue

**3. User Experience:**
- Collect: User feedback on remediation guidance clarity
- Target: "Clear what to fix" rating ≥4/5

**4. Framework Impact:**
- Track: Stories reaching "QA Approved" with incomplete DoD
- Target: 0 (after Phase 2, should be impossible)

---

**PHASE 2 EXECUTION PLAN COMPLETE**

**Ready to Execute:** Yes (all steps defined, validation procedures ready)
**Estimated Time:** 2-3 hours (with testing)
**Risk Level:** Medium (algorithm complexity, but comprehensive testing mitigates)
**Recommended Start:** After Phase 1 committed (can start immediately)
**Prerequisites:** Phase 1 complete ✅
