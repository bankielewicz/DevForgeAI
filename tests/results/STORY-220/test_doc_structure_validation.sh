#!/bin/bash
# Test DOC Structure: Validate overall documentation structure
# Ensures new section integrates properly with existing CLAUDE.md structure
# Expected: FAIL initially (before implementation)

CLAUDE_FILE="src/CLAUDE.md"

echo "=== DOC Structure: Documentation Integration Validation ==="

# Check if CLAUDE.md exists
if [ ! -f "$CLAUDE_FILE" ]; then
    echo "FAIL: Target file $CLAUDE_FILE does not exist"
    exit 1
fi

# Test 1: Section uses proper Markdown formatting
CRITICAL_LINE=$(grep -n "## CRITICAL: No Deviation from Skill Phases" "$CLAUDE_FILE" | head -1 | cut -d: -f1)

if [ -z "$CRITICAL_LINE" ]; then
    echo "  [FAIL] New section not found"
    exit 1
fi

# Extract section content (include header for separator check, skip to find end)
SECTION_END=$((CRITICAL_LINE + 150))
SECTION_CONTENT=$(sed -n "${CRITICAL_LINE},${SECTION_END}p" "$CLAUDE_FILE" | sed '1d' | sed '/^## [A-Za-z]/q' | head -n -1)

# Test 2: Section has horizontal rule separator (---)
if echo "$SECTION_CONTENT" | grep -qE "^---$"; then
    echo "  [PASS] Section includes horizontal rule separator"
else
    echo "  [WARN] Section missing horizontal rule separator (optional but recommended)"
fi

# Test 3: Section uses consistent header levels (### for subsections)
SUBSECTION_COUNT=$(echo "$SECTION_CONTENT" | grep -cE "^### " | head -1)
if [ "$SUBSECTION_COUNT" -ge 1 ]; then
    echo "  [PASS] Section uses ### for subsections ($SUBSECTION_COUNT found)"
else
    echo "  [WARN] No subsections (###) found - may want to add for organization"
fi

# Test 4: Section contains code blocks for examples
CODE_BLOCK_COUNT=$(echo "$SECTION_CONTENT" | grep -cE "^\`\`\`" | head -1)
if [ "$CODE_BLOCK_COUNT" -ge 2 ]; then
    echo "  [PASS] Section contains code blocks for examples ($CODE_BLOCK_COUNT found)"
else
    echo "  [FAIL] Missing code blocks for examples (need at least 2)"
    exit 1
fi

# Test 5: Section does not use emojis (per CLAUDE.md convention)
EMOJI_COUNT=$(echo "$SECTION_CONTENT" | grep -cP "[\x{1F300}-\x{1F9FF}]" 2>/dev/null | head -1)
if [ "$EMOJI_COUNT" -eq 0 ] || [ -z "$EMOJI_COUNT" ]; then
    echo "  [PASS] Section avoids emojis (per convention)"
else
    echo "  [WARN] Section contains emojis ($EMOJI_COUNT) - should use text markers instead"
fi

# Test 6: Section minimum length check (should be substantial)
LINE_COUNT=$(echo "$SECTION_CONTENT" | wc -l)
if [ "$LINE_COUNT" -ge 30 ]; then
    echo "  [PASS] Section has sufficient content ($LINE_COUNT lines)"
else
    echo "  [FAIL] Section too short ($LINE_COUNT lines) - expected at least 30 lines"
    exit 1
fi

echo "PASS: DOC Structure - Documentation integrates properly"
exit 0
