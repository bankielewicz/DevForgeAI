# STORY-054 Test Suite - Quick Start Guide

## Run Tests

```bash
# Execute test suite
bash tests/STORY-054/test-prompting-guidance.sh

# Save results to file
bash tests/STORY-054/test-prompting-guidance.sh > test-results.log 2>&1
```

## Expected Output (RED Phase)

```
==========================================
STORY-054 Test Suite (RED Phase)
==========================================
File: ./.claude/skills/claude-code-terminal-expert/SKILL.md
Timestamp: Fri Nov 21 18:56:19 UTC 2025

[... 39 individual test results ...]

==========================================
TEST SUITE SUMMARY
==========================================

Total Tests: 39
Passed: 11
Failed: 28

TEST SUITE FAILED (RED Phase - Expected)

Failed tests indicate incomplete implementation:
  - AC#1: Section not yet added
  - AC#2: Cross-references not yet added
  - AC#3: Examples not yet added
  - AC#4: Principle explanation not yet added
  - NFR-001: Token measurement pending
  - NFR-005: Terminology validation pending

Next steps (Phase 2 - GREEN):
  1. Add 'How DevForgeAI Skills Work with User Input' section
  2. Add cross-references to guidance documents
  3. Add 5-10 paired examples (❌/✅ pattern)
  4. Add 'Ask, Don't Assume' principle explanation
  5. Run this test suite again - all tests should PASS
```

## Test Summary

| Phase | Status | Count | Details |
|-------|--------|-------|---------|
| **RED** (Current) | FAILING | 28 of 39 | Implementation not yet started |
| **GREEN** (Phase 2) | PASSING | 39 of 39 | After implementation complete |

## Test Distribution

```
Acceptance Criteria Tests:  29 tests
├─ AC#1: Section Added         4 tests (1 PASS, 3 FAIL)
├─ AC#2: Cross-References      6 tests (0 PASS, 6 FAIL)
├─ AC#3: Examples              7 tests (0 PASS, 7 FAIL)
├─ AC#4: Principle             5 tests (0 PASS, 5 FAIL)
└─ AC#5: No Breaking Changes   7 tests (7 PASS, 0 FAIL) ✅

Technical Spec Tests:           4 tests (0 PASS, 4 FAIL)
Business Rules Tests:           3 tests (2 PASS, 1 INFO)
Non-Functional Req Tests:       3 tests (1 PASS, 2 INFO)

TOTAL:                         39 tests (11 PASS, 28 FAIL)
```

## File Locations

| File | Purpose |
|------|---------|
| `tests/STORY-054/test-prompting-guidance.sh` | Main test suite (578 lines) |
| `tests/STORY-054/run_all_tests.sh` | Test runner script |
| `tests/STORY-054/TEST-SUITE-DOCUMENTATION.md` | Comprehensive documentation |
| `tests/STORY-054/QUICK-START.md` | This file |
| `./.claude/skills/claude-code-terminal-expert/SKILL.md` | File under test |

## What Tests Validate

### Acceptance Criteria Tests ✅

1. **AC#1: Section Added** (4 tests)
   - ✅ File exists
   - ❌ Section header present
   - ❌ Section positioned correctly
   - ❌ Section size 100-200 lines

2. **AC#2: Cross-References** (6 tests)
   - ❌ effective-prompting-guide.md linked
   - ❌ user-input-guidance.md linked
   - ❌ Links have descriptions (≥15 words)

3. **AC#3: Examples** (7 tests)
   - ❌ 5-10 paired examples (❌/✅)
   - ❌ Feature request example
   - ❌ Story creation example
   - ❌ Error reporting example
   - ❌ Technology decision example
   - ❌ Feedback provision example

4. **AC#4: Principle Explained** (5 tests)
   - ❌ "Ask, Don't Assume" subsection
   - ❌ WHEN guidance
   - ❌ WHAT NOT guidance
   - ❌ WHY rationale
   - ❌ HOW integration

5. **AC#5: No Breaking Changes** (7 tests)
   - ✅ YAML frontmatter preserved
   - ✅ Existing sections intact
   - ✅ Core features documented
   - ✅ Progressive disclosure works
   - ✅ Reference file loading works

## Phase 2 Implementation Checklist

When implementing the feature, ensure these items are added:

### Required Additions to SKILL.md

- [ ] Section header: `## How DevForgeAI Skills Work with User Input`
- [ ] Position: After "Core Claude Code Terminal Features" section
- [ ] Content: 100-200 lines covering:
  - [ ] Cross-reference to effective-prompting-guide.md (15-30 word description)
  - [ ] Cross-reference to user-input-guidance.md (15-30 word description)
  - [ ] 5-10 paired examples (❌ ineffective vs ✅ effective)
  - [ ] "Ask, Don't Assume" principle subsection with:
    - [ ] WHEN to use AskUserQuestion
    - [ ] WHAT NOT to assume
    - [ ] WHY principle exists
    - [ ] HOW it integrates with quality gates

### Verification After Implementation

```bash
# 1. Run test suite
bash tests/STORY-054/test-prompting-guidance.sh

# 2. Expected result
Total Tests: 39
Passed: 39 ✅
Failed: 0

# 3. Check backward compatibility
grep "AC#5" test-results.txt
# All should show: [PASS]
```

## Test Patterns Used

All tests use simple bash patterns:

```bash
# Pattern 1: File existence
if [ -f "$file" ]; then PASS; else FAIL; fi

# Pattern 2: Pattern matching
if grep -q "pattern" "$file"; then PASS; else FAIL; fi

# Pattern 3: Count validation
count=$(grep -o "pattern" "$file" | wc -l)
if [ $count -ge 5 ] && [ $count -le 10 ]; then PASS; else FAIL; fi

# Pattern 4: Line position validation
line=$(grep -n "pattern" "$file" | cut -d: -f1)
if [ $line -le 300 ]; then PASS; else FAIL; fi
```

## Success Criteria

### RED Phase (Current)
- ✅ Tests created and executable
- ✅ Tests accurately validate acceptance criteria
- ✅ Tests correctly FAIL (no implementation yet)
- ✅ Clear failure messages indicate what's needed
- ✅ Backward compatibility tests verify existing features

### GREEN Phase (Phase 2)
- ⏳ Implement new section in SKILL.md
- ⏳ Add cross-references to both guidance documents
- ⏳ Include 5-10 paired examples covering all scenarios
- ⏳ Explain "Ask, Don't Assume" principle
- ⏳ Run test suite - ALL 39 TESTS MUST PASS
- ⏳ Verify no breaking changes to existing skill

### REFACTOR Phase (Phase 3)
- Code review and quality validation
- Integration with other skills/commands
- Performance testing (token overhead ≤1,000)
- Documentation updates
- Framework-wide consistency checks

## Test Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Total Tests | 39 | 39 ✅ |
| Passing (RED) | ≥10 | 11 ✅ |
| Failing (RED) | ≥28 | 28 ✅ |
| AC Coverage | 100% | 100% ✅ |
| Backward Compat | 100% | 100% ✅ |

## Common Questions

**Q: Why are so many tests failing?**
A: This is the RED phase of TDD. Tests should fail until the implementation is added. This validates that tests actually test the feature, not just pass by default.

**Q: What do I need to do to make tests pass?**
A: Implement the feature in Phase 2 (GREEN phase):
1. Add new section to SKILL.md
2. Add cross-references and examples
3. Explain the principle
4. Run tests again - they should all PASS

**Q: Can I skip any tests?**
A: No. All 39 tests must PASS in Phase 2 (GREEN) before moving to Phase 3 (Refactor).

**Q: How long should tests take to run?**
A: <1 second. If slower, check system performance.

**Q: What if I get different results?**
A: Check:
1. File path is correct: `./.claude/skills/claude-code-terminal-expert/SKILL.md`
2. Run from project root: `pwd` should show `/mnt/c/Projects/DevForgeAI2` or similar
3. Test file exists: `ls -l tests/STORY-054/test-prompting-guidance.sh`

## Next Steps

1. **Phase 2 (GREEN):** Implement feature in SKILL.md
2. **Run Tests:** Execute test suite again
3. **Verify:** All 39 tests should PASS
4. **Phase 3 (Refactor):** Quality review and optimization

## Support

For detailed test documentation, see:
- `TEST-SUITE-DOCUMENTATION.md` - Comprehensive reference
- `devforgeai/specs/Stories/STORY-054-claude-code-terminal-expert-enhancement.story.md` - Story requirements

---

**Test Framework:** Bash + grep/wc utilities
**No external dependencies required**
**TDD Phase:** RED (All tests written, implementation pending)
