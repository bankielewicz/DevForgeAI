"""
Shared fixtures and helpers for STORY-033 tests

Provides:
- Temporary project directories
- Mock audit reports
- Mock hooks configurations
- Mock CLI responses
- Helpers for subprocess mocking
"""

import pytest
import json
import tempfile
import shutil
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, List
from unittest.mock import MagicMock, patch
import subprocess


# ============================================================================
# DIRECTORY FIXTURES
# ============================================================================

@pytest.fixture
def temp_project_dir():
    """Create temporary DevForgeAI project structure with all required directories"""
    temp_dir = tempfile.mkdtemp(prefix="devforgeai_test_story033_")

    # Create standard DevForgeAI directory structure
    dirs = [
        "devforgeai/qa",
        "devforgeai/config",
        "devforgeai/feedback/logs",
        "devforgeai/adrs",
        ".ai_docs/Stories",
        ".claude/commands",
    ]

    for d in dirs:
        os.makedirs(f"{temp_dir}/{d}", exist_ok=True)

    yield temp_dir

    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def project_with_context(temp_project_dir):
    """Project directory with hooks config already set up"""
    # Create default hooks config
    config = {
        "enabled": True,
        "trigger_on": "all",
        "operations": {
            "audit-deferrals": {
                "enabled": True,
                "trigger_on": "all"
            }
        }
    }

    config_dir = f"{temp_project_dir}/devforgeai/config"
    with open(f"{config_dir}/hooks.yaml", 'w') as f:
        json.dump(config, f)

    return temp_project_dir


# ============================================================================
# AUDIT REPORT FIXTURES
# ============================================================================

@pytest.fixture
def sample_audit_report(temp_project_dir):
    """Create a realistic audit report with 10 deferrals"""
    report_content = {
        "timestamp": datetime.now().isoformat(),
        "audit_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "command": "/audit-deferrals",
        "scope": 25,
        "stories_audited": 25,
        "stories_with_deferrals": 3,
        "total_deferrals": 10,
        "resolvable_count": 2,
        "valid_count": 5,
        "invalid_count": 1,
        "violations_by_severity": {
            "CRITICAL": 1,
            "HIGH": 2,
            "MEDIUM": 1,
            "LOW": 0
        },
        "oldest_age_days": 45,
        "circular_chains": [
            "STORY-004 → STORY-005 → STORY-004"
        ],
        "deferrals": [
            {
                "story_id": "STORY-001",
                "item": "Implement error handling",
                "reason": "Deferred to STORY-002 (dependency resolved)",
                "age_days": 10,
                "status": "resolvable",
                "blocker_status": "RESOLVED (story Released)"
            },
            {
                "story_id": "STORY-002",
                "item": "Add logging layer",
                "reason": "Blocked by: npm packages installation",
                "age_days": 25,
                "status": "valid",
                "blocker_status": "VALID (npm not installed)"
            },
            {
                "story_id": "STORY-003",
                "item": "Security audit",
                "reason": "Out of scope: ADR-001",
                "age_days": 45,
                "status": "valid",
                "blocker_status": "RESOLVED (ADR documented)"
            },
            {
                "story_id": "STORY-004",
                "item": "Exit code handling",
                "reason": "Deferred to STORY-005",
                "age_days": 30,
                "status": "valid",
                "blocker_status": "VALID (work in STORY-005)"
            },
            {
                "story_id": "STORY-005",
                "item": "Exit code validation",
                "reason": "Deferred to STORY-006",
                "age_days": 25,
                "status": "valid",
                "blocker_status": "VALID (work in STORY-006)"
            },
        ],
        "violations": [
            {
                "type": "Multi-level deferral chain",
                "severity": "CRITICAL",
                "stories_involved": ["STORY-004", "STORY-005", "STORY-006"],
                "description": "Chain spans 2 hops, work may be lost"
            }
        ]
    }

    report_path = f"{temp_project_dir}/devforgeai/qa/deferral-audit-sample.json"
    with open(report_path, 'w') as f:
        json.dump(report_content, f, indent=2)

    return report_path


@pytest.fixture
def empty_audit_report(temp_project_dir):
    """Create audit report with zero deferrals"""
    report_content = {
        "timestamp": datetime.now().isoformat(),
        "scope": 25,
        "stories_with_deferrals": 0,
        "total_deferrals": 0,
        "resolvable_count": 0,
        "valid_count": 0,
        "invalid_count": 0,
        "oldest_age_days": None,
        "circular_chains": [],
        "deferrals": []
    }

    report_path = f"{temp_project_dir}/devforgeai/qa/deferral-audit-empty.json"
    with open(report_path, 'w') as f:
        json.dump(report_content, f)

    return report_path


@pytest.fixture
def massive_audit_report(temp_project_dir):
    """Create audit report with 150 deferrals (requires truncation)"""
    deferrals = []

    # Create 5 CRITICAL deferrals
    for i in range(5):
        deferrals.append({
            "story_id": f"STORY-{i:03d}",
            "item": f"CRITICAL item {i}",
            "priority": "CRITICAL",
            "age_days": 10 + i,
            "status": "valid"
        })

    # Create 20 HIGH deferrals
    for i in range(5, 25):
        deferrals.append({
            "story_id": f"STORY-{i:03d}",
            "item": f"HIGH item {i}",
            "priority": "HIGH",
            "age_days": 15 + (i - 5),
            "status": "valid"
        })

    # Create 125 MEDIUM deferrals
    for i in range(25, 150):
        deferrals.append({
            "story_id": f"STORY-{i:03d}",
            "item": f"MEDIUM item {i}",
            "priority": "MEDIUM",
            "age_days": 20 + (i - 25),
            "status": "valid"
        })

    report_content = {
        "timestamp": datetime.now().isoformat(),
        "scope": 200,
        "total_deferrals": 150,
        "resolvable_count": 50,
        "valid_count": 95,
        "invalid_count": 5,
        "oldest_age_days": 365,
        "circular_chains": ["STORY-100->STORY-101->STORY-102->STORY-100"],
        "deferrals": deferrals,
        "violations": [
            {"type": "Circular deferral", "severity": "CRITICAL", "chain": "STORY-100->STORY-101->STORY-102->STORY-100"}
        ]
    }

    report_path = f"{temp_project_dir}/devforgeai/qa/deferral-audit-massive.json"
    with open(report_path, 'w') as f:
        json.dump(report_content, f)

    return report_path


@pytest.fixture
def audit_with_sensitive_data(temp_project_dir):
    """Create audit report containing sensitive data that should be sanitized"""
    report_content = {
        "timestamp": datetime.now().isoformat(),
        "scope": 5,
        "stories_with_deferrals": 2,
        "deferrals": [
            {
                "story_id": "STORY-100",
                "item": "Configure API integration",
                "reason": "Blocked by: Need api_key=sk-abc123xyz789 from service",
                "description": "Configure with api_key=sk-abc123xyz789 and secret=my-secret-key-12345"
            },
            {
                "story_id": "STORY-101",
                "item": "Database connection",
                "reason": "Need password=dbpass@123 from ops team",
                "description": "Connect with password=dbpass@123 and token=ghp_abcdef123456"
            }
        ]
    }

    report_path = f"{temp_project_dir}/devforgeai/qa/deferral-audit-sensitive.json"
    with open(report_path, 'w') as f:
        json.dump(report_content, f)

    return report_path


# ============================================================================
# MOCK HOOKS CONFIGURATION FIXTURES
# ============================================================================

@pytest.fixture
def valid_hooks_config(temp_project_dir):
    """Create valid hooks.yaml configuration"""
    config = {
        "enabled": True,
        "trigger_on": "all",
        "feedback_types": ["questions", "insights"],
        "operations": {
            "audit-deferrals": {
                "enabled": True,
                "trigger_on": "all",
                "skip_all": False
            },
            "dev": {
                "enabled": True,
                "trigger_on": "all"
            }
        }
    }

    config_dir = f"{temp_project_dir}/devforgeai/config"
    os.makedirs(config_dir, exist_ok=True)

    config_path = f"{config_dir}/hooks.yaml"
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

    return config_path


@pytest.fixture
def invalid_hooks_config(temp_project_dir):
    """Create invalid/corrupted hooks.yaml"""
    config_dir = f"{temp_project_dir}/devforgeai/config"
    os.makedirs(config_dir, exist_ok=True)

    config_path = f"{config_dir}/hooks.yaml"
    with open(config_path, 'w') as f:
        # Write invalid YAML/JSON
        f.write("{ invalid json [ not ] closed }")

    return config_path


@pytest.fixture
def hooks_disabled_config(temp_project_dir):
    """Create hooks config with hooks disabled"""
    config = {
        "enabled": False,
        "operations": {
            "audit-deferrals": {
                "enabled": False
            }
        }
    }

    config_dir = f"{temp_project_dir}/devforgeai/config"
    os.makedirs(config_dir, exist_ok=True)

    config_path = f"{config_dir}/hooks.yaml"
    with open(config_path, 'w') as f:
        json.dump(config, f)

    return config_path


# ============================================================================
# MOCK CLI RESPONSE FIXTURES
# ============================================================================

@pytest.fixture
def mock_check_hooks_eligible():
    """Mock successful check-hooks response (hooks are eligible)"""
    return {
        "returncode": 0,
        "stdout": '{"eligible": true, "reason": "audit-deferrals enabled and trigger matches"}',
        "stderr": ""
    }


@pytest.fixture
def mock_check_hooks_ineligible():
    """Mock check-hooks response (hooks not eligible)"""
    return {
        "returncode": 1,
        "stdout": '{"eligible": false, "reason": "audit-deferrals disabled in config"}',
        "stderr": ""
    }


@pytest.fixture
def mock_check_hooks_cli_missing():
    """Mock check-hooks response when CLI is not installed"""
    return {
        "returncode": 127,
        "stdout": "",
        "stderr": "devforgeai: command not found"
    }


@pytest.fixture
def mock_invoke_hooks_success():
    """Mock successful invoke-hooks response"""
    return {
        "returncode": 0,
        "stdout": '{"session_id": "sess-20251117-001", "status": "success"}',
        "stderr": ""
    }


@pytest.fixture
def mock_invoke_hooks_failure():
    """Mock failed invoke-hooks response"""
    return {
        "returncode": 1,
        "stdout": "",
        "stderr": "Error: Feedback skill failed to execute"
    }


# ============================================================================
# LOG FILE FIXTURES
# ============================================================================

@pytest.fixture
def invocation_log_path(temp_project_dir):
    """Get path to hook invocations log"""
    log_dir = f"{temp_project_dir}/devforgeai/feedback/logs"
    os.makedirs(log_dir, exist_ok=True)
    return f"{log_dir}/hook-invocations.log"


@pytest.fixture
def sample_log_entry():
    """Create a sample log entry"""
    return {
        "timestamp": datetime.now().isoformat(),
        "operation": "audit-deferrals",
        "status": "check_hooks_success",
        "outcome": "invoke_hooks_called",
        "session_id": "sess-test-001",
        "error_message": None
    }


# ============================================================================
# HELPER FUNCTIONS (as fixtures)
# ============================================================================

@pytest.fixture
def create_audit_context():
    """Factory to create audit context for invoke-hooks"""
    def _create(audit_report_path: str, truncate_to: int = None) -> Dict[str, Any]:
        with open(audit_report_path, 'r') as f:
            report = json.load(f)

        # Build context for invoke-hooks
        deferrals = report.get("deferrals", [])

        # Truncate if needed
        if truncate_to and len(deferrals) > truncate_to:
            deferrals = deferrals[:truncate_to]

        context = {
            "operation": "audit-deferrals",
            "operation_metadata": {
                "audit_summary": {
                    "resolvable_count": report.get("resolvable_count", 0),
                    "valid_count": report.get("valid_count", 0),
                    "invalid_count": report.get("invalid_count", 0),
                    "oldest_age": report.get("oldest_age_days", 0),
                    "circular_chains": report.get("circular_chains", [])
                },
                "total_deferrals": len(report.get("deferrals", [])),
                "top_deferrals": deferrals
            }
        }

        return context

    return _create


@pytest.fixture
def sanitize_context():
    """Factory to sanitize sensitive data from context"""
    def _sanitize(context: Dict[str, Any]) -> Dict[str, Any]:
        import re

        # Recursively sanitize all string values
        def sanitize_value(value):
            if isinstance(value, str):
                patterns = [
                    (r'api_key\s*=\s*[^\s,]+', 'api_key=[REDACTED]'),
                    (r'password\s*=\s*[^\s,]+', 'password=[REDACTED]'),
                    (r'token\s*=\s*[^\s,]+', 'token=[REDACTED]'),
                    (r'secret\s*=\s*[^\s,]+', 'secret=[REDACTED]'),
                ]

                for pattern, replacement in patterns:
                    value = re.sub(pattern, replacement, value, flags=re.IGNORECASE)
                return value
            elif isinstance(value, dict):
                return {k: sanitize_value(v) for k, v in value.items()}
            elif isinstance(value, list):
                return [sanitize_value(v) for v in value]
            else:
                return value

        return sanitize_value(context)

    return _sanitize


@pytest.fixture
def write_log_entry():
    """Factory to write log entry to file"""
    def _write(log_path: str, entry: Dict[str, Any]):
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, 'a') as f:
            f.write(json.dumps(entry) + '\n')

    return _write


@pytest.fixture
def read_log_entries():
    """Factory to read all log entries from file"""
    def _read(log_path: str) -> List[Dict[str, Any]]:
        if not os.path.exists(log_path):
            return []

        entries = []
        with open(log_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('['):  # Skip [WARNING] style lines
                    try:
                        entries.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass

        return entries

    return _read


@pytest.fixture
def validate_context_size():
    """Factory to validate context is ≤50KB"""
    def _validate(context: Dict[str, Any]) -> bool:
        json_str = json.dumps(context)
        size_bytes = len(json_str.encode('utf-8'))
        return size_bytes <= 50000

    return _validate


# ============================================================================
# SUBPROCESS MOCKING HELPERS
# ============================================================================

@pytest.fixture
def mock_subprocess_check_hooks(mocker):
    """Mock subprocess.run for check-hooks command"""
    def _mock(return_value=None):
        if return_value is None:
            return_value = {
                "returncode": 0,
                "stdout": '{"eligible": true}',
                "stderr": ""
            }

        mock_run = mocker.patch('subprocess.run')
        mock_run.return_value = MagicMock(
            returncode=return_value["returncode"],
            stdout=return_value["stdout"],
            stderr=return_value["stderr"]
        )
        return mock_run

    return _mock


@pytest.fixture
def mock_subprocess_invoke_hooks(mocker):
    """Mock subprocess.run for invoke-hooks command"""
    def _mock(return_value=None):
        if return_value is None:
            return_value = {
                "returncode": 0,
                "stdout": '{"session_id": "sess-001"}',
                "stderr": ""
            }

        mock_run = mocker.patch('subprocess.run')
        mock_run.return_value = MagicMock(
            returncode=return_value["returncode"],
            stdout=return_value["stdout"],
            stderr=return_value["stderr"]
        )
        return mock_run

    return _mock


if __name__ == "__main__":
    # This file is meant to be imported by pytest
    pass
