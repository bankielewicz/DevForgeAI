#!/bin/bash
# Test AC#5: File Path Reference
# Verifies dev-result-interpreter.md shows full analysis path in output

set -e
TARGET_FILE=".claude/agents/dev-result-interpreter.md"

echo "AC#5: Verifying file path reference..."

# Test 1: Full analysis path shown
if ! grep -q 'Full analysis.*devforgeai/feedback/ai-analysis\|devforgeai/feedback/ai-analysis.*STORY' "$TARGET_FILE"; then
    echo "FAIL: Missing full analysis path reference"
    exit 1
fi

# Test 2: Path includes {STORY_ID} placeholder
if ! grep -q 'ai-analysis/{STORY_ID}\|ai-analysis/.*STORY' "$TARGET_FILE"; then
    echo "FAIL: Path missing {STORY_ID} placeholder"
    exit 1
fi

echo "PASS: AC#5 File Path Reference"
