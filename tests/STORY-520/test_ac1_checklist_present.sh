#!/bin/bash
# Test: AC#1 - Phase 1.5 Completion Checklist Present
# Story: STORY-520
# Generated: 2026-03-01

set -euo pipefail

# === Test Configuration ===
PASSED=0
FAILED=0
TARGET_FILE="/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-qa/SKILL.md"

run_test() {
    local name="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        PASSED=$((PASSED + 1))
    else
        echo "  FAIL: $name"
        FAILED=$((FAILED + 1))
    fi
}

echo "=== AC#1: Phase 1.5 Completion Checklist Present ==="
echo ""

# === Test 1: Header exists ===
grep -q "### Phase 1.5 Completion Checklist" "$TARGET_FILE"
run_test "Phase 1.5 Completion Checklist header exists in SKILL.md" $?

# === Test 2: Exactly 5 checkbox items in the checklist section ===
# Extract Phase 1.5 Completion Checklist section (from header to next ### or ## header)
CHECKLIST_ITEMS=$(awk '
    /^### Phase 1\.5 Completion Checklist/ { found=1; next }
    found && /^##/ { found=0 }
    found && /^- \[ \]/ { count++ }
    END { print count+0 }
' "$TARGET_FILE")

if [ "$CHECKLIST_ITEMS" -eq 5 ]; then
    run_test "Exactly 5 checkbox items in Phase 1.5 Completion Checklist (found: $CHECKLIST_ITEMS)" 0
else
    run_test "Exactly 5 checkbox items in Phase 1.5 Completion Checklist (found: $CHECKLIST_ITEMS, expected: 5)" 1
fi

# === Test 3: Item (a) - Diff regression detection ===
SECTION=$(awk '/^### Phase 1\.5 Completion Checklist/{found=1; next} found && /^##/{found=0} found{print}' "$TARGET_FILE")
echo "$SECTION" | grep -qi "diff regression detection" && R=0 || R=1
run_test "Checklist contains item about diff regression detection" $R

# === Test 4: Item (b) - Test integrity snapshot read ===
echo "$SECTION" | grep -qi "test integrity snapshot" && R=0 || R=1
run_test "Checklist contains item about test integrity snapshot" $R

# === Test 5: Item (c) - Checksum comparison ===
echo "$SECTION" | grep -qi "checksum comparison" && R=0 || R=1
run_test "Checklist contains item about checksum comparison" $R

# === Test 6: Item (d) - Findings classified by severity ===
echo "$SECTION" | grep -qi "findings classified.*severity\|severity.*classif" && R=0 || R=1
run_test "Checklist contains item about findings classified by severity" $R

# === Test 7: Item (e) - Phase result determined ===
echo "$SECTION" | grep -qi "phase result determined" && R=0 || R=1
run_test "Checklist contains item about phase result determined" $R

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
