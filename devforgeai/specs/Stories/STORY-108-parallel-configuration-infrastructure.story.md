---
id: STORY-108
title: Parallel Configuration Infrastructure
epic: EPIC-017
sprint: Backlog
status: Backlog
points: 5
depends_on: []
priority: Medium
assigned_to: TBD
created: 2025-12-18
format_version: "2.2"
---

# Story: Parallel Configuration Infrastructure

## Description

**As a** DevForgeAI user,
**I want** a configuration file for parallel task orchestration with profile support and timeout settings,
**so that** I can match my Anthropic subscription tier and ensure long-running operations fail gracefully.

This story implements EPIC-017 Feature 1: Create `.devforgeai/config/parallel-orchestration.yaml` with profile support, timeout settings, and retry configuration. Foundation for all parallel patterns.

## Acceptance Criteria

### AC#1: Configuration File Schema

**Given** the DevForgeAI framework is installed,
**When** a user creates `.devforgeai/config/parallel-orchestration.yaml`,
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
      file_path: ".devforgeai/config/parallel-orchestration.yaml"
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

    - type: "Service"
      name: "ParallelConfigLoader"
      file_path: "src/skills/orchestration/parallel-config-loader.py"
      interface: "IParallelConfigLoader"
      lifecycle: "Singleton"
      dependencies:
        - "yaml"
        - "jsonschema"
      requirements:
        - id: "SVC-001"
          description: "Load and parse parallel-orchestration.yaml"
          testable: true
          test_requirement: "Test: Load valid config file and return ParallelConfig object"
          priority: "Critical"
        - id: "SVC-002"
          description: "Validate config against JSON schema"
          testable: true
          test_requirement: "Test: Invalid config raises ValidationError with helpful message"
          priority: "Critical"
        - id: "SVC-003"
          description: "Merge profile settings with defaults"
          testable: true
          test_requirement: "Test: Custom profile inherits unspecified values from defaults"
          priority: "High"

    - type: "DataModel"
      name: "ParallelConfig"
      table: "N/A (in-memory)"
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
      validation: "Range check against bounds"
      error_handling: "Raise ConfigurationError with field name and valid range"
      test_requirement: "Test: Values 0, 11 rejected; values 1, 10 accepted"
      priority: "Critical"
    - id: "BR-002"
      rule: "timeout_ms must be between 1000 and 600000 (10 minutes max)"
      trigger: "Config validation on load"
      validation: "Range check against bounds"
      error_handling: "Raise ConfigurationError with field name and valid range"
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
      requirement: "Config loading must complete within 100ms"
      metric: "< 100ms p95 load time"
      test_requirement: "Test: Benchmark config loading across 100 iterations"
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
- Config loading: < 100ms (p95)

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

- [ ] **PyYAML** v6.0+
  - **Purpose:** YAML parsing
  - **Approved:** Yes (in tech-stack.md)
  - **Added to dependencies.md:** Pending

- [ ] **jsonschema** v4.0+
  - **Purpose:** Config validation
  - **Approved:** Yes (in tech-stack.md)
  - **Added to dependencies.md:** Pending

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for ParallelConfigLoader

**Test Scenarios:**
1. **Happy Path:** Load valid config, verify all fields populated
2. **Edge Cases:**
   - Empty profiles section
   - Custom profile with partial settings
   - Profile name with special characters
3. **Error Cases:**
   - Invalid YAML syntax
   - Missing required fields
   - Out-of-range values

---

## Acceptance Criteria Verification Checklist

### AC#1: Configuration File Schema

- [ ] Schema defined in JSON schema format - **Phase:** 2 - **Evidence:** TBD
- [ ] YAML file loads successfully - **Phase:** 3 - **Evidence:** TBD
- [ ] All required keys validated - **Phase:** 3 - **Evidence:** TBD

### AC#2: Profile Presets

- [ ] Pro preset defined with correct values - **Phase:** 3 - **Evidence:** TBD
- [ ] Max preset defined with correct values - **Phase:** 3 - **Evidence:** TBD
- [ ] API preset defined with correct values - **Phase:** 3 - **Evidence:** TBD

### AC#3: Configurable Timeouts

- [ ] Timeout monitoring implemented - **Phase:** 3 - **Evidence:** TBD
- [ ] Graceful termination on timeout - **Phase:** 3 - **Evidence:** TBD
- [ ] Error logged on timeout - **Phase:** 3 - **Evidence:** TBD

### AC#4: Configuration Validation

- [ ] Range validation for max_concurrent_tasks - **Phase:** 3 - **Evidence:** TBD
- [ ] Range validation for timeout_ms - **Phase:** 3 - **Evidence:** TBD
- [ ] Clear error messages on validation failure - **Phase:** 3 - **Evidence:** TBD

---

**Checklist Progress:** 0/12 items complete (0%)

---

## Definition of Done

### Implementation
- [ ] `.devforgeai/config/parallel-orchestration.yaml` schema defined
- [ ] ParallelConfigLoader service implemented
- [ ] Profile presets (Pro/Max/API) configured with correct defaults
- [ ] Configuration validation with JSON schema

### Quality
- [ ] All 4 acceptance criteria have passing tests
- [ ] Edge cases covered (invalid YAML, missing fields, out-of-range values)
- [ ] Data validation enforced (BR-001, BR-002)
- [ ] NFRs met (< 100ms load time)
- [ ] Code coverage >95% for ParallelConfigLoader

### Testing
- [ ] Unit tests for config loading
- [ ] Unit tests for validation logic
- [ ] Unit tests for profile preset application
- [ ] Integration test for end-to-end config flow

### Documentation
- [ ] Configuration reference documented
- [ ] Profile presets documented with use cases
- [ ] Error messages documented in troubleshooting guide

---

## Workflow Status

- [ ] Architecture phase complete
- [ ] Development phase complete
- [ ] QA phase complete
- [ ] Released

## Notes

**Design Decisions:**
- Profile presets are locked to prevent misconfiguration that could exceed API limits
- YAML chosen over JSON for human-friendly editing with comments

**Related ADRs:**
- None yet (may create ADR for profile preset values)

**References:**
- EPIC-017: Parallel Task Orchestration for DevForgeAI
- [Anthropic rate limits documentation](https://docs.anthropic.com/en/docs/rate-limits)
- Research: `docs/enhancements/2025-12-04/research/parallel-orchestration-research.md`

---

**Story Template Version:** 2.2
**Last Updated:** 2025-12-18
