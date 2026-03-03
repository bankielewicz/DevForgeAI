#!/bin/bash
# STORY-319 AC#4: Backend-Architect Extraction Rules
# Tests that extraction rules for backend-architect output are documented
# Expected: FAIL (file does not exist yet - TDD Red phase)

set -e

SOURCE_FILE="src/claude/agents/observation-extractor.md"

echo "=== AC#4: Backend-Architect Extraction Rules Tests ==="

# Pre-check: File must exist
if [ ! -f "$SOURCE_FILE" ]; then
    echo "FAIL: Source file does not exist: $SOURCE_FILE"
    exit 1
fi

# Test 4.1: Extraction rule for pattern_compliance.violations[] exists
echo -n "Test 4.1: Extraction rule for 'pattern_compliance.violations' documented... "
if grep -q "pattern_compliance" "$SOURCE_FILE" && grep -q "violations" "$SOURCE_FILE"; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: Reference to 'pattern_compliance.violations' extraction rule"
    exit 1
fi

# Test 4.2: pattern_compliance.violations maps to category "pattern"
echo -n "Test 4.2: pattern_compliance.violations maps to category 'pattern'... "
if grep -A10 -B10 "pattern_compliance\|violations" "$SOURCE_FILE" | grep -q "pattern"; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: pattern_compliance.violations to map to category 'pattern'"
    exit 1
fi

# Test 4.3: backend-architect is mentioned as source subagent
echo -n "Test 4.3: backend-architect mentioned as source subagent... "
if grep -qi "backend-architect" "$SOURCE_FILE"; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: Reference to 'backend-architect' subagent"
    exit 1
fi

echo ""
echo "=== AC#4: All tests passed ==="
exit 0
