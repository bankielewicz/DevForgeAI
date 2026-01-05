"""
STORY-175 AC#2: Classify Violations

Tests that violations are classified as REGRESSION or PRE_EXISTING based on changed files.
All tests follow TDD Red phase - they should FAIL until implementation exists.

Given: violations are detected
When: classifying each violation
Then: violations in changed files are `REGRESSION`, others are `PRE_EXISTING`

Coverage Target: 95%+
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from dataclasses import dataclass
from typing import List


class TestViolationClassification:
    """Test AC#2: Violations in changed files are REGRESSION, others are PRE_EXISTING."""

    def test_classify_violation_returns_regression_for_changed_file(self):
        """
        Test: classify_violation() returns REGRESSION for violations in changed files.

        Given: A violation in a file that was changed
        When: classify_violation() is called
        Then: Returns "REGRESSION"
        """
        # Arrange
        from devforgeai.qa.regression_classifier import classify_violation

        violation = {
            "file": "src/module/changed_file.py",
            "line": 10,
            "message": "Cyclomatic complexity too high"
        }
        changed_files = ["src/module/changed_file.py", "src/module/other_file.py"]

        # Act
        result = classify_violation(violation, changed_files)

        # Assert
        assert result == "REGRESSION"

    def test_classify_violation_returns_pre_existing_for_unchanged_file(self):
        """
        Test: classify_violation() returns PRE_EXISTING for violations in unchanged files.

        Given: A violation in a file that was not changed
        When: classify_violation() is called
        Then: Returns "PRE_EXISTING"
        """
        # Arrange
        from devforgeai.qa.regression_classifier import classify_violation

        violation = {
            "file": "src/module/old_file.py",
            "line": 25,
            "message": "Missing docstring"
        }
        changed_files = ["src/module/changed_file.py"]

        # Act
        result = classify_violation(violation, changed_files)

        # Assert
        assert result == "PRE_EXISTING"

    def test_classify_violation_is_case_sensitive(self):
        """
        Test: classify_violation() performs case-sensitive file matching.

        Given: Violation file path has different case than changed files
        When: classify_violation() is called
        Then: Case mismatch results in PRE_EXISTING classification
        """
        # Arrange
        from devforgeai.qa.regression_classifier import classify_violation

        violation = {"file": "src/Module/File.py", "line": 1, "message": "Issue"}
        changed_files = ["src/module/file.py"]  # Different case

        # Act
        result = classify_violation(violation, changed_files)

        # Assert - exact match required
        assert result == "PRE_EXISTING"

    def test_classify_violation_normalizes_path_separators(self):
        """
        Test: classify_violation() normalizes path separators (/ vs \).

        Given: Violation path uses backslashes, changed files use forward slashes
        When: classify_violation() is called
        Then: Paths are normalized before comparison
        """
        # Arrange
        from devforgeai.qa.regression_classifier import classify_violation

        violation = {"file": "src\\module\\file.py", "line": 1, "message": "Issue"}
        changed_files = ["src/module/file.py"]

        # Act
        result = classify_violation(violation, changed_files)

        # Assert - should match after normalization
        assert result == "REGRESSION"


class TestClassifyViolationsInBatch:
    """Test batch classification of multiple violations."""

    def test_classify_violations_processes_multiple_violations(self):
        """
        Test: classify_violations() processes a list of violations.

        Given: Multiple violations
        When: classify_violations() is called
        Then: Each violation is classified correctly
        """
        # Arrange
        from devforgeai.qa.regression_classifier import classify_violations

        violations = [
            {"file": "src/changed.py", "line": 1, "message": "Issue 1"},
            {"file": "src/unchanged.py", "line": 2, "message": "Issue 2"},
            {"file": "src/changed.py", "line": 3, "message": "Issue 3"},
        ]
        changed_files = ["src/changed.py"]

        # Act
        result = classify_violations(violations, changed_files)

        # Assert
        assert len(result) == 3
        assert result[0]["classification"] == "REGRESSION"
        assert result[1]["classification"] == "PRE_EXISTING"
        assert result[2]["classification"] == "REGRESSION"

    def test_classify_violations_adds_classification_field(self):
        """
        Test: classify_violations() adds 'classification' field to each violation.

        Given: Violations without classification field
        When: classify_violations() is called
        Then: Each violation has 'classification' field added
        """
        # Arrange
        from devforgeai.qa.regression_classifier import classify_violations

        violations = [
            {"file": "src/file.py", "line": 1, "message": "Issue"},
        ]
        changed_files = ["src/file.py"]

        # Act
        result = classify_violations(violations, changed_files)

        # Assert
        assert "classification" in result[0]
        assert result[0]["classification"] in ["REGRESSION", "PRE_EXISTING"]

    def test_classify_violations_preserves_original_violation_data(self):
        """
        Test: classify_violations() preserves all original violation fields.

        Given: Violations with multiple fields
        When: classify_violations() is called
        Then: Original fields are preserved, classification is added
        """
        # Arrange
        from devforgeai.qa.regression_classifier import classify_violations

        violations = [
            {
                "file": "src/file.py",
                "line": 42,
                "column": 10,
                "message": "Too complex",
                "severity": "HIGH",
                "rule": "complexity-check"
            },
        ]
        changed_files = ["src/file.py"]

        # Act
        result = classify_violations(violations, changed_files)

        # Assert - all original fields preserved
        assert result[0]["file"] == "src/file.py"
        assert result[0]["line"] == 42
        assert result[0]["column"] == 10
        assert result[0]["message"] == "Too complex"
        assert result[0]["severity"] == "HIGH"
        assert result[0]["rule"] == "complexity-check"
        assert result[0]["classification"] == "REGRESSION"

    def test_classify_violations_returns_empty_list_for_no_violations(self):
        """
        Test: classify_violations() returns empty list when no violations.

        Given: Empty violations list
        When: classify_violations() is called
        Then: Returns empty list
        """
        # Arrange
        from devforgeai.qa.regression_classifier import classify_violations

        violations = []
        changed_files = ["src/file.py"]

        # Act
        result = classify_violations(violations, changed_files)

        # Assert
        assert isinstance(result, list)
        assert len(result) == 0


class TestViolationModel:
    """Test violation data model with classification."""

    def test_classified_violation_has_required_fields(self):
        """
        Test: Classified violation has all required fields.

        Given: A violation is classified
        When: Result is inspected
        Then: Contains file, classification fields at minimum
        """
        # Arrange
        from devforgeai.qa.regression_classifier import classify_violations

        violations = [{"file": "src/file.py", "line": 1, "message": "Issue"}]
        changed_files = ["src/file.py"]

        # Act
        result = classify_violations(violations, changed_files)

        # Assert
        assert "file" in result[0]
        assert "classification" in result[0]

    def test_classification_values_are_uppercase_constants(self):
        """
        Test: Classification values are uppercase string constants.

        Given: Classifications are returned
        When: Values are inspected
        Then: Values are "REGRESSION" or "PRE_EXISTING" (uppercase)
        """
        # Arrange
        from devforgeai.qa.regression_classifier import classify_violations

        violations = [
            {"file": "src/changed.py", "line": 1, "message": "Issue 1"},
            {"file": "src/unchanged.py", "line": 2, "message": "Issue 2"},
        ]
        changed_files = ["src/changed.py"]

        # Act
        result = classify_violations(violations, changed_files)

        # Assert
        valid_classifications = {"REGRESSION", "PRE_EXISTING"}
        for v in result:
            assert v["classification"] in valid_classifications
            assert v["classification"].isupper()
