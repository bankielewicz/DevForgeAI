#!/bin/bash
# Test AC-2: Fundamental Principle Documented
# DOC-002: Document fundamental principle that skills are state machines
# Expected: FAIL initially (before implementation)

CLAUDE_FILE="src/CLAUDE.md"

echo "=== AC-2: Fundamental Principle Documented ==="

# Check if CLAUDE.md exists
if [ ! -f "$CLAUDE_FILE" ]; then
    echo "FAIL: Target file $CLAUDE_FILE does not exist"
    exit 1
fi

# Get content of the CRITICAL section (up to 100 lines after header)
CRITICAL_LINE=$(grep -n "## CRITICAL: No Deviation from Skill Phases" "$CLAUDE_FILE" | head -1 | cut -d: -f1)

if [ -z "$CRITICAL_LINE" ]; then
    echo "FAIL: Section '## CRITICAL: No Deviation from Skill Phases' not found"
    exit 1
fi

# Extract section content (skip header, find next ## section)
SECTION_START=$((CRITICAL_LINE + 1))
SECTION_END=$((CRITICAL_LINE + 100))
SECTION_CONTENT=$(sed -n "${SECTION_START},${SECTION_END}p" "$CLAUDE_FILE" | sed '/^## [A-Za-z]/q' | head -n -1)

# Test 1: States skills are NOT guidelines
if echo "$SECTION_CONTENT" | grep -qiE "(skills|skill).*(NOT|not|never).*(guidelines?|optional|suggestions?)"; then
    echo "  [PASS] States skills are NOT guidelines"
else
    echo "  [FAIL] Missing statement that skills are NOT guidelines"
    exit 1
fi

# Test 2: States skills are state machines
if echo "$SECTION_CONTENT" | grep -qiE "(skills?|skill).*(state.?machines?|deterministic|sequential)"; then
    echo "  [PASS] States skills are state machines"
else
    echo "  [FAIL] Missing statement that skills are state machines"
    exit 1
fi

# Test 3: Contains at least 4 MUST requirements
# Count occurrences of MUST (case sensitive) or **MUST**
MUST_COUNT=$(echo "$SECTION_CONTENT" | grep -oE '\bMUST\b|\*\*MUST\*\*' | wc -l)

if [ "$MUST_COUNT" -ge 4 ]; then
    echo "  [PASS] Contains $MUST_COUNT MUST requirements (minimum: 4)"
else
    echo "  [FAIL] Contains only $MUST_COUNT MUST requirements (minimum: 4 required)"
    exit 1
fi

# Test 4: Contains fundamental principle statement
if echo "$SECTION_CONTENT" | grep -qiE "(fundamental|core|critical).*(principle|rule|requirement)"; then
    echo "  [PASS] Contains fundamental principle statement"
else
    echo "  [FAIL] Missing fundamental principle statement"
    exit 1
fi

echo "PASS: AC-2 - Fundamental principle documented with all required elements"
exit 0
