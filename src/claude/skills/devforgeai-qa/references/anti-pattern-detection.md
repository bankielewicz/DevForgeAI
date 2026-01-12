# Anti-Pattern Detection Reference

## Overview

This guide provides detection algorithms and techniques for identifying anti-patterns that lead to technical debt.

## Detection Algorithms

### Static Code Analysis

**Grep-based pattern matching:**
```python
def detect_sql_injection(source_path):
    # Pattern: String concatenation in SQL queries
    patterns = [
        r'ExecuteRawSql\(.*\+',
        r'string\.Format.*SELECT',
        r'f"SELECT.*\{',
        r'`SELECT.*\$\{'
    ]

    violations = []
    for pattern in patterns:
        matches = grep(pattern, source_path)
        for match in matches:
            violations.append({
                "severity": "CRITICAL",
                "file": match.file,
                "line": match.line,
                "pattern": pattern,
                "fix": "Use parameterized queries"
            })

    return violations
```

### Complexity Analysis

**Calculate cyclomatic complexity:**
```python
def calculate_complexity(method_ast):
    """
    Complexity = 1 + number of decision points
    Decision points: if, while, for, case, catch, &&, ||, ?:
    """
    complexity = 1

    for node in ast.walk(method_ast):
        if isinstance(node, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
            complexity += 1
        elif isinstance(node, ast.BoolOp):  # and, or
            complexity += len(node.values) - 1

    return complexity
```

### Dependency Graph Analysis

**Detect circular dependencies:**
```python
def detect_circular_dependencies(project_path):
    # Build dependency graph
    graph = {}
    for file in find_source_files(project_path):
        imports = extract_imports(file)
        graph[file] = imports

    # Find cycles using DFS
    visited = set()
    stack = set()
    cycles = []

    def dfs(node, path):
        if node in stack:
            # Cycle detected
            cycle_start = path.index(node)
            cycles.append(path[cycle_start:])
            return

        if node in visited:
            return

        visited.add(node)
        stack.add(node)

        for dependency in graph.get(node, []):
            dfs(dependency, path + [node])

        stack.remove(node)

    for file in graph:
        dfs(file, [])

    return cycles
```

## Anti-Pattern Categories

### Category 1: Library Substitution (CRITICAL)

**Detection:**
```python
def detect_library_substitution(tech_stack_md, source_path):
    # Load locked technologies
    locked_tech = parse_tech_stack(tech_stack_md)

    violations = []

    # Check ORM substitution
    if locked_tech["ORM"] == "Dapper":
        ef_usage = grep("using EntityFramework|using Microsoft.EntityFrameworkCore", source_path)
        if ef_usage:
            violations.append({
                "severity": "CRITICAL",
                "category": "Library Substitution",
                "locked_tech": "Dapper",
                "actual_tech": "Entity Framework",
                "files": ef_usage.files
            })

    # Check state management (React)
    if locked_tech.get("StateManagement") == "Zustand":
        redux_usage = grep("from '@reduxjs/toolkit'|import.*redux", source_path)
        if redux_usage:
            violations.append({
                "severity": "CRITICAL",
                "category": "Library Substitution",
                "locked_tech": "Zustand",
                "actual_tech": "Redux"
            })

    return violations
```

### Category 2: Structure Violations (HIGH)

**Detection:**
```python
def detect_structure_violations(source_tree_md, files):
    rules = parse_source_tree_rules(source_tree_md)
    violations = []

    for file in files:
        # Determine expected location based on file type
        expected_location = get_expected_location(file, rules)

        if file.path != expected_location:
            violations.append({
                "severity": "HIGH",
                "category": "Structure Violation",
                "file": file.path,
                "expected": expected_location,
                "rule": rules.get_rule_for_file(file)
            })

    return violations
```

### Category 3: Cross-Layer Dependencies (CRITICAL)

**Detection:**
```python
def detect_layer_violations(architecture_constraints_md, source_path):
    # Load layer dependency matrix
    matrix = parse_layer_matrix(architecture_constraints_md)
    # Example: Domain can only reference Domain

    violations = []

    # Check Domain layer purity
    domain_files = glob("src/Domain/**/*.cs")
    for file in domain_files:
        imports = extract_imports(file)

        for imp in imports:
            if "Infrastructure" in imp or "Application" in imp:
                violations.append({
                    "severity": "CRITICAL",
                    "category": "Cross-Layer Dependency",
                    "file": file,
                    "violation": imp,
                    "rule": "Domain must not reference Application/Infrastructure"
                })

    return violations
```

### Category 4: Security Anti-Patterns (CRITICAL)

**SQL Injection Detection:**
```python
patterns = {
    "sql_injection": [
        r'ExecuteRawSql\(.*\+',
        r'string\.Format.*SELECT',
        r'f"SELECT.*\{',
        r'\$"SELECT.*\{',
        r'`SELECT.*\$\{'
    ],
    "xss": [
        r'innerHTML\s*=',
        r'dangerouslySetInnerHTML',
        r'document\.write\('
    ],
    "hardcoded_secrets": [
        r'password\s*=\s*["\'][^"\']{8,}["\']',
        r'api_?key\s*=\s*["\'][^"\']+["\']',
        r'connectionstring\s*=\s*["\'].*password='
    ]
}
```

### Category 5: Code Smells (MEDIUM/LOW)

**God Object Detection:**
```python
def detect_god_objects(source_path):
    violations = []

    for file in find_source_files(source_path):
        lines = count_lines(file)
        methods = count_methods(file)
        responsibilities = estimate_responsibilities(file)

        if lines > 500 or methods > 20 or responsibilities > 5:
            violations.append({
                "severity": "MEDIUM",
                "category": "God Object",
                "file": file,
                "lines": lines,
                "methods": methods,
                "responsibilities": responsibilities,
                "fix": "Split into smaller, focused classes"
            })

    return violations
```

**Magic Number Detection:**
```python
def detect_magic_numbers(source_path):
    # Pattern: Numeric literals (not in const/enum declarations)
    pattern = r'(?<!const\s)(?<!enum\s)\b\d{3,}\b'

    violations = []
    matches = grep(pattern, source_path)

    for match in matches:
        # Filter out acceptable cases
        if is_in_const_declaration(match) or is_in_test(match.file):
            continue

        violations.append({
            "severity": "LOW",
            "category": "Magic Number",
            "file": match.file,
            "line": match.line,
            "number": match.text,
            "fix": "Extract to named constant"
        })

    return violations
```

## Severity Assessment

### Severity Levels

| Level | Description | Examples | Action |
|-------|-------------|----------|--------|
| CRITICAL | Security/Architecture violations | SQL injection, layer violations | Block immediately |
| HIGH | Spec/Design violations | API mismatch, structure violations | Block release |
| MEDIUM | Maintainability issues | High complexity, code smells | Address soon |
| LOW | Code quality | Documentation, formatting | Technical debt |

### Severity Decision Tree

```python
def assess_severity(violation):
    # Security issues are always CRITICAL
    if violation.category in ["SQL Injection", "XSS", "Hardcoded Secret"]:
        return "CRITICAL"

    # Architecture violations are CRITICAL
    if violation.category == "Cross-Layer Dependency":
        return "CRITICAL"

    # Library substitution is CRITICAL
    if violation.category == "Library Substitution":
        return "CRITICAL"

    # Structure violations are HIGH
    if violation.category == "Structure Violation":
        return "HIGH"

    # Complexity/maintainability is MEDIUM
    if violation.category in ["High Complexity", "God Object", "Long Method"]:
        return "MEDIUM"

    # Code quality is LOW
    return "LOW"
```

## False Positive Handling

### Context-Aware Assessment

```python
def reduce_false_positives(violations, context):
    filtered = []

    for violation in violations:
        # Check if violation is in test code
        if is_test_file(violation.file):
            # Lower severity for test code
            if violation.severity == "MEDIUM":
                violation.severity = "LOW"

        # Check if pattern is in legacy code
        if is_legacy_code(violation.file, context):
            # Document as accepted technical debt
            violation.note = "Legacy code - accepted technical debt"

        # Check if pattern has documented exception
        if has_documented_exception(violation, context):
            continue  # Skip this violation

        filtered.append(violation)

    return filtered
```

### When to Use AskUserQuestion

```python
def handle_ambiguous_violation(violation):
    # Pattern: Method complexity slightly over threshold
    if violation.category == "High Complexity" and violation.complexity <= 12:
        # Ask user if this is acceptable
        return ask_user_question(
            "Method has complexity 12 (threshold 10) but is well-tested. Accept?",
            options=["Yes, accept", "No, refactor required"]
        )

    # Pattern: Large method with good reason
    if violation.category == "Long Method" and violation.is_cohesive:
        return ask_user_question(
            "Method is 150 lines but cohesive (single responsibility). Accept?",
            options=["Yes, acceptable", "No, extract methods"]
        )
```

## Integration with Context Files

### Load and Enforce Context

```python
def validate_against_context(source_path):
    # Load all context files
    tech_stack = read("devforgeai/specs/context/tech-stack.md")
    source_tree = read("devforgeai/specs/context/source-tree.md")
    dependencies = read("devforgeai/specs/context/dependencies.md")
    coding_standards = read("devforgeai/specs/context/coding-standards.md")
    architecture = read("devforgeai/specs/context/architecture-constraints.md")
    anti_patterns = read("devforgeai/specs/context/anti-patterns.md")

    violations = []

    # Detect violations for each category
    violations.extend(detect_library_substitution(tech_stack, source_path))
    violations.extend(detect_structure_violations(source_tree, source_path))
    violations.extend(detect_layer_violations(architecture, source_path))
    violations.extend(detect_coding_standard_violations(coding_standards, source_path))
    violations.extend(detect_anti_patterns(anti_patterns, source_path))

    return violations
```

## Quick Reference

### Detection Commands

```bash
# SQL Injection
grep -r "ExecuteRawSql(.*+" --include="*.cs"

# Hardcoded Secrets
grep -ri "password\s*=\s*[\"']" src/

# Cross-layer violations
grep -r "using.*Infrastructure" src/Domain/

# Magic numbers
grep -rE "\s\d{3,}\s" src/ --exclude-dir=tests

# God objects
find src/ -name "*.cs" -exec wc -l {} \; | awk '$1 > 500'
```

### Common Patterns

| Anti-Pattern | Grep Pattern | Severity |
|--------------|--------------|----------|
| SQL Injection | `string.Format.*SELECT` | CRITICAL |
| Hardcoded Secret | `password\s*=\s*"[^"]+"` | CRITICAL |
| Layer Violation | `using.*Infrastructure` in Domain | CRITICAL |
| Magic Number | `\b\d{3,}\b` (not in const) | LOW |
| Long Method | Methods > 100 lines | MEDIUM |
| High Coupling | > 10 dependencies | MEDIUM |

This reference should be loaded when performing comprehensive anti-pattern detection during deep QA validation.
