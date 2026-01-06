#!/bin/bash
# Run all STORY-232 tests
# This is a simple runner that executes each test script

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=============================================="
echo "STORY-232: Running All Tests"
echo "=============================================="
echo ""

total_exit_code=0

for test_file in "$SCRIPT_DIR"/test-ac*.sh; do
    echo "Running: $(basename "$test_file")"
    echo "----------------------------------------------"
    bash "$test_file"
    exit_code=$?
    if [[ $exit_code -ne 0 ]]; then
        total_exit_code=1
    fi
    echo ""
done

echo "=============================================="
if [[ $total_exit_code -eq 0 ]]; then
    echo "All tests passed (GREEN)"
else
    echo "Tests failed (RED) - Expected for TDD Red Phase"
fi
echo "=============================================="

exit $total_exit_code
