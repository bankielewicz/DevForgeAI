#!/bin/bash

# STORY-161: RCA-011 Immediate Execution Checkpoint
# Test Runner Script
# Usage: bash tests/STORY-161/run-tests.sh

set -e

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TEST_DIR="$PROJECT_ROOT/tests/STORY-161"
SKILL_FILE="$PROJECT_ROOT/.claude/skills/devforgeai-development/SKILL.md"

echo "=========================================="
echo "STORY-161 Test Suite Runner"
echo "=========================================="
echo "Project Root: $PROJECT_ROOT"
echo "Test Directory: $TEST_DIR"
echo "Target File: $SKILL_FILE"
echo "=========================================="
echo ""

# Verify test directory exists
if [ ! -d "$TEST_DIR" ]; then
    echo "ERROR: Test directory not found: $TEST_DIR"
    exit 1
fi

# Verify target file exists
if [ ! -f "$SKILL_FILE" ]; then
    echo "ERROR: SKILL.md not found: $SKILL_FILE"
    exit 1
fi

cd "$PROJECT_ROOT"

# Array to track test results
TESTS=(
    "test-ac1-checkpoint-section-exists.sh"
    "test-ac1-checkpoint-section-position.sh"
    "test-ac1-checkpoint-self-check-boxes.sh"
    "test-ac1-checkpoint-claude-references.sh"
    "test-ac2-stop-and-ask-detection.sh"
    "test-ac3-claude-md-quotes.sh"
    "test-ac4-recovery-path.sh"
)

PASSED=0
FAILED=0
TOTAL=${#TESTS[@]}

echo "Running $TOTAL tests..."
echo ""

for TEST in "${TESTS[@]}"; do
    TEST_PATH="$TEST_DIR/$TEST"

    if [ ! -f "$TEST_PATH" ]; then
        echo "[SKIP] $TEST (file not found)"
        continue
    fi

    echo "---"
    echo "Running: $TEST"
    echo "---"

    # Run test and capture exit code
    if bash "$TEST_PATH"; then
        PASSED=$((PASSED + 1))
        echo ""
    else
        FAILED=$((FAILED + 1))
        echo ""
    fi
done

echo "=========================================="
echo "Test Results Summary"
echo "=========================================="
echo "Total Tests:  $TOTAL"
echo "Passed:       $PASSED"
echo "Failed:       $FAILED"
echo "=========================================="
echo ""

if [ "$FAILED" -eq 0 ]; then
    echo "SUCCESS: All tests passed!"
    exit 0
else
    echo "FAILURE: $FAILED test(s) failed"
    echo "This is expected for TDD Red phase."
    echo "Tests should fail until implementation is complete."
    exit 1
fi
