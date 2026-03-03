"""
Test: AC#3 - Stage 2 LLM Classification with Chain-of-Thought
Story: STORY-401
Generated: 2026-02-14

Validates Stage 2 LLM classification behavior including chain-of-thought reasoning,
classification categories (code/documentation/todo), and confidence scoring.
These tests will FAIL until the Stage 2 LLM prompt template is added to
.claude/agents/anti-pattern-scanner/references/two-stage-filter-patterns.md
"""
import re
import pytest


# === Fixture: Load Stage 2 configuration from reference file ===

def load_stage2_config():
    """
    Load Stage 2 LLM classification configuration from two-stage-filter-patterns.md.
    Returns a dict with prompt_template, confidence_threshold, context_lines, classifications.
    """
    import os

    reference_path = os.path.join(
        os.path.dirname(__file__),
        "..", "..",
        ".claude", "agents", "anti-pattern-scanner",
        "references", "two-stage-filter-patterns.md"
    )
    reference_path = os.path.normpath(reference_path)

    if not os.path.exists(reference_path):
        pytest.fail(
            f"Reference file not found: {reference_path}. "
            "Stage 2 LLM classification config must be added."
        )

    with open(reference_path, "r") as f:
        content = f.read()

    config = _extract_stage2_config(content)

    if not config:
        pytest.fail(
            "Stage 2 LLM classification for commented-out code not found in "
            "two-stage-filter-patterns.md. Expected section with LLM prompt template, "
            "confidence threshold, and classification categories."
        )

    return config


def _extract_stage2_config(content: str) -> dict:
    """
    Extract Stage 2 LLM configuration for commented-out code detection.
    Returns dict with keys: prompt_template, confidence_threshold, context_lines, classifications.
    """
    config = {}

    # Check for commented-out code Stage 2 section
    lower_content = content.lower()
    if "commented" not in lower_content:
        return {}

    # Look for chain-of-thought / thinking tags
    if "thinking" in lower_content or "chain-of-thought" in lower_content or "chain_of_thought" in lower_content:
        config["has_chain_of_thought"] = True

    # Look for classification categories
    classifications = []
    for category in ["code", "documentation", "todo"]:
        if f"'{category}'" in lower_content or f'"{category}"' in lower_content:
            classifications.append(category)
    config["classifications"] = classifications

    # Look for confidence threshold
    threshold_match = re.search(r"confidence.*?(?:threshold|>=)\s*([\d.]+)", lower_content)
    if threshold_match:
        config["confidence_threshold"] = float(threshold_match.group(1))

    # Look for context lines specification
    context_match = re.search(r"[+-]?\s*(\d+)\s*lines?\s*(?:of\s*)?(?:surrounding\s*)?context", lower_content)
    if context_match:
        config["context_lines"] = int(context_match.group(1))

    # Look for LLM prompt template
    code_blocks = re.findall(r"```[^\n]*\n(.*?)```", content, re.DOTALL)
    for block in code_blocks:
        if "classify" in block.lower() or "assess" in block.lower():
            if "commented" in block.lower() or "comment" in block.lower():
                config["prompt_template"] = block.strip()
                break

    return config if len(config) > 1 else {}


# === Unit Tests ===

class TestStage2ConfigLoading:
    """Tests that Stage 2 LLM config loads from reference file."""

    def test_should_load_config_when_reference_file_exists(self):
        """Stage 2 config should load successfully."""
        config = load_stage2_config()
        assert config is not None, "Stage 2 configuration should not be None"
        assert len(config) > 0, "Stage 2 configuration should not be empty"


class TestStage2ChainOfThought:
    """Tests that Stage 2 uses chain-of-thought reasoning (PE-005)."""

    def test_should_include_thinking_tags_when_prompt_generated(self):
        """LLM prompt should include thinking/chain-of-thought instructions."""
        config = load_stage2_config()
        assert config.get("has_chain_of_thought", False), (
            "Stage 2 must include chain-of-thought (PE-005) reasoning. "
            "Expected 'thinking' or 'chain-of-thought' in prompt template."
        )

    def test_should_have_prompt_template_when_config_loaded(self):
        """A prompt template should exist for LLM classification."""
        config = load_stage2_config()
        assert "prompt_template" in config, (
            "Stage 2 must have a prompt template for LLM classification. "
            "Expected a code block with classify/assess instructions."
        )

    def test_should_reference_context_in_prompt_when_template_exists(self):
        """Prompt template should reference surrounding context lines."""
        config = load_stage2_config()
        if "prompt_template" in config:
            template = config["prompt_template"].lower()
            assert "context" in template or "surrounding" in template, (
                "Prompt template should reference surrounding context lines"
            )


class TestStage2ClassificationCategories:
    """Tests that Stage 2 supports code/documentation/todo classifications."""

    def test_should_have_code_classification_when_config_loaded(self):
        """Classification 'code' should be available for actual commented-out code."""
        config = load_stage2_config()
        classifications = config.get("classifications", [])
        assert "code" in classifications, (
            "Stage 2 must support 'code' classification for actual commented-out code"
        )

    def test_should_have_documentation_classification_when_config_loaded(self):
        """Classification 'documentation' should be available for docstring examples."""
        config = load_stage2_config()
        classifications = config.get("classifications", [])
        assert "documentation" in classifications, (
            "Stage 2 must support 'documentation' classification for docstring examples"
        )

    def test_should_have_todo_classification_when_config_loaded(self):
        """Classification 'todo' should be available for TODO with code sketches."""
        config = load_stage2_config()
        classifications = config.get("classifications", [])
        assert "todo" in classifications, (
            "Stage 2 must support 'todo' classification for intentional TODO comments"
        )

    def test_should_have_exactly_three_classifications_when_config_loaded(self):
        """Should have exactly three classification categories."""
        config = load_stage2_config()
        classifications = config.get("classifications", [])
        assert len(classifications) == 3, (
            f"Expected exactly 3 classifications (code, documentation, todo), "
            f"got {len(classifications)}: {classifications}"
        )


class TestStage2ConfidenceThreshold:
    """Tests confidence threshold configuration."""

    def test_should_have_confidence_threshold_when_config_loaded(self):
        """Confidence threshold should be defined (expected 0.7)."""
        config = load_stage2_config()
        assert "confidence_threshold" in config, (
            "Stage 2 must define a confidence threshold for reporting decisions"
        )

    def test_should_set_threshold_at_zero_point_seven_when_configured(self):
        """Confidence threshold should be 0.7 per AC#3."""
        config = load_stage2_config()
        threshold = config.get("confidence_threshold")
        assert threshold == 0.7, (
            f"Confidence threshold should be 0.7 (per AC#3), got {threshold}"
        )


class TestStage2ContextLines:
    """Tests context line configuration for LLM assessment."""

    def test_should_specify_context_lines_when_config_loaded(self):
        """Should specify number of surrounding context lines for LLM."""
        config = load_stage2_config()
        assert "context_lines" in config, (
            "Stage 2 must specify context_lines (expected 5 per AC#3)"
        )

    def test_should_use_five_context_lines_when_configured(self):
        """Should use +/-5 lines of surrounding context per AC#3."""
        config = load_stage2_config()
        context_lines = config.get("context_lines")
        assert context_lines == 5, (
            f"Context lines should be 5 (per AC#3), got {context_lines}"
        )


class TestStage2DecisionLogic:
    """Tests the decision logic for Stage 2 classification."""

    def test_should_report_when_confidence_at_threshold(self):
        """Confidence exactly at 0.7 should result in REPORT."""
        # This tests the business rule: confidence >= 0.7 = REPORT
        config = load_stage2_config()
        threshold = config.get("confidence_threshold", 0.7)
        confidence = 0.7
        decision = "REPORT" if confidence >= threshold else "SUPPRESS"
        assert decision == "REPORT", (
            f"Confidence {confidence} >= threshold {threshold} should REPORT"
        )

    def test_should_suppress_when_confidence_below_threshold(self):
        """Confidence below 0.7 should result in SUPPRESS."""
        config = load_stage2_config()
        threshold = config.get("confidence_threshold", 0.7)
        confidence = 0.69
        decision = "REPORT" if confidence >= threshold else "SUPPRESS"
        assert decision == "SUPPRESS", (
            f"Confidence {confidence} < threshold {threshold} should SUPPRESS"
        )

    def test_should_default_confidence_to_half_when_missing(self):
        """If confidence is missing, default to 0.5 (suppress)."""
        # Business rule BR-003: If confidence missing, default to 0.5
        config = load_stage2_config()
        threshold = config.get("confidence_threshold", 0.7)
        default_confidence = 0.5
        decision = "REPORT" if default_confidence >= threshold else "SUPPRESS"
        assert decision == "SUPPRESS", (
            f"Default confidence {default_confidence} should result in SUPPRESS"
        )
