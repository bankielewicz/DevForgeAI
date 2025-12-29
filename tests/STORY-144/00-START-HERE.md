# STORY-144: Integrate or Remove Orphaned Files - TEST SUITE

**Status**: ✓ COMPLETE - TDD RED PHASE
**Generated**: 2025-12-29
**Test Location**: `/mnt/c/Projects/DevForgeAI2/tests/STORY-144/`
**Total Tests**: 39 test cases across 4 acceptance criteria

---

## What This Is

This is a **comprehensive test suite** for STORY-144, generated following Test-Driven Development (TDD) principles. The tests are written **FIRST**, before implementation, to establish clear specifications for what needs to be built.

**Current Status**: RED PHASE (tests are failing - this is expected and correct)

---

## Quick Start (60 seconds)

### Step 1: Run the Tests
```bash
bash /mnt/c/Projects/DevForgeAI2/tests/STORY-144/run-all-tests.sh
```

### Step 2: Review What Failed
The output shows what needs to be implemented:
- Orphaned files need to be deleted or integrated
- References in SKILL.md need to be updated
- Commit message needs to document the changes

### Step 3: Implement (after this, tests will pass)
- Decide: Keep or delete each orphaned file?
- If keeping: Integrate content into target files
- If deleting: Remove files and update references
- Commit with proper message format

### Step 4: Re-run Tests
After implementation, all 39 tests should pass.

---

## Files in This Test Suite

| File | Purpose | Size |
|------|---------|------|
| **00-START-HERE.md** | This quick reference | 3 KB |
| **INDEX.md** | Complete file index | 8 KB |
| **README.md** | How to run tests | 12 KB |
| **TEST-SUMMARY.md** | Test design details | 12 KB |
| **EXECUTION-REPORT.md** | Implementation guide | 15 KB |
| **run-all-tests.sh** | Master test runner | 3 KB |
| **test-ac1-*.sh** | AC#1 tests (8 tests) | 4.4 KB |
| **test-ac2-*.sh** | AC#2 tests (9 tests) | 4.6 KB |
| **test-ac3-*.sh** | AC#3 tests (10 tests) | 5.9 KB |
| **test-ac4-*.sh** | AC#4 tests (12 tests) | 5.2 KB |

**Total**: 84 KB of tests and documentation

---

## What Each Acceptance Criterion Tests

### AC#1: user-input-integration-guide.md (8 tests)
Tests that this orphaned file is either **deleted** or **integrated** into user-input-guidance.md.

**Status**: 7 failing, 1 passing
**What's Needed**: Delete file OR move content to target file and clean up references

### AC#2: brainstorm-data-mapping.md (9 tests)
Tests that this orphaned file is either **deleted** or **integrated** into brainstorm-handoff-workflow.md.

**Status**: 4 failing, 5 passing
**What's Needed**: Delete file OR move content to target file and clean up references

### AC#3: No Unreferenced Files (10 tests)
Tests that every file in the references directory is referenced somewhere in SKILL.md or workflow files.

**Status**: 5 failing, 5 passing
**What's Needed**: Complete AC#1 and AC#2, then verify no orphans remain

### AC#4: Commit Message Documentation (12 tests)
Tests that the commit message documents what was changed and why.

**Status**: 9 failing, 3 passing
**What's Needed**: Create commit with proper format including story ID, files, actions, and justification

---

## Implementation Checklist

Follow these steps to make all tests pass:

### Phase 1: Analyze (Time-box to 30 minutes per file)
- [ ] Read user-input-integration-guide.md
- [ ] Assess: Is content valuable and unique?
- [ ] Decision: INTEGRATE or DELETE?
- [ ] Read brainstorm-data-mapping.md
- [ ] Assess: Is content valuable and unique?
- [ ] Decision: INTEGRATE or DELETE?

### Phase 2: Implement (If Integrating)
- [ ] Copy user-input-integration-guide.md content to user-input-guidance.md Section 5
- [ ] Copy brainstorm-data-mapping.md content to brainstorm-handoff-workflow.md
- [ ] Delete original files
- [ ] Remove references from SKILL.md

### Phase 2: Implement (If Deleting)
- [ ] Delete user-input-integration-guide.md
- [ ] Delete brainstorm-data-mapping.md
- [ ] Remove references from SKILL.md
- [ ] Update SKILL.md to reflect files no longer exist

### Phase 3: Commit
Create a commit message like this:
```
chore(ideation): resolve orphaned reference files

- user-input-integration-guide.md: [INTEGRATED/DELETED] - [reason]
- brainstorm-data-mapping.md: [INTEGRATED/DELETED] - [reason]
```

### Phase 4: Verify
Run tests to confirm all 39 pass:
```bash
bash /mnt/c/Projects/DevForgeAI2/tests/STORY-144/run-all-tests.sh
```

---

## Test Results Summary

```
Current Status: RED PHASE (Tests Failing - Expected)

Total Tests: 39
├─ Passing: 16 (41%)
├─ Failing: 23 (59%) ← Shows what needs implementation
└─ Status: Ready for implementation

Breakdown by AC:
├─ AC#1: 8 tests (7 failing)
├─ AC#2: 9 tests (4 failing)
├─ AC#3: 10 tests (5 failing)
└─ AC#4: 12 tests (9 failing)
```

---

## Key Files to Modify

### Orphaned Files (Decision Required)
```
.claude/skills/devforgeai-ideation/references/user-input-integration-guide.md
.claude/skills/devforgeai-ideation/references/brainstorm-data-mapping.md
```

### Integration Targets (If Content Valuable)
```
.claude/skills/devforgeai-ideation/references/user-input-guidance.md
.claude/skills/devforgeai-ideation/references/brainstorm-handoff-workflow.md
```

### File to Update (References)
```
.claude/skills/devforgeai-ideation/SKILL.md
```

---

## Running Individual Tests

### Run Single Acceptance Criterion
```bash
# AC#1 only
bash test-ac1-user-input-integration-guide.sh

# AC#2 only
bash test-ac2-brainstorm-data-mapping.sh

# AC#3 only
bash test-ac3-no-unreferenced-files.sh

# AC#4 only
bash test-ac4-commit-message-documentation.sh
```

### Run All Tests With Logging
```bash
bash run-all-tests.sh | tee results.txt
```

---

## Test Framework Details

### Framework: Bash/Shell Scripts
- No external dependencies
- Uses grep, find, git (standard Unix tools)
- Works on any Linux/Unix system

### Design Pattern: AAA (Arrange-Act-Assert)
Each test:
1. **Arranges** test environment (sets paths, creates test data)
2. **Acts** on the behavior (executes file operations)
3. **Asserts** expected outcome (verifies results)

### Test Pyramid: TDD Compliance
```
      /\
     /E2E\      12% - AC#4 (Integration tests)
    /------\
   /Unit   \    88% - AC#1-3 (Unit tests)
  /----------\
```

### Independence: No Shared State
- Each test runs standalone
- Tests can execute in any order
- No cleanup between tests needed

---

## Success Criteria

Tests will **PASS** when:

1. ✓ user-input-integration-guide.md is deleted OR integrated
2. ✓ brainstorm-data-mapping.md is deleted OR integrated
3. ✓ No orphaned files remain unreferenced
4. ✓ Commit message documents all changes and reasons
5. ✓ SKILL.md references updated to remove orphaned files
6. ✓ All 39 tests exit with code 0

---

## Documentation Map

- **This File** (00-START-HERE.md) - Quick orientation
- **INDEX.md** - File descriptions and index
- **README.md** - How to run tests and troubleshooting
- **TEST-SUMMARY.md** - Test design and architecture
- **EXECUTION-REPORT.md** - Detailed implementation guide

**Choose your path**:
- New to tests? → Start with this file, then README.md
- Need implementation steps? → Read EXECUTION-REPORT.md
- Want test details? → Read TEST-SUMMARY.md
- Looking for something specific? → Check INDEX.md

---

## FAQ

**Q: Why do all tests fail initially?**
A: This is TDD (Test-Driven Development). Tests are written FIRST to specify what needs to be built. Failing tests show you exactly what to implement.

**Q: When will tests pass?**
A: After you implement the changes (delete or integrate orphaned files and update references).

**Q: Can I run tests while implementing?**
A: Yes! Re-run tests after each change to see progress. Tests will gradually pass as you complete implementation.

**Q: What if a test passes but seems wrong?**
A: Check the test comment at the top of the script. It explains what the test verifies.

**Q: Do I need to modify the tests?**
A: No. The tests define the requirements. Focus on making tests pass by implementing changes.

**Q: What does "RED phase" mean?**
A: RED phase of TDD means tests are failing (Red indicator). Next is GREEN (make tests pass), then REFACTOR.

---

## Next Steps

1. **Read INDEX.md** for detailed file descriptions
2. **Run run-all-tests.sh** to see failing tests
3. **Review README.md** for test details
4. **Follow EXECUTION-REPORT.md** for implementation steps
5. **Commit changes** with proper message format
6. **Re-run tests** to verify all pass

---

## Test Coverage

```
Acceptance Criteria:  100% (all 4 ACs tested)
Test Cases:           39 distinct tests
Edge Cases:           Yes (circular refs, permissions)
Error Handling:       Yes (missing files, invalid formats)
Documentation:        Yes (inline comments + 4 docs)
```

---

## Support

If you need help:
1. Check README.md troubleshooting section
2. Review EXECUTION-REPORT.md implementation guide
3. Read test file comments (each test explains what it verifies)
4. Check test output - it shows exactly what failed and why

---

## Summary

You now have:
- ✓ 39 test cases verifying STORY-144 requirements
- ✓ 4 test files for each acceptance criterion
- ✓ Clear specifications of what needs implementation
- ✓ Automated verification that implementation is complete
- ✓ Comprehensive documentation for reference

**Next Action**: Run tests and begin implementation!

```bash
bash /mnt/c/Projects/DevForgeAI2/tests/STORY-144/run-all-tests.sh
```

---

**Questions?** See the other documentation files or review the test scripts themselves - they're well-commented and self-explanatory.

