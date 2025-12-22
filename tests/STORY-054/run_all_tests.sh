#!/bin/bash

# ============================================================================
# STORY-054 Test Runner
# ============================================================================
# Executes all test suites for claude-code-terminal-expert enhancement
# ============================================================================

set -e

TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$TEST_DIR/../.." && pwd)"

cd "$PROJECT_ROOT"

echo "=========================================="
echo "STORY-054 Test Suite Runner"
echo "=========================================="
echo ""
echo "Project Root: $PROJECT_ROOT"
echo "Test Directory: $TEST_DIR"
echo "Timestamp: $(date -u)"
echo ""

# Run main test suite
echo "Running: test-prompting-guidance.sh"
echo ""

if bash "$TEST_DIR/test-prompting-guidance.sh"; then
    exit_code=0
else
    exit_code=$?
fi

echo ""
echo "=========================================="
echo "Test Run Complete"
echo "=========================================="
echo "Exit Code: $exit_code"

exit $exit_code
