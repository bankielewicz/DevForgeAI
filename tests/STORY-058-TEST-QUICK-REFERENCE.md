# STORY-058 Test Suite - Quick Reference Card

## Test Suite Overview

**Story:** STORY-058 - Documentation Updates with User Input Guidance Cross-References
**Total Tests:** 62
**Status:** RED PHASE (all tests should initially fail)
**Location:** `/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/`

---

## Quick Commands

```bash
# Run all tests (comprehensive)
bash tests/user-input-guidance/test-ac1-claude-md-section.sh && \
bash tests/user-input-guidance/test-ac2-commands-cross-references.sh && \
bash tests/user-input-guidance/test-ac3-skills-cross-references.sh && \
bash tests/user-input-guidance/test-ac4-5-6-quality-validation.sh && \
bash tests/user-input-guidance/test-ac7-sync-checklist.sh && \
bash tests/user-input-guidance/validate-cross-references.sh

# Quick validation only (fastest)
bash tests/user-input-guidance/validate-cross-references.sh

# Run specific test suite
bash tests/user-input-guidance/test-ac1-claude-md-section.sh
bash tests/user-input-guidance/test-ac2-commands-cross-references.sh
bash tests/user-input-guidance/test-ac3-skills-cross-references.sh
bash tests/user-input-guidance/test-ac4-5-6-quality-validation.sh
bash tests/user-input-guidance/test-ac7-sync-checklist.sh
```

---

## Test Files Summary

| File | Tests | AC | Purpose |
|------|-------|----|---------|
| test-ac1-claude-md-section.sh | 10 | #1 | CLAUDE.md Learning section |
| test-ac2-commands-cross-references.sh | 8 | #2 | Commands cross-references (11 cmds) |
| test-ac3-skills-cross-references.sh | 9 | #3 | Skills cross-references (13 skills) |
| test-ac4-5-6-quality-validation.sh | 18 | #4,5,6,8 | Quality, structure, consistency |
| test-ac7-sync-checklist.sh | 10 | #7 | Sync preparation & checklist |
| validate-cross-references.sh | 7 | #4 | Cross-reference validation |

---

## Test Pass/Fail Status

### RED Phase (Before Implementation)
```
Expected: 0/62 passing
All tests FAIL - implementation not started
```

### GREEN Phase (After Implementation)
```
Expected: 62/62 passing
All tests PASS - implementation complete
```

### REFACTOR Phase (Quality Improvement)
```
Expected: 62/62 passing
All tests still PASS - code improved
```

---

## Acceptance Criteria Coverage

| AC | Title | Tests | Expected Result |
|----|-------|-------|-----------------|
| AC#1 | CLAUDE.md Learning Section | 10 | FAIL → PASS |
| AC#2 | Commands Cross-References | 8 | FAIL → PASS |
| AC#3 | Skills Cross-References | 9 | FAIL → PASS |
| AC#4 | Cross-Reference Consistency | 11 | FAIL → PASS |
| AC#5 | Discoverability | 3 | FAIL → PASS |
| AC#6 | Structure Integration | 3 | FAIL → PASS |
| AC#7 | Sync Preparation | 10 | FAIL → PASS |
| AC#8 | Quality Standards | 5 | FAIL → PASS |

---

## What's Being Tested

### AC#1: CLAUDE.md Section (10 tests)
- [ ] Section exists: `## Learning DevForgeAI`
- [ ] Positioned: After "Quick Reference", Before "Development Workflow"
- [ ] Subsection 1: `### Writing Effective Feature Descriptions`
- [ ] Subsection 2: `### User Input Guidance Resources`
- [ ] Subsection 3: `### Progressive Learning Path`
- [ ] Examples: 3-5 good vs bad pairs (❌/✅)
- [ ] Load commands: 3 Read() statements
- [ ] Learning levels: basic, advanced, framework-specific

### AC#2: Commands Cross-References (8 tests)
- [ ] 11 command sections documented
- [ ] Each has: `#### User Input Guidance`
- [ ] Each has: **File:**, **Load:**, **Example:**
- [ ] Descriptions present and non-empty
- [ ] Consistent formatting

### AC#3: Skills Cross-References (9 tests)
- [ ] 13 applicable skills documented
- [ ] Each has: `#### User Input Guidance`
- [ ] Each has: **File:**, **Load:**, **Example:**
- [ ] Descriptions skill-specific
- [ ] Appears after Invocation section

### AC#4: Consistency (4 tests)
- [ ] File paths exist
- [ ] Load syntax correct: Read(file_path=...)
- [ ] No relative paths (use src/ prefix)
- [ ] No cat/@file/source/include patterns

### AC#5: Discoverability (3 tests)
- [ ] Section in first 400 lines
- [ ] Clear directions provided
- [ ] Complete load commands (no additional search needed)

### AC#6: Structure (3 tests)
- [ ] Core sections preserved
- [ ] Section numbering intact
- [ ] Formatting conventions followed

### AC#7: Sync (10 tests)
- [ ] Source files (src/*) updated
- [ ] Sync checklist created
- [ ] All 3 files listed in checklist
- [ ] Mappings clear (src/ → .claude/)
- [ ] Checkboxes present
- [ ] STORY-060 referenced

### AC#8: Quality (5 tests)
- [ ] No placeholders: TODO, TBD, FIXME
- [ ] Concrete examples (not generic)
- [ ] Absolute repository-relative paths
- [ ] Read tool used exclusively
- [ ] Clear, accessible language

---

## Implementation Checklist

### Before Testing
- [ ] Navigate to project root: `/mnt/c/Projects/DevForgeAI2`
- [ ] Verify test scripts are executable: `chmod +x tests/user-input-guidance/*.sh`
- [ ] Check src/ files exist: `ls -la src/CLAUDE.md src/claude/memory/`

### RED Phase
- [ ] Run tests: `bash tests/user-input-guidance/test-ac1-*.sh`
- [ ] Verify all FAIL (expected)
- [ ] Read FAIL output to understand requirements

### Implementation
- [ ] Add Learning section to src/CLAUDE.md
- [ ] Add User Input Guidance to src/claude/memory/commands-reference.md (11 commands)
- [ ] Add User Input Guidance to src/claude/memory/skills-reference.md (13 skills)
- [ ] Create sync checklist: devforgeai/stories/STORY-058/sync-checklist.md

### GREEN Phase
- [ ] Run AC#1 tests: should PASS
- [ ] Run AC#2 tests: should PASS
- [ ] Run AC#3 tests: should PASS
- [ ] Run AC#4-8 tests: should PASS
- [ ] Run validation: should PASS

### Commit
- [ ] All 62/62 tests passing
- [ ] All 7/7 validations passing
- [ ] No outstanding issues
- [ ] Ready for QA

---

## File References

### Source Files (to be updated)
- `src/CLAUDE.md` - Add Learning section
- `src/claude/memory/commands-reference.md` - Add 11 cross-references
- `src/claude/memory/skills-reference.md` - Add 13 cross-references

### Files Created (by STORY-058)
- `devforgeai/stories/STORY-058/sync-checklist.md` - Sync tracking

### Referenced Files (must exist)
- `src/claude/memory/effective-prompting-guide.md` (from STORY-052)
- `src/claude/memory/user-input-guidance.md` (from STORY-053)

### Test Files (in tests/user-input-guidance/)
- `test-ac1-claude-md-section.sh`
- `test-ac2-commands-cross-references.sh`
- `test-ac3-skills-cross-references.sh`
- `test-ac4-5-6-quality-validation.sh`
- `test-ac7-sync-checklist.sh`
- `validate-cross-references.sh`
- `README.md` (full documentation)
- `TEST-EXECUTION-GUIDE.md` (how to run)
- `TEST-SUITE-SUMMARY.md` (comprehensive summary)

---

## Performance

| Test | Time | Status |
|------|------|--------|
| AC#1 | 1-2s | Quick |
| AC#2 | 2-3s | Quick |
| AC#3 | 2-3s | Quick |
| AC#4-6,8 | 3-4s | Medium |
| AC#7 | 2-3s | Quick |
| Validation | 1-2s | Very Quick |
| **Total** | 13-18s | **Total** |

---

## Common Issues

### "File not found"
- Ensure source files exist in src/
- Run from project root directory

### "Pattern not found"
- Implementation incomplete
- Add required sections per AC

### "All tests fail"
- Expected in RED phase
- Implementation needed

### Test script not executable
- Fix: `chmod +x tests/user-input-guidance/*.sh`

---

## Test Documentation

| Document | Purpose |
|----------|---------|
| README.md | Detailed test documentation |
| TEST-EXECUTION-GUIDE.md | How to run tests |
| TEST-SUITE-SUMMARY.md | Comprehensive summary |

**Read from:** `tests/user-input-guidance/`

---

## Success Criteria

✓ **62/62 tests passing**
✓ **7/7 validations passing**
✓ **All ACs (1-8) validated**
✓ **Ready for QA**

---

## Quick Validation

```bash
# Fastest check (2-3 seconds)
bash tests/user-input-guidance/validate-cross-references.sh

# Expected output:
# ✓ PASS: All file paths exist
# ✓ PASS: Load command syntax correct
# ✓ PASS: No prohibited patterns
# ...
# All validations PASSED
```

---

**Last Updated:** 2025-01-22
**Framework:** Bash/Shell
**Status:** RED PHASE
**Total Tests:** 62
**Ready for Implementation:** YES
