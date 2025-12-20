---
id: STORY-115
title: CLI Validator Foundation - ast-grep Integration
epic: EPIC-018
sprint: SPRINT-7
status: Ready for Dev
points: 8
depends_on: []
priority: Medium
assigned_to: Unassigned
created: 2025-12-20
format_version: "2.2"
---

# Story: CLI Validator Foundation - ast-grep Integration

## Description

**As a** DevForgeAI user,
**I want** the CLI to automatically detect and manage ast-grep installation,
**so that** I can use semantic code analysis without manual setup or workflow interruption.

**Context:** This story implements Feature 1 of EPIC-018 (ast-grep Foundation & Core Rules). It creates the foundation CLI validator that wraps ast-grep, handles installation detection, and provides graceful fallback to grep-based analysis when ast-grep is unavailable.

## Acceptance Criteria

### AC#1: Auto-Install via PyPI

**Given** ast-grep is not installed on the system,
**When** a user runs `devforgeai ast-grep scan`,
**Then** the CLI:
1. Detects ast-grep is missing
2. Prompts user with installation options
3. If user confirms, installs `ast-grep-cli` via pip
4. Verifies installation succeeded
5. Proceeds with the scan

---

### AC#2: Interactive Missing Dependency Prompt

**Given** ast-grep is not installed and cannot be auto-installed,
**When** the user attempts to use ast-grep features,
**Then** the CLI displays an interactive prompt with options:
1. "Install now (pip install ast-grep-cli)" - attempts installation
2. "Use fallback (grep-based analysis)" - continues with reduced accuracy
3. "Skip" - exits gracefully with informational message

---

### AC#3: Graceful Fallback to Grep

**Given** ast-grep is unavailable (not installed or installation failed),
**When** the user selects "Use fallback" or configures fallback mode,
**Then** the CLI:
1. Logs a warning about reduced accuracy (expected 60-75% vs 90-95%)
2. Executes grep-based pattern matching instead
3. Returns results in the same format as ast-grep would
4. Marks results with `analysis_method: "grep-fallback"` in output

---

### AC#4: Version Compatibility Check

**Given** ast-grep is installed,
**When** the CLI initializes,
**Then** it verifies:
1. Version is >=0.40.0 and <1.0.0 (per EPIC-018 requirements)
2. If version incompatible, warns user and offers upgrade
3. Logs the detected version for debugging

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service"
      name: "AstGrepValidator"
      file_path: "src/claude/scripts/devforgeai_cli/validators/ast_grep_validator.py"
      interface: "BaseValidator"
      lifecycle: "Singleton"
      dependencies:
        - "subprocess"
        - "shutil"
        - "pip"
      requirements:
        - id: "SVC-001"
          description: "Detect ast-grep installation via shutil.which() or subprocess call"
          testable: true
          test_requirement: "Test: Mock subprocess to simulate installed/missing ast-grep"
          priority: "Critical"
        - id: "SVC-002"
          description: "Install ast-grep via pip programmatically"
          testable: true
          test_requirement: "Test: Mock pip install success/failure scenarios"
          priority: "High"
        - id: "SVC-003"
          description: "Parse ast-grep version output and validate compatibility"
          testable: true
          test_requirement: "Test: Version strings 0.39.0, 0.40.0, 0.99.0, 1.0.0"
          priority: "High"

    - type: "Service"
      name: "GrepFallbackAnalyzer"
      file_path: "src/claude/scripts/devforgeai_cli/validators/grep_fallback.py"
      interface: "IAnalyzer"
      lifecycle: "Singleton"
      dependencies:
        - "re"
        - "subprocess"
      requirements:
        - id: "SVC-004"
          description: "Execute grep-based pattern matching for security rules"
          testable: true
          test_requirement: "Test: Detect SQL injection pattern in test fixture"
          priority: "Critical"
        - id: "SVC-005"
          description: "Format grep results to match ast-grep output schema"
          testable: true
          test_requirement: "Test: Compare output format against ast-grep schema"
          priority: "High"

    - type: "Configuration"
      name: "ast-grep-config"
      file_path: ".devforgeai/ast-grep/config.yaml"
      required_keys:
        - key: "fallback_mode"
          type: "bool"
          example: "false"
          required: false
          default: "false"
          validation: "Boolean only"
          test_requirement: "Test: Load config with fallback_mode true/false"
        - key: "min_version"
          type: "string"
          example: "0.40.0"
          required: false
          default: "0.40.0"
          validation: "Semantic version format"
          test_requirement: "Test: Parse version constraint from config"

    - type: "API"
      name: "ast-grep-scan"
      endpoint: "devforgeai ast-grep scan"
      method: "CLI"
      authentication:
        required: false
      request:
        content_type: "CLI arguments"
        schema:
          path:
            type: "string"
            required: true
            validation: "Valid directory path"
          category:
            type: "string"
            required: false
            validation: "One of: security, anti-patterns, complexity, architecture"
          language:
            type: "string"
            required: false
            validation: "One of: python, csharp, typescript, javascript"
          format:
            type: "string"
            required: false
            validation: "One of: text, json, markdown"
      response:
        success:
          status_code: 0
          schema:
            violations: "array"
            analysis_method: "string"
            version: "string"
        errors:
          - status_code: 1
            condition: "ast-grep not installed and user declined install"
            schema:
              error: "string"
              message: "ast-grep not available"
      requirements:
        - id: "API-001"
          description: "Parse CLI arguments and route to appropriate handler"
          testable: true
          test_requirement: "Test: CLI invocation with various argument combinations"
          priority: "Critical"

  business_rules:
    - id: "BR-001"
      rule: "ast-grep version must be >=0.40.0 and <1.0.0"
      trigger: "On first use of ast-grep features"
      validation: "Parse version output and compare semantically"
      error_handling: "Warn user and offer upgrade if incompatible"
      test_requirement: "Test: Boundary versions 0.39.9, 0.40.0, 0.99.9, 1.0.0"
      priority: "High"
    - id: "BR-002"
      rule: "Fallback mode must produce results in identical schema to ast-grep"
      trigger: "When grep fallback is active"
      validation: "JSON schema validation of output"
      error_handling: "Log warning if schema drift detected"
      test_requirement: "Test: Validate grep output against ast-grep JSON schema"
      priority: "Critical"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Installation detection must complete in <500ms"
      metric: "p95 latency <500ms for shutil.which() or subprocess check"
      test_requirement: "Test: Measure detection time across 100 runs"
      priority: "Medium"
    - id: "NFR-002"
      category: "Reliability"
      requirement: "Fallback must work on all supported platforms (Linux, macOS, Windows/WSL)"
      metric: "100% of grep commands execute successfully on all platforms"
      test_requirement: "Test: Run fallback on Linux, macOS, Windows fixtures"
      priority: "High"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- Installation detection: <500ms (p95)
- Fallback analysis: <5s for 100 files

**Throughput:**
- Support analysis of 1000+ files per scan

---

### Security

**Authentication:** None required (local CLI tool)

**Data Protection:**
- No credentials stored
- No network calls except pip install (user-initiated)

---

### Reliability

**Error Handling:**
- Graceful fallback on ast-grep failure
- Clear error messages for all failure modes
- No crashes on missing dependencies

**Platform Support:**
- Linux (full support)
- macOS (full support)
- Windows/WSL (full support)

---

## Dependencies

### Prerequisite Stories

None - this is the foundation story for EPIC-018.

### Technology Dependencies

- [ ] **Package:** ast-grep-cli >=0.40.0,<1.0.0
  - **Purpose:** Semantic code analysis engine
  - **Approved:** Pending (requires addition to dependencies.md)

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for business logic

**Test Scenarios:**
1. **Happy Path:** ast-grep installed, version compatible, scan succeeds
2. **Edge Cases:**
   - ast-grep missing, user accepts install
   - ast-grep missing, user selects fallback
   - ast-grep version too old
   - ast-grep version too new (>=1.0.0)
3. **Error Cases:**
   - pip install fails
   - Invalid path provided
   - Permission denied on target directory

---

### Integration Tests

**Coverage Target:** 85%

**Test Scenarios:**
1. End-to-end CLI invocation with real ast-grep
2. Fallback mode produces valid output
3. Version check against real installation

---

## Acceptance Criteria Verification Checklist

### AC#1: Auto-Install via PyPI

- [ ] Detection logic implemented - **Phase:** 03 - **Evidence:** ast_grep_validator.py
- [ ] Install prompt displays - **Phase:** 03 - **Evidence:** test_install_prompt.py
- [ ] pip install executes - **Phase:** 03 - **Evidence:** test_pip_install.py
- [ ] Post-install verification - **Phase:** 03 - **Evidence:** test_verify_install.py

### AC#2: Interactive Missing Dependency Prompt

- [ ] Three options displayed - **Phase:** 03 - **Evidence:** test_prompt_options.py
- [ ] Install option works - **Phase:** 03 - **Evidence:** test_install_option.py
- [ ] Fallback option works - **Phase:** 03 - **Evidence:** test_fallback_option.py
- [ ] Skip option works - **Phase:** 03 - **Evidence:** test_skip_option.py

### AC#3: Graceful Fallback to Grep

- [ ] Warning logged - **Phase:** 03 - **Evidence:** test_fallback_warning.py
- [ ] Grep patterns execute - **Phase:** 03 - **Evidence:** test_grep_execution.py
- [ ] Output format matches - **Phase:** 03 - **Evidence:** test_output_format.py
- [ ] analysis_method field set - **Phase:** 03 - **Evidence:** test_analysis_method.py

### AC#4: Version Compatibility Check

- [ ] Version parsing works - **Phase:** 03 - **Evidence:** test_version_parsing.py
- [ ] Boundary versions handled - **Phase:** 03 - **Evidence:** test_version_boundaries.py
- [ ] Upgrade prompt displayed - **Phase:** 03 - **Evidence:** test_upgrade_prompt.py

---

**Checklist Progress:** 0/15 items complete (0%)

---

## Definition of Done

### Implementation
- [ ] AstGrepValidator class created with detection logic
- [ ] GrepFallbackAnalyzer class created with pattern matching
- [ ] CLI command `devforgeai ast-grep scan` registered
- [ ] Configuration file schema defined
- [ ] Interactive prompts implemented with AskUserQuestion pattern

### Quality
- [ ] All 4 acceptance criteria have passing tests
- [ ] Edge cases covered (version boundaries, install failures, fallback)
- [ ] Input validation enforced (path, category, language, format)
- [ ] Code coverage >95% for validators module

### Testing
- [ ] Unit tests for AstGrepValidator (10+ test cases)
- [ ] Unit tests for GrepFallbackAnalyzer (5+ test cases)
- [ ] Integration tests for CLI invocation (3+ scenarios)
- [ ] Cross-platform tests (Linux, macOS, Windows/WSL)

### Documentation
- [ ] CLI help text updated with new command
- [ ] README updated with ast-grep usage
- [ ] dependencies.md updated with ast-grep-cli

---

## Workflow History

### 2025-12-20 14:30:00 - Status: Ready for Dev
- Added to SPRINT-7: Sprint 7 - AST-Grep
- Transitioned from Backlog to Ready for Dev
- Sprint capacity: 32 points
- Priority in sprint: [1 of 5]

## Workflow Status

- [ ] Architecture phase complete
- [ ] Development phase complete
- [ ] QA phase complete
- [ ] Released

## Notes

**Design Decisions:**
- Using pip for installation (PyPI) as primary method per EPIC-018 requirements
- Fallback to grep ensures workflow continues even without ast-grep
- Version pinning to <1.0.0 protects against breaking API changes

**Open Questions:**
- [ ] Should fallback mode be configurable globally or per-scan? - **Owner:** Architecture - **Due:** Before implementation

**References:**
- [EPIC-018: ast-grep Foundation & Core Rules](../Epics/EPIC-018-astgrep-foundation-core-rules.epic.md)
- [ast-grep documentation](https://ast-grep.github.io/)

---

**Story Template Version:** 2.2
**Created:** 2025-12-20
