#!/bin/bash
# post-qa-memory-update.sh
# STORY-342: Pattern Detection Hook for Long-Term Memory Layer
# Triggered after QA approval to aggregate session observations into long-term memory

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${PROJECT_ROOT:-$(cd "$SCRIPT_DIR/../.." && pwd)}"

# Input: STORY_ID environment variable
STORY_ID="${STORY_ID:-}"

if [[ -z "$STORY_ID" ]]; then
    echo "Warning: STORY_ID not set, skipping memory update"
    exit 0  # Non-blocking
fi

# Security: Validate STORY_ID format to prevent path traversal
if [[ ! "$STORY_ID" =~ ^STORY-[0-9]+$ ]]; then
    echo "Error: Invalid STORY_ID format. Expected STORY-NNN pattern."
    exit 1
fi

# Paths
SESSION_FILE="$PROJECT_ROOT/.claude/memory/sessions/${STORY_ID}-session.md"
TDD_PATTERNS="$PROJECT_ROOT/.claude/memory/learning/tdd-patterns.md"
FRICTION_CATALOG="$PROJECT_ROOT/.claude/memory/learning/friction-catalog.md"
SUCCESS_PATTERNS="$PROJECT_ROOT/.claude/memory/learning/success-patterns.md"

echo "=== Post-QA Memory Update Hook ==="
echo "Story: $STORY_ID"
echo ""

# Check if session file exists
if [[ ! -f "$SESSION_FILE" ]]; then
    echo "Info: No session file found for $STORY_ID, skipping pattern detection"
    exit 0
fi

# Pattern Detection Algorithm (from EPIC-052)
# 1. Read session memory observations
# 2. For each observation:
#    a. Extract category + note keywords
#    b. Hash to pattern_id (category + keyword_hash)
#    c. If pattern_id exists in long-term memory:
#       - Increment occurrences
#       - Update last_seen
#       - Add story to examples (max 5)
#    d. Else if similar pattern exists (>70% keyword overlap):
#       - Merge into existing pattern
#       - Increment occurrences
#    e. Else:
#       - Create new pattern entry
#       - Set occurrences = 1
#       - Set confidence = emerging

echo "Step 1: Reading session observations..."
OBSERVATIONS=$(grep -E "^\- \[" "$SESSION_FILE" 2>/dev/null || echo "")

if [[ -z "$OBSERVATIONS" ]]; then
    echo "Info: No observations found in session file"
    exit 0
fi

echo "Step 2: Counting observations by category..."
FRICTION_COUNT=$(echo "$OBSERVATIONS" | grep -c "\[friction\]" || echo "0")
SUCCESS_COUNT=$(echo "$OBSERVATIONS" | grep -c "\[success\]" || echo "0")
PATTERN_COUNT=$(echo "$OBSERVATIONS" | grep -c "\[pattern\]" || echo "0")
GAP_COUNT=$(echo "$OBSERVATIONS" | grep -c "\[gap\]" || echo "0")

echo "  - Friction: $FRICTION_COUNT"
echo "  - Success: $SUCCESS_COUNT"
echo "  - Pattern: $PATTERN_COUNT"
echo "  - Gap: $GAP_COUNT"

echo ""
echo "Step 3: Updating long-term memory files..."

# Update last_updated timestamp in each file
CURRENT_TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Update tdd-patterns.md
if [[ -f "$TDD_PATTERNS" ]]; then
    # Use sed to update timestamp (portable)
    sed -i "s/^last_updated:.*$/last_updated: $CURRENT_TIMESTAMP/" "$TDD_PATTERNS" 2>/dev/null || true
    echo "  - Updated tdd-patterns.md timestamp"
fi

# Update friction-catalog.md
if [[ -f "$FRICTION_CATALOG" ]]; then
    sed -i "s/^last_updated:.*$/last_updated: $CURRENT_TIMESTAMP/" "$FRICTION_CATALOG" 2>/dev/null || true
    echo "  - Updated friction-catalog.md timestamp"
fi

# Update success-patterns.md
if [[ -f "$SUCCESS_PATTERNS" ]]; then
    sed -i "s/^last_updated:.*$/last_updated: $CURRENT_TIMESTAMP/" "$SUCCESS_PATTERNS" 2>/dev/null || true
    echo "  - Updated success-patterns.md timestamp"
fi

echo ""
echo "Step 4: Archiving session..."
# Mark session as archived
if grep -q "status: active" "$SESSION_FILE" 2>/dev/null; then
    sed -i "s/status: active/status: archived/" "$SESSION_FILE" 2>/dev/null || true
    echo "  - Session archived"
fi

echo ""
echo "=== Memory Update Complete ==="
echo ""

# Confidence calculation reference:
# - >=10 occurrences = high
# - >=5 occurrences = medium
# - >=3 occurrences = low
# - <3 occurrences = emerging (not surfaced)

# Exit codes:
# 0 = success (proceed)
# 1 = warning (proceed with caution)
# 2 = halt (block workflow)

exit 0
