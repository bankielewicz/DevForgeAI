"""
Test: AC#1 - Stage 1 Grep Pattern Detection
Story: STORY-406
Generated: 2026-02-16

Validates that the Grep pattern \\w+(\\.\\w+\\([^)]*\\)){3,} correctly
matches 3+ chained method calls and is documented in the scanner spec.
"""
import re
import os
import pytest


# ============================================================
# Unit Tests: Pattern Matching Behavior
# ============================================================

class TestGrepPatternMatches3PlusChains:
    """Pattern must match method chains with 3 or more chained calls."""

    def test_ac1_three_chain_matches(self, grep_pattern, navigation_chain_code):
        """Arrange: 3-level chain. Act: Apply pattern. Assert: Match found."""
        result = re.search(grep_pattern, navigation_chain_code)
        assert result is not None, (
            f"Pattern should match 3-level chain: {navigation_chain_code}"
        )

    def test_ac1_four_chain_matches(self, grep_pattern, long_navigation_chain):
        """Arrange: 4-level chain. Act: Apply pattern. Assert: Match found."""
        result = re.search(grep_pattern, long_navigation_chain)
        assert result is not None, (
            f"Pattern should match 4-level chain: {long_navigation_chain}"
        )

    def test_ac1_builder_chain_matches_stage1(self, grep_pattern, builder_chain_code):
        """Arrange: Builder chain (3+ calls). Act: Apply pattern. Assert: Match found.
        Note: Stage 1 is high-recall; suppression happens in Stage 2."""
        result = re.search(grep_pattern, builder_chain_code)
        assert result is not None, (
            f"Stage 1 should match builder chains too (filtering in Stage 2): {builder_chain_code}"
        )

    def test_ac1_promise_chain_matches_stage1(self, grep_pattern, promise_chain_code):
        """Arrange: Promise chain (3+ calls). Act: Apply pattern. Assert: Match found."""
        result = re.search(grep_pattern, promise_chain_code)
        assert result is not None, (
            f"Stage 1 should match promise chains too: {promise_chain_code}"
        )


class TestGrepPatternRejectsBelowThreshold:
    """Pattern must NOT match chains with fewer than 3 chained calls."""

    def test_ac1_two_chain_no_match(self, grep_pattern, short_chain_code):
        """Arrange: 2-level chain. Act: Apply pattern. Assert: No match."""
        result = re.search(grep_pattern, short_chain_code)
        assert result is None, (
            f"Pattern should NOT match 2-level chain: {short_chain_code}"
        )

    def test_ac1_single_call_no_match(self, grep_pattern):
        """Arrange: Single method call. Act: Apply pattern. Assert: No match."""
        code = "obj.getData()"
        result = re.search(grep_pattern, code)
        assert result is None, f"Pattern should NOT match single call: {code}"

    def test_ac1_no_parens_no_match(self, grep_pattern):
        """Arrange: Property access (no parens). Act: Apply pattern. Assert: No match."""
        code = "obj.a.b.c.d"
        result = re.search(grep_pattern, code)
        assert result is None, (
            f"Pattern should NOT match property access without parens: {code}"
        )


class TestGrepPatternInScannerSpec:
    """The pattern MUST be documented in the anti-pattern-scanner.md spec."""

    def test_ac1_pattern_exists_in_spec(self, src_scanner_spec_path):
        """Arrange: Read scanner spec. Act: Search for pattern. Assert: Found."""
        spec_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            src_scanner_spec_path,
        )
        assert os.path.exists(spec_path), (
            f"Scanner spec not found at {spec_path} - implementation needed"
        )
        with open(spec_path, "r") as f:
            content = f.read()
        # The pattern or its description must exist in the spec
        assert "message_chain" in content.lower() or "message chain" in content.lower(), (
            "Scanner spec must contain message chain detection section"
        )

    def test_ac1_min_chain_length_3_in_spec(self, src_scanner_spec_path):
        """Arrange: Read scanner spec. Act: Search for min chain length. Assert: 3."""
        spec_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            src_scanner_spec_path,
        )
        assert os.path.exists(spec_path), (
            f"Scanner spec not found at {spec_path} - implementation needed"
        )
        with open(spec_path, "r") as f:
            content = f.read()
        # Must specify minimum chain length of 3
        assert "{3,}" in content or "min_chain_length" in content, (
            "Scanner spec must specify minimum chain length of 3"
        )
