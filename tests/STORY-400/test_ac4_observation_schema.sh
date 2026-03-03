#!/usr/bin/env bash
# STORY-400 AC#4: Observation schema compliance
# TDD Red Phase - These tests MUST fail before implementation
# Verifies SKILL.md documents the observation schema with all required fields

set -uo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SKILL_FILE="${PROJECT_ROOT}/src/claude/skills/devforgeai-development/SKILL.md"

PASS=0
FAIL=0
TOTAL=0

run_test() {
    local name="$1"
    local result="$2"
    TOTAL=$((TOTAL + 1))
    if [ "$result" -eq 0 ]; then
        PASS=$((PASS + 1))
        echo "  PASS: $name"
    else
        FAIL=$((FAIL + 1))
        echo "  FAIL: $name"
    fi
}

echo "=== AC#4: Observation Schema Compliance ==="
echo ""

if [ ! -f "$SKILL_FILE" ]; then
    run_test "SKILL.md source file exists" 1
    echo "--- AC#4 Results: $PASS/$TOTAL passed, $FAIL failed ---"
    exit 1
fi

# Test 1: Schema defines "phase" field (string)
if grep -q '"phase"' "$SKILL_FILE" 2>/dev/null; then
    run_test "Schema defines 'phase' field" 0
else
    run_test "Schema defines 'phase' field" 1
fi

# Test 2: Schema defines "source" field (string)
if grep -q '"source"' "$SKILL_FILE" 2>/dev/null; then
    run_test "Schema defines 'source' field" 0
else
    run_test "Schema defines 'source' field" 1
fi

# Test 3: Schema defines "type" field with valid enum values
if grep -q '"type".*friction\|friction.*success.*gap.*idea' "$SKILL_FILE" 2>/dev/null; then
    run_test "Schema defines 'type' field with enum (friction|success|gap|idea)" 0
else
    run_test "Schema defines 'type' field with enum (friction|success|gap|idea)" 1
fi

# Test 4: Schema defines "content" field with max 200 chars constraint
if grep -q '"content"' "$SKILL_FILE" 2>/dev/null && grep -q '200' "$SKILL_FILE" 2>/dev/null; then
    run_test "Schema defines 'content' field with 200 char max" 0
else
    run_test "Schema defines 'content' field with 200 char max" 1
fi

# Test 5: Schema defines "timestamp" field with ISO 8601 format
if grep -q '"timestamp"' "$SKILL_FILE" 2>/dev/null && grep -q 'ISO 8601\|iso.8601\|ISO8601' "$SKILL_FILE" 2>/dev/null; then
    run_test "Schema defines 'timestamp' field with ISO 8601 format" 0
else
    run_test "Schema defines 'timestamp' field with ISO 8601 format" 1
fi

# Test 6: Observation type enum lists exactly 4 values
count=$(grep -o 'friction\|success\|gap\|idea' "$SKILL_FILE" 2>/dev/null | sort -u | wc -l)
if [ "$count" -ge 4 ]; then
    run_test "All 4 observation types documented (friction, success, gap, idea)" 0
else
    run_test "All 4 observation types documented (friction, success, gap, idea)" 1
fi

echo ""
echo "--- AC#4 Results: $PASS/$TOTAL passed, $FAIL failed ---"

if [ "$FAIL" -gt 0 ]; then
    exit 1
fi
exit 0
