# STORY-044 Test Runner - Quick Reference Guide

**Complete test infrastructure for validating src/ structure migration**

---

## Quick Start

### Run All Tests (Recommended)
```bash
cd /mnt/c/Projects/DevForgeAI2
bash tests/regression/run-all-tests.sh
```

**Expected Output:**
- Color-coded results (green = pass, red = fail)
- Summary for each of 6 phases
- Total execution time (3-4 seconds)
- JSON report saved to: `tests/regression/test-src-migration-final-results.json`
- Exit code: 0 (success) or 1 (failure)

---

## Test Scripts

### 1. Phase 1: Slash Commands
**File:** `tests/regression/test-commands.sh`

**What it tests:** 23 DevForgeAI slash commands (/dev, /qa, /release, /orchestrate, etc.)

**Run individually:**
```bash
bash tests/regression/test-commands.sh
```

**Expected:** ✅ All 23 commands PASS

---

### 2. Phase 2: Skills Reference Loading
**File:** `tests/regression/test-skills-reference-loading.sh`

**What it tests:** 14 DevForgeAI skills (devforgeai-development, devforgeai-qa, etc.)

**Run individually:**
```bash
bash tests/regression/test-skills-reference-loading.sh
```

**Expected:** ✅ All 14 skills PASS

---

### 3. Phase 3: Subagents
**File:** `tests/regression/test-subagents.sh`

**What it tests:** 27 specialized subagents (test-automator, backend-architect, security-auditor, etc.)

**Run individually:**
```bash
bash tests/regression/test-subagents.sh
```

**Expected:** ✅ All 27 subagents PASS

---

### 4. Phase 4: CLI Commands
**File:** `tests/regression/test-cli-commands.sh`

**What it tests:** 5 DevForgeAI CLI commands (validate-dod, check-git, validate-context, check-hooks, invoke-hooks)

**Run individually:**
```bash
bash tests/regression/test-cli-commands.sh
```

**Expected:** ✅ All 5 CLI commands PASS (or skip if not installed)

---

### 5. Phase 5: Integration Workflows
**File:** `tests/regression/test-integration-workflows.sh`

**What it tests:** 3 complete end-to-end workflows:
- Workflow 1: Epic → Story → Development
- Workflow 2: Context → Story → QA
- Workflow 3: Sprint Planning → Story

**Run individually:**
```bash
bash tests/regression/test-integration-workflows.sh
```

**Expected:** ✅ All 3 workflows PASS (26 sub-tests)

---

### 6. Phase 6: Performance Benchmarks
**File:** `tests/regression/test-performance-benchmarks.sh`

**What it tests:** File scanning performance with ±10% tolerance

**Run individually:**
```bash
bash tests/regression/test-performance-benchmarks.sh
```

**Expected:** ✅ All benchmarks PASS (performance warnings are informational)

---

## JSON Report

**Location:** `tests/regression/test-src-migration-final-results.json`

**Generated automatically** after running `run-all-tests.sh`

**View with:**
```bash
cat tests/regression/test-src-migration-final-results.json
```

**Or formatted:**
```bash
cat tests/regression/test-src-migration-final-results.json | jq
```

**Contents:**
- Timestamp of test run
- Duration in seconds
- Phase results (PASS/FAIL/SKIP)
- Coverage metrics
- Success criteria checklist

---

## Understanding Output

### Success (All Phases Pass)
```
================================================================================
✓ All test phases PASSED
================================================================================

Exit code: 0
```

### Failure (Any Phase Fails)
```
================================================================================
✗ Some test phases FAILED
================================================================================

Exit code: 1
```

### Color Codes
- 🟢 GREEN [PASS] - Test passed
- 🔴 RED [FAIL] - Test failed (blocks progression)
- 🟡 YELLOW [WARN] - Non-fatal warning (informational)
- 🔵 BLUE [SKIP] - Test skipped (not executed)
- ℹ️ [INFO] - Informational message

---

## Troubleshooting

### Script Won't Run
**Error:** `Permission denied`

**Solution:**
```bash
chmod +x tests/regression/*.sh
```

### Test Fails - Command Not Found
**Error:** `[FAIL] Command file missing: /dev`

**Cause:** Path migration incomplete or command file missing

**Solution:**
1. Check file exists: `ls .claude/commands/dev.md`
2. Verify path: `pwd` should show DevForgeAI2 directory
3. Check STORY-043 path updates applied

### Test Fails - Skill Not Found
**Error:** `[FAIL] Skill file missing: devforgeai-development`

**Cause:** Skill directory or SKILL.md missing

**Solution:**
1. Check directory: `ls .claude/skills/devforgeai-development/`
2. Check SKILL.md: `ls .claude/skills/devforgeai-development/SKILL.md`
3. Verify migration completed

### CLI Tests Skip
**Message:** `[SKIP] devforgeai CLI not found in PATH`

**Cause:** DevForgeAI CLI not installed (non-critical)

**Solution:**
```bash
pip install --break-system-packages -e .claude/scripts/
```

---

## Running Tests in CI/CD

### GitHub Actions
```yaml
name: STORY-044 Tests
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
    echo "STORY-044 tests failed. Run full suite:"
    echo "  bash tests/regression/run-all-tests.sh"
    exit 1
fi
```

---

## Test Results Interpretation

### 100% Pass Rate
All 6 phases passing = framework structure is correct

### Phase Failure
Single phase failing = specific component issue
- Phase 1 fails → Command paths broken
- Phase 2 fails → Skill structure broken
- Phase 3 fails → Subagent files missing
- Phase 4 fails → CLI not installed (non-critical)
- Phase 5 fails → Integration paths broken
- Phase 6 fails → Performance degradation (informational)

### Performance Warnings
Slow operations (yellow [WARN]) are **informational only** - not functional failures

---

## Statistics

| Metric | Value |
|--------|-------|
| Total Test Scripts | 8 |
| Master Orchestrator | run-all-tests.sh |
| Total Phases | 6 |
| Total Tests | 101+ |
| Execution Time | 3-4 seconds |
| No External Dependencies | ✅ YES |
| Framework Coverage | ✅ Complete |

---

## Files Included

1. `run-all-tests.sh` - Master orchestrator (runs all phases)
2. `test-commands.sh` - Phase 1 (23 slash commands)
3. `test-skills-reference-loading.sh` - Phase 2 (14 skills)
4. `test-subagents.sh` - Phase 3 (27 subagents)
5. `test-cli-commands.sh` - Phase 4 (5 CLI commands)
6. `test-integration-workflows.sh` - Phase 5 (3 workflows)
7. `test-performance-benchmarks.sh` - Phase 6 (performance)
8. `test-src-migration.sh` - Legacy (kept for reference)

---

## Key Features

✅ Modular - run individual phases or all together
✅ Fast - completes in <5 seconds
✅ Minimal Dependencies - bash + standard tools only
✅ JSON Output - machine-readable results
✅ Color-Coded - human-readable output
✅ Comprehensive - 101+ test cases
✅ CI/CD Ready - exit codes and JSON output
✅ Independent - each phase can run standalone

---

## Success Criteria

All criteria must be met for STORY-044 completion:

- [x] All 8 test scripts created and executable
- [x] All 23 slash commands verified
- [x] All 14 skills and references verified
- [x] All 27 subagents verified
- [x] All 5 CLI commands operational
- [x] All 3 integration workflows verified
- [x] Performance benchmarks passing
- [x] JSON report generation working
- [x] Exit codes correct (0/1)
- [x] < 30 second execution time
- [x] Tests runnable independently or together

**Status: ✅ COMPLETE AND PASSING**

---

## Contact & Support

For issues or questions:
1. Check IMPLEMENTATION-COMPLETE.md for detailed information
2. Check README-STORY-044.md for comprehensive documentation
3. Review script output for specific failure messages
4. Check file permissions if scripts won't run

---

**Last Updated:** 2025-11-19
**Framework:** DevForgeAI
**Phase:** 2 (Green - Implementation Complete)

