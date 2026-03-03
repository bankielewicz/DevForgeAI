"""
Test: AC#3 - Grep Fallback for Unsupported Languages
Story: STORY-399
Generated: 2026-02-14

Validates that anti-pattern-scanner.md documents Grep fallback
for languages unsupported by Treelint (C#, Java, Go).

Tests validate STRUCTURE and CONTENT of Markdown files (not executable code).
All tests MUST FAIL initially (TDD Red phase) since content has not been added yet.
"""
import os
import re
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


def read_file(relative_path):
    """Read a file relative to the project root."""
    full_path = os.path.join(PROJECT_ROOT, relative_path)
    with open(full_path, 'r') as f:
        return f.read()


class TestAC3GrepFallback:
    """AC#3: Grep Fallback for Unsupported Languages in anti-pattern-scanner.md."""

    SCANNER_PATH = 'src/claude/agents/anti-pattern-scanner.md'

    @pytest.fixture(autouse=True)
    def setup(self):
        """Arrange: Load the anti-pattern-scanner.md content."""
        self.content = read_file(self.SCANNER_PATH)

    # --- Act & Assert ---

    def test_should_document_grep_fallback_for_unsupported_languages(self):
        """Must document Grep fallback when Treelint is unavailable."""
        content_lower = self.content.lower()
        assert 'grep' in content_lower and 'fallback' in content_lower, \
            "Must document Grep as a fallback mechanism"

    def test_should_mention_csharp_as_unsupported(self):
        """Must list C# as an unsupported language requiring Grep fallback."""
        assert re.search(r'C#|csharp|\.cs', self.content, re.IGNORECASE), \
            "Must mention C# as an unsupported Treelint language"

    def test_should_mention_java_as_unsupported(self):
        """Must list Java as an unsupported language requiring Grep fallback."""
        assert re.search(r'Java(?!Script)', self.content), \
            "Must mention Java as an unsupported Treelint language"

    def test_should_mention_go_as_unsupported(self):
        """Must list Go as an unsupported language requiring Grep fallback."""
        assert re.search(r'\bGo\b|\.go\b', self.content), \
            "Must mention Go as an unsupported Treelint language"

    def test_should_specify_exit_code_127_triggers_fallback(self):
        """Must specify exit code 127 (binary not found) triggers Grep fallback."""
        assert '127' in self.content, \
            "Must specify exit code 127 as Treelint-not-found trigger for Grep fallback"

    def test_should_specify_exit_code_126_triggers_fallback(self):
        """Must specify exit code 126 (permission denied) triggers Grep fallback."""
        assert '126' in self.content, \
            "Must specify exit code 126 as permission-denied trigger for Grep fallback"

    def test_should_contain_grep_pattern_for_class_detection(self):
        r"""Must contain Grep pattern class\s+\w+ for class detection."""
        assert re.search(r'class\\s\+\\w\+|class\\s\+\\w\*|class\s*\\s\+\\w',
                         self.content), \
            r"Must contain Grep pattern like 'class\s+\w+' for class detection"

    def test_should_distinguish_exit_zero_from_fallback(self):
        """Exit code 0 with empty results must NOT trigger fallback."""
        # Look for documentation that exit 0 = valid (no fallback)
        assert re.search(r'exit\s*(code\s*)?0.*valid|exit\s*(code\s*)?0.*do\s*not\s*fall',
                         self.content, re.IGNORECASE), \
            "Must document that exit code 0 with empty results is valid (no fallback)"
