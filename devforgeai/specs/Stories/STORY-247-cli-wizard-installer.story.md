---
id: STORY-247
title: CLI Wizard Installer
type: feature
epic: EPIC-039
sprint: Backlog
priority: Medium
points: 8
depends_on: ["STORY-235", "STORY-236", "STORY-237"]
status: Backlog
created: 2025-01-06
updated: 2025-01-06
format_version: "2.5"
---

# STORY-247: CLI Wizard Installer

## User Story

**As a** first-time DevForgeAI user,
**I want** a guided wizard installation with step-by-step prompts,
**So that** I can configure my project without reading documentation.

## Acceptance Criteria

### AC#1: Welcome Screen Display

**Given** the user runs `python -m installer wizard /path/to/project`
**When** the wizard launches
**Then** a welcome screen is displayed with:
- Framework name and version
- Brief description of what will be installed
- Estimated time to complete
**And** the user can press Enter to continue or Ctrl+C to cancel

### AC#2: License Agreement Step

**Given** the wizard has displayed the welcome screen
**When** the user presses Enter
**Then** the license agreement is displayed
**And** the user must type "accept" to continue
**And** typing anything else returns to the prompt
**And** the license text is scrollable for long licenses

### AC#3: Installation Path Selection

**Given** the user has accepted the license
**When** the path selection step is shown
**Then** the default path is displayed (from command line argument)
**And** the user can press Enter to accept the default
**Or** type a different path
**And** the path is validated for write permissions
**And** if invalid, an error is shown and user is re-prompted

### AC#4: Component Selection

**Given** the installation path has been selected
**When** the component selection step is shown
**Then** a checkbox list is displayed with:
- [x] Core Framework (.claude/, devforgeai/) - required, pre-checked
- [ ] CLI Tools (devforgeai command)
- [ ] Templates (project templates)
- [ ] Examples (example projects)
**And** the user can use arrow keys to navigate and spacebar to toggle
**And** Core Framework cannot be unchecked
**And** total installation size is displayed for selected components

### AC#5: Configuration Options

**Given** components have been selected
**When** the configuration options step is shown
**Then** additional options are presented:
- [ ] Initialize Git repository
- [ ] Create initial commit
- [ ] Run validation after install
**And** the user can toggle each option
**And** Git options are disabled if Git is not available

### AC#6: Installation Progress

**Given** the user has confirmed their selections
**When** the installation begins
**Then** a progress bar is displayed showing:
- Current step name
- Progress percentage
- Estimated time remaining
**And** the progress bar updates in real-time
**And** detailed logs are written to install.log
**And** critical errors stop installation with clear error message

### AC#7: Completion Summary

**Given** the installation has completed successfully
**When** the final step is reached
**Then** a success message is displayed showing:
- ✓ Installation successful!
- Installation path
- Components installed
- Next steps (commands to run)
**And** the user can press Enter to exit

### AC#8: Error Recovery

**Given** an error occurs during installation
**When** the error is encountered
**Then** the wizard displays:
- Clear error message
- Suggested remediation steps
- Option to retry, skip (if non-critical), or abort
**And** partial installation state is logged for manual cleanup

## AC Verification Checklist

### AC#1 Verification (Welcome Screen)
- [ ] Welcome screen displays framework name and version
- [ ] Description is clear and concise
- [ ] User can continue with Enter
- [ ] Ctrl+C cancellation works

### AC#2 Verification (License)
- [ ] License text is readable
- [ ] "accept" (case-insensitive) continues
- [ ] Other input re-prompts
- [ ] Long licenses are scrollable

### AC#3 Verification (Path Selection)
- [ ] Default path shown correctly
- [ ] Custom path can be entered
- [ ] Write permissions validated
- [ ] Invalid path shows error and re-prompts

### AC#4 Verification (Component Selection)
- [ ] All 4 components listed
- [ ] Core Framework pre-checked and locked
- [ ] Arrow keys navigate, spacebar toggles
- [ ] Installation size displayed

### AC#5 Verification (Configuration Options)
- [ ] Git options shown
- [ ] Git options disabled if Git unavailable
- [ ] Validation option available
- [ ] Options toggle correctly

### AC#6 Verification (Progress)
- [ ] Progress bar updates in real-time
- [ ] Current step name displayed
- [ ] Percentage accurate
- [ ] Log file created

### AC#7 Verification (Completion)
- [ ] Success message displayed
- [ ] All components listed
- [ ] Next steps provided
- [ ] Wizard exits cleanly

### AC#8 Verification (Error Recovery)
- [ ] Error message is clear
- [ ] Remediation steps provided
- [ ] Retry/skip/abort options work
- [ ] Partial state logged

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"
  story_id: STORY-247

  components:
    - name: WizardInstaller
      type: Service
      path: installer/wizard.py
      description: Main CLI wizard orchestrator with step-by-step flow
      public_methods:
        - name: run
          signature: "run() -> int"
          description: Execute main wizard flow, return exit code
        - name: step_welcome
          signature: "step_welcome() -> bool"
          description: Display welcome screen with framework info
        - name: step_license
          signature: "step_license() -> bool"
          description: Display and accept license agreement
        - name: step_path
          signature: "step_path() -> bool"
          description: Select and validate installation path
        - name: step_components
          signature: "step_components() -> bool"
          description: Select components to install
        - name: step_config
          signature: "step_config() -> bool"
          description: Configure installation options
        - name: step_install
          signature: "step_install() -> bool"
          description: Run installation with progress tracking
        - name: step_complete
          signature: "step_complete() -> None"
          description: Display completion summary
      test_requirement: "Unit tests for each wizard step with mocked input"

    - name: Component
      type: DataModel
      path: installer/wizard.py
      description: Definition of installable component
      fields:
        - name: id
          type: str
          description: Component identifier (core, cli, templates, examples)
        - name: name
          type: str
          description: Display name
        - name: description
          type: str
          description: Component description
        - name: size_mb
          type: float
          description: Installation size in MB
        - name: required
          type: bool
          description: True if component cannot be deselected
          default: false
        - name: selected
          type: bool
          description: Current selection state
          default: false
      test_requirement: "Validation tests for component dataclass"

    - name: WizardState
      type: DataModel
      path: installer/wizard.py
      description: Tracks wizard progress and selections
      fields:
        - name: current_step
          type: int
          description: Current step index (0-6)
        - name: target_path
          type: Path
          description: Installation target directory
        - name: components
          type: List[Component]
          description: Available components with selection state
        - name: config
          type: Dict[str, bool]
          description: Configuration options (init_git, etc.)
        - name: progress
          type: float
          description: Installation progress (0.0-1.0)
      test_requirement: "State persistence tests"

  business_rules:
    - id: BR-001
      description: Core Framework component MUST always be selected and cannot be deselected
      validation: Core component has required=True
      test_requirement: "Test that core cannot be unchecked"

    - id: BR-002
      description: License MUST be explicitly accepted with "accept" text (case-insensitive)
      validation: Check for exact "accept" string
      test_requirement: "Test license acceptance flow"

    - id: BR-003
      description: Installation path MUST be validated for write permissions before proceeding
      validation: Call os.access() with W_OK flag
      test_requirement: "Test path validation with valid/invalid paths"

    - id: BR-004
      description: Git options MUST be disabled if Git is not available on the system
      validation: Check for git command availability
      test_requirement: "Test git option disabling when git not found"

    - id: BR-005
      description: Progress bar MUST update in real-time (not batch at end)
      validation: Progress callback invoked per-file or per-step
      test_requirement: "Test progress update frequency"

  non_functional_requirements:
    - id: NFR-001
      category: Usability
      description: Wizard must be completable in under 2 minutes for typical installation
      metric: installation_time
      target: "< 120 seconds"
      test_requirement: "Timed installation tests"

    - id: NFR-002
      category: Usability
      description: All prompts must have sensible defaults (Enter to accept)
      metric: default_acceptance_rate
      target: "> 80% of prompts have defaults"
      test_requirement: "Prompt default analysis"

    - id: NFR-003
      category: Reliability
      description: Ctrl+C at any point must exit cleanly without partial state
      metric: clean_exit_rate
      target: "100%"
      test_requirement: "Interrupt handling tests"

    - id: NFR-004
      category: Compatibility
      description: Wizard must work in both TTY and non-TTY environments
      metric: environment_compatibility
      target: "100%"
      test_requirement: "Non-TTY mode tests"
```

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "Arrow key navigation"
    limitation: "Arrow keys for component selection require TTY; non-TTY uses numbered input"
    decision: "workaround:fallback-mode"
    discovered_phase: "Architecture"
    impact: "CI/CD environments use numbered input instead of arrow keys"
```

## File Structure

```
installer/
├── wizard.py           # Main wizard implementation (WizardInstaller class)
├── wizard_ui.py        # UI components (progress bar, menus)
├── wizard_steps.py     # Individual step implementations
└── wizard_state.py     # State management (WizardState dataclass)
```

## Error Handling

**Error Categories:**
- **Fatal:** Insufficient permissions, missing dependencies
- **Recoverable:** Network timeout, checksum mismatch
- **Warnings:** Optional component unavailable, Git not found

**Recovery Strategy:**
- Fatal → Abort with cleanup
- Recoverable → Retry up to 3 times
- Warnings → Log and continue

## Implementation Notes

### Dependencies
- **STORY-235 (Platform Detection):** Required for OS-specific steps
- **STORY-236 (Pre-flight Validator):** Run before installation begins
- **STORY-237 (Exit Codes):** Return appropriate codes for CI/CD

### Technology Constraints
- **Standard Library Preferred:** Use `input()` and print formatting
- **Optional inquirer:** Enhanced UI if available, but not required
- **No ncurses:** Maintain Windows compatibility

### Testing Strategy
- **Unit Tests:** Each wizard step in isolation
- **Integration Tests:** Full wizard flow with mock user input
- **E2E Tests:** Actual installation in test directories

## Definition of Done

- [ ] All acceptance criteria verified and passing
- [ ] Unit tests written and passing (95%+ coverage)
- [ ] Integration tests written and passing
- [ ] Code reviewed and approved
- [ ] Documentation updated
- [ ] No Critical/High anti-pattern violations
- [ ] Pre-flight validation integrated
- [ ] Exit codes properly returned

## Notes

- Consider adding a "Quick Install" mode that skips optional steps
- Progress bar should work in both TTY and non-TTY environments
- Wizard state could be saved to allow resume after interruption

## Change Log

**Current Status:** Backlog

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2025-01-06 | claude/batch-creation | Story Creation | Initial story created from EPIC-039 Feature 1 | STORY-247-cli-wizard-installer.story.md |
| 2025-01-06 | claude/normalization | Template Update | Normalized to format_version 2.5 | STORY-247-cli-wizard-installer.story.md |

---

**Template Version:** 2.5
**Created:** 2025-01-06 by /create-missing-stories (batch mode)
