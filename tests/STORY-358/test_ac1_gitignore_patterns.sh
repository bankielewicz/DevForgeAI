#!/bin/bash
# STORY-358 AC#1: Gitignore Pattern Section Added to source-tree.md
# TDD Red Phase - These tests MUST FAIL before implementation
#
# Validates: A gitignore pattern documentation subsection exists in the
# "Directory Purpose and Rules" section, listing exactly 3 file patterns
# (index.db, daemon.sock, config.toml) with recommendations and rationales.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

SOURCE_TREE="$PROJECT_ROOT/devforgeai/specs/context/source-tree.md"

echo "=== AC#1: Gitignore Pattern Section in source-tree.md ==="
echo "Target file: $SOURCE_TREE"
echo ""

PASS=0
FAIL=0
TOTAL=6

# Test 1.1: A gitignore pattern section/heading exists in source-tree.md
echo -n "Test 1.1: Gitignore pattern section heading exists... "
if grep -qiE '(##|###).*gitignore.*pattern' "$SOURCE_TREE" 2>/dev/null; then
    echo "PASS"
    PASS=$((PASS + 1))
else
    echo "FAIL - No gitignore pattern section heading found in source-tree.md"
    FAIL=$((FAIL + 1))
fi

# Test 1.2: Section appears AFTER "Directory Purpose and Rules" heading
echo -n "Test 1.2: Section is within Directory Purpose and Rules area... "
DIR_PURPOSE_LINE=$(grep -n 'Directory Purpose and Rules' "$SOURCE_TREE" 2>/dev/null | head -1 | cut -d: -f1)
GITIGNORE_SECTION_LINE=$(grep -niE '(##|###).*gitignore.*pattern' "$SOURCE_TREE" 2>/dev/null | head -1 | cut -d: -f1)
if [ -n "$DIR_PURPOSE_LINE" ] && [ -n "$GITIGNORE_SECTION_LINE" ] && [ "$GITIGNORE_SECTION_LINE" -gt "$DIR_PURPOSE_LINE" ]; then
    echo "PASS"
    PASS=$((PASS + 1))
else
    echo "FAIL - Gitignore pattern section not found after Directory Purpose and Rules"
    FAIL=$((FAIL + 1))
fi

# Test 1.3: index.db appears in the gitignore documentation section (not just the tree diagram)
echo -n "Test 1.3: index.db documented in gitignore pattern section... "
if [ -n "$GITIGNORE_SECTION_LINE" ]; then
    # Search from gitignore section onward for index.db with a recommendation keyword
    if tail -n +"$GITIGNORE_SECTION_LINE" "$SOURCE_TREE" 2>/dev/null | head -50 | grep -qi 'index\.db'; then
        echo "PASS"
        PASS=$((PASS + 1))
    else
        echo "FAIL - index.db not found in gitignore pattern section"
        FAIL=$((FAIL + 1))
    fi
else
    echo "FAIL - Gitignore pattern section not found"
    FAIL=$((FAIL + 1))
fi

# Test 1.4: daemon.sock appears in the gitignore documentation section
echo -n "Test 1.4: daemon.sock documented in gitignore pattern section... "
if [ -n "$GITIGNORE_SECTION_LINE" ]; then
    if tail -n +"$GITIGNORE_SECTION_LINE" "$SOURCE_TREE" 2>/dev/null | head -50 | grep -qi 'daemon\.sock'; then
        echo "PASS"
        PASS=$((PASS + 1))
    else
        echo "FAIL - daemon.sock not found in gitignore pattern section"
        FAIL=$((FAIL + 1))
    fi
else
    echo "FAIL - Gitignore pattern section not found"
    FAIL=$((FAIL + 1))
fi

# Test 1.5: config.toml appears in the gitignore documentation section
echo -n "Test 1.5: config.toml documented in gitignore pattern section... "
if [ -n "$GITIGNORE_SECTION_LINE" ]; then
    if tail -n +"$GITIGNORE_SECTION_LINE" "$SOURCE_TREE" 2>/dev/null | head -50 | grep -qi 'config\.toml'; then
        echo "PASS"
        PASS=$((PASS + 1))
    else
        echo "FAIL - config.toml not found in gitignore pattern section"
        FAIL=$((FAIL + 1))
    fi
else
    echo "FAIL - Gitignore pattern section not found"
    FAIL=$((FAIL + 1))
fi

# Test 1.6: Exactly 3 file patterns documented (count distinct .treelint/ file entries in section)
echo -n "Test 1.6: Exactly 3 file patterns listed... "
if [ -n "$GITIGNORE_SECTION_LINE" ]; then
    PATTERN_COUNT=$(tail -n +"$GITIGNORE_SECTION_LINE" "$SOURCE_TREE" 2>/dev/null | head -50 | grep -ciE '(index\.db|daemon\.sock|config\.toml)')
    if [ "$PATTERN_COUNT" -eq 3 ]; then
        echo "PASS (found $PATTERN_COUNT)"
        PASS=$((PASS + 1))
    else
        echo "FAIL - Expected 3 file patterns, found $PATTERN_COUNT"
        FAIL=$((FAIL + 1))
    fi
else
    echo "FAIL - Gitignore pattern section not found"
    FAIL=$((FAIL + 1))
fi

echo ""
echo "=== AC#1 Results: $PASS/$TOTAL tests passed, $FAIL failed ==="
exit $FAIL
