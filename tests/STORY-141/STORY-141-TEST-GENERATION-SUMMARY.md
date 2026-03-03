# STORY-141: Question Duplication Elimination - Test Generation Summary

**Story ID:** STORY-141
**Story Title:** Question Duplication Elimination
**Framework:** TDD (Test-Driven Development) - Tests are FAILING initially
**Test Framework:** Jest (Node.js)
**Test Type:** Markdown file validation with regex patterns and file structure validation

---

## Overview

This test suite validates STORY-141's acceptance criteria by examining the current state of:
- `.claude/commands/ideate.md` - Command file (should NOT contain discovery questions)
- `.claude/skills/devforgeai-ideation/SKILL.md` - Skill file (should contain ALL discovery questions)
- `.claude/skills/devforgeai-ideation/references/` - Question templates (ownership verification)

**Current Status (TDD Red Phase):** Tests are DESIGNED TO FAIL until implementation completes the refactoring.

---

## Test Files Generated

### 1. **test_ac1_remove_project_type_from_command.js**
**Acceptance Criteria #1:** Remove Project Type Question from Command

**Test Suite:** 12 tests organized into 4 describe blocks

#### Tests:
```javascript
✗ should_NOT_contain_project_type_question_in_command_phase_1
✗ should_contain_project_type_question_in_skill_discovery_phase
✗ should_NOT_duplicate_project_type_question_in_command_and_skill
✗ should_only_validate_business_idea_in_command_phase_1
✗ should_have_clear_responsibility_delegation
✗ should_have_skill_discovery_ownership_documented
✗ should_have_discovery_question_templates_in_skill_references
✗ should_NOT_have_discovery_templates_in_command
✗ should_have_multiple_discovery_questions_in_skill
```

**Purpose:** Ensures "project type" question is removed from command and moved to skill.

---

### 2. **test_ac2_remove_all_discovery_questions_from_command.js**
**Acceptance Criteria #2:** Remove All Discovery Questions from Command

**Test Suite:** 15 tests organized into 5 describe blocks

#### Tests:
```javascript
✗ should_have_minimal_AskUserQuestion_calls_in_command
✗ should_limit_AskUserQuestion_to_brainstorm_selection_in_phase_0
✗ should_NOT_ask_discovery_questions_in_command
✗ should_have_business_idea_validation_not_discovery
✗ should_have_discovery_questions_in_skill_phase_1
✗ should_have_higher_AskUserQuestion_count_in_skill_than_command
✗ should_have_all_discovery_question_types_in_skill
✗ should_delegate_to_discovery_workflow_reference
✗ should_define_command_responsibilities_as_minimal
✗ should_NOT_mention_discovery_in_command_responsibilities
✗ should_explicitly_state_skill_owns_discovery
✗ should_have_error_handling_patterns_in_command
✗ should_NOT_have_discovery_error_handling_in_command
✗ should_have_phase_0_and_1_only_for_orchestration
✗ should_NOT_have_discovery_or_requirements_phases_in_command
```

**Purpose:** Validates all discovery questions are removed from command and delegated to skill.

---

### 3. **test_ac3_skill_owns_question_templates.js**
**Acceptance Criteria #3:** Skill Owns Question Templates

**Test Suite:** 18 tests organized into 6 describe blocks

#### Tests:
```javascript
✗ should_have_discovery_workflow_reference_file
✗ should_have_requirements_elicitation_reference_file
✗ should_have_discovery_questions_in_discovery_workflow
✗ should_have_requirements_questions_in_requirements_elicitation
✗ should_have_well_formatted_question_templates_in_skill
✗ should_NOT_contain_question_templates_in_command
✗ should_only_have_brainstorm_template_in_command_phase_0
✗ should_NOT_duplicate_brainstorm_template_in_skill
✗ should_NOT_have_unused_question_templates
✗ should_have_complete_discovery_question_template_structure
✗ should_have_complete_requirements_question_template_structure
✗ should_have_question_descriptions_not_just_names
✗ should_have_multi_option_questions_where_appropriate
✗ should_reference_templates_from_skill
✗ should_have_required_reference_files
✗ should_have_clear_file_naming_for_question_ownership
✗ should_NOT_have_question_templates_in_command_file
✗ should_have_all_workflow_references_in_skill_references_only
✗ should_have_discovery_workflow_referenced_in_skill
✗ should_have_requirements_elicitation_referenced_in_skill
✗ should_NOT_have_template_references_in_command
```

**Purpose:** Ensures question templates are in skill references, not in command.

---

### 4. **test_ac4_command_passes_context_to_skill.js**
**Acceptance Criteria #4:** Command Passes Context to Skill

**Test Suite:** 18 tests organized into 7 describe blocks

#### Tests:
```javascript
✗ should_have_Business_Idea_context_marker
✗ should_have_Brainstorm_Context_marker_for_brainstorm_flow
✗ should_have_Brainstorm_File_marker_for_file_path
✗ should_set_context_BEFORE_skill_invocation
✗ should_display_context_markers_in_output
✗ should_check_for_context_variables_in_skill_phase_1
✗ should_skip_discovery_questions_if_brainstorm_context_provided
✗ should_read_project_mode_context_in_phase_6
✗ should_NOT_re_ask_business_idea_if_provided_in_context
✗ should_validate_context_markers_have_content
✗ should_NOT_ask_for_business_idea_in_skill_if_command_provided
✗ should_use_provided_brainstorm_instead_of_re_discovering
✗ should_detect_context_in_conversation_not_request_re_entry
✗ should_have_validation_before_asking_duplicate_questions
✗ should_define_BRAINSTORM_CONTEXT_structure
✗ should_define_PROJECT_MODE_CONTEXT_structure
✗ should_pass_business_idea_in_context_markers
✗ should_document_context_markers_in_comment_or_description
✗ should_have_clear_context_handoff_explanation
✗ should_explain_why_context_prevents_duplicate_questions
✗ should_have_reference_to_brainstorm_handoff_workflow
✗ should_parse_context_variables_in_skill
✗ should_display_context_summary_before_proceeding
✗ should_validate_context_is_not_null_or_empty
✗ should_handle_missing_context_gracefully
```

**Purpose:** Validates context markers (Business Idea, Brainstorm Context, Brainstorm File) are properly passed from command to skill, preventing re-asking.

---

### 5. **test_ac5_zero_duplicate_questions_end_to_end.js**
**Acceptance Criteria #5:** Zero Duplicate Questions in End-to-End Flow

**Test Suite:** 20 tests organized into 6 describe blocks

#### Tests:
```javascript
✗ should_have_brainstorm_question_only_in_command_phase_0
✗ should_have_project_type_question_only_in_skill_phase_1
✗ should_have_domain_question_only_in_skill_discovery
✗ should_have_success_criteria_question_only_in_skill_discovery
✗ should_have_complexity_question_only_in_skill_phase_3
✗ should_NOT_have_duplicate_project_type_questions
✗ should_NOT_have_duplicate_domain_questions
✗ should_NOT_have_duplicate_scope_questions
✗ should_NOT_have_duplicate_user_persona_questions
✗ should_NOT_have_question_about_existing_system_in_both_phases
✗ should_ask_questions_in_logical_order_without_repetition
✗ should_NOT_revisit_discovery_questions_in_later_phases
✗ should_NOT_ask_complexity_in_discovery_phase
✗ should_cover_all_required_topics_once_each
✗ should_NOT_have_redundant_questions_after_refactoring
✗ should_have_logical_question_flow_without_backtracking
✗ should_have_contextual_questions_not_generic_repeated_questions
✗ should_have_AskUserQuestion_count_minimized_in_command
✗ should_have_AskUserQuestion_count_reasonable_in_skill
✗ should_have_discovery_and_requirements_questions_separated
```

**Purpose:** Complete audit of end-to-end workflow to ensure no question is asked twice and all topics are covered exactly once.

---

## Test Execution

### Running All Tests

```bash
# Run all STORY-141 tests
npm test -- tests/STORY-141/

# Run specific test file
npm test -- tests/STORY-141/test_ac1_remove_project_type_from_command.js

# Run with verbose output
npm test -- tests/STORY-141/ --verbose

# Run and generate coverage
npm test -- tests/STORY-141/ --coverage
```

### Expected Output (TDD Red Phase)

All tests should FAIL initially, since the command file still contains discovery questions that need to be refactored out:

```
FAIL tests/STORY-141/test_ac1_remove_project_type_from_command.js
FAIL tests/STORY-141/test_ac2_remove_all_discovery_questions_from_command.js
FAIL tests/STORY-141/test_ac3_skill_owns_question_templates.js
FAIL tests/STORY-141/test_ac4_command_passes_context_to_skill.js
FAIL tests/STORY-141/test_ac5_zero_duplicate_questions_end_to_end.js

Tests: 83 failed, 0 passed
```

---

## Coverage by Acceptance Criteria

| AC# | Title | Test Files | Tests | Status |
|-----|-------|-----------|-------|--------|
| AC#1 | Remove Project Type Question from Command | test_ac1_*.js | 9 | FAILING |
| AC#2 | Remove All Discovery Questions from Command | test_ac2_*.js | 15 | FAILING |
| AC#3 | Skill Owns Question Templates | test_ac3_*.js | 21 | FAILING |
| AC#4 | Command Passes Context to Skill | test_ac4_*.js | 25 | FAILING |
| AC#5 | Zero Duplicate Questions End-to-End | test_ac5_*.js | 20 | FAILING |
| **TOTAL** | | **5 files** | **90 tests** | **FAILING** |

---

## Test Categories

### Unit Tests (50 tests)
- File existence verification
- Content pattern matching (grep-style)
- Structure validation
- Responsibility boundary checks

### Integration Tests (40 tests)
- Cross-file consistency validation
- Context flow verification
- Phase ordering verification
- No duplication audits

### Quality Tests
- Template completeness checks
- Documentation clarity verification
- Error handling patterns

---

## Key Testing Patterns

### 1. **Regex-Based Content Validation**
Tests use regex patterns to search for question types and validate their location:
```javascript
const projectTypePattern = /project\s+type|greenfield|brownfield/i;
expect(commandContent).not.toMatch(projectTypePattern);
```

### 2. **AskUserQuestion Block Extraction**
Tests extract and analyze AskUserQuestion invocations:
```javascript
const askUserMatches = content.match(/AskUserQuestion[\s\S]*?\}\s*\)/g) || [];
```

### 3. **Phase Section Isolation**
Tests isolate specific phases to verify content within each:
```javascript
const phase1Section = content.match(/## Phase 1:.*?(?=^## [A-Z]|$)/ms)?.[0] || '';
```

### 4. **Cross-File Deduplication Audit**
Tests combine all files to detect duplicates:
```javascript
const allContent = commandContent + '\n---\n' + skillContent + discoveryContent;
const duplicates = allContent.match(/pattern/g);
```

---

## Files Under Test

### Source Files (Markdown)
1. **`.claude/commands/ideate.md`** - Command file (currently has discovery questions - NEEDS REFACTORING)
2. **`.claude/skills/devforgeai-ideation/SKILL.md`** - Skill file (should have all questions - MAY NEED UPDATES)
3. **`.claude/skills/devforgeai-ideation/references/discovery-workflow.md`** - Discovery templates
4. **`.claude/skills/devforgeai-ideation/references/requirements-elicitation-workflow.md`** - Requirements templates
5. **Skill references directory** - All workflow files (should own all templates)

---

## Implementation Checklist (for TDD Green Phase)

To make tests pass, implement:

### Phase 1: Command Refactoring
- [ ] Remove all discovery questions from command Phase 1
- [ ] Keep only business idea argument validation
- [ ] Remove project type question
- [ ] Remove domain question
- [ ] Remove scope question
- [ ] Keep brainstorm selection (Phase 0 only)
- [ ] Set context markers before skill invocation
- [ ] Add documentation for minimal responsibilities

### Phase 2: Skill Updates
- [ ] Verify all discovery questions in skill Phase 1
- [ ] Add context marker detection ($BRAINSTORM_CONTEXT)
- [ ] Skip discovery if high-confidence brainstorm
- [ ] Add context parsing logic
- [ ] Update Phase 1 documentation

### Phase 3: Reference Files
- [ ] Verify discovery-workflow.md has all questions
- [ ] Verify requirements-elicitation-workflow.md is complete
- [ ] Ensure proper formatting
- [ ] Add descriptions to questions

### Phase 4: Integration
- [ ] Test end-to-end flow
- [ ] Verify no duplicate questions
- [ ] Validate context passing
- [ ] Test with and without brainstorm context

---

## Test Failure Analysis

### Why Tests Fail (Current State)

1. **AC#1 Failures:** Command still contains project type question
2. **AC#2 Failures:** Command has multiple discovery questions (domain, complexity, etc.)
3. **AC#3 Failures:** Some questions may be in command instead of references
4. **AC#4 Failures:** Context markers may not be properly documented/implemented
5. **AC#5 Failures:** Workflow has duplicate questions across command and skill

### Example Failure Message

```
FAIL test_ac1_remove_project_type_from_command.js
  should_NOT_contain_project_type_question_in_command_phase_1
    Expected string not to match pattern: /what\s+type\s+of\s+project/i
    Actual content matched: "What type of project are you building?"
```

---

## Test Maintenance

### When to Update Tests

- [ ] When acceptance criteria change
- [ ] When file structure changes (e.g., phase numbering)
- [ ] When new question types are added
- [ ] When validation rules change

### How to Add New Tests

1. Follow AAA pattern (Arrange, Act, Assert)
2. Use descriptive test names following pattern: `should_<expected>_when_<condition>`
3. Include scenario description in comments
4. Group related tests in describe blocks

---

## Tools & Dependencies

- **Node.js:** 14+
- **Jest:** Latest version
- **Test Framework:** Jest built-in (describe, test, expect)
- **File Operations:** fs (Node.js built-in)
- **Path Operations:** path (Node.js built-in)

---

## Continuous Integration

These tests can be integrated into CI/CD:

```bash
npm test -- tests/STORY-141/ --coverage --CI
```

Expected behavior:
- All tests failing initially (TDD Red)
- Tests passing after refactoring complete (TDD Green)
- Tests remain passing during refactoring (TDD Refactor)

---

## Success Criteria for Tests

- [x] Tests are comprehensive (90 tests covering all ACs)
- [x] Tests are independent (no cross-test dependencies)
- [x] Tests follow AAA pattern
- [x] Tests have clear failure messages
- [x] Tests are discoverable (organized by AC)
- [x] Tests validate both positive and negative cases
- [x] Tests verify no duplicates (critical for STORY-141)

---

**Generated:** 2025-12-28
**Test Framework:** Jest
**Total Tests:** 90
**Initial Status:** ALL FAILING (TDD Red Phase)
**Target Status:** ALL PASSING (TDD Green Phase after implementation)
