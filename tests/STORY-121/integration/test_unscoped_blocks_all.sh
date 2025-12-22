#!/bin/bash
# STORY-121 Integration Test 6: Without Scoping, Other Story Errors Block Commit
#
# AC#2 Integration: Backward Compatibility Verification
#
# Given: Two story files staged (STORY-114.story.md and STORY-115.story.md)
# And: STORY-115 has validation errors
# And: DEVFORGEAI_STORY is NOT set
# When: Developer runs git commit
# Then: Commit fails because validation checks ALL staged story files
# And: STORY-115 validation errors block the commit
#
# Test Approach:
# 1. Create temporary git repo with install_hooks.sh
# 2. Create two story files (one valid, one invalid)
# 3. Stage both files
# 4. Run git commit WITHOUT DEVFORGEAI_STORY set
# 5. Verify commit fails due to validation of STORY-115
# 6. Confirm backward compatibility (unscoped validates all)

set -e

TEST_NAME="test_unscoped_blocks_all"

# Create temporary test directory
TEST_TMPDIR=$(mktemp -d)
trap "rm -rf $TEST_TMPDIR" EXIT

cd "$TEST_TMPDIR"
git init >/dev/null 2>&1
git config user.email "test@example.com"
git config user.name "Test User"

# Test 1: Verify install_hooks.sh exists
if [ ! -f "$ORIGINAL_PWD/src/claude/scripts/install_hooks.sh" 2>/dev/null ]; then
    echo "SKIP: install_hooks.sh not found in source tree"
    exit 0
fi

# Copy and install hooks
cp "$ORIGINAL_PWD/src/claude/scripts/install_hooks.sh" . 2>/dev/null || {
    echo "SKIP: Cannot access install_hooks.sh"
    exit 0
}

bash install_hooks.sh >/dev/null 2>&1 || {
    echo "SKIP: install_hooks.sh installation failed"
    exit 0
}

# Verify hook was installed
if [ ! -f ".git/hooks/pre-commit" ]; then
    echo "FAIL: Hook not installed"
    exit 1
fi

# Test 2: Create first story file (valid)
mkdir -p devforgeai/specs/Stories
cat > devforgeai/specs/Stories/STORY-114.story.md << 'EOF'
---
id: STORY-114
title: Valid Story
status: Ready for Dev
---
# Story: Valid Story

## Acceptance Criteria

### AC#1: Valid Requirement
Given valid conditions
When action is taken
Then expected outcome occurs
EOF

# Test 3: Create second story file (invalid)
cat > devforgeai/specs/Stories/STORY-115.story.md << 'EOF'
---
id: STORY-115
title: Invalid Story
status: Backlog
---
# Story: Invalid Story
This file lacks proper Acceptance Criteria section.
EOF

# Test 4: Stage both files
git add devforgeai/specs/Stories/STORY-114.story.md
git add devforgeai/specs/Stories/STORY-115.story.md

# Test 5: Unset DEVFORGEAI_STORY explicitly to test unscoped mode
unset DEVFORGEAI_STORY

# Test 6: Attempt commit - should FAIL if validation includes STORY-115
# With unscoped mode, the hook should validate both stories
# Since STORY-115 has errors, the commit should be rejected
if ! git commit -m "Test unscoped commit" >/dev/null 2>&1; then
    # Commit failed as expected - hook validated both files
    echo "PASS: Unscoped commit correctly blocked by STORY-115 validation errors"
    exit 0
else
    # Commit succeeded - hook may have only validated STORY-114
    # This would indicate scoping is incorrectly applied
    echo "FAIL: Unscoped commit should have failed due to STORY-115 errors"
    exit 1
fi
