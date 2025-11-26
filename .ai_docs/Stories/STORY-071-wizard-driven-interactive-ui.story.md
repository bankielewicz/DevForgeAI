---
id: STORY-071
title: Wizard-Driven Interactive UI
epic: EPIC-013
sprint: Sprint-4
status: Backlog
points: 10
priority: Medium
assigned_to: TBD
created: 2025-11-25
format_version: "2.1"
---

# Story: Wizard-Driven Interactive UI

## Description

**As a** developer installing DevForgeAI on a new project,
**I want** an interactive wizard with visual feedback and clear prompts,
**so that** I can confidently configure installation options without reading documentation and recover from errors immediately.

## Acceptance Criteria

Define testable, specific conditions that must be met for story completion. Use Given/When/Then format for clarity.

### AC#1: Step-by-step wizard workflow

**Given** a developer runs `devforgeai install` without flags
**When** the installation wizard starts
**Then** the wizard displays sequential prompts for:
- Target directory (with default: current directory)
- Installation mode (minimal, standard, full)
- CLAUDE.md merge strategy (preserve-user, merge-smart, replace)
**And** each prompt shows current value, available options, and keyboard navigation hints
**And** user can navigate with arrow keys and confirm with Enter

---

### AC#2: Progress indicators during operations

**Given** the wizard is executing a long-running operation (file copying, validation)
**When** the operation duration exceeds 200ms
**Then** the terminal displays an animated spinner (Ora) with operation description
**And** for operations with known total (multiple files), displays a progress bar (CLI-Progress) showing percentage complete
**And** spinner text updates to reflect sub-operation status (e.g., "Copying src/ [23/50 files]")

---

### AC#3: Color-coded output for status

**Given** the wizard is displaying output messages
**When** operations complete or errors occur
**Then** the terminal uses Chalk colors:
- Green for success messages (e.g., "✓ Installation complete")
- Yellow for warnings (e.g., "⚠ Existing CLAUDE.md found")
- Red for errors (e.g., "✗ Target directory not writable")
- Blue for informational prompts (e.g., "? Select installation mode:")
**And** color codes are consistent across all wizard screens

---

### AC#4: Confirmation prompts for destructive actions

**Given** the wizard detects an operation that will modify/delete existing files
**When** the user attempts to proceed (overwrite CLAUDE.md, uninstall, replace mode)
**Then** the wizard displays a confirmation prompt with:
- Clear description of what will be affected (file paths, line count)
- Yes/No options (default: No for destructive actions)
- Warning color (yellow or red)
**And** "No" cancels the operation and returns to previous step

---

### AC#5: Non-interactive mode with --yes flag

**Given** a CI/CD pipeline runs `devforgeai install --yes`
**When** the installer encounters prompts
**Then** all prompts are automatically answered with defaults:
- Target directory: current directory
- Installation mode: standard
- Merge strategy: merge-smart
- Confirmations: skip (proceed with operation)
**And** no user input is required (process completes without blocking)
**And** exit code is 0 on success, non-zero on failure

---

### AC#6: Quiet mode with --quiet flag

**Given** a user runs `devforgeai install --quiet`
**When** the wizard executes
**Then** the terminal suppresses:
- Spinner animations
- Progress bars
- Informational messages
- Success messages
**And** displays only:
- Error messages (to stderr)
- Confirmation prompts (if --yes not set)
**And** final status message (success or failure)

---

### AC#7: Keyboard interrupt handling

**Given** the wizard is running and displaying a prompt or spinner
**When** the user presses Ctrl+C
**Then** the wizard:
- Stops current operation gracefully (no partial writes)
- Displays cancellation message: "✗ Installation cancelled by user"
- Cleans up temporary files (if any)
- Exits with code 130 (standard SIGINT code)

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    # CLI Entry Point
    - type: "Service"
      name: "InstallWizard"
      file_path: "src/cli/wizard/install-wizard.js"
      interface: "IInstallWizard"
      lifecycle: "Singleton"
      dependencies:
        - "IPromptService"
        - "IProgressService"
        - "IOutputFormatter"
        - "IInstaller"
      requirements:
        - id: "SVC-001"
          description: "Orchestrate wizard flow: prompts → validation → installation"
          testable: true
          test_requirement: "Test: Mock prompts return values, verify installation called with correct config"
          priority: "Critical"
        - id: "SVC-002"
          description: "Handle --yes flag to skip interactive prompts"
          testable: true
          test_requirement: "Test: With --yes flag, verify zero prompts displayed, defaults used"
          priority: "Critical"
        - id: "SVC-003"
          description: "Handle --quiet flag to suppress non-error output"
          testable: true
          test_requirement: "Test: With --quiet flag, verify only stderr output for errors"
          priority: "High"

    # Prompt Service
    - type: "Service"
      name: "PromptService"
      file_path: "src/cli/wizard/prompt-service.js"
      interface: "IPromptService"
      lifecycle: "Singleton"
      dependencies:
        - "inquirer"
        - "IOutputFormatter"
      requirements:
        - id: "SVC-004"
          description: "Display target directory prompt with default (current directory)"
          testable: true
          test_requirement: "Test: Verify prompt text, default value, and validation message"
          priority: "Critical"
        - id: "SVC-005"
          description: "Display installation mode prompt (minimal, standard, full)"
          testable: true
          test_requirement: "Test: Verify 3 options displayed, default is 'standard'"
          priority: "Critical"
        - id: "SVC-006"
          description: "Display merge strategy prompt (preserve-user, merge-smart, replace)"
          testable: true
          test_requirement: "Test: Verify 3 options displayed, default is 'merge-smart'"
          priority: "Critical"
        - id: "SVC-007"
          description: "Display confirmation prompt for destructive actions"
          testable: true
          test_requirement: "Test: Verify Yes/No options, default is No, warning color applied"
          priority: "High"
        - id: "SVC-008"
          description: "Skip prompts when TTY not available"
          testable: true
          test_requirement: "Test: Mock process.stdout.isTTY=false, verify error message"
          priority: "High"

    # Progress Service
    - type: "Service"
      name: "ProgressService"
      file_path: "src/cli/wizard/progress-service.js"
      interface: "IProgressService"
      lifecycle: "Singleton"
      dependencies:
        - "ora"
        - "cli-progress"
      requirements:
        - id: "SVC-009"
          description: "Display spinner for indeterminate operations (>200ms)"
          testable: true
          test_requirement: "Test: Verify spinner starts after 200ms threshold"
          priority: "High"
        - id: "SVC-010"
          description: "Display progress bar for determinate operations (file counts)"
          testable: true
          test_requirement: "Test: Verify progress bar shows percentage, updates on increment"
          priority: "High"
        - id: "SVC-011"
          description: "Update spinner text with sub-operation status"
          testable: true
          test_requirement: "Test: Verify text updates to 'Copying src/ [23/50 files]'"
          priority: "Medium"
        - id: "SVC-012"
          description: "Disable spinners/progress when --quiet flag set"
          testable: true
          test_requirement: "Test: With --quiet, verify no spinner/progress bar output"
          priority: "High"

    # Output Formatter
    - type: "Service"
      name: "OutputFormatter"
      file_path: "src/cli/wizard/output-formatter.js"
      interface: "IOutputFormatter"
      lifecycle: "Singleton"
      dependencies:
        - "chalk"
      requirements:
        - id: "SVC-013"
          description: "Format success messages with green color and ✓ symbol"
          testable: true
          test_requirement: "Test: Verify output contains chalk.green and '✓'"
          priority: "High"
        - id: "SVC-014"
          description: "Format warning messages with yellow color and ⚠ symbol"
          testable: true
          test_requirement: "Test: Verify output contains chalk.yellow and '⚠'"
          priority: "High"
        - id: "SVC-015"
          description: "Format error messages with red color and ✗ symbol"
          testable: true
          test_requirement: "Test: Verify output contains chalk.red and '✗'"
          priority: "High"
        - id: "SVC-016"
          description: "Format info prompts with blue color and ? symbol"
          testable: true
          test_requirement: "Test: Verify output contains chalk.blue and '?'"
          priority: "Medium"
        - id: "SVC-017"
          description: "Detect NO_COLOR env var and disable colors"
          testable: true
          test_requirement: "Test: With NO_COLOR set, verify no ANSI codes in output"
          priority: "High"
        - id: "SVC-018"
          description: "Fallback to ASCII symbols when Unicode not supported"
          testable: true
          test_requirement: "Test: With TERM=dumb, verify [OK], [ERROR], [WARN] used"
          priority: "Medium"

    # Signal Handler
    - type: "Service"
      name: "SignalHandler"
      file_path: "src/cli/wizard/signal-handler.js"
      interface: "ISignalHandler"
      lifecycle: "Singleton"
      dependencies:
        - "IOutputFormatter"
        - "ICleanupService"
      requirements:
        - id: "SVC-019"
          description: "Handle SIGINT (Ctrl+C) gracefully"
          testable: true
          test_requirement: "Test: Emit SIGINT, verify cleanup called, exit code 130"
          priority: "Critical"
        - id: "SVC-020"
          description: "Stop current operation without partial writes"
          testable: true
          test_requirement: "Test: Interrupt during file copy, verify no partial files"
          priority: "Critical"
        - id: "SVC-021"
          description: "Display cancellation message before exit"
          testable: true
          test_requirement: "Test: Verify '✗ Installation cancelled by user' displayed"
          priority: "High"

    # Configuration
    - type: "Configuration"
      name: "WizardConfig"
      file_path: "src/cli/wizard/config.js"
      required_keys:
        - key: "defaults.targetDirectory"
          type: "string"
          example: "."
          required: true
          default: "."
          validation: "Valid filesystem path"
          test_requirement: "Test: Verify default is current directory"
        - key: "defaults.installationMode"
          type: "string"
          example: "standard"
          required: true
          default: "standard"
          validation: "One of: minimal, standard, full"
          test_requirement: "Test: Verify default is 'standard'"
        - key: "defaults.mergeStrategy"
          type: "string"
          example: "merge-smart"
          required: true
          default: "merge-smart"
          validation: "One of: preserve-user, merge-smart, replace"
          test_requirement: "Test: Verify default is 'merge-smart'"
        - key: "thresholds.spinnerDelayMs"
          type: "int"
          example: 200
          required: true
          default: 200
          validation: "Positive integer"
          test_requirement: "Test: Verify spinner starts after 200ms"
        - key: "exitCodes.success"
          type: "int"
          example: 0
          required: true
          default: 0
          validation: "Integer 0"
          test_requirement: "Test: Verify success exits with 0"
        - key: "exitCodes.sigint"
          type: "int"
          example: 130
          required: true
          default: 130
          validation: "Integer 130 (128 + SIGINT)"
          test_requirement: "Test: Verify Ctrl+C exits with 130"

    # DataModel for Installation Config
    - type: "DataModel"
      name: "InstallationConfig"
      table: "N/A (in-memory)"
      purpose: "Stores user-selected installation configuration"
      fields:
        - name: "targetDirectory"
          type: "String"
          constraints: "Required, valid path"
          description: "Target directory for installation"
          test_requirement: "Test: Validate path exists or parent exists"
        - name: "installationMode"
          type: "Enum"
          constraints: "Required, one of: minimal, standard, full"
          description: "Installation scope"
          test_requirement: "Test: Validate against allowed values"
        - name: "mergeStrategy"
          type: "Enum"
          constraints: "Required, one of: preserve-user, merge-smart, replace"
          description: "CLAUDE.md merge strategy"
          test_requirement: "Test: Validate against allowed values"
        - name: "nonInteractive"
          type: "Boolean"
          constraints: "Optional, default: false"
          description: "Whether --yes flag was used"
          test_requirement: "Test: Verify defaults to false"
        - name: "quiet"
          type: "Boolean"
          constraints: "Optional, default: false"
          description: "Whether --quiet flag was used"
          test_requirement: "Test: Verify defaults to false"

  business_rules:
    - id: "BR-001"
      rule: "Non-TTY environments require --yes flag for installation"
      trigger: "process.stdout.isTTY === false and --yes not set"
      validation: "Check TTY status on wizard start"
      error_handling: "Display error message and exit with code 1"
      test_requirement: "Test: Mock non-TTY, verify error without --yes"
      priority: "Critical"

    - id: "BR-002"
      rule: "Destructive actions require explicit confirmation (default: No)"
      trigger: "User attempts overwrite, uninstall, or replace operations"
      validation: "Display Yes/No prompt with default No"
      error_handling: "Cancel operation and return to previous step on No"
      test_requirement: "Test: Verify default is No, pressing Enter cancels"
      priority: "Critical"

    - id: "BR-003"
      rule: "--yes flag overrides all prompts with default values"
      trigger: "--yes flag present in CLI arguments"
      validation: "Skip all prompts, use default values"
      error_handling: "Log defaults used, proceed with installation"
      test_requirement: "Test: With --yes, verify all defaults applied"
      priority: "Critical"

    - id: "BR-004"
      rule: "--quiet flag suppresses non-error output"
      trigger: "--quiet flag present in CLI arguments"
      validation: "Route stdout through quiet filter"
      error_handling: "Only display errors to stderr"
      test_requirement: "Test: With --quiet, verify only stderr output"
      priority: "High"

    - id: "BR-005"
      rule: "Conflicting flags must be rejected before wizard starts"
      trigger: "--yes with --no-confirm, or --quiet with --verbose"
      validation: "Validate flag combinations in Commander.js"
      error_handling: "Display error message and exit with code 1"
      test_requirement: "Test: Pass conflicting flags, verify error exit"
      priority: "High"

    - id: "BR-006"
      rule: "CI=true environment variable auto-enables --yes and --quiet"
      trigger: "CI=true detected in environment"
      validation: "Apply flags unless explicitly overridden"
      error_handling: "Log that CI mode detected, flags applied"
      test_requirement: "Test: With CI=true, verify --yes --quiet behavior"
      priority: "Medium"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Prompt response time under 50ms (p95)"
      metric: "< 50ms from keypress to screen update"
      test_requirement: "Test: Measure keypress-to-update latency, assert < 50ms p95"
      priority: "High"

    - id: "NFR-002"
      category: "Performance"
      requirement: "Spinner animation at 60 FPS"
      metric: "16ms per frame minimum"
      test_requirement: "Test: Verify Ora spinner frame rate configuration"
      priority: "Medium"

    - id: "NFR-003"
      category: "Performance"
      requirement: "Wizard initialization under 200ms"
      metric: "< 200ms to first prompt"
      test_requirement: "Test: Measure time from command start to first prompt"
      priority: "High"

    - id: "NFR-004"
      category: "Performance"
      requirement: "Memory footprint under 50MB"
      metric: "process.memoryUsage().heapUsed < 50MB"
      test_requirement: "Test: Monitor heap during wizard execution"
      priority: "Medium"

    - id: "NFR-005"
      category: "Compatibility"
      requirement: "Support Windows Terminal, CMD, PowerShell, iTerm2, GNOME Terminal"
      metric: "All features functional on supported terminals"
      test_requirement: "Test: Run E2E tests on each terminal emulator"
      priority: "Critical"

    - id: "NFR-006"
      category: "Compatibility"
      requirement: "Support Node.js 18.x, 20.x, 22.x"
      metric: "Tests pass on all supported Node versions"
      test_requirement: "Test: CI matrix with Node 18, 20, 22"
      priority: "Critical"

    - id: "NFR-007"
      category: "Accessibility"
      requirement: "Keyboard-only navigation for all wizard operations"
      metric: "Zero mouse-only interactions"
      test_requirement: "Test: Complete wizard using only keyboard"
      priority: "High"

    - id: "NFR-008"
      category: "Reliability"
      requirement: "Atomic file operations with no partial writes on interruption"
      metric: "Zero partial files after SIGINT"
      test_requirement: "Test: Interrupt during file copy, verify no partial files"
      priority: "Critical"

    - id: "NFR-009"
      category: "Security"
      requirement: "No command injection via user input"
      metric: "All file operations use Node.js fs API (not child_process)"
      test_requirement: "Test: Pass malicious path input, verify fs API used"
      priority: "Critical"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- Prompt response: < 50ms (p95) from keypress to screen update
- Spinner animation: 60 FPS (16ms per frame)
- Progress bar update: < 100ms latency

**Startup:**
- Wizard initialization: < 200ms to first prompt

**Memory:**
- Memory footprint: < 50 MB heap used

---

### Security

**Input Validation:**
- Path traversal prevention: Reject paths containing `..`, `~`, environment variables
- No command injection: Use Node.js fs API, never shell commands
- No sensitive data logging: Redact directory paths in public logs

**Authentication:**
- N/A (local CLI tool)

---

### Scalability

**N/A** - This is a CLI tool, not a server application.

---

### Reliability

**Error Handling:**
- All file operations wrapped in try-catch
- User-friendly error messages (no stack traces)
- Detailed errors logged to `.devforgeai/logs/install-error-{timestamp}.log`

**Graceful Degradation:**
- If spinner library fails, fallback to text updates
- If Chalk fails, output plain text (no colors)
- If Unicode not supported, use ASCII fallbacks

**Atomic Operations:**
- File writes use temp file + rename
- No partial files on interruption

---

### Observability

**Logging:**
- Log level: INFO default, DEBUG with --verbose
- Log file: `.devforgeai/logs/install.log`
- Include timestamps and operation descriptions

**Metrics:**
- Installation duration
- Prompts displayed count
- Files copied count

---

## Dependencies

### Prerequisite Stories

- [ ] **EPIC-012 Stories:** NPM package structure must be in place
  - **Why:** Wizard is invoked via `devforgeai install` command
  - **Status:** Not Started

### External Dependencies

None - all dependencies are npm packages.

### Technology Dependencies

- [ ] **inquirer:** ^9.0.0
  - **Purpose:** Interactive prompts
  - **Approved:** Yes (per EPIC-013 architecture)
  - **Added to dependencies.md:** Pending

- [ ] **commander:** ^11.0.0
  - **Purpose:** CLI argument parsing
  - **Approved:** Yes (per EPIC-013 architecture)
  - **Added to dependencies.md:** Pending

- [ ] **ora:** ^6.0.0
  - **Purpose:** Spinner animations
  - **Approved:** Yes (per EPIC-013 architecture)
  - **Added to dependencies.md:** Pending

- [ ] **cli-progress:** ^3.0.0
  - **Purpose:** Progress bars
  - **Approved:** Yes (per EPIC-013 architecture)
  - **Added to dependencies.md:** Pending

- [ ] **chalk:** ^5.0.0
  - **Purpose:** Terminal colors
  - **Approved:** Yes (per EPIC-013 architecture)
  - **Added to dependencies.md:** Pending

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for wizard services

**Test Scenarios:**
1. **Happy Path:** User completes wizard with all prompts
2. **Edge Cases:**
   - Non-TTY environment
   - NO_COLOR environment variable
   - Ctrl+C interrupt
   - Invalid input to prompts
   - Conflicting flags
3. **Error Cases:**
   - Unwritable target directory
   - Invalid installation mode
   - Missing permissions

**Example Test Structure:**
```javascript
describe('InstallWizard', () => {
  it('should display prompts in sequence', async () => {
    // Arrange
    const mockPrompts = createMockPrompts();
    const wizard = new InstallWizard(mockPrompts);

    // Act
    const config = await wizard.run();

    // Assert
    expect(mockPrompts.targetDirectory).toHaveBeenCalled();
    expect(mockPrompts.installationMode).toHaveBeenCalled();
    expect(mockPrompts.mergeStrategy).toHaveBeenCalled();
  });

  it('should skip prompts with --yes flag', async () => {
    // Arrange
    const wizard = new InstallWizard({ yes: true });

    // Act
    const config = await wizard.run();

    // Assert
    expect(config.targetDirectory).toBe('.');
    expect(config.installationMode).toBe('standard');
    expect(config.mergeStrategy).toBe('merge-smart');
  });
});
```

---

### Integration Tests

**Coverage Target:** 85%+ for wizard flow

**Test Scenarios:**
1. **End-to-End Wizard Flow:** Complete installation with prompts
2. **Non-Interactive Flow:** --yes flag completes without prompts
3. **Signal Handling:** Ctrl+C cleanup

---

### E2E Tests

**Coverage Target:** Critical paths only

**Test Scenarios:**
1. **Interactive Installation:** Full wizard completion on real terminal
2. **CI/CD Mode:** --yes --quiet completes without interaction

---

## Edge Cases

1. **Non-TTY environment (piped output, CI/CD):** Detect `process.stdout.isTTY === false`. Automatically disable interactive prompts, spinners, and colors. Fallback to line-by-line text output. If --yes not set, display error: "Interactive prompts require TTY. Use --yes for non-interactive mode." Exit code 1.

2. **Terminal without color support (TERM=dumb, NO_COLOR env var):** Detect color support via `chalk.supportsColor`. Disable Chalk colors, use ASCII symbols instead: "✓" → "[OK]", "✗" → "[ERROR]", "⚠" → "[WARN]". Spinner uses simple text updates (no animations).

3. **Interrupted prompts mid-operation (Ctrl+C during file copy):** Inquirer.js emits 'SIGINT' event. Catch via `process.on('SIGINT')`. Stop file operations immediately. Remove partially written files. Restore original state if possible. Log interruption to `.devforgeai/logs/install-interrupted-{timestamp}.log`.

4. **Invalid user input to prompts (wrong directory format, unknown mode):** Inquirer.js validate function checks input. Display red error message below prompt. Keep prompt active (don't advance). Allow user to correct input. After 3 consecutive failures, offer to use default value.

5. **Conflicting flags (--yes and --no-confirm, --quiet and --verbose):** Commander.js pre-validates flag combinations. Display error: "Cannot use --yes and --no-confirm together." Exit code 1 before wizard starts.

6. **Windows terminal with limited Unicode support:** Detect Windows via `process.platform === 'win32'`. Use safe fallback symbols: spinner uses ASCII characters (|, /, -, \\). Progress bar uses simple characters ([=====>    ]).

7. **Terminal resized during progress bar display:** CLI-Progress handles terminal width changes. Progress bar reflows to new width. If terminal too narrow (<40 columns), switch to percentage-only display.

---

## Data Validation Rules

1. **Target directory validation:**
   - Must be valid filesystem path (absolute or relative)
   - Check directory exists OR parent exists (create if missing)
   - Check write permissions via `fs.access(dir, fs.constants.W_OK)`
   - Reject system directories: /, /usr, /etc, C:\Windows
   - Maximum path length: 260 characters (Windows MAX_PATH)

2. **Installation mode validation:**
   - Must be one of: "minimal", "standard", "full"
   - Case-insensitive comparison
   - Default: "standard"

3. **Merge strategy validation:**
   - Must be one of: "preserve-user", "merge-smart", "replace"
   - Only applicable if existing CLAUDE.md detected
   - Default: "merge-smart"

4. **Flag combination validation:**
   - `--yes` and `--no-confirm` are mutually exclusive
   - `--quiet` and `--verbose` are mutually exclusive
   - `--yes` with `--quiet` is valid

---

## Acceptance Criteria Verification Checklist

**Purpose:** Real-time progress tracking during TDD implementation.

### AC#1: Step-by-step wizard workflow

- [ ] Target directory prompt displayed - **Phase:** 2 - **Evidence:** prompt-service.test.js
- [ ] Installation mode prompt displayed - **Phase:** 2 - **Evidence:** prompt-service.test.js
- [ ] Merge strategy prompt displayed - **Phase:** 2 - **Evidence:** prompt-service.test.js
- [ ] Keyboard navigation works - **Phase:** 4 - **Evidence:** E2E test

### AC#2: Progress indicators during operations

- [ ] Spinner displays for >200ms operations - **Phase:** 2 - **Evidence:** progress-service.test.js
- [ ] Progress bar shows percentage - **Phase:** 2 - **Evidence:** progress-service.test.js
- [ ] Spinner text updates with status - **Phase:** 2 - **Evidence:** progress-service.test.js

### AC#3: Color-coded output for status

- [ ] Green for success messages - **Phase:** 2 - **Evidence:** output-formatter.test.js
- [ ] Yellow for warnings - **Phase:** 2 - **Evidence:** output-formatter.test.js
- [ ] Red for errors - **Phase:** 2 - **Evidence:** output-formatter.test.js
- [ ] Blue for info prompts - **Phase:** 2 - **Evidence:** output-formatter.test.js

### AC#4: Confirmation prompts for destructive actions

- [ ] Yes/No prompt displayed - **Phase:** 2 - **Evidence:** prompt-service.test.js
- [ ] Default is No - **Phase:** 2 - **Evidence:** prompt-service.test.js
- [ ] No cancels operation - **Phase:** 2 - **Evidence:** install-wizard.test.js

### AC#5: Non-interactive mode with --yes flag

- [ ] All prompts skipped - **Phase:** 2 - **Evidence:** install-wizard.test.js
- [ ] Default values used - **Phase:** 2 - **Evidence:** install-wizard.test.js
- [ ] Exit code 0 on success - **Phase:** 4 - **Evidence:** E2E test

### AC#6: Quiet mode with --quiet flag

- [ ] Spinners suppressed - **Phase:** 2 - **Evidence:** progress-service.test.js
- [ ] Only errors to stderr - **Phase:** 2 - **Evidence:** output-formatter.test.js

### AC#7: Keyboard interrupt handling

- [ ] SIGINT caught - **Phase:** 2 - **Evidence:** signal-handler.test.js
- [ ] Cleanup performed - **Phase:** 2 - **Evidence:** signal-handler.test.js
- [ ] Exit code 130 - **Phase:** 2 - **Evidence:** signal-handler.test.js

---

**Checklist Progress:** 0/22 items complete (0%)

---

## Definition of Done

### Implementation
- [ ] InstallWizard service orchestrates wizard flow
- [ ] PromptService displays all prompts with Inquirer.js
- [ ] ProgressService displays spinners (Ora) and progress bars (CLI-Progress)
- [ ] OutputFormatter applies Chalk colors consistently
- [ ] SignalHandler catches SIGINT and performs cleanup
- [ ] WizardConfig provides default values
- [ ] --yes flag skips all prompts
- [ ] --quiet flag suppresses non-error output

### Quality
- [ ] All 7 acceptance criteria have passing tests
- [ ] Edge cases covered (non-TTY, NO_COLOR, Ctrl+C, invalid input, conflicting flags)
- [ ] Data validation enforced for directory, mode, strategy
- [ ] NFRs met (50ms response, 200ms startup, 50MB memory)
- [ ] Code coverage >95% for wizard services

### Testing
- [ ] Unit tests for InstallWizard
- [ ] Unit tests for PromptService
- [ ] Unit tests for ProgressService
- [ ] Unit tests for OutputFormatter
- [ ] Unit tests for SignalHandler
- [ ] Integration tests for wizard flow
- [ ] E2E test: interactive installation
- [ ] E2E test: --yes --quiet mode

### Documentation
- [ ] JSDoc comments for all public methods
- [ ] README section for wizard usage
- [ ] --help output documented

---

## Workflow Status

- [ ] Architecture phase complete
- [ ] Development phase complete
- [ ] QA phase complete
- [ ] Released

## Notes

**Design Decisions:**
- Use Inquirer.js for prompts (industry standard, excellent TTY handling)
- Use Ora for spinners (lightweight, cross-platform)
- Use CLI-Progress for progress bars (customizable, reflows on resize)
- Use Chalk for colors (widely supported, respects NO_COLOR)

**Open Questions:**
- None

**Related ADRs:**
- ADR-004: NPM Package Distribution (parent architecture)

**References:**
- EPIC-013: Interactive Installer & Validation
- Inquirer.js documentation: https://github.com/SBoudrias/Inquirer.js
- Ora documentation: https://github.com/sindresorhus/ora

---

**Story Template Version:** 2.1
**Last Updated:** 2025-11-25
