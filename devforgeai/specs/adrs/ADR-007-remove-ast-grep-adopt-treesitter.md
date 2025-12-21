# ADR-007: Remove ast-grep and Evaluate Tree-sitter for Static Analysis

**Status**: ACCEPTED
**Date**: 2025-12-21
**Decision Makers**: DevForgeAI Framework Team
**Related Stories**: STORY-115, STORY-116, STORY-117, STORY-118
**Related Epic**: EPIC-018 (ast-grep Foundation & Core Rules)

---

## Context

DevForgeAI evaluated ast-grep as the static analysis foundation for security and anti-pattern rule detection (EPIC-018). After implementing 25+ rules and extensive testing, fundamental limitations were discovered that prevent the tool from meeting framework requirements.

### The Problem

ast-grep's pattern matching system has critical limitations for production use:

1. **Multi-line Pattern Matching Failures**: Patterns with multiple statements (common in real code) fail to match when:
   - Comments exist between statements
   - Code has type annotations
   - Indentation varies from expected whitespace
   - Method bodies span multiple lines

2. **Language-Specific AST Constraints**: Undocumented behaviors for:
   - Python class/method detection
   - C# catch blocks and access modifiers
   - TypeScript type annotations

3. **Semantic Analysis Impossible**: ast-grep is purely structural and cannot:
   - Detect duplicate code (requires token stream analysis)
   - Count methods/fields (requires AST traversal, not pattern matching)
   - Perform cross-file analysis

### Evidence from STORY-118 Remediation

**Test Results**: 52/59 passing (88.1%), 6 tests failing despite comprehensive remediation

**Specific Failures**:

| Rule | Test | Pattern Attempted | Result |
|------|------|-------------------|--------|
| AP-001 | God Object Methods | Multi-line class with 10+ method defs | No matches |
| AP-001 | God Object Fields | Class with 10+ `self.$` assignments | No matches |
| AP-002 | Async Void | Pattern with access modifiers | No matches |
| AP-004 | Magic Numbers | 30+ pattern variants | No matches |
| AP-008 | Excessive Params | 7 parameter variations | No matches |
| AP-010 | Empty Catch | C# catch block patterns | No matches |

**Diagnostic Command**:
```bash
$ ast-grep scan --rule god-object.yml god_object_many_fields.py --json
[]  # No matches despite 21 fields in fixture
```

---

## Decision

**Remove ast-grep from the DevForgeAI framework and explore tree-sitter as a replacement for static analysis capabilities.**

### Actions

1. **Immediate**: Mark EPIC-018 as CANCELLED
2. **Immediate**: Uninstall ast-grep from project dependencies
3. **Immediate**: Archive ast-grep rules (retain for reference, mark as deprecated)
4. **Follow-up**: Create new epic for tree-sitter evaluation
5. **Follow-up**: Enhance devforgeai CLI with tree-sitter bindings

---

## Alternatives Considered

### Alternative 1: Continue with ast-grep (REJECTED)

**Pros**: Already implemented, 25+ rules written
**Cons**: Fundamental pattern matching limitations make it unusable for production
**Decision**: REJECTED - Cannot meet quality gate (95% test pass rate)

### Alternative 2: Use ast-grep for simple patterns only (REJECTED)

**Pros**: Some rules work (console.log, simple patterns)
**Cons**: Inconsistent coverage (10% of intended rules work), creates false confidence
**Decision**: REJECTED - Partial solution worse than no solution

### Alternative 3: Contribute fixes to ast-grep upstream (REJECTED)

**Pros**: Would fix root cause
**Cons**: Requires deep Rust/tree-sitter knowledge, unknown timeline, may not be accepted
**Decision**: REJECTED - Too risky and time-consuming for framework timeline

### Alternative 4: Switch to tree-sitter (ACCEPTED)

**Pros**:
- Direct AST access (not pattern matching)
- Python bindings available (`py-tree-sitter`)
- Can traverse, count, and analyze (not just match)
- Widely used (GitHub, Neovim, Helix)
- Supports 100+ languages
- Can be integrated into devforgeai CLI

**Cons**:
- Requires new implementation
- Different paradigm (traversal vs pattern matching)
- Learning curve for tree-sitter queries

**Decision**: ACCEPTED - Better architectural fit for framework needs

### Alternative 5: Use Semgrep instead (DEFERRED)

**Pros**: More mature pattern matching, supports semantic analysis
**Cons**: Commercial licensing for advanced features, heavier dependency
**Decision**: DEFERRED - Evaluate after tree-sitter assessment

---

## ast-grep Limitations (Documented for Reference)

### Limitation 1: Multi-line Pattern Whitespace Sensitivity

ast-grep patterns require exact whitespace matching in YAML. Python's indentation-based syntax makes this particularly problematic.

```yaml
# This pattern DOES NOT MATCH real code:
rule:
  pattern: |
    class $CLASS:
        def $M1($$$): $$$
        def $M2($$$): $$$
```

**Why it fails**: Fixtures have docstrings, comments, type annotations between method definitions.

### Limitation 2: Cannot Match Across Comments

Sequential patterns break when comments exist:

```python
# Fixture (should match):
class MyClass:
    def method1(self):
        pass  # Comment here

    def method2(self):  # Another comment
        pass
```

Pattern expects consecutive `def` statements but comments break the sequence.

### Limitation 3: No Counting or Accumulation

ast-grep patterns match structural occurrences but cannot:
- Count how many methods exist in a class
- Count how many fields are assigned
- Aggregate findings across a file

This makes "god object detection" (>20 methods) fundamentally impossible.

### Limitation 4: C# Access Modifier Handling

Patterns like `async void $METHOD($$$)` don't match when preceded by access modifiers:

```csharp
// Pattern expects: async void Process()
// Actual code:     public async void Process()  // NO MATCH
```

Even adding `public async void $METHOD($$$)` to the pattern didn't produce matches, suggesting deeper AST representation issues.

### Limitation 5: Semantic Patterns Unsupported

ast-grep is structural only. It cannot detect:
- Duplicate code (requires token stream comparison like jscpd)
- Unused variables (requires scope analysis)
- Type mismatches (requires type inference)

---

## Tree-sitter Integration Plan

### Phase 1: Evaluation (STORY-TBD)

1. Install `py-tree-sitter` and language bindings
2. Implement Python class/method counter
3. Test against STORY-118 fixtures
4. Benchmark against ast-grep

### Phase 2: CLI Integration (STORY-TBD)

1. Add `devforgeai analyze` command
2. Implement god object detection via AST traversal
3. Implement async void detection for C#
4. Implement magic numbers detection

### Phase 3: Rule Engine (STORY-TBD)

1. Define tree-sitter query format for rules
2. Build rule loader and executor
3. Port security rules from ast-grep
4. Port anti-pattern rules from ast-grep

### Expected Benefits

| Capability | ast-grep | tree-sitter |
|------------|----------|-------------|
| Pattern matching | Limited | N/A (uses traversal) |
| Node counting | No | Yes |
| Comment handling | Breaks patterns | Comments are nodes |
| Cross-file analysis | No | Yes (with scope) |
| Semantic analysis | No | Possible |
| Python bindings | No | Yes |
| Integration with CLI | External process | Native library |

---

## Consequences

### Positive

1. **Removes Blocker**: EPIC-018 no longer blocked by tool limitations
2. **Better Architecture**: tree-sitter provides full AST access
3. **Native Integration**: Python bindings integrate directly with devforgeai CLI
4. **Future-Proof**: tree-sitter is industry standard (GitHub, Neovim, Helix)

### Negative

1. **Sunk Cost**: 25+ ast-grep rules need reimplementation
2. **Timeline Impact**: Tree-sitter integration is new work
3. **Learning Curve**: Different paradigm (traversal vs patterns)

### Neutral

1. **Rule Files**: Can archive ast-grep rules as implementation reference
2. **Test Fixtures**: All fixtures remain valid for tree-sitter testing
3. **Documentation**: ast-grep docs serve as requirements source

---

## Implementation Status

- [x] ADR-007 created (this document)
- [ ] STORY-118 updated with cancellation
- [ ] tech-stack.md updated to remove ast-grep
- [ ] EPIC-018 marked as CANCELLED
- [ ] ast-grep uninstalled
- [ ] New epic created for tree-sitter evaluation
- [ ] devforgeai CLI tree-sitter integration planned

---

## References

- [STORY-118 Remediation Report](../../../STORY-118-REMEDIATION-STATUS.md)
- [EPIC-018: ast-grep Foundation](../Epics/EPIC-018-astgrep-foundation-core-rules.epic.md)
- [tree-sitter Documentation](https://tree-sitter.github.io/tree-sitter/)
- [py-tree-sitter GitHub](https://github.com/tree-sitter/py-tree-sitter)
- [ast-grep Documentation](https://ast-grep.github.io/)

---

**Approved By**: Framework Team
**Approval Date**: 2025-12-21
