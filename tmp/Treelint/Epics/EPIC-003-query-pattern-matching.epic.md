# EPIC-003: Query Pattern Matching

---
id: EPIC-003
title: Query Pattern Matching
status: Backlog
created: 2025-11-01
target_sprint: Sprint-2
estimated_points: 26
priority: CRITICAL
---

## Business Goal

Implement S-expression query execution engine that matches code patterns against parsed ASTs, enabling accurate detection of anti-patterns, architecture violations, and security issues.

## Success Metrics

- ✅ Execute tree-sitter queries (.scm files) against ASTs
- ✅ Support capture groups (@variable.name)
- ✅ Support predicates (#match?, #eq?, #not-eq?)
- ✅ Query execution <250ms per pattern (10K line file)
- ✅ Return match locations (file, line, column, code snippet)

## Features

### Feature 1: Query Parser
- Parse S-expression query syntax
- Validate query structure
- Pre-compile queries for reuse
- Handle query syntax errors gracefully

### Feature 2: Query Execution Engine
- Execute queries against AST
- Extract capture groups
- Evaluate predicates
- Handle negation and alternation

### Feature 3: Match Result Handling
- Extract match locations (byte offset → line/column)
- Extract code snippets (surrounding context)
- Format match results
- Deduplicate overlapping matches

### Feature 4: Predicate Support
- `#match?` - Regex matching on captured text
- `#eq?` - Equality check
- `#not-eq?` - Inequality check
- Custom predicates (e.g., `#count-lines`)

### Feature 5: Violation Reporting
- Map matches to Violation struct
- Include severity, message, code snippet
- JSON serialization
- Text formatting

## Requirements Addressed

- **FR-2:** Query Pattern Matching (CRITICAL)
- **NFR-1:** Performance (Query execution <250ms)
- **NFR-3:** Accuracy (<5% false positive rate)

## Non-Functional Requirements

- **Performance:** <250ms per query (10K line file)
- **Accuracy:** 100% capture of actual matches
- **Memory:** <100MB per query execution

## Architecture Considerations

**Module Structure:**
```
src/
├── query/
│   ├── mod.rs          # Query engine interface
│   ├── parser.rs       # Parse .scm query files
│   ├── executor.rs     # Execute queries against AST
│   ├── predicates.rs   # Predicate evaluation
│   └── results.rs      # Match result handling
└── violation.rs        # Violation struct and formatting
```

**Query Execution Flow:**
```rust
pub struct QueryEngine {
    query: Query,
    pattern_name: String,
}

impl QueryEngine {
    pub fn new(pattern_name: &str, query_source: &str) -> Result<Self> {
        let query = Query::new(language, query_source)?;
        Ok(QueryEngine {
            query,
            pattern_name: pattern_name.to_string(),
        })
    }

    pub fn execute(&self, tree: &Tree, source: &str) -> Vec<Violation> {
        let mut cursor = QueryCursor::new();
        let matches = cursor.matches(&self.query, tree.root_node(), source.as_bytes());

        matches
            .flat_map(|m| self.extract_violations(m, source))
            .collect()
    }
}
```

**Key Design Decisions:**
- **lazy_static** for query pre-compilation (parse once, execute many times)
- **Byte offset → Line/Column:** Use newline counting for conversion
- **Code Snippet Extraction:** ±3 lines of context around match
- **Deduplication:** Use HashSet based on file + line + column

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Query syntax errors hard to debug | Medium | Provide clear error messages with line/column info |
| Cross-language query differences | High | Test each pattern against all 5 languages separately |
| Performance: Slow queries | Medium | Benchmark early, optimize if needed |
| Predicate evaluation errors | Low | Comprehensive predicate tests |

## Assumptions

- Tree-sitter query syntax is sufficient for all 12 patterns
- Line/column calculation from byte offset is accurate
- Code snippet extraction (±3 lines) is sufficient context

## Dependencies

**Crates:**
- `tree-sitter = "0.20"` (Query, QueryCursor)
- `lazy_static = "1.4"` (query pre-compilation)
- `regex = "1.10"` (for #match? predicate)

**Development:**
- Test fixtures with known patterns (god objects, SQL injection, etc.)

## Testing Strategy

**Unit Tests:**
- Query parsing (valid syntax, invalid syntax)
- Predicate evaluation (#match?, #eq?, #not-eq?)
- Line/column calculation
- Code snippet extraction

**Integration Tests:**
```rust
#[test]
fn test_detect_god_object() {
    let source = r#"
        class GodClass {
            // 501 lines of code...
        }
    "#;

    let tree = parse_typescript(source)?;
    let engine = QueryEngine::new("god-objects", GOD_OBJECT_QUERY)?;
    let violations = engine.execute(&tree, source);

    assert_eq!(violations.len(), 1);
    assert_eq!(violations[0].pattern_id, "god-objects");
}
```

## Example Query Patterns

**God Objects:**
```scheme
; Detect classes with >500 lines
(class_declaration
  name: (identifier) @class.name
  body: (class_body) @body
  (#count-lines @body >500))
```

**SQL Injection:**
```scheme
; Detect string concatenation in SQL
(binary_expression
  left: (string_literal) @sql.left
  operator: "+"
  right: (identifier) @user.input
  (#match? @sql.left "SELECT|INSERT|UPDATE|DELETE"))
```

**Dependency Injection:**
```scheme
; Detect direct instantiation in business logic
(new_expression
  constructor: (identifier) @class.name
  (#match? @class.name ".*Service|.*Repository"))
```

## Next Steps

After completing this epic:
1. Proceed to EPIC-004 (Query Library) - implement 12 core patterns
2. Integrate with EPIC-006 (Performance Optimization) - optimize query execution
3. Test with DevForgeAI codebase - validate accuracy

## Related Epics

- **EPIC-002:** Tree-sitter AST Parsing (dependency - provides parsed ASTs)
- **EPIC-004:** Query Library (consumes query engine)
- **EPIC-006:** Performance Optimization (optimizes query execution)

---

**Epic Owner:** Solo Developer
**Target Completion:** End of Sprint 2 (Week 6)
**Learning Resources:**
- Tree-sitter query documentation: https://tree-sitter.github.io/tree-sitter/using-parsers#pattern-matching-with-queries
- Tree-sitter query examples: https://github.com/nvim-treesitter/nvim-treesitter/tree/master/queries
