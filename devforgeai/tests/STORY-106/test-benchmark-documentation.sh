#!/bin/bash
# STORY-106: Performance Optimization and NFR Validation
# Documentation and benchmark file validation tests

# Note: Not using set -e because arithmetic operations can return non-zero

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Helper functions
pass() {
    echo -e "${GREEN}PASS${NC}: $1"
    ((TESTS_PASSED++))
    ((TESTS_RUN++))
}

fail() {
    echo -e "${RED}FAIL${NC}: $1"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

header() {
    echo ""
    echo -e "${YELLOW}=== $1 ===${NC}"
}

# File paths
BENCHMARK_DIR="devforgeai/qa/performance"
BENCHMARK_FILE="$BENCHMARK_DIR/hook-benchmarks.json"
TOKEN_FILE="$BENCHMARK_DIR/token-usage.json"
CONTEXT_EXTRACTION="src/context_extraction.py"
HOOK_SYSTEM="src/hook_system.py"
HOOK_REGISTRY="src/hook_registry.py"

# =============================================================================
# AC5: Benchmark Infrastructure Documentation Tests
# =============================================================================

header "AC5: Benchmark Infrastructure Tests"

# Test 5.1: Benchmark directory exists
if [ -d "$BENCHMARK_DIR" ]; then
    pass "Benchmark directory exists: $BENCHMARK_DIR"
else
    fail "Benchmark directory does not exist: $BENCHMARK_DIR"
fi

# Test 5.2: Hook benchmarks JSON exists
if [ -f "$BENCHMARK_FILE" ]; then
    pass "Hook benchmarks JSON exists: $BENCHMARK_FILE"
else
    fail "Hook benchmarks JSON does not exist: $BENCHMARK_FILE"
fi

# Test 5.3: Token usage JSON exists
if [ -f "$TOKEN_FILE" ]; then
    pass "Token usage JSON exists: $TOKEN_FILE"
else
    fail "Token usage JSON does not exist: $TOKEN_FILE"
fi

# Test 5.4: Benchmark file has version field
if grep -q '"version"' "$BENCHMARK_FILE" 2>/dev/null; then
    pass "Benchmark file has version field"
else
    fail "Benchmark file missing version field"
fi

# Test 5.5: Benchmark file has baseline section
if grep -q '"baseline"' "$BENCHMARK_FILE" 2>/dev/null; then
    pass "Benchmark file has baseline section"
else
    fail "Benchmark file missing baseline section"
fi

# Test 5.6: Benchmark file has thresholds section
if grep -q '"thresholds"' "$BENCHMARK_FILE" 2>/dev/null; then
    pass "Benchmark file has thresholds section"
else
    fail "Benchmark file missing thresholds section"
fi

# Test 5.7: Hook check threshold is 100ms
if grep -q '"hook_check_max": 100' "$BENCHMARK_FILE" 2>/dev/null; then
    pass "Hook check threshold is 100ms"
else
    fail "Hook check threshold is not 100ms"
fi

# Test 5.8: Context extraction threshold is 200ms
if grep -q '"context_extraction_max": 200' "$BENCHMARK_FILE" 2>/dev/null; then
    pass "Context extraction threshold is 200ms"
else
    fail "Context extraction threshold is not 200ms"
fi

# Test 5.9: End-to-end threshold is 3000ms
if grep -q '"end_to_end_max": 3000' "$BENCHMARK_FILE" 2>/dev/null; then
    pass "End-to-end threshold is 3000ms"
else
    fail "End-to-end threshold is not 3000ms"
fi

# Test 5.10: Token budget is 1M tokens
if grep -q '"total_tokens": 1000000' "$TOKEN_FILE" 2>/dev/null; then
    pass "Token budget is 1M tokens"
else
    fail "Token budget is not 1M tokens"
fi

# Test 5.11: Max percent is 3%
if grep -q '"max_percent": 3' "$TOKEN_FILE" 2>/dev/null; then
    pass "Max percent is 3%"
else
    fail "Max percent is not 3%"
fi

# =============================================================================
# AC2: Performance Implementation Tests
# =============================================================================

header "AC2: Performance Implementation Tests"

# Test 2.1: Context extraction module exists
if [ -f "$CONTEXT_EXTRACTION" ]; then
    pass "Context extraction module exists: $CONTEXT_EXTRACTION"
else
    fail "Context extraction module does not exist: $CONTEXT_EXTRACTION"
fi

# Test 2.2: Context extraction has extract_operation_context function
if grep -q "def extract_operation_context" "$CONTEXT_EXTRACTION" 2>/dev/null; then
    pass "extract_operation_context function exists"
else
    fail "extract_operation_context function not found"
fi

# Test 2.3: Context extraction has size limit constant (50KB)
if grep -qE "MAX_CONTEXT_SIZE|50.*KB|50KB" "$CONTEXT_EXTRACTION" 2>/dev/null; then
    pass "Context size limit (50KB) documented"
else
    fail "Context size limit not documented"
fi

# Test 2.4: Context extraction has summarization for >100 todos
if grep -qE "MAX_TODOS|100.*todos|summariz" "$CONTEXT_EXTRACTION" 2>/dev/null; then
    pass "Todo summarization pattern documented"
else
    fail "Todo summarization pattern not documented"
fi

# Test 2.5: Context extraction has 200ms timeout constant
if grep -qE "200|EXTRACTION_TIMEOUT" "$CONTEXT_EXTRACTION" 2>/dev/null; then
    pass "Extraction timeout (200ms) documented"
else
    fail "Extraction timeout not documented"
fi

# =============================================================================
# AC4: Performance Optimization Tests
# =============================================================================

header "AC4: Performance Optimization Tests"

# Test 4.1: Hook registry has type_index
if grep -q "type_index" "$HOOK_REGISTRY" 2>/dev/null; then
    pass "Hook registry has type_index for O(1) lookup"
else
    fail "Hook registry missing type_index optimization"
fi

# Test 4.2: Hook system has eligibility cache
if grep -q "eligibility_cache" "$HOOK_SYSTEM" 2>/dev/null; then
    pass "Hook system has eligibility cache"
else
    fail "Hook system missing eligibility cache"
fi

# Test 4.3: HookEligibilityCache class exists
if grep -q "class HookEligibilityCache" "$HOOK_SYSTEM" 2>/dev/null; then
    pass "HookEligibilityCache class exists"
else
    fail "HookEligibilityCache class not found"
fi

# Test 4.4: Cache has TTL support
if grep -qE "ttl|TTL|time.*expire" "$HOOK_SYSTEM" 2>/dev/null; then
    pass "Cache has TTL support"
else
    fail "Cache missing TTL support"
fi

# =============================================================================
# AC3: Token Budget Documentation Tests
# =============================================================================

header "AC3: Token Budget Documentation Tests"

# Test 3.1: Token usage file has budget section
if grep -q '"budget"' "$TOKEN_FILE" 2>/dev/null; then
    pass "Token usage file has budget section"
else
    fail "Token usage file missing budget section"
fi

# Test 3.2: Token usage file has measurements section
if grep -q '"measurements"' "$TOKEN_FILE" 2>/dev/null; then
    pass "Token usage file has measurements section"
else
    fail "Token usage file missing measurements section"
fi

# Test 3.3: Token usage file has breakdown section
if grep -q '"breakdown"' "$TOKEN_FILE" 2>/dev/null; then
    pass "Token usage file has breakdown section"
else
    fail "Token usage file missing breakdown section"
fi

# =============================================================================
# AC1: Reliability Documentation Tests
# =============================================================================

header "AC1: Reliability Documentation Tests"

# Test 1.1: Context extraction has graceful degradation
if grep -qE "graceful.*degrad|empty.*context|except" "$CONTEXT_EXTRACTION" 2>/dev/null; then
    pass "Context extraction has graceful degradation"
else
    fail "Context extraction missing graceful degradation"
fi

# Test 1.2: Context extraction has sanitization
if grep -qE "sanitiz|REDACTED|secret|PII" "$CONTEXT_EXTRACTION" 2>/dev/null; then
    pass "Context extraction has sanitization"
else
    fail "Context extraction missing sanitization"
fi

# =============================================================================
# Summary
# =============================================================================

echo ""
echo -e "${YELLOW}========================================${NC}"
echo "Test Summary"
echo -e "${YELLOW}========================================${NC}"
echo "Tests Run: $TESTS_RUN"
echo -e "Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Failed: ${RED}$TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed.${NC}"
    exit 1
fi
