---
id: STORY-308
title: Fix Binary Name Mismatch in Python CLI
type: bugfix
epic: EPIC-050
sprint: Backlog
status: QA Approved
points: 2
depends_on: []
priority: High
created: 2026-01-25
updated: 2026-01-25
format_version: "2.7"
---

# STORY-308: Fix Binary Name Mismatch in Python CLI

## Description

**As a** DevForgeAI user,
**I want** the Python CLI binary name to be consistent across setup.py, cli.py, and reference files,
**so that** Phase 01 preflight CLI detection works correctly.

**Problem (from RCA-026):**
- `setup.py` line 41 registers: `'devforgeai-validate=devforgeai_cli.cli:main'`
- `cli.py` line 31 declares: `prog='devforgeai'` (WRONG)
- Phase 01 checks for `devforgeai` command (WRONG)
- Result: CLI detection fails even when correctly installed

---

## Provenance

```xml
<provenance>
  <origin document="RCA-026" section="Root Cause Analysis">
    <quote>"Binary name mismatch between setup.py registration (devforgeai-validate) and cli.py prog declaration (devforgeai)"</quote>
    <line_reference>devforgeai/RCA/RCA-026-phase-cli-module-path-incorrect.md</line_reference>
    <quantified_impact>100% of Phase 01 preflight checks fail with properly installed CLI</quantified_impact>
  </origin>
  <decision rationale="Standardize on setup.py name">
    <selected>Update cli.py and references to use 'devforgeai-validate'</selected>
    <rejected>Change setup.py to use 'devforgeai' (would require pip reinstall for all users)</rejected>
    <trade_off>Reference file updates required, but no user reinstallation needed</trade_off>
  </decision>
</provenance>
```

---

## Acceptance Criteria

### AC#1: CLI prog name matches setup.py entry point

```xml
<acceptance_criteria id="AC1">
  <given>The Python CLI is installed via pip install -e .claude/scripts/</given>
  <when>User runs devforgeai-validate --help</when>
  <then>The help text shows prog='devforgeai-validate' (not 'devforgeai')</then>
  <verification>
    <source_files>
      <file hint="CLI entry point">src/claude/scripts/devforgeai_cli/cli.py</file>
    </source_files>
    <test_file>tests/devforgeai_cli/test_cli_binary_name.py</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Phase 01 preflight checks for correct command

```xml
<acceptance_criteria id="AC2">
  <given>Phase 01 preflight check is running</given>
  <when>The CLI detection step executes</when>
  <then>It checks for 'devforgeai-validate' command (not 'devforgeai')</then>
  <verification>
    <source_files>
      <file hint="Phase 01 preflight">src/claude/skills/devforgeai-development/phases/phase-01-preflight.md</file>
    </source_files>
  </verification>
</acceptance_criteria>
```

---

### AC#3: All reference files use consistent command name

```xml
<acceptance_criteria id="AC3">
  <given>All reference files that check for CLI existence</given>
  <when>They are updated</when>
  <then>They check for 'devforgeai-validate' consistently</then>
  <verification>
    <source_files>
      <file hint="CLI check reference">src/claude/skills/devforgeai-development/references/preflight/01.0.5-cli-check.md</file>
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
    - type: "Configuration"
      name: "CLI Entry Point"
      file_path: "src/claude/scripts/devforgeai_cli/cli.py"
      requirements:
        - id: "CLI-001"
          description: "Change prog='devforgeai' to prog='devforgeai-validate'"
          testable: true
          test_requirement: "Test: CLI --help output shows 'usage: devforgeai-validate'"
          priority: "Critical"
          exact_edit: |
            old: prog='devforgeai',
            new: prog='devforgeai-validate',

    - type: "Documentation"
      name: "CLI Check Reference"
      file_path: "src/claude/skills/devforgeai-development/references/preflight/01.0.5-cli-check.md"
      requirements:
        - id: "DOC-001"
          description: "Change command detection from 'devforgeai' to 'devforgeai-validate'"
          testable: true
          test_requirement: "Test: Grep for 'command -v devforgeai-validate' in file"
          priority: "Critical"
          exact_edit: |
            old: command -v devforgeai
            new: command -v devforgeai-validate
        - id: "DOC-002"
          description: "Change version check from 'devforgeai --version' to 'devforgeai-validate --version'"
          testable: true
          test_requirement: "Test: Grep for 'devforgeai-validate --version' in file"
          priority: "Critical"
          exact_edit: |
            old: devforgeai --version
            new: devforgeai-validate --version
        - id: "DOC-003"
          description: "Update echo message to show correct binary name"
          testable: true
          test_requirement: "Test: Grep for 'devforgeai-validate CLI' in file"
          priority: "High"
          exact_edit: |
            old: DEVFORGEAI_VERSION=$(devforgeai --version
            new: DEVFORGEAI_VERSION=$(devforgeai-validate --version

  business_rules:
    - id: "BR-001"
      rule: "CLI binary name must match setup.py entry_points registration"
      test_requirement: "Test: Verify setup.py and cli.py use identical command name"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Reliability"
      requirement: "Phase 01 preflight CLI detection must pass when CLI is installed"
      metric: "100% detection rate for properly installed CLI"
      test_requirement: "Test: Install CLI, run phase 01, verify detection passes"
```

---

## Files to Modify

1. `src/claude/scripts/devforgeai_cli/cli.py` - Change `prog='devforgeai'` to `prog='devforgeai-validate'`
2. `src/claude/skills/devforgeai-development/references/preflight/01.0.5-cli-check.md` - Update 3 occurrences:
   - Line 13: `command -v devforgeai` → `command -v devforgeai-validate`
   - Line 20: `devforgeai --version` → `devforgeai-validate --version`
   - Line 21: Output message to match new binary name

**Verification after changes:**
```bash
# Find any remaining incorrect references
grep -r "command -v devforgeai[^-]" .claude/
grep -r "devforgeai --version" .claude/
# Both should return empty (no matches)
```

---

## Definition of Done

### Implementation
- [x] cli.py prog name changed to 'devforgeai-validate' - **Phase 03** src/claude/scripts/devforgeai_cli/cli.py
- [x] Phase 01 preflight updated to check for 'devforgeai-validate' - **Phase 03** src/claude/skills/devforgeai-development/references/preflight/01.0.5-cli-check.md
- [x] All reference files updated consistently - **Phase 03** both src/ and .claude/ copies
- [x] No remaining references to bare 'devforgeai' command - **Phase 03** verified by tests

### Testing
- [x] Unit test verifies CLI help text shows correct prog name - **Phase 02** tests/STORY-308/test_ac1_cli_binary_name.py
- [x] Integration test verifies Phase 01 preflight passes with installed CLI - **Phase 02** tests/STORY-308/test_ac2_ac3_reference_files.py
- [x] Grep search confirms no inconsistent command references - **Phase 02** tests/STORY-308/test_ac2_ac3_reference_files.py

### Documentation
- [x] RCA-026 marked as resolved with STORY-308 reference - **Phase 06** devforgeai/RCA/RCA-026-phase-cli-module-path-incorrect.md

---

## AC Verification Checklist

### AC#1: CLI prog name matches setup.py
- [x] cli.py line 31 updated - **Phase:** 3 - **Evidence:** src/claude/scripts/devforgeai_cli/cli.py line 31: `prog='devforgeai-validate'`
- [x] Help output verified - **Phase:** 3 - **Evidence:** test_cli_help_shows_devforgeai_validate_prog_name PASSED

### AC#2: Phase 01 preflight checks correct command
- [x] preflight.md updated - **Phase:** 3 - **Evidence:** src/claude/skills/devforgeai-development/references/preflight/01.0.5-cli-check.md
- [x] Detection passes - **Phase:** 3 - **Evidence:** test_preflight_checks_for_devforgeai_validate_command PASSED

### AC#3: Reference files consistent
- [x] All files grepped - **Phase:** 3 - **Evidence:** test_no_bare_devforgeai_command_in_reference_files PASSED
- [x] Updates applied - **Phase:** 3 - **Evidence:** Both src/ and .claude/ copies updated

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-25 | claude/opus | Created | Story created from EPIC-050 plan | STORY-308-fix-binary-name-mismatch.story.md |
| 2026-01-26 | claude/opus | Phase 02 | TDD Red: Created failing tests (7 tests, all fail) | tests/STORY-308/*.py |
| 2026-01-26 | claude/opus | Phase 03 | TDD Green: Implementation complete (7 tests, all pass) | src/claude/scripts/devforgeai_cli/cli.py, src/claude/skills/.../01.0.5-cli-check.md |
| 2026-01-26 | claude/opus | Phase 04 | TDD Refactor: Code review passed, no refactoring needed | - |
| 2026-01-26 | claude/opus | Phase 06 | Deferral: No deferrals, RCA-026 resolved | devforgeai/RCA/RCA-026-phase-cli-module-path-incorrect.md |
| 2026-01-26 | claude/opus | Phase 07 | DoD Update: All items complete, Implementation Notes added | STORY-308-fix-binary-name-mismatch.story.md |
| 2026-01-26 | claude/opus | Phase 08 | Git Commit: 5bf80ca3 (9 files, 991 insertions) | All STORY-308 files |
| 2026-01-26 | claude/qa-result-interpreter | QA Deep | PASSED: Tests 7/7, Validators 2/2, 0 violations | devforgeai/qa/reports/STORY-308-qa-report.md |

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent (claude/opus)
**Implemented:** 2026-01-26
**Commit:** 5bf80ca3
**Branch:** main

- [x] cli.py prog name changed to 'devforgeai-validate' - Completed: src/claude/scripts/devforgeai_cli/cli.py line 31 updated
- [x] Phase 01 preflight updated to check for 'devforgeai-validate' - Completed: src/claude/skills/devforgeai-development/references/preflight/01.0.5-cli-check.md updated
- [x] All reference files updated consistently - Completed: Both src/ and .claude/ copies synchronized
- [x] No remaining references to bare 'devforgeai' command - Completed: Verified by 7 passing tests
- [x] Unit test verifies CLI help text shows correct prog name - Completed: tests/STORY-308/test_ac1_cli_binary_name.py
- [x] Integration test verifies Phase 01 preflight passes with installed CLI - Completed: tests/STORY-308/test_ac2_ac3_reference_files.py
- [x] Grep search confirms no inconsistent command references - Completed: tests/STORY-308/test_ac2_ac3_reference_files.py
- [x] RCA-026 marked as resolved with STORY-308 reference - Completed: devforgeai/RCA/RCA-026-phase-cli-module-path-incorrect.md

### TDD Workflow Summary

**Phase 02 (Red): Test-First Design**
- Generated 7 comprehensive tests covering all 3 acceptance criteria
- Tests placed in tests/STORY-308/
- Test files: test_ac1_cli_binary_name.py, test_ac2_ac3_reference_files.py

**Phase 03 (Green): Implementation**
- Updated cli.py prog name from 'devforgeai' to 'devforgeai-validate'
- Updated 01.0.5-cli-check.md with correct command references
- All 7 tests passing (100% pass rate)

**Phase 04 (Refactor): Code Quality**
- No refactoring needed (minimal string change bug fix)
- Code review passed: APPROVED

**Phase 05 (Integration): Full Validation**
- All 7 tests passing
- AC compliance verification passed (2x - Phase 4.5 and 5.5)

**Phase 06 (Deferral Challenge): DoD Validation**
- All Definition of Done items validated
- 0 deferrals
- RCA-026 marked as resolved

### Files Created/Modified

**Modified:**
- src/claude/scripts/devforgeai_cli/cli.py
- src/claude/skills/devforgeai-development/references/preflight/01.0.5-cli-check.md
- .claude/scripts/devforgeai_cli/cli.py (operational copy)
- .claude/skills/devforgeai-development/references/preflight/01.0.5-cli-check.md (operational copy)
- devforgeai/RCA/RCA-026-phase-cli-module-path-incorrect.md

**Created:**
- tests/STORY-308/test_ac1_cli_binary_name.py
- tests/STORY-308/test_ac2_ac3_reference_files.py

---

## Notes

**Related RCA:** RCA-026: Phase CLI Module Path Incorrect

**References:**
- devforgeai/RCA/RCA-026-phase-cli-module-path-incorrect.md
- src/claude/scripts/setup.py (entry_points definition)
