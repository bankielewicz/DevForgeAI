---
id: STORY-560
title: CLI Test Integrity Verification Command
type: feature
epic: EPIC-087
sprint: Sprint-30
status: Backlog
points: 5
depends_on: []
priority: Medium
advisory: false
source_gap: null
source_story: null
assigned_to: null
created: 2026-03-03
format_version: "2.9"
---

# Story: CLI Test Integrity Verification Command

## Description

**As a** DevForgeAI QA workflow,
**I want** a `devforgeai-validate verify-test-integrity` CLI command that independently computes and compares test file SHA-256 checksums against the red-phase snapshot,
**so that** test integrity verification produces a deterministic exit code that cannot be rationalized away by the orchestrator.

**Source:** RCA-046 (REC-5) — QA Test Integrity Bypass Via Rationalization
**Root Cause Addressed:** Self-enforcement paradox — the same agent that modifies test files should not be the sole verifier of those modifications.

## Acceptance Criteria

### AC#1: CLI Command Exists and Is Callable

```xml
<acceptance_criteria id="AC1" implements="REC-5">
  <given>The devforgeai-validate CLI is installed</given>
  <when>A user runs `devforgeai-validate verify-test-integrity STORY-531 --project-root=.`</when>
  <then>The command executes without error and returns an exit code (0 for pass or missing snapshot with warning, 1 for mismatch, 2 for error such as corrupted JSON)</then>
  <verification>
    <source_files>
      <file hint="CLI entry point">src/claude/scripts/devforgeai_cli/cli.py</file>
      <file hint="Command implementation">src/claude/scripts/devforgeai_cli/commands/verify_test_integrity.py</file>
    </source_files>
    <test_file>tests/STORY-560/test_ac1_cli_command.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Checksum Comparison Returns Exit Code 1 on Mismatch

```xml
<acceptance_criteria id="AC2" implements="REC-5">
  <given>A red-phase snapshot exists at devforgeai/qa/snapshots/{STORY_ID}/red-phase-checksums.json with known checksums</given>
  <when>One or more test files have been modified (checksums differ from snapshot)</when>
  <then>The command returns exit code 1 and prints each mismatched file with expected and actual SHA-256 values. Output includes "CRITICAL: TEST TAMPERING" for each mismatched file.</then>
  <verification>
    <source_files>
      <file hint="Command implementation">src/claude/scripts/devforgeai_cli/commands/verify_test_integrity.py</file>
    </source_files>
    <test_file>tests/STORY-560/test_ac2_mismatch_detection.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Graceful Degradation When Snapshot Missing

```xml
<acceptance_criteria id="AC3" implements="REC-5">
  <given>No red-phase snapshot exists for the given story ID</given>
  <when>The command runs</when>
  <then>The command returns exit code 0 (pass) with a WARNING message: "Test integrity snapshot not found — skipping verification (graceful degradation for pre-STORY-502 stories)". It does NOT block QA.</then>
  <verification>
    <source_files>
      <file hint="Command implementation">src/claude/scripts/devforgeai_cli/commands/verify_test_integrity.py</file>
    </source_files>
    <test_file>tests/STORY-560/test_ac3_missing_snapshot.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#4: All Checksums Match Returns Exit Code 0

```xml
<acceptance_criteria id="AC4" implements="REC-5">
  <given>A red-phase snapshot exists and all test files match their expected checksums</given>
  <when>The command runs</when>
  <then>The command returns exit code 0 and prints "Test integrity verified — all checksums match red-phase snapshot"</then>
  <verification>
    <source_files>
      <file hint="Command implementation">src/claude/scripts/devforgeai_cli/commands/verify_test_integrity.py</file>
    </source_files>
    <test_file>tests/STORY-560/test_ac4_all_match.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#5: QA Phase 1.5 Updated to Use CLI Command

```xml
<acceptance_criteria id="AC5" implements="REC-5">
  <given>The diff-regression-detection.md reference file defines Phase 1.5 Step 1.5.4</given>
  <when>QA Phase 1.5 executes test integrity verification</when>
  <then>The orchestrator calls `devforgeai-validate verify-test-integrity {STORY_ID} --project-root=.` via Bash and uses the exit code to determine pass/fail, instead of computing checksums itself. Exit code 1 sets overall_verdict = FAIL unconditionally.</then>
  <verification>
    <source_files>
      <file hint="QA Phase 1.5 reference">src/claude/skills/devforgeai-qa/references/diff-regression-detection.md</file>
    </source_files>
    <test_file>tests/STORY-560/test_ac5_phase_integration.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service"
      name: "verify-test-integrity-command"
      file_path: "src/claude/scripts/devforgeai_cli/commands/verify_test_integrity.py"
      required_keys:
        - key: "verify_test_integrity"
          type: "function"
          example: "def verify_test_integrity(story_id, project_root)"
          required: true
          validation: "Must compute SHA-256 using hashlib, compare against snapshot, return exit code"
          test_requirement: "Test: Verify function exists with correct signature"
        - key: "load_snapshot"
          type: "function"
          example: "def load_snapshot(story_id, project_root)"
          required: true
          validation: "Must read and parse red-phase-checksums.json"
          test_requirement: "Test: Verify snapshot loading with valid and invalid JSON"
        - key: "compute_sha256"
          type: "function"
          example: "def compute_sha256(file_path)"
          required: true
          validation: "Must use hashlib.sha256 to compute file digest"
          test_requirement: "Test: Verify SHA-256 computation matches known values"

    - type: "Configuration"
      name: "cli-registration"
      file_path: "src/claude/scripts/devforgeai_cli/cli.py"
      required_keys:
        - key: "verify_test_integrity_subcommand"
          type: "string"
          example: "subparsers.add_parser('verify-test-integrity')"
          required: true
          validation: "Must register verify-test-integrity as CLI subcommand"
          test_requirement: "Test: Verify CLI help shows verify-test-integrity command"

    - type: "Configuration"
      name: "phase-1.5-integration"
      file_path: "src/claude/skills/devforgeai-qa/references/diff-regression-detection.md"
      required_keys:
        - key: "cli_invocation"
          type: "string"
          example: "Bash(command='devforgeai-validate verify-test-integrity {STORY_ID}')"
          required: true
          validation: "Phase 1.5 Step 1.5.4 must call CLI command instead of orchestrator-computed comparison"
          test_requirement: "Test: Verify diff-regression-detection.md references CLI command"

  business_rules:
    - id: "BR-001"
      rule: "Exit code 1 on ANY checksum mismatch — no partial pass"
      trigger: "One or more files have different checksums"
      validation: "Even a single mismatch returns exit code 1"
      error_handling: "Print all mismatched files before exiting"
      test_requirement: "Test: Single file mismatch returns exit 1"
      priority: "Critical"
    - id: "BR-002"
      rule: "SHA-256 computed using Python hashlib, not shell sha256sum"
      trigger: "Checksum computation"
      validation: "Uses hashlib.sha256 for cross-platform consistency"
      error_handling: "N/A — hashlib is stdlib"
      test_requirement: "Test: Verify hashlib usage in source code"
      priority: "High"
    - id: "BR-003"
      rule: "Missing snapshot = graceful degradation (exit 0), not error"
      trigger: "Snapshot file not found"
      validation: "Returns exit 0 with WARNING, not exit 1"
      error_handling: "Log warning, return 0"
      test_requirement: "Test: Missing snapshot returns exit 0 with warning"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Command must complete in < 2 seconds for up to 50 test files"
      metric: "< 2000ms execution time"
      test_requirement: "Test: Time command execution with 50 test files"
      priority: "Medium"
    - id: "NFR-002"
      category: "Reliability"
      requirement: "Command must not crash on corrupted snapshot JSON"
      metric: "Graceful error handling for malformed JSON"
      test_requirement: "Test: Feed corrupted JSON, verify exit code 2 with error message"
      priority: "High"
```

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "Cross-platform checksums"
    limitation: "SHA-256 computed by hashlib may differ from sha256sum if files have different line endings (CRLF vs LF)"
    decision: "workaround:Use Python hashlib for BOTH snapshot creation and verification to ensure consistency. Never mix hashlib with shell sha256sum."
    discovered_phase: "Architecture"
    impact: "Snapshot creation (Phase 02) must also use Python hashlib, not sha256sum"
```

## Non-Functional Requirements (NFRs)

### Performance
- Command completes in < 2 seconds for typical story (5-20 test files)

### Security
- No sensitive data handled (checksums are not secrets)

### Scalability
- Supports up to 50 test files per story

### Reliability
- Graceful degradation on missing snapshot
- Error handling for corrupted JSON
- Cross-platform consistent checksums via hashlib

### Observability
- Prints each mismatched file with expected/actual values for debugging

## Dependencies

### Prerequisite Stories
- None (independent implementation)

### External Dependencies
- Python 3.9+ (hashlib is stdlib)

### Technology Dependencies
- Python hashlib (stdlib, no external package)
- Existing devforgeai-validate CLI framework

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+

**Test Scenarios:**
1. Load valid snapshot JSON
2. Load corrupted snapshot JSON (error handling)
3. Compute SHA-256 of known file
4. Compare matching checksums (exit 0)
5. Compare mismatching checksums (exit 1)
6. Missing snapshot file (exit 0 with warning)
7. Missing test file on disk (exit 1 — file deleted)

### Integration Tests

**Coverage Target:** 85%+

**Test Scenarios:**
1. End-to-end: Create snapshot, modify file, run command, verify exit 1
2. End-to-end: Create snapshot, don't modify, run command, verify exit 0
3. CLI registration: `devforgeai-validate verify-test-integrity --help` succeeds

## Acceptance Criteria Verification Checklist

### AC#1: CLI Command Exists
- [ ] Command registered in cli.py - **Phase:** 2
- [ ] --help shows verify-test-integrity - **Phase:** 2
- [ ] Accepts STORY_ID and --project-root args - **Phase:** 2

### AC#2: Mismatch Detection
- [ ] Exit code 1 on mismatch - **Phase:** 2
- [ ] Prints expected vs actual SHA-256 - **Phase:** 2
- [ ] Prints CRITICAL: TEST TAMPERING - **Phase:** 2

### AC#3: Missing Snapshot
- [ ] Exit code 0 when snapshot missing - **Phase:** 2
- [ ] WARNING message printed - **Phase:** 2

### AC#4: All Match
- [ ] Exit code 0 when all match - **Phase:** 2
- [ ] Success message printed - **Phase:** 2

### AC#5: Phase Integration
- [ ] diff-regression-detection.md updated - **Phase:** 5
- [ ] References CLI command in Step 1.5.4 - **Phase:** 5

---

**Checklist Progress:** 0/12 items complete (0%)

## Implementation Notes

*(To be filled during /dev workflow)*

## Definition of Done

### Implementation
- [ ] verify_test_integrity.py created with load_snapshot, compute_sha256, verify functions
- [ ] CLI subcommand registered in cli.py
- [ ] diff-regression-detection.md updated to call CLI command in Step 1.5.4
- [ ] Exit codes: 0 (pass), 1 (mismatch), 2 (error)

### Quality
- [ ] hashlib used for SHA-256 (not shell sha256sum)
- [ ] Graceful error handling for all edge cases
- [ ] No hardcoded paths

### Testing
- [ ] Unit tests for all 5 ACs pass
- [ ] Integration test for end-to-end flow
- [ ] Coverage > 95% for business logic

### Documentation
- [ ] CLI --help text documents command usage
- [ ] Exit code meanings documented

### TDD Workflow Summary

*(To be filled during /dev workflow)*

### Files Created/Modified

*(To be filled during /dev workflow)*

## Change Log

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-03-03 | RCA-046 | Created | Story created from RCA-046 REC-5 | STORY-560 |

## Notes

**Design Decisions:**
- Use Python hashlib (not shell sha256sum) for cross-platform consistency
- Exit code 0 for missing snapshot (graceful degradation, not error)
- This command eliminates the self-enforcement paradox identified in RCA-046
- Pattern mirrors existing devforgeai-validate commands (validate-dod, phase-complete)

**References:**
- RCA-046: QA Test Integrity Bypass Via Rationalization
- STORY-502: Red-Phase Test Integrity Checksums
- RCA-043: Test Integrity Snapshot Skipped
- TL-001: Snapshot creation should also use hashlib for consistency

---

## Exact Implementation Specification

### Exit Code Contract (Definitive — Resolves AC#1/AC#3 Alignment)

| Exit Code | Meaning | When |
|-----------|---------|------|
| 0 | PASS | All checksums match OR snapshot missing (graceful degradation) |
| 1 | FAIL — TEST TAMPERING | One or more checksums mismatch |
| 2 | ERROR | Corrupted JSON, file permission error, or unexpected exception |

**Missing snapshot = exit 0 with WARNING on stderr**, NOT exit 2. This is graceful degradation for stories created before STORY-502.

### Snapshot JSON Schema

The snapshot file lives at `devforgeai/qa/snapshots/{STORY_ID}/red-phase-checksums.json`:
```json
{
  "story_id": "STORY-531",
  "phase": "02-red",
  "created": "2026-03-03T00:00:00Z",
  "test_files": {
    "tests/STORY-531/test_ac1_lean_canvas_generation.sh": "51b0a8ebee321faff7355b6dcf7d3304b04fdc08fd32e9f30742de1ba0cf1e3f",
    "tests/STORY-531/test_ac2_adaptive_depth.sh": "370bc2f5b207a36788f34033c7b990bbcbbb0e0c887f19fcb3d0635cb0a0d5fe"
  },
  "total_tests": 2,
  "all_red": true
}
```

Key fields: `test_files` is a dict mapping relative file paths to SHA-256 hex digest strings.

### Existing CLI Pattern to Follow

**File structure:**
```
src/claude/scripts/devforgeai_cli/
├── cli.py                          # Main entry point, subparser registration
├── phase_state.py                  # Phase state management class
├── commands/
│   ├── __init__.py
│   ├── phase_commands.py           # phase-init, phase-check, phase-complete, etc.
│   ├── check_hooks.py              # check-hooks command
│   ├── invoke_hooks.py             # invoke-hooks command
│   ├── validate_installation.py    # validate-installation command
│   └── verify_test_integrity.py    # ← NEW: This story creates this file
```

**Registration pattern in cli.py** (follow existing pattern):
```python
# In cli.py main(), add after existing subparsers:
vti_parser = subparsers.add_parser(
    'verify-test-integrity',
    help='Verify test file checksums against red-phase snapshot',
    description='Computes SHA-256 of test files and compares against snapshot'
)
vti_parser.add_argument('story_id', help='Story ID (e.g., STORY-531)')
vti_parser.add_argument('--project-root', default='.', help='Project root directory')
```

**Command module pattern** (follow phase_commands.py style):
```python
# verify_test_integrity.py
"""
Verify test file integrity against red-phase snapshot.

Exit codes:
- 0: All checksums match (or snapshot missing — graceful degradation)
- 1: One or more checksums mismatch (TEST TAMPERING)
- 2: Error (corrupted JSON, file access error)
"""
import json
import hashlib
import sys
from pathlib import Path


def compute_sha256(file_path: Path) -> str:
    """Compute SHA-256 hex digest of a file using hashlib."""
    h = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def load_snapshot(story_id: str, project_root: Path) -> dict | None:
    """Load red-phase checksums snapshot. Returns None if not found."""
    snapshot_path = project_root / "devforgeai" / "qa" / "snapshots" / story_id / "red-phase-checksums.json"
    if not snapshot_path.exists():
        return None
    with open(snapshot_path) as f:
        return json.load(f)


def verify_test_integrity(story_id: str, project_root: str) -> int:
    """Main verification function. Returns exit code."""
    root = Path(project_root)
    snapshot = load_snapshot(story_id, root)

    if snapshot is None:
        print(f"WARNING: Test integrity snapshot not found for {story_id}", file=sys.stderr)
        print(f"Skipping verification (graceful degradation for pre-STORY-502 stories)")
        return 0  # Graceful degradation

    mismatches = []
    for rel_path, expected_sha in snapshot.get("test_files", {}).items():
        file_path = root / rel_path
        if not file_path.exists():
            mismatches.append((rel_path, expected_sha, "FILE_DELETED"))
            continue
        actual_sha = compute_sha256(file_path)
        if actual_sha != expected_sha:
            mismatches.append((rel_path, expected_sha, actual_sha))

    if mismatches:
        for rel_path, expected, actual in mismatches:
            finding = "FILE DELETED" if actual == "FILE_DELETED" else "TEST TAMPERING"
            print(f"CRITICAL: {finding}")
            print(f"  File: {rel_path}")
            print(f"  Expected: {expected}")
            print(f"  Actual:   {actual}")
            print()
        return 1  # Mismatch detected

    print(f"Test integrity verified — all checksums match red-phase snapshot")
    return 0  # All match
```

### Phase 1.5 Integration — Exact Change to diff-regression-detection.md

Replace the current orchestrator-computed Step 1.5.4 with CLI invocation:

**Current text to replace in Section 8:**
```
Bash(command="sha256sum {file_path}")
IF actual_sha256 != expected_sha256:
```

**New text:**
```
Bash(command="devforgeai-validate verify-test-integrity {STORY_ID} --project-root=.")

IF exit_code == 0:
    Display: "✓ Test integrity verified"
    Record: test_integrity: PASS
ELIF exit_code == 1:
    Display: "❌ CRITICAL: TEST TAMPERING DETECTED"
    overall_verdict = FAIL
    HALT: QA approval blocked unconditionally
ELIF exit_code == 2:
    Display: "❌ ERROR: Test integrity verification failed"
    overall_verdict = FAIL
```

### TL-001 Out-of-Scope Note

The technical limitation about snapshot creation needing to use hashlib is **out of scope** for this story. The current snapshot creation (in implementing-stories Phase 02) may use sha256sum or another tool. If checksums are computed differently during creation vs verification, mismatches will occur.

**Mitigation:** The `compute_sha256` function reads files in binary mode (`'rb'`), which matches the output of `sha256sum` on Linux/WSL for files without CRLF issues. If a mismatch occurs due to tool differences, that's a separate bug to fix in the snapshot creation process (Phase 02), not in this verification command.

---

Story Template Version: 2.9
Last Updated: 2026-03-03
