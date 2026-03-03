# DevForgeAI Installation Wizard

Interactive CLI wizard for DevForgeAI installation with visual feedback and guided prompts.

## Services

### InstallWizard
Main orchestrator for the installation wizard flow. Coordinates prompts, progress indicators, and error handling.

```javascript
const { InstallWizard } = require('./install-wizard');

const wizard = new InstallWizard({
  promptService,
  progressService,
  outputFormatter,
  signalHandler,
  installer
});

const config = await wizard.run({ yes: false, quiet: false });
```

### PromptService
Handles interactive prompts using Inquirer.js.

**Prompts:**
- `promptTargetDirectory()` - Target installation directory (default: current directory)
- `promptInstallationMode()` - Installation mode: minimal, standard, full (default: standard)
- `promptMergeStrategy()` - CLAUDE.md merge: preserve-user, merge-smart, replace (default: merge-smart)
- `promptConfirmation(message, options)` - Yes/No confirmation for destructive actions

### ProgressService
Visual progress indicators using Ora (spinners) and CLI-Progress (progress bars).

**Methods:**
- `startSpinner(text)` - Start spinner for indeterminate operations
- `updateSpinner(text)` - Update spinner text
- `stopSpinner(success, text)` - Stop spinner with success/failure indicator
- `startProgressBar(total, label)` - Start progress bar for determinate operations
- `updateProgressBar(current)` - Update progress bar
- `stopProgressBar()` - Stop progress bar

### OutputFormatter
Color-coded terminal output using Chalk.

**Methods:**
- `success(message)` - Green output with ✓ symbol
- `warning(message)` - Yellow output with ⚠ symbol
- `error(message)` - Red output with ✗ symbol
- `info(message)` - Blue output with ? symbol

### SignalHandler
Graceful SIGINT (Ctrl+C) handling with cleanup.

**Methods:**
- `register()` - Register SIGINT handler
- `unregister()` - Remove SIGINT handler
- `trackFile(path)` - Track file for cleanup on interrupt
- `captureState(state)` - Capture state for restoration

### WizardConfig
Configuration defaults and validation.

**Defaults:**
- `targetDirectory`: "."
- `installationMode`: "standard"
- `mergeStrategy`: "merge-smart"
- `spinnerDelayMs`: 200
- `exitCodes.success`: 0
- `exitCodes.sigint`: 130

## CLI Flags

| Flag | Description | Default |
|------|-------------|---------|
| `--yes` | Skip all prompts, use defaults | false |
| `--quiet` | Suppress non-error output | false |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `CI=true` | Auto-enables --yes and --quiet |
| `NO_COLOR` | Disables color output |
| `TERM=dumb` | Uses ASCII fallback symbols |

## Exit Codes

| Code | Description |
|------|-------------|
| 0 | Success |
| 1 | General error |
| 130 | Cancelled by user (Ctrl+C) |

## Dependencies

- `inquirer@8.2.6` - Interactive prompts (CommonJS)
- `ora@5.4.1` - Spinners (CommonJS)
- `cli-progress@3.12.0` - Progress bars
- `chalk@4.1.2` - Colors (CommonJS)
- `commander@11.0.0` - CLI parsing

See ADR-006 for ESM/CJS compatibility decisions.
