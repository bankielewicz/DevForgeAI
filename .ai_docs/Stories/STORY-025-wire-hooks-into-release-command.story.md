---
id: STORY-025
title: Wire hooks into /release command
epic: EPIC-006
sprint: Sprint-2
status: Backlog
points: 5
priority: Critical
assigned_to: TBD
created: 2025-11-12
format_version: "2.0"
---

# Story: Wire hooks into /release command

## Description

**As a** DevOps engineer deploying stories via /release,
**I want** automatic retrospective feedback prompts after both staging and production deployments complete,
**so that** I can reflect on deployment experiences (issues, surprises, performance) immediately while context is fresh, without needing to manually trigger /feedback.

## Acceptance Criteria

### AC1: Hook Integration into Staging Deployment (Success Path)
**Given** a user runs `/release STORY-025 staging` and staging deployment succeeds,
**When** the staging deployment completes (smoke tests pass, deployment validated),
**Then** the system invokes `devforgeai check-hooks --operation=release-staging --status=SUCCESS` (<100ms),
**And** if hooks are enabled and trigger matches, invokes `devforgeai invoke-hooks --operation=release-staging --story=STORY-025` (<3s),
**And** presents retrospective questions (deployment issues, performance observations, unexpected behaviors),
**And** proceeds to completion message after feedback collection.

### AC2: Hook Integration into Staging Deployment (Failure Path)
**Given** a user runs `/release STORY-025 staging` and staging deployment fails (smoke test failure, infrastructure error, validation failure),
**When** the deployment failure is detected,
**Then** the system invokes `devforgeai check-hooks --operation=release-staging --status=FAILURE`,
**And** invokes `devforgeai invoke-hooks --operation=release-staging --story=STORY-025` (failure triggers enabled by default),
**And** presents failure-specific retrospective questions (what went wrong, root cause observations, mitigation notes),
**And** displays deployment failure summary after feedback collection.

### AC3: Hook Integration into Production Deployment (Success Path)
**Given** staging deployment succeeded and user approved production deployment,
**When** production deployment completes successfully (all production smoke tests pass),
**Then** the system invokes `devforgeai check-hooks --operation=release-production --status=SUCCESS`,
**And** if hooks enabled for production success (default: failures-only disabled for production success),
**Then** proceeds to completion without feedback prompt (respects failures-only default),
**Or** if user configured `"on_success": true` in hooks.yaml, invokes feedback prompt.

### AC4: Hook Integration into Production Deployment (Failure Path)
**Given** production deployment fails (rollback triggered, smoke tests fail, infrastructure unavailable),
**When** the production deployment failure is detected,
**Then** the system invokes `devforgeai check-hooks --operation=release-production --status=FAILURE`,
**And** invokes `devforgeai invoke-hooks --operation=release-production --story=STORY-025` (failure triggers always enabled),
**And** presents critical failure retrospective questions (production impact, rollback observations, incident notes),
**And** displays failure summary with rollback status after feedback collection.

### AC5: Graceful Degradation on Hook Failures
**Given** a user runs `/release STORY-025` and hook infrastructure encounters errors (CLI not installed, config file missing, hook script crashes),
**When** `devforgeai check-hooks` or `devforgeai invoke-hooks` fails (exit code ≠ 0),
**Then** the system logs warning "Hook execution failed: [error details]" to `.devforgeai/logs/release-hooks-STORY-025.log`,
**And** continues deployment workflow without interruption,
**And** displays note "Note: Post-deployment feedback unavailable (hook error)" in completion message,
**And** deployment status remains accurate (success/failure based on deployment, not hook status).

### AC6: Hook Eligibility Validation
**Given** hooks.yaml configuration exists with `release-staging` and `release-production` hooks defined,
**When** `devforgeai check-hooks --operation=release-staging --status=SUCCESS` is invoked,
**Then** the CLI reads hooks.yaml and evaluates:
- Hook exists for `release-staging` operation ✓
- `enabled: true` in configuration ✓
- Trigger matches (status SUCCESS vs. trigger `on_success: false` default) → eligibility FALSE (skip hook)
**And** returns exit code 1 (not eligible) with message "Hook skipped: trigger does not match (failures-only mode)",
**And** /release command skips `invoke-hooks` call, proceeds to next phase.

### AC7: Consistent UX Across Commands
**Given** a user has used /dev and /qa commands with hooks enabled,
**When** the user runs `/release STORY-025` and encounters a staging deployment failure,
**Then** the feedback questions presented match the same adaptive questioning engine patterns:
- Question routing based on operation context (release-specific questions: deployment speed, rollback effectiveness, infrastructure issues)
- Skip tracking active (user can skip questions, patterns recorded)
- Retrospective config respected (same hot-reload behavior, same question customization)
- Answer persistence to `.devforgeai/feedback/releases/STORY-025-staging-[timestamp].json` (same file structure as dev/qa feedback)
**And** user experience feels identical (same CLI output formatting, same question flow, same skip behavior).

## Edge Cases

### Edge Case 1: Multiple Deployment Attempts (Retry Scenario)
**Scenario:** User runs `/release STORY-025 staging`, deployment fails, user fixes issue and re-runs `/release STORY-025 staging`.
**Expected Behavior:**
- First attempt: Hook triggered on failure (feedback collected, saved to `STORY-025-staging-[timestamp1].json`)
- Second attempt: Hook triggered again on success/failure (new feedback collected, saved to `STORY-025-staging-[timestamp2].json`)
- System maintains separate feedback files per attempt (timestamp differentiation)
- No feedback file overwrites (each deployment attempt generates unique feedback record)

### Edge Case 2: Staging Success → Production Deployment Skipped by User
**Scenario:** Staging deployment succeeds, hook prompt appears (if configured), user completes feedback, then user decides NOT to proceed to production (cancels at approval prompt).
**Expected Behavior:**
- Staging hook completes successfully (feedback saved)
- Production deployment never starts (user canceled)
- No production hook triggered (operation never executed)
- Staging feedback persists in `.devforgeai/feedback/releases/STORY-025-staging-[timestamp].json`
- Story status remains "Staging Complete" (not "Released")

### Edge Case 3: Simultaneous Staging and Production Hooks (Unlikely but Possible)
**Scenario:** User configured `/release` to deploy to staging AND production in a single command (non-standard but technically possible), both complete simultaneously.
**Expected Behavior:**
- System invokes `check-hooks` for `release-staging` first, then `release-production`
- If both eligible, invokes hooks sequentially (staging feedback → production feedback)
- Two separate feedback sessions (user answers staging questions, then production questions)
- Feedback saved to two files: `STORY-025-staging-[timestamp].json` and `STORY-025-production-[timestamp].json`
- Hook invocation total time: <6s (3s staging + 3s production, within acceptable delay)

### Edge Case 4: Hook Configuration Changed Mid-Deployment
**Scenario:** Deployment starts with hooks enabled, during deployment user edits `.devforgeai/config/hooks.yaml` to disable release hooks, deployment completes.
**Expected Behavior:**
- Hook eligibility checked at deployment completion time (not deployment start time)
- If hooks disabled by completion, `check-hooks` returns exit code 1 (not eligible)
- No feedback prompt presented (respects current configuration)
- Deployment completes normally without feedback

### Edge Case 5: Rollback Triggered During Production Deployment
**Scenario:** Production deployment detects critical issue (smoke test fails, health check fails), automatic rollback executes, rollback succeeds.
**Expected Behavior:**
- Deployment status = FAILURE (rollback was necessary)
- Hook triggered with `--status=FAILURE` (even though rollback succeeded)
- Feedback questions focus on failure context: "What triggered the rollback?", "Was rollback smooth?", "What would prevent this in future?"
- Rollback details included in operation context (hook receives rollback metadata)

### Edge Case 6: Production Deployment Partial Success (Some Services Deploy, Some Fail)
**Scenario:** Multi-service deployment, 2 of 3 services deploy successfully to production, 1 fails, overall deployment marked as FAILURE.
**Expected Behavior:**
- Hook triggered with `--status=FAILURE` (overall deployment failed)
- Operation context includes partial success details (`deployed_services: [service1, service2], failed_services: [service3]`)
- Feedback questions probe partial failure: "Which services deployed successfully?", "What caused service3 to fail?", "Impact of partial deployment?"
- Feedback saved with partial deployment metadata

## Technical Specification

```yaml
components:
  - type: Service
    name: ReleaseCommandHookIntegration
    file_path: .claude/commands/release.md
    description: |
      Integrates feedback hook system into /release command workflow. Adds Phase N
      (Post-Deployment Hooks) that executes after staging and production deployments
      complete. Triggers retrospective feedback conversations for deployment reflection
      without manual user action.
    dependencies:
      - devforgeai CLI (check-hooks command)
      - devforgeai CLI (invoke-hooks command)
      - .devforgeai/config/hooks.yaml
      - Feedback persistence layer
    interfaces:
      - name: check-hooks CLI
        type: CLI invocation
        operations:
          - operation: check-hooks
            parameters: ["--operation=release-staging|release-production", "--status=SUCCESS|FAILURE"]
            returns: "Exit code (0=eligible, 1=not eligible, 2+=error)"
      - name: invoke-hooks CLI
        type: CLI invocation
        operations:
          - operation: invoke-hooks
            parameters: ["--operation=release-staging|release-production", "--story=STORY-ID"]
            returns: "Exit code (0=success, 2+=error)"
    test_requirements:
      - requirement: Hook phase executes after staging deployment, before completion message
        type: integration
        priority: critical
      - requirement: check-hooks called with correct operation and deployment status
        type: unit
        priority: critical
      - requirement: invoke-hooks called only when check-hooks returns 0
        type: integration
        priority: critical
      - requirement: Production hooks triggered separately from staging hooks
        type: integration
        priority: critical
      - requirement: Hook CLI errors logged, deployment proceeds
        type: integration
        priority: high
      - requirement: Operation context includes environment, status, rollback, services
        type: unit
        priority: high
      - requirement: Hook integration adds <3.5 seconds overhead
        type: performance
        priority: medium

  - type: Configuration
    name: ReleaseHooksConfiguration
    file_path: .devforgeai/config/hooks.yaml
    description: |
      Hook configuration schema extension for release command. Defines staging and
      production hook triggers, questions, and behavior. Defaults to failures-only
      mode for production (less intrusive for successful deployments).
    dependencies: []
    interfaces:
      - name: YAML schema
        type: Configuration file
        operations:
          - operation: read_config
            parameters: ["operation_name"]
            returns: "HookConfig(enabled, triggers, questions)"
    test_requirements:
      - requirement: hooks.yaml validates with release-staging operation
        type: unit
        priority: critical
      - requirement: hooks.yaml validates with release-production operation
        type: unit
        priority: critical
      - requirement: Default config skips production success, triggers production failure
        type: integration
        priority: high
      - requirement: Staging questions differ from production questions
        type: integration
        priority: medium

  - type: Logging
    name: ReleaseHookLogger
    file_path: .devforgeai/logs/release-hooks-{STORY-ID}.log
    description: |
      Structured logging for release hook invocations. Logs all hook attempts
      (success, failure, skip) with timestamps, operation context, and exit codes.
      Enables debugging and audit trail for hook system reliability.
    dependencies:
      - Python logging module
      - File system write permissions
    interfaces:
      - name: Log writer
        type: File I/O
        operations:
          - operation: log_hook_invocation
            parameters: ["timestamp", "operation", "story_id", "status", "exit_code"]
            returns: "None (writes to file)"
    test_requirements:
      - requirement: Log file created on first hook invocation with structured JSON
        type: integration
        priority: high
      - requirement: Hook CLI crash logged with error details
        type: integration
        priority: high
      - requirement: Skipped hooks logged with reason
        type: unit
        priority: medium
      - requirement: Log rotation at 10MB threshold
        type: integration
        priority: low

  - type: DataModel
    name: ReleaseFeedbackRecord
    file_path: .devforgeai/feedback/releases/{STORY-ID}-{environment}-{timestamp}.json
    description: |
      Extended feedback record schema for deployment-specific metadata. Includes
      environment (staging/production), deployment status, rollback flag, deployed
      services list, and deployment duration. Enables richer retrospective analysis.
    dependencies:
      - Feedback persistence layer (STORY-019)
    interfaces:
      - name: Feedback JSON schema
        type: Data model
        operations:
          - operation: save_feedback
            parameters: ["operation_context", "user_answers", "metadata"]
            returns: "Feedback file path"
    test_requirements:
      - requirement: Feedback JSON includes environment, deployment_status, rollback_triggered, deployed_services
        type: unit
        priority: critical
      - requirement: Separate feedback files for staging and production
        type: integration
        priority: high
      - requirement: Feedback JSON includes deployment_duration_seconds
        type: unit
        priority: medium

business_rules:
  - rule: Hook eligibility evaluated at deployment completion time (not start time)
    rationale: Respects real-time configuration changes (user can enable/disable hooks mid-deployment)
    test_requirement: "Configuration changed mid-deployment edge case validated"

  - rule: Staging and production hooks trigger independently (two separate check-hooks calls)
    rationale: Different trigger configurations (staging may trigger on success, production failures-only by default)
    test_requirement: "Both staging and production hooks can trigger in single /release execution"

  - rule: Hook failures never affect deployment status (deployment success/failure independent of hook status)
    rationale: Retrospective feedback is optional enhancement, not critical path; deployment correctness is primary concern
    test_requirement: "Hook CLI crashes logged, deployment marked successful if actual deployment succeeded"

  - rule: Failures-only default for production hooks (on_success: false, on_failure: true)
    rationale: Less intrusive UX for successful production deployments (most deployments succeed, feedback valuable mainly for failures)
    test_requirement: "Production success skips feedback unless user configured on_success: true"

  - rule: Operation context includes deployment-specific metadata (environment, rollback status, deployed services)
    rationale: Enables context-aware questioning (different questions for staging vs. production, for rollback vs. clean deployment)
    test_requirement: "invoke-hooks receives operation context JSON with deployment metadata"

  - rule: Hook invocation timeout 30 seconds (auto-skip if user unresponsive)
    rationale: Prevents deployment workflow from hanging indefinitely if user walks away mid-feedback
    test_requirement: "invoke-hooks exceeds 30s, command logs timeout warning and proceeds"

non_functional_requirements:
  - category: Performance
    requirement: Hook eligibility check completes in <100ms
    metric: "Response time from check-hooks invocation to exit code return"
    target: "<100ms (p95)"
    priority: high

  - category: Performance
    requirement: Hook invocation completes in <3 seconds
    metric: "Time from invoke-hooks start to feedback file written"
    target: "<3s (p95)"
    priority: high

  - category: Performance
    requirement: Total deployment delay from hook integration <3.5 seconds
    metric: "Deployment duration with hooks minus deployment duration without hooks"
    target: "<3.5s (average)"
    priority: medium

  - category: Reliability
    requirement: Hook failures never break deployment workflow
    metric: "Percentage of deployments completing successfully despite hook errors"
    target: "100%"
    priority: critical

  - category: Reliability
    requirement: All hook errors logged with context for debugging
    metric: "Percentage of hook errors with complete stack trace in logs"
    target: "100%"
    priority: high

  - category: Reliability
    requirement: Hook invocation idempotent (retry-safe)
    metric: "Percentage of hook retries resulting in duplicate feedback files"
    target: "0% (all retries create unique timestamped files)"
    priority: medium

  - category: Security
    requirement: Feedback files created with restrictive permissions (owner read/write only)
    metric: "File permissions on newly created feedback JSON files"
    target: "0600 (owner rw, no group/world access)"
    priority: high

  - category: Security
    requirement: Hook CLI input sanitization prevents injection attacks
    metric: "Percentage of malicious inputs successfully sanitized"
    target: "100%"
    priority: medium

  - category: Usability
    requirement: Consistent UX across /dev, /qa, /release commands
    metric: "User feedback on consistency (survey question)"
    target: "80%+ users report 'same experience across commands'"
    priority: medium

  - category: Usability
    requirement: User can abort feedback session without breaking deployment
    metric: "Percentage of Ctrl+C aborts that result in accurate deployment status"
    target: "100%"
    priority: high

  - category: Maintainability
    requirement: Hook integration pattern reusable for remaining 8 commands
    metric: "Code duplication percentage across command hook integrations"
    target: "<10% (centralized CLI, config-driven)"
    priority: medium

  - category: Maintainability
    requirement: Configuration hot-reload (no command restart required for config changes)
    metric: "Time from hooks.yaml edit to configuration active"
    target: "0s (immediate)"
    priority: low
```

## UI Specification

**UI Required:** No - This is a CLI command enhancement with no graphical user interface.

**CLI Interaction Details:**
- Hook invocation occurs in terminal after deployment completion
- Feedback questions presented via `devforgeai invoke-hooks` CLI (text-based Q&A)
- Progress indicators: "Question 2 of 5" (CLI text output)
- Skip behavior: Press Enter to skip question (CLI input handling)
- Abort: Ctrl+C to exit feedback session (signal handling)

**No additional UI specification needed** - CLI interaction patterns already defined in STORY-020 (Feedback CLI Commands).

## Definition of Done

### Implementation
- [ ] Phase N (Post-Deployment Hooks) added to `.claude/commands/release.md`
- [ ] Hook check invoked after staging deployment: `devforgeai check-hooks --operation=release-staging --status=$STATUS`
- [ ] Hook invocation conditional on check result: `if [ $? -eq 0 ]; then devforgeai invoke-hooks ...`
- [ ] Hook check invoked after production deployment: `devforgeai check-hooks --operation=release-production --status=$STATUS`
- [ ] Hook invocation conditional on check result for production
- [ ] Operation context passed to invoke-hooks (environment, deployment status, rollback flag, deployed services)
- [ ] Graceful degradation implemented (hook errors logged, deployment proceeds)
- [ ] Hook invocation logs written to `.devforgeai/logs/release-hooks-{STORY-ID}.log`

### Configuration
- [ ] `release-staging` hook definition added to hooks.yaml schema example
- [ ] `release-production` hook definition added to hooks.yaml schema example
- [ ] Default triggers documented: `on_failure: true`, `on_success: false` for production
- [ ] Custom questions documented per deployment environment (staging vs. production)

### Quality
- [ ] AC1-AC7 test coverage 100% (all acceptance criteria have corresponding tests)
- [ ] Unit tests: Hook eligibility validation logic
- [ ] Integration tests: Hook invocation in /release workflow (staging and production)
- [ ] Integration tests: Graceful degradation (hook CLI not installed, hook crashes)
- [ ] Integration tests: Configuration hot-reload (config changed mid-deployment)
- [ ] Performance tests: Hook check <100ms, invocation <3s, total overhead <3.5s
- [ ] Edge case tests: All 6 edge cases validated (retry, skip prod, simultaneous, config change, rollback, partial success)
- [ ] Regression tests: Existing /release behavior unchanged when hooks disabled

### Testing
- [ ] Manual test: /release with hooks enabled (staging failure triggers feedback)
- [ ] Manual test: /release with hooks disabled (no feedback prompt)
- [ ] Manual test: /release production success (skips feedback by default)
- [ ] Manual test: /release production failure (triggers feedback)
- [ ] Manual test: Hook CLI not installed (warning logged, deployment succeeds)
- [ ] Manual test: User skips all feedback questions (skip tracking increments)
- [ ] Manual test: User aborts feedback with Ctrl+C (deployment status accurate)
- [ ] Manual test: Multiple deployment retries (separate feedback files per attempt)

### Documentation
- [ ] /release command Phase N documented with inline comments
- [ ] Hook integration pattern documented in `.devforgeai/docs/hook-integration-pattern.md`
- [ ] Release hook configuration examples in `.devforgeai/config/hooks.yaml.example`
- [ ] Troubleshooting guide updated with release-specific hook issues

### Deployment
- [ ] Changes committed to version control
- [ ] /release command tested in staging environment
- [ ] Hook integration tested with real story deployment
- [ ] Rollback plan documented (comment out Phase N if issues arise)

## Dependencies

- **STORY-021:** devforgeai check-hooks CLI command (MUST be complete)
- **STORY-022:** devforgeai invoke-hooks CLI command (MUST be complete)
- **STORY-023:** /dev command pilot (reference implementation for pattern)
- **STORY-024:** /qa command integration (validates pattern works across commands)

## Story History

| Date | Event | Notes |
|------|-------|-------|
| 2025-11-12 | Created | Part of EPIC-006 Feature 6.2 rollout (third command after /dev, /qa) |
