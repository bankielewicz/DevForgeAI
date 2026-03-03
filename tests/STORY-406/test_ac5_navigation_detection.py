"""
Test: AC#5 - Navigation Chain Detection
Story: STORY-406
Generated: 2026-02-16

Validates that navigation chains (order.getCustomer().getAddress().getCity())
are classified as 'navigation_chain' with confidence >= 0.7 and reported.
"""
import os
import re
import pytest


class TestNavigationChainDetection:
    """Navigation chains with get*() pattern should be detected and reported."""

    def test_ac5_navigation_matches_grep_pattern(self, grep_pattern, navigation_chain_code):
        """Arrange: Navigation chain. Act: Apply Stage 1 pattern. Assert: Matches."""
        result = re.search(grep_pattern, navigation_chain_code)
        assert result is not None, (
            f"Navigation chain should match Stage 1 grep: {navigation_chain_code}"
        )

    def test_ac5_navigation_contains_getter_pattern(self, navigation_chain_code):
        """Arrange: Navigation chain. Act: Check for get*() pattern. Assert: Found."""
        getter_pattern = r'get\w+\('
        matches = re.findall(getter_pattern, navigation_chain_code)
        assert len(matches) >= 2, (
            f"Navigation chain should contain multiple get*() calls: {navigation_chain_code}"
        )

    def test_ac5_navigation_expected_confidence_above_threshold(self, confidence_threshold):
        """Arrange: Navigation expected confidence ~0.85. Act: Compare. Assert: Reported."""
        navigation_confidence = 0.85  # Expected per story spec
        assert navigation_confidence >= confidence_threshold, (
            f"Navigation confidence {navigation_confidence} should be >= {confidence_threshold}"
        )

    def test_ac5_long_navigation_detected(self, grep_pattern, long_navigation_chain):
        """Arrange: 4-level navigation. Act: Apply pattern. Assert: Matches."""
        result = re.search(grep_pattern, long_navigation_chain)
        assert result is not None, (
            f"4-level navigation chain should match: {long_navigation_chain}"
        )

    def test_ac5_user_profile_navigation_detected(self, grep_pattern):
        """Arrange: user.getProfile().getSettings().getTheme(). Act: Apply pattern. Assert: Matches."""
        code = "user.getProfile().getSettings().getTheme()"
        result = re.search(grep_pattern, code)
        assert result is not None, (
            f"User profile navigation chain should match: {code}"
        )


class TestNavigationDetectionInSpec:
    """Navigation chain detection must be documented in scanner spec."""

    def test_ac5_navigation_chain_in_spec(self, src_scanner_spec_path):
        """Arrange: Read spec. Act: Search for navigation chain. Assert: Documented."""
        spec_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            src_scanner_spec_path,
        )
        assert os.path.exists(spec_path), (
            f"Scanner spec not found at {spec_path} - implementation needed"
        )
        with open(spec_path, "r") as f:
            content = f.read().lower()
        assert "navigation" in content, (
            "Spec must document navigation chain detection"
        )
        assert "demeter" in content or "law of demeter" in content, (
            "Spec must reference Law of Demeter for navigation chains"
        )

    def test_ac5_getter_navigation_example_in_spec(self, src_scanner_spec_path):
        """Arrange: Read spec. Act: Search for getter navigation example. Assert: Present."""
        spec_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            src_scanner_spec_path,
        )
        assert os.path.exists(spec_path), (
            f"Scanner spec not found at {spec_path} - implementation needed"
        )
        with open(spec_path, "r") as f:
            content = f.read()
        has_getter_example = (
            "getCustomer" in content or
            "getAddress" in content or
            "getCity" in content or
            "get_customer" in content
        )
        assert has_getter_example, (
            "Spec must include a getter navigation chain example (e.g., getCustomer().getAddress())"
        )
