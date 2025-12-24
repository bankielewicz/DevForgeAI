# STORY-134 Test Suite Index

**Story:** Smart Greenfield/Brownfield Detection
**Status:** Test Generation Complete (Red Phase - All Tests FAILING)
**Created:** 2025-12-24

---

## Overview

This test suite validates the smart greenfield/brownfield detection feature for the `/ideate` command. The feature automatically detects whether a project is greenfield (no context files) or brownfield (has 6+ context files) and passes this mode to the skill for intelligent next-step recommendations.

**Test Framework:** Bash (native to Claude Code)
**Total Tests:** 29
**Expected Status:** All FAILING (TDD Red Phase - feature not yet implemented)

---

## Test Files

| File | Purpose | Test Count | Status |
|------|---------|-----------|--------|
| `test-ac1-brownfield-detection.sh` | AC#1: Brownfield detection (6 context files) | 7 | FAILING |
| `test-ac2-greenfield-detection.sh` | AC#2: Greenfield detection (<6 context files) | 7 | FAILING |
| `test-ac3-context-passing.sh` | AC#3: Mode context passing to skill | 10 | FAILING |
| `test-ac4-performance.sh` | AC#4: Performance and consistency | 7 | FAILING |
| **Total** | | **29** | **FAILING** |

---

## Test Details

### Test AC#1: Brownfield Detection (`test-ac1-brownfield-detection.sh`)

**Scenario:** 6 context files present → brownfield mode detected

Tests validate:
- 1.1: All 6 context files exist (tech-stack.md, source-tree.md, dependencies.md, coding-standards.md, architecture-constraints.md, anti-patterns.md)
- 1.2: Glob check in ideate.md Phase 1
- 1.3: Mode determination logic (6 files = brownfield)
- 1.4: Context marker passed to skill
- 1.5: Detection latency <50ms
- 1.6: Mode marker format correctness
- 1.7: Next action suggestion for brownfield (/orchestrate recommended)

**Expected Outcome:** All tests PASS after implementation

---

### Test AC#2: Greenfield Detection (`test-ac2-greenfield-detection.sh`)

**Scenario:** <6 context files present → greenfield mode detected

Tests validate:
- 2.1: Mode determination logic (< 6 files = greenfield)
- 2.2: Greenfield mode marker display
- 2.3: Greenfield-specific guidance provided (/create-context recommended)
- 2.4: File count display
- 2.5: Zero context files scenario
- 2.6: Partial context files (5/6) - greenfield not brownfield
- 2.7: Consistency across multiple invocations

**Expected Outcome:** All tests PASS after implementation

---

### Test AC#3: Context Passing (`test-ac3-context-passing.sh`)

**Scenario:** Detected mode passed to skill, skill Phase 6.6 uses it for next-action

Tests validate:
- 3.1: Context marker header display ("Project Mode Context")
- 3.2: Mode value display (**Mode:** greenfield|brownfield)
- 3.3: Context files count display
- 3.4: Detection method documented
- 3.5: Skill Phase 6.6 references mode
- 3.6: Greenfield path in Phase 6.6 (/create-context recommended)
- 3.7: Brownfield path in Phase 6.6 (/orchestrate recommended)
- 3.8: Mode marker parseability
- 3.9: Context marker timing (before Skill() invocation)
- 3.10: Mode-based decision in skill (not hardcoded in command)

**Expected Outcome:** All tests PASS after implementation

---

### Test AC#4: Performance & Consistency (`test-ac4-performance.sh`)

**Scenario:** Detection is fast (<50ms) and deterministic

Tests validate:
- 4.1: Exact count comparison (== 6 brownfield, < 6 greenfield)
- 4.2: Latency <50ms (p95 measurement)
- 4.3: Consistency across invocations (same state = same result)
- 4.4: Edge case - extra context files (>6 treated as brownfield)
- 4.5: No caching side effects (detects filesystem changes)
- 4.6: Glob pattern specification
- 4.7: Deterministic detection (no randomness)

**Expected Outcome:** All tests PASS after implementation

---

## Running the Tests

### Run All Tests

```bash
cd /mnt/c/Projects/DevForgeAI2/devforgeai/tests/STORY-134/

# Run each test file
./test-ac1-brownfield-detection.sh
./test-ac2-greenfield-detection.sh
./test-ac3-context-passing.sh
./test-ac4-performance.sh

# Or run all at once
for test in test-*.sh; do bash "$test"; echo ""; done
```

### Expected Output

Each test will display:
- Red (✗ FAIL) indicators for all assertions
- Reasons for failures (feature not yet implemented)
- Test counters showing all tests failed

Example:
```
✗ FAIL: ideate.md contains Glob check for context files in Phase 1
  Not found in: .claude/commands/ideate.md
  Search text: Glob.*pattern.*devforgeai/specs/context
```

---

## Implementation Checklist

Before tests will PASS, the following must be implemented:

### In `.claude/commands/ideate.md`

- [ ] Add Glob check in Phase 1: `Glob(pattern="devforgeai/specs/context/*.md")`
- [ ] Count context files: `file_count=$(find devforgeai/specs/context -name "*.md" | wc -l)`
- [ ] Mode determination:
  ```
  if [ "$file_count" -eq 6 ]; then
      mode="brownfield"
  else
      mode="greenfield"
  fi
  ```
- [ ] Display context marker before Skill() invocation:
  ```
  **Project Mode Context:**
  - **Mode:** {mode}
  - **Context Files Found:** {count}/6
  - **Detection Method:** Filesystem glob
  ```
- [ ] Invoke skill with mode marker displayed

### In `.claude/skills/devforgeai-ideation/SKILL.md`

- [ ] Phase 6.6 reads mode from context marker
- [ ] If greenfield: recommend `/create-context [project-name]`
- [ ] If brownfield: recommend `/create-sprint` or `/create-story`

---

## Technical Specifications

### Context File Detection
- **Method:** Filesystem glob on `devforgeai/specs/context/*.md`
- **Files Counted:**
  1. tech-stack.md
  2. source-tree.md
  3. dependencies.md
  4. coding-standards.md
  5. architecture-constraints.md
  6. anti-patterns.md
- **Brownfield Threshold:** == 6 files
- **Greenfield Threshold:** < 6 files
- **Performance Target:** <50ms (p95)

### Mode Marker Format
```
**Project Mode Context:**
- **Mode:** {greenfield|brownfield}
- **Context Files Found:** {count}/6
- **Detection Method:** Filesystem glob
```

### Skill Consumption (Phase 6.6)
- Pattern match: `**Mode:** greenfield` → recommend `/create-context`
- Pattern match: `**Mode:** brownfield` → recommend `/create-sprint` or `/create-story`
- No parsing required, simple string matching sufficient

---

## Test Execution Notes

### TDD Red Phase
All tests in this suite are expected to FAIL initially. This is correct behavior and validates that:
- Test harness works correctly
- Tests target actual missing features
- Tests will guide implementation

### No Fixtures Pre-created
Tests create temporary fixtures as needed:
- AC#2 creates `/tmp/greenfield-test-fixture/` for scenario testing
- AC#4 creates `/tmp/performance-test-fixture/` for performance measurement
- All fixtures cleaned up after test completion

### Real Filesystem Validation
Tests against actual:
- `.claude/commands/ideate.md` file
- `.claude/skills/devforgeai-ideation/SKILL.md` file
- `devforgeai/specs/context/` directory (6 context files exist)

---

## Related Documentation

- **Story:** `/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-134-smart-greenfield-brownfield-detection.story.md`
- **Command:** `/mnt/c/Projects/DevForgeAI2/.claude/commands/ideate.md`
- **Skill:** `/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-ideation/SKILL.md`
- **Context Files:** `/mnt/c/Projects/DevForgeAI2/devforgeai/specs/context/`

---

## Coverage Mapping

| AC | Tests | Coverage |
|----|-------|----------|
| AC#1: Brownfield Detection | test-ac1-brownfield-detection.sh (7 tests) | 100% |
| AC#2: Greenfield Detection | test-ac2-greenfield-detection.sh (7 tests) | 100% |
| AC#3: Context Passing | test-ac3-context-passing.sh (10 tests) | 100% |
| AC#4: Performance | test-ac4-performance.sh (7 tests) | 100% |
| **Total** | **29 tests** | **100%** |

---

## Next Steps (TDD Green Phase)

Once all tests FAIL as expected:

1. **Phase 03 (Green):** Implement feature in ideate.md and skill
2. **Phase 04 (Refactor):** Improve code quality, optimize latency
3. **Phase 05 (Integration):** Validate cross-component interactions
4. **Phase 08 (Git):** Commit implementation with passing tests

---

## Notes

- Tests are Bash-based for maximum compatibility with Claude Code
- No external dependencies required (standard Unix tools only)
- Tests validate both command logic and skill integration
- Performance tests measure actual latency on project filesystem
- All tests use descriptive names for easy debugging

---

**Last Updated:** 2025-12-24
**Test Framework Version:** 1.0
**Compatible Story Version:** 2.3
