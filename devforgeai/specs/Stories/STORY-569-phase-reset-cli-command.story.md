---
id: STORY-569
title: Add phase-reset CLI Command to devforgeai-validate
type: feature
epic: EPIC-087
sprint: null
status: Backlog
points: 3
depends_on: []
priority: High
advisory: false
source_gap: null
source_story: null
assigned_to: null
created: 2026-03-03
format_version: "2.9"
---

# Story: Add phase-reset CLI Command to devforgeai-validate

## Description

**As a** DevForgeAI orchestrator,
**I want** a `devforgeai-validate phase-reset STORY-XXX --to=02` CLI command,
**so that** backward phase transitions are programmatic, auditable, and enforce regression limits instead of requiring manual phase-state.json editing.

**Source:** RCA-047 (REC-4) — Orchestrator Test Modification Phase Violation

**Context:** The CLI currently supports forward-only phase transitions (phase-init, phase-check, phase-complete, phase-status, phase-record). Adding `phase-reset` enables programmatic backward transitions with state management, audit logging in the `regressions` array, and a maximum 2 regressions limit.

## Acceptance Criteria

### AC#1: Backward Phase Reset Succeeds

```xml
<acceptance_criteria id="AC1" implements="REC-4">
  <given>A story phase-state.json exists with current_phase "03"</given>
  <when>Running `devforgeai-validate phase-reset STORY-XXX --to=02`</when>
  <then>Exit code 0, current_phase updated to "02" in phase-state.json</then>
  <verification>
    <source_files>
      <file hint="CLI command">src/claude/scripts/devforgeai_cli/commands/phase_commands.py</file>
      <file hint="CLI entry point">src/claude/scripts/devforgeai_cli/cli.py</file>
    </source_files>
    <test_file>tests/STORY-569/test_phase_reset_cli.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Forward Transition Rejected

```xml
<acceptance_criteria id="AC2" implements="REC-4">
  <given>A story phase-state.json exists with current_phase "02"</given>
  <when>Running `devforgeai-validate phase-reset STORY-XXX --to=03`</when>
  <then>Exit code 1, error message "Not a backward transition", phase-state.json unchanged</then>
  <verification>
    <source_files>
      <file hint="CLI command">src/claude/scripts/devforgeai_cli/commands/phase_commands.py</file>
    </source_files>
    <test_file>tests/STORY-569/test_phase_reset_cli.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Regression Logged in State File

```xml
<acceptance_criteria id="AC3" implements="REC-4">
  <given>A successful phase reset from 03 to 02</given>
  <when>Reading the phase-state.json after reset</when>
  <then>A `regressions` array entry exists with `from`, `to`, `timestamp`, and `reason` fields</then>
  <verification>
    <source_files>
      <file hint="CLI command">src/claude/scripts/devforgeai_cli/commands/phase_commands.py</file>
    </source_files>
    <test_file>tests/STORY-569/test_phase_reset_cli.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Maximum 2 Regressions Enforced

```xml
<acceptance_criteria id="AC4" implements="REC-4">
  <given>A phase-state.json with 2 existing regressions</given>
  <when>Running `devforgeai-validate phase-reset STORY-XXX --to=02`</when>
  <then>Exit code 3, error message "Maximum regressions exceeded (2)", phase-state.json unchanged</then>
  <verification>
    <source_files>
      <file hint="CLI command">src/claude/scripts/devforgeai_cli/commands/phase_commands.py</file>
    </source_files>
    <test_file>tests/STORY-569/test_phase_reset_cli.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#5: JSON Output Format Supported

```xml
<acceptance_criteria id="AC5" implements="REC-4">
  <given>A valid phase reset scenario</given>
  <when>Running `devforgeai-validate phase-reset STORY-XXX --to=02 --format=json`</when>
  <then>Output is valid JSON with `success`, `story_id`, `from`, and `to` fields</then>
  <verification>
    <source_files>
      <file hint="CLI command">src/claude/scripts/devforgeai_cli/commands/phase_commands.py</file>
    </source_files>
    <test_file>tests/STORY-569/test_phase_reset_cli.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

## Technical Specification

**Files to Modify:**
1. `src/claude/scripts/devforgeai_cli/commands/phase_commands.py` — add `phase_reset_command` function
2. `src/claude/scripts/devforgeai_cli/cli.py` — add subparser and dispatch block

### Implementation Reference: phase_commands.py

Add this function at the end of `phase_commands.py` (after the last existing command function). The function follows the same pattern as `phase_init_command`, `phase_check_command`, etc. It uses `_get_phase_state(project_root)` to get a PhaseState instance, then reads/writes `devforgeai/workflows/${STORY_ID}-phase-state.json`.

```python
def phase_reset_command(
    story_id: str,
    project_root: str,
    target_phase: str,
    format: str = "text",
    workflow: str = "dev"
) -> int:
    """
    Reset phase state to an earlier phase (backward transition).

    Used for Phase Regression when test infrastructure defects require
    returning to Phase 02 for test-automator regeneration.

    Args:
        story_id: Story identifier (e.g., "STORY-001")
        project_root: Project root directory
        target_phase: Phase to reset to (must be < current phase)
        format: Output format ("text" or "json")
        workflow: Workflow type ("dev" or "qa")

    Returns:
        Exit code: 0=reset success, 1=not backward, 2=invalid ID, 3=max regressions
    """
    try:
        ps = _get_phase_state(project_root)
        state_path = ps._get_state_path(story_id)

        if not state_path.exists():
            if format == "json":
                print(json.dumps({"success": False, "error": "State file not found", "story_id": story_id}))
            else:
                print(f"State file not found for {story_id}")
            return 2

        with open(state_path) as f:
            state = json.load(f)

        current_phase = state.get("current_phase", "01")

        # Validate backward transition
        if target_phase >= current_phase:
            if format == "json":
                print(json.dumps({"success": False, "error": f"Not a backward transition: {current_phase} -> {target_phase}"}))
            else:
                print(f"ERROR: Target phase {target_phase} is not before current phase {current_phase}")
            return 1

        # Check regression limit
        regressions = state.get("regressions", [])
        if len(regressions) >= 2:
            if format == "json":
                print(json.dumps({"success": False, "error": "Maximum regressions exceeded (2)"}))
            else:
                print(f"ERROR: Maximum 2 regressions per story exceeded ({len(regressions)} already recorded)")
            return 3

        # Perform reset
        from datetime import datetime, timezone
        regression_entry = {
            "from": current_phase,
            "to": target_phase,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "reason": "test infrastructure defect"
        }
        regressions.append(regression_entry)
        state["regressions"] = regressions
        state["current_phase"] = target_phase

        with open(state_path, 'w') as f:
            json.dump(state, f, indent=2)

        if format == "json":
            print(json.dumps({"success": True, "story_id": story_id, "from": current_phase, "to": target_phase}))
        else:
            print(f"Phase reset for {story_id}: {current_phase} -> {target_phase}")
            print(f"  Regression logged ({len(regressions)}/2 max)")

        return 0

    except ValueError as e:
        if format == "json":
            print(json.dumps({"success": False, "error": str(e), "story_id": story_id}))
        else:
            print(f"ERROR: {e}")
        return 2
```

### Implementation Reference: cli.py

**Change A — Add subparser** (insert after the `phase-record` subparser block, around line 315):

```python
    # ======================================================================
    # phase-reset command (RCA-047)
    # ======================================================================
    phase_reset_parser = subparsers.add_parser(
        'phase-reset',
        help='Reset phase state to earlier phase (backward transition)',
        description='Resets current phase to a prior phase for test regeneration'
    )
    phase_reset_parser.add_argument(
        'story_id',
        help='Story ID (format: STORY-XXX)'
    )
    phase_reset_parser.add_argument(
        '--to',
        required=True,
        dest='target_phase',
        help='Target phase to reset to (must be < current phase)'
    )
    phase_reset_parser.add_argument(
        '--project-root',
        default='.',
        help='Project root directory'
    )
    phase_reset_parser.add_argument(
        '--format',
        choices=['text', 'json'],
        default='text',
        help='Output format'
    )
    phase_reset_parser.add_argument(
        '--workflow',
        choices=['dev', 'qa'],
        default='dev',
        help='Workflow type'
    )
```

**Change B — Add dispatch block** (insert after the `phase-record` dispatch block, around line 566):

```python
        elif args.command == 'phase-reset':
            from .commands.phase_commands import phase_reset_command
            return phase_reset_command(
                story_id=args.story_id,
                project_root=args.project_root,
                target_phase=args.target_phase,
                format=args.format,
                workflow=getattr(args, 'workflow', 'dev')
            )
```

### Exit Code Reference

| Exit Code | Meaning |
|-----------|---------|
| 0 | Phase reset successful |
| 1 | Target phase >= current phase (not a backward transition) |
| 2 | Invalid story ID or state file not found |
| 3 | Maximum regressions exceeded (>2) |

### Usage

```bash
devforgeai-validate phase-reset STORY-XXX --to=02
devforgeai-validate phase-reset STORY-XXX --to=02 --format=json
```

### Structured Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service"
      name: "phase_reset_command"
      file_path: "src/claude/scripts/devforgeai_cli/commands/phase_commands.py"
      interface: "CLI function"
      lifecycle: "Transient"
      dependencies:
        - "PhaseState"
        - "json"
        - "datetime"
      requirements:
        - id: "SVC-001"
          description: "Reset phase state to earlier phase with validation"
          testable: true
          test_requirement: "Test: phase_reset_command returns 0 for valid backward reset"
          priority: "Critical"
        - id: "SVC-002"
          description: "Reject forward transitions with exit code 1"
          testable: true
          test_requirement: "Test: phase_reset_command returns 1 for forward transition"
          priority: "Critical"
        - id: "SVC-003"
          description: "Enforce maximum 2 regressions with exit code 3"
          testable: true
          test_requirement: "Test: phase_reset_command returns 3 when limit exceeded"
          priority: "High"
        - id: "SVC-004"
          description: "Log regression entry with from, to, timestamp, reason"
          testable: true
          test_requirement: "Test: regressions array has entry after reset"
          priority: "High"

    - type: "Configuration"
      name: "cli.py subparser"
      file_path: "src/claude/scripts/devforgeai_cli/cli.py"
      required_keys:
        - key: "phase-reset subparser"
          type: "object"
          example: "argparse subparser with story_id, --to, --format, --workflow"
          required: true
          validation: "Subparser registered and dispatches correctly"
          test_requirement: "Test: CLI dispatches phase-reset to phase_reset_command"

  business_rules:
    - id: "BR-001"
      rule: "Target phase must be strictly less than current phase"
      trigger: "On phase-reset invocation"
      validation: "target_phase < current_phase string comparison"
      error_handling: "Exit code 1 with descriptive error"
      test_requirement: "Test: Forward reset rejected"
      priority: "Critical"
    - id: "BR-002"
      rule: "Maximum 2 regressions per story"
      trigger: "On phase-reset invocation"
      validation: "len(regressions) < 2"
      error_handling: "Exit code 3 with count"
      test_requirement: "Test: Third regression blocked"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Phase reset completes within 100ms"
      metric: "< 100ms p95 for file read/write operation"
      test_requirement: "Test: Operation completes under 100ms"
      priority: "Medium"
    - id: "NFR-002"
      category: "Reliability"
      requirement: "State file integrity preserved on error"
      metric: "No partial writes on validation failure"
      test_requirement: "Test: State unchanged on rejected reset"
      priority: "Critical"
```

---

## Technical Limitations

```yaml
technical_limitations: []
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- phase-reset command: < 100ms (p95)

### Security

**Authentication:** None (local CLI)
**Authorization:** None

### Scalability

N/A — single-file JSON operation

### Reliability

**Error Handling:**
- Invalid story ID: exit code 2
- State file not found: exit code 2
- Forward transition: exit code 1
- Max regressions: exit code 3
- File I/O error: exit code 2

### Observability

**Logging:**
- Regression logged in phase-state.json `regressions` array
- Text and JSON output formats supported

---

## Dependencies

### Prerequisite Stories

- None (existing phase_commands.py provides implementation pattern)

### External Dependencies

- None

### Technology Dependencies

- None (uses existing Python stdlib: json, datetime, pathlib)

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+

**Test Scenarios:**
1. **Happy Path:** Backward reset from 03 to 02 succeeds
2. **Edge Cases:**
   - Reset from 04 to 02 succeeds
   - JSON output format
   - First regression vs second regression
3. **Error Cases:**
   - Forward transition rejected (exit 1)
   - Missing state file (exit 2)
   - Invalid story ID (exit 2)
   - Max regressions exceeded (exit 3)

### Integration Tests

**Coverage Target:** 85%

**Test Scenarios:**
1. **CLI Integration:** `devforgeai-validate phase-reset` dispatches correctly
2. **State Persistence:** phase-state.json updated correctly after reset

---

## Acceptance Criteria Verification Checklist

### AC#1: Backward Reset

- [ ] Reset from 03→02 succeeds with exit 0 - **Phase:** 2 - **Evidence:** test_phase_reset_cli.py
- [ ] current_phase updated in JSON - **Phase:** 3 - **Evidence:** test_phase_reset_cli.py

### AC#2: Forward Rejected

- [ ] Forward 02→03 returns exit 1 - **Phase:** 2 - **Evidence:** test_phase_reset_cli.py
- [ ] State file unchanged - **Phase:** 3 - **Evidence:** test_phase_reset_cli.py

### AC#3: Regression Logged

- [ ] regressions array has entry - **Phase:** 3 - **Evidence:** test_phase_reset_cli.py
- [ ] Entry has from, to, timestamp, reason - **Phase:** 3 - **Evidence:** test_phase_reset_cli.py

### AC#4: Max Enforced

- [ ] Third regression returns exit 3 - **Phase:** 2 - **Evidence:** test_phase_reset_cli.py

### AC#5: JSON Output

- [ ] --format=json produces valid JSON - **Phase:** 3 - **Evidence:** test_phase_reset_cli.py

---

**Checklist Progress:** 0/8 items complete (0%)

---

<!-- IMPLEMENTATION NOTES FORMAT REQUIREMENT (Critical for pre-commit validation):
See: .claude/skills/implementing-stories/references/dod-update-workflow.md for complete details
-->

## Implementation Notes

*To be filled during development*

## Definition of Done

### Implementation
- [ ] phase_reset_command function added to phase_commands.py
- [ ] CLI subparser registered in cli.py
- [ ] Dispatch block added in cli.py
- [ ] Backward transition validation (target < current)
- [ ] Maximum 2 regressions enforcement
- [ ] Regression entry logging with timestamp
- [ ] Text and JSON output formats

### Quality
- [ ] All 5 acceptance criteria have passing tests
- [ ] Exit codes match specification (0, 1, 2, 3)
- [ ] State file integrity on error paths
- [ ] Code coverage >95% for phase_reset_command

### Testing
- [ ] Unit test: backward reset success
- [ ] Unit test: forward rejection
- [ ] Unit test: regression logging
- [ ] Unit test: max regressions
- [ ] Unit test: JSON output
- [ ] Unit test: missing state file
- [ ] Integration test: CLI dispatch

### Documentation
- [ ] phase_commands.py docstring updated with new command
- [ ] Story Implementation Notes completed

---

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|

---

## Change Log

**Current Status:** Backlog

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-03-03 | .claude/story-requirements-analyst | Created | Story created from RCA-047 REC-4 | STORY-569.story.md |

## Notes

**Source:** RCA-047 — Orchestrator Test Modification Phase Violation
**Source Recommendation:** REC-4 — Add `phase-reset` CLI command to devforgeai-validate

**Design Decisions:**
- Follows existing CLI command pattern (phase_init_command, phase_check_command, etc.)
- Exit codes: 0=success, 1=not backward, 2=invalid ID/missing, 3=max regressions
- Regression limit (2) prevents infinite regression loops
- phase-reset is the missing inverse of phase-complete

**References:**
- RCA-047: devforgeai/RCA/RCA-047-orchestrator-test-modification-phase-violation.md
- phase_commands.py: src/claude/scripts/devforgeai_cli/commands/phase_commands.py
- cli.py: src/claude/scripts/devforgeai_cli/cli.py

---

Story Template Version: 2.9
Last Updated: 2026-03-03
