# RCA-012: QA Enhancement (REC-5)
## Add AC-DoD Traceability Validation to QA Workflow

**Recommendation ID:** REC-5
**Priority:** HIGH
**Effort:** 2 hours
**Target:** Prevent quality gate bypass, enforce 100% traceability

---

## Objective

Add Phase 0.9 to devforgeai-qa skill that validates 100% AC-to-DoD traceability and enforces documented deferrals for incomplete items, preventing stories like STORY-038 from reaching "QA Approved" with undocumented incomplete DoD checkboxes.

---

## Problem Statement

**Current QA Workflow:**
- Phase 0: Parameter extraction
- Phase 1: Validation mode selection
- Phase 2-6: Various validations (build, test, coverage, security, etc.)

**Gap:** No validation that:
1. Every AC requirement has corresponding DoD coverage
2. Incomplete DoD items have "Approved Deferrals" documentation
3. User approval timestamp present for all deferrals

**Result:** STORY-038 reached "QA Approved" with 4 incomplete items, no deferral documentation

---

## Solution: Phase 0.9 Traceability Validation

### New Workflow Position

```
Phase 0: Parameter Extraction
  ↓
Phase 0.9: AC-DoD Traceability Validation ← NEW
  ↓
Phase 1: Validation Mode Selection
  ↓
Phase 2-6: Existing validations
```

**Rationale:** Traceability must be validated BEFORE expensive validations (build, tests, coverage) to fail fast if story structure is incomplete.

---

## Traceability Validation Algorithm

### Step 1: Extract AC Count and Requirements

**Purpose:** Understand what needs to be validated in DoD

**Algorithm:**
```
Read story file

# Count AC headers
IF template v2.1+:
  ac_headers = grep count "^### AC#[0-9]:"
ELSE IF template v2.0 or v1.0:
  ac_headers = grep count "^### [0-9]\. \["

ac_count = ac_headers

# Extract granular requirements from each AC
ac_requirements = []

FOR each AC section:
  # Parse Given/When/Then scenarios
  then_clauses = grep "^\*\*Then\*\*" in AC section
  ac_requirements.append(then_clauses)

  # Parse bullet list requirements
  bullet_requirements = grep "^- " in AC section (after Then)
  ac_requirements.append(bullet_requirements)

  # Parse measurable criteria
  metrics = grep patterns like "≥X", "<X", "X-Y range"
  ac_requirements.append(metrics)

total_ac_requirements = ac_requirements.length
```

**Example (STORY-052 AC#1):**
```
AC#1: Document Completeness
  → Then document contains:
    → Introduction (≥200 words) [requirement 1]
    → 11 commands [requirement 2]
    → 20-30 examples [requirement 3]
    → Quick reference [requirement 4]
    → ≥10 pitfalls [requirement 5]
    → Progressive disclosure [requirement 6]

  Total: 6 granular requirements from AC#1
```

---

### Step 2: Extract DoD Items

**Purpose:** Understand what coverage exists

**Algorithm:**
```
Read DoD section from story file

# Count total checkboxes
dod_items = grep count "^- \[" (both [x] and [ ])

# Count checked items
dod_checked = grep count "^- \[x\]"

# Count unchecked items
dod_unchecked = grep count "^- \[ \]"

# Calculate completion
dod_completion_pct = (dod_checked / dod_items) * 100
```

---

### Step 3: Map AC Requirements to DoD Coverage

**Purpose:** Verify every AC requirement has DoD validation

**Algorithm:**
```
traceability_map = {}
missing_traceability = []

FOR each ac_req in ac_requirements:
  # Extract keywords from requirement
  keywords = extract_keywords(ac_req)
  # Example: "Introduction ≥200 words" → ["introduction", "200", "words"]

  # Search DoD section for coverage
  dod_coverage = search_dod_for_keywords(keywords)

  IF dod_coverage found:
    # Determine coverage type
    IF dod_item is explicit checkbox mentioning requirement:
      coverage_type = "Explicit Checkbox"
      # Example: "- [x] Document includes introduction (648 words)"

    ELSE IF dod_item references test validating requirement:
      coverage_type = "Test Validation"
      # Example: "- [x] Structure validation test (AC1, AC5 - PASS)"

    ELSE IF dod_item provides metric proving requirement:
      coverage_type = "Metric Validation"
      # Example: "- [x] Introduction words: 648 (>200 required)"

    traceability_map[ac_req] = {
      dod_item: dod_coverage,
      coverage_type: coverage_type
    }
  ELSE:
    missing_traceability.append(ac_req)

traceability_score = ((total_ac_requirements - missing_traceability.length) / total_ac_requirements) * 100
```

**Example (STORY-052):**
```
AC#1 Requirement: "Introduction ≥200 words"
  → DoD Coverage: "Document includes introduction (648 words)"
  → Coverage Type: Explicit Checkbox
  → Traceability: ✓ PASS

AC#2 Requirement: "≥50 words explanations per example"
  → DoD Coverage: "Example validation test (AC2 - PASS)"
  → Coverage Type: Test Validation
  → Traceability: ✓ PASS

Missing Coverage Example:
AC#X Requirement: "Feature processes data in <100ms"
  → DoD Coverage: NOT FOUND
  → Traceability: ✗ FAIL
  → Action: Add DoD item OR remove AC requirement
```

---

### Step 4: Validate Deferrals (If DoD Incomplete)

**Purpose:** Ensure incomplete items have user approval

**Algorithm:**
```
IF dod_unchecked > 0:
  # Story has incomplete DoD items

  # Search for "Approved Deferrals" section
  has_deferral_section = grep "^## Approved Deferrals" story_file

  IF has_deferral_section:
    # Extract deferral details
    Extract:
      - User approval timestamp
      - List of deferred items
      - Blocker justification for each
      - Follow-up story references (if any)

    # Validate each incomplete DoD item is in deferral list
    FOR each unchecked_item in dod_unchecked_items:
      IF unchecked_item in approved_deferrals:
        deferral_map[unchecked_item] = "DOCUMENTED"
      ELSE:
        undocumented_items.append(unchecked_item)

    IF undocumented_items.length == 0:
      deferral_status = "VALID (all {dod_unchecked} items user-approved)"
    ELSE:
      deferral_status = "INVALID ({undocumented_items.length} items lack approval)"

  ELSE:
    # No deferral section
    deferral_status = "INVALID (no Approved Deferrals section, {dod_unchecked} items incomplete)"

ELSE:
  # DoD 100% complete
  deferral_status = "N/A (DoD 100% complete)"
```

**Example (STORY-023):**
```
DoD Status:
  • Total: 22 items
  • Complete: 15 items
  • Incomplete: 7 items

Deferral Documentation:
  • Section exists: YES
  • User approval: 2025-11-14 14:30 UTC
  • Deferred items: 7 (all Quality/Testing items)
  • Follow-up: STORY-024 (completed)

Validation: ✓ PASS (all 7 incomplete items documented with approval)
```

**Example (STORY-038):**
```
DoD Status:
  • Total: 31 items
  • Complete: 27 items
  • Incomplete: 4 items

Deferral Documentation:
  • Section exists: NO
  • User approval: MISSING
  • Deferred items: 0 (no documentation)

Validation: ✗ FAIL (4 incomplete items without approval)
```

---

### Step 5: Apply Quality Gate Rules

**Quality Gate Decision Tree:**

```
IF traceability_score < 100:
  ┌─ HALT QA Workflow ─┐
  │                    │
  │ Display:           │
  │ "❌ AC-DoD         │
  │  Traceability      │
  │  Insufficient"     │
  │                    │
  │ Missing coverage:  │
  │ • {AC req 1}       │
  │ • {AC req 2}       │
  │                    │
  │ Remediation:       │
  │ Add DoD items OR   │
  │ update AC to       │
  │ clarify coverage   │
  └────────────────────┘
  EXIT (do not proceed to Phase 1)

ELSE IF dod_unchecked > 0 AND deferral_status contains "INVALID":
  ┌─ HALT QA Workflow ─┐
  │                    │
  │ Display:           │
  │ "❌ Incomplete DoD │
  │  Without Approval" │
  │                    │
  │ Incomplete: {N}    │
  │ Documented: {M}    │
  │ Missing approval:  │
  │ {N - M} items      │
  │                    │
  │ Remediation:       │
  │ Add "Approved      │
  │ Deferrals" section │
  │ with user approval │
  │ timestamp          │
  └────────────────────┘
  EXIT

ELSE:
  ┌─ PASS ─────────────┐
  │                    │
  │ Display:           │
  │ "✓ Traceability    │
  │  Validation PASS"  │
  │                    │
  │ • AC-DoD: 100%     │
  │ • DoD: {pct}%      │
  │ • Deferrals: {sts} │
  └────────────────────┘
  Proceed to Phase 1 (Validation Mode Selection)
```

---

## Implementation Details

### File Changes Required

**Primary File:**
`.claude/skills/devforgeai-qa/SKILL.md`

**Change:** Insert Phase 0.9 after Phase 0, before Phase 1

**New Content:** ~150 lines (algorithm execution, display template, quality gate rules)

---

**Secondary File (NEW):**
`.claude/skills/devforgeai-qa/references/traceability-validation-algorithm.md`

**Content:** ~200-300 lines
- Complete algorithm specification
- Keyword extraction logic
- Mapping procedures
- Edge case handling
- Example mappings

---

**Tertiary File (NEW):**
`.claude/skills/devforgeai-qa/assets/traceability-report-template.md`

**Content:** ~100 lines
- Display template for traceability report
- PASS/FAIL message formats
- Remediation guidance templates

---

### Implementation Sequence

**Step 1: Create Reference File (30 minutes)**
```
Write(
  file_path=".claude/skills/devforgeai-qa/references/traceability-validation-algorithm.md",
  content={Complete algorithm from Step 1-5 above}
)
```

**Step 2: Create Report Template (15 minutes)**
```
Write(
  file_path=".claude/skills/devforgeai-qa/assets/traceability-report-template.md",
  content={Display templates for PASS/FAIL scenarios}
)
```

**Step 3: Insert Phase 0.9 into QA Skill (45 minutes)**
```
Read .claude/skills/devforgeai-qa/SKILL.md

Find: Phase 0 end / Phase 1 start (search for "Phase 1: Validation Mode Selection")

Edit:
  Insert Phase 0.9 section before Phase 1
  Include:
    - Purpose statement
    - Reference to algorithm file
    - Display template
    - Quality gate rules
```

**Step 4: Test Implementation (30 minutes)**
- Create test stories (valid, invalid, deferrals)
- Run /qa on each
- Verify Phase 0.9 executes correctly
- Verify PASS/FAIL behavior matches expectations

---

## Testing Scenarios

### Scenario 1: Perfect Traceability (Should PASS)

**Test Story:**
```markdown
## Acceptance Criteria

### AC#1: Feature Works
**Given** valid input, **When** user submits, **Then** system processes successfully

## Definition of Done

### Implementation
- [x] Feature implemented
- [x] Processing logic complete
- [x] Success response returned

### Testing
- [x] Unit test: Valid input processing
```

**Expected Result:**
```
Phase 0.9: AC-DoD Traceability Validation

AC Analysis:
  • Total ACs: 1
  • Total requirements: 1 (system processes successfully)

Traceability:
  • AC#1 (1 req) → 3 DoD items (feature, logic, response) ✓

Traceability Score: 100% ✅
DoD Completion: 100% (3/3 items)

✓ PASS - Traceability validated
```

**QA Proceeds to Phase 1**

---

### Scenario 2: Missing DoD Coverage (Should FAIL)

**Test Story:**
```markdown
## Acceptance Criteria

### AC#1: Feature Works
**Given** valid input, **When** user submits, **Then** system processes in <100ms

### AC#2: Error Handling
**Given** invalid input, **When** user submits, **Then** system returns error message

## Definition of Done

### Implementation
- [x] Feature implemented (AC#1 covered)
# MISSING: No DoD item for "<100ms" performance requirement
# MISSING: No DoD item for AC#2 error handling

### Testing
- [x] Unit test: Valid input
```

**Expected Result:**
```
Phase 0.9: AC-DoD Traceability Validation

AC Analysis:
  • Total ACs: 2
  • Total requirements: 3 (processes, <100ms, error message)

Traceability:
  • AC#1 (1 req) → 1 DoD item ✓
  • AC#1 performance (<100ms) → NOT FOUND ✗
  • AC#2 (error handling) → NOT FOUND ✗

Traceability Score: 33% ❌ (1/3 requirements have coverage)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ QA VALIDATION FAILED - AC-DoD Traceability Insufficient

Traceability Score: 33% (100% required)

Missing DoD Coverage for AC Requirements:
  • AC#1: System processes in <100ms (performance requirement)
  • AC#2: Error handling with error message

Action Required:
1. Add DoD items for missing AC requirements:
   - Add to Implementation or Testing section:
     "- [ ] Performance validated: <100ms processing time"
     "- [ ] Error handling implemented for invalid input"

2. OR update ACs to clarify existing DoD items cover requirements
   (if DoD items exist but weren't detected due to different wording)

3. Re-run: /qa {STORY_ID}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**QA HALTS - Does not proceed to Phase 1**

---

### Scenario 3: Incomplete DoD with Documented Deferrals (Should PASS)

**Test Story:**
```markdown
## Acceptance Criteria

### AC#1: Feature Complete
**Given** all scenarios, **When** tested, **Then** feature works

## Definition of Done

### Implementation
- [x] Feature implemented
- [x] Core functionality complete

### Testing
- [x] Unit tests passing
- [ ] Performance test (10K load)
- [ ] E2E test (full workflow)

## Approved Deferrals

**User Approval:** 2025-01-21 10:30 UTC
**Approval Type:** Low-Priority Enhancement Deferral

**Deferred Items:**
1. **Performance test: 10K load**
   - Reason: No load testing infrastructure available
   - Blocker: Toolchain (requires JMeter setup)
   - Follow-up: STORY-XXX (load testing infrastructure)

2. **E2E test: Full workflow**
   - Reason: E2E framework not yet implemented
   - Blocker: Dependency (STORY-YYY must complete first)
   - Follow-up: Implement after STORY-YYY complete
```

**Expected Result:**
```
Phase 0.9: AC-DoD Traceability Validation

AC Analysis:
  • Total ACs: 1
  • Total requirements: 1

Traceability:
  • AC#1 → 2 DoD items ✓

Traceability Score: 100% ✅

DoD Completion: 60% (3/5 items)

Deferral Documentation:
  • Section exists: YES
  • User approval: 2025-01-21 10:30 UTC ✓
  • Incomplete items: 2
  • Documented deferrals: 2 (100% coverage)

✓ PASS - Traceability validated, deferrals properly documented
```

**QA Proceeds to Phase 1**

---

### Scenario 4: Incomplete DoD WITHOUT Deferrals (Should FAIL - STORY-038 Pattern)

**Test Story:** (Simulating STORY-038 issue)
```markdown
## Acceptance Criteria

### AC#1: Quality Metrics Calculated
**Then** system calculates complexity, duplication, maintainability index

## Definition of Done

### Implementation
- [x] Metrics calculation implemented
- [x] Thresholds validated
- [x] Recommendations generated

### Testing
- [x] Unit test: Complexity calculation
- [x] Integration test: Full workflow
- [ ] Performance test: 10K LOC <30s
- [ ] Edge case: Zero-line files

# NO "Approved Deferrals" section
```

**Expected Result:**
```
Phase 0.9: AC-DoD Traceability Validation

AC Analysis:
  • Total ACs: 1
  • Total requirements: 3 (complexity, duplication, MI)

Traceability:
  • AC#1 → 3 DoD items ✓

Traceability Score: 100% ✅

DoD Completion: 71% (5/7 items)

Deferral Documentation:
  • Section exists: NO ✗
  • Incomplete items: 2
  • Documented deferrals: 0 (0% coverage)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ QA VALIDATION FAILED - Incomplete DoD Without Approval

DoD Completion: 71% (5/7 items complete)
Incomplete Items: 2

Deferral Documentation: MISSING

Incomplete Items Lacking Approval:
  • Performance test: 10K LOC <30s
  • Edge case: Zero-line files

Action Required:
1. Complete all incomplete DoD items, OR

2. Create "Approved Deferrals" section with:
   ## Approved Deferrals

   **User Approval:** {timestamp} UTC
   **Approval Type:** {Design-Phase | Low-Priority | Blocker-Dependent}

   **Deferred Items:**
   1. **Performance test: 10K LOC <30s**
      - Reason: {Why deferred}
      - Blocker: {Dependency | Toolchain | Artifact | ADR}
      - Follow-up: {Story ref or condition}

   2. **Edge case: Zero-line files**
      - Reason: {Why deferred}
      - Blocker: {Type}
      - Follow-up: {Action}

3. Re-run: /qa {STORY_ID}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**QA HALTS - This is the behavior that would have prevented STORY-038 bypass**

---

## Display Template Specification

### PASS Template

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
  {... for all ACs ...}

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

✓ PASS - Traceability validated, story ready for QA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### FAIL Template (Missing Traceability)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Phase 0.9: AC-DoD Traceability Validation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Acceptance Criteria Analysis:
  • Total ACs: {ac_count}
  • Total AC requirements: {ac_req_count}

Traceability Mapping:
  • AC#1 → {coverage} {status}
  • AC#2 → {coverage} {status}
  {... for all ACs, highlighting ✗ FAIL ones ...}

Traceability Score: {score}% ❌ (100% required)

Missing DoD Coverage for AC Requirements:
  • {AC requirement 1 description}
  • {AC requirement 2 description}
  {... list all missing ...}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ QA VALIDATION FAILED - AC-DoD Traceability Insufficient
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Traceability Score: {score}% (100% required)

Missing Coverage: {missing_count} AC requirements have no DoD validation

Action Required:

Option 1: Add DoD Items (Recommended)
  Add to appropriate DoD subsection (Implementation/Quality/Testing/Documentation):

  {FOR each missing requirement}:
  - [ ] {requirement description with measurable criteria}

  Example:
  - [ ] Performance validated: API response <200ms (p95)
  - [ ] Error handling tested for 5 failure scenarios

Option 2: Clarify Existing Coverage
  If DoD items exist but weren't detected (different wording):
    1. Review DoD items for implicit coverage
    2. Update DoD item text to explicitly mention AC requirement
    3. Re-run /qa

  Example:
    Before: "- [x] All tests passing"
    After:  "- [x] All tests passing (AC#2: Error handling validated)"

Option 3: Update AC (If Requirement Invalid)
  If AC requirement is no longer relevant or incorrectly stated:
    1. Edit story file AC section
    2. Remove or revise requirement
    3. Document decision in Implementation Notes
    4. Re-run /qa

After fixing, re-run: /qa {STORY_ID}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### FAIL Template (Undocumented Deferrals)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ QA VALIDATION FAILED - Incomplete DoD Without Approval
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DoD Completion: {completion_pct}% ({dod_checked}/{dod_total} items)

Incomplete Items: {dod_unchecked}

Deferral Documentation: {deferral_status}

{IF no deferral section}:
No "Approved Deferrals" section found. Story has {dod_unchecked} incomplete DoD items without documented user approval.

{IF deferral section exists but incomplete}:
"Approved Deferrals" section exists but only documents {documented_count}/{dod_unchecked} incomplete items.

Undocumented Incomplete Items:
  • {item 1 text}
  • {item 2 text}
  {... for all undocumented items ...}

Action Required:

Option 1: Complete All Items (Preferred)
  Implement all {dod_unchecked} incomplete items:
  {list items with brief implementation guidance}

Option 2: Document Deferrals (If Valid Blockers)
  Add "Approved Deferrals" section to Implementation Notes:

  ## Approved Deferrals

  **User Approval:** {current timestamp} UTC
  **Approval Type:** {Design-Phase | Low-Priority | Blocker-Dependent}

  **Deferred Items:**
  {FOR each incomplete item}:
  1. **{item text}**
     - Reason: {Why this is deferred - be specific}
     - Blocker Type: {Dependency | Toolchain | Artifact | ADR | Low-Priority}
     - Follow-up: {Story reference OR condition for completion}

  **Impact:** {What's complete vs. what's deferred - business context}

  Then re-run: /qa {STORY_ID}

Option 3: Remove Items (If No Longer Relevant)
  If items are obsolete or incorrectly included:
    1. Edit story file DoD section
    2. Remove obsolete items
    3. Document removal decision in Implementation Notes
    4. Re-run /qa

After fixing, re-run: /qa {STORY_ID}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Edge Cases & Handling

### Edge Case 1: AC Requirement Covered by Multiple DoD Items

**Scenario:** AC#1 requires "User authentication with email and password"

**DoD Coverage:**
- Implementation: "Email validation implemented"
- Implementation: "Password hashing implemented (bcrypt)"
- Testing: "Auth integration test passing"

**Handling:** Count as COVERED (3 DoD items collectively validate the requirement)

---

### Edge Case 2: One DoD Item Covers Multiple AC Requirements

**Scenario:** DoD item: "All tests passing (validates AC#1, AC#2, AC#3)"

**AC Coverage:**
- AC#1: Covered by "All tests passing"
- AC#2: Covered by "All tests passing"
- AC#3: Covered by "All tests passing"

**Handling:** Count as COVERED for all 3 ACs (rollup validation)

---

### Edge Case 3: AC Requirement Validated by NFR Metric

**Scenario:** AC#2 requires "Response time <200ms"

**DoD Coverage:** NFRs section states "Performance: <200ms p95 validated"

**Handling:** Search DoD AND NFR sections for coverage (count as COVERED)

---

### Edge Case 4: Design-Phase Story with Implementation Deferred

**Scenario:** STORY-023 pattern (design complete, implementation deferred to STORY-024)

**Expected:**
- AC-DoD traceability: 100% (design requirements have design DoD items)
- DoD completion: 60-80% (implementation items deferred)
- Approved Deferrals: Section exists with STORY-024 reference

**Handling:** PASS (design complete, implementation properly deferred)

---

## Integration with Existing QA Phases

### Phase 0.9 Position Rationale

**Why Between Phase 0 and Phase 1:**

**Phase 0 (Parameter Extraction):**
- Lightweight (<1K tokens)
- Determines STORY_ID and mode
- No file reading beyond story file

**Phase 0.9 (Traceability Validation):**
- Lightweight validation (~2K tokens)
- Reads only story file (already loaded)
- Fast failure if traceability missing
- Prevents expensive validations if story structure invalid

**Phase 1 (Validation Mode Selection):**
- Determines light vs. deep
- Expensive validations begin (build, tests, coverage)

**Benefit:** Fail fast on structural issues before spending tokens on build/test validation

---

### Phase Flow with 0.9 Inserted

```
User runs: /qa STORY-001 deep
  ↓
Phase 0: Extract STORY_ID="STORY-001", mode="deep"
  ↓
Phase 0.9: Validate AC-DoD traceability
  ├─ IF traceability < 100% → HALT (display remediation)
  ├─ IF incomplete DoD without deferrals → HALT (display deferral requirements)
  └─ IF all PASS → Continue
  ↓
Phase 1: Validation mode = deep
  ↓
Phase 2-6: Deep validation (build, test, coverage, security, architecture)
  ↓
Phase 7: Report generation
```

**Token Savings:** If Phase 0.9 catches issue, saves ~50-80K tokens from Phases 2-6 that would execute then fail

---

## Implementation Checklist

### Phase 0.9 Addition to QA Skill

- [ ] Read current devforgeai-qa/SKILL.md structure
- [ ] Identify insertion point (after Phase 0, before Phase 1)
- [ ] Create traceability-validation-algorithm.md reference file
- [ ] Create traceability-report-template.md asset file
- [ ] Insert Phase 0.9 section into SKILL.md (includes algorithm reference, display, quality gate)
- [ ] Update phase numbering (Phase 1 → 2 → 3... may shift if Phase 0.9 affects numbering)
- [ ] Test with all 4 scenarios (perfect, missing coverage, documented deferrals, undocumented)
- [ ] Validate PASS/FAIL behavior matches expectations
- [ ] Document integration in validation-procedures.md

### Reference File Creation

**traceability-validation-algorithm.md Must Include:**
- [ ] Step-by-step algorithm (Steps 1-5 from above)
- [ ] Keyword extraction logic
- [ ] Mapping procedures
- [ ] Edge case handling (4 edge cases documented)
- [ ] Example mappings (STORY-052, STORY-023)
- [ ] Pseudocode for clarity

### Template File Creation

**traceability-report-template.md Must Include:**
- [ ] PASS display template
- [ ] FAIL (traceability) display template
- [ ] FAIL (deferrals) display template
- [ ] Remediation guidance templates (3 options per failure type)
- [ ] Examples for each template type

---

## Success Metrics

**Quantitative:**
- Phase 0.9 catches missing traceability: 100% detection rate
- Phase 0.9 catches undocumented deferrals: 100% detection rate
- False positive rate: <5% (valid stories incorrectly flagged)
- Token savings: ~60K tokens per caught issue (avoid expensive validations)

**Qualitative:**
- Users understand remediation guidance (clear action steps)
- Stories fixed after QA failure (remediation actionable)
- No confusion about quality gate (expectations clear)

---

## Rollback Procedure

**If Phase 0.9 creates false positives:**

### Step 1: Disable Phase 0.9
```
Edit .claude/skills/devforgeai-qa/SKILL.md

Comment out Phase 0.9 section:
<!-- Phase 0.9 disabled due to false positives - investigating -->
<!--
Phase 0.9 content here...
-->

Save changes
```

### Step 2: Document False Positive Pattern
```
Record in devforgeai/RCA/RCA-012/FALSE-POSITIVE-LOG.md:
- Which story triggered false positive
- What was incorrectly flagged
- Why algorithm missed valid coverage
- How to fix algorithm
```

### Step 3: Fix Algorithm
```
Edit traceability-validation-algorithm.md
Add handling for false positive case
Test on previously flagged story
Verify now PASSES correctly
```

### Step 4: Re-Enable Phase 0.9
```
Edit .claude/skills/devforgeai-qa/SKILL.md
Uncomment Phase 0.9
Test with all scenarios again
Verify false positive resolved
```

---

## Related Documents

- **INDEX.md** - RCA-012 navigation
- **REMEDIATION-PLAN.md** - Phase 2 overview
- **IMPLEMENTATION-GUIDE.md** - Step 2.2, 2.3, 2.4 (detailed execution)
- **VALIDATION-PROCEDURES.md** - Test scenarios and validation
- **TESTING-PLAN.md** - End-to-end validation strategy

---

**REC-5 Status:** Ready for Implementation
**Effort:** 2 hours (algorithm + integration + testing)
**Priority:** HIGH (prevents future STORY-038-style bypasses)
**Impact:** Quality gate integrity restored
