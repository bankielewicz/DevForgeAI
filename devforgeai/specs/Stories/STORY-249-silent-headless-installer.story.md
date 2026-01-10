---
id: STORY-249
title: Silent/Headless Installer
type: feature
epic: EPIC-039
sprint: Backlog
priority: Medium
points: 5
depends_on: ["STORY-235", "STORY-236"]
status: QA Approved
created: 2025-01-06
updated: 2025-01-06
format_version: "2.5"
---

# STORY-249: Silent/Headless Installer

## User Story

**As a** DevOps engineer,
**I want** a configuration-driven silent installation mode,
**So that** I can automate DevForgeAI deployments in CI/CD pipelines.

## Acceptance Criteria

### AC#1: YAML Configuration File Support

**Given** a silent install configuration file `install-config.yaml`
**When** the installer runs with `--silent --config install-config.yaml`
**Then** the installer reads configuration from the YAML file
**And** no interactive prompts are displayed
**And** installation proceeds automatically using config values
**And** missing required fields cause immediate failure with error code

**Example Config:**
```yaml
target: /opt/devforgeai
components:
  - core
  - cli
  - templates
options:
  initialize_git: true
  create_backup: false
  run_validation: true
log_file: /var/log/devforgeai-install.log
```

### AC#2: Environment Variable Configuration

**Given** environment variables are set for installation
**When** the installer runs with `--silent` (no config file)
**Then** configuration is read from environment variables:
- `DEVFORGEAI_TARGET` → installation path
- `DEVFORGEAI_COMPONENTS` → comma-separated component list
- `DEVFORGEAI_INIT_GIT` → true/false
- `DEVFORGEAI_LOG_FILE` → log file path
**And** environment variables override config file values
**And** missing required variables cause failure

### AC#3: No Interactive Prompts

**Given** silent mode is enabled
**When** the installer encounters any decision point
**Then** no user input is requested
**And** default or configured values are used
**And** terminal input is never read
**And** the installer can run in headless/non-TTY environments

### AC#4: Structured Logging

**Given** silent installation is running
**When** installation progresses through steps
**Then** all output is written to the configured log file
**And** log entries include:
  - Timestamp (ISO 8601 format)
  - Log level (INFO, WARNING, ERROR)
  - Message
  - Component/module name
**And** stdout contains only JSON progress updates (optional)
**And** stderr contains only critical errors

**Example Log Entry:**
```
2025-01-06T12:34:56Z [INFO] installer.preflight: Disk space check passed (50GB available)
2025-01-06T12:34:57Z [INFO] installer.core: Extracting core framework...
2025-01-06T12:35:10Z [WARNING] installer.git: Git not found, skipping repository initialization
2025-01-06T12:35:15Z [INFO] installer.validation: Installation validated successfully
```

### AC#5: Exit Codes for CI/CD

**Given** silent installation completes
**When** the installer exits
**Then** appropriate exit codes are returned:
- `0` → Success
- `1` → Configuration error
- `2` → Pre-flight validation failure
- `3` → Installation error
- `4` → Post-install validation failure
**And** exit codes match `installer/exit_codes.py` (STORY-237)
**And** CI/CD pipelines can detect failures via exit code

### AC#6: Dry-Run Mode

**Given** the installer runs with `--silent --dry-run`
**When** the dry-run executes
**Then** all pre-flight checks are performed
**And** configuration is validated
**And** installation steps are logged but not executed
**And** log output includes "DRY RUN:" prefix for each would-be action
**And** exit code 0 is returned if dry-run passes

### AC#7: Idempotency

**Given** a successful silent installation has completed
**When** the same silent installation is run again
**Then** the installer detects existing installation
**And** no duplicate files are created
**And** existing files are preserved (not overwritten)
**And** log indicates "Already installed" status
**And** exit code 0 is returned (success, no changes)

### AC#8: JSON Progress Output (Optional)

**Given** the installer runs with `--silent --json`
**When** installation progresses
**Then** JSON progress updates are written to stdout:
```json
{"status": "in_progress", "percent": 45, "step": "Installing CLI Tools"}
{"status": "complete", "percent": 100, "installed_components": ["core", "cli"]}
{"status": "error", "code": 3, "message": "Permission denied"}
```
**And** each line is valid JSON (newline-delimited JSON stream)
**And** CI/CD tools can parse progress updates

## AC Verification Checklist

### AC#1 Verification (YAML Config)
- [ ] YAML file parsed correctly
- [ ] All config fields applied
- [ ] Missing fields cause error
- [ ] Invalid YAML causes error with clear message

### AC#2 Verification (Environment Variables)
- [ ] All env vars read correctly
- [ ] Env vars override config file
- [ ] Missing required vars cause error
- [ ] Invalid values cause error

### AC#3 Verification (No Prompts)
- [ ] No input() calls executed
- [ ] No user interaction required
- [ ] Works in non-TTY environment
- [ ] Automated tests pass

### AC#4 Verification (Logging)
- [ ] Log file created at specified path
- [ ] Timestamps in ISO 8601 format
- [ ] Log levels correct
- [ ] No sensitive data logged

### AC#5 Verification (Exit Codes)
- [ ] Success returns 0
- [ ] Config error returns 1
- [ ] Pre-flight failure returns 2
- [ ] Installation error returns 3
- [ ] Validation failure returns 4

### AC#6 Verification (Dry-Run)
- [ ] No files created
- [ ] All checks performed
- [ ] Log shows DRY RUN prefix
- [ ] Exit code correct

### AC#7 Verification (Idempotency)
- [ ] Existing install detected
- [ ] No duplicate files
- [ ] No overwrites
- [ ] Exit code 0 on re-run

### AC#8 Verification (JSON Output)
- [ ] JSON lines valid
- [ ] Progress updates accurate
- [ ] Error JSON includes details
- [ ] Newline-delimited format

## Technical Specification

### Architecture

**Component:** `installer/silent.py`
**Dependencies:**
- `installer/platform_detector.py` (STORY-235)
- `installer/preflight.py` (STORY-236)
- `installer/exit_codes.py` (STORY-237)
- `PyYAML` (for config parsing)

**Class Structure:**
```python
class SilentInstaller:
    def __init__(self, config: Union[Path, Dict]):
        self.config = self._load_config(config)
        self.logger = self._setup_logger()

    def _load_config(self, source) -> InstallConfig:
        """Load from YAML file or dict"""
        pass

    def _setup_logger(self) -> logging.Logger:
        """Configure structured logging"""
        pass

    def run(self) -> int:
        """Execute silent installation"""
        try:
            self._validate_config()
            self._run_preflight()
            self._install_components()
            self._run_validation()
            return ExitCode.SUCCESS
        except ConfigError:
            return ExitCode.CONFIG_ERROR
        except PreflightError:
            return ExitCode.PREFLIGHT_ERROR
        except InstallError:
            return ExitCode.INSTALL_ERROR
        except ValidationError:
            return ExitCode.VALIDATION_ERROR

    def _emit_json_progress(self, status, **kwargs):
        """Emit JSON to stdout if --json enabled"""
        pass
```

### Configuration Schema

```python
@dataclass
class InstallConfig:
    target: Path
    components: List[str]
    options: InstallOptions
    log_file: Path = Path("install.log")

@dataclass
class InstallOptions:
    initialize_git: bool = False
    create_backup: bool = False
    run_validation: bool = True
    dry_run: bool = False
```

### Environment Variable Mapping

| Environment Variable | Config Field | Default |
|---------------------|--------------|---------|
| `DEVFORGEAI_TARGET` | `target` | (required) |
| `DEVFORGEAI_COMPONENTS` | `components` | `core` |
| `DEVFORGEAI_INIT_GIT` | `options.initialize_git` | `false` |
| `DEVFORGEAI_LOG_FILE` | `log_file` | `install.log` |
| `DEVFORGEAI_DRY_RUN` | `options.dry_run` | `false` |

### Logging Configuration

```python
import logging
import json
from datetime import datetime

class StructuredFormatter(logging.Formatter):
    def format(self, record):
        timestamp = datetime.utcnow().isoformat() + 'Z'
        return f"{timestamp} [{record.levelname}] {record.name}: {record.getMessage()}"

logger = logging.getLogger('installer')
handler = logging.FileHandler(config.log_file)
handler.setFormatter(StructuredFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)
```

### Idempotency Check

```python
def is_already_installed(target_path: Path) -> bool:
    """Check if DevForgeAI is already installed"""
    marker_file = target_path / ".devforgeai_installed"
    if marker_file.exists():
        with open(marker_file) as f:
            data = json.load(f)
        logger.info(f"Installation detected: version {data['version']}")
        return True
    return False
```

## Technical Notes

### Dependencies
- **STORY-235 (Platform Detection):** Detect OS for path validation
- **STORY-236 (Pre-flight Validator):** Run validation before install
- **STORY-237 (Exit Codes):** Use standardized exit codes

### Technology Constraints
- **PyYAML:** Only external dependency (already in project)
- **Standard Library:** Use logging, json modules
- **No TTY Assumptions:** Never call input() or readline()

### CI/CD Integration Examples

**GitHub Actions:**
```yaml
- name: Install DevForgeAI
  run: |
    python -m installer install . \
      --silent \
      --config .github/install-config.yaml \
      --log install.log
  env:
    DEVFORGEAI_INIT_GIT: false
```

**GitLab CI:**
```yaml
install_devforgeai:
  script:
    - python -m installer install $CI_PROJECT_DIR --silent --json
  artifacts:
    when: always
    paths:
      - install.log
```

## Definition of Done

- [x] All acceptance criteria verified and passing
- [x] YAML config parsing works
- [x] Environment variable override works
- [x] Exit codes correct for all scenarios
- [x] Dry-run mode functional
- [x] Idempotency verified
- [x] JSON output format valid
- [x] CI/CD integration tested
- [x] No interactive prompts in silent mode

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2025-01-09
**Branch:** refactor/devforgeai-migration

- [x] All acceptance criteria verified and passing - Completed: 75 tests covering all 8 ACs
- [x] YAML config parsing works - Completed: TestYamlConfigurationFileSupport 7 tests
- [x] Environment variable override works - Completed: TestEnvironmentVariableConfiguration 6 tests
- [x] Exit codes correct for all scenarios - Completed: TestExitCodesForCICD 6 tests
- [x] Dry-run mode functional - Completed: TestDryRunMode 6 tests
- [x] Idempotency verified - Completed: TestIdempotency 6 tests
- [x] JSON output format valid - Completed: TestJsonProgressOutput 6 tests
- [x] CI/CD integration tested - Completed: TestCICDCompatibility 3 tests
- [x] No interactive prompts in silent mode - Completed: TestNoInteractivePrompts 4 tests

### TDD Workflow Summary

**Phase 02 (Red):** 75 tests generated covering all 8 acceptance criteria
**Phase 03 (Green):** installer/silent.py implemented (510 lines)
**Phase 04 (Refactor):** DRY refactoring (_parse_env_boolean helper)
**Phase 05 (Integration):** All 5 integration points validated

### Files Created

- `installer/silent.py` - SilentInstaller service with InstallConfig, InstallOptions dataclasses
- `installer/tests/test_silent.py` - 75 comprehensive tests

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2025-01-06 | claude/batch-creation | Story Creation | Initial story created from EPIC-039 Feature 3 | STORY-249-silent-headless-installer.story.md |
| 2025-01-06 | claude/normalization | Template Update | Normalized to format_version 2.5 | STORY-249-silent-headless-installer.story.md |
| 2025-01-09 | claude/test-automator | Red (Phase 02) | 75 tests generated | installer/tests/test_silent.py |
| 2025-01-09 | claude/backend-architect | Green (Phase 03) | Implementation complete | installer/silent.py |
| 2025-01-09 | claude/refactoring-specialist | Refactor (Phase 04) | DRY refactoring applied | installer/silent.py |
| 2025-01-09 | claude/opus | DoD Update (Phase 07) | Development complete, DoD validated | STORY-249-silent-headless-installer.story.md |
| 2025-01-09 | claude/qa-result-interpreter | QA Deep | PASS WITH WARNINGS: Coverage 89%, 1 HIGH violation (path traversal - remediation noted) | devforgeai/qa/reports/STORY-249-qa-report.md |

---

**Template Version:** 2.5
**Created:** 2025-01-06 by /create-missing-stories (batch mode)
