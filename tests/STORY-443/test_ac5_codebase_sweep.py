"""AC#5: Full Codebase Grep Sweep — Zero Stale References.

Tests that active code directories contain zero references to old skill names:
  - devforgeai-brainstorming
  - devforgeai-ideation
  - devforgeai-development  (as skill name in active skill files)

Exclusions (historical, intentional):
  - devforgeai/feedback/
  - devforgeai/RCA/
  - devforgeai/specs/Stories/   (completed story Implementation Notes)
  - devforgeai/specs/Epics/     (epic history)
  - devforgeai/specs/brainstorms/
  - Any .backup directories
  - tests/STORY-443/ (this test suite itself)

Also validates that a sweep report file exists at:
  devforgeai/reports/STORY-443-sweep-report.md

All tests MUST FAIL before implementation (TDD Red phase).
Story: STORY-443
"""
import os
import subprocess

from conftest import PROJECT_ROOT, SWEEP_REPORT, HISTORICAL_DIRS

# Active code directories to sweep
SWEEP_DIRS = [
    os.path.join(PROJECT_ROOT, "devforgeai", "specs", "context"),
    os.path.join(PROJECT_ROOT, ".claude", "skills"),
    os.path.join(PROJECT_ROOT, ".claude", "commands"),
    os.path.join(PROJECT_ROOT, ".claude", "memory"),
    os.path.join(PROJECT_ROOT, "src", "claude"),
]

# File patterns to include in the sweep
SWEEP_INCLUDE_PATTERNS = [
    "*.md", "*.py", "*.yaml", "*.yml", "*.json", "*.ts",
]

# Stale names to check — these must have zero active references
STALE_NAMES = [
    "devforgeai-brainstorming",
    "devforgeai-ideation",
]

# devforgeai-development gets special treatment: we check for it as a skill
# name in skills catalog files, not in general prose.
DEV_SKILL_STALE_PATTERNS = [
    'Skill(command="devforgeai-development")',
    'command="devforgeai-development"',
    ".claude/skills/devforgeai-development/",
    "src/claude/skills/devforgeai-development/",
]


def _grep_in_dir(pattern: str, directory: str) -> list[str]:
    """Run grep and return non-empty, non-excluded match lines."""
    if not os.path.isdir(directory):
        return []

    cmd = ["grep", "-r", "--include=*.md", "--include=*.py",
           "--include=*.yaml", "--include=*.yml", "--include=*.json",
           pattern, directory]
    result = subprocess.run(cmd, capture_output=True, text=True)
    lines = [
        line for line in result.stdout.strip().split("\n")
        if line and not any(excl in line for excl in HISTORICAL_DIRS)
        # Exclude the test files themselves
        and "tests/STORY-443" not in line
        and "STORY-443" not in line
    ]
    return lines


def _grep_across_active_dirs(pattern: str) -> list[str]:
    """Grep pattern across all active sweep directories, excluding historical."""
    all_matches = []
    for sweep_dir in SWEEP_DIRS:
        all_matches.extend(_grep_in_dir(pattern, sweep_dir))
    return all_matches


class TestAC5SweepDevforgeaiBrainstorming:
    """Verify zero active references to devforgeai-brainstorming."""

    def test_should_have_zero_matches_in_context_files_when_swept(self):
        matches = _grep_in_dir(
            "devforgeai-brainstorming",
            os.path.join(PROJECT_ROOT, "devforgeai", "specs", "context")
        )
        assert len(matches) == 0, (
            f"Found {len(matches)} references to devforgeai-brainstorming in context files:\n"
            + "\n".join(matches[:10])
        )

    def test_should_have_zero_matches_in_claude_skills_when_swept(self):
        matches = _grep_in_dir(
            "devforgeai-brainstorming",
            os.path.join(PROJECT_ROOT, ".claude", "skills")
        )
        assert len(matches) == 0, (
            f"Found {len(matches)} references to devforgeai-brainstorming in .claude/skills/:\n"
            + "\n".join(matches[:10])
        )

    def test_should_have_zero_matches_in_claude_memory_when_swept(self):
        matches = _grep_in_dir(
            "devforgeai-brainstorming",
            os.path.join(PROJECT_ROOT, ".claude", "memory")
        )
        assert len(matches) == 0, (
            f"Found {len(matches)} references to devforgeai-brainstorming in .claude/memory/:\n"
            + "\n".join(matches[:10])
        )

    def test_should_have_zero_matches_in_src_claude_when_swept(self):
        matches = _grep_in_dir(
            "devforgeai-brainstorming",
            os.path.join(PROJECT_ROOT, "src", "claude")
        )
        assert len(matches) == 0, (
            f"Found {len(matches)} references to devforgeai-brainstorming in src/claude/:\n"
            + "\n".join(matches[:10])
        )


class TestAC5SweepDevforgeaiIdeation:
    """Verify zero active references to devforgeai-ideation."""

    def test_should_have_zero_matches_in_context_files_when_swept(self):
        matches = _grep_in_dir(
            "devforgeai-ideation",
            os.path.join(PROJECT_ROOT, "devforgeai", "specs", "context")
        )
        assert len(matches) == 0, (
            f"Found {len(matches)} references to devforgeai-ideation in context files:\n"
            + "\n".join(matches[:10])
        )

    def test_should_have_zero_matches_in_claude_skills_when_swept(self):
        matches = _grep_in_dir(
            "devforgeai-ideation",
            os.path.join(PROJECT_ROOT, ".claude", "skills")
        )
        assert len(matches) == 0, (
            f"Found {len(matches)} references to devforgeai-ideation in .claude/skills/:\n"
            + "\n".join(matches[:10])
        )

    def test_should_have_zero_matches_in_claude_memory_when_swept(self):
        matches = _grep_in_dir(
            "devforgeai-ideation",
            os.path.join(PROJECT_ROOT, ".claude", "memory")
        )
        assert len(matches) == 0, (
            f"Found {len(matches)} references to devforgeai-ideation in .claude/memory/:\n"
            + "\n".join(matches[:10])
        )

    def test_should_have_zero_matches_in_src_claude_when_swept(self):
        matches = _grep_in_dir(
            "devforgeai-ideation",
            os.path.join(PROJECT_ROOT, "src", "claude")
        )
        assert len(matches) == 0, (
            f"Found {len(matches)} references to devforgeai-ideation in src/claude/:\n"
            + "\n".join(matches[:10])
        )


class TestAC5SweepDevforgeaiDevelopmentSkillRef:
    """Verify no active skill invocation patterns for devforgeai-development."""

    def test_should_have_zero_skill_command_matches_in_memory_when_swept(self):
        """skills-reference.md must not invoke devforgeai-development."""
        matches = _grep_in_dir(
            'command="devforgeai-development"',
            os.path.join(PROJECT_ROOT, ".claude", "memory")
        )
        assert len(matches) == 0, (
            f"Found {len(matches)} Skill() invocations for devforgeai-development in .claude/memory/:\n"
            + "\n".join(matches[:10])
        )

    def test_should_have_zero_skill_command_matches_in_src_memory_when_swept(self):
        """src/claude/memory skills-reference must not invoke devforgeai-development."""
        matches = _grep_in_dir(
            'command="devforgeai-development"',
            os.path.join(PROJECT_ROOT, "src", "claude", "memory")
        )
        assert len(matches) == 0, (
            f"Found {len(matches)} Skill() invocations for devforgeai-development in src/claude/memory/:\n"
            + "\n".join(matches[:10])
        )

    def test_should_have_zero_skill_path_references_to_devforgeai_development_when_swept(self):
        """No active .claude/skills/devforgeai-development/ path references in skills."""
        matches = _grep_in_dir(
            ".claude/skills/devforgeai-development/",
            os.path.join(PROJECT_ROOT, ".claude", "skills")
        )
        assert len(matches) == 0, (
            f"Found {len(matches)} path references to .claude/skills/devforgeai-development/:\n"
            + "\n".join(matches[:10])
        )


class TestAC5SweepReportExists:
    """Verify the sweep report file is generated."""

    def test_should_have_sweep_report_file_when_sweep_complete(self):
        assert os.path.isfile(SWEEP_REPORT), (
            f"Sweep report must exist at {SWEEP_REPORT}. "
            "Run the codebase sweep and generate the report."
        )

    def test_should_have_non_empty_sweep_report_when_generated(self):
        if not os.path.isfile(SWEEP_REPORT):
            import pytest
            pytest.skip("Sweep report does not exist yet")
        with open(SWEEP_REPORT, encoding="utf-8") as f:
            content = f.read()
        assert len(content.strip()) > 100, (
            "Sweep report must contain meaningful content (>100 characters)"
        )

    def test_should_have_story_443_reference_in_sweep_report_when_generated(self):
        if not os.path.isfile(SWEEP_REPORT):
            import pytest
            pytest.skip("Sweep report does not exist yet")
        with open(SWEEP_REPORT, encoding="utf-8") as f:
            content = f.read()
        assert "STORY-443" in content, (
            "Sweep report must reference STORY-443"
        )

    def test_should_confirm_zero_unintentional_stale_references_in_report_when_generated(self):
        """Sweep report must confirm zero unintentional stale references."""
        if not os.path.isfile(SWEEP_REPORT):
            import pytest
            pytest.skip("Sweep report does not exist yet")
        with open(SWEEP_REPORT, encoding="utf-8") as f:
            content = f.read()
        # Report must contain some indication of completion/zero stale references
        has_completion_marker = any(
            marker in content.lower()
            for marker in ["zero stale", "0 stale", "no stale", "zero unintentional", "sweep complete"]
        )
        assert has_completion_marker, (
            "Sweep report must confirm zero unintentional stale references "
            "(expected phrase like 'zero stale' or 'sweep complete')"
        )
