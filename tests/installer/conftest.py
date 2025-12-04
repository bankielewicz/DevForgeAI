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
