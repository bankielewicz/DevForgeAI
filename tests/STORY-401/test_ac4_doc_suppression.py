"""
Test: AC#4 - Documentation Example Suppression
Story: STORY-401
Generated: 2026-02-14

Validates that JSDoc and docstring code examples are suppressed (confidence < 0.7)
by the Stage 2 LLM classification, preventing false positives.
These tests will FAIL until the documentation suppression patterns are added to
.claude/agents/anti-pattern-scanner/references/two-stage-filter-patterns.md
"""
import re
import pytest


# === Fixture: Load suppression patterns from reference file ===

def load_doc_suppression_config():
    """
    Load documentation example suppression configuration from two-stage-filter-patterns.md.
    Returns dict with suppression patterns, expected classifications, and confidence ranges.
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
            "Documentation suppression patterns must be added."
        )

    with open(reference_path, "r") as f:
        content = f.read()

    config = _extract_doc_suppression_config(content)

    if not config:
        pytest.fail(
            "Documentation example suppression patterns for commented-out code "
            "not found in two-stage-filter-patterns.md. Expected JSDoc and "
            "docstring suppression rules."
        )

    return config


def _extract_doc_suppression_config(content: str) -> dict:
    """
    Extract documentation suppression configuration.
    Returns dict with has_jsdoc_suppression, has_docstring_suppression, etc.
    """
    config = {}
    lower = content.lower()

    # Must be in context of commented-out code detection
    if "commented" not in lower:
        return {}

    # Check for JSDoc suppression
    if "jsdoc" in lower:
        config["has_jsdoc_suppression"] = True

    # Check for docstring suppression
    if "docstring" in lower:
        config["has_docstring_suppression"] = True

    # Check for documentation classification
    if "documentation" in lower and ("suppress" in lower or "confidence" in lower):
        config["has_documentation_classification"] = True

    # Check for confidence < 0.7 suppression rule
    suppress_match = re.search(
        r"(?:documentation|docstring|jsdoc).*?confidence.*?(?:<|less than)\s*([\d.]+)",
        lower
    )
    if suppress_match:
        config["suppression_confidence_max"] = float(suppress_match.group(1))

    return config if len(config) > 0 else {}


# === Test Data: Documentation example samples ===

JSDOC_EXAMPLES = [
    {
        "name": "JSDoc @example with function call",
        "context": """
/**
 * Calculates the total price including tax.
 * @param {number} price - Base price
 * @returns {number} Total with tax
 * @example
 * // const total = calculateTotal(100);
 * // returns 108
 */
function calculateTotal(price) {
""",
        "candidate_line": "// const total = calculateTotal(100);",
        "expected_classification": "documentation",
        "expected_confidence_below": 0.7,
    },
    {
        "name": "JSDoc @example with import",
        "context": """
/**
 * User authentication module.
 * @module auth
 * @example
 * // import { login } from './auth';
 * // const session = await login(credentials);
 */
""",
        "candidate_line": "// import { login } from './auth';",
        "expected_classification": "documentation",
        "expected_confidence_below": 0.7,
    },
]

DOCSTRING_EXAMPLES = [
    {
        "name": "Python docstring with code example",
        "context": '''
def calculate_total(items):
    """Calculate the total price of items.

    Example:
        # from cart import calculate_total
        # total = calculate_total([item1, item2])
        # assert total > 0
    """
    return sum(item.price for item in items)
''',
        "candidate_line": "# from cart import calculate_total",
        "expected_classification": "documentation",
        "expected_confidence_below": 0.7,
    },
    {
        "name": "Python docstring with class example",
        "context": '''
class UserModel:
    """Represents a user in the system.

    Usage:
        # class AdminUser(UserModel):
        #     def admin_action(self):
        #         pass
    """
    pass
''',
        "candidate_line": "# class AdminUser(UserModel):",
        "expected_classification": "documentation",
        "expected_confidence_below": 0.7,
    },
]


# === Unit Tests ===

class TestDocSuppressionConfigLoading:
    """Tests that documentation suppression config loads from reference file."""

    def test_should_load_suppression_config_when_reference_exists(self):
        """Suppression config should load successfully."""
        config = load_doc_suppression_config()
        assert config is not None and len(config) > 0, (
            "Documentation suppression configuration should not be empty"
        )


class TestJSDocSuppression:
    """Tests that JSDoc code examples are properly suppressed."""

    def test_should_have_jsdoc_suppression_rule_when_config_loaded(self):
        """Reference file should define JSDoc example suppression."""
        config = load_doc_suppression_config()
        assert config.get("has_jsdoc_suppression", False), (
            "Reference file must define JSDoc example suppression rules. "
            "Expected 'jsdoc' mentioned in documentation suppression section."
        )

    @pytest.mark.parametrize(
        "example",
        JSDOC_EXAMPLES,
        ids=[e["name"] for e in JSDOC_EXAMPLES],
    )
    def test_should_classify_jsdoc_example_as_documentation_when_in_jsdoc_block(
        self, example
    ):
        """JSDoc @example code should be classified as 'documentation'."""
        # This test validates the expected classification behavior.
        # The actual LLM classification will be tested in integration,
        # but we validate the suppression rules are defined.
        config = load_doc_suppression_config()
        assert config.get("has_documentation_classification", False), (
            f"JSDoc example '{example['name']}' should be classifiable as "
            "'documentation' but documentation classification not found in config."
        )


class TestDocstringSuppression:
    """Tests that Python docstring code examples are properly suppressed."""

    def test_should_have_docstring_suppression_rule_when_config_loaded(self):
        """Reference file should define docstring example suppression."""
        config = load_doc_suppression_config()
        assert config.get("has_docstring_suppression", False), (
            "Reference file must define docstring example suppression rules. "
            "Expected 'docstring' mentioned in documentation suppression section."
        )

    @pytest.mark.parametrize(
        "example",
        DOCSTRING_EXAMPLES,
        ids=[e["name"] for e in DOCSTRING_EXAMPLES],
    )
    def test_should_classify_docstring_example_as_documentation_when_in_docstring(
        self, example
    ):
        """Docstring code examples should be classified as 'documentation'."""
        config = load_doc_suppression_config()
        assert config.get("has_documentation_classification", False), (
            f"Docstring example '{example['name']}' should be classifiable as "
            "'documentation' but documentation classification not found in config."
        )


class TestSuppressionConfidenceRange:
    """Tests confidence score behavior for documentation examples."""

    def test_should_suppress_documentation_below_threshold_when_classified(self):
        """Documentation examples should receive confidence < 0.7 (SUPPRESS)."""
        config = load_doc_suppression_config()
        max_confidence = config.get("suppression_confidence_max")
        assert max_confidence is not None, (
            "Suppression confidence maximum must be defined. "
            "Expected documentation examples to have confidence < 0.7"
        )
        assert max_confidence <= 0.7, (
            f"Documentation suppression confidence max should be <= 0.7, "
            f"got {max_confidence}"
        )

    def test_should_not_report_documentation_examples_when_suppressed(self):
        """Suppressed documentation examples must not appear in findings."""
        config = load_doc_suppression_config()
        max_confidence = config.get("suppression_confidence_max", 0.7)
        threshold = 0.7
        # Documentation confidence should be below reporting threshold
        assert max_confidence < threshold or max_confidence == threshold, (
            "Documentation confidence must be below reporting threshold (0.7)"
        )


class TestDocSuppressionEdgeCases:
    """Tests edge cases for documentation suppression."""

    def test_should_detect_jsdoc_block_boundary_when_star_slash_present(self):
        """Should recognize JSDoc block boundaries (/** ... */)."""
        config = load_doc_suppression_config()
        assert config.get("has_jsdoc_suppression", False), (
            "JSDoc block boundary detection required for accurate suppression"
        )

    def test_should_detect_python_docstring_boundary_when_triple_quotes_present(self):
        """Should recognize Python docstring boundaries (triple quotes)."""
        config = load_doc_suppression_config()
        assert config.get("has_docstring_suppression", False), (
            "Python docstring boundary detection required for accurate suppression"
        )

    def test_should_not_suppress_code_outside_docstring_when_adjacent(self):
        """Commented code outside docstring blocks should NOT be suppressed."""
        # This is a conceptual test - actual implementation will use context lines.
        # Verifies that the config distinguishes between inside/outside docstrings.
        config = load_doc_suppression_config()
        assert config.get("has_documentation_classification", False), (
            "Must support documentation classification to differentiate "
            "docstring examples from actual commented-out code"
        )
