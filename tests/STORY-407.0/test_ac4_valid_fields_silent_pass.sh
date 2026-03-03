#!/usr/bin/env bash
# =============================================================================
# STORY-407 AC#4: Valid Treelint Field References Pass Silently
# =============================================================================
# Validates that story-requirements-analyst.md contains:
#   1. Silent pass behavior when all fields match canonical names
#   2. Reference to the canonical field set
#   3. At least a subset of canonical field names documented
#   4. No warning output for valid fields
#
# Canonical fields (from treelint-search-patterns.md):
#   results, type, name, file, lines, start, end, signature, body, count,
#   query, members, methods, properties, class_methods, bases, files, path,
#   rank, score, references, complexity, total_files, returned
#
# Target: src/claude/agents/story-requirements-analyst.md
# TDD Phase: RED - Tests expected to FAIL until implementation complete.
# =============================================================================

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
TARGET_FILE="${PROJECT_ROOT}/src/claude/agents/story-requirements-analyst.md"

PASS_COUNT=0
FAIL_COUNT=0
TOTAL_COUNT=0

pass() {
    PASS_COUNT=$((PASS_COUNT + 1))
    TOTAL_COUNT=$((TOTAL_COUNT + 1))
    echo "  PASS: $1"
}

fail() {
    FAIL_COUNT=$((FAIL_COUNT + 1))
    TOTAL_COUNT=$((TOTAL_COUNT + 1))
    echo "  FAIL: $1"
}

echo "=============================================="
echo "  AC#4: Valid Treelint Field References Pass Silently"
echo "=============================================="
echo ""

# -----------------------------------------------------------------------------
# Test 1: Target file exists
# -----------------------------------------------------------------------------
echo "--- Test 1: File Existence ---"
if [[ -r "$TARGET_FILE" ]]; then
    pass "story-requirements-analyst.md exists and is readable"
else
    fail "story-requirements-analyst.md not found"
    echo ""
    echo "=============================================="
    echo "  AC#4 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Silent pass behavior documented
# -----------------------------------------------------------------------------
echo "--- Test 2: Silent Pass Behavior Documented ---"
if grep -qiE '(silent.*pass|no.*warning|zero.*output|no.*visible.*output|pass.*silent)' "$TARGET_FILE"; then
    pass "Silent pass behavior documented for valid field references"
else
    fail "Missing silent pass behavior (valid fields should produce zero visible output)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: Canonical field names referenced (at least core fields)
# -----------------------------------------------------------------------------
echo "--- Test 3: Core Canonical Fields Referenced ---"
# Check for at least 5 canonical field names in the file
canonical_count=0
grep -q '`results`\|"results"' "$TARGET_FILE" && canonical_count=$((canonical_count + 1))
grep -q '`name`\|"name"' "$TARGET_FILE" && canonical_count=$((canonical_count + 1))
grep -q '`file`\|"file"' "$TARGET_FILE" && canonical_count=$((canonical_count + 1))
grep -q '`lines`\|"lines"' "$TARGET_FILE" && canonical_count=$((canonical_count + 1))
grep -q '`signature`\|"signature"' "$TARGET_FILE" && canonical_count=$((canonical_count + 1))
grep -q '`count`\|"count"' "$TARGET_FILE" && canonical_count=$((canonical_count + 1))
grep -q '`members`\|"members"' "$TARGET_FILE" && canonical_count=$((canonical_count + 1))
grep -q '`methods`\|"methods"' "$TARGET_FILE" && canonical_count=$((canonical_count + 1))
grep -q '`complexity`\|"complexity"' "$TARGET_FILE" && canonical_count=$((canonical_count + 1))

if [[ "$canonical_count" -ge 5 ]]; then
    pass "At least 5 canonical field names referenced (found ${canonical_count})"
else
    fail "Only ${canonical_count}/9 core canonical fields found (need at least 5)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Valid field matching logic present
# -----------------------------------------------------------------------------
echo "--- Test 4: Valid Field Matching Logic ---"
if grep -qiE '(match.*canonical|exact.*match|field.*match|match.*field.*name|cross.reference.*check)' "$TARGET_FILE"; then
    pass "Valid field matching logic documented"
else
    fail "Missing valid field matching logic (exact match against canonical set)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: No-warning condition explicitly stated
# -----------------------------------------------------------------------------
echo "--- Test 5: No-Warning Condition Explicit ---"
if grep -qiE '(no.*warning.*emitted|zero.*warning|warning.*not.*produced|silent|no.*output)' "$TARGET_FILE"; then
    pass "No-warning condition explicitly stated for valid fields"
else
    fail "Missing explicit no-warning condition for valid field references"
fi
echo ""

# =============================================================================
# Summary
# =============================================================================
echo "=============================================="
echo "  AC#4 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
echo "=============================================="

if [[ "$FAIL_COUNT" -gt 0 ]]; then
    echo "  STATUS: FAILED"
    exit 1
else
    echo "  STATUS: PASSED"
    exit 0
fi
