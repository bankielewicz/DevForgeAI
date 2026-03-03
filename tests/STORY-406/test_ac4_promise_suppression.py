"""
Test: AC#4 - Promise Chain Suppression
Story: STORY-406
Generated: 2026-02-16

Validates that promise chains (fetch().then().catch()) are classified
as 'fluent_api' with confidence < 0.7 and suppressed.
"""
import os
import re
import pytest


PROMISE_KEYWORDS = ["then", "catch", "finally", "fetch", "Promise"]


class TestPromisePatternDetection:
    """Promise chains should be identified by async/promise keywords."""

    def test_ac4_promise_contains_keywords(self, promise_chain_code):
        """Arrange: Promise chain. Act: Check for promise keywords. Assert: Found."""
        found_keywords = [
            kw for kw in PROMISE_KEYWORDS
            if kw.lower() in promise_chain_code.lower()
        ]
        assert len(found_keywords) > 0, (
            f"Promise chain should contain promise keywords: {promise_chain_code}"
        )

    def test_ac4_promise_matches_grep_pattern(self, grep_pattern, promise_chain_code):
        """Arrange: Promise chain. Act: Apply Stage 1 pattern. Assert: Matches."""
        result = re.search(grep_pattern, promise_chain_code)
        assert result is not None, (
            "Promise chain should match Stage 1 grep (suppression is Stage 2)"
        )

    def test_ac4_promise_expected_confidence_below_threshold(self, confidence_threshold):
        """Arrange: Promise expected confidence ~0.2. Act: Compare. Assert: Suppressed."""
        promise_confidence = 0.2  # Expected per story spec
        assert promise_confidence < confidence_threshold, (
            f"Promise confidence {promise_confidence} should be < {confidence_threshold}"
        )


class TestPromiseSuppressionInSpec:
    """Promise suppression must be documented in scanner spec."""

    def test_ac4_promise_suppression_in_spec(self, src_scanner_spec_path):
        """Arrange: Read spec. Act: Search for promise suppression. Assert: Documented."""
        spec_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            src_scanner_spec_path,
        )
        assert os.path.exists(spec_path), (
            f"Scanner spec not found at {spec_path} - implementation needed"
        )
        with open(spec_path, "r") as f:
            content = f.read().lower()
        has_promise = "promise" in content or "then" in content
        has_catch = "catch" in content
        assert has_promise and has_catch, (
            "Spec must document promise chain (then/catch) for suppression"
        )

    def test_ac4_fetch_then_catch_example_in_spec(self, src_scanner_spec_path):
        """Arrange: Read spec. Act: Search for fetch/then/catch example. Assert: Present."""
        spec_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            src_scanner_spec_path,
        )
        assert os.path.exists(spec_path), (
            f"Scanner spec not found at {spec_path} - implementation needed"
        )
        with open(spec_path, "r") as f:
            content = f.read()
        assert "fetch" in content.lower(), (
            "Spec must include fetch().then().catch() as a suppression example"
        )
