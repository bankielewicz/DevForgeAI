"""
Test: AC#2 - Stage 2 LLM Classification
Story: STORY-406
Generated: 2026-02-16

Validates that Stage 2 classification logic is specified in the scanner:
- Returns 'navigation_chain' or 'fluent_api' classification
- Includes confidence score
- Confidence >= 0.7 means REPORT, < 0.7 means SUPPRESS
"""
import os
import pytest


class TestStage2ClassificationSpec:
    """Stage 2 LLM classification must be documented in scanner spec."""

    def test_ac2_classification_types_in_spec(self, src_scanner_spec_path):
        """Arrange: Read spec. Act: Search for classification types. Assert: Both present."""
        spec_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            src_scanner_spec_path,
        )
        assert os.path.exists(spec_path), (
            f"Scanner spec not found at {spec_path} - implementation needed"
        )
        with open(spec_path, "r") as f:
            content = f.read()
        assert "navigation_chain" in content, (
            "Spec must define 'navigation_chain' classification type"
        )
        assert "fluent_api" in content, (
            "Spec must define 'fluent_api' classification type"
        )

    def test_ac2_confidence_threshold_in_spec(self, src_scanner_spec_path):
        """Arrange: Read spec. Act: Search for confidence threshold. Assert: 0.7 defined."""
        spec_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            src_scanner_spec_path,
        )
        assert os.path.exists(spec_path), (
            f"Scanner spec not found at {spec_path} - implementation needed"
        )
        with open(spec_path, "r") as f:
            content = f.read()
        assert "0.7" in content, (
            "Spec must define confidence threshold of 0.7"
        )

    def test_ac2_two_stage_pipeline_in_spec(self, src_scanner_spec_path):
        """Arrange: Read spec. Act: Search for two-stage pipeline. Assert: Documented."""
        spec_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            src_scanner_spec_path,
        )
        assert os.path.exists(spec_path), (
            f"Scanner spec not found at {spec_path} - implementation needed"
        )
        with open(spec_path, "r") as f:
            content = f.read()
        has_stage1 = "stage 1" in content.lower() or "stage1" in content.lower()
        has_stage2 = "stage 2" in content.lower() or "stage2" in content.lower()
        assert has_stage1 and has_stage2, (
            "Spec must document both Stage 1 and Stage 2 of the pipeline"
        )


class TestStage2ClassificationLogic:
    """Classification logic: confidence >= 0.7 = REPORT, < 0.7 = SUPPRESS."""

    def test_ac2_high_confidence_means_report(self, confidence_threshold):
        """Arrange: confidence = 0.85. Act: Compare to threshold. Assert: REPORT."""
        confidence = 0.85
        should_report = confidence >= confidence_threshold
        assert should_report is True, (
            f"Confidence {confidence} >= {confidence_threshold} should mean REPORT"
        )

    def test_ac2_low_confidence_means_suppress(self, confidence_threshold):
        """Arrange: confidence = 0.3. Act: Compare to threshold. Assert: SUPPRESS."""
        confidence = 0.3
        should_report = confidence >= confidence_threshold
        assert should_report is False, (
            f"Confidence {confidence} < {confidence_threshold} should mean SUPPRESS"
        )

    def test_ac2_boundary_confidence_means_report(self, confidence_threshold):
        """Arrange: confidence = 0.7 (exact threshold). Act: Compare. Assert: REPORT."""
        confidence = 0.7
        should_report = confidence >= confidence_threshold
        assert should_report is True, (
            f"Confidence {confidence} == {confidence_threshold} should mean REPORT (>= boundary)"
        )

    def test_ac2_just_below_threshold_means_suppress(self, confidence_threshold):
        """Arrange: confidence = 0.69. Act: Compare. Assert: SUPPRESS."""
        confidence = 0.69
        should_report = confidence >= confidence_threshold
        assert should_report is False, (
            f"Confidence {confidence} < {confidence_threshold} should mean SUPPRESS"
        )
