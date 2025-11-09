# EPIC-004: Query Library (12 Patterns)

---
id: EPIC-004
title: Query Library (12 Patterns)
status: Backlog
created: 2025-11-01
target_sprint: Sprint-2, Sprint-3
estimated_points: 40
priority: CRITICAL
---

## Business Goal

Implement 12 core tree-sitter query patterns that detect anti-patterns, architecture violations, security issues, and test coverage gaps with <5% false positive rate.

## Success Metrics

- ✅ 12 patterns implemented across 4 categories
- ✅ Each pattern tested against all 5 bundled languages
- ✅ <5% false positive rate on test suite (100+ test cases)
- ✅ 100% detection of actual violations (no false negatives)
- ✅ Pattern documentation with examples and rationale
- ✅ Embedded in binary (no external files required)

## Features

### Feature 1: Anti-Patterns Library (4 patterns)

#### Pattern 1.1: God Objects (Classes >500 lines)
- **Query:** `queries/anti-patterns/god-objects.scm`
- **Detection:** Class declarations with >500 line bodies
- **Languages:** JavaScript, TypeScript, Python, C#, Go, Rust
- **Severity:** CRITICAL
- **Rationale:** Classes with >500 lines violate Single Responsibility Principle

**Example (JavaScript):**
```scheme
(class_declaration
  name: (identifier) @class.name
  body: (class_body) @body
  (#count-lines @body >500))
```

#### Pattern 1.2: Direct Instantiation (Violates DI)
- **Query:** `queries/anti-patterns/direct-instantiation.scm`
- **Detection:** `new Service()` calls in business logic classes
- **Languages:** JavaScript, TypeScript, Python, C#, Go
- **Severity:** HIGH
- **Rationale:** Direct instantiation prevents dependency injection and testing

**Example (TypeScript):**
```scheme
(new_expression
  constructor: (identifier) @class.name
  (#match? @class.name ".*Service|.*Repository|.*Manager"))
```

#### Pattern 1.3: Magic Numbers
- **Query:** `queries/anti-patterns/magic-numbers.scm`
- **Detection:** Numeric literals not in const/final declarations
- **Languages:** All 5 bundled languages
- **Severity:** MEDIUM
- **Rationale:** Hardcoded numbers reduce maintainability

**Example (Python):**
```scheme
(integer
  (#not-parent? @integer const_declaration)
  (#not-parent? @integer assignment final))
```

#### Pattern 1.4: Long Functions
- **Query:** `queries/anti-patterns/long-functions.scm`
- **Detection:** Functions >50 lines
- **Languages:** All 5 bundled languages
- **Severity:** MEDIUM
- **Rationale:** Long functions are hard to test and maintain

**Example (Rust):**
```scheme
(function_item
  name: (identifier) @function.name
  body: (block) @body
  (#count-lines @body >50))
```

---

### Feature 2: Architecture Patterns Library (4 patterns)

#### Pattern 2.1: Layer Boundaries
- **Query:** `queries/architecture/layer-boundaries.scm`
- **Detection:** Domain layer importing Infrastructure layer
- **Languages:** All (via import statement analysis)
- **Severity:** CRITICAL
- **Rationale:** Violates Clean Architecture dependency rules

**Example (TypeScript):**
```scheme
; In files matching src/domain/**/*
(import_statement
  source: (string_literal) @import.path
  (#match? @import.path ".*infrastructure.*|.*infra.*"))
```

#### Pattern 2.2: Dependency Injection Validation
- **Query:** `queries/architecture/dependency-injection.scm`
- **Detection:** Services without constructor injection
- **Languages:** C#, TypeScript, Python, Go
- **Severity:** HIGH
- **Rationale:** Ensures testability through DI

**Example (C#):**
```scheme
(class_declaration
  name: (identifier) @class.name
  (#match? @class.name ".*Service")
  (declaration_list
    (constructor_declaration) @constructor
    (#not-match? @constructor ".*IRepository.*|.*IService.*")))
```

#### Pattern 2.3: Circular Dependencies
- **Query:** `queries/architecture/circular-dependencies.scm`
- **Detection:** Module A imports B, B imports A
- **Languages:** All (via import graph analysis)
- **Severity:** HIGH
- **Rationale:** Circular dependencies indicate poor module design

**Implementation:** Requires multi-file analysis (build import graph)

#### Pattern 2.4: Clean Architecture Compliance
- **Query:** `queries/architecture/clean-architecture.scm`
- **Detection:** Violations of dependency inversion principle
- **Languages:** All (via import analysis by directory)
- **Severity:** MEDIUM
- **Rationale:** Ensures architectural integrity

---

### Feature 3: Security Patterns Library (3 patterns)

#### Pattern 3.1: SQL Injection
- **Query:** `queries/security/sql-injection.scm`
- **Detection:** String concatenation in SQL queries
- **Languages:** All (SQL strings universal)
- **Severity:** CRITICAL
- **Rationale:** OWASP #1, prevents SQL injection attacks

**Example (Python):**
```scheme
; Pattern 1: String concatenation with SQL keywords
(binary_expression
  left: (string) @sql.left
  operator: "+"
  right: (identifier) @user.input
  (#match? @sql.left "SELECT|INSERT|UPDATE|DELETE|DROP"))

; Pattern 2: f-strings with SQL
(formatted_string_literal
  (interpolation (identifier) @user.input)
  (#match? @formatted_string "SELECT|INSERT|UPDATE|DELETE"))
```

#### Pattern 3.2: Hardcoded Secrets
- **Query:** `queries/security/hardcoded-secrets.scm`
- **Detection:** API keys, passwords, tokens in string literals
- **Languages:** All
- **Severity:** CRITICAL
- **Rationale:** Prevents credential leaks

**Example (All Languages):**
```scheme
; Detect patterns like: api_key = "sk-..."
(variable_declarator
  name: (identifier) @var.name
  value: (string_literal) @secret.value
  (#match? @var.name ".*key|.*token|.*password|.*secret.*")
  (#match? @secret.value "^['\"]sk-|^['\"]ghp_|^['\"]pk_"))
```

#### Pattern 3.3: Weak Cryptography
- **Query:** `queries/security/weak-crypto.scm`
- **Detection:** MD5, SHA1 usage (deprecated algorithms)
- **Languages:** All (library usage patterns)
- **Severity:** HIGH
- **Rationale:** MD5/SHA1 are cryptographically broken

**Example (JavaScript/TypeScript):**
```scheme
(call_expression
  function: (member_expression
    property: (property_identifier) @method
    (#match? @method "createHash"))
  arguments: (arguments
    (string) @algorithm
    (#match? @algorithm "md5|sha1")))
```

---

### Feature 4: Testing Patterns Library (1 pattern)

#### Pattern 4.1: Public Functions (Coverage Gap Analysis)
- **Query:** `queries/testing/public-functions.scm`
- **Detection:** All public/exported functions
- **Languages:** All (language-specific export patterns)
- **Severity:** INFO (not a violation, used for coverage analysis)
- **Rationale:** Identifies functions that should have tests

**Example (TypeScript):**
```scheme
; Exported functions
(export_statement
  declaration: (function_declaration
    name: (identifier) @function.name))

; Named exports
(export_statement
  (export_clause
    (export_specifier
      name: (identifier) @function.name)))
```

**Example (Python):**
```scheme
; Module-level functions (not inside classes)
(module
  (function_definition
    name: (identifier) @function.name
    (#not-in-class? @function.name)))
```

**Example (Rust):**
```scheme
; Public functions
(function_item
  (visibility_modifier) @vis
  name: (identifier) @function.name
  (#eq? @vis "pub"))
```

---

## Requirements Addressed

- **FR-3:** Pattern Library (CRITICAL)
- **NFR-1:** Performance (Query execution <250ms each)
- **NFR-3:** Accuracy (<5% false positive rate)

## Non-Functional Requirements

- **Accuracy:** <5% false positive rate per pattern
- **Performance:** <250ms query execution per pattern
- **Coverage:** Works across all 5 bundled languages
- **Maintainability:** Documented with examples and rationale

## Architecture Considerations

**Pattern Storage:**
```
queries/
├── anti-patterns/
│   ├── god-objects.scm
│   ├── direct-instantiation.scm
│   ├── magic-numbers.scm
│   └── long-functions.scm
├── architecture/
│   ├── layer-boundaries.scm
│   ├── dependency-injection.scm
│   ├── circular-dependencies.scm
│   └── clean-architecture.scm
├── security/
│   ├── sql-injection.scm
│   ├── hardcoded-secrets.scm
│   └── weak-crypto.scm
└── testing/
    └── public-functions.scm
```

**Pattern Registry:**
```rust
// src/patterns/registry.rs

use lazy_static::lazy_static;
use include_dir::{include_dir, Dir};

static PATTERNS: Dir = include_dir!("$CARGO_MANIFEST_DIR/queries");

lazy_static! {
    static ref PATTERN_REGISTRY: HashMap<String, Pattern> = {
        let mut registry = HashMap::new();

        // Load all .scm files from embedded directory
        for file in PATTERNS.files() {
            if file.path().extension() == Some("scm") {
                let pattern = Pattern::from_file(file)?;
                registry.insert(pattern.id.clone(), pattern);
            }
        }

        registry
    };
}

pub fn get_pattern(id: &str) -> Option<&Pattern> {
    PATTERN_REGISTRY.get(id)
}

pub fn get_category(category: &str) -> Vec<&Pattern> {
    PATTERN_REGISTRY.values()
        .filter(|p| p.category == category)
        .collect()
}
```

**Key Design Decisions:**
- **Embed patterns at compile time** (include_dir macro) - Work offline
- **lazy_static for registry** - Pre-compile queries once at startup
- **Category support** - Run all anti-patterns with single command
- **Extensible** - Add patterns by adding .scm files to queries/

---

## Testing Strategy

### Accuracy Testing

**For each pattern, create test fixtures:**

```
tests/fixtures/
├── anti-patterns/
│   ├── god-object.rs          # 501-line class (should detect)
│   ├── normal-class.rs        # 200-line class (should NOT detect)
│   ├── direct-instantiation.ts # new Service() (should detect)
│   ├── injected-service.ts    # constructor DI (should NOT detect)
│   └── ...
├── architecture/
│   ├── layer-violation.py     # domain imports infra (should detect)
│   ├── clean-import.py        # domain imports domain (should NOT detect)
│   └── ...
└── security/
    ├── sql-injection.js       # "SELECT * FROM " + user (should detect)
    ├── parameterized-query.js # Prepared statement (should NOT detect)
    └── ...
```

**Accuracy Test:**
```rust
#[test]
fn test_god_object_detection_accuracy() {
    // True positive (should detect)
    let violations = analyze_pattern(
        "god-objects",
        "tests/fixtures/anti-patterns/god-object.rs"
    ).unwrap();
    assert_eq!(violations.len(), 1, "Should detect 501-line class");

    // True negative (should NOT detect)
    let violations = analyze_pattern(
        "god-objects",
        "tests/fixtures/anti-patterns/normal-class.rs"
    ).unwrap();
    assert_eq!(violations.len(), 0, "Should not flag 200-line class");
}
```

**Run against all patterns:**
```bash
# Accuracy validation
cargo test accuracy --test pattern_accuracy_tests

# Expected: >95% accuracy (true positives + true negatives)
```

---

### Cross-Language Testing

**Each pattern must work in all applicable languages:**

```rust
#[test]
fn test_god_objects_cross_language() {
    let test_cases = vec![
        ("tests/fixtures/god-object.js", Language::JavaScript),
        ("tests/fixtures/god-object.py", Language::Python),
        ("tests/fixtures/god-object.cs", Language::CSharp),
        ("tests/fixtures/god-object.go", Language::Go),
        ("tests/fixtures/god-object.rs", Language::Rust),
    ];

    for (file, language) in test_cases {
        let violations = analyze_pattern("god-objects", file).unwrap();
        assert_eq!(
            violations.len(), 1,
            "{:?} should detect god object in {}", language, file
        );
    }
}
```

---

### Performance Testing

**Benchmark each pattern:**

```rust
// benches/pattern_performance.rs

use criterion::{black_box, criterion_group, criterion_main, Criterion};

fn benchmark_god_objects(c: &mut Criterion) {
    let source = include_str!("../tests/fixtures/large-file.rs");  // 10K lines
    let tree = parse_rust(source).unwrap();

    c.bench_function("god-objects pattern", |b| {
        b.iter(|| {
            detect_god_objects(black_box(&tree), black_box(source))
        });
    });
}

criterion_group!(benches, benchmark_god_objects);
criterion_main!(benches);
```

**Target:** <250ms per pattern (10K line file)

---

## Pattern Implementation Workflow

### For Each Pattern (12 iterations)

**Step 1: Research** (1 day)
- Study existing tree-sitter queries for similar patterns
- Understand language-specific AST structures
- Review Neovim, Helix query libraries for examples

**Step 2: Write Queries** (1 day)
- Create .scm file for each language variant
- Test query syntax with `tree-sitter-cli`
- Document capture groups and predicates

**Step 3: Implement Detection Logic** (1 day)
- Integrate query into pattern registry
- Add Violation extraction logic
- Handle edge cases (syntax errors, partial matches)

**Step 4: Test** (1 day)
- Create test fixtures (true positives + true negatives)
- Write accuracy tests
- Test across all 5 languages
- Measure false positive rate

**Step 5: Document** (0.5 days)
- Add pattern to README
- Document rationale and severity
- Provide examples (✅ CORRECT vs ❌ FORBIDDEN)
- Link to related anti-patterns.md section

**Total per pattern:** ~5 days
**12 patterns:** ~12 weeks at 1 pattern per week (conservative)

**Optimized:** 2-3 patterns per week once workflow established
**Realistic:** 3-4 weeks total for 12 patterns (Sprint 2-3)

---

## Pattern Priority (Implementation Order)

### Sprint 2 (Weeks 4-6): Critical Patterns (6)

**High Impact + High Severity:**
1. SQL Injection (security) - CRITICAL
2. Hardcoded Secrets (security) - CRITICAL
3. Layer Boundaries (architecture) - CRITICAL
4. God Objects (anti-pattern) - CRITICAL
5. Direct Instantiation (anti-pattern) - HIGH
6. Dependency Injection (architecture) - HIGH

**Rationale:** Security and architecture patterns are most critical for DevForgeAI

---

### Sprint 3 (Weeks 7-9): Remaining Patterns (6)

**Medium Priority:**
7. Weak Crypto (security) - HIGH
8. Circular Dependencies (architecture) - HIGH
9. Magic Numbers (anti-pattern) - MEDIUM
10. Long Functions (anti-pattern) - MEDIUM
11. Clean Architecture (architecture) - MEDIUM
12. Public Functions (testing) - INFO

**Rationale:** Complete coverage, lower urgency

---

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Cross-language queries don't work uniformly | High | Test early (Week 4), accept language-specific variants |
| False positive rate >5% | High | Refine queries iteratively, add negative tests |
| Implementation takes longer than 3-4 weeks | Medium | Prioritize critical patterns, defer medium if needed |
| Tree-sitter predicate limitations | Medium | Research existing queries, fallback to Rust logic if needed |

## Assumptions

- Tree-sitter query language can express all 12 patterns
- #count-lines predicate available (or implementable)
- Import graph analysis feasible for circular dependencies
- Test fixtures can be created for all patterns

## Dependencies

**Crates:**
- `tree-sitter = "0.20"` (query execution)
- `lazy_static = "1.4"` (pattern registry)
- `include_dir = "0.7"` (embed queries)
- `regex = "1.10"` (for #match? predicate)

**Test Dependencies:**
- Test fixtures for each pattern (in `tests/fixtures/`)
- Sample codebases with known violations

**Development:**
- tree-sitter-cli (for testing queries during development)

---

## Pattern Documentation Template

Each pattern must have:

**1. Pattern Definition (.scm file)**
```scheme
; queries/anti-patterns/god-objects.scm
; Detect classes with >500 lines

(class_declaration
  name: (identifier) @class.name
  body: (class_body) @body
  (#count-lines @body >500))
```

**2. Metadata**
```rust
Pattern {
    id: "god-objects",
    name: "God Objects",
    category: PatternCategory::AntiPattern,
    severity: Severity::Critical,
    description: "Classes with >500 lines violate Single Responsibility Principle",
    languages: vec!["javascript", "typescript", "python", "csharp", "go", "rust"],
}
```

**3. Documentation (docs/patterns/god-objects.md)**
```markdown
# God Objects

**Category:** Anti-Pattern
**Severity:** CRITICAL

## Description
Classes with more than 500 lines typically violate the Single Responsibility
Principle and should be refactored into smaller, focused classes.

## Detection
Counts lines in class body. Triggers if >500 lines.

## Examples

❌ FORBIDDEN:
```typescript
class GodClass {
    // 501 lines of mixed responsibilities
    // User management, order processing, email sending, etc.
}
```

✅ CORRECT:
```typescript
class UserManager {
    // 120 lines focused on user operations
}

class OrderProcessor {
    // 150 lines focused on order handling
}

class EmailService {
    // 80 lines focused on email sending
}
```

## Rationale
- Single Responsibility Principle (SOLID)
- Easier testing (focused tests)
- Better maintainability
- Clearer intent

## References
- Clean Code by Robert C. Martin (Chapter 10: Classes)
- SOLID Principles: Single Responsibility
```

---

## Integration with DevForgeAI

**Subagent Usage:**

```python
# context-validator.md

import subprocess
import json

def validate_all_anti_patterns(src_path: str) -> list[dict]:
    """Run all anti-pattern checks."""
    result = subprocess.run(
        ['treelint', 'analyze', '--pattern=anti-patterns', '--format=json', src_path],
        capture_output=True,
        text=True,
        check=True
    )

    violations = json.loads(result.stdout)
    return violations

def validate_layer_boundaries(domain_path: str) -> list[dict]:
    """Check architectural layer boundaries."""
    result = subprocess.run(
        ['treelint', 'analyze', '--pattern=layer-boundaries', '--format=json', domain_path],
        capture_output=True,
        text=True,
        check=True
    )

    violations = json.loads(result.stdout)
    return violations
```

**Light QA Integration:**
```python
# devforgeai-qa skill (light mode)

# Run 4 critical patterns
patterns = ['layer-boundaries', 'sql-injection', 'hardcoded-secrets', 'god-objects']

all_violations = []
for pattern in patterns:
    violations = run_treelint_pattern(pattern, 'src/')
    all_violations.extend(violations)

# Block if critical violations found
critical_violations = [v for v in all_violations if v['severity'] == 'CRITICAL']
if critical_violations:
    raise ValidationError(f"Found {len(critical_violations)} CRITICAL violations")
```

---

## Next Steps

After completing this epic:
1. Integrate with EPIC-006 (Performance Optimization) - Benchmark patterns
2. Test with DevForgeAI codebase - Validate real-world accuracy
3. Document pattern library in user guide
4. Prepare for v1.1 (10 additional patterns)

## Related Epics

- **EPIC-003:** Query Pattern Matching (dependency - query engine must exist)
- **EPIC-002:** Tree-sitter AST Parsing (dependency - provides parsed ASTs)
- **EPIC-006:** Performance Optimization (optimizes pattern execution)

---

**Epic Owner:** Solo Developer
**Target Completion:** End of Sprint 3 (Week 9)
**Learning Resources:**
- Tree-sitter query examples: https://github.com/nvim-treesitter/nvim-treesitter/tree/master/queries
- Pattern catalog: https://refactoring.guru/design-patterns/catalog
- OWASP Top 10: https://owasp.org/www-project-top-ten/
