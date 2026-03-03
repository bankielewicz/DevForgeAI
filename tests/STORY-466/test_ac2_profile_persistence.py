"""
Test: AC#2 - Profile YAML Persistence
Story: STORY-466
Phase: TDD Red (tests must FAIL until implementation is complete)

Verifies:
- Profile output specification is documented in SKILL.md
- SKILL.md specifies the YAML schema with all 7 dimension fields
- SKILL.md specifies timestamps (created, last_calibrated) and schema_version
- Valid enum values are documented for all 7 dimensions
"""

import os
import re

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

SKILL_MD_PATH = os.path.join(
    PROJECT_ROOT, "src", "claude", "skills", "assessing-entrepreneur", "SKILL.md"
)

# All schema fields that must appear in the SKILL.md profile output specification
REQUIRED_SCHEMA_FIELDS = [
    "schema_version",
    "created",
    "last_calibrated",
    "task_chunk_size",
    "session_length",
    "check_in_frequency",
    "progress_visualization",
    "celebration_intensity",
    "reminder_style",
    "overwhelm_prevention",
]

# Enum values per dimension (must all appear in the specification)
DIMENSION_ENUMS = {
    "task_chunk_size": ["micro", "standard", "extended"],
    "session_length": ["short", "medium", "long"],
    "check_in_frequency": ["frequent", "moderate", "minimal"],
    "progress_visualization": ["per_task", "daily", "weekly"],
    "celebration_intensity": ["high", "medium", "low"],
    "reminder_style": ["specific", "balanced", "gentle"],
    "overwhelm_prevention": ["strict", "moderate", "open"],
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


# ---------------------------------------------------------------------------
# SKILL.md profile output specification tests
# ---------------------------------------------------------------------------


class TestSkillMdProfileOutputSpec:
    """AC#2: SKILL.md must document the user-profile.yaml output specification."""

    def test_skill_md_exists(self):
        """SKILL.md must exist at the src/ tree path."""
        assert os.path.isfile(SKILL_MD_PATH), (
            f"SKILL.md not found at expected path: {SKILL_MD_PATH}"
        )

    def test_skill_md_references_user_profile_yaml(self):
        """SKILL.md must reference 'user-profile.yaml' as the output file."""
        content = _read_file(SKILL_MD_PATH)
        assert "user-profile.yaml" in content, (
            "SKILL.md does not reference 'user-profile.yaml' output file"
        )

    def test_skill_md_documents_schema_version_field(self):
        """SKILL.md must document 'schema_version' field in profile schema."""
        content = _read_file(SKILL_MD_PATH)
        assert "schema_version" in content, (
            "SKILL.md missing 'schema_version' field in profile output specification"
        )

    def test_skill_md_documents_created_timestamp(self):
        """SKILL.md must document 'created' timestamp field."""
        content = _read_file(SKILL_MD_PATH)
        assert re.search(r"\bcreated\b", content), (
            "SKILL.md missing 'created' timestamp field in profile output specification"
        )

    def test_skill_md_documents_last_calibrated_timestamp(self):
        """SKILL.md must document 'last_calibrated' timestamp field."""
        content = _read_file(SKILL_MD_PATH)
        assert "last_calibrated" in content, (
            "SKILL.md missing 'last_calibrated' timestamp field in profile output specification"
        )

    def test_skill_md_documents_all_required_schema_fields(self):
        """SKILL.md must document all 10 required profile schema fields."""
        content = _read_file(SKILL_MD_PATH)
        missing = [field for field in REQUIRED_SCHEMA_FIELDS if field not in content]
        assert not missing, (
            f"SKILL.md profile output specification missing fields: {missing}"
        )

    def test_skill_md_documents_profile_output_path(self):
        """SKILL.md must specify the output path devforgeai/specs/business/user-profile.yaml."""
        content = _read_file(SKILL_MD_PATH)
        assert re.search(
            r"devforgeai/specs/business/user-profile\.yaml", content
        ), (
            "SKILL.md missing output path 'devforgeai/specs/business/user-profile.yaml'"
        )


class TestSkillMdDimensionEnumValues:
    """AC#2: SKILL.md must document valid enum values for all 7 dimensions."""

    def test_task_chunk_size_enums_documented(self):
        """task_chunk_size enums (micro|standard|extended) must appear in SKILL.md."""
        content = _read_file(SKILL_MD_PATH)
        for val in DIMENSION_ENUMS["task_chunk_size"]:
            assert val in content, (
                f"SKILL.md missing task_chunk_size enum value '{val}'"
            )

    def test_session_length_enums_documented(self):
        """session_length enums (short|medium|long) must appear in SKILL.md."""
        content = _read_file(SKILL_MD_PATH)
        for val in DIMENSION_ENUMS["session_length"]:
            assert val in content, (
                f"SKILL.md missing session_length enum value '{val}'"
            )

    def test_check_in_frequency_enums_documented(self):
        """check_in_frequency enums (frequent|moderate|minimal) must appear in SKILL.md."""
        content = _read_file(SKILL_MD_PATH)
        for val in DIMENSION_ENUMS["check_in_frequency"]:
            assert val in content, (
                f"SKILL.md missing check_in_frequency enum value '{val}'"
            )

    def test_progress_visualization_enums_documented(self):
        """progress_visualization enums (per_task|daily|weekly) must appear in SKILL.md."""
        content = _read_file(SKILL_MD_PATH)
        for val in DIMENSION_ENUMS["progress_visualization"]:
            assert val in content, (
                f"SKILL.md missing progress_visualization enum value '{val}'"
            )

    def test_celebration_intensity_enums_documented(self):
        """celebration_intensity enums (high|medium|low) must appear in SKILL.md."""
        content = _read_file(SKILL_MD_PATH)
        for val in DIMENSION_ENUMS["celebration_intensity"]:
            assert val in content, (
                f"SKILL.md missing celebration_intensity enum value '{val}'"
            )

    def test_reminder_style_enums_documented(self):
        """reminder_style enums (specific|balanced|gentle) must appear in SKILL.md."""
        content = _read_file(SKILL_MD_PATH)
        for val in DIMENSION_ENUMS["reminder_style"]:
            assert val in content, (
                f"SKILL.md missing reminder_style enum value '{val}'"
            )

    def test_overwhelm_prevention_enums_documented(self):
        """overwhelm_prevention enums (strict|moderate|open) must appear in SKILL.md."""
        content = _read_file(SKILL_MD_PATH)
        for val in DIMENSION_ENUMS["overwhelm_prevention"]:
            assert val in content, (
                f"SKILL.md missing overwhelm_prevention enum value '{val}'"
            )
