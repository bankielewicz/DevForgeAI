# Two-Stage Filter Patterns for Data Class Detection

**Pattern ID:** PE-060
**Version:** 1.0
**Purpose:** Reduce false positive rate from 40-60% to <15% for data class smell detection.

---

## Stage 1: High-Recall Candidate Detection

Stage 1 identifies all classes matching structural thresholds, prioritizing recall over precision. It casts a wide net, accepting some false positives that Stage 2 will filter.

**Threshold Logic:**
- `method_count < 3 AND property_count > 2`
- Methods excluded from count: `__init__`, `__str__`, `__repr__`, `__eq__`, `__hash__` (Python dunder methods)
- Properties include: instance variables, class fields, annotated attributes

**Treelint Query:**
```bash
treelint search --type class --format json
```

**JSON Output Parsing:**
- Parse `members.methods` array to count behavioral methods
- Parse `members.properties` array to count data fields
- Apply threshold to determine Stage 1 candidates

**Stage 1 Output:** List of candidate classes with file, line, class_name, method_count, property_count.

---

## Stage 2: High-Precision LLM Assessment

Stage 2 reads the class body source code and determines whether each candidate is a true data class or a valid pattern that should be suppressed.

**LLM Prompt Template** (applied to each Stage 1 candidate):

```
Assess the following class body for data class smell detection.

Class: {class_name}
File: {file_path}
Line: {line_number}
Method count: {method_count}
Property count: {property_count}

Class source code:
{class_body}

Determine:
1. Does this class contain meaningful behavior beyond getters/setters?
2. Is this an intentional data-holding pattern (@dataclass, DTO with validation, record)?
3. Should this be REPORTED as a data class smell or SUPPRESSED as a valid pattern?

Return a confidence score (0.0-1.0) where:
- >= 0.7 means REPORT as data class smell
- < 0.7 means SUPPRESS as valid pattern
```

**Decision Logic:**
- confidence >= 0.7: REPORT the finding as a data class code smell
- confidence < 0.7: SUPPRESS the finding as a valid pattern

---

## DataClassFinding Output Schema

Each confirmed data class produces a finding with the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `smell_type` | String | Fixed value: "data_class" |
| `severity` | Enum | Fixed value: "MEDIUM" |
| `class_name` | String | Name of the detected class |
| `file` | String | Relative file path |
| `line` | Int | Line number of class definition |
| `method_count` | Int | Number of behavioral methods (excluding dunder) |
| `property_count` | Int | Number of properties/fields |
| `confidence` | Float | Stage 2 confidence score (range 0.0-1.0) |
| `evidence` | String | Human-readable detection explanation |
| `remediation` | String | Suggested fix action |

---

## False Positive Suppression Patterns

The following patterns are recognized as valid and receive confidence < 0.7 during Stage 2 assessment:

### Pattern 1: Python @dataclass Decorator

The @dataclass decorator is a valid Python pattern that explicitly declares a class as an intentional data container with auto-generated methods. Because the developer has made a conscious choice, these should be suppressed.

**Detection:** Look for `@dataclass` decorator above class definition.
**Action:** Suppress with confidence 0.3-0.5 (valid intentional pattern).

### Pattern 2: TypeScript Interface Exclusion

A TypeScript interface is structural by design -- it has no runtime representation and is not a class. Interfaces should be excluded entirely from data class detection.

**Detection:** Look for `interface` keyword instead of `class`.
**Action:** Exclude from Stage 1 entirely (interfaces are not classes).

### Pattern 3: DTO with Validation Logic

A DTO with validation methods (validate, check, assert, verify) demonstrates meaningful behavior beyond simple data holding. These are not pure data classes.

**Detection:** Look for validation methods in class body.
**Action:** Suppress with confidence 0.2-0.4 (DTO with validation is a valid pattern).

### Pattern 4: Record Types

Language-level record types (Python NamedTuple, C# record, Java record) are intentional value objects and should not be flagged.

**Detection:** Look for record keyword or NamedTuple base class.
**Action:** Suppress with confidence 0.2-0.4.

---

## Confidence Scoring Guidelines

| Scenario | Expected Confidence | Decision |
|----------|-------------------|----------|
| Class with 0 methods, 5+ properties, no decorator | 0.85-0.95 | REPORT |
| Class with only getters/setters | 0.75-0.85 | REPORT |
| @dataclass decorated class | 0.3-0.5 | SUPPRESS |
| TypeScript interface | N/A (excluded) | EXCLUDE |
| DTO with validation methods | 0.2-0.4 | SUPPRESS |
| Record/NamedTuple | 0.2-0.4 | SUPPRESS |
| Borderline (2 methods, 4 properties) | 0.5-0.7 | LLM decides |

---

## Commented-Out Code Detection

**Pattern ID:** PE-060-COC
**Version:** 1.0
**Purpose:** Detect commented-out code blocks that should be deleted rather than commented. Version control (git) should be used instead of commenting out code.

### Stage 1: Python Commented-Out Code Patterns

High-recall Grep patterns that identify potential commented-out Python code. These patterns match lines that start with `#` followed by Python language keywords.

**Python Stage 1 Grep Pattern:**
```
^\s*#\s*(def |class |import |from |return |if |for |while |try:|except)
```

**Matched Cases:**
- `# def old_function():` - Commented function definition
- `# class OldClass:` - Commented class definition
- `# import os` - Commented import statement
- `# from module import something` - Commented from-import
- `# return value` - Commented return statement
- `# if condition:` - Commented if statement
- `# for item in items:` - Commented for loop
- `# while True:` - Commented while loop
- `# try:` - Commented try block
- `# except Exception:` - Commented except clause
- `    # def nested():` - Indented commented function

**False Positive Exclusions (NOT matched by this pattern):**
- `# This is a regular comment` - Prose comments
- `# TODO: fix this` - TODO comments
- `# FIXME: handle edge case` - FIXME comments
- `# Author: John Doe` - Attribution comments
- `#!/usr/bin/env python` - Shebang line (starts at column 0 with `!`)
- `code = "value"  # inline comment` - Inline comments after code

### Stage 1: TypeScript/JavaScript Commented-Out Code Patterns

High-recall Grep patterns for TS/JS commented-out code using `//` single-line comments.

**TypeScript/JavaScript Stage 1 Grep Pattern:**
```
^\s*//\s*(function |class |import |export |return |const |let |var |if |for )
```

**Matched Cases:**
- `// function oldFunc()` - Commented function declaration
- `// class OldComponent` - Commented class declaration
- `// import { something }` - Commented import
- `// export const value` - Commented export
- `// return result` - Commented return
- `// const oldValue` - Commented const declaration
- `// let counter` - Commented let declaration
- `// var legacy` - Commented var declaration
- `// if (condition)` - Commented if statement
- `// for (let i = 0` - Commented for loop
- `  // function nested()` - Indented commented function

**False Positive Exclusions (NOT matched by this pattern):**
- `// This is a comment` - Prose comments
- `// TODO: refactor` - TODO comments
- `// eslint-disable-next-line` - ESLint directives
- `// @ts-ignore` - TypeScript directives
- `/// <reference path="..." />` - Triple-slash directives
- `// https://example.com` - URL in comment

### Stage 1: Multiline Block Comment Patterns

For TypeScript/JavaScript `/* ... */` block comments containing code.

**Multiline Block Comment Grep Pattern:**
```
/\*[\s\S]*?(function|class|import|return)[\s\S]*?\*/
```

**Note:** Requires `multiline=true` flag for Grep tool.

**Matched Cases:**
- `/* function oldHandler() { ... } */` - Commented function block
- `/* class OldClass { ... } */` - Commented class block
- `/* import { x } from 'y'; */` - Commented import in block
- Multi-line blocks containing code keywords

**False Positive Exclusions:**
- `/* This is documentation */` - Pure documentation blocks (no code keywords)
- `/** JSDoc comment */` - JSDoc comments (handled by suppression rules)

---

### Stage 2: LLM Classification with Chain-of-Thought

Stage 2 reads ±5 lines of surrounding context and classifies candidates as 'code', 'documentation', or 'todo'.

**Confidence Threshold:** 0.7
- confidence >= 0.7: REPORT the finding
- confidence < 0.7: SUPPRESS the finding

**Context Lines:** 5 (read 5 lines before and 5 lines after the candidate)

**Classifications:**
- `code`: Actual commented-out code that should be deleted (confidence 0.7-1.0 = REPORT)
- `documentation`: Code example in docstring/JSDoc, not actual dead code (confidence < 0.7 = SUPPRESS)
- `todo`: Intentional TODO with code sketch, not actionable dead code (confidence varies)

**Stage 2 LLM Prompt Template:**

```
<thinking>
Analyze the following commented line and its surrounding context to determine if this is actual commented-out code or a documentation example.

Candidate line: {candidate_line}
File: {file_path}
Line number: {line_number}

Surrounding context (±5 lines):
{context_before}
>>> {candidate_line}
{context_after}

Consider:
1. Is this line inside a docstring (""" or ''') or JSDoc (/** ... */)?
2. Does the context suggest this is a code example showing usage?
3. Is this part of a TODO/FIXME with a code sketch?
4. Is this actual production code that was commented out?

Based on my analysis of the context, I will classify this commented line as...
</thinking>

Classification: {code|documentation|todo}
Confidence: {0.0-1.0}
Reasoning: {brief explanation}
```

---

### Documentation Example Suppression Rules

JSDoc and docstring code examples should NOT be reported as commented-out code.

**JSDoc Suppression (TypeScript/JavaScript):**
- If the candidate line is within a `/** ... */` block, classify as 'documentation'
- If surrounding context contains `@example`, `@param`, `@returns`, classify as 'documentation'
- Confidence for JSDoc examples: 0.2-0.4 (SUPPRESS)

**Docstring Suppression (Python):**
- If the candidate line follows a `"""` or `'''` and is before the closing quotes, classify as 'documentation'
- If surrounding context contains `Args:`, `Returns:`, `Example:`, classify as 'documentation'
- Confidence for docstring examples: 0.2-0.4 (SUPPRESS)

**Suppression Decision:**
- JSDoc or docstring context detected: confidence < 0.7 → SUPPRESS finding
- No documentation context: proceed with normal confidence scoring → may REPORT

---

### CommentedOutCodeFinding Output Schema

Each confirmed commented-out code finding produces a JSON object with the following 10 fields:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `smell_type` | String | Required, fixed: "commented_out_code" | Smell type identifier |
| `severity` | String | Required, fixed: "LOW" | Severity level (LOW because clutter, not security) |
| `file` | String | Required, relative path | File path where commented code found |
| `line_start` | Int | Required, positive | First line of commented block |
| `line_end` | Int | Required, >= line_start | Last line of commented block |
| `excerpt` | String | Required, max 200 chars | Truncated preview of commented code |
| `confidence` | Float | Required, range 0.0-1.0 | Stage 2 LLM confidence score |
| `classification` | Enum | Required: 'code'\|'documentation'\|'todo' | Stage 2 classification result |
| `evidence` | String | Required | Human-readable explanation of detection |
| `remediation` | String | Required | Suggested fix: delete commented code, use git history |

**Example Output:**
```json
{
  "smell_type": "commented_out_code",
  "severity": "LOW",
  "file": "src/services/auth_service.py",
  "line_start": 45,
  "line_end": 52,
  "excerpt": "# def old_authenticate(user, pwd):\n#     if user == 'admin':\n#         return True...",
  "confidence": 0.92,
  "classification": "code",
  "evidence": "8-line commented function definition detected. Code keywords: def, if, return. Not in docstring context.",
  "remediation": "Delete this commented-out code block. Use git history (git log -p) to retrieve if needed later."
}
```

---

### Confidence Scoring Guidelines for Commented-Out Code

| Scenario | Expected Confidence | Decision |
|----------|-------------------|----------|
| Multi-line commented function/class | 0.85-0.95 | REPORT |
| Single commented import/return line | 0.60-0.75 | BORDERLINE |
| Code example in JSDoc `@example` block | 0.2-0.4 | SUPPRESS |
| Code example in Python docstring | 0.2-0.4 | SUPPRESS |
| TODO comment with code sketch | 0.4-0.6 | SUPPRESS |
| Commented-out test case | 0.75-0.85 | REPORT |
| `// eslint-disable` or `# type: ignore` | 0.1-0.2 | SUPPRESS |

---

## References

- PE-060: Two-Stage Filtering pattern specification
- PE-059: Confidence Scoring pattern specification
- PE-005: Chain-of-Thought pattern specification
- ADR-013: Treelint Integration for AST-Aware Code Search
- EPIC-064: AI-Generated Code Smell Detection Gap Closure
- STORY-399: Add Data Class Detection to Anti-Pattern Scanner
- STORY-401: Add Commented-Out Code Detection to Anti-Pattern Scanner
