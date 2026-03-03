#!/bin/bash
# Test AC#2: Self-Reference Investigated and Resolved
# STORY-452 - Portability Fix
#
# Verifies:
# 1. The Integration Instructions block (lines ~585-603) has been resolved:
#    Either (a) self-reference retained with inline comment, or
#    (b) path corrected to intended target file
# 2. No bare self-reference without explanation

set -euo pipefail

TARGET_FILE="src/claude/skills/discovering-requirements/references/user-input-guidance.md"

PASS=0
FAIL=0

# Test 1: Self-reference has inline comment OR path was changed to different target
echo "Test 1: Self-reference resolved (comment added or path corrected)"

# Extract the Integration Instructions Read() line
READ_LINE=$(grep -n 'Read(file_path=' "$TARGET_FILE" | grep -i 'user-input-guidance\|discovering-requirements' | tail -1 || true)

if [ -z "$READ_LINE" ]; then
    # Path was changed to a completely different file — that counts as resolved
    echo "  PASS: Self-reference removed (path changed to different target)"
    PASS=$((PASS + 1))
else
    # Self-reference still exists — check for inline comment
    LINE_NUM=$(echo "$READ_LINE" | cut -d: -f1)
    # Check if there's a comment on or near the Read() line (within 2 lines)
    CONTEXT=$(sed -n "$((LINE_NUM-1)),$((LINE_NUM+1))p" "$TARGET_FILE")
    if echo "$CONTEXT" | grep -qi 'example\|self-reference\|this file\|note:'; then
        echo "  PASS: Self-reference retained with clarifying comment"
        PASS=$((PASS + 1))
    else
        echo "  FAIL: Self-reference exists without clarifying comment"
        FAIL=$((FAIL + 1))
    fi
fi

# Test 2: Story implementation notes document the determination
echo "Test 2: Implementation Notes document the self-reference determination"
STORY_FILE="devforgeai/specs/Stories/STORY-452-portability-fix-remove-hardcoded-wsl-path.story.md"
if grep -qi 'self-reference\|self reference\|copy-paste' "$STORY_FILE" 2>/dev/null; then
    if grep -q '## Implementation Notes' "$STORY_FILE"; then
        echo "  PASS: Implementation Notes contain self-reference determination"
        PASS=$((PASS + 1))
    else
        echo "  FAIL: Implementation Notes section missing"
        FAIL=$((FAIL + 1))
    fi
else
    echo "  FAIL: No self-reference determination documented in story"
    FAIL=$((FAIL + 1))
fi

# Summary
echo ""
echo "Results: $PASS passed, $FAIL failed"

if [ "$FAIL" -gt 0 ]; then
    echo "OVERALL: FAIL"
    exit 1
else
    echo "OVERALL: PASS"
    exit 0
fi
