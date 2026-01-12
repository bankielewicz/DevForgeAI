---
id: STORY-255
title: Add Graceful Error Handling for Missing PhaseState Module
type: feature
epic: None
sprint: Backlog
status: Backlog
points: 3
depends_on: ["STORY-254"]
priority: Medium
assigned_to: Unassigned
created: 2026-01-12
format_version: "2.5"
source_rca: RCA-001
source_recommendation: REC-3
---

# Story: Add Graceful Error Handling for Missing PhaseState Module

## Description

**As a** DevForgeAI CLI user,
**I want** graceful error handling when the PhaseState module is unavailable,
**so that** I understand what went wrong and how to fix it, rather than seeing a cryptic ImportError.

## Acceptance Criteria

### AC#1: Provide helpful error message when PhaseState import fails

**Given** the PhaseState module is missing or cannot be imported
**When** any phase command is executed (phase-init, phase-check, phase-complete, phase-status, phase-record)
**Then** a clear error message is displayed containing:
  - What went wrong (ImportError with original error)
  - Expected module location: `.claude/scripts/devforgeai_cli/phase_state.py`
  - Fix instructions: `pip install -e .claude/scripts/`
  - Note that `/dev` workflow can continue without CLI-based phase enforcement

---

### AC#2: Error message includes context about STORY-253 implementation

**Given** the PhaseState module is not found
**When** `_get_phase_state()` raises ImportError
**Then** the error message mentions:
  - STORY-253 must be implemented (PhaseState module creation)
  - Installation command to reinstall the CLI
  - Backward compatibility note that workflow continues without phase enforcement

---

### AC#3: Error is raised as ImportError with cause chain

**Given** PhaseState module fails to import
**When** `_get_phase_state(project_root)` is called
**Then** an ImportError is raised:
  - Original exception preserved as `__cause__` (for traceback)
  - Message contains all required information
  - Not silently caught or transformed to different type

---

### AC#4: All phase commands handle error consistently

**Given** any phase command invokes `_get_phase_state()`
**When** ImportError is raised
**Then** the error propagates with helpful message to CLI output
  - Exit code reflects failure (non-zero)
  - User sees actionable guidance

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service"
      name: "GracefulErrorHandling"
      file_path: ".claude/scripts/devforgeai_cli/commands/phase_commands.py"
      interface: "_get_phase_state() with try/except"
      lifecycle: "N/A (error handling enhancement)"
      dependencies:
        - "..phase_state.PhaseState"
      requirements:
        - id: "SVC-001"
          description: "Add try/except block to catch ImportError"
          testable: true
          test_requirement: "Test: Missing module raises ImportError with helpful message"
          priority: "Critical"
        - id: "SVC-002"
          description: "Error message includes expected location"
          testable: true
          test_requirement: "Test: Error message contains '.claude/scripts/devforgeai_cli/phase_state.py'"
          priority: "High"
        - id: "SVC-003"
          description: "Error message includes fix instructions"
          testable: true
          test_requirement: "Test: Error message contains 'pip install -e .claude/scripts/'"
          priority: "High"
        - id: "SVC-004"
          description: "Original exception preserved as __cause__"
          testable: true
          test_requirement: "Test: Raised ImportError has __cause__ attribute"
          priority: "Medium"

  business_rules:
    - id: "BR-001"
      rule: "Error message must be user-friendly and actionable"
      trigger: "Import failure"
      validation: "Message contains all 4 required elements"
      error_handling: "Re-raise with enhanced message"
      test_requirement: "Test: Verify message format"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Usability"
      requirement: "Error message readability"
      metric: "Plain English, < 200 characters per section"
      test_requirement: "Test: Human review of error message"
      priority: "High"
    - id: "NFR-002"
      category: "Performance"
      requirement: "Error handling overhead"
      metric: "< 1ms (error path only)"
      test_requirement: "Test: Time error handling execution"
      priority: "Low"
```

## Technical Limitations

```yaml
technical_limitations: []
```

## Non-Functional Requirements

### Performance
- Error handling execution: < 1ms
- Error message generation: < 5ms
- No impact on normal operation

### Usability
- Plain English error message
- Clear sections: problem, location, fix, note
- Executable fix command (copy/paste ready)

### Security
- No sensitive information in error message
- Safe to display project paths

## Edge Cases

1. **Module has syntax errors:** ImportError with syntax details, still shows fix instructions
2. **Circular import failure:** Guides user to reinstall CLI
3. **Module removed after install:** Same recovery path (reinstall)
4. **Error during PhaseState instantiation:** Propagates unchanged (not import issue)
5. **Windows path display:** Use forward slashes (platform-agnostic)
6. **Running before STORY-253:** Error explains dependency

## Data Validation Rules

| Input | Validation |
|-------|-----------|
| ImportError | Preserve as __cause__ |
| Module path | Use `.claude/scripts/devforgeai_cli/phase_state.py` consistently |
| Original error | Include verbatim in message |

## Dependencies

### Prerequisite Stories
- [x] **STORY-254:** Update phase_commands.py Import
  - **Why:** Base import path must be set before adding error handling
  - **Status:** Backlog

## Test Strategy

### Unit Tests

**Test File:** `.claude/scripts/devforgeai_cli/tests/test_phase_commands.py`

**Test Scenarios:**
1. **Module Present:** No error, PhaseState returned
2. **Module Missing:** ImportError with helpful message
3. **Message Content:** Verify all 4 required elements present

### Manual Testing

```bash
# Temporarily rename module
mv .claude/scripts/devforgeai_cli/phase_state.py .claude/scripts/devforgeai_cli/phase_state.py.bak

# Run command
devforgeai-validate phase-init STORY-TEST
# Should show helpful error message

# Restore module
mv .claude/scripts/devforgeai_cli/phase_state.py.bak .claude/scripts/devforgeai_cli/phase_state.py
```

## Acceptance Criteria Verification Checklist

### AC#1: Helpful error message
- [ ] Error message displayed on import failure - **Phase:** 3 - **Evidence:** test_phase_commands.py
- [ ] Contains expected location - **Phase:** 3 - **Evidence:** test_phase_commands.py
- [ ] Contains fix instructions - **Phase:** 3 - **Evidence:** test_phase_commands.py
- [ ] Contains /dev workflow note - **Phase:** 3 - **Evidence:** test_phase_commands.py

### AC#2: STORY-253 context
- [ ] Mentions STORY-253 - **Phase:** 3 - **Evidence:** test_phase_commands.py

### AC#3: Exception handling
- [ ] ImportError raised - **Phase:** 3 - **Evidence:** test_phase_commands.py
- [ ] __cause__ preserved - **Phase:** 3 - **Evidence:** test_phase_commands.py

### AC#4: Consistent handling
- [ ] All commands show same error - **Phase:** 5 - **Evidence:** CLI test

---

**Checklist Progress:** 0/8 items complete (0%)

## Definition of Done

### Implementation
- [ ] try/except block added to _get_phase_state()
- [ ] Error message includes all 4 required elements
- [ ] `raise ImportError(...) from e` pattern used
- [ ] Docstring updated to document exception

### Quality
- [ ] Error message is clear and actionable
- [ ] Normal operation unaffected

### Testing
- [ ] Unit test for missing module scenario
- [ ] Unit test verifies message content
- [ ] Manual CLI test completed

### Documentation
- [ ] Docstring documents ImportError raise

## Change Log

**Current Status:** Backlog

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-12 12:00 | claude/story-requirements-analyst | Created | Story created from RCA-001 REC-3 | STORY-255.story.md |

## Notes

**Code Implementation:**

```python
def _get_phase_state(project_root: str):
    """
    Get PhaseState instance with graceful error handling.

    PhaseState is co-located in the same package for simple imports.

    Raises:
        ImportError: If phase_state.py module cannot be imported, with
                     helpful diagnostic message
    """
    try:
        from ..phase_state import PhaseState
        return PhaseState(project_root=Path(project_root))
    except ImportError as e:
        raise ImportError(
            f"PhaseState module not found: {e}\n\n"
            "The phase_state.py module is required for phase tracking.\n"
            "Expected location: .claude/scripts/devforgeai_cli/phase_state.py\n\n"
            "To fix:\n"
            "  1. Ensure STORY-253 (PhaseState module) is implemented\n"
            "  2. Reinstall CLI: pip install -e .claude/scripts/\n"
            "  3. Retry your command\n\n"
            "Note: The /dev workflow can continue without CLI-based phase\n"
            "enforcement if this module is unavailable. Phase tracking is\n"
            "optional and does not block story development."
        ) from e
```

**References:**
- RCA-001 REC-3

---

**Story Template Version:** 2.5
**Last Updated:** 2026-01-12
