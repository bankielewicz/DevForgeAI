#!/bin/bash
# Test AC#3: Session Memory Archived on Completion
# Verifies archive logic exists for story completion
# Expected: FAIL (TDD Red phase - implementation not yet done)

set -e

echo "AC#3: Verifying session memory archive on completion..."

# Primary location: QA skill or release skill
# Check src/ (source of truth) first
SRC_PREFIX="src/claude"
OP_PREFIX=".claude"
if [ -d "src/claude/skills" ]; then
    PREFIX="src/claude"
else
    PREFIX=".claude"
fi
QA_SKILL="$PREFIX/skills/devforgeai-qa/SKILL.md"
RELEASE_SKILL="$PREFIX/skills/devforgeai-release/SKILL.md"
PHASE_10="$PREFIX/skills/devforgeai-development/phases/phase-10-result.md"

ARCHIVE_FOUND=false

# Test 1: Check QA skill for archive logic
if [ -f "$QA_SKILL" ]; then
    if grep -qE '(archive|archived).*session' "$QA_SKILL"; then
        ARCHIVE_FOUND=true
        echo "INFO: Archive logic found in devforgeai-qa skill"
    fi
fi

# Test 2: Check release skill for archive logic
if [ -f "$RELEASE_SKILL" ]; then
    if grep -qE '(archive|archived).*session' "$RELEASE_SKILL"; then
        ARCHIVE_FOUND=true
        echo "INFO: Archive logic found in devforgeai-release skill"
    fi
fi

# Test 3: Check Phase 10 for archive logic
if [ -f "$PHASE_10" ]; then
    if grep -qE '(archive|archived).*session|status.*archived' "$PHASE_10"; then
        ARCHIVE_FOUND=true
        echo "INFO: Archive logic found in phase-10-result.md"
    fi
fi

# Test 4: Check for status field update to "archived"
if grep -rq 'status.*archived' "$PREFIX/skills/devforgeai-development/"; then
    ARCHIVE_FOUND=true
    echo "INFO: Status=archived pattern found in development skill"
fi

if [ "$ARCHIVE_FOUND" = false ]; then
    echo "FAIL: No session memory archive logic found"
    echo "      Expected in: QA skill, Release skill, or Phase 10"
    exit 1
fi

echo "PASS: AC#3 Session memory archived on completion"
