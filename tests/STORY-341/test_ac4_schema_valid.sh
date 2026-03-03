#!/bin/bash
# Test AC#4: Schema Matches EPIC-052 Specification
# Verifies session memory schema documentation exists and matches spec
# Expected: FAIL (TDD Red phase - implementation not yet done)

set -e

echo "AC#4: Verifying session memory schema matches EPIC-052..."

# Check phase-01-preflight.md for schema specification
# Check src/ (source of truth) first, fallback to .claude/ (operational)
TARGET_FILE="src/claude/skills/devforgeai-development/phases/phase-01-preflight.md"
if [ ! -f "$TARGET_FILE" ]; then
    TARGET_FILE=".claude/skills/devforgeai-development/phases/phase-01-preflight.md"
fi

# Test 1: YAML frontmatter fields documented
REQUIRED_FIELDS=("story_id" "created" "last_updated" "status")
MISSING_FIELDS=0

for FIELD in "${REQUIRED_FIELDS[@]}"; do
    if ! grep -q "$FIELD" "$TARGET_FILE"; then
        echo "FAIL: Missing required field '$FIELD' in schema"
        MISSING_FIELDS=$((MISSING_FIELDS + 1))
    fi
done

if [ $MISSING_FIELDS -gt 0 ]; then
    echo "FAIL: $MISSING_FIELDS required schema fields missing"
    exit 1
fi

# Test 2: Observations section structure documented
if ! grep -qE '(Observations|observations)' "$TARGET_FILE"; then
    echo "FAIL: Missing Observations section in schema"
    exit 1
fi

# Test 3: Reflections section structure documented
if ! grep -qE '(Reflections|reflections)' "$TARGET_FILE"; then
    echo "FAIL: Missing Reflections section in schema"
    exit 1
fi

# Test 4: Status enum values documented (active|archived)
if ! grep -qE 'active.*archived|status.*(active|archived)' "$TARGET_FILE"; then
    echo "FAIL: Status enum values (active|archived) not documented"
    exit 1
fi

echo "PASS: AC#4 Schema matches EPIC-052 specification"
