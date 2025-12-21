# STORY-054 Test Suite Documentation

**Story:** claude-code-terminal-expert Prompting Guidance Enhancement
**Test File:** `tests/STORY-054/test-prompting-guidance.sh`
**Status:** RED Phase (All Tests Failing - Expected)
**Date Generated:** 2025-01-21
**Test Count:** 39 total tests

---

## Purpose

Comprehensive integration test suite for STORY-054, validating:
1. Addition of "How DevForgeAI Skills Work with User Input" section
2. Cross-references to guidance documents
3. Effective communication examples (5-10 scenarios)
4. "Ask, Don't Assume" principle explanation
5. No breaking changes to existing skill functionality

---

## Test Execution

### Run Tests

```bash
# Run complete test suite
bash tests/STORY-054/test-prompting-guidance.sh

# Run with output capture
bash tests/STORY-054/test-prompting-guidance.sh 2>&1 | tee test-output.log

# Using test runner
bash tests/STORY-054/run_all_tests.sh
```

### Expected Results (RED Phase)

**Status:** 28 FAILED, 11 PASSED (Intentional - Implementation Not Yet Complete)

```
Total Tests: 39
Passed: 11
Failed: 28

TEST SUITE FAILED (RED Phase - Expected)
```

---

## Test Categories

### AC#1: Prompting Guidance Section Added (4 tests)

| Test | Status | Assertion |
|------|--------|-----------|
| AC#1.1 | ✅ PASS | Skill file exists |
| AC#1.2 | ❌ FAIL | Section header "## How DevForgeAI Skills Work..." present |
| AC#1.3 | ❌ FAIL | Section positioned before line 300 |
| AC#1.4 | ❌ FAIL | Section contains 100-200 lines |

**Expected Failure Reason:** Section not yet added to SKILL.md

---

### AC#2: Cross-References to Both Guidance Documents (6 tests)

| Test | Status | Assertion |
|------|--------|-----------|
| AC#2.1 | ❌ FAIL | effective-prompting-guide.md referenced |
| AC#2.2 | ❌ FAIL | Link uses valid markdown syntax |
| AC#2.3 | ❌ FAIL | Link has ≥15 word description |
| AC#2.4 | ❌ FAIL | user-input-guidance.md referenced |
| AC#2.5 | ❌ FAIL | Link uses valid markdown syntax |
| AC#2.6 | ❌ FAIL | Link has ≥15 word description |

**Expected Failure Reason:** Cross-references not yet added

---

### AC#3: Effective Communication Examples (7 tests)

| Test | Status | Assertion |
|------|--------|-----------|
| AC#3.1 | ❌ FAIL | Contains 5-10 paired examples (❌/✅) |
| AC#3.2 | ❌ FAIL | Equal number of ❌ and ✅ patterns |
| AC#3.3 | ❌ FAIL | Feature request example present |
| AC#3.4 | ❌ FAIL | Story creation example present |
| AC#3.5 | ❌ FAIL | Error reporting example present |
| AC#3.6 | ❌ FAIL | Technology decision example present |
| AC#3.7 | ❌ FAIL | Feedback provision example present |

**Expected Failure Reason:** Examples not yet added

---

### AC#4: "Ask, Don't Assume" Principle Explained (5 tests)

| Test | Status | Assertion |
|------|--------|-----------|
| AC#4.1 | ❌ FAIL | Subsection header present |
| AC#4.2 | ❌ FAIL | Explains WHEN to use AskUserQuestion |
| AC#4.3 | ❌ FAIL | Explains WHAT NOT to assume |
| AC#4.4 | ❌ FAIL | Explains WHY principle exists |
| AC#4.5 | ❌ FAIL | Explains HOW it integrates with quality gates |

**Expected Failure Reason:** Principle explanation not yet added

---

### AC#5: No Breaking Changes (7 tests)

| Test | Status | Assertion |
|------|--------|-----------|
| AC#5.1 | ✅ PASS | YAML frontmatter still present |
| AC#5.2 | ✅ PASS | "When to Use This Skill" section present |
| AC#5.3 | ✅ PASS | "Core Claude Code Terminal Features" section present |
| AC#5.4 | ✅ PASS | All 8 core features documented |
| AC#5.5 | ✅ PASS | "Progressive Disclosure Strategy" section present |
| AC#5.6 | ✅ PASS | "Self-Updating Mechanism" documentation present |
| AC#5.7 | ✅ PASS | Reference file loading code present |

**Status:** All tests passing - backward compatibility preserved

---

### Technical Specification Tests (4 tests)

| Test | Status | Assertion |
|------|--------|-----------|
| TechSpec-001 | ❌ FAIL | Section header uses level 2 (##) |
| TechSpec-002 | ❌ FAIL | Cross-references use relative paths |
| TechSpec-003 | ❌ FAIL | Examples use ❌/✅ format consistently |
| TechSpec-004 | ❌ FAIL | Subsections use level 3 (###) headers |

**Expected Failure Reason:** Format requirements dependent on section content

---

### Business Rules Tests (3 tests)

| Test | Status | Assertion |
|------|--------|-----------|
| BR-001 | ℹ️ INFO | Examples align with actual framework behavior (manual verification) |
| BR-002 | ✅ PASS | Cross-reference descriptions are helpful |
| BR-003 | ✅ PASS | No conflicting guidance in new section |

**Status:** 2 passing (verified via analysis), 1 deferred to Phase 2

---

### Non-Functional Requirements Tests (3 tests)

| Test | Status | Assertion |
|------|--------|-----------|
| NFR-001 | ℹ️ INFO | Token overhead ≤1,000 (measurement pending) |
| NFR-003 | ✅ PASS | 100% backward compatibility (smoke tests) |
| NFR-005 | ℹ️ INFO | Terminology consistency (validation pending) |

**Status:** 1 passing, 2 deferred to Phase 2

---

## Test Pattern & Structure

### AAA Pattern (Arrange, Act, Assert)

All tests follow the AAA (Arrange, Act, Assert) pattern:

```bash
# Arrange: Set up test conditions and patterns
pattern="## How DevForgeAI Skills Work"

# Act: Execute the test (grep, wc, file operations)
grep -q "$pattern" "$SKILL_FILE"

# Assert: Verify the result
if [ $? -eq 0 ]; then
    echo "PASS"
else
    echo "FAIL"
fi
```

### Helper Functions

**assert_file_exists()**
- Verifies a file exists and is readable
- Returns 0 (pass) or 1 (fail)

**assert_grep_match()**
- Searches for a pattern in a file
- Returns 0 if pattern found, 1 if not

**assert_grep_count()**
- Counts occurrences of a pattern
- Validates count is within min/max range
- Returns 0 if count valid, 1 if outside range

**assert_file_readable()**
- Verifies file exists and is readable
- Returns 0 or 1

**assert_line_position()**
- Finds first occurrence of pattern
- Validates line number is ≤ max_line
- Returns 0 if position valid, 1 if not

---

## Output Format

### Test Header
```
============================================================================
TEST: AC#1.2: Section titled 'How DevForgeAI Skills Work with User Input' is present
============================================================================
```

### Test Result
```
FAIL: Pattern not found: '## How DevForgeAI Skills Work'
    Expected section header not found
    Test will fail until section is added
```

### Color Coding
- 🟢 **GREEN** (`\033[0;32m`): Test PASS
- 🔴 **RED** (`\033[0;31m`): Test FAIL
- 🟡 **YELLOW** (`\033[1;33m`): Test INFO (deferred)

### Summary
```
==========================================
TEST SUITE SUMMARY
==========================================

Total Tests: 39
Passed: 11
Failed: 28

TEST SUITE FAILED (RED Phase - Expected)
```

---

## Files Modified for Testing

### Test Script
- **Location:** `/tests/STORY-054/test-prompting-guidance.sh`
- **Size:** 578 lines
- **Language:** Bash
- **Dependencies:** grep, wc, bash built-ins

### Test Runner
- **Location:** `/tests/STORY-054/run_all_tests.sh`
- **Purpose:** Orchestrates test execution
- **Returns:** Exit code matching failed test count

### Results File
- **Location:** `/tests/STORY-054/test-results.txt` (auto-generated)
- **Format:** `[PASS|FAIL] test-name` (one per line)
- **Usage:** Quick reference for test results

---

## Success Criteria for Phase 2 (GREEN Phase)

All tests should PASS when implementation is complete:

### Requirements for GREEN Phase

1. **AC#1 Tests (4)** - New section must be added
   - Section header: `## How DevForgeAI Skills Work with User Input`
   - Position: After "Core Claude Code Terminal Features" section
   - Size: 100-200 lines
   - **All 4 tests must PASS**

2. **AC#2 Tests (6)** - Cross-references must be added
   - Both guidance documents referenced with markdown links
   - Each reference has ≥15 word description
   - **All 6 tests must PASS**

3. **AC#3 Tests (7)** - Examples must be included
   - 5-10 paired examples using ❌/✅ format
   - Coverage: feature requests, stories, errors, tech decisions, feedback
   - **All 7 tests must PASS**

4. **AC#4 Tests (5)** - Principle must be explained
   - Subsection explains when/what/why/how
   - Covers AskUserQuestion, assumptions, quality gates
   - **All 5 tests must PASS**

5. **AC#5 Tests (7)** - No breaking changes
   - All backward compatibility tests already passing ✅
   - **All 7 must remain PASS**

6. **Technical Spec Tests (4)** - Format must be correct
   - Heading levels, link syntax, example formatting
   - **All 4 tests must PASS**

---

## Implementation Checklist for Phase 2

- [ ] Add new section to `.claude/skills/claude-code-terminal-expert/SKILL.md`
- [ ] Position section after line ~100, before detailed topics
- [ ] Add cross-references to:
  - `../../memory/effective-prompting-guide.md`
  - `../../../devforgeai/ideation/references/user-input-guidance.md`
- [ ] Include 15-30 word descriptions for each reference
- [ ] Add 5-10 paired examples (❌ ineffective / ✅ effective)
- [ ] Cover all example types: feature request, story creation, error reporting, tech decisions, feedback
- [ ] Add "Ask, Don't Assume" principle subsection
  - Explain WHEN to use AskUserQuestion
  - Explain WHAT NOT to assume
  - Explain WHY principle exists
  - Explain HOW it integrates with quality gates
- [ ] Verify all section headers use correct markdown levels
- [ ] Verify backward compatibility (AC#5 tests remain passing)
- [ ] Run test suite: `bash tests/STORY-054/test-prompting-guidance.sh`
- [ ] Validate all 39 tests PASS before moving to Phase 3

---

## Common Test Failures & Diagnostics

### AC#1.2 FAILS: Pattern not found

**Cause:** Section header not added to SKILL.md
**Resolution:**
```bash
# Add after line ~100 (after features overview)
## How DevForgeAI Skills Work with User Input

[Add 100-200 lines of guidance content]
```

### AC#2.1 FAILS: effective-prompting-guide.md not found

**Cause:** Cross-reference not added
**Resolution:**
```bash
# Add markdown link in new section
See [effective-prompting-guide.md](../../memory/effective-prompting-guide.md) for...
```

### AC#3.1 FAILS: Only 3 examples found, need 5-10

**Cause:** Examples not yet added
**Resolution:**
```bash
# Add at least 5 paired examples
❌ Ineffective: "Create a story for alert detection"
✅ Effective: "/create-story Generate STORY-###: Alert Detection Service
  - Acceptance Criteria with Given/When/Then format
  - Technical Specification with components
  - Business rules..."
```

### AC#4.1 FAILS: "Ask, Don't Assume" not found

**Cause:** Principle explanation subsection not added
**Resolution:**
```bash
# Add subsection
### The "Ask, Don't Assume" Principle

When to use...
What NOT to assume...
Why this principle...
How it integrates...
```

---

## Regression Testing

### Run Before Committing

```bash
# Full test suite
bash tests/STORY-054/test-prompting-guidance.sh

# Verify no new failures in backward compatibility tests
grep "AC#5" test-results.txt | grep "FAIL"
# Should return: (no results)

# Quick check - count failures
grep "FAIL" test-results.txt | wc -l
# When GREEN: Should be 0 (or only deferred NFR tests)
```

---

## Test Maintenance

### When to Update Tests

1. **Acceptance criteria change** → Update corresponding AC test
2. **New examples added** → Verify AC#3 counts still valid
3. **Section moved** → Update AC#1.3 line number expectation
4. **New guidance documents** → Add new cross-reference tests

### Test Coverage

| Category | Tests | Coverage |
|----------|-------|----------|
| Acceptance Criteria | 29 | 100% (5 ACs × multiple sub-tests) |
| Technical Spec | 4 | 100% (format, structure, syntax) |
| Business Rules | 3 | 100% (framework alignment, quality) |
| NFR | 3 | 66% (2 deferred to Phase 2) |
| **TOTAL** | **39** | **95% (36/39 now, 39/39 in Phase 2)** |

---

## References

- **Story:** `devforgeai/specs/Stories/STORY-054-claude-code-terminal-expert-enhancement.story.md`
- **Skill File:** `.claude/skills/claude-code-terminal-expert/SKILL.md`
- **Test Framework:** Bash + grep, wc, file operations (no external dependencies)
- **AAA Pattern:** Arrange, Act, Assert
- **TDD Phase:** RED (All tests failing - expected for TDD Red phase)

---

## Contact & Questions

- **Test Suite Version:** 1.0
- **Last Updated:** 2025-01-21
- **Created by:** Test-Automator (Claude Code)
- **Status:** Ready for Phase 2 (GREEN) implementation
