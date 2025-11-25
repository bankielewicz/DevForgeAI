#!/bin/bash
# Test execution script for STORY-063: code-quality-auditor subagent
# TDD Red Phase: All tests should FAIL initially (before implementation)

set -e

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
cd "$PROJECT_ROOT"

echo "=============================================="
echo "STORY-063: code-quality-auditor Test Suite"
echo "TDD Phase: RED (Tests First)"
echo "=============================================="
echo ""

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "ERROR: pytest not installed"
    echo "Install: pip install pytest pytest-cov pytest-mock"
    exit 1
fi

echo "Test Files:"
echo "  - tests/unit/subagents/test_code_quality_auditor.py (812 lines, 20+ tests)"
echo "  - tests/integration/test_code_quality_auditor_integration.py (554 lines, 10+ tests)"
echo "  - tests/fixtures/code_quality_fixtures.py (549 lines, 9 fixtures)"
echo ""

echo "Expected Result: ALL TESTS FAIL (Red Phase)"
echo "Reason: code-quality-auditor subagent not yet implemented"
echo ""

# Option 1: Run all tests with verbose output
if [ "$1" == "verbose" ]; then
    echo "Running all tests (verbose)..."
    pytest tests/unit/subagents/test_code_quality_auditor.py \
           tests/integration/test_code_quality_auditor_integration.py \
           -v \
           --tb=short \
           -x

# Option 2: Run with coverage analysis
elif [ "$1" == "coverage" ]; then
    echo "Running tests with coverage analysis..."
    pytest tests/unit/subagents/test_code_quality_auditor.py \
           tests/integration/test_code_quality_auditor_integration.py \
           --cov=src/claude/agents/code_quality_auditor \
           --cov-report=term \
           --cov-report=html \
           --cov-fail-under=95

# Option 3: Run unit tests only
elif [ "$1" == "unit" ]; then
    echo "Running unit tests only..."
    pytest tests/unit/subagents/test_code_quality_auditor.py -v --tb=short

# Option 4: Run integration tests only
elif [ "$1" == "integration" ]; then
    echo "Running integration tests only..."
    pytest tests/integration/test_code_quality_auditor_integration.py -v --tb=short

# Option 5: Run specific test class
elif [ "$1" == "class" ] && [ -n "$2" ]; then
    echo "Running test class: $2"
    pytest tests/unit/subagents/test_code_quality_auditor.py::$2 -v --tb=short

# Default: Run all tests with summary
else
    echo "Running all tests (summary)..."
    pytest tests/unit/subagents/test_code_quality_auditor.py \
           tests/integration/test_code_quality_auditor_integration.py \
           --tb=short \
           -q

    echo ""
    echo "=============================================="
    echo "Test Execution Options:"
    echo "=============================================="
    echo "./tests/run_story_063_tests.sh verbose       # Verbose output"
    echo "./tests/run_story_063_tests.sh coverage      # With coverage"
    echo "./tests/run_story_063_tests.sh unit          # Unit tests only"
    echo "./tests/run_story_063_tests.sh integration   # Integration tests only"
    echo "./tests/run_story_063_tests.sh class TestSubagentSpecification  # Specific class"
    echo ""
fi

echo ""
echo "=============================================="
echo "Next Steps (GREEN PHASE):"
echo "=============================================="
echo "1. Implement src/claude/agents/code-quality-auditor.md"
echo "2. Add prompt template to devforgeai-qa skill references"
echo "3. Re-run tests (should PASS after implementation)"
echo "4. Validate coverage ≥95% business logic"
echo ""
