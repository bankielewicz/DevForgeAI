---
id: STORY-254
title: Update phase_commands.py Import
type: feature
epic: None
sprint: Backlog
status: Backlog
points: 2
depends_on: ["STORY-253"]
priority: High
assigned_to: Unassigned
created: 2026-01-12
format_version: "2.5"
source_rca: RCA-001
source_recommendation: REC-2
---

# Story: Update phase_commands.py Import

## Description

**As a** CLI package maintainer,
**I want** to simplify the `_get_phase_state()` function in `phase_commands.py` by using relative imports instead of sys.path manipulation,
**so that** the import path is clear, maintainable, and follows Python packaging best practices after STORY-253 implements PhaseState in the correct package location.

## Acceptance Criteria

### AC#1: Relative import replaces sys.path manipulation

**Given** STORY-253 has been completed and PhaseState is available at `.claude/scripts/devforgeai_cli/phase_state.py`
**When** the `_get_phase_state()` function in `phase_commands.py` is updated
**Then** the function uses `from ..phase_state import PhaseState` (relative import) instead of sys.path.insert() and `from installer.phase_state import PhaseState`

---

### AC#2: Function behavior remains unchanged

**Given** the refactored `_get_phase_state()` function
**When** called with a valid project_root parameter
**Then** it returns a PhaseState instance with the same behavior as before (no behavior change, only import path change)

---

### AC#3: All phase commands still work correctly

**Given** the updated import in `_get_phase_state()`
**When** all phase command functions are invoked (phase_init, phase_check, phase_complete, phase_status, phase_record, phase_observe)
**Then** all commands execute without import errors and maintain existing functionality

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service"
      name: "PhaseCommandsRefactor"
      file_path: ".claude/scripts/devforgeai_cli/commands/phase_commands.py"
      interface: "_get_phase_state() helper function"
      lifecycle: "N/A (function refactoring)"
      dependencies:
        - "..phase_state.PhaseState (NEW relative import)"
      requirements:
        - id: "SVC-001"
          description: "Replace sys.path manipulation with relative import"
          testable: true
          test_requirement: "Test: Import succeeds with from ..phase_state import PhaseState"
          priority: "Critical"
        - id: "SVC-002"
          description: "Function returns PhaseState instance unchanged"
          testable: true
          test_requirement: "Test: _get_phase_state('.') returns PhaseState instance"
          priority: "Critical"
        - id: "SVC-003"
          description: "All phase commands work after refactor"
          testable: true
          test_requirement: "Test: Run all 6 phase commands without ImportError"
          priority: "Critical"
        - id: "SVC-004"
          description: "Remove unused sys import if applicable"
          testable: true
          test_requirement: "Test: Check sys usage, remove if not needed elsewhere"
          priority: "Low"

  business_rules:
    - id: "BR-001"
      rule: "Import path must be relative (from ..phase_state)"
      trigger: "Module import"
      validation: "Code inspection"
      error_handling: "ImportError if incorrect path"
      test_requirement: "Test: Verify import statement in code"
      priority: "Critical"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Import latency"
      metric: "< 5ms per import (no sys.path overhead)"
      test_requirement: "Test: Time _get_phase_state() call"
      priority: "Medium"
    - id: "NFR-002"
      category: "Maintainability"
      requirement: "Code simplicity"
      metric: "Function reduced from 8 lines to 3 lines"
      test_requirement: "Test: Line count verification"
      priority: "High"
```

## Technical Limitations

```yaml
technical_limitations: []
```

## Non-Functional Requirements

### Performance
- Import latency: < 5ms (faster than sys.path manipulation)
- No sys.path modification overhead

### Maintainability
- Code reduced from 8 lines to 3 lines
- Follows Python packaging best practices (PEP 328)
- Platform-agnostic (no path string operations)

### Compatibility
- Python 3.0+ (relative imports standard)
- No new dependencies

## Edge Cases

1. **PhaseState module not found:** ImportError raised immediately (fail-fast, desired behavior)
2. **Circular import risk:** Verify phase_state.py has no imports from commands module
3. **Package structure:** Ensure `__init__.py` exists in devforgeai_cli
4. **STORY-253 dependency:** This story must wait for STORY-253 completion

## Data Validation Rules

| Element | Rule |
|---------|------|
| Import path | Must be `from ..phase_state import PhaseState` |
| Module location | PhaseState at `.claude/scripts/devforgeai_cli/phase_state.py` |
| Package structure | `__init__.py` must exist |

## Dependencies

### Prerequisite Stories
- [x] **STORY-253:** Create PhaseState Module in Correct Location
  - **Why:** PhaseState must exist before import can work
  - **Status:** Backlog

## Test Strategy

### Unit Tests

**Test File:** `.claude/scripts/devforgeai_cli/tests/test_phase_commands.py`

**Test Scenarios:**
1. **Happy Path:** Import succeeds, PhaseState returned
2. **Error Case:** Module not found raises ImportError

### Integration Tests

```bash
# After STORY-253 and STORY-254 implemented:
pip install -e .claude/scripts/
devforgeai-validate phase-init STORY-TEST --project-root=.
# Should succeed without "No module named" error
```

## Acceptance Criteria Verification Checklist

### AC#1: Relative import
- [ ] Import statement uses `from ..phase_state` - **Phase:** 3 - **Evidence:** phase_commands.py
- [ ] sys.path.insert() removed - **Phase:** 3 - **Evidence:** phase_commands.py

### AC#2: Function behavior
- [ ] Returns PhaseState instance - **Phase:** 3 - **Evidence:** test_phase_commands.py

### AC#3: Commands work
- [ ] phase-init command works - **Phase:** 5 - **Evidence:** CLI test
- [ ] phase-status command works - **Phase:** 5 - **Evidence:** CLI test

---

**Checklist Progress:** 0/5 items complete (0%)

## Definition of Done

### Implementation
- [ ] `_get_phase_state()` updated with relative import
- [ ] sys.path manipulation code removed
- [ ] sys import removed if unused elsewhere
- [ ] Docstring updated

### Quality
- [ ] All phase commands work without ImportError
- [ ] Code style follows PEP 8

### Testing
- [ ] Unit test updated/added
- [ ] Manual CLI test passes

### Documentation
- [ ] Code comment explains relative import

## Change Log

**Current Status:** Backlog

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-12 12:00 | claude/story-requirements-analyst | Created | Story created from RCA-001 REC-2 | STORY-254.story.md |

## Notes

**Code Change Preview:**

**Before (8 lines):**
```python
def _get_phase_state(project_root: str):
    installer_path = Path(project_root) / "installer"
    if installer_path.exists() and str(installer_path) not in sys.path:
        sys.path.insert(0, str(installer_path.parent))
    from installer.phase_state import PhaseState
    return PhaseState(project_root=Path(project_root))
```

**After (3 lines):**
```python
def _get_phase_state(project_root: str):
    from ..phase_state import PhaseState
    return PhaseState(project_root=Path(project_root))
```

**References:**
- RCA-001 REC-2

---

**Story Template Version:** 2.5
**Last Updated:** 2026-01-12
