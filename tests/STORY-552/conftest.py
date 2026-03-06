"""
Shared fixtures for STORY-552 Funding Options Guide tests.
"""
import os
import pytest

GUIDE_PATH = os.path.join(
    os.path.dirname(__file__), '..', '..',
    'src', 'claude', 'skills', 'managing-finances', 'references',
    'funding-options-guide.md'
)


@pytest.fixture
def guide_content():
    """Read the funding options guide markdown file.

    Will raise FileNotFoundError in RED phase (file does not exist yet).
    """
    with open(GUIDE_PATH, 'r') as f:
        return f.read()


@pytest.fixture
def guide_sections(guide_content):
    """Split guide into sections by ## headers."""
    import re
    sections = re.split(r'^## ', guide_content, flags=re.MULTILINE)
    return sections
