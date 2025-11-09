---
id: STORY-009
title: Skip Pattern Tracking
epic: EPIC-002
sprint: Sprint-1
status: Backlog
points: 6
priority: Critical
assigned_to: TBD
created: 2025-11-07
---

# Story: Skip Pattern Tracking

## User Story

**As a** DevForgeAI system administrator,
**I want** to monitor when users skip feedback prompts and automatically suggest disabling the feedback feature when patterns indicate token waste,
**so that** I can optimize token usage and improve user experience by reducing unnecessary interruptions.

## Acceptance Criteria

### 1. [x] Skip Counter Tracks Operations
**Given** a user is executing operations that trigger feedback prompts
**When** the user skips 1, 2, or 5 feedback prompts across different operation types
**Then** the skip counter increments correctly per operation type (e.g., "skill_invocation_skips: 2", "subagent_invocation_skips: 1")
**And** counters are stored in `.devforgeai/config/feedback-preferences.yaml` in YAML format
**And** counters persist across sessions (survive terminal restart)

---

### 2. [x] Pattern Detection Triggers at 3+ Consecutive Skips
**Given** a user has skipped feedback prompts for the same operation type
**When** the skip count reaches 3 consecutive skips for that operation type
**Then** the system detects the pattern and triggers a suggestion workflow
**And** the AskUserQuestion appears with options: "Disable feedback for [operation-type]?", "Keep feedback", "Ask me later"
**And** the pattern detection occurs only once per session (not on every subsequent skip)

---

### 3. [x] Preference Storage and Enforcement
**Given** a user confirms "Disable feedback for [operation-type]" via AskUserQuestion
**When** the preference is stored in `.devforgeai/config/feedback-preferences.yaml`
**Then** subsequent operations of that type DO NOT trigger feedback prompts
**And** the disabled status is clearly documented (reason: "User disabled after 3+ skips")
**And** users can re-enable via manual config edit (documented process)

---

### 4. [x] Skip Counter Reset on User Preference Change
**Given** a user has disabled feedback for an operation type
**When** the user manually re-enables feedback (edit config file or AskUserQuestion option)
**Then** the skip counter for that operation type resets to 0
**And** pattern detection starts fresh (requires 3 new consecutive skips)

---

### 5. [x] Token Waste Calculation and Reporting
**Given** feedback has been prompted for various operations
**When** a pattern is detected (3+ consecutive skips)
**Then** the suggestion includes estimated token waste: "Feedback prompts for [operation-type] have wasted ~{X} tokens"
**And** the calculation is accurate: tokens_per_prompt × skip_count = waste estimate
**And** the estimate is shown to user in AskUserQuestion context

---

### 6. [x] Multi-Operation-Type Tracking
**Given** a user skips feedback for different operation types (e.g., skill invocation AND subagent invocation)
**When** each operation type reaches 3+ consecutive skips independently
**Then** separate pattern detection triggers for each operation type
**And** user can disable feedback for multiple operation types simultaneously or separately
**And** skip counters for each operation type remain independent (disabling one doesn't affect others)

## Technical Specification

### Data Models

#### Feedback Preferences Config Schema
```yaml
---
version: "1.0"
created_at: "2025-11-07T10:30:00Z"
last_updated: "2025-11-07T10:45:00Z"
---

# Skip counters per operation type
skip_counters:
  skill_invocation: 0
  subagent_invocation: 0
  command_execution: 0
  context_loading: 0

# Disabled feedback types
disabled_feedback:
  skill_invocation: false
  subagent_invocation: false
  command_execution: false
  context_loading: false

# Disable reasons (for audit trail)
disable_reasons:
  skill_invocation: null
  subagent_invocation: "User disabled after 3+ consecutive skips on 2025-11-07"
  command_execution: null
  context_loading: null
```

#### Skip Event Schema
```json
{
  "event_id": "UUID",
  "timestamp": "ISO 8601",
  "operation_type": "skill_invocation|subagent_invocation|command_execution|context_loading",
  "skip_action": "skip_all|skip_question",
  "consecutive_count": 3,
  "pattern_detected": true,
  "token_waste_estimate": 4500
}
```

### API Endpoints

None - Configuration management only (no HTTP API)

### Business Rules

1. **Consecutive Skip Threshold:**
   - Trigger pattern detection at 3+ consecutive skips
   - Non-consecutive skips reset counter
   - Threshold applies per operation type independently

2. **Token Waste Calculation:**
   - Formula: `tokens_per_prompt × skip_count = waste_estimate`
   - Average tokens per prompt: ~1500 tokens (5-10 AskUserQuestion interactions)
   - Display in AskUserQuestion: "~4,500 tokens wasted"

3. **Preference Enforcement:**
   - Disabled feedback types: No prompts shown
   - Enabled feedback types: Normal prompts
   - Manual re-enable: Reset skip counter to 0

4. **Config File Management:**
   - Create if missing on first skip
   - Backup before modification (`.yaml.backup`)
   - Corrupted file: Create backup, generate fresh config

5. **Session Persistence:**
   - Skip counters persist across terminal restarts
   - Preferences loaded at session initialization
   - Counter updates written immediately (not batched)

### Dependencies

- **PyYAML:** YAML file read/write
- **Python pathlib:** File system operations
- **Python datetime:** Timestamp generation
- **AskUserQuestion tool:** User preference collection

### File Locations

- **Config:** `.devforgeai/config/feedback-preferences.yaml`
- **Backups:** `.devforgeai/config/backups/feedback-preferences-{timestamp}.yaml.backup`
- **Logs:** `.devforgeai/logs/skip-pattern-detection.log`

## Edge Cases

### 1. User Skips on First Attempt
**Scenario:** User skips feedback on operation #1
**Expected:** Skip counter increments to 1, no pattern detected (requires 3+ consecutive)
**Validation:** Counter shows "1 of 3 for pattern detection"

### 2. Non-Consecutive Skips Don't Trigger Pattern
**Scenario:** User skips feedback, answers next feedback, then skips 2 more (pattern broken)
**Expected:** Skip counter resets to 1 (sequence broken)
**Validation:** Only consecutive skips count toward 3+ threshold

### 3. Config File Missing on First Skip
**Scenario:** `.devforgeai/config/feedback-preferences.yaml` does not exist
**Expected:** System creates config file with initial structure and skip counter increments
**Validation:** File created with YAML frontmatter and initial counters

### 4. Manual Config Edit Causes Inconsistency
**Scenario:** User manually edits config file to set skip_counter to 5 while disabled_feedback is true
**Expected:** System prioritizes disabled_feedback flag (no prompts shown)
**Validation:** Disabled status enforced regardless of counter value

### 5. Corrupted Config File
**Scenario:** `.devforgeai/config/feedback-preferences.yaml` is malformed YAML
**Expected:** System logs error, creates backup (`.yaml.backup`), creates fresh config
**Validation:** Fresh config created, user notified (non-blocking), operations continue

### 6. Pattern Detection Across Two Sessions
**Scenario:** User skips feedback 2 times in Session 1, 1 time in Session 2
**Expected:** Consecutive count is maintained across sessions (total = 3 consecutive)
**Validation:** Pattern detection triggers at start of Session 2 on 3rd skip

## Data Validation Rules

### Skip Counter Validation
1. **Type:** Integer
2. **Range:** 0-100 (prevents overflow)
3. **Increment:** +1 per skip (no manual increments)
4. **Reset:** On preference change or 30 days of no skips (stale cleanup)

### Operation Type Validation
1. **Allowed values:** `skill_invocation`, `subagent_invocation`, `command_execution`, `context_loading`
2. **Case sensitivity:** Lowercase only (`.lower()`)
3. **Format:** Snake_case (regex: `^[a-z_]+$`)
4. **New types:** Require code change (whitelist validation)

### Disabled Feedback Flag Validation
1. **Type:** Boolean
2. **Values:** `true` or `false` only (YAML native)
3. **Consistency:** Must match operation type

### Disable Reason Validation
1. **Type:** String or null
2. **Max length:** 200 characters
3. **Format:** Reason + timestamp (e.g., "User disabled after 3+ consecutive skips on 2025-11-07T10:45:00Z")

### Config File Structure Validation
1. **File format:** YAML with frontmatter
2. **Required sections:** version, created_at, skip_counters, disabled_feedback, disable_reasons
3. **Version constraint:** Must match code version
4. **Timestamp format:** ISO 8601

## Non-Functional Requirements

### Performance
- Skip counter increment: <10ms
- Pattern detection check: <50ms
- Config file read: <100ms (session start)
- Config file write: <200ms (preference change)
- Combined operations: <500ms total

### Storage
- Config file size: <5KB
- Skip counter memory: <1KB per operation type (in-memory cache)
- Backup retention: Last 3 versions

### Reliability
- Config file persistence: 100%
- Pattern detection accuracy: 100% (3+ consecutive strictly enforced)
- Counter reset reliability: 100%
- Backup creation: 100% (before modifications)

### User Experience
- Suggestion timing: <500ms after 3rd skip (instant perception)
- AskUserQuestion options: Maximum 3 (simplicity)
- Clarity: Token waste context provided
- Friction: 1-click disable (no multi-step)

### Maintainability
- Code documentation: 80%+ API coverage
- Logging: DEBUG (counter increments), INFO (pattern detection)
- Error messages: Specific and actionable

### Security
- Config file permissions: User-readable only (mode 600)
- No sensitive data stored
- Injection prevention: Operation type whitelist

### Audit Trail
- Change tracking: Record disable/re-enable (timestamp + reason)
- Pattern history: Log detection events (operation type + skip count + time)
- Manual edits: Recommend documentation

## Definition of Done

### Implementation
- [ ] Skip counter increments per operation type
- [ ] Pattern detection triggers at 3+ consecutive skips
- [ ] AskUserQuestion appears with disable/keep/ask-later options
- [ ] User preference stored in `.devforgeai/config/feedback-preferences.yaml`
- [ ] Preferences persist across sessions
- [ ] Disabled feedback types enforced (no prompts)
- [ ] Token waste calculation accurate
- [ ] Multi-operation-type tracking independent
- [ ] Config file created if missing
- [ ] Corrupted config: backup + fresh config
- [ ] Consecutive count maintained across sessions

### Quality
- [ ] All 6 acceptance criteria have passing tests
- [ ] Edge cases covered (non-consecutive resets, missing config, corrupted config, session persistence)
- [ ] Data validation enforced (4 validation categories)
- [ ] NFRs met (<500ms combined, 100% persistence, <5KB storage)
- [ ] Code coverage >95% for skip tracking module

### Testing
- [ ] Unit tests: 25+ cases (counter logic, pattern detection, config parsing, edge cases)
- [ ] Integration tests: 10+ cases (skip → pattern → preference → enforcement)
- [ ] E2E test: First skip (counter=1, no pattern)
- [ ] E2E test: 3rd consecutive skip (pattern detected, AskUserQuestion)
- [ ] E2E test: Non-consecutive skips (counter resets)
- [ ] E2E test: Disable preference (no prompts shown)
- [ ] E2E test: Re-enable preference (counter resets, prompts resume)
- [ ] E2E test: Missing config file (auto-created)
- [ ] E2E test: Corrupted config (backup, fresh config)
- [ ] E2E test: Cross-session persistence (skip in Session 1, pattern in Session 2)

### Documentation
- [ ] Config file schema documented
- [ ] Skip event schema documented
- [ ] Token waste calculation formula explained
- [ ] User guide: How to re-enable feedback manually
- [ ] Developer guide: How to add new operation types

### Release Readiness
- [ ] Feature flag: `enable_skip_tracking` (default: enabled)
- [ ] Config file permissions validated (mode 600)
- [ ] No sensitive data in config verified
- [ ] Operation type whitelist enforced
- [ ] Backup strategy tested
- [ ] Audit trail logging validated

## Workflow History

- **2025-11-07:** Story created from EPIC-002 Feature 1.3 (batch mode)
