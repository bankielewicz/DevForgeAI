#!/bin/bash
# Test: AC#2 - Pre-flight logic extracted to reference file
# Story: STORY-459
# Generated: 2026-02-20
# Phase: TDD Red (tests MUST fail before implementation)
#
# Validates:
# - resume-detection.md exists and contains "Resume Pre-Flight Validation" section
# - resume-dev.md does NOT contain devforgeai-validate
# - resume-dev.md does NOT contain Task(subagent_type="tech-stack-detector"
# - resume-dev.md does NOT contain spec comparison logic
# - resume-detection.md contains Step 1.1 context validation
# - resume-detection.md contains Step 1.2 tech-stack-detector
# - resume-detection.md contains Step 1.3 spec-vs-context

set -uo pipefail

# === Test Configuration ===
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
COMMAND_FILE="${PROJECT_ROOT}/src/claude/commands/resume-dev.md"
REFERENCE_FILE="${PROJECT_ROOT}/src/claude/skills/implementing-stories/references/resume-detection.md"
PASSED=0
FAILED=0
TOTAL=0

run_test() {
    local name="$1"
    local result="$2"
    ((TOTAL++))
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        ((PASSED++))
    else
        echo "  FAIL: $name"
        ((FAILED++))
    fi
}

echo "=========================================="
echo "  AC#2: Pre-Flight Logic Extraction Tests"
echo "  Story: STORY-459"
echo "=========================================="
echo ""

# === Test 1: resume-detection.md exists ===
test -f "$REFERENCE_FILE"
run_test "resume-detection.md exists at expected path" $?

# === Test 2: resume-detection.md contains "Resume Pre-Flight Validation" section ===
if [ -f "$REFERENCE_FILE" ]; then
    grep -q "Resume Pre-Flight Validation" "$REFERENCE_FILE"
    run_test "resume-detection.md contains 'Resume Pre-Flight Validation' section header" $?
else
    ((TOTAL++)); ((FAILED++))
    echo "  FAIL: resume-detection.md contains 'Resume Pre-Flight Validation' section header (file missing)"
fi

# === Test 3: resume-dev.md does NOT contain devforgeai-validate ===
FOUND=$(grep -c 'devforgeai-validate' "$COMMAND_FILE" || true)
test "$FOUND" -eq 0
run_test "resume-dev.md does NOT contain 'devforgeai-validate' (found: $FOUND)" $?

# === Test 4: resume-dev.md does NOT contain Task(subagent_type="tech-stack-detector" ===
FOUND=$(grep -c 'Task(subagent_type="tech-stack-detector"' "$COMMAND_FILE" || true)
test "$FOUND" -eq 0
run_test "resume-dev.md does NOT contain Task(subagent_type=\"tech-stack-detector\") (found: $FOUND)" $?

# === Test 5: resume-dev.md does NOT contain spec comparison logic ===
# Spec comparison logic uses spec-vs-context or mismatch detection patterns
FOUND=$(grep -c -E '(spec-vs-context|spec.*mismatch|context.*comparison|validate.*spec)' "$COMMAND_FILE" || true)
test "$FOUND" -eq 0
run_test "resume-dev.md does NOT contain spec comparison logic (found: $FOUND)" $?

# === Test 6: resume-detection.md contains Step 1.1 context validation ===
if [ -f "$REFERENCE_FILE" ]; then
    grep -q -E '(Step 1\.1|1\.1.*context.*valid|context.*validation.*Step)' "$REFERENCE_FILE"
    run_test "resume-detection.md contains Step 1.1 context validation" $?
else
    ((TOTAL++)); ((FAILED++))
    echo "  FAIL: resume-detection.md contains Step 1.1 context validation (file missing)"
fi

# === Test 7: resume-detection.md contains Step 1.2 tech-stack-detector ===
if [ -f "$REFERENCE_FILE" ]; then
    grep -q -E '(Step 1\.2|1\.2.*tech-stack|tech-stack-detector)' "$REFERENCE_FILE"
    run_test "resume-detection.md contains Step 1.2 tech-stack-detector" $?
else
    ((TOTAL++)); ((FAILED++))
    echo "  FAIL: resume-detection.md contains Step 1.2 tech-stack-detector (file missing)"
fi

# === Test 8: resume-detection.md contains Step 1.3 spec-vs-context ===
if [ -f "$REFERENCE_FILE" ]; then
    grep -q -E '(Step 1\.3|1\.3.*spec|spec-vs-context)' "$REFERENCE_FILE"
    run_test "resume-detection.md contains Step 1.3 spec-vs-context" $?
else
    ((TOTAL++)); ((FAILED++))
    echo "  FAIL: resume-detection.md contains Step 1.3 spec-vs-context (file missing)"
fi

# === Summary ===
echo ""
echo "=========================================="
echo "  Results: $PASSED passed, $FAILED failed out of $TOTAL tests"
echo "=========================================="
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
