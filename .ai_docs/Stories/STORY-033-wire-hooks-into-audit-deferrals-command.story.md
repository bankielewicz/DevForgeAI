---
id: STORY-033
title: Wire hooks into /audit-deferrals command
epic: EPIC-006
sprint: Sprint-3
status: Backlog
points: 4
priority: High
assigned_to: TBD
created: 2025-11-13
format_version: "2.0"
---

# Story: Wire hooks into /audit-deferrals command

## Description

**As a** DevForgeAI maintainer,
**I want** the /audit-deferrals command to automatically trigger post-audit feedback when eligible,
**so that** I can capture insights about the audit process, deferral patterns discovered, and debt reduction strategies while the analysis is fresh in my mind.

## Acceptance Criteria

### 1. [ ] Hook Eligibility Check After Audit Complete

**Given** the /audit-deferrals command has completed Phase 5 (audit report generation) and all deferral validation is complete,
**When** the command reaches the hook integration phase,
**Then** it invokes `devforgeai check-hooks --operation=audit-deferrals --status=completed` to determine feedback eligibility,
**And** the eligibility result (eligible: true/false) is captured,
**And** the command proceeds to feedback invocation only if eligible=true.

---

### 2. [ ] Automatic Feedback Invocation When Eligible

**Given** the hook eligibility check returns eligible=true,
**When** the eligibility check completes successfully,
**Then** the command invokes `devforgeai invoke-hooks --operation=audit-deferrals` automatically,
**And** the feedback conversation launches with audit-specific context,
**And** operation_metadata includes audit_summary with resolvable_count, valid_count, invalid_count, oldest_age (days), and circular_chains (array of STORY-IDs),
**And** retrospective questions adapt to reference the audit findings.

---

### 3. [ ] Graceful Degradation on Hook Failures

**Given** hook eligibility check or invocation fails (CLI not installed, config error, hook execution error),
**When** the failure occurs during hook integration phase,
**Then** the command logs a warning message: "Feedback system unavailable (reason: [error_type]), continuing without feedback...",
**And** the /audit-deferrals workflow completes normally without throwing exceptions,
**And** the user receives their complete audit report in `.devforgeai/qa/deferral-audit-{timestamp}.md`,
**And** the command exits with status code 0 (success).

---

### 4. [ ] Context-Aware Feedback Collection

**Given** feedback conversation is invoked after audit completion,
**When** the retrospective questions are presented to the user,
**Then** questions reference audit-specific context (e.g., "You found [X] resolvable deferrals. What patterns did you notice?"),
**And** operation_metadata includes audit_summary: {resolvable_count: int, valid_count: int, invalid_count: int, oldest_age: int, circular_chains: [STORY-IDs]},
**And** the feedback captures actionable insights for improving deferral management processes,
**And** the context size is ≤50KB (summarized if necessary).

---

### 5. [ ] Pilot Pattern Consistency

**Given** hook integration follows the /dev pilot pattern established in STORY-023,
**When** implementing the hook integration phase in /audit-deferrals,
**Then** the implementation structure matches the pilot (Phase N: eligibility check → conditional invocation → graceful degradation),
**And** error handling follows the same approach (log warnings, don't break workflow, exit cleanly),
**And** the hook phase is documented with clear phase number and workflow position,
**And** the code structure is recognizable as the same pattern used in /dev.

---

### 6. [ ] Invocation Tracking and Audit Trail

**Given** hooks are invoked during /audit-deferrals execution,
**When** either check-hooks or invoke-hooks is called,
**Then** all invocations are logged to `.devforgeai/feedback/logs/hook-invocations.log` with timestamp, operation, status, and outcome,
**And** failures include error messages and stack traces for debugging,
**And** successful invocations include feedback session ID for traceability,
**And** the log file is created if it doesn't exist (with proper permissions).

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "audit-deferrals command hook integration"
      file_path: ".claude/commands/audit-deferrals.md"
      requirements:
        - id: "CONF-001"
          description: "Add Phase N after Phase 5 (audit report generation) to invoke hooks"
          testable: true
          test_requirement: "Test: Verify Phase N section exists in command file after Phase 5"
          priority: "Critical"

        - id: "CONF-002"
          description: "Add bash code block calling 'devforgeai check-hooks --operation=audit-deferrals --status=completed'"
          testable: true
          test_requirement: "Test: Verify check-hooks call with correct arguments exists in Phase N"
          priority: "Critical"

        - id: "CONF-003"
          description: "Add conditional logic: if exit code 0, call 'devforgeai invoke-hooks --operation=audit-deferrals'"
          testable: true
          test_requirement: "Test: Verify invoke-hooks called only when check-hooks returns 0"
          priority: "Critical"

        - id: "CONF-004"
          description: "Parse audit report and build audit_summary context: resolvable_count, valid_count, invalid_count, oldest_age, circular_chains"
          testable: true
          test_requirement: "Test: Verify context JSON includes all 5 metadata fields when invoking hooks"
          priority: "High"

        - id: "CONF-005"
          description: "Sanitize sensitive data from story descriptions before passing to invoke-hooks"
          testable: true
          test_requirement: "Test: Story with 'api_key=secret' in description has 'api_key=[REDACTED]' in operation_metadata"
          priority: "High"

        - id: "CONF-006"
          description: "Ensure Phase N is non-blocking (errors logged, command succeeds regardless)"
          testable: true
          test_requirement: "Test: Simulate hook failure, verify command still completes successfully with audit report created"
          priority: "High"

        - id: "CONF-007"
          description: "Log all hook invocations to .devforgeai/feedback/logs/hook-invocations.log"
          testable: true
          test_requirement: "Test: After hook invocation, verify log file contains entry with timestamp, operation, status, outcome"
          priority: "Medium"

        - id: "CONF-008"
          description: "Implement circular invocation prevention guard (detect parent_operation == audit-deferrals)"
          testable: true
          test_requirement: "Test: Simulate nested invocation, verify guard check prevents recursion, logs warning"
          priority: "Medium"

        - id: "CONF-009"
          description: "Truncate massive audit results (>100 deferrals) to top 20 by priority, enforce 50KB context size limit"
          testable: true
          test_requirement: "Test: Generate 150 deferrals, verify audit_summary contains only 20, verify total context ≤50KB"
          priority: "Medium"

  business_rules:
    - id: "BR-001"
      rule: "Hook invocation must not block audit report generation success"
      test_requirement: "Test: Run audit with hooks disabled/failing, verify audit report created successfully"

    - id: "BR-002"
      rule: "Hook eligibility check must complete in <100ms (audit command is non-interactive, fast check expected)"
      test_requirement: "Test: Measure check-hooks execution time, assert <100ms 95th percentile"

    - id: "BR-003"
      rule: "Audit context must include all 5 audit_summary fields for meaningful feedback about debt patterns"
      test_requirement: "Test: Run audit with 10 deferrals, verify hook context includes resolvable_count, valid_count, invalid_count, oldest_age, circular_chains"

    - id: "BR-004"
      rule: "Hook integration must follow same pattern as /dev pilot (STORY-023) for consistency"
      test_requirement: "Test: Compare Phase N structure in audit-deferrals vs dev, verify pattern match"

  non_functional_requirements:
    - id: "NFR-P1"
      category: "Performance"
      requirement: "Hook eligibility check must complete in <100ms"
      metric: "Measured via command execution time logs, 95th percentile"
      test_requirement: "Test: Run /audit-deferrals 20 times, measure check-hooks duration, assert <100ms for 19+ runs"

    - id: "NFR-P2"
      category: "Performance"
      requirement: "Context extraction from audit report must complete in <300ms"
      metric: "Parse JSON, build metadata, sanitize data - all within 300ms (p95)"
      test_requirement: "Test: Generate 100-deferral audit report, time context extraction, assert <300ms 95th percentile over 20 runs"

    - id: "NFR-P3"
      category: "Performance"
      requirement: "Total Phase N overhead adds <2 seconds to command execution time"
      metric: "Measured via before/after comparison with hooks enabled but skip_all:true"
      test_requirement: "Test: Compare /audit-deferrals execution time with hooks disabled vs skip_all:true, assert difference <2s"

    - id: "NFR-R1"
      category: "Reliability"
      requirement: "Command must maintain 100% success rate regardless of hook system state"
      metric: "Audit report created successfully even if hooks fail (exit code 0 regardless)"
      test_requirement: "Test: Simulate 5 hook failure scenarios (CLI missing, config invalid, hook crash, timeout, permission error), verify command returns exit code 0 with audit report created in all cases"

    - id: "NFR-R2"
      category: "Reliability"
      requirement: "All hook invocations must be logged for audit trail and debugging"
      metric: "100% invocation logging with structured format (timestamp, operation, status, outcome, session_id)"
      test_requirement: "Test: Run 10 audits with hooks enabled, verify all 10 invocations logged to .devforgeai/feedback/logs/hook-invocations.log with complete metadata"

    - id: "NFR-S1"
      category: "Security"
      requirement: "Sensitive data must be sanitized before passing to feedback system"
      metric: "Regex pattern matching for credentials (api_key, secret, password, token), 100% redaction rate"
      test_requirement: "Test: Create story with description containing 'api_key=sk-abc123', run audit, verify operation_metadata contains 'api_key=[REDACTED]', not actual key"

    - id: "NFR-SC1"
      category: "Scalability"
      requirement: "Support audit reports up to 5MB without performance degradation"
      metric: "Parse time scales linearly, ≤50ms per MB, total memory footprint ≤50MB"
      test_requirement: "Test: Generate 5MB audit report (1000+ deferrals), measure parse time, assert <250ms, measure memory usage, assert <50MB"

    - id: "NFR-SC2"
      category: "Scalability"
      requirement: "Handle up to 1000 deferred items with automatic summarization"
      metric: "If count >100, truncate to top 20 by priority: circular deps (CRITICAL) → oldest resolvable (HIGH) → remaining by age"
      test_requirement: "Test: Generate 1000 deferrals (5 circular, 50 resolvable, 945 valid), verify audit_summary contains 5 circular + 15 oldest resolvable = 20 total"
```

## UI Specification

Not applicable - This is a command-line interface modification with no graphical UI components.

## Edge Cases

- **CLI not installed:** If `devforgeai` CLI command is not found in PATH, the check-hooks invocation will fail with "command not found" error. Command catches this error, logs warning "devforgeai CLI not found, skipping feedback. Install with: pip install --break-system-packages -e .claude/scripts/", and completes successfully with audit report. User can install CLI later and re-run audit to trigger feedback.

- **Config file corrupted or missing:** If `.devforgeai/config/hooks.yaml` is invalid YAML, has syntax errors, or doesn't exist, check-hooks may fail to parse configuration. Command catches YAML parsing errors, logs warning "Hook configuration invalid or missing, skipping feedback. Validate with: devforgeai check-hooks --validate", and completes successfully. User can fix config and re-run to enable feedback.

- **No deferrals found (empty audit):** If audit discovers zero deferred DoD items across all QA Approved/Released stories, audit_summary includes zero counts: {resolvable_count: 0, valid_count: 0, invalid_count: 0, oldest_age: null, circular_chains: []}. Hook is still invoked if eligible (captures insights about clean debt state). Feedback questions adapt: "No deferrals found. What practices helped maintain zero technical debt?"

- **Massive audit results (100+ deferrals):** If audit discovers 100+ deferred items, audit_summary is truncated to top 20 deferrals by priority (circular dependencies first, then oldest resolvable items). Context size validated to be ≤50KB. Feedback questions focus on high-priority items only. Full audit report remains available in `.devforgeai/qa/deferral-audit-{timestamp}.md` for detailed review.

- **User interrupts feedback (Ctrl+C during conversation):** If user presses Ctrl+C mid-feedback, invoke-hooks catches KeyboardInterrupt, saves partial responses (if any questions were answered), logs "Feedback interrupted by user", and exits gracefully. /audit-deferrals detects non-zero exit code from invoke-hooks, logs "Feedback session interrupted", and completes successfully. Feedback is marked incomplete but not re-triggered on subsequent audit runs (uses session_id tracking).

- **Circular invocation prevention:** If invoke-hooks internally triggers another /audit-deferrals command (theoretical edge case), guard checks detect operation_context.parent_operation == "audit-deferrals" and prevent nested invocation. Warning logged: "Circular hook invocation detected (audit-deferrals → feedback → audit-deferrals), skipping nested feedback to prevent infinite loop."

- **Concurrent audit executions:** If user runs /audit-deferrals in multiple terminals simultaneously, each execution gets unique timestamp-based audit report filename. Hook invocations are independent (separate processes). Invocation log uses file locking to prevent write conflicts. All executions complete successfully without interference.

- **Very old deferrals (oldest_age > 365 days):** If oldest deferral exceeds 1 year, feedback questions emphasize urgency: "You have deferrals over [X] days old. What blockers prevent resolution?" Audit summary includes age in days (not capped). Feedback captures insights about long-lived technical debt.

## Non-Functional Requirements

- **NFR-P1 (Performance):** Hook eligibility check completes in <100ms (95th percentile), fast decision with no blocking

- **NFR-P2 (Performance):** Context extraction from audit report completes in <300ms (95th percentile), including JSON parsing and metadata construction

- **NFR-P3 (Performance):** Total Phase N overhead adds <2 seconds to /audit-deferrals execution time (measured with skip_all:true)

- **NFR-R1 (Reliability):** Command success rate 100% regardless of hook failures (graceful degradation), exit code 0 always

- **NFR-R2 (Reliability):** All hook invocations logged to `.devforgeai/feedback/logs/hook-invocations.log` with structured format for debugging

- **NFR-S1 (Security):** Sensitive data sanitized before passing to feedback (credentials, API keys, secrets replaced with [REDACTED])

- **NFR-SC1 (Scalability):** Support audit reports up to 5MB without performance degradation, parse time ≤50ms per MB

- **NFR-SC2 (Scalability):** Handle up to 1000 deferred items with automatic summarization (truncate to top 20 by priority if >100)

## Dependencies

### Prerequisites
- **STORY-021:** devforgeai check-hooks CLI command must be implemented and tested
- **STORY-022:** devforgeai invoke-hooks CLI command must be implemented and tested
- **STORY-023:** /dev pilot integration completed and pattern validated

### Dependent Stories
None (this is the last story in Feature 6.2 - Command Integration Rollout)

## Definition of Done

### Implementation
- [ ] Phase N added to .claude/commands/audit-deferrals.md after Phase 5 (audit report generation)
- [ ] Bash code block with check-hooks call implemented
- [ ] Conditional invoke-hooks call implemented (exit code 0 check)
- [ ] Audit context passed to hooks (resolvable_count, valid_count, invalid_count, oldest_age, circular_chains)
- [ ] Sensitive data sanitization implemented (api_key, secret, password, token patterns)
- [ ] Error handling with graceful degradation implemented
- [ ] User-friendly messaging for feedback invocation
- [ ] Warning messages for hook failures (<50 words, non-alarming)
- [ ] Pattern matches /dev pilot (STORY-023) for consistency
- [ ] Invocation logging to .devforgeai/feedback/logs/hook-invocations.log
- [ ] Circular invocation prevention guard implemented

### Quality
- [ ] Unit tests: Hook check logic verified (5+ test cases)
- [ ] Integration tests: Full command flow with hooks enabled/disabled (12+ scenarios including context passing)
- [ ] Edge case tests: All 8 edge cases covered
- [ ] Performance test: Hook check <100ms (20 runs measured)
- [ ] Performance test: Context extraction <300ms (20 runs measured)
- [ ] Performance test: Total overhead <2s (10 runs measured)
- [ ] Reliability test: Command succeeds with hooks failing (5 failure scenarios)
- [ ] Context passing test: Verify all 5 metadata fields included
- [ ] Sanitization test: Verify sensitive data redaction (api_key, secret, password, token)
- [ ] Scalability test: 1000 deferrals with summarization to top 20
- [ ] Code review: Pattern consistency verified against STORY-023

### Testing
- [ ] Test Case 1: Audit complete (10 deferrals), check-hooks returns 0 → invoke-hooks called with context
- [ ] Test Case 2: Audit complete, check-hooks returns 1 → invoke-hooks skipped
- [ ] Test Case 3: CLI missing → warning logged, command succeeds, audit report created
- [ ] Test Case 4: Config invalid → warning logged, command succeeds
- [ ] Test Case 5: Hook crashes → error logged, command succeeds
- [ ] Test Case 6: User cancels feedback → partial save, command already complete
- [ ] Test Case 7: No deferrals (empty audit) → context has zero counts, feedback still triggered if eligible
- [ ] Test Case 8: 150 deferrals → context truncated to top 20, full report on disk
- [ ] Test Case 9: Measure overhead with skip_all:true → <2s total
- [ ] Test Case 10: Compare Phase N with /dev → pattern match confirmed
- [ ] Test Case 11: Audit context → verify all 5 fields (resolvable_count, valid_count, invalid_count, oldest_age, circular_chains)
- [ ] Test Case 12: Sensitive data → verify "api_key=secret" becomes "api_key=[REDACTED]"

### Documentation
- [ ] Command integration documented in `.claude/commands/audit-deferrals.md`
- [ ] Pattern documented in `.devforgeai/protocols/hook-integration-pattern.md`
- [ ] Audit context passing format documented
- [ ] User guide updated with /audit-deferrals feedback capability
- [ ] Troubleshooting section added for hook failures

## Acceptance Sign-Off

- [ ] Product Owner: Story meets acceptance criteria
- [ ] Tech Lead: Implementation follows pilot pattern (STORY-023)
- [ ] QA Lead: All tests pass, no regressions
- [ ] User Testing: 3+ users validate hook experience with audit workflows

---

**Related Documents:**
- Epic: `.ai_docs/Epics/EPIC-006-feedback-integration-completion.epic.md`
- Sprint: `.ai_docs/Sprints/Sprint-3.md`
- Pilot Story: `.ai_docs/Stories/STORY-023-wire-hooks-into-dev-command-pilot.story.md`
- Hook Infrastructure: `STORY-021`, `STORY-022`
