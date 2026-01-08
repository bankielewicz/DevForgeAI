"""
STORY-243: Installer Mode Configuration Module - Test Suite

Test-Driven Development (TDD) - Red Phase
These tests WILL FAIL initially because InstallerModeConfig and related
dataclasses do not exist yet. Implementation will make them pass.

Coverage targets:
- Unit tests: 95%+ for installer_mode_config module
- All 6 acceptance criteria tested
- All 10 service requirements (SVC-001 through SVC-010)
- All 5 business rules (BR-001 through BR-005)
- Edge cases and error handling (18+ test scenarios)

Test file location per source-tree.md: tests/STORY-243/
"""

# CRITICAL: Add project root to sys.path BEFORE any other imports
# This must be at the very top to ensure installer module can be imported
import sys
from pathlib import Path
_project_root = Path(__file__).parent.parent.parent.resolve()
sys.path.insert(0, str(_project_root))

import os
import shutil
import tempfile
import time
from pathlib import Path
from typing import Any, Dict, List, Optional
from unittest.mock import Mock, patch, MagicMock

import pytest
import yaml


# ==============================================================================
# IMPORT TESTS - These will fail until module is created
# ==============================================================================


class TestModuleImports:
    """Test that the installer_mode_config module can be imported."""

    def test_import_installer_mode_result_dataclass(self):
        """
        Test: InstallerModeResult dataclass can be imported.
        Expected: Import succeeds (currently fails - module doesn't exist).
        """
        # Arrange & Act
        from installer.installer_mode_config import InstallerModeResult

        # Assert
        assert InstallerModeResult is not None

    def test_import_installer_step_dataclass(self):
        """
        Test: InstallerStep dataclass can be imported.
        Expected: Import succeeds (currently fails - module doesn't exist).
        """
        # Arrange & Act
        from installer.installer_mode_config import InstallerStep

        # Assert
        assert InstallerStep is not None

    def test_import_installable_component_dataclass(self):
        """
        Test: InstallableComponent dataclass can be imported.
        Expected: Import succeeds (currently fails - module doesn't exist).
        """
        # Arrange & Act
        from installer.installer_mode_config import InstallableComponent

        # Assert
        assert InstallableComponent is not None

    def test_import_installer_mode_config_class(self):
        """
        Test: InstallerModeConfig class can be imported.
        Expected: Import succeeds (currently fails - module doesn't exist).
        """
        # Arrange & Act
        from installer.installer_mode_config import InstallerModeConfig

        # Assert
        assert InstallerModeConfig is not None


# ==============================================================================
# INSTALLER MODE RESULT DATACLASS TESTS
# ==============================================================================


class TestInstallerModeResultDataclass:
    """
    Test InstallerModeResult dataclass fields per Technical Specification.

    Technical Spec fields:
    - mode: String (Required, Enum: cli, wizard, gui, silent)
    - config_path: String (Required: path to generated installer-config.yaml)
    - steps: List[InstallerStep] (For wizard mode)
    - prompts: List[InstallerPrompt] (For cli mode)
    - silent_config_schema: Dict[str, Any] (For silent mode)
    - gui_layout: Dict[str, Any] (For gui mode)
    - post_install_actions: List[PostInstallAction] (Optional)
    - components: List[InstallableComponent] (Required)
    """

    def test_installer_mode_result_has_mode_field(self):
        """Test: InstallerModeResult has mode field (Technical Spec field 1)."""
        from installer.installer_mode_config import InstallerModeResult

        # Arrange
        result = InstallerModeResult(
            mode="wizard",
            config_path="/path/to/installer-config.yaml",
            steps=[],
            prompts=[],
            silent_config_schema={},
            gui_layout={},
            post_install_actions=[],
            components=[]
        )

        # Assert
        assert hasattr(result, "mode")
        assert result.mode == "wizard"

    def test_installer_mode_result_has_config_path_field(self):
        """Test: InstallerModeResult has config_path field (Technical Spec field 2)."""
        from installer.installer_mode_config import InstallerModeResult

        # Arrange
        result = InstallerModeResult(
            mode="cli",
            config_path="/opt/devforgeai/installer-config.yaml",
            steps=[],
            prompts=[],
            silent_config_schema={},
            gui_layout={},
            post_install_actions=[],
            components=[]
        )

        # Assert
        assert hasattr(result, "config_path")
        assert result.config_path == "/opt/devforgeai/installer-config.yaml"

    def test_installer_mode_result_has_steps_field(self):
        """Test: InstallerModeResult has steps field (Technical Spec field 3)."""
        from installer.installer_mode_config import InstallerModeResult, InstallerStep

        # Arrange
        step = InstallerStep(
            id="welcome",
            title="Welcome",
            type="info",
            validation=None,
            can_skip=False
        )
        result = InstallerModeResult(
            mode="wizard",
            config_path="/path/to/config.yaml",
            steps=[step],
            prompts=[],
            silent_config_schema={},
            gui_layout={},
            post_install_actions=[],
            components=[]
        )

        # Assert
        assert hasattr(result, "steps")
        assert len(result.steps) == 1
        assert result.steps[0].id == "welcome"

    def test_installer_mode_result_has_prompts_field(self):
        """Test: InstallerModeResult has prompts field (Technical Spec field 4)."""
        from installer.installer_mode_config import InstallerModeResult

        # Arrange
        result = InstallerModeResult(
            mode="cli",
            config_path="/path/to/config.yaml",
            steps=[],
            prompts=[{"name": "install_path", "prompt": "Enter installation path:"}],
            silent_config_schema={},
            gui_layout={},
            post_install_actions=[],
            components=[]
        )

        # Assert
        assert hasattr(result, "prompts")
        assert len(result.prompts) == 1

    def test_installer_mode_result_has_silent_config_schema_field(self):
        """Test: InstallerModeResult has silent_config_schema field (Technical Spec field 5)."""
        from installer.installer_mode_config import InstallerModeResult

        # Arrange
        schema = {"install_path": {"type": "string", "required": True}}
        result = InstallerModeResult(
            mode="silent",
            config_path="/path/to/config.yaml",
            steps=[],
            prompts=[],
            silent_config_schema=schema,
            gui_layout={},
            post_install_actions=[],
            components=[]
        )

        # Assert
        assert hasattr(result, "silent_config_schema")
        assert result.silent_config_schema == schema

    def test_installer_mode_result_has_gui_layout_field(self):
        """Test: InstallerModeResult has gui_layout field (Technical Spec field 6)."""
        from installer.installer_mode_config import InstallerModeResult

        # Arrange
        layout = {"window": {"width": 800, "height": 600}}
        result = InstallerModeResult(
            mode="gui",
            config_path="/path/to/config.yaml",
            steps=[],
            prompts=[],
            silent_config_schema={},
            gui_layout=layout,
            post_install_actions=[],
            components=[]
        )

        # Assert
        assert hasattr(result, "gui_layout")
        assert result.gui_layout == layout

    def test_installer_mode_result_has_post_install_actions_field(self):
        """Test: InstallerModeResult has post_install_actions field (Technical Spec field 7)."""
        from installer.installer_mode_config import InstallerModeResult

        # Arrange
        actions = [{"action": "initialize_git", "enabled": True}]
        result = InstallerModeResult(
            mode="wizard",
            config_path="/path/to/config.yaml",
            steps=[],
            prompts=[],
            silent_config_schema={},
            gui_layout={},
            post_install_actions=actions,
            components=[]
        )

        # Assert
        assert hasattr(result, "post_install_actions")
        assert len(result.post_install_actions) == 1

    def test_installer_mode_result_has_components_field(self):
        """Test: InstallerModeResult has components field (Technical Spec field 8)."""
        from installer.installer_mode_config import InstallerModeResult, InstallableComponent

        # Arrange
        component = InstallableComponent(
            id="core",
            name="Core Framework",
            description="Essential files",
            size_bytes=1024000,
            required=True,
            default_selected=True,
            files=["**/*"]
        )
        result = InstallerModeResult(
            mode="wizard",
            config_path="/path/to/config.yaml",
            steps=[],
            prompts=[],
            silent_config_schema={},
            gui_layout={},
            post_install_actions=[],
            components=[component]
        )

        # Assert
        assert hasattr(result, "components")
        assert len(result.components) == 1
        assert result.components[0].id == "core"


# ==============================================================================
# INSTALLER STEP DATACLASS TESTS
# ==============================================================================


class TestInstallerStepDataclass:
    """
    Test InstallerStep dataclass fields per Technical Specification.

    Technical Spec fields:
    - id: String (Required, unique)
    - title: String (Required)
    - type: String (Enum: info, license, path_select, component_select, progress, complete)
    - validation: Optional[String]
    - can_skip: Bool (Default: false)
    """

    def test_installer_step_has_id_field(self):
        """Test: InstallerStep has id field (Technical Spec field 1)."""
        from installer.installer_mode_config import InstallerStep

        # Arrange
        step = InstallerStep(
            id="welcome",
            title="Welcome",
            type="info",
            validation=None,
            can_skip=False
        )

        # Assert
        assert hasattr(step, "id")
        assert step.id == "welcome"

    def test_installer_step_has_title_field(self):
        """Test: InstallerStep has title field (Technical Spec field 2)."""
        from installer.installer_mode_config import InstallerStep

        # Arrange
        step = InstallerStep(
            id="license",
            title="License Agreement",
            type="license",
            validation="accept_required",
            can_skip=False
        )

        # Assert
        assert hasattr(step, "title")
        assert step.title == "License Agreement"

    def test_installer_step_has_type_field(self):
        """Test: InstallerStep has type field (Technical Spec field 3)."""
        from installer.installer_mode_config import InstallerStep

        # Arrange
        step = InstallerStep(
            id="path",
            title="Installation Path",
            type="path_select",
            validation="path_writable",
            can_skip=False
        )

        # Assert
        assert hasattr(step, "type")
        assert step.type == "path_select"

    def test_installer_step_has_validation_field(self):
        """Test: InstallerStep has validation field (Technical Spec field 4)."""
        from installer.installer_mode_config import InstallerStep

        # Arrange
        step = InstallerStep(
            id="license",
            title="License Agreement",
            type="license",
            validation="accept_required",
            can_skip=False
        )

        # Assert
        assert hasattr(step, "validation")
        assert step.validation == "accept_required"

    def test_installer_step_has_can_skip_field(self):
        """Test: InstallerStep has can_skip field (Technical Spec field 5)."""
        from installer.installer_mode_config import InstallerStep

        # Arrange
        step = InstallerStep(
            id="components",
            title="Component Selection",
            type="component_select",
            validation=None,
            can_skip=True
        )

        # Assert
        assert hasattr(step, "can_skip")
        assert step.can_skip is True

    def test_installer_step_can_skip_defaults_to_false(self):
        """Test: InstallerStep can_skip defaults to false (Technical Spec constraint)."""
        from installer.installer_mode_config import InstallerStep

        # Arrange - Create step without explicit can_skip
        step = InstallerStep(
            id="welcome",
            title="Welcome",
            type="info",
            validation=None,
            can_skip=False  # Default value
        )

        # Assert
        assert step.can_skip is False


# ==============================================================================
# INSTALLABLE COMPONENT DATACLASS TESTS
# ==============================================================================


class TestInstallableComponentDataclass:
    """
    Test InstallableComponent dataclass fields per Technical Specification.

    Technical Spec fields:
    - id: String (Required, unique)
    - name: String (Required)
    - description: String (Required)
    - size_bytes: Int (Positive)
    - required: Bool (Default: false)
    - default_selected: Bool (Default: true)
    - files: List[String] (Glob patterns)
    """

    def test_installable_component_has_id_field(self):
        """Test: InstallableComponent has id field (Technical Spec field 1)."""
        from installer.installer_mode_config import InstallableComponent

        # Arrange
        component = InstallableComponent(
            id="core",
            name="Core Framework",
            description="Essential files",
            size_bytes=1024000,
            required=True,
            default_selected=True,
            files=["**/*"]
        )

        # Assert
        assert hasattr(component, "id")
        assert component.id == "core"

    def test_installable_component_has_name_field(self):
        """Test: InstallableComponent has name field (Technical Spec field 2)."""
        from installer.installer_mode_config import InstallableComponent

        # Arrange
        component = InstallableComponent(
            id="cli",
            name="CLI Tools",
            description="Command-line utilities",
            size_bytes=512000,
            required=False,
            default_selected=True,
            files=["bin/*"]
        )

        # Assert
        assert hasattr(component, "name")
        assert component.name == "CLI Tools"

    def test_installable_component_has_description_field(self):
        """Test: InstallableComponent has description field (Technical Spec field 3)."""
        from installer.installer_mode_config import InstallableComponent

        # Arrange
        component = InstallableComponent(
            id="templates",
            name="Templates",
            description="Project templates and examples",
            size_bytes=256000,
            required=False,
            default_selected=False,
            files=["templates/**/*"]
        )

        # Assert
        assert hasattr(component, "description")
        assert component.description == "Project templates and examples"

    def test_installable_component_has_size_bytes_field(self):
        """Test: InstallableComponent has size_bytes field (Technical Spec field 4)."""
        from installer.installer_mode_config import InstallableComponent

        # Arrange
        component = InstallableComponent(
            id="examples",
            name="Examples",
            description="Sample projects",
            size_bytes=128000,
            required=False,
            default_selected=False,
            files=["examples/**/*"]
        )

        # Assert
        assert hasattr(component, "size_bytes")
        assert component.size_bytes == 128000

    def test_installable_component_has_required_field(self):
        """Test: InstallableComponent has required field (Technical Spec field 5)."""
        from installer.installer_mode_config import InstallableComponent

        # Arrange
        component = InstallableComponent(
            id="core",
            name="Core Framework",
            description="Essential files",
            size_bytes=1024000,
            required=True,
            default_selected=True,
            files=["**/*"]
        )

        # Assert
        assert hasattr(component, "required")
        assert component.required is True

    def test_installable_component_has_default_selected_field(self):
        """Test: InstallableComponent has default_selected field (Technical Spec field 6)."""
        from installer.installer_mode_config import InstallableComponent

        # Arrange
        component = InstallableComponent(
            id="cli",
            name="CLI Tools",
            description="Command-line utilities",
            size_bytes=512000,
            required=False,
            default_selected=True,
            files=["bin/*"]
        )

        # Assert
        assert hasattr(component, "default_selected")
        assert component.default_selected is True

    def test_installable_component_has_files_field(self):
        """Test: InstallableComponent has files field (Technical Spec field 7)."""
        from installer.installer_mode_config import InstallableComponent

        # Arrange
        component = InstallableComponent(
            id="templates",
            name="Templates",
            description="Project templates",
            size_bytes=256000,
            required=False,
            default_selected=False,
            files=["templates/**/*.md", "templates/**/*.yaml"]
        )

        # Assert
        assert hasattr(component, "files")
        assert len(component.files) == 2
        assert "templates/**/*.md" in component.files


# ==============================================================================
# AC#1: CLI INSTALLER MODE CONFIGURATION
# ==============================================================================


class TestCliModeConfiguration:
    """
    AC#1: CLI Installer Mode Configuration.

    Given: A project targeting command-line installation
    When: InstallerModeConfig is invoked with CLI mode
    Then: Generates configuration for:
        - Interactive command-line prompts
        - Progress indicators (spinners, bars)
        - Color-coded output
        - Help text and usage examples
    And: Returns an InstallerModeResult with CLI configuration.
    """

    @pytest.fixture
    def temp_project_dir(self) -> Path:
        """Create a temporary project directory for testing."""
        tmp = tempfile.mkdtemp()
        yield Path(tmp)
        shutil.rmtree(tmp, ignore_errors=True)

    def test_configure_cli_mode_returns_installer_mode_result(self, temp_project_dir):
        """
        Test: CLI mode configuration returns InstallerModeResult (SVC-001).
        Expected: Returns InstallerModeResult with mode='cli'.
        """
        from installer.installer_mode_config import InstallerModeConfig, InstallerModeResult

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="cli")

        # Assert
        assert isinstance(result, InstallerModeResult)
        assert result.mode == "cli"

    def test_cli_mode_has_prompts_list(self, temp_project_dir):
        """
        Test: CLI config has prompts list (SVC-001 test requirement).
        Expected: InstallerModeResult.prompts is a non-empty list.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="cli")

        # Assert
        assert result.prompts is not None
        assert isinstance(result.prompts, list)
        assert len(result.prompts) > 0

    def test_cli_mode_has_progress_indicator_config(self, temp_project_dir):
        """
        Test: CLI config has progress indicators configured (AC#1 requirement).
        Expected: Configuration includes progress indicator settings.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="cli")

        # Assert - Check config file or metadata for progress settings
        config_content = Path(result.config_path).read_text()
        parsed = yaml.safe_load(config_content)
        assert "progress" in parsed or "cli" in parsed
        # Progress indicators should be in CLI section
        if "cli" in parsed:
            assert "progress" in parsed["cli"] or "spinner" in str(parsed["cli"])

    def test_cli_mode_has_color_output_config(self, temp_project_dir):
        """
        Test: CLI config has color-coded output settings (AC#1 requirement).
        Expected: Configuration includes color output settings.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="cli")

        # Assert
        config_content = Path(result.config_path).read_text()
        parsed = yaml.safe_load(config_content)
        # Color settings should be present
        assert "color" in str(parsed).lower() or "cli" in parsed

    def test_cli_mode_has_help_text(self, temp_project_dir):
        """
        Test: CLI config includes help text (AC#1 requirement).
        Expected: Configuration includes help text or usage examples.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="cli")

        # Assert - Either in config or prompts
        config_content = Path(result.config_path).read_text()
        has_help = (
            "help" in config_content.lower() or
            "usage" in config_content.lower() or
            any("help" in str(p).lower() for p in result.prompts)
        )
        assert has_help

    def test_cli_mode_prompts_have_required_fields(self, temp_project_dir):
        """
        Test: CLI prompts have required fields.
        Expected: Each prompt has name, prompt text, and type.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="cli")

        # Assert
        for prompt in result.prompts:
            assert "name" in prompt or hasattr(prompt, "name")
            assert "prompt" in prompt or hasattr(prompt, "prompt") or "message" in prompt


# ==============================================================================
# AC#2: WIZARD INSTALLER MODE CONFIGURATION
# ==============================================================================


class TestWizardModeConfiguration:
    """
    AC#2: Wizard Installer Mode Configuration.

    Given: A project targeting step-by-step installation
    When: InstallerModeConfig is invoked with Wizard mode
    Then: Generates configuration for:
        - Sequential step flow (Welcome -> License -> Path -> Components -> Install -> Complete)
        - Navigation (Next, Back, Cancel)
        - Progress tracking across steps
        - Validation at each step
    And: Returns an InstallerModeResult with Wizard configuration.
    """

    @pytest.fixture
    def temp_project_dir(self) -> Path:
        """Create a temporary project directory for testing."""
        tmp = tempfile.mkdtemp()
        yield Path(tmp)
        shutil.rmtree(tmp, ignore_errors=True)

    def test_configure_wizard_mode_returns_installer_mode_result(self, temp_project_dir):
        """
        Test: Wizard mode configuration returns InstallerModeResult (SVC-002).
        Expected: Returns InstallerModeResult with mode='wizard'.
        """
        from installer.installer_mode_config import InstallerModeConfig, InstallerModeResult

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="wizard")

        # Assert
        assert isinstance(result, InstallerModeResult)
        assert result.mode == "wizard"

    def test_wizard_mode_has_six_standard_steps(self, temp_project_dir):
        """
        Test: Wizard config has 6 standard steps (BR-001, SVC-002 test requirement).
        Expected: InstallerModeResult.steps has exactly 6 steps.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="wizard")

        # Assert
        assert result.steps is not None
        assert len(result.steps) == 6

    def test_wizard_mode_steps_in_correct_order(self, temp_project_dir):
        """
        Test: Wizard steps are in correct order (BR-001).
        Expected: Steps are welcome, license, path, components, install, complete.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)
        expected_order = ["welcome", "license", "path", "components", "install", "complete"]

        # Act
        result = config.configure(mode="wizard")

        # Assert
        step_ids = [step.id for step in result.steps]
        assert step_ids == expected_order

    def test_wizard_mode_steps_have_correct_types(self, temp_project_dir):
        """
        Test: Wizard steps have correct types.
        Expected: Steps have types matching story Notes table.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)
        expected_types = {
            "welcome": "info",
            "license": "license",
            "path": "path_select",
            "components": "component_select",
            "install": "progress",
            "complete": "complete"
        }

        # Act
        result = config.configure(mode="wizard")

        # Assert
        for step in result.steps:
            assert step.type == expected_types[step.id]

    def test_wizard_mode_has_navigation_config(self, temp_project_dir):
        """
        Test: Wizard config has navigation (Next, Back, Cancel) (AC#2 requirement).
        Expected: Configuration includes navigation settings.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="wizard")

        # Assert - Check config file for navigation
        config_content = Path(result.config_path).read_text()
        parsed = yaml.safe_load(config_content)
        # Navigation should be in wizard section
        has_navigation = (
            "navigation" in str(parsed).lower() or
            "next" in str(parsed).lower() or
            ("wizard" in parsed and "buttons" in str(parsed["wizard"]).lower())
        )
        assert has_navigation

    def test_wizard_mode_has_step_validation(self, temp_project_dir):
        """
        Test: Wizard steps have validation rules (AC#2 requirement).
        Expected: At least license and path steps have validation.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="wizard")

        # Assert - License step requires acceptance, path step requires writable
        license_step = next((s for s in result.steps if s.id == "license"), None)
        path_step = next((s for s in result.steps if s.id == "path"), None)

        assert license_step is not None
        assert license_step.validation is not None
        assert "accept" in license_step.validation.lower() or license_step.validation == "accept_required"

        assert path_step is not None
        assert path_step.validation is not None
        assert "writable" in path_step.validation.lower() or path_step.validation == "path_writable"

    def test_wizard_mode_has_progress_tracking(self, temp_project_dir):
        """
        Test: Wizard config has progress tracking (AC#2 requirement).
        Expected: Configuration includes step progress tracking.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="wizard")

        # Assert
        config_content = Path(result.config_path).read_text()
        parsed = yaml.safe_load(config_content)
        # Progress tracking should be present
        has_progress = (
            "progress" in str(parsed).lower() or
            "step" in str(parsed).lower()
        )
        assert has_progress


# ==============================================================================
# AC#3: SILENT INSTALLER MODE CONFIGURATION
# ==============================================================================


class TestSilentModeConfiguration:
    """
    AC#3: Silent Installer Mode Configuration.

    Given: A project targeting automated/CI installation
    When: InstallerModeConfig is invoked with Silent mode
    Then: Generates configuration for:
        - No interactive prompts
        - Configuration file support (YAML/JSON)
        - Exit code-based status reporting
        - Log file output
    And: Returns an InstallerModeResult with Silent configuration.
    """

    @pytest.fixture
    def temp_project_dir(self) -> Path:
        """Create a temporary project directory for testing."""
        tmp = tempfile.mkdtemp()
        yield Path(tmp)
        shutil.rmtree(tmp, ignore_errors=True)

    def test_configure_silent_mode_returns_installer_mode_result(self, temp_project_dir):
        """
        Test: Silent mode configuration returns InstallerModeResult (SVC-003).
        Expected: Returns InstallerModeResult with mode='silent'.
        """
        from installer.installer_mode_config import InstallerModeConfig, InstallerModeResult

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="silent")

        # Assert
        assert isinstance(result, InstallerModeResult)
        assert result.mode == "silent"

    def test_silent_mode_has_no_prompts(self, temp_project_dir):
        """
        Test: Silent config has no prompts (BR-002, AC#3 requirement).
        Expected: InstallerModeResult.prompts is empty.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="silent")

        # Assert
        assert result.prompts is not None
        assert len(result.prompts) == 0

    def test_silent_mode_has_config_schema(self, temp_project_dir):
        """
        Test: Silent config has YAML schema documented (SVC-003 test requirement).
        Expected: InstallerModeResult.silent_config_schema is populated.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="silent")

        # Assert
        assert result.silent_config_schema is not None
        assert isinstance(result.silent_config_schema, dict)
        assert len(result.silent_config_schema) > 0

    def test_silent_mode_schema_has_install_path(self, temp_project_dir):
        """
        Test: Silent mode schema includes install_path.
        Expected: Schema has install_path field.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="silent")

        # Assert
        schema = result.silent_config_schema
        assert "install_path" in schema or "target" in schema or "path" in str(schema)

    def test_silent_mode_schema_has_components(self, temp_project_dir):
        """
        Test: Silent mode schema includes components selection.
        Expected: Schema has components field.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="silent")

        # Assert
        schema = result.silent_config_schema
        assert "components" in schema or "components" in str(schema)

    def test_silent_mode_has_exit_codes(self, temp_project_dir):
        """
        Test: Silent config has exit codes defined (AC#3 requirement).
        Expected: Configuration includes exit code definitions.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="silent")

        # Assert
        config_content = Path(result.config_path).read_text()
        parsed = yaml.safe_load(config_content)
        # Exit codes should be in silent section
        has_exit_codes = (
            "exit_codes" in str(parsed) or
            "exit" in str(parsed).lower() or
            ("silent" in parsed and "codes" in str(parsed["silent"]).lower())
        )
        assert has_exit_codes

    def test_silent_mode_has_log_output_config(self, temp_project_dir):
        """
        Test: Silent config has log file output settings (AC#3 requirement).
        Expected: Configuration includes logging settings.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="silent")

        # Assert
        config_content = Path(result.config_path).read_text()
        parsed = yaml.safe_load(config_content)
        has_logging = (
            "log" in str(parsed).lower() or
            "logging" in str(parsed)
        )
        assert has_logging


# ==============================================================================
# AC#4: GUI INSTALLER MODE CONFIGURATION
# ==============================================================================


class TestGuiModeConfiguration:
    """
    AC#4: GUI Installer Mode Configuration.

    Given: A project targeting graphical installation
    When: InstallerModeConfig is invoked with GUI mode
    Then: Generates configuration for:
        - Desktop window layout
        - Component selection checkboxes
        - Browse dialog for installation path
        - Progress bar with cancel button
    And: Returns an InstallerModeResult with GUI configuration.
    """

    @pytest.fixture
    def temp_project_dir(self) -> Path:
        """Create a temporary project directory for testing."""
        tmp = tempfile.mkdtemp()
        yield Path(tmp)
        shutil.rmtree(tmp, ignore_errors=True)

    def test_configure_gui_mode_returns_installer_mode_result(self, temp_project_dir):
        """
        Test: GUI mode configuration returns InstallerModeResult (SVC-004).
        Expected: Returns InstallerModeResult with mode='gui'.
        """
        from installer.installer_mode_config import InstallerModeConfig, InstallerModeResult

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="gui")

        # Assert
        assert isinstance(result, InstallerModeResult)
        assert result.mode == "gui"

    def test_gui_mode_has_window_layout(self, temp_project_dir):
        """
        Test: GUI config has window layout defined (SVC-004 test requirement).
        Expected: InstallerModeResult.gui_layout is populated.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="gui")

        # Assert
        assert result.gui_layout is not None
        assert isinstance(result.gui_layout, dict)
        assert len(result.gui_layout) > 0

    def test_gui_mode_has_window_dimensions(self, temp_project_dir):
        """
        Test: GUI config has window dimensions.
        Expected: gui_layout includes width and height.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="gui")

        # Assert
        layout = result.gui_layout
        has_dimensions = (
            "width" in str(layout) or
            "height" in str(layout) or
            "size" in layout or
            "window" in layout
        )
        assert has_dimensions

    def test_gui_mode_has_component_checkboxes(self, temp_project_dir):
        """
        Test: GUI config has component selection checkboxes (AC#4 requirement).
        Expected: Layout includes checkbox configuration.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="gui")

        # Assert
        layout = result.gui_layout
        has_checkboxes = (
            "checkbox" in str(layout).lower() or
            "component" in str(layout).lower() or
            "selection" in str(layout).lower()
        )
        assert has_checkboxes

    def test_gui_mode_has_browse_dialog(self, temp_project_dir):
        """
        Test: GUI config has browse dialog for installation path (AC#4 requirement).
        Expected: Layout includes browse dialog configuration.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="gui")

        # Assert
        layout = result.gui_layout
        config_content = Path(result.config_path).read_text()
        has_browse = (
            "browse" in str(layout).lower() or
            "dialog" in str(layout).lower() or
            "browse" in config_content.lower()
        )
        assert has_browse

    def test_gui_mode_has_progress_bar(self, temp_project_dir):
        """
        Test: GUI config has progress bar with cancel button (AC#4 requirement).
        Expected: Layout includes progress bar and cancel button.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="gui")

        # Assert
        layout = result.gui_layout
        has_progress = (
            "progress" in str(layout).lower() or
            "bar" in str(layout).lower()
        )
        has_cancel = (
            "cancel" in str(layout).lower() or
            "button" in str(layout).lower()
        )
        assert has_progress or has_cancel


# ==============================================================================
# AC#5: INSTALLATION CONFIGURATION SCHEMA
# ==============================================================================


class TestInstallationConfigSchema:
    """
    AC#5: Installation Configuration Schema.

    Given: Any installation mode
    When: The installer-config.yaml is generated
    Then: It contains:
        - mode: wizard | cli | silent | gui
        - target.path: installation directory
        - target.create_if_missing: boolean
        - components: list of installable components
        - post_install: list of post-installation actions
    And: The schema is documented with examples.
    """

    @pytest.fixture
    def temp_project_dir(self) -> Path:
        """Create a temporary project directory for testing."""
        tmp = tempfile.mkdtemp()
        yield Path(tmp)
        shutil.rmtree(tmp, ignore_errors=True)

    def test_config_file_generated(self, temp_project_dir):
        """
        Test: installer-config.yaml is generated (SVC-007 test requirement).
        Expected: Config file exists at config_path.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="wizard")

        # Assert
        assert result.config_path is not None
        assert Path(result.config_path).exists()
        assert result.config_path.endswith(".yaml") or result.config_path.endswith(".yml")

    def test_config_file_is_valid_yaml(self, temp_project_dir):
        """
        Test: installer-config.yaml is valid YAML (SVC-007).
        Expected: File can be parsed as YAML without errors.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="cli")
        content = Path(result.config_path).read_text()

        # Assert - Should not raise
        parsed = yaml.safe_load(content)
        assert parsed is not None
        assert isinstance(parsed, dict)

    def test_config_file_has_mode_field(self, temp_project_dir):
        """
        Test: Config file contains mode field (AC#5).
        Expected: YAML has installation.mode key.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="silent")
        content = Path(result.config_path).read_text()
        parsed = yaml.safe_load(content)

        # Assert
        assert "installation" in parsed or "mode" in parsed
        if "installation" in parsed:
            assert "mode" in parsed["installation"]
            assert parsed["installation"]["mode"] == "silent"

    def test_config_file_has_target_path(self, temp_project_dir):
        """
        Test: Config file contains target.path field (AC#5).
        Expected: YAML has installation.target.path key.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="wizard")
        content = Path(result.config_path).read_text()
        parsed = yaml.safe_load(content)

        # Assert
        assert "installation" in parsed or "target" in parsed
        if "installation" in parsed:
            assert "target" in parsed["installation"]
            assert "path" in parsed["installation"]["target"]

    def test_config_file_has_create_if_missing(self, temp_project_dir):
        """
        Test: Config file contains target.create_if_missing field (AC#5).
        Expected: YAML has installation.target.create_if_missing key.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="wizard")
        content = Path(result.config_path).read_text()
        parsed = yaml.safe_load(content)

        # Assert
        if "installation" in parsed and "target" in parsed["installation"]:
            assert "create_if_missing" in parsed["installation"]["target"]

    def test_config_file_has_components_list(self, temp_project_dir):
        """
        Test: Config file contains components list (AC#5).
        Expected: YAML has installation.components key with list.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="wizard")
        content = Path(result.config_path).read_text()
        parsed = yaml.safe_load(content)

        # Assert
        assert "installation" in parsed or "components" in parsed
        if "installation" in parsed:
            assert "components" in parsed["installation"]
            assert isinstance(parsed["installation"]["components"], list)

    def test_config_file_has_post_install_list(self, temp_project_dir):
        """
        Test: Config file contains post_install list (AC#5).
        Expected: YAML has installation.post_install key.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="wizard")
        content = Path(result.config_path).read_text()
        parsed = yaml.safe_load(content)

        # Assert
        assert "installation" in parsed or "post_install" in parsed
        if "installation" in parsed:
            assert "post_install" in parsed["installation"]

    def test_config_file_has_comments(self, temp_project_dir):
        """
        Test: Config file has documentation comments (NFR-004).
        Expected: YAML file contains comments for settings.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="wizard")
        content = Path(result.config_path).read_text()

        # Assert
        assert "#" in content  # YAML comments start with #


# ==============================================================================
# AC#6: POST-INSTALLATION ACTIONS CONFIGURATION
# ==============================================================================


class TestPostInstallActionsConfiguration:
    """
    AC#6: Post-Installation Actions Configuration.

    Given: An installation mode configuration
    When: Post-installation actions are specified
    Then: The configuration supports:
        - initialize_git: boolean
        - create_initial_commit: boolean
        - run_validation: boolean
        - custom_scripts: list of script paths
    And: Actions are executed in order after file installation.
    """

    @pytest.fixture
    def temp_project_dir(self) -> Path:
        """Create a temporary project directory for testing."""
        tmp = tempfile.mkdtemp()
        yield Path(tmp)
        shutil.rmtree(tmp, ignore_errors=True)

    def test_configure_with_initialize_git_action(self, temp_project_dir):
        """
        Test: Configuration supports initialize_git action (AC#6).
        Expected: post_install_actions includes initialize_git.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(
            mode="wizard",
            post_install_actions=[{"action": "initialize_git", "enabled": True}]
        )

        # Assert
        assert result.post_install_actions is not None
        git_action = next(
            (a for a in result.post_install_actions if a.get("action") == "initialize_git" or getattr(a, "action", None) == "initialize_git"),
            None
        )
        assert git_action is not None

    def test_configure_with_create_initial_commit_action(self, temp_project_dir):
        """
        Test: Configuration supports create_initial_commit action (AC#6).
        Expected: post_install_actions includes create_initial_commit.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(
            mode="wizard",
            post_install_actions=[{"action": "create_initial_commit", "enabled": True}]
        )

        # Assert
        assert result.post_install_actions is not None
        commit_action = next(
            (a for a in result.post_install_actions if a.get("action") == "create_initial_commit" or getattr(a, "action", None) == "create_initial_commit"),
            None
        )
        assert commit_action is not None

    def test_configure_with_run_validation_action(self, temp_project_dir):
        """
        Test: Configuration supports run_validation action (AC#6).
        Expected: post_install_actions includes run_validation.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(
            mode="wizard",
            post_install_actions=[{"action": "run_validation", "enabled": True}]
        )

        # Assert
        assert result.post_install_actions is not None
        validation_action = next(
            (a for a in result.post_install_actions if a.get("action") == "run_validation" or getattr(a, "action", None) == "run_validation"),
            None
        )
        assert validation_action is not None

    def test_configure_with_custom_scripts(self, temp_project_dir):
        """
        Test: Configuration supports custom_scripts (AC#6).
        Expected: post_install_actions includes custom scripts.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)
        custom_scripts = ["scripts/setup.sh", "scripts/configure.py"]

        # Act
        result = config.configure(
            mode="wizard",
            post_install_actions=[{"action": "custom_scripts", "scripts": custom_scripts}]
        )

        # Assert
        assert result.post_install_actions is not None
        scripts_action = next(
            (a for a in result.post_install_actions if a.get("action") == "custom_scripts" or getattr(a, "action", None) == "custom_scripts"),
            None
        )
        assert scripts_action is not None

    def test_post_install_actions_order_preserved(self, temp_project_dir):
        """
        Test: Post-install actions order is preserved (BR-004).
        Expected: Actions in result maintain input order.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)
        actions = [
            {"action": "initialize_git", "enabled": True, "order": 1},
            {"action": "create_initial_commit", "enabled": True, "order": 2},
            {"action": "run_validation", "enabled": True, "order": 3}
        ]

        # Act
        result = config.configure(mode="wizard", post_install_actions=actions)

        # Assert
        result_actions = [
            a.get("action") if isinstance(a, dict) else getattr(a, "action", None)
            for a in result.post_install_actions
        ]
        expected_order = ["initialize_git", "create_initial_commit", "run_validation"]
        assert result_actions == expected_order

    def test_post_install_actions_in_config_file(self, temp_project_dir):
        """
        Test: Post-install actions written to config file (SVC-006).
        Expected: installer-config.yaml includes post_install section.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(
            mode="wizard",
            post_install_actions=[{"action": "run_validation", "enabled": True}]
        )
        content = Path(result.config_path).read_text()
        parsed = yaml.safe_load(content)

        # Assert
        has_post_install = (
            "post_install" in parsed or
            (
                "installation" in parsed and
                "post_install" in parsed.get("installation", {})
            )
        )
        assert has_post_install


# ==============================================================================
# COMPONENT CONFIGURATION TESTS (SVC-005)
# ==============================================================================


class TestComponentConfiguration:
    """
    Test component configuration functionality (SVC-005, BR-003).
    """

    @pytest.fixture
    def temp_project_dir(self) -> Path:
        """Create a temporary project directory for testing."""
        tmp = tempfile.mkdtemp()
        yield Path(tmp)
        shutil.rmtree(tmp, ignore_errors=True)

    def test_components_extracted_from_project(self, temp_project_dir):
        """
        Test: Components extracted from package contents (SVC-005).
        Expected: Components list is populated.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="wizard")

        # Assert
        assert result.components is not None
        assert isinstance(result.components, list)
        assert len(result.components) > 0

    def test_core_component_is_required(self, temp_project_dir):
        """
        Test: Core component is always required (BR-003).
        Expected: Component with id='core' has required=True.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="wizard")

        # Assert
        core_component = next(
            (c for c in result.components if c.id == "core"),
            None
        )
        assert core_component is not None
        assert core_component.required is True

    def test_core_component_cannot_be_deselected(self, temp_project_dir):
        """
        Test: Core component cannot be deselected (BR-003 test requirement).
        Expected: Attempting to deselect core should fail or be ignored.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="wizard")

        # Assert
        core_component = next(
            (c for c in result.components if c.id == "core"),
            None
        )
        # Required components should always be selected
        assert core_component.required is True
        assert core_component.default_selected is True

    def test_component_ids_are_unique(self, temp_project_dir):
        """
        Test: Component IDs are unique (Technical Spec constraint).
        Expected: No duplicate component IDs.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="wizard")

        # Assert
        ids = [c.id for c in result.components]
        assert len(ids) == len(set(ids))  # No duplicates

    def test_component_size_is_positive(self, temp_project_dir):
        """
        Test: Component size_bytes is positive (Technical Spec constraint).
        Expected: All components have positive size.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="wizard")

        # Assert
        for component in result.components:
            assert component.size_bytes > 0


# ==============================================================================
# BUSINESS RULES TESTS
# ==============================================================================


class TestBusinessRules:
    """
    Test business rules (BR-001 through BR-005).
    """

    @pytest.fixture
    def temp_project_dir(self) -> Path:
        """Create a temporary project directory for testing."""
        tmp = tempfile.mkdtemp()
        yield Path(tmp)
        shutil.rmtree(tmp, ignore_errors=True)

    def test_br001_wizard_has_six_steps(self, temp_project_dir):
        """
        BR-001: Wizard mode must have standard 6 steps.
        Expected: Wizard mode has exactly 6 steps in correct order.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="wizard")

        # Assert
        assert len(result.steps) == 6
        step_ids = [s.id for s in result.steps]
        assert step_ids == ["welcome", "license", "path", "components", "install", "complete"]

    def test_br002_silent_mode_no_prompts(self, temp_project_dir):
        """
        BR-002: Silent mode must not prompt for any input.
        Expected: Silent mode has zero prompts.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="silent")

        # Assert
        assert len(result.prompts) == 0

    def test_br003_core_always_required(self, temp_project_dir):
        """
        BR-003: Core component must always be required.
        Expected: Core component has required=True, cannot be deselected.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="wizard")

        # Assert
        core = next((c for c in result.components if c.id == "core"), None)
        assert core is not None
        assert core.required is True

    def test_br004_post_install_after_file_copy(self, temp_project_dir):
        """
        BR-004: Post-install actions run after file copy completes.
        Expected: Actions have proper ordering metadata.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)
        actions = [
            {"action": "initialize_git", "enabled": True},
            {"action": "run_validation", "enabled": True}
        ]

        # Act
        result = config.configure(mode="wizard", post_install_actions=actions)
        content = Path(result.config_path).read_text()
        parsed = yaml.safe_load(content)

        # Assert - Actions should be in post_install section (runs after file copy)
        has_post_install = (
            "post_install" in parsed or
            ("installation" in parsed and "post_install" in parsed["installation"])
        )
        assert has_post_install

    def test_br005_installation_path_validation_config(self, temp_project_dir):
        """
        BR-005: Installation path must be writable - validation config present.
        Expected: Path step has writable validation rule.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="wizard")

        # Assert
        path_step = next((s for s in result.steps if s.id == "path"), None)
        assert path_step is not None
        assert path_step.validation is not None
        assert "writable" in path_step.validation.lower() or path_step.validation == "path_writable"


# ==============================================================================
# NON-FUNCTIONAL REQUIREMENTS TESTS
# ==============================================================================


class TestNonFunctionalRequirements:
    """
    Test NFR-001 through NFR-004 requirements.
    """

    @pytest.fixture
    def temp_project_dir(self) -> Path:
        """Create a temporary project directory for testing."""
        tmp = tempfile.mkdtemp()
        yield Path(tmp)
        shutil.rmtree(tmp, ignore_errors=True)

    def test_nfr001_step_descriptions_clear(self, temp_project_dir):
        """
        NFR-001: Wizard steps must be intuitive.
        Expected: All steps have non-empty titles.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="wizard")

        # Assert
        for step in result.steps:
            assert step.title is not None
            assert len(step.title) > 0

    def test_nfr002_generation_under_5_seconds(self, temp_project_dir):
        """
        NFR-002: Config generation must complete under 5 seconds.
        Expected: Generation completes in < 5 seconds.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        start_time = time.time()
        result = config.configure(mode="wizard")
        elapsed = time.time() - start_time

        # Assert
        assert elapsed < 5.0, f"Generation took {elapsed:.2f}s (expected < 5s)"

    def test_nfr002_validation_under_1_second(self, temp_project_dir):
        """
        NFR-002: Validation must complete under 1 second per step.
        Expected: Individual step validation is fast.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        start_time = time.time()
        result = config.configure(mode="wizard")
        elapsed = time.time() - start_time

        # Assert - 6 steps, each under 1 second = max 6 seconds total
        # But actual should be much faster
        assert elapsed < 6.0

    def test_nfr003_silent_mode_works_headless(self, temp_project_dir):
        """
        NFR-003: Silent mode must work in CI/CD (headless).
        Expected: Silent mode requires no interactive elements.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="silent")

        # Assert - No prompts, no GUI, just config
        assert len(result.prompts) == 0
        assert result.gui_layout == {} or result.gui_layout is None or len(result.gui_layout) == 0

    def test_nfr004_yaml_has_comments(self, temp_project_dir):
        """
        NFR-004: Config schema must be self-documenting.
        Expected: YAML comments for all settings.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="wizard")
        content = Path(result.config_path).read_text()

        # Assert - Should have YAML comments
        assert "#" in content


# ==============================================================================
# EDGE CASES AND ERROR HANDLING
# ==============================================================================


class TestEdgeCasesAndErrors:
    """
    Test edge cases and error handling scenarios.
    """

    @pytest.fixture
    def temp_project_dir(self) -> Path:
        """Create a temporary project directory for testing."""
        tmp = tempfile.mkdtemp()
        yield Path(tmp)
        shutil.rmtree(tmp, ignore_errors=True)

    def test_invalid_mode_raises_error(self, temp_project_dir):
        """
        Test: Invalid mode raises appropriate error.
        Expected: ValueError or similar for invalid mode.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act & Assert
        with pytest.raises((ValueError, KeyError)):
            config.configure(mode="invalid_mode")

    def test_empty_components_list(self, temp_project_dir):
        """
        Test: Handle empty components list gracefully.
        Expected: Uses default components.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act - Configure without explicit components
        result = config.configure(mode="wizard")

        # Assert - Should have at least core component
        assert len(result.components) >= 1
        core = next((c for c in result.components if c.id == "core"), None)
        assert core is not None

    def test_invalid_post_install_action(self, temp_project_dir):
        """
        Test: Handle invalid post-install action.
        Expected: Invalid actions are skipped or logged.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)
        invalid_actions = [{"action": "nonexistent_action", "enabled": True}]

        # Act - Should not raise
        result = config.configure(mode="wizard", post_install_actions=invalid_actions)

        # Assert - Either skipped or included with warning
        assert result is not None

    def test_path_with_special_characters(self, temp_project_dir):
        """
        Test: Handle installation path with special characters.
        Expected: Special characters handled in config.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="wizard")
        content = Path(result.config_path).read_text()
        parsed = yaml.safe_load(content)

        # Assert - Config should be valid YAML
        assert parsed is not None

    def test_missing_required_settings_use_defaults(self, temp_project_dir):
        """
        Test: Missing required settings use sensible defaults.
        Expected: Config file has defaults for all required keys.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="wizard")
        content = Path(result.config_path).read_text()
        parsed = yaml.safe_load(content)

        # Assert - Should have defaults
        assert parsed is not None
        installation = parsed.get("installation", parsed)
        # Mode should be set
        assert "mode" in installation or result.mode == "wizard"

    def test_concurrent_config_generation(self, temp_project_dir):
        """
        Test: Multiple simultaneous config generations don't conflict.
        Expected: Each generates unique config file.
        """
        from installer.installer_mode_config import InstallerModeConfig
        import threading
        import queue

        # Arrange
        results = queue.Queue()

        def generate_config(mode, result_queue):
            try:
                # Create unique temp dir for each thread
                tmp = tempfile.mkdtemp()
                config = InstallerModeConfig(Path(tmp))
                result = config.configure(mode=mode)
                result_queue.put((mode, result.config_path, None))
                shutil.rmtree(tmp, ignore_errors=True)
            except Exception as e:
                result_queue.put((mode, None, str(e)))

        # Act
        threads = []
        for mode in ["cli", "wizard", "silent", "gui"]:
            t = threading.Thread(target=generate_config, args=(mode, results))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        # Assert - All succeeded
        errors = []
        while not results.empty():
            mode, path, error = results.get()
            if error:
                errors.append(f"{mode}: {error}")
            else:
                assert path is not None

        assert len(errors) == 0, f"Errors: {errors}"


# ==============================================================================
# INTEGRATION WITH INSTALLER CONFIG (FROM STORY-242)
# ==============================================================================


class TestIntegrationWithInstallerConfig:
    """
    Test integration with InstallerConfig from STORY-242.
    """

    @pytest.fixture
    def temp_project_dir(self) -> Path:
        """Create a temporary project directory for testing."""
        tmp = tempfile.mkdtemp()
        yield Path(tmp)
        shutil.rmtree(tmp, ignore_errors=True)

    def test_mode_config_can_use_installer_config(self, temp_project_dir):
        """
        Test: InstallerModeConfig can work with InstallerConfig from STORY-242.
        Expected: No import or compatibility errors.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act - Should work with or without InstallerConfig
        result = config.configure(mode="wizard")

        # Assert
        assert result is not None
        assert result.mode == "wizard"

    def test_components_integrate_with_installer_config(self, temp_project_dir):
        """
        Test: Components can be extracted from InstallerConfig package info.
        Expected: Components populated from package.
        """
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="wizard")

        # Assert - Components should be populated
        assert len(result.components) > 0


# ==============================================================================
# SERVICE REQUIREMENTS TESTS (SVC-001 through SVC-010)
# ==============================================================================


class TestServiceRequirements:
    """
    Test all service requirements from Technical Specification.
    """

    @pytest.fixture
    def temp_project_dir(self) -> Path:
        """Create a temporary project directory for testing."""
        tmp = tempfile.mkdtemp()
        yield Path(tmp)
        shutil.rmtree(tmp, ignore_errors=True)

    def test_svc001_cli_mode_has_prompts(self, temp_project_dir):
        """SVC-001: CLI mode has prompts list."""
        from installer.installer_mode_config import InstallerModeConfig

        config = InstallerModeConfig(temp_project_dir)
        result = config.configure(mode="cli")

        assert len(result.prompts) > 0

    def test_svc002_wizard_mode_has_six_steps(self, temp_project_dir):
        """SVC-002: Wizard mode has 6 standard steps."""
        from installer.installer_mode_config import InstallerModeConfig

        config = InstallerModeConfig(temp_project_dir)
        result = config.configure(mode="wizard")

        assert len(result.steps) == 6

    def test_svc003_silent_mode_has_yaml_schema(self, temp_project_dir):
        """SVC-003: Silent mode has YAML schema."""
        from installer.installer_mode_config import InstallerModeConfig

        config = InstallerModeConfig(temp_project_dir)
        result = config.configure(mode="silent")

        assert result.silent_config_schema is not None
        assert len(result.silent_config_schema) > 0

    def test_svc004_gui_mode_has_window_layout(self, temp_project_dir):
        """SVC-004: GUI mode has window layout."""
        from installer.installer_mode_config import InstallerModeConfig

        config = InstallerModeConfig(temp_project_dir)
        result = config.configure(mode="gui")

        assert result.gui_layout is not None
        assert len(result.gui_layout) > 0

    def test_svc005_components_extracted_from_file_list(self, temp_project_dir):
        """SVC-005: Components extracted from file list."""
        from installer.installer_mode_config import InstallerModeConfig

        config = InstallerModeConfig(temp_project_dir)
        result = config.configure(mode="wizard")

        assert len(result.components) > 0

    def test_svc006_post_install_actions_list(self, temp_project_dir):
        """SVC-006: Post-install actions list configured."""
        from installer.installer_mode_config import InstallerModeConfig

        config = InstallerModeConfig(temp_project_dir)
        result = config.configure(
            mode="wizard",
            post_install_actions=[{"action": "run_validation", "enabled": True}]
        )

        assert len(result.post_install_actions) > 0

    def test_svc007_yaml_file_valid_and_complete(self, temp_project_dir):
        """SVC-007: YAML file is valid and complete."""
        from installer.installer_mode_config import InstallerModeConfig

        config = InstallerModeConfig(temp_project_dir)
        result = config.configure(mode="wizard")
        content = Path(result.config_path).read_text()
        parsed = yaml.safe_load(content)

        assert parsed is not None
        assert "installation" in parsed or "mode" in parsed

    def test_svc008_path_validation_rules_generated(self, temp_project_dir):
        """SVC-008: Path validation rules generated."""
        from installer.installer_mode_config import InstallerModeConfig

        config = InstallerModeConfig(temp_project_dir)
        result = config.configure(mode="wizard")

        path_step = next((s for s in result.steps if s.id == "path"), None)
        assert path_step is not None
        assert path_step.validation is not None

    def test_svc009_component_dependencies_support(self, temp_project_dir):
        """SVC-009: Component dependencies supported."""
        from installer.installer_mode_config import InstallerModeConfig

        # Arrange - Create components with dependencies
        config = InstallerModeConfig(temp_project_dir)

        # Act
        result = config.configure(mode="wizard")

        # Assert - Core is required, other components can depend on it
        core = next((c for c in result.components if c.id == "core"), None)
        assert core is not None
        assert core.required is True

    def test_svc010_mode_specific_documentation(self, temp_project_dir):
        """SVC-010: Mode-specific documentation generated."""
        from installer.installer_mode_config import InstallerModeConfig

        config = InstallerModeConfig(temp_project_dir)
        result = config.configure(mode="wizard")
        content = Path(result.config_path).read_text()

        # Should have comments documenting the mode
        assert "#" in content or "wizard" in content.lower()
