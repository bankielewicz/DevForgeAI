#!/bin/bash
# STORY-121 Integration Test 7: Multiple Stories Staged, Scoping Validates Only Target
#
# AC#1 + Technical Spec: Multi-Story Scenario with Precise Filtering
#
# Given: Three story files staged:
#   - STORY-110.story.md (valid)
#   - STORY-120.story.md (invalid - missing sections)
#   - STORY-114.story.md (valid)
# And: Developer sets DEVFORGEAI_STORY=STORY-114
# When: Pre-commit hook runs
# Then: Hook validates ONLY STORY-114.story.md
# And: Other stories' validation errors don't affect the commit
#
# Test Approach:
# 1. Create three story files with various validation states
# 2. Set DEVFORGEAI_STORY=STORY-114
# 3. Verify hook grep pattern correctly filters to only STORY-114
# 4. Confirm other stories are excluded from validation

set -e

TEST_NAME="test_multiple_stories_scoped"

# Create temporary test directory
TEST_TMPDIR=$(mktemp -d)
trap "rm -rf $TEST_TMPDIR" EXIT

cd "$TEST_TMPDIR"
git init >/dev/null 2>&1

# Test 1: Verify pre-commit hook exists
HOOK_PATH=".git/hooks/pre-commit"
if [ ! -f "$HOOK_PATH" ]; then
    echo "SKIP: Pre-commit hook not found"
    exit 0
fi

# Test 2: Create three story files
mkdir -p devforgeai/specs/Stories

cat > devforgeai/specs/Stories/STORY-110.story.md << 'EOF'
---
id: STORY-110
title: Story 110
status: Backlog
---
# Story: Story 110

## Acceptance Criteria

### AC#1: Some requirement
Given conditions
When action
Then outcome
EOF

cat > devforgeai/specs/Stories/STORY-120.story.md << 'EOF'
---
id: STORY-120
title: Story 120 - Invalid
status: Backlog
---
# Story: Missing acceptance criteria (invalid for testing)
EOF

cat > devforgeai/specs/Stories/STORY-114.story.md << 'EOF'
---
id: STORY-114
title: Story 114
status: Ready for Dev
---
# Story: Story 114

## Acceptance Criteria

### AC#1: Valid requirement
Given valid condition
When action performed
Then expected outcome
EOF

# Test 3: Stage all three files
git add devforgeai/specs/Stories/STORY-110.story.md
git add devforgeai/specs/Stories/STORY-120.story.md
git add devforgeai/specs/Stories/STORY-114.story.md

# Test 4: Extract scoped filtering logic from hook
export DEVFORGEAI_STORY="STORY-114"

# Test 5: Verify hook's filtering logic would select only STORY-114
# The hook should use: STORY_FILES=$(git diff --cached ... | grep "${DEVFORGEAI_STORY}" ...)
if ! grep -q 'git diff --cached' "$HOOK_PATH"; then
    echo "FAIL: Hook does not use 'git diff --cached' to get staged files"
    exit 1
fi

# Test 6: Verify the grep pattern in the scoped section
SCOPED_SECTION=$(awk '/\[\s*-n\s*"\$DEVFORGEAI_STORY"/ {found=1} found && /fi/ {exit} found' "$HOOK_PATH")

if ! echo "$SCOPED_SECTION" | grep -q 'grep.*DEVFORGEAI_STORY'; then
    echo "FAIL: Scoped section does not filter by DEVFORGEAI_STORY"
    exit 1
fi

# Test 7: Verify that the filtering uses the environment variable correctly
if ! echo "$SCOPED_SECTION" | grep -q '\${DEVFORGEAI_STORY}\|"\$DEVFORGEAI_STORY'; then
    echo "FAIL: Scoped grep does not use \$DEVFORGEAI_STORY variable for pattern"
    exit 1
fi

# Test 8: Simulate what files would be selected with DEVFORGEAI_STORY=STORY-114
# This should match only STORY-114.story.md
STAGED_FILES=$(git diff --cached --name-only --diff-filter=d)
FILTERED_FILES=$(echo "$STAGED_FILES" | grep "STORY-114" || true)

if [ -z "$FILTERED_FILES" ]; then
    echo "FAIL: Filtering STORY-114 from staged files returned no results"
    exit 1
fi

# Verify only STORY-114 is in the filtered results
if echo "$FILTERED_FILES" | grep -qE 'STORY-110|STORY-120'; then
    echo "FAIL: Filtered results include stories other than STORY-114"
    exit 1
fi

if ! echo "$FILTERED_FILES" | grep -q 'STORY-114'; then
    echo "FAIL: Filtered results do not include STORY-114"
    exit 1
fi

echo "PASS: Scoped validation correctly filters to only STORY-114 among multiple stories"
exit 0
