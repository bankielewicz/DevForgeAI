# STORY-160 Test Suite Index

**Story:** STORY-160 - RCA-008 Skill Documentation Update
**Created:** 2025-12-31
**Location:** `/mnt/c/Projects/DevForgeAI2/tests/STORY-160/`

---

## Files in This Directory

### Executable Test Scripts

1. **run-all-tests.sh** [198 lines]
   - Main test runner that executes all 5 AC tests
   - Provides comprehensive summary report
   - Use this for complete validation
   - Exit code: 0 = all pass, 1 = some fail

2. **test-ac1-skill-md-validation-steps.sh** [143 lines]
   - AC-1: SKILL.md Overview Updated
   - 7 individual tests
   - Validates 10 validation steps documentation

3. **test-ac2-reference-files-documented.sh** [150 lines]
   - AC-2: Reference Files Documented
   - 8 individual tests
   - Validates preflight-validation.md and git-workflow-conventions.md

4. **test-ac3-subagent-coordination-updated.sh** [142 lines]
   - AC-3: Subagent Coordination Updated
   - 7 individual tests
   - Validates git-validator coordination documentation

5. **test-ac4-changelog-entry.sh** [119 lines]
   - AC-4: Change Log Entry
   - 6 individual tests
   - Validates RCA-008 changelog entry

6. **test-ac5-skills-reference-memory-file.sh** [138 lines]
   - AC-5: Skills Reference Memory File
   - 8 individual tests
   - Validates skills-reference.md content

7. **test-integration-cross-file-references.sh** [235 lines]
   - Integration Tests
   - 10 comprehensive tests
   - Validates cross-file references and consistency

8. **test-documentation-accuracy.sh** [233 lines]
   - Documentation Quality Tests
   - 10 accuracy verification tests
   - Validates documentation standards

9. **validate-test-suite.sh** [220 lines]
   - Test suite validation script
   - Verifies test infrastructure
   - Checks test structure and completeness

### Documentation Files

10. **README.md** [354 lines]
    - Comprehensive test suite documentation
    - How to run tests
    - Test output format
    - Troubleshooting guide
    - Full reference for all tests

11. **VERIFICATION-REPORT.md** [400 lines]
    - Detailed verification report
    - Executive summary
    - Test composition details
    - Coverage metrics
    - Integration points
    - RCA-008 context

12. **TEST-SUITE-SUMMARY.md** [330 lines]
    - Quick reference guide
    - Quick start instructions
    - File listing with line counts
    - Test coverage summary
    - RCA-008 features verified
    - Expected test results

13. **INDEX.md** [this file]
    - Directory index
    - File descriptions
    - Quick navigation guide

### Support Files

14. **test-results.txt** (generated)
    - Test execution results
    - Created when tests are run
    - Contains colored output

---

## Quick Navigation

### To Run Tests
1. **Run everything:** `bash run-all-tests.sh`
2. **Run AC-1 only:** `bash test-ac1-skill-md-validation-steps.sh`
3. **Run AC-2 only:** `bash test-ac2-reference-files-documented.sh`
4. **Run AC-3 only:** `bash test-ac3-subagent-coordination-updated.sh`
5. **Run AC-4 only:** `bash test-ac4-changelog-entry.sh`
6. **Run AC-5 only:** `bash test-ac5-skills-reference-memory-file.sh`
7. **Run integration tests:** `bash test-integration-cross-file-references.sh`
8. **Run quality tests:** `bash test-documentation-accuracy.sh`

### To Read Documentation
- **Getting Started:** Read `TEST-SUITE-SUMMARY.md` first (this is quick!)
- **Detailed Guide:** Read `README.md` for comprehensive information
- **Verification Details:** Read `VERIFICATION-REPORT.md` for metrics and coverage
- **This Index:** You're reading it now!

### To Understand Test Structure
- Each AC test is independent and can run standalone
- Test runner (`run-all-tests.sh`) orchestrates all 5 AC tests
- Integration and quality tests are supplementary
- All tests use bash script with color-coded output

---

## File Statistics

| Category | Count | Lines |
|----------|-------|-------|
| Test Scripts (AC) | 5 | 652 |
| Test Scripts (Integration/Quality) | 2 | 468 |
| Test Infrastructure | 2 | 418 |
| Documentation | 3 | 1,084 |
| **Total** | **12** | **2,622** |

---

## Test Coverage

```
STORY-160 Acceptance Criteria
├── AC-1: SKILL.md Overview Updated
│   └── test-ac1-skill-md-validation-steps.sh (7 tests)
├── AC-2: Reference Files Documented
│   └── test-ac2-reference-files-documented.sh (8 tests)
├── AC-3: Subagent Coordination Updated
│   └── test-ac3-subagent-coordination-updated.sh (7 tests)
├── AC-4: Change Log Entry
│   └── test-ac4-changelog-entry.sh (6 tests)
└── AC-5: Skills Reference Memory File
    └── test-ac5-skills-reference-memory-file.sh (8 tests)

Integration & Quality Testing
├── Cross-file References
│   └── test-integration-cross-file-references.sh (10 tests)
└── Documentation Accuracy
    └── test-documentation-accuracy.sh (10 tests)

Total: 56 Tests Across 8 Scripts
```

---

## Getting Started (3-Step Quick Start)

### Step 1: Navigate to Project Root
```bash
cd /mnt/c/Projects/DevForgeAI2
```

### Step 2: Run All Tests
```bash
bash tests/STORY-160/run-all-tests.sh
```

### Step 3: Review Results
- Check exit code: `echo $?` (0 = all pass)
- Review colored output for details
- Check any WARNINGS or FAILURES

---

## Documentation Reading Order

**For Quick Overview (15 minutes):**
1. This INDEX.md
2. TEST-SUITE-SUMMARY.md

**For Complete Understanding (1 hour):**
1. README.md
2. VERIFICATION-REPORT.md
3. Individual test scripts

**For Specific Topics:**
- How to run tests → README.md section "How to Run Tests"
- What's being tested → VERIFICATION-REPORT.md section "Documentation Verified"
- RCA-008 context → VERIFICATION-REPORT.md section "RCA-008 Context"
- Test structure → README.md section "Test Suite Structure"

---

## Key Acceptance Criteria

### AC-1: SKILL.md Overview Updated
- SKILL.md lists 10 validation steps
- Includes Steps 0.1.5 and 0.1.6
- Pre-Flight Validation section complete

### AC-2: Reference Files Documented
- preflight-validation.md referenced with RCA-008 note
- git-workflow-conventions.md referenced with Stash Safety Protocol note
- Both reference files exist and contain relevant content

### AC-3: Subagent Coordination Updated
- git-validator mentioned in coordination context
- Enhanced file analysis (Phase 2.5) referenced
- RCA-008 enhancements documented

### AC-4: Change Log Entry
- RCA-008 entry in SKILL.md changelog
- Entry describes git safety enhancements
- Entry properly formatted and dated

### AC-5: Skills Reference Memory File
- devforgeai-development section in skills-reference.md
- User consent checkpoint documented
- Stash warning workflow documented
- Smart stash strategy documented

---

## Test Execution Environment

**Requirements:**
- Bash shell (3.2+)
- grep utility
- Project root: `/mnt/c/Projects/DevForgeAI2`
- LF line endings (not CRLF)

**Tested On:**
- Linux (WSL2)
- Bash 5.1

---

## Maintenance Notes

### Adding New Tests
1. Create script in this directory: `test-{name}.sh`
2. Add executable bit: `chmod +x test-{name}.sh`
3. Include proper shebang and error handling
4. Update run-all-tests.sh if it's an AC test
5. Update this INDEX.md

### Updating Existing Tests
1. Edit script file
2. Maintain consistent style
3. Test the changes: `bash {script}.sh`
4. Update documentation if behavior changes

### Test Results Archive
- Results saved to: `test-results.txt`
- Archive old results before rerunning tests
- Use results for QA sign-off and auditing

---

## Related Documentation

**Story Files:**
- Story: `/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-160-rca-008-skill-documentation-update.story.md`
- RCA: `/mnt/c/Projects/DevForgeAI2/devforgeai/RCA/RCA-008-autonomous-git-stashing.md`

**Tested Files:**
- SKILL.md: `/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-development/SKILL.md`
- Reference: `/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-development/references/`
- Memory: `/mnt/c/Projects/DevForgeAI2/.claude/memory/skills-reference.md`
- Agents: `/mnt/c/Projects/DevForgeAI2/.claude/agents/git-validator.md`

---

## Quick Command Reference

```bash
# Run all tests
bash tests/STORY-160/run-all-tests.sh

# Run single AC test
bash tests/STORY-160/test-ac1-skill-md-validation-steps.sh

# Run integration tests
bash tests/STORY-160/test-integration-cross-file-references.sh

# Save results
bash tests/STORY-160/run-all-tests.sh | tee tests/STORY-160/test-results.txt

# Check test syntax
bash -n tests/STORY-160/test-ac1-skill-md-validation-steps.sh

# List all test files
ls -la tests/STORY-160/*.sh
```

---

## Support & Troubleshooting

### Tests Fail: File Not Found
- Check working directory is project root
- Verify all documentation files exist
- Use `ls` to confirm file locations

### Tests Fail: Content Not Found
- Review test expectations vs actual documentation
- Check for spelling variations
- Examine documentation content with grep

### Tests Fail: Script Errors
- Check for CRLF line endings: `file {script}.sh`
- Convert if needed: `dos2unix {script}.sh`
- Verify bash version: `bash --version`

### Need Help?
1. Check README.md Troubleshooting section
2. Review VERIFICATION-REPORT.md
3. Look at individual test script comments
4. Run with debug: `bash -x {script}.sh`

---

## Version & Status

| Aspect | Value |
|--------|-------|
| Created | 2025-12-31 |
| Version | 1.0 |
| Status | READY FOR EXECUTION |
| Total Tests | 56 |
| Acceptance Criteria | 5/5 (100%) |

---

**Next Step:** Run `bash run-all-tests.sh` to execute the complete test suite!

**Quick Links:**
- [TEST-SUITE-SUMMARY.md](TEST-SUITE-SUMMARY.md) - Quick start
- [README.md](README.md) - Full documentation
- [VERIFICATION-REPORT.md](VERIFICATION-REPORT.md) - Detailed report
