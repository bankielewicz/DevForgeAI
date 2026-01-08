---
id: STORY-245
title: Registry Configuration
type: feature
epic: EPIC-038
sprint: Backlog
priority: Medium
points: 3
depends_on: []
status: Dev Complete
created: 2025-01-06
updated: 2026-01-08
---

# STORY-245: Registry Configuration

## User Story

**As a** developer configuring package publishing,
**I want** a YAML configuration file for registry settings,
**So that** I can customize registry endpoints, enable/disable registries, and configure version conflict behavior.

## Acceptance Criteria

### AC#1: Registry Configuration File Schema

**Given** the DevForgeAI release workflow
**When** registry publishing is configured
**Then** a `registry-config.yaml` file is created in `devforgeai/deployment/`
**And** the schema supports all 6 registries (npm, pypi, nuget, docker, github, crates)
**And** each registry has enabled, endpoint, and options fields
**And** JSON Schema validation is available for the config file

### AC#2: Registry Enable/Disable Control

**Given** a registry-config.yaml file
**When** a registry has `enabled: false`
**Then** that registry is skipped during publishing
**And** a log message indicates "Registry {name} disabled in config"
**And** the skip does not count as a failure

### AC#3: Custom Registry Endpoints

**Given** a registry-config.yaml file
**When** a registry has a custom `registry` or `source` URL
**Then** publish commands use the custom endpoint instead of default
**And** npm uses `--registry {url}` flag
**And** NuGet uses `--source {url}` flag
**And** Docker uses the custom registry prefix

### AC#4: Version Conflict Handling Configuration

**Given** a registry-config.yaml file
**When** `skip-existing: true` is set for a registry
**Then** version conflict errors are handled gracefully
**And** publish skips with info message instead of failing
**And** when `skip-existing: false`, version conflict causes failure

### AC#5: Credential Environment Variable Mapping

**Given** a registry-config.yaml file
**When** custom credential environment variable names are specified
**Then** the publisher uses the configured variable names
**And** default variable names are used if not specified
**And** missing required credentials cause clear error messages

### AC#6: Configuration Validation on Load

**Given** a registry-config.yaml file with invalid content
**When** the release skill loads the configuration
**Then** JSON Schema validation fails with specific error
**And** error message indicates line/field with issue
**And** publish does not proceed until config is valid

## AC Verification Checklist

### AC#1 Verification (Schema)
- [ ] registry-config.yaml template created
- [ ] All 6 registries have configuration blocks
- [ ] JSON Schema file created (registry-config.schema.json)
- [ ] Schema validates enabled, registry/source, options fields
- [ ] Example config with all options documented

### AC#2 Verification (Enable/Disable)
- [ ] enabled: true/false parsed correctly
- [ ] Disabled registries logged as skipped
- [ ] Disabled registries don't count in success/failure
- [ ] Default is enabled: true if field missing

### AC#3 Verification (Custom Endpoints)
- [ ] npm --registry flag constructed correctly
- [ ] nuget --source flag constructed correctly
- [ ] docker registry prefix applied
- [ ] pypi --repository option supported
- [ ] GitHub registry URLs supported (npm.pkg.github.com, ghcr.io)

### AC#4 Verification (Skip Existing)
- [ ] skip-existing: true enables graceful skip
- [ ] skip-existing: false causes version error to fail
- [ ] Default is skip-existing: true
- [ ] Skip reason logged clearly

### AC#5 Verification (Credentials)
- [ ] Custom env var names parsed from config
- [ ] Default env var names documented
- [ ] Missing credential error includes variable name
- [ ] Credential validation before any publish

### AC#6 Verification (Validation)
- [ ] JSON Schema validation on load
- [ ] Invalid YAML syntax detected
- [ ] Missing required fields detected
- [ ] Invalid field values detected
- [ ] Line number in error messages

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"
  story_id: STORY-245

  components:
    - name: RegistryConfig
      type: Configuration
      path: devforgeai/deployment/registry-config.yaml
      description: YAML configuration for registry publishing
      fields:
        - name: registries
          type: dict
          description: Registry configurations keyed by name
        - name: defaults
          type: dict
          description: Default settings for all registries
      test_requirement: "Validation tests with valid and invalid configs"

    - name: RegistryConfigLoader
      type: Service
      path: installer/registry_config.py
      description: Load and validate registry configuration
      public_methods:
        - name: load
          signature: "load(config_path: str = None) -> RegistryConfig"
          description: Load config from file with validation
        - name: validate
          signature: "validate(config: dict) -> ValidationResult"
          description: Validate config against JSON Schema
        - name: get_registry
          signature: "get_registry(name: str) -> RegistrySettings"
          description: Get settings for specific registry
        - name: get_enabled_registries
          signature: "get_enabled_registries() -> list[str]"
          description: List all enabled registry names
      test_requirement: "Unit tests for loading, validation, and registry access"

    - name: RegistrySettings
      type: DataModel
      path: installer/registry_config.py
      description: Settings for a single registry
      fields:
        - name: name
          type: str
          description: Registry identifier (npm, pypi, etc.)
        - name: enabled
          type: bool
          description: Whether registry is enabled
          default: true
        - name: registry_url
          type: Optional[str]
          description: Custom registry endpoint
        - name: skip_existing
          type: bool
          description: Skip if version exists
          default: true
        - name: credentials
          type: CredentialConfig
          description: Credential environment variable mapping
        - name: options
          type: dict
          description: Registry-specific options
      test_requirement: "Validation tests for all field combinations"

    - name: CredentialConfig
      type: DataModel
      path: installer/registry_config.py
      description: Credential environment variable configuration
      fields:
        - name: token_var
          type: Optional[str]
          description: Single token env var name
        - name: username_var
          type: Optional[str]
          description: Username env var name
        - name: password_var
          type: Optional[str]
          description: Password env var name
      test_requirement: "Tests for credential resolution"

    - name: ConfigValidationResult
      type: DataModel
      path: installer/registry_config.py
      description: Result of configuration validation
      fields:
        - name: valid
          type: bool
          description: Whether config is valid
        - name: errors
          type: list[ConfigError]
          description: List of validation errors
        - name: warnings
          type: list[ConfigWarning]
          description: List of validation warnings
      test_requirement: "Tests for error aggregation"

    - name: registry-config.schema.json
      type: Configuration
      path: devforgeai/deployment/registry-config.schema.json
      description: JSON Schema for registry configuration validation
      test_requirement: "Schema validation tests with edge cases"

  business_rules:
    - id: BR-001
      description: Missing config file uses sensible defaults (all registries enabled, default endpoints)
      validation: Default config generated when file not found
      test_requirement: "Test with missing config file"

    - id: BR-002
      description: Invalid config blocks publishing (fail fast)
      validation: Validation runs before any publish attempt
      test_requirement: "Test invalid config prevents publish"

    - id: BR-003
      description: Custom credentials override defaults, not append
      validation: Only configured credential vars are checked
      test_requirement: "Test custom credential priority"

    - id: BR-004
      description: Disabled registries are logged but not counted as success/failure
      validation: Separate counter for skipped/disabled
      test_requirement: "Test disabled registry counting"

  non_functional_requirements:
    - id: NFR-001
      category: Performance
      description: Config loading and validation < 500ms
      metric: config_load_time
      target: "< 500ms"
      test_requirement: "Timed config load test"

    - id: NFR-002
      category: Usability
      description: Validation errors include line numbers and fix suggestions
      metric: error_actionability
      target: "100% actionable errors"
      test_requirement: "Error message quality tests"

    - id: NFR-003
      category: Reliability
      description: Config file changes detected on each publish (no caching issues)
      metric: config_freshness
      target: "Always fresh read"
      test_requirement: "File modification detection test"
```

## Technical Limitations

```yaml
technical_limitations: []
```

## UI Specification

**UI Type:** Configuration File

### Configuration Template

```yaml
# registry-config.yaml
# DevForgeAI Registry Publishing Configuration
# Schema: devforgeai/deployment/registry-config.schema.json

# Default settings applied to all registries
defaults:
  skip-existing: true  # Skip if version already published
  dry-run: false       # Set true to test without publishing

registries:
  npm:
    enabled: true
    registry: https://registry.npmjs.org
    access: public  # public | restricted
    # credentials: uses NPM_TOKEN by default

  pypi:
    enabled: true
    repository: pypi  # pypi | testpypi | <custom-url>
    skip-existing: true
    # credentials: uses TWINE_USERNAME, TWINE_PASSWORD by default

  nuget:
    enabled: false  # Disabled by default
    source: https://api.nuget.org/v3/index.json
    skip-duplicate: true
    # credentials: uses NUGET_API_KEY by default

  docker:
    enabled: true
    registry: docker.io
    repository: ""  # Set to org/repo name
    tags:
      - latest
      - "{{version}}"
    # credentials: uses DOCKER_USERNAME, DOCKER_PASSWORD by default

  github:
    enabled: true
    packages: true      # npm/nuget packages
    container: true     # container registry (ghcr.io)
    # credentials: uses GITHUB_TOKEN by default

  crates:
    enabled: false  # Disabled by default
    allow-dirty: false
    # credentials: uses CARGO_REGISTRY_TOKEN by default
```

### CLI Output on Config Error

```
❌ Registry configuration invalid

Errors in devforgeai/deployment/registry-config.yaml:
  Line 12: registries.npm.access must be 'public' or 'restricted', got 'private'
  Line 18: registries.pypi.repository must be valid URL or 'pypi'/'testpypi'

Fix these errors and run again.
```

## Non-Functional Requirements

| Category | Requirement | Target | Measurement |
|----------|-------------|--------|-------------|
| Performance | Config load time | < 500ms | Timer in load function |
| Usability | Error messages | 100% actionable | Include line number and fix |
| Reliability | File freshness | Always fresh | No caching between runs |
| Maintainability | Schema versioning | Backward compatible | Version field in schema |

## Edge Cases

1. **Missing config file** - Use defaults (all registries enabled, default endpoints)
2. **Partial config** - Merge with defaults (missing fields use defaults)
3. **Unknown registry** - Log warning, ignore (don't fail)
4. **Invalid YAML syntax** - Fail with parse error and line number
5. **Missing required field** - Fail with field name and expected type
6. **Empty registries section** - Treat as all registries disabled
7. **Custom credential vars missing** - Check configured names, not defaults

## Dependencies

### Internal Dependencies
- None (foundation story for STORY-244)

### External Dependencies
- PyYAML for YAML parsing
- jsonschema for validation

## Definition of Done

### Implementation
- [x] RegistryConfig dataclass created - Completed: RegistryConfig container dataclass in installer/registry_config.py
- [x] RegistryConfigLoader with load/validate methods - Completed: Full service class with load(), validate(), get_registry(), get_enabled_registries()
- [x] registry-config.yaml template created - Completed: Template in devforgeai/deployment/registry-config.yaml with all 6 registries
- [x] registry-config.schema.json created - Completed: JSON Schema in devforgeai/deployment/registry-config.schema.json
- [x] Default config generation when file missing - Completed: BR-001 defaults all registries enabled when file not found
- [x] Merge logic for partial configs - Completed: Partial configs merged with defaults per Edge Case 2

### Testing
- [x] Unit tests for config loading - Completed: TestRegistryConfigLoaderService class (5 tests)
- [x] Unit tests for JSON Schema validation - Completed: TestConfigurationValidationOnLoad class (5 tests)
- [x] Tests for default value merging - Completed: TestBusinessRules test_br001 and Edge Case 2 tests
- [x] Tests for custom credential mapping - Completed: TestCredentialEnvironmentVariableMapping class (9 tests)
- [x] Edge case tests (missing file, invalid syntax, etc.) - Completed: TestEdgeCases class (7 tests)

### Documentation
- [x] Config file template with all options - Completed: Template includes all 6 registries with documented options
- [x] Comments explaining each field - Completed: Inline comments in registry-config.yaml
- [x] Schema file with descriptions - Completed: JSON Schema includes description for all properties

### Quality
- [x] Code coverage > 85% - Completed: 91% coverage (exceeds 85% threshold)
- [x] Schema validates all examples in tests - Completed: Inline validation covers all test scenarios
- [x] Error messages are actionable - Completed: NFR-002 tested for actionable error messages

## Implementation Notes

**Developer:** DevForgeAI AI Agent (claude/opus)
**Implemented:** 2026-01-08
**Branch:** refactor/devforgeai-migration

- [x] RegistryConfig dataclass created - Completed: RegistryConfig container dataclass in installer/registry_config.py
- [x] RegistryConfigLoader with load/validate methods - Completed: Full service class with load(), validate(), get_registry(), get_enabled_registries()
- [x] registry-config.yaml template created - Completed: Template in devforgeai/deployment/registry-config.yaml with all 6 registries
- [x] registry-config.schema.json created - Completed: JSON Schema in devforgeai/deployment/registry-config.schema.json
- [x] Default config generation when file missing - Completed: BR-001 defaults all registries enabled when file not found
- [x] Merge logic for partial configs - Completed: Partial configs merged with defaults per Edge Case 2
- [x] Unit tests for config loading - Completed: TestRegistryConfigLoaderService class (5 tests)
- [x] Unit tests for JSON Schema validation - Completed: TestConfigurationValidationOnLoad class (5 tests)
- [x] Tests for default value merging - Completed: TestBusinessRules test_br001 and Edge Case 2 tests
- [x] Tests for custom credential mapping - Completed: TestCredentialEnvironmentVariableMapping class (9 tests)
- [x] Edge case tests (missing file, invalid syntax, etc.) - Completed: TestEdgeCases class (7 tests)
- [x] Config file template with all options - Completed: Template includes all 6 registries with documented options
- [x] Comments explaining each field - Completed: Inline comments in registry-config.yaml
- [x] Schema file with descriptions - Completed: JSON Schema includes description for all properties
- [x] Code coverage > 85% - Completed: 91% coverage (exceeds 85% threshold)
- [x] Schema validates all examples in tests - Completed: Inline validation covers all test scenarios
- [x] Error messages are actionable - Completed: NFR-002 tested for actionable error messages

### TDD Workflow Summary

**Phase 02 (Red): Test-First Design**
- Generated 65 comprehensive tests covering all 6 acceptance criteria
- Tests placed in installer/tests/test_registry_config.py
- All tests follow AAA pattern (Arrange/Act/Assert)
- Test framework: pytest

**Phase 03 (Green): Implementation**
- Implemented RegistryConfigLoader service via backend-architect subagent
- Created 6 dataclasses: CredentialConfig, ConfigError, ConfigWarning, ConfigValidationResult, RegistrySettings, RegistryConfig
- All 65 tests passing (100% pass rate)

**Phase 04 (Refactor): Code Quality**
- Refactoring-specialist: No changes needed - code already well-structured
- Code-reviewer: APPROVED with minor suggestions for future improvements
- All tests remain green after review

**Phase 05 (Integration): Full Validation**
- Full test suite executed: 65 passed in 0.31s
- Coverage verified: 91% (exceeds 80% threshold)
- One cross-component observation: RegistryConfig naming collision with registry_publisher.py (medium severity)

**Phase 06 (Deferral Challenge): DoD Validation**
- User chose "HALT and implement NOW" for missing template files
- Created registry-config.yaml and registry-config.schema.json
- No deferrals remaining

### Files Created

- installer/registry_config.py (538 lines)
- installer/tests/test_registry_config.py (1511 lines)
- devforgeai/deployment/registry-config.yaml (72 lines)
- devforgeai/deployment/registry-config.schema.json (175 lines)

### Test Results

- **Total tests:** 65
- **Pass rate:** 100%
- **Coverage:** 91%
- **Execution time:** 0.31 seconds

## Change Log

**Current Status:** Dev Complete

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2025-01-06 | claude/story-creation | Story Creation | Created story from EPIC-038 Feature 2 | STORY-245-registry-configuration.story.md |
| 2026-01-08 | claude/opus | DoD Update (Phase 07) | Development complete, DoD validated | STORY-245-registry-configuration.story.md |

---

**Template Version:** 2.5
**Created:** 2025-01-06 by devforgeai-story-creation skill (batch mode)
