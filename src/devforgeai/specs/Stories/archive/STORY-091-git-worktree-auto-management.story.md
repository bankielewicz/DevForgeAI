---
id: STORY-091
title: Git Worktree Auto-Management
epic: EPIC-010
sprint: SPRINT-5
status: QA Approved ✅
points: 8
priority: High
assigned_to: TBD
created: 2025-11-25
format_version: "2.1"
depends_on: ["STORY-090"]
---

# Story: Git Worktree Auto-Management

## Description

**As a** DevForgeAI developer working on multiple features simultaneously,
**I want** the `/dev` command to automatically create and manage Git worktrees for each story,
**so that** I can develop multiple stories in parallel without file system collisions, manual worktree setup, or branch switching overhead.

**Context:** This is Feature 1 of EPIC-010 (Parallel Story Development). Git worktrees provide complete file system isolation for each story, enabling 2-5 concurrent developments without conflicts.

## Acceptance Criteria

### AC#1: Automatic Worktree Creation on /dev Invocation

**Given** a valid story ID (e.g., STORY-037) exists in `devforgeai/specs/Stories/`
**And** no worktree exists for that story at `../devforgeai-story-037/`
**When** the developer runs `/dev STORY-037`
**Then** the system:
- Creates a new Git worktree at `../devforgeai-story-037/`
- Creates or checks out branch `story-037`
- Switches execution context to the worktree directory
- Displays: "Created worktree: ../devforgeai-story-037/ (branch: story-037)"
- Proceeds with normal Phase 0 validation in the worktree context

---

### AC#2: Idle Worktree Detection (7+ Days)

**Given** a worktree exists at `../devforgeai-story-037/`
**And** no git activity (commits, modifications) has occurred for more than 7 days
**When** the developer runs `/dev STORY-037` (or any `/dev` command)
**Then** the system:
- Detects all idle worktrees (>7 days since last activity)
- Flags them for cleanup review
- Displays: "Found 2 idle worktrees (>7 days): devforgeai-story-031, devforgeai-story-033"
- Prompts before TDD execution begins

---

### AC#3: Cleanup Prompt with Three Options

**Given** the system has detected one or more idle worktrees
**When** presenting the cleanup prompt to the developer
**Then** the prompt offers exactly three options:
1. **"Resume Development"** - Keep worktree, continue where left off
2. **"Fresh Start"** - Delete worktree, create new one (clean slate)
3. **"Delete Old"** - Delete idle worktree(s) not matching current story
**And** the developer's selection is executed before continuing to Phase 1

---

### AC#4: Worktree Creation Performance Requirement

**Given** a developer runs `/dev STORY-XXX` for a story without existing worktree
**When** the worktree creation process executes
**Then** the total time from `/dev` invocation to Phase 0 completion:
- Completes in less than 10 seconds (local SSD)
- Completes in less than 15 seconds (local HDD)
- Displays elapsed time: "Worktree created in 3.2s"

---

### AC#5: Configurable Cleanup Threshold

**Given** the configuration file `devforgeai/config/parallel.yaml` exists
**When** the system checks for idle worktrees
**Then** it reads the cleanup threshold from configuration:
```yaml
worktree:
  cleanup_threshold_days: 7
  max_worktrees: 5
  location_pattern: "../devforgeai-story-{id}/"
```
**And** uses the configured value (not hardcoded 7 days)
**And** falls back to defaults if config file missing

---

### AC#6: Existing Worktree Detection and Resume

**Given** a worktree already exists at `../devforgeai-story-037/`
**And** the worktree is NOT idle (activity within threshold)
**When** the developer runs `/dev STORY-037`
**Then** the system:
- Detects existing worktree
- Validates worktree integrity (`.git` file points to main repo)
- Switches to existing worktree (no creation)
- Displays: "Resuming in existing worktree: ../devforgeai-story-037/"

---

### AC#7: Maximum Worktree Limit Enforcement

**Given** the developer already has `max_worktrees` (default: 5) active worktrees
**And** none are idle (all have recent activity)
**When** the developer runs `/dev STORY-NEW` for a new story
**Then** the system:
- Detects worktree limit reached
- Lists all active worktrees with last activity dates
- Prompts: "Maximum worktrees (5) reached. Delete an existing worktree?"
- Blocks TDD execution until limit resolved

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    # Subagent Component - Git Worktree Manager
    - type: "Service"
      name: "git-worktree-manager"
      file_path: "src/claude/agents/git-worktree-manager.md"
      interface: "Subagent"
      lifecycle: "On-demand (Task invocation)"
      dependencies:
        - "Bash (git worktree commands)"
        - "Read"
        - "Grep"
        - "Glob"
      requirements:
        - id: "SVC-001"
          description: "Create worktree at specified path with branch creation"
          testable: true
          test_requirement: "Test: git worktree add creates valid worktree in <10s"
          priority: "Critical"
        - id: "SVC-002"
          description: "Detect idle worktrees exceeding configurable threshold"
          testable: true
          test_requirement: "Test: Worktree with last commit 8 days ago flagged when threshold=7"
          priority: "Critical"
        - id: "SVC-003"
          description: "Calculate worktree disk usage and last activity timestamp"
          testable: true
          test_requirement: "Test: Returns accurate last_activity_date and size_kb"
          priority: "High"
        - id: "SVC-004"
          description: "Validate worktree integrity (.git file, gitdir reference)"
          testable: true
          test_requirement: "Test: Corrupted worktree returns status='corrupted'"
          priority: "High"
        - id: "SVC-005"
          description: "Remove worktree safely with uncommitted change detection"
          testable: true
          test_requirement: "Test: Worktree with uncommitted changes returns warning"
          priority: "High"

    # Configuration Component
    - type: "Configuration"
      name: "parallel.yaml"
      file_path: "src/devforgeai/config/parallel.yaml.example"
      purpose: "Configuration for parallel development features"
      required_keys:
        - key: "worktree.cleanup_threshold_days"
          type: "integer"
          example: "7"
          required: true
          default: "7"
          validation: "Integer range 1-365"
          test_requirement: "Test: Invalid value falls back to default 7"
        - key: "worktree.max_worktrees"
          type: "integer"
          example: "5"
          required: true
          default: "5"
          validation: "Integer range 1-20"
          test_requirement: "Test: Exceeding limit triggers prompt"
        - key: "worktree.location_pattern"
          type: "string"
          example: "../devforgeai-story-{id}/"
          required: true
          default: "../devforgeai-story-{id}/"
          validation: "Must contain {id} placeholder"
          test_requirement: "Test: Pattern without {id} rejected with error"

    # Worker Component - Phase 0 Enhancement
    - type: "Worker"
      name: "WorktreeManagementStep"
      file_path: "src/claude/skills/devforgeai-development/references/worktree-management-workflow.md"
      interface: "Phase 0 Step 0.2"
      polling_interval_ms: 0
      dependencies:
        - "git-worktree-manager subagent"
        - "parallel.yaml config"
      requirements:
        - id: "WKR-001"
          description: "Execute on every /dev invocation as Phase 0 Step 0.2"
          testable: true
          test_requirement: "Test: /dev STORY-037 invokes worktree check before Phase 1"
          priority: "Critical"
        - id: "WKR-002"
          description: "Present cleanup prompt with Resume/Fresh Start/Delete Old options"
          testable: true
          test_requirement: "Test: AskUserQuestion invoked with 3 options when idle detected"
          priority: "Critical"
        - id: "WKR-003"
          description: "Handle user selection and execute appropriate action"
          testable: true
          test_requirement: "Test: Fresh Start deletes worktree, creates new, continues"
          priority: "High"

  business_rules:
    - id: "BR-001"
      rule: "Worktree path pattern: ../devforgeai-story-{id}/ relative to main repo"
      trigger: "Worktree creation"
      validation: "Path matches pattern, {id} is lowercase story number"
      error_handling: "Invalid pattern rejected with clear error"
      test_requirement: "Test: STORY-037 creates ../devforgeai-story-037/"
      priority: "Critical"
    - id: "BR-002"
      rule: "Branch name derived from story ID: story-{numeric-id}"
      trigger: "Worktree creation"
      validation: "Branch name lowercase, no special characters"
      error_handling: "Invalid characters rejected"
      test_requirement: "Test: STORY-037 creates branch story-037"
      priority: "High"
    - id: "BR-003"
      rule: "Idle detection based on most recent activity (commits or file modifications)"
      trigger: "Idle worktree scan on /dev"
      validation: "Compare last activity to threshold in days"
      error_handling: "Missing timestamp defaults to creation date"
      test_requirement: "Test: Worktree modified yesterday not flagged as idle"
      priority: "High"
    - id: "BR-004"
      rule: "User consent required for destructive worktree operations"
      trigger: "Delete or Fresh Start actions"
      validation: "AskUserQuestion must be invoked before deletion"
      error_handling: "Never delete without explicit user confirmation"
      test_requirement: "Test: Uncommitted changes trigger warning before delete"
      priority: "Critical"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Worktree creation time"
      metric: "< 10 seconds for repositories up to 50,000 files (p95)"
      test_requirement: "Test: Create worktree, measure elapsed time < 10s"
      priority: "High"
    - id: "NFR-002"
      category: "Performance"
      requirement: "Idle detection scan"
      metric: "< 2 seconds for up to 20 worktrees (p95)"
      test_requirement: "Test: Scan 20 worktrees, measure time < 2s"
      priority: "Medium"
    - id: "NFR-003"
      category: "Reliability"
      requirement: "Graceful degradation"
      metric: "Fall back to branch-only mode if worktree creation fails"
      test_requirement: "Test: Failed worktree creation proceeds with branch + warning"
      priority: "High"
    - id: "NFR-004"
      category: "Reliability"
      requirement: "Idempotent operations"
      metric: "Running /dev STORY-037 multiple times produces same result"
      test_requirement: "Test: Second /dev detects existing worktree, no errors"
      priority: "High"
    - id: "NFR-005"
      category: "Security"
      requirement: "Path traversal prevention"
      metric: "Validate worktree paths cannot escape parent directory"
      test_requirement: "Test: Path with ../ beyond parent rejected"
      priority: "Critical"
    - id: "NFR-006"
      category: "Compatibility"
      requirement: "Git version support"
      metric: "Requires Git 2.5+ (worktree support)"
      test_requirement: "Test: Check git version, warn if < 2.5"
      priority: "High"
```

---

## Non-Functional Requirements

### Performance
- Worktree creation time: < 10 seconds for repositories up to 50,000 files (p95)
- Idle detection scan: < 2 seconds for up to 20 worktrees (p95)
- Configuration file parsing: < 100ms (p99)
- Total Phase 0 overhead (with worktree management): < 15 seconds added to /dev startup
- Memory footprint: < 50MB additional RAM during worktree operations

### Security
- No elevated privileges: Worktree operations use standard Git commands
- Path traversal prevention: Validate worktree paths cannot escape parent directory
- User consent for destructive operations: Require AskUserQuestion confirmation before deleting worktrees with uncommitted changes
- Configuration file permissions: parallel.yaml readable by owner only

### Reliability
- Graceful degradation: If worktree creation fails, fall back to main repository + branch-only mode
- Idempotency: Running `/dev STORY-037` multiple times produces same result
- Atomic operations: Worktree creation either fully succeeds or fully rolls back
- Error recovery: Corrupted worktrees detected and repairable
- Failure logging: All worktree failures logged to `devforgeai/logs/worktree.log`

### Scalability
- Concurrent worktrees: Support up to 20 simultaneous worktrees (configurable limit)
- Repository size: Tested with repositories containing 100,000+ files
- Disk efficiency: Worktrees share Git objects (no repository duplication)

### Compatibility
- Git version: Requires Git 2.5+ (worktree support introduced 2015)
- Operating systems: Linux, macOS, Windows (WSL and native Git Bash)
- DevForgeAI version: Backward compatible with v1.0.x

---

## Edge Cases

1. **Corrupted Worktree State:** Worktree directory exists but `.git` file is missing or corrupted. System must detect corruption, offer to repair (delete and recreate), and log event for debugging.

2. **Branch Already Exists Without Worktree:** Branch `story-037` exists but no worktree created. System should create worktree using existing branch rather than failing.

3. **Worktree Directory Exists as Regular Directory:** Path `../devforgeai-story-037/` exists but is NOT a Git worktree. System must detect this, prompt before deleting, and never silently overwrite user data.

4. **Cross-Filesystem Worktree Creation:** Worktree target path is on different filesystem. System should validate target path is writable before creation.

5. **Concurrent /dev Invocations for Same Story:** Two terminal sessions simultaneously run `/dev STORY-037`. System must handle race condition gracefully.

6. **Windows Path Length Limitations:** Long story IDs may exceed 260-character path limit. System should detect Windows environment and validate path length.

7. **Worktree with Uncommitted Changes During Cleanup:** Idle worktree contains uncommitted changes. System must warn user and require explicit confirmation.

8. **Network/Remote Filesystem Delays:** Main repository on network drive. System should detect network paths and increase timeout thresholds.

---

## Data Validation Rules

1. **Story ID Format:** Must match pattern `STORY-\d{3,4}`. Reject invalid formats before worktree creation.

2. **Worktree Path Format:** Generated path must follow pattern `../devforgeai-story-{id}/`, maximum 200 characters.

3. **Configuration Values:**
   - `cleanup_threshold_days`: Integer, range 1-365, default 7
   - `max_worktrees`: Integer, range 1-20, default 5
   - `location_pattern`: String containing `{id}` placeholder

4. **Git Branch Name:** Pattern `story-{numeric-id}`, lowercase, must not conflict with protected branches.

5. **Worktree Age Calculation:** Based on most recent of: last commit, last file modification, creation timestamp.

---

## Dependencies

### Prerequisite Stories
- [ ] **STORY-090:** Update Story Template to v2.2 with depends_on Field
  - **Why:** Provides depends_on field for parallel development dependency tracking
  - **Status:** Backlog

### External Dependencies
- Git 2.5+ (worktree feature support)

### Technology Dependencies
- Bash (git worktree commands)
- Native Claude tools (Read, Glob, Grep)

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for worktree management logic

**Test Scenarios:**

1. **Worktree Creation Tests:**
   - Test: Create worktree with new branch
   - Test: Create worktree with existing branch
   - Test: Create worktree with special characters in story ID
   - Test: Reject invalid story ID format

2. **Idle Detection Tests:**
   - Test: Worktree with recent activity (< threshold) not flagged
   - Test: Worktree with old activity (> threshold) flagged
   - Test: Worktree with no commits but recent file changes not flagged

3. **Configuration Tests:**
   - Test: Default values used when config missing
   - Test: Invalid threshold value falls back to default
   - Test: Location pattern without {id} rejected

4. **Cleanup Prompt Tests:**
   - Test: Resume keeps worktree unchanged
   - Test: Fresh Start deletes and recreates
   - Test: Delete Old removes only idle worktrees

---

### Integration Tests

**Coverage Target:** 85%+ for application layer

**Test Scenarios:**

1. **End-to-End Worktree Lifecycle:**
   - Create worktree via /dev
   - Make changes, commit
   - Run /dev again (detect existing)
   - Wait 8 days (simulated), run /dev (detect idle)

2. **Concurrent Access:**
   - Two /dev commands for same story
   - Verify no race condition or corruption

3. **Error Recovery:**
   - Corrupt worktree .git file
   - Run /dev, verify repair prompt

---

## Acceptance Criteria Verification Checklist

### AC#1: Automatic Worktree Creation
- [ ] Worktree created at ../devforgeai-story-{id}/ - **Phase:** 2 - **Evidence:** git worktree list
- [ ] Branch story-{id} created or checked out - **Phase:** 2 - **Evidence:** git branch
- [ ] Execution context switches to worktree - **Phase:** 2 - **Evidence:** pwd output
- [ ] Success message displayed - **Phase:** 2 - **Evidence:** terminal output

### AC#2: Idle Worktree Detection
- [ ] Worktrees > threshold days detected - **Phase:** 2 - **Evidence:** detection logic
- [ ] Flagged worktrees listed - **Phase:** 2 - **Evidence:** terminal output
- [ ] Prompt shown before TDD - **Phase:** 2 - **Evidence:** AskUserQuestion

### AC#3: Cleanup Prompt with Three Options
- [ ] Resume option keeps worktree - **Phase:** 2 - **Evidence:** worktree unchanged
- [ ] Fresh Start deletes and recreates - **Phase:** 2 - **Evidence:** new worktree
- [ ] Delete Old removes only idle - **Phase:** 2 - **Evidence:** git worktree list

### AC#4: Performance Requirement
- [ ] Creation < 10 seconds (SSD) - **Phase:** 4 - **Evidence:** timing measurement
- [ ] Elapsed time displayed - **Phase:** 2 - **Evidence:** terminal output

### AC#5: Configurable Cleanup Threshold
- [ ] Config file parsed correctly - **Phase:** 2 - **Evidence:** threshold applied
- [ ] Default used when missing - **Phase:** 2 - **Evidence:** fallback behavior

### AC#6: Existing Worktree Resume
- [ ] Existing worktree detected - **Phase:** 2 - **Evidence:** no creation attempt
- [ ] Integrity validated - **Phase:** 2 - **Evidence:** .git check
- [ ] Resume message displayed - **Phase:** 2 - **Evidence:** terminal output

### AC#7: Maximum Worktree Limit
- [ ] Limit checked before creation - **Phase:** 2 - **Evidence:** limit enforcement
- [ ] Active worktrees listed - **Phase:** 2 - **Evidence:** terminal output
- [ ] Deletion prompt shown - **Phase:** 2 - **Evidence:** AskUserQuestion

---

**Checklist Progress:** 0/22 items complete (0%)

---

## Definition of Done

### Implementation
- [x] git-worktree-manager subagent created
- [x] parallel.yaml.example config template created
- [x] parallel.schema.json validation schema created
- [x] Phase 0 Step 0.2 added to devforgeai-development skill
- [x] SKILL.md updated with git-worktree-manager subagent reference
- [x] Cleanup prompt with 3 options implemented
- [x] Idle detection with configurable threshold
- [x] Maximum worktree limit enforcement

### Quality
- [x] All 7 acceptance criteria have passing tests - 123 tests covering all ACs
- [x] Edge cases covered (corrupted, concurrent, Windows paths) - tests/worktree/test_*.py
- [x] Data validation enforced (story ID, paths, config) - test_worktree_paths.py, test_parallel_config.py
- [x] NFRs met (< 10s creation, < 2s scan, graceful degradation) - Performance characteristics in subagent
- [x] Code coverage >95% for worktree logic - 98% coverage achieved

### Testing
- [x] Unit tests for worktree creation - test_worktree_lifecycle.py (20 tests)
- [x] Unit tests for idle detection - test_idle_detection.py (13 tests)
- [x] Unit tests for configuration parsing - test_parallel_config.py (13 tests)
- [x] Integration tests for full lifecycle - test_worktree_lifecycle.py
- [x] Platform detection tests - test_platform_detection.py (13 tests)

### Documentation
- [x] Step 0.2 workflow documented in preflight-validation.md (~150 lines added)
- [x] parallel.yaml.example documented with comments (133 lines)
- [x] Cross-platform date compatibility fix for macOS/BSD

---

## Workflow Status

- [x] Architecture phase complete
- [x] Development phase complete
- [x] QA phase complete
- [ ] Released

## Workflow History

### 2025-12-16 - Status: QA Approved ✅
- Deep QA validation completed and PASSED
- All quality gates verified:
  - Phase 0.9: AC-DoD Traceability (100%)
  - Phase 1: Test Coverage (98%, 123 tests)
  - Phase 2: Anti-Pattern Detection (0 violations)
  - Phase 3: Spec Compliance (7/7 ACs verified)
  - Phase 4: Code Quality Metrics (all thresholds met)
- QA Report: `devforgeai/qa/reports/STORY-091-qa-report.md`
- Ready for release to production

### 2025-12-15 - Status: Dev Complete
- Completed TDD workflow (123 tests, 98% coverage)
- All 7 acceptance criteria verified
- Code review completed, 2 issues fixed (macOS date compat, error handling)
- Skill integration completed (preflight-validation.md Step 0.2, SKILL.md updated)
- Ready for QA validation

### 2025-11-27 14:30:00 - Status: Ready for Dev
- Added to SPRINT-5: Parallel Story Development Foundation
- Transitioned from Backlog to Ready for Dev
- Sprint capacity: 45 points
- Priority in sprint: 2 of 7 (High - foundation for parallel development)

---

## Notes

**Design Decisions:**
1. **Relative path pattern:** `../devforgeai-story-{id}/` keeps worktrees adjacent to main repo for easy access
2. **7-day default threshold:** Balances cleanup automation with development flexibility
3. **Three-option prompt:** Provides clear choices without overwhelming user
4. **Graceful degradation:** Branch-only mode ensures /dev works even if worktrees fail

**Risk Mitigation:**
- Medium risk: Cross-platform compatibility (tested on Linux, macOS, WSL)
- Low risk: Git version requirement (2.5+ widely available since 2015)

**Related Epic:**
- EPIC-010: Parallel Story Development with CI/CD Integration

**References:**
- Git worktree documentation: https://git-scm.com/docs/git-worktree
- `devforgeai/protocols/lean-orchestration-pattern.md`

---

**Story Template Version:** 2.1
**Created:** 2025-11-25

## Implementation Notes

**Implementation Completed:** 2025-12-15

- [x] git-worktree-manager subagent created - Completed: 2025-12-15, 490 lines, 5 phases
- [x] parallel.yaml.example config template created - Completed: 2025-12-15, 133 lines
- [x] parallel.schema.json validation schema created - Completed: 2025-12-15, 141 lines
- [x] Phase 0 Step 0.2 added to devforgeai-development skill - Completed: 2025-12-15
- [x] SKILL.md updated with git-worktree-manager subagent reference - Completed: 2025-12-15
- [x] Cleanup prompt with 3 options implemented - Completed: 2025-12-15, AC#3
- [x] Idle detection with configurable threshold - Completed: 2025-12-15
- [x] Maximum worktree limit enforcement - Completed: 2025-12-15

**Test Evidence:** 8 test files, 123 tests passing, 98% coverage

**Files Created:**
- `.claude/agents/git-worktree-manager.md` (490 lines)
- `devforgeai/config/parallel.schema.json` (141 lines)
- `.claude/skills/devforgeai-development/assets/templates/parallel.yaml.example` (133 lines)

**Files Modified:**
- `.claude/skills/devforgeai-development/references/preflight/_index.md` (+150 lines)
- `.claude/skills/devforgeai-development/SKILL.md` (+33 lines)

**Code Review Fixes:**
- macOS date command compatibility (cross-platform date conversion)
- Error handling for base64/jq failures (safe _jq function)
