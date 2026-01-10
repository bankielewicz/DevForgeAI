# Test Specification: STORY-199

## Story Information

| Field | Value |
|-------|-------|
| Story ID | STORY-199 |
| Title | Document Hook Design Philosophy and Update Process |
| Type | Documentation |
| Epic | EPIC-033-framework-enhancement-triage-q4-2025 |
| Source RCA | RCA-015, REC-5 |
| Implementation Output | `.claude/hooks/README.md` |

## Test Suite Overview

| Test File | Acceptance Criteria | Status |
|-----------|---------------------|--------|
| `test-ac1-readme-creation.sh` | AC#1: README Creation | Ready |
| `test-ac2-safe-pattern-criteria.sh` | AC#2: Safe Pattern Criteria | Ready |
| `test-ac3-blocked-pattern-criteria.sh` | AC#3: Blocked Pattern Criteria | Ready |
| `test-ac4-update-process.sh` | AC#4: Update Process Documentation | Ready |
| `test-ac5-debugging-information.sh` | AC#5: Debugging Information | Ready |
| `run-all-tests.sh` | All Tests Runner | Ready |

## Test Details

### AC#1: README Creation (test-ac1-readme-creation.sh)

**Purpose:** Verify README.md file exists with basic structure

**Tests:**
1. README.md exists at `.claude/hooks/README.md`
2. File is not empty
3. Contains main title header (`# DevForgeAI` or `# Pre-Tool-Use Hook`)
4. DOC-001: Contains `## Purpose` section
5. Purpose section has meaningful content

**Technical Specification Coverage:**
- DOC-001: Document hook purpose and overview

---

### AC#2: Safe Pattern Criteria (test-ac2-safe-pattern-criteria.sh)

**Purpose:** Verify documentation of safe pattern selection criteria

**Tests:**
1. DOC-002: Contains 'Safe Patterns' section
2. Documents read-only commands as safe
3. Documents framework operations as safe
4. Documents navigation commands as safe
5. Documents non-destructive operations as safe
6. Contains examples of safe commands (git status, ls, pwd, etc.)
7. Contains selection criteria explanation

**Technical Specification Coverage:**
- DOC-002: Document safe pattern selection criteria

**Required Content:**
- Categories: read-only, framework ops, navigation, non-destructive
- Examples: git status, git log, git diff, ls, pwd, cat

---

### AC#3: Blocked Pattern Criteria (test-ac3-blocked-pattern-criteria.sh)

**Purpose:** Verify documentation of blocked pattern criteria

**Tests:**
1. DOC-003: Contains 'Blocked Patterns' section
2. Documents `rm -rf` as blocked
3. Documents `sudo` as blocked
4. Documents `git push` as blocked
5. Documents `npm publish` as blocked
6. Documents `curl/wget` as blocked
7. Contains explanation of why patterns are blocked
8. Contains at least 5 blocked command examples

**Technical Specification Coverage:**
- DOC-003: Document blocked pattern criteria

**Required Blocked Patterns:**
- `rm -rf` (destructive file deletion)
- `sudo` (privilege escalation)
- `git push` (remote modification)
- `npm publish` (package registry modification)
- `curl/wget` (network operations)

---

### AC#4: Update Process Documentation (test-ac4-update-process.sh)

**Purpose:** Verify 7-step update process is documented

**Tests:**
1. DOC-004: Contains 'Update Process' section
2. Contains at least 7 numbered steps
3. Step 1: Run analysis
4. Step 2: Review candidates
5. Step 3: Validate safety
6. Step 4: Add patterns
7. Step 5: Test
8. Step 6: Commit
9. Step 7: Monitor
10. References analysis tool (STORY-198)

**Technical Specification Coverage:**
- DOC-004: Document 7-step update process

**Required 7-Step Process:**
1. Run analysis (using STORY-198 tool)
2. Review candidates
3. Validate safety
4. Add patterns
5. Test
6. Commit
7. Monitor

---

### AC#5: Debugging Information (test-ac5-debugging-information.sh)

**Purpose:** Verify debugging resources are documented

**Tests:**
1. DOC-005: Contains 'Debugging' section
2. Documents log locations
3. References analysis tool (STORY-198)
4. Contains debugging commands or procedures
5. Documents common issues or error scenarios
6. Contains hook file location reference
7. Contains enable/disable debugging guidance

**Technical Specification Coverage:**
- DOC-005: Document debugging resources (log locations, tools)

**Required Content:**
- Log file locations
- Reference to STORY-198 analysis tool
- Common troubleshooting steps
- Hook file location (`.claude/hooks/`)

---

## Running Tests

### Run All Tests
```bash
cd /mnt/c/Projects/DevForgeAI2
./devforgeai/tests/STORY-199/run-all-tests.sh
```

### Run Individual Test
```bash
cd /mnt/c/Projects/DevForgeAI2
./devforgeai/tests/STORY-199/test-ac1-readme-creation.sh
```

## Expected Results (TDD Red Phase)

All tests should **FAIL** initially because the implementation does not exist yet:
- `.claude/hooks/README.md` does not exist

After implementation, all tests should **PASS**.

## Test Output Format

Each test produces:
1. Console output with PASS/FAIL for each check
2. JSON results file: `test-acN-results.json`

**JSON Format:**
```json
{
  "test_name": "AC1: README Creation",
  "total_tests": 5,
  "passed": 5,
  "failed": 0,
  "exit_code": 0,
  "timestamp": "2026-01-10T12:00:00Z"
}
```

## Validation Checklist

- [ ] All 5 test scripts created
- [ ] run-all-tests.sh runner created
- [ ] Tests follow AAA pattern (Arrange-Act-Assert)
- [ ] Tests validate structure (not narrative content)
- [ ] Tests use grep for pattern matching
- [ ] Tests produce JSON results files
- [ ] Tests exit with proper exit codes (0=pass, 1=fail)

## Technical Notes

**Implementation Type:** Documentation (Markdown)
**Output Type:** Test Specification Document + Executable Bash Scripts

**Test Strategy:**
- Structural validation (section headers, numbered lists)
- Content presence validation (required patterns/keywords)
- NOT narrative content validation (per test-automator guidelines)

**Coverage Mapping:**

| Technical Spec ID | Test File | Test Number |
|-------------------|-----------|-------------|
| DOC-001 | test-ac1-readme-creation.sh | Test 4 |
| DOC-002 | test-ac2-safe-pattern-criteria.sh | Test 1 |
| DOC-003 | test-ac3-blocked-pattern-criteria.sh | Test 1 |
| DOC-004 | test-ac4-update-process.sh | Test 1 |
| DOC-005 | test-ac5-debugging-information.sh | Test 1 |

---

**Generated by:** test-automator subagent
**Date:** 2026-01-10
**Story Template Version:** 2.5
