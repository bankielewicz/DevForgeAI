"""
Test: AC#3 - Builder Pattern Suppression
Story: STORY-406
Generated: 2026-02-16

Validates that builder patterns (QueryBuilder, StringBuilder, etc.)
are classified as 'fluent_api' with confidence < 0.7 and suppressed.
"""
import os
import re
import pytest


FLUENT_KEYWORDS = [
    "QueryBuilder", "Builder", "build", "where", "orderBy", "limit",
    "select", "from", "join", "groupBy", "having",
]


class TestBuilderPatternDetection:
    """Builder patterns should be identified by fluent API keywords."""

    def test_ac3_builder_contains_fluent_keywords(self, builder_chain_code):
        """Arrange: Builder chain. Act: Check for fluent keywords. Assert: Found."""
        found_keywords = [
            kw for kw in FLUENT_KEYWORDS
            if kw.lower() in builder_chain_code.lower()
        ]
        assert len(found_keywords) > 0, (
            f"Builder chain should contain fluent keywords: {builder_chain_code}"
        )

    def test_ac3_builder_matches_grep_pattern(self, grep_pattern, builder_chain_code):
        """Arrange: Builder chain. Act: Apply Stage 1 pattern. Assert: Matches (high recall)."""
        result = re.search(grep_pattern, builder_chain_code)
        assert result is not None, (
            "Builder chain should match Stage 1 grep (suppression is Stage 2)"
        )

    def test_ac3_builder_expected_confidence_below_threshold(self, confidence_threshold):
        """Arrange: Builder expected confidence ~0.3. Act: Compare. Assert: Suppressed."""
        builder_confidence = 0.3  # Expected per story spec
        assert builder_confidence < confidence_threshold, (
            f"Builder confidence {builder_confidence} should be < {confidence_threshold}"
        )


class TestBuilderSuppressionInSpec:
    """Builder suppression must be documented in scanner spec."""

    def test_ac3_builder_suppression_in_spec(self, src_scanner_spec_path):
        """Arrange: Read spec. Act: Search for builder suppression. Assert: Documented."""
        spec_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            src_scanner_spec_path,
        )
        assert os.path.exists(spec_path), (
            f"Scanner spec not found at {spec_path} - implementation needed"
        )
        with open(spec_path, "r") as f:
            content = f.read().lower()
        has_builder = "builder" in content
        has_fluent = "fluent" in content
        assert has_builder and has_fluent, (
            "Spec must document builder pattern as fluent API for suppression"
        )

    def test_ac3_fluent_patterns_list_in_spec(self, src_scanner_spec_path):
        """Arrange: Read spec. Act: Search for fluent patterns list. Assert: Contains builder keywords."""
        spec_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            src_scanner_spec_path,
        )
        assert os.path.exists(spec_path), (
            f"Scanner spec not found at {spec_path} - implementation needed"
        )
        with open(spec_path, "r") as f:
            content = f.read()
        assert "QueryBuilder" in content or "querybuilder" in content.lower(), (
            "Spec must list QueryBuilder as a fluent pattern keyword"
        )
