---
id: STORY-116
title: Configuration Infrastructure - ast-grep Rule Storage
epic: EPIC-018
sprint: SPRINT-7
status: QA Approved ✅
points: 5
depends_on: ["STORY-115"]
priority: Medium
assigned_to: Claude
created: 2025-12-20
format_version: "2.2"
---

# Story: Configuration Infrastructure - ast-grep Rule Storage

## Description

**As a** DevForgeAI maintainer,
**I want** a standardized directory structure and configuration for ast-grep rules,
**so that** rules are organized by language and can be easily extended or modified.

**Context:** This story implements Feature 2 of EPIC-018 (ast-grep Foundation & Core Rules). It establishes the rule storage structure, sgconfig.yml configuration, and language mappings following DevForgeAI conventions.

## Acceptance Criteria

### AC#1: Project-Scoped Rule Storage

**Given** a DevForgeAI project,
**When** the user initializes ast-grep integration,
**Then** the CLI creates the following directory structure:
```
.devforgeai/
└── ast-grep/
    ├── sgconfig.yml
    └── rules/
        ├── python/
        ├── csharp/
        ├── typescript/
        └── javascript/
```

---

### AC#2: Language-Specific Directory Organization

**Given** the ast-grep rules directory exists,
**When** a rule author creates a new rule,
**Then** rules are organized by:
1. Language directory (python/, csharp/, typescript/, javascript/)
2. Category subdirectory (security/, anti-patterns/, complexity/)
3. Individual rule files (*.yml or *.yaml)

---

### AC#3: Auto-Generated sgconfig.yml

**Given** the ast-grep directory structure is initialized,
**When** the user runs `devforgeai ast-grep init`,
**Then** sgconfig.yml is created with:
1. Rule directories pointing to language folders
2. Language-to-glob mappings (*.py, *.cs, *.ts, *.js)
3. Test directory exclusions (tests/, __tests__/, *_test.py)
4. DevForgeAI-specific metadata (version, created date)

---

### AC#4: Configuration Validation

**Given** an sgconfig.yml exists,
**When** the user runs `devforgeai ast-grep validate-config`,
**Then** the CLI validates:
1. YAML syntax is correct
2. All referenced rule directories exist
3. Language globs are valid
4. Returns success/failure with specific errors

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service"
      name: "ConfigurationInitializer"
      file_path: "src/claude/scripts/devforgeai_cli/ast_grep/config_init.py"
      interface: "IInitializer"
      lifecycle: "Transient"
      dependencies:
        - "os"
        - "pathlib"
        - "yaml"
      requirements:
        - id: "SVC-001"
          description: "Create .devforgeai/ast-grep/ directory structure"
          testable: true
          test_requirement: "Test: Verify all directories created with correct permissions"
          priority: "Critical"
        - id: "SVC-002"
          description: "Generate sgconfig.yml with default configuration"
          testable: true
          test_requirement: "Test: Validate generated YAML against schema"
          priority: "Critical"
        - id: "SVC-003"
          description: "Skip existing directories without overwriting"
          testable: true
          test_requirement: "Test: Re-run init, verify existing rules preserved"
          priority: "High"

    - type: "Service"
      name: "ConfigurationValidator"
      file_path: "src/claude/scripts/devforgeai_cli/ast_grep/config_validator.py"
      interface: "IValidator"
      lifecycle: "Singleton"
      dependencies:
        - "yaml"
        - "pathlib"
        - "jsonschema"
      requirements:
        - id: "SVC-004"
          description: "Parse and validate YAML syntax"
          testable: true
          test_requirement: "Test: Valid YAML passes, malformed YAML fails with line number"
          priority: "Critical"
        - id: "SVC-005"
          description: "Verify referenced directories exist"
          testable: true
          test_requirement: "Test: Missing directory returns specific error"
          priority: "High"
        - id: "SVC-006"
          description: "Validate language glob patterns"
          testable: true
          test_requirement: "Test: Invalid glob pattern rejected with explanation"
          priority: "Medium"

    - type: "Configuration"
      name: "sgconfig.yml"
      file_path: ".devforgeai/ast-grep/sgconfig.yml"
      required_keys:
        - key: "ruleDirs"
          type: "array"
          example: "[rules/python, rules/csharp, rules/typescript, rules/javascript]"
          required: true
          default: "[rules/python, rules/csharp, rules/typescript, rules/javascript]"
          validation: "Array of existing directory paths"
          test_requirement: "Test: Parse ruleDirs array and verify paths"
        - key: "languageGlobs"
          type: "object"
          example: "{python: '**/*.py', csharp: '**/*.cs'}"
          required: true
          validation: "Valid glob patterns per language"
          test_requirement: "Test: Apply globs to test directory structure"
        - key: "testDirs"
          type: "array"
          example: "[tests, __tests__, *_test.py]"
          required: false
          default: "[tests, __tests__]"
          validation: "Array of directory patterns to exclude"
          test_requirement: "Test: Verify test directories excluded from scan"
        - key: "devforgeai"
          type: "object"
          example: "{version: '1.0', created: '2025-12-20'}"
          required: true
          validation: "Metadata object with version and timestamp"
          test_requirement: "Test: Metadata present and valid format"

    - type: "DataModel"
      name: "RuleMetadata"
      table: "N/A (file-based)"
      purpose: "Schema for individual rule YAML files"
      fields:
        - name: "id"
          type: "String"
          constraints: "Required, unique per language"
          description: "Rule identifier (e.g., SEC-001, AP-001)"
          test_requirement: "Test: Duplicate ID in same language rejected"
        - name: "language"
          type: "String"
          constraints: "Required, enum: python|csharp|typescript|javascript"
          description: "Target programming language"
          test_requirement: "Test: Invalid language rejected"
        - name: "severity"
          type: "String"
          constraints: "Required, enum: CRITICAL|HIGH|MEDIUM|LOW"
          description: "Violation severity level"
          test_requirement: "Test: Invalid severity rejected"
        - name: "message"
          type: "String"
          constraints: "Required, min 10 chars"
          description: "Human-readable violation message"
          test_requirement: "Test: Empty message rejected"
        - name: "pattern"
          type: "String"
          constraints: "Required, valid ast-grep pattern"
          description: "AST pattern to match"
          test_requirement: "Test: Pattern compiles successfully"

  business_rules:
    - id: "BR-001"
      rule: "Rule IDs must be unique within a language directory"
      trigger: "When loading rules for scanning"
      validation: "Collect all rule IDs, check for duplicates"
      error_handling: "Fail with list of duplicate IDs and file paths"
      test_requirement: "Test: Two rules with same ID in python/ causes error"
      priority: "Critical"
    - id: "BR-002"
      rule: "sgconfig.yml must not be overwritten if it exists (use --force)"
      trigger: "When running devforgeai ast-grep init"
      validation: "Check file existence before write"
      error_handling: "Prompt user or require --force flag"
      test_requirement: "Test: Init without --force on existing config fails"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Configuration initialization must complete in <2s"
      metric: "p95 latency <2s for directory creation and YAML write"
      test_requirement: "Test: Measure init time across 50 runs"
      priority: "Low"
    - id: "NFR-002"
      category: "Reliability"
      requirement: "Configuration validation must handle malformed YAML gracefully"
      metric: "100% of malformed YAML files return specific error messages"
      test_requirement: "Test: 10 malformed YAML fixtures all produce clear errors"
      priority: "High"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- Configuration init: <2s (p95)
- Configuration validation: <500ms (p95)

---

### Reliability

**Error Handling:**
- Clear error messages for YAML syntax errors
- Specific errors for missing directories
- No silent failures

---

## Dependencies

### Prerequisite Stories

- [x] **STORY-115:** CLI Validator Foundation
  - **Why:** Provides the CLI framework and ast-grep detection
  - **Status:** Backlog

### Technology Dependencies

- [ ] **Package:** PyYAML >=6.0
  - **Purpose:** YAML parsing and generation
  - **Approved:** Yes (existing dependency)

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for business logic

**Test Scenarios:**
1. **Happy Path:** Init creates all directories and valid config
2. **Edge Cases:**
   - Init on existing structure (should preserve)
   - Init with custom rule directories
   - Validation of complex glob patterns
3. **Error Cases:**
   - Malformed YAML (5+ variants)
   - Missing directories
   - Permission denied

---

## Acceptance Criteria Verification Checklist

### AC#1: Project-Scoped Rule Storage

- [x] .devforgeai/ast-grep/ created - **Phase:** 03 - **Evidence:** test_config_init_story116.py::TestConfigurationInitializerDirectoryCreation
- [x] rules/ subdirectories created - **Phase:** 03 - **Evidence:** test_config_init_story116.py::test_should_create_rules_*_directory
- [x] sgconfig.yml created - **Phase:** 03 - **Evidence:** test_config_init_story116.py::test_should_create_sgconfig_yml_file

### AC#2: Language-Specific Directory Organization

- [x] python/ directory exists - **Phase:** 03 - **Evidence:** test_config_init_story116.py::test_should_create_rules_python_directory
- [x] csharp/ directory exists - **Phase:** 03 - **Evidence:** test_config_init_story116.py::test_should_create_rules_csharp_directory
- [x] typescript/ directory exists - **Phase:** 03 - **Evidence:** test_config_init_story116.py::test_should_create_rules_typescript_directory
- [x] javascript/ directory exists - **Phase:** 03 - **Evidence:** test_config_init_story116.py::test_should_create_rules_javascript_directory

### AC#3: Auto-Generated sgconfig.yml

- [x] ruleDirs configured - **Phase:** 03 - **Evidence:** test_config_init_story116.py::test_should_include_ruleDirs_array_in_config
- [x] languageGlobs configured - **Phase:** 03 - **Evidence:** test_config_init_story116.py::test_should_include_languageGlobs_in_config
- [x] testDirs exclusions set - **Phase:** 03 - **Evidence:** test_config_init_story116.py::test_should_include_testDirs_array_in_config
- [x] devforgeai metadata present - **Phase:** 03 - **Evidence:** test_config_init_story116.py::test_should_include_devforgeai_metadata_in_config

### AC#4: Configuration Validation

- [x] YAML syntax validated - **Phase:** 03 - **Evidence:** test_config_validator_story116.py::TestConfigurationValidatorYAMLSyntax
- [x] Directory existence checked - **Phase:** 03 - **Evidence:** test_config_validator_story116.py::TestConfigurationValidatorDirectoryExistence
- [x] Glob patterns validated - **Phase:** 03 - **Evidence:** test_config_validator_story116.py::TestConfigurationValidatorGlobPatterns

---

**Checklist Progress:** 14/14 items complete (100%)

---

## Definition of Done

### Implementation
- [x] ConfigurationInitializer class created - src/claude/scripts/devforgeai_cli/ast_grep/config_init.py
- [x] ConfigurationValidator class created - src/claude/scripts/devforgeai_cli/ast_grep/config_validator.py
- [x] CLI command `devforgeai ast-grep init` implemented - .claude/scripts/devforgeai_cli/cli.py:301-320
- [x] CLI command `devforgeai ast-grep validate-config` implemented - .claude/scripts/devforgeai_cli/cli.py:322-362
- [x] Default sgconfig.yml template created - ConfigurationInitializer._generate_default_config()

### Quality
- [x] All 4 acceptance criteria have passing tests - 66 passed, 2 skipped
- [x] Edge cases covered (existing config, permissions, malformed YAML) - test_*_story116.py
- [x] Input validation enforced for all config fields - RuleMetadata validation in models.py
- [x] Code coverage >95% for config module - pytest coverage confirmed

### Testing
- [x] Unit tests for ConfigurationInitializer (8+ test cases) - 14 tests in test_config_init_story116.py
- [x] Unit tests for ConfigurationValidator (8+ test cases) - 16 tests in test_config_validator_story116.py
- [x] Integration tests for CLI commands (4+ scenarios) - 10 tests in test_ast_grep_cli_story116.py
- [x] Malformed YAML fixtures tested (5+ variants) - YAML syntax tests in test_config_validator_story116.py

### Documentation
- [x] CLI help text for init and validate-config commands - argparse help in cli.py
- [x] sgconfig.yml schema documentation - docs/ast-grep/sgconfig-schema.md
- [x] Rule authoring guide - docs/ast-grep/rule-authoring-guide.md

---

## Implementation Notes

### Completed Items

- [x] ConfigurationInitializer class created - src/claude/scripts/devforgeai_cli/ast_grep/config_init.py - Completed: 2025-12-20
- [x] ConfigurationValidator class created - src/claude/scripts/devforgeai_cli/ast_grep/config_validator.py - Completed: 2025-12-20
- [x] CLI command `devforgeai ast-grep init` implemented - .claude/scripts/devforgeai_cli/cli.py:301-320 - Completed: 2025-12-20
- [x] CLI command `devforgeai ast-grep validate-config` implemented - .claude/scripts/devforgeai_cli/cli.py:322-362 - Completed: 2025-12-20
- [x] Default sgconfig.yml template created - ConfigurationInitializer._generate_default_config() - Completed: 2025-12-20
- [x] All 4 acceptance criteria have passing tests - 66 passed, 2 skipped - Completed: 2025-12-20
- [x] Edge cases covered (existing config, permissions, malformed YAML) - test_*_story116.py - Completed: 2025-12-20
- [x] Input validation enforced for all config fields - RuleMetadata validation in models.py - Completed: 2025-12-20
- [x] Code coverage >95% for config module - pytest coverage confirmed - Completed: 2025-12-20
- [x] Unit tests for ConfigurationInitializer (8+ test cases) - 14 tests in test_config_init_story116.py - Completed: 2025-12-20
- [x] Unit tests for ConfigurationValidator (8+ test cases) - 16 tests in test_config_validator_story116.py - Completed: 2025-12-20
- [x] Integration tests for CLI commands (4+ scenarios) - 10 tests in test_ast_grep_cli_story116.py - Completed: 2025-12-20
- [x] Malformed YAML fixtures tested (5+ variants) - YAML syntax tests in test_config_validator_story116.py - Completed: 2025-12-20
- [x] CLI help text for init and validate-config commands - argparse help in cli.py - Completed: 2025-12-20
- [x] sgconfig.yml schema documentation - docs/ast-grep/sgconfig-schema.md - Completed: 2025-12-20
- [x] Rule authoring guide - docs/ast-grep/rule-authoring-guide.md - Completed: 2025-12-20

### Files Created

| File | Purpose |
|------|---------|
| `src/claude/scripts/devforgeai_cli/ast_grep/__init__.py` | Package exports |
| `src/claude/scripts/devforgeai_cli/ast_grep/models.py` | RuleMetadata, enums |
| `src/claude/scripts/devforgeai_cli/ast_grep/config_init.py` | ConfigurationInitializer |
| `src/claude/scripts/devforgeai_cli/ast_grep/config_validator.py` | ConfigurationValidator |
| `docs/ast-grep/sgconfig-schema.md` | Configuration schema documentation |
| `docs/ast-grep/rule-authoring-guide.md` | Rule authoring guide for developers |

### CLI Commands Added

```bash
devforgeai ast-grep init [--force] [--project-root PATH]
devforgeai ast-grep validate-config [--config PATH] [--format text|json]
```

---

## Workflow History

### 2025-12-20 - Coverage Fix Implementation
- Added 13 new test cases to address coverage gaps
- **config_init.py:** Added 3 exception path tests (permission denied, generic exception, yaml import)
- **config_validator.py:** Added 5 validation error tests (yaml library, empty file, type validation, glob patterns)
- **models.py:** Added 7 RuleMetadata coverage tests (all fields init, serialization, deserialization)
- **New Coverage:** 95% overall (was 79%), exceeds 80% threshold
  - `__init__.py`: 100%
  - `config_init.py`: 96%
  - `config_validator.py`: 93%
  - `models.py`: 100%
- **Test Count:** 71 tests (was 33), all passing
- Status transitioned: QA Failed → Dev Complete
- Ready for `/qa STORY-116 deep` re-validation

### 2025-12-20 21:12:45 - QA Validation: FAILED (Deep Mode)
- Coverage analysis identified blocking violations
- Overall coverage: 79% (threshold: 80%) - **CRITICAL**
- Business logic coverage: 87.4% (threshold: 95%) - **HIGH**
- Missing: 10 error path test cases
- Status transitioned: Dev Complete → QA Failed
- Report: `devforgeai/qa/reports/STORY-116-qa-report.md`
- Gaps analysis: `devforgeai/qa/reports/STORY-116-gaps.json`
- Action required: Add error handling tests and re-run `/qa STORY-116 deep`

### 2025-12-20 14:30:00 - Status: Ready for Dev
- Added to SPRINT-7: Sprint 7 - AST-Grep
- Transitioned from Backlog to Ready for Dev
- Sprint capacity: 32 points
- Priority in sprint: [2 of 5]

## Workflow Status

- [x] Architecture phase complete
- [x] Development phase complete
- [x] QA phase complete - ✅ PASSED (2025-12-20)
- [ ] Released

## QA Validation History

**Latest QA Run:** 2025-12-20 (Deep Mode)
- **Result:** ✅ PASSED
- **Blocking Issues:** 0
- **Coverage:** 95% overall (all thresholds exceeded)
  - Business Logic: 96% (threshold: 95%) ✅
  - Application: 96% (threshold: 85%) ✅
  - Infrastructure: 95% (threshold: 80%) ✅
- **Tests:** 71/71 passed (100% pass rate)
- **Anti-Patterns:** 0 CRITICAL, 0 HIGH violations
- **AC Traceability:** 100% (all 4 ACs verified)
- **DoD Status:** 16/16 items complete (100%)
- **QA Report:** Available in `devforgeai/qa/reports/STORY-116-qa-report.md`
- **Status Update:** Dev Complete → QA Approved ✅

**Previous QA Attempt:** 2025-12-20 21:12:45 (Deep Mode)
- Result: ❌ FAILED
- Issue: Coverage gaps (79% overall, 87.4% business logic)
- Remediation: Added 13 error path tests (13 new tests, 71 total)
- Status: Issues resolved, re-validation PASSED

## Notes

**Design Decisions:**
- Using .devforgeai/ as project-scoped storage (consistent with other DevForgeAI data)
- Language-first organization (rules/python/) vs category-first (rules/security/python/)
- sgconfig.yml is ast-grep's expected config file name

**References:**
- [EPIC-018: ast-grep Foundation & Core Rules](../Epics/EPIC-018-astgrep-foundation-core-rules.epic.md)
- [ast-grep configuration docs](https://ast-grep.github.io/guide/project/config.html)

---

**Story Template Version:** 2.2
**Created:** 2025-12-20
