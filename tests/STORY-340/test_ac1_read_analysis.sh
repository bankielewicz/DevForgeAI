#!/bin/bash
# Test AC#1: Read ai-analysis.json
# Verifies dev-result-interpreter.md contains Read() instruction for ai-analysis.json

set -e
TARGET_FILE=".claude/agents/dev-result-interpreter.md"

echo "AC#1: Verifying Read() instruction for ai-analysis.json..."

# Test 1: Read() call with ai-analysis path pattern
if ! grep -q 'Read.*ai-analysis' "$TARGET_FILE"; then
    echo "FAIL: Missing Read() instruction for ai-analysis.json"
    exit 1
fi

# Test 2: Path uses STORY_ID variable
if ! grep -q 'devforgeai/feedback/ai-analysis.*STORY' "$TARGET_FILE"; then
    echo "FAIL: Path missing STORY_ID variable reference"
    exit 1
fi

echo "PASS: AC#1 Read ai-analysis.json"
