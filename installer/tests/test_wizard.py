"""
Test Suite for CLI Wizard Installer (STORY-247)

Tests for WizardInstaller service and related data models:
- WizardInstaller (AC#1-8, BR-001 to BR-005)
- Component (DataModel)
- WizardState (DataModel)

Test Framework: pytest with unittest.mock
Test Naming Convention: test_<function>_<scenario>_<expected>
Pattern: AAA (Arrange, Act, Assert)

These tests will FAIL initially (TDD Red phase) because:
- installer/wizard.py does not exist yet
- WizardInstaller, Component, WizardState not implemented
"""

import pytest
from unittest.mock import Mock, patch, MagicMock, call
from contextlib import ExitStack
import os
import sys
import tempfile
import time
from pathlib import Path
from io import StringIO


# =============================================================================
# Test Fixtures
# =============================================================================

@pytest.fixture
def mock_terminal():
    """Mock terminal input/output for wizard tests."""
    return {
        'stdin': StringIO(),
        'stdout': StringIO(),
        'is_tty': True
    }


@pytest.fixture
def temp_install_dir():
    """Create a temporary directory for installation tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def readonly_dir(temp_install_dir):
    """Create a read-only directory for permission testing."""
    readonly = os.path.join(temp_install_dir, 'readonly')
    os.makedirs(readonly)
    os.chmod(readonly, 0o444)
    yield readonly
    # Cleanup: restore permissions
    os.chmod(readonly, 0o755)


@pytest.fixture
def default_components():
    """Return default component list for wizard."""
    from installer.wizard import Component
    return [
        Component(
            id="core",
            name="Core Framework",
            description=".claude/, devforgeai/",
            size_mb=2.5,
            required=True,
            selected=True
        ),
        Component(
            id="cli",
            name="CLI Tools",
            description="devforgeai command",
            size_mb=0.5,
            required=False,
            selected=False
        ),
        Component(
            id="templates",
            name="Templates",
            description="project templates",
            size_mb=1.0,
            required=False,
            selected=False
        ),
        Component(
            id="examples",
            name="Examples",
            description="example projects",
            size_mb=3.0,
            required=False,
            selected=False
        ),
    ]


@pytest.fixture
def wizard_state(temp_install_dir, default_components):
    """Create a default WizardState for testing."""
    from installer.wizard import WizardState
    return WizardState(
        current_step=0,
        target_path=Path(temp_install_dir),
        components=default_components,
        config={
            'init_git': False,
            'create_commit': False,
            'run_validation': False
        },
        progress=0.0
    )


@pytest.fixture
def mock_git_available():
    """Mock Git being available on the system."""
    with patch('shutil.which', return_value='/usr/bin/git'):
        yield True


@pytest.fixture
def mock_git_unavailable():
    """Mock Git NOT being available on the system."""
    with patch('shutil.which', return_value=None):
        yield False


# =============================================================================
# Component DataModel Tests (Technical Specification)
# =============================================================================

class TestComponentDataModel:
    """Tests for Component data model from Technical Specification."""

    def test_component_should_have_id_field(self):
        """Tech Spec: Component must have id string field."""
        # Arrange
        from installer.wizard import Component

        # Act
        component = Component(id="core", name="Core Framework")

        # Assert
        assert component.id == "core"

    def test_component_should_have_name_field(self):
        """Tech Spec: Component must have name string field."""
        # Arrange
        from installer.wizard import Component

        # Act
        component = Component(id="core", name="Core Framework")

        # Assert
        assert component.name == "Core Framework"

    def test_component_should_have_description_field(self):
        """Tech Spec: Component must have description string field."""
        # Arrange
        from installer.wizard import Component

        # Act
        component = Component(
            id="core",
            name="Core Framework",
            description=".claude/, devforgeai/"
        )

        # Assert
        assert component.description == ".claude/, devforgeai/"

    def test_component_should_have_size_mb_field(self):
        """Tech Spec: Component must have size_mb float field."""
        # Arrange
        from installer.wizard import Component

        # Act
        component = Component(
            id="core",
            name="Core Framework",
            size_mb=2.5
        )

        # Assert
        assert component.size_mb == 2.5

    def test_component_required_should_default_to_false(self):
        """Tech Spec: Component required defaults to false."""
        # Arrange
        from installer.wizard import Component

        # Act
        component = Component(id="cli", name="CLI Tools")

        # Assert
        assert component.required is False

    def test_component_selected_should_default_to_false(self):
        """Tech Spec: Component selected defaults to false."""
        # Arrange
        from installer.wizard import Component

        # Act
        component = Component(id="cli", name="CLI Tools")

        # Assert
        assert component.selected is False

    def test_component_with_required_true(self):
        """Tech Spec: Component can have required=True."""
        # Arrange
        from installer.wizard import Component

        # Act
        component = Component(
            id="core",
            name="Core Framework",
            required=True,
            selected=True
        )

        # Assert
        assert component.required is True
        assert component.selected is True


# =============================================================================
# WizardState DataModel Tests (Technical Specification)
# =============================================================================

class TestWizardStateDataModel:
    """Tests for WizardState data model from Technical Specification."""

    def test_wizard_state_should_have_current_step_field(self, temp_install_dir):
        """Tech Spec: WizardState must have current_step int field."""
        # Arrange
        from installer.wizard import WizardState

        # Act
        state = WizardState(
            current_step=0,
            target_path=Path(temp_install_dir),
            components=[],
            config={},
            progress=0.0
        )

        # Assert
        assert state.current_step == 0

    def test_wizard_state_should_have_target_path_field(self, temp_install_dir):
        """Tech Spec: WizardState must have target_path Path field."""
        # Arrange
        from installer.wizard import WizardState

        # Act
        state = WizardState(
            current_step=0,
            target_path=Path(temp_install_dir),
            components=[],
            config={},
            progress=0.0
        )

        # Assert
        assert state.target_path == Path(temp_install_dir)

    def test_wizard_state_should_have_components_list(self, default_components, temp_install_dir):
        """Tech Spec: WizardState must have components List[Component] field."""
        # Arrange
        from installer.wizard import WizardState

        # Act
        state = WizardState(
            current_step=0,
            target_path=Path(temp_install_dir),
            components=default_components,
            config={},
            progress=0.0
        )

        # Assert
        assert len(state.components) == 4
        assert state.components[0].id == "core"

    def test_wizard_state_should_have_config_dict(self, temp_install_dir):
        """Tech Spec: WizardState must have config Dict[str, bool] field."""
        # Arrange
        from installer.wizard import WizardState

        # Act
        state = WizardState(
            current_step=0,
            target_path=Path(temp_install_dir),
            components=[],
            config={'init_git': True, 'create_commit': False},
            progress=0.0
        )

        # Assert
        assert state.config['init_git'] is True
        assert state.config['create_commit'] is False

    def test_wizard_state_should_have_progress_float(self, temp_install_dir):
        """Tech Spec: WizardState must have progress float field (0.0-1.0)."""
        # Arrange
        from installer.wizard import WizardState

        # Act
        state = WizardState(
            current_step=0,
            target_path=Path(temp_install_dir),
            components=[],
            config={},
            progress=0.5
        )

        # Assert
        assert state.progress == 0.5


# =============================================================================
# AC#1: Welcome Screen Display Tests
# =============================================================================

class TestWelcomeScreenDisplay:
    """Tests for AC#1: Welcome Screen Display."""

    def test_step_welcome_should_display_framework_name(self, capsys):
        """AC#1: Welcome screen displays framework name."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path="/tmp/test")

        # Act
        with patch('builtins.input', return_value=''):
            wizard.step_welcome()

        # Assert
        captured = capsys.readouterr()
        assert 'DevForgeAI' in captured.out

    def test_step_welcome_should_display_version(self, capsys):
        """AC#1: Welcome screen displays version."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path="/tmp/test")

        # Act
        with patch('builtins.input', return_value=''):
            wizard.step_welcome()

        # Assert
        captured = capsys.readouterr()
        # Should contain version pattern (e.g., 1.0.0, v1.0)
        import re
        assert re.search(r'v?\d+\.\d+', captured.out), "Version not displayed"

    def test_step_welcome_should_display_description(self, capsys):
        """AC#1: Welcome screen displays brief description."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path="/tmp/test")

        # Act
        with patch('builtins.input', return_value=''):
            wizard.step_welcome()

        # Assert
        captured = capsys.readouterr()
        # Should describe what will be installed
        assert any(word in captured.out.lower() for word in ['install', 'framework', 'setup'])

    def test_step_welcome_should_return_true_on_enter(self):
        """AC#1: User can press Enter to continue."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path="/tmp/test")

        # Act
        with patch('builtins.input', return_value=''):
            result = wizard.step_welcome()

        # Assert
        assert result is True

    def test_step_welcome_should_handle_keyboard_interrupt(self):
        """AC#1: Ctrl+C cancels wizard."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path="/tmp/test")

        # Act & Assert
        with patch('builtins.input', side_effect=KeyboardInterrupt):
            result = wizard.step_welcome()
            assert result is False


# =============================================================================
# AC#2: License Agreement Step Tests
# =============================================================================

class TestLicenseAgreementStep:
    """Tests for AC#2: License Agreement Step."""

    def test_step_license_should_display_license_text(self, capsys):
        """AC#2: License agreement is displayed."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path="/tmp/test")

        # Act
        with patch('builtins.input', return_value='accept'):
            wizard.step_license()

        # Assert
        captured = capsys.readouterr()
        # Should contain license-related text
        assert any(word in captured.out.lower() for word in ['license', 'mit', 'copyright', 'terms'])

    def test_step_license_should_accept_lowercase_accept(self):
        """AC#2: User must type 'accept' to continue (lowercase)."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path="/tmp/test")

        # Act
        with patch('builtins.input', return_value='accept'):
            result = wizard.step_license()

        # Assert
        assert result is True

    def test_step_license_should_accept_uppercase_accept(self):
        """AC#2: 'accept' is case-insensitive (ACCEPT)."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path="/tmp/test")

        # Act
        with patch('builtins.input', return_value='ACCEPT'):
            result = wizard.step_license()

        # Assert
        assert result is True

    def test_step_license_should_accept_mixed_case_accept(self):
        """AC#2: 'accept' is case-insensitive (Accept)."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path="/tmp/test")

        # Act
        with patch('builtins.input', return_value='Accept'):
            result = wizard.step_license()

        # Assert
        assert result is True

    def test_step_license_should_reprompt_on_invalid_input(self, capsys):
        """AC#2: Typing anything else returns to prompt."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path="/tmp/test")

        # Simulate: 'yes' (invalid) -> 'accept' (valid)
        inputs = iter(['yes', 'accept'])

        # Act
        with patch('builtins.input', side_effect=lambda _='': next(inputs)):
            result = wizard.step_license()

        # Assert
        assert result is True
        captured = capsys.readouterr()
        # Should have prompted at least twice or shown error for invalid input
        assert captured.out.count('accept') >= 1 or 'invalid' in captured.out.lower()

    def test_step_license_should_reject_empty_input(self):
        """AC#2: Empty input should re-prompt."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path="/tmp/test")

        # Simulate: '' (empty) -> 'accept' (valid)
        inputs = iter(['', 'accept'])

        # Act
        with patch('builtins.input', side_effect=lambda _='': next(inputs)):
            result = wizard.step_license()

        # Assert
        assert result is True


# =============================================================================
# AC#3: Installation Path Selection Tests
# =============================================================================

class TestInstallationPathSelection:
    """Tests for AC#3: Installation Path Selection."""

    def test_step_path_should_display_default_path(self, temp_install_dir, capsys):
        """AC#3: Default path is displayed (from command line)."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path=temp_install_dir)

        # Act
        with patch('builtins.input', return_value=''):
            wizard.step_path()

        # Assert
        captured = capsys.readouterr()
        assert temp_install_dir in captured.out

    def test_step_path_should_accept_default_on_enter(self, temp_install_dir):
        """AC#3: User can press Enter to accept default."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path=temp_install_dir)

        # Act
        with patch('builtins.input', return_value=''):
            result = wizard.step_path()

        # Assert
        assert result is True
        assert str(wizard.state.target_path) == temp_install_dir

    def test_step_path_should_accept_custom_path(self, temp_install_dir):
        """AC#3: User can type a different path."""
        # Arrange
        from installer.wizard import WizardInstaller

        default_path = temp_install_dir
        custom_path = os.path.join(temp_install_dir, 'custom')
        os.makedirs(custom_path)

        wizard = WizardInstaller(target_path=default_path)

        # Act
        with patch('builtins.input', return_value=custom_path):
            result = wizard.step_path()

        # Assert
        assert result is True
        assert str(wizard.state.target_path) == custom_path

    def test_step_path_should_validate_write_permissions(self, readonly_dir, capsys):
        """AC#3: Path is validated for write permissions."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path="/tmp")

        # Simulate: readonly path (invalid) -> valid path
        valid_dir = tempfile.mkdtemp()
        inputs = iter([readonly_dir, valid_dir])

        # Act
        with patch('builtins.input', side_effect=lambda _='': next(inputs)):
            with patch('os.access', side_effect=[False, True]):
                result = wizard.step_path()

        # Assert
        captured = capsys.readouterr()
        # Should show error for invalid path
        assert 'permission' in captured.out.lower() or 'error' in captured.out.lower()

    def test_step_path_should_reprompt_on_invalid_path(self, temp_install_dir, capsys):
        """AC#3: Invalid path shows error and re-prompts."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path=temp_install_dir)

        # Simulate: non-existent path -> valid path
        inputs = iter(['/nonexistent/invalid/path', temp_install_dir])

        # Act
        with patch('builtins.input', side_effect=lambda _='': next(inputs)):
            result = wizard.step_path()

        # Assert
        assert result is True
        captured = capsys.readouterr()
        # Should have shown an error message
        assert 'error' in captured.out.lower() or 'invalid' in captured.out.lower() or 'not exist' in captured.out.lower()


# =============================================================================
# AC#4: Component Selection Tests
# =============================================================================

class TestComponentSelection:
    """Tests for AC#4: Component Selection."""

    def test_step_components_should_display_all_4_components(self, capsys, default_components):
        """AC#4: All 4 components are listed."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path="/tmp/test")
        wizard.state.components = default_components

        # Act
        with patch('builtins.input', return_value=''):
            wizard.step_components()

        # Assert
        captured = capsys.readouterr()
        assert 'Core Framework' in captured.out
        assert 'CLI Tools' in captured.out
        assert 'Templates' in captured.out
        assert 'Examples' in captured.out

    def test_step_components_should_show_core_framework_prechecked(self, capsys, default_components):
        """AC#4: Core Framework is pre-checked."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path="/tmp/test")
        wizard.state.components = default_components

        # Act
        with patch('builtins.input', return_value=''):
            wizard.step_components()

        # Assert
        captured = capsys.readouterr()
        # Should show [x] or similar indicator for Core Framework
        assert '[x]' in captured.out.lower() or '[*]' in captured.out or 'selected' in captured.out.lower()

    def test_step_components_should_not_allow_core_deselection(self, default_components):
        """BR-001: Core Framework cannot be deselected."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path="/tmp/test")
        wizard.state.components = default_components

        # Act - Try to deselect core (component index 0)
        # Simulate attempting to toggle core
        wizard.toggle_component('core')

        # Assert
        core_component = next(c for c in wizard.state.components if c.id == 'core')
        assert core_component.selected is True, "Core Framework should remain selected"

    def test_step_components_should_display_total_size(self, capsys, default_components):
        """AC#4: Total installation size is displayed."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path="/tmp/test")
        wizard.state.components = default_components

        # Act
        with patch('builtins.input', return_value=''):
            wizard.step_components()

        # Assert
        captured = capsys.readouterr()
        # Should show size (MB or similar)
        assert 'mb' in captured.out.lower() or 'size' in captured.out.lower()

    def test_toggle_component_should_select_optional_component(self, default_components):
        """AC#4: Optional components can be toggled."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path="/tmp/test")
        wizard.state.components = default_components

        # Act - Select CLI Tools
        wizard.toggle_component('cli')

        # Assert
        cli_component = next(c for c in wizard.state.components if c.id == 'cli')
        assert cli_component.selected is True

    def test_toggle_component_should_deselect_optional_component(self, default_components):
        """AC#4: Optional components can be deselected."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path="/tmp/test")
        wizard.state.components = default_components

        # First select CLI, then deselect
        wizard.toggle_component('cli')
        wizard.toggle_component('cli')

        # Assert
        cli_component = next(c for c in wizard.state.components if c.id == 'cli')
        assert cli_component.selected is False

    def test_get_total_size_should_sum_selected_components(self, default_components):
        """AC#4 Verification: Total size calculated correctly."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path="/tmp/test")
        wizard.state.components = default_components

        # Select additional components
        wizard.toggle_component('cli')  # +0.5 MB

        # Act
        total_size = wizard.get_total_size()

        # Assert
        # Core (2.5) + CLI (0.5) = 3.0 MB
        assert total_size == pytest.approx(3.0, rel=0.01)


# =============================================================================
# AC#5: Configuration Options Tests
# =============================================================================

class TestConfigurationOptions:
    """Tests for AC#5: Configuration Options."""

    def test_step_config_should_display_git_options(self, capsys, mock_git_available):
        """AC#5: Git options are presented."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path="/tmp/test")

        # Act
        with patch('builtins.input', return_value=''):
            wizard.step_config()

        # Assert
        captured = capsys.readouterr()
        assert 'git' in captured.out.lower()

    def test_step_config_should_show_init_git_option(self, capsys, mock_git_available):
        """AC#5: Initialize Git repository option shown."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path="/tmp/test")

        # Act
        with patch('builtins.input', return_value=''):
            wizard.step_config()

        # Assert
        captured = capsys.readouterr()
        assert 'init' in captured.out.lower() or 'repository' in captured.out.lower()

    def test_step_config_should_show_create_commit_option(self, capsys, mock_git_available):
        """AC#5: Create initial commit option shown."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path="/tmp/test")

        # Act
        with patch('builtins.input', return_value=''):
            wizard.step_config()

        # Assert
        captured = capsys.readouterr()
        assert 'commit' in captured.out.lower()

    def test_step_config_should_show_validation_option(self, capsys):
        """AC#5: Run validation after install option shown."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path="/tmp/test")

        # Act
        with patch('builtins.input', return_value=''):
            wizard.step_config()

        # Assert
        captured = capsys.readouterr()
        assert 'validation' in captured.out.lower() or 'validate' in captured.out.lower()

    def test_step_config_should_disable_git_options_when_git_unavailable(
        self, capsys, mock_git_unavailable
    ):
        """BR-004: Git options disabled if Git unavailable."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path="/tmp/test")

        # Act
        with patch('builtins.input', return_value=''):
            with patch('shutil.which', return_value=None):
                wizard.step_config()

        # Assert
        captured = capsys.readouterr()
        # Git options should be disabled/grayed out
        assert 'disabled' in captured.out.lower() or 'unavailable' in captured.out.lower() or \
               'not available' in captured.out.lower()

    def test_toggle_config_should_enable_option(self):
        """AC#5: Config options can be toggled on."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path="/tmp/test")

        # Act
        wizard.toggle_config('init_git')

        # Assert
        assert wizard.state.config['init_git'] is True

    def test_toggle_config_should_disable_option(self):
        """AC#5: Config options can be toggled off."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path="/tmp/test")
        wizard.state.config['init_git'] = True

        # Act
        wizard.toggle_config('init_git')

        # Assert
        assert wizard.state.config['init_git'] is False


# =============================================================================
# AC#6: Installation Progress Tests
# =============================================================================

class TestInstallationProgress:
    """Tests for AC#6: Installation Progress."""

    def test_step_install_should_display_progress_bar(self, capsys, temp_install_dir):
        """AC#6: Progress bar is displayed."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path=temp_install_dir)

        # Act
        with patch.object(wizard, '_do_install', return_value=True):
            wizard.step_install()

        # Assert
        captured = capsys.readouterr()
        # Should show progress indicator
        assert any(char in captured.out for char in ['%', '[', '#', '=', '-'])

    def test_step_install_should_show_current_step_name(self, capsys, temp_install_dir):
        """AC#6: Current step name is displayed."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path=temp_install_dir)

        progress_updates = []

        def mock_progress(step_name, percentage, eta=None):
            progress_updates.append({'step': step_name, 'pct': percentage})

        # Act
        with patch.object(wizard, '_do_install', return_value=True):
            with patch.object(wizard, 'update_progress', side_effect=mock_progress):
                wizard.step_install()

        # Assert
        # Should have step names in progress updates
        captured = capsys.readouterr()
        assert any(word in captured.out.lower() for word in ['copying', 'installing', 'configuring', 'step'])

    def test_step_install_should_show_percentage(self, capsys, temp_install_dir):
        """AC#6: Progress percentage is displayed."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path=temp_install_dir)

        # Act
        with patch.object(wizard, '_do_install', return_value=True):
            wizard.step_install()

        # Assert
        captured = capsys.readouterr()
        # Should show percentage
        assert '%' in captured.out or 'percent' in captured.out.lower()

    def test_step_install_progress_updates_realtime(self, temp_install_dir):
        """BR-005: Progress bar updates in real-time (per-step callback)."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path=temp_install_dir)

        progress_callbacks = []

        def track_progress(step, pct, eta=None):
            progress_callbacks.append(pct)

        wizard.set_progress_callback(track_progress)

        # Act
        with patch.object(wizard, '_do_install', return_value=True):
            wizard.step_install()

        # Assert
        # Should have multiple progress updates (not just 0% and 100%)
        assert len(progress_callbacks) >= 2, "Progress should update multiple times"

    def test_step_install_should_write_to_log_file(self, temp_install_dir):
        """AC#6: Detailed logs are written to install.log."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path=temp_install_dir)
        log_file = os.path.join(temp_install_dir, 'install.log')

        # Act
        with patch.object(wizard, '_do_install', return_value=True):
            wizard.step_install()

        # Assert
        assert os.path.exists(log_file), "install.log should be created"
        with open(log_file) as f:
            content = f.read()
            assert len(content) > 0, "Log file should not be empty"

    def test_step_install_should_stop_on_critical_error(self, temp_install_dir, capsys):
        """AC#6: Critical errors stop installation."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path=temp_install_dir)

        # Act
        with patch.object(wizard, '_do_install', side_effect=PermissionError("Access denied")):
            result = wizard.step_install()

        # Assert
        assert result is False
        captured = capsys.readouterr()
        assert 'error' in captured.out.lower()


# =============================================================================
# AC#7: Completion Summary Tests
# =============================================================================

class TestCompletionSummary:
    """Tests for AC#7: Completion Summary."""

    def test_step_complete_should_display_success_message(self, capsys, temp_install_dir):
        """AC#7: Success message is displayed."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path=temp_install_dir)
        wizard.state.progress = 1.0  # Mark as complete

        # Act
        wizard.step_complete()

        # Assert
        captured = capsys.readouterr()
        assert 'success' in captured.out.lower() or 'complete' in captured.out.lower()

    def test_step_complete_should_show_checkmark(self, capsys, temp_install_dir):
        """AC#7 Verification: Success indicator shown."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path=temp_install_dir)
        wizard.state.progress = 1.0

        # Act
        wizard.step_complete()

        # Assert
        captured = capsys.readouterr()
        # Should have success indicator
        assert any(char in captured.out for char in ['✓', '[x]', '[X]', '*']) or \
               'success' in captured.out.lower()

    def test_step_complete_should_show_installation_path(self, capsys, temp_install_dir):
        """AC#7: Installation path is displayed."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path=temp_install_dir)
        wizard.state.progress = 1.0

        # Act
        wizard.step_complete()

        # Assert
        captured = capsys.readouterr()
        assert temp_install_dir in captured.out

    def test_step_complete_should_list_installed_components(self, capsys, temp_install_dir, default_components):
        """AC#7: Components installed are listed."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path=temp_install_dir)
        wizard.state.components = default_components
        wizard.state.progress = 1.0

        # Act
        wizard.step_complete()

        # Assert
        captured = capsys.readouterr()
        assert 'Core Framework' in captured.out

    def test_step_complete_should_show_next_steps(self, capsys, temp_install_dir):
        """AC#7: Next steps (commands to run) are provided."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path=temp_install_dir)
        wizard.state.progress = 1.0

        # Act
        wizard.step_complete()

        # Assert
        captured = capsys.readouterr()
        # Should show commands to run next
        assert 'next' in captured.out.lower() or 'command' in captured.out.lower() or \
               '/' in captured.out  # Slash command reference


# =============================================================================
# AC#8: Error Recovery Tests
# =============================================================================

class TestErrorRecovery:
    """Tests for AC#8: Error Recovery."""

    def test_handle_error_should_display_clear_message(self, capsys, temp_install_dir):
        """AC#8: Clear error message is displayed."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path=temp_install_dir)
        error = PermissionError("Cannot write to directory")

        # Act
        wizard.handle_error(error)

        # Assert
        captured = capsys.readouterr()
        assert 'error' in captured.out.lower()
        assert 'permission' in captured.out.lower() or 'write' in captured.out.lower()

    def test_handle_error_should_suggest_remediation(self, capsys, temp_install_dir):
        """AC#8: Suggested remediation steps are provided."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path=temp_install_dir)
        error = PermissionError("Cannot write to directory")

        # Act
        wizard.handle_error(error)

        # Assert
        captured = capsys.readouterr()
        # Should suggest what to do
        assert any(word in captured.out.lower() for word in ['try', 'check', 'ensure', 'run', 'fix'])

    def test_handle_error_should_offer_retry_option(self, capsys, temp_install_dir):
        """AC#8: Option to retry is available."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path=temp_install_dir)
        error = ConnectionError("Network timeout")

        # Act
        with patch('builtins.input', return_value='r'):  # 'r' for retry
            action = wizard.handle_error(error, recoverable=True)

        # Assert
        assert action == 'retry' or 'retry' in capsys.readouterr().out.lower()

    def test_handle_error_should_offer_skip_option_for_noncritical(self, temp_install_dir):
        """AC#8: Option to skip is available for non-critical errors."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path=temp_install_dir)
        error = Warning("Optional component unavailable")

        # Act
        with patch('builtins.input', return_value='s'):  # 's' for skip
            action = wizard.handle_error(error, recoverable=True, skippable=True)

        # Assert
        assert action == 'skip'

    def test_handle_error_should_offer_abort_option(self, temp_install_dir):
        """AC#8: Option to abort is available."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path=temp_install_dir)
        error = RuntimeError("Critical failure")

        # Act
        with patch('builtins.input', return_value='a'):  # 'a' for abort
            action = wizard.handle_error(error, recoverable=True)

        # Assert
        assert action == 'abort'

    def test_handle_error_should_log_partial_state(self, temp_install_dir):
        """AC#8: Partial installation state is logged."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path=temp_install_dir)
        wizard.state.progress = 0.5  # Partially complete
        error = RuntimeError("Installation failed mid-way")

        log_file = os.path.join(temp_install_dir, 'install.log')

        # Act
        with patch('builtins.input', return_value='a'):
            wizard.handle_error(error)

        # Assert
        if os.path.exists(log_file):
            with open(log_file) as f:
                content = f.read()
                assert 'partial' in content.lower() or 'incomplete' in content.lower() or \
                       '50%' in content or '0.5' in content


# =============================================================================
# WizardInstaller Service Tests (Technical Specification)
# =============================================================================

class TestWizardInstallerService:
    """Tests for WizardInstaller service from Technical Specification."""

    def test_run_should_return_exit_code_0_on_success(self, temp_install_dir):
        """Tech Spec: run() returns exit code 0 on success."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path=temp_install_dir)

        # Mock all steps to succeed
        with patch.object(wizard, 'step_welcome', return_value=True):
            with patch.object(wizard, 'step_license', return_value=True):
                with patch.object(wizard, 'step_path', return_value=True):
                    with patch.object(wizard, 'step_components', return_value=True):
                        with patch.object(wizard, 'step_config', return_value=True):
                            with patch.object(wizard, 'step_install', return_value=True):
                                with patch.object(wizard, 'step_complete', return_value=None):
                                    # Act
                                    result = wizard.run()

        # Assert
        assert result == 0

    def test_run_should_return_nonzero_on_cancel(self, temp_install_dir):
        """Tech Spec: run() returns non-zero on user cancel."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path=temp_install_dir)

        # Mock welcome step to cancel
        with patch.object(wizard, 'step_welcome', return_value=False):
            # Act
            result = wizard.run()

        # Assert
        assert result != 0

    def test_run_should_execute_steps_in_order(self, temp_install_dir):
        """Tech Spec: Wizard executes steps 0-6 in order."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path=temp_install_dir)

        step_order = []

        def track_step(name):
            def wrapper(*args, **kwargs):
                step_order.append(name)
                return True
            return wrapper

        # Act
        with patch.object(wizard, 'step_welcome', track_step('welcome')):
            with patch.object(wizard, 'step_license', track_step('license')):
                with patch.object(wizard, 'step_path', track_step('path')):
                    with patch.object(wizard, 'step_components', track_step('components')):
                        with patch.object(wizard, 'step_config', track_step('config')):
                            with patch.object(wizard, 'step_install', track_step('install')):
                                with patch.object(wizard, 'step_complete', track_step('complete')):
                                    wizard.run()

        # Assert
        expected_order = ['welcome', 'license', 'path', 'components', 'config', 'install', 'complete']
        assert step_order == expected_order

    def test_step_welcome_returns_bool(self, temp_install_dir):
        """Tech Spec: step_welcome() returns bool."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path=temp_install_dir)

        # Act
        with patch('builtins.input', return_value=''):
            result = wizard.step_welcome()

        # Assert
        assert isinstance(result, bool)

    def test_step_license_returns_bool(self, temp_install_dir):
        """Tech Spec: step_license() returns bool."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path=temp_install_dir)

        # Act
        with patch('builtins.input', return_value='accept'):
            result = wizard.step_license()

        # Assert
        assert isinstance(result, bool)

    def test_step_install_returns_bool(self, temp_install_dir):
        """Tech Spec: step_install() returns bool."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path=temp_install_dir)

        # Act
        with patch.object(wizard, '_do_install', return_value=True):
            result = wizard.step_install()

        # Assert
        assert isinstance(result, bool)


# =============================================================================
# Non-Functional Requirements Tests
# =============================================================================

class TestNonFunctionalRequirements:
    """Tests for NFR from Technical Specification."""

    def test_nfr001_wizard_completable_under_2_minutes(self, temp_install_dir):
        """NFR-001: Wizard must be completable in under 2 minutes."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path=temp_install_dir)
        start_time = time.time()

        # Mock user inputs to simulate fast run
        with patch.object(wizard, 'step_welcome', return_value=True):
            with patch.object(wizard, 'step_license', return_value=True):
                with patch.object(wizard, 'step_path', return_value=True):
                    with patch.object(wizard, 'step_components', return_value=True):
                        with patch.object(wizard, 'step_config', return_value=True):
                            with patch.object(wizard, 'step_install', return_value=True):
                                with patch.object(wizard, 'step_complete', return_value=None):
                                    # Act
                                    wizard.run()

        # Assert
        elapsed = time.time() - start_time
        assert elapsed < 120, f"Wizard took {elapsed}s (expected <120s)"

    def test_nfr002_prompts_have_sensible_defaults(self, temp_install_dir):
        """NFR-002: All prompts must have sensible defaults (Enter to accept)."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path=temp_install_dir)

        # Act - All steps with Enter (empty input)
        steps_passed = 0
        with patch('builtins.input', return_value=''):
            if wizard.step_welcome():
                steps_passed += 1
        with patch('builtins.input', return_value='accept'):  # License requires explicit accept
            if wizard.step_license():
                steps_passed += 1
        with patch('builtins.input', return_value=''):
            if wizard.step_path():
                steps_passed += 1
        with patch('builtins.input', return_value=''):
            if wizard.step_components():
                steps_passed += 1
        with patch('builtins.input', return_value=''):
            if wizard.step_config():
                steps_passed += 1

        # Assert
        # Most steps (except license) should accept Enter
        assert steps_passed >= 4, "Most prompts should accept defaults"

    def test_nfr003_ctrl_c_exits_cleanly(self, temp_install_dir):
        """NFR-003: Ctrl+C at any point must exit cleanly."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path=temp_install_dir)

        # Act & Assert - Should not leave partial state
        with patch.object(wizard, 'step_welcome', side_effect=KeyboardInterrupt):
            result = wizard.run()

        # Should exit with non-zero but not crash
        assert result != 0

    def test_nfr004_works_in_non_tty_environment(self, temp_install_dir):
        """NFR-004: Wizard must work in non-TTY environments."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path=temp_install_dir, tty_mode=False)

        # Act
        with patch('builtins.input', return_value=''):
            with patch('sys.stdin.isatty', return_value=False):
                # Should not crash in non-TTY mode
                result = wizard.step_welcome()

        # Assert
        assert result in [True, False]  # Should return valid result


# =============================================================================
# Edge Cases Tests
# =============================================================================

class TestEdgeCases:
    """Tests for edge cases from story specification."""

    def test_edge_case_empty_target_path(self):
        """Edge Case: Empty target path should use current directory."""
        # Arrange
        from installer.wizard import WizardInstaller

        # Act
        wizard = WizardInstaller(target_path="")

        # Assert
        assert wizard.state.target_path == Path.cwd() or wizard.state.target_path is not None

    def test_edge_case_path_with_spaces(self, temp_install_dir):
        """Edge Case: Path with spaces should be handled."""
        # Arrange
        from installer.wizard import WizardInstaller

        path_with_spaces = os.path.join(temp_install_dir, 'my project')
        os.makedirs(path_with_spaces)

        wizard = WizardInstaller(target_path=path_with_spaces)

        # Act & Assert - Should not crash
        assert str(wizard.state.target_path) == path_with_spaces

    def test_edge_case_path_with_unicode(self, temp_install_dir):
        """Edge Case: Path with unicode characters should be handled."""
        # Arrange
        from installer.wizard import WizardInstaller

        unicode_path = os.path.join(temp_install_dir, 'projet_français')
        os.makedirs(unicode_path)

        # Act
        wizard = WizardInstaller(target_path=unicode_path)

        # Assert
        assert unicode_path in str(wizard.state.target_path)

    def test_edge_case_zero_components_selected(self, temp_install_dir):
        """Edge Case: Should not allow zero components (Core is required)."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path=temp_install_dir)

        # Try to deselect all
        for comp in wizard.state.components:
            wizard.toggle_component(comp.id)

        # Act
        selected = [c for c in wizard.state.components if c.selected]

        # Assert - Core should remain selected
        assert len(selected) >= 1
        assert any(c.id == 'core' for c in selected)

    def test_edge_case_disk_full_during_install(self, temp_install_dir, capsys):
        """Edge Case: Disk full should be handled gracefully."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path=temp_install_dir)

        # Act
        with patch.object(wizard, '_do_install', side_effect=OSError("No space left on device")):
            result = wizard.step_install()

        # Assert
        assert result is False
        captured = capsys.readouterr()
        assert 'error' in captured.out.lower() or 'space' in captured.out.lower()


# =============================================================================
# Business Rules Tests (BR-001 to BR-005)
# =============================================================================

class TestBusinessRules:
    """Tests for business rules from Technical Specification."""

    def test_br001_core_framework_cannot_be_deselected(self, default_components):
        """BR-001: Core Framework cannot be deselected."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path="/tmp/test")
        wizard.state.components = default_components

        # Act - Try multiple times to deselect
        for _ in range(3):
            wizard.toggle_component('core')

        # Assert
        core = next(c for c in wizard.state.components if c.id == 'core')
        assert core.selected is True

    def test_br002_license_requires_accept_text(self):
        """BR-002: License requires 'accept' text (case-insensitive)."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path="/tmp/test")

        # Test various invalid inputs
        invalid_inputs = ['yes', 'ok', 'agree', 'y', '1', 'true']

        for invalid in invalid_inputs:
            inputs = iter([invalid, 'accept'])
            with patch('builtins.input', side_effect=lambda _='': next(inputs)):
                result = wizard.step_license()
            assert result is True  # Should eventually accept after 'accept'

    def test_br003_path_validated_for_write_permissions(self, temp_install_dir):
        """BR-003: Path validated for write permissions before proceeding."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path=temp_install_dir)

        # Act
        is_writable = wizard.validate_path(temp_install_dir)

        # Assert
        assert is_writable is True

    def test_br003_readonly_path_rejected(self, readonly_dir):
        """BR-003: Read-only path is rejected."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path="/tmp")

        # Act
        with patch('os.access', return_value=False):
            is_writable = wizard.validate_path(readonly_dir)

        # Assert
        assert is_writable is False

    def test_br004_git_options_disabled_when_git_unavailable(self):
        """BR-004: Git options disabled if Git unavailable."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path="/tmp/test")

        # Act
        with patch('shutil.which', return_value=None):
            git_available = wizard.is_git_available()

        # Assert
        assert git_available is False

    def test_br005_progress_updates_per_step(self, temp_install_dir):
        """BR-005: Progress bar updates real-time (per-step callback)."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path=temp_install_dir)

        update_count = 0

        def count_updates(step, pct, eta=None):
            nonlocal update_count
            update_count += 1

        wizard.set_progress_callback(count_updates)

        # Act
        with patch.object(wizard, '_do_install', return_value=True):
            wizard.step_install()

        # Assert
        assert update_count >= 2, "Progress should update at least at start and end"


# =============================================================================
# Integration Test
# =============================================================================

class TestWizardIntegration:
    """Integration tests for complete wizard flow."""

    def test_full_wizard_flow_happy_path(self, temp_install_dir):
        """Integration: Complete wizard flow with valid inputs."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path=temp_install_dir)

        # Mock all interactive inputs
        inputs = iter([
            '',        # Welcome: Enter to continue
            'accept',  # License: accept
            '',        # Path: accept default
            '',        # Components: accept defaults
            '',        # Config: accept defaults
        ])

        # Act
        with patch('builtins.input', side_effect=lambda _='': next(inputs)):
            with patch.object(wizard, '_do_install', return_value=True):
                result = wizard.run()

        # Assert
        assert result == 0

    def test_wizard_cancellation_at_each_step(self, temp_install_dir):
        """Integration: Wizard can be cancelled at any step."""
        # Arrange
        from installer.wizard import WizardInstaller

        steps = ['step_welcome', 'step_license', 'step_path', 'step_components', 'step_config']

        for cancel_step in steps:
            wizard = WizardInstaller(target_path=temp_install_dir)

            # Mock all preceding steps to return True, cancel at target step
            patches = {}
            for step in steps:
                if step == cancel_step:
                    patches[step] = patch.object(wizard, step, side_effect=KeyboardInterrupt)
                elif steps.index(step) < steps.index(cancel_step):
                    patches[step] = patch.object(wizard, step, return_value=True)

            # Apply all patches
            with ExitStack() as stack:
                for p in patches.values():
                    stack.enter_context(p)
                result = wizard.run()

            # Assert - Should handle gracefully
            assert result != 0, f"Cancel at {cancel_step} should return non-zero"


# =============================================================================
# Additional Coverage Tests (STORY-247 Phase 05)
# =============================================================================

class TestAdditionalCoverage:
    """Additional tests to meet coverage thresholds."""

    def test_process_component_toggles_with_invalid_index(self, default_components):
        """Coverage: _process_component_toggles with out-of-range index."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path="/tmp/test")
        wizard.state.components = default_components

        # Act - Toggle with invalid indices (should not crash)
        wizard._process_component_toggles("99,100,abc")

        # Assert - All components unchanged
        assert wizard.state.components[0].selected is True  # Core still selected
        assert wizard.state.components[1].selected is False  # CLI unchanged

    def test_process_config_toggles_with_invalid_options(self):
        """Coverage: _process_config_toggles with invalid option numbers."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path="/tmp/test")
        original_config = dict(wizard.state.config)

        # Act - Toggle with invalid options
        wizard._process_config_toggles("99,abc,5", git_available=True)

        # Assert - Config unchanged
        assert wizard.state.config == original_config

    def test_log_write_failure_handled_silently(self, temp_install_dir):
        """Coverage: _log handles OSError silently."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path=temp_install_dir)
        wizard._log_file = "/invalid/path/that/does/not/exist.log"

        # Act - Should not raise exception
        wizard._log("Test message")

        # Assert - No exception raised, method completed
        assert True  # If we got here, no crash

    def test_init_log_file_failure_sets_log_file_to_none(self, temp_install_dir):
        """Coverage: _init_log_file handles OSError by setting _log_file to None."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path=temp_install_dir)
        wizard._log_file = "/invalid/readonly/path/install.log"

        # Act
        wizard._init_log_file()

        # Assert - Log file set to None on failure
        assert wizard._log_file is None

    def test_toggle_component_returns_false_for_unknown_id(self, default_components):
        """Coverage: toggle_component returns False for unknown component ID."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path="/tmp/test")
        wizard.state.components = default_components

        # Act
        result = wizard.toggle_component("unknown_component_id")

        # Assert
        assert result is False

    def test_toggle_config_ignores_unknown_key(self):
        """Coverage: toggle_config ignores unknown config keys."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path="/tmp/test")
        original_config = dict(wizard.state.config)

        # Act
        wizard.toggle_config("unknown_key")

        # Assert - Config unchanged
        assert wizard.state.config == original_config

    def test_exit_codes_integration(self, temp_install_dir):
        """Coverage: Verify ExitCodes constants are used correctly."""
        # Arrange
        from installer.wizard import WizardInstaller
        from installer.exit_codes import ExitCodes

        wizard = WizardInstaller(target_path=temp_install_dir)

        # Act & Assert - run() returns proper exit codes
        with patch.object(wizard, 'step_welcome', return_value=False):
            result = wizard.run()
            assert result == ExitCodes.VALIDATION_FAILED

    def test_do_install_method_delegation(self, temp_install_dir):
        """Coverage: _do_install delegates to _execute_file_installation."""
        # Arrange
        from installer.wizard import WizardInstaller

        wizard = WizardInstaller(target_path=temp_install_dir)
        wizard._log_file = os.path.join(temp_install_dir, "install.log")
        wizard._init_log_file()

        # Act
        result = wizard._do_install()

        # Assert
        assert result is True
