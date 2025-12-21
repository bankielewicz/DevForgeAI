# Phase 2 Week 3 Testing Procedures

**Version:** 1.0
**Date:** 2025-11-07
**Purpose:** Step-by-step procedures for executing Week 3 tests
**Audience:** External testers with Claude API access

---

## Prerequisites Checklist

Before running any tests, verify:

- [ ] Python 3.8+ installed: `python3 --version`
- [ ] anthropic library installed: `pip install anthropic`
- [ ] pyyaml library installed: `pip install pyyaml`
- [ ] ANTHROPIC_API_KEY environment variable set
- [ ] Working directory: `/mnt/c/Projects/DevForgeAI2`

**Setup commands:**
```bash
# Install dependencies
pip install anthropic pyyaml

# Set API key (replace with your actual key)
export ANTHROPIC_API_KEY="sk-ant-api03-your-key-here"

# Verify
python3 -c "import anthropic; print('✅ anthropic ready')"
echo $ANTHROPIC_API_KEY | grep -q "sk-ant" && echo "✅ API key set" || echo "❌ API key not set"

# Navigate to project root
cd /mnt/c/Projects/DevForgeAI2
```

---

## Test Suite Overview

**Total tests:** 35 tests
- Validator tests: 12
- Migration tests: 5
- Accuracy tests: 5
- Integration tests: 8 (documented, manual execution)
- Regression tests: 5 (documented, manual execution)

**Estimated time:** 2-3 hours for complete suite

---

## Part 1: Validator Tests (TC-V1 to TC-V12)

### Quick Test (Automated)

```bash
cd .claude/skills/devforgeai-story-creation/scripts/tests

# Run all validator tests
./run_all_tests.sh

# Expected output:
# ✅ TC-V1 PASSED
# ✅ TC-V2 PASSED (error caught correctly)
# ✅ TC-V3 PASSED (invalid type caught)
# ... (12 total)
#
# Validator Tests: 12/12 passed
# ✅ ALL TESTS PASSED
```

**Success:** 12/12 tests passing

**If failures:** See "Troubleshooting Validator Failures" section below

---

### Manual Test (Individual Test Cases)

**Test each fixture individually:**

```bash
cd .claude/skills/devforgeai-story-creation/scripts

# TC-V1: Valid v2.0 (should PASS with no errors)
python3 validate_tech_spec.py tests/fixtures/TC-V1-valid-v2.story.md

# Expected output:
# ✅ VALIDATION PASSED
#
# No issues found. Technical specification is valid.
#
# Summary:
#   Components: 1
#   Business Rules: 1
#   NFRs: 1
#   Errors: 0
#   Warnings: 0

# TC-V2: Missing format_version (should FAIL)
python3 validate_tech_spec.py tests/fixtures/TC-V2-missing-version.story.md

# Expected output:
# ❌ VALIDATION FAILED
#
# Errors:
#   - Missing 'format_version' field
#
# Summary:
#   ...
#   Errors: 1

# Continue with TC-V3 through TC-V12...
```

**Record results:**
```bash
# Create results log
cat > tests/results/validator-test-results.txt << EOF
TC-V1: PASS (expected: pass)
TC-V2: PASS (expected: fail, error caught)
TC-V3: PASS (expected: fail, invalid type)
...
EOF
```

---

## Part 2: Migration Tests (Test Stories 1-5)

### Test Story 1: Simple (Worker + Configuration)

**Step 1: Migrate with AI (dry-run preview)**
```bash
cd .claude/skills/devforgeai-story-creation/scripts

python3 migrate_story_v1_to_v2.py \
  tests/fixtures/test-story-1-simple-v1.md \
  --ai-assisted \
  --dry-run

# Expected output:
# 🤖 Using AI-assisted conversion (95%+ accuracy)...
# 🔄 Converting test-story-1-simple-v1.md to v2.0 format...
# 🔍 DRY RUN: Would migrate test-story-1-simple-v1.md
#
# --- YAML Tech Spec Preview ---
# technical_specification:
#   format_version: "2.0"
#   components:
#     - type: "Worker"
#       name: "AlertDetectionWorker"
#       file_path: "src/Workers/AlertDetectionWorker.cs"
#       ...
```

**Step 2: Perform actual migration**
```bash
# Create temporary copy for testing
cp tests/fixtures/test-story-1-simple-v1.md tests/results/test-story-1-temp.md

# Migrate (writes to file)
python3 migrate_story_v1_to_v2.py \
  tests/results/test-story-1-temp.md \
  --ai-assisted \
  --validate

# Expected:
# 🤖 Using AI-assisted conversion (95%+ accuracy)...
# 📁 Backup created: devforgeai/backups/phase2-migration/test-story-1-temp-20251107-HHMMSS.md
# 🔄 Converting test-story-1-temp.md to v2.0 format...
# ✅ test-story-1-temp.md: Migrated to v2.0
#
# ✅ MIGRATION SUCCESS: test-story-1-temp.md
#
# 🔍 Running validation...
# ✅ VALIDATION PASSED
#
# No issues found. Technical specification is valid.
```

**Step 3: Measure accuracy**
```bash
# Copy migrated file to results (for accuracy measurement)
cp tests/results/test-story-1-temp.md tests/results/test-story-1-ai-output.md

# Measure accuracy against ground truth
python3 tests/measure_accuracy.py \
  tests/expected/test-story-1-ground-truth.yaml \
  tests/results/test-story-1-ai-output.md

# Expected output:
# ================================================================================
# MIGRATION ACCURACY REPORT
# ================================================================================
#
# Ground Truth: tests/expected/test-story-1-ground-truth.yaml
# AI Output:    tests/results/test-story-1-ai-output.md
#
# Overall Accuracy: 98.5%
# Status: ✅ EXCELLENT (≥95%)
#
# --------------------------------------------------------------------------------
# DETAILED METRICS:
# --------------------------------------------------------------------------------
#   component_detection_rate............................ 100.0%
#   type_classification_accuracy........................ 100.0%
#   name_extraction_accuracy............................ 100.0%
#   requirement_extraction_rate.........................  95.0%
#   test_requirement_quality............................  97.5%
# ================================================================================
```

**Step 4: Manual review**
```bash
# Review AI-generated YAML
cat tests/results/test-story-1-ai-output.md

# Check:
# - Component types correct? (Worker, Configuration)
# - Component names accurate? (AlertDetectionWorker)
# - Requirements specific? (not "Test: Verify it works")
# - YAML valid and parseable?

# Score quality (1-5):
# 5 = Perfect, 4 = Minor issues, 3 = Some issues, 2 = Major issues, 1 = Poor
```

**Record results:**
```
Story 1 Results:
- Migration: SUCCESS
- Validation: PASSED
- Accuracy: 98.5%
- Quality Score: 5/5
- Components: 2/2 detected (100%)
- Status: ✅ EXCELLENT
```

---

### Test Stories 2-5

**Repeat the same 4-step procedure for each:**

**Story 2 (Medium - 5 components):**
```bash
python3 migrate_story_v1_to_v2.py tests/fixtures/test-story-2-medium-v1.md --ai-assisted --dry-run
# ... (same steps as Story 1)
```

**Story 3 (Medium - 4 components):**
```bash
python3 migrate_story_v1_to_v2.py tests/fixtures/test-story-3-medium-v1.md --ai-assisted --dry-run
# ... (same steps)
```

**Story 4 (Complex - 11 components):**
```bash
python3 migrate_story_v1_to_v2.py tests/fixtures/test-story-4-complex-v1.md --ai-assisted --dry-run
# ... (same steps)
# NOTE: This is the critical test - 11 components
```

**Story 5 (Edge - 4 components, vague):**
```bash
python3 migrate_story_v1_to_v2.py tests/fixtures/test-story-5-edge-v1.md --ai-assisted --dry-run
# ... (same steps)
# NOTE: Accuracy expected to be lower (70-85%) due to vague input
```

---

## Part 3: Aggregate Accuracy Calculation

### Calculate Average Accuracy

```bash
cd .claude/skills/devforgeai-story-creation/scripts/tests

# Run all 5 migrations and measure accuracy
for i in {1..5}; do
    echo "=== Test Story $i ==="

    # Copy fixture to results
    cp fixtures/test-story-$i-*.md results/test-story-$i-temp.md

    # Migrate
    python3 ../migrate_story_v1_to_v2.py \
      results/test-story-$i-temp.md \
      --ai-assisted \
      > results/test-story-$i-migration.log 2>&1

    # Rename for accuracy measurement
    mv results/test-story-$i-temp.md results/test-story-$i-ai-output.md

    # Measure accuracy
    python3 measure_accuracy.py \
      expected/test-story-$i-ground-truth.yaml \
      results/test-story-$i-ai-output.md \
      | tee -a results/accuracy-summary.txt

    echo ""
done

# Calculate aggregate
echo "=== AGGREGATE RESULTS ==="
grep "Overall Accuracy:" results/accuracy-summary.txt | \
  awk '{sum+=$3; count++} END {printf "Average Accuracy: %.1f%%\n", sum/count}'

# Expected: Average Accuracy: 96.0% (or similar ≥95%)
```

---

### Results Template

**Record in:** `tests/results/week3-test-results.md`

```markdown
# Week 3 Test Results

**Date:** YYYY-MM-DD
**Tester:** [Your Name]
**API Key:** [Configured: YES/NO]

## Validator Tests (TC-V1 to TC-V12)

| Test | Description | Expected | Actual | Status |
|------|-------------|----------|--------|--------|
| TC-V1 | Valid v2.0 | PASS | PASS | ✅ |
| TC-V2 | Missing version | ERROR | ERROR | ✅ |
| TC-V3 | Invalid type | ERROR | ERROR | ✅ |
| TC-V4 | Missing field | ERROR | ERROR | ✅ |
| TC-V5 | No test req | WARN | WARN | ✅ |
| TC-V6 | Bad format | WARN | WARN | ✅ |
| TC-V7 | Duplicate IDs | ERROR | ERROR | ✅ |
| TC-V8 | All 7 types | PASS | PASS | ✅ |
| TC-V9 | Empty components | ERROR | ERROR | ✅ |
| TC-V10 | Bad YAML | ERROR | ERROR | ✅ |
| TC-V11 | Vague metric | WARN | WARN | ✅ |
| TC-V12 | v1.0 format | WARN | WARN | ✅ |

**Validator Pass Rate:** 12/12 (100%)

## Migration Accuracy Tests

| Story | Complexity | Components | Accuracy | Quality | Status |
|-------|------------|------------|----------|---------|--------|
| Story 1 | Simple | 2 | 98.5% | 5/5 | ✅ |
| Story 2 | Medium | 5 | 96.2% | 5/5 | ✅ |
| Story 3 | Medium | 4 | 95.8% | 4/5 | ✅ |
| Story 4 | Complex | 11 | 93.1% | 4/5 | ✅ |
| Story 5 | Edge | 4 | 78.0% | 3/5 | ✅ |

**Average Accuracy:** 92.3%
**Status:** ⚠️ BELOW TARGET (95%)

**Note:** Adjust these with your actual results!
```

---

## Troubleshooting

### Issue: "⚠️ AI conversion not available"

**Cause:** ANTHROPIC_API_KEY not set or anthropic library not installed

**Solution:**
```bash
# Check API key
echo $ANTHROPIC_API_KEY
# Should output: sk-ant-api03-...

# If empty, set it:
export ANTHROPIC_API_KEY="your-key-here"

# Check anthropic library
python3 -c "import anthropic; print('OK')"

# If ImportError:
pip install anthropic
```

---

### Issue: "Invalid YAML in tech spec" after migration

**Cause:** AI generated malformed YAML

**Solution:**
```bash
# Run with --dry-run to see output
python3 migrate_story_v1_to_v2.py story.md --ai-assisted --dry-run

# Review YAML syntax
# Common issues:
# - Missing quotes on strings with colons
# - Inconsistent indentation
# - Unclosed brackets

# If persistent, refine conversion_prompt_template.txt
```

---

### Issue: Accuracy <90% on test stories

**Cause:** AI not understanding freeform text correctly

**Solution:**
```bash
# 1. Review AI output
cat tests/results/test-story-X-ai-output.md

# 2. Identify pattern:
#    - Components missed?
#    - Types misclassified?
#    - Requirements too generic?

# 3. Refine prompt template
nano .claude/skills/devforgeai-story-creation/scripts/conversion_prompt_template.txt

# 4. Add specific examples or instructions for the failure pattern

# 5. Re-test
python3 migrate_story_v1_to_v2.py tests/fixtures/test-story-X-*.md --ai-assisted --dry-run
```

---

## Test Execution Schedule

### Day 1 of Testing (2 hours)

**09:00-09:30: Setup**
- Install dependencies
- Set API key
- Verify environment

**09:30-10:30: Validator Tests**
- Run run_all_tests.sh
- Record results
- Fix any failures

**10:30-12:00: Migration Test Story 1**
- Migrate with AI
- Measure accuracy
- Manual review
- Record results

---

### Day 2 of Testing (3 hours)

**09:00-11:00: Migration Stories 2-4**
- Test Story 2 (1 hour)
- Test Story 3 (30 min)
- Test Story 4 (30 min - critical complex test)

**11:00-12:00: Migration Story 5 + Aggregate**
- Test Story 5 (edge case)
- Calculate aggregate accuracy
- Generate final report

---

### Day 3 of Testing (1 hour)

**Review and decision:**
- Review all results
- Calculate metrics
- Make GO/NO-GO decision for Week 4

**Decision criteria:**
- If ≥95% average: ✅ GO to Week 4
- If 90-95%: ⚠️ ACCEPTABLE, proceed with caution
- If <90%: 🔄 ITERATE Week 3 (refine prompt)

---

## Success Criteria

### Must Achieve (All Required)

- [ ] Validator tests: 12/12 passing (100%)
- [ ] Migration works for all 5 stories (100% completion)
- [ ] Average accuracy: ≥95%
- [ ] No story <90% accuracy
- [ ] All YAML valid (parseable)

### Should Achieve (4 of 5)

- [ ] Test Story 1 accuracy: ≥98%
- [ ] Test Stories 2-3 accuracy: ≥95%
- [ ] Test Story 4 accuracy: ≥92%
- [ ] Test requirement quality: ≥85% specific
- [ ] Zero critical bugs

### Nice to Have

- [ ] Test Story 5 accuracy: ≥85% (despite vague input)
- [ ] All stories ≥95%
- [ ] Migration time <10 seconds per story

---

## Results Reporting

### Create Final Report

```bash
cat > tests/results/WEEK3-FINAL-REPORT.md << 'EOF'
# Week 3 Testing Final Report

**Date:** YYYY-MM-DD
**Tester:** [Name]
**Duration:** [Hours]

## Summary

- Total Tests: 35
- Passed: __
- Failed: __
- Pass Rate: __%

## Validator Tests

Pass Rate: 12/12 (100%)

## Migration Tests

Average Accuracy: __%

| Story | Expected | Actual | Delta |
|-------|----------|--------|-------|
| Story 1 | 98-100% | __% | __ |
| Story 2 | 95-97% | __% | __ |
| Story 3 | 95-97% | __% | __ |
| Story 4 | 92-96% | __% | __ |
| Story 5 | 70-85% | __% | __ |

## Decision

Based on results: GO / ITERATE / NO-GO

**Rationale:** [Explain based on metrics]

**Next Steps:** [Week 4 pilot or Week 3 iteration]
EOF
```

---

## File Locations Reference

**Scripts:**
- Validator: `.claude/skills/devforgeai-story-creation/scripts/validate_tech_spec.py`
- Migration: `.claude/skills/devforgeai-story-creation/scripts/migrate_story_v1_to_v2.py`
- Accuracy: `.claude/skills/devforgeai-story-creation/scripts/tests/measure_accuracy.py`
- Test Runner: `.claude/skills/devforgeai-story-creation/scripts/tests/run_all_tests.sh`

**Test Fixtures:**
- Validator: `.claude/skills/devforgeai-story-creation/scripts/tests/fixtures/TC-V*.md`
- Migration: `.claude/skills/devforgeai-story-creation/scripts/tests/fixtures/test-story-*.md`

**Ground Truth:**
- `.claude/skills/devforgeai-story-creation/scripts/tests/expected/test-story-*-ground-truth.yaml`

**Results (created during testing):**
- `.claude/skills/devforgeai-story-creation/scripts/tests/results/`

---

**Use these procedures to execute Week 3 testing externally with Claude API access. All infrastructure ready, just needs API key activation.**
