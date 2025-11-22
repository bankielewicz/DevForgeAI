# STORY-058 Test Execution Guide

## Quick Start

### Run All Tests (Comprehensive)
```bash
# Navigate to project root
cd /mnt/c/Projects/DevForgeAI2

# Run all test suites sequentially
bash tests/user-input-guidance/test-ac1-claude-md-section.sh && \
bash tests/user-input-guidance/test-ac2-commands-cross-references.sh && \
bash tests/user-input-guidance/test-ac3-skills-cross-references.sh && \
bash tests/user-input-guidance/test-ac4-5-6-quality-validation.sh && \
bash tests/user-input-guidance/test-ac7-sync-checklist.sh && \
bash tests/user-input-guidance/validate-cross-references.sh
```

### Quick Validation Only
```bash
# Fastest validation (cross-reference checks only)
bash tests/user-input-guidance/validate-cross-references.sh
```

---

## Individual Test Suites

### Test AC#1: CLAUDE.md Learning Section (10 tests)
```bash
bash tests/user-input-guidance/test-ac1-claude-md-section.sh
```

**What it validates:**
- Section header exists and is positioned correctly
- Three required subsections present
- 3-5 good/bad examples included
- Learning levels mentioned (basic, advanced, framework-specific)

**Expected output (RED phase):**
```
FAIL: Section header '## Learning DevForgeAI' not found in src/CLAUDE.md
```

---

### Test AC#2: Commands Cross-References (8 tests)
```bash
bash tests/user-input-guidance/test-ac2-commands-cross-references.sh
```

**What it validates:**
- All 11 commands have sections
- Each command has "User Input Guidance" subsection
- Consistent structure: File, Load, Example
- Guidance descriptions exist

**Tested commands:**
- /ideate, /create-context, /create-epic, /create-sprint
- /create-story, /create-ui, /dev, /qa, /release, /orchestrate, /audit-deferrals

---

### Test AC#3: Skills Cross-References (9 tests)
```bash
bash tests/user-input-guidance/test-ac3-skills-cross-references.sh
```

**What it validates:**
- 13 applicable skills documented
- Each skill has "User Input Guidance" subsection
- Descriptions are skill-specific
- User Input Guidance appears after Invocation

**Tested skills:**
- devforgeai-ideation, devforgeai-architecture, devforgeai-orchestration
- devforgeai-story-creation, devforgeai-ui-generator, devforgeai-development
- devforgeai-qa, devforgeai-release, devforgeai-documentation
- devforgeai-feedback, devforgeai-mcp-cli-converter, devforgeai-subagent-creation
- devforgeai-rca

---

### Test AC#4, 5, 6, 8: Quality & Structure (18 tests)
```bash
bash tests/user-input-guidance/test-ac4-5-6-quality-validation.sh
```

**What it validates:**

**AC#4 - Cross-Reference Consistency (4 tests):**
- File paths exist
- Load commands use Read() syntax
- File paths use src/ prefix
- No prohibited patterns

**AC#5 - Discoverability (3 tests):**
- Learning section in first 400 lines
- Clear directions provided
- Complete load commands

**AC#6 - Structure Integration (3 tests):**
- Core sections preserved
- Section numbering intact
- Formatting conventions followed

**AC#8 - Quality Standards (5 tests):**
- No placeholders (TODO, TBD, FIXME)
- Examples are concrete
- File paths absolute and repository-relative
- Read tool used exclusively
- Documentation is clear and accessible

---

### Test AC#7: Sync Checklist (10 tests)
```bash
bash tests/user-input-guidance/test-ac7-sync-checklist.sh
```

**What it validates:**
- Source files (src/*) contain updates
- Sync checklist exists
- Checklist has all 3 file mappings
- Checklist has checkbox tracking items
- Checklist references STORY-060

**Files checked:**
- src/CLAUDE.md
- src/claude/memory/commands-reference.md
- src/claude/memory/skills-reference.md

---

### Validate Cross-References (7 validations)
```bash
# Text output (default)
bash tests/user-input-guidance/validate-cross-references.sh

# JSON output (machine-readable)
bash tests/user-input-guidance/validate-cross-references.sh json

# CSV output (spreadsheet-compatible)
bash tests/user-input-guidance/validate-cross-references.sh csv
```

**What it validates:**
1. File paths point to existing files
2. Load command syntax correct
3. File path format (repository-relative)
4. No duplicate guidance sections
5. Terminology consistency
6. Read() command syntax presence
7. No Bash/cat in documentation

---

## TDD Workflow

### Phase 1: RED (Tests Fail - Before Implementation)
```bash
$ bash tests/user-input-guidance/test-ac1-claude-md-section.sh

FAIL: Section header '## Learning DevForgeAI' not found in src/CLAUDE.md
  Expected section header '## Learning DevForgeAI' not found in src/CLAUDE.md
...
TEST SUMMARY: AC#1
Passed: 0
Failed: 10

exit 1
```

### Phase 2: GREEN (Tests Pass - After Implementation)
```bash
$ bash tests/user-input-guidance/test-ac1-claude-md-section.sh

PASS: Section header '## Learning DevForgeAI' found
PASS: Learning DevForgeAI section positioned correctly between Quick Reference and Development Workflow
...
TEST SUMMARY: AC#1
Passed: 10
Failed: 0

exit 0
```

### Phase 3: REFACTOR (Maintain Passing Tests - Quality Improvement)
```bash
# Run tests after refactoring
$ bash tests/user-input-guidance/test-ac1-claude-md-section.sh

PASS: ... (all tests still pass)
```

---

## Expected Test Results by Acceptance Criteria

### AC#1: 10/10 Tests
- Section header exists ✓
- Section positioned correctly ✓
- 3 subsections exist ✓
- 3-5 examples included ✓
- 3 Read commands present ✓
- Learning levels mentioned ✓
- Subsections in order ✓

### AC#2: 8/8 Tests
- File exists ✓
- All 11 command sections ✓
- All have User Input Guidance ✓
- Consistent structure ✓
- Descriptions present ✓
- Read commands found ✓
- 11 guidance subsections ✓
- Consistent formatting ✓

### AC#3: 9/9 Tests
- File exists ✓
- 13 skill sections ✓
- All have User Input Guidance ✓
- Structure complete ✓
- 13+ guidance subsections ✓
- Infrastructure skills excluded ✓
- Skill-specific descriptions ✓
- Consistent formatting ✓
- Correct ordering ✓

### AC#4, 5, 6, 8: 18/18 Tests
- File paths exist (AC#4) ✓
- Read syntax correct (AC#4) ✓
- src/ prefix used (AC#4) ✓
- No bad patterns (AC#4) ✓
- Section in first 400 lines (AC#5) ✓
- Clear directions (AC#5) ✓
- Complete commands (AC#5) ✓
- Core sections preserved (AC#6) ✓
- Numbering intact (AC#6) ✓
- Formatting follows conventions (AC#6) ✓
- No placeholders (AC#8) ✓
- Concrete examples (AC#8) ✓
- Absolute paths (AC#8) ✓
- Read tool used (AC#8) ✓
- Clear language (AC#8) ✓

### AC#7: 10/10 Tests
- Source file exists (AC#7) ✓
- Source has updates (AC#7) ✓
- Sync checklist exists (AC#7) ✓
- All 3 files listed (AC#7) ✓
- Mappings clear (AC#7) ✓
- Checkboxes present (AC#7) ✓
- STORY-060 referenced (AC#7) ✓

### Validation Script: 7/7 Checks
- File paths valid ✓
- Load syntax correct ✓
- Path format correct ✓
- No duplicates ✓
- Terminology consistent ✓
- Read() usage present ✓
- No Bash patterns ✓

---

## Interpreting Test Output

### PASS Status
```
PASS: [Test description]
```
✓ Test passed - assertion succeeded

### FAIL Status
```
FAIL: [Test description]
  Expected: [condition]
  Found: [actual result]
```
✗ Test failed - assertion did not match

### INFO Status
```
INFO: [Informational message]
```
ℹ Non-blocking informational message (test may still pass)

---

## Common Issues & Solutions

### Issue: "File does not exist: src/CLAUDE.md"
**Cause:** Source files haven't been set up
**Solution:**
```bash
# Check if files exist
ls -la src/CLAUDE.md src/claude/memory/commands-reference.md src/claude/memory/skills-reference.md

# If missing, check context
echo "Project root should be: /mnt/c/Projects/DevForgeAI2"
pwd
```

### Issue: "Pattern not found" in multiple tests
**Cause:** Implementation not started or incomplete
**Solution:** Start implementing the story features:
1. Add Learning section to src/CLAUDE.md
2. Add User Input Guidance to commands-reference.md (11 commands)
3. Add User Input Guidance to skills-reference.md (13 skills)
4. Create sync checklist

### Issue: Some tests pass, some fail
**Cause:** Partial implementation
**Solution:** Continue implementing remaining sections:
```bash
# Run individual test to see what's missing
bash tests/user-input-guidance/test-ac1-claude-md-section.sh 2>&1 | grep "FAIL"

# Implement the failed items, run test again
bash tests/user-input-guidance/test-ac1-claude-md-section.sh
```

---

## Test Metrics

### Total Tests: 62
- AC#1: 10 tests
- AC#2: 8 tests
- AC#3: 9 tests
- AC#4-6, #8: 18 tests
- AC#7: 10 tests
- Validation Script: 7 checks

### Test Coverage by Layer
- **Structure:** 20 tests (section headers, positioning, formatting)
- **Content:** 25 tests (examples, descriptions, terminology)
- **Integration:** 12 tests (file paths, linking, sync)
- **Quality:** 5 tests (placeholders, standards compliance)

### Expected Pass Rate Progression
| Phase | Expected | When |
|-------|----------|------|
| RED | 0% | Before implementation |
| GREEN | 100% | After implementation complete |
| REFACTOR | 100% | After code review & improvements |

---

## Performance Expectations

### Single Test Suite Execution Time
```
test-ac1: ~1-2 seconds
test-ac2: ~2-3 seconds
test-ac3: ~2-3 seconds
test-ac4-5-6-8: ~3-4 seconds
test-ac7: ~2-3 seconds
validate-cross-references: ~1-2 seconds
```

### Total Full Suite Execution Time
```
~13-18 seconds for all tests combined
```

### Optimization Tips
```bash
# Run only failing tests (skip passing ones)
bash tests/user-input-guidance/test-ac1-claude-md-section.sh || true
bash tests/user-input-guidance/test-ac2-commands-cross-references.sh || true

# Parallel execution (if using multiple terminals)
(bash test-ac1-...; bash test-ac2-...; bash test-ac3-...) &
```

---

## Continuous Testing During Development

### Before Each Implementation Session
```bash
# Quick status check
bash tests/user-input-guidance/validate-cross-references.sh
```

### After Each Major Change
```bash
# Test the specific AC you just implemented
bash tests/user-input-guidance/test-ac1-claude-md-section.sh
```

### Before Commit
```bash
# Full test suite
bash tests/user-input-guidance/test-ac1-claude-md-section.sh && \
bash tests/user-input-guidance/test-ac2-commands-cross-references.sh && \
bash tests/user-input-guidance/test-ac3-skills-cross-references.sh && \
bash tests/user-input-guidance/test-ac4-5-6-quality-validation.sh && \
bash tests/user-input-guidance/test-ac7-sync-checklist.sh && \
bash tests/user-input-guidance/validate-cross-references.sh

# Exit code 0 = all pass, 1 = failures
echo $?
```

---

## References

- **Story File:** .ai_docs/Stories/STORY-058-documentation-updates.story.md
- **Test Suite README:** tests/user-input-guidance/README.md
- **Test Fixtures:** tests/user-input-guidance/fixtures/
- **Documentation Files:**
  - src/CLAUDE.md (to be updated)
  - src/claude/memory/commands-reference.md (to be updated)
  - src/claude/memory/skills-reference.md (to be updated)

---

**Last Updated:** 2025-01-22
**Test Framework:** Bash/Shell
**TDD Status:** RED PHASE (tests written, implementation pending)
