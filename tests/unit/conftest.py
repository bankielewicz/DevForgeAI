"""
Pytest configuration and shared fixtures for STORY-035 tests
"""

import pytest
from pathlib import Path


@pytest.fixture(scope="session")
def project_root():
    """Return project root directory"""
    return Path(__file__).parent.parent.parent


@pytest.fixture(scope="session")
def agent_file_path(project_root):
    """Path to internet-sleuth agent file"""
    return project_root / ".claude" / "agents" / "internet-sleuth.md"


@pytest.fixture(scope="session")
def context_files_dir(project_root):
    """Path to DevForgeAI context files directory"""
    return project_root / "devforgeai" / "context"


@pytest.fixture(scope="session")
def research_output_dir(project_root):
    """Path to research output directory"""
    return project_root / "devforgeai" / "research"


@pytest.fixture(scope="session")
def adrs_dir(project_root):
    """Path to ADRs directory"""
    return project_root / "devforgeai" / "adrs"


@pytest.fixture
def mock_context_files(tmp_path):
    """
    Create mock context files for testing

    Returns dict with file paths for all 6 context files
    """
    context_dir = tmp_path / "devforgeai" / "context"
    context_dir.mkdir(parents=True, exist_ok=True)

    context_files = {
        'tech-stack.md': context_dir / 'tech-stack.md',
        'source-tree.md': context_dir / 'source-tree.md',
        'dependencies.md': context_dir / 'dependencies.md',
        'coding-standards.md': context_dir / 'coding-standards.md',
        'architecture-constraints.md': context_dir / 'architecture-constraints.md',
        'anti-patterns.md': context_dir / 'anti-patterns.md'
    }

    # Create all 6 files with minimal content
    for name, path in context_files.items():
        path.write_text(f"# {name}\n\nMock content for testing.")

    return context_files


@pytest.fixture
def mock_incomplete_context_files(tmp_path):
    """
    Create mock context files with only 4 of 6 files (for brownfield edge case)

    Returns dict with file paths (2 missing)
    """
    context_dir = tmp_path / "devforgeai" / "context"
    context_dir.mkdir(parents=True, exist_ok=True)

    # Only create 4 of 6 files
    created_files = {
        'tech-stack.md': context_dir / 'tech-stack.md',
        'source-tree.md': context_dir / 'source-tree.md',
        'dependencies.md': context_dir / 'dependencies.md',
        'coding-standards.md': context_dir / 'coding-standards.md'
    }

    for name, path in created_files.items():
        path.write_text(f"# {name}\n\nMock content for testing.")

    # Return dict including missing files
    all_files = created_files.copy()
    all_files['architecture-constraints.md'] = context_dir / 'architecture-constraints.md'  # Missing
    all_files['anti-patterns.md'] = context_dir / 'anti-patterns.md'  # Missing

    return all_files


@pytest.fixture
def mock_tech_stack_with_react(tmp_path):
    """
    Create mock tech-stack.md with React (for technology conflict testing)
    """
    context_dir = tmp_path / "devforgeai" / "context"
    context_dir.mkdir(parents=True, exist_ok=True)

    tech_stack = context_dir / 'tech-stack.md'
    tech_stack.write_text("""# Tech Stack

## Frontend
- Framework: React 18.2+
- State Management: Zustand

## Backend
- Language: Node.js 20+
- Framework: Express.js
""")

    return tech_stack


def pytest_configure(config):
    """
    Pytest configuration hook
    """
    # Register custom markers
    config.addinivalue_line(
        "markers",
        "story_035: Tests for STORY-035 Internet-Sleuth Framework Compliance"
    )
    config.addinivalue_line(
        "markers",
        "acceptance_criteria: Tests verifying acceptance criteria"
    )
    config.addinivalue_line(
        "markers",
        "comp: Tests for technical specification components"
    )
