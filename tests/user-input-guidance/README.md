# STORY-058: Test Suite - Documentation Updates with User Input Guidance Cross-References

## Overview

This test suite validates all acceptance criteria and technical specifications for **STORY-058: Documentation Updates with User Input Guidance Cross-References**.

The story adds learning guidance cross-references to three core documentation files:
1. **src/CLAUDE.md** - New "Learning DevForgeAI" section
2. **src/claude/memory/commands-reference.md** - User Input Guidance for 11 commands
3. **src/claude/memory/skills-reference.md** - User Input Guidance for 13 skills

**Test Framework:** Bash/Shell scripting (grep, awk, test operators)
**Test Pattern:** AAA (Arrange, Act, Assert)
**Status:** RED PHASE - All tests should initially FAIL (TDD)

---

## Test Files

### 1. test-ac1-claude-md-section.sh
**Validates AC#1: CLAUDE.md Learning Section Added**

**Tests:**
- Section header exists (`## Learning DevForgeAI`)
- Section positioned between "Quick Reference" and "Development Workflow"
- Three subsections present:
  - `### Writing Effective Feature Descriptions`
  - `### User Input Guidance Resources`
  - `### Progressive Learning Path`
- 3-5 good vs bad examples (marked with ❌/✅)
- 3 Read() commands for guidance documents
- Learning levels mentioned (basic, advanced, framework-specific)

**Exit Codes:**
- 0 = All tests passed
- 1 = One or more tests failed

**Run:**
```bash
bash tests/user-input-guidance/test-ac1-claude-md-section.sh
```

---

### 2. test-ac2-commands-cross-references.sh
**Validates AC#2: Commands Reference Cross-References Added**

**Tests:**
- All 11 commands have `### Command` sections
- Each command has `#### User Input Guidance` subsection
- Each guidance subsection has:
  - **File:** path reference
  - **Load:** Read command example
  - **Example:** usage example
- Consistent formatting across all 11 commands
- Guidance descriptions exist and are non-empty

**Tested Commands:**
- /ideate, /create-context, /create-epic, /create-sprint
- /create-story, /create-ui, /dev
- /qa, /release, /orchestrate, /audit-deferrals

**Exit Codes:**
- 0 = All tests passed
- 1 = One or more tests failed

**Run:**
```bash
bash tests/user-input-guidance/test-ac2-commands-cross-references.sh
```

---

### 3. test-ac3-skills-cross-references.sh
**Validates AC#3: Skills Reference Cross-References Added**

**Tests:**
- 13 applicable skills documented (excluding claude-code-terminal-expert)
- Each skill has `#### User Input Guidance` subsection
- Each guidance subsection has File, Load, Example structure
- Subsections appear after "Invocation" subsection
- Descriptions are skill-specific (not generic)

**Tested Skills (13 total):**
- devforgeai-ideation
- devforgeai-architecture
- devforgeai-orchestration
- devforgeai-story-creation
- devforgeai-ui-generator
- devforgeai-development
- devforgeai-qa
- devforgeai-release
- devforgeai-documentation
- devforgeai-feedback
- devforgeai-mcp-cli-converter
- devforgeai-subagent-creation
- devforgeai-rca

**Exit Codes:**
- 0 = All tests passed
- 1 = One or more tests failed

**Run:**
```bash
bash tests/user-input-guidance/test-ac3-skills-cross-references.sh
```

---

### 4. test-ac4-5-6-quality-validation.sh
**Validates AC#4, AC#5, AC#6, AC#8: Quality, Structure, and Discoverability**

**AC#4 - Cross-Reference Consistency Validation:**
- File paths exist (effective-prompting-guide.md, user-input-guidance.md, etc.)
- Load commands use Read() syntax only
- File paths use src/ prefix (not .claude/)
- No prohibited patterns (cat, @file, source, include)

**AC#5 - Discoverability Verification:**
- Learning section appears in first 400 lines of CLAUDE.md
- Clear directions provided to guidance documents
- File paths and load commands are complete

**AC#6 - Integration with Existing Structure:**
- Core sections remain (Quick Reference, Development Workflow)
- Section numbering/structure preserved
- Formatting conventions followed

**AC#8 - Documentation Quality Standards:**
- No placeholder content (TODO, TBD, FIXME, etc.)
- Examples are concrete and practical
- File paths are absolute and repository-relative
- Load commands use Read tool exclusively
- Clear language suitable for new users

**Exit Codes:**
- 0 = All tests passed
- 1 = One or more tests failed

**Run:**
```bash
bash tests/user-input-guidance/test-ac4-5-6-quality-validation.sh
```

---

### 5. test-ac7-sync-checklist.sh
**Validates AC#7: Source and Operational Sync Preparation**

**Tests:**
- Source files updated (src/CLAUDE.md, src/claude/memory/*)
- Updates present in source files, not operational files
- Sync checklist exists (.devforgeai/stories/STORY-058/sync-checklist.md)
- Checklist lists all 3 files for synchronization
- Checklist has clear source → destination mappings
- Checklist has checkbox items for tracking
- Checklist references STORY-060

**Exit Codes:**
- 0 = All tests passed
- 1 = One or more tests failed

**Run:**
```bash
bash tests/user-input-guidance/test-ac7-sync-checklist.sh
```

---

### 6. validate-cross-references.sh
**Comprehensive Cross-Reference Validation Script**

Validates AC#4 requirements in detail:

**Validations:**
1. File paths point to existing files
2. Load command syntax correct (Read tool)
3. File path format (repository-relative with src/ prefix)
4. No duplicate guidance sections
5. Terminology consistency
6. Read() command syntax usage
7. No Bash/cat in documentation examples

**Output Formats:**
- `text` (default) - Human-readable colored output
- `json` - Machine-readable JSON format
- `csv` - Comma-separated values

**Exit Codes:**
- 0 = All validations passed
- 1 = One or more validations failed

**Run:**
```bash
# Default text output
bash tests/user-input-guidance/validate-cross-references.sh

# JSON output
bash tests/user-input-guidance/validate-cross-references.sh json

# CSV output
bash tests/user-input-guidance/validate-cross-references.sh csv
```

---

## Test Execution

### Run All Tests
```bash
# Run all test suites
bash tests/user-input-guidance/test-ac1-claude-md-section.sh && \
bash tests/user-input-guidance/test-ac2-commands-cross-references.sh && \
bash tests/user-input-guidance/test-ac3-skills-cross-references.sh && \
bash tests/user-input-guidance/test-ac4-5-6-quality-validation.sh && \
bash tests/user-input-guidance/test-ac7-sync-checklist.sh && \
bash tests/user-input-guidance/validate-cross-references.sh
```

### Run Specific Test Suite
```bash
bash tests/user-input-guidance/test-ac1-claude-md-section.sh
```

### Quick Validation
```bash
bash tests/user-input-guidance/validate-cross-references.sh
```

---

## Test Status Progression

### Phase: RED (Initial - Tests Should Fail)
All tests written but implementation not started.

```
FAIL: Learning DevForgeAI section not found in CLAUDE.md
FAIL: Commands Reference cross-references incomplete
FAIL: Skills Reference cross-references incomplete
...
```

### Phase: GREEN (Tests Pass)
Implementation complete, all documentation updated.

```
PASS: Learning DevForgeAI section created
PASS: All 11 commands have User Input Guidance
PASS: All 13 skills have User Input Guidance
...
```

### Phase: REFACTOR (Quality Improvement)
Code review, documentation refinement, edge case handling.

---

## Success Criteria

All test suites pass with 0 failures:

```
AC#1: 10/10 tests pass
AC#2: 8/8 tests pass
AC#3: 9/9 tests pass
AC#4-6, #8: 18/18 tests pass
AC#7: 10/10 tests pass
Validation Script: 7/7 checks pass
```

**Total: 62/62 tests passing**

---

## Story Acceptance Criteria Coverage

| AC | Test File | Test Count | Status |
|----|-----------|-----------|--------|
| AC#1 | test-ac1-claude-md-section.sh | 10 | RED |
| AC#2 | test-ac2-commands-cross-references.sh | 8 | RED |
| AC#3 | test-ac3-skills-cross-references.sh | 9 | RED |
| AC#4 | test-ac4-5-6-quality-validation.sh | 7 | RED |
| AC#5 | test-ac4-5-6-quality-validation.sh | 4 | RED |
| AC#6 | test-ac4-5-6-quality-validation.sh | 3 | RED |
| AC#7 | test-ac7-sync-checklist.sh | 10 | RED |
| AC#8 | test-ac4-5-6-quality-validation.sh | 5 | RED |
| Validation | validate-cross-references.sh | 7 | RED |

---

## Implementation Notes

### Before Running Tests

1. **Ensure source files exist:**
   ```bash
   ls -l src/CLAUDE.md
   ls -l src/claude/memory/commands-reference.md
   ls -l src/claude/memory/skills-reference.md
   ```

2. **Ensure test scripts are executable:**
   ```bash
   chmod +x tests/user-input-guidance/*.sh
   ```

3. **Verify referenced guidance files exist:**
   ```bash
   ls -l src/claude/memory/effective-prompting-guide.md
   ls -l src/claude/memory/user-input-guidance.md
   ```

### During Implementation (TDD Cycle)

1. **Red Phase:** Run tests, verify all fail
   ```bash
   bash tests/user-input-guidance/test-ac1-claude-md-section.sh
   # All tests FAIL ✓
   ```

2. **Green Phase:** Implement features, run tests until passing
   ```bash
   # Edit src/CLAUDE.md to add Learning section
   bash tests/user-input-guidance/test-ac1-claude-md-section.sh
   # Tests PASS ✓
   ```

3. **Refactor Phase:** Improve implementation, maintain passing tests
   ```bash
   bash tests/user-input-guidance/test-ac1-claude-md-section.sh
   # Tests still PASS ✓
   ```

### After Implementation

Run full validation suite:
```bash
bash tests/user-input-guidance/validate-cross-references.sh
```

Should see:
```
Validations Passed: 7
Validations Failed: 0

All validations PASSED
✓ All file paths exist
✓ All load commands use correct syntax
✓ All file paths use repository-relative format
✓ No duplicate guidance sections
✓ Terminology consistent
```

---

## Edge Cases Handled

1. **Section ordering conflicts** - Tests verify header placement using anchors, not line numbers
2. **Commands without applicable guidance** - Tests verify N/A sections for /audit-deferrals, /audit-budget, /rca
3. **Skill invocation chains** - Tests verify upstream guidance references for downstream skills
4. **Documentation sync conflicts** - Tests verify source files updated, not operational files
5. **Terminology consistency** - Tests validate approved terms across all 3 files

---

## Test Data Requirements

### Prerequisite Stories
- STORY-052: User-Facing Prompting Guide (effective-prompting-guide.md required)
- STORY-053: Framework-Internal Guidance Reference (user-input-guidance.md required)
- STORY-054: claude-code-terminal-expert Enhancement (existing skill documented)

### File References
All tests assume these files exist and are properly formatted:
- src/CLAUDE.md (source file to update)
- src/claude/memory/commands-reference.md (source file to update)
- src/claude/memory/skills-reference.md (source file to update)
- src/claude/memory/effective-prompting-guide.md (existing reference)
- src/claude/memory/user-input-guidance.md (existing reference)

---

## Troubleshooting

### Tests Fail: "File does not exist"
**Issue:** Referenced documentation files not found
**Solution:** Verify STORY-052 and STORY-053 are complete before implementing STORY-058

### Tests Fail: "Section not found"
**Issue:** Implementation incomplete
**Solution:** Add required sections to documentation files per acceptance criteria

### Tests Fail: "Pattern not found"
**Issue:** Formatting inconsistent with test expectations
**Solution:** Ensure subsection structure matches: **File:** → **Load:** → **Example:**

### Validation Script Shows Failures
**Issue:** Cross-references invalid or incorrectly formatted
**Solution:** Check file paths are absolute (src/ prefix), load commands use Read(file_path=...)

---

## Test Maintenance

### When Adding New Commands
1. Update commands-reference.md with User Input Guidance section
2. Add command to test-ac2-commands-cross-references.sh COMMANDS array
3. Run tests to verify new command subsection

### When Adding New Skills
1. Update skills-reference.md with User Input Guidance section
2. Add skill to test-ac3-skills-cross-references.sh APPLICABLE_SKILLS array
3. Run tests to verify new skill subsection

### When Changing File Paths
1. Update validate-cross-references.sh with new paths
2. Run validation script to verify all paths exist
3. Update test expectations if needed

---

## References

- **Story Definition:** .ai_docs/Stories/STORY-058-documentation-updates.story.md
- **Technical Specification:** STORY-058 Technical Specification section (YAML in story file)
- **Test Framework:** Bash/Shell (grep, awk, wc, test operators)
- **Pattern:** AAA (Arrange, Act, Assert)
- **TDD Workflow:** Red → Green → Refactor

---

## Author Notes

**Created:** 2025-01-22
**Test Framework:** Bash/Shell scripting
**Test Pattern:** AAA (Arrange, Act, Assert)
**Status:** RED PHASE - All 62 tests initially fail (no implementation yet)

This test suite follows TDD principles:
1. Tests written BEFORE implementation
2. All tests fail initially (RED phase)
3. Implementation makes tests pass (GREEN phase)
4. Refactoring improves code while keeping tests green (REFACTOR phase)

---

**End of Test Suite Documentation**
