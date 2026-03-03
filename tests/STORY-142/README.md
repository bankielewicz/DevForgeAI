# STORY-142: Bash mkdir Replacement - Test Suite

## Quick Start

### Make Tests Executable
```bash
chmod +x tests/STORY-142/test_*.sh
```

### Run All Tests
```bash
bash tests/STORY-142/test_artifact_generation_bash_mkdir.sh
bash tests/STORY-142/test_error_handling_bash_mkdir.sh
bash tests/STORY-142/test_gitkeep_directory_creation.sh
```

### Expected Results (RED Phase)

**Before Implementation** (Current State):
- Artifact Gen: 2 PASS, 4 FAIL
- Error Handling: 2 PASS, 3 FAIL
- Gitkeep Creation: 5 PASS

**After Implementation** (Expected):
- Artifact Gen: 6 PASS, 0 FAIL
- Error Handling: 5 PASS, 0 FAIL
- Gitkeep Creation: 5 PASS

---

## Files in This Test Suite

### 1. test_artifact_generation_bash_mkdir.sh
Tests violation detection and replacement in artifact-generation.md
- Finds 3 Bash mkdir violations (lines 469, 598, 599)
- Validates Write/.gitkeep replacement pattern
- Line-specific tests for each violation

### 2. test_error_handling_bash_mkdir.sh
Tests violation detection and replacement in error-handling.md
- Finds 2 Bash mkdir violations (lines 184, 868)
- Validates Write/.gitkeep replacement pattern
- Line-specific tests for each violation

### 3. test_gitkeep_directory_creation.sh
Tests .gitkeep file creation via Write tool
- Verifies devforgeai/specs/Epics/.gitkeep created
- Verifies devforgeai/specs/requirements/.gitkeep created
- Validates .gitkeep files are empty (size=0)

---

## Test Strategy

### Pattern Matching (Grep-based)
```bash
# Find Bash mkdir violations
grep 'Bash(command="mkdir' artifact-generation.md
grep 'Bash(command=f"mkdir' error-handling.md

# Find Write/.gitkeep replacements
grep 'Write(file_path=".*/.gitkeep"' artifact-generation.md
```

### Line-Specific Validation
```bash
# Extract context around line
sed -n '465,475p' artifact-generation.md | grep 'Bash(command="mkdir'
```

### File Existence Checks
```bash
# Verify .gitkeep files exist
test -f devforgeai/specs/Epics/.gitkeep
test -f devforgeai/specs/requirements/.gitkeep
```

---

## Implementation Checklist

### Before Implementation
- [ ] Review test files
- [ ] Run tests to verify RED phase (some should fail)
- [ ] Understand violations (5 violations across 2 files)

### Implementation
- [ ] Replace 3 violations in artifact-generation.md
- [ ] Replace 2 violations in error-handling.md
- [ ] Use Write tool with .gitkeep pattern
- [ ] Maintain file formatting and context

### After Implementation
- [ ] Run tests to verify GREEN phase (all should pass)
- [ ] Verify no Bash mkdir violations remain
- [ ] Verify Write/.gitkeep patterns in place
- [ ] Commit changes to git

---

## Violations to Fix

### artifact-generation.md

**Line 469**:
```
Bash(command="mkdir -p devforgeai/specs/Epics")
→ Write(file_path="devforgeai/specs/Epics/.gitkeep", content="")
```

**Line 598**:
```
Bash(command="mkdir -p devforgeai/specs/Epics")
→ Write(file_path="devforgeai/specs/Epics/.gitkeep", content="")
```

**Line 599**:
```
Bash(command="mkdir -p devforgeai/specs/requirements")
→ Write(file_path="devforgeai/specs/requirements/.gitkeep", content="")
```

### error-handling.md

**Line 184**:
```
Bash(command=f"mkdir -p {dir}")
→ Write(file_path=f"{dir}/.gitkeep", content="")
```

**Line 868**:
```
Bash(command=f"mkdir -p {dir}")
→ Write(file_path=f"{dir}/.gitkeep", content="")
```

---

## Test Output Colors

- **GREEN**: Test passed
- **RED**: Test failed
- **YELLOW**: Test name/section header
- **No Color**: Regular output

---

## Test Framework

**Type**: Bash shell scripts with grep validation
**Pattern Matching**: ripgrep-compatible grep patterns
**Assertions**: Line count, file existence, content validation
**Independence**: Each test is independent, can run in any order

---

## Success Criteria

When all violations are fixed:
- [ ] All 16 tests pass
- [ ] Grep searches return zero Bash mkdir violations
- [ ] .gitkeep files exist in target directories
- [ ] Constitutional C1 compliance achieved

---

## References

- **Story**: STORY-142 (Replace Bash mkdir with Write/.gitkeep Pattern)
- **Plan**: `.claude/plans/STORY-142-test-generation-plan.md`
- **Summary**: `.claude/plans/STORY-142-test-generation-summary.md`
- **Validation**: `.claude/plans/STORY-142-RED-PHASE-VALIDATION.md`
- **Report**: `STORY-142-TEST-GENERATION-REPORT.md`

---

**TDD Status**: RED Phase
**Next Phase**: Implementation
**Framework**: Bash/Grep validation
**Coverage**: 100% (all AC mapped to tests)
