"""
Integration tests for STORY-467: Cross-file consistency validation.

Verifies that SKILL.md and business-coach.md reference the same persona definitions,
that referenced files exist, and that source-tree.md compliance is maintained.
"""

import pytest
import os
import yaml
from pathlib import Path


class TestSkillAndAgentFileLocations:
    """Verify both files exist at correct source-tree.md paths."""

    def test_skill_file_at_src_path(self):
        """SKILL.md must exist at src/claude/skills/coaching-entrepreneur/SKILL.md"""
        skill_path = Path("src/claude/skills/coaching-entrepreneur/SKILL.md")
        assert skill_path.exists(), f"Skill file not found at {skill_path}"
        assert skill_path.is_file(), f"{skill_path} is not a regular file"

    def test_subagent_file_at_src_path(self):
        """business-coach.md must exist at src/claude/agents/business-coach.md"""
        agent_path = Path("src/claude/agents/business-coach.md")
        assert agent_path.exists(), f"Agent file not found at {agent_path}"
        assert agent_path.is_file(), f"{agent_path} is not a regular file"

    def test_skill_references_directory_exists(self):
        """references/ directory must exist under coaching-entrepreneur skill"""
        ref_dir = Path("src/claude/skills/coaching-entrepreneur/references")
        assert ref_dir.exists(), f"References directory not found at {ref_dir}"
        assert ref_dir.is_dir(), f"{ref_dir} is not a directory"


class TestReferenceFileExistence:
    """Verify all referenced files exist."""

    def test_celebration_engine_reference_exists(self):
        """celebration-engine.md must exist in references/"""
        ref_file = Path("src/claude/skills/coaching-entrepreneur/references/celebration-engine.md")
        assert ref_file.exists(), f"celebration-engine.md not found at {ref_file}"

    def test_confidence_building_patterns_reference_exists(self):
        """confidence-building-patterns.md must exist in references/"""
        ref_file = Path("src/claude/skills/coaching-entrepreneur/references/confidence-building-patterns.md")
        assert ref_file.exists(), f"confidence-building-patterns.md not found at {ref_file}"

    def test_imposter_syndrome_interventions_reference_exists(self):
        """imposter-syndrome-interventions.md must exist in references/"""
        ref_file = Path("src/claude/skills/coaching-entrepreneur/references/imposter-syndrome-interventions.md")
        assert ref_file.exists(), f"imposter-syndrome-interventions.md not found at {ref_file}"

    def test_skill_references_in_metadata(self):
        """References section of SKILL.md must list all existing files"""
        skill_path = Path("src/claude/skills/coaching-entrepreneur/SKILL.md")
        content = skill_path.read_text()

        # Extract references section
        references_start = content.find("## References")
        assert references_start != -1, "## References section not found in SKILL.md"

        references_section = content[references_start:]

        # Verify all reference files are mentioned
        assert "celebration-engine.md" in references_section, \
            "celebration-engine.md not mentioned in References section"
        assert "confidence-building-patterns.md" in references_section, \
            "confidence-building-patterns.md not mentioned in References section"
        assert "imposter-syndrome-interventions.md" in references_section, \
            "imposter-syndrome-interventions.md not mentioned in References section"


class TestPersonaDefinitionConsistency:
    """Verify Coach and Consultant persona definitions are consistent between files."""

    def test_skill_defines_coach_mode(self):
        """SKILL.md must have a Coach Mode section"""
        skill_path = Path("src/claude/skills/coaching-entrepreneur/SKILL.md")
        content = skill_path.read_text()
        assert "### Coach Mode" in content, "Coach Mode section missing from SKILL.md"

    def test_skill_defines_consultant_mode(self):
        """SKILL.md must have a Consultant Mode section"""
        skill_path = Path("src/claude/skills/coaching-entrepreneur/SKILL.md")
        content = skill_path.read_text()
        assert "### Consultant Mode" in content, "Consultant Mode section missing from SKILL.md"

    def test_agent_references_skill_persona_definitions(self):
        """business-coach.md must reference coaching-entrepreneur SKILL.md for persona details"""
        agent_path = Path("src/claude/agents/business-coach.md")
        content = agent_path.read_text()

        # Verify reference to SKILL.md
        assert "coaching-entrepreneur SKILL.md" in content or "coaching-entrepreneur skill" in content, \
            "business-coach.md does not reference coaching-entrepreneur skill"

        # Verify persona mode references
        assert "Coach mode" in content, "Coach mode not mentioned in business-coach.md"
        assert "Consultant mode" in content, "Consultant mode not mentioned in business-coach.md"

    def test_agent_coach_mode_characteristics_align_with_skill(self):
        """business-coach.md Coach mode description must align with SKILL.md"""
        skill_path = Path("src/claude/skills/coaching-entrepreneur/SKILL.md")
        agent_path = Path("src/claude/agents/business-coach.md")

        skill_content = skill_path.read_text()
        agent_content = agent_path.read_text()

        # Extract Coach mode section from SKILL.md
        coach_start = skill_content.find("### Coach Mode")
        coach_end = skill_content.find("### Consultant Mode")
        skill_coach_section = skill_content[coach_start:coach_end]

        # Key Coach characteristics that should be referenced
        coach_keywords = ["empathetic", "encouraging", "celebrates", "self-doubt"]
        agent_coach_mentions = 0

        for keyword in coach_keywords:
            if keyword.lower() in agent_content.lower():
                agent_coach_mentions += 1

        assert agent_coach_mentions >= 2, \
            f"business-coach.md does not adequately reference Coach mode characteristics. " \
            f"Only {agent_coach_mentions}/4 key characteristics mentioned"

    def test_agent_consultant_mode_characteristics_align_with_skill(self):
        """business-coach.md Consultant mode description must align with SKILL.md"""
        skill_path = Path("src/claude/skills/coaching-entrepreneur/SKILL.md")
        agent_path = Path("src/claude/agents/business-coach.md")

        skill_content = skill_path.read_text()
        agent_content = agent_path.read_text()

        # Key Consultant characteristics
        consultant_keywords = ["structured", "deliverable", "professional", "analytical"]
        agent_consultant_mentions = 0

        for keyword in consultant_keywords:
            if keyword.lower() in agent_content.lower():
                agent_consultant_mentions += 1

        assert agent_consultant_mentions >= 2, \
            f"business-coach.md does not adequately reference Consultant mode characteristics. " \
            f"Only {agent_consultant_mentions}/4 key characteristics mentioned"


class TestPersonaBlendTransitionIndicators:
    """Verify both files document when to shift between personas."""

    def test_skill_has_transition_indicators_table(self):
        """SKILL.md must have transition indicators documentation"""
        skill_path = Path("src/claude/skills/coaching-entrepreneur/SKILL.md")
        content = skill_path.read_text()

        assert "Transition Indicators" in content or "transition" in content.lower(), \
            "Transition indicators section missing from SKILL.md"

    def test_agent_has_confidence_detection_decision_tree(self):
        """business-coach.md must have confidence detection decision tree"""
        agent_path = Path("src/claude/agents/business-coach.md")
        content = agent_path.read_text()

        assert "decision tree" in content.lower() or "confidence detection" in content.lower(), \
            "Confidence detection decision tree missing from business-coach.md"

    def test_agent_confidence_triggers_match_skill_indicators(self):
        """business-coach.md confidence triggers should align with SKILL.md persona indicators"""
        agent_path = Path("src/claude/agents/business-coach.md")
        content = agent_path.read_text()

        # Check for confidence-related language triggers
        triggers = [
            "Self-doubt",
            "Imposter Syndrome",
            "Avoidance",
            "Momentum"
        ]

        for trigger in triggers:
            assert trigger in content, f"Confidence trigger '{trigger}' not found in business-coach.md"


class TestProfileIntegration:
    """Verify both files handle user profile integration consistently."""

    def test_skill_reads_user_profile_at_session_start(self):
        """SKILL.md must document reading user-profile.yaml at session start"""
        skill_path = Path("src/claude/skills/coaching-entrepreneur/SKILL.md")
        content = skill_path.read_text()

        assert "user-profile.yaml" in content, "user-profile.yaml reference missing from SKILL.md"
        assert "Session Start" in content or "session start" in content.lower(), \
            "Session start instructions missing from SKILL.md"

    def test_skill_profile_is_read_only(self):
        """SKILL.md must explicitly state that user-profile.yaml is read-only"""
        skill_path = Path("src/claude/skills/coaching-entrepreneur/SKILL.md")
        content = skill_path.read_text()

        assert "read-only" in content.lower(), \
            "Read-only constraint on user-profile.yaml not documented in SKILL.md"

    def test_skill_has_fallback_when_profile_missing(self):
        """SKILL.md must document graceful fallback when profile is missing"""
        skill_path = Path("src/claude/skills/coaching-entrepreneur/SKILL.md")
        content = skill_path.read_text()

        assert "missing" in content.lower() or "unavailable" in content.lower() or "fallback" in content.lower(), \
            "Fallback behavior for missing profile not documented in SKILL.md"

    def test_skill_has_profile_dimensions_documented(self):
        """SKILL.md must document profile dimensions (celebration_intensity, progress_visualization)"""
        skill_path = Path("src/claude/skills/coaching-entrepreneur/SKILL.md")
        content = skill_path.read_text()

        assert "celebration_intensity" in content, "celebration_intensity dimension not documented"
        assert "progress_visualization" in content, "progress_visualization dimension not documented"


class TestYamlFrontmatterConsistency:
    """Verify YAML frontmatter is valid and consistent between files."""

    def test_skill_frontmatter_is_valid_yaml(self):
        """SKILL.md frontmatter must be valid YAML"""
        skill_path = Path("src/claude/skills/coaching-entrepreneur/SKILL.md")
        content = skill_path.read_text()

        # Extract frontmatter
        parts = content.split("---")
        assert len(parts) >= 3, "SKILL.md frontmatter delimiters missing or invalid"

        frontmatter_text = parts[1]
        try:
            yaml.safe_load(frontmatter_text)
        except yaml.YAMLError as e:
            pytest.fail(f"SKILL.md frontmatter is not valid YAML: {e}")

    def test_agent_frontmatter_is_valid_yaml(self):
        """business-coach.md frontmatter must be valid YAML"""
        agent_path = Path("src/claude/agents/business-coach.md")
        content = agent_path.read_text()

        # Extract frontmatter
        parts = content.split("---")
        assert len(parts) >= 3, "business-coach.md frontmatter delimiters missing or invalid"

        frontmatter_text = parts[1]
        try:
            yaml.safe_load(frontmatter_text)
        except yaml.YAMLError as e:
            pytest.fail(f"business-coach.md frontmatter is not valid YAML: {e}")

    def test_skill_name_matches_directory(self):
        """SKILL.md name field must match 'coaching-entrepreneur'"""
        skill_path = Path("src/claude/skills/coaching-entrepreneur/SKILL.md")
        content = skill_path.read_text()

        parts = content.split("---")
        frontmatter_text = parts[1]
        frontmatter = yaml.safe_load(frontmatter_text)

        assert frontmatter.get("name") == "coaching-entrepreneur", \
            f"SKILL.md name field is '{frontmatter.get('name')}', expected 'coaching-entrepreneur'"

    def test_agent_name_is_business_coach(self):
        """business-coach.md name field must match 'business-coach'"""
        agent_path = Path("src/claude/agents/business-coach.md")
        content = agent_path.read_text()

        parts = content.split("---")
        frontmatter_text = parts[1]
        frontmatter = yaml.safe_load(frontmatter_text)

        assert frontmatter.get("name") == "business-coach", \
            f"business-coach.md name field is '{frontmatter.get('name')}', expected 'business-coach'"


class TestDocumentationCompletion:
    """Verify documentation completeness across both files."""

    def test_skill_documents_fallback_behavior(self):
        """SKILL.md must have Fallback Behavior section"""
        skill_path = Path("src/claude/skills/coaching-entrepreneur/SKILL.md")
        content = skill_path.read_text()

        assert "Fallback Behavior" in content, "Fallback Behavior section missing from SKILL.md"
        assert "Coach mode" in content, "Fallback to Coach mode not documented"

    def test_skill_documents_confidence_detection(self):
        """SKILL.md must have Confidence Detection section"""
        skill_path = Path("src/claude/skills/coaching-entrepreneur/SKILL.md")
        content = skill_path.read_text()

        assert "Confidence Detection" in content, "Confidence Detection section missing from SKILL.md"

    def test_agent_documents_confidence_detection_decision_tree(self):
        """business-coach.md must document confidence detection with decision tree"""
        agent_path = Path("src/claude/agents/business-coach.md")
        content = agent_path.read_text()

        assert "Confidence Detection" in content, "Confidence Detection section missing from business-coach.md"
        assert "Decision" in content or "decision" in content.lower(), \
            "Decision tree or decision-making logic not documented in business-coach.md"

    def test_agent_documents_reference_loading_instructions(self):
        """business-coach.md must document when and how to load reference files"""
        agent_path = Path("src/claude/agents/business-coach.md")
        content = agent_path.read_text()

        # Should reference loading reference files
        assert "Load" in content or "load" in content.lower(), \
            "Instructions for loading reference files missing from business-coach.md"
        assert "reference" in content.lower(), "Reference file loading not documented in business-coach.md"
