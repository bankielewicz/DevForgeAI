"""
Pytest fixtures for File Overlap Detector tests (STORY-094).

Provides:
    - fixtures_dir: Path to test fixture files
    - story_with_spec: Story content with valid technical_specification
    - story_without_spec: Story content without technical_specification
    - story_with_empty_components: Story with empty components array
    - story_multi_path: Story with 5 file_path values
    - active_stories_map: Pre-built map of active story IDs to file_paths
    - overlapping_stories: Pre-built overlap scenario
    - temp_stories_dir: Temporary directory with test story files
"""
import pytest
import tempfile
import shutil
from pathlib import Path


@pytest.fixture
def fixtures_dir():
    """Return path to test fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def story_with_spec():
    """Story content with valid technical_specification (single file_path)."""
    return '''---
id: STORY-200
title: Single Path Test Story
epic: EPIC-TEST
sprint: SPRINT-TEST
status: In Development
points: 3
priority: Medium
depends_on: []
created: 2025-12-16
format_version: "2.0"
---

# Story: Single Path Test Story

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service"
      name: "single-service"
      file_path: "src/services/single_service.py"
      interface: "Python Module"
```
'''


@pytest.fixture
def story_without_spec():
    """Story content without technical_specification section."""
    return '''---
id: STORY-202
title: No Spec Test Story
epic: EPIC-TEST
sprint: SPRINT-TEST
status: In Development
points: 2
priority: Low
depends_on: []
created: 2025-12-16
format_version: "2.0"
---

# Story: No Spec Test Story

## Description

Test story WITHOUT a technical_specification section.
'''


@pytest.fixture
def story_with_empty_components():
    """Story content with technical_specification but empty components."""
    return '''---
id: STORY-203
title: Empty Components Test Story
epic: EPIC-TEST
sprint: SPRINT-TEST
status: In Development
points: 1
priority: Low
depends_on: []
created: 2025-12-16
format_version: "2.0"
---

# Story: Empty Components Test Story

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components: []
```
'''


@pytest.fixture
def story_multi_path():
    """Story content with 5 file_path values."""
    return '''---
id: STORY-201
title: Multi Path Test Story
epic: EPIC-TEST
sprint: SPRINT-TEST
status: In Development
points: 5
priority: High
depends_on: []
created: 2025-12-16
format_version: "2.0"
---

# Story: Multi Path Test Story

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service"
      name: "user-service"
      file_path: "src/services/user_service.py"

    - type: "Repository"
      name: "user-repository"
      file_path: "src/repositories/user_repository.py"

    - type: "API"
      name: "user-api"
      file_path: "src/api/user_endpoints.py"

    - type: "Configuration"
      name: "user-config"
      file_path: "src/config/user_settings.yaml"

    - type: "DataModel"
      name: "user-model"
      file_path: "src/models/user.py"
```
'''


@pytest.fixture
def story_with_depends_on():
    """Story content with depends_on field."""
    return '''---
id: STORY-207
title: Depends On 204 Test Story
epic: EPIC-TEST
sprint: SPRINT-TEST
status: In Development
points: 5
priority: High
depends_on: ["STORY-204"]
created: 2025-12-16
format_version: "2.0"
---

# Story: Depends On 204 Test Story

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service"
      name: "shared-service"
      file_path: "src/services/shared_service.py"
```
'''


@pytest.fixture
def active_stories_map():
    """Map of active story IDs to their file_paths."""
    return {
        "STORY-204": [
            "src/services/shared_service.py",
            "src/repositories/shared_repository.py",
            "src/config/app_settings.yaml"
        ],
        "STORY-205": [
            "src/services/shared_service.py",
            "src/config/app_settings.yaml",
            "src/services/unique_to_205.py"
        ],
        "STORY-206": [
            "src/services/isolated_service.py",
            "src/api/isolated_endpoints.py"
        ],
    }


@pytest.fixture
def overlapping_stories():
    """Pre-built overlap scenario: STORY-204 and STORY-205 share files."""
    return {
        "STORY-205": [
            "src/services/shared_service.py",
            "src/config/app_settings.yaml"
        ],
    }


@pytest.fixture
def temp_stories_dir(fixtures_dir):
    """Create a temporary directory with test story files copied from fixtures."""
    temp_dir = tempfile.mkdtemp(prefix="test_stories_")
    temp_path = Path(temp_dir)

    # Copy all fixture story files to temp directory
    for story_file in fixtures_dir.glob("*.story.md"):
        shutil.copy(story_file, temp_path / story_file.name)

    yield temp_path

    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def temp_git_dir():
    """Create a temporary git-initialized directory for git diff tests."""
    temp_dir = tempfile.mkdtemp(prefix="test_git_")
    temp_path = Path(temp_dir)

    # Initialize git
    import subprocess
    subprocess.run(["git", "init"], cwd=temp_path, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=temp_path, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=temp_path, capture_output=True)

    yield temp_path

    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def sample_overlap_report():
    """Expected structure of an overlap report."""
    return {
        "story_id": "STORY-204",
        "analysis_type": "pre-flight",
        "timestamp": "2025-12-16T14:30:00Z",
        "overlaps": {
            "STORY-205": ["src/services/shared_service.py"]
        },
        "overlap_count": 1,
        "recommendations": [
            "Coordinate with STORY-205 developer on src/services/shared_service.py"
        ]
    }


@pytest.fixture
def malformed_yaml_story():
    """Story content with malformed YAML in technical_specification."""
    return '''---
id: STORY-999
title: Malformed YAML Story
status: In Development
depends_on: []
---

# Story

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"
  components:
    - type: "Service"
      name: "broken
      file_path: missing-quote
    invalid yaml here
```
'''


@pytest.fixture
def story_factory():
    """Factory for creating test story content with custom parameters."""
    def _create(
        story_id: str = "STORY-100",
        status: str = "In Development",
        depends_on: list = None,
        file_paths: list = None
    ) -> str:
        depends_on = depends_on or []
        file_paths = file_paths or ["src/default.py"]

        components_yaml = ""
        for i, path in enumerate(file_paths):
            components_yaml += f'''
    - type: "Service"
      name: "service-{i}"
      file_path: "{path}"'''

        return f'''---
id: {story_id}
title: Generated Test Story {story_id}
status: {status}
depends_on: {depends_on}
---

# Story: {story_id}

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"
  components:{components_yaml}
```
'''
    return _create
