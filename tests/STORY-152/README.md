# STORY-152 Test Suite

Comprehensive test suite for **STORY-152: Unified Story Change Log Tracking with Subagent Attribution**

## Overview

This test suite validates the implementation of a unified Change Log section in story files that tracks all modifications with subagent attribution. Tests are organized by acceptance criteria and technical specifications.

## Test Coverage

### Acceptance Criteria Tests (7 test suites)

#### AC#1: Story Template Updated with Change Log Section
**File:** `test-ac1-story-template-changelog-section.sh`

Tests that the story template:
- Contains `## Change Log` section (not `## Workflow Status`)
- Has `**Current Status:** Backlog` header
- Contains 5-column table: Date | Author | Phase/Action | Change | Files Affected
- Includes initial entry with author `claude/story-requirements-analyst`

**Test Count:** 12 tests

#### AC#2: Shared Changelog Reference Guide Created
**File:** `test-ac2-changelog-reference-guide.sh`

Tests that the reference guide at `.claude/references/changelog-update-guide.md`:
- Exists and is valid markdown
- Documents format specification with 5-column table
- Specifies author attribution patterns
- Contains Edit tool snippets
- Documents timestamp format (YYYY-MM-DD HH:MM)

**Test Count:** 12 tests

#### AC#3: devforgeai-development Skill Appends Changelog Entries
**File:** `test-ac3-dev-skill-changelog-integration.sh`

Tests that the Dev skill:
- References the shared changelog guide
- Appends changelog entries at each TDD phase
- Uses correct subagent authors (e.g., `claude/test-automator`)
- Updates `dod-update-workflow.md` to use Change Log (not Workflow Status)

**Test Count:** 12 tests

#### AC#4: devforgeai-qa Skill Appends Changelog Entry
**File:** `test-ac4-qa-skill-changelog-integration.sh`

Tests that the QA skill:
- References the shared changelog guide
- Contains changelog append instruction in Phase 3.4
- Uses author `claude/qa-result-interpreter`
- Documents QA result format (Coverage %, violations)
- Supports both Light and Deep QA modes

**Test Count:** 12 tests

#### AC#5: devforgeai-release Skill Appends Changelog and Archives Story
**File:** `test-ac5-release-skill-changelog-integration.sh`

Tests that the Release skill:
- References the shared changelog guide
- Contains changelog append instruction in Phase 5
- Uses author `claude/deployment-engineer`
- Documents story archiving to `devforgeai/specs/Stories/archive/`
- Updates project CHANGELOG.md
- Updates source-tree.md with archive directory

**Test Count:** 12 tests

#### AC#6: Project CHANGELOG.md Created with Keep a Changelog Format
**File:** `test-ac6-project-changelog-format.sh`

Tests that CHANGELOG.md:
- Contains `## [Unreleased]` section
- Has version sections with date (e.g., `## [X.Y.Z] - YYYY-MM-DD`)
- Uses Keep a Changelog v1.1.0 format
- Contains story entries: `- Feature description ([STORY-XXX])`
- Has reference links: `[STORY-XXX]: devforgeai/specs/Stories/archive/...`

**Test Count:** 12 tests

#### AC#7: Backward Compatible with Existing Stories
**File:** `test-ac7-backward-compatibility.sh`

Tests that:
- Existing stories without Change Log section are detected
- Missing section is created with "Story Migrated" entry
- Existing story content is preserved
- All skills have backward compatibility checks
- Shared guide documents migration procedure

**Test Count:** 12 tests

### Technical Specification Tests (2 test suites)

#### Data Model: Changelog Entry Format Validation
**File:** `test-changelog-entry-format-validation.sh`

Validates the changelog entry data model:
- 5-column markdown table format (DM-001)
- Author pattern validation regex (DM-002)
- Change field max 100 characters (DM-003)
- Timestamp format YYYY-MM-DD HH:MM (CFG-004)

**Test Count:** 12 tests

#### Service: Story Template Version 2.5
**File:** `test-story-template-version.sh`

Validates template updates:
- Change Log section present
- Current Status field present
- 5-column table with correct headers
- Template version 2.5 indicator
- Workflow Status section removed
- Essential sections preserved

**Test Count:** 12 tests

## Running Tests

### Run All Tests
```bash
bash /mnt/c/Projects/DevForgeAI2/tests/STORY-152/run-all-tests.sh
```

### Run Individual Test Suite
```bash
# AC#1
bash /mnt/c/Projects/DevForgeAI2/tests/STORY-152/test-ac1-story-template-changelog-section.sh

# AC#2
bash /mnt/c/Projects/DevForgeAI2/tests/STORY-152/test-ac2-changelog-reference-guide.sh

# AC#3
bash /mnt/c/Projects/DevForgeAI2/tests/STORY-152/test-ac3-dev-skill-changelog-integration.sh

# AC#4
bash /mnt/c/Projects/DevForgeAI2/tests/STORY-152/test-ac4-qa-skill-changelog-integration.sh

# AC#5
bash /mnt/c/Projects/DevForgeAI2/tests/STORY-152/test-ac5-release-skill-changelog-integration.sh

# AC#6
bash /mnt/c/Projects/DevForgeAI2/tests/STORY-152/test-ac6-project-changelog-format.sh

# AC#7
bash /mnt/c/Projects/DevForgeAI2/tests/STORY-152/test-ac7-backward-compatibility.sh

# Tech Spec: Format Validation
bash /mnt/c/Projects/DevForgeAI2/tests/STORY-152/test-changelog-entry-format-validation.sh

# Tech Spec: Template Version
bash /mnt/c/Projects/DevForgeAI2/tests/STORY-152/test-story-template-version.sh
```

## Test Design Principles

### TDD Red Phase
All tests are designed to **fail initially** (Red phase) since the features don't exist yet. This follows Test-Driven Development principles:
1. **Red:** Tests fail (no implementation)
2. **Green:** Implement features to pass tests
3. **Refactor:** Improve code quality while keeping tests green

### AAA Pattern
Each test follows the Arrange-Act-Assert pattern:
- **Arrange:** Set up test conditions
- **Act:** Execute the behavior being tested
- **Assert:** Verify the expected outcome

### Test Independence
- Tests can run in any order
- No shared state between tests
- Each test is self-contained

### File-Based Testing
- Tests use Bash shell scripts (per DevForgeAI pattern)
- Use native tools: Read, Write, Edit, Grep
- No external dependencies required

## Files Being Tested

### Core Implementation Files
- `.claude/references/changelog-update-guide.md` - Shared reference guide (AC#2)
- `.claude/skills/devforgeai-story-creation/assets/templates/story-template.md` - Updated template (AC#1)
- `.claude/skills/devforgeai-development/SKILL.md` - Dev skill with changelog appends (AC#3)
- `.claude/skills/devforgeai-development/references/dod-update-workflow.md` - DoD workflow update (AC#3)
- `.claude/skills/devforgeai-qa/SKILL.md` - QA skill with changelog appends (AC#4)
- `.claude/skills/devforgeai-release/SKILL.md` - Release skill with changelog appends (AC#5)
- `devforgeai/specs/context/source-tree.md` - Archive directory documentation (AC#5)
- `CHANGELOG.md` - Project changelog (AC#6)

## Test Statistics

| Category | Count |
|----------|-------|
| Acceptance Criteria Test Suites | 7 |
| Technical Specification Test Suites | 2 |
| Total Test Suites | 9 |
| Tests per Suite | 12 |
| Total Test Cases | 108 |

## Expected Output Format

### Individual Test Success
```
TEST N: Test description... PASS
```

### Individual Test Failure
```
TEST N: Test description... FAIL
  Expected: What should have been found
```

### Test Suite Summary
```
================================================================
SUMMARY: AC#X Tests
================================================================
PASSED: 12
FAILED: 0
TOTAL:  12

All AC#X tests PASSED
```

## CI/CD Integration

To integrate into CI/CD pipeline:

```bash
#!/bin/bash
set -e  # Exit on first failure

# Run test suite
bash /mnt/c/Projects/DevForgeAI2/tests/STORY-152/run-all-tests.sh

# Optional: Generate coverage report
echo "All STORY-152 tests passed"
```

## Debugging Failed Tests

### Check File Existence
If a file is not found, verify the path:
```bash
ls -la /mnt/c/Projects/DevForgeAI2/.claude/references/changelog-update-guide.md
```

### Check File Content
Use grep to search for expected patterns:
```bash
grep "## Change Log" /mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-story-creation/assets/templates/story-template.md
```

### Manual Validation
Review the relevant file to ensure content matches expectations:
```bash
cat /mnt/c/Projects/DevForgeAI2/.claude/references/changelog-update-guide.md
```

## Test Maintenance

### Adding New Tests
1. Create new test file: `test-name.sh`
2. Add shebang: `#!/bin/bash`
3. Set error handling: `set -euo pipefail`
4. Follow existing test structure with 12 tests
5. Update `run-all-tests.sh` to include new test
6. Update this README

### Updating Existing Tests
- Modify assertion logic as needed
- Keep test names descriptive
- Update test count if adding/removing tests
- Document changes in README

## References

- [STORY-152 Story File](devforgeai/specs/Stories/STORY-152-unified-story-changelog-tracking.story.md)
- [Keep a Changelog Format](https://keepachangelog.com/en/1.1.0/)
- [Test-Driven Development](https://en.wikipedia.org/wiki/Test-driven_development)

## Notes

- All test scripts are executable Bash files
- Tests validate both existence and content of files
- Backward compatibility is a key validation criterion
- Tests follow DevForgeAI framework patterns (Bash, native tools)
