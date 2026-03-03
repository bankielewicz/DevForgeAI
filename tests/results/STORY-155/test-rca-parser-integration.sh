#!/bin/bash
# Integration Tests for STORY-155: RCA Document Parsing
#
# End-to-end integration tests validating complete RCA parsing workflow
# Tests the interaction between all acceptance criteria components

set -e

# Test utility functions
assert_equals() {
    local expected="$1"
    local actual="$2"
    local test_name="$3"

    if [ "$expected" = "$actual" ]; then
        echo "✓ PASS: $test_name"
        return 0
    else
        echo "✗ FAIL: $test_name"
        echo "  Expected: $expected"
        echo "  Actual: $actual"
        return 1
    fi
}

# Setup: Create comprehensive RCA for integration testing
setup_comprehensive_rca() {
    cat > /tmp/test-rca-integration.md <<'EOF'
---
id: RCA-022
title: Database Connection Pool Exhaustion Incident
date: 2025-12-20
severity: CRITICAL
status: OPEN
reporter: Alice Chen
---

# RCA-022: Database Connection Pool Exhaustion

## Executive Summary
On 2025-12-18, our production database experienced connection pool exhaustion under high load,
resulting in 45 minutes of service degradation affecting 2,300 concurrent users.

## Root Cause
The connection pool was configured with a maximum size of 10 connections, which proved
insufficient for the actual peak load of 100+ concurrent database operations during
peak traffic hours.

## Timeline
- 14:32 UTC: First connection timeouts detected
- 14:45 UTC: Service degradation noticed by monitoring
- 15:17 UTC: Incident declared CRITICAL
- 15:22 UTC: Temporary mitigation applied (request queuing)
- 16:15 UTC: Incident resolved with permanent pool size increase

## Recommendations

### REC-1: CRITICAL - Increase Connection Pool Size
The connection pool size must be increased immediately to handle peak load.
Current configuration of 10 connections is dangerously low.
Industry standard for 100 concurrent users is 50-75 connections.

**Effort Estimate:** 8 hours

**Success Criteria:**
- [ ] Connection pool maximum increased to 50
- [ ] Performance tested under 100+ concurrent connections
- [ ] No connection timeouts in 24-hour validation period

### REC-2: CRITICAL - Implement Comprehensive Load Testing
Establish automated load testing to catch capacity issues before production.
Current test coverage only tests up to 10 concurrent users.

**Effort Estimate:** 5 story points

**Success Criteria:**
- [ ] Load testing suite created (tests up to 200 concurrent)
- [ ] Automated load tests run on every deployment
- [ ] Performance metrics captured and trended

### REC-3: HIGH - Database Connection Monitoring
Add real-time monitoring of connection pool metrics to detect future exhaustion.
Without visibility, issues go undetected until they cause outages.

**Effort Estimate:** 12 hours

**Success Criteria:**
- [ ] Dashboard created showing active connections
- [ ] Alerts configured for 80% pool utilization
- [ ] Runbook updated with troubleshooting procedures
- [ ] Historical metrics stored for trend analysis

### REC-4: HIGH - Connection Pool Documentation
Document the connection pool configuration and tuning procedures.
This knowledge is currently only in one engineer's head.

**Effort Estimate:** 3 story points

**Success Criteria:**
- [ ] Configuration guide written
- [ ] Tuning procedures documented
- [ ] Team trained on configuration
- [ ] Process added to onboarding

### REC-5: MEDIUM - Code Review: Connection Handling
Review application code for connection pool anti-patterns.
May reveal additional inefficient database usage.

**Effort Estimate:** 6 hours

**Success Criteria:**
- [ ] Code review completed
- [ ] Anti-patterns documented
- [ ] Refactoring plan created (if needed)

### REC-6: MEDIUM - Database Query Optimization
Optimize slow queries that consume connections for extended periods.
Longer connection hold times = fewer available for new requests.

**Effort Estimate:** 4 story points

**Success Criteria:**
- [ ] Slow queries identified
- [ ] Query plan optimization completed
- [ ] 20% reduction in average connection hold time

### REC-7: LOW - Database Pooling Library Upgrade
Consider upgrading to latest HikariCP version for improved performance.
Current version is 18 months old, may have optimizations.

**Effort Estimate:** 2 hours

**Success Criteria:**
- [ ] New version evaluated for compatibility
- [ ] Performance improvement measured
- [ ] Migration plan documented

### REC-8: LOW - Create Architecture Decision Record
Document the decision to increase pool size and rationale.
Prevents future teams from reverting the change without understanding why.

**Effort Estimate:** 1 hour

**Success Criteria:**
- [ ] ADR-NNN created in documentation
- [ ] Approved by architecture team
- [ ] Linked in runbook
EOF
}

# Integration Test 1: Parse complete RCA with all components
test_parse_complete_rca_structure() {
    setup_comprehensive_rca

    # Should parse all components:
    # - Frontmatter (id, title, date, severity, status, reporter)
    # - Recommendations (8 total with varied priorities)
    # - Effort estimates (mix of hours and story points)
    # - Success criteria (4 have criteria)
    # Expected: Complete RCADocument object with all nested data

    echo "TEST: test_parse_complete_rca_structure"
    echo "  Scenario: Parse comprehensive RCA with all components"
    echo "  Expected: RCADocument with:"
    echo "    - id=RCA-022"
    echo "    - 8 recommendations extracted"
    echo "    - All effort estimates parsed"
    echo "    - All success criteria associated"
    echo "  Implementation needed: Complete parser integration"
}

# Integration Test 2: Filter and sort real RCA recommendations
test_filter_sort_complete_rca() {
    setup_comprehensive_rca

    # Parse RCA, then filter with threshold=4 hours
    # Recommendations >= 4 hours: REC-1 (8), REC-2 (20), REC-3 (12), REC-4 (12), REC-5 (6), REC-6 (16)
    # Exclude: REC-7 (2), REC-8 (1)
    # Then sort by priority:
    # CRITICAL: REC-1, REC-2
    # HIGH: REC-3, REC-4
    # MEDIUM: REC-5, REC-6
    # Expected: Exact order [REC-1, REC-2, REC-3, REC-4, REC-5, REC-6]

    echo "TEST: test_filter_sort_complete_rca"
    echo "  Scenario: Filter with threshold=4 hours and sort by priority"
    echo "  Expected: 6 recommendations in order [REC-1, REC-2, REC-3, REC-4, REC-5, REC-6]"
    echo "  Implementation needed: Complete workflow with BR-001 and BR-002"
}

# Integration Test 3: Story point conversion in context of full RCA
test_story_points_in_complete_rca() {
    setup_comprehensive_rca

    # REC-2: 5 story points = 20 hours
    # REC-4: 3 story points = 12 hours
    # REC-6: 4 story points = 16 hours
    # Filter threshold=10 hours: all three included
    # Expected: Points converted correctly to hours for comparison

    echo "TEST: test_story_points_in_complete_rca"
    echo "  Scenario: Story point conversion applied during filtering"
    echo "  Expected: 5 points = 20 hours, 3 points = 12 hours, 4 points = 16 hours"
    echo "  Implementation needed: BR-003 integrated with BR-001"
}

# Integration Test 4: Success criteria associated with correct recommendations
test_success_criteria_association_complete_rca() {
    setup_comprehensive_rca

    # Verify success criteria linked to correct parent:
    # REC-1 should have 3 criteria
    # REC-2 should have 3 criteria
    # REC-3 should have 4 criteria
    # REC-4 should have 4 criteria
    # REC-5 should have 3 criteria
    # REC-6 should have 3 criteria
    # REC-7 should have 3 criteria
    # REC-8 should have 3 criteria
    # Expected: 26 total criteria across 8 recommendations

    echo "TEST: test_success_criteria_association_complete_rca"
    echo "  Scenario: Verify each recommendation linked to its criteria"
    echo "  Expected: 26 total criteria distributed correctly across 8 recommendations"
    echo "  Implementation needed: Proper parent-child association"
}

# Integration Test 5: Handle RCA with mixed effort units
test_mixed_effort_units_complete_rca() {
    setup_comprehensive_rca

    # REC-1, REC-3, REC-5, REC-7, REC-8: hours
    # REC-2, REC-4, REC-6: story points
    # Filter should handle mixed units transparently
    # Expected: No errors, all converted to hours for threshold comparison

    echo "TEST: test_mixed_effort_units_complete_rca"
    echo "  Scenario: RCA with mixed hours and story point effort units"
    echo "  Expected: Parser handles transparently, converts all to hours"
    echo "  Implementation needed: Handle mixed units throughout"
}

# Integration Test 6: Validate all enum fields in complete RCA
test_enum_validation_complete_rca() {
    setup_comprehensive_rca

    # Validate:
    # - Frontmatter: severity=CRITICAL, status=OPEN (valid enums)
    # - All recommendations: priorities include CRITICAL, HIGH, MEDIUM, LOW
    # Expected: All enum values valid

    echo "TEST: test_enum_validation_complete_rca"
    echo "  Scenario: Validate all enum fields throughout RCA"
    echo "  Expected: All severity, status, and priority values valid"
    echo "  Implementation needed: Complete enum validation"
}

# Integration Test 7: End-to-end parsing workflow
test_end_to_end_parsing_workflow() {
    setup_comprehensive_rca

    # Complete workflow:
    # 1. Load file
    # 2. Parse frontmatter
    # 3. Extract recommendations
    # 4. Parse effort estimates
    # 5. Extract success criteria
    # 6. Apply filtering
    # 7. Sort by priority
    # 8. Return result
    # Expected: Complete RCADocument with filtered and sorted recommendations

    echo "TEST: test_end_to_end_parsing_workflow"
    echo "  Scenario: Complete parse -> extract -> filter -> sort workflow"
    echo "  Expected: Final result with all transformations applied"
    echo "  Implementation needed: Complete parser orchestration"
}

# Integration Test 8: Performance: Parse large RCA under 500ms
test_performance_large_rca() {
    # Note: This test creates a large RCA to validate performance requirement
    cat > /tmp/test-rca-large.md <<'EOF'
---
id: RCA-100
title: Large RCA with 100 Recommendations
date: 2025-12-20
severity: CRITICAL
status: OPEN
reporter: Test User
---

## Recommendations
EOF

    # Add 100 recommendations with varied effort and priorities
    local priorities=("CRITICAL" "HIGH" "MEDIUM" "LOW")
    for i in {1..100}; do
        local priority_idx=$((i % 4))
        local priority="${priorities[$priority_idx]}"
        local effort=$((RANDOM % 40 + 1))

        cat >> /tmp/test-rca-large.md <<EOF

### REC-$i: $priority - Recommendation $i
Description of recommendation $i.

**Effort Estimate:** $effort hours

**Success Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2
EOF
    done

    # Should parse in under 500ms (performance requirement)
    # Expected: Parser completes quickly even with 100 recommendations

    echo "TEST: test_performance_large_rca"
    echo "  Scenario: Parse RCA with 100 recommendations"
    echo "  Expected: Complete in <500ms (per NFR)"
    echo "  Implementation needed: Performance-optimized parser"
}

# Integration Test 9: Verify data model relationships
test_data_model_relationships() {
    setup_comprehensive_rca

    # Verify object relationships:
    # RCADocument
    #   ├── recommendations: [Recommendation]
    #   └── each Recommendation
    #       └── success_criteria: [string]
    # Expected: Proper hierarchy maintained

    echo "TEST: test_data_model_relationships"
    echo "  Scenario: Verify data model object relationships"
    echo "  Expected: RCADocument contains Recommendation array"
    echo "            each Recommendation contains success_criteria array"
    echo "  Implementation needed: Proper data structure"
}

# Integration Test 10: Error handling in complete workflow
test_error_handling_complete_workflow() {
    # Create RCA with various errors
    cat > /tmp/test-rca-errors.md <<'EOF'
---
id: RCA-999
title: Error Test RCA
date: invalid-date
severity: INVALID
status: OPEN
reporter: Test
---

## Recommendations

### REC-1: INVALID - Bad Priority
Invalid priority value.

**Effort Estimate:** ABC hours

**Success Criteria:**
- Not a checkbox format

### REC-INVALID: HIGH - Bad ID Format
Wrong ID format (missing hyphen).

### REC-3 MISSING: Colon After ID
Missing colon separator.
EOF

    # Should handle errors gracefully:
    # - Invalid date format: log warning
    # - Invalid severity: log warning
    # - Non-numeric effort: skip field
    # - Invalid checklist format: skip item
    # - Malformed headers: log warning
    # Expected: Partial parsing with warnings

    echo "TEST: test_error_handling_complete_workflow"
    echo "  Scenario: RCA with multiple error conditions"
    echo "  Expected: Graceful degradation with warnings"
    echo "  Implementation needed: Comprehensive error handling"
}

# Integration Test 11: Large recommendation description handling
test_large_recommendation_description() {
    setup_comprehensive_rca

    # REC-1 and REC-3 have multi-paragraph descriptions
    # Should preserve all text
    # Expected: Complete descriptions extracted

    echo "TEST: test_large_recommendation_description"
    echo "  Scenario: Recommendations with large multi-paragraph descriptions"
    echo "  Expected: Complete description text preserved"
    echo "  Implementation needed: Multi-line description capture"
}

# Integration Test 12: Real-world usage scenario
test_real_world_workflow() {
    setup_comprehensive_rca

    # Real-world workflow:
    # 1. Load RCA-022 from devforgeai/RCA/
    # 2. Parse complete document
    # 3. Filter with threshold_hours=5
    # 4. Sort by priority
    # 5. Present top 3 CRITICAL recommendations to user
    # Expected: User sees REC-1 and REC-2 (both CRITICAL, >= 5 hours)

    echo "TEST: test_real_world_workflow"
    echo "  Scenario: Practical workflow - identify top critical recommendations"
    echo "  Expected: REC-1 and REC-2 surfaced as highest priority"
    echo "  Implementation needed: Complete parser for production use"
}

# Integration Test 13: Multiple RCA parsing in sequence
test_multiple_rca_parsing() {
    setup_comprehensive_rca

    # Should be able to parse multiple RCA files sequentially
    # Expected: No state leakage between files

    echo "TEST: test_multiple_rca_parsing"
    echo "  Scenario: Parse multiple RCA files in sequence"
    echo "  Expected: Each RCA parsed independently without interference"
    echo "  Implementation needed: Stateless parser"
}

# Integration Test 14: Filtering edge cases integration
test_filtering_edge_cases() {
    setup_comprehensive_rca

    # Test various threshold values:
    # - threshold=0: include all
    # - threshold=100: include none (or only REC-2 if counting as 20)
    # - threshold=<negative>: handle error
    # - threshold=null: default behavior
    # Expected: Consistent behavior across all cases

    echo "TEST: test_filtering_edge_cases"
    echo "  Scenario: Filtering with edge case thresholds"
    echo "  Expected: Consistent behavior for all threshold values"
    echo "  Implementation needed: Robust threshold handling"
}

# Integration Test 15: Update story changelog
test_changelog_update() {
    # Verify that parser implementation will trigger changelog update
    # in story YAML frontmatter
    # Expected: Phase 02 Red adds changelog entry

    echo "TEST: test_changelog_update"
    echo "  Scenario: Story file changelog updated after test generation"
    echo "  Expected: Entry added with timestamp, author, phase, status"
    echo "  Implementation needed: STORY-152 change log integration"
}

# Main test execution
main() {
    echo "=========================================="
    echo "STORY-155 Integration Tests"
    echo "=========================================="
    echo ""
    echo "These tests validate end-to-end parsing and interaction"
    echo "between all acceptance criteria components."
    echo ""

    test_parse_complete_rca_structure
    test_filter_sort_complete_rca
    test_story_points_in_complete_rca
    test_success_criteria_association_complete_rca
    test_mixed_effort_units_complete_rca
    test_enum_validation_complete_rca
    test_end_to_end_parsing_workflow
    test_performance_large_rca
    test_data_model_relationships
    test_error_handling_complete_workflow
    test_large_recommendation_description
    test_real_world_workflow
    test_multiple_rca_parsing
    test_filtering_edge_cases
    test_changelog_update

    echo ""
    echo "=========================================="
    echo "All integration tests generated (FAILING)"
    echo "Implementation required for all tests"
    echo "=========================================="
}

main "$@"
