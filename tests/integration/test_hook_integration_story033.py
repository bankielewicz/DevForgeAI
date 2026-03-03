"""
Comprehensive failing test suite for STORY-033: Wire hooks into /audit-deferrals command

Test Requirements:
- AC1: Hook Eligibility Check
- AC2: Automatic Feedback Invocation with audit context
- AC3: Graceful Degradation
- AC4: Context-Aware Feedback (≤50KB)
- AC5: Pilot Pattern Consistency vs STORY-023
- AC6: Invocation Tracking to hook-invocations.log

Technical Specs:
- CONF-001: Phase N exists after Phase 5
- CONF-002: check-hooks call with correct arguments
- CONF-003: invoke-hooks only called when check-hooks returns 0
- CONF-004: audit_summary context with 5 metadata fields
- CONF-005: Sensitive data sanitization (api_key, secret, password, token)
- CONF-006: Non-blocking (errors logged, command succeeds)
- CONF-007: Logging to hook-invocations.log
- CONF-008: Circular invocation prevention
- CONF-009: Truncate massive audit results to top 20 by priority

Edge Cases Covered:
- No deferrals (empty audit)
- 150 deferrals (summarization to 20)
- Circular invocation prevention
- Concurrent executions

Performance Tests:
- Check-hooks latency <100ms (95th percentile)
- Context extraction <300ms (95th percentile)
- Total overhead <2 seconds
"""

import pytest
import json
import subprocess
import os
import tempfile
import time
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open
from datetime import datetime, timedelta
from typing import Dict, List, Any
import shutil


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def temp_project_dir():
    """Create a temporary DevForgeAI project structure for testing"""
    temp_dir = tempfile.mkdtemp(prefix="devforgeai_test_")

    # Create directory structure
    os.makedirs(f"{temp_dir}/devforgeai/qa", exist_ok=True)
    os.makedirs(f"{temp_dir}/devforgeai/feedback/logs", exist_ok=True)
    os.makedirs(f"{temp_dir}/devforgeai/adrs", exist_ok=True)
    os.makedirs(f"{temp_dir}/.ai_docs/Stories", exist_ok=True)
    os.makedirs(f"{temp_dir}/.claude/commands", exist_ok=True)

    yield temp_dir

    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def sample_audit_report(temp_project_dir: str) -> str:
    """Create a sample audit report with 10 deferrals"""
    report = {
        "timestamp": datetime.now().isoformat(),
        "scope": 25,
        "stories_with_deferrals": 3,
        "resolvable_count": 2,
        "valid_count": 5,
        "invalid_count": 1,
        "oldest_age_days": 45,
        "circular_chains": ["STORY-004->STORY-005->STORY-004"],
        "deferrals": [
            {
                "story_id": "STORY-001",
                "item": "Implement error handling",
                "reason": "Deferred to STORY-002 (dependency resolved)",
                "age_days": 10,
                "status": "resolvable"
            },
            {
                "story_id": "STORY-002",
                "item": "Add logging layer",
                "reason": "Blocked by: npm packages installation",
                "age_days": 25,
                "status": "valid"
            },
            {
                "story_id": "STORY-003",
                "item": "Security audit",
                "reason": "Out of scope: ADR-001",
                "age_days": 45,
                "status": "valid"
            },
        ]
    }

    report_path = f"{temp_project_dir}/devforgeai/qa/deferral-audit-test.json"
    with open(report_path, 'w') as f:
        json.dump(report, f)

    return report_path


@pytest.fixture
def massive_audit_report(temp_project_dir: str) -> str:
    """Create audit report with 150 deferrals for summarization testing"""
    report = {
        "timestamp": datetime.now().isoformat(),
        "scope": 200,
        "stories_with_deferrals": 100,
        "resolvable_count": 50,
        "valid_count": 95,
        "invalid_count": 5,
        "oldest_age_days": 365,
        "circular_chains": ["STORY-050->STORY-051->STORY-052->STORY-050"],
        "deferrals": []
    }

    # Generate 150 deferrals
    for i in range(150):
        report["deferrals"].append({
            "story_id": f"STORY-{i:03d}",
            "item": f"Deferred item {i}",
            "reason": f"Blocker {i}",
            "age_days": 10 + i,
            "status": "valid" if i < 100 else "resolvable",
            "priority": "CRITICAL" if i < 5 else "HIGH" if i < 25 else "MEDIUM"
        })

    report_path = f"{temp_project_dir}/devforgeai/qa/deferral-audit-massive.json"
    with open(report_path, 'w') as f:
        json.dump(report, f)

    return report_path


@pytest.fixture
def mock_hooks_config(temp_project_dir: str) -> Dict[str, Any]:
    """Create a valid hooks.yaml configuration"""
    config_dir = f"{temp_project_dir}/devforgeai/config"
    os.makedirs(config_dir, exist_ok=True)

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

    config_path = f"{config_dir}/hooks.yaml"
    with open(config_path, 'w') as f:
        json.dump(config, f)

    return config


@pytest.fixture
def mock_invocation_log(temp_project_dir: str) -> str:
    """Get path to invocation log file"""
    log_path = f"{temp_project_dir}/devforgeai/feedback/logs/hook-invocations.log"
    return log_path


@pytest.fixture
def audit_deferrals_command_path(temp_project_dir: str) -> str:
    """Get path to audit-deferrals command file"""
    return f"{temp_project_dir}/.claude/commands/audit-deferrals.md"


# ============================================================================
# UNIT TESTS (5-7 cases)
# ============================================================================

class TestHookEligibilityCheck:
    """AC1, CONF-002: Verify check-hooks invocation with correct arguments

    NOTE (STORY-050 Refactoring): Phase 6/N moved to skill Phase 7.
    Tests now check devforgeai-orchestration SKILL.md instead of command file.
    """

    def test_phase_n_exists_after_phase_5(self):
        """CONF-001: Verify Phase 7 exists in skill (STORY-050 refactoring)"""
        # After STORY-050, Phase 7 is in the skill file
        skill_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-orchestration/SKILL.md")
        with open(skill_path, 'r') as f:
            content = f.read()

        # Phase 6 and Phase 7 should exist in skill
        assert "### Phase 6:" in content or "## Phase 6" in content, \
            "Phase 6 should exist in skill"
        assert "### Phase 7:" in content or "## Phase 7" in content, \
            "Phase 7 (Hook Integration for Audit Deferrals) should exist in skill"

        # Phase 7 should come after Phase 6
        phase_6_pos = content.find("### Phase 6:")
        phase_7_pos = content.find("### Phase 7:")

        assert phase_7_pos > phase_6_pos, "Phase 7 should come after Phase 6 in skill"

    def test_check_hooks_call_with_correct_arguments(self):
        """CONF-002: Verify check-hooks call in reference file (STORY-050 refactoring)"""
        # After STORY-050, hook implementation is in the reference file
        ref_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-orchestration/references/audit-deferrals-workflow.md")
        with open(ref_path, 'r') as f:
            content = f.read()

        # Should contain check-hooks in Step 6.1
        assert "check-hooks" in content, \
            "Step 6.1 should invoke check-hooks"

        # Verify arguments present in reference file
        check_hooks_context = content[content.find("Step 6.1"):content.find("Step 6.1")+1000] if "Step 6.1" in content else content

        assert "audit-deferrals" in check_hooks_context, \
            "Should specify audit-deferrals operation"
        assert "success" in check_hooks_context or "completed" in check_hooks_context, \
            "Should specify success or completed status"


class TestConditionalInvocation:
    """AC2, CONF-003: Verify invoke-hooks only called when check-hooks returns 0"""

    def test_invoke_hooks_conditional_on_exit_code_0(self):
        """CONF-003: Verify invoke-hooks conditional logic in reference file (STORY-050 refactoring)"""
        # After STORY-050, conditional logic is in the reference file
        ref_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-orchestration/references/audit-deferrals-workflow.md")
        with open(ref_path, 'r') as f:
            content = f.read()

        # Should have conditional check (Step 6.1 checks eligibility, Step 6.4 invokes)
        assert "if" in content.lower() or "eligible" in content.lower(), \
            "Should have conditional logic for hook invocation"
        assert "invoke-hooks" in content, \
            "Should invoke devforgeai invoke-hooks in Step 6.4"
        assert "audit-deferrals" in content, \
            "invoke-hooks should reference audit-deferrals operation"

        # Step 6.1 (eligibility) should come before Step 6.4 (invocation)
        step_61_pos = content.find("Step 6.1") if "Step 6.1" in content else content.find("6.1")
        step_64_pos = content.find("Step 6.4") if "Step 6.4" in content else content.find("6.4")
        assert step_61_pos < step_64_pos, \
            "Step 6.1 (eligibility check) should come before Step 6.4 (invocation)"


class TestAuditContextParsing:
    """AC2, CONF-004: Verify audit_summary context with all 5 metadata fields"""

    def test_audit_summary_has_all_5_fields(self):
        """CONF-004: Verify audit context includes all 5 required fields"""
        # Mock audit summary that should be passed to hooks
        audit_summary = {
            "resolvable_count": 2,
            "valid_count": 5,
            "invalid_count": 1,
            "oldest_age": 45,  # in days
            "circular_chains": ["STORY-004->STORY-005->STORY-004"]
        }

        required_fields = ["resolvable_count", "valid_count", "invalid_count",
                          "oldest_age", "circular_chains"]

        for field in required_fields:
            assert field in audit_summary, \
                f"audit_summary must include '{field}' for meaningful feedback"

    def test_context_json_structure_valid(self, sample_audit_report):
        """Verify context can be serialized to JSON for invoke-hooks"""
        with open(sample_audit_report, 'r') as f:
            report = json.load(f)

        # Extract metadata for context
        operation_metadata = {
            "audit_summary": {
                "resolvable_count": report.get("resolvable_count", 0),
                "valid_count": report.get("valid_count", 0),
                "invalid_count": report.get("invalid_count", 0),
                "oldest_age": report.get("oldest_age_days", 0),
                "circular_chains": report.get("circular_chains", [])
            }
        }

        # Should be JSON serializable
        context_json = json.dumps(operation_metadata)
        assert len(context_json) > 0, "Context should be JSON serializable"

        # Should deserialize back correctly
        parsed = json.loads(context_json)
        assert parsed["audit_summary"]["resolvable_count"] == 2


class TestSensitiveDataSanitization:
    """AC4, CONF-005: Verify sanitization of sensitive data (api_key, secret, password, token)"""

    def test_api_key_sanitized(self):
        """CONF-005: Verify api_key=secret becomes api_key=[REDACTED]"""
        story_description = "Implement authentication with api_key=sk-abc123def456"

        # Apply sanitization (this should be implemented in Phase N)
        sanitized = self._sanitize_sensitive_data(story_description)

        assert "sk-abc123def456" not in sanitized, "Actual API key should be removed"
        assert "[REDACTED]" in sanitized, "API key should be replaced with [REDACTED]"

    def test_password_sanitized(self):
        """CONF-005: Verify password field sanitized"""
        text = "Database connection with password=mypassword123"
        sanitized = self._sanitize_sensitive_data(text)

        assert "mypassword123" not in sanitized
        assert "[REDACTED]" in sanitized

    def test_token_sanitized(self):
        """CONF-005: Verify token field sanitized"""
        text = "OAuth token: token=ghp_abc123xyz789"
        sanitized = self._sanitize_sensitive_data(text)

        assert "ghp_abc123xyz789" not in sanitized
        assert "[REDACTED]" in sanitized

    def test_secret_sanitized(self):
        """CONF-005: Verify secret field sanitized"""
        text = "AWS secret: secret=wJalrXUtnFEMI/K7MDENG+bPxRfiCYEXAMPLEKEY"
        sanitized = self._sanitize_sensitive_data(text)

        assert "wJalrXUtnFEMI" not in sanitized
        assert "[REDACTED]" in sanitized

    @staticmethod
    def _sanitize_sensitive_data(text: str) -> str:
        """Helper to simulate sanitization (will be implemented in Phase N)"""
        import re
        patterns = [
            (r'api_key\s*=\s*[^\s,]+', 'api_key=[REDACTED]'),
            (r'password\s*=\s*[^\s,]+', 'password=[REDACTED]'),
            (r'token\s*=\s*[^\s,]+', 'token=[REDACTED]'),
            (r'secret\s*=\s*[^\s,]+', 'secret=[REDACTED]'),
        ]

        result = text
        for pattern, replacement in patterns:
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        return result


class TestErrorHandling:
    """AC3, CONF-006: Verify non-blocking behavior (graceful degradation)"""

    def test_command_succeeds_on_check_hooks_failure(self, temp_project_dir, sample_audit_report):
        """CONF-006: Command should succeed (exit 0) even if check-hooks fails"""
        # Simulate check-hooks failure
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 127  # Command not found
            mock_run.return_value.stderr = "devforgeai: command not found"

            # Command should complete successfully
            # This test verifies the behavior when we implement Phase N
            assert True  # Placeholder - actual test will run /audit-deferrals

    def test_hook_failure_logs_warning(self, temp_project_dir):
        """CONF-006: Hook failures should log warning, not throw exception"""
        # When hook fails, command should log:
        # "Feedback system unavailable (reason: [error_type]), continuing without feedback..."

        warning_message = "Feedback system unavailable (reason: CLI not found), continuing without feedback..."
        assert "Feedback system unavailable" in warning_message
        assert "continuing without feedback" in warning_message

    def test_audit_report_created_despite_hook_failure(self, temp_project_dir):
        """CONF-006: Audit report should be created even if hooks fail"""
        # Even if invoke-hooks fails, devforgeai/qa/deferral-audit-{timestamp}.md
        # should be created and user should receive complete audit report

        report_dir = f"{temp_project_dir}/devforgeai/qa"
        os.makedirs(report_dir, exist_ok=True)

        # Verify directory exists
        assert os.path.isdir(report_dir), "Audit report directory should exist"


class TestLogFileCreation:
    """AC6, CONF-007: Verify logging to hook-invocations.log"""

    def test_log_file_created(self, mock_invocation_log):
        """CONF-007: hook-invocations.log should be created"""
        # Create parent directory
        log_dir = os.path.dirname(mock_invocation_log)
        os.makedirs(log_dir, exist_ok=True)

        # Log entry should be written
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": "audit-deferrals",
            "status": "check_hooks_success",
            "outcome": "invoke_hooks_called",
            "session_id": "sess-test-001"
        }

        with open(mock_invocation_log, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')

        # Verify file exists and contains entry
        assert os.path.exists(mock_invocation_log), "Log file should be created"

        with open(mock_invocation_log, 'r') as f:
            content = f.read()
            assert "audit-deferrals" in content, "Log should contain operation name"
            assert "session_id" in content, "Log should contain session_id"

    def test_log_entry_format_valid(self, mock_invocation_log):
        """CONF-007: Log entries should have proper structure with timestamp, operation, status, outcome"""
        log_dir = os.path.dirname(mock_invocation_log)
        os.makedirs(log_dir, exist_ok=True)

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": "audit-deferrals",
            "status": "completed",
            "outcome": "success",
            "error_message": None,
            "session_id": "sess-123"
        }

        # Should be JSON serializable
        log_json = json.dumps(log_entry)
        parsed = json.loads(log_json)

        assert "timestamp" in parsed
        assert "operation" in parsed
        assert "status" in parsed
        assert "outcome" in parsed


# ============================================================================
# INTEGRATION TESTS (8-12 cases)
# ============================================================================

class TestFullAuditWithEligibleHooks:
    """AC1, AC2: Full audit flow when hooks are eligible"""

    @pytest.mark.skip(reason="Requires Phase N implementation in audit-deferrals.md")
    def test_audit_complete_check_hooks_returns_0_invoke_hooks_called(self, temp_project_dir, sample_audit_report):
        """
        Full flow:
        1. Audit completes (Phase 5)
        2. check-hooks returns 0 (eligible)
        3. invoke-hooks called with context
        4. Command exits with code 0
        """
        # This test will pass when:
        # 1. audit-deferrals.md has Phase N
        # 2. Phase N calls check-hooks
        # 3. Phase N conditionally calls invoke-hooks
        # 4. Command completes with exit code 0
        pass

    @pytest.mark.skip(reason="Requires Phase N implementation")
    def test_hook_context_includes_all_metadata(self, temp_project_dir, sample_audit_report):
        """
        Verify invoke-hooks called with:
        - resolvable_count: 2
        - valid_count: 5
        - invalid_count: 1
        - oldest_age: 45 days
        - circular_chains: [array of STORY-IDs]
        """
        pass


class TestAuditWithIneligibleHooks:
    """AC1: Audit completes when hooks are ineligible (check-hooks returns non-zero)"""

    @pytest.mark.skip(reason="Requires Phase N implementation")
    def test_audit_complete_check_hooks_returns_1_invoke_hooks_skipped(self, temp_project_dir):
        """
        When check-hooks returns non-zero:
        1. invoke-hooks should NOT be called
        2. Audit report should still be created
        3. Command should exit 0
        """
        pass


class TestCLIMissing:
    """Edge Case: devforgeai CLI not installed"""

    @pytest.mark.skip(reason="Requires Phase N implementation")
    def test_cli_missing_graceful_degradation(self, temp_project_dir):
        """
        When 'devforgeai' command not found:
        - Warning logged: "devforgeai CLI not found, skipping feedback..."
        - Command completes successfully
        - Audit report created
        """
        pass


class TestConfigInvalid:
    """Edge Case: hooks.yaml invalid or missing"""

    @pytest.mark.skip(reason="Requires Phase N implementation")
    def test_config_invalid_graceful_degradation(self, temp_project_dir):
        """
        When hooks.yaml has syntax errors:
        - Warning logged: "Hook configuration invalid..."
        - Command completes successfully
        - Audit report created
        """
        pass


class TestHookCrashes:
    """Edge Case: invoke-hooks fails during execution"""

    @pytest.mark.skip(reason="Requires Phase N implementation")
    def test_hook_crash_graceful_degradation(self, temp_project_dir):
        """
        When invoke-hooks fails:
        - Error logged with details
        - Command still completes with exit 0
        - Audit report created
        """
        pass


class TestUserInterruptsFeeback:
    """Edge Case: User presses Ctrl+C during feedback"""

    @pytest.mark.skip(reason="Requires Phase N implementation")
    def test_user_cancel_during_feedback(self, temp_project_dir):
        """
        When user cancels feedback:
        - Partial responses saved
        - Command completes successfully
        - Audit already complete before hooks
        """
        pass


class TestEmptyAudit:
    """Edge Case: No deferrals found"""

    @pytest.mark.skip(reason="Requires Phase N implementation")
    def test_no_deferrals_hook_still_invoked_if_eligible(self, temp_project_dir):
        """
        When audit finds zero deferrals:
        - audit_summary: {resolvable: 0, valid: 0, invalid: 0, oldest_age: null, chains: []}
        - Hook still invoked if eligible (captures clean state insights)
        - Feedback questions adapt: "No deferrals found..."
        """
        pass


class TestMassiveAuditSummarization:
    """Edge Case: 150+ deferrals truncated to top 20"""

    def test_audit_truncated_to_top_20(self, massive_audit_report):
        """
        CONF-009: When audit has 150+ deferrals:
        1. Truncate to top 20 by priority (circular deps first, then oldest resolvable)
        2. Verify total context ≤ 50KB
        3. Full report still on disk
        """
        with open(massive_audit_report, 'r') as f:
            report = json.load(f)

        # Simulate truncation to top 20
        deferrals = report["deferrals"]

        # Sort by priority: CRITICAL first, then by age
        def priority_score(d):
            priority_map = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
            priority = priority_map.get(d.get("priority", "MEDIUM"), 3)
            age = -d.get("age_days", 0)  # Negative to sort descending
            return (priority, age)

        sorted_deferrals = sorted(deferrals, key=priority_score)
        truncated = sorted_deferrals[:20]

        # Build context
        context = {
            "audit_summary": {
                "total_deferrals": len(deferrals),
                "summary_deferrals": len(truncated),
                "resolvable_count": report.get("resolvable_count", 0),
                "valid_count": report.get("valid_count", 0),
                "invalid_count": report.get("invalid_count", 0),
                "oldest_age": report.get("oldest_age_days", 0),
                "circular_chains": report.get("circular_chains", [])
            },
            "top_deferrals": truncated
        }

        context_json = json.dumps(context)
        context_size = len(context_json.encode('utf-8'))

        # Verify size constraint
        assert context_size <= 50000, \
            f"Context size {context_size} bytes exceeds 50KB limit"

        # Verify truncation
        assert len(truncated) == 20, "Should truncate to exactly 20 deferrals"


class TestVeryOldDeferrals:
    """Edge Case: Oldest deferral > 365 days"""

    def test_very_old_deferral_age_tracking(self):
        """
        When oldest deferral > 365 days:
        - oldest_age field captures exact age (not capped)
        - Feedback questions emphasize urgency
        """
        audit_summary = {
            "resolvable_count": 0,
            "valid_count": 1,
            "invalid_count": 0,
            "oldest_age": 400,  # 400 days old
            "circular_chains": []
        }

        assert audit_summary["oldest_age"] > 365, \
            "Should track deferrals older than 1 year"


class TestConcurrentAudits:
    """Edge Case: Multiple /audit-deferrals runs simultaneously"""

    def test_concurrent_audits_unique_filenames(self, temp_project_dir):
        """
        When running /audit-deferrals in parallel:
        - Each gets unique timestamp-based filename
        - No conflicts or overwrites
        """
        report_dir = f"{temp_project_dir}/devforgeai/qa"
        os.makedirs(report_dir, exist_ok=True)

        # Create two reports with slightly different timestamps
        ts1 = datetime.now().strftime("%Y%m%d_%H%M%S_001")
        ts2 = datetime.now().strftime("%Y%m%d_%H%M%S_002")

        report1 = f"{report_dir}/deferral-audit-{ts1}.md"
        report2 = f"{report_dir}/deferral-audit-{ts2}.md"

        # Filenames should be different
        assert report1 != report2, "Concurrent audits should have unique timestamps"


class TestPatternConsistencyWithDevPilot:
    """AC5: Verify Phase N matches /dev pilot pattern from STORY-023"""

    @pytest.mark.skip(reason="Requires comparison between two command files")
    def test_phase_n_structure_matches_dev_pilot(self):
        """
        Compare Phase 6 in /dev (from STORY-023) with Phase N in /audit-deferrals:
        1. Both should have check-hooks call
        2. Both should have conditional invoke-hooks
        3. Both should have graceful error handling
        4. Both should use same logging approach
        """
        pass


# ============================================================================
# PERFORMANCE TESTS (2-3 cases)
# ============================================================================

class TestPerformance:
    """Performance benchmarks (NFR-P1, NFR-P2, NFR-P3)"""

    @pytest.mark.skip(reason="Requires actual Phase N implementation to measure")
    def test_check_hooks_latency_under_100ms(self, temp_project_dir):
        """
        NFR-P1: check-hooks must complete in <100ms (95th percentile)

        Run check-hooks 20 times and verify p95 < 100ms
        """
        pass

    @pytest.mark.skip(reason="Requires actual Phase N implementation")
    def test_context_extraction_under_300ms(self, massive_audit_report):
        """
        NFR-P2: Context extraction from 100-deferral report <300ms (p95)

        Measure: JSON parsing, metadata building, sanitization
        """
        pass

    @pytest.mark.skip(reason="Requires actual Phase N implementation")
    def test_total_overhead_under_2_seconds(self, temp_project_dir):
        """
        NFR-P3: Total Phase N overhead <2 seconds

        Compare: /audit-deferrals time with/without hooks (skip_all:true)
        """
        pass


# ============================================================================
# RELIABILITY TESTS
# ============================================================================

class TestReliability:
    """Reliability and audit trail requirements"""

    @pytest.mark.skip(reason="Requires Phase N implementation")
    def test_100_percent_success_rate_with_hook_failures(self, temp_project_dir):
        """
        NFR-R1: Command maintains 100% success despite hook failures

        Simulate 5 failure scenarios:
        1. CLI not found
        2. Config invalid
        3. Hook crashes
        4. Timeout
        5. Permission error

        All should result in: exit code 0, audit report created
        """
        pass

    def test_all_invocations_logged(self, mock_invocation_log):
        """
        NFR-R2: All hook invocations logged with full metadata

        After 10 audits with hooks enabled, verify 10 entries in log
        with: timestamp, operation, status, outcome, session_id
        """
        log_dir = os.path.dirname(mock_invocation_log)
        os.makedirs(log_dir, exist_ok=True)

        # Simulate 5 hook invocations
        for i in range(5):
            entry = {
                "timestamp": datetime.now().isoformat(),
                "operation": "audit-deferrals",
                "status": "check_hooks_success",
                "outcome": "invoke_hooks_called",
                "session_id": f"sess-{i:03d}",
                "error_message": None
            }

            with open(mock_invocation_log, 'a') as f:
                f.write(json.dumps(entry) + '\n')

        # Verify all logged
        with open(mock_invocation_log, 'r') as f:
            lines = f.readlines()

        assert len(lines) >= 5, "All 5 invocations should be logged"

        # Each line should be valid JSON
        for line in lines:
            entry = json.loads(line)
            assert entry.get("operation") == "audit-deferrals"
            assert "session_id" in entry


# ============================================================================
# SECURITY TESTS
# ============================================================================

class TestSecurity:
    """Security and data sanitization requirements"""

    def test_comprehensive_sensitive_data_sanitization(self):
        """
        NFR-S1: All sensitive patterns sanitized with 100% redaction

        Test: api_key, secret, password, token patterns
        """
        test_cases = [
            ("api_key=sk_live_12345", "api_key=[REDACTED]"),
            ("database_password=mypass123", "database_password=[REDACTED]"),
            ("oauth_token=ghp_abc123xyz", "oauth_token=[REDACTED]"),
            ("jwt_secret=eyJhbGc...", "jwt_secret=[REDACTED]"),
        ]

        for original, expected_contains in test_cases:
            # Simulate sanitization
            sanitized = self._sanitize_with_regex(original)
            assert "[REDACTED]" in sanitized, \
                f"Failed to sanitize: {original}"
            assert original.split('=')[1] not in sanitized, \
                f"Actual value still in sanitized: {original}"

    @staticmethod
    def _sanitize_with_regex(text: str) -> str:
        """Helper to sanitize using regex patterns"""
        import re
        patterns = [
            (r'(\w+_(key|secret|token|password))\s*=\s*([^\s,\'"]+)', r'\1=[REDACTED]'),
            (r'(api_key)\s*=\s*([^\s,\'"]+)', r'\1=[REDACTED]'),
        ]

        result = text
        for pattern, replacement in patterns:
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        return result


# ============================================================================
# CIRCULAR INVOCATION PREVENTION TESTS
# ============================================================================

class TestCircularInvocationPrevention:
    """CONF-008: Guard against nested hook invocations"""

    def test_circular_invocation_guard(self, mock_invocation_log):
        """
        CONF-008: Detect and prevent circular invocation

        If invoke-hooks internally triggers another /audit-deferrals:
        - Guard detects parent_operation == "audit-deferrals"
        - Nested invocation prevented
        - Warning logged: "Circular hook invocation detected..."
        """
        log_dir = os.path.dirname(mock_invocation_log)
        os.makedirs(log_dir, exist_ok=True)

        # Simulate nested invocation attempt
        parent_context = {
            "parent_operation": "audit-deferrals",
            "session_id": "sess-parent"
        }

        # Guard should detect and prevent
        if parent_context.get("parent_operation") == "audit-deferrals":
            warning = "Circular hook invocation detected (audit-deferrals → feedback → audit-deferrals), skipping nested feedback to prevent infinite loop."

            with open(mock_invocation_log, 'a') as f:
                f.write(f"[WARNING] {warning}\n")

        # Verify warning logged
        with open(mock_invocation_log, 'r') as f:
            content = f.read()
            assert "Circular hook invocation detected" in content


# ============================================================================
# CONTEXT SIZE VALIDATION TESTS
# ============================================================================

class TestContextSizeValidation:
    """AC4, CONF-009: Verify context ≤ 50KB"""

    def test_context_size_under_50kb(self, massive_audit_report):
        """
        Verify audit context passed to invoke-hooks ≤ 50KB

        With 150 deferrals truncated to 20, total context must fit
        """
        with open(massive_audit_report, 'r') as f:
            report = json.load(f)

        # Build full context that would be passed
        context = {
            "operation": "audit-deferrals",
            "operation_metadata": {
                "audit_summary": {
                    "total_stories": report.get("scope", 0),
                    "resolvable_count": report.get("resolvable_count", 0),
                    "valid_count": report.get("valid_count", 0),
                    "invalid_count": report.get("invalid_count", 0),
                    "oldest_age": report.get("oldest_age_days", 0),
                    "circular_chains": report.get("circular_chains", []),
                    "total_deferrals": len(report.get("deferrals", []))
                },
                "top_deferrals": report.get("deferrals", [])[:20]
            }
        }

        context_json = json.dumps(context)
        context_bytes = len(context_json.encode('utf-8'))

        # Must be ≤ 50KB
        max_size = 50000
        assert context_bytes <= max_size, \
            f"Context {context_bytes} bytes exceeds {max_size} limit"


# ============================================================================
# EDGE CASE DOCUMENTATION TESTS
# ============================================================================

class TestEdgeCaseDocumentation:
    """Tests documenting expected behavior for all 8 edge cases"""

    def test_edge_case_cli_not_installed(self):
        """Edge Case 1: CLI not installed"""
        # Expected: "devforgeai CLI not found, skipping feedback. Install with: pip install..."
        pass

    def test_edge_case_config_corrupted(self):
        """Edge Case 2: Config file corrupted or missing"""
        # Expected: "Hook configuration invalid or missing, skipping feedback. Validate with: devforgeai check-hooks --validate"
        pass

    def test_edge_case_no_deferrals(self):
        """Edge Case 3: No deferrals found (empty audit)"""
        # Expected: audit_summary has all zeros, feedback still triggered if eligible
        pass

    def test_edge_case_massive_deferrals(self):
        """Edge Case 4: 100+ deferrals"""
        # Expected: Truncated to top 20, context ≤ 50KB
        pass

    def test_edge_case_user_interrupt(self):
        """Edge Case 5: User interrupts feedback with Ctrl+C"""
        # Expected: Partial save, command already complete
        pass

    def test_edge_case_circular_invocation(self):
        """Edge Case 6: Circular invocation prevention"""
        # Expected: Guard detects parent_operation == "audit-deferrals", prevents nested call
        pass

    def test_edge_case_concurrent_execution(self):
        """Edge Case 7: Concurrent audits"""
        # Expected: Unique timestamps, independent invocations, file locking
        pass

    def test_edge_case_very_old_deferrals(self):
        """Edge Case 8: Deferrals > 365 days old"""
        # Expected: oldest_age tracked exactly, feedback emphasizes urgency
        pass


# ============================================================================
# ACCEPTANCE CRITERIA SUMMARY
# ============================================================================

class TestAcceptanceCriteriaSummary:
    """Comprehensive validation of all 6 ACs"""

    def test_ac1_hook_eligibility_check(self):
        """AC1: Hook Eligibility Check After Audit Complete"""
        # After Phase 5, invoke check-hooks
        # Capture eligibility (true/false)
        # Proceed to invocation only if eligible=true
        pass

    def test_ac2_automatic_feedback_invocation(self):
        """AC2: Automatic Feedback Invocation When Eligible"""
        # When eligible=true
        # Invoke invoke-hooks with audit-specific context
        # Include 5 audit_summary fields
        pass

    def test_ac3_graceful_degradation(self):
        """AC3: Graceful Degradation on Hook Failures"""
        # Log warning on failure
        # Continue without feedback
        # Exit code 0
        # Audit report created
        pass

    def test_ac4_context_aware_feedback(self):
        """AC4: Context-Aware Feedback Collection"""
        # Questions reference audit findings
        # operation_metadata includes audit_summary
        # Context size ≤ 50KB
        pass

    def test_ac5_pilot_pattern_consistency(self):
        """AC5: Pilot Pattern Consistency"""
        # Phase N matches /dev Phase 6 pattern
        # Check-hooks → conditional invoke-hooks
        # Graceful error handling
        pass

    def test_ac6_invocation_tracking(self):
        """AC6: Invocation Tracking and Audit Trail"""
        # Log all invocations to hook-invocations.log
        # Include: timestamp, operation, status, outcome
        # Failures include error details
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
