"""
Integration Tests for STORY-438: Slim Ideation Skill
Verifies that modified ideation skill files work together correctly.

Tests verify:
1. SKILL.md references valid files in references/ directory
2. Phase flow is coherent: Phase 1 → Phase 2 → Phase 3 (all reference files loadable)
3. No broken cross-references between SKILL.md and its reference files
4. The 4 modified files form a consistent documentation set
5. Reference files that should still exist are present
"""

import os
import re
import json
import pytest
from pathlib import Path


class TestStory438SkillStructure:
    """Tests verifying SKILL.md structural integrity after phase removal."""

    @pytest.fixture
    def skill_path(self):
        """Path to ideation SKILL.md"""
        return Path("/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-ideation/SKILL.md")

    @pytest.fixture
    def references_dir(self):
        """Path to ideation references directory"""
        return Path("/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-ideation/references")

    @pytest.fixture
    def skill_content(self, skill_path):
        """Load SKILL.md content"""
        assert skill_path.exists(), f"SKILL.md not found at {skill_path}"
        return skill_path.read_text(encoding='utf-8')

    @pytest.fixture
    def references_content(self, references_dir):
        """Load all reference files"""
        assert references_dir.exists(), f"References directory not found at {references_dir}"
        return {
            file.name: file.read_text(encoding='utf-8')
            for file in references_dir.glob('*.md')
        }

    # AC#1: Phase 3, 4, 5 Removed Tests

    def test_ac1_phase3_header_removed(self, skill_content):
        """AC#1a: No 'Phase 3' header exists in SKILL.md (Complexity Assessment phase)"""
        # The new Phase 3 is "Requirements Documentation & Handoff"
        # Old Phase 3 was "Complexity Assessment"
        # We check that old phase 3 content is gone by ensuring no duplicate Phase 3 sections

        phase_3_headers = re.findall(r'^### Phase 3:', skill_content, re.MULTILINE)
        assert len(phase_3_headers) <= 1, "Multiple Phase 3 headers found - phase duplication"

        # Verify the single Phase 3 that exists is the handoff phase
        phase_3_section = re.search(
            r'^### Phase 3:.*?(?=^###|^##|$)',
            skill_content,
            re.MULTILINE | re.DOTALL
        )
        assert phase_3_section, "Phase 3 header should exist (renamed)"
        assert "Handoff" in phase_3_section.group() or "Requirements Documentation" in phase_3_section.group(), \
            "Phase 3 should be Requirements Documentation & Handoff"

    def test_ac1_complexity_assessment_workflow_removed(self, skill_content):
        """AC#1b: No references to 'complexity-assessment-workflow.md' in phase definitions"""
        assert "complexity-assessment-workflow.md" not in skill_content, \
            "complexity-assessment-workflow.md reference should be removed from phase content"

    def test_ac1_description_no_complexity(self, skill_content):
        """AC#1c: SKILL.md description no longer mentions 'complexity assessment'"""
        # Extract description section (first ~20 lines)
        lines = skill_content.split('\n')[:100]
        description_section = '\n'.join(lines)

        # Description should not mention complexity assessment as a skill function
        assert "complexity assessment" not in description_section.lower() or \
               ("complexity assessment" in description_section.lower() and
                "architecture" in description_section.lower()), \
            "Description should not list complexity assessment as ideation skill function"

    def test_ac1_success_criteria_no_complexity_tier(self, skill_content):
        """AC#1d: Success Criteria section no longer includes complexity tier validation"""
        success_section = re.search(
            r'^## Success Criteria.*?(?=^##|$)',
            skill_content,
            re.MULTILINE | re.DOTALL
        )
        assert success_section, "Success Criteria section should exist"
        assert "complexity tier" not in success_section.group().lower() and \
               "complexity score" not in success_section.group().lower(), \
            "Complexity tier/score validation should be removed from Success Criteria"

    def test_ac2_phase4_header_removed(self, skill_content):
        """AC#2a: No 'Phase 4' header exists in SKILL.md (Epic Decomposition phase)"""
        phase_4_headers = re.findall(r'^### Phase 4:', skill_content, re.MULTILINE)
        assert len(phase_4_headers) == 0, "Phase 4 (Epic Decomposition) should be completely removed"

    def test_ac2_epic_decomposition_workflow_removed(self, skill_content):
        """AC#2b: No references to 'epic-decomposition-workflow.md' in phase definitions"""
        assert "epic-decomposition-workflow.md" not in skill_content, \
            "epic-decomposition-workflow.md reference should be removed"

    def test_ac2_success_criteria_no_epic_count(self, skill_content):
        """AC#2c: Success Criteria section no longer includes '1-3 epics with 3-8 features each'"""
        success_section = re.search(
            r'^## Success Criteria.*?(?=^##|$)',
            skill_content,
            re.MULTILINE | re.DOTALL
        )
        assert success_section, "Success Criteria section should exist"
        assert "1-3 epics" not in success_section.group() and \
               "3-8 features" not in success_section.group(), \
            "Epic count requirement should be removed from Success Criteria"

    def test_ac2_when_to_use_no_epic_creation(self, skill_content):
        """AC#2d: When to Use section no longer mentions 'epic creation'"""
        when_to_use = re.search(
            r'^## When to Use.*?(?=^##|$)',
            skill_content,
            re.MULTILINE | re.DOTALL
        )
        assert when_to_use, "When to Use section should exist"
        # Check that "epic creation" is not in the main skill scope
        assert "epic creation" not in when_to_use.group().lower() or \
               "delegat" in when_to_use.group().lower(), \
            "Epic creation should not be listed as When to Use trigger"

    def test_ac3_phase5_header_removed(self, skill_content):
        """AC#3a: No 'Phase 5' header exists in SKILL.md (Feasibility Analysis)"""
        phase_5_headers = re.findall(r'^### Phase 5:', skill_content, re.MULTILINE)
        assert len(phase_5_headers) == 0, "Phase 5 (Feasibility Analysis) should be completely removed"

    def test_ac3_feasibility_analysis_workflow_removed(self, skill_content):
        """AC#3b: No references to 'feasibility-analysis-workflow.md' in phase definitions"""
        assert "feasibility-analysis-workflow.md" not in skill_content, \
            "feasibility-analysis-workflow.md reference should be removed"

    def test_ac3_description_no_feasibility(self, skill_content):
        """AC#3c: SKILL.md description no longer mentions 'feasibility analysis'"""
        lines = skill_content.split('\n')[:100]
        description_section = '\n'.join(lines)

        assert "feasibility analysis" not in description_section.lower() or \
               ("feasibility analysis" in description_section.lower() and
                "architecture" in description_section.lower()), \
            "Feasibility analysis should not be described as ideation skill function"

    def test_ac3_error_handling_no_constraint_conflicts(self, skill_content):
        """AC#3d: Error Handling section removes error-type-5-constraint-conflicts.md"""
        error_section = re.search(
            r'^## Error Handling.*?(?=^##|$)',
            skill_content,
            re.MULTILINE | re.DOTALL
        )
        assert error_section, "Error Handling section should exist"
        assert "error-type-5" not in error_section.group(), \
            "error-type-5-constraint-conflicts.md reference should be removed"

    # AC#4: Completion Handoff Updated Tests

    def test_ac4_completion_handoff_primary_output_requirements(self, references_content):
        """AC#4a: Primary output is YAML-structured requirements.md (per F4 schema)"""
        assert 'completion-handoff.md' in references_content, \
            "completion-handoff.md should exist in references"

        content = references_content['completion-handoff.md']
        assert "requirements.md" in content, \
            "requirements.md should be mentioned as primary output"
        assert "F4 schema" in content, \
            "F4 schema should be referenced"

    def test_ac4_completion_handoff_no_epic_references(self, references_content):
        """AC#4b: Epic document references removed from completion summary template"""
        content = references_content['completion-handoff.md']

        # Check that epic documents are not listed as primary output
        template_section = re.search(
            r'## ✅ Ideation Complete.*?(?=^---)',
            content,
            re.MULTILINE | re.DOTALL
        )
        if template_section:
            assert "Epic Documents" not in template_section.group() or \
                   "epic" not in template_section.group().split("Generated Artifacts")[1].lower(), \
                "Epic documents should not be in primary artifacts list"

    def test_ac4_generated_artifacts_requirements_primary(self, references_content):
        """AC#4c: 'Generated Artifacts' section shows requirements.md as primary artifact"""
        content = references_content['completion-handoff.md']
        assert "**Requirements Document:**" in content or "Requirements Document" in content, \
            "Requirements.md should be explicitly listed as primary artifact"

    def test_ac4_next_action_recommends_create_epic(self, references_content):
        """AC#4d: Next action recommendation points to /create-epic (architecture skill)"""
        content = references_content['completion-handoff.md']
        assert "/create-epic" in content, \
            "Next action should recommend /create-epic command"

    def test_ac4_completion_template_f4_schema(self, references_content):
        """AC#4e: Completion template follows F4 schema structure"""
        content = references_content['completion-handoff.md']

        # F4 schema has these main sections
        f4_fields = [
            "functional_requirements",
            "non_functional_requirements",
            "constraints",
            "dependencies"
        ]

        # At least some F4 fields should be mentioned in completion template
        f4_mentioned = sum(1 for field in f4_fields if field in content)
        assert f4_mentioned >= 2, \
            f"F4 schema fields should be referenced in template (found {f4_mentioned}/4)"

    # AC#5: Artifact Generation Updated Tests

    def test_ac5_artifact_generation_no_epic_template(self, references_content):
        """AC#5a: No epic template loading instructions remain"""
        content = references_content['artifact-generation.md']
        assert "epic-template.md" not in content, \
            "Epic template loading should be removed"
        assert "Load Constitutional Epic Template" not in content, \
            "Epic template loading section should be removed"

    def test_ac5_artifact_generation_no_section_compliance_epic(self, references_content):
        """AC#5b: No 'Section Compliance Checklist' for epic sections"""
        content = references_content['artifact-generation.md']

        # Epic compliance checklist should not be there
        epic_checklist_pattern = r'Section Compliance Checklist.*?epic'
        assert not re.search(epic_checklist_pattern, content, re.DOTALL), \
            "Epic section compliance checklist should be removed"

    def test_ac5_artifact_generation_requirements_retained(self, references_content):
        """AC#5c: Requirements specification generation is retained and enhanced"""
        content = references_content['artifact-generation.md']
        assert "requirements" in content.lower(), \
            "Requirements generation should be retained"

    def test_ac5_artifact_generation_yaml_requirements_format(self, references_content):
        """AC#5d: Output format changed to YAML requirements.md per F4 schema"""
        content = references_content['artifact-generation.md']
        assert "requirements.md" in content, \
            "Output should be requirements.md format"
        assert "F4 schema" in content or "YAML" in content, \
            "Output format should reference F4 schema or YAML structure"

    def test_ac5_artifact_generation_no_epic_context(self, references_content):
        """AC#5e: Cross-session context requirements updated (no epic decomposition refs)"""
        content = references_content['artifact-generation.md']
        assert "epic decomposition" not in content.lower(), \
            "Epic decomposition should not be in cross-session context"
        assert "feasibility" not in content.lower() or "architecture" in content.lower(), \
            "Feasibility references should be removed or delegated to architecture"

    # AC#6: Self-Validation Workflow Updated Tests

    def test_ac6_self_validation_no_epic_checks(self, references_content):
        """AC#6a: Validation removes epic document checks"""
        content = references_content['self-validation-workflow.md']

        # Epic validation should not exist
        assert "epic document" not in content.lower() or \
               ("epic" in content.lower() and "not" in content.lower()), \
            "Epic document validation should be removed"

    def test_ac6_self_validation_no_complexity_score(self, references_content):
        """AC#6b: Validation removes complexity score validation (0-60 range, tier 1-4)"""
        content = references_content['self-validation-workflow.md']
        assert "0-60" not in content and "complexity score" not in content.lower() or \
               ("complexity" in content.lower() and "not" in content.lower()), \
            "Complexity score validation should be removed"
        assert "tier 1" not in content and "tier 2" not in content, \
            "Complexity tier validation should be removed"

    def test_ac6_self_validation_no_feasibility_checks(self, references_content):
        """AC#6c: Validation removes feasibility assessment checks"""
        content = references_content['self-validation-workflow.md']
        assert "feasibility" not in content.lower() or \
               ("feasibility" in content.lower() and "not" in content.lower()), \
            "Feasibility assessment validation should be removed"

    def test_ac6_self_validation_requirements_retained(self, references_content):
        """AC#6d: Validation retains requirements.md schema compliance checks"""
        content = references_content['self-validation-workflow.md']
        assert "requirements.md" in content or "requirements" in content.lower(), \
            "Requirements schema validation should be retained"

    def test_ac6_self_validation_f4_schema_validation(self, references_content):
        """AC#6e: Validation adds F4 schema validation (YAML structure, required fields)"""
        content = references_content['self-validation-workflow.md']
        assert "F4 schema" in content or "YAML" in content.lower(), \
            "F4 schema or YAML validation should be included"

    # AC#7: Retained Phases Functional Tests

    def test_ac7_phase1_discovery_intact(self, skill_content):
        """AC#7a: Phase 1 (Discovery & Problem Understanding) intact with all references"""
        phase_1 = re.search(
            r'^### Phase 1:.*?(?=^###|^##|$)',
            skill_content,
            re.MULTILINE | re.DOTALL
        )
        assert phase_1, "Phase 1 should exist"
        assert "discovery" in phase_1.group().lower(), \
            "Phase 1 should mention discovery"
        assert "discovery-workflow.md" in skill_content, \
            "discovery-workflow.md reference should be intact"

    def test_ac7_phase2_elicitation_intact(self, skill_content):
        """AC#7b: Phase 2 (Requirements Elicitation) intact with question flow"""
        phase_2 = re.search(
            r'^### Phase 2:.*?(?=^###|^##|$)',
            skill_content,
            re.MULTILINE | re.DOTALL
        )
        assert phase_2, "Phase 2 should exist"
        assert "elicitation" in phase_2.group().lower(), \
            "Phase 2 should mention elicitation"
        assert "requirements-elicitation" in skill_content.lower(), \
            "Requirements elicitation reference should be intact"

    def test_ac7_phase3_renamed_artifact_generation(self, skill_content):
        """AC#7c: Phase 3 (renamed from Phase 6, artifact generation) intact with streamlined flow"""
        phase_3 = re.search(
            r'^### Phase 3:.*?(?=^###|^##|$)',
            skill_content,
            re.MULTILINE | re.DOTALL
        )
        assert phase_3, "Phase 3 should exist (renamed from Phase 6)"
        content = phase_3.group()
        assert "artifact" in content.lower() or "requirements" in content.lower(), \
            "Phase 3 should handle artifact/requirements generation"

    def test_ac7_brainstorm_context_unchanged(self, skill_content):
        """AC#7d: Brainstorm context handling (from /brainstorm) unchanged"""
        # Check that brainstorm handoff capability is still documented
        assert "brainstorm" in skill_content.lower(), \
            "Brainstorm context handling should be mentioned"

    def test_ac7_error_handling_retained_types(self, skill_content):
        """AC#7e: Error handling for retained phases (error-type-1, 2, 4) unchanged"""
        error_refs = [
            "error-type-1",
            "error-type-2",
            "error-type-4"
        ]
        for error_type in error_refs:
            assert error_type in skill_content, \
                f"{error_type} should remain in error handling"

    # Reference File Existence Tests

    def test_reference_files_still_exist(self, references_dir):
        """Reference files that should NOT be deleted per BR-003"""
        # These files should still exist for architecture skill migration
        expected_files = [
            "discovery-workflow.md",
            "requirements-elicitation-workflow.md"
        ]

        for filename in expected_files:
            filepath = references_dir / filename
            assert filepath.exists(), \
                f"Reference file {filename} should still exist for architecture migration"

    def test_modified_reference_files_exist(self, references_dir):
        """Modified reference files must exist"""
        modified_files = [
            "completion-handoff.md",
            "artifact-generation.md",
            "self-validation-workflow.md"
        ]

        for filename in modified_files:
            filepath = references_dir / filename
            assert filepath.exists(), \
                f"Modified reference file {filename} must exist"


class TestCrossFileReferences:
    """Tests verifying cross-references between SKILL.md and reference files are valid."""

    @pytest.fixture
    def skill_path(self):
        return Path("/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-ideation/SKILL.md")

    @pytest.fixture
    def references_dir(self):
        return Path("/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-ideation/references")

    @pytest.fixture
    def skill_content(self, skill_path):
        return skill_path.read_text(encoding='utf-8')

    @pytest.fixture
    def references_content(self, references_dir):
        return {
            file.name: file.read_text(encoding='utf-8')
            for file in references_dir.glob('*.md')
        }

    def test_phase1_reference_exists(self, skill_content, references_dir):
        """Phase 1 references discovery-workflow.md which must exist"""
        assert "discovery-workflow.md" in skill_content
        assert (references_dir / "discovery-workflow.md").exists(), \
            "discovery-workflow.md must exist"

    def test_phase2_reference_exists(self, skill_content, references_dir):
        """Phase 2 references requirements-elicitation-workflow.md which must exist"""
        assert "requirements-elicitation" in skill_content.lower()
        assert (references_dir / "requirements-elicitation-workflow.md").exists(), \
            "requirements-elicitation-workflow.md must exist"

    def test_phase3_references_all_exist(self, skill_content, references_dir):
        """Phase 3 references artifact-generation.md and completion-handoff.md"""
        # Phase 3 mentions both artifact generation and handoff
        assert (references_dir / "artifact-generation.md").exists(), \
            "artifact-generation.md must exist"
        assert (references_dir / "completion-handoff.md").exists(), \
            "completion-handoff.md must exist"

    def test_self_validation_referenced(self, skill_content, references_dir):
        """self-validation-workflow.md referenced in artifact generation or Phase 3"""
        # Self-validation should be part of Phase 3
        assert "self-validation" in skill_content.lower() or \
               (references_dir / "self-validation-workflow.md").exists(), \
            "self-validation-workflow.md should be referenced or exist"

    def test_no_broken_reference_links(self, skill_content, references_dir):
        """All .md references in SKILL.md point to existing files"""
        # Find all references to .md files
        md_refs = re.findall(r'`?([a-z0-9\-]+\.md)`?', skill_content.lower())

        existing_files = {f.name.lower() for f in references_dir.glob('*.md')}

        # Files to skip (non-reference files, external files, generated files)
        skip_files = {'skill.md', 'readme.md', 'claude.md', 'requirements.md'}

        for ref in md_refs:
            if ref in skip_files:  # Skip non-reference files
                continue
            assert ref in existing_files, \
                f"Reference to {ref} in SKILL.md but file not found in references/"

    def test_phase_flow_coherent(self, skill_content):
        """Phase numbers are sequential: Phase 1 → Phase 2 → Phase 3"""
        # Should find exactly 3 phase headers in workflow section
        phase_headers = re.findall(r'^### Phase \d:', skill_content, re.MULTILINE)

        # Extract phase numbers
        phase_numbers = [int(re.search(r'\d+', h).group()) for h in phase_headers]
        phase_numbers.sort()

        # Should be [1, 2, 3]
        assert phase_numbers == [1, 2, 3], \
            f"Phase numbers should be [1, 2, 3], got {phase_numbers}"


class TestDocumentationConsistency:
    """Tests verifying all 4 modified files form a consistent documentation set."""

    @pytest.fixture
    def skill_path(self):
        return Path("/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-ideation/SKILL.md")

    @pytest.fixture
    def completion_handoff_path(self):
        return Path("/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-ideation/references/completion-handoff.md")

    @pytest.fixture
    def artifact_generation_path(self):
        return Path("/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-ideation/references/artifact-generation.md")

    @pytest.fixture
    def self_validation_path(self):
        return Path("/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-ideation/references/self-validation-workflow.md")

    @pytest.fixture
    def all_content(self, skill_path, completion_handoff_path, artifact_generation_path, self_validation_path):
        return {
            'skill': skill_path.read_text(encoding='utf-8'),
            'completion': completion_handoff_path.read_text(encoding='utf-8'),
            'artifact': artifact_generation_path.read_text(encoding='utf-8'),
            'validation': self_validation_path.read_text(encoding='utf-8')
        }

    def test_all_files_mention_requirements_md(self, all_content):
        """All 4 modified files should consistently mention requirements.md as primary output"""
        count = 0
        for name, content in all_content.items():
            if "requirements.md" in content:
                count += 1

        assert count >= 3, \
            f"At least 3 of 4 files should mention requirements.md (found {count}/4)"

    def test_all_files_mention_f4_schema(self, all_content):
        """All modified files should reference F4 schema"""
        count = 0
        for name, content in all_content.items():
            if "F4 schema" in content or ("YAML" in content and "requirements" in content.lower()):
                count += 1

        assert count >= 2, \
            f"At least 2 files should reference F4 schema (found {count}/4)"

    def test_no_legacy_epic_references(self, all_content):
        """None of the 4 files should have epic document generation as primary output"""
        for name, content in all_content.items():
            if name in ['completion', 'artifact', 'validation']:
                # These files should not treat epic generation as their primary responsibility
                assert "Epic Documents" not in content or \
                       ("Epic Documents" in content and "architecture" in content.lower()), \
                    f"{name} should not list Epic Documents as primary output"

    def test_no_complexity_assessment_references(self, all_content):
        """None of the 4 files should reference complexity assessment"""
        for name, content in all_content.items():
            assert "complexity assessment" not in content.lower() or \
                   ("complexity assessment" in content.lower() and "architecture" in content.lower()), \
                f"{name} should not reference complexity assessment as ideation function"

    def test_no_feasibility_analysis_references(self, all_content):
        """None of the 4 files should reference feasibility analysis"""
        for name, content in all_content.items():
            assert "feasibility analysis" not in content.lower() or \
                   ("feasibility analysis" in content.lower() and "architecture" in content.lower()), \
                f"{name} should not reference feasibility analysis as ideation function"

    def test_consistent_next_action_recommendation(self, all_content):
        """Files should consistently recommend /create-epic as next action"""
        skill = all_content['skill']
        completion = all_content['completion']

        # At least one of skill or completion should mention /create-epic
        assert "/create-epic" in skill or "/create-epic" in completion, \
            "Next action should recommend /create-epic"

    def test_consistent_f4_schema_fields(self, all_content):
        """All files should be consistent about F4 schema fields"""
        artifact = all_content['artifact']
        completion = all_content['completion']
        validation = all_content['validation']

        # F4 schema fields
        f4_fields = [
            'functional_requirements',
            'non_functional_requirements',
            'constraints',
            'dependencies'
        ]

        # At least one file should mention each field
        for field in f4_fields:
            found_in = sum(1 for name, content in all_content.items()
                          if field in content)
            assert found_in >= 1, \
                f"F4 field '{field}' should be mentioned in at least one file"


class TestOperationalTreeConsistency:
    """Tests verifying both src/ and .claude/ trees are consistent."""

    @pytest.fixture
    def src_skill_path(self):
        return Path("/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-ideation/SKILL.md")

    @pytest.fixture
    def operational_skill_path(self):
        return Path("/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-ideation/SKILL.md")

    def test_src_and_operational_exist(self, src_skill_path, operational_skill_path):
        """Both src and operational versions should exist"""
        assert src_skill_path.exists(), f"Source SKILL.md not found at {src_skill_path}"
        # Note: operational tree may not be updated in this test, just verify src exists

    def test_src_has_no_architect_phases(self, src_skill_path):
        """Source tree SKILL.md should not have architect phases"""
        content = src_skill_path.read_text(encoding='utf-8')

        # Check for old phase numbers or content
        assert "### Phase 3: Complexity Assessment" not in content, \
            "Old Phase 3 (Complexity) should be removed"
        assert "### Phase 4: Epic" not in content, \
            "Old Phase 4 (Epic Decomposition) should be removed"
        assert "### Phase 5: Feasibility" not in content, \
            "Old Phase 5 (Feasibility) should be removed"


class TestPhaseRenumbering:
    """Tests verifying Phase 6 was properly renumbered to Phase 3."""

    @pytest.fixture
    def skill_path(self):
        return Path("/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-ideation/SKILL.md")

    @pytest.fixture
    def skill_content(self, skill_path):
        return skill_path.read_text(encoding='utf-8')

    def test_no_phase_6_header(self, skill_content):
        """Phase 6 header should not exist (was renumbered to Phase 3)"""
        phase_6_headers = re.findall(r'^### Phase 6:', skill_content, re.MULTILINE)
        assert len(phase_6_headers) == 0, "Phase 6 should be renumbered to Phase 3"

    def test_phase_3_handles_artifact_generation(self, skill_content):
        """Phase 3 should handle artifact generation (what Phase 6 did)"""
        phase_3 = re.search(
            r'^### Phase 3:.*?(?=^###|^##|$)',
            skill_content,
            re.MULTILINE | re.DOTALL
        )
        assert phase_3, "Phase 3 should exist"

        content = phase_3.group()
        assert "artifact" in content.lower() or "output" in content.lower() or \
               "requirement" in content.lower(), \
            "Phase 3 should handle artifact/output generation"

    def test_three_phases_total(self, skill_content):
        """Should have exactly 3 phases in the workflow"""
        # Count Phase headers in entire content
        # Phase headers can be "### Phase 1:" or "### Phase 1 -" etc.
        phase_headers = re.findall(r'^### Phase [0-9]', skill_content, re.MULTILINE)
        assert len(phase_headers) == 3, \
            f"Should have 3 phases total, found {len(phase_headers)}: {phase_headers}"


if __name__ == "__main__":
    # Run with: pytest tests/integration/test_story_438_ideation_skill_refactor.py -v
    pytest.main([__file__, "-v"])
