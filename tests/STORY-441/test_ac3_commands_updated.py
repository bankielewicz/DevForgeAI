"""AC#3: Command Files Updated."""
import os
import glob as globmod

from conftest import PROJECT_ROOT

COMMANDS_DIR = os.path.join(PROJECT_ROOT, "src", "claude", "commands")


class TestAC3CommandsUpdated:
    """AC#3: Command files reference discovering-requirements."""

    def test_should_invoke_discovering_requirements_in_ideate_command(self):
        ideate_path = os.path.join(COMMANDS_DIR, "ideate.md")
        assert os.path.isfile(ideate_path), f"ideate.md not found at {ideate_path}"
        with open(ideate_path) as f:
            content = f.read()
        assert "discovering-requirements" in content, "ideate.md must invoke discovering-requirements"

    def test_should_not_have_old_name_in_any_command_file(self):
        for fpath in globmod.glob(os.path.join(COMMANDS_DIR, "*.md")):
            with open(fpath) as f:
                content = f.read()
            assert "devforgeai-ideation" not in content, \
                f"{os.path.basename(fpath)} still references devforgeai-ideation"
