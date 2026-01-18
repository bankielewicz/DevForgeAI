#!/bin/bash
# Test AC-1: TodoWrite Created at Phase 0 Start (all 5 phases as "pending")
# Expected: FAIL initially (before implementation)

SKILL_FILE=".claude/skills/devforgeai-qa/SKILL.md"

echo "=== AC-1: Initial TodoWrite at Phase 0 Start ==="

# Test: TodoWrite with 5 phases present in Phase 0 section (lines 97-150)
PHASE0_CONTENT=$(sed -n '97,200p' "$SKILL_FILE")

# Check for TodoWrite call with Phase 0 in_progress and Phases 1-4 pending
if echo "$PHASE0_CONTENT" | grep -qE "TodoWrite\s*\(" && \
   echo "$PHASE0_CONTENT" | grep -qE "Phase 0.*in_progress" && \
   echo "$PHASE0_CONTENT" | grep -qE "Phase 1.*pending" && \
   echo "$PHASE0_CONTENT" | grep -qE "Phase 2.*pending" && \
   echo "$PHASE0_CONTENT" | grep -qE "Phase 3.*pending" && \
   echo "$PHASE0_CONTENT" | grep -qE "Phase 4.*pending"; then
    echo "PASS: Initial TodoWrite found (Phase 0 in_progress, Phases 1-4 pending)"
    exit 0
else
    echo "FAIL: Missing initial TodoWrite with 5 pending phases in Phase 0 section"
    exit 1
fi
