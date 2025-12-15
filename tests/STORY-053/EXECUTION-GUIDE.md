# STORY-053 Test Suite - Execution Guide

## Quick Start

### Run All Tests at Once
```bash
bash tests/STORY-053/run_all_tests.sh
```

### Run Individual Test Suites
```bash
# Test 1: Pattern Structure (Bash)
bash tests/STORY-053/test-pattern-structure.sh

# Test 2: Template Syntax (Python3)
python3 tests/STORY-053/test-template-syntax.py

# Test 3: Quantification Table (Python3)
python3 tests/STORY-053/test-quantification-table.py

# Test 4: Skill Integration (Bash)
bash tests/STORY-053/test-skill-integration.sh

# Test 5: Framework Alignment (Bash)
bash tests/STORY-053/test-framework-alignment.sh

# Test 6: Performance & NFR (Python3)
python3 tests/STORY-053/test-performance.py
```

---

## Test Files Overview

### File Manifest
```
tests/STORY-053/
├── run_all_tests.sh              # Master test runner
├── test-pattern-structure.sh      # AC#1 validation (14 tests)
├── test-template-syntax.py        # AC#2 validation (15 tests)
├── test-quantification-table.py   # AC#3 validation (14 tests)
├── test-skill-integration.sh      # AC#4 validation (14 tests)
├── test-framework-alignment.sh    # AC#5 validation (11 tests)
├── test-performance.py            # NFR validation (8 tests)
├── TEST-README.md                 # Comprehensive documentation
├── INTEGRATION-CHECKLIST.md       # Integration matrix
├── EXECUTION-GUIDE.md             # This file
└── test-results.txt               # Test output (generated)
```

### Lines of Code
```
test-pattern-structure.sh      ~280 lines
test-template-syntax.py        ~350 lines
test-quantification-table.py   ~350 lines
test-skill-integration.sh      ~280 lines
test-framework-alignment.sh    ~280 lines
test-performance.py            ~280 lines
run_all_tests.sh               ~100 lines
---
TOTAL:                        ~1,900 lines of test code
```

---

## Test Execution Scenarios

### Scenario 1: RED Phase (Before Implementation)
**File Status**: Does not exist
**Expected Result**: ~8/76 tests passing (file existence checks only)

```bash
$ bash tests/STORY-053/run_all_tests.sh

[Output shows file not found warnings for all suites]

Test 1: test-pattern-structure.sh
  ✗ FAIL: File does not exist: src/claude/skills/devforgeai-ideation/references/user-input-guidance.md

Test 2: test-template-syntax.py
  ✗ FAIL: Guidance file does not exist

[... etc.]

Result: 0/76 tests passing (all FAIL - RED PHASE expected)
```

### Scenario 2: Partial Implementation
**File Status**: Created but incomplete (only patterns, no templates)
**Expected Result**: ~30-40/76 tests passing

```bash
$ bash tests/STORY-053/run_all_tests.sh

Test 1: test-pattern-structure.sh
  ✓ PASS: File exists
  ✓ PASS: Found 12 patterns (10-15 required)
  ✓ PASS: All 12 patterns have Problem sections
  ... [14/14 PASS]

Test 2: test-template-syntax.py
  ✓ PASS: File exists
  ✗ FAIL: Found 0 templates (need 20-30)
  ... [2/15 FAIL]

[... incomplete results for other suites]

Result: ~30/76 tests passing (partial GREEN, partial RED)
```

### Scenario 3: Complete Implementation
**File Status**: Fully complete with all sections
**Expected Result**: 76/76 tests passing (100%)

```bash
$ bash tests/STORY-053/run_all_tests.sh

Test 1: test-pattern-structure.sh
  ✓ PASS: File exists
  ✓ PASS: Found 12 patterns (10-15 required)
  ... [14/14 PASS]

Test 2: test-template-syntax.py
  ✓ PASS: Found 25 templates (20-30 required)
  ... [15/15 PASS]

Test 3: test-quantification-table.py
  ✓ PASS: Found 18 vague terms (≥15 required)
  ... [14/14 PASS]

Test 4: test-skill-integration.sh
  ✓ PASS: Found integration references for 5 skills
  ... [14/14 PASS]

Test 5: test-framework-alignment.sh
  ✓ PASS: All 6 context files referenced
  ... [11/11 PASS]

Test 6: test-performance.py
  ✓ PASS: File loads in 42ms (< 500ms required)
  ... [8/8 PASS]

Result: 76/76 tests passing (100% - GREEN PHASE!)
```

---

## Step-by-Step Execution Plan

### Step 1: Initial Setup
```bash
# Verify test files exist
ls -la tests/STORY-053/

# Make test runner executable
chmod +x tests/STORY-053/run_all_tests.sh
chmod +x tests/STORY-053/test-pattern-structure.sh
chmod +x tests/STORY-053/test-skill-integration.sh
chmod +x tests/STORY-053/test-framework-alignment.sh

# Verify Python3 is available
python3 --version   # Should be 3.9+

# Verify Bash is available
bash --version      # Should be 4.0+
```

### Step 2: Initial Test Run (Before Implementation)
```bash
# Run tests to confirm they fail (RED phase expected)
bash tests/STORY-053/run_all_tests.sh

# Expected: File not found errors from all suites
# This confirms tests are working correctly in RED phase
```

### Step 3: Create Stub File
```bash
# Create the file (initially empty)
mkdir -p src/claude/skills/devforgeai-ideation/references/
touch src/claude/skills/devforgeai-ideation/references/user-input-guidance.md

# Run tests again
bash tests/STORY-053/run_all_tests.sh

# Expected: Still failing but file exists checks pass
# File exists: ~8/76 PASS, rest FAIL
```

### Step 4: Add Content Incrementally
```bash
# Phase 1: Add patterns (10-15 with all sections)
# Edit: src/claude/skills/devforgeai-ideation/references/user-input-guidance.md
# Add patterns with: Problem, Solution, Template, Example sections

bash tests/STORY-053/test-pattern-structure.sh
# Expected: 14/14 PASS

# Phase 2: Add templates (20-30 AskUserQuestion templates)
# Add 20-30 templates with: question, header, options, multiSelect

python3 tests/STORY-053/test-template-syntax.py
# Expected: 15/15 PASS

# Phase 3: Add quantification table (≥15 vague terms)
# Add table with: Term, Measurable Range, Example, Template columns

python3 tests/STORY-053/test-quantification-table.py
# Expected: 14/14 PASS

# Phase 4: Add skill integration sections (5 skills)
# Add integration docs for: ideation, story-creation, architecture, ui-generator, orchestration

bash tests/STORY-053/test-skill-integration.sh
# Expected: 14/14 PASS

# Phase 5: Add framework terminology
# Reference: context files, quality gates, workflow states, story structure

bash tests/STORY-053/test-framework-alignment.sh
# Expected: 11/11 PASS

# Phase 6: Verify performance
# Ensure file is <500KB and well-structured

python3 tests/STORY-053/test-performance.py
# Expected: 8/8 PASS
```

### Step 5: Final Validation
```bash
# Run all tests once more
bash tests/STORY-053/run_all_tests.sh

# Expected: 76/76 tests PASS (100%)
# All AC #1-5 validated
# All NFRs validated
```

---

## Understanding Test Output

### PASS Message Format
```
✓ PASS: [Description of what passed]
```
Example:
```
✓ PASS: Found 12 patterns (10-15 required)
✓ PASS: All 12 patterns have Problem sections
```

### FAIL Message Format
```
✗ FAIL: [Description of what failed and why]
```
Example:
```
✗ FAIL: Found 8 patterns (need 10-15)
✗ FAIL: Only 10/12 patterns have Problem sections
```

### SKIP Message Format
```
⊘ SKIP: [Description of test that was skipped]
```
Example:
```
⊘ SKIP: Pattern content quality validation
```

### Summary Output
```
================================================================
AC1: Pattern Completeness
================================================================

Test 1: File exists at expected location
✓ PASS: File exists: src/claude/skills/devforgeai-ideation/references/user-input-guidance.md

Test 2: Pattern count is within range (10-15)
✓ PASS: Found 12 patterns (10-15 required)

[... more tests ...]

================================================================
Summary
================================================================

Total Tests: 14
Passed: 14
Failed: 0

Result: ALL TESTS PASSED
```

---

## Troubleshooting

### Issue: "File does not exist"
**Cause**: `user-input-guidance.md` has not been created yet
**Solution**:
```bash
mkdir -p src/claude/skills/devforgeai-ideation/references/
touch src/claude/skills/devforgeai-ideation/references/user-input-guidance.md
```

### Issue: "python3: command not found"
**Cause**: Python3 not in PATH
**Solution**:
```bash
# Find python3
which python3

# If not found, install Python3 (depends on OS):
# macOS: brew install python3
# Ubuntu: sudo apt-get install python3
# Windows: https://www.python.org/downloads/

# Verify installation
python3 --version
```

### Issue: "Permission denied" on test scripts
**Cause**: Scripts don't have execute permission
**Solution**:
```bash
chmod +x tests/STORY-053/*.sh
```

### Issue: Pattern count shows 0 but patterns exist
**Cause**: Pattern headings use wrong format
**Solution**:
Verify patterns use markdown heading format:
```markdown
### Pattern 1: [Name]  ← Correct format

## Pattern 1: [Name]   ← Wrong (needs 3 #'s)

Pattern 1: [Name]     ← Wrong (no heading)
```

### Issue: Template syntax test shows 0 templates
**Cause**: Template blocks don't use `AskUserQuestion(` pattern
**Solution**:
Verify templates use proper format:
```python
AskUserQuestion(
    questions=[{
        question: "...",
        header: "...",
        options: [...],
        multiSelect: false
    }]
)
```

### Issue: Quantification table test fails
**Cause**: Table doesn't use markdown format or missing data
**Solution**:
Verify table format:
```markdown
| Vague Term | Measurable Range | Example | Template |
|------------|------------------|---------|----------|
| fast       | < 200ms          | [Ex]    | [Link]   |
| scalable   | ≥ 1M users       | [Ex]    | [Link]   |
```

### Issue: Integration tests show 0 skills
**Cause**: Skill names not in file
**Solution**:
Verify file contains references to all 5 skills:
```
- devforgeai-ideation
- devforgeai-story-creation
- devforgeai-architecture
- devforgeai-ui-generator
- devforgeai-orchestration
```

---

## Performance Benchmarks

### Expected Execution Times
```
test-pattern-structure.sh      ~2 seconds
test-template-syntax.py        ~3 seconds
test-quantification-table.py   ~3 seconds
test-skill-integration.sh      ~2 seconds
test-framework-alignment.sh    ~2 seconds
test-performance.py            ~1 second
---
Total (all tests):            ~13 seconds
```

### File Performance Targets
```
File Load Time:     < 500ms    (actual: typically 10-50ms)
Grep Search Time:   < 30s      (actual: typically <100ms)
Token Count:        ≤ 3,000    (actual: ~2,500-2,800 tokens)
File Size:          < 500KB    (target: ~100-150KB)
```

---

## Continuous Integration

### Git Hook Integration
To run tests automatically before commit:

```bash
# Create pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# Run STORY-053 tests before commit
bash tests/STORY-053/run_all_tests.sh
if [ $? -ne 0 ]; then
  echo "STORY-053 tests failed - commit blocked"
  exit 1
fi
EOF

chmod +x .git/hooks/pre-commit
```

### CI/CD Pipeline Integration
```yaml
# Example GitHub Actions workflow
- name: Run STORY-053 Tests
  run: bash tests/STORY-053/run_all_tests.sh

- name: Check Test Results
  run: |
    if [ $(grep -c "PASS" test-results.txt) -ne 76 ]; then
      echo "Not all tests passed"
      exit 1
    fi
```

---

## Documentation References

### Related Files
- **Story Definition**: `devforgeai/specs/Stories/STORY-053-framework-internal-guidance-reference.story.md`
- **Test Documentation**: `tests/STORY-053/TEST-README.md`
- **Integration Matrix**: `tests/STORY-053/INTEGRATION-CHECKLIST.md`
- **Target File**: `src/claude/skills/devforgeai-ideation/references/user-input-guidance.md`

### Framework References
- **CLAUDE.md**: Core framework documentation
- **Tech Stack**: `devforgeai/context/tech-stack.md`
- **Source Tree**: `devforgeai/context/source-tree.md`
- **Prompting Guide**: `src/claude/memory/effective-prompting-guide.md`

---

## Quick Reference: Test Commands

```bash
# All tests
bash tests/STORY-053/run_all_tests.sh

# Individual tests (in dependency order)
bash tests/STORY-053/test-pattern-structure.sh && \
python3 tests/STORY-053/test-template-syntax.py && \
python3 tests/STORY-053/test-quantification-table.py && \
bash tests/STORY-053/test-skill-integration.sh && \
bash tests/STORY-053/test-framework-alignment.sh && \
python3 tests/STORY-053/test-performance.py

# Parallel execution (faster)
bash tests/STORY-053/test-pattern-structure.sh &
python3 tests/STORY-053/test-template-syntax.py &
python3 tests/STORY-053/test-quantification-table.py &
bash tests/STORY-053/test-skill-integration.sh &
bash tests/STORY-053/test-framework-alignment.sh &
python3 tests/STORY-053/test-performance.py &
wait

# Count passing tests
bash tests/STORY-053/run_all_tests.sh 2>&1 | grep "PASS:" | wc -l

# Count failing tests
bash tests/STORY-053/run_all_tests.sh 2>&1 | grep "FAIL:" | wc -l

# Show only failures
bash tests/STORY-053/run_all_tests.sh 2>&1 | grep "FAIL:"

# Show test summary
bash tests/STORY-053/run_all_tests.sh 2>&1 | tail -20
```

---

## Success Criteria Checklist

When all tests pass, verify:

- [ ] Total Tests: 76
- [ ] Tests Passed: 76
- [ ] Tests Failed: 0
- [ ] Success Rate: 100%

By Test Suite:
- [ ] Pattern Structure: 14/14 ✓
- [ ] Template Syntax: 15/15 ✓
- [ ] Quantification Table: 14/14 ✓
- [ ] Skill Integration: 14/14 ✓
- [ ] Framework Alignment: 11/11 ✓
- [ ] Performance & NFR: 8/8 ✓

By Acceptance Criterion:
- [ ] AC#1 Pattern Completeness: PASS ✓
- [ ] AC#2 Template Usability: PASS ✓
- [ ] AC#3 NFR Quantification: PASS ✓
- [ ] AC#4 Skill Integration: PASS ✓
- [ ] AC#5 Framework Alignment: PASS ✓

By NFR Category:
- [ ] Performance (NFR-001, 002, 003): PASS ✓
- [ ] Usability (NFR-004, 005): PASS ✓
- [ ] Maintainability (NFR-006): PASS ✓
- [ ] Quality (NFR-007, 008): PASS ✓
- [ ] Reusability (NFR-009): PASS ✓
- [ ] Scalability (NFR-010): PASS ✓

---

**Version**: 1.0
**Created**: 2025-01-20
**Last Updated**: 2025-01-20
