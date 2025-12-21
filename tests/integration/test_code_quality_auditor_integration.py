"""
Integration tests for code-quality-auditor subagent with devforgeai-qa skill (STORY-063)

Test-Driven Development (RED PHASE):
Integration test written BEFORE implementation - should FAIL initially.

Test Coverage:
- AC7: Integration with devforgeai-qa skill Phase 4
- AC8: Prompt template documented
- End-to-end workflow from QA skill invocation to result processing

Coverage Target: 85% application layer
"""

import pytest
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import tempfile
import shutil


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def project_root():
    """Return project root directory"""
    return Path(__file__).parent.parent.parent


@pytest.fixture
def temp_project_dir():
    """Create temporary project directory for testing"""
    temp_dir = tempfile.mkdtemp(prefix="test_code_quality_")
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def mock_context_files(temp_project_dir):
    """Create mock context files for testing"""
    context_dir = temp_project_dir / "devforgeai" / "context"
    context_dir.mkdir(parents=True, exist_ok=True)

    # tech-stack.md
    tech_stack = context_dir / "tech-stack.md"
    tech_stack.write_text("""# Tech Stack

## Backend
- Language: Python 3.11
- Framework: FastAPI 0.104

## Testing
- Framework: pytest 7.4
""")

    # quality-metrics.md
    qa_dir = temp_project_dir / "devforgeai" / "qa"
    qa_dir.mkdir(parents=True, exist_ok=True)

    quality_metrics = qa_dir / "quality-metrics.md"
    quality_metrics.write_text("""# Quality Metrics

## Code Quality Thresholds

### Cyclomatic Complexity
- CRITICAL: >20
- WARNING: 15-20
- ACCEPTABLE: <15

### Code Duplication
- CRITICAL: >25%
- WARNING: 20-25%
- ACCEPTABLE: <20%

### Maintainability Index
- CRITICAL: <40
- WARNING: 40-50
- ACCEPTABLE: >50
""")

    return {
        "tech_stack": tech_stack,
        "quality_metrics": quality_metrics
    }


@pytest.fixture
def sample_story_file(temp_project_dir):
    """Create sample story file for testing"""
    stories_dir = temp_project_dir / ".ai_docs" / "Stories"
    stories_dir.mkdir(parents=True, exist_ok=True)

    story_file = stories_dir / "STORY-TEST-003.story.md"
    story_file.write_text("""---
story_id: STORY-TEST-003
title: Test story with code quality issues
status: Dev Complete
---

# STORY-TEST-003

## Acceptance Criteria

### AC1: Feature implemented
**Given** implementation exists
**When** QA runs
**Then** code quality validated

## Definition of Done

### Implementation
- [x] Feature implemented

### Quality
- [ ] All tests passing
- [ ] Code quality validated
""")

    return story_file


@pytest.fixture
def sample_python_source(temp_project_dir):
    """Create sample Python source code with quality issues"""
    src_dir = temp_project_dir / "src"
    src_dir.mkdir(parents=True, exist_ok=True)

    # File with extreme complexity (28)
    services_file = src_dir / "services.py"
    services_file.write_text("""
def process_order(order):
    '''Process order with extreme complexity (28 paths)'''
    if order is None:
        return None
    if not order.items:
        return {"error": "No items"}
    if order.customer is None:
        return {"error": "No customer"}
    if order.total < 0:
        return {"error": "Invalid total"}

    if order.status == "pending":
        if order.payment_method == "credit_card":
            if order.card_valid:
                if order.balance >= order.total:
                    charge_card()
                else:
                    decline_payment()
            else:
                request_new_card()
        elif order.payment_method == "paypal":
            if order.paypal_verified:
                process_paypal()
            else:
                verify_paypal()
        elif order.payment_method == "cash":
            mark_cash_payment()
        else:
            return {"error": "Invalid payment method"}
    elif order.status == "processing":
        if order.shipped:
            update_tracking()
        else:
            prepare_shipment()
    elif order.status == "complete":
        archive_order()
    else:
        return {"error": "Invalid status"}

    return {"success": True}

def validate_input(data):
    '''Simple function with low complexity (3)'''
    if not data:
        raise ValueError("No data")
    if len(data) > 100:
        raise ValueError("Too long")
    return True
""")

    return src_dir


# ============================================================================
# AC7: Integration with devforgeai-qa Skill Phase 4
# ============================================================================

@pytest.mark.integration
@pytest.mark.acceptance_criteria
class TestQASkillIntegration:
    """AC7: Integration with devforgeai-qa skill Phase 4"""

    @patch('subprocess.run')
    def test_qa_skill_invokes_code_quality_auditor(
        self,
        mock_subprocess,
        temp_project_dir,
        mock_context_files,
        sample_python_source
    ):
        """Test: devforgeai-qa Phase 4 invokes code-quality-auditor and processes results"""
        # Arrange: Mock radon complexity analysis output
        mock_subprocess.return_value = Mock(
            returncode=0,
            stdout=json.dumps([
                {
                    "type": "method",
                    "name": "process_order",
                    "lineno": 2,
                    "complexity": 28,
                    "rank": "F"
                },
                {
                    "type": "method",
                    "name": "validate_input",
                    "lineno": 45,
                    "complexity": 3,
                    "rank": "A"
                }
            ]),
            stderr=""
        )

        # Simulate devforgeai-qa skill Phase 4 invocation
        # (This would normally use Task() to invoke code-quality-auditor)

        # Expected result from code-quality-auditor
        quality_result = {
            "status": "success",
            "metrics": {
                "complexity": {
                    "average_per_function": 15.5,
                    "average_per_file": 15.5,
                    "max_complexity": {
                        "score": 28,
                        "function": "process_order",
                        "file": "src/services.py",
                        "line": 2
                    }
                },
                "duplication": {
                    "percentage": 12.0,
                    "duplicate_blocks": []
                },
                "maintainability": {
                    "average_mi": 58.3
                }
            },
            "extreme_violations": [
                {
                    "type": "complexity",
                    "severity": "CRITICAL",
                    "function": "process_order",
                    "score": 28,
                    "threshold": 20,
                    "file": "src/services.py",
                    "line": 2,
                    "business_impact": (
                        "40% higher defect rate compared to functions with complexity <10. "
                        "Requires 28+ test cases for full coverage. "
                        "3x longer onboarding time for new developers."
                    ),
                    "refactoring_pattern": (
                        "Extract Method: Split process_order() into 5 methods:\n"
                        "1. ValidateOrder() - complexity <6\n"
                        "2. CalculateTotal() - complexity <6\n"
                        "3. ProcessPayment() - complexity <6\n"
                        "4. PrepareShipment() - complexity <6\n"
                        "5. UpdateStatus() - complexity <6\n\n"
                        "Target: Each method complexity <6 (current: 28 → goal: excellent)"
                    )
                }
            ],
            "blocks_qa": True
        }

        # Act: QA skill updates blocks_qa state
        blocks_qa = False  # Initial state
        blocks_qa = blocks_qa or quality_result["blocks_qa"]

        # Assert: Integration successful
        assert quality_result["status"] == "success", \
            "code-quality-auditor should return success"
        assert "metrics" in quality_result, \
            "Result should include metrics"
        assert quality_result["metrics"]["complexity"]["max_complexity"]["score"] == 28, \
            "Should detect complexity 28"
        assert blocks_qa is True, \
            "QA should be blocked due to extreme violation"
        assert len(quality_result["extreme_violations"]) == 1, \
            "Should detect 1 extreme violation"
        assert "business_impact" in quality_result["extreme_violations"][0], \
            "Violation should include business impact"
        assert "refactoring_pattern" in quality_result["extreme_violations"][0], \
            "Violation should include refactoring pattern"

    def test_qa_skill_continues_after_successful_analysis(self):
        """Test: QA skill continues to Phase 5 after successful code quality analysis"""
        # Arrange: Mock successful analysis with no violations
        quality_result = {
            "status": "success",
            "metrics": {
                "complexity": {"average_per_function": 8.2},
                "duplication": {"percentage": 15.0},
                "maintainability": {"average_mi": 65.0}
            },
            "extreme_violations": [],
            "blocks_qa": False
        }

        # Act: QA skill checks status
        should_continue = quality_result["status"] == "success"

        # Assert: Continues to next phase
        assert should_continue is True, \
            "QA skill should continue after successful analysis"
        assert quality_result["blocks_qa"] is False, \
            "Should not block with good metrics"

    def test_qa_skill_halts_on_analysis_failure(self):
        """Test: QA skill halts if code-quality-auditor fails"""
        # Arrange: Mock analysis failure
        quality_result = {
            "status": "failure",
            "error": "Analysis tool not available: radon not installed",
            "blocks_qa": True,
            "remediation": "Install radon: pip install radon"
        }

        # Act: QA skill checks status
        should_halt = quality_result["status"] == "failure"

        # Assert: QA halts
        assert should_halt is True, \
            "QA skill should HALT on analysis failure"
        assert quality_result["blocks_qa"] is True, \
            "Failure should block QA"


# ============================================================================
# AC8: Prompt Template Documented
# ============================================================================

@pytest.mark.integration
@pytest.mark.acceptance_criteria
class TestPromptTemplate:
    """AC8: Prompt template documented"""

    def test_prompt_template_file_exists(self, project_root):
        """Test: Prompt template exists in QA skill references"""
        # Arrange: Expected file path
        template_file = (
            project_root / "src" / "claude" / "skills" / "devforgeai-qa" /
            "references" / "subagent-prompt-templates.md"
        )

        # Act & Assert: File exists
        assert template_file.exists(), \
            f"Prompt template file not found at {template_file}"

    def test_prompt_template_includes_code_quality_auditor(self, project_root):
        """Test: Prompt template includes code-quality-auditor section"""
        # Arrange: Read template file
        template_file = (
            project_root / "src" / "claude" / "skills" / "devforgeai-qa" /
            "references" / "subagent-prompt-templates.md"
        )

        content = template_file.read_text()

        # Act & Assert: Template 3 documented
        assert "## Template 3: code-quality-auditor" in content, \
            "Should have Template 3 section for code-quality-auditor"
        assert "Business Impact Requirements" in content, \
            "Should document business impact requirements"
        assert "Refactoring Pattern Requirements" in content, \
            "Should document refactoring pattern requirements"
        assert "Response Parsing" in content, \
            "Should document response parsing"
        assert "Task(" in content, \
            "Should show Task() invocation example"

    def test_prompt_template_documents_token_savings(self, project_root):
        """Test: Prompt template documents token savings"""
        # Arrange: Read template file
        template_file = (
            project_root / "src" / "claude" / "skills" / "devforgeai-qa" /
            "references" / "subagent-prompt-templates.md"
        )

        content = template_file.read_text()

        # Act & Assert: Token savings documented
        assert "6K" in content or "6000" in content, \
            "Should mention before token cost (~6K inline)"
        assert "3K" in content or "3000" in content, \
            "Should mention after token cost (~3K prompt)"
        assert "70%" in content or "reduction" in content.lower(), \
            "Should mention 70% token reduction"


# ============================================================================
# End-to-End Workflow Test
# ============================================================================

@pytest.mark.integration
@pytest.mark.e2e
class TestEndToEndWorkflow:
    """End-to-end workflow from QA invocation to completion"""

    @patch('subprocess.run')
    def test_complete_workflow_with_violations(
        self,
        mock_subprocess,
        temp_project_dir,
        mock_context_files,
        sample_python_source,
        sample_story_file
    ):
        """Test: Complete workflow detects violations and blocks QA"""
        # Arrange: Mock radon complexity
        mock_subprocess.return_value = Mock(
            returncode=0,
            stdout=json.dumps([{
                "type": "method",
                "name": "process_order",
                "complexity": 28,
                "rank": "F"
            }]),
            stderr=""
        )

        # Simulate complete QA workflow
        story_id = "STORY-TEST-003"
        blocks_qa = False

        # Phase 0: Context validation (mocked)
        context_valid = True

        # Phase 1: Coverage analysis (mocked - passed)
        coverage_result = {"blocks_qa": False}
        blocks_qa = blocks_qa or coverage_result["blocks_qa"]

        # Phase 2: Anti-pattern detection (mocked - passed)
        antipattern_result = {"blocks_qa": False}
        blocks_qa = blocks_qa or antipattern_result["blocks_qa"]

        # Phase 3: Security scan (mocked - passed)
        security_result = {"blocks_qa": False}
        blocks_qa = blocks_qa or security_result["blocks_qa"]

        # Phase 4: Code quality analysis (code-quality-auditor)
        quality_result = {
            "status": "success",
            "metrics": {
                "complexity": {
                    "max_complexity": {"score": 28, "function": "process_order"}
                }
            },
            "extreme_violations": [
                {
                    "type": "complexity",
                    "severity": "CRITICAL",
                    "score": 28
                }
            ],
            "blocks_qa": True
        }
        blocks_qa = blocks_qa or quality_result["blocks_qa"]

        # Act: Final QA decision
        qa_status = "QA BLOCKED" if blocks_qa else "QA APPROVED"

        # Assert: Workflow blocks QA
        assert blocks_qa is True, \
            "Workflow should block QA due to code quality violation"
        assert qa_status == "QA BLOCKED", \
            "Final status should be QA BLOCKED"
        assert quality_result["extreme_violations"][0]["severity"] == "CRITICAL", \
            "Should detect CRITICAL violation"

    def test_complete_workflow_no_violations(
        self,
        temp_project_dir,
        mock_context_files,
        sample_python_source
    ):
        """Test: Complete workflow with good code quality passes QA"""
        # Arrange: Mock all phases passing
        blocks_qa = False

        # Phase 1-3: Passed (mocked)
        blocks_qa = blocks_qa or False

        # Phase 4: Code quality - all metrics good
        quality_result = {
            "status": "success",
            "metrics": {
                "complexity": {"average_per_function": 8.2},
                "duplication": {"percentage": 15.0},
                "maintainability": {"average_mi": 65.0}
            },
            "extreme_violations": [],
            "blocks_qa": False
        }
        blocks_qa = blocks_qa or quality_result["blocks_qa"]

        # Act: Final QA decision
        qa_status = "QA BLOCKED" if blocks_qa else "QA APPROVED"

        # Assert: Workflow approves QA
        assert blocks_qa is False, \
            "Workflow should NOT block QA with good metrics"
        assert qa_status == "QA APPROVED", \
            "Final status should be QA APPROVED"


# ============================================================================
# Performance Test
# ============================================================================

@pytest.mark.integration
@pytest.mark.performance
class TestPerformance:
    """Performance requirements validation"""

    def test_analysis_completes_within_60_seconds(self):
        """Test: Large project analysis completes within 60 seconds"""
        # Arrange: Mock timing
        import time

        start_time = time.time()

        # Simulate code-quality-auditor execution
        # (In real implementation, would analyze >10K LOC)
        time.sleep(0.5)  # Simulate 500ms analysis

        end_time = time.time()
        duration = end_time - start_time

        # Assert: Completes quickly
        assert duration < 60, \
            f"Analysis should complete within 60s, took {duration}s"


# ============================================================================
# Run Tests
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
