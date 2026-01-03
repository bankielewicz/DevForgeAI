# STORY-167 Test Suite

Tests for STORY-167: RCA-012 Story Template Version Tracking

## Quick Start

Run all tests:
```bash
bash test-ac1-template-version-metadata.sh
bash test-ac2-changelog-section.sh
bash test-ac3-generated-stories-include-version.sh
```

Run from project root:
```bash
cd /mnt/c/Projects/DevForgeAI2
bash tests/STORY-167/test-ac1-template-version-metadata.sh
bash tests/STORY-167/test-ac2-changelog-section.sh
bash tests/STORY-167/test-ac3-generated-stories-include-version.sh
```

## Test Files

### test-ac1-template-version-metadata.sh
Tests that the story template YAML frontmatter contains `template_version` and `last_updated` metadata.

**AC#1:** Template Version in Frontmatter
- Given: the story template
- When: I review the header section
- Then: there should be `template_version` and `last_updated` metadata

**Tests:** 8
- Template file exists
- Frontmatter has template_version field
- Frontmatter has last_updated field
- Version follows semantic versioning (X.Y or X.Y.Z)
- Date is in YYYY-MM-DD format
- Frontmatter has proper delimiters (---)
- template_version value is not empty
- last_updated value is not empty

**Status:** 2/8 PASS (template file exists, delimiters OK; missing metadata fields)

### test-ac2-changelog-section.sh
Tests that the story template includes a changelog documenting template evolution.

**AC#2:** Changelog Section
- Given: the story template
- When: I look for version history
- Then: there should be a changelog documenting versions 1.0, 2.0, 2.1

**Tests:** 10
- Changelog section exists
- Version 1.0 is documented
- Version 2.0 is documented
- Version 2.1 is documented
- Version 1.0 has description
- Version 2.0 has description
- Version 2.1 has description
- RCA-012 is referenced
- Changelog is markdown formatted
- v2.1 mentions AC header checkbox removal

**Status:** 10/10 PASS (changelog is complete and well-documented)

### test-ac3-generated-stories-include-version.sh
Tests that newly created stories include `format_version: "2.1"` in YAML frontmatter.

**AC#3:** Generated Stories Include Version
- Given: a newly created story
- When: I check the YAML frontmatter
- Then: `format_version: "2.1"` should be present

**Tests:** 10
- Template has format_version field
- format_version is set to "2.1"
- format_version is in YAML frontmatter (not in body)
- format_version is before story content
- Generated story includes format_version
- format_version is a quoted string
- All stories have consistent format_version
- YAML syntax is proper
- format_version is not commented
- format_version is in YAML frontmatter

**Status:** 3/10 PASS (field exists but value is 2.5 not 2.1; needs to be in frontmatter)

## Test Results Summary

| AC | Tests | Pass | Fail | Status |
|----|-------|------|------|--------|
| AC#1 | 8 | 2 | 6 | FAILING (needs frontmatter metadata) |
| AC#2 | 10 | 10 | 0 | PASSING (already satisfied) |
| AC#3 | 10 | 3 | 7 | FAILING (format_version value wrong) |
| **Total** | **28** | **15** | **13** | **50% PASS** |

## Red Phase Status

All tests are FAILING as expected (Red phase - TDD).

Implementation gaps:
1. Template frontmatter needs `template_version: "2.1"` field
2. Template frontmatter needs `last_updated: "2025-12-31"` field
3. Template format_version value needs to be `"2.1"` (currently `"2.5"`)

## Next Steps (Green Phase)

Implement the following to make tests pass:

1. **Edit:** `.claude/skills/devforgeai-story-creation/assets/templates/story-template.md`
2. **Lines 1-5 should be:**
   ```yaml
   ---
   template_version: "2.1"
   last_updated: "2025-12-31"
   format_version: "2.1"
   ---
   ```

3. **Run tests again** to verify all pass

## Test Framework

- **Language:** Bash Shell Script
- **Assertions:** assert_equal, assert_not_empty, assert_file_exists, assert_contains
- **Pattern:** AAA (Arrange-Act-Assert)
- **Exit Code:** 0 for all pass, 1 if any test fails
- **Output:** Colored terminal (✓ pass, ✗ fail)

## Viewing Test Output

Colored output shows:
- `✓` Green = Test passed
- `✗` Red = Test failed

Example:
```
========================================================================
Test Suite: AC#1 - Template Version in Frontmatter
Story: STORY-167 - RCA-012 Story Template Version Tracking
========================================================================

✓ Template file should exist at expected location
✗ Frontmatter should contain 'template_version' field
  Looking for: template_version

...

========================================================================
Test Results Summary
========================================================================
Tests run:    8
Tests passed: 2
Tests failed: 6

RESULT: FAILED
```

## Notes for Developers

1. **Test Independence:** Tests can run in any order, no setup required
2. **No External Dependencies:** Uses only Bash builtins and grep
3. **Temporary Files:** Tests create temp directory and clean up on exit
4. **Grep Patterns:** Extended regex used for matching version strings
5. **YAML Parsing:** Simple grep-based parsing of YAML frontmatter

## File Locations

- **Story:** `/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-167-rca-012-template-version-tracking.story.md`
- **Template:** `/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-story-creation/assets/templates/story-template.md`
- **Tests:** `/mnt/c/Projects/DevForgeAI2/tests/STORY-167/`
- **Report:** `/mnt/c/Projects/DevForgeAI2/STORY-167-TEST-GENERATION-REPORT.md`

## Related Stories

- **STORY-166:** RCA-012 AC Header Documentation Clarification
- **STORY-222:** Plan File Knowledge Base Extraction
- **STORY-152:** Unified Story Change Log Tracking

## Questions?

See the full test generation report:
`/mnt/c/Projects/DevForgeAI2/STORY-167-TEST-GENERATION-REPORT.md`
