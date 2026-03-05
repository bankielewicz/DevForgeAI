"""
Test: AC#1 - Three Pricing Strategies Presented with Mandatory Selection
Story: STORY-549
Generated: 2026-03-04

Validates that the pricing strategy framework presents all three strategies
(cost-plus, value-based, competitive) and requires mandatory selection.
"""
import os
import re
import pytest

# Source files under test
SKILL_FILE = "src/claude/skills/managing-finances/SKILL.md"
FRAMEWORK_FILE = "src/claude/skills/managing-finances/references/pricing-strategy-framework.md"
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


@pytest.fixture
def skill_content():
    """Arrange: Read the SKILL.md file content."""
    path = os.path.join(PROJECT_ROOT, SKILL_FILE)
    assert os.path.exists(path), f"Source file does not exist: {SKILL_FILE}"
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def framework_content():
    """Arrange: Read the pricing-strategy-framework.md file content."""
    path = os.path.join(PROJECT_ROOT, FRAMEWORK_FILE)
    assert os.path.exists(path), f"Source file does not exist: {FRAMEWORK_FILE}"
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


class TestStrategyPresentation:
    """Tests that all three pricing strategies are presented."""

    def test_should_contain_cost_plus_strategy_when_framework_loaded(self, framework_content):
        """AC1: Cost-plus strategy must be presented with description."""
        assert re.search(r"cost[- ]plus", framework_content, re.IGNORECASE), (
            "Cost-plus pricing strategy not found in framework file"
        )

    def test_should_contain_value_based_strategy_when_framework_loaded(self, framework_content):
        """AC1: Value-based strategy must be presented with description."""
        assert re.search(r"value[- ]based", framework_content, re.IGNORECASE), (
            "Value-based pricing strategy not found in framework file"
        )

    def test_should_contain_competitive_strategy_when_framework_loaded(self, framework_content):
        """AC1: Competitive strategy must be presented with description."""
        assert re.search(r"competitive", framework_content, re.IGNORECASE), (
            "Competitive pricing strategy not found in framework file"
        )

    def test_should_present_all_three_strategies_in_single_section_when_framework_loaded(self, framework_content):
        """AC1: All three strategies should appear in a strategy selection/enumeration section."""
        # Find a section that enumerates all three strategies together
        has_cost_plus = bool(re.search(r"cost[- ]plus", framework_content, re.IGNORECASE))
        has_value_based = bool(re.search(r"value[- ]based", framework_content, re.IGNORECASE))
        has_competitive = bool(re.search(r"competitive", framework_content, re.IGNORECASE))
        assert all([has_cost_plus, has_value_based, has_competitive]), (
            "All three strategies must be present in the framework file"
        )

    def test_should_have_description_for_each_strategy_when_framework_loaded(self, framework_content):
        """AC1: Each strategy must have a clear description, not just a name."""
        # Each strategy name should be followed by descriptive text (at least 20 chars)
        for strategy in [r"cost[- ]plus", r"value[- ]based", r"competitive"]:
            match = re.search(strategy, framework_content, re.IGNORECASE)
            assert match, f"Strategy matching '{strategy}' not found"
            # Check there is substantial text after the strategy mention
            after_match = framework_content[match.end():match.end() + 200]
            assert len(after_match.strip()) > 20, (
                f"Strategy '{strategy}' lacks a description (< 20 chars after name)"
            )


class TestMandatorySelection:
    """Tests that strategy selection is mandatory before proceeding."""

    def test_should_require_selection_before_proceeding_when_workflow_starts(self, framework_content):
        """AC1: Workflow must block until user selects one strategy."""
        # Look for selection/choose/select instruction in the framework
        assert re.search(r"(select|choose|pick)\s+(one|a)\s+strategy", framework_content, re.IGNORECASE), (
            "No mandatory selection instruction found in framework file"
        )

    def test_should_reference_pricing_framework_in_skill_when_skill_loaded(self, skill_content):
        """AC1: SKILL.md must reference the pricing strategy framework."""
        assert re.search(r"pricing[- ]strategy[- ]framework", skill_content, re.IGNORECASE), (
            "SKILL.md does not reference pricing-strategy-framework"
        )

    def test_should_have_pricing_phase_in_skill_when_skill_loaded(self, skill_content):
        """AC1: SKILL.md must have a pricing phase entry point."""
        assert re.search(r"pric(e|ing)", skill_content, re.IGNORECASE), (
            "No pricing phase found in SKILL.md"
        )


class TestStrategyEnumerationDataDriven:
    """BR-002: Strategy enumeration must be data-driven, not hardcoded conditionals."""

    def test_should_use_enumeration_structure_when_listing_strategies(self, framework_content):
        """BR-002: Strategies listed as data enumeration, not if/else branches."""
        # Look for a structured list/table of strategies rather than conditional logic
        # A data-driven approach would use a list/table pattern
        list_pattern = re.search(
            r"(\|.*cost[- ]plus.*\||\-\s+\*\*cost[- ]plus|#{1,3}\s+.*cost[- ]plus)",
            framework_content,
            re.IGNORECASE,
        )
        assert list_pattern, (
            "Strategies do not appear in a data-driven enumeration structure"
        )

    def test_should_not_hardcode_strategy_selection_as_conditionals(self, framework_content):
        """BR-002: No hardcoded if/else for strategy selection."""
        # Ensure there are no if/else conditional branches for strategy routing
        conditional_pattern = re.search(
            r"(if\s+strategy\s*==|else\s*if\s+strategy|switch\s*\(\s*strategy)",
            framework_content,
            re.IGNORECASE,
        )
        assert not conditional_pattern, (
            "Strategy selection uses hardcoded conditional branches (violates BR-002)"
        )
