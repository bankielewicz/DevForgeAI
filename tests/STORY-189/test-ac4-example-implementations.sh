#!/bin/bash
# STORY-189 AC-4: Example Implementations Provided
# Verifies example hook implementations are included

set -e

HOOKS_README=".claude/hooks/README.md"

echo "=== STORY-189 AC-4: Example Implementations Provided ==="

FAILED=0

# Test 1: Check for code block with example implementation
# Look for bash code block markers near qa hook content
if grep -A 20 "QA Lifecycle Hooks" "$HOOKS_README" | grep -q '```'; then
    echo "PASS: Code block found in QA Lifecycle section"
else
    echo "FAIL: No code block found in QA Lifecycle section"
    FAILED=1
fi

# Test 2: Check for example script content (shebang or script structure)
if grep -A 30 "QA Lifecycle Hooks" "$HOOKS_README" | grep -q '#!/bin/bash\|echo\|exit'; then
    echo "PASS: Example script content found"
else
    echo "FAIL: No example script content found (#!/bin/bash, echo, or exit)"
    FAILED=1
fi

if [[ $FAILED -eq 1 ]]; then
    echo ""
    echo "RESULT: Example implementations missing or incomplete"
    exit 1
fi

echo ""
echo "RESULT: Example implementations provided"
exit 0
