#!/usr/bin/env bash
# STORY-375 Edge Case Tests
# Tests verify the research document handles edge cases properly:
#   - Treelint unavailability handling (SKIPPED annotation)
#   - Division-by-zero handling for zero-result queries
#   - Unsupported file type fallback tracking
#   - Negative reduction percentages (regression)

set -uo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
RESEARCH_DIR="$PROJECT_ROOT/devforgeai/specs/research"

# Find the research document
RESEARCH_FILE=""
for f in "$RESEARCH_DIR"/RESEARCH-*-treelint-token-validation*.md; do
    if [ -f "$f" ]; then
        RESEARCH_FILE="$f"
        break
    fi
done

PASS=0
FAIL=0
TOTAL=0

run_test() {
    local name="$1"
    local result="$2"
    TOTAL=$((TOTAL + 1))
    if [ "$result" -eq 0 ]; then
        PASS=$((PASS + 1))
        echo "  PASS: $name"
    else
        FAIL=$((FAIL + 1))
        echo "  FAIL: $name"
    fi
}

echo "=== Edge Case Tests ==="
echo ""

# Guard: if no document, all tests fail
if [ -z "$RESEARCH_FILE" ] || [ ! -f "$RESEARCH_FILE" ]; then
    run_test "Research document exists" 1
    run_test "Treelint unavailability handling documented" 1
    run_test "Division-by-zero handling documented" 1
    run_test "Negative reduction (regression) handling documented" 1
    run_test "Fallback annotation pattern exists" 1
    run_test "SKIPPED or No Fallback annotation present" 1
else
    run_test "Research document exists" 0

    # Test 1: Treelint unavailability handling documented
    # The document should mention how unavailability is handled
    if grep -qi "unavailab\|SKIPPED\|daemon.*fail\|treelint.*fail\|treelint.*not.*install" "$RESEARCH_FILE" 2>/dev/null; then
        run_test "Treelint unavailability handling documented" 0
    else
        run_test "Treelint unavailability handling documented" 1
    fi

    # Test 2: Division-by-zero handling documented (or N/A noted)
    # The document should mention zero-result handling or show calculation avoids it
    if grep -qi "division.*zero\|zero.*result\|N/A.*no.*result\|baseline.*zero\|empty.*result" "$RESEARCH_FILE" 2>/dev/null; then
        run_test "Division-by-zero handling documented" 0
    else
        # Alternative: If all queries have non-zero results, no division-by-zero scenario exists
        # Check if the document notes this or has positive baselines
        if grep -qE "Baseline.*Chars.*[1-9][0-9]*" "$RESEARCH_FILE" 2>/dev/null; then
            run_test "Division-by-zero handling documented" 0
        else
            run_test "Division-by-zero handling documented" 1
        fi
    fi

    # Test 3: Negative reduction (regression) handling
    # Document should show negative percentages or REGRESSION classification
    if grep -qi "REGRESSION\|negative.*reduction\|-[0-9]*\.[0-9]*%\|treelint.*worse" "$RESEARCH_FILE" 2>/dev/null; then
        run_test "Negative reduction (regression) handling documented" 0
    else
        run_test "Negative reduction (regression) handling documented" 1
    fi

    # Test 4: Fallback annotation pattern exists in table structure
    if grep -qi "Fallback.*Annotation\|fallback.*event\|No.*Fallback" "$RESEARCH_FILE" 2>/dev/null; then
        run_test "Fallback annotation pattern exists" 0
    else
        run_test "Fallback annotation pattern exists" 1
    fi

    # Test 5: SKIPPED or No Fallback annotation present (indicating scenario handling)
    if grep -qiE "SKIPPED|No Fallback|fallback.*=.*0" "$RESEARCH_FILE" 2>/dev/null; then
        run_test "SKIPPED or No Fallback annotation present" 0
    else
        run_test "SKIPPED or No Fallback annotation present" 1
    fi
fi

echo ""
echo "--- Edge Case Results: $PASS/$TOTAL passed, $FAIL failed ---"

if [ "$FAIL" -gt 0 ]; then
    exit 1
fi
exit 0
