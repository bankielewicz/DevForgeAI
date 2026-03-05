"""Integration tests for STORY-536: Competitive Landscape Analysis.

Validates cross-file consistency, phase flow integration, subagent invocation
patterns, and reference file linkage across implementation files.

Story: STORY-536
Phase: Integration (Phase 05)
"""
import os
import re
import pytest


# ---------------------------------------------------------------------------
# Scenario 1: Skill Phase Flow Integration
# Competitive analysis phase (Step 10) follows market sizing phases (Steps 0-9)
# ---------------------------------------------------------------------------


class TestSkillPhaseFlowIntegration:
    """Verify competitive analysis phase integrates correctly with existing
    skill phases -- Step 10 follows Step 9 in SKILL.md."""

    def test_step_10_exists_after_step_9(self, skill_content):
        """Step 10 must appear after Step 9 in SKILL.md."""
        assert skill_content, "SKILL.md is empty or missing"
        step_9_pos = skill_content.find("Step 9")
        step_10_pos = skill_content.find("Step 10")
        assert step_9_pos != -1, "Step 9 not found in SKILL.md"
        assert step_10_pos != -1, "Step 10 not found in SKILL.md"
        assert step_10_pos > step_9_pos, (
            f"Step 10 (pos {step_10_pos}) must appear after Step 9 (pos {step_9_pos})"
        )

    def test_competitive_analysis_section_exists(self, skill_content):
        """SKILL.md must have a Competitive Analysis Phase section."""
        assert skill_content, "SKILL.md is empty or missing"
        assert re.search(r"(?i)##.*competitive\s+analysis", skill_content), (
            "SKILL.md must contain a '## Competitive Analysis' section header"
        )

    def test_step_10_is_about_competitive_analysis(self, skill_content):
        """Step 10 content must relate to competitive analysis."""
        assert skill_content, "SKILL.md is empty or missing"
        # Find Step 10 section and check its content mentions competitive/market-analyst
        step_10_match = re.search(
            r"###?\s*Step\s*10[:\s].*?((?:competitive|market.analyst))",
            skill_content,
            re.IGNORECASE | re.DOTALL,
        )
        assert step_10_match, (
            "Step 10 heading must reference competitive analysis or market-analyst"
        )

    def test_no_phase_gap_between_9_and_10(self, skill_content):
        """No missing step numbers between Step 9 and Step 10."""
        assert skill_content, "SKILL.md is empty or missing"
        step_numbers = [
            int(m.group(1))
            for m in re.finditer(r"###?\s*Step\s+(\d+)", skill_content)
        ]
        assert 9 in step_numbers, "Step 9 missing"
        assert 10 in step_numbers, "Step 10 missing"


# ---------------------------------------------------------------------------
# Scenario 2: Subagent Invocation Consistency
# SKILL.md must invoke market-analyst via Task() with correct subagent_type
# ---------------------------------------------------------------------------


class TestSubagentInvocationIntegration:
    """Verify SKILL.md correctly references market-analyst subagent via Task()
    and the subagent file exists at the expected path."""

    def test_skill_task_invocation_matches_subagent_name(
        self, skill_content, subagent_content
    ):
        """Task(subagent_type=...) in SKILL.md must match subagent 'name' field."""
        assert skill_content, "SKILL.md is empty or missing"
        assert subagent_content, "market-analyst.md is empty or missing"

        # Extract name from subagent YAML frontmatter
        name_match = re.search(r"^name:\s*(.+)$", subagent_content, re.MULTILINE)
        assert name_match, "market-analyst.md must have 'name:' in YAML frontmatter"
        subagent_name = name_match.group(1).strip()

        # Verify SKILL.md references this exact name in Task()
        assert subagent_name in skill_content, (
            f"SKILL.md must reference subagent name '{subagent_name}' in Task() invocation"
        )

    def test_skill_provides_research_context_to_subagent(self, skill_content):
        """Task() prompt in SKILL.md must pass research context to market-analyst."""
        assert skill_content, "SKILL.md is empty or missing"
        # The Task() call should mention research/competitors/market in prompt
        task_block = re.search(
            r'Task\s*\([^)]*market.analyst[^)]*\)', skill_content, re.DOTALL
        )
        assert task_block, "SKILL.md must have Task() call for market-analyst"
        task_text = task_block.group(0)
        has_context = any(
            kw in task_text.lower()
            for kw in ["competitor", "market", "research", "landscape", "positioning"]
        )
        assert has_context, (
            "Task() invocation must pass research context (competitor/market/research keywords)"
        )

    def test_subagent_does_not_invoke_skills(self, subagent_content):
        """market-analyst subagent must not invoke skills (subagent convention)."""
        assert subagent_content, "market-analyst.md is empty or missing"
        # Subagents must not contain Skill() invocations
        assert not re.search(r'Skill\s*\(', subagent_content), (
            "Subagent must not invoke Skill() -- subagent convention violation"
        )


# ---------------------------------------------------------------------------
# Scenario 3: Cross-File Consistency
# Subagent output dimensions must match template structure
# ---------------------------------------------------------------------------


class TestCrossFileConsistency:
    """Verify subagent positioning matrix dimensions match the output template
    structure in competitive-analysis.md."""

    REQUIRED_DIMENSIONS = [
        "name",
        "category",
        "strengths",
        "weaknesses",
        "market position summary",
        "differentiation",
    ]

    def test_subagent_dimensions_match_template_columns(
        self, subagent_content, output_content
    ):
        """All 6 positioning matrix dimensions in subagent must appear in template."""
        assert subagent_content, "market-analyst.md is empty or missing"
        assert output_content, "competitive-analysis.md is empty or missing"

        for dim in self.REQUIRED_DIMENSIONS:
            assert re.search(re.escape(dim), subagent_content, re.IGNORECASE), (
                f"Dimension '{dim}' missing from market-analyst.md"
            )
            # Template must have matching column or section
            assert re.search(re.escape(dim), output_content, re.IGNORECASE), (
                f"Dimension '{dim}' missing from competitive-analysis.md template"
            )

    def test_template_has_positioning_matrix_table(self, output_content):
        """competitive-analysis.md must contain a markdown table for positioning matrix."""
        assert output_content, "competitive-analysis.md is empty or missing"
        assert re.search(r"\|.*Name.*\|.*Category.*\|", output_content, re.IGNORECASE), (
            "competitive-analysis.md must contain positioning matrix table with Name and Category columns"
        )

    def test_template_has_competitor_profiles_section(self, output_content):
        """competitive-analysis.md must have Competitor Profiles section."""
        assert output_content, "competitive-analysis.md is empty or missing"
        assert re.search(r"(?i)##.*competitor\s+profiles", output_content), (
            "competitive-analysis.md must have '## Competitor Profiles' section"
        )

    def test_template_has_differentiation_section(self, output_content):
        """competitive-analysis.md must have Differentiation Opportunities section."""
        assert output_content, "competitive-analysis.md is empty or missing"
        assert re.search(r"(?i)##.*differentiation", output_content), (
            "competitive-analysis.md must have '## Differentiation Opportunities' section"
        )

    def test_subagent_output_template_matches_template_file(
        self, subagent_content, output_content
    ):
        """Subagent's output template section structure must align with template file."""
        assert subagent_content, "market-analyst.md is empty or missing"
        assert output_content, "competitive-analysis.md is empty or missing"

        # Both must have: Positioning Matrix, Competitor Profiles, Differentiation
        for section in [
            "Positioning Matrix",
            "Competitor Profiles",
            "Differentiation",
        ]:
            assert re.search(re.escape(section), subagent_content, re.IGNORECASE), (
                f"Subagent missing section: {section}"
            )
            assert re.search(re.escape(section), output_content, re.IGNORECASE), (
                f"Template missing section: {section}"
            )


# ---------------------------------------------------------------------------
# Scenario 4: Reference File Linkage
# SKILL.md must reference competitive-analysis-framework.md
# ---------------------------------------------------------------------------


class TestReferenceFileLinkage:
    """Verify SKILL.md references the competitive-analysis-framework.md file."""

    def test_skill_references_framework_file(self, skill_content):
        """SKILL.md must reference competitive-analysis-framework.md."""
        assert skill_content, "SKILL.md is empty or missing"
        assert re.search(
            r"competitive-analysis-framework\.md", skill_content
        ), (
            "SKILL.md must reference competitive-analysis-framework.md"
        )

    def test_skill_reference_table_includes_framework(self, skill_content):
        """SKILL.md Reference Files table must list the framework reference."""
        assert skill_content, "SKILL.md is empty or missing"
        # Check for reference table entry
        assert re.search(
            r"\|.*[Cc]ompetitive.*\|.*competitive-analysis-framework", skill_content
        ), (
            "SKILL.md Reference Files table must include competitive-analysis-framework.md"
        )

    def test_skill_integration_section_lists_market_analyst(self, skill_content):
        """SKILL.md Integration section must list market-analyst as subagent dependency."""
        assert skill_content, "SKILL.md is empty or missing"
        # Find Integration section and verify market-analyst listed
        integration_match = re.search(
            r"(?i)##\s*Integration(.*?)(?=^##\s|\Z)",
            skill_content,
            re.MULTILINE | re.DOTALL,
        )
        assert integration_match, "SKILL.md must have '## Integration' section"
        integration_text = integration_match.group(1)
        assert re.search(r"market.analyst", integration_text, re.IGNORECASE), (
            "Integration section must list market-analyst as a subagent dependency"
        )

    def test_skill_output_files_lists_competitive_analysis(self, skill_content):
        """SKILL.md must list competitive-analysis.md as an output file."""
        assert skill_content, "SKILL.md is empty or missing"
        assert re.search(
            r"competitive-analysis\.md", skill_content
        ), (
            "SKILL.md must list competitive-analysis.md as an output file"
        )
