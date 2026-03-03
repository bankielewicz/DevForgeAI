"""
Test: AC#1 - Seven-Dimension Profile Generation
Story: STORY-466
Phase: TDD Red (tests must FAIL until implementation is complete)

Verifies:
- Profile synthesis phase documented in src/claude/skills/assessing-entrepreneur/SKILL.md
- All 7 calibration dimensions specified with correct ranges
- Calibration engine reference file exists at the correct src/ path
- plan-calibration-engine.md contains 7-dimension calibration logic
"""

import os
import re

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

SKILL_MD_PATH = os.path.join(
    PROJECT_ROOT, "src", "claude", "skills", "assessing-entrepreneur", "SKILL.md"
)

CALIBRATION_ENGINE_PATH = os.path.join(
    PROJECT_ROOT,
    "src",
    "claude",
    "skills",
    "assessing-entrepreneur",
    "references",
    "plan-calibration-engine.md",
)

ALL_SEVEN_DIMENSIONS = [
    "task_chunk_size",
    "session_length",
    "check_in_frequency",
    "progress_visualization",
    "celebration_intensity",
    "reminder_style",
    "overwhelm_prevention",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _read_file(path: str) -> str:
    """Read a file and return its content. Raises FileNotFoundError if missing."""
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


# ---------------------------------------------------------------------------
# SKILL.md tests
# ---------------------------------------------------------------------------


class TestSkillMdProfileSynthasePhase:
    """AC#1: Profile synthesis phase must be documented in SKILL.md."""

    def test_skill_md_exists(self):
        """SKILL.md must exist at the src/ tree path."""
        assert os.path.isfile(SKILL_MD_PATH), (
            f"SKILL.md not found at expected path: {SKILL_MD_PATH}"
        )

    def test_skill_md_contains_profile_synthesis_phase(self):
        """SKILL.md must contain a profile synthesis phase section."""
        content = _read_file(SKILL_MD_PATH)
        # Must reference profile synthesis as a named phase
        assert re.search(
            r"profile\s+synthesis", content, re.IGNORECASE
        ), "SKILL.md missing 'profile synthesis' phase documentation"

    def test_skill_md_documents_all_seven_dimensions(self):
        """SKILL.md must document all 7 calibration dimensions by name."""
        content = _read_file(SKILL_MD_PATH)
        missing = [dim for dim in ALL_SEVEN_DIMENSIONS if dim not in content]
        assert not missing, (
            f"SKILL.md is missing the following calibration dimensions: {missing}"
        )

    def test_skill_md_documents_task_chunk_size_range(self):
        """task_chunk_size must specify the 5-60 minute range."""
        content = _read_file(SKILL_MD_PATH)
        assert re.search(r"5[-–]60\s*min", content, re.IGNORECASE), (
            "SKILL.md missing task_chunk_size range '5-60 min'"
        )

    def test_skill_md_documents_session_length_range(self):
        """session_length must specify the 15-60 minute range."""
        content = _read_file(SKILL_MD_PATH)
        assert re.search(r"15[-–]60\s*min", content, re.IGNORECASE), (
            "SKILL.md missing session_length range '15-60 min'"
        )

    def test_skill_md_documents_check_in_frequency_range(self):
        """check_in_frequency must specify the every 1-5 tasks range."""
        content = _read_file(SKILL_MD_PATH)
        assert re.search(
            r"every\s+1[-–]5\s+tasks", content, re.IGNORECASE
        ), "SKILL.md missing check_in_frequency range 'every 1-5 tasks'"

    def test_skill_md_documents_progress_visualization_range(self):
        """progress_visualization must specify per-task to weekly range."""
        content = _read_file(SKILL_MD_PATH)
        assert re.search(r"per.task", content, re.IGNORECASE), (
            "SKILL.md missing progress_visualization lower bound 'per-task'"
        )
        assert re.search(r"weekly", content, re.IGNORECASE), (
            "SKILL.md missing progress_visualization upper bound 'weekly'"
        )

    def test_skill_md_documents_celebration_intensity_range(self):
        """celebration_intensity must specify every-completion to milestone-only range."""
        content = _read_file(SKILL_MD_PATH)
        assert re.search(r"every.completion", content, re.IGNORECASE), (
            "SKILL.md missing celebration_intensity lower bound 'every-completion'"
        )
        assert re.search(r"milestone.only", content, re.IGNORECASE), (
            "SKILL.md missing celebration_intensity upper bound 'milestone-only'"
        )

    def test_skill_md_documents_reminder_style_range(self):
        """reminder_style must specify specific-next-action to gentle-nudge range."""
        content = _read_file(SKILL_MD_PATH)
        assert re.search(r"specific.next.action", content, re.IGNORECASE), (
            "SKILL.md missing reminder_style lower bound 'specific-next-action'"
        )
        assert re.search(r"gentle.nudge", content, re.IGNORECASE), (
            "SKILL.md missing reminder_style upper bound 'gentle-nudge'"
        )

    def test_skill_md_documents_overwhelm_prevention_range(self):
        """overwhelm_prevention must specify next-3-tasks-only to full-roadmap range."""
        content = _read_file(SKILL_MD_PATH)
        assert re.search(r"next.3.tasks.only", content, re.IGNORECASE), (
            "SKILL.md missing overwhelm_prevention lower bound 'next-3-tasks-only'"
        )
        assert re.search(r"full.roadmap", content, re.IGNORECASE), (
            "SKILL.md missing overwhelm_prevention upper bound 'full-roadmap'"
        )


# ---------------------------------------------------------------------------
# plan-calibration-engine.md tests
# ---------------------------------------------------------------------------


class TestCalibrationEngineReferenceFile:
    """AC#1: plan-calibration-engine.md must contain 7-dimension calibration logic."""

    def test_calibration_engine_exists(self):
        """plan-calibration-engine.md must exist at the src/ references path."""
        assert os.path.isfile(CALIBRATION_ENGINE_PATH), (
            f"Calibration engine not found at expected path: {CALIBRATION_ENGINE_PATH}"
        )

    def test_calibration_engine_documents_all_seven_dimensions(self):
        """plan-calibration-engine.md must reference all 7 calibration dimensions."""
        content = _read_file(CALIBRATION_ENGINE_PATH)
        missing = [dim for dim in ALL_SEVEN_DIMENSIONS if dim not in content]
        assert not missing, (
            f"plan-calibration-engine.md missing calibration logic for: {missing}"
        )

    def test_calibration_engine_specifies_calibration_logic(self):
        """plan-calibration-engine.md must contain explicit calibration or mapping logic."""
        content = _read_file(CALIBRATION_ENGINE_PATH)
        assert re.search(
            r"calibrat(e|ion|ing)", content, re.IGNORECASE
        ), "plan-calibration-engine.md missing calibration logic section"

    def test_calibration_engine_specifies_task_chunk_enums(self):
        """Calibration engine must map to micro|standard|extended enum values."""
        content = _read_file(CALIBRATION_ENGINE_PATH)
        for enum_val in ("micro", "standard", "extended"):
            assert enum_val in content, (
                f"plan-calibration-engine.md missing task_chunk_size enum value '{enum_val}'"
            )

    def test_calibration_engine_specifies_overwhelm_prevention_enums(self):
        """Calibration engine must map to strict|moderate|open enum values."""
        content = _read_file(CALIBRATION_ENGINE_PATH)
        for enum_val in ("strict", "moderate", "open"):
            assert enum_val in content, (
                f"plan-calibration-engine.md missing overwhelm_prevention enum value '{enum_val}'"
            )
