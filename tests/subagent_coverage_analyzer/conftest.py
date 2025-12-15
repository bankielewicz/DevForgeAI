"""
Shared fixtures for coverage-analyzer subagent tests.

Provides:
- Mock context files (tech-stack.md, source-tree.md, coverage-thresholds.md)
- Mock coverage reports (JSON, XML formats for different languages)
- Mock file structures and classification results
- Test data for threshold validation
"""

import pytest
from pathlib import Path
import tempfile
import json
from typing import Dict, Any


# AC1 Test Fixtures: Subagent specification validation
@pytest.fixture
def subagent_spec_path():
    """Path to coverage-analyzer subagent specification."""
    return Path("/mnt/c/Projects/DevForgeAI2/.claude/agents/coverage-analyzer.md")


@pytest.fixture
def valid_subagent_yaml_frontmatter():
    """Valid YAML frontmatter for coverage-analyzer subagent."""
    return {
        "name": "coverage-analyzer",
        "description": "Test coverage analysis specialist that validates coverage by architectural layer against strict thresholds (95%/85%/80%)",
        "tools": [
            "Read",
            "Grep",
            "Glob",
            "Bash"
        ],
        "model": "claude-haiku-4-5-20251001"
    }


# AC2 Test Fixtures: Language-specific coverage tooling
@pytest.fixture
def language_tool_mapping():
    """Mapping of languages to coverage tools."""
    return {
        "Python": {
            "command": "pytest --cov=src --cov-report=json",
            "report_format": "json",
            "report_file": "coverage.json"
        },
        "C#": {
            "command": "dotnet test --collect:'XPlat Code Coverage'",
            "report_format": "xml",
            "report_file": "coverage.cobertura.xml"
        },
        "Node.js": {
            "command": "npm test -- --coverage",
            "report_format": "json",
            "report_file": "coverage/coverage-final.json"
        },
        "Go": {
            "command": "go test ./... -coverprofile=coverage.out",
            "report_format": "text",
            "report_file": "coverage.out"
        },
        "Rust": {
            "command": "cargo tarpaulin --out Json",
            "report_format": "json",
            "report_file": "coverage.json"
        },
        "Java": {
            "command": "mvn test jacoco:report",
            "report_format": "xml",
            "report_file": "target/site/jacoco/jacoco.xml"
        }
    }


@pytest.fixture
def mock_tech_stack_python():
    """Mock tech-stack.md for Python project."""
    return """# Technology Stack

primary_language: Python
version: 3.9+
testing_framework: pytest
coverage_tool: pytest-cov
"""


@pytest.fixture
def mock_tech_stack_csharp():
    """Mock tech-stack.md for C# project."""
    return """# Technology Stack

primary_language: C#
version: .NET 6.0+
testing_framework: xUnit
coverage_tool: XPlat Code Coverage
"""


@pytest.fixture
def mock_pytest_coverage_report():
    """Mock pytest coverage report (JSON format)."""
    return {
        "meta": {
            "version": "5.5",
            "timestamp": 1234567890,
            "branch_coverage": True
        },
        "totals": {
            "covered_lines": 850,
            "num_statements": 1000,
            "percent_covered": 85.0,
            "percent_covered_display": "85.00",
            "missing_lines": 150,
            "excluded_lines": 0,
            "num_branches": 200,
            "num_partial_branches": 10,
            "covered_branches": 180,
            "missing_branches": 20
        },
        "files": {
            "src/domain/order.py": {
                "executed_lines": [1, 2, 3, 5, 8, 10],
                "missing_lines": [4, 6, 7, 9],
                "excluded_lines": [],
                "line_rate": 0.857,
                "num_statements": 14,
                "num_branches": 4,
                "num_partial_branches": 0,
                "covered_lines": 6,
                "percent_covered": 85.71
            },
            "src/application/service.py": {
                "executed_lines": [1, 2, 3, 5, 8],
                "missing_lines": [4, 6, 7],
                "excluded_lines": [],
                "line_rate": 0.714,
                "num_statements": 10,
                "num_branches": 2,
                "num_partial_branches": 0,
                "covered_lines": 5,
                "percent_covered": 71.43
            },
            "src/infrastructure/repository.py": {
                "executed_lines": [1, 2, 3],
                "missing_lines": [4, 5],
                "excluded_lines": [],
                "line_rate": 0.6,
                "num_statements": 8,
                "num_branches": 1,
                "num_partial_branches": 0,
                "covered_lines": 3,
                "percent_covered": 60.0
            }
        }
    }


# AC3 Test Fixtures: File classification by architectural layer
@pytest.fixture
def mock_source_tree_md():
    """Mock source-tree.md with layer classification patterns."""
    return """# Source Tree Structure

## Architectural Layers

### Business Logic Layer
- src/Domain/**
- src/Core/**
- src/Entities/**
- src/ValueObjects/**

### Application Layer
- src/Application/**
- src/Services/**
- src/UseCases/**
- src/DTOs/**

### Infrastructure Layer
- src/Infrastructure/**
- src/Data/**
- src/Persistence/**
- src/ExternalServices/**
"""


@pytest.fixture
def classified_files():
    """Expected classification of files by layer."""
    return {
        "src/Domain/Order.cs": {
            "layer": "business_logic",
            "coverage": 96.5,
            "uncovered_lines": [25, 42]
        },
        "src/Application/OrderService.cs": {
            "layer": "application",
            "coverage": 82.1,
            "uncovered_lines": [15, 18, 22, 33]
        },
        "src/Infrastructure/OrderRepository.cs": {
            "layer": "infrastructure",
            "coverage": 72.5,
            "uncovered_lines": [10, 12, 20, 24, 28, 31]
        }
    }


# AC4 Test Fixtures: Coverage thresholds and validation
@pytest.fixture
def mock_coverage_thresholds_md():
    """Mock coverage-thresholds.md file."""
    return """# Coverage Thresholds

## Layer Thresholds (Strict)

### Business Logic (CRITICAL)
- Minimum: 95%
- Severity: CRITICAL
- Blocking: true

### Application (HIGH)
- Minimum: 85%
- Severity: HIGH
- Blocking: true

### Infrastructure (MEDIUM)
- Minimum: 80%
- Severity: HIGH
- Blocking: true

### Overall
- Minimum: 80%
- Severity: HIGH
- Blocking: true
"""


@pytest.fixture
def threshold_test_cases():
    """Test cases for threshold validation."""
    return {
        "all_pass": {
            "business_logic": 96.0,
            "application": 87.0,
            "infrastructure": 82.0,
            "overall": 88.0,
            "blocks_qa": False,
            "violations": []
        },
        "business_logic_fails": {
            "business_logic": 93.0,
            "application": 87.0,
            "infrastructure": 82.0,
            "overall": 88.0,
            "blocks_qa": True,
            "violations": [
                {
                    "layer": "business_logic",
                    "severity": "CRITICAL",
                    "message": "Business logic coverage 93.0% below threshold 95%"
                }
            ]
        },
        "application_fails": {
            "business_logic": 96.0,
            "application": 82.0,
            "infrastructure": 82.0,
            "overall": 86.0,
            "blocks_qa": True,
            "violations": [
                {
                    "layer": "application",
                    "severity": "HIGH",
                    "message": "Application coverage 82.0% below threshold 85%"
                }
            ]
        },
        "overall_fails": {
            "business_logic": 96.0,
            "application": 87.0,
            "infrastructure": 72.0,
            "overall": 75.0,
            "blocks_qa": True,
            "violations": [
                {
                    "layer": "overall",
                    "severity": "HIGH",
                    "message": "Overall coverage 75.0% below threshold 80%"
                }
            ]
        }
    }


# AC5 Test Fixtures: Gap identification with evidence
@pytest.fixture
def coverage_gap_example():
    """Example coverage gap with file:line evidence."""
    return {
        "file": "/mnt/c/Projects/MyProject/src/Infrastructure/OrderRepository.cs",
        "layer": "infrastructure",
        "current_coverage": 72.5,
        "target_coverage": 80.0,
        "gap_percentage": 7.5,
        "uncovered_lines": [10, 12, 20, 24, 28, 31],
        "uncovered_ranges": [
            {"start": 10, "end": 12, "count": 2},
            {"start": 20, "end": 20, "count": 1},
            {"start": 24, "end": 24, "count": 1},
            {"start": 28, "end": 31, "count": 4}
        ],
        "suggested_tests": [
            "Test error handling in Execute method (lines 10-12)",
            "Test transaction rollback on exception (line 20)",
            "Test connection retry logic (line 24)",
            "Test batch operations (lines 28-31)"
        ]
    }


# AC6 Test Fixtures: Recommendations
@pytest.fixture
def gap_and_recommendations():
    """Gap data with expected recommendations."""
    return {
        "gaps": [
            {
                "file": "src/Domain/Order.cs",
                "layer": "business_logic",
                "current_coverage": 93.0,
                "target_coverage": 95.0
            },
            {
                "file": "src/Infrastructure/Repository.cs",
                "layer": "infrastructure",
                "current_coverage": 72.5,
                "target_coverage": 80.0
            }
        ],
        "expected_recommendations": [
            "BLOCKING: Business logic gap in src/Domain/Order.cs (93.0%, needs 95%)",
            "Add tests for Order validation logic (line 25, 42)",
            "Medium Priority: Infrastructure gap in src/Infrastructure/Repository.cs (72.5%, needs 80%)"
        ]
    }


# AC7 Test Fixtures: QA skill integration
@pytest.fixture
def qa_skill_invocation_context():
    """Context for QA skill invoking coverage-analyzer."""
    return {
        "story_id": "STORY-TEST-001",
        "language": "Python",
        "test_command": "pytest --cov=src --cov-report=json",
        "thresholds": {
            "business_logic": 0.95,
            "application": 0.85,
            "overall": 0.80
        },
        "context_files": {
            "tech_stack": "/mnt/c/Projects/MyProject/devforgeai/context/tech-stack.md",
            "source_tree": "/mnt/c/Projects/MyProject/devforgeai/context/source-tree.md",
            "coverage_thresholds": "/mnt/c/Projects/MyProject/.claude/skills/devforgeai-qa/assets/config/coverage-thresholds.md"
        }
    }


# AC9 Test Fixtures: Error scenarios
@pytest.fixture
def error_scenario_context_missing():
    """Error scenario: context files missing."""
    return {
        "scenario": "context_missing",
        "missing_file": "devforgeai/context/source-tree.md",
        "expected_response": {
            "status": "failure",
            "error": "Context file missing: devforgeai/context/source-tree.md",
            "blocks_qa": True,
            "remediation": "Run /create-context to create missing context files"
        }
    }


@pytest.fixture
def error_scenario_command_failed():
    """Error scenario: coverage command execution failed."""
    return {
        "scenario": "command_failed",
        "command": "pytest --cov=src --cov-report=json",
        "exit_code": 1,
        "stderr": "ModuleNotFoundError: No module named 'pytest_cov'",
        "expected_response": {
            "status": "failure",
            "error": "Coverage command failed: ModuleNotFoundError: No module named 'pytest_cov'",
            "blocks_qa": True,
            "remediation": "Install coverage tool: pip install pytest-cov"
        }
    }


@pytest.fixture
def error_scenario_parse_error():
    """Error scenario: coverage report parse error."""
    return {
        "scenario": "parse_error",
        "report_file": "coverage.json",
        "content": "{invalid json",
        "error_type": "JSONDecodeError",
        "expected_response": {
            "status": "failure",
            "error": "Failed to parse coverage report: coverage.json (JSONDecodeError)",
            "blocks_qa": True,
            "remediation": "Verify coverage report is valid JSON. Re-run coverage command: pytest --cov=src --cov-report=json"
        }
    }


@pytest.fixture
def error_scenario_no_classification():
    """Error scenario: no files could be classified."""
    return {
        "scenario": "no_classification",
        "coverage_report": {
            "files": {
                "unknown/file1.py": {"coverage": 85},
                "unknown/file2.py": {"coverage": 90}
            }
        },
        "source_tree_patterns": {
            "business_logic": ["src/Domain/**"],
            "application": ["src/Application/**"],
            "infrastructure": ["src/Infrastructure/**"]
        },
        "expected_response": {
            "status": "failure",
            "error": "Could not classify files using source-tree.md patterns. 0 of 2 files classified.",
            "blocks_qa": True,
            "remediation": "Update source-tree.md with patterns that match your project structure. Example: 'unknown/**' for unknown/ files"
        }
    }


# AC8 Test Fixtures: Prompt template
@pytest.fixture
def prompt_template_file_path():
    """Path to subagent-prompt-templates.md."""
    return Path("/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-qa/references/subagent-prompt-templates.md")


@pytest.fixture
def expected_template_sections():
    """Expected sections in prompt template."""
    return [
        "## Template: coverage-analyzer",
        "### Context File Loading",
        "### Language Detection",
        "### Tool Selection",
        "### Coverage Command Execution",
        "### Report Parsing",
        "### Layer Classification",
        "### Threshold Validation",
        "### Gap Identification",
        "### Response Parsing",
        "### Error Handling",
        "### Integration Example",
        "### Token Budget Impact"
    ]
