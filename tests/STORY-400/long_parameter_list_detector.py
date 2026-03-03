"""
Long Parameter List Detection - Implementation Module
Story: STORY-400
Phase: TDD Green

Provides detection logic for anti-pattern-scanner Phase 5 (Code Smells):
- Treelint-based parameter counting for Python, TypeScript, JavaScript
- Self/cls exclusion for Python methods
- Variadic parameter (*args/**kwargs) exclusion
- Grep fallback for unsupported languages (C#, Java, Go)
- LongParameterListFinding output schema

Threshold: parameter_count > 4 flags violation (MEDIUM severity).
No two-stage filtering required (parameter count is deterministic).
"""

import re
from typing import Optional


# =============================================================================
# Constants
# =============================================================================

TREELINT_SUPPORTED_LANGUAGES = {"python", "typescript", "javascript"}
UNSUPPORTED_LANGUAGES = {"csharp", "java", "go"}
DEFAULT_THRESHOLD = 4


# =============================================================================
# Parameter Parsing from Treelint Signatures
# =============================================================================


def parse_parameters_from_signature(signature: str) -> list[str]:
    """
    Extract parameter names from a Treelint function signature string.

    Handles:
    - Python: def func(a, b: int, c="default", *args, **kwargs)
    - TypeScript: function func(a: string, b: number)
    - JavaScript arrow: const handler = (a, b, c) =>

    Returns list of parameter name strings (including self, cls, *args, **kwargs).
    """
    # Extract content between parentheses
    paren_match = re.search(r"\(([^)]*)\)", signature)
    if not paren_match:
        return []

    params_str = paren_match.group(1).strip()
    if not params_str:
        return []

    # Split by comma and extract parameter names
    raw_params = params_str.split(",")
    result = []

    for raw_param in raw_params:
        param = raw_param.strip()
        if not param:
            continue

        # Preserve * and ** prefix for variadic detection
        prefix = ""
        if param.startswith("**"):
            prefix = "**"
            param = param[2:]
        elif param.startswith("*"):
            prefix = "*"
            param = param[1:]

        # Remove type annotation (: type)
        if ":" in param:
            param = param.split(":")[0].strip()

        # Remove default value (= value)
        if "=" in param:
            param = param.split("=")[0].strip()

        # Clean whitespace
        param = param.strip()

        if param:
            result.append(prefix + param)

    return result


# =============================================================================
# Effective Parameter Counting
# =============================================================================


def count_effective_parameters(params: list[str]) -> int:
    """
    Count parameters excluding self/cls (first position only) and variadic (*args, **kwargs).

    Rules:
    - self/cls excluded ONLY when in first position
    - Any parameter starting with * or ** is excluded (covers *args, **kwargs, *extra, **options)
    - All other parameters are counted

    Note: Delegates to _get_effective_params to avoid DRY violation (STORY-400 refactoring).
    """
    return len(_get_effective_params(params))


def _get_effective_params(params: list[str]) -> list[str]:
    """
    Return the list of effective parameter names (excluding self/cls and variadic).

    Used internally to populate the 'parameters' field in findings.
    """
    if not params:
        return []

    effective = []
    for i, param in enumerate(params):
        if i == 0 and param in ("self", "cls"):
            continue
        if param.startswith("*"):
            continue
        effective.append(param)

    return effective


def _build_finding(
    func_name: str,
    file_path: str,
    line: int,
    param_count: int,
    param_names: list[str],
    threshold: int = DEFAULT_THRESHOLD,
) -> dict:
    """
    Build a LongParameterListFinding dict with standard fields.

    Extracted to avoid DRY violation (STORY-400 refactoring).
    Used by both detect_long_parameter_list and detect_long_parameter_list_grep.
    """
    return {
        "smell_type": "long_parameter_list",
        "severity": "MEDIUM",
        "function_name": func_name,
        "file": file_path,
        "line": line,
        "parameter_count": param_count,
        "parameters": param_names,
        "evidence": (
            f"Function '{func_name}' has {param_count} parameters "
            f"(threshold: {threshold}). "
            f"Parameters: {', '.join(param_names)}"
        ),
        "remediation": (
            "Consider grouping related parameters into a Parameter Object "
            "or data class to reduce the number of individual arguments."
        ),
    }


# =============================================================================
# Treelint-Based Detection
# =============================================================================


def detect_long_parameter_list(
    treelint_output: dict, threshold: int = DEFAULT_THRESHOLD
) -> list[dict]:
    """
    Detect functions with parameter count exceeding threshold from Treelint output.

    Args:
        treelint_output: Treelint JSON output with 'results' array.
            Each result has: name, type, file, lines.start, signature.
        threshold: Maximum allowed parameters before flagging (default: 4).
            Functions with parameter_count > threshold are flagged.

    Returns:
        List of LongParameterListFinding dicts for violating functions.
        Each finding contains: smell_type, severity, function_name, file, line,
        parameter_count, parameters, evidence, remediation.
        No 'confidence' field (detection is deterministic, not probabilistic).
    """
    results = treelint_output.get("results", [])
    findings = []

    for result in results:
        signature = result.get("signature", "")
        if not signature:
            continue

        all_params = parse_parameters_from_signature(signature)
        effective_params = _get_effective_params(all_params)
        effective_count = len(effective_params)

        if effective_count > threshold:
            finding = _build_finding(
                func_name=result["name"],
                file_path=result["file"],
                line=result["lines"]["start"],
                param_count=effective_count,
                param_names=effective_params,
                threshold=threshold,
            )
            findings.append(finding)

    return findings


# =============================================================================
# Grep Fallback for Unsupported Languages
# =============================================================================


def get_long_param_grep_pattern() -> str:
    """
    Return Grep regex pattern for detecting function signatures with 5+ parameters.

    The pattern matches signatures containing 4+ commas (indicating 5+ parameters).
    Works across Python, C#, Java, Go function declaration styles.
    """
    # Match: opening paren, then at least 4 commas within the param list, then closing paren
    # This catches any function/method with 5+ parameters
    return r"\w+\s*\([^)]*,[^)]*,[^)]*,[^)]*,[^)]*\)"


# Language-specific function declaration patterns for Grep fallback
_LANGUAGE_PATTERNS = {
    "csharp": re.compile(
        r"(?:public|private|protected|internal|static|\s)+"
        r"\w+\s+(\w+)\s*\(([^)]+)\)",
        re.MULTILINE,
    ),
    "java": re.compile(
        r"(?:public|private|protected|static|\s)+"
        r"\w+\s+(\w+)\s*\(([^)]+)\)",
        re.MULTILINE,
    ),
    "go": re.compile(
        r"func\s+(\w+)\s*\(([^)]+)\)",
        re.MULTILINE,
    ),
}


def detect_long_parameter_list_grep(
    code_content: str, file_path: str, language: str
) -> list[dict]:
    """
    Detect long parameter lists using Grep patterns for unsupported languages.

    Args:
        code_content: Source code content to scan.
        file_path: File path for the finding.
        language: Programming language (csharp, java, go).

    Returns:
        List of LongParameterListFinding dicts for violating functions.
    """
    pattern = _LANGUAGE_PATTERNS.get(language)
    if pattern is None:
        return []

    findings = []
    lines = code_content.split("\n")

    for match in pattern.finditer(code_content):
        func_name = match.group(1)
        params_str = match.group(2).strip()

        # Count parameters by counting commas + 1
        param_parts = [p.strip() for p in params_str.split(",") if p.strip()]
        param_count = len(param_parts)

        if param_count > DEFAULT_THRESHOLD:
            # Determine line number
            match_start = match.start()
            line_number = code_content[:match_start].count("\n") + 1

            # Extract simple parameter names (strip types for display)
            param_names = []
            for p in param_parts:
                # For typed languages, take the last word as the name
                tokens = p.strip().split()
                if tokens:
                    param_names.append(tokens[-1])

            finding = _build_finding(
                func_name=func_name,
                file_path=file_path,
                line=line_number,
                param_count=param_count,
                param_names=param_names,
                threshold=DEFAULT_THRESHOLD,
            )
            findings.append(finding)

    return findings


# =============================================================================
# Fallback Decision Logic
# =============================================================================


def should_use_grep_fallback(language: str, treelint_exit_code: int) -> bool:
    """
    Determine if Grep fallback should be used based on language and Treelint exit code.

    Returns True if:
    - Language is not supported by Treelint (C#, Java, Go)
    - OR Treelint exit code is 127 (binary not found) or 126 (permission denied)

    Returns False if:
    - Language is supported by Treelint AND Treelint exit code is 0
    """
    if language.lower() in UNSUPPORTED_LANGUAGES:
        return True
    if treelint_exit_code in (126, 127):
        return True
    return False
