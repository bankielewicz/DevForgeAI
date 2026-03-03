"""
Test: NFR Quality Validation (cross-cutting)
Story: STORY-435
Generated: 2026-02-17 (TDD Red Phase)

Validates BR-004 (success criteria must be quantified) and
additional cross-cutting quality checks.
"""
import re
import pytest


QUANTIFIER_PATTERN = r"[\d]+|[<>]=?|%|ms|seconds|minutes"


class TestSuccessCriteriaQuantified:
    """BR-004: Success criteria must contain numbers or comparators."""

    def test_should_accept_quantified_target(self, sample_valid_success_criteria):
        # Arrange
        target = sample_valid_success_criteria[0]["target"]

        # Act
        has_quantifier = bool(re.search(QUANTIFIER_PATTERN, target))

        # Assert
        assert has_quantifier, f"Target '{target}' should contain quantifier"

    def test_should_reject_vague_target(self):
        # Arrange
        vague_target = "good performance"

        # Act
        has_quantifier = bool(re.search(QUANTIFIER_PATTERN, vague_target))

        # Assert
        assert not has_quantifier, f"Vague target '{vague_target}' should be rejected"

    @pytest.mark.parametrize("target", [
        "> 85%",
        "< 200ms",
        ">= 99.9%",
        "3 seconds",
        "100 requests per minute",
    ])
    def test_should_accept_various_quantified_formats(self, target):
        has_quantifier = bool(re.search(QUANTIFIER_PATTERN, target))
        assert has_quantifier, f"Target '{target}' should be accepted as quantified"

    @pytest.mark.parametrize("target", [
        "fast",
        "reliable",
        "good enough",
        "acceptable",
    ])
    def test_should_reject_various_vague_targets(self, target):
        has_quantifier = bool(re.search(QUANTIFIER_PATTERN, target))
        assert not has_quantifier, f"Target '{target}' should be rejected as vague"


class TestSuccessCriteriaRequiredFields:
    """Success criteria must have id, metric, target, measurement."""

    def test_should_have_id(self, sample_valid_success_criteria):
        sc = sample_valid_success_criteria[0]
        assert "id" in sc

    def test_should_have_metric(self, sample_valid_success_criteria):
        sc = sample_valid_success_criteria[0]
        assert "metric" in sc

    def test_should_have_target(self, sample_valid_success_criteria):
        sc = sample_valid_success_criteria[0]
        assert "target" in sc

    def test_should_have_measurement(self, sample_valid_success_criteria):
        sc = sample_valid_success_criteria[0]
        assert "measurement" in sc
