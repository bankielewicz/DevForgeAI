"""Shared fixtures for STORY-465 tests."""
import pytest
from pathlib import Path


@pytest.fixture
def project_root():
    """Return the project root directory."""
    return Path("/mnt/c/Projects/DevForgeAI2")


@pytest.fixture
def skill_dir(project_root):
    """Return the assessing-entrepreneur skill directory."""
    return project_root / "src" / "claude" / "skills" / "assessing-entrepreneur"


@pytest.fixture
def skill_file(skill_dir):
    """Return the SKILL.md file path."""
    return skill_dir / "SKILL.md"


@pytest.fixture
def subagent_file(project_root):
    """Return the entrepreneur-assessor subagent file path."""
    return project_root / "src" / "claude" / "agents" / "entrepreneur-assessor.md"


@pytest.fixture
def references_dir(skill_dir):
    """Return the references directory path."""
    return skill_dir / "references"


def parse_yaml_frontmatter(file_path: Path) -> dict:
    """Parse YAML frontmatter from a Markdown file.

    Returns a dict of frontmatter key-value pairs.
    Raises ValueError if no valid frontmatter found.
    """
    import yaml

    content = file_path.read_text(encoding="utf-8")
    if not content.startswith("---"):
        raise ValueError(f"No YAML frontmatter found in {file_path}")

    end_index = content.index("---", 3)
    frontmatter_text = content[3:end_index].strip()
    return yaml.safe_load(frontmatter_text)
