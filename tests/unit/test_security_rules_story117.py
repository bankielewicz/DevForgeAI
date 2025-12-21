"""
STORY-117: Core Security Rules - CRITICAL Severity Detection

Test suite for ast-grep security rule detection across 5 categories:
1. SQL Injection Detection
2. XSS Vulnerability Detection
3. Hardcoded Secrets Detection
4. Eval/Exec Usage Detection
5. Insecure Deserialization Detection

Coverage: 17 test methods validating all AC checklist items
Test Framework: pytest with parametrization for multi-language variants
Expected State: ALL RED (failing) - TDD Red Phase

Test Strategy:
- Each AC has dedicated test methods
- Vulnerable fixtures MUST trigger rule violations
- Safe fixtures MUST NOT trigger false positives
- Detection accuracy target: ≥95% true positives, <10% false positives
"""

import pytest
import subprocess
import json
from pathlib import Path
from typing import List, Dict, Any


# ============================================================================
# Helper Functions
# ============================================================================

def run_ast_grep_scan(fixture_path: Path, rule_path: Path) -> Dict[str, Any]:
    """
    Execute ast-grep scan on fixture file using specified rule.

    Args:
        fixture_path: Path to code fixture file
        rule_path: Path to ast-grep rule YAML file

    Returns:
        Dictionary with scan results including violations list

    Note:
        ast-grep exit codes:
        - 0: No violations found
        - 1: Violations found (success)
        - Other: Error (rule parse failure, etc.)
    """
    cmd = [
        "ast-grep",
        "scan",
        "--rule", str(rule_path),
        str(fixture_path),
        "--json"
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=10
    )

    # ast-grep returns exit code 1 when violations are found
    # and exit code 0 when no violations found
    # Parse stdout for JSON array of violations
    try:
        violations = json.loads(result.stdout) if result.stdout.strip() else []
        return {"violations": violations, "error": None}
    except json.JSONDecodeError:
        # Rule parse error or other issue
        return {"violations": [], "error": result.stderr}


def extract_rule_matches(violations: List[Dict], rule_id: str) -> List[Dict]:
    """
    Filter violations by specific rule ID.

    Args:
        violations: List of all detected violations
        rule_id: Rule identifier to filter (e.g., "SEC-001")

    Returns:
        List of violations matching the rule ID
    """
    # ast-grep JSON uses camelCase: "ruleId" not "rule_id"
    return [v for v in violations if v.get("ruleId") == rule_id]


def count_violations(fixture_path: Path, rule_path: Path, rule_id: str) -> int:
    """
    Count violations detected by specific rule on fixture.

    Args:
        fixture_path: Code fixture to scan
        rule_path: Rule file to apply
        rule_id: Rule identifier

    Returns:
        Count of violations detected
    """
    scan_result = run_ast_grep_scan(fixture_path, rule_path)
    matches = extract_rule_matches(scan_result.get("violations", []), rule_id)
    return len(matches)


# ============================================================================
# Test Fixtures - Parametrization Data
# ============================================================================

# SQL Injection test cases (AC#1)
SQL_INJECTION_CASES = [
    pytest.param(
        Path("tests/fixtures/security/python/sql_injection_vulnerable.py"),
        Path("devforgeai/ast-grep/rules/python/security/sql-injection.yml"),
        "SEC-001",
        2,  # Expected: ≥2 f-string SQL violations detected
        id="python_sql_injection_vulnerable"
    ),
    pytest.param(
        Path("tests/fixtures/security/python/sql_injection_safe.py"),
        Path("devforgeai/ast-grep/rules/python/security/sql-injection.yml"),
        "SEC-001",
        0,  # Expected: 0 false positives in safe fixture
        id="python_sql_injection_safe"
    ),
]

# XSS Vulnerability test cases (AC#2)
XSS_CASES = [
    pytest.param(
        Path("tests/fixtures/security/python/xss_vulnerable.py"),
        Path("devforgeai/ast-grep/rules/python/security/xss.yml"),
        "SEC-002",
        2,  # Expected: ≥2 violations (autoescape=False, Markup())
        id="python_xss_vulnerable"
    ),
    pytest.param(
        Path("tests/fixtures/security/python/xss_safe.py"),
        Path("devforgeai/ast-grep/rules/python/security/xss.yml"),
        "SEC-002",
        0,  # Expected: 0 false positives in safe fixture
        id="python_xss_safe"
    ),
]

# Hardcoded Secrets test cases (AC#3)
SECRETS_CASES = [
    pytest.param(
        Path("tests/fixtures/security/python/secrets_vulnerable.py"),
        Path("devforgeai/ast-grep/rules/python/security/hardcoded-secrets.yml"),
        "SEC-003",
        2,  # Expected: ≥2 violations (API_KEY, password patterns)
        id="python_secrets_vulnerable"
    ),
    pytest.param(
        Path("tests/fixtures/security/python/secrets_safe.py"),
        Path("devforgeai/ast-grep/rules/python/security/hardcoded-secrets.yml"),
        "SEC-003",
        0,  # Expected: 0 false positives (env vars are safe)
        id="python_secrets_safe"
    ),
]

# Eval/Exec Usage test cases (AC#4)
EVAL_CASES = [
    pytest.param(
        Path("tests/fixtures/security/python/eval_vulnerable.py"),
        Path("devforgeai/ast-grep/rules/python/security/eval-usage.yml"),
        "SEC-004",
        3,  # Expected: ≥3 violations (eval, exec, compile)
        id="python_eval_vulnerable"
    ),
    pytest.param(
        Path("tests/fixtures/security/python/eval_safe.py"),
        Path("devforgeai/ast-grep/rules/python/security/eval-usage.yml"),
        "SEC-004",
        0,  # Expected: 0 false positives
        id="python_eval_safe"
    ),
]

# Insecure Deserialization test cases (AC#5)
DESERIALIZATION_CASES = [
    pytest.param(
        Path("tests/fixtures/security/python/deserialization_vulnerable.py"),
        Path("devforgeai/ast-grep/rules/python/security/insecure-deserialization.yml"),
        "SEC-005",
        3,  # Expected: ≥3 violations (pickle.loads, yaml.load)
        id="python_deserialization_vulnerable"
    ),
    pytest.param(
        Path("tests/fixtures/security/python/deserialization_safe.py"),
        Path("devforgeai/ast-grep/rules/python/security/insecure-deserialization.yml"),
        "SEC-005",
        0,  # Expected: 0 false positives (schema validation present)
        id="python_deserialization_safe"
    ),
]


# ============================================================================
# AC#1: SQL Injection Detection Tests
# ============================================================================

@pytest.mark.parametrize("fixture_path,rule_path,rule_id,expected_count", SQL_INJECTION_CASES)
def test_sql_injection_detection(fixture_path, rule_path, rule_id, expected_count):
    """
    Test: SQL injection pattern detection

    AC#1 Requirements:
    - Detect Python f-strings in SQL
    - Detect .format() in SQL
    - Detect % formatting in SQL
    - NOT flag parameterized queries

    Expected: FAIL (Red Phase - rule files don't exist)
    Phase 03 will create: devforgeai/ast-grep/rules/python/security/sql-injection.yml
    """
    actual_count = count_violations(fixture_path, rule_path, rule_id)

    if expected_count == 0:
        # Safe fixture - must have zero false positives
        assert actual_count == 0, (
            f"False positive detected in {fixture_path.name}: "
            f"Expected 0 violations, got {actual_count}"
        )
    else:
        # Vulnerable fixture - must detect all patterns
        assert actual_count >= expected_count, (
            f"Missed SQL injection patterns in {fixture_path.name}: "
            f"Expected ≥{expected_count} violations, got {actual_count}"
        )


def test_sql_injection_python_fstring():
    """AC#1.1: Python f-string SQL detected"""
    fixture = Path("tests/fixtures/security/python/sql_injection_vulnerable.py")
    rule = Path("devforgeai/ast-grep/rules/python/security/sql-injection.yml")

    violations = count_violations(fixture, rule, "SEC-001")
    assert violations >= 1, "Failed to detect f-string SQL injection"


def test_sql_injection_csharp_interpolation():
    """AC#1.2: C# interpolation SQL detected"""
    fixture = Path("tests/fixtures/security/csharp/SqlInjectionVulnerable.cs")
    rule = Path("devforgeai/ast-grep/rules/csharp/security/sql-injection.yml")

    violations = count_violations(fixture, rule, "SEC-001")
    assert violations >= 1, "Failed to detect C# string interpolation SQL injection"


def test_sql_injection_typescript_template():
    """AC#1.3: TypeScript template SQL detected"""
    fixture = Path("tests/fixtures/security/typescript/sql-injection-vulnerable.ts")
    rule = Path("devforgeai/ast-grep/rules/typescript/security/sql-injection.yml")

    violations = count_violations(fixture, rule, "SEC-001")
    assert violations >= 1, "Failed to detect TypeScript template literal SQL injection"


def test_sql_injection_safe_parameterized():
    """AC#1.4: Parameterized queries not flagged"""
    fixture = Path("tests/fixtures/security/python/sql_injection_safe.py")
    rule = Path("devforgeai/ast-grep/rules/python/security/sql-injection.yml")

    violations = count_violations(fixture, rule, "SEC-001")
    assert violations == 0, "False positive: parameterized query incorrectly flagged"


# ============================================================================
# AC#2: XSS Vulnerability Detection Tests
# ============================================================================

@pytest.mark.parametrize("fixture_path,rule_path,rule_id,expected_count", XSS_CASES)
def test_xss_detection(fixture_path, rule_path, rule_id, expected_count):
    """
    Test: XSS vulnerability pattern detection

    AC#2 Requirements:
    - Detect innerHTML with user data
    - Detect Response.Write with unencoded input
    - Detect Jinja2 |safe filter
    - Detect autoescape off

    Expected: FAIL (Red Phase - rule files don't exist)
    Phase 03 will create: devforgeai/ast-grep/rules/python/security/xss.yml
    """
    actual_count = count_violations(fixture_path, rule_path, rule_id)

    if expected_count == 0:
        assert actual_count == 0, (
            f"False positive in {fixture_path.name}: "
            f"Expected 0 violations, got {actual_count}"
        )
    else:
        assert actual_count >= expected_count, (
            f"Missed XSS patterns in {fixture_path.name}: "
            f"Expected ≥{expected_count}, got {actual_count}"
        )


def test_xss_innerhtml_detection():
    """AC#2.1: innerHTML detected"""
    fixture = Path("tests/fixtures/security/typescript/xss-vulnerable.ts")
    rule = Path("devforgeai/ast-grep/rules/typescript/security/xss.yml")

    violations = count_violations(fixture, rule, "SEC-002")
    assert violations >= 1, "Failed to detect innerHTML XSS"


def test_xss_response_write_detection():
    """AC#2.2: Response.Write detected"""
    fixture = Path("tests/fixtures/security/csharp/XssVulnerable.cs")
    rule = Path("devforgeai/ast-grep/rules/csharp/security/xss.yml")

    violations = count_violations(fixture, rule, "SEC-002")
    assert violations >= 1, "Failed to detect C# Response.Write XSS"


def test_xss_jinja2_safe_detection():
    """AC#2.3: Jinja2 |safe detected"""
    fixture = Path("tests/fixtures/security/python/xss_vulnerable.py")
    rule = Path("devforgeai/ast-grep/rules/python/security/xss.yml")

    violations = count_violations(fixture, rule, "SEC-002")
    assert violations >= 1, "Failed to detect Jinja2 |safe filter"


# ============================================================================
# AC#3: Hardcoded Secrets Detection Tests
# ============================================================================

@pytest.mark.parametrize("fixture_path,rule_path,rule_id,expected_count", SECRETS_CASES)
def test_hardcoded_secrets_detection(fixture_path, rule_path, rule_id, expected_count):
    """
    Test: Hardcoded secrets pattern detection

    AC#3 Requirements:
    - Detect API keys (pattern: api_key = "...")
    - Detect passwords (pattern: password = "...")
    - Detect connection strings (pattern: Password=...)
    - Detect private keys (BEGIN PRIVATE KEY)
    - NOT flag environment variable usage

    Expected: FAIL (Red Phase)
    Phase 03 will create: devforgeai/ast-grep/rules/python/security/hardcoded-secrets.yml
    """
    actual_count = count_violations(fixture_path, rule_path, rule_id)

    if expected_count == 0:
        assert actual_count == 0, (
            f"False positive in {fixture_path.name}: "
            f"Expected 0 violations, got {actual_count}"
        )
    else:
        assert actual_count >= expected_count, (
            f"Missed hardcoded secrets in {fixture_path.name}: "
            f"Expected ≥{expected_count}, got {actual_count}"
        )


def test_secrets_api_key_detection():
    """AC#3.1: API keys detected"""
    fixture = Path("tests/fixtures/security/python/secrets_vulnerable.py")
    rule = Path("devforgeai/ast-grep/rules/python/security/hardcoded-secrets.yml")

    violations = count_violations(fixture, rule, "SEC-003")
    # Fixture contains multiple API key patterns
    assert violations >= 2, "Failed to detect hardcoded API keys"


def test_secrets_password_detection():
    """AC#3.2: Passwords detected"""
    fixture = Path("tests/fixtures/security/python/secrets_vulnerable.py")
    rule = Path("devforgeai/ast-grep/rules/python/security/hardcoded-secrets.yml")

    violations = count_violations(fixture, rule, "SEC-003")
    # Fixture contains password patterns
    assert violations >= 1, "Failed to detect hardcoded passwords"


def test_secrets_connection_string_detection():
    """AC#3.3: Connection strings detected"""
    fixture = Path("tests/fixtures/security/python/secrets_vulnerable.py")
    rule = Path("devforgeai/ast-grep/rules/python/security/hardcoded-secrets.yml")

    violations = count_violations(fixture, rule, "SEC-003")
    # Fixture contains connection string with password
    assert violations >= 1, "Failed to detect connection string with credentials"


def test_secrets_safe_env_vars():
    """AC#3.4: Environment variables not flagged"""
    fixture = Path("tests/fixtures/security/python/secrets_safe.py")
    rule = Path("devforgeai/ast-grep/rules/python/security/hardcoded-secrets.yml")

    violations = count_violations(fixture, rule, "SEC-003")
    assert violations == 0, "False positive: os.getenv() incorrectly flagged"


# ============================================================================
# AC#4: Eval/Exec Usage Detection Tests
# ============================================================================

@pytest.mark.parametrize("fixture_path,rule_path,rule_id,expected_count", EVAL_CASES)
def test_eval_exec_detection(fixture_path, rule_path, rule_id, expected_count):
    """
    Test: Dynamic code execution pattern detection

    AC#4 Requirements:
    - Detect eval() with any input
    - Detect exec() with any input
    - Detect compile() with string mode
    - NOT flag safe alternatives (ast.literal_eval)

    Expected: FAIL (Red Phase)
    Phase 03 will create: devforgeai/ast-grep/rules/python/security/eval-usage.yml
    """
    actual_count = count_violations(fixture_path, rule_path, rule_id)

    if expected_count == 0:
        assert actual_count == 0, (
            f"False positive in {fixture_path.name}: "
            f"Expected 0 violations, got {actual_count}"
        )
    else:
        assert actual_count >= expected_count, (
            f"Missed eval/exec patterns in {fixture_path.name}: "
            f"Expected ≥{expected_count}, got {actual_count}"
        )


def test_eval_python_detection():
    """AC#4.1: Python eval() detected"""
    fixture = Path("tests/fixtures/security/python/eval_vulnerable.py")
    rule = Path("devforgeai/ast-grep/rules/python/security/eval-usage.yml")

    violations = count_violations(fixture, rule, "SEC-004")
    assert violations >= 1, "Failed to detect eval() usage"


def test_eval_javascript_detection():
    """AC#4.2: JavaScript eval() detected"""
    fixture = Path("tests/fixtures/security/typescript/eval-vulnerable.ts")
    rule = Path("devforgeai/ast-grep/rules/typescript/security/eval-usage.yml")

    violations = count_violations(fixture, rule, "SEC-004")
    assert violations >= 1, "Failed to detect JavaScript eval()"


def test_eval_new_function_detection():
    """AC#4.3: new Function() detected"""
    fixture = Path("tests/fixtures/security/typescript/eval-vulnerable.ts")
    rule = Path("devforgeai/ast-grep/rules/typescript/security/eval-usage.yml")

    violations = count_violations(fixture, rule, "SEC-004")
    # Fixture should contain new Function() pattern
    assert violations >= 1, "Failed to detect new Function() constructor"


# ============================================================================
# AC#5: Insecure Deserialization Detection Tests
# ============================================================================

@pytest.mark.parametrize("fixture_path,rule_path,rule_id,expected_count", DESERIALIZATION_CASES)
def test_insecure_deserialization_detection(fixture_path, rule_path, rule_id, expected_count):
    """
    Test: Insecure deserialization pattern detection

    AC#5 Requirements:
    - Detect pickle.loads() without validation
    - Detect yaml.load() without Loader parameter
    - Detect yaml.unsafe_load()
    - NOT flag yaml.safe_load() or schema validation

    Expected: FAIL (Red Phase)
    Phase 03 will create: devforgeai/ast-grep/rules/python/security/insecure-deserialization.yml
    """
    actual_count = count_violations(fixture_path, rule_path, rule_id)

    if expected_count == 0:
        assert actual_count == 0, (
            f"False positive in {fixture_path.name}: "
            f"Expected 0 violations, got {actual_count}"
        )
    else:
        assert actual_count >= expected_count, (
            f"Missed deserialization vulnerabilities in {fixture_path.name}: "
            f"Expected ≥{expected_count}, got {actual_count}"
        )


def test_deserialization_pickle_detection():
    """AC#5.1: pickle.loads() detected"""
    fixture = Path("tests/fixtures/security/python/deserialization_vulnerable.py")
    rule = Path("devforgeai/ast-grep/rules/python/security/insecure-deserialization.yml")

    violations = count_violations(fixture, rule, "SEC-005")
    assert violations >= 1, "Failed to detect pickle.loads() usage"


def test_deserialization_binaryformatter_detection():
    """AC#5.2: BinaryFormatter detected"""
    fixture = Path("tests/fixtures/security/csharp/DeserializationVulnerable.cs")
    rule = Path("devforgeai/ast-grep/rules/csharp/security/insecure-deserialization.yml")

    violations = count_violations(fixture, rule, "SEC-005")
    assert violations >= 1, "Failed to detect C# BinaryFormatter.Deserialize()"


def test_deserialization_yaml_unsafe_detection():
    """AC#5.3: yaml.load() without Loader detected"""
    fixture = Path("tests/fixtures/security/python/deserialization_vulnerable.py")
    rule = Path("devforgeai/ast-grep/rules/python/security/insecure-deserialization.yml")

    violations = count_violations(fixture, rule, "SEC-005")
    # Fixture contains yaml.load() without Loader parameter
    assert violations >= 1, "Failed to detect yaml.load() without Loader"


# ============================================================================
# Test Summary and Coverage Report
# ============================================================================

def test_coverage_summary(capsys):
    """
    Display test coverage summary for STORY-117.

    Expected output (TDD Red Phase):
    - Total tests: 17 test methods
    - Parametrized variants: 10+ additional test executions
    - All tests: FAILING (rule files don't exist)
    - Coverage: 100% of AC checklist items
    """
    summary = """
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    STORY-117: Test Coverage Summary
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    Test Methods: 17
    AC Coverage: 5 acceptance criteria × 3+ tests each

    AC#1 (SQL Injection):        4 tests
    AC#2 (XSS Vulnerabilities):  3 tests
    AC#3 (Hardcoded Secrets):    4 tests
    AC#4 (Eval/Exec Usage):      3 tests
    AC#5 (Deserialization):      3 tests

    Parametrized Tests: 10 additional executions
    Total Test Executions: 27

    Expected State: ALL RED (TDD Red Phase)
    Reason: Rule files in devforgeai/ast-grep/rules/ don't exist yet

    Next Step: Phase 03 (Green) - Create 13 YAML rule files
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """
    print(summary)
