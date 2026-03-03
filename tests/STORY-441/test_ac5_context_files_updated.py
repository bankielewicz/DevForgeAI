"""AC#5: Context Files Updated."""
import os

from conftest import PROJECT_ROOT


class TestAC5ContextFilesUpdated:
    """AC#5: Context files reflect new skill name."""

    def test_should_list_discovering_requirements_in_source_tree(self):
        path = os.path.join(PROJECT_ROOT, "devforgeai", "specs", "context", "source-tree.md")
        with open(path) as f:
            content = f.read()
        assert "discovering-requirements/" in content

    def test_should_not_list_old_name_in_source_tree(self):
        path = os.path.join(PROJECT_ROOT, "devforgeai", "specs", "context", "source-tree.md")
        with open(path) as f:
            content = f.read()
        assert "devforgeai-ideation/" not in content
