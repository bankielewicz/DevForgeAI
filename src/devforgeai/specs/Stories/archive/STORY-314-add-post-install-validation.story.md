---
id: STORY-314
title: Add Post-Install Validation Command
type: feature
epic: EPIC-050
sprint: Backlog
status: Dev Complete
points: 3
depends_on: ["STORY-308", "STORY-310"]
priority: Medium
created: 2026-01-25
updated: 2026-01-25
format_version: "2.7"
---

# STORY-314: Add Post-Install Validation Command

## Description

**As a** DevForgeAI user,
**I want** a single command to verify my installation is correct,
**so that** I can self-diagnose installation issues.

**Command:** `devforgeai-validate validate-installation [--project-root=.]`

---

## Provenance

```xml
<provenance>
  <origin document="EPIC-050" section="Friction Points">
    <quote>"FP-11: No post-install validation command - MEDIUM priority, 3 points"</quote>
    <line_reference>EPIC-050-installation-process-improvements.epic.md</line_reference>
    <quantified_impact>Users have no way to self-diagnose installation issues</quantified_impact>
  </origin>
  <decision rationale="Single command for all checks">
    <selected>Add validate-installation subcommand to existing CLI</selected>
    <rejected alternative="separate script">Fragmentation of CLI tools</rejected>
    <trade_off>CLI binary must be installed first, but provides comprehensive validation</trade_off>
  </decision>
</provenance>
```

---

## Acceptance Criteria

### AC#1: All 6 checks pass on valid installation

```xml
<acceptance_criteria id="AC1">
  <given>A correctly installed DevForgeAI project</given>
  <when>User runs devforgeai-validate validate-installation</when>
  <then>All 6 checks pass and report success</then>
  <verification>
    <source_files>
      <file hint="Validation command">src/claude/scripts/devforgeai_cli/commands/validate_installation.py</file>
    </source_files>
    <test_file>tests/devforgeai_cli/test_validate_installation.py</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Clear error for incomplete installation

```xml
<acceptance_criteria id="AC2">
  <given>An incomplete installation (missing CLI)</given>
  <when>User runs validate-installation</when>
  <then>Clear error message indicates what is missing</then>
  <verification>
    <source_files>
      <file hint="Validation command">src/claude/scripts/devforgeai_cli/commands/validate_installation.py</file>
    </source_files>
  </verification>
</acceptance_criteria>
```

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "CLI"
      name: "Validate Installation Command"
      file_path: "src/claude/scripts/devforgeai_cli/commands/validate_installation.py"
      requirements:
        - id: "CLI-001"
          description: "Check CLI availability (devforgeai-validate --version)"
          testable: true
          test_requirement: "Test: Verify CLI check returns pass/fail"
          priority: "Critical"
        - id: "CLI-002"
          description: "Check context files (6 files in devforgeai/specs/context/)"
          testable: true
          test_requirement: "Test: Verify context file check returns pass/fail"
          priority: "Critical"
        - id: "CLI-003"
          description: "Check hook installation (.git/hooks/pre-commit exists)"
          testable: true
          test_requirement: "Test: Verify hook check returns pass/fail"
          priority: "High"
        - id: "CLI-004"
          description: "Check PYTHONPATH configuration"
          testable: true
          test_requirement: "Test: Verify PYTHONPATH check returns pass/fail"
          priority: "Medium"
        - id: "CLI-005"
          description: "Check Git repository (.git/ exists)"
          testable: true
          test_requirement: "Test: Verify Git check returns pass/fail"
          priority: "High"
        - id: "CLI-006"
          description: "Check settings file (.claude/settings.json exists)"
          testable: true
          test_requirement: "Test: Verify settings check returns pass/fail"
          priority: "Medium"

    - type: "CLI"
      name: "CLI Entry Point Update"
      file_path: "src/claude/scripts/devforgeai_cli/cli.py"
      requirements:
        - id: "CLI-007"
          description: "Add validate-installation subcommand"
          testable: true
          test_requirement: "Test: devforgeai-validate validate-installation --help works"
          priority: "Critical"

  business_rules:
    - id: "BR-001"
      rule: "Each check must return pass/fail with clear reason"
      test_requirement: "Test: All checks produce human-readable output"
    - id: "BR-002"
      rule: "Actionable fix must be suggested for each failure"
      test_requirement: "Test: Failed checks include 'To fix:' instructions"
    - id: "BR-003"
      rule: "Exit code 0 only if all checks pass"
      test_requirement: "Test: Any failure results in non-zero exit code"
```

---

## Checks to Implement

| # | Check | Pass Condition | Fail Message |
|---|-------|----------------|--------------|
| 1 | CLI availability | `devforgeai-validate --version` succeeds | "CLI not installed. Run: pip install -e .claude/scripts/" |
| 2 | Context files | 6 files in `devforgeai/specs/context/` | "Missing context files: [list]. Run: /create-context" |
| 3 | Hook installation | `.git/hooks/pre-commit` exists | "Hooks not installed. Run: bash .claude/scripts/install_hooks.sh" |
| 4 | PYTHONPATH | CLI imports succeed | "PYTHONPATH not configured. See coding-standards.md" |
| 5 | Git repository | `.git/` exists | "Not a Git repository. Run: git init" |
| 6 | Settings file | `.claude/settings.json` exists | "Settings missing. Run installer to create" |

---

## Output Format

```
DevForgeAI Installation Validation
==================================

[✓] CLI available: devforgeai-validate 0.1.0
[✓] Context files: 6/6 present
[✓] Git hooks: pre-commit installed
[✓] PYTHONPATH: configured
[✓] Git repository: initialized
[✓] Settings file: present

Result: PASS (6/6 checks passed)
```

**On failure:**
```
DevForgeAI Installation Validation
==================================

[✓] CLI available: devforgeai-validate 0.1.0
[✗] Context files: 4/6 present
    Missing: anti-patterns.md, dependencies.md
    To fix: Run /create-context to generate missing files
[✓] Git hooks: pre-commit installed
[✓] PYTHONPATH: configured
[✓] Git repository: initialized
[✓] Settings file: present

Result: FAIL (5/6 checks passed)
```

---

## Definition of Done

### Implementation
- [x] Command implemented with all 6 checks - Completed: validate_installation.py with 6 check functions
- [x] Clear pass/fail output for each check - Completed: ValidationResult dataclass with passed/message fields
- [x] Actionable error messages with fix instructions - Completed: fix_instruction field with "To fix:" prefix
- [x] Exit code 0 on success, non-zero on any failure - Completed: exit_code=0 if success else 1

### Testing
- [x] Unit tests for each individual check - Completed: 21 tests in test_validate_installation.py
- [x] Integration test for full validation run - Completed: TestCLIIntegration class
- [x] Test with intentionally broken installation - Completed: TestIncompleteInstallation class (6 tests)

### Documentation
- [x] Command documented in CLI --help - Completed: validate-installation subparser in cli.py
- [x] Added to INSTALL.md as verification step - Completed: installer/INSTALL.md updated

---

## AC Verification Checklist

### AC#1: All 6 checks pass on valid installation
- [x] validate_installation.py created - **Phase:** 3 - **Evidence:** .claude/scripts/devforgeai_cli/commands/validate_installation.py
- [x] CLI subcommand added - **Phase:** 3 - **Evidence:** cli.py lines 357-375, 548-553
- [x] All 6 checks implemented - **Phase:** 3 - **Evidence:** 6 check functions in validate_installation.py
- [x] Tests pass on valid install - **Phase:** 4 - **Evidence:** 21/21 tests pass (pytest output)

### AC#2: Clear error for incomplete installation
- [x] Error messages include what's missing - **Phase:** 3 - **Evidence:** ValidationResult.message includes details
- [x] Fix instructions provided - **Phase:** 3 - **Evidence:** ValidationResult.fix_instruction with "To fix:" prefix
- [x] Tests verify error output - **Phase:** 4 - **Evidence:** TestIncompleteInstallation class (6 tests pass)

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent (claude/opus)
**Implemented:** 2026-01-27
**Commit:** pending
**Branch:** main

- [x] Command implemented with all 6 checks - Completed: validate_installation.py with 6 check functions
- [x] Clear pass/fail output for each check - Completed: ValidationResult dataclass with passed/message fields
- [x] Actionable error messages with fix instructions - Completed: fix_instruction field with "To fix:" prefix
- [x] Exit code 0 on success, non-zero on any failure - Completed: exit_code=0 if success else 1
- [x] Unit tests for each individual check - Completed: 21 tests in test_validate_installation.py
- [x] Integration test for full validation run - Completed: TestCLIIntegration class
- [x] Test with intentionally broken installation - Completed: TestIncompleteInstallation class (6 tests)
- [x] Command documented in CLI --help - Completed: validate-installation subparser in cli.py
- [x] Added to INSTALL.md as verification step - Completed: installer/INSTALL.md updated

### TDD Workflow Summary

**Phase 02 (Red): Test-First Design**
- Generated 21 tests covering all acceptance criteria
- Tests placed in tests/devforgeai_cli/test_validate_installation.py
- Test framework: pytest

**Phase 03 (Green): Implementation**
- Implemented validate_installation.py (413 lines)
- 6 check functions: CLI, context files, hooks, PYTHONPATH, Git, settings
- All 21 tests passing (100% pass rate)

**Phase 04 (Refactor): Code Quality**
- Code review: APPROVED
- No refactoring needed - code already clean
- Cyclomatic complexity: all functions below 10

**Phase 05 (Integration): Full Validation**
- Full test suite executed (21/21 pass)
- CLI integration verified
- Context validation PASSED

**Phase 06 (Deferral Challenge): DoD Validation**
- All DoD items validated
- 0 deferrals
- INSTALL.md documentation added

### Files Created/Modified

**Created:**
- .claude/scripts/devforgeai_cli/commands/validate_installation.py
- tests/devforgeai_cli/__init__.py
- tests/devforgeai_cli/test_validate_installation.py

**Modified:**
- .claude/scripts/devforgeai_cli/cli.py (added validate-installation subcommand)
- installer/INSTALL.md (added validate-installation documentation)

---

## Change Log

**Current Status:** Dev Complete

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-25 | claude/opus | Created | Story created from EPIC-050 plan | STORY-314-add-post-install-validation.story.md |
| 2026-01-26 | claude/opus | Phase 02 | TDD Red: 21 tests written, all skipped (awaiting implementation) | tests/devforgeai_cli/test_validate_installation.py |
| 2026-01-27 | claude/opus | Phase 03 | TDD Green: Implementation complete, 21/21 tests pass | validate_installation.py, cli.py |
| 2026-01-27 | claude/opus | Phase 04 | TDD Refactor: Code review APPROVED, no refactoring needed | No changes |
| 2026-01-27 | claude/opus | DoD Update (Phase 07) | Development complete, DoD validated | STORY-314.story.md |

---

## Notes

**Dependencies:** STORY-308 (binary name fix) and STORY-310 (PYTHONPATH consolidation) should be completed first so the validation command checks for the correct binary name and PYTHONPATH patterns.

**References:**
- src/claude/scripts/devforgeai_cli/cli.py
- src/claude/scripts/devforgeai_cli/commands/
