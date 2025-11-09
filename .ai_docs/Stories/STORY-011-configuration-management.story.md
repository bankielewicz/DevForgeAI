---
id: STORY-011
title: Configuration Management
epic: EPIC-003
sprint: Sprint-1
status: Backlog
points: 10
priority: High
assigned_to: TBD
created: 2025-11-07
---

# Story: Configuration Management

## User Story

**As a** framework maintainer/DevForgeAI administrator,
**I want to** configure the feedback capture system behavior through a YAML-based configuration file,
**so that** I can control when and how user feedback is collected without modifying code, with sensible defaults ensuring secure and balanced feedback collection.

## Acceptance Criteria

### 1. [x] Configuration File Loads with Valid YAML Structure
**Given** the `.devforgeai/config/feedback.yaml` file exists with valid YAML structure
**When** the feedback system initializes
**Then** the configuration is successfully parsed
**And** all configuration sections are accessible (enabled, trigger_mode, conversation_settings, skip_tracking, templates)
**And** no parsing errors are logged

---

### 2. [x] Master Enable/Disable Controls All Feedback Operations
**Given** the configuration has `enabled: false` set in the master section
**When** any skill attempts to trigger feedback capture
**Then** no feedback is collected
**And** no AskUserQuestion prompts are displayed
**And** workflow continues without interruption
**And** a debug log entry confirms feedback system is disabled

**And Given** the configuration has `enabled: true` in the master section
**When** the trigger conditions are met
**Then** feedback collection proceeds according to trigger_mode settings

---

### 3. [x] Trigger Mode Determines When Feedback is Collected
**Given** `trigger_mode: always` is configured
**When** any skill completes a phase
**Then** feedback is collected unconditionally (if enabled: true)
**And** AskUserQuestion is shown for feedback input

**And Given** `trigger_mode: failures-only` is configured
**When** a skill phase completes successfully
**Then** no feedback is collected
**And** no AskUserQuestion is displayed

**And Given** `trigger_mode: failures-only` is configured
**When** a skill phase fails (test failure, validation error)
**Then** feedback is collected automatically
**And** AskUserQuestion displays failure context (error message, operation type)

**And Given** `trigger_mode: specific-operations` is configured
**And** the configuration specifies `operations: [qa, deployment]`
**When** a QA or deployment operation completes
**Then** feedback is collected
**And** other operations bypass feedback collection

**And Given** `trigger_mode: never` is configured
**When** any skill operation completes
**Then** feedback is never collected
**And** all feedback UI elements are hidden

---

### 4. [x] Conversation Settings Enforce Question Limits and Skip Permissions
**Given** `conversation_settings.max_questions: 3` is configured
**When** the user has already answered 3 feedback questions in the current session
**And** another feedback trigger occurs
**Then** no additional AskUserQuestion is displayed
**And** feedback is silently discarded (not collected)
**And** a debug log confirms question limit reached

**And Given** `conversation_settings.allow_skip: true` is configured
**When** an AskUserQuestion for feedback is displayed
**Then** an "Other: Skip this feedback" option is available
**And** user can dismiss feedback without providing response
**And** skip action is tracked (if skip_tracking enabled)

**And Given** `conversation_settings.allow_skip: false` is configured
**When** feedback AskUserQuestion is displayed
**Then** no skip/dismiss option is available
**And** user must provide feedback or one of the predefined options

---

### 5. [x] Skip Tracking Maintains Feedback Collection Statistics
**Given** `skip_tracking.enabled: true` and `skip_tracking.max_consecutive_skips: 5` are configured
**When** user skips feedback 5 consecutive times
**Then** the next feedback trigger does not show AskUserQuestion
**And** a system message explains: "Feedback collection is temporarily paused. Resume in your config settings."
**And** skip count is logged in `.devforgeai/logs/feedback-skips.log`

**And Given** `skip_tracking.reset_on_positive: true` is configured
**When** user provides positive feedback (selects "Positive" or rating >= 4)
**Then** the consecutive skip counter resets to 0
**And** future skips count from 0 again

**And Given** `skip_tracking.enabled: false` is configured
**When** user skips feedback multiple times
**Then** no skip tracking occurs
**And** max_consecutive_skips limit is not enforced

---

### 6. [x] Template Preferences Control Feedback Collection Format
**Given** `templates.format: structured` is configured
**When** feedback is collected
**Then** AskUserQuestion displays with predefined options (e.g., "Very helpful", "Helpful", "Neutral", "Unhelpful", "Blocking")
**And** user selects from these options (not free text)

**And Given** `templates.format: free-text` is configured
**When** feedback is collected
**Then** AskUserQuestion displays with open text input
**And** user can provide custom feedback

**And Given** `templates.tone: brief` is configured
**When** AskUserQuestion is displayed
**Then** question text is ≤50 characters
**And** no context explanation is included

**And Given** `templates.tone: detailed` is configured
**When** AskUserQuestion is displayed
**Then** question text includes context (operation type, outcome)
**And** question may include failure details if relevant

---

### 7. [x] Invalid Configuration Values Rejected with Clear Error Messages
**Given** the configuration file has `trigger_mode: invalid-mode`
**When** the feedback system initializes
**Then** initialization FAILS with error message: "Invalid trigger_mode value: 'invalid-mode'. Must be one of: always, failures-only, specific-operations, never"
**And** the error is logged in `.devforgeai/logs/config-errors.log`
**And** the workflow HALTS with clear instruction to fix config

---

### 8. [x] Missing Configuration File Uses Sensible Defaults
**Given** the `.devforgeai/config/feedback.yaml` file does not exist
**When** the feedback system initializes
**Then** system uses default configuration (enabled: true, trigger_mode: failures-only, max_questions: 5, allow_skip: true)
**And** a log message confirms: "Using default feedback configuration"
**And** the system proceeds without errors

---

### 9. [x] Configuration Hot-Reload Updates Settings Without Restart
**Given** the feedback system is running with `enabled: true`
**When** the user modifies `.devforgeai/config/feedback.yaml` to `enabled: false`
**And** saves the file
**Then** within 5 seconds, the system detects the file change
**And** the new configuration is loaded
**And** feedback collection immediately stops
**And** no restart/terminal restart required

## Technical Specification

### Configuration Schema

```yaml
# DevForgeAI Feedback System Configuration
# Version: 1.0

enabled: true  # Boolean - Master enable/disable

trigger_mode: failures-only  # String - always|failures-only|specific-operations|never

# Conditional - required if trigger_mode: specific-operations
operations:  # Array[String]
  - qa
  - development

conversation_settings:
  max_questions: 5      # Integer - 0 = unlimited
  allow_skip: true      # Boolean

skip_tracking:
  enabled: true                   # Boolean
  max_consecutive_skips: 3        # Integer - 0 = no limit
  reset_on_positive: true         # Boolean

templates:
  format: structured  # String - structured|free-text
  tone: brief         # String - brief|detailed
```

### Data Models

#### Configuration Object
```python
@dataclass
class FeedbackConfiguration:
    enabled: bool
    trigger_mode: TriggerMode  # Enum: ALWAYS, FAILURES_ONLY, SPECIFIC_OPS, NEVER
    operations: Optional[List[str]]
    conversation_settings: ConversationSettings
    skip_tracking: SkipTrackingSettings
    templates: TemplateSettings

@dataclass
class ConversationSettings:
    max_questions: int  # 0 = unlimited
    allow_skip: bool

@dataclass
class SkipTrackingSettings:
    enabled: bool
    max_consecutive_skips: int  # 0 = no limit
    reset_on_positive: bool

@dataclass
class TemplateSettings:
    format: TemplateFormat  # Enum: STRUCTURED, FREE_TEXT
    tone: TemplateTone      # Enum: BRIEF, DETAILED
```

### API Endpoints

None - Configuration management only (file-based, no HTTP API)

### Business Rules

1. **Master Switch Rule:**
   - If `enabled: false`, all other settings ignored
   - No feedback collected regardless of trigger_mode
   - Skip tracking paused

2. **Trigger Mode Precedence:**
   - `never` > `specific-operations` > `failures-only` > `always`
   - Once `never` set, no checks performed (fastest path)

3. **Default Values:**
   - enabled: true (opt-out, not opt-in)
   - trigger_mode: failures-only (balance feedback + token cost)
   - max_questions: 5
   - allow_skip: true
   - skip_tracking.enabled: true
   - max_consecutive_skips: 3
   - templates.format: structured
   - templates.tone: brief

4. **Hot-Reload Safety:**
   - In-flight feedback collection unaffected by reload
   - New collections use new config
   - Invalid config: keep previous valid config, log error

### Dependencies

- **PyYAML:** YAML parsing
- **JSON Schema Validator:** Config validation against schema
- **File System Watchers:** Hot-reload (watchdog library or equivalent)

## Edge Cases

### 1. Concurrent Feedback Triggers During Skip Tracking
**Scenario:** `max_consecutive_skips: 2`, user skips twice, then two operations trigger simultaneously
**Expected:** Skip counter correctly maintained, both operations blocked
**Handling:** Atomic skip counter updates, thread-safe

### 2. Empty Configuration File
**Scenario:** File exists but contains only comments or is blank
**Expected:** System uses defaults, logs "Configuration file empty, using defaults"
**Handling:** Empty parse result treated as missing file

### 3. Partial Configuration
**Scenario:** File has `enabled: true` but missing all other sections
**Expected:** Merge with defaults, log merged sections
**Handling:** Deep merge algorithm (user values override defaults)

### 4. Extremely Large max_questions Value
**Scenario:** `max_questions: 1000000`
**Expected:** Accept value (no arbitrary upper limit)
**Handling:** Validation passes, practical limit is session length

### 5. Special Characters in YAML
**Scenario:** Unicode characters in configuration values
**Expected:** YAML parser handles correctly, preserves characters
**Handling:** UTF-8 encoding, YAML 1.2 spec compliance

### 6. Configuration File Becomes Unreadable
**Scenario:** Permissions changed, file deleted after initial load
**Expected:** Log warning, continue with last valid config
**Handling:** Graceful degradation, no workflow interruption

### 7. Multiple Skill Invocations Before Config Load Complete
**Scenario:** Parallel skills invoke feedback before initialization
**Expected:** Block until initialization complete, all use same config
**Handling:** Initialization lock/semaphore

## Data Validation Rules

See Technical Specification table for complete validation rules (10 fields validated).

## Non-Functional Requirements

### Performance
- Configuration load time: <100ms
- Hot-reload detection: ≤5 seconds
- Skip counter lookup: <10ms
- Per-feedback processing overhead: <50ms

### Reliability
- Configuration persistence: Atomic writes
- State recovery: No data loss on crash
- Backwards compatibility: v1.x compatible
- Data integrity: Concurrent modifications handled safely

### Security
- Input validation: No code execution
- File permissions: Authorized users only
- Sensitive data: No secrets in config
- Logging: No PII in logs

### Maintainability
- Schema documented (JSON Schema)
- Options documented (README.md with 3+ examples)
- Logging at INFO level (timestamps)
- Error messages reference documentation

### Scalability
- Concurrent triggers: 100+ simultaneous
- Session duration: In-memory (no repeated file reads)
- Log rotation: At 1MB

### Observability
- Configuration audit log (all changes tracked)
- Debug mode available (env variable)
- Validation report (JSON format)
- Health check command

## Definition of Done

### Implementation
- [ ] Configuration file template created
- [ ] JSON Schema created for IDE support
- [ ] YAML parser with full validation
- [ ] Hot-reload with file system watchers
- [ ] Skip tracking with atomic writes
- [ ] Default merging logic
- [ ] Clear error messages (reference docs)
- [ ] 4 log files configured

### Quality
- [ ] All 9 acceptance criteria have passing tests
- [ ] Edge cases covered (7 scenarios)
- [ ] Data validation enforced (10 fields)
- [ ] NFRs met (load <100ms, hot-reload ≤5s, coverage ≥95%)
- [ ] Code coverage >95%

### Testing
- [ ] Unit tests: 20+ cases (parsing, validation, merging, hot-reload)
- [ ] Integration tests: 8+ cases (end-to-end config load → feedback)
- [ ] Edge case tests: 7+ cases (all edge cases validated)
- [ ] Performance tests: Load time, hot-reload latency

### Documentation
- [ ] JSON Schema: `.devforgeai/config/feedback.schema.json`
- [ ] README: `.devforgeai/config/README.md` (3+ examples)
- [ ] Troubleshooting guide
- [ ] Migration guide (future versions)

### Release Readiness
- [ ] Default config template deployed
- [ ] Validation errors tested and verified
- [ ] Hot-reload tested in production environment
- [ ] Logging verified (4 log files created correctly)
- [ ] Deployed to staging for smoke testing

## Workflow History

- **2025-11-07:** Story created from EPIC-003 Feature 2.2 (batch mode)
