#!/bin/bash

# STORY-170 AC-4: Counter Persists Across Session
# Test that iteration counter persists in story workflow section and
# resumes correctly when user runs /resume-dev
#
# This test SHOULD FAIL initially (Red phase - TDD)
# Implementation needed: Add iteration_count to story workflow section and phase-state.json

set -e

SKILL_FILE=".claude/skills/devforgeai-development/SKILL.md"
SAMPLE_STATE_FILE="devforgeai/workflows/STORY-162-phase-state.json"

echo "TEST: AC-4 - Counter Persists Across Session"
echo "============================================="
echo ""

# Check if SKILL.md exists
if [ ! -f "$SKILL_FILE" ]; then
    echo "FAIL: $SKILL_FILE does not exist"
    exit 1
fi

echo "Checking for iteration persistence logic..."
echo ""

# Test 1: Check for iteration storage documentation in story workflow section
# Per tech spec: Store in "Story file workflow section"
if grep -qE "(iteration_count|iteration.*persist|persist.*iteration)" "$SKILL_FILE"; then
    echo "PASS: Found iteration persistence reference in SKILL.md"
else
    echo "FAIL: No iteration persistence documentation found"
    echo ""
    echo "Expected: Documentation showing iteration_count storage in story workflow section"
    echo "  Example format in story:"
    echo "  ## Workflow Status"
    echo "  - iteration_count: 2"
    echo "  - last_iteration_date: 2025-12-31"
    exit 1
fi

# Test 2: Check for phase-state.json iteration field documentation
# The phase-state.json should include iteration_count
if grep -qE "phase-state\.json.*iteration|iteration.*phase-state" "$SKILL_FILE"; then
    echo "PASS: Found phase-state.json iteration storage reference"
else
    echo "FAIL: No phase-state.json iteration storage documentation"
    echo ""
    echo "Expected: iteration_count stored in phase-state.json for persistence"
    exit 1
fi

# Test 3: Check for resume logic that reads iteration count
# When resuming, should read iteration_count from storage
if grep -qE "(resume|/resume-dev|Resume).*iteration" "$SKILL_FILE"; then
    echo "PASS: Found resume-iteration connection"
else
    # Alternative check - look for reading iteration on resume
    RESUME_CONTEXT=$(grep -iB5 -A5 "resume" "$SKILL_FILE" 2>/dev/null || true)
    if echo "$RESUME_CONTEXT" | grep -qiE "iteration"; then
        echo "PASS: Found iteration handling in resume context"
    else
        echo "FAIL: No logic to restore iteration count on resume"
        echo ""
        echo "Expected: When /resume-dev is run, read iteration_count from storage"
        echo "          and continue from that value (not reset to 1)"
        exit 1
    fi
fi

# Test 4: Check for workflow status YAML format in documentation
# Tech spec shows: "- iteration_count: 2"
if grep -qE "iteration_count:\s*[0-9]" "$SKILL_FILE"; then
    echo "PASS: Found iteration_count YAML format example"
else
    echo "FAIL: iteration_count YAML format not documented"
    echo ""
    echo "Expected format in story workflow section:"
    echo "  ## Workflow Status"
    echo "  - iteration_count: 2"
    exit 1
fi

# Test 5: Check for phase-state.json schema documentation with iteration_count
# The schema is documented in SKILL.md with example JSON
SCHEMA_DOC=$(grep -A20 "Phase State Schema" "$SKILL_FILE" 2>/dev/null || true)
if echo "$SCHEMA_DOC" | grep -q '"iteration_count"'; then
    echo "PASS: Phase state schema documentation includes iteration_count field"
else
    echo "FAIL: Phase state schema documentation missing iteration_count"
    echo ""
    echo "Expected: SKILL.md Phase State Schema should include 'iteration_count' field"
    exit 1
fi

# Test 6: Verify schema includes last_iteration_date for audit trail
if echo "$SCHEMA_DOC" | grep -q "last_iteration_date"; then
    echo "PASS: Phase state schema includes last_iteration_date for audit"
else
    echo "FAIL: Phase state schema missing last_iteration_date"
    echo ""
    echo "Expected: Schema should include last_iteration_date for tracking"
    exit 1
fi

echo ""
echo "============================================="
echo "ALL TESTS PASSED: AC-4 Counter Persists Across Session"
echo "============================================="
exit 0
