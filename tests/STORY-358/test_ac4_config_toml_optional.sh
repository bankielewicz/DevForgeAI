#!/bin/bash
# STORY-358 AC#4: config.toml Documented as OPTIONAL COMMIT with Rationale
# TDD Red Phase - These tests MUST FAIL before implementation
#
# Validates: config.toml is marked OPTIONAL COMMIT with rationale mentioning
# "project-specific settings" and .gitignore negation pattern note.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

SOURCE_TREE="$PROJECT_ROOT/devforgeai/specs/context/source-tree.md"

echo "=== AC#4: config.toml Documented as OPTIONAL COMMIT ==="
echo "Target file: $SOURCE_TREE"
echo ""

PASS=0
FAIL=0
TOTAL=5

# Locate the gitignore pattern section start line
GITIGNORE_SECTION_LINE=$(grep -niE '(##|###).*gitignore.*pattern' "$SOURCE_TREE" 2>/dev/null | head -1 | cut -d: -f1)

if [ -n "$GITIGNORE_SECTION_LINE" ]; then
    SECTION_CONTENT=$(tail -n +"$GITIGNORE_SECTION_LINE" "$SOURCE_TREE" 2>/dev/null | head -50)
else
    SECTION_CONTENT=""
fi

# Test 4.1: config.toml has OPTIONAL COMMIT recommendation in the section
echo -n "Test 4.1: config.toml marked as OPTIONAL COMMIT... "
if echo "$SECTION_CONTENT" | grep -iE 'config\.toml.*OPTIONAL.COMMIT|OPTIONAL.COMMIT.*config\.toml' >/dev/null 2>&1; then
    echo "PASS"
    PASS=$((PASS + 1))
else
    echo "FAIL - config.toml with OPTIONAL COMMIT not found in gitignore pattern section"
    FAIL=$((FAIL + 1))
fi

# Test 4.2: Rationale mentions project-specific settings
echo -n "Test 4.2: Rationale mentions project-specific settings... "
if echo "$SECTION_CONTENT" | grep -iE 'project.specific' >/dev/null 2>&1; then
    echo "PASS"
    PASS=$((PASS + 1))
else
    echo "FAIL - Rationale does not mention 'project-specific'"
    FAIL=$((FAIL + 1))
fi

# Test 4.3: .gitignore negation pattern note present (!.treelint/config.toml)
echo -n "Test 4.3: .gitignore negation pattern note present... "
if echo "$SECTION_CONTENT" | grep -qE '!\.treelint/config\.toml|negation' >/dev/null 2>&1; then
    echo "PASS"
    PASS=$((PASS + 1))
else
    echo "FAIL - No .gitignore negation pattern note found"
    FAIL=$((FAIL + 1))
fi

# Test 4.4: Rationale has at least 2 sentences
echo -n "Test 4.4: Rationale has minimum 2 sentences... "
CONFIG_RATIONALE=$(echo "$SECTION_CONTENT" | grep -iA2 'config\.toml')
PERIOD_COUNT=$(echo "$CONFIG_RATIONALE" | grep -o '\.' | wc -l)
if [ "$PERIOD_COUNT" -ge 2 ]; then
    echo "PASS (found $PERIOD_COUNT periods)"
    PASS=$((PASS + 1))
else
    echo "FAIL - Rationale has fewer than 2 sentences (found $PERIOD_COUNT periods)"
    FAIL=$((FAIL + 1))
fi

# Test 4.5: Only valid recommendation values used (GITIGNORED or OPTIONAL COMMIT, not COMMITTED)
echo -n "Test 4.5: No invalid recommendation values (e.g., COMMITTED, REQUIRED)... "
if echo "$SECTION_CONTENT" | grep -iE '\bCOMMITTED\b|\bREQUIRED\b' >/dev/null 2>&1; then
    echo "FAIL - Invalid recommendation value found (COMMITTED or REQUIRED)"
    FAIL=$((FAIL + 1))
else
    echo "PASS"
    PASS=$((PASS + 1))
fi

echo ""
echo "=== AC#4 Results: $PASS/$TOTAL tests passed, $FAIL failed ==="
exit $FAIL
