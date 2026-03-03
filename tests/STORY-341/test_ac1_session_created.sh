#!/bin/bash
# Test AC#1: Session Memory Created at Phase 01
# Verifies phase-01-preflight.md contains session memory creation instructions
# Expected: FAIL (TDD Red phase - implementation not yet done)

set -e
# Check src/ (source of truth) first, fallback to .claude/ (operational)
TARGET_FILE="src/claude/skills/devforgeai-development/phases/phase-01-preflight.md"
if [ ! -f "$TARGET_FILE" ]; then
    TARGET_FILE=".claude/skills/devforgeai-development/phases/phase-01-preflight.md"
fi

echo "AC#1: Verifying session memory creation at Phase 01..."

# Test 1: Session Memory Creation section exists
if ! grep -q 'Session Memory Creation' "$TARGET_FILE"; then
    echo "FAIL: Missing 'Session Memory Creation' section in phase-01-preflight.md"
    exit 1
fi

# Test 2: Write() instruction for session memory file
# Check for both: Write() instruction AND session path definition
if ! grep -q 'Write(' "$TARGET_FILE"; then
    echo "FAIL: Missing Write() instruction for session memory file"
    exit 1
fi
if ! grep -q '\.claude/memory/sessions/.*session\.md' "$TARGET_FILE"; then
    echo "FAIL: Missing session memory path (.claude/memory/sessions/)"
    exit 1
fi

# Test 3: Path uses STORY_ID variable
if ! grep -q 'sessions/.*STORY.*session\.md' "$TARGET_FILE"; then
    echo "FAIL: Session memory path missing STORY_ID variable"
    exit 1
fi

# Test 4: YAML frontmatter fields specified
if ! grep -q 'story_id:' "$TARGET_FILE" && ! grep -q 'frontmatter' "$TARGET_FILE"; then
    echo "FAIL: Missing YAML frontmatter specification for session memory"
    exit 1
fi

echo "PASS: AC#1 Session memory creation at Phase 01"
