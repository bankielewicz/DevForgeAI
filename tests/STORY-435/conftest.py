"""
Shared fixtures for STORY-435 tests.
Story: STORY-435 - Define Structured Requirements Schema
Generated: 2026-02-17 (TDD Red Phase)
"""
import os
import pytest

# Paths relative to project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC_TEMPLATES_DIR = os.path.join(
    PROJECT_ROOT,
    "src", "claude", "skills", "devforgeai-ideation", "assets", "templates",
)
SCHEMA_PATH = os.path.join(SRC_TEMPLATES_DIR, "requirements-schema.yaml")
TEMPLATE_PATH = os.path.join(SRC_TEMPLATES_DIR, "requirements-template.md")
OLD_TEMPLATE_PATH = os.path.join(SRC_TEMPLATES_DIR, "requirements-spec-template.md")


@pytest.fixture
def schema_path():
    return SCHEMA_PATH


@pytest.fixture
def template_path():
    return TEMPLATE_PATH


@pytest.fixture
def old_template_path():
    return OLD_TEMPLATE_PATH


@pytest.fixture
def templates_dir():
    return SRC_TEMPLATES_DIR


@pytest.fixture
def sample_valid_decisions():
    """Sample valid decisions array for testing."""
    return [
        {
            "id": "DR-1",
            "domain": "authentication",
            "decision": "Use JWT tokens with 15-minute expiry",
            "rejected": [
                {"option": "Session cookies", "reason": "Not suitable for API-first architecture"}
            ],
            "rationale": "JWT enables stateless auth suitable for microservices",
            "locked": True,
        }
    ]


@pytest.fixture
def sample_valid_scope():
    """Sample valid scope object for testing."""
    return {
        "in": ["User registration and login", "Product catalog browsing"],
        "out": [
            {"item": "Payment processing", "deferral_target": "Phase 2"},
            {"item": "Social media integration", "deferral_target": "Never"},
        ],
    }


@pytest.fixture
def sample_valid_success_criteria():
    """Sample valid success criteria for testing."""
    return [
        {
            "id": "SC-1",
            "metric": "User registration completion rate",
            "target": "> 85%",
            "measurement": "Analytics funnel tracking",
        }
    ]
