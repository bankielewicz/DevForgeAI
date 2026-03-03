"""
Test: AC#7 - Confidence Scoring for Dynamic Dispatch
Story: STORY-403
Generated: 2026-02-14

Validates that functions potentially called via dynamic dispatch
(getattr, reflection) receive confidence < 0.5 and include
uncertainty_reason: "dynamic_dispatch".

These tests MUST FAIL initially (TDD Red phase).
"""
import re
import pytest


class TestConfidenceScoring:
    """Verify dynamic dispatch confidence scoring logic."""

    def test_should_document_dynamic_dispatch_detection_when_phase_4_defined(
        self, subagent_content
    ):
        """AC#7: Dynamic dispatch detection must be documented."""
        content = subagent_content
        assert re.search(
            r"(?i)dynamic.dispatch", content
        ), "Dynamic dispatch detection not documented in subagent"

    def test_should_set_confidence_below_05_for_dynamic_dispatch(
        self, subagent_content
    ):
        """AC#7: Confidence must be < 0.5 for dynamic dispatch functions."""
        content = subagent_content
        assert re.search(
            r"(?i)(confidence.*<\s*0\.5|confidence.*0\.[0-4]|low.confidence)",
            content,
        ), "Confidence < 0.5 rule for dynamic dispatch not documented"

    def test_should_include_uncertainty_reason_dynamic_dispatch(
        self, subagent_content
    ):
        """AC#7: Finding must include uncertainty_reason: dynamic_dispatch."""
        content = subagent_content
        assert re.search(
            r'(?i)uncertainty_reason.*dynamic_dispatch', content
        ), "uncertainty_reason: dynamic_dispatch not documented"

    def test_should_detect_getattr_as_dynamic_dispatch_indicator(
        self, subagent_content
    ):
        """AC#7: getattr() must be recognized as dynamic dispatch pattern."""
        content = subagent_content
        assert re.search(
            r"(?i)getattr", content
        ), "getattr not recognized as dynamic dispatch indicator"

    def test_should_detect_reflection_as_dynamic_dispatch_indicator(
        self, subagent_content
    ):
        """AC#7: Reflection patterns must be recognized as dynamic dispatch."""
        content = subagent_content
        assert re.search(
            r"(?i)reflect", content
        ), "Reflection not recognized as dynamic dispatch indicator"

    def test_should_set_high_confidence_for_definite_dead_code(
        self, subagent_content
    ):
        """AC#7: Functions with 0 callers and no dynamic dispatch should get high confidence (~0.9)."""
        content = subagent_content
        assert re.search(
            r"(?i)(confidence.*0\.9|high.confidence|confidence.*(?:high|1\.0))",
            content,
        ), "High confidence for definite dead code not documented"

    def test_should_handle_inheritance_override_with_medium_confidence(
        self, subagent_content
    ):
        """BR-004: Overridden methods should get medium confidence (~0.6) if check fails."""
        content = subagent_content
        assert re.search(
            r"(?i)(inherit|override|overridden)", content
        ), "Inheritance/override handling not documented"
