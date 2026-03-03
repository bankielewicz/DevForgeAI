#!/bin/bash
# STORY-379 AC#1: Overview Section Explains Treelint Integration Purpose and Architecture
# Tests verify the overview section contains:
#   - Treelint purpose (AST-aware code search)
#   - Token reduction benefit (40-80%)
#   - Grep comparison
#   - 7 subagent names
#   - ADR-013 reference
#
# TDD Red Phase: All tests MUST FAIL because docs/guides/treelint-integration-guide.md does not exist yet.

set -e

GUIDE="/mnt/c/Projects/DevForgeAI2/docs/guides/treelint-integration-guide.md"

echo "=== AC#1: Overview Section Explains Treelint Integration Purpose and Architecture ==="

# Test 1: Guide file exists at correct location
echo -n "Test 1: Guide file exists at docs/guides/treelint-integration-guide.md... "
if [ -f "$GUIDE" ]; then
    echo "PASS"
else
    echo "FAIL - File does not exist"
    exit 1
fi

# Test 2: Overview section header exists
echo -n "Test 2: Overview section header exists... "
if grep -qi "## Overview" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - Overview section header not found"
    exit 1
fi

# Test 3: Treelint described as AST-aware code search tool
echo -n "Test 3: Treelint described as AST-aware code search... "
if grep -qi "AST-aware" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - 'AST-aware' not found in guide"
    exit 1
fi

# Test 4: Token reduction benefit stated (40-80%)
echo -n "Test 4: Token reduction range 40-80% stated... "
if grep -q "40-80%" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - '40-80%' token reduction range not found"
    exit 1
fi

# Test 5: Grep comparison documented (semantic vs text matching)
echo -n "Test 5: Grep comparison documented... "
if grep -qi "Grep" "$GUIDE" && grep -qi "text matching\|text-based\|text search" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - Grep comparison or text matching reference not found"
    exit 1
fi

# Test 6: Subagent - test-automator listed
echo -n "Test 6: Subagent test-automator listed... "
if grep -q "test-automator" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - test-automator not found"
    exit 1
fi

# Test 7: Subagent - code-reviewer listed
echo -n "Test 7: Subagent code-reviewer listed... "
if grep -q "code-reviewer" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - code-reviewer not found"
    exit 1
fi

# Test 8: Subagent - backend-architect listed
echo -n "Test 8: Subagent backend-architect listed... "
if grep -q "backend-architect" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - backend-architect not found"
    exit 1
fi

# Test 9: Subagent - security-auditor listed
echo -n "Test 9: Subagent security-auditor listed... "
if grep -q "security-auditor" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - security-auditor not found"
    exit 1
fi

# Test 10: Subagent - refactoring-specialist listed
echo -n "Test 10: Subagent refactoring-specialist listed... "
if grep -q "refactoring-specialist" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - refactoring-specialist not found"
    exit 1
fi

# Test 11: Subagent - coverage-analyzer listed
echo -n "Test 11: Subagent coverage-analyzer listed... "
if grep -q "coverage-analyzer" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - coverage-analyzer not found"
    exit 1
fi

# Test 12: Subagent - anti-pattern-scanner listed
echo -n "Test 12: Subagent anti-pattern-scanner listed... "
if grep -q "anti-pattern-scanner" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - anti-pattern-scanner not found"
    exit 1
fi

# Test 13: ADR-013 referenced
echo -n "Test 13: ADR-013 referenced... "
if grep -q "ADR-013" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - ADR-013 reference not found"
    exit 1
fi

echo ""
echo "=== AC#1 All Tests Passed ==="
exit 0
