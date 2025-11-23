"""
Shared pytest fixtures and configuration for STORY-059 test suite.

This module provides common fixtures used across all test modules for:
- Path initialization
- Test data setup
- Cleanup handlers
- Logging configuration
"""

import pytest
from pathlib import Path


@pytest.fixture(scope="session")
def test_suite_base_path():
    """Base path for the entire test suite (session scope)"""
    return Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance")


@pytest.fixture(scope="function")
def temp_test_fixture_path(tmp_path):
    """Temporary directory for test fixtures (function scope)"""
    return tmp_path / "fixtures"


@pytest.fixture(scope="function")
def temp_test_script_path(tmp_path):
    """Temporary directory for test scripts (function scope)"""
    return tmp_path / "scripts"


@pytest.fixture(scope="function")
def temp_test_reports_path(tmp_path):
    """Temporary directory for test reports (function scope)"""
    return tmp_path / "reports"


@pytest.fixture(autouse=True)
def cleanup_test_artifacts(tmp_path):
    """
    Automatic cleanup fixture that removes temporary test artifacts
    after each test completes (function scope).
    """
    yield  # Run the test

    # Cleanup happens automatically when tmp_path is destroyed
    # (pytest automatically removes tmp_path after test)


@pytest.fixture
def sample_baseline_content():
    """Sample content for baseline fixture"""
    return """Create a user management feature. The system should allow administrators to manage users
effectively. Users should be created, updated, and deleted easily. The feature should perform
well and be secure. All user data should be validated before storage. The system should handle
errors gracefully and maintain data integrity."""


@pytest.fixture
def sample_enhanced_content():
    """Sample content for enhanced fixture"""
    return """Create a user management REST API feature for administrative operations. The system must
support the following operations: create new users (POST /api/users), update user profiles (PUT /api/users/{id}),
and delete users (DELETE /api/users/{id}). Each operation requires authentication and authorization checks.

Acceptance Criteria:
Given an administrator with valid credentials
When they submit a POST request to /api/users with valid user data (email, first_name, last_name, role)
Then the system creates the user and returns HTTP 201 with the new user object

Acceptance Criteria:
Given a user record exists in the database
When an administrator submits a PUT request with updated data
Then the system validates all required fields, updates only non-null fields, and returns HTTP 200 with updated user

Non-Functional Requirements:
- Performance: All operations must complete within 200ms (99th percentile)
- Security: All endpoints require bearer token authentication; passwords stored with bcrypt (salt rounds ≥12)
- Reliability: Database operations must use transactions; failed updates must rollback completely
- Scalability: API must handle 1000 concurrent user management requests without performance degradation"""


@pytest.fixture
def sample_expected_improvements():
    """Sample expected improvements JSON structure"""
    return {
        "fixture_id": "01",
        "category": "crud-operations",
        "baseline_issues": [
            "vague scope (system ambiguity)",
            "missing success criteria (no metrics)",
            "ambiguous acceptance criteria (no Given/When/Then)",
            "omitted non-functional requirements"
        ],
        "expected_improvements": {
            "token_savings": 25.0,
            "ac_completeness": 85.0,
            "nfr_coverage": 75.0,
            "specificity_score": 80.0
        },
        "rationale": "The enhanced version clarifies scope by specifying REST API endpoints, adds testable acceptance criteria in Given/When/Then format (two AC criteria for POST and PUT operations), documents 3 NFR categories with measurable targets (200ms performance, bcrypt security, transaction reliability), and replaces vague terms ('perform well', 'handle errors') with specific metrics and implementations."
    }


@pytest.fixture
def mock_fixture_directory_structure(tmp_path):
    """Create mock directory structure for testing"""
    base_path = tmp_path / "test_suite"
    fixtures_path = base_path / "fixtures"

    (fixtures_path / "baseline").mkdir(parents=True, exist_ok=True)
    (fixtures_path / "enhanced").mkdir(parents=True, exist_ok=True)
    (fixtures_path / "expected").mkdir(parents=True, exist_ok=True)
    (base_path / "scripts").mkdir(parents=True, exist_ok=True)
    (base_path / "reports").mkdir(parents=True, exist_ok=True)

    return base_path


# Pytest configuration hooks

def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "unit: Mark test as a unit test (AC#1-4)"
    )
    config.addinivalue_line(
        "markers", "integration: Mark test as integration test (AC#5-8, end-to-end, error handling, partial handling, concurrent)"
    )
    config.addinivalue_line(
        "markers", "regression: Mark test as regression test (fixture quality, script consistency)"
    )
    config.addinivalue_line(
        "markers", "slow: Mark test as slow (concurrent, end-to-end)"
    )


def pytest_collection_modifyitems(config, items):
    """Automatically mark tests based on module name"""
    for item in items:
        # Mark unit tests
        if "test_directory_structure" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "test_baseline_fixtures" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "test_enhanced_fixtures" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "test_expected_files" in str(item.fspath):
            item.add_marker(pytest.mark.unit)

        # Mark integration tests
        elif "test_end_to_end" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
            item.add_marker(pytest.mark.slow)
        elif "test_error_handling" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "test_partial_handling" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "test_concurrent" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
            item.add_marker(pytest.mark.slow)

        # Mark regression tests
        elif "test_fixture_regression" in str(item.fspath):
            item.add_marker(pytest.mark.regression)
        elif "test_script_consistency" in str(item.fspath):
            item.add_marker(pytest.mark.regression)
