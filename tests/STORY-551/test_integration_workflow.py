"""
Test: Integration - Full /financial-model Command Workflow Chain
Story: STORY-551
Generated: 2026-03-05

Validates cross-file integration points:
1. Command -> Skill delegation (file existence + reference consistency)
2. Skill -> Subagent coordination (subagent referenced and capabilities align)
3. Skill -> References (pricing-strategy-framework.md, break-even-analysis.md exist)
4. Cross-file consistency (disclaimer, naming)
5. End-to-end workflow chain (command -> skill -> subagent linkage)
"""

import re
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# Integration Point 1: Command -> Skill Delegation
# ---------------------------------------------------------------------------


class TestCommandToSkillDelegation:
    """Verify the command file delegates to the skill and the skill exists."""

    def test_command_references_managing_finances_skill(self, command_content):
        """Command must reference managing-finances skill by exact name."""
        assert "managing-finances" in command_content, (
            "Command does not reference 'managing-finances' skill. "
            "Integration broken: command cannot delegate to skill."
        )

    def test_skill_file_exists_at_expected_path(self, skill_file):
        """The skill file the command delegates to must exist."""
        assert skill_file.exists(), (
            f"Skill file not found at {skill_file}. "
            "Command delegates to managing-finances but skill file is missing."
        )

    def test_command_skill_invocation_matches_skill_name(
        self, command_content, skill_content
    ):
        """The skill name in the command invocation must match the skill's
        YAML frontmatter name field."""
        # Extract skill name from command invocation
        invocation_match = re.search(
            r'Skill\(command="([^"]+)"', command_content
        )
        assert invocation_match, (
            "Command does not contain Skill(command=\"...\") invocation pattern."
        )
        invoked_name = invocation_match.group(1)

        # Extract skill name from YAML frontmatter
        frontmatter_match = re.search(
            r'^---\s*\n(.*?)\n---', skill_content, re.DOTALL
        )
        assert frontmatter_match, "Skill file missing YAML frontmatter."
        frontmatter = frontmatter_match.group(1)
        name_match = re.search(r'name:\s*(\S+)', frontmatter)
        assert name_match, "Skill frontmatter missing 'name' field."
        skill_name = name_match.group(1)

        assert invoked_name == skill_name, (
            f"Command invokes '{invoked_name}' but skill name is '{skill_name}'. "
            "Name mismatch breaks delegation chain."
        )

    def test_skill_contains_phases_referenced_by_command(self, skill_content):
        """Skill must contain workflow phases (command delegates all logic)."""
        phase_pattern = re.compile(r'###\s+Phase\s+\d+', re.IGNORECASE)
        phases_found = phase_pattern.findall(skill_content)
        assert len(phases_found) >= 3, (
            f"Skill has only {len(phases_found)} phases. "
            "Command delegates full workflow; skill needs multiple phases."
        )


# ---------------------------------------------------------------------------
# Integration Point 2: Skill -> Subagent Coordination
# ---------------------------------------------------------------------------


class TestSkillToSubagentCoordination:
    """Verify the skill references the subagent and capabilities align."""

    def test_skill_references_financial_modeler_subagent(self, skill_content):
        """Skill must reference the financial-modeler subagent."""
        assert "financial-modeler" in skill_content.lower(), (
            "Skill does not reference 'financial-modeler' subagent. "
            "Integration broken: skill cannot coordinate with subagent."
        )

    def test_subagent_file_exists(self, subagent_file):
        """The subagent file referenced by the skill must exist."""
        assert subagent_file.exists(), (
            f"Subagent file not found at {subagent_file}. "
            "Skill references financial-modeler but file is missing."
        )

    def test_subagent_produces_projections_skill_expects(
        self, skill_content, subagent_content
    ):
        """Subagent output capabilities must align with what the skill expects.
        The skill expects revenue projections; the subagent must declare that
        capability."""
        # Skill expects revenue projection output
        assert re.search(r'(?i)revenue\s+projection', skill_content), (
            "Skill does not mention revenue projection in its workflow."
        )
        # Subagent must declare projection output capability
        assert re.search(r'(?i)revenue\s+projection', subagent_content), (
            "Subagent does not declare revenue projection capability. "
            "Skill expects projections but subagent cannot produce them."
        )

    def test_subagent_has_no_skill_invocations(self, subagent_content):
        """Subagent must not invoke skills (constraint from AC#2).
        This is an integration concern: circular invocation would break
        the chain."""
        skill_call = re.search(
            r'Skill\s*\(', subagent_content
        )
        assert not skill_call, (
            "Subagent contains Skill() invocation. "
            "Circular dependency: subagent must not call back to skills."
        )


# ---------------------------------------------------------------------------
# Integration Point 3: Skill -> Reference Files
# ---------------------------------------------------------------------------


class TestSkillToReferenceFiles:
    """Verify referenced files (pricing-strategy, break-even) exist."""

    @pytest.fixture
    def references_dir(self, project_root):
        """Path to the managing-finances references directory."""
        return (
            project_root
            / "claude"
            / "skills"
            / "managing-finances"
            / "references"
        )

    def test_pricing_strategy_framework_exists(self, references_dir):
        """pricing-strategy-framework.md must exist as referenced by skill."""
        ref_file = references_dir / "pricing-strategy-framework.md"
        assert ref_file.exists(), (
            f"Reference file not found: {ref_file}. "
            "Skill references pricing-strategy-framework.md but file is missing."
        )

    def test_break_even_analysis_exists(self, references_dir):
        """break-even-analysis.md must exist as referenced by skill."""
        ref_file = references_dir / "break-even-analysis.md"
        assert ref_file.exists(), (
            f"Reference file not found: {ref_file}. "
            "Skill references break-even-analysis.md but file is missing."
        )

    def test_skill_references_pricing_strategy(self, skill_content):
        """Skill must contain a reference to pricing-strategy-framework.md."""
        assert "pricing-strategy-framework.md" in skill_content, (
            "Skill does not reference pricing-strategy-framework.md. "
            "Phase 2 (Pricing Strategy) requires this reference."
        )

    def test_skill_references_break_even_analysis(self, skill_content):
        """Skill must contain a reference to break-even-analysis.md."""
        assert "break-even-analysis.md" in skill_content, (
            "Skill does not reference break-even-analysis.md. "
            "Phase 5 (Break-Even Analysis) requires this reference."
        )


# ---------------------------------------------------------------------------
# Integration Point 4: Cross-File Consistency
# ---------------------------------------------------------------------------


class TestCrossFileConsistency:
    """Verify naming and disclaimer consistency across all three files."""

    def test_disclaimer_in_subagent(self, subagent_content):
        """Subagent must contain the mandatory disclaimer text."""
        assert re.search(
            r'(?i)not\s+financial\s+advice', subagent_content
        ), (
            "Subagent missing 'not financial advice' disclaimer. "
            "BR-001 requires disclaimer on all outputs."
        )

    def test_skill_references_disclaimer_requirement(self, skill_content):
        """Skill success criteria must reference the disclaimer requirement."""
        assert re.search(
            r'(?i)not\s+financial\s+advice.*disclaimer', skill_content
        ), (
            "Skill does not reference 'not financial advice' disclaimer "
            "in success criteria. Cross-file consistency violation."
        )

    def test_consistent_command_name_across_files(
        self, command_content, skill_content
    ):
        """The command name 'financial-model' must appear consistently."""
        assert "financial-model" in command_content, (
            "Command file does not contain 'financial-model' name."
        )
        # Skill should reference the command or the command's purpose
        assert re.search(
            r'(?i)financial', skill_content
        ), (
            "Skill does not reference financial modeling capability."
        )

    def test_subagent_name_consistent_with_skill_reference(
        self, skill_content, subagent_content
    ):
        """The subagent name used in the skill must match the subagent's
        own name declaration."""
        # Extract name from subagent frontmatter
        fm_match = re.search(
            r'^---\s*\n(.*?)\n---', subagent_content, re.DOTALL
        )
        assert fm_match, "Subagent missing YAML frontmatter."
        name_match = re.search(r'name:\s*(\S+)', fm_match.group(1))
        assert name_match, "Subagent frontmatter missing 'name' field."
        subagent_name = name_match.group(1)

        assert subagent_name in skill_content, (
            f"Skill does not reference subagent by its declared name "
            f"'{subagent_name}'. Naming inconsistency."
        )


# ---------------------------------------------------------------------------
# Integration Point 5: End-to-End Workflow Chain
# ---------------------------------------------------------------------------


class TestEndToEndWorkflowChain:
    """Verify the full command -> skill -> subagent chain is properly linked."""

    def test_full_chain_command_to_skill_to_subagent(
        self, command_content, skill_content, subagent_content
    ):
        """Verify the complete delegation chain:
        command -> skill (via Skill() call) -> subagent (via reference).
        All three files must exist and be linked."""
        # Step 1: Command invokes skill
        assert re.search(
            r'Skill\(command="managing-finances"', command_content
        ), "Chain broken at command->skill: no Skill() invocation found."

        # Step 2: Skill references subagent
        assert "financial-modeler" in skill_content, (
            "Chain broken at skill->subagent: skill does not reference "
            "financial-modeler subagent."
        )

        # Step 3: Subagent declares its constrained role
        assert re.search(
            r'(?i)subagent', subagent_content
        ), (
            "Chain broken: subagent file does not identify itself as a subagent."
        )

    def test_command_does_not_bypass_skill(self, command_content):
        """Command must not directly reference the subagent, bypassing skill."""
        # Command should delegate to skill, not directly to subagent
        has_direct_subagent = re.search(
            r'(?i)Agent\s*\(\s*subagent_type\s*=\s*["\']financial-modeler',
            command_content,
        )
        assert not has_direct_subagent, (
            "Command directly invokes financial-modeler subagent, "
            "bypassing the managing-finances skill. Violates thin delegator pattern."
        )

    def test_skill_workflow_covers_required_phases(self, skill_content):
        """Skill must cover the key workflow phases for a complete
        financial model: context discovery, pricing, revenue, summary."""
        required_concepts = [
            ("context", r'(?i)context\s+discovery|financial\s+context'),
            ("pricing", r'(?i)pricing\s+strategy'),
            ("revenue", r'(?i)revenue\s+projection'),
            ("summary", r'(?i)financial\s+summary'),
        ]
        for concept_name, pattern in required_concepts:
            assert re.search(pattern, skill_content), (
                f"Skill missing required workflow phase: {concept_name}. "
                "End-to-end workflow incomplete."
            )

    def test_all_three_files_have_yaml_frontmatter(
        self, command_content, skill_content, subagent_content
    ):
        """All three component files must have valid YAML frontmatter,
        ensuring they are properly parseable by the framework."""
        for name, content in [
            ("command", command_content),
            ("skill", skill_content),
            ("subagent", subagent_content),
        ]:
            assert content.strip().startswith("---"), (
                f"{name} file missing YAML frontmatter. "
                "Framework requires frontmatter for all component files."
            )
            # Must have closing ---
            parts = content.split("---")
            assert len(parts) >= 3, (
                f"{name} file has malformed YAML frontmatter "
                "(missing closing ---)."
            )
