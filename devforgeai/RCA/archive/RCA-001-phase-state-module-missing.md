# RCA-001: Phase State Module Missing From CLI

**Date:** 2026-01-11
**Reporter:** User
**Component:** devforgeai-validate CLI (phase_commands.py)
**Severity:** MEDIUM
**Status:** OPEN

---

## Issue Description

When running `devforgeai-validate phase-init STORY-001 --project-root=.`, the CLI fails with:

```
ERROR: No module named 'installer'
EXIT_CODE:2
```

This prevents all phase-related CLI commands (`phase-init`, `phase-check`, `phase-complete`, `phase-status`, `phase-record`, `phase-observe`) from functioning.

**Expected Behavior:** CLI should initialize phase state file for workflow tracking
**Actual Behavior:** CLI crashes with import error
**Impact:** Cannot use CLI-based phase enforcement for `/dev` workflow

---

## 5 Whys Analysis

**Issue Statement:** devforgeai-validate CLI fails with "No module named 'installer'" when executing phase commands

### Why #1
**Q:** Why does `devforgeai-validate phase-init` fail with 'No module named installer'?
**A:** The `phase_commands.py` file (lines 27-33) tries to import `PhaseState` from `installer.phase_state`, but the `installer/` directory doesn't exist in the project.

### Why #2
**Q:** Why does the code reference an `installer/phase_state` module that doesn't exist?
**A:** The `phase_commands.py` module was designed to depend on a `PhaseState` class that was supposed to be implemented in an `installer/` directory, but this module was never created.

### Why #3
**Q:** Why was the `PhaseState` class never implemented?
**A:** The CLI commands (`phase-init`, `phase-check`, `phase-complete`, `phase-status`, `phase-record`) were added to the CLI (STORY-148, STORY-149) but the underlying `PhaseState` infrastructure was planned but not implemented.

### Why #4
**Q:** Why was the dependency on `PhaseState` not validated before the CLI was installed?
**A:** The CLI package was installable because `setup.py` doesn't enforce runtime dependencies on the `installer` package. The error only manifests when the phase commands are actually executed, not at install time.

### Why #5 (ROOT CAUSE)
**Q:** Why was the `installer.phase_state` module never created to support the CLI?
**A:** **ROOT CAUSE:** The Phase Execution Enforcement System (STORY-148/149) was partially implemented - the CLI interface was created but the underlying state management module was never developed. Additionally, the original design placed `PhaseState` in `installer/` at project root, which is architecturally incorrect - it should be co-located with the CLI code that consumes it.

---

## Evidence Collected

### File: `.claude/scripts/devforgeai_cli/commands/phase_commands.py`
- **Lines Examined:** 21-33
- **Finding:** Import expects `installer.phase_state` module that doesn't exist
- **Excerpt:**
```python
def _get_phase_state(project_root: str):
    """
    Get PhaseState instance.

    Handles import path complexity for both CLI and test contexts.
    """
    # Add installer directory to path for PhaseState import
    installer_path = Path(project_root) / "installer"
    if installer_path.exists() and str(installer_path) not in sys.path:
        sys.path.insert(0, str(installer_path.parent))

    from installer.phase_state import PhaseState
    return PhaseState(project_root=Path(project_root))
```
- **Significance:** CRITICAL - This is where the error originates
- **Design Issue:** The `installer/` location at project root is architecturally incorrect

### File: `.claude/scripts/devforgeai_cli/cli.py`
- **Lines Examined:** 154-309
- **Finding:** All phase commands registered and properly wired
- **Significance:** HIGH - Shows CLI interface is complete, only implementation missing

### File: `.claude/scripts/setup.py`
- **Lines Examined:** 1-56
- **Finding:** Only `PyYAML>=6.0` listed as dependency, no `installer` package
- **Significance:** HIGH - Explains why install succeeds but runtime fails

### Directory: `installer/`
- **Finding:** Does not exist
- **Significance:** CRITICAL - The expected location for `PhaseState` class (but wrong location)

### Architectural Analysis
- **Finding:** `PhaseState` should be in `.claude/scripts/devforgeai_cli/` alongside `phase_commands.py`
- **Rationale:**
  1. Keep producer and consumer in same package
  2. Already installed via `pip install -e .claude/scripts/`
  3. Enables simple relative import (no sys.path manipulation)
  4. Avoids project root pollution with `installer/` directory
- **Significance:** HIGH - Corrects original design flaw

---

## Recommendations

### CRITICAL Priority

#### REC-1: Create PhaseState Module in Correct Location

**Problem Addressed:** CLI phase commands fail because `PhaseState` class doesn't exist

**Proposed Solution:** Create `phase_state.py` in `.claude/scripts/devforgeai_cli/` (same package as consumer)

**Why This Location (Not `installer/`):**
- `phase_commands.py` is already in `.claude/scripts/devforgeai_cli/` - keep related code together
- Package is already installed via `pip install -e .claude/scripts/`
- Enables simple relative import: `from .phase_state import PhaseState`
- No sys.path manipulation needed
- Avoids polluting project root with `installer/` directory

**Implementation Details:**
- **File:** `.claude/scripts/devforgeai_cli/phase_state.py` (NEW)
- **Required Methods:**
  - `__init__(self, project_root: Path)` - Initialize with project root
  - `create(self, story_id: str) -> dict` - Create new phase state file
  - `read(self, story_id: str) -> Optional[dict]` - Read existing state
  - `complete_phase(self, story_id: str, phase: str, checkpoint_passed: bool) -> bool` - Mark phase complete
  - `record_subagent(self, story_id: str, phase: str, subagent: str) -> bool` - Record subagent invocation
  - `add_observation(self, story_id: str, phase_id: str, category: str, note: str, severity: str) -> Optional[str]` - Add observation
  - `_get_state_path(self, story_id: str) -> Path` - Get path to state file

**State File Location:** `devforgeai/workflows/STORY-XXX-phase-state.json`

**State File Schema:**
```json
{
  "story_id": "STORY-XXX",
  "current_phase": "01",
  "workflow_started": "2026-01-11T12:00:00Z",
  "blocking_status": false,
  "phases": {
    "01": {"status": "pending", "subagents_required": ["git-validator", "tech-stack-detector"], "subagents_invoked": []},
    "02": {"status": "pending", "subagents_required": ["test-automator"], "subagents_invoked": []},
    "03": {"status": "pending", "subagents_required": ["backend-architect", "context-validator"], "subagents_invoked": []},
    "04": {"status": "pending", "subagents_required": ["refactoring-specialist", "code-reviewer"], "subagents_invoked": []},
    "05": {"status": "pending", "subagents_required": ["integration-tester"], "subagents_invoked": []},
    "06": {"status": "pending", "subagents_required": [], "subagents_invoked": []},
    "07": {"status": "pending", "subagents_required": [], "subagents_invoked": []},
    "08": {"status": "pending", "subagents_required": [], "subagents_invoked": []},
    "09": {"status": "pending", "subagents_required": [], "subagents_invoked": []},
    "10": {"status": "pending", "subagents_required": ["dev-result-interpreter"], "subagents_invoked": []}
  },
  "observations": []
}
```

**Rationale:** This is the missing infrastructure that prevents all phase commands from working. Placing it in the correct location also fixes the architectural issue.

**Testing:**
1. Run `devforgeai-validate phase-init STORY-TEST --project-root=.`
2. Verify state file created in `devforgeai/workflows/STORY-TEST-phase-state.json`
3. Run `devforgeai-validate phase-status STORY-TEST` to confirm readable
4. Run `devforgeai-validate phase-complete STORY-TEST --phase=01 --checkpoint-passed` to test update
5. Run `devforgeai-validate phase-record STORY-TEST --phase=01 --subagent=git-validator` to test recording

**Effort Estimate:** 2-3 hours
- PhaseState class implementation: 1.5 hours
- Unit tests: 1 hour
- Integration testing: 30 minutes

**Impact:**
- **Benefit:** Enables all phase enforcement CLI commands
- **Risk:** Low - new module, no existing code affected
- **Scope:** All `/dev` workflow executions

---

### HIGH Priority

#### REC-2: Update phase_commands.py Import

**Problem Addressed:** Current code uses complex sys.path manipulation for wrong location

**Proposed Solution:** Replace `_get_phase_state()` with simple relative import

**Implementation Details:**
- **File:** `.claude/scripts/devforgeai_cli/commands/phase_commands.py`
- **Section:** Lines 21-33

**Current Code (REMOVE):**
```python
def _get_phase_state(project_root: str):
    """
    Get PhaseState instance.

    Handles import path complexity for both CLI and test contexts.
    """
    # Add installer directory to path for PhaseState import
    installer_path = Path(project_root) / "installer"
    if installer_path.exists() and str(installer_path) not in sys.path:
        sys.path.insert(0, str(installer_path.parent))

    from installer.phase_state import PhaseState
    return PhaseState(project_root=Path(project_root))
```

**New Code (REPLACE WITH):**
```python
def _get_phase_state(project_root: str):
    """
    Get PhaseState instance.

    PhaseState is co-located in the same package for simple imports.
    """
    from ..phase_state import PhaseState
    return PhaseState(project_root=Path(project_root))
```

**Rationale:**
- Eliminates sys.path manipulation (fragile, hard to debug)
- Uses standard Python relative imports
- PhaseState is in same package, so import is straightforward

**Testing:**
```bash
# After REC-1 and REC-2 implemented:
.venv/bin/devforgeai-validate phase-init STORY-TEST --project-root=.
# Should succeed without "No module named" error
```

**Effort Estimate:** 15 minutes

**Impact:**
- **Benefit:** Clean imports, removes sys.path complexity
- **Risk:** None - simpler code is better
- **Scope:** `phase_commands.py` only

---

### MEDIUM Priority

#### REC-3: Add Graceful Error Handling

**Problem Addressed:** CLI crashes with unhelpful error if PhaseState import fails

**Proposed Solution:** Add try/except with helpful error message

**Implementation Details:**
- **File:** `.claude/scripts/devforgeai_cli/commands/phase_commands.py`
- **Section:** `_get_phase_state()` function (after REC-2 changes)

**Updated Code:**
```python
def _get_phase_state(project_root: str):
    """
    Get PhaseState instance with graceful error handling.

    PhaseState is co-located in the same package for simple imports.
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
            "  1. Ensure phase_state.py exists in the devforgeai_cli package\n"
            "  2. Reinstall CLI: pip install -e .claude/scripts/\n\n"
            "For backward compatibility, the /dev workflow will continue without\n"
            "CLI-based phase enforcement if this module is unavailable."
        ) from e
```

**Rationale:** Better error messages help users understand the issue and fix it.

**Testing:**
1. Temporarily rename `phase_state.py`
2. Run `devforgeai-validate phase-init STORY-TEST`
3. Verify helpful error message shown
4. Restore `phase_state.py`

**Effort Estimate:** 15 minutes

**Impact:**
- **Benefit:** Improved UX, clearer guidance when module missing
- **Risk:** None - only affects error path
- **Scope:** All phase commands

---

## Implementation Checklist

- [ ] **REC-1:** [STORY-253](../specs/Stories/STORY-253-create-phase-state-module.story.md) - Create `.claude/scripts/devforgeai_cli/phase_state.py` with PhaseState class
- [ ] **REC-2:** [STORY-254](../specs/Stories/STORY-254-update-phase-commands-import.story.md) - Update `phase_commands.py` to use relative import `from ..phase_state import PhaseState`
- [ ] Reinstall CLI: `pip install -e .claude/scripts/`
- [ ] Test `devforgeai-validate phase-init STORY-TEST --project-root=.`
- [ ] Test `devforgeai-validate phase-status STORY-TEST`
- [ ] Test `devforgeai-validate phase-complete STORY-TEST --phase=01 --checkpoint-passed`
- [ ] Test `devforgeai-validate phase-record STORY-TEST --phase=01 --subagent=git-validator`
- [ ] **REC-3:** [STORY-255](../specs/Stories/STORY-255-add-graceful-error-handling.story.md) - Add graceful error handling to `_get_phase_state()`
- [ ] Clean up test state file: `rm devforgeai/workflows/STORY-TEST-phase-state.json`
- [ ] Update this RCA status to RESOLVED
- [ ] Commit changes with reference to RCA-001

---

## Prevention Strategy

### Short-term
- Implement REC-1, REC-2, REC-3 to enable phase enforcement
- Add unit tests for PhaseState class

### Long-term
- Add integration tests that verify CLI commands work end-to-end before release
- Establish code review guideline: new CLI commands must have working implementations
- Consider adding CI check that imports all CLI modules to catch missing dependencies

### Monitoring
- Watch for: "No module named" or "ImportError" in CLI usage
- When to audit: After any changes to CLI command structure
- Escalation: If phase commands fail after changes, investigate immediately

---

## Related RCAs

None - This is the first RCA (RCA-001).

---

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-01-11 | Claude | RCA created |
| 2026-01-11 | Claude | Updated: Corrected PhaseState location from `installer/` to `.claude/scripts/devforgeai_cli/` per architectural review |
| 2026-01-12 | Claude | Stories created from recommendations: STORY-253 (REC-1), STORY-254 (REC-2), STORY-255 (REC-3) - using devforgeai-story-creation skill |

---

**End of RCA-001**
