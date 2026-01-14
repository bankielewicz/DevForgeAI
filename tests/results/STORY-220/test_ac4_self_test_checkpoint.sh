#!/bin/bash
# Test AC-4: Self-Test Checkpoint
# DOC-005: Include self-test checkpoint for skill execution verification
# Expected: FAIL initially (before implementation)

CLAUDE_FILE="src/CLAUDE.md"

echo "=== AC-4: Self-Test Checkpoint ==="

# Check if CLAUDE.md exists
if [ ! -f "$CLAUDE_FILE" ]; then
    echo "FAIL: Target file $CLAUDE_FILE does not exist"
    exit 1
fi

# Get content of the CRITICAL section
CRITICAL_LINE=$(grep -n "## CRITICAL: No Deviation from Skill Phases" "$CLAUDE_FILE" | head -1 | cut -d: -f1)

if [ -z "$CRITICAL_LINE" ]; then
    echo "FAIL: Section '## CRITICAL: No Deviation from Skill Phases' not found"
    exit 1
fi

# Extract section content (skip header, find next ## section)
SECTION_START=$((CRITICAL_LINE + 1))
SECTION_END=$((CRITICAL_LINE + 150))
SECTION_CONTENT=$(sed -n "${SECTION_START},${SECTION_END}p" "$CLAUDE_FILE" | sed '/^## [A-Za-z]/q' | head -n -1)

# Test 1: Contains self-test or checkpoint section
if echo "$SECTION_CONTENT" | grep -qiE "(self.?test|checkpoint|verification|checklist)"; then
    echo "  [PASS] Contains self-test/checkpoint section"
else
    echo "  [FAIL] Missing self-test/checkpoint section"
    exit 1
fi

# Test 2: Mentions MANDATORY subagents
if echo "$SECTION_CONTENT" | grep -qiE "(MANDATORY|mandatory|required).*(subagent|agent)"; then
    echo "  [PASS] Mentions MANDATORY subagents"
else
    echo "  [FAIL] Missing reference to MANDATORY subagents"
    exit 1
fi

# Test 3: Contains HALT instruction
if echo "$SECTION_CONTENT" | grep -qE "\bHALT\b"; then
    echo "  [PASS] Contains HALT instruction"
else
    echo "  [FAIL] Missing HALT instruction"
    exit 1
fi

# Test 4: Clear test criteria (questions or checkboxes or verification steps)
if echo "$SECTION_CONTENT" | grep -qE "(\[ \]|\[x\]|\?|verify|check:|question)"; then
    echo "  [PASS] Contains clear test criteria (checkboxes/questions/verification steps)"
else
    echo "  [FAIL] Missing clear test criteria"
    exit 1
fi

# Test 5: Test mentions skill phase completion verification
if echo "$SECTION_CONTENT" | grep -qiE "(phase|step).*(complete|finish|execute|skip)"; then
    echo "  [PASS] Contains phase completion verification guidance"
else
    echo "  [FAIL] Missing phase completion verification guidance"
    exit 1
fi

echo "PASS: AC-4 - Self-test checkpoint with all required elements"
exit 0
