---
id: STORY-028
title: Wire Hooks Into /create-epic Command
epic: EPIC-006
sprint: Sprint-3
status: Backlog
points: 5
priority: High
assigned_to: Unassigned
created: 2025-11-12
format_version: "2.0"
---

# Story: Wire Hooks Into /create-epic Command

## Description

**As a** DevForgeAI user creating epics,
**I want** automatic feedback prompts after epic creation completes,
**so that** I can reflect on epic quality, feature decomposition effectiveness, and technical complexity assessment while details are fresh.

## Acceptance Criteria

### 1. [ ] Automatic Hook Trigger After Successful Epic Creation

**Given** the feedback system is enabled in configuration,
**When** /create-epic command completes successfully (epic file created, features decomposed, validation passed),
**Then** the system automatically invokes `devforgeai invoke-hooks --operation=epic-create --epic-id=EPIC-NNN` and presents retrospective questions about epic quality, feature count appropriateness (3-8 range), confidence in feature breakdown, technical complexity assessment accuracy, and identified risks.

---

### 2. [ ] Hook Failure Doesn't Break Epic Creation

**Given** the feedback hook invocation fails (timeout, CLI error, configuration issue),
**When** /create-epic command attempts to trigger feedback,
**Then** the system logs the hook failure (warning level), displays brief message "Feedback hook unavailable (continuing)", completes epic creation successfully, and exits with success status (hook failure is non-blocking).

---

### 3. [ ] Hook Respects Configuration State

**Given** hooks are disabled in `.devforgeai/config/hooks.yaml` (enabled: false for epic-create operation),
**When** /create-epic command completes,
**Then** the system skips hook check entirely (zero overhead), displays no feedback prompt, and proceeds directly to command completion summary.

---

### 4. [ ] Hook Receives Complete Epic Context

**Given** epic creation completed with all metadata (EPIC-ID, features list, complexity score, risks, stakeholders, success criteria),
**When** feedback hook is invoked,
**Then** the system passes epic metadata via TodoWrite context (`--epic-id=EPIC-NNN`), hook CLI reads epic file, retrospective questions reference specific epic details (e.g., "You identified 5 features - was this the right granularity?"), and user responses are tagged with epic ID for future analysis.

---

### 5. [ ] Hook Integration Preserves Lean Orchestration Pattern

**Given** /create-epic command follows lean orchestration pattern (command delegates to skill),
**When** feedback hook integration is implemented,
**Then** hook logic resides in devforgeai-orchestration skill (Phase 4A.9: Post-Epic Feedback), command remains under 15K character budget (currently 11,270 chars, 75% usage), and command only adds minimal Phase 4 display logic (<20 lines) to output hook result.

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service"
      name: "EpicHookIntegration"
      file_path: ".claude/skills/devforgeai-orchestration/SKILL.md"
      dependencies:
        - "devforgeai-cli (check-hooks, invoke-hooks)"
        - "hooks.yaml"
      requirements:
        - id: "SVC-001"
          description: "Hook integrated into Phase 4A.9 of orchestration skill epic creation workflow"
          testable: true
          test_requirement: "Test: Create epic, verify Phase 4A.9 executes, hook invoked"
          priority: "Critical"
        - id: "SVC-002"
          description: "Hook check executes in <100ms"
          testable: true
          test_requirement: "Test: Run check-hooks 100 times for epic-create operation, measure p95 < 100ms"
          priority: "Critical"
        - id: "SVC-003"
          description: "Hook invocation includes complete epic context"
          testable: true
          test_requirement: "Test: Invoke hook, verify CLI receives epic-id, reads epic file, extracts features/complexity/risks"
          priority: "High"
        - id: "SVC-004"
          description: "Hook failure doesn't break epic creation"
          testable: true
          test_requirement: "Test: Mock hook CLI failure, verify create-epic completes successfully (exit 0)"
          priority: "Critical"

    - type: "Configuration"
      name: "EpicHookConfiguration"
      file_path: ".devforgeai/config/hooks.yaml"
      dependencies:
        - "hooks.schema.json"
      required_keys:
        - key: "feedback.hooks.epic_create.enabled"
          type: "boolean"
          example: "true"
          required: true
          default: "false"
          validation: "Must be boolean true/false"
          test_requirement: "Test: Load config, verify epic_create.enabled field exists and is boolean"
        - key: "feedback.hooks.epic_create.timeout"
          type: "int"
          example: "30000"
          required: false
          default: "30000"
          validation: "Must be positive integer in milliseconds"
          test_requirement: "Test: Set timeout=15000, verify hook times out after 15s"
        - key: "feedback.hooks.epic_create.questions"
          type: "array"
          example: '["How confident are you in the feature decomposition?", "Was the complexity score accurate?"]'
          required: false
          default: "[]"
          validation: "Array of strings, max 10 questions"
          test_requirement: "Test: Configure custom questions, verify they appear in feedback conversation"

    - type: "Logging"
      name: "EpicHookLogging"
      file_path: ".devforgeai/feedback/.logs/hooks.log"
      dependencies:
        - "Python logging module"
      sinks:
        - name: "File"
          path: ".devforgeai/feedback/.logs/hooks.log"
          test_requirement: "Test: Create epic, verify hooks.log contains entry with timestamp, operation=epic-create, epic-id, status, duration"
        - name: "File"
          path: ".devforgeai/feedback/.logs/hook-errors.log"
          test_requirement: "Test: Mock hook failure, verify hook-errors.log contains timestamp, epic-id, error message, stack trace"

  business_rules:
    - id: "BR-001"
      rule: "Hook triggers only after successful epic file creation"
      trigger: "After Phase 4A.5 (Epic File Creation) completes successfully"
      validation: "Check epic file exists at .ai_docs/Epics/{EPIC-ID}.epic.md before invoking hook"
      error_handling: "If file missing, skip hook invocation (epic creation incomplete)"
      test_requirement: "Test: Delete epic file after Phase 4A.5 → hook skipped, no error"
      priority: "High"

    - id: "BR-002"
      rule: "Hook invocation non-blocking for epic creation"
      trigger: "When hook CLI invoked"
      validation: "Catch all exceptions from hook CLI process"
      error_handling: "Log exception, display warning, continue with exit 0"
      test_requirement: "Test: Hook CLI crashes → epic creation exits 0, error logged"
      priority: "Critical"

    - id: "BR-003"
      rule: "Hook respects disabled configuration"
      trigger: "Before Phase 4A.9 (hook invocation)"
      validation: "Call check-hooks CLI, parse enabled boolean from JSON response"
      error_handling: "If enabled=false, skip Phase 4A.9 entirely"
      test_requirement: "Test: Set enabled=false → hook not invoked, zero overhead"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Hook check executes in <100ms (p95)"
      metric: "Response time for check-hooks CLI call"
      test_requirement: "Test: Run check-hooks 100 times, verify p95 <100ms"
      priority: "Critical"

    - id: "NFR-002"
      category: "Performance"
      requirement: "Total hook overhead <3 seconds (p95)"
      metric: "Time from epic file creation to first feedback question displayed"
      test_requirement: "Test: Measure end-to-end latency <3000ms"
      priority: "High"

    - id: "NFR-003"
      category: "Reliability"
      requirement: "99.9%+ epic creation success rate despite hook failures"
      metric: "Epic creation exit code"
      test_requirement: "Test: Mock 1000 hooks (10 fail) → 1000 epics created (exit 0)"
      priority: "Critical"

    - id: "NFR-004"
      category: "Security"
      requirement: "Epic ID validated before CLI invocation"
      metric: "Regex validation ^EPIC-\\d{3}$"
      test_requirement: "Test: Invalid ID (EPIC-99999) → validation fails, no command injection"
      priority: "High"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- **Hook check:** < 100ms (p95), < 150ms (p99)
- **Total hook overhead:** < 3s (from epic creation complete to first feedback question)

**Throughput:**
- Not applicable (single-user CLI, sequential epic creation)

**Performance Test:**
- Run check-hooks 100 times for epic-create operation, verify p95 < 100ms
- Measure end-to-end hook overhead < 3000ms

---

### Security

**Authentication:**
- Not applicable (hooks execute in user context)

**Authorization:**
- Hook scripts execute with caller's permissions (no privilege escalation)

**Data Protection:**
- Epic IDs validated via regex before shell invocation
- No command injection vulnerabilities

**Security Testing:**
- [x] No SQL injection vulnerabilities (not applicable)
- [x] No XSS vulnerabilities (not applicable)
- [x] No hardcoded secrets
- [x] Proper input validation (epic ID regex)
- [x] Proper output encoding
- [x] No privilege escalation

---

### Scalability

**Horizontal Scaling:**
- Stateless design: Yes (hooks are per-invocation, no shared state)

**Database:**
- Not applicable (file-based feedback storage)

**Caching:**
- Cache strategy: None (hook config loaded on-demand)

---

### Reliability

**Error Handling:**
- Hook failures logged to `.devforgeai/feedback/.logs/hook-errors.log`
- User-friendly warning displayed ("Feedback hook unavailable (continuing)")
- Epic creation exits with code 0 (success)

**Retry Logic:**
- No automatic retry (user can manually retry with `devforgeai invoke-hooks`)

**Monitoring:**
- Metrics: Hook success rate, hook duration, hook failures
- Alerts: If hook success rate < 95% over 100 invocations

---

### Observability

**Logging:**
- Log level: INFO for successful hooks, WARN for failures
- Log structured data (timestamp, operation=epic-create, epic-id, status, duration)
- Include correlation ID (epic ID)
- Do NOT log sensitive data

**Metrics:**
- Hook invocation count per operation
- Hook check response time (p50, p95, p99)
- Hook failure rate
- Hook timeout rate

**Tracing:**
- Not applicable (single-process CLI)

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

1. **Epic creation interrupted mid-workflow:** If /create-epic fails during feature decomposition (Phase 4A.3), technical assessment (Phase 4A.4), or validation (Phase 4A.7), no epic file is created. Hook invocation is skipped (no epic ID available). Command exits with failure status. User must fix issues and re-run /create-epic (hook will trigger on successful completion).

2. **Hook invocation timeout (30-second limit):** If feedback CLI takes >30 seconds to respond (network issues, heavy processing, user abandons questions mid-conversation), skill terminates hook process, logs timeout warning ("Feedback hook timed out after 30s"), displays message "Feedback session timed out (you can run 'devforgeai invoke-hooks --operation=epic-create --epic-id=EPIC-NNN' manually later)", and completes epic creation successfully.

3. **Epic created via orchestration skill (not direct /create-epic command):** If epic is created by /orchestrate command invoking devforgeai-orchestration skill in epic mode, hook still triggers (skill Phase 4A.9 executes regardless of caller). Hook questions appear in orchestration workflow. User can disable hooks via config if unwanted during orchestration.

4. **Multiple epics created in batch (future scenario):** If /create-epic is enhanced to support batch mode (e.g., create 3 epics from ideation output), hook triggers once per epic (sequential: epic 1 feedback → epic 2 feedback → epic 3 feedback). User can skip remaining feedback sessions via AskUserQuestion option. Configuration supports per-operation batch behavior (prompt once vs. prompt each).

5. **Hook CLI not installed or misconfigured:** If `devforgeai` CLI command not found (not in PATH, not installed), skill detects missing CLI during `devforgeai check-hooks` execution, logs error ("Feedback CLI not found - install via 'pip install -e .claude/scripts'"), displays message "Feedback system unavailable (see .devforgeai/logs/hooks.log)", and completes epic creation successfully (hook is optional).

---

## Data Validation Rules

1. **Operation name validation:** Hook operation must be `epic-create` (exact match, case-sensitive). CLI validates operation against registered hooks in hooks.yaml. Invalid operation returns error exit code 1. Skill handles error gracefully (logs warning, skips hook).

2. **Epic ID format validation:** Epic ID must match pattern `EPIC-\d{3}` (EPIC-001 through EPIC-999). CLI validates format before reading epic file. Invalid format returns error exit code 2. Skill passes epic ID from Phase 4A.1 (discovery phase) where format was already validated by orchestration skill.

3. **Hook status validation (check-hooks):** `devforgeai check-hooks --operation=epic-create` returns JSON with `enabled` boolean and `available` boolean. Skill parses JSON, validates schema, handles malformed JSON (assume disabled). Exit code 0 = valid JSON returned. Exit code 1 = operation not found. Exit code 2 = configuration invalid.

4. **Hook metadata validation (invoke-hooks):** CLI validates epic file exists at `.ai_docs/Epics/{EPIC-ID}.epic.md` before starting feedback. If file missing, CLI returns error exit code 3 ("Epic file not found"). Skill ensures epic file written (Phase 4A.5) before invoking hook (Phase 4A.9).

5. **Configuration file validation:** hooks.yaml must be valid YAML with required fields (operations list, each operation has name/enabled/questions/storage). CLI validates on load. Invalid YAML logs error, falls back to disabled state for all hooks. Skill tolerates missing hooks.yaml (assumes all hooks disabled).

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for hook integration logic in Phase 4A.9

**Test Scenarios:**
1. **Happy Path:** Hook enabled → epic created → hook invoked → feedback conversation starts
2. **Edge Cases:**
   - Hook disabled → epic created → no hook invoked
   - Hook enabled → epic creation fails → no hook invoked
3. **Error Cases:**
   - Hook CLI not found → warning logged, epic creation exits 0
   - Hook timeout (30s) → warning logged, epic creation exits 0
   - Hook crash → error logged, epic creation exits 0

**Example Test Structure:**
```bash
# Test 1: Hook triggers on successful epic creation
/create-epic "Test Epic Name"
→ Verify: Epic created (.epic.md exists)
→ Verify: Hook check executed (logs contain check-hooks invocation)
→ Verify: Hook invoked (logs contain invoke-hooks invocation for epic-create)

# Test 2: Hook respects disabled config
echo "enabled: false" > .devforgeai/config/hooks.yaml (for epic_create operation)
/create-epic "Test Epic Name"
→ Verify: Epic created (.epic.md exists)
→ Verify: No hook invoked (logs do not contain invoke-hooks for epic-create)

# Test 3: Hook failure doesn't break epic creation
Mock devforgeai invoke-hooks to exit 1
/create-epic "Test Epic Name"
→ Verify: Epic created (.epic.md exists)
→ Verify: Command exits 0 (success)
→ Verify: Error logged to hook-errors.log
```

---

### Integration Tests

**Coverage Target:** 85%+ for end-to-end hook workflow

**Test Scenarios:**
1. **End-to-End Hook Flow:** Epic creation → hook check → hook invocation → feedback conversation → responses saved
2. **Hook CLI Integration:** Verify check-hooks and invoke-hooks CLIs work correctly with epic-create operation
3. **Epic Metadata Extraction:** Verify hook CLI reads epic file, extracts features/complexity/risks, uses in questions

**Example Test:**
```bash
# Integration test: Full epic hook workflow
/create-epic "Feature Set Epic"

# Expected behavior:
# 1. Epic EPIC-NNN.epic.md created
# 2. check-hooks --operation=epic-create executed
# 3. invoke-hooks --operation=epic-create --epic-id=EPIC-NNN executed
# 4. Feedback conversation starts with epic-specific questions
# 5. User answers questions
# 6. Responses saved to .devforgeai/feedback/epic-create/EPIC-NNN-{timestamp}.json
# 7. Command exits 0

# Verify:
assert file_exists(".ai_docs/Epics/EPIC-NNN.epic.md")
assert file_exists(".devforgeai/feedback/epic-create/EPIC-NNN-*.json")
assert exit_code == 0
```

---

## Workflow Status

- [ ] Architecture phase complete
- [ ] Development phase complete
- [ ] QA phase complete
- [ ] Released

## Notes

**Design Decisions:**
- **Hook integration point:** Phase 4A.9 added to orchestration skill epic creation workflow, after epic file creation (Phase 4A.5) and validation (Phase 4A.7)
- **Skill location:** Hook logic in devforgeai-orchestration skill (not command) to preserve lean orchestration pattern
- **Graceful degradation:** Hook failures isolated (logged, warned) but don't break epic creation (exit 0)

**Open Questions:**
- [ ] Should hooks trigger for epics created during ideation skill execution? - **Owner:** Framework team - **Due:** Before implementation
  - **Resolution:** TBD - Ideation currently outputs requirements, not epics. If ideation auto-creates epics in future, hooks should trigger.

**Related ADRs:**
- ADR-XXX: Event-Driven Hook System Architecture (STORY-018 design decisions)

**References:**
- STORY-021: devforgeai check-hooks implementation
- STORY-022: devforgeai invoke-hooks implementation
- STORY-027: Wire hooks into /create-story (similar pattern)
- EPIC-006: Feedback System Integration Completion

---

**Story Template Version:** 2.0
**Last Updated:** 2025-11-12
