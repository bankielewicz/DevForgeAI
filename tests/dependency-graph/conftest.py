"""
Pytest fixtures for dependency-graph-analyzer tests.
STORY-093: Dependency Graph Enforcement with Transitive Resolution
"""
import pytest
from pathlib import Path


@pytest.fixture
def fixtures_dir():
    """Return the path to test fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def valid_story_content():
    """Return valid story content with depends_on field."""
    return '''---
id: STORY-100
title: Test Story
epic: EPIC-TEST
sprint: SPRINT-TEST
status: Ready for Dev
points: 3
priority: Medium
assigned_to: TBD
created: 2025-12-16
format_version: "2.1"
depends_on: ["STORY-101"]
---

# Test Story
'''


@pytest.fixture
def empty_depends_on_content():
    """Return story content with empty depends_on."""
    return '''---
id: STORY-110
title: No Dependencies
epic: EPIC-TEST
sprint: SPRINT-TEST
status: Ready for Dev
points: 2
priority: Low
assigned_to: TBD
created: 2025-12-16
format_version: "2.1"
depends_on: []
---

# No Dependencies Story
'''


@pytest.fixture
def invalid_id_content():
    """Return story content with invalid dependency IDs."""
    return '''---
id: STORY-111
title: Invalid IDs Story
epic: EPIC-TEST
sprint: SPRINT-TEST
status: Ready for Dev
points: 3
priority: Medium
assigned_to: TBD
created: 2025-12-16
format_version: "2.1"
depends_on: ["STORY-1", "story-102", "INVALID", "STORY-103"]
---

# Invalid IDs Story
'''


@pytest.fixture
def sample_graph():
    """Return a sample dependency graph for testing."""
    return {
        "STORY-100": ["STORY-101"],
        "STORY-101": [],
        "STORY-103": ["STORY-104"],
        "STORY-104": ["STORY-105"],
        "STORY-105": [],
    }


@pytest.fixture
def circular_graph():
    """Return a graph with circular dependency."""
    return {
        "STORY-106": ["STORY-107"],
        "STORY-107": ["STORY-106"],
    }


@pytest.fixture
def status_map_valid():
    """Return status map where all dependencies are valid."""
    return {
        "STORY-101": "QA Approved",
        "STORY-104": "Dev Complete",
        "STORY-105": "QA Approved",
    }


@pytest.fixture
def status_map_invalid():
    """Return status map with invalid dependency statuses."""
    return {
        "STORY-101": "QA Approved",
        "STORY-102": "In Development",
        "STORY-108": "QA Failed",
    }
