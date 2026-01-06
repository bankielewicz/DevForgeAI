# STORY-178 Test Suite

## Story: Document Specification File Testing Pattern in Test-Automator

**Story Type:** DOCUMENTATION
**Story Points:** 1
**Estimated Hours:** 15 minutes

## Purpose

Tests validate that the `test-automator.md` agent file includes documentation for testing Markdown specification files (skills/commands) using structural validation rather than brittle text matching.

## Acceptance Criteria Mapping

| AC | Test File | Description |
|----|-----------|-------------|
| AC-1 | `test_ac1_spec_file_testing_section.sh` | Specification File Testing section exists in test-automator.md |
| AC-2 | `test_ac2_structural_testing_guidance.sh` | Guidance for testing section headers, phase markers documented |
| AC-3 | `test_ac3_tool_invocation_guidance.sh` | Guidance for testing AskUserQuestion, Read, Write references documented |
| AC-4 | `test_ac4_anti_pattern_documented.sh` | "Avoid testing for specific comment text" anti-pattern documented |
| AC-5 | `test_ac5_example_patterns.sh` | Example test patterns for Markdown commands included |

## Running Tests

```bash
# Run all tests
./tests/STORY-178/run_all_tests.sh

# Run individual AC tests
./tests/STORY-178/test_ac1_spec_file_testing_section.sh
./tests/STORY-178/test_ac2_structural_testing_guidance.sh
./tests/STORY-178/test_ac3_tool_invocation_guidance.sh
./tests/STORY-178/test_ac4_anti_pattern_documented.sh
./tests/STORY-178/test_ac5_example_patterns.sh
```

## Test Strategy

Since STORY-178 is a DOCUMENTATION story (not code implementation), tests validate:

1. **Structural Presence**: The new section exists with correct header
2. **Content Validation**: Required guidance topics are documented
3. **Anti-Pattern Documentation**: Warning against brittle text testing
4. **Example Quality**: Code examples demonstrate the pattern

### Test Design Principles

These tests follow the same principle they document:

- **Test structure, not text**: Tests use `grep` patterns for headers and keywords
- **Avoid brittle matching**: No exact text string matches that would break on rewording
- **Validate presence of concepts**: Check that topics are covered, not specific wording

## Expected Results

### TDD Red Phase (Before Implementation)
All tests should FAIL because the "Specification File Testing" section does not exist yet.

### TDD Green Phase (After Implementation)
All tests should PASS after adding ~40-50 lines of documentation to test-automator.md.

## Target File

**File to modify:** `.claude/agents/test-automator.md`

**Content to add:** Approximately 40-50 lines including:
1. Section header: `### Specification File Testing (Markdown Commands/Skills)`
2. Structural element testing guidance
3. Tool invocation testing guidance
4. Anti-pattern documentation
5. Example test patterns

## Notes

- Tests are designed to be resilient to documentation rewording
- Tests validate concepts are present, not exact phrasing
- Run `run_all_tests.sh` for consolidated output
