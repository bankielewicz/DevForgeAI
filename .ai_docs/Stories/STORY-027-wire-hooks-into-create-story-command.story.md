---
id: STORY-027
title: Wire Hooks Into /create-story Command
epic: EPIC-006
sprint: Sprint-3
status: Backlog
points: 5
priority: High
assigned_to: Unassigned
created: 2025-11-12
format_version: "2.0"
---

# Story: Wire Hooks Into /create-story Command

## Description

**As a** DevForgeAI user creating stories,
**I want** automatic retrospective feedback prompts after story creation completes,
**so that** I can reflect on story quality and improve my requirements definition skills without having to manually trigger feedback conversations.

## Acceptance Criteria

### 1. [ ] Hook triggers after successful story creation

**Given** feedback hooks are enabled in `.devforgeai/config/hooks.yaml`,
**When** `/create-story` command completes successfully and creates a .story.md file,
**Then** the system automatically invokes `devforgeai invoke-hooks --operation=story-create --story-id=STORY-NNN` and presents the feedback conversation to the user.

---

### 2. [ ] Hook failure doesn't break story creation workflow

**Given** a story is being created and feedback hooks are enabled,
**When** the hook invocation fails (timeout, CLI error, or hook script crash),
**Then** the `/create-story` command logs the hook error, displays a warning to the user ("Feedback hook failed - story created successfully"), and completes with exit code 0 (story creation still successful).

---

### 3. [ ] Hook respects configuration (enabled/disabled state)

**Given** the user has set `feedback.hooks.story_create.enabled: false` in `.devforgeai/config/hooks.yaml`,
**When** `/create-story` command completes successfully,
**Then** no feedback hook is invoked, and the command proceeds directly to completion summary.

---

### 4. [ ] Hook check executes efficiently

**Given** feedback hooks are enabled,
**When** `/create-story` reaches the hook integration phase,
**Then** the `devforgeai check-hooks --operation=story-create` command completes in <100ms and returns the hook configuration (enabled status, questions, template).

---

### 5. [ ] Hook doesn't trigger during batch story creation

**Given** `/create-story` is invoked in batch mode (creating multiple stories from epic features),
**When** individual stories are created within the batch,
**Then** the feedback hook is deferred and only invoked once at the end of the batch, passing all created story IDs as context.

---

### 6. [ ] Hook invocation includes complete story context

**Given** feedback hooks are enabled and story creation completed,
**When** the hook is invoked via `devforgeai invoke-hooks`,
**Then** the hook receives operation metadata including: story ID, epic ID (if any), sprint reference (if any), story title, story points, priority, and timestamp.

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service"
      name: "HookIntegrationPhase"
      file_path: ".claude/commands/create-story.md"
      dependencies:
        - "devforgeai-cli (check-hooks, invoke-hooks)"
        - "hooks.yaml"
      requirements:
        - id: "SVC-001"
          description: "Hook check must execute in <100ms"
          testable: true
          test_requirement: "Test: Run check-hooks 100 times, measure p95 < 100ms"
          priority: "Critical"
        - id: "SVC-002"
          description: "Hook invocation must include complete story context"
          testable: true
          test_requirement: "Test: Invoke hook, verify all metadata fields present (story-id, epic-id, sprint, title, points, priority, timestamp)"
          priority: "Critical"
        - id: "SVC-003"
          description: "Hook failure must not break command exit code"
          testable: true
          test_requirement: "Test: Mock hook failure, verify create-story exits 0"
          priority: "Critical"
        - id: "SVC-004"
          description: "Batch mode must defer hooks until completion"
          testable: true
          test_requirement: "Test: Batch create 3 stories, verify hook runs once at end with all 3 story IDs"
          priority: "High"

    - type: "Configuration"
      name: "HookConfiguration"
      file_path: ".devforgeai/config/hooks.yaml"
      dependencies:
        - "hooks.schema.json"
      required_keys:
        - key: "feedback.hooks.story_create.enabled"
          type: "boolean"
          example: "true"
          required: true
          default: "false"
          validation: "Must be boolean true/false"
          test_requirement: "Test: Load config, verify enabled field is boolean"
        - key: "feedback.hooks.story_create.timeout"
          type: "int"
          example: "30000"
          required: false
          default: "30000"
          validation: "Must be positive integer in milliseconds"
          test_requirement: "Test: Set timeout=10000, verify hook times out after 10s"

    - type: "Logging"
      name: "HookLogging"
      file_path: ".devforgeai/feedback/.logs/hooks.log"
      dependencies:
        - "Python logging module"
      sinks:
        - name: "File"
          path: ".devforgeai/feedback/.logs/hooks.log"
          test_requirement: "Test: Create story, verify hooks.log contains entry with timestamp, operation, story-id, status, duration"
        - name: "File"
          path: ".devforgeai/feedback/.logs/hook-errors.log"
          test_requirement: "Test: Mock hook failure, verify hook-errors.log contains timestamp, operation, story-id, error message, stack trace"

  business_rules:
    - id: "BR-001"
      rule: "Hook invocation deferred in batch mode"
      trigger: "When batch mode marker detected in conversation context"
      validation: "Check for **Batch Mode:** true marker"
      error_handling: "If marker present, append story ID to batch list and skip hook invocation"
      test_requirement: "Test: Batch create 3 stories → hook runs once with all IDs"
      priority: "High"

    - id: "BR-002"
      rule: "Hook check returns JSON with enabled boolean"
      trigger: "When check-hooks CLI invoked"
      validation: "Parse JSON output, check for 'enabled' field"
      error_handling: "If JSON malformed, treat as enabled: false (safe default)"
      test_requirement: "Test: check-hooks returns {\"enabled\": true/false} in <100ms"
      priority: "Critical"

    - id: "BR-003"
      rule: "Hook failures don't propagate to command exit code"
      trigger: "When hook invocation fails (timeout, CLI error, script crash)"
      validation: "Catch all hook exceptions"
      error_handling: "Log error to hook-errors.log, display warning, continue with exit 0"
      test_requirement: "Test: Mock hook crash → story creation exits 0, error logged"
      priority: "Critical"

    - id: "BR-004"
      rule: "Story file existence required before hook invocation"
      trigger: "Before invoking hook"
      validation: "Check if .ai_docs/Stories/STORY-NNN-*.story.md exists"
      error_handling: "If missing, skip hook invocation (story creation incomplete)"
      test_requirement: "Test: Delete story file after creation → hook skipped, no error thrown"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Hook check executes in <100ms (p95)"
      metric: "Response time measured via time command (p95 and p99)"
      test_requirement: "Test: Run check-hooks 100 times, verify p95 <100ms"
      priority: "Critical"

    - id: "NFR-002"
      category: "Performance"
      requirement: "Total hook overhead <3 seconds"
      metric: "Time from story creation complete to first feedback question"
      test_requirement: "Test: Measure end-to-end latency <3000ms"
      priority: "Critical"

    - id: "NFR-003"
      category: "Reliability"
      requirement: "99.9%+ story creation success rate despite hook failures"
      metric: "Story creation exit code"
      test_requirement: "Test: Mock 1000 hooks (10 fail) → 1000 stories created (exit 0)"
      priority: "Critical"

    - id: "NFR-004"
      category: "Security"
      requirement: "Story ID validated before shell invocation"
      metric: "Regex validation ^STORY-\\d{3}$"
      test_requirement: "Test: Invalid ID (STORY-999999) → validation fails, no command injection"
      priority: "High"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- **Hook check:** < 100ms (p95), < 150ms (p99)
- **Total hook overhead:** < 3s (from story creation complete to first feedback question)

**Throughput:**
- Support concurrent story creation without hook bottleneck

**Performance Test:**
- Run check-hooks 100 times, verify p95 < 100ms
- Measure end-to-end hook overhead < 3000ms

---

### Security

**Authentication:**
- Not applicable (hooks execute in user context)

**Authorization:**
- Hook scripts execute with caller's permissions (no privilege escalation)

**Data Protection:**
- Sensitive fields: Story IDs validated via regex before shell invocation
- No command injection vulnerabilities

**Security Testing:**
- [x] No SQL injection vulnerabilities (not applicable)
- [x] No XSS vulnerabilities (not applicable)
- [x] No hardcoded secrets
- [x] Proper input validation (story ID regex)
- [x] Proper output encoding
- [x] No privilege escalation

---

### Scalability

**Horizontal Scaling:**
- Stateless design: Yes (hooks are per-invocation, no shared state)
- Load balancing: Not applicable (single-user CLI)

**Database:**
- Not applicable (file-based configuration)

**Caching:**
- Cache strategy: None (hook config loaded on-demand)

---

### Reliability

**Error Handling:**
- Hook failures logged to `.devforgeai/feedback/.logs/hook-errors.log`
- User-friendly warning displayed ("Feedback hook failed - story created successfully")
- Story creation exits with code 0 (success)

**Retry Logic:**
- No automatic retry for hook failures (user can manually retry with `devforgeai invoke-hooks`)

**Monitoring:**
- Metrics: Hook success rate, hook duration, hook failures
- Alerts: If hook success rate < 95% over 100 invocations

---

### Observability

**Logging:**
- Log level: INFO for successful hooks, WARN for failures
- Log structured data (timestamp, operation, story-id, status, duration)
- Include correlation ID for request tracing (story ID)
- Do NOT log sensitive data

**Metrics:**
- Hook invocation count
- Hook check response time (p50, p95, p99)
- Hook failure rate
- Hook timeout rate

**Tracing:**
- Distributed tracing: Not applicable (single-process CLI)

---

## Dependencies

### Prerequisite Stories

- [x] **STORY-021:** Implement devforgeai check-hooks CLI command
  - **Why:** Required for hook eligibility checking
  - **Status:** Complete (Feature 6.1)

- [x] **STORY-022:** Implement devforgeai invoke-hooks CLI command
  - **Why:** Required for triggering feedback conversations
  - **Status:** Complete (Feature 6.1)

### External Dependencies

- None

### Technology Dependencies

- [ ] **Python 3.10+:** CLI commands require Python 3.10+
  - **Purpose:** Hook CLI implementation
  - **Approved:** Yes (already in tech-stack.md)
  - **Added to dependencies.md:** Yes

---

## Edge Cases

1. **Batch mode story creation (multiple stories from epic):** Hook should be deferred until all stories in the batch are created, then invoked once with all story IDs as context. User answers feedback questions once for the entire batch (e.g., "How confident are you in the requirements for these 5 stories?").

2. **Story creation interrupted mid-workflow (user cancels, error during validation):** Hook should NOT trigger if story file wasn't successfully written to disk. Detection: Check story file existence before invoking hook.

3. **Hook invocation timeout (feedback conversation takes >30s):** After 30 seconds, hook invocation should timeout with graceful degradation. Warning displayed: "Feedback timeout - you can manually run 'devforgeai invoke-hooks --operation=story-create --story-id=STORY-NNN' later."

4. **Hook configuration file missing or corrupted:** If `.devforgeai/config/hooks.yaml` doesn't exist or is malformed, `devforgeai check-hooks` returns `enabled: false` (safe default). No error thrown, hook silently skipped with debug log entry.

5. **Story created via orchestration skill (not direct command):** When devforgeai-orchestration skill creates stories during sprint planning, hooks should still trigger (same Phase N integration pattern applies to skill).

6. **User disables hooks mid-command execution:** Race condition where hooks.yaml changes from enabled→disabled during story creation. Hook check happens at Phase N (after story file written), so respects state at invocation time (enabled when checked).

---

## Data Validation Rules

1. **Operation name:** Must match one of the registered hook types in hooks.yaml schema (`story-create`, `dev`, `qa`, `release`, `orchestrate`). Validation: Regex `^[a-z-]+$`.

2. **Story ID format:** Must match `STORY-\d{3}` pattern (e.g., STORY-027). Validation: Regex check before passing to hook invocation.

3. **Hook status validation:** `devforgeai check-hooks` must return JSON with `enabled` boolean field. Missing field = treat as `enabled: false` (safe default).

4. **Story file existence:** Before invoking hook, verify `.ai_docs/Stories/STORY-NNN-*.story.md` exists on disk. If missing, skip hook (story creation incomplete).

5. **Batch mode detection:** Check for conversation context marker `**Batch Mode:** true` set by /create-story command. If present, defer hook invocation.

6. **Hook timeout value:** Maximum hook invocation time is 30 seconds (configurable in hooks.yaml via `feedback.hooks.story_create.timeout` field, default: 30000ms).

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for hook integration logic

**Test Scenarios:**
1. **Happy Path:** Hook enabled → story created → hook invoked → feedback conversation starts
2. **Edge Cases:**
   - Hook disabled → story created → no hook invoked
   - Hook enabled → batch mode → hook deferred until batch complete
   - Hook enabled → story creation fails → no hook invoked
3. **Error Cases:**
   - Hook CLI not found → warning logged, story creation exits 0
   - Hook timeout (30s) → warning logged, story creation exits 0
   - Hook crash → error logged, story creation exits 0

**Example Test Structure:**
```bash
# Test 1: Hook triggers on successful story creation
/create-story "Test feature"
→ Verify: Story created (.story.md exists)
→ Verify: Hook check executed (logs contain check-hooks invocation)
→ Verify: Hook invoked (logs contain invoke-hooks invocation)

# Test 2: Hook respects disabled config
echo "enabled: false" > .devforgeai/config/hooks.yaml
/create-story "Test feature"
→ Verify: Story created (.story.md exists)
→ Verify: No hook invoked (logs do not contain invoke-hooks)

# Test 3: Hook failure doesn't break story creation
Mock devforgeai invoke-hooks to exit 1
/create-story "Test feature"
→ Verify: Story created (.story.md exists)
→ Verify: Command exits 0 (success)
→ Verify: Error logged to hook-errors.log
```

---

### Integration Tests

**Coverage Target:** 85%+ for end-to-end hook workflow

**Test Scenarios:**
1. **End-to-End Hook Flow:** Story creation → hook check → hook invocation → feedback conversation → responses saved
2. **Batch Mode:** Create 3 stories in batch → hook invoked once at end with all 3 IDs
3. **Hook CLI Integration:** Verify check-hooks and invoke-hooks CLIs work correctly

**Example Test:**
```bash
# Integration test: Full hook workflow
/create-story "Feature with hooks enabled"

# Expected behavior:
# 1. Story STORY-NNN-*.story.md created
# 2. check-hooks --operation=story-create executed
# 3. invoke-hooks --operation=story-create --story-id=STORY-NNN executed
# 4. Feedback conversation starts
# 5. User answers questions
# 6. Responses saved to .devforgeai/feedback/STORY-NNN-feedback.json
# 7. Command exits 0

# Verify:
assert file_exists(".ai_docs/Stories/STORY-NNN-*.story.md")
assert file_exists(".devforgeai/feedback/STORY-NNN-feedback.json")
assert exit_code == 0
```

---

### E2E Tests (If Applicable)

**Coverage Target:** 10% of total tests (critical paths only)

**Test Scenarios:**
1. **Critical User Journey:** User creates story → hook triggers → user provides feedback → feedback saved

---

## Definition of Done

### Implementation
- [ ] Hook integration phase added to /create-story command (Phase N after story file creation)
- [ ] `devforgeai check-hooks --operation=story-create` command functional (<100ms execution)
- [ ] `devforgeai invoke-hooks --operation=story-create` command functional with story context
- [ ] Hook configuration read from `.devforgeai/config/hooks.yaml` (enabled/disabled state respected)
- [ ] Batch mode story creation defers hooks until all stories created
- [ ] Graceful degradation implemented (hook failures don't break story creation, exit code 0)

### Quality
- [ ] All 6 acceptance criteria have passing tests
- [ ] Edge cases covered (hook timeout, hook CLI error, hook script crash, missing config)
- [ ] Data validation enforced (story context metadata complete, hook config format valid)
- [ ] NFRs met (hook check <100ms, hook invocation <500ms, graceful failure handling)
- [ ] Code coverage >95% for hook integration logic

### Testing
- [ ] Unit tests for hook configuration reading and enabled/disabled state
- [ ] Unit tests for hook context metadata assembly (story ID, epic, sprint, title, points, priority)
- [ ] Unit tests for graceful degradation (hook failure doesn't crash workflow)
- [ ] Integration test: /create-story hook triggers successfully
- [ ] Integration test: /create-story with hooks disabled skips hook invocation
- [ ] Integration test: Batch story creation defers hooks until batch completion
- [ ] E2E test: Complete story creation workflow with hook triggering

### Documentation
- [ ] Hook integration documentation added to devforgeai-story-creation skill guide
- [ ] Configuration example added to `.devforgeai/config/hooks.yaml.example`
- [ ] Troubleshooting guide: "Hook not triggering after story creation" - resolution steps
- [ ] Framework maintainer guide updated with hook lifecycle for /create-story

---

## Implementation Notes

**This story wires hook integration into /create-story command workflow. See Technical Specification for hook architecture details.**

**Hook Integration Pattern:**
- Hooks triggered via `devforgeai invoke-hooks --operation=story-create` after story file creation
- Story context passed to hook includes ID, epic, sprint, title, points, priority
- Graceful degradation ensures hook failures don't prevent story creation (exit 0)

**Configuration Pattern:**
- Hooks controlled via `.devforgeai/config/hooks.yaml` enabled/disabled flag
- Batch mode defers hook invocation until all stories in batch complete
- Hook check completes in <100ms

**Related Stories:**
- STORY-021: devforgeai check-hooks implementation
- STORY-022: devforgeai invoke-hooks implementation

## Workflow Status

- [ ] Architecture phase complete
- [ ] Development phase complete
- [ ] QA phase complete
- [ ] Released

## Notes

**Design Decisions:**
- **Hook integration point:** Phase N added at end of /create-story workflow, after story file creation completes but before final success message
- **Graceful degradation:** Hook failures isolated (logged, warned) but don't break story creation (exit 0)
- **Batch mode deferral:** Hooks deferred in batch mode to avoid interrupting user with feedback questions for each story (single feedback session at end)

**Open Questions:**
- [ ] Should hooks also trigger for stories created via orchestration skill? - **Owner:** Framework team - **Due:** Before implementation
  - **Resolution:** YES - Orchestration skill also adds Phase N (consistent pattern)

**Related ADRs:**
- ADR-XXX: Event-Driven Hook System Architecture (STORY-018 design decisions)

**References:**
- STORY-021: devforgeai check-hooks implementation
- STORY-022: devforgeai invoke-hooks implementation
- EPIC-006: Feedback System Integration Completion

---

**Story Template Version:** 2.0
**Last Updated:** 2025-11-12
