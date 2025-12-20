---
id: STORY-108
title: Parallel Configuration Infrastructure
epic: EPIC-017
sprint: Backlog
status: QA Approved
points: 5
depends_on: []
priority: Medium
assigned_to: Claude
created: 2025-12-18
format_version: "2.2"
---

# Story: Parallel Configuration Infrastructure

## Description

**As a** DevForgeAI user,
**I want** a configuration file for parallel task orchestration with profile support and timeout settings,
**so that** I can match my Anthropic subscription tier and ensure long-running operations fail gracefully.

This story implements EPIC-017 Feature 1: Create `devforgeai/config/parallel-orchestration.yaml` with profile support, timeout settings, and retry configuration. Foundation for all parallel patterns.

## Acceptance Criteria

### AC#1: Configuration File Schema

**Given** the DevForgeAI framework is installed,
**When** a user creates `devforgeai/config/parallel-orchestration.yaml`,
**Then** the file supports profile definitions with max_concurrent_tasks, timeout_ms, and retry configuration.

---

### AC#2: Profile Presets

**Given** the parallel configuration file exists,
**When** a user specifies a profile preset (Pro/Max/API),
**Then** the framework loads appropriate defaults:
- Pro: max_concurrent_tasks=4, timeout_ms=120000
- Max: max_concurrent_tasks=6, timeout_ms=180000
- API: max_concurrent_tasks=8, timeout_ms=300000

---

### AC#3: Configurable Timeouts

**Given** a parallel task is running,
**When** the task exceeds the configured timeout_ms,
**Then** the task is gracefully terminated and error is logged.

---

### AC#4: Configuration Validation

**Given** a user provides a parallel orchestration config,
**When** the framework loads the configuration,
**Then** invalid values are rejected with clear error messages (e.g., max_concurrent_tasks must be 1-10).

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "parallel-orchestration.yaml"
      file_path: "devforgeai/config/parallel-orchestration.yaml"
      required_keys:
        - key: "version"
          type: "string"
          example: "1.0"
          required: true
          validation: "Semantic version format"
          test_requirement: "Test: Verify version field is present and valid"
        - key: "default_profile"
          type: "string"
          example: "pro"
          required: true
          validation: "Must be one of: pro, max, api, custom"
          test_requirement: "Test: Verify default_profile accepts valid values"
        - key: "profiles"
          type: "object"
          example: "{ pro: { max_concurrent_tasks: 4 } }"
          required: true
          validation: "Each profile must have max_concurrent_tasks and timeout_ms"
          test_requirement: "Test: Verify profiles object structure"
        - key: "profiles.[name].max_concurrent_tasks"
          type: "int"
          example: "4"
          required: true
          validation: "Range 1-10"
          test_requirement: "Test: Verify max_concurrent_tasks bounds validation"
        - key: "profiles.[name].timeout_ms"
          type: "int"
          example: "120000"
          required: true
          validation: "Range 1000-600000"
          test_requirement: "Test: Verify timeout_ms bounds validation"
        - key: "profiles.[name].retry"
          type: "object"
          example: "{ max_attempts: 3, backoff_ms: 1000 }"
          required: false
          validation: "max_attempts 0-5, backoff_ms 100-10000"
          test_requirement: "Test: Verify retry configuration optional with defaults"

    - type: "Configuration"
      name: "Parallel Config Documentation"
      file_path: ".claude/skills/devforgeai-orchestration/references/parallel-config.md"
      purpose: "Documents how skills load and validate parallel orchestration config"
      required_sections:
        - section: "Config Loading Pattern"
          description: "How to read config using Read tool"
          test_requirement: "Test: Pattern produces valid config loading"
        - section: "Validation Rules"
          description: "How to validate config values using Grep patterns"
          test_requirement: "Test: Validation catches invalid values"
        - section: "Default Fallback"
          description: "How to apply defaults when config missing"
          test_requirement: "Test: Missing config returns default profile"

    - type: "Service"
      name: "validate-parallel-config.sh"
      file_path: "scripts/validate-parallel-config.sh"
      interface: "CLI Script"
      lifecycle: "On-demand"
      dependencies:
        - "bash 4.0+"
        - "grep"
      requirements:
        - id: "SVC-001"
          description: "Validate config file exists and has valid YAML structure"
          testable: true
          test_requirement: "Test: Script returns 0 for valid config, 1 for invalid"
          priority: "Critical"
        - id: "SVC-002"
          description: "Validate required keys present using grep patterns"
          testable: true
          test_requirement: "Test: Missing required key returns error with field name"
          priority: "Critical"
        - id: "SVC-003"
          description: "Validate value ranges using bash arithmetic"
          testable: true
          test_requirement: "Test: Out-of-range values rejected with helpful message"
          priority: "High"

    - type: "DataModel"
      name: "ParallelConfig"
      table: "N/A (in-memory, documented pattern)"
      purpose: "Represents loaded parallel orchestration configuration"
      fields:
        - name: "version"
          type: "String"
          constraints: "Required"
          description: "Config schema version"
          test_requirement: "Test: Verify version field populated"
        - name: "default_profile"
          type: "String"
          constraints: "Required, Enum(pro, max, api, custom)"
          description: "Active profile name"
          test_requirement: "Test: Verify default_profile field populated"
        - name: "profiles"
          type: "Dict[String, ProfileConfig]"
          constraints: "Required, min 1 profile"
          description: "Profile name to settings mapping"
          test_requirement: "Test: Verify profiles dictionary populated"

  business_rules:
    - id: "BR-001"
      rule: "max_concurrent_tasks must be between 1 and 10 inclusive"
      trigger: "Config validation on load"
      validation: "Bash arithmetic range check"
      error_handling: "Display error with field name and valid range"
      test_requirement: "Test: Values 0, 11 rejected; values 1, 10 accepted"
      priority: "Critical"
    - id: "BR-002"
      rule: "timeout_ms must be between 1000 and 600000 (10 minutes max)"
      trigger: "Config validation on load"
      validation: "Bash arithmetic range check"
      error_handling: "Display error with field name and valid range"
      test_requirement: "Test: Values 999, 600001 rejected; values 1000, 600000 accepted"
      priority: "Critical"
    - id: "BR-003"
      rule: "Profile presets (pro/max/api) have locked defaults that cannot be overridden"
      trigger: "Config merge during load"
      validation: "Preset values take precedence over user values"
      error_handling: "Log warning if user attempts to override preset values"
      test_requirement: "Test: Preset profile ignores user overrides"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Config validation must complete within 1 second"
      metric: "< 1s validation time"
      test_requirement: "Test: Benchmark config validation"
      priority: "High"
    - id: "NFR-002"
      category: "Reliability"
      requirement: "Missing config file falls back to sensible defaults"
      metric: "Default pro profile applied when no config exists"
      test_requirement: "Test: No config file returns default ParallelConfig"
      priority: "High"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- Config validation: < 1 second

**Throughput:**
- N/A (configuration loaded once at startup)

---

### Security

**Authentication:** None (local file access)

**Data Protection:**
- Config file should not contain secrets
- Warn if credentials detected in config

---

### Reliability

**Error Handling:**
- Invalid config: Clear error message with field name and expected format
- Missing config: Fall back to defaults with warning log

**Retry Logic:** N/A (single load operation)

---

## Dependencies

### Prerequisite Stories

None - this is a foundation story.

### Technology Dependencies

- [ ] **bash 4.0+** (standard)
  - **Purpose:** Config validation script
  - **Approved:** Yes (in tech-stack.md - "Bash scripting")

- [ ] **grep** (standard)
  - **Purpose:** YAML field extraction
  - **Approved:** Yes (in tech-stack.md - "Grep patterns for YAML frontmatter")

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for validation script

**Test Scenarios:**
1. **Happy Path:** Load valid config, verify all fields extracted
2. **Edge Cases:**
   - Empty profiles section
   - Custom profile with partial settings
   - Profile name with special characters
3. **Error Cases:**
   - Invalid YAML syntax (malformed)
   - Missing required fields
   - Out-of-range values

---

## Acceptance Criteria Verification Checklist

### AC#1: Configuration File Schema

- [x] Schema documented in parallel-config.md - **Phase:** 2 - **Evidence:** `.claude/skills/devforgeai-orchestration/references/parallel-config.md`
- [x] YAML file loads successfully via Read tool - **Phase:** 3 - **Evidence:** `devforgeai/config/parallel-orchestration.yaml`
- [x] All required keys validated via grep - **Phase:** 3 - **Evidence:** `test-ac1-configuration-schema.sh` (4/4 PASS)

### AC#2: Profile Presets

- [x] Pro preset defined with correct values - **Phase:** 3 - **Evidence:** `test-ac2-profile-presets.sh` (pro: tasks=4, timeout=120000)
- [x] Max preset defined with correct values - **Phase:** 3 - **Evidence:** `test-ac2-profile-presets.sh` (max: tasks=6, timeout=180000)
- [x] API preset defined with correct values - **Phase:** 3 - **Evidence:** `test-ac2-profile-presets.sh` (api: tasks=8, timeout=300000)

### AC#3: Configurable Timeouts

- [x] Timeout monitoring documented in pattern - **Phase:** 3 - **Evidence:** `parallel-config.md` "Timeout Handling Pattern" section
- [x] KillShell invocation for timeout - **Phase:** 3 - **Evidence:** `parallel-config.md` "Graceful Termination with KillShell" section
- [x] Error logged on timeout - **Phase:** 3 - **Evidence:** `parallel-config.md` Logger Pattern section

### AC#4: Configuration Validation

- [x] Range validation for max_concurrent_tasks - **Phase:** 3 - **Evidence:** `test-ac4-configuration-validation.sh` BR-001 tests (5/5 PASS)
- [x] Range validation for timeout_ms - **Phase:** 3 - **Evidence:** `test-ac4-configuration-validation.sh` BR-002 tests (5/5 PASS)
- [x] Clear error messages on validation failure - **Phase:** 3 - **Evidence:** `test-ac4-configuration-validation.sh` error message tests (2/2 PASS)

---

**Checklist Progress:** 12/12 items complete (100%)

---

## Definition of Done

### Implementation
- [x] `devforgeai/config/parallel-orchestration.yaml` template created
- [x] `scripts/validate-parallel-config.sh` validation script created
- [x] `.claude/skills/devforgeai-orchestration/references/parallel-config.md` documentation created
- [x] Profile presets (Pro/Max/API) documented with correct defaults

### Quality
- [x] All 4 acceptance criteria have passing tests (28/28 tests)
- [x] Edge cases covered (invalid YAML, missing fields, out-of-range values)
- [x] Data validation enforced (BR-001, BR-002)
- [x] NFRs met (< 1s validation time) - validation completes in ~0.05s
- [x] Test coverage >95% for validation script (28 tests cover all code paths)

### Testing
- [x] Unit tests for config validation script (`test-ac4-configuration-validation.sh`)
- [x] Unit tests for validation logic (BR-001/BR-002 range tests)
- [x] Unit tests for profile preset application (`test-ac2-profile-presets.sh`)
- [x] Integration test for end-to-end config flow (`validate-parallel-config.sh` run on real config)

### Documentation
- [x] Configuration reference documented (`parallel-config.md`)
- [x] Profile presets documented with use cases (Quick Reference table)
- [x] Error messages documented in troubleshooting guide (Troubleshooting section)

---

## Implementation Notes

**Developer:** Claude (DevForgeAI AI Agent)
**Implemented:** 2025-12-19
**Branch:** refactor/devforgeai-migration

- [x] `devforgeai/config/parallel-orchestration.yaml` template created - Completed: Config file with Pro/Max/API/custom profiles, version 1.0
- [x] `scripts/validate-parallel-config.sh` validation script created - Completed: Bash script with BR-001/BR-002/BR-003 validation, exit codes 0/1/2
- [x] `.claude/skills/devforgeai-orchestration/references/parallel-config.md` documentation created - Completed: Reference doc with Config Loading, Validation Rules, Default Fallback, Timeout Handling sections
- [x] Profile presets (Pro/Max/API) documented with correct defaults - Completed: Pro=4/120000, Max=6/180000, API=8/300000
- [x] All 4 acceptance criteria have passing tests (28/28 tests) - Completed: test-ac1 (4), test-ac2 (9), test-ac3 (3), test-ac4 (12)
- [x] Edge cases covered (invalid YAML, missing fields, out-of-range values) - Completed: BR-001/BR-002 boundary tests (0, 1, 10, 11, 999, 1000, 600000, 600001)
- [x] Data validation enforced (BR-001, BR-002) - Completed: Range validation with clear error messages
- [x] NFRs met (< 1s validation time) - Completed: Validation completes in ~0.05s
- [x] Test coverage >95% for validation script (28 tests cover all code paths) - Completed: All code paths exercised
- [x] Unit tests for config validation script - Completed: test-ac4-configuration-validation.sh
- [x] Unit tests for validation logic (BR-001/BR-002 range tests) - Completed: 10 boundary tests
- [x] Unit tests for profile preset application - Completed: test-ac2-profile-presets.sh (9 tests)
- [x] Integration test for end-to-end config flow - Completed: validate-parallel-config.sh run on real config
- [x] Configuration reference documented - Completed: parallel-config.md Quick Reference section
- [x] Profile presets documented with use cases - Completed: Quick Reference table with tier mappings
- [x] Error messages documented in troubleshooting guide - Completed: Troubleshooting section in parallel-config.md

### TDD Workflow Summary

**Phase 01 (Red):** 28 tests written, all FAILED (config/script/doc missing)
**Phase 02 (Green):** Implementation added, 28/28 tests PASSED
**Phase 03 (Refactor):** Code reviewed, no changes needed

### Files Created

- `devforgeai/config/parallel-orchestration.yaml` (57 lines)
- `scripts/validate-parallel-config.sh` (165 lines)
- `.claude/skills/devforgeai-orchestration/references/parallel-config.md` (198 lines)
- `devforgeai/tests/STORY-108/test-ac1-configuration-schema.sh` (130 lines)
- `devforgeai/tests/STORY-108/test-ac2-profile-presets.sh` (149 lines)
- `devforgeai/tests/STORY-108/test-ac3-configurable-timeouts.sh` (120 lines)
- `devforgeai/tests/STORY-108/test-ac4-configuration-validation.sh` (339 lines)

---

## QA Validation History

### QA Attempt 1 (2025-12-19) - PASSED

**Mode:** Deep Validation
**Validator:** DevForgeAI QA Skill

| Phase | Result | Details |
|-------|--------|---------|
| Phase 0.9: Traceability | PASS | 100% (4 ACs, 16 DoD items) |
| Phase 1: Coverage | PASS | 28/28 tests, 100% coverage |
| Phase 2: Anti-Patterns | PASS | 0 violations |
| Phase 3: Spec Compliance | PASS | 4/4 ACs, 2/2 NFRs |
| Phase 4: Code Quality | PASS | All metrics within thresholds |

**Deferral Validation:** N/A (no deferrals)
**Report:** `devforgeai/qa/reports/STORY-108-qa-report.md`

---

## Workflow Status

- [x] Architecture phase complete - Not required (framework-level story)
- [x] Development phase complete - Completed: 2025-12-19
- [x] QA phase complete - Completed: 2025-12-19 (PASSED)
- [ ] Released - Pending: Run /release STORY-108

## Notes

**Design Decisions:**
- Profile presets are locked to prevent misconfiguration that could exceed API limits
- YAML chosen over JSON for human-friendly editing with comments
- **Framework-compliant:** Uses bash script + grep patterns instead of Python (per tech-stack.md)
- **Path corrected:** Uses `devforgeai/config/` (not `.devforgeai/`) per source-tree.md

**Related ADRs:**
- None yet (may create ADR for profile preset values)

**References:**
- EPIC-017: Parallel Task Orchestration for DevForgeAI
- [Anthropic rate limits documentation](https://docs.anthropic.com/en/docs/rate-limits)
- Research: `docs/enhancements/2025-12-04/research/parallel-orchestration-research.md`

---

**Story Template Version:** 2.2
**Last Updated:** 2025-12-19
**Context Compliance:** Verified against tech-stack.md, source-tree.md, dependencies.md, anti-patterns.md
