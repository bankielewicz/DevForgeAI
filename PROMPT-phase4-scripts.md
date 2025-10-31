# DevForgeAI Release Skill - Phase 4: Automation Scripts

**Session Objective**: Implement 5 automation scripts and README for the devforgeai-release skill

**Context**: Phases 0-3 are complete (67% done). This session focuses on Phase 4: creating Python/Bash scripts for deployment automation.

---

## Quick Start Instructions

### 1. Load Context Files (Read these first)

```
Read the following files to understand what's been completed:

1. Progress tracker:
   Read(file_path="/mnt/c/Projects/DevForgeAI2/PROMPT-implement-release-skill.md")

2. SKILL.md (to understand script requirements):
   Read(file_path="/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-release/SKILL.md")

3. Reference files (for script implementation details):
   Read(file_path="/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-release/references/smoke-testing-guide.md")
   Read(file_path="/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-release/references/monitoring-metrics.md")
   Read(file_path="/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-release/references/rollback-procedures.md")

4. Skill creator guide (for best practices):
   Read(file_path="/mnt/c/Projects/DevForgeAI2/.claude/skills/skill-creator/skill.md")
```

### 2. Current Status Summary

**Completed**:
- ✅ Phase 0: Preparation
- ✅ Phase 1: SKILL.md (18,000 tokens)
- ✅ Phase 2: Reference Files (5 files, 24,500 tokens)
- ✅ Phase 3: Asset Templates (3 files, 7,600 tokens)

**Current Phase**: Phase 4 - Automation Scripts

**Total Progress**: 67% complete (50,100 / 75,000 tokens)

---

## Phase 4: Scripts to Implement

Create these 5 scripts in `.claude/skills/devforgeai-release/scripts/`:

### 1. **health_check.py** (~3,000 tokens)

**Purpose**: HTTP health endpoint checker with retry logic

**Requirements**:
- HTTP GET request to health endpoint
- Retry logic with exponential backoff (e.g., 1s, 2s, 4s, 8s, 16s)
- Configurable retry count and timeout
- Validate JSON response structure
- Exit codes: 0 (success), 1 (failure)
- Command-line arguments: --url, --retries, --timeout
- Usage example: `python health_check.py --url https://api.example.com/health --retries 5 --timeout 10`

**Implementation Notes**:
- Use `requests` library
- Support both HTTP and HTTPS
- Log each retry attempt
- Pretty-print JSON response on success
- Clear error messages on failure

---

### 2. **smoke_test_runner.py** (~4,000 tokens)

**Purpose**: Orchestrate pytest smoke test suite with environment-specific configuration

**Requirements**:
- Execute pytest smoke tests for specified environment
- Support environment parameter: staging, production, production-green, production-canary
- Configuration file: `.devforgeai/smoke-tests/config.json` (environment URLs, credentials)
- Parallel test execution support (pytest-xdist)
- Results aggregation and reporting
- Generate HTML report
- Exit codes: 0 (all passed), 1 (any failed)
- Command-line arguments: --environment, --tests (all, critical_path, api, database)
- Usage example: `python smoke_test_runner.py --environment production --tests critical_path`

**Implementation Notes**:
- Use `pytest` with custom markers (@pytest.mark.smoke, @pytest.mark.critical_path)
- Load environment configuration from JSON
- Support test filtering by marker
- Generate junit XML and HTML reports
- Summary report with pass/fail counts

---

### 3. **metrics_collector.py** (~4,000 tokens)

**Purpose**: Collect metrics from monitoring systems and compare against baseline

**Requirements**:
- Support multiple monitoring backends: AWS CloudWatch, Datadog, Prometheus, Azure Monitor
- Collect metrics: error_rate, response_time_p95, response_time_p99, request_rate, cpu, memory
- Time window parameter (duration in seconds)
- Baseline comparison mode (--baseline-compare flag)
- Load baseline from `.devforgeai/monitoring/baselines/{environment}-baseline.json`
- Calculate percentage change and status (NORMAL, WARNING, CRITICAL)
- Output JSON report with violations
- Determine if rollback recommended (exit code 2 if critical violations)
- Command-line arguments: --environment, --duration, --baseline-compare, --output
- Usage example: `python metrics_collector.py --environment production --duration 900 --baseline-compare --output metrics-report.json`

**Implementation Notes**:
- Use boto3 (AWS), datadog library, prometheus_api_client, azure-monitor-query
- Configuration file: `.devforgeai/monitoring/config.json` (credentials, namespaces)
- Threshold configuration in monitoring-metrics.md reference
- Exit codes: 0 (healthy), 1 (warnings), 2 (critical - rollback recommended)

---

### 4. **rollback_automation.sh** (~2,000 tokens)

**Purpose**: Automated rollback for multiple platforms

**Requirements**:
- Platform detection or manual specification (--platform flag)
- Support platforms: kubernetes, azure, aws_ecs, docker
- Rollback to specified version (--version parameter)
- Deployment name/identifier parameter (--deployment)
- Database rollback integration (optional --rollback-db flag)
- Verification after rollback (health check)
- Logging all commands executed
- Exit codes: 0 (success), 1 (failure)
- Command-line arguments: --platform, --deployment, --version, --namespace, --rollback-db
- Usage example: `./rollback_automation.sh --platform kubernetes --deployment myapp --version v1.9.0 --namespace production`

**Implementation Notes**:
- Bash script (not Python)
- Execute platform-specific commands from rollback-procedures.md reference
- Verify rollback success with health check
- Create rollback log file in `.devforgeai/releases/rollback-logs/`

---

### 5. **release_notes_generator.py** (~2,000 tokens)

**Purpose**: Generate release notes from story document and template

**Requirements**:
- Parse story document (`.ai_docs/Stories/{story-id}.story.md`)
- Extract: title, acceptance criteria, changes, QA status, version
- Load template (`.claude/skills/devforgeai-release/assets/templates/release-notes-template.md`)
- Replace {{VARIABLE}} placeholders with actual values
- Generate release notes file in `.devforgeai/releases/release-{version}.md`
- Update CHANGELOG.md with new entry
- Command-line arguments: --story, --version, --qa-report, --metrics-report
- Usage example: `python release_notes_generator.py --story STORY-001 --version v1.2.3 --qa-report .devforgeai/qa/reports/STORY-001-qa-report.md --metrics-report metrics.json`

**Implementation Notes**:
- Parse YAML frontmatter from story
- Extract acceptance criteria from markdown
- Load QA report and metrics JSON
- Template variable substitution
- Append to CHANGELOG.md using conventional commits format

---

### 6. **README.md** (~1,000 tokens)

**Purpose**: Document all scripts with usage examples

**Requirements**:
- Overview of all scripts
- Installation instructions (dependencies)
- Configuration requirements
- Usage examples for each script
- Troubleshooting section
- Integration with release workflow

**Structure**:
```markdown
# Release Skill Automation Scripts

## Overview
[Description of scripts and purpose]

## Installation
[pip install requirements, etc.]

## Configuration
[Config files needed]

## Scripts

### health_check.py
[Usage, examples, exit codes]

### smoke_test_runner.py
[Usage, examples, exit codes]

... (for each script)

## Troubleshooting
[Common issues and solutions]
```

---

## Implementation Guidelines

### Quality Standards

1. **Comprehensive Implementation**: No concise versions - full, production-ready code
2. **Error Handling**: Robust try/except blocks with clear error messages
3. **Logging**: Use Python `logging` module with configurable levels
4. **Documentation**: Docstrings for all functions, clear comments
5. **Exit Codes**: Consistent exit code conventions (0=success, 1=failure, 2=critical)
6. **Configuration**: External config files, not hardcoded values
7. **Command-Line Interface**: Use `argparse` with clear help text
8. **Dependencies**: Minimal dependencies, document all requirements

### Code Structure (Python Scripts)

```python
#!/usr/bin/env python3
"""
Script description

Usage:
    python script.py --arg1 value1 --arg2 value2

Exit Codes:
    0: Success
    1: Failure
    2: Critical (if applicable)
"""

import argparse
import logging
import sys
# ... other imports

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Script description')
    parser.add_argument('--arg', required=True, help='Argument description')
    args = parser.parse_args()

    try:
        # Main logic
        result = do_work(args)
        logger.info("Success")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)

def do_work(args):
    """Core functionality"""
    pass

if __name__ == '__main__':
    main()
```

### Token Budget

| Script | Estimated | Target |
|--------|-----------|--------|
| health_check.py | 3,000 | Comprehensive implementation |
| smoke_test_runner.py | 4,000 | Full orchestration logic |
| metrics_collector.py | 4,000 | Multi-backend support |
| rollback_automation.sh | 2,000 | All platform commands |
| release_notes_generator.py | 2,000 | Template population |
| README.md | 1,000 | Complete documentation |
| **TOTAL** | **16,000** | Phase 4 complete |

---

## Step-by-Step Execution

### Step 1: Create Todo List

```
Use TodoWrite to create a todo list with 6 items:
1. Create health_check.py
2. Create smoke_test_runner.py
3. Create metrics_collector.py
4. Create rollback_automation.sh
5. Create release_notes_generator.py
6. Create README.md for scripts
```

### Step 2: Implement Scripts

For each script:
1. Mark todo as "in_progress"
2. Use Write tool to create the script (NOT Bash commands)
3. Include full implementation (no placeholders or TODO comments)
4. Mark todo as "completed"
5. Move to next script

### Step 3: Update Progress Tracker

After all scripts complete:
```
Edit(file_path="/mnt/c/Projects/DevForgeAI2/PROMPT-implement-release-skill.md",
     old_string="**Current Status**: Phase 3 Complete",
     new_string="**Current Status**: Phase 4 Complete")

Update token budget table with actual token counts
Update checklist items to mark scripts complete
```

---

## Reference Files (Already Created)

These files contain implementation details for the scripts:

1. **smoke-testing-guide.md**: Test categories, code examples
2. **monitoring-metrics.md**: Metrics collection, threshold logic
3. **rollback-procedures.md**: Platform-specific rollback commands
4. **deployment-strategies.md**: Deployment execution details

Reference these files while implementing scripts to ensure consistency with the documented procedures.

---

## Success Criteria

Phase 4 is complete when:

- [x] All 6 files created in `.claude/skills/devforgeai-release/scripts/`
- [x] Each script has complete implementation (no placeholders)
- [x] Command-line interfaces with argparse
- [x] Error handling and logging
- [x] Usage examples in script docstrings
- [x] README.md documents all scripts
- [x] Progress tracker updated with Phase 4 completion
- [x] Token budget table updated with actual counts

---

## After Phase 4 Completion

**Next**: Phase 5 - Validation & Testing
- Validate SKILL.md against skill-creator requirements
- Test skill invocation patterns
- Verify integration points
- Check token efficiency
- Final quality review

**Estimated Time**: 30 minutes

---

## Important Reminders

1. **Use Native Tools**: Write(file_path="...") NOT `cat > file` or `echo >`
2. **No Concise Versions**: Full implementations only
3. **Quality Over Speed**: Production-ready code, not quick prototypes
4. **Update Progress**: Mark todos and update progress tracker as you go
5. **Reference Existing Work**: Use completed reference files for implementation details

---

## Start Command

```
Begin Phase 4 implementation:

1. Read progress tracker to understand current state
2. Read SKILL.md to understand script requirements
3. Read relevant reference files
4. Create todo list for 6 scripts
5. Implement each script sequentially
6. Update progress tracker when complete
```

**Good luck! This is the final major implementation phase before validation.**
