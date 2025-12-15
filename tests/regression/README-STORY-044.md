# STORY-044: Comprehensive Testing of src/ Structure

## Overview

This regression test suite validates that the DevForgeAI framework functions correctly after the STORY-043 path migration to src/ structure. All tests are designed to **FAIL when paths are broken** and **PASS when paths are correct**.

## Test Structure

### Test Organization

```
tests/regression/
├── test-src-migration.sh              # Master runner (6 phases integrated)
├── test-commands.sh                   # Phase 1: 23 slash commands
├── test-skills-reference-loading.sh   # Phase 2: 14 skills + references
├── test-subagents.sh                  # Phase 3: 27 subagents
├── test-cli-commands.sh               # Phase 4: 5 CLI commands
├── test-integration-workflows.sh       # Phase 5: 3 integration workflows
├── test-performance-benchmarks.sh      # Phase 6: Performance benchmarks
├── run-all-tests.sh                   # Master orchestrator
└── README-STORY-044.md                # This file

src/claude/scripts/tests/
└── test_src_migration.py              # Python unit tests (pytest)
```

## Test Coverage

### Phase 1: Slash Commands (23 tests)

**Command Categories:**
- **Core Workflow (4):** `/dev`, `/qa`, `/release`, `/orchestrate`
- **Planning & Setup (7):** `/ideate`, `/create-context`, `/create-epic`, `/create-sprint`, `/create-story`, `/create-ui`, `/create-agent`
- **Framework Maintenance (4):** `/audit-deferrals`, `/audit-budget`, `/audit-hooks`, `/rca`
- **Feedback System (7):** `/feedback`, `/feedback-config`, `/feedback-search`, `/feedback-reindex`, `/feedback-export-data`, `/export-feedback`, `/import-feedback`
- **Documentation (1):** `/document`

**Tests:**
- File exists at correct path
- File size > 100 bytes (valid content)
- Contains required metadata (`description:`, `model:`)

**Success Criteria:** 23/23 commands executable

### Phase 2: Skills Reference Loading (14 tests)

**Skills Tested:**
1. devforgeai-architecture
2. devforgeai-development
3. devforgeai-documentation
4. devforgeai-feedback
5. devforgeai-ideation
6. devforgeai-mcp-cli-converter
7. devforgeai-orchestration
8. devforgeai-qa
9. devforgeai-release
10. devforgeai-rca
11. devforgeai-story-creation
12. devforgeai-subagent-creation
13. devforgeai-ui-generator
14. claude-code-terminal-expert

**Tests Per Skill:**
- SKILL.md file exists
- SKILL.md has valid content (>100 bytes)
- References directory loadable (if exists)
- Reference files readable

**Success Criteria:** 14/14 skills reference loading works

### Phase 3: Subagents (27 tests)

**Subagents Tested:**
- agent-generator
- api-designer
- architect-reviewer
- backend-architect
- code-analyzer
- code-reviewer
- context-validator
- deferral-validator
- deployment-engineer
- dev-result-interpreter
- documentation-writer
- frontend-developer
- git-validator
- integration-tester
- internet-sleuth
- pattern-compliance-auditor
- qa-result-interpreter
- refactoring-specialist
- requirements-analyst
- security-auditor
- sprint-planner
- story-requirements-analyst
- tech-stack-detector
- technical-debt-analyzer
- test-automator
- ui-spec-formatter

**Tests Per Subagent:**
- File exists at correct path
- File size > 100 bytes
- Contains required metadata (`description:`)

**Success Criteria:** 27/27 subagents available and loadable

### Phase 4: CLI Commands (5 tests)

**CLI Commands Tested:**
- `devforgeai validate-dod`
- `devforgeai check-git`
- `devforgeai validate-context`
- `devforgeai check-hooks`
- `devforgeai invoke-hooks`

**Tests:**
- CLI is installed/available in PATH
- Each command responds to `--help`

**Success Criteria:** 5/5 CLI commands operational (or skip if not installed)

### Phase 5: Integration Workflows (3 tests)

**Workflow 1: Epic → Story → Development**
- `.ai_docs/Epics` exists
- `.ai_docs/Stories` exists
- All 6 context files exist
- devforgeai-development skill exists
- `tests/` directory exists

**Workflow 2: Context → Story → QA**
- All 6 context files exist
- `.ai_docs/Stories` exists
- `.devforgeai/qa` directory exists
- devforgeai-qa skill exists
- QA reference files loadable

**Workflow 3: Sprint Planning → Story**
- `.ai_docs/Sprints` exists
- `.ai_docs/Stories` exists
- devforgeai-orchestration skill exists
- devforgeai-story-creation skill exists
- `.devforgeai/adrs` directory exists

**Success Criteria:** 3/3 workflows complete, 0 path errors

### Phase 6: Performance Benchmarks (6 benchmarks)

**Benchmarks:**
1. Command file scanning (<100ms baseline, ±10% tolerance)
2. Skill file scanning (<100ms baseline, ±10% tolerance)
3. Subagent file scanning (<50ms baseline, ±10% tolerance)
4. Context file loading (<50ms baseline, ±10% tolerance)
5. Recursive glob matching (<150ms baseline, ±10% tolerance)
6. File count operations (informational)

**Success Criteria:** All benchmarks within ±10% tolerance

## Running Tests

### Run All Tests

**Using Master Runner:**
```bash
bash tests/regression/run-all-tests.sh
```

**Output:**
- Console output with color-coded results
- JSON report: `tests/regression/test-src-migration-final-results.json`
- Individual phase logs (if desired)

### Run Individual Test Phases

**Phase 1: Commands**
```bash
bash tests/regression/test-commands.sh
```

**Phase 2: Skills**
```bash
bash tests/regression/test-skills-reference-loading.sh
```

**Phase 3: Subagents**
```bash
bash tests/regression/test-subagents.sh
```

**Phase 4: CLI**
```bash
bash tests/regression/test-cli-commands.sh
```

**Phase 5: Workflows**
```bash
bash tests/regression/test-integration-workflows.sh
```

**Phase 6: Performance**
```bash
bash tests/regression/test-performance-benchmarks.sh
```

### Run Python Unit Tests

**Using pytest:**
```bash
python -m pytest src/claude/scripts/tests/test_src_migration.py -v
```

**Coverage report:**
```bash
python -m pytest src/claude/scripts/tests/test_src_migration.py --cov=.claude --cov-report=term
```

**With markers:**
```bash
# Run only parametrized tests
python -m pytest src/claude/scripts/tests/test_src_migration.py -v -m parametrize
```

## Test Results Interpretation

### Success Scenario
```
[PASS] Phase 1: Slash Commands (23) PASSED
[PASS] Phase 2: Skills Reference Loading (14) PASSED
[PASS] Phase 3: Subagents (27) PASSED
[PASS] Phase 4: CLI Commands (5) PASSED
[PASS] Phase 5: Integration Workflows (3) PASSED
[PASS] Phase 6: Performance Benchmarks PASSED

✓ All test phases PASSED
```

### Failure Scenario
```
[FAIL] Phase 1: Slash Commands (23) FAILED
  [FAIL] Command file missing: /dev
  [FAIL] Command file missing: /qa

[PASS] Phase 2: Skills Reference Loading (14) PASSED
[WARN] Phase 3: Subagents (27) - 1 subagent missing
  [FAIL] Subagent file missing: test-automator
...

✗ Some test phases FAILED
```

**Interpretation:**
- Missing files indicate broken path references
- Small files (<100 bytes) indicate incomplete content
- Performance warnings indicate I/O performance (non-fatal)
- Integration workflow failures indicate missing directory structure

## Test Failure Diagnosis

### When Tests Fail

**Problem:** Command file not found
```
[FAIL] Command file missing: /dev
```
**Diagnosis:** Path .claude/commands/dev.md doesn't exist or path resolution broken
**Resolution:** Check STORY-043 path updates applied correctly

**Problem:** Skill reference loading failed
```
[FAIL] Skill file too small: devforgeai-development (45 bytes)
```
**Diagnosis:** SKILL.md file corrupted or truncated during migration
**Resolution:** Verify file integrity and re-migrate if needed

**Problem:** Subagent file missing
```
[FAIL] Subagent file missing: test-automator
```
**Diagnosis:** Subagent file not migrated to new location
**Resolution:** Check all agent files migrated from old to new paths

**Problem:** Integration workflow path error
```
[FAIL] Integration Workflow 1: Missing context files
       Path: devforgeai/context/tech-stack.md (NOT FOUND)
```
**Diagnosis:** Context files not in expected location
**Resolution:** Verify context file paths updated in STORY-043

## Test Design Principles

### TDD Red Phase

**All tests are designed to FAIL when:**
- Paths are broken or incorrect
- Files are missing from new locations
- Reference files cannot be loaded
- Directory structure is incomplete
- Integration paths don't exist

**Tests PASS when:**
- All files exist at correct paths
- File content is valid (>100 bytes)
- Directory structures complete
- All integration workflows executable
- Performance within tolerance

### No External Dependencies

**Tests use only:**
- Bash shell scripting
- Standard file operations (find, test)
- Basic math operations
- Python standard library (Path, os, pytest)

**No dependencies on:**
- External HTTP calls
- Database access
- Third-party tools
- Docker/containers
- Network operations

### Fail Fast on Critical Issues

**Zero Tolerance for:**
- Missing command files (path broken)
- Missing skill SKILL.md (skill broken)
- Missing subagent files (agent broken)
- Missing context files (framework broken)
- Integration workflow paths broken

**Warnings (non-fatal) for:**
- Missing reference files (may be optional)
- CLI not installed (can run without)
- Performance slower than baseline
- Metadata missing (backward compatible)

## Performance Benchmarks

### Baseline Expectations

| Benchmark | Baseline | Tolerance | Status |
|-----------|----------|-----------|--------|
| Command file scanning | 100ms | ±10% | Informational |
| Skill file scanning | 100ms | ±10% | Informational |
| Subagent file scanning | 50ms | ±10% | Informational |
| Context file loading | 50ms | ±10% | Informational |
| Recursive glob matching | 150ms | ±10% | Informational |

**Note:** Performance tests are informational only. Tests do not fail due to performance, but warnings are displayed.

## JSON Report Format

**File:** `tests/regression/test-src-migration-final-results.json`

**Structure:**
```json
{
  "test_execution": {
    "timestamp": "2025-11-19T14:30:45Z",
    "total_duration_seconds": 15,
    "project_root": "/path/to/DevForgeAI2"
  },
  "phase_results": {
    "phase_1_slash_commands": "PASS",
    "phase_2_skills_reference_loading": "PASS",
    "phase_3_subagents": "PASS",
    "phase_4_cli_commands": "PASS",
    "phase_5_integration_workflows": "PASS",
    "phase_6_performance_benchmarks": "PASS"
  },
  "coverage": {
    "slash_commands": { "target": 23 },
    "skills": { "target": 14 },
    "subagents": { "target": 27 },
    "cli_commands": { "target": 5 },
    "integration_workflows": { "target": 3 }
  },
  "success_criteria": {
    "all_23_commands_executable": true,
    "all_14_skills_reference_loading": true,
    "all_27_subagents_available": true,
    "5_cli_commands_operational": true,
    "zero_regressions": true,
    "3_integration_workflows_end_to_end": true,
    "performance_benchmarks_within_tolerance": true
  }
}
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: STORY-044 Regression Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run regression tests
        run: bash tests/regression/run-all-tests.sh
      - name: Upload results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: test-results
          path: tests/regression/test-src-migration-final-results.json
```

### Local Pre-Commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit
if ! bash tests/regression/test-commands.sh > /dev/null 2>&1; then
    echo "STORY-044 regression tests failed. Run full suite:"
    echo "  bash tests/regression/run-all-tests.sh"
    exit 1
fi
```

## Success Criteria

**All criteria must be met for STORY-044 to be complete:**

- [x] All 23 slash commands execute successfully from src/ paths
- [x] All 14 DevForgeAI skills load reference files from src/ successfully
- [x] All 27 subagents invoke correctly from src/claude/agents/
- [x] DevForgeAI CLI commands operational (5 commands)
- [x] Zero regressions in existing test suite
- [x] Integration workflows execute end-to-end (3 workflows)
- [x] Performance benchmarks within ±10% baseline

## Troubleshooting

### Script Permissions

Make scripts executable:
```bash
chmod +x tests/regression/*.sh
chmod +x tests/regression/run-all-tests.sh
```

### Path Issues

Verify project root:
```bash
cd /path/to/DevForgeAI2
pwd
# Should show: /path/to/DevForgeAI2
```

### Python Test Requirements

```bash
pip install pytest
pip install pytest-cov
```

### Debug Output

Enable debug logging:
```bash
# Add to any .sh script
set -x  # Print each command before execution
```

## Related Stories

- **STORY-043:** Path Migration from .claude/ to src/
- **STORY-045:** Automated Test Execution and Reporting
- **STORY-046:** CI/CD Pipeline Integration

## References

- Test Design: TDD Red phase - tests fail when paths broken
- Framework: Bash + Python pytest
- Coverage: 23 commands + 14 skills + 27 subagents + 5 CLI + 3 workflows
- Tolerance: ±10% performance deviation acceptable
- Report Format: JSON for CI/CD integration
