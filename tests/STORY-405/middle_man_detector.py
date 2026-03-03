"""
Middle Man Detection - Implementation Module
Story: STORY-405
Phase: TDD Green (Implemented)

Provides detection logic for anti-pattern-scanner Phase 5 (Code Smells):
- Treelint-based method body size analysis for Python, TypeScript, JavaScript
- Delegation ratio calculation (delegation_methods / total_methods)
- Minimum method threshold enforcement (>= 3 methods)
- Grep fallback for unsupported languages (C#, Java, Go)
- MiddleManFinding output schema

Business Rules:
- BR-001: Delegation method = body size <= 2 lines
- BR-002: Middle man threshold = delegation_ratio > 0.80
- BR-003: Minimum method count >= 3
- BR-004: Facade classes with complex orchestration (>2 lines) are NOT middle men

Threshold: delegation_ratio > 0.80 flags violation (MEDIUM severity).
"""

import re
from typing import Optional


# =============================================================================
# Constants
# =============================================================================

TREELINT_SUPPORTED_LANGUAGES = {"python", "typescript", "javascript"}
UNSUPPORTED_LANGUAGES = {"csharp", "java", "go"}
DEFAULT_DELEGATION_THRESHOLD = 0.80
DEFAULT_MIN_METHODS = 3
DEFAULT_DELEGATION_BODY_SIZE = 2


# =============================================================================
# Method Body Size Calculation
# =============================================================================


def calculate_method_body_size(method: dict) -> int:
    """
    Calculate method body size from Treelint lines.start and lines.end.

    Args:
        method: Treelint method result dict with 'lines' containing 'start' and 'end'.

    Returns:
        Body size as (lines.end - lines.start).
        Returns -1 if lines data is unavailable.
    """
    try:
        lines = method.get("lines")
        if lines is None:
            return -1
        start = lines.get("start")
        end = lines.get("end")
        if start is None or end is None:
            return -1
        return end - start
    except (KeyError, TypeError, AttributeError):
        return -1


def is_delegation_method(
    method: dict, max_body_size: int = DEFAULT_DELEGATION_BODY_SIZE
) -> bool:
    """
    Determine if a method is a delegation method based on body size.

    A delegation method has body_size <= max_body_size (default: 2 lines),
    indicating it contains only a single delegation call (possibly with a return).

    Args:
        method: Treelint method result dict.
        max_body_size: Maximum body size to classify as delegation (default: 2).

    Returns:
        True if method body size <= max_body_size, False otherwise.
        Returns False if body size cannot be calculated.
    """
    body_size = calculate_method_body_size(method)
    if body_size < 0:
        return False
    return body_size <= max_body_size


# =============================================================================
# Delegation Ratio Calculation
# =============================================================================


def calculate_delegation_ratio(
    methods: list[dict],
    max_body_size: int = DEFAULT_DELEGATION_BODY_SIZE,
) -> float:
    """
    Calculate the delegation ratio for a class.

    delegation_ratio = delegation_methods / total_methods

    Args:
        methods: List of Treelint method result dicts for a single class.
        max_body_size: Maximum body size for delegation classification.

    Returns:
        Delegation ratio as float (0.0 to 1.0).
        Returns 0.0 if no methods provided.
    """
    if not methods:
        return 0.0
    delegation_count = count_delegation_methods(methods, max_body_size)
    return delegation_count / len(methods)


def count_delegation_methods(
    methods: list[dict],
    max_body_size: int = DEFAULT_DELEGATION_BODY_SIZE,
) -> int:
    """
    Count the number of delegation methods in a class.

    Args:
        methods: List of Treelint method result dicts.
        max_body_size: Maximum body size for delegation classification.

    Returns:
        Number of methods with body_size <= max_body_size.
    """
    return sum(1 for m in methods if is_delegation_method(m, max_body_size))


# =============================================================================
# Middle Man Detection
# =============================================================================


def detect_middle_man(
    treelint_class_output: dict,
    delegation_threshold: float = DEFAULT_DELEGATION_THRESHOLD,
    min_methods: int = DEFAULT_MIN_METHODS,
    max_body_size: int = DEFAULT_DELEGATION_BODY_SIZE,
) -> list[dict]:
    """
    Detect middle man classes from Treelint class output.

    A class is flagged as a middle man when:
    - total_methods >= min_methods (default: 3)
    - delegation_ratio > delegation_threshold (default: 0.80)

    Args:
        treelint_class_output: Treelint JSON output with class and method data.
            Expected structure:
            {
                "results": [
                    {
                        "name": "ClassName",
                        "type": "class",
                        "file": "path/to/file.py",
                        "lines": {"start": 10, "end": 50},
                        "members": {
                            "methods": [
                                {
                                    "name": "method_name",
                                    "lines": {"start": 12, "end": 13}
                                },
                                ...
                            ]
                        }
                    }
                ]
            }
        delegation_threshold: Ratio above which a class is flagged (default: 0.80).
        min_methods: Minimum number of methods required for flagging (default: 3).
        max_body_size: Maximum body size for delegation classification (default: 2).

    Returns:
        List of MiddleManFinding dicts for violating classes.
    """
    findings = []

    results = treelint_class_output.get("results", [])
    for class_result in results:
        # Get class info
        class_name = class_result.get("name", "Unknown")
        file_path = class_result.get("file", "")
        lines = class_result.get("lines", {})
        line = lines.get("start", 0) if lines else 0

        # Get methods from members
        members = class_result.get("members", {})
        methods = members.get("methods", [])

        total_methods = len(methods)

        # Skip if below minimum method threshold (BR-003)
        if total_methods < min_methods:
            continue

        # Calculate delegation ratio
        delegating_methods = count_delegation_methods(methods, max_body_size)
        ratio = delegating_methods / total_methods if total_methods > 0 else 0.0

        # Flag if ratio exceeds threshold (BR-002: strict >)
        if ratio > delegation_threshold:
            finding = build_middle_man_finding(
                class_name=class_name,
                file_path=file_path,
                line=line,
                total_methods=total_methods,
                delegating_methods=delegating_methods,
                delegation_ratio=ratio,
            )
            findings.append(finding)

    return findings


# =============================================================================
# Grep Fallback for Unsupported Languages
# =============================================================================


def detect_middle_man_grep(
    code_content: str,
    file_path: str,
    language: str,
    delegation_threshold: float = DEFAULT_DELEGATION_THRESHOLD,
    min_methods: int = DEFAULT_MIN_METHODS,
    max_body_size: int = DEFAULT_DELEGATION_BODY_SIZE,
) -> list[dict]:
    """
    Detect middle man classes using Grep patterns for unsupported languages.

    Args:
        code_content: Source code content to scan.
        file_path: File path for the finding.
        language: Programming language (csharp, java, go).
        delegation_threshold: Ratio above which a class is flagged.
        min_methods: Minimum number of methods required.
        max_body_size: Maximum body lines for delegation method.

    Returns:
        List of MiddleManFinding dicts for violating classes.
    """
    language = language.lower()

    if language not in UNSUPPORTED_LANGUAGES:
        return []

    if language == "csharp":
        return _detect_middle_man_csharp(
            code_content, file_path, delegation_threshold, min_methods, max_body_size
        )
    elif language == "java":
        return _detect_middle_man_java(
            code_content, file_path, delegation_threshold, min_methods, max_body_size
        )
    elif language == "go":
        return _detect_middle_man_go(
            code_content, file_path, delegation_threshold, min_methods, max_body_size
        )

    return []


def _scan_brace_delimited_classes(
    lines: list[str],
    class_pattern: re.Pattern,
    method_classifier: callable,
    file_path: str,
    delegation_threshold: float,
    min_methods: int,
    max_body_size: int,
) -> list[dict]:
    """
    Scan brace-delimited source for classes and evaluate middle man pattern.

    Shared scanner for C# and Java: finds classes via class_pattern, tracks brace
    nesting to determine class scope, and delegates method classification to the
    provided method_classifier callback.

    Args:
        lines: Source lines.
        class_pattern: Compiled regex to match class declarations (group 1 = name).
        method_classifier: Callable(current_line, line_index, all_lines) -> Optional[dict].
            Returns {"body_size": N} if the line declares a method, or None otherwise.
        file_path: File path for findings.
        delegation_threshold: Middle man threshold.
        min_methods: Minimum method count.
        max_body_size: Max body size for delegation classification.

    Returns:
        List of MiddleManFinding dicts.
    """
    findings = []
    i = 0
    while i < len(lines):
        class_match = class_pattern.search(lines[i])
        if class_match:
            class_name = class_match.group(1)
            class_start_line = i + 1

            methods, j = _extract_class_methods(lines, i, method_classifier)

            finding = _evaluate_and_build_finding(
                methods, class_name, file_path, class_start_line,
                delegation_threshold, min_methods, max_body_size,
            )
            if finding:
                findings.append(finding)

            i = j

        i += 1

    return findings


def _extract_class_methods(
    lines: list[str],
    class_start: int,
    method_classifier: callable,
) -> tuple[list[dict], int]:
    """
    Scan a brace-delimited class body and classify its methods.

    Args:
        lines: All source lines.
        class_start: Line index where the class declaration begins.
        method_classifier: Callable(current_line, line_index, all_lines) -> Optional[dict].

    Returns:
        Tuple of (methods list, end line index).
    """
    brace_count = 0
    class_started = False
    methods = []
    j = class_start

    while j < len(lines):
        current_line = lines[j]
        for char in current_line:
            if char == '{':
                brace_count += 1
                class_started = True
            elif char == '}':
                brace_count -= 1

        if class_started and brace_count > 0:
            result = method_classifier(current_line, j, lines)
            if result is not None:
                methods.append(result)

        if class_started and brace_count == 0:
            break
        j += 1

    return methods, j


def _classify_csharp_method(current_line: str, line_index: int, lines: list[str]) -> Optional[dict]:
    """Classify a C# method line by body size. Returns None if not a method."""
    _method_pat = re.compile(
        r'(?:public|private|internal|protected)\s+(?:static\s+)?(?:async\s+)?(?:\w+(?:<[^>]+>)?)\s+(\w+)\s*\([^)]*\)'
    )
    if not _method_pat.search(current_line):
        return None
    if re.search(r'=>\s*[^;]+;', current_line):
        return {"body_size": 1}
    if re.search(r'\{\s*(?:return\s+)?[^;]+;\s*\}', current_line):
        return {"body_size": 1}
    return {"body_size": _count_method_body_lines(lines, line_index)}


def _detect_middle_man_csharp(
    code_content: str,
    file_path: str,
    delegation_threshold: float,
    min_methods: int,
    max_body_size: int,
) -> list[dict]:
    """Detect middle man classes in C# code."""
    lines = code_content.split('\n')
    class_pattern = re.compile(r'(?:public|private|internal|protected)?\s*(?:static\s+)?class\s+(\w+)')
    return _scan_brace_delimited_classes(
        lines, class_pattern, _classify_csharp_method,
        file_path, delegation_threshold, min_methods, max_body_size,
    )


def _evaluate_and_build_finding(
    methods: list[dict],
    class_name: str,
    file_path: str,
    line: int,
    delegation_threshold: float,
    min_methods: int,
    max_body_size: int,
) -> Optional[dict]:
    """
    Evaluate a class's methods for middle man pattern and build finding if violated.

    Returns a MiddleManFinding dict if the class exceeds the delegation threshold,
    or None if the class is not a middle man.
    """
    total_methods = len(methods)
    if total_methods < min_methods:
        return None

    delegating = sum(1 for m in methods if m["body_size"] <= max_body_size)
    ratio = delegating / total_methods

    if ratio > delegation_threshold:
        return build_middle_man_finding(
            class_name=class_name,
            file_path=file_path,
            line=line,
            total_methods=total_methods,
            delegating_methods=delegating,
            delegation_ratio=ratio,
        )
    return None


def _count_method_body_lines(lines: list[str], method_start: int) -> int:
    """Count body lines of a brace-delimited method (C#, Java, Go)."""
    brace_count = 0
    started = False
    body_lines = 0

    for i in range(method_start, len(lines)):
        line = lines[i]
        for char in line:
            if char == '{':
                brace_count += 1
                started = True
            elif char == '}':
                brace_count -= 1

        if started and brace_count > 0:
            body_lines += 1
        elif started and brace_count == 0:
            break

    return body_lines


def _classify_java_method(current_line: str, line_index: int, lines: list[str]) -> Optional[dict]:
    """Classify a Java method line by body size. Returns None if not a method."""
    _method_pat = re.compile(
        r'(?:public|private|protected)\s+(?:static\s+)?(?:final\s+)?(?:\w+(?:<[^>]+>)?)\s+(\w+)\s*\([^)]*\)'
    )
    if not _method_pat.search(current_line):
        return None
    if re.search(r'\{[^{}]*\}', current_line):
        return {"body_size": 1}
    return {"body_size": _count_method_body_lines(lines, line_index)}


def _detect_middle_man_java(
    code_content: str,
    file_path: str,
    delegation_threshold: float,
    min_methods: int,
    max_body_size: int,
) -> list[dict]:
    """Detect middle man classes in Java code."""
    lines = code_content.split('\n')
    class_pattern = re.compile(r'(?:public|private|protected)?\s*(?:static\s+)?(?:final\s+)?class\s+(\w+)')
    return _scan_brace_delimited_classes(
        lines, class_pattern, _classify_java_method,
        file_path, delegation_threshold, min_methods, max_body_size,
    )


def _detect_middle_man_go(
    code_content: str,
    file_path: str,
    delegation_threshold: float,
    min_methods: int,
    max_body_size: int,
) -> list[dict]:
    """Detect middle man structs in Go code (receiver methods)."""
    findings = []
    lines = code_content.split('\n')

    # Find struct definitions and their receiver methods
    struct_pattern = re.compile(r'type\s+(\w+)\s+struct')
    receiver_pattern = re.compile(r'func\s+\(\s*\w+\s+\*?(\w+)\s*\)\s+(\w+)')

    # First pass: find all structs
    structs = {}
    for i, line in enumerate(lines):
        struct_match = struct_pattern.search(line)
        if struct_match:
            struct_name = struct_match.group(1)
            structs[struct_name] = {"line": i + 1, "methods": []}

    # Second pass: find receiver methods and associate with structs
    for i, line in enumerate(lines):
        receiver_match = receiver_pattern.search(line)
        if receiver_match:
            struct_name = receiver_match.group(1)
            if struct_name in structs:
                # Count body lines for this method
                body_lines = _count_method_body_lines(lines, i)
                structs[struct_name]["methods"].append({"body_size": body_lines})

    # Analyze each struct
    for struct_name, data in structs.items():
        finding = _evaluate_and_build_finding(
            data["methods"], struct_name, file_path, data["line"],
            delegation_threshold, min_methods, max_body_size,
        )
        if finding:
            findings.append(finding)

    return findings


def should_use_grep_fallback(language: str, treelint_exit_code: int) -> bool:
    """
    Determine if Grep fallback should be used based on language and Treelint exit code.

    Returns True if:
    - Language is not supported by Treelint (C#, Java, Go)
    - OR Treelint exit code is 127 (binary not found) or 126 (permission denied)

    Returns False if:
    - Language is supported by Treelint AND Treelint exit code is 0
    """
    language = language.lower()

    # Check unsupported languages
    if language in UNSUPPORTED_LANGUAGES:
        return True

    # Check Treelint exit codes indicating unavailability
    if treelint_exit_code in (126, 127):
        return True

    return False


# =============================================================================
# Finding Builder
# =============================================================================


def build_middle_man_finding(
    class_name: str,
    file_path: str,
    line: int,
    total_methods: int,
    delegating_methods: int,
    delegation_ratio: float,
) -> dict:
    """
    Build a MiddleManFinding dict with all required fields.

    Required fields (AC#5):
    - smell_type: "middle_man" (fixed)
    - severity: "MEDIUM" (fixed)
    - class_name: Name of the class
    - file: Relative file path
    - line: Line number of class definition
    - total_methods: Total method count in class
    - delegating_methods: Count of delegation methods
    - delegation_ratio: Ratio as float (0.0-1.0)
    - evidence: Human-readable description
    - remediation: Suggested fix

    Returns:
        MiddleManFinding dict.
    """
    return {
        "smell_type": "middle_man",
        "severity": "MEDIUM",
        "class_name": class_name,
        "file": file_path,
        "line": line,
        "total_methods": total_methods,
        "delegating_methods": delegating_methods,
        "delegation_ratio": delegation_ratio,
        "evidence": (
            f"Class '{class_name}' has {delegating_methods}/{total_methods} methods "
            f"({delegation_ratio:.1%}) that delegate to another class. "
            f"This indicates the class may be a middle man adding no value."
        ),
        "remediation": (
            f"Consider removing '{class_name}' and having clients call the delegated "
            f"class directly. Review if the class provides any additional value "
            f"beyond simple delegation."
        ),
    }
