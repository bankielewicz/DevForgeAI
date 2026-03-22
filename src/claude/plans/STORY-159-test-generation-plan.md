# STORY-159: Test Generation Plan

**Story**: STORY-159 - Create /create-stories-from-rca Command Shell
**Status**: TEST GENERATION (TDD Red Phase)
**Created**: 2025-12-31
**Test Framework**: Bash shell scripts (per source-tree.md)
**Test Location**: `/mnt/c/Projects/DevForgeAI2/tests/STORY-159/`

---

## Overview

This plan details the test-first (TDD Red phase) approach for STORY-159. Tests are generated BEFORE implementation of the command file at `.claude/commands/create-stories-from-rca.md`.

---

## Acceptance Criteria Analysis

### AC#1: Create Command File with YAML Frontmatter
- **Given**: Need for new slash command
- **When**: Creating the command
- **Then**: File exists at `.claude/commands/create-stories-from-rca.md` with valid YAML frontmatter
- **Required Fields**: name, description, argument-hint, allowed-tools, model

### AC#2: Implement Argument Parsing and Validation
- **Given**: User runs `/create-stories-from-rca RCA-022`
- **When**: Command executes
- **Then**: RCA ID parsed, validated (format RCA-NNN), file located in `devforgeai/RCA/`

### AC#3: Implement Help Text
- **Given**: User runs `--help` or `help`
- **When**: Command executes
- **Then**: Help text displayed with usage, examples, related commands

### AC#4: Handle Invalid Arguments
- **Given**: Invalid RCA ID or missing argument
- **When**: Command executes
- **Then**: Clear error with format guidance and list of available RCAs

### AC#5: Orchestrate to Story Creation Components
- **Given**: Valid RCA ID provided
- **When**: Command executes
- **Then**: Orchestrates Parse RCA → Select Recommendations → Create Stories → Link Back

---

## Technical Requirements Summary

- **Component Type**: Slash Command (Markdown-based)
- **Path**: `.claude/commands/create-stories-from-rca.md`
- **Allowed Tools**: Read, Write, Edit, Glob, Grep, AskUserQuestion, Skill, TodoWrite
- **Model**: sonnet
- **YAML Frontmatter Required**: name, description, argument-hint, allowed-tools, model
- **Business Rule BR-001**: File < 15,000 characters (lean orchestration)
- **Business Rule BR-002**: Case-insensitive RCA ID (rca-022 → RCA-022)
- **Business Rule BR-003**: File existence check before proceeding

---

## Test Strategy

### Test Framework
- **Language**: Bash shell scripts (DevForgeAI standard for Markdown component testing)
- **Test Location**: `/mnt/c/Projects/DevForgeAI2/tests/STORY-159/`
- **Test Files**:
  - `test-ac1-command-file-creation.sh` - Command file exists and has valid YAML
  - `test-ac2-argument-parsing.sh` - RCA ID validation and file location
  - `test-ac3-help-text.sh` - Help output displays correctly
  - `test-ac4-invalid-arguments.sh` - Error handling with clear messages
  - `test-ac5-orchestration.sh` - Skill orchestration chain

### Test Pyramid Distribution
- **Unit Tests (70%)**: Argument parsing, file existence, YAML validation
- **Integration Tests (20%)**: Command execution with real RCA files
- **E2E Tests (10%)**: Full workflow with orchestration

---

## Test Cases

### Test File 1: test-ac1-command-file-creation.sh

**AC#1: Create Command File with YAML Frontmatter**

#### Test Case 1.1: Command file exists at correct location
```bash
test_ac1_command_file_exists() {
    # Test that .claude/commands/create-stories-from-rca.md exists
    EXPECTED_FILE=".claude/commands/create-stories-from-rca.md"

    # This test will FAIL before implementation
    # Expected failure: File not found
}
```

#### Test Case 1.2: YAML frontmatter contains required fields
```bash
test_ac1_yaml_frontmatter_valid() {
    # Test YAML frontmatter has: name, description, argument-hint, allowed-tools, model

    # This test will FAIL before implementation
    # Expected failure: File missing or incomplete frontmatter
}
```

#### Test Case 1.3: name field matches command
```bash
test_ac1_name_field_correct() {
    # Test that name: field equals "create-stories-from-rca"

    # This test will FAIL before implementation
    # Expected failure: Field missing or incorrect value
}
```

#### Test Case 1.4: description field is present and non-empty
```bash
test_ac1_description_field_present() {
    # Test that description: exists and not empty

    # This test will FAIL before implementation
    # Expected failure: Field missing
}
```

#### Test Case 1.5: argument-hint field is present
```bash
test_ac1_argument_hint_field_present() {
    # Test that argument-hint: exists with format hint (RCA-NNN [--help])

    # This test will FAIL before implementation
    # Expected failure: Field missing
}
```

#### Test Case 1.6: allowed-tools field includes required tools
```bash
test_ac1_allowed_tools_includes_required() {
    # Test that allowed-tools: includes Read, Write, Edit, Glob, Grep, AskUserQuestion, Skill, TodoWrite

    # This test will FAIL before implementation
    # Expected failure: Field missing or incomplete
}
```

#### Test Case 1.7: model field is set to "sonnet"
```bash
test_ac1_model_field_correct() {
    # Test that model: equals "sonnet"

    # This test will FAIL before implementation
    # Expected failure: Field missing or incorrect value
}
```

---

### Test File 2: test-ac2-argument-parsing.sh

**AC#2: Implement Argument Parsing and Validation**

#### Test Case 2.1: Accepts RCA-NNN format
```bash
test_ac2_accepts_valid_rca_format() {
    # Test parsing RCA-022 (uppercase format)
    # Extract and validate that RCA ID is parsed correctly

    # This test will FAIL before implementation
    # Expected failure: No argument parsing logic
}
```

#### Test Case 2.2: Accepts case-insensitive RCA ID
```bash
test_ac2_accepts_lowercase_rca_format() {
    # Test parsing rca-022 (lowercase - BR-002)
    # Verify converts to RCA-022

    # This test will FAIL before implementation
    # Expected failure: No case normalization logic
}
```

#### Test Case 2.3: Locates RCA file in devforgeai/RCA/
```bash
test_ac2_locates_rca_file() {
    # Test that RCA-022 locates devforgeai/RCA/RCA-022-*.md
    # Verify file existence check (BR-003)

    # This test will FAIL before implementation
    # Expected failure: No file location logic
}
```

#### Test Case 2.4: Validates RCA-NNN format (3 digits)
```bash
test_ac2_validates_rca_format_digits() {
    # Test RCA-022 is valid (3 digits)
    # Test RCA-22 is invalid (2 digits)
    # Test RCA-0022 is invalid (4 digits)

    # This test will FAIL before implementation
    # Expected failure: No format validation
}
```

#### Test Case 2.5: Rejects invalid format gracefully
```bash
test_ac2_rejects_invalid_format() {
    # Test that INVALID-022, rca22, RCA022, etc. are rejected

    # This test will FAIL before implementation
    # Expected failure: No validation
}
```

---

### Test File 3: test-ac3-help-text.sh

**AC#3: Implement Help Text**

#### Test Case 3.1: --help flag displays help
```bash
test_ac3_help_flag_displays_help() {
    # Test command with --help shows help text
    # Verify output contains "usage", "create-stories-from-rca", and examples

    # This test will FAIL before implementation
    # Expected failure: No help implementation
}
```

#### Test Case 3.2: help argument displays help
```bash
test_ac3_help_argument_displays_help() {
    # Test command with "help" argument shows help text

    # This test will FAIL before implementation
    # Expected failure: No help implementation
}
```

#### Test Case 3.3: Help text includes usage information
```bash
test_ac3_help_includes_usage() {
    # Test help output contains usage pattern
    # Example: "/create-stories-from-rca RCA-022"

    # This test will FAIL before implementation
    # Expected failure: No usage documentation
}
```

#### Test Case 3.4: Help text includes examples
```bash
test_ac3_help_includes_examples() {
    # Test help output contains at least one example command

    # This test will FAIL before implementation
    # Expected failure: No examples in help
}
```

#### Test Case 3.5: Help text mentions related commands
```bash
test_ac3_help_mentions_related_commands() {
    # Test help text references related commands
    # Examples: /rca, /brainstorm, /create-story

    # This test will FAIL before implementation
    # Expected failure: No related commands mentioned
}
```

---

### Test File 4: test-ac4-invalid-arguments.sh

**AC#4: Handle Invalid Arguments**

#### Test Case 4.1: Missing argument shows error
```bash
test_ac4_missing_argument_shows_error() {
    # Test command with no argument shows error message
    # Error should include format guidance: "Expected: RCA-NNN"

    # This test will FAIL before implementation
    # Expected failure: No error handling
}
```

#### Test Case 4.2: Error message includes format guidance
```bash
test_ac4_error_includes_format_guidance() {
    # Test error message explains expected format (RCA-NNN)

    # This test will FAIL before implementation
    # Expected failure: No format guidance in error
}
```

#### Test Case 4.3: Error message lists available RCAs
```bash
test_ac4_error_lists_available_rcas() {
    # Test error message when RCA not found includes list of available RCAs
    # Should show: "Available RCAs: RCA-001, RCA-002, ..."

    # This test will FAIL before implementation
    # Expected failure: No RCA listing in error
}
```

#### Test Case 4.4: Non-existent RCA ID shows clear error
```bash
test_ac4_nonexistent_rca_shows_error() {
    # Test RCA-999 (doesn't exist) shows error with available RCAs

    # This test will FAIL before implementation
    # Expected failure: No validation for RCA existence
}
```

#### Test Case 4.5: Invalid format shows actionable guidance
```bash
test_ac4_invalid_format_actionable() {
    # Test various invalid formats show guidance to user
    # Examples: "invalid-022", "RCA-22", "rca_022"

    # This test will FAIL before implementation
    # Expected failure: No format validation
}
```

---

### Test File 5: test-ac5-orchestration.sh

**AC#5: Orchestrate to Story Creation Components**

#### Test Case 5.1: Command invokes Skill(devforgeai-story-creation)
```bash
test_ac5_invokes_story_creation_skill() {
    # Test that command calls Skill(command="devforgeai-story-creation .....")
    # Verify orchestration structure in command file

    # This test will FAIL before implementation
    # Expected failure: No skill invocation
}
```

#### Test Case 5.2: Orchestration includes STORY-155 (RCA Parser)
```bash
test_ac5_orchestration_includes_story_155() {
    # Test that command or skill references STORY-155 for RCA parsing
    # Verify orchestration mentions parse RCA phase

    # This test will FAIL before implementation
    # Expected failure: No STORY-155 reference
}
```

#### Test Case 5.3: Orchestration includes STORY-156 (Recommendation Selector)
```bash
test_ac5_orchestration_includes_story_156() {
    # Test that command or skill references STORY-156 for recommendation selection
    # Verify orchestration mentions select recommendations phase

    # This test will FAIL before implementation
    # Expected failure: No STORY-156 reference
}
```

#### Test Case 5.4: Orchestration includes STORY-157 (Batch Story Creator)
```bash
test_ac5_orchestration_includes_story_157() {
    # Test that command or skill references STORY-157 for story creation
    # Verify orchestration mentions create stories phase

    # This test will FAIL before implementation
    # Expected failure: No STORY-157 reference
}
```

#### Test Case 5.5: Orchestration includes STORY-158 (RCA Story Linker)
```bash
test_ac5_orchestration_includes_story_158() {
    # Test that command or skill references STORY-158 for linking back
    # Verify orchestration mentions link RCA to stories phase

    # This test will FAIL before implementation
    # Expected failure: No STORY-158 reference
}
```

#### Test Case 5.6: Orchestration preserves lean pattern (< 15K characters)
```bash
test_ac5_command_respects_size_limit() {
    # Test that command file is < 15,000 characters (BR-001)
    # Count characters in final command file

    # This test will FAIL before implementation
    # Expected failure: File doesn't exist or exceeds size
}
```

---

## Expected Test Failures (Before Implementation)

All tests will FAIL initially because:

1. **test-ac1-command-file-creation.sh**: File `.claude/commands/create-stories-from-rca.md` doesn't exist
   - Test 1.1: FileNotFound error
   - Tests 1.2-1.7: File missing, cannot validate YAML fields

2. **test-ac2-argument-parsing.sh**: No argument parsing logic in command
   - Tests 2.1-2.5: Cannot parse or validate RCA ID format
   - No file location mechanism

3. **test-ac3-help-text.sh**: No help text implementation
   - Tests 3.1-3.5: Help text not implemented or incomplete

4. **test-ac4-invalid-arguments.sh**: No error handling
   - Tests 4.1-4.5: Missing argument handling, no error messages
   - No RCA listing in error output

5. **test-ac5-orchestration.sh**: No skill orchestration
   - Tests 5.1-5.6: No Skill() invocations
   - No STORY references
   - File doesn't exist (exceeds size requirement by default)

---

## Test Commands

### Run All Tests
```bash
bash /mnt/c/Projects/DevForgeAI2/tests/STORY-159/test-ac1-command-file-creation.sh
bash /mnt/c/Projects/DevForgeAI2/tests/STORY-159/test-ac2-argument-parsing.sh
bash /mnt/c/Projects/DevForgeAI2/tests/STORY-159/test-ac3-help-text.sh
bash /mnt/c/Projects/DevForgeAI2/tests/STORY-159/test-ac4-invalid-arguments.sh
bash /mnt/c/Projects/DevForgeAI2/tests/STORY-159/test-ac5-orchestration.sh
```

### Run Single Test File
```bash
bash /mnt/c/Projects/DevForgeAI2/tests/STORY-159/test-ac1-command-file-creation.sh
```

### Run Single Test Case
```bash
bash /mnt/c/Projects/DevForgeAI2/tests/STORY-159/test-ac1-command-file-creation.sh -t test_ac1_command_file_exists
```

---

## Test Coverage Summary

| Acceptance Criteria | Test Cases | Expected Failures |
|-------------------|------------|------------------|
| AC#1 (File + YAML) | 7 tests | 7 failures (file missing) |
| AC#2 (Arg Parsing) | 5 tests | 5 failures (no parsing logic) |
| AC#3 (Help Text) | 5 tests | 5 failures (no help impl) |
| AC#4 (Error Handling) | 5 tests | 5 failures (no error handling) |
| AC#5 (Orchestration) | 6 tests | 6 failures (no skill calls) |
| **TOTAL** | **28 tests** | **28 failures** |

---

## Next Steps

1. **Phase 02 (TDD Red - Current)**: Implement tests in bash scripts
2. **Phase 03 (TDD Green)**: Implement command file to pass tests
3. **Phase 04 (Refactor)**: Clean up command code
4. **Phase 05 (Integration)**: Verify cross-component interactions
5. **Phase 06 (Deferral)**: Validate any deferred items
6. **Phase 07 (DoD)**: Update Definition of Done
7. **Phase 08 (Git)**: Commit changes
8. **Phase 09 (Feedback)**: Collect feedback
9. **Phase 10 (Result)**: Report results

---

## References

- Story: `/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-159-create-stories-from-rca-command.story.md`
- Source Tree: `/mnt/c/Projects/DevForgeAI2/devforgeai/specs/context/source-tree.md`
- Tech Stack: `/mnt/c/Projects/DevForgeAI2/devforgeai/specs/context/tech-stack.md`
- Test Location Rule: Tests in `/mnt/c/Projects/DevForgeAI2/tests/STORY-159/` per source-tree.md
- Bash Testing: DevForgeAI standard for Markdown component testing

---

## Progress Tracking

- [x] Analysis of story acceptance criteria complete
- [x] Test strategy defined (Bash shell scripts)
- [x] Test location validated against source-tree.md
- [ ] Test file 1 (AC#1) generated
- [ ] Test file 2 (AC#2) generated
- [ ] Test file 3 (AC#3) generated
- [ ] Test file 4 (AC#4) generated
- [ ] Test file 5 (AC#5) generated
- [ ] All tests run and confirmed failing (TDD Red)
- [ ] Ready for Phase 03 (Implementation)
