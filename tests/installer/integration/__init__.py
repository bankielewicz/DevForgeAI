"""
Integration test suite for STORY-045 Version-Aware Installer.

This package contains end-to-end integration tests that validate
the complete installation workflow with REAL file operations.

Test Modules:
- conftest.py: Shared fixtures for integration tests
- test_fresh_install_workflow.py: Fresh installation tests (8 tests)
- test_upgrade_workflow.py: Upgrade from v1.0.0 to v1.0.1 (7 tests)
- test_rollback_workflow.py: Rollback after upgrade (6 tests)
- test_validate_workflow.py: Installation validation (5 tests)
- test_uninstall_workflow.py: Framework uninstall with data preservation (5 tests)
- test_error_recovery.py: Error handling and automatic rollback (6 tests)
- test_performance_benchmarks.py: Performance NFR validation (7 tests)

Total Test Coverage: 44 integration tests
All tests use real file I/O (no mocking of filesystem)

Running Integration Tests:
    pytest installer/tests/integration/ -v
    pytest installer/tests/integration/test_fresh_install_workflow.py -v
    pytest installer/tests/integration/ -k "performance" -v

Test Categories:
- Workflow Tests (8-7-6-5-5 = 31 tests): Main scenarios
- Error Recovery (6 tests): Failure scenarios and rollback
- Performance (7 tests): NFR validation and benchmarks
- Fixtures (conftest.py): Shared setup and utilities
"""
