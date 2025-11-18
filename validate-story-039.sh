#!/bin/bash

# STORY-039: Update Framework Documentation for Lean Orchestration Pattern
# Test Script: Validates all 7 Acceptance Criteria

# Don't exit on first error - we want to see all results
set +e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counters
PASS=0
FAIL=0

# Helper function to print test result
test_result() {
    local test_name=$1
    local result=$2

    if [ "$result" -eq 0 ]; then
        echo -e "${GREEN}✓ PASS${NC}: $test_name"
        ((PASS++))
    else
        echo -e "${RED}✗ FAIL${NC}: $test_name"
        ((FAIL++))
    fi
}

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "STORY-039: Documentation Testing"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# AC-1: Protocol Documentation Updated
echo "AC-1: Protocol Documentation Updated"
echo "---"
test -f ".devforgeai/protocols/lean-orchestration-pattern.md"
test_result "Protocol file exists" $?
grep -q "Case Study" ".devforgeai/protocols/lean-orchestration-pattern.md"
test_result "Case Study references exist" $?
grep -q "Pattern Consistency Analysis" ".devforgeai/protocols/lean-orchestration-pattern.md"
test_result "Pattern Consistency Analysis section exists" $?

echo ""
echo "AC-2: Command Budget Reference Updated"
echo "---"
test -f ".devforgeai/protocols/command-budget-reference.md"
test_result "Budget reference file exists" $?
grep -q "Current Command Status" ".devforgeai/protocols/command-budget-reference.md"
test_result "Current Command Status section exists" $?

echo ""
echo "AC-3: Commands Reference Updated"
echo "---"
test -f ".claude/memory/commands-reference.md"
test_result "Commands reference file exists" $?
grep -q "Pattern" ".claude/memory/commands-reference.md"
test_result "Pattern references in commands-reference" $?

echo ""
echo "AC-4: Command Template"
echo "---"
test -f ".claude/skills/devforgeai-subagent-creation/assets/templates/command-template-lean-orchestration.md"
test_result "Command template file exists" $?

echo ""
echo "AC-5: Troubleshooting Guide"
echo "---"
test -f ".devforgeai/protocols/troubleshooting-lean-orchestration-violations.md"
test_result "Troubleshooting guide file exists" $?

echo ""
echo "AC-6: Documentation Completeness"
echo "---"
grep -q "refactoring-case-studies.md" ".devforgeai/protocols/lean-orchestration-pattern.md"
test_result "Cross-references present" $?

echo ""
echo "AC-7: Documentation Accuracy"
echo "---"
grep -q "Commands orchestrate" ".devforgeai/protocols/lean-orchestration-pattern.md"
test_result "Constitutional principle defined" $?

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
total=$((PASS + FAIL))
echo "TESTS: $PASS passed, $FAIL failed of $total"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

[ "$FAIL" -eq 0 ]
