#!/bin/bash
# Test AC#1: Test Scenario Defined with Reproducible Queries
# STORY-353: Validate Token Reduction with A/B Test
# Status: RED (failing) - Implementation required

set -e

RESEARCH_FILE="devforgeai/specs/research/RESEARCH-007-token-reduction-validation.research.md"
REQUIRED_QUERY_COUNT=5

echo "=== AC#1: Test Scenarios Validation ==="

# Test 1: Research file exists
test_research_file_exists() {
    echo "Test: Research file exists"
    if [[ ! -f "$RESEARCH_FILE" ]]; then
        echo "FAIL: $RESEARCH_FILE does not exist"
        exit 1
    fi
    echo "PASS: Research file exists"
}

# Test 2: At least 5 distinct queries documented (BR-002)
test_minimum_query_count() {
    echo "Test: At least $REQUIRED_QUERY_COUNT queries documented"
    # Count Q1-Q9 query rows in measurement table
    query_count=$(grep -cE "^\|\s*Q[0-9]" "$RESEARCH_FILE" 2>/dev/null || echo "0")
    if [[ $query_count -lt $REQUIRED_QUERY_COUNT ]]; then
        echo "FAIL: Found $query_count queries, need at least $REQUIRED_QUERY_COUNT"
        exit 1
    fi
    echo "PASS: Found $query_count queries"
}

# Test 3: Function lookup query exists (BR-003)
test_function_lookup_query() {
    echo "Test: Function lookup query documented"
    if ! grep -q "function" "$RESEARCH_FILE"; then
        echo "FAIL: No function lookup query found"
        exit 1
    fi
    echo "PASS: Function lookup query exists"
}

# Test 4: Class search query exists (BR-003)
test_class_search_query() {
    echo "Test: Class search query documented"
    if ! grep -q "class" "$RESEARCH_FILE"; then
        echo "FAIL: No class search query found"
        exit 1
    fi
    echo "PASS: Class search query exists"
}

# Test 5: Method search query exists (BR-003)
test_method_search_query() {
    echo "Test: Method search query documented"
    if ! grep -q "method" "$RESEARCH_FILE"; then
        echo "FAIL: No method search query found"
        exit 1
    fi
    echo "PASS: Method search query exists"
}

# Test 6: Symbol search query exists (BR-003)
test_symbol_search_query() {
    echo "Test: Symbol search query documented"
    if ! grep -q "symbol" "$RESEARCH_FILE"; then
        echo "FAIL: No symbol search query found"
        exit 1
    fi
    echo "PASS: Symbol search query exists"
}

# Test 7: Multi-file pattern query exists (BR-003)
test_multifile_pattern_query() {
    echo "Test: Multi-file pattern query documented"
    if ! grep -q -i "multi-file\|multifile\|import" "$RESEARCH_FILE"; then
        echo "FAIL: No multi-file pattern query found"
        exit 1
    fi
    echo "PASS: Multi-file pattern query exists"
}

# Run all tests
test_research_file_exists
test_minimum_query_count
test_function_lookup_query
test_class_search_query
test_method_search_query
test_symbol_search_query
test_multifile_pattern_query

echo ""
echo "=== All AC#1 tests passed ==="
