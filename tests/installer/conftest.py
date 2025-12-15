"""
Shared fixtures for CLAUDE.md merge service tests.

Provides fixtures for:
- Markdown content samples
- Merge operation test data
- Logger protocol mocks
- File system test utilities
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from typing import Generator, Optional, List
from dataclasses import dataclass
from datetime import datetime
from unittest.mock import Mock, MagicMock


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """
    Create temporary directory for test isolation.

    Automatically cleaned up after test completion.
    """
    tmp = Path(tempfile.mkdtemp())
    yield tmp
    shutil.rmtree(tmp, ignore_errors=True)


@pytest.fixture
def mock_logger() -> Mock:
    """
    Mock logger following ILogger protocol.

    Protocol:
    - log(message: str) -> None
    """
    logger = Mock()
    logger.log = Mock(return_value=None)
    return logger


@pytest.fixture
def simple_claudemd() -> str:
    """
    Simple CLAUDE.md content for basic merge testing.

    Contains:
    - Framework section: "Repository Overview"
    - User section: "My Custom Configuration"
    """
    return """# CLAUDE.md

## Repository Overview

Framework guidance goes here.

## My Custom Configuration

This is user-created content.

### Important Details

User-specific project guidelines.
"""


@pytest.fixture
def complex_claudemd() -> str:
    """
    Complex CLAUDE.md with multiple sections and edge cases.

    Contains:
    - 15 framework sections
    - 8 user sections
    - Code blocks
    - Nested headers
    """
    return """# CLAUDE.md

## Repository Overview

Framework content here.

## My Project Structure

User created this section.

```
src/
  components/
  utils/
```

## Critical Rules

Framework section with important information.

### Security Rules

User added these critical rules.

```python
# Code example
def important():
    pass
```

## Development Workflow

Framework workflow documentation.

## Team Guidelines

User guidelines for team collaboration.

### Code Review Standards

Minimum 2 approvals required.

## Ambiguity Resolution Protocol

Framework protocol section.

## Project Constraints

User-defined project constraints.

- No external dependencies
- Python 3.10+ required
- PostgreSQL only

## Anti-Patterns

Framework anti-patterns guide.

## When Working in Repository

User working guidelines specific to project.

### Setup Instructions

```bash
pip install -r requirements.txt
pytest
```

## References

Framework references section.

## Additional Resources

User-added resource links.

- Internal wiki
- Team documentation
- External tools
"""


@pytest.fixture
def conflicting_claudemd() -> str:
    """
    CLAUDE.md with user modifications to framework sections.

    Used to test conflict detection (>30% content change).
    """
    return """# CLAUDE.md

## Repository Overview

USER HAS MODIFIED THIS: Framework guidance was completely replaced.
This is now entirely user content. Original framework section is gone.
User added many new instructions here. Complete rewrite occurred.

## My Custom Configuration

This is user-created content.

### Important Details

User-specific project guidelines modified significantly.

## Critical Rules

USER HEAVILY MODIFIED: Original framework rules replaced.
User added custom rules here. Completely different content now.
Framework section restructured by user with new requirements.
"""


@pytest.fixture
def empty_claudemd() -> str:
    """Empty CLAUDE.md file for testing edge cases."""
    return ""


@pytest.fixture
def minimal_claudemd() -> str:
    """Minimal CLAUDE.md with only header."""
    return "# CLAUDE.md\n"


@pytest.fixture
def framework_template() -> str:
    """
    DevForgeAI framework template for merge operations.

    Contains all framework sections that should be merged/replaced.
    """
    return """# CLAUDE.md

## Repository Overview

Use native tools over bash.

Halt! if using Bash.

Use AskUserQuestion tool to ask questions.

## Critical Rules

1. Technology Decisions - ALWAYS check tech-stack.md
2. File Operations - Use native tools (40-73% token savings)
3. Ambiguity Resolution - Use AskUserQuestion
4. Context Files Are Immutable - Never violate constraints
5. TDD Is Mandatory - Tests before implementation
6. Quality Gates Are Strict - Coverage thresholds enforced
7. No Library Substitution - Cannot swap without approval
8. Anti-Patterns Are Forbidden - Check patterns.md
9. Document All Decisions - Create ADRs
10. Ask, Don't Assume - HALT and use AskUserQuestion

## Development Workflow

### Complete Lifecycle

1. IDEATION (devforgeai-ideation)
2. ARCHITECTURE (devforgeai-architecture)
3. ORCHESTRATION (devforgeai-orchestration)
4. UI GENERATION (devforgeai-ui-generator)
5. DEVELOPMENT (devforgeai-development)
6. QA (devforgeai-qa)
7. RELEASE (devforgeai-release)

## References

- Framework documentation: ROADMAP.md
- Skills: .claude/skills/*/SKILL.md
- Subagents: .claude/agents/*.md
"""


@pytest.fixture
def large_claudemd() -> str:
    """
    Large CLAUDE.md (>500KB simulation with repeated content).

    Used for performance testing with NFR-001 requirement.
    """
    base = """
## Section {n}

User content section {n}.

This section contains detailed information about {n}.

### Subsection {n}.1

Details for subsection {n}.1.

### Subsection {n}.2

Details for subsection {n}.2.

Some code example:

```python
def function_{n}():
    return {n}
```

End of section {n}.
"""
    sections = "\n".join(base.format(n=i) for i in range(1, 101))
    return f"# CLAUDE.md\n{sections}"


@pytest.fixture
def invalid_utf8_bytes() -> bytes:
    """Invalid UTF-8 byte sequence for encoding error testing."""
    return b"Valid UTF-8 here\xff\xfe and invalid bytes"


@pytest.fixture
def mock_merge_result():
    """
    Mock MergeResult dataclass following specification.

    Fields:
    - status: Enum (SUCCESS, CONFLICT, ERROR, SKIPPED)
    - strategy: str (auto-merge, replace, skip, manual)
    - merged_content: Optional[str]
    - backup_path: Optional[Path]
    - conflicts: List[ConflictDetail]
    - error_message: Optional[str]
    - timestamp: str
    """
    return Mock(
        status="SUCCESS",
        strategy="auto-merge",
        merged_content="merged content",
        backup_path=Path("/tmp/backup-20251204-100000"),
        conflicts=[],
        error_message=None,
        timestamp="2025-12-04T10:00:00Z"
    )


@pytest.fixture
def mock_conflict_detail():
    """
    Mock ConflictDetail dataclass following specification.

    Fields:
    - section_name: str
    - line_start: int
    - line_end: int
    - user_excerpt: str (max 200 chars)
    - framework_excerpt: str (max 200 chars)
    - similarity_ratio: float (0.0 to 1.0)
    """
    return Mock(
        section_name="Critical Rules",
        line_start=10,
        line_end=25,
        user_excerpt="USER HEAVILY MODIFIED: Original framework rules replaced.",
        framework_excerpt="Framework critical rules and constraints.",
        similarity_ratio=0.35  # 35% similarity = 65% difference = conflict
    )


@pytest.fixture
def markdown_samples():
    """Dictionary of markdown samples for testing various parsing scenarios."""
    return {
        "atx_headers": """# H1 Title
## H2 Title
### H3 Title
#### H4 Title
##### H5 Title
###### H6 Title
""",
        "setext_headers": """H1 Title
==========

H2 Title
----------
""",
        "code_blocks": """## Section

```python
def code():
    return True
```

Regular text.

```
Plain code block
```

More text.
""",
        "nested_structure": """# Main

## Sub 1

Content 1.

### Sub 1.1

Content 1.1.

## Sub 2

Content 2.

### Sub 2.1

Content 2.1.

#### Sub 2.1.1

Content 2.1.1.
""",
        "mixed_content": """# Title

Text with **bold** and *italic*.

- List item 1
- List item 2

## Section

1. Numbered item
2. Another item

```python
code()
```

Final content.
"""
    }


@pytest.fixture
def file_permission_tests(temp_dir: Path):
    """
    Create files with various permission states for testing.

    Returns dict with file paths and permission info.
    """
    import os

    # Regular file (644)
    regular = temp_dir / "regular.txt"
    regular.write_text("content")
    os.chmod(regular, 0o644)

    # Read-only file (444)
    readonly = temp_dir / "readonly.txt"
    readonly.write_text("content")
    os.chmod(readonly, 0o444)

    # Executable file (755)
    executable = temp_dir / "executable.sh"
    executable.write_text("#!/bin/bash\necho 'test'")
    os.chmod(executable, 0o755)

    return {
        "regular": regular,
        "readonly": readonly,
        "executable": executable,
        "regular_mode": 0o644,
        "readonly_mode": 0o444,
        "executable_mode": 0o755
    }


@pytest.fixture
def timestamp_format_tests():
    """Test cases for timestamp format validation."""
    return {
        "valid": [
            "20251204-100000",
            "20251201-235959",
            "20250101-000000",
        ],
        "invalid": [
            "2025-12-04-10-00-00",  # Wrong format (dashes)
            "12/04/2025 10:00:00",  # Date format
            "invalid-timestamp",    # Random string
            "20251204",              # Missing time
        ]
    }


@pytest.fixture
def similarity_threshold_tests():
    """Test cases for similarity threshold boundary conditions."""
    return {
        "no_conflict": [
            {"original": "Framework rules", "modified": "Framework rules", "ratio": 1.0},
            {"original": "Framework content", "modified": "Framework content (user comment)", "ratio": 0.85},
            {"original": "Section content", "modified": "Section content with minor addition", "ratio": 0.75},
        ],
        "conflict": [
            {"original": "Framework rules", "modified": "USER MODIFIED: Completely different", "ratio": 0.30},
            {"original": "Rules", "modified": "Different content", "ratio": 0.25},
            {"original": "Framework", "modified": "Something else", "ratio": 0.0},
        ],
        "boundary": [
            {"original": "Content", "modified": "Content", "ratio": 0.70},  # Exactly 70% - NO conflict
            {"original": "Content", "modified": "Modified", "ratio": 0.69},  # Just below - CONFLICT
            {"original": "Framework", "modified": "Framework modified", "ratio": 0.70},  # 70% - NO conflict
            {"original": "Framework", "modified": "Completely changed", "ratio": 0.69},  # 69% - CONFLICT
        ]
    }


@pytest.fixture
def excerpt_truncation_tests():
    """Test cases for MAX_EXCERPT_LENGTH = 200 chars."""
    short_text = "This is short content."
    long_text = "A" * 300  # 300 chars
    exactly_200 = "B" * 200  # Exactly 200 chars
    almost_200 = "C" * 199  # 199 chars

    return {
        "short": short_text,
        "long": long_text,
        "exactly_200": exactly_200,
        "almost_200": almost_200,
        "max_length": 200
    }


@pytest.fixture
def symlink_test_files(temp_dir: Path):
    """
    Create various symlink scenarios for security testing.

    Returns dict with symlink paths and targets.
    """
    import os

    # Regular file (allowed target)
    target_file = temp_dir / "target.txt"
    target_file.write_text("target content")

    # Symlink to regular file (allowed)
    allowed_symlink = temp_dir / "allowed_symlink"
    os.symlink(target_file, allowed_symlink)

    # Symlink to system file (forbidden)
    system_symlink = temp_dir / "system_symlink"
    try:
        os.symlink("/etc/passwd", system_symlink)
        has_system_symlink = True
    except (OSError, PermissionError):
        has_system_symlink = False

    # Symlink outside project (forbidden)
    outside_symlink = temp_dir / "outside_symlink"
    try:
        os.symlink("/tmp/outside", outside_symlink)
        has_outside_symlink = True
    except OSError:
        has_outside_symlink = False

    return {
        "target_file": target_file,
        "allowed_symlink": allowed_symlink,
        "system_symlink": system_symlink if has_system_symlink else None,
        "outside_symlink": outside_symlink if has_outside_symlink else None,
        "temp_dir": temp_dir,
        "has_system_symlink": has_system_symlink,
        "has_outside_symlink": has_outside_symlink
    }


# ============================================================================
# Merged from installer/tests/conftest.py (STORY-045/078 fixtures)
# ============================================================================

import pytest
import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone
from installer.repair_service import SecurityError  # Make SecurityError available for tests


def pytest_sessionstart(session):
    """Inject SecurityError before tests start."""
    # Make sure test_repair_service uses our SecurityError
    import tests.installer.test_repair_service as test_module
    # Replace the locally-defined SecurityError with ours
    test_module.SecurityError = SecurityError
    # Also update builtins so it's available everywhere
    import builtins
    if not hasattr(builtins, 'SecurityError'):
        builtins.SecurityError = SecurityError


@pytest.fixture
def tmp_project(tmp_path):
    """
    Create a temporary project directory with DevForgeAI framework installed.

    Returns:
        dict: Contains 'root' (project root), 'claude' (.claude/), 'devforgeai' (.devforgeai/)
    """
    root = tmp_path / "test_project"
    root.mkdir()

    # Create .claude/ structure
    claude_dir = root / ".claude"
    claude_dir.mkdir()
    (claude_dir / "agents").mkdir()
    (claude_dir / "commands").mkdir()
    (claude_dir / "memory").mkdir()
    (claude_dir / "scripts").mkdir()
    (claude_dir / "skills").mkdir()

    # Create .devforgeai/ structure
    devforgeai_dir = root / ".devforgeai"
    devforgeai_dir.mkdir()
    (devforgeai_dir / "config").mkdir()
    (devforgeai_dir / "context").mkdir()
    (devforgeai_dir / "protocols").mkdir()
    (devforgeai_dir / "specs").mkdir()
    (devforgeai_dir / "qa").mkdir()
    (devforgeai_dir / "adrs").mkdir()

    # Create backup directory (for tests that check backup paths)
    backups_dir = root / ".backups"
    backups_dir.mkdir()

    return {
        "root": root,
        "claude": claude_dir,
        "devforgeai": devforgeai_dir,
        "backups": backups_dir,
    }


@pytest.fixture
def installed_version_1_0_0(tmp_project):
    """
    Create version.json for an installed version 1.0.0 in test project.

    Returns:
        dict: Version metadata for 1.0.0
    """
    version_data = {
        "version": "1.0.0",
        "installed_at": "2025-11-15T10:00:00Z",
        "mode": "fresh_install",
        "schema_version": "1.0",
    }

    version_file = tmp_project["devforgeai"] / ".version.json"
    version_file.write_text(json.dumps(version_data, indent=2))

    return version_data


@pytest.fixture
def source_version_1_0_1():
    """
    Create source version 1.0.1 data (would come from src/devforgeai/version.json).

    Returns:
        dict: Version metadata for 1.0.1 (source)
    """
    return {
        "version": "1.0.1",
        "released_at": "2025-11-17T12:00:00Z",
        "schema_version": "1.0",
        "changes": ["Bug fix 1", "Bug fix 2"],
    }


@pytest.fixture
def backup_manifest():
    """
    Create a sample backup manifest (manifest.json from backup directory).

    Returns:
        dict: Complete backup manifest with integrity data
    """
    return {
        "created_at": "2025-11-17T14:30:00Z",
        "reason": "upgrade",
        "from_version": "1.0.0",
        "to_version": "1.0.1",
        "files_backed_up": 450,
        "total_size_mb": 15.2,
        "backup_integrity_hash": "sha256:abcdef123456789abcdef123456789abcdef123456789abcdef123456789ab",
    }


@pytest.fixture
def mock_source_files(tmp_path):
    """
    Create mock source file structure (simulating src/ directory).

    Creates:
    - src/claude/ with 370 mock files
    - src/devforgeai/ with 80 mock files
    - src/devforgeai/version.json with v1.0.1

    Returns:
        dict: Paths to source structure {'root', 'claude', 'devforgeai', 'version_file'}
    """
    src_root = tmp_path / "mock_src"
    src_root.mkdir()

    # Create src/claude structure
    src_claude = src_root / "claude"
    src_claude.mkdir()
    (src_claude / "agents").mkdir()
    (src_claude / "commands").mkdir()
    (src_claude / "memory").mkdir()
    (src_claude / "scripts").mkdir()
    (src_claude / "skills").mkdir()

    # Create mock files in src/claude
    for i in range(370):
        subdir = src_claude / ["agents", "commands", "memory", "skills"][i % 4]
        (subdir / f"file_{i:03d}.md").write_text(f"Mock file {i}")

    # Create src/devforgeai structure
    src_devforgeai = src_root / "devforgeai"
    src_devforgeai.mkdir()
    (src_devforgeai / "config").mkdir()
    (src_devforgeai / "protocols").mkdir()
    (src_devforgeai / "specs").mkdir()
    (src_devforgeai / "tests").mkdir()

    # Create mock files in src/devforgeai
    for i in range(80):
        subdir = src_devforgeai / ["config", "protocols", "specs", "tests"][i % 4]
        (subdir / f"spec_{i:03d}.md").write_text(f"Mock spec {i}")

    # Create version.json
    version_file = src_devforgeai / "version.json"
    version_file.write_text(
        json.dumps(
            {
                "version": "1.0.1",
                "released_at": "2025-11-17T12:00:00Z",
                "schema_version": "1.0",
            },
            indent=2,
        )
    )

    return {
        "root": src_root,
        "claude": src_claude,
        "devforgeai": src_devforgeai,
        "version_file": version_file,
    }


@pytest.fixture
def mock_user_config(tmp_project):
    """
    Create user configuration files that should be preserved during upgrade.

    Returns:
        dict: Paths to user config files
    """
    hooks_file = tmp_project["devforgeai"] / "config" / "hooks.yaml"
    hooks_file.write_text("# User custom hooks\ncustom_hook: value\n")

    feedback_file = tmp_project["devforgeai"] / "feedback" / "config.yaml"
    (tmp_project["devforgeai"] / "feedback").mkdir(exist_ok=True)
    feedback_file.write_text("# User feedback config\nfeedback_enabled: true\n")

    context_file = tmp_project["devforgeai"] / "context" / "tech-stack.md"
    context_file.write_text("# User tech stack\n- Python 3.8+\n- pytest\n")

    return {
        "hooks": hooks_file,
        "feedback": feedback_file,
        "context": context_file,
    }


@pytest.fixture
def fixed_timestamp():
    """
    Provide a fixed timestamp for deterministic testing (no random time).

    Returns:
        str: ISO format timestamp "2025-11-17T14:30:00Z"
    """
    return "2025-11-17T14:30:00Z"


@pytest.fixture
def mock_datetime(fixed_timestamp):
    """
    Mock datetime.datetime.now() to return fixed timestamp for deterministic tests.

    Yields:
        MagicMock: Patched datetime that returns fixed time
    """
    fixed_dt = datetime.fromisoformat(fixed_timestamp.replace("Z", "+00:00"))

    with patch("datetime.datetime") as mock_dt:
        mock_dt.now.return_value = fixed_dt
        mock_dt.utcnow.return_value = fixed_dt
        mock_dt.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)
        yield mock_dt


@pytest.fixture
def installation_states():
    """
    Provide different installation states for testing mode detection.

    Returns:
        dict: Installation state configurations for different scenarios
    """
    return {
        "fresh": {
            "has_version_file": False,
            "has_claude_dir": False,
            "has_devforgeai_dir": False,
        },
        "existing_1_0_0": {
            "has_version_file": True,
            "version": "1.0.0",
            "has_claude_dir": True,
            "has_devforgeai_dir": True,
        },
        "existing_1_0_1": {
            "has_version_file": True,
            "version": "1.0.1",
            "has_claude_dir": True,
            "has_devforgeai_dir": True,
        },
        "corrupted": {
            "has_version_file": False,  # Missing version.json
            "has_claude_dir": True,  # But .claude/ exists
            "has_devforgeai_dir": True,  # And .devforgeai/ exists
        },
    }


@pytest.fixture
def error_scenarios():
    """
    Provide error scenarios for error handling testing.

    Returns:
        dict: Error configuration and expected responses
    """
    return {
        "permission_denied": {
            "error": PermissionError("Permission denied: .claude/commands/"),
            "message": "Permission denied writing to .claude/commands/",
        },
        "disk_full": {
            "error": OSError("[Errno 28] No space left on device"),
            "message": "Insufficient disk space for deployment",
        },
        "corrupted_backup": {
            "error": ValueError("Backup manifest validation failed"),
            "message": "Backup integrity check failed",
        },
        "network_timeout": {
            "error": TimeoutError("Network timeout during pip install"),
            "message": "CLI installation failed (network timeout)",
        },
        "invalid_version": {
            "error": ValueError("Invalid version format"),
            "message": "Invalid version in source",
        },
    }


# ============================================================================
# STORY-079: Fix/Repair Installation Mode - Test Fixtures
# ============================================================================


@pytest.fixture
def corrupted_installation(tmp_project, tmp_path):
    """
    Create an installation with corrupted files (checksums don't match).

    Returns:
        dict: Contains 'manifest_path', 'corrupted_files' list
    """
    manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"

    # Create files with wrong checksums
    corrupted_file1 = tmp_project["root"] / "file1.txt"
    corrupted_file1.write_text("Modified content 1")

    corrupted_file2 = tmp_project["claude"] / "modified.md"
    corrupted_file2.write_text("Modified markdown")

    manifest_data = {
        "version": "1.0.0",
        "created_at": "2025-11-25T10:00:00Z",
        "files": [
            {
                "path": "file1.txt",
                "checksum": "a" * 64,  # Wrong!
                "size": 100,
                "is_user_modifiable": False,
            },
            {
                "path": ".claude/modified.md",
                "checksum": "b" * 64,  # Wrong!
                "size": 200,
                "is_user_modifiable": False,
            },
        ],
        "schema_version": 1,
    }
    manifest_path.write_text(json.dumps(manifest_data, indent=2))

    return {
        "manifest_path": manifest_path,
        "corrupted_files": [str(corrupted_file1), str(corrupted_file2)],
        "root": tmp_project["root"],
    }


@pytest.fixture
def user_modified_installation(tmp_project):
    """
    Create an installation with user-modified files.

    Returns:
        dict: Contains 'manifest_path', 'user_modified_files' list
    """
    manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"

    # Create user-modifiable files
    ai_docs = tmp_project["root"] / ".ai_docs"
    ai_docs.mkdir()
    user_story = ai_docs / "my_story.md"
    user_story.write_text("# My Custom Story")

    context_file = tmp_project["devforgeai"] / "context" / "tech-stack.md"
    context_file.write_text("# Custom Tech Stack\nPython 3.11")

    manifest_data = {
        "version": "1.0.0",
        "created_at": "2025-01-01T10:00:00Z",  # Older than modifications
        "files": [
            {
                "path": ".ai_docs/my_story.md",
                "checksum": "original_checksum_1" + ("a" * 44),
                "size": 100,
                "is_user_modifiable": True,
            },
            {
                "path": "devforgeai/context/tech-stack.md",
                "checksum": "original_checksum_2" + ("b" * 44),
                "size": 200,
                "is_user_modifiable": True,
            },
        ],
        "schema_version": 1,
    }
    manifest_path.write_text(json.dumps(manifest_data, indent=2))

    return {
        "manifest_path": manifest_path,
        "user_modified_files": [str(user_story), str(context_file)],
        "root": tmp_project["root"],
    }


@pytest.fixture
def missing_manifest_installation(tmp_project):
    """
    Create an installation with no manifest file.

    Returns:
        dict: Contains 'root' and 'expected_manifest_path'
    """
    manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"

    # Create some files but no manifest
    file1 = tmp_project["root"] / "file1.txt"
    file1.write_text("Content 1")

    file2 = tmp_project["claude"] / "file2.md"
    file2.write_text("Content 2")

    return {
        "root": tmp_project["root"],
        "expected_manifest_path": manifest_path,
        "existing_files": [str(file1), str(file2)],
    }


@pytest.fixture
def healthy_installation(tmp_project):
    """
    Create a healthy installation with valid manifest and matching files.

    Returns:
        dict: Contains 'manifest_path', 'root', 'file_count'
    """
    manifest_path = tmp_project["devforgeai"] / ".install-manifest.json"

    files = []
    for i in range(10):
        file_path = tmp_project["root"] / f"file_{i:02d}.txt"
        content = f"Content {i}"
        file_path.write_text(content)

        files.append({
            "path": f"file_{i:02d}.txt",
            "checksum": TestFixtures._calculate_sha256(content),
            "size": len(content),
            "is_user_modifiable": False,
        })

    manifest_data = {
        "version": "1.0.0",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "files": files,
        "schema_version": 1,
    }
    manifest_path.write_text(json.dumps(manifest_data, indent=2))

    return {
        "manifest_path": manifest_path,
        "root": tmp_project["root"],
        "file_count": len(files),
    }


@pytest.fixture
def mock_source_package(tmp_path):
    """
    Create a mock source package with repair files.

    Returns:
        dict: Contains 'root' directory with source files
    """
    source_root = tmp_path / "source_package"
    source_root.mkdir()

    # Create various source files
    (source_root / ".claude").mkdir()
    (source_root / ".devforgeai").mkdir()

    source_files = [
        (".claude/agents/test.md", "Test agent content"),
        ("devforgeai/context/tech-stack.md", "Tech stack content"),
        ("file1.txt", "File 1 content"),
        ("file2.txt", "File 2 content"),
    ]

    for path, content in source_files:
        file_path = source_root / path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)

    return {
        "root": source_root,
        "files": source_files,
    }


class TestFixtures:
    """Helper class for fixture utilities."""

    @staticmethod
    def _calculate_sha256(content: str) -> str:
        """Calculate SHA256 checksum for string content."""
        return hashlib.sha256(content.encode()).hexdigest()


# Import hashlib for fixture use
import hashlib


# ============================================================================
# STORY-079: Add helper method to all test classes
# ============================================================================

@pytest.fixture(autouse=True)
def inject_test_helpers(request):
    """Inject _calculate_sha256 helper into test instances."""
    if request.instance:
        # Add helper method to test instance
        if not hasattr(request.instance, '_calculate_sha256'):
            request.instance._calculate_sha256 = lambda content: hashlib.sha256(content.encode()).hexdigest()
