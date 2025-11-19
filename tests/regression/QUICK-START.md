# STORY-044 Regression Tests - Quick Start Guide

## In 30 Seconds

```bash
# Make scripts executable (one-time)
chmod +x tests/regression/*.sh

# Run all tests (15-30 seconds)
bash tests/regression/run-all-tests.sh

# View results
cat tests/regression/test-src-migration-final-results.json | jq .
```

## Test Suite Overview

| Phase | Script | Purpose | Time |
|-------|--------|---------|------|
| 1 | test-commands.sh | 23 slash commands | 2-3s |
| 2 | test-skills-reference-loading.sh | 14 skills + refs | 3-4s |
| 3 | test-subagents.sh | 27 subagents | 2-3s |
| 4 | test-cli-commands.sh | 5 CLI commands | 1-2s |
| 5 | test-integration-workflows.sh | 3 workflows | 2-3s |
| 6 | test-performance-benchmarks.sh | 6 benchmarks | 3-5s |
| **Total** | **run-all-tests.sh** | **All phases** | **15-30s** |

## What Tests Validate

**FAIL when:**
- ❌ Command files missing or < 100 bytes
- ❌ Skill SKILL.md files not found
- ❌ Subagent files missing
- ❌ CLI commands not available
- ❌ Integration workflow paths broken
- ❌ Directory structure incomplete

**PASS when:**
- ✅ All files exist at correct paths
- ✅ File content valid (readable, >100 bytes)
- ✅ Directory structure complete
- ✅ Integration workflows accessible
- ✅ Performance within ±10% tolerance

## Expected Output

### Success
```
================================================================================
STORY-044: Comprehensive Testing of src/ Structure
================================================================================

[PHASE 1] Slash Commands (23)
[PASS] ✓ All 23 commands verified

[PHASE 2] Skills Reference Loading (14)
[PASS] ✓ All 14 skills verified

[PHASE 3] Subagents (27)
[PASS] ✓ All 27 subagents verified

[PHASE 4] CLI Commands (5)
[PASS] ✓ CLI commands verified

[PHASE 5] Integration Workflows (3)
[PASS] ✓ All 3 workflows verified

[PHASE 6] Performance Benchmarks
[PASS] ✓ Performance within tolerance

================================================================================
✓ All test phases PASSED
================================================================================
```

### Failure Example
```
[PHASE 1] Slash Commands (23)
[FAIL] Command file missing: /dev
       Path: /path/to/DevForgeAI2/.claude/commands/dev.md

[FAIL] ✗ 1 command(s) failed

================================================================================
✗ Some test phases FAILED
================================================================================
```

## Individual Test Commands

```bash
# Test just commands (23)
bash tests/regression/test-commands.sh

# Test just skills (14)
bash tests/regression/test-skills-reference-loading.sh

# Test just subagents (27)
bash tests/regression/test-subagents.sh

# Test just CLI (5)
bash tests/regression/test-cli-commands.sh

# Test just workflows (3)
bash tests/regression/test-integration-workflows.sh

# Test just performance (6)
bash tests/regression/test-performance-benchmarks.sh

# Python unit tests
python -m pytest src/claude/scripts/tests/test_src_migration.py -v
```

## Interpreting Results

### Green [PASS]
```
[PASS] ✓ Command file exists: /dev (12450 bytes)
```
✅ Test passed - file found and valid

### Red [FAIL]
```
[FAIL] Command file missing: /dev
       Path: .claude/commands/dev.md (NOT FOUND)
```
❌ Test failed - file not found at expected path

### Yellow [WARN]
```
[WARN] devforgeai CLI not found in PATH
```
⚠️ Informational - optional component not installed (tests continue)

### Blue [INFO]
```
[INFO] ✓ Skill has 8 reference files: devforgeai-qa
```
ℹ️ Informational - additional metadata

## Troubleshooting

### Scripts not executable
```bash
chmod +x tests/regression/*.sh
bash tests/regression/run-all-tests.sh
```

### Project root incorrect
```bash
cd /path/to/DevForgeAI2  # Must be project root
pwd  # Should show DevForgeAI2
bash tests/regression/run-all-tests.sh
```

### Python tests need pytest
```bash
pip install pytest
python -m pytest src/claude/scripts/tests/test_src_migration.py -v
```

### CLI tests skip
```bash
# If devforgeai CLI not installed, tests skip gracefully
# To install: pip install --break-system-packages -e .claude/scripts/
pip install --break-system-packages -e .claude/scripts/
bash tests/regression/test-cli-commands.sh
```

## Key Files

```
tests/regression/
├── run-all-tests.sh                   ← Master runner (start here)
├── test-src-migration.sh              ← Integrated 6-phase tester
├── test-commands.sh                   ← Phase 1
├── test-skills-reference-loading.sh   ← Phase 2
├── test-subagents.sh                  ← Phase 3
├── test-cli-commands.sh               ← Phase 4
├── test-integration-workflows.sh       ← Phase 5
├── test-performance-benchmarks.sh      ← Phase 6
├── README-STORY-044.md                ← Full documentation
└── QUICK-START.md                     ← This file

src/claude/scripts/tests/
└── test_src_migration.py              ← Python unit tests
```

## Coverage Summary

| Component | Count | Tests | Status |
|-----------|-------|-------|--------|
| Slash commands | 23 | 23 | FAIL→PASS |
| DevForgeAI skills | 14 | 14+ | FAIL→PASS |
| Subagents | 27 | 27 | FAIL→PASS |
| CLI commands | 5 | 5 | FAIL→PASS |
| Workflows | 3 | 18+ | FAIL→PASS |
| Performance | 6 | 6 | INFO |
| **Total** | | **52+** | **All tests** |

## JSON Report

After running `run-all-tests.sh`, check:
```bash
cat tests/regression/test-src-migration-final-results.json | jq .
```

Example output:
```json
{
  "phase_results": {
    "phase_1_slash_commands": "PASS",
    "phase_2_skills_reference_loading": "PASS",
    "phase_3_subagents": "PASS",
    "phase_4_cli_commands": "PASS",
    "phase_5_integration_workflows": "PASS",
    "phase_6_performance_benchmarks": "PASS"
  }
}
```

## Next Steps

1. **Run tests:** `bash tests/regression/run-all-tests.sh`
2. **Check results:** All phases should show PASS
3. **Read results:** View JSON report for metrics
4. **Proceed:** If all pass, STORY-044 complete

## Documentation

- **Full Guide:** `tests/regression/README-STORY-044.md`
- **Test Design:** `STORY-044-TEST-DELIVERABLES.md`
- **Troubleshooting:** Detailed section in README-STORY-044.md
- **CI/CD:** GitHub Actions example in README-STORY-044.md

## Support

**Issue:** Tests failing?
**Solution:** Check README-STORY-044.md section "Test Failure Diagnosis"

**Issue:** Scripts not executable?
**Solution:** `chmod +x tests/regression/*.sh`

**Issue:** Python tests fail?
**Solution:** `pip install pytest` then retry

---

**TL;DR:** Run `bash tests/regression/run-all-tests.sh` and wait 30 seconds.
