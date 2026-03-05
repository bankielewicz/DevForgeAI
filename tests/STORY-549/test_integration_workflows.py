"""
Integration tests for STORY-549: Pricing Strategy Framework
Validates full end-to-end workflow paths across SKILL.md and pricing-strategy-framework.md.

Test scenarios:
1. Full Cost-Plus Workflow
2. Full Value-Based Workflow
3. Full Competitive Workflow (data present)
4. Full Competitive Workflow (data absent)
"""

import os
import re
import pytest

# Paths relative to project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SKILL_PATH = os.path.join(PROJECT_ROOT, "src", "claude", "skills", "managing-finances", "SKILL.md")
FRAMEWORK_PATH = os.path.join(
    PROJECT_ROOT, "src", "claude", "skills", "managing-finances", "references", "pricing-strategy-framework.md"
)

DISCLAIMER_TEXT = "not financial advice"


@pytest.fixture(scope="module")
def skill_content():
    """Load SKILL.md content."""
    with open(SKILL_PATH, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture(scope="module")
def framework_content():
    """Load pricing-strategy-framework.md content."""
    with open(FRAMEWORK_PATH, "r", encoding="utf-8") as f:
        return f.read()


# ---------------------------------------------------------------------------
# Cross-component integration: SKILL.md references framework correctly
# ---------------------------------------------------------------------------

class TestSkillFrameworkIntegration:
    """Verify SKILL.md correctly references and delegates to the framework."""

    def test_skill_references_pricing_framework_file(self, skill_content):
        assert "pricing-strategy-framework.md" in skill_content

    def test_skill_phase2_mentions_three_strategies(self, skill_content):
        assert "cost-plus" in skill_content.lower()
        assert "value-based" in skill_content.lower()
        assert "competitive" in skill_content.lower()

    def test_skill_references_output_path(self, skill_content):
        assert "pricing-model.md" in skill_content

    def test_skill_mentions_disclaimer_requirement(self, skill_content):
        assert DISCLAIMER_TEXT in skill_content.lower()


# ---------------------------------------------------------------------------
# Integration Test 1: Full Cost-Plus Workflow
# Strategy selection -> inputs -> calculation -> ASCII table -> file write -> disclaimer
# ---------------------------------------------------------------------------

class TestFullCostPlusWorkflow:
    """End-to-end cost-plus pricing workflow path through the framework."""

    def test_strategy_selection_presents_cost_plus(self, framework_content):
        assert "Cost-Plus Pricing" in framework_content

    def test_cost_plus_collects_variable_cost(self, framework_content):
        section = _extract_section(framework_content, "Strategy 1: Cost-Plus Pricing")
        assert "variable cost" in section.lower()

    def test_cost_plus_collects_fixed_cost(self, framework_content):
        section = _extract_section(framework_content, "Strategy 1: Cost-Plus Pricing")
        assert "fixed cost" in section.lower()

    def test_cost_plus_collects_unit_volume(self, framework_content):
        section = _extract_section(framework_content, "Strategy 1: Cost-Plus Pricing")
        assert "unit volume" in section.lower()

    def test_cost_plus_collects_margin(self, framework_content):
        section = _extract_section(framework_content, "Strategy 1: Cost-Plus Pricing")
        assert "margin" in section.lower()

    def test_cost_plus_formula_documented(self, framework_content):
        assert "VarCost + FixedCost / Units" in framework_content

    def test_cost_plus_ascii_table_present(self, framework_content):
        section = _extract_section(framework_content, "Strategy 1: Cost-Plus Pricing")
        assert "+-" in section, "ASCII table border not found in cost-plus section"

    def test_cost_plus_output_file_section_exists(self, framework_content):
        assert "Output File" in framework_content

    def test_cost_plus_disclaimer_in_framework(self, framework_content):
        assert DISCLAIMER_TEXT in framework_content.lower()


# ---------------------------------------------------------------------------
# Integration Test 2: Full Value-Based Workflow
# Strategy selection -> perceived value -> WTP anchors -> price range -> file write -> disclaimer
# ---------------------------------------------------------------------------

class TestFullValueBasedWorkflow:
    """End-to-end value-based pricing workflow path through the framework."""

    def test_strategy_selection_presents_value_based(self, framework_content):
        assert "Value-Based Pricing" in framework_content

    def test_value_based_collects_key_benefits(self, framework_content):
        section = _extract_section(framework_content, "Strategy 2: Value-Based Pricing")
        assert "key benefits" in section.lower()

    def test_value_based_collects_differentiation_factors(self, framework_content):
        section = _extract_section(framework_content, "Strategy 2: Value-Based Pricing")
        assert "differentiation" in section.lower()

    def test_value_based_collects_comparable_alternatives(self, framework_content):
        section = _extract_section(framework_content, "Strategy 2: Value-Based Pricing")
        assert "comparable alternatives" in section.lower()

    def test_value_based_collects_budget_range(self, framework_content):
        section = _extract_section(framework_content, "Strategy 2: Value-Based Pricing")
        assert "budget range" in section.lower()

    def test_value_based_collects_floor_price(self, framework_content):
        section = _extract_section(framework_content, "Strategy 2: Value-Based Pricing")
        assert "floor price" in section.lower()

    def test_value_based_generates_price_range(self, framework_content):
        section = _extract_section(framework_content, "Strategy 2: Value-Based Pricing")
        assert "price range" in section.lower()

    def test_value_based_includes_rationale(self, framework_content):
        section = _extract_section(framework_content, "Strategy 2: Value-Based Pricing")
        assert "rationale" in section.lower()

    def test_value_based_output_file_spec_matches(self, framework_content):
        output_section = _extract_section(framework_content, "Output File")
        assert "strategy name" in output_section.lower()
        assert "inputs summary" in output_section.lower()
        assert "disclaimer" in output_section.lower()


# ---------------------------------------------------------------------------
# Integration Test 3: Full Competitive Workflow (data present)
# Strategy selection -> market data read -> comparison table -> file write -> disclaimer
# ---------------------------------------------------------------------------

class TestFullCompetitiveWorkflowDataPresent:
    """End-to-end competitive pricing workflow when EPIC-074 data is available."""

    def test_strategy_selection_presents_competitive(self, framework_content):
        assert "Competitive Pricing" in framework_content

    def test_competitive_references_epic074_file(self, framework_content):
        section = _extract_section(framework_content, "Strategy 3: Competitive Pricing")
        assert "competitive-landscape.md" in section

    def test_competitive_extracts_competitor_names(self, framework_content):
        section = _extract_section(framework_content, "Strategy 3: Competitive Pricing")
        assert "competitor names" in section.lower()

    def test_competitive_extracts_pricing_data(self, framework_content):
        section = _extract_section(framework_content, "Strategy 3: Competitive Pricing")
        assert "price" in section.lower()

    def test_competitive_renders_comparison_table(self, framework_content):
        section = _extract_section(framework_content, "Strategy 3: Competitive Pricing")
        assert "comparison table" in section.lower()

    def test_competitive_positions_user_price(self, framework_content):
        section = _extract_section(framework_content, "Strategy 3: Competitive Pricing")
        assert "your price" in section.lower()

    def test_competitive_output_includes_all_required_sections(self, framework_content):
        output_section = _extract_section(framework_content, "Required Output Sections")
        required = ["strategy name", "date", "inputs summary", "calculated price", "rationale", "disclaimer"]
        for req in required:
            assert req in output_section.lower(), f"Missing required output section: {req}"


# ---------------------------------------------------------------------------
# Integration Test 4: Full Competitive Workflow (data absent)
# Strategy selection -> fallback message -> manual entry -> comparison table -> file write -> disclaimer
# ---------------------------------------------------------------------------

class TestFullCompetitiveWorkflowDataAbsent:
    """End-to-end competitive pricing workflow when EPIC-074 data is missing."""

    def test_graceful_degradation_section_exists(self, framework_content):
        assert "Graceful Degradation" in framework_content

    def test_fallback_message_for_missing_file(self, framework_content):
        section = _extract_section(framework_content, "Graceful Degradation")
        assert "unavailable" in section.lower() or "not found" in section.lower()

    def test_fallback_message_for_unparseable_file(self, framework_content):
        section = _extract_section(framework_content, "Graceful Degradation")
        assert "malformed" in section.lower() or "unparseable" in section.lower()

    def test_manual_entry_fallback_documented(self, framework_content):
        section = _extract_section(framework_content, "Graceful Degradation")
        assert "manual entry" in section.lower()

    def test_manual_entry_collects_competitor_names(self, framework_content):
        section = _extract_section(framework_content, "Graceful Degradation")
        assert "competitor" in section.lower()

    def test_workflow_completes_without_error(self, framework_content):
        section = _extract_section(framework_content, "Graceful Degradation")
        assert "without error" in section.lower() or "proceed" in section.lower()

    def test_disclaimer_present_in_all_outputs(self, framework_content):
        disclaimer_section = _extract_section(framework_content, "Disclaimer")
        assert DISCLAIMER_TEXT in disclaimer_section.lower()


# ---------------------------------------------------------------------------
# Output file spec cross-validation
# ---------------------------------------------------------------------------

class TestOutputFileSpecConsistency:
    """Verify output file spec is consistent across all strategies."""

    def test_output_path_documented(self, framework_content):
        assert "devforgeai/specs/business/financial/pricing-model.md" in framework_content

    def test_atomic_write_documented(self, framework_content):
        assert "atomic" in framework_content.lower()

    def test_all_six_required_sections_documented(self, framework_content):
        output_section = _extract_section(framework_content, "Required Output Sections")
        assert "strategy name" in output_section.lower()
        assert "date" in output_section.lower()
        assert "inputs summary" in output_section.lower()
        assert "rationale" in output_section.lower()
        assert "disclaimer" in output_section.lower()

    def test_disclaimer_text_specified(self, framework_content):
        disclaimer_section = _extract_section(framework_content, "Disclaimer")
        assert len(disclaimer_section) > 50, "Disclaimer section too short to contain required text"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _extract_section(content: str, heading: str) -> str:
    """Extract content from a markdown heading to the next same-level or higher heading."""
    lines = content.split("\n")
    start_idx = None
    heading_level = 0

    # Find the heading line
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("#") and heading in stripped:
            heading_level = len(stripped) - len(stripped.lstrip("#"))
            start_idx = i
            break

    if start_idx is None:
        return ""

    # Find next heading at same or higher level
    for i in range(start_idx + 1, len(lines)):
        stripped = lines[i].strip()
        if stripped.startswith("#"):
            level = len(stripped) - len(stripped.lstrip("#"))
            if level <= heading_level:
                return "\n".join(lines[start_idx:i])

    return "\n".join(lines[start_idx:])
