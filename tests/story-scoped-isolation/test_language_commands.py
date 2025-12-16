"""
Test language-specific command generation for story-scoped test isolation.

Tests AC#4: Multi-Language Test Command Generation
- pytest command with story-scoped paths
- jest command with story-scoped paths
- dotnet command with story-scoped paths
- go test command with story-scoped paths
"""
import pytest


def generate_test_command(
    language: str,
    story_id: str,
    config: dict,
    test_path: str = "."
) -> str:
    """
    Generate test command with story-scoped output paths.

    Args:
        language: Programming language (python, javascript, dotnet, go, java, rust)
        story_id: Story identifier (e.g., "STORY-092")
        config: Test isolation configuration
        test_path: Path to tests (default: current directory)

    Returns:
        Complete test command with story-scoped output paths
    """
    paths = config.get("paths", {})
    results_base = paths.get("results_base", "tests/results")
    coverage_base = paths.get("coverage_base", "tests/coverage")

    results_dir = f"{results_base}/{story_id}"
    coverage_dir = f"{coverage_base}/{story_id}"

    language_outputs = config.get("language_outputs", {})
    lang_config = language_outputs.get(language, {})

    commands = {
        "python": (
            f"pytest {test_path} "
            f"--cov=src "
            f"--cov-report=json:{coverage_dir}/{lang_config.get('coverage_file', 'coverage.json')} "
            f"--junitxml={results_dir}/{lang_config.get('results_file', 'test-results.xml')}"
        ),
        "javascript": (
            f"npm test -- "
            f"--coverage "
            f"--coverageDirectory={coverage_dir} "
            f"--outputFile={results_dir}/{lang_config.get('results_file', 'test-results.json')}"
        ),
        "dotnet": (
            f"dotnet test {test_path} "
            f'--collect:"XPlat Code Coverage" '
            f"--results-directory={results_dir}"
        ),
        "go": (
            f"go test {test_path} "
            f"-coverprofile={coverage_dir}/{lang_config.get('coverage_file', 'coverage.out')} "
            f"-json > {results_dir}/{lang_config.get('results_file', 'test-results.json')}"
        ),
        "java": (
            f"mvn test jacoco:report "
            f"-Djacoco.destFile={coverage_dir}/{lang_config.get('coverage_file', 'jacoco.exec')} "
            f"-Dsurefire.reportsDirectory={results_dir}"
        ),
        "rust": (
            f"cargo tarpaulin "
            f"--out Json "
            f"--output-dir {coverage_dir}"
        )
    }

    if language not in commands:
        raise ValueError(f"Unsupported language: {language}")

    return commands[language]


class TestPythonCommands:
    """Tests for Python/pytest command generation."""

    @pytest.fixture
    def default_config(self):
        return {
            "paths": {
                "results_base": "tests/results",
                "coverage_base": "tests/coverage"
            },
            "language_outputs": {
                "python": {
                    "coverage_file": "coverage.json",
                    "results_file": "test-results.xml"
                }
            }
        }

    def test_pytest_command_includes_junitxml(self, default_config):
        """Test: pytest command includes --junitxml=tests/results/{STORY_ID}/."""
        # Given: Story ID
        story_id = "STORY-092"

        # When: Generating command
        command = generate_test_command("python", story_id, default_config)

        # Then: Command includes story-scoped junitxml path
        assert "--junitxml=tests/results/STORY-092/test-results.xml" in command

    def test_pytest_command_includes_coverage(self, default_config):
        """Test: pytest command includes --cov-report with story path."""
        # Given: Story ID
        story_id = "STORY-092"

        # When: Generating command
        command = generate_test_command("python", story_id, default_config)

        # Then: Command includes story-scoped coverage path
        assert "--cov-report=json:tests/coverage/STORY-092/coverage.json" in command


class TestJavaScriptCommands:
    """Tests for JavaScript/jest command generation."""

    @pytest.fixture
    def default_config(self):
        return {
            "paths": {
                "results_base": "tests/results",
                "coverage_base": "tests/coverage"
            },
            "language_outputs": {
                "javascript": {
                    "coverage_file": "coverage-summary.json",
                    "results_file": "test-results.json"
                }
            }
        }

    def test_jest_command_includes_coverage_directory(self, default_config):
        """Test: jest command includes --coverageDirectory=tests/coverage/{STORY_ID}/."""
        # Given: Story ID
        story_id = "STORY-092"

        # When: Generating command
        command = generate_test_command("javascript", story_id, default_config)

        # Then: Command includes story-scoped coverage directory
        assert "--coverageDirectory=tests/coverage/STORY-092" in command

    def test_jest_command_includes_output_file(self, default_config):
        """Test: jest command includes --outputFile with story path."""
        # Given: Story ID
        story_id = "STORY-092"

        # When: Generating command
        command = generate_test_command("javascript", story_id, default_config)

        # Then: Command includes story-scoped output file
        assert "--outputFile=tests/results/STORY-092/test-results.json" in command


class TestDotNetCommands:
    """Tests for .NET/dotnet test command generation."""

    @pytest.fixture
    def default_config(self):
        return {
            "paths": {
                "results_base": "tests/results",
                "coverage_base": "tests/coverage"
            },
            "language_outputs": {
                "dotnet": {
                    "coverage_file": "coverage.cobertura.xml",
                    "results_file": "test-results.trx"
                }
            }
        }

    def test_dotnet_command_includes_results_directory(self, default_config):
        """Test: dotnet command includes --results-directory=tests/results/{STORY_ID}/."""
        # Given: Story ID
        story_id = "STORY-092"

        # When: Generating command
        command = generate_test_command("dotnet", story_id, default_config)

        # Then: Command includes story-scoped results directory
        assert "--results-directory=tests/results/STORY-092" in command

    def test_dotnet_command_includes_coverage_collector(self, default_config):
        """Test: dotnet command includes XPlat Code Coverage collector."""
        # Given: Story ID
        story_id = "STORY-092"

        # When: Generating command
        command = generate_test_command("dotnet", story_id, default_config)

        # Then: Command includes coverage collector
        assert '--collect:"XPlat Code Coverage"' in command


class TestGoCommands:
    """Tests for Go test command generation."""

    @pytest.fixture
    def default_config(self):
        return {
            "paths": {
                "results_base": "tests/results",
                "coverage_base": "tests/coverage"
            },
            "language_outputs": {
                "go": {
                    "coverage_file": "coverage.out",
                    "results_file": "test-results.json"
                }
            }
        }

    def test_go_command_includes_coverprofile(self, default_config):
        """Test: go test includes -coverprofile=tests/coverage/{STORY_ID}/."""
        # Given: Story ID
        story_id = "STORY-092"

        # When: Generating command
        command = generate_test_command("go", story_id, default_config)

        # Then: Command includes story-scoped coverage profile
        assert "-coverprofile=tests/coverage/STORY-092/coverage.out" in command

    def test_go_command_includes_json_output(self, default_config):
        """Test: go test includes -json output redirection."""
        # Given: Story ID
        story_id = "STORY-092"

        # When: Generating command
        command = generate_test_command("go", story_id, default_config)

        # Then: Command includes JSON output to story-scoped path
        assert "-json > tests/results/STORY-092/test-results.json" in command


class TestCustomConfiguration:
    """Tests for custom path configuration."""

    def test_custom_base_paths_used(self):
        """Test: Custom base paths override defaults."""
        # Given: Custom configuration
        config = {
            "paths": {
                "results_base": "output/results",
                "coverage_base": "output/coverage"
            },
            "language_outputs": {
                "python": {
                    "coverage_file": "cov.json",
                    "results_file": "results.xml"
                }
            }
        }

        # When: Generating command
        command = generate_test_command("python", "STORY-001", config)

        # Then: Custom paths used
        assert "output/results/STORY-001" in command
        assert "output/coverage/STORY-001" in command

    def test_unsupported_language_raises_error(self):
        """Test: Unsupported language raises ValueError."""
        # Given: Unsupported language
        config = {"paths": {}}

        # When/Then: ValueError raised
        with pytest.raises(ValueError, match="Unsupported language"):
            generate_test_command("cobol", "STORY-001", config)
