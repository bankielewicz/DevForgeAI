"""
STORY-015 Comprehensive Test Suite

This package contains:
- Unit tests for template/story DoD insertion
- Integration tests for complete workflows
- E2E tests for real-world usage

Test organization:
- tests/unit/ - Unit tests (14 tests, 78%)
- tests/integration/ - Integration tests (3 tests, 17%)
- tests/e2e/ - End-to-end tests (1 test, 5%)
- tests/conftest.py - Shared fixtures and configuration
- tests/pytest.ini - Pytest configuration with coverage settings
- tests/README.md - Comprehensive test documentation

Target Coverage: ≥95% for template/story edit operations
Performance Target: <2 minutes for full suite execution

See tests/README.md for detailed documentation.
"""

__version__ = "1.0"
__author__ = "DevForgeAI Framework"
__maintainer__ = "DevForgeAI Testing Team"

# Make fixtures available to tests
from pathlib import Path

__test_root__ = Path(__file__).parent
