---
id: STORY-068
title: Global CLI Entry Point
epic: EPIC-012
sprint: Backlog
status: Backlog
points: 5
priority: Medium
assigned_to: TBD
created: 2025-11-25
format_version: "2.1"
---

# Story: Global CLI Entry Point

## Description

**As a** DevForgeAI user installing the framework via npm,
**I want** a global `devforgeai` CLI command available in my PATH,
**so that** I can run framework commands from any directory without prefixing with `npx` or navigating to the installation directory.

## Acceptance Criteria

### AC#1: Global command availability after npm installation

**Given** a user installs DevForgeAI globally via `npm install -g devforgeai`
**When** the installation completes successfully
**Then** the `devforgeai` command is available in the system PATH and can be executed from any directory

---

### AC#2: Install subcommand routes to installer entry point

**Given** the `devforgeai` command is available globally
**When** a user runs `devforgeai install /path/to/project`
**Then** the command routes to the Python installer entry point with the provided path argument

---

### AC#3: Help flag displays usage information

**Given** the `devforgeai` command is available globally
**When** a user runs `devforgeai --help` or `devforgeai -h`
**Then** the command displays:
- Usage syntax: `devforgeai [command] [options]`
- Available commands: `install`, `--version`, `--help`
- Command descriptions and examples
- Exit code 0

---

### AC#4: Version flag displays current package version

**Given** the `devforgeai` command is available globally
**When** a user runs `devforgeai --version` or `devforgeai -v`
**Then** the command displays the current package version matching package.json and exits with code 0

---

### AC#5: Cross-platform compatibility (Windows)

**Given** DevForgeAI is installed globally on Windows 10/11
**When** a user runs `devforgeai --version` in PowerShell, CMD, or Git Bash
**Then** the command executes successfully without errors

---

### AC#6: Cross-platform compatibility (macOS)

**Given** DevForgeAI is installed globally on macOS
**When** a user runs `devforgeai --version` in Bash or Zsh terminal
**Then** the command executes successfully without errors

---

### AC#7: Cross-platform compatibility (Linux)

**Given** DevForgeAI is installed globally on Linux
**When** a user runs `devforgeai --version` in Bash terminal
**Then** the command executes successfully without errors

---

### AC#8: Error handling for invalid commands

**Given** the `devforgeai` command is available globally
**When** a user runs `devforgeai invalid-command`
**Then** the CLI displays error message with suggestion to run `devforgeai --help` and exits with non-zero code

---

### AC#9: Python runtime detection and error reporting

**Given** the `devforgeai install` command requires Python 3.8+
**When** a user runs `devforgeai install` without Python installed
**Then** the CLI displays clear error message "Python 3.8+ required" with exit code 1

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service"
      name: "CLIEntryPoint"
      file_path: "bin/devforgeai.js"
      requirements:
        - id: "SVC-001"
          description: "CLI starts with Node.js shebang"
          testable: true
          test_requirement: "Test: First line is #!/usr/bin/env node"
          priority: "Critical"
        - id: "SVC-002"
          description: "CLI parses --help flag"
          testable: true
          test_requirement: "Test: devforgeai --help exits 0 with usage text"
          priority: "Critical"
        - id: "SVC-003"
          description: "CLI parses --version flag"
          testable: true
          test_requirement: "Test: devforgeai --version outputs version from package.json"
          priority: "Critical"
        - id: "SVC-004"
          description: "CLI routes install command to Python installer"
          testable: true
          test_requirement: "Test: devforgeai install spawns python3 installer/install.py"
          priority: "Critical"
        - id: "SVC-005"
          description: "CLI detects Python availability"
          testable: true
          test_requirement: "Test: Missing Python shows clear error message"
          priority: "High"
        - id: "SVC-006"
          description: "CLI handles invalid commands gracefully"
          testable: true
          test_requirement: "Test: Invalid command shows error with --help suggestion"
          priority: "High"

    - type: "Configuration"
      name: "PackageBinEntry"
      file_path: "package.json"
      requirements:
        - id: "CONF-001"
          description: "bin field points to CLI entry point"
          testable: true
          test_requirement: "Test: package.json bin.devforgeai = bin/devforgeai.js"
          priority: "Critical"

  business_rules:
    - id: "BR-001"
      rule: "Valid commands: install, --help, -h, --version, -v"
      test_requirement: "Test: Only valid commands accepted, others rejected"
    - id: "BR-002"
      rule: "Exit code 0 for success, non-zero for errors"
      test_requirement: "Test: Verify exit codes for success and failure cases"
    - id: "BR-003"
      rule: "Python version must be 3.8+"
      test_requirement: "Test: Python 3.7 rejected, 3.8+ accepted"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "CLI startup time"
      metric: "< 500ms for --help/--version"
      test_requirement: "Test: time devforgeai --version < 0.5s"
    - id: "NFR-002"
      category: "Security"
      requirement: "No hardcoded credentials"
      metric: "Zero credentials in CLI source"
      test_requirement: "Test: grep for API_KEY/SECRET/TOKEN returns 0"
    - id: "NFR-003"
      category: "Reliability"
      requirement: "Cross-platform compatibility"
      metric: "Works on Windows, macOS, Linux"
      test_requirement: "Test: CI matrix tests all platforms"
    - id: "NFR-004"
      category: "Maintainability"
      requirement: "Single source of truth for version"
      metric: "Version read from package.json only"
      test_requirement: "Test: No hardcoded version strings in code"
```

---

## Non-Functional Requirements (NFRs)

### Performance
- CLI startup time: < 500ms for --help/--version
- Command routing overhead: < 50ms to Python subprocess

### Security
- No hardcoded credentials
- Path arguments sanitized to prevent injection

### Reliability
- 100% functional on Windows 10/11, macOS 11+, Ubuntu 20.04+
- Graceful degradation: Missing Python shows actionable error

---

## Edge Cases

1. **npm local installation (not global):** User must use `npx devforgeai` - display helpful message
2. **Multiple Python versions:** Detect correct Python 3.8+ executable
3. **PATH conflicts:** Warn if existing `devforgeai` found in PATH
4. **Insufficient permissions:** Clear error message for EACCES during global install
5. **Windows long path issues:** Warn if path > 200 characters

---

## Definition of Done

### Implementation
- [ ] bin/devforgeai.js CLI entry point created
- [ ] --help flag implemented with usage text
- [ ] --version flag reads from package.json
- [ ] install command routes to Python installer
- [ ] Python detection with clear error message
- [ ] Invalid command handling with suggestions

### Quality
- [ ] All 9 acceptance criteria have passing tests
- [ ] Edge cases covered
- [ ] Cross-platform testing (Windows, macOS, Linux)

### Testing
- [ ] Unit tests for argument parsing
- [ ] Unit tests for Python detection
- [ ] Integration tests on all platforms

### Documentation
- [ ] --help text complete and accurate
- [ ] README.md CLI usage section

---

## Workflow Status

- [ ] Architecture phase complete
- [ ] Development phase complete
- [ ] QA phase complete
- [ ] Released

## Notes

**Design Decisions:**
- Pure JavaScript CLI wrapper (no native dependencies)
- Delegate to Python installer (reuse existing code)
- npm auto-generates platform shims

**Dependencies:**
- STORY-066: NPM Package Creation & Structure (provides package.json bin field)

---

**Story Template Version:** 2.1
**Last Updated:** 2025-11-25
