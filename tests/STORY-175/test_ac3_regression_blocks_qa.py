"""
STORY-175 AC#3: REGRESSION Violations Block QA

Tests that REGRESSION violations block QA (blocking=true) and PRE_EXISTING are warnings only.
All tests follow TDD Red phase - they should FAIL until implementation exists.

Given: violations classified
Then: `REGRESSION` violations block QA (blocking=true)
And: `PRE_EXISTING` violations are warnings only (blocking=false)

Coverage Target: 95%+
"""

import pytest
from unittest.mock import Mock, patch, MagicMock


class TestRegressionViolationsBlock:
    """Test AC#3: REGRESSION violations set blocking=true."""

    def test_regression_violation_has_blocking_true(self):
        """
        Test: REGRESSION violation has blocking=true.

        Given: A violation classified as REGRESSION
        When: blocking status is set
        Then: blocking=true
        """
        # Arrange
        from devforgeai.qa.regression_classifier import set_blocking_status

        violation = {
            "file": "src/file.py",
            "line": 1,
            "message": "Issue",
            "classification": "REGRESSION"
        }

        # Act
        result = set_blocking_status(violation)

        # Assert
        assert result["blocking"] is True

    def test_pre_existing_violation_has_blocking_false(self):
        """
        Test: PRE_EXISTING violation has blocking=false.

        Given: A violation classified as PRE_EXISTING
        When: blocking status is set
        Then: blocking=false
        """
        # Arrange
        from devforgeai.qa.regression_classifier import set_blocking_status

        violation = {
            "file": "src/old_file.py",
            "line": 1,
            "message": "Legacy issue",
            "classification": "PRE_EXISTING"
        }

        # Act
        result = set_blocking_status(violation)

        # Assert
        assert result["blocking"] is False


class TestBlockingStatusBatch:
    """Test batch blocking status assignment."""

    def test_set_blocking_status_for_all_violations(self):
        """
        Test: set_all_blocking_status() sets blocking for all violations.

        Given: List of classified violations
        When: set_all_blocking_status() is called
        Then: Each violation has correct blocking status
        """
        # Arrange
        from devforgeai.qa.regression_classifier import set_all_blocking_status

        violations = [
            {"file": "src/changed.py", "classification": "REGRESSION"},
            {"file": "src/old.py", "classification": "PRE_EXISTING"},
            {"file": "src/changed.py", "classification": "REGRESSION"},
        ]

        # Act
        result = set_all_blocking_status(violations)

        # Assert
        assert result[0]["blocking"] is True   # REGRESSION
        assert result[1]["blocking"] is False  # PRE_EXISTING
        assert result[2]["blocking"] is True   # REGRESSION

    def test_blocking_status_preserves_other_fields(self):
        """
        Test: set_all_blocking_status() preserves all other violation fields.

        Given: Violations with multiple fields
        When: set_all_blocking_status() is called
        Then: All original fields are preserved
        """
        # Arrange
        from devforgeai.qa.regression_classifier import set_all_blocking_status

        violations = [
            {
                "file": "src/file.py",
                "line": 42,
                "column": 10,
                "message": "Complex method",
                "severity": "HIGH",
                "classification": "REGRESSION"
            },
        ]

        # Act
        result = set_all_blocking_status(violations)

        # Assert
        assert result[0]["file"] == "src/file.py"
        assert result[0]["line"] == 42
        assert result[0]["column"] == 10
        assert result[0]["message"] == "Complex method"
        assert result[0]["severity"] == "HIGH"
        assert result[0]["classification"] == "REGRESSION"
        assert result[0]["blocking"] is True


class TestQABlockingDecision:
    """Test QA pass/fail decision based on blocking violations."""

    def test_qa_fails_when_regression_violations_exist(self):
        """
        Test: QA validation fails when REGRESSION violations exist.

        Given: At least one violation with blocking=true
        When: should_block_qa() is called
        Then: Returns True (QA should be blocked)
        """
        # Arrange
        from devforgeai.qa.regression_classifier import should_block_qa

        violations = [
            {"file": "src/file.py", "classification": "REGRESSION", "blocking": True},
            {"file": "src/old.py", "classification": "PRE_EXISTING", "blocking": False},
        ]

        # Act
        result = should_block_qa(violations)

        # Assert
        assert result is True

    def test_qa_passes_when_only_pre_existing_violations(self):
        """
        Test: QA validation passes when only PRE_EXISTING violations exist.

        Given: All violations have blocking=false
        When: should_block_qa() is called
        Then: Returns False (QA should not be blocked)
        """
        # Arrange
        from devforgeai.qa.regression_classifier import should_block_qa

        violations = [
            {"file": "src/old1.py", "classification": "PRE_EXISTING", "blocking": False},
            {"file": "src/old2.py", "classification": "PRE_EXISTING", "blocking": False},
        ]

        # Act
        result = should_block_qa(violations)

        # Assert
        assert result is False

    def test_qa_passes_when_no_violations(self):
        """
        Test: QA validation passes when no violations exist.

        Given: Empty violations list
        When: should_block_qa() is called
        Then: Returns False (QA should not be blocked)
        """
        # Arrange
        from devforgeai.qa.regression_classifier import should_block_qa

        violations = []

        # Act
        result = should_block_qa(violations)

        # Assert
        assert result is False

    def test_qa_fails_with_single_regression_among_many_pre_existing(self):
        """
        Test: QA fails even with just one REGRESSION among many PRE_EXISTING.

        Given: Many PRE_EXISTING and one REGRESSION violation
        When: should_block_qa() is called
        Then: Returns True (one regression is enough to block)
        """
        # Arrange
        from devforgeai.qa.regression_classifier import should_block_qa

        violations = [
            {"file": "src/old1.py", "classification": "PRE_EXISTING", "blocking": False},
            {"file": "src/old2.py", "classification": "PRE_EXISTING", "blocking": False},
            {"file": "src/old3.py", "classification": "PRE_EXISTING", "blocking": False},
            {"file": "src/changed.py", "classification": "REGRESSION", "blocking": True},
            {"file": "src/old4.py", "classification": "PRE_EXISTING", "blocking": False},
        ]

        # Act
        result = should_block_qa(violations)

        # Assert
        assert result is True


class TestBlockingCounts:
    """Test counting of blocking vs non-blocking violations."""

    def test_count_blocking_violations(self):
        """
        Test: count_blocking() returns count of violations with blocking=true.

        Given: Mixed list of blocking and non-blocking violations
        When: count_blocking() is called
        Then: Returns correct count of blocking violations
        """
        # Arrange
        from devforgeai.qa.regression_classifier import count_blocking

        violations = [
            {"blocking": True},
            {"blocking": False},
            {"blocking": True},
            {"blocking": False},
            {"blocking": True},
        ]

        # Act
        result = count_blocking(violations)

        # Assert
        assert result == 3

    def test_count_non_blocking_violations(self):
        """
        Test: count_non_blocking() returns count of violations with blocking=false.

        Given: Mixed list of blocking and non-blocking violations
        When: count_non_blocking() is called
        Then: Returns correct count of non-blocking violations
        """
        # Arrange
        from devforgeai.qa.regression_classifier import count_non_blocking

        violations = [
            {"blocking": True},
            {"blocking": False},
            {"blocking": True},
            {"blocking": False},
            {"blocking": True},
        ]

        # Act
        result = count_non_blocking(violations)

        # Assert
        assert result == 2
