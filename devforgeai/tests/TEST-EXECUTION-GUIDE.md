# Test Execution Guide for STORY-090

**Purpose:** Quick reference for executing STORY-090 test suite
**Total Tests:** 85+ tests across 3 test files
**Framework:** Claude Code native tools (Read, Write, Edit, Grep, Bash)
**Status:** ALL FAILING (TDD Red Phase)

---

## Quick Start

### Test Files Location
```
/mnt/c/Projects/DevForgeAI2/.devforgeai/tests/

Files:
  1. STORY-090-template-depends-on-tests.md (45 tests)
  2. STORY-090-technical-spec-coverage.md (40+ tests)
  3. STORY-090-TEST-SUITE-SUMMARY.md (reference)
  4. TEST-EXECUTION-GUIDE.md (this file)
```

### Target Story
```
File: /mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-090-story-template-v2.2-depends-on-field.story.md
Status: Ready for Dev
Story Points: 3
Priority: Critical
```

---

## Test Execution by Acceptance Criterion

### AC#1: Template has depends_on field
**Tests:** 1.1-1.6 (6 tests)
**Time:** ~2-3 minutes

**Quick Test:**
```bash
Read /mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-story-creation/assets/templates/story-template.md
# Verify section between --- markers contains:
#   depends_on: []
# Verify position is AFTER points: and BEFORE status:
```

**All Tests:**
1. Template contains depends_on field
2. Field positioned correctly
3. Field has usage comment
4. Default value is empty array
5. Single dependency example exists
6. Multiple dependency example exists

**Expected Result:** All 6 FAILING (field not yet added)

---

### AC#2: Format Version = 2.2
**Tests:** 2.1-2.4 (4 tests)
**Time:** ~1-2 minutes

**Quick Test:**
```bash
Read /mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-story-creation/assets/templates/story-template.md
# Search for: format_version: "2.2"
# Current: format_version: "2.1" → FAILS
```

**All Tests:**
1. format_version equals "2.2"
2. Version is semantic versioning (MAJOR.MINOR)
3. Not a prerelease version
4. Changelog references v2.2

**Expected Result:** All 4 FAILING (version still 2.1)

---

### AC#3: Changelog Documents v2.2
**Tests:** 3.1-3.6 (6 tests)
**Time:** ~2-3 minutes

**Quick Test:**
```bash
Read /mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-story-creation/assets/templates/story-template.md
# Extract lines 1-60 (changelog section)
# Search for: v2.2 (2025-11-25)
# Current: Only v2.1 and v2.0 entries → FAILS
```

**All Tests:**
1. Changelog has v2.2 entry header
2. Changelog includes date 2025-11-25
3. Changelog includes depends_on description
4. Changelog includes backward compatibility note
5. Format matches existing entries
6. Clarifies non-breaking change

**Expected Result:** All 6 FAILING (changelog not updated)

---

### AC#4: Six Stories Standardized to Array Format
**Tests:** 4.1-4.12 (12 tests)
**Time:** ~3-5 minutes

**Quick Test - STORY-044:**
```bash
Read /mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-044.story.md
# Extract YAML frontmatter (between --- markers)
# Search for: depends_on:
# Verify format is array: depends_on: [] or depends_on: ["STORY-NNN"]
# Current: May be missing or in wrong format → FAILS
```

**Stories to Check:**
- STORY-044
- STORY-045
- STORY-046
- STORY-047
- STORY-048
- STORY-070

**Tests Per Story:**
- Array format check
- Body content unchanged (selected stories)
- Other frontmatter unchanged

**Aggregate Tests:**
- No string format used
- No comma-separated format used
- All references valid STORY-ID format

**Expected Result:** All 12 FAILING (standardization not done)

---

### AC#5: Skill Phase 1 Dependency Question
**Tests:** 5.1-5.8 (8 tests)
**Time:** ~2-3 minutes

**Quick Test:**
```bash
Read /mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-story-creation/references/story-discovery.md
# Or: .claude/skills/devforgeai-story-creation/SKILL.md
# Search for: "depend" or "STORY-ID" in Phase 1 section
# Current: Question may not exist → FAILS
```

**Tests:**
1. Phase 1 includes dependency question
2. Accepts "none" input → `[]`
3. Accepts single STORY-ID → `["STORY-NNN"]`
4. Accepts comma-separated → array
5. Rejects invalid formats
6. Question is optional
7. Generated story has depends_on field
8. Question format matches Phase 1 style

**Expected Result:** All 8 FAILING (enhancement not implemented)

---

### AC#6: Directory Sync Complete
**Tests:** 6.1-6.3 (3 tests)
**Time:** ~1-2 minutes

**Quick Test:**
```bash
# Compare file sizes/content
Read /mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-story-creation/assets/templates/story-template.md
Read /mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-story-creation/assets/templates/story-template.md
# Verify identical content
# Current: May differ until sync completes → FAILS
```

**Tests:**
1. Source and operational templates identical
2. Operational template has v2.2 update
3. diff returns 0 (no differences)

**Expected Result:** All 3 FAILING (sync not done)

---

### AC#7: Content Preservation
**Tests:** 7.1-7.6 (6 tests)
**Time:** ~2-3 minutes

**Quick Test - STORY-044:**
```bash
# Before update (get reference version, e.g., from git history)
git show HEAD:path/to/STORY-044.story.md > story-before.md
# After update (when implemented)
Read /mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-044.story.md
# Compare body sections (after frontmatter)
# Verify identical except depends_on field
```

**Tests:**
1. STORY-044 body unchanged
2. STORY-045 other frontmatter unchanged
3. STORY-046 description unchanged
4. STORY-047 acceptance criteria unchanged
5. STORY-048 definition of done unchanged
6. STORY-070 complete content preserved

**Expected Result:** All 6 FAILING (stories not yet updated)

---

## Component-Level Test Execution

### Configuration Component (story-template.md)
**Tests:** 6 tests
**Location:** STORY-090-technical-spec-coverage.md (C1.1-C1.6)

```bash
# C1.1: File exists at correct paths
Read /mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-story-creation/assets/templates/story-template.md
Read /mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-story-creation/assets/templates/story-template.md

# C1.2: All required frontmatter keys exist
# C1.3: depends_on field type is array
# C1.4: depends_on items validate STORY-ID format
# C1.5: format_version is semantic version
# C1.6: Changelog documents v2.2
```

**Expected Result:** All FAILING

---

### Service Component (devforgeai-story-creation skill)
**Tests:** 5 tests
**Location:** STORY-090-technical-spec-coverage.md (S2.1-S2.5)

```bash
# S2.1: Phase 1 workflow file exists
Read /mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-story-creation/references/story-discovery.md

# S2.2: Phase 1 includes AskUserQuestion for dependencies
Grep -n "depend\|STORY-ID" story-discovery.md

# S2.3-S2.5: Input normalization and defaults
# (Tested after implementation)
```

**Expected Result:** All FAILING

---

### Worker Component (standardize-depends-on.sh script)
**Tests:** 10 tests
**Location:** STORY-090-technical-spec-coverage.md (W3.1-W3.10)

```bash
# W3.1: Script exists
ls -la /mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-story-creation/scripts/standardize-depends-on.sh

# W3.2-W3.10: Script behavior tests
# (Tested after script is created)
# Would run: bash standardize-depends-on.sh test-story.md
```

**Expected Result:** All FAILING (script not yet created)

---

## Business Rules Validation

### BR-001: depends_on must be YAML array
```bash
# Valid: depends_on: []
# Valid: depends_on: ["STORY-044"]
# Invalid: depends_on: "STORY-044" (string)
# Invalid: depends_on: null
# Invalid: depends_on: STORY-044, STORY-045 (no brackets)
```

### BR-002: STORY-ID format validation
```bash
# Regex pattern: ^STORY-\d{3,4}$
# Valid: STORY-044, STORY-001, STORY-9999
# Invalid: story-044 (lowercase), STORY-44 (2 digits), STORY-99999 (5 digits)
```

### BR-003: v2.1 stories backward compatible
```bash
# Test: Old story without depends_on field
Read /mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-030.story.md
# Verify: Parses successfully (no errors)
# Verify: Missing field treated as empty array []
```

### BR-004: Template sync to operational directory
```bash
# Verify: src/ and .claude/ versions identical
diff src/claude/skills/devforgeai-story-creation/assets/templates/story-template.md \
     .claude/skills/devforgeai-story-creation/assets/templates/story-template.md
# Exit code 0 = SUCCESS (no differences)
```

---

## Performance Tests

### NFR-001: Single file < 100ms
```bash
# (After script implementation)
time bash standardize-depends-on.sh test-story.md
# Expected: real 0m0.05s or less
```

### NFR-002: All 6 stories < 2 seconds
```bash
# (After script implementation)
time bash standardize-depends-on.sh STORY-044.story.md STORY-045.story.md ... STORY-070.story.md
# Expected: real 0m1.5s or less
```

### NFR-003: Idempotent operation
```bash
# (After script implementation)
bash standardize-depends-on.sh test-story.md
cp test-story.md test-story-after-run1.md

bash standardize-depends-on.sh test-story.md
cp test-story.md test-story-after-run2.md

diff test-story-after-run1.md test-story-after-run2.md
# Expected: exit code 0 (no differences)
```

---

## Test Result Recording

### Template for Recording Results

```
Test: [Test Number - Test Name]
Status: FAILING | PASSING
Expected: [Expected outcome]
Actual: [Actual outcome]
Evidence: [File/Location showing proof]
Date: YYYY-MM-DD HH:MM:SS
```

### Example Recording

```
Test: 1.1 - Template contains depends_on field in frontmatter
Status: FAILING
Expected: depends_on: [] exists in YAML frontmatter
Actual: depends_on field not found
Evidence: /mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-story-creation/assets/templates/story-template.md
Date: 2025-12-14 10:30:00
Notes: Field will be added during TDD Green phase
```

---

## Troubleshooting

### Tests Not Failing as Expected
- Verify you're reading correct file paths
- Confirm file encoding (UTF-8)
- Check that you're reading the template, not another file

### File Not Found Errors
- Verify absolute paths are correct
- Check file exists: `ls -la /full/path/to/file.md`
- Confirm .md files present in expected directories

### YAML Parsing Issues
- Verify frontmatter is between `---` markers
- Check indentation (YAML is whitespace-sensitive)
- Use tools that understand YAML format

### Test Execution Order
- Tests can run in any order (independent)
- AC#2 depends on AC#1 (template must exist)
- AC#3 depends on AC#2 (changelog in template)
- AC#6 depends on AC#1-4 (implementation complete)
- AC#7 depends on AC#4 (stories updated)

---

## Integration with TDD Workflow

### Red Phase (Current)
- All tests FAIL (expected)
- Tests document what needs to be built
- Record baseline (all 85 tests failing)

### Green Phase (Implementation)
- Run tests frequently during implementation
- Fix code until tests pass
- Target: All 85 tests PASSING

### Refactor Phase
- Keep all tests passing
- Improve code quality
- No new test failures

### QA Phase
- Verify all tests still pass
- Check coverage metrics
- Validate edge cases

---

## Success Criteria

### Red Phase (Now)
- [ ] All 85 tests execute without errors
- [ ] All tests FAIL with clear messages
- [ ] Test failures document requirements
- [ ] No implementation code exists

### Green Phase (After Implementation)
- [ ] All 85 tests PASS
- [ ] No test failures or errors
- [ ] Implementation matches test specifications
- [ ] No code quality issues introduced

### Final Status
- [ ] All tests documented and passing
- [ ] Code coverage >95% for business logic
- [ ] Backward compatibility verified
- [ ] Story marked "QA Approved"

---

## Quick Reference - All Test Counts

| Item | Count |
|------|-------|
| Total Tests | 85+ |
| AC#1 Tests | 6 |
| AC#2 Tests | 4 |
| AC#3 Tests | 6 |
| AC#4 Tests | 12 |
| AC#5 Tests | 8 |
| AC#6 Tests | 3 |
| AC#7 Tests | 6 |
| Tech Spec Tests | 40+ |
| Component Tests | 27 |
| BR Tests | 4 |
| NFR Tests | 5 |
| Edge Case Tests | 3+ |

---

## Next Steps

1. **Review test files:**
   - STORY-090-template-depends-on-tests.md
   - STORY-090-technical-spec-coverage.md

2. **Verify baseline (all failing):**
   - Run sample tests to confirm FAILING status
   - Record baseline metrics

3. **Proceed to implementation:**
   - TDD Green phase begins
   - Code changes guided by test failures
   - Tests provide specifications

4. **Iterate until green:**
   - Implement template changes
   - Implement script
   - Implement skill enhancement
   - Run tests after each change

5. **Final verification:**
   - All 85 tests PASS
   - Coverage metrics acceptable
   - Backward compatibility confirmed

---

**Document Version:** 1.0
**Created:** 2025-12-14
**Status:** READY FOR USE
**All Tests:** FAILING (EXPECTED - TDD Red Phase)
