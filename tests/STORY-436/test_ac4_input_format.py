"""
Test: AC#4 - Input Format Accepts YAML Structured Requirements
Story: STORY-436
Generated: 2026-02-18

Validates Phase 6.2 references requirements-schema.yaml and
documents required fields with legacy fallback.
"""
import re
from pathlib import Path

import pytest

SKILL_MD = Path(__file__).resolve().parents[2] / "src" / "claude" / "skills" / "devforgeai-architecture" / "SKILL.md"


@pytest.fixture
def skill_content():
    assert SKILL_MD.exists(), f"SKILL.md not found at {SKILL_MD}"
    return SKILL_MD.read_text(encoding="utf-8")


@pytest.fixture
def phase6_section(skill_content):
    match = re.search(r"(##\s+Phase\s+6.*?)(?=\n##\s+[^#]|\Z)", skill_content, re.DOTALL)
    assert match, "Phase 6 section not found"
    return match.group(1)


class TestYAMLSchemaReference:
    """Phase 6.2 must reference requirements-schema.yaml."""

    def test_should_reference_requirements_schema_yaml(self, phase6_section):
        assert "requirements-schema.yaml" in phase6_section, \
            "Phase 6 must reference requirements-schema.yaml"

    def test_should_place_schema_reference_in_phase_6_2(self, phase6_section):
        match = re.search(r"6\.2.*?(?=6\.3|\Z)", phase6_section, re.DOTALL)
        assert match, "Sub-phase 6.2 not found"
        assert "requirements-schema" in match.group(0), \
            "requirements-schema must be referenced in Phase 6.2"


class TestRequiredFields:
    """Phase 6 must document required schema fields."""

    REQUIRED_FIELDS = [
        "decisions",
        "scope",
        "success_criteria",
        "constraints",
        "nfrs",
        "stakeholders",
    ]

    @pytest.mark.parametrize("field", REQUIRED_FIELDS)
    def test_should_document_required_field(self, phase6_section, field):
        assert field in phase6_section, \
            f"Phase 6 must document required field '{field}'"


class TestLegacyFallback:
    """Phase 6 must document fallback for legacy narrative requirements."""

    def test_should_document_legacy_fallback(self, phase6_section):
        assert re.search(r"fallback|legacy|narrative", phase6_section, re.IGNORECASE), \
            "Phase 6 must document fallback behavior for legacy narrative requirements"
