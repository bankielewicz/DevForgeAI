# Code Smell Detection Catalog

**Version**: 1.0
**Last Updated**: 2026-02-16
**Status**: Reference documentation for anti-pattern-scanner Phase 5

## God Object

Definition: A class that has accumulated too many responsibilities, violating the Single Responsibility Principle. It knows too much or does too much.

Threshold: >20 methods OR >300 lines

Severity: CRITICAL

Detection Method: Treelint

Two-Stage: No — deterministic metric-based detection requires no LLM assessment.

JSON Output Schema:
```json
{
  "smell_type": "god_object",
  "severity": "CRITICAL",
  "class_name": "OrderManager",
  "file": "src/services/order_manager.py",
  "line": 15,
  "method_count": 25,
  "line_count": 450,
  "evidence": "Class has 25 methods and 450 lines, exceeding thresholds of 20 methods / 300 lines",
  "remediation": "Extract cohesive method groups into separate classes using Extract Class refactoring"
}
```

Test Scenarios:

1. Class with 25 methods and 150 lines should be flagged (method threshold exceeded)
2. Class with 10 methods and 400 lines should be flagged (line threshold exceeded)
3. Class with 5 methods and 50 lines should NOT be flagged (both below threshold)
4. Interface with 30 method signatures should NOT be flagged (interface, not class)

False Positive Patterns:
- Test fixture classes that legitimately have many test methods
- Generated code (ORM models, protocol buffers)
- Facade classes that intentionally aggregate APIs

Fowler Reference: "Large Class" smell — Fowler recommends Extract Class and Extract Subclass refactorings.

---

## Long Method

Definition: A method or function that has grown too long, making it difficult to understand, test, and maintain.

Threshold: >50 lines

Severity: MEDIUM

Detection Method: Treelint

Two-Stage: No — line count is deterministic.

JSON Output Schema:
```json
{
  "smell_type": "long_method",
  "severity": "MEDIUM",
  "function_name": "process_order",
  "file": "src/services/order_service.py",
  "line": 42,
  "line_count": 85,
  "evidence": "Function has 85 lines, exceeding threshold of 50 lines",
  "remediation": "Extract logical blocks into smaller helper methods using Extract Method refactoring"
}
```

Test Scenarios:

1. Function with 85 lines should be flagged
2. Function with 50 lines should NOT be flagged (at threshold, not over)
3. Function with 10 lines should NOT be flagged
4. Class __init__ with 60 lines of assignments should be flagged

False Positive Patterns:
- Switch/match statements with many cases that are inherently verbose
- Data initialization methods with many field assignments
- Generated code (serializers, parsers)

Fowler Reference: "Long Method" smell — refactoring.guru/smells/long-method

---

## Magic Number

Definition: A hardcoded numeric literal used in code without explanation, making the code harder to understand and maintain.

Threshold: Hardcoded numeric literals (excluding 0, 1, -1, common HTTP status codes)

Severity: MEDIUM

Detection Method: Grep

Two-Stage: No — pattern matching is sufficient.

JSON Output Schema:
```json
{
  "smell_type": "magic_number",
  "severity": "MEDIUM",
  "file": "src/billing/calculator.py",
  "line": 23,
  "value": "0.0825",
  "evidence": "Hardcoded numeric literal 0.0825 without named constant",
  "remediation": "Extract to named constant: TAX_RATE = 0.0825"
}
```

Test Scenarios:

1. `if count > 42:` should be flagged (unexplained literal)
2. `TAX_RATE = 0.0825` should NOT be flagged (named constant assignment)
3. `for i in range(0, 10):` — 0 excluded, 10 flagged
4. `return 200` in HTTP handler should NOT be flagged (common HTTP status)

False Positive Patterns:
- Named constant assignments (LEFT side of `=`)
- Common values: 0, 1, -1, 2 (loop increments)
- HTTP status codes: 200, 201, 204, 301, 400, 401, 403, 404, 500
- Array/string index 0

Fowler Reference: "Magic Number" — refactoring.guru/refactoring/smells/magic-number

---

## Data Class

Definition: A class that contains only fields/properties with no meaningful behavior — essentially a data container that should either be a plain data structure or have behavior added.

Threshold: <3 methods AND >2 properties

Severity: MEDIUM

Detection Method: Treelint

Two-Stage: Yes — Stage 1 identifies candidates via AST metrics, Stage 2 LLM assesses whether the class legitimately serves as a data transfer object.

JSON Output Schema:
```json
{
  "smell_type": "data_class",
  "severity": "MEDIUM",
  "class_name": "UserDTO",
  "file": "src/models/user.py",
  "line": 10,
  "method_count": 1,
  "property_count": 8,
  "confidence": 0.85,
  "evidence": "Class has 1 method and 8 properties; likely a data-only container",
  "remediation": "Consider adding behavior methods or converting to dataclass/record type"
}
```

Test Scenarios:

1. Class with 0 methods and 5 properties should be flagged
2. Class with 2 methods and 4 properties should be flagged (<3 methods, >2 properties)
3. Class with 5 methods and 10 properties should NOT be flagged (>=3 methods)
4. Dataclass/record decorator should reduce confidence (intentional DTO)

False Positive Patterns:
- Classes decorated with `@dataclass`, `@attrs`, or TypeScript `interface` types
- ORM model classes that intentionally map to database tables
- DTO/VO classes explicitly named as such (UserDTO, OrderVO)

Fowler Reference: "Data Class" smell — Fowler recommends Move Method to push behavior into the class.

---

## Long Parameter List

Definition: A function or method that accepts too many parameters, making it hard to call correctly and understand.

Threshold: >4 parameters (excluding self/cls and variadic *args/**kwargs)

Severity: MEDIUM

Detection Method: Treelint

Two-Stage: No — parameter count is deterministic.

JSON Output Schema:
```json
{
  "smell_type": "long_parameter_list",
  "severity": "MEDIUM",
  "function_name": "create_order",
  "file": "src/services/order_service.py",
  "line": 30,
  "parameter_count": 7,
  "parameters": ["customer_id", "product_id", "quantity", "price", "discount", "shipping", "tax"],
  "evidence": "Function has 7 parameters, exceeding threshold of 4",
  "remediation": "Introduce Parameter Object or use builder pattern to reduce parameter count"
}
```

Test Scenarios:

1. Function with 7 parameters should be flagged
2. Function with 4 parameters should NOT be flagged (at threshold, not over)
3. Python method with `self` + 5 params should be flagged (self excluded, 5 > 4)
4. Function with `*args, **kwargs` should exclude variadic from count

False Positive Patterns:
- Constructor/initializer methods that legitimately set many fields
- Framework callback signatures (Django views, Express middleware)
- Mathematical functions with domain-specific parameter sets

Fowler Reference: "Long Parameter List" — refactoring.guru/refactoring/smells/long-parameter-list

---

## Commented-Out Code

Definition: Code that has been commented out rather than deleted, creating clutter and confusion about what is active.

Threshold: Commented code blocks (lines containing commented-out executable statements)

Severity: LOW

Detection Method: Grep

Two-Stage: Yes — Stage 1 Grep for high-recall pattern matching, Stage 2 LLM classifies as code vs documentation vs TODO.

JSON Output Schema:
```json
{
  "smell_type": "commented_out_code",
  "severity": "LOW",
  "file": "src/services/auth.py",
  "line_start": 45,
  "line_end": 52,
  "excerpt": "# def old_validate(token): ...",
  "confidence": 0.85,
  "classification": "code",
  "evidence": "Block of 8 lines contains commented-out function definition",
  "remediation": "Delete commented code; use git history to recover if needed"
}
```

Test Scenarios:

1. `# def old_function():` should be flagged as commented-out code
2. `# TODO: implement caching` should NOT be flagged (todo comment)
3. `# This function validates tokens` should NOT be flagged (documentation)
4. JSDoc `@example` block should NOT be flagged (documentation suppression)

False Positive Patterns:
- Documentation comments explaining code behavior
- TODO/FIXME comments (separate smell type)
- JSDoc/docstring `@example` blocks showing usage
- License headers and copyright notices

Fowler Reference: Related to "Comments" smell — unnecessary comments often indicate code that should be refactored or removed.

---

## Orphaned Import

Definition: An import statement that brings in a symbol never referenced elsewhere in the file, adding unnecessary dependencies.

Threshold: Import with zero usages of imported symbol outside the import line

Severity: LOW

Detection Method: Grep

Two-Stage: No — symbol usage search is deterministic.

JSON Output Schema:
```json
{
  "smell_type": "orphaned_import",
  "severity": "LOW",
  "file": "src/services/user_service.py",
  "line": 3,
  "import_statement": "from utils.crypto import encrypt_password",
  "imported_symbol": "encrypt_password",
  "usage_count": 0,
  "evidence": "Symbol 'encrypt_password' imported but never referenced in file",
  "remediation": "Remove unused import: from utils.crypto import encrypt_password"
}
```

Test Scenarios:

1. `import os` with no `os.` usage should be flagged
2. `from typing import List` used in type annotation should NOT be flagged
3. `import * from module` should be excluded (wildcard import, cannot determine usage)
4. Re-export `export { X } from './y'` should be excluded

False Positive Patterns:
- Wildcard imports (`import *`) — cannot determine individual symbol usage
- Re-export patterns in barrel files
- Side-effect imports (`import './polyfill'`)
- Symbols listed in Python `__all__`

Fowler Reference: Related to "Speculative Generality" — importing what you do not need.

---

## Dead Code

Definition: Code that is unreachable or never executed — functions never called, branches that cannot be entered, or variables never read.

Threshold: Functions/methods with zero callers across the codebase

Severity: LOW

Detection Method: Treelint

Two-Stage: No — call graph analysis is deterministic.

JSON Output Schema:
```json
{
  "smell_type": "dead_code",
  "severity": "LOW",
  "function_name": "legacy_process",
  "file": "src/services/processor.py",
  "line": 120,
  "caller_count": 0,
  "evidence": "Function 'legacy_process' has zero callers in the codebase",
  "remediation": "Remove dead function or verify it is an entry point / public API"
}
```

Test Scenarios:

1. Private function with zero callers should be flagged
2. Public API endpoint handler should NOT be flagged (entry point)
3. Test helper function called only from tests should NOT be flagged
4. Function referenced via string-based dispatch should be excluded (dynamic call)

False Positive Patterns:
- Entry points: main(), API handlers, CLI commands, event handlers
- Framework hooks: `__init__`, `setUp`, `tearDown`, lifecycle methods
- Dynamically invoked code (reflection, string dispatch, decorators)
- Public API methods intended for external consumption

Fowler Reference: "Dead Code" — refactoring.guru/refactoring/smells/dead-code

---

## Placeholder Code

Definition: Code containing TODO, FIXME, HACK, or similar markers indicating incomplete implementation that should be resolved before release.

Threshold: TODO/FIXME/HACK/XXX markers in source code

Severity: HIGH

Detection Method: Grep

Two-Stage: No — keyword pattern matching is sufficient.

JSON Output Schema:
```json
{
  "smell_type": "placeholder_code",
  "severity": "HIGH",
  "file": "src/services/payment.py",
  "line": 67,
  "marker": "TODO",
  "text": "TODO: implement retry logic for failed payments",
  "evidence": "Placeholder marker 'TODO' found indicating incomplete implementation",
  "remediation": "Implement the described functionality or create a story to track the work"
}
```

Test Scenarios:

1. `# TODO: implement caching` should be flagged
2. `// FIXME: race condition here` should be flagged
3. `/* HACK: workaround for API bug */` should be flagged
4. `todoList.add(item)` should NOT be flagged (variable name, not marker)

False Positive Patterns:
- Variable/function names containing "todo" (e.g., `todoList`, `fixMethod`)
- Documentation describing TODO workflow or methodology
- Test file comments explaining expected behavior

Fowler Reference: Not directly in Fowler's catalog, but related to "Incomplete Library Class" and technical debt tracking.

---

## Middle Man

Definition: A class where the majority of methods simply delegate to another class, adding an unnecessary layer of indirection.

Threshold: >80% delegation ratio with >=3 methods

Severity: MEDIUM

Detection Method: Treelint

Two-Stage: No — delegation ratio calculation from AST is deterministic.

JSON Output Schema:
```json
{
  "smell_type": "middle_man",
  "severity": "MEDIUM",
  "class_name": "OrderProxy",
  "file": "src/services/order_proxy.py",
  "line": 5,
  "total_methods": 4,
  "delegating_methods": 4,
  "delegation_ratio": 1.0,
  "evidence": "Class has 4/4 methods delegating (100%), exceeding 80% threshold",
  "remediation": "Remove middle man class; have callers use the delegate directly"
}
```

Test Scenarios:

1. Class with 4 methods, all delegating (100%) should be flagged
2. Class with 5 methods, 3 delegating (60%) should NOT be flagged (below 80%)
3. Class with 2 methods, both delegating should NOT be flagged (<3 methods minimum)
4. Adapter pattern class should be excluded if it transforms data between calls

False Positive Patterns:
- Adapter/Bridge pattern classes that transform data between delegate calls
- Decorator classes that add behavior before/after delegation
- Classes with fewer than 3 methods (too small to be meaningful middle man)

Fowler Reference: "Middle Man" smell — Fowler recommends Remove Middle Man refactoring. See refactoring.guru/refactoring/smells/middle-man.

---

## Message Chain

Definition: A sequence of calls navigating through multiple objects (a.getB().getC().getD()), violating the Law of Demeter and creating tight coupling.

Threshold: 3+ chained method calls

Severity: LOW

Detection Method: Grep

Two-Stage: Yes — Stage 1 Grep detects chain patterns, Stage 2 LLM distinguishes navigation chains from fluent APIs.

JSON Output Schema:
```json
{
  "smell_type": "message_chain",
  "severity": "LOW",
  "file": "src/services/report.py",
  "line": 34,
  "chain_excerpt": "order.getCustomer().getAddress().getCity()",
  "chain_length": 3,
  "confidence": 0.85,
  "evidence": "3-call navigation chain violates Law of Demeter",
  "remediation": "Create encapsulation method on intermediate object, e.g., order.getCustomerCity()"
}
```

Test Scenarios:

1. `order.getCustomer().getAddress().getCity()` should be flagged (navigation chain)
2. `QueryBuilder().where(x).orderBy(y).limit(10)` should NOT be flagged (fluent API)
3. `promise.then(a).catch(b).finally(c)` should NOT be flagged (promise chain)
4. `a.b.c.d` property access chain with 4 levels should be flagged

False Positive Patterns:
- Fluent/Builder API patterns (QueryBuilder, StringBuilder)
- Promise/Future chains (then/catch/finally)
- jQuery chains (starting with `$`)
- Stream/LINQ chains (map/filter/reduce)

Fowler Reference: "Message Chains" smell — Fowler recommends Hide Delegate refactoring. See refactoring.guru/refactoring/smells/message-chains.

---

## Summary Table

| Name | Threshold | Severity | Detection Method | Two-Stage |
|------|-----------|----------|-----------------|-----------|
| God Object | >20 methods OR >300 lines | CRITICAL | Treelint | No |
| Long Method | >50 lines | MEDIUM | Treelint | No |
| Magic Number | Hardcoded numeric literals | MEDIUM | Grep | No |
| Data Class | <3 methods AND >2 properties | MEDIUM | Treelint | Yes |
| Long Parameter List | >4 parameters | MEDIUM | Treelint | No |
| Commented-Out Code | Commented code blocks | LOW | Grep | Yes |
| Orphaned Import | Unused imports | LOW | Grep | No |
| Dead Code | Unreachable code | LOW | Treelint | No |
| Placeholder Code | TODO/FIXME markers | HIGH | Grep | No |
| Middle Man | >80% delegation ratio, >=3 methods | MEDIUM | Treelint | No |
| Message Chain | 3+ chained method calls | LOW | Grep | Yes |

## Cross-References

- Fowler, Martin. *Refactoring: Improving the Design of Existing Code* (2nd edition)
- https://refactoring.guru/refactoring/smells — online catalog of code smells with refactoring recipes
