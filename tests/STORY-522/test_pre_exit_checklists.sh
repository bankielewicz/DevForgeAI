#!/bin/bash
# Test: STORY-522 - Phase Execution Checklists
# Validates that all 12 phase files contain Pre-Exit Checklist sections
# Generated: 2026-03-02
# TDD Phase: RED (all tests expected to FAIL)

# === Test Configuration ===
PASSED=0
FAILED=0
PHASE_DIR="src/claude/skills/implementing-stories/phases"

run_test() {
    local name="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        ((PASSED++))
    else
        echo "  FAIL: $name"
        ((FAILED++))
    fi
}

# Helper: extract text AFTER "## Pre-Exit Checklist" header until next "## " header or EOF
extract_checklist() {
    local file="$1"
    if [ ! -f "$file" ]; then
        echo ""
        return
    fi
    sed -n '/^## Pre-Exit Checklist/,/^## [^P]/p' "$file" | head -n -1
}

# Helper: check if a pattern exists within the Pre-Exit Checklist section
checklist_contains() {
    local file="$1"
    local pattern="$2"
    local section
    section=$(extract_checklist "$file")
    if [ -z "$section" ]; then
        return 1
    fi
    echo "$section" | grep -qi "$pattern"
}

# === AC#4: All 12 phase files have Pre-Exit Checklist ===
echo ""
echo "=== AC#4: All 12 phase files have Pre-Exit Checklist ==="

PHASE_FILES=(
    "phase-01-preflight.md"
    "phase-02-test-first.md"
    "phase-03-implementation.md"
    "phase-04-refactoring.md"
    "phase-04.5-ac-verification.md"
    "phase-05-integration.md"
    "phase-05.5-ac-verification.md"
    "phase-06-deferral.md"
    "phase-07-dod-update.md"
    "phase-08-git-workflow.md"
    "phase-09-feedback.md"
    "phase-10-result.md"
)

CHECKLIST_COUNT=0
for f in "${PHASE_FILES[@]}"; do
    if grep -q "^## Pre-Exit Checklist" "$PHASE_DIR/$f" 2>/dev/null; then
        ((CHECKLIST_COUNT++))
    fi
done

test "$CHECKLIST_COUNT" -eq 12
run_test "All 12 phase files contain Pre-Exit Checklist header (found: $CHECKLIST_COUNT/12)" $?

# Individual file checks for AC#4
for f in "${PHASE_FILES[@]}"; do
    grep -q "^## Pre-Exit Checklist" "$PHASE_DIR/$f" 2>/dev/null
    run_test "$f contains Pre-Exit Checklist" $?
done

# === AC#1: phase-01-preflight.md specific items ===
echo ""
echo "=== AC#1: phase-01 Pre-Exit Checklist items ==="

P01="$PHASE_DIR/phase-01-preflight.md"

checklist_contains "$P01" "git-validator invoked"
run_test "phase-01 checklist includes git-validator invoked" $?

checklist_contains "$P01" "context files loaded"
run_test "phase-01 checklist includes context files loaded" $?

checklist_contains "$P01" "story loaded"
run_test "phase-01 checklist includes story loaded" $?

checklist_contains "$P01" "tech-stack-detector invoked"
run_test "phase-01 checklist includes tech-stack-detector invoked" $?

checklist_contains "$P01" "session memory created"
run_test "phase-01 checklist includes session memory created" $?

checklist_contains "$P01" "stale cleanup executed"
run_test "phase-01 checklist includes stale cleanup executed" $?

checklist_contains "$P01" "context-preservation-validator invoked"
run_test "phase-01 checklist includes context-preservation-validator invoked" $?

# === AC#2: phase-02-test-first.md specific items ===
echo ""
echo "=== AC#2: phase-02 Pre-Exit Checklist items ==="

P02="$PHASE_DIR/phase-02-test-first.md"

checklist_contains "$P02" "test-automator invoked"
run_test "phase-02 checklist includes test-automator invoked" $?

checklist_contains "$P02" "RED state verified"
run_test "phase-02 checklist includes RED state verified" $?

checklist_contains "$P02" "snapshot created"
run_test "phase-02 checklist includes snapshot created" $?

checklist_contains "$P02" "snapshot verified via Glob"
run_test "phase-02 checklist includes snapshot verified via Glob" $?

checklist_contains "$P02" "AC checklist updated"
run_test "phase-02 checklist includes AC checklist updated" $?

checklist_contains "$P02" "observation capture executed"
run_test "phase-02 checklist includes observation capture executed" $?

# === AC#3: phase-04-refactoring.md specific items ===
echo ""
echo "=== AC#3: phase-04 Pre-Exit Checklist items ==="

P04="$PHASE_DIR/phase-04-refactoring.md"

checklist_contains "$P04" "refactoring-specialist invoked"
run_test "phase-04 checklist includes refactoring-specialist invoked" $?

checklist_contains "$P04" "coverage validation"
run_test "phase-04 checklist includes coverage validation" $?

checklist_contains "$P04" "code-reviewer invoked"
run_test "phase-04 checklist includes code-reviewer invoked" $?

checklist_contains "$P04" "anti-gaming validation"
run_test "phase-04 checklist includes anti-gaming validation" $?

checklist_contains "$P04" "light QA executed"
run_test "phase-04 checklist includes light QA executed" $?

checklist_contains "$P04" "AC checklist updated"
run_test "phase-04 checklist includes AC checklist updated" $?

checklist_contains "$P04" "observation capture"
run_test "phase-04 checklist includes observation capture" $?

# === Summary ===
echo ""
echo "========================================"
echo "Results: $PASSED passed, $FAILED failed"
echo "========================================"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
