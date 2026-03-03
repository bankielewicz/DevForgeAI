"""
Integration Tests: Long Parameter List Detection (STORY-400)
Story: STORY-400
Type: Integration
Generated: 2026-02-14

Validates cross-component interactions for STORY-400:
1. End-to-end Treelint output -> findings pipeline
2. Integration with existing data_class detection (STORY-399) in Phase 5
3. Output format compatibility with scanner's violation aggregation JSON
4. Grep fallback decision chain (language + exit code -> detection path)

These tests verify component boundaries, NOT individual function behavior
(that is covered by the 82 unit tests in test_ac1-ac5 files).
"""

import json
import os
import re
import sys
import pytest

# Add test directory to path for import
sys.path.insert(0, os.path.dirname(__file__))
from long_parameter_list_detector import (
    detect_long_parameter_list,
    detect_long_parameter_list_grep,
    parse_parameters_from_signature,
    count_effective_parameters,
    should_use_grep_fallback,
    get_long_param_grep_pattern,
    _get_effective_params,
    _build_finding,
    DEFAULT_THRESHOLD,
    TREELINT_SUPPORTED_LANGUAGES,
    UNSUPPORTED_LANGUAGES,
)


# =============================================================================
# Integration Test 1: End-to-End Treelint Output -> Findings Pipeline
# =============================================================================


class TestEndToEndTreelintPipeline:
    """
    Integration: Validates the full pipeline from realistic Treelint JSON
    output through parameter parsing, counting, threshold check, to final
    finding output with all required fields.
    """

    def test_e2e_realistic_treelint_output_produces_valid_findings(self):
        """
        Arrange: Realistic Treelint JSON with multiple functions across files
        Act: Run detect_long_parameter_list on full output
        Assert: Only violating functions produce findings with complete schema
        """
        # Arrange - realistic multi-file, multi-function Treelint output
        treelint_output = {
            "results": [
                {
                    "name": "__init__",
                    "type": "function",
                    "file": "src/models/order.py",
                    "lines": {"start": 12, "end": 30},
                    "signature": "def __init__(self, order_id, customer_id, product_id, quantity, price, discount)",
                },
                {
                    "name": "validate",
                    "type": "function",
                    "file": "src/models/order.py",
                    "lines": {"start": 32, "end": 45},
                    "signature": "def validate(self, strict)",
                },
                {
                    "name": "process_payment",
                    "type": "function",
                    "file": "src/services/payment.py",
                    "lines": {"start": 5, "end": 20},
                    "signature": "def process_payment(amount: float, currency: str, source: str, metadata: dict, idempotency_key: str)",
                },
                {
                    "name": "log_event",
                    "type": "function",
                    "file": "src/utils/logger.py",
                    "lines": {"start": 1, "end": 3},
                    "signature": "def log_event(message, level)",
                },
                {
                    "name": "create_report",
                    "type": "function",
                    "file": "src/services/reporting.py",
                    "lines": {"start": 50, "end": 80},
                    "signature": "def create_report(cls, title, data, format, template, output_path, *args, **kwargs)",
                },
            ]
        }

        # Act
        findings = detect_long_parameter_list(treelint_output, threshold=4)

        # Assert - exactly 3 functions should be flagged
        assert len(findings) == 3

        # __init__ with self excluded: 6 real params > 4
        init_finding = next(f for f in findings if f["function_name"] == "__init__")
        assert init_finding["parameter_count"] == 6
        assert "self" not in init_finding["parameters"]
        assert init_finding["file"] == "src/models/order.py"
        assert init_finding["line"] == 12

        # process_payment: 5 real params > 4
        payment_finding = next(
            f for f in findings if f["function_name"] == "process_payment"
        )
        assert payment_finding["parameter_count"] == 5
        assert "amount" in payment_finding["parameters"]

        # create_report with cls excluded, *args/**kwargs excluded: 5 real params > 4
        report_finding = next(
            f for f in findings if f["function_name"] == "create_report"
        )
        assert report_finding["parameter_count"] == 5
        assert "cls" not in report_finding["parameters"]
        assert "*args" not in report_finding["parameters"]
        assert "**kwargs" not in report_finding["parameters"]

        # validate (1 real param) and log_event (2 params) should NOT appear
        flagged_names = [f["function_name"] for f in findings]
        assert "validate" not in flagged_names
        assert "log_event" not in flagged_names

    def test_e2e_all_findings_have_complete_schema(self):
        """
        Arrange: Treelint output producing findings
        Act: Run detection
        Assert: Every finding has all 9 required fields with correct types
        """
        treelint_output = {
            "results": [
                {
                    "name": "complex_handler",
                    "type": "function",
                    "file": "src/api/handler.py",
                    "lines": {"start": 100, "end": 150},
                    "signature": "def complex_handler(request, response, middleware, config, logger, metrics)",
                },
            ]
        }

        findings = detect_long_parameter_list(treelint_output)

        assert len(findings) == 1
        finding = findings[0]

        # Verify all 9 required fields
        assert finding["smell_type"] == "long_parameter_list"
        assert finding["severity"] == "MEDIUM"
        assert finding["function_name"] == "complex_handler"
        assert finding["file"] == "src/api/handler.py"
        assert finding["line"] == 100
        assert finding["parameter_count"] == 6
        assert finding["parameters"] == [
            "request",
            "response",
            "middleware",
            "config",
            "logger",
            "metrics",
        ]
        assert isinstance(finding["evidence"], str)
        assert len(finding["evidence"]) > 0
        assert isinstance(finding["remediation"], str)
        assert len(finding["remediation"]) > 0

        # Verify NO extra fields (no confidence, no stage2)
        assert set(finding.keys()) == {
            "smell_type",
            "severity",
            "function_name",
            "file",
            "line",
            "parameter_count",
            "parameters",
            "evidence",
            "remediation",
        }

    def test_e2e_empty_treelint_output_returns_empty_list(self):
        """Pipeline handles empty Treelint results gracefully."""
        assert detect_long_parameter_list({"results": []}) == []
        assert detect_long_parameter_list({}) == []

    def test_e2e_malformed_signature_skipped_gracefully(self):
        """Functions with missing/empty signatures are skipped without error."""
        treelint_output = {
            "results": [
                {
                    "name": "no_sig",
                    "type": "function",
                    "file": "src/x.py",
                    "lines": {"start": 1, "end": 2},
                    "signature": "",
                },
                {
                    "name": "good_func",
                    "type": "function",
                    "file": "src/y.py",
                    "lines": {"start": 5, "end": 10},
                    "signature": "def good_func(a, b, c, d, e)",
                },
            ]
        }

        findings = detect_long_parameter_list(treelint_output)
        assert len(findings) == 1
        assert findings[0]["function_name"] == "good_func"


# =============================================================================
# Integration Test 2: Coexistence with Data Class Detection (STORY-399)
# =============================================================================


class TestPhase5CoexistenceWithDataClass:
    """
    Integration: Validates that long_parameter_list findings and data_class
    findings can coexist in the same Phase 5 output without conflict.

    The anti-pattern-scanner Phase 5 produces both data_class (STORY-399)
    and long_parameter_list (STORY-400) findings. They must be
    independently aggregated into violations.medium[].
    """

    def test_long_param_findings_have_distinct_smell_type_from_data_class(self):
        """
        Arrange: A long_parameter_list finding
        Assert: smell_type is 'long_parameter_list', NOT 'data_class'
        """
        treelint_output = {
            "results": [
                {
                    "name": "overloaded",
                    "type": "function",
                    "file": "src/svc.py",
                    "lines": {"start": 1, "end": 5},
                    "signature": "def overloaded(a, b, c, d, e)",
                }
            ]
        }

        findings = detect_long_parameter_list(treelint_output)
        assert len(findings) == 1
        assert findings[0]["smell_type"] == "long_parameter_list"
        assert findings[0]["smell_type"] != "data_class"

    def test_long_param_findings_lack_confidence_field(self):
        """
        Data class findings have a 'confidence' field (two-stage filtering).
        Long parameter list findings must NOT have it (deterministic detection).
        This ensures the two finding types are distinguishable.
        """
        treelint_output = {
            "results": [
                {
                    "name": "many_params",
                    "type": "function",
                    "file": "src/x.py",
                    "lines": {"start": 1, "end": 5},
                    "signature": "def many_params(a, b, c, d, e)",
                }
            ]
        }

        findings = detect_long_parameter_list(treelint_output)
        assert "confidence" not in findings[0]

    def test_long_param_and_data_class_can_merge_into_medium_violations(self):
        """
        Simulate the scanner aggregating both finding types into violations.medium[].
        Both use severity=MEDIUM and can coexist in the same array.
        """
        # Simulate a data_class finding from STORY-399
        data_class_finding = {
            "smell_type": "data_class",
            "severity": "MEDIUM",
            "class_name": "OrderDTO",
            "file": "src/models/order_dto.py",
            "line": 5,
            "method_count": 1,
            "property_count": 8,
            "confidence": 0.85,
            "evidence": "Class has 8 properties and only 1 method",
            "remediation": "Consider adding behavior methods",
        }

        # Generate a long_parameter_list finding from STORY-400
        treelint_output = {
            "results": [
                {
                    "name": "create_order",
                    "type": "function",
                    "file": "src/services/order_service.py",
                    "lines": {"start": 20, "end": 40},
                    "signature": "def create_order(customer, product, qty, discount, shipping)",
                }
            ]
        }
        long_param_findings = detect_long_parameter_list(treelint_output)

        # Merge into violations.medium array (as scanner would)
        medium_violations = [data_class_finding] + long_param_findings

        # Assert both coexist
        assert len(medium_violations) == 2

        smell_types = {v["smell_type"] for v in medium_violations}
        assert smell_types == {"data_class", "long_parameter_list"}

        # Both have severity MEDIUM
        assert all(v["severity"] == "MEDIUM" for v in medium_violations)

        # They have different field sets (data_class has confidence, long_param does not)
        data_class_keys = set(data_class_finding.keys())
        long_param_keys = set(long_param_findings[0].keys())
        assert "confidence" in data_class_keys
        assert "confidence" not in long_param_keys
        assert "parameter_count" in long_param_keys
        assert "parameter_count" not in data_class_keys

    def test_scanner_output_json_structure_compatibility(self):
        """
        Validate that long_parameter_list findings fit into the scanner's
        standard output JSON structure: violations.medium[].
        """
        findings = detect_long_parameter_list(
            {
                "results": [
                    {
                        "name": "func",
                        "type": "function",
                        "file": "x.py",
                        "lines": {"start": 1, "end": 2},
                        "signature": "def func(a, b, c, d, e, f)",
                    }
                ]
            }
        )

        # Build scanner output structure
        scanner_output = {
            "status": "success",
            "story_id": "STORY-400",
            "violations": {
                "critical": [],
                "high": [],
                "medium": findings,
                "low": [],
            },
            "summary": {
                "critical_count": 0,
                "high_count": 0,
                "medium_count": len(findings),
                "low_count": 0,
                "total_violations": len(findings),
            },
            "blocks_qa": False,
        }

        # Validate JSON serialization round-trip
        json_str = json.dumps(scanner_output, indent=2)
        parsed = json.loads(json_str)

        assert parsed["violations"]["medium"][0]["smell_type"] == "long_parameter_list"
        assert parsed["summary"]["medium_count"] == 1
        assert parsed["blocks_qa"] is False  # MEDIUM does not block QA


# =============================================================================
# Integration Test 3: Grep Fallback Decision Chain
# =============================================================================


class TestGrepFallbackDecisionChain:
    """
    Integration: Validates the complete decision chain from
    language + exit code -> fallback decision -> grep detection -> findings.
    """

    def test_e2e_csharp_fallback_chain(self):
        """
        Arrange: C# code with 5+ parameter method
        Act: Check fallback needed, then run grep detection
        Assert: Complete chain produces valid findings
        """
        # Step 1: Decision
        assert should_use_grep_fallback("csharp", treelint_exit_code=0) is True

        # Step 2: Detection
        csharp_code = """
public class OrderService
{
    public void ProcessOrder(int customerId, int productId, int quantity, decimal discount, string shippingMethod)
    {
        // implementation
    }

    public void SimpleMethod(int id, string name)
    {
        // no violation
    }
}
"""
        findings = detect_long_parameter_list_grep(
            csharp_code, "src/OrderService.cs", "csharp"
        )

        # Step 3: Validate
        assert len(findings) == 1
        assert findings[0]["function_name"] == "ProcessOrder"
        assert findings[0]["parameter_count"] == 5
        assert findings[0]["smell_type"] == "long_parameter_list"
        assert findings[0]["severity"] == "MEDIUM"
        assert findings[0]["file"] == "src/OrderService.cs"

    def test_e2e_java_fallback_chain(self):
        """Full Java fallback chain from decision to findings."""
        assert should_use_grep_fallback("java", treelint_exit_code=0) is True

        java_code = """
public class ReportService {
    public void generateReport(String title, String format, String template, String outputPath, boolean compress) {
        // implementation
    }
}
"""
        findings = detect_long_parameter_list_grep(
            java_code, "src/ReportService.java", "java"
        )
        assert len(findings) == 1
        assert findings[0]["function_name"] == "generateReport"
        assert findings[0]["parameter_count"] == 5

    def test_e2e_go_fallback_chain(self):
        """Full Go fallback chain from decision to findings."""
        assert should_use_grep_fallback("go", treelint_exit_code=0) is True

        go_code = """
func CreateOrder(customerID int, productID int, quantity int, discount float64, method string) error {
    return nil
}
"""
        findings = detect_long_parameter_list_grep(
            go_code, "cmd/order.go", "go"
        )
        assert len(findings) == 1
        assert findings[0]["function_name"] == "CreateOrder"

    def test_e2e_treelint_unavailable_triggers_grep_for_supported_lang(self):
        """
        When Treelint binary is missing (exit 127) even for Python,
        the fallback decision should return True, enabling Grep detection.
        """
        # Treelint binary missing
        assert should_use_grep_fallback("python", treelint_exit_code=127) is True
        assert should_use_grep_fallback("python", treelint_exit_code=126) is True

        # But when available, no fallback needed
        assert should_use_grep_fallback("python", treelint_exit_code=0) is False

    def test_e2e_unsupported_language_returns_empty_for_unknown(self):
        """Unknown languages return empty findings from grep (no pattern match)."""
        findings = detect_long_parameter_list_grep(
            "some code with many params", "src/main.rs", "rust"
        )
        assert findings == []

    def test_grep_findings_have_same_schema_as_treelint_findings(self):
        """
        Grep fallback findings must have identical field set to Treelint findings
        so they can be merged into the same violations.medium[] array.
        """
        # Treelint finding
        treelint_output = {
            "results": [
                {
                    "name": "treelint_func",
                    "type": "function",
                    "file": "src/a.py",
                    "lines": {"start": 1, "end": 5},
                    "signature": "def treelint_func(a, b, c, d, e)",
                }
            ]
        }
        treelint_findings = detect_long_parameter_list(treelint_output)

        # Grep finding
        csharp_code = """
public class Svc
{
    public void GrepFunc(int a, int b, int c, int d, int e)
    {
    }
}
"""
        grep_findings = detect_long_parameter_list_grep(
            csharp_code, "src/Svc.cs", "csharp"
        )

        assert len(treelint_findings) == 1
        assert len(grep_findings) == 1

        # Same field set
        treelint_keys = set(treelint_findings[0].keys())
        grep_keys = set(grep_findings[0].keys())
        assert treelint_keys == grep_keys, (
            f"Field mismatch: Treelint has {treelint_keys - grep_keys}, "
            f"Grep has {grep_keys - treelint_keys}"
        )

        # Same fixed values
        assert treelint_findings[0]["smell_type"] == grep_findings[0]["smell_type"]
        assert treelint_findings[0]["severity"] == grep_findings[0]["severity"]


# =============================================================================
# Integration Test 4: Parameter Parsing -> Counting -> Finding Pipeline
# =============================================================================


class TestParameterParsingCountingPipeline:
    """
    Integration: Validates that parse_parameters_from_signature ->
    count_effective_parameters -> _build_finding produces consistent results
    across the full pipeline for complex real-world signatures.
    """

    @pytest.mark.parametrize(
        "signature, expected_effective_count, excluded",
        [
            # Python method with self, type hints, defaults, and variadic
            (
                "def configure(self, host: str, port: int = 5432, db: str = 'test', user: str = 'admin', password: str = '', **kwargs)",
                5,
                {"self", "**kwargs"},
            ),
            # TypeScript function with many typed params
            (
                "function processEvent(eventType: string, payload: object, timestamp: number, source: string, priority: number)",
                5,
                set(),
            ),
            # Python classmethod with cls and *args
            (
                "def from_dict(cls, data: dict, strict: bool, validate: bool, transform: bool, cache: bool, *args)",
                5,
                {"cls", "*args"},
            ),
            # Minimal violation: exactly 5 params
            (
                "def func(a, b, c, d, e)",
                5,
                set(),
            ),
            # Not a violation: exactly 4 params
            (
                "def func(a, b, c, d)",
                4,
                set(),
            ),
        ],
        ids=[
            "python-method-full-complexity",
            "typescript-typed-params",
            "classmethod-with-cls-and-args",
            "minimal-violation",
            "at-threshold-no-violation",
        ],
    )
    def test_pipeline_signature_to_effective_count(
        self, signature, expected_effective_count, excluded
    ):
        """Parse -> count pipeline produces correct effective count."""
        all_params = parse_parameters_from_signature(signature)
        effective = _get_effective_params(all_params)
        effective_count = len(effective)

        assert effective_count == expected_effective_count

        # Verify excluded params are not in effective list
        for exc in excluded:
            assert exc not in effective

    def test_pipeline_consistent_count_between_direct_and_treelint(self):
        """
        The count from parse+count matches what detect_long_parameter_list
        puts in the finding's parameter_count field.
        """
        signature = "def handler(self, request, response, middleware, config, logger, **kwargs)"

        # Direct pipeline
        all_params = parse_parameters_from_signature(signature)
        direct_count = count_effective_parameters(all_params)

        # Through Treelint detection
        treelint_output = {
            "results": [
                {
                    "name": "handler",
                    "type": "function",
                    "file": "src/api.py",
                    "lines": {"start": 1, "end": 10},
                    "signature": signature,
                }
            ]
        }
        findings = detect_long_parameter_list(treelint_output)

        assert direct_count == findings[0]["parameter_count"]
        assert direct_count == 5  # self, **kwargs excluded


# =============================================================================
# Integration Test 5: Scanner Specification Compliance
# =============================================================================


class TestScannerSpecificationCompliance:
    """
    Integration: Validates that the implementation matches the specification
    in src/claude/agents/anti-pattern-scanner.md for Phase 5.
    """

    def test_spec_treelint_command_present(self):
        """Scanner spec must reference 'treelint search --type function --format json'."""
        scanner_path = os.path.normpath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "src",
                "claude",
                "agents",
                "anti-pattern-scanner.md",
            )
        )
        with open(scanner_path, "r", encoding="utf-8") as f:
            content = f.read()

        assert "treelint search --type function --format json" in content

    def test_spec_threshold_matches_implementation(self):
        """Scanner spec threshold (>4) matches implementation DEFAULT_THRESHOLD."""
        assert DEFAULT_THRESHOLD == 4

        scanner_path = os.path.normpath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "src",
                "claude",
                "agents",
                "anti-pattern-scanner.md",
            )
        )
        with open(scanner_path, "r", encoding="utf-8") as f:
            content = f.read()

        assert "parameter_count > 4" in content

    def test_spec_output_schema_field_count(self):
        """Scanner spec says 'exactly 9 fields' - implementation must match."""
        treelint_output = {
            "results": [
                {
                    "name": "func",
                    "type": "function",
                    "file": "x.py",
                    "lines": {"start": 1, "end": 2},
                    "signature": "def func(a, b, c, d, e)",
                }
            ]
        }
        findings = detect_long_parameter_list(treelint_output)
        assert len(findings[0]) == 9

    def test_spec_no_confidence_field(self):
        """Scanner spec says 'No confidence field' for long param findings."""
        treelint_output = {
            "results": [
                {
                    "name": "func",
                    "type": "function",
                    "file": "x.py",
                    "lines": {"start": 1, "end": 2},
                    "signature": "def func(a, b, c, d, e)",
                }
            ]
        }
        findings = detect_long_parameter_list(treelint_output)
        assert "confidence" not in findings[0]

    def test_spec_language_support_sets(self):
        """Supported and unsupported language sets match spec."""
        assert TREELINT_SUPPORTED_LANGUAGES == {"python", "typescript", "javascript"}
        assert UNSUPPORTED_LANGUAGES == {"csharp", "java", "go"}

    def test_spec_grep_fallback_pattern_format(self):
        """Grep pattern matches spec format for 4+ commas."""
        pattern = get_long_param_grep_pattern()
        # Pattern should match 5+ param signatures (4+ commas)
        assert re.search(pattern, "func(a, b, c, d, e)") is not None
        assert re.search(pattern, "func(a, b, c, d)") is None

    def test_spec_severity_is_medium(self):
        """Scanner spec says severity is MEDIUM for long parameter list."""
        finding = _build_finding("f", "x.py", 1, 5, ["a", "b", "c", "d", "e"])
        assert finding["severity"] == "MEDIUM"

    def test_spec_remediation_suggests_parameter_object(self):
        """Scanner spec says remediation suggests Parameter Object or data class."""
        finding = _build_finding("f", "x.py", 1, 5, ["a", "b", "c", "d", "e"])
        remediation_lower = finding["remediation"].lower()
        assert "parameter object" in remediation_lower or "data class" in remediation_lower
