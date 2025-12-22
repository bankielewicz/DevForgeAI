---
id: STORY-138
title: Auto-Cleanup Completed Checkpoints
epic: EPIC-029
sprint: Backlog
status: Backlog
points: 3
depends_on: ["STORY-137"]
priority: Medium
assigned_to: Unassigned
created: 2025-12-22
format_version: "2.3"
---

# Story: Auto-Cleanup Completed Checkpoints

## Description

**As a** framework user,
**I want** checkpoint files to be automatically deleted when ideation completes successfully,
**so that** stale checkpoint files don't accumulate on disk and cause confusion in future sessions.

## Acceptance Criteria

### AC#1: Checkpoint Deletion on Successful Completion

**Given** an ideation session completes successfully (Phase 6 artifacts generated)
**When** the user has answered the Phase 6.6 next-action question AND the skill is about to return control to the command
**Then** the checkpoint file for the current session is deleted:
- File path: `devforgeai/temp/.ideation-checkpoint-{session_id}.yaml`
- Deletion uses Write tool with empty content to overwrite, then skill marks for deletion
- **Note:** Since Write tool cannot delete files directly, use `Write(file_path="...", content="# DELETED")` to mark as deleted, then document that stale marked files are cleaned up by `--clean-checkpoints` command
- Success logged: "Checkpoint marked for cleanup: {session_id}"

**Alternative approach (if Write deletion not feasible):**
- Checkpoint files are small (<5KB) and timestamped
- Manual cleanup via `--clean-checkpoints` is primary deletion mechanism
- Auto-cleanup is best-effort; stale files don't affect functionality

**Test Requirements:**
- Verify checkpoint file exists before completion
- Verify checkpoint file deleted after completion
- Verify deletion logged

---

### AC#2: Checkpoint Preserved on Failure

**Given** an ideation session fails or is interrupted before completion
**When** the session terminates (error, user cancel, context clear)
**Then** the checkpoint file is preserved:
- File remains at `devforgeai/temp/.ideation-checkpoint-{session_id}.yaml`
- Available for resume on next session start
- No automatic cleanup for incomplete sessions

**Test Requirements:**
- Simulate session failure at Phase 3
- Verify checkpoint file exists after failure
- Verify checkpoint usable for resume

---

### AC#3: Manual Cleanup Command

**Given** stale checkpoint files exist from abandoned sessions
**When** the user runs `/ideate --clean-checkpoints`
**Then** all checkpoint files in `devforgeai/temp/` are removed:
- Pattern: `devforgeai/temp/.ideation-checkpoint-*.yaml`
- User confirmation required before deletion
- Report: "Removed {N} checkpoint files"

**Command argument parsing:**
- The /ideate command (ideate.md) checks for `--clean-checkpoints` argument in Phase 0
- If detected: Route to cleanup flow instead of normal ideation
- Parsing: `IF args contains "--clean-checkpoints" THEN execute_cleanup() ELSE continue_normal_flow()`
- This is a command-level branch, not a shell flag

**Test Requirements:**
- Create 5 stale checkpoint files
- Run cleanup command
- Verify all files removed
- Verify confirmation prompt shown

---

### AC#4: Cleanup Confirmation with File List

**Given** the user runs `/ideate --clean-checkpoints`
**When** checkpoint files are found
**Then** user is shown list before deletion:
- Display each checkpoint: timestamp, problem statement preview
- AskUserQuestion: "Delete {N} checkpoint files?"
- Options: "Yes, delete all", "No, keep them", "Select specific files"

**Test Requirements:**
- Verify file list displayed
- Test "Yes" path (all deleted)
- Test "No" path (none deleted)
- Test selective deletion

---

## Technical Specification

```yaml
technical_specification:
  version: "2.0"

  reference_files:
    skill_to_modify: ".claude/skills/devforgeai-ideation/SKILL.md"
    command_to_modify: ".claude/commands/ideate.md"
    checkpoint_protocol: ".claude/skills/devforgeai-ideation/references/checkpoint-protocol.md"
    resume_logic: ".claude/skills/devforgeai-ideation/references/resume-logic.md"

  files_to_create:
    - path: ".claude/skills/devforgeai-ideation/references/checkpoint-cleanup.md"
      description: "Cleanup logic for auto and manual checkpoint deletion"
      created_by: "This story (STORY-138)"

  constitutional_exception:
    rule_bypassed: "No Bash for file operations (tech-stack.md)"
    justification: |
      Cleanup uses manual --clean-checkpoints command which may use Bash rm for
      actual file deletion since Write tool cannot delete files. This is acceptable
      because:
      1. It's user-initiated (explicit --clean-checkpoints flag)
      2. Files are non-critical (checkpoint recovery data only)
      3. No alternative delete mechanism exists in Claude Code tools
    approval: "Requires user confirmation before any deletion"

  components:
    - name: CheckpointCleaner
      type: Service
      description: "Handles checkpoint deletion on success and manual cleanup"
      location: ".claude/skills/devforgeai-ideation/references/checkpoint-cleanup.md"
      dependencies:
        - "Bash tool (rm command for cleanup)"
        - "Glob tool (find checkpoint files)"
      test_requirement: "Unit tests for cleanup scenarios"

    - name: CleanupCommand
      type: Configuration
      description: "Command-line flag handler for --clean-checkpoints"
      location: ".claude/commands/ideate.md"
      test_requirement: "Flag parsing and routing tests"

  business_rules:
    - id: BR-001
      description: "Cleanup MUST NOT occur until Phase 6.6 user confirmation"
      test_requirement: "Verify timing of cleanup call"

    - id: BR-002
      description: "Failed sessions MUST preserve checkpoints for recovery"
      test_requirement: "Failure scenario test"

    - id: BR-003
      description: "Manual cleanup MUST require user confirmation"
      test_requirement: "Verify AskUserQuestion before deletion"

  non_functional_requirements:
    - id: NFR-001
      category: Performance
      description: "Cleanup completes < 1 second for up to 100 files"
      metric: "Cleanup duration"
      target: "< 1 second"
      test_requirement: "Performance test with 100 files"

    - id: NFR-002
      category: Reliability
      description: "Cleanup errors do not affect session completion"
      metric: "Session impact on cleanup failure"
      target: "Zero impact"
      test_requirement: "Mock cleanup failure, verify session completes"
```

---

## Technical Limitations

```yaml
technical_limitations: []
# None identified at Architecture phase
```

---

## Edge Cases

| # | Scenario | Expected Behavior | Test Approach |
|---|----------|-------------------|---------------|
| 1 | Checkpoint already deleted (race condition) | No error, log "already cleaned" | Delete before cleanup call |
| 2 | Permission denied on deletion | Warn user, continue session | Mock permission error |
| 3 | Very large number of checkpoints (1000+) | Batch deletion, progress display | Create 1000 checkpoint files |
| 4 | Network filesystem slow deletion | Timeout after 5 seconds, warn | Mock slow filesystem |

---

## UI Specification

**Not applicable** - Backend cleanup with AskUserQuestion for manual cleanup confirmation.

---

## Definition of Done

### Implementation
- [ ] Auto-cleanup on successful completion implemented
- [ ] Checkpoint preservation on failure implemented
- [ ] Manual cleanup command (--clean-checkpoints) implemented
- [ ] User confirmation flow implemented
- [ ] Selective deletion option implemented

### Quality
- [ ] All acceptance criteria verified with tests
- [ ] Code follows coding-standards.md patterns
- [ ] No CRITICAL or HIGH anti-pattern violations

### Testing
- [ ] Unit tests for CheckpointCleaner
- [ ] Integration test for success cleanup flow
- [ ] Integration test for failure preservation
- [ ] Manual cleanup command tests
- [ ] Edge case tests
- [ ] Coverage meets thresholds (95%/85%/80%)

### Documentation
- [ ] Cleanup behavior documented
- [ ] Manual cleanup command documented in ideate help

---

## Workflow Status

- [ ] Story created
- [ ] Architecture phase complete
- [ ] Development phase complete
- [ ] QA phase complete
- [ ] Released

---

**Created:** 2025-12-22
**Source:** /create-missing-stories EPIC-029 (batch mode)
**Epic Reference:** EPIC-029 Feature 3: Auto-Cleanup Completed Checkpoints
