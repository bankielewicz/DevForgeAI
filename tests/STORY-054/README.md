# STORY-054 Failing Test Suite

**Comprehensive integration test suite for STORY-054: claude-code-terminal-expert Prompting Guidance Enhancement**

---

## Quick Start

### Run Tests
```bash
bash tests/STORY-054/test-prompting-guidance.sh
```

### Expected Result (RED Phase)
```
Total Tests: 39
Passed: 11
Failed: 28

TEST SUITE FAILED (RED Phase - Expected)
Exit Code: 28
```

---

## Documentation Files

Choose based on your needs:

### For Quick Reference
- **`QUICK-START.md`** (250 lines)
  - One-page overview
  - Test commands
  - Expected output
  - Phase 2 checklist
  - FAQ

### For Detailed Test Breakdown
- **`TEST-SUITE-DOCUMENTATION.md`** (432 lines)
  - Comprehensive test documentation
  - All 39 tests explained
  - Test patterns and helpers
  - Regression testing
  - Success criteria

### For Execution Results
- **`TEST-EXECUTION-RESULTS.md`** (420 lines)
  - Detailed test results
  - Breakdown by AC and feature
  - What's working
  - What needs implementation
  - Phase 2 roadmap

### For Overview
- **`GENERATION-SUMMARY.md`** (501 lines)
  - Test generation summary
  - By-the-numbers breakdown
  - TDD workflow
  - Key metrics
  - Support references

---

## Test Suite Components

### Test Script: `test-prompting-guidance.sh` (579 lines)
Main test suite with 39 integration tests

**Structure:**
- Helper functions (5 reusable assertion patterns)
- AC#1 tests (4 tests - Section added)
- AC#2 tests (6 tests - Cross-references)
- AC#3 tests (7 tests - Examples)
- AC#4 tests (5 tests - Principle)
- AC#5 tests (7 tests - No breaking changes)
- Technical Specification tests (4 tests)
- Business Rules tests (3 tests)
- NFR tests (3 tests)
- Summary and exit handling

**Test Pattern:** AAA (Arrange, Act, Assert)

### Test Runner: `run_all_tests.sh` (41 lines)
Orchestrates test execution and handles exit codes

---

## Test Results Summary

```
ACCEPTANCE CRITERIA TESTS (29 total)

AC#1: Section Added                    4 tests  [██░░░░░░░░]  25% PASS
AC#2: Cross-References                 6 tests  [██░░░░░░░░]   0% PASS
AC#3: Examples (5-10 scenarios)         7 tests  [██░░░░░░░░]   0% PASS
AC#4: "Ask, Don't Assume" Principle     5 tests  [██░░░░░░░░]   0% PASS
AC#5: No Breaking Changes              7 tests  [██████████] 100% PASS ✅

SUPPLEMENTARY TESTS (10 total)

Technical Specification (4 tests)      [██░░░░░░░░]   0% PASS
Business Rules (3 tests)               [██████░░░░]  67% PASS
Non-Functional Requirements (3 tests)  [██████░░░░]  33% PASS

────────────────────────────────────────────────────────────────

TOTAL: 39 tests                        [███░░░░░░░░]  28% PASS
       ✅ 11 Passing (backward compatibility)
       ❌ 28 Failing (expected for RED phase)
```

---

## What's Passing ✅ (AC#5 - Backward Compatibility)

All existing skill functionality preserved:
- YAML frontmatter intact
- All 8 core features documented
- Progressive disclosure mechanism functional
- Self-updating capability preserved
- Reference file loading works
- Integration patterns unchanged

---

## What's Failing ❌ (Features Not Yet Implemented)

### AC#1: Section Not Added (3 tests failing)
- Need: `## How DevForgeAI Skills Work with User Input` section
- Size: 100-200 lines
- Position: After "Core Claude Code Terminal Features"

### AC#2: Cross-References Not Added (6 tests failing)
- Need: Link to effective-prompting-guide.md
- Need: Link to user-input-guidance.md
- Each: With 15-30 word description

### AC#3: Examples Not Added (7 tests failing)
- Need: 5-10 paired examples (❌ ineffective / ✅ effective)
- Coverage: Feature requests, story creation, error reporting, tech decisions, feedback

### AC#4: Principle Not Explained (5 tests failing)
- Need: "Ask, Don't Assume" subsection
- Must explain: When, What NOT, Why, How it integrates

### Format & Structure (4 tests failing)
- Heading level 2 for section
- Heading level 3 for subsections
- Markdown link syntax for references
- ❌/✅ pattern for examples

---

## How to Proceed

### Phase 1: RED (CURRENT) ✅
```bash
# 1. Review failing tests
bash tests/STORY-054/test-prompting-guidance.sh

# 2. Read QUICK-START.md for implementation checklist
cat tests/STORY-054/QUICK-START.md

# 3. Understand what needs to be added
cat tests/STORY-054/TEST-SUITE-DOCUMENTATION.md | head -100
```

### Phase 2: GREEN (IMPLEMENTATION)
```bash
# 1. Edit the skill file
nano ./.claude/skills/claude-code-terminal-expert/SKILL.md

# 2. Add:
#    - New section "How DevForgeAI Skills Work with User Input"
#    - Cross-references to guidance documents
#    - 5-10 paired ❌/✅ examples
#    - "Ask, Don't Assume" principle explanation

# 3. Run tests
bash tests/STORY-054/test-prompting-guidance.sh

# 4. Expected result: All 39 tests PASS
```

### Phase 3: REFACTOR (QUALITY)
```bash
# 1. Code review and optimization
# 2. Token overhead validation (≤1,000 tokens)
# 3. Terminology consistency check
# 4. Integration testing
```

---

## Key Metrics

| Metric | Value |
|--------|-------|
| Total Tests | 39 |
| Test Script Size | 579 lines |
| Test Execution Time | <1 second |
| Passing Tests (RED) | 11 (28%) |
| Failing Tests (RED) | 28 (72%) |
| AC Coverage | 100% (5/5 ACs) |
| Documentation | 1,600+ lines |
| External Dependencies | 0 (pure bash) |

---

## File Locations

```
tests/STORY-054/
├── README.md                          (This file)
├── test-prompting-guidance.sh         (Main test suite - 579 lines)
├── run_all_tests.sh                   (Test runner - 41 lines)
├── QUICK-START.md                     (Quick reference - 250 lines)
├── TEST-SUITE-DOCUMENTATION.md        (Full docs - 432 lines)
├── TEST-EXECUTION-RESULTS.md          (Results - 420 lines)
├── GENERATION-SUMMARY.md              (Overview - 501 lines)
└── test-results.txt                   (Auto-generated results)
```

---

## Test Pattern Reference

### Pattern 1: File Existence
```bash
assert_file_exists "$file" "description"
```

### Pattern 2: Grep Match
```bash
assert_grep_match "pattern" "$file" "description"
```

### Pattern 3: Count Range
```bash
assert_grep_count "pattern" "$file" 5 10 "description"
# Validates 5-10 occurrences
```

### Pattern 4: Position Validation
```bash
assert_line_position "pattern" "$file" 300 "description"
# Validates pattern appears before line 300
```

---

## Execution Examples

### Run Full Test Suite
```bash
bash tests/STORY-054/test-prompting-guidance.sh
```
Exit Code: 28 (28 failed tests)

### Save Results to File
```bash
bash tests/STORY-054/test-prompting-guidance.sh > test-output.log 2>&1
```

### View Results File
```bash
cat tests/STORY-054/test-results.txt
```

### Count Failures
```bash
grep "FAIL" tests/STORY-054/test-results.txt | wc -l
# Result: 28
```

### See Only Passing Tests
```bash
grep "PASS" tests/STORY-054/test-results.txt
```

---

## Success Criteria

### RED Phase (Current) ✅
- ✅ Tests written and executable
- ✅ Tests correctly fail (28/39 failing)
- ✅ Tests validate all 5 ACs
- ✅ Clear error messages
- ✅ Backward compatibility verified
- ✅ No external dependencies

### GREEN Phase (Next)
- ⏳ All 39 tests PASSING
- ⏳ Section added to SKILL.md
- ⏳ Cross-references present
- ⏳ Examples included (5-10 pairs)
- ⏳ Principle explained (when/what/why/how)
- ⏳ Exit code: 0

### REFACTOR Phase (Final)
- ⏳ Code quality review
- ⏳ Token overhead ≤1,000
- ⏳ Terminology consistency
- ⏳ Integration validated

---

## Troubleshooting

### Tests Won't Execute
```bash
# Ensure script is executable
chmod +x tests/STORY-054/test-prompting-guidance.sh

# Run with bash explicitly
bash tests/STORY-054/test-prompting-guidance.sh
```

### Wrong Test Count
```bash
# Verify file exists
ls -l ./.claude/skills/claude-code-terminal-expert/SKILL.md

# Count test headers
grep -c "^print_test_header" tests/STORY-054/test-prompting-guidance.sh
# Should show: 39
```

### Tests Run Slower Than Expected
- Verify disk I/O is not maxed
- Check for background processes
- Normal execution: <1 second

---

## Related Documentation

### Story File
→ `devforgeai/specs/Stories/STORY-054-claude-code-terminal-expert-enhancement.story.md`

### Skill File (Under Test)
→ `./.claude/skills/claude-code-terminal-expert/SKILL.md`

### Related Stories
- STORY-052: User-Facing Prompting Guide
- STORY-053: Framework-Internal Guidance Reference

---

## Summary

This test suite validates STORY-054 requirements using integration testing patterns. All 39 tests are currently failing (RED phase), which is correct - the feature hasn't been implemented yet.

**Next Step:** Implement the feature in SKILL.md, then run tests for GREEN phase validation.

---

**Test Suite Version:** 1.0
**TDD Phase:** RED
**Status:** ✅ Complete and validated
**Exit Code:** 28 (28 failing tests)
**Documentation:** Comprehensive
**Dependencies:** None
**Generated:** November 21, 2025

For detailed information, see:
- QUICK-START.md - 1-page reference
- TEST-SUITE-DOCUMENTATION.md - Comprehensive guide
- TEST-EXECUTION-RESULTS.md - Detailed analysis
- GENERATION-SUMMARY.md - Overview
