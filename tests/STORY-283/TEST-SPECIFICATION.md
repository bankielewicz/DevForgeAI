# Test Specification Document - STORY-283

**Story:** STORY-283 - Story Creation Automation for AC-TechSpec Traceability
**Implementation Type:** Slash Command / Skill modification (.md files)
**Target File:** `.claude/skills/devforgeai-story-creation/references/technical-specification-creation.md`
**Test Type:** Structural Validation (non-executable specification tests)
**TDD Phase:** RED (tests defined, implementation pending)

---

## Test Categories

| Category | Test Count | Status |
|----------|------------|--------|
| AC#1: Auto-Generation | 4 tests | RED |
| AC#2: Cross-Reference | 3 tests | RED |
| AC#3: Warning Generation | 3 tests | RED |
| AC#4: User Override | 2 tests | RED |
| **Total** | **12 tests** | **RED** |

---

## AC#1: Auto-Generation During Story Creation

### Test 1.1: test_ac1_keyword_extraction_section_exists

**Scenario:** Technical specification contains AC keyword extraction logic
**Given:** The technical-specification-creation.md file
**When:** Searching for keyword extraction patterns
**Then:** Should find section documenting AC keyword analysis

**Validation Pattern:**
```bash
grep -qE "(keyword|extract|AC|acceptance.criteria).*(analysis|extract|parse)" \
  ".claude/skills/devforgeai-story-creation/references/technical-specification-creation.md"
```

**Expected:** Pattern found (exit code 0)
**Current:** FAIL (no auto-generation logic exists)

---

### Test 1.2: test_ac1_implements_ac_auto_population

**Scenario:** COMP requirements get implements_ac field populated automatically
**Given:** Story being created with COMP requirements
**When:** Story creation generates Technical Specification
**Then:** Each COMP should have implements_ac array populated

**Validation Pattern:**
```bash
grep -qE "implements_ac.*auto|auto.*implements_ac|populate.*implements_ac" \
  ".claude/skills/devforgeai-story-creation/references/technical-specification-creation.md"
```

**Expected:** Auto-population logic documented
**Current:** FAIL (implements_ac requires manual entry)

---

### Test 1.3: test_ac1_semantic_analysis_algorithm

**Scenario:** Semantic analysis matches COMP descriptions to AC keywords
**Given:** COMP with description text
**When:** Traceability generator runs
**Then:** Should use semantic matching to find related ACs

**Validation Pattern:**
```bash
grep -qE "(semantic|match|similarity).*(AC|acceptance|criteria)" \
  ".claude/skills/devforgeai-story-creation/references/technical-specification-creation.md"
```

**Expected:** Semantic matching algorithm documented
**Current:** FAIL (no semantic matching exists)

---

### Test 1.4: test_ac1_svc001_svc002_implementation

**Scenario:** SVC-001 and SVC-002 requirements implemented
**Given:** Technical specification with SVC-001 (keyword extraction) and SVC-002 (matching)
**When:** Checking for implementation hooks
**Then:** Should find both services referenced

**Validation Checks:**
- [ ] SVC-001: AC keyword extraction function
- [ ] SVC-002: COMP-to-AC matching logic

**Expected:** Both services implemented in workflow
**Current:** FAIL (services not implemented)

---

## AC#2: Cross-Reference with AC Section

### Test 2.1: test_ac2_valid_ac_id_validation

**Scenario:** Generated implements_ac links are validated against AC section
**Given:** Generated implements_ac array with AC IDs
**When:** Cross-reference validation runs
**Then:** Should verify each AC ID exists in story AC section

**Validation Pattern:**
```bash
grep -qE "(valid|verify|check).*(AC.*ID|implements_ac|cross-reference)" \
  ".claude/skills/devforgeai-story-creation/references/technical-specification-creation.md"
```

**Expected:** Cross-reference validation logic present
**Current:** FAIL (no validation exists)

---

### Test 2.2: test_ac2_invalid_ac_id_rejection

**Scenario:** Invalid AC IDs are rejected
**Given:** implements_ac contains "AC#99" (non-existent)
**When:** Validation runs
**Then:** Should reject or warn about invalid ID

**Validation Pattern:**
```bash
grep -qE "(invalid|reject|error).*(AC.*ID|implements_ac)" \
  ".claude/skills/devforgeai-story-creation/references/technical-specification-creation.md"
```

**Expected:** Invalid ID handling documented
**Current:** FAIL (no rejection logic)

---

### Test 2.3: test_ac2_svc003_implementation

**Scenario:** SVC-003 validates links against AC section
**Given:** Technical specification with SVC-003 requirement
**When:** Checking implementation
**Then:** Should find link validation logic

**Validation Check:**
- [ ] SVC-003: Validation logic that parses AC section and verifies IDs

**Expected:** Validation function implemented
**Current:** FAIL (SVC-003 not implemented)

---

## AC#3: Warning for Unlinked COMPs

### Test 3.1: test_ac3_unlinked_comp_detection

**Scenario:** COMPs without implements_ac are detected
**Given:** Story generation completes
**When:** COMP has no implements_ac or empty array
**Then:** Should flag COMP as unlinked

**Validation Pattern:**
```bash
grep -qE "(unlinked|empty|missing).*(implements_ac|traceability)" \
  ".claude/skills/devforgeai-story-creation/references/technical-specification-creation.md"
```

**Expected:** Unlinked detection logic present
**Current:** FAIL (no detection logic)

---

### Test 3.2: test_ac3_warning_message_format

**Scenario:** Warning message follows required format
**Given:** COMP-XXX has no implements_ac
**When:** Warning is generated
**Then:** Should display: "COMP-XXX has no AC traceability - consider adding implements_ac"

**Validation Pattern:**
```bash
grep -qE "COMP-.*has no AC traceability.*consider adding implements_ac" \
  ".claude/skills/devforgeai-story-creation/references/technical-specification-creation.md"
```

**Expected:** Exact warning message format in code
**Current:** FAIL (warning message not defined)

---

### Test 3.3: test_ac3_svc004_implementation

**Scenario:** SVC-004 generates warnings for unlinked COMPs
**Given:** Technical specification with SVC-004 requirement
**When:** Checking implementation
**Then:** Should find warning generation logic

**Validation Check:**
- [ ] SVC-004: Warning generation for unlinked COMPs
- [ ] Warning displayed to user during story creation

**Expected:** Warning generation implemented
**Current:** FAIL (SVC-004 not implemented)

---

## AC#4: User Override Option

### Test 4.1: test_ac4_file_format_editable

**Scenario:** Generated story file is standard editable markdown
**Given:** Auto-generated implements_ac links
**When:** User wants to modify links
**Then:** File format should be standard YAML/markdown (no binary lock)

**Validation Pattern:**
```bash
# Verify generated story files are plain text markdown
file devforgeai/specs/Stories/*.story.md | grep -q "text"
```

**Expected:** All story files are text format
**Current:** PASS (stories are already markdown - AC#4 satisfied by design)

---

### Test 4.2: test_ac4_no_readonly_lock

**Scenario:** implements_ac field has no read-only lock
**Given:** Story file with implements_ac array
**When:** User edits implements_ac manually
**Then:** No validation should block manual changes

**Validation Pattern:**
```bash
# Check for absence of lock/readonly patterns on implements_ac
! grep -qE "(readonly|locked|immutable).*implements_ac" \
  ".claude/skills/devforgeai-story-creation/references/technical-specification-creation.md"
```

**Expected:** No lock mechanism present
**Current:** PASS (no lock exists - AC#4 satisfied by design)

---

## Business Rules Tests

### Test BR-001: Best-Effort Generation

**Scenario:** Uncertain cases result in empty implements_ac
**Given:** COMP description that doesn't clearly match any AC
**When:** Auto-generation runs with low confidence
**Then:** implements_ac should be empty (not forced match)

**Validation Pattern:**
```bash
grep -qE "(uncertain|low.confidence|best.effort).*empty|empty.*(uncertain|low)" \
  ".claude/skills/devforgeai-story-creation/references/technical-specification-creation.md"
```

**Expected:** Best-effort behavior documented
**Current:** FAIL (behavior not documented)

---

### Test BR-002: User Override Preserved

**Scenario:** User manual edits are preserved
**Given:** User modifies implements_ac manually
**When:** Story is re-processed
**Then:** Manual changes should not be overwritten

**Validation Pattern:**
```bash
grep -qE "(preserve|maintain|respect).*(manual|user|override)" \
  ".claude/skills/devforgeai-story-creation/references/technical-specification-creation.md"
```

**Expected:** Override preservation documented
**Current:** FAIL (preservation not documented)

---

## Test Execution Summary

```
Total Tests: 14
Passing: 2 (AC#4 tests - satisfied by design)
Failing: 12 (implementation pending)
Coverage: 14.3%
```

---

## Implementation Checklist for GREEN Phase

To move tests from RED to GREEN, implement in technical-specification-creation.md:

- [ ] **Section: AC Keyword Extraction** (AC#1, SVC-001)
  - Parse AC section for keywords
  - Extract key phrases from Given/When/Then

- [ ] **Section: COMP-to-AC Matching** (AC#1, SVC-002)
  - Semantic similarity algorithm
  - Match COMP descriptions to AC keywords
  - Confidence threshold (high confidence only)

- [ ] **Section: Link Validation** (AC#2, SVC-003)
  - Cross-reference AC IDs
  - Reject invalid AC references
  - Validate format (AC#N pattern)

- [ ] **Section: Unlinked COMP Warning** (AC#3, SVC-004)
  - Detect empty implements_ac
  - Generate warning message
  - Display during story creation

- [ ] **Section: Best-Effort Behavior** (BR-001)
  - Document uncertain case handling
  - Empty implements_ac for low confidence

- [ ] **Section: Override Preservation** (BR-002)
  - Document user override capability
  - No re-processing of manual changes

---

## Phase Completion Status

| Phase | Status | Evidence |
|-------|--------|----------|
| RED (Test-First) | COMPLETE | 14 tests defined, 12 failing |
| GREEN (Implementation) | PENDING | Implementation not started |
| REFACTOR | PENDING | N/A |

**TDD Iteration:** 1/5
**Date:** 2026-01-19

---

## References

- **Story File:** `devforgeai/specs/Stories/STORY-283-story-creation-traceability-automation.story.md`
- **Target File:** `.claude/skills/devforgeai-story-creation/references/technical-specification-creation.md`
- **Schema Reference:** `devforgeai/specs/STRUCTURED-FORMAT-SPECIFICATION.md`
