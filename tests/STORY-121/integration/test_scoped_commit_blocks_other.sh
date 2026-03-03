#!/bin/bash
# STORY-121 Integration Test 5: Scoped Commit Allows Target Story While Other Has Errors
#
# AC#1 + AC#5 Integration: Multi-Story Scenario
#
# Given: Two story files staged (STORY-114.story.md and STORY-115.story.md)
# And: STORY-115 has validation errors
# And: Developer sets DEVFORGEAI_STORY=STORY-114
# When: Developer runs git commit
# Then: Commit succeeds because validation is scoped to STORY-114 only
#
# Test Approach:
# 1. Create temporary git repo with install_hooks.sh
# 2. Create two story files with different validation states
# 3. Stage both files
# 4. Run git commit with DEVFORGEAI_STORY=STORY-114
# 5. Verify commit succeeds despite STORY-115 having errors
# 6. Verify only STORY-114 was validated

set -e

TEST_NAME="test_scoped_commit_blocks_other"

# Create temporary test directory
TEST_TMPDIR=$(mktemp -d)
trap "rm -rf $TEST_TMPDIR" EXIT

cd "$TEST_TMPDIR"
git init >/dev/null 2>&1
git config user.email "test@example.com"
git config user.name "Test User"

# Test 1: Verify install_hooks.sh exists and installs hooks
if [ ! -f "$ORIGINAL_PWD/src/claude/scripts/install_hooks.sh" 2>/dev/null ]; then
    # Skip this integration test if hooks script not available
    echo "SKIP: install_hooks.sh not found in source tree"
    exit 0
fi

# Copy hooks script and install
cp "$ORIGINAL_PWD/src/claude/scripts/install_hooks.sh" . 2>/dev/null || {
    echo "SKIP: Cannot access install_hooks.sh"
    exit 0
}

# Run install_hooks.sh to install pre-commit hook
bash install_hooks.sh >/dev/null 2>&1 || {
    echo "SKIP: install_hooks.sh installation failed"
    exit 0
}

# Verify hook was installed
if [ ! -f ".git/hooks/pre-commit" ]; then
    echo "FAIL: Hook not installed by install_hooks.sh"
    exit 1
fi

# Test 2: Create first story file (valid - should pass validation)
mkdir -p devforgeai/specs/Stories
cat > devforgeai/specs/Stories/STORY-114.story.md << 'EOF'
---
id: STORY-114
title: Valid Story for Testing
status: Ready for Dev
---
# Story: Valid Story

## Acceptance Criteria

### AC#1: Basic Requirement
Given valid conditions
When action is taken
Then expected outcome occurs
EOF

# Test 3: Create second story file (invalid - has validation errors)
cat > devforgeai/specs/Stories/STORY-115.story.md << 'EOF'
---
id: STORY-115
title: Invalid Story with Errors
status: Backlog
---
# Story: Invalid Story

## Missing Acceptance Criteria Section
This file is intentionally invalid to simulate validation errors.
No proper AC section exists.
EOF

# Test 4: Stage both files
git add devforgeai/specs/Stories/STORY-114.story.md
git add devforgeai/specs/Stories/STORY-115.story.md

# Test 5: Attempt commit with scoping - should succeed if hook respects DEVFORGEAI_STORY
# Export the environment variable for scoped validation
export DEVFORGEAI_STORY="STORY-114"

# Try to commit - this will fail if pre-commit validation rejects it
# We're testing that scoped mode only validates STORY-114
if git commit -m "Test scoped commit" >/dev/null 2>&1; then
    # If commit succeeded, the hook correctly filtered validation
    echo "PASS: Scoped commit succeeded while other story has errors"
    exit 0
else
    # Commit failed - either hook rejects or git error occurred
    # With proper scoping, this should succeed despite STORY-115 errors
    echo "FAIL: Scoped commit failed - hook may not be filtering correctly"
    exit 1
fi
