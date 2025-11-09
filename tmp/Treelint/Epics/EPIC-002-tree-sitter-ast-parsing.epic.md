# EPIC-002: Tree-sitter AST Parsing

---
id: EPIC-002
title: Tree-sitter AST Parsing
status: Backlog
created: 2025-11-01
target_sprint: Sprint-1, Sprint-2
estimated_points: 34
priority: CRITICAL
---

## Business Goal

Integrate tree-sitter for AST parsing, enabling syntax-aware code analysis that eliminates the 20-30% false positive rate of grep-based approaches.

## Success Metrics

- ✅ Parse JavaScript, TypeScript, Python, C#, Go, Rust files successfully
- ✅ 5 grammars bundled in binary (work offline)
- ✅ Auto-install downloads and compiles missing grammars
- ✅ Parse 10,000 line file in <700ms
- ✅ Gracefully handle syntax errors (partial parsing)

## Features

### Feature 1: Tree-sitter FFI Integration
- Integrate tree-sitter Rust crate
- Parse source code to AST
- Handle tree-sitter C FFI (unsafe blocks)
- AST traversal and node inspection

### Feature 2: Language Detection
- Detect language from file extension (.js, .py, .cs, .go, .rs)
- Handle ambiguous extensions (.h → C/C++)
- Map extensions to tree-sitter grammars
- Override via `--language` CLI flag

### Feature 3: Grammar Bundling
- Bundle 5 grammars at compile time
- Embed grammar binaries in executable
- Use `include_dir!` macro for embedding
- Test bundled grammars work offline

**Bundled Languages:**
1. JavaScript/TypeScript
2. Python
3. C#
4. Go
5. Rust

### Feature 4: Grammar Auto-Install System
- Download grammars from tree-sitter GitHub organization
- Detect gcc/clang availability
- Compile grammar using tree-sitter CLI
- Cache compiled grammars in `~/.treelint/grammars/`
- Show progress: "[1/3] Downloading...", "[2/3] Compiling...", "[3/3] Caching..."

### Feature 5: Smart Context Detection
- Detect CI environment (CI=true env var)
- Detect TTY availability (interactive terminal)
- Auto-install in local dev (with progress)
- Fail-fast in CI (don't auto-install)
- Override via `--auto-install` / `--no-auto-install` flags

### Feature 6: Grammar Management Commands
- `treelint grammar list` - List available grammars
- `treelint grammar install <language>` - Manual grammar installation
- `treelint grammar cache` - Show cached grammar locations

## Requirements Addressed

- **FR-1:** AST Parsing (CRITICAL)
- **FR-4:** Grammar Management (HIGH)
- **FR-6:** Language Detection (MEDIUM)
- **NFR-1:** Performance (Parse <700ms)
- **NFR-4:** Error Handling (Context-aware auto-install)
- **NFR-5:** Availability (Offline with bundled grammars)

## Non-Functional Requirements

- **Performance:** Parse 10,000 line file <700ms
- **Memory:** <500MB for single parse operation
- **Binary Size:** <30MB with 5 bundled grammars
- **Error Handling:** Helpful messages if gcc/clang missing

## Architecture Considerations

**Module Structure:**
```
src/
├── parser/
│   ├── mod.rs           # Parser interface
│   ├── tree_sitter.rs   # tree-sitter integration
│   └── languages.rs     # Language detection
├── grammars/
│   ├── mod.rs           # Grammar manager
│   ├── bundled.rs       # Bundled grammars
│   ├── downloader.rs    # Grammar downloader
│   └── compiler.rs      # Grammar compiler
└── cache/
    └── mod.rs           # Cache management
```

**Key Design Decisions:**
- **tree-sitter Rust Crate:** Use official bindings (avoid manual FFI)
- **Grammar Bundling:** Use `include_dir!` macro to embed grammars at compile time
- **Cache Location:** `~/.treelint/grammars/` (XDG-compliant on Linux)
- **Compiler Detection:** Check for gcc, clang, cl.exe (MSVC) in PATH

**Tree-sitter Initialization:**
```rust
use tree_sitter::{Parser, Language};

pub struct CodeParser {
    parser: Parser,
    language: Language,
}

impl CodeParser {
    pub fn new(language: Language) -> Result<Self> {
        let mut parser = Parser::new();
        parser.set_language(language)?;
        Ok(CodeParser { parser, language })
    }

    pub fn parse_file(&mut self, path: &Path) -> Result<Tree> {
        let source = std::fs::read_to_string(path)?;
        self.parser.parse(&source, None)
            .ok_or_else(|| anyhow!("Failed to parse {}", path.display()))
    }
}
```

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Tree-sitter FFI complexity (unsafe code) | Medium | Use official Rust bindings, avoid manual unsafe |
| Grammar compilation fails (missing gcc) | Medium | Bundled grammars cover 90%, clear error messages |
| Cross-language AST differences | High | Test each bundled language separately, document quirks |
| Binary size bloat (bundled grammars) | Low | 5 grammars = ~20MB (acceptable for developer tool) |

## Assumptions

- Tree-sitter Rust crate is stable and maintained
- Tree-sitter grammars are available on GitHub (tree-sitter org)
- User machines have internet for auto-install (or use bundled grammars)
- gcc/clang available on most dev machines (or bundled grammars sufficient)

## Dependencies

**Crates:**
- `tree-sitter = "0.20"`
- `tree-sitter-javascript = "0.20"`
- `tree-sitter-typescript = "0.20"`
- `tree-sitter-python = "0.20"`
- `tree-sitter-c-sharp = "0.20"`
- `tree-sitter-go = "0.20"`
- `tree-sitter-rust = "0.20"`
- `include_dir = "0.7"` (embed grammars)
- `dirs = "5.0"` (XDG cache directory)
- `reqwest = { version = "0.11", features = ["blocking"] }` (download grammars)
- `which = "5.0"` (detect gcc/clang)

**External:**
- gcc or clang (for compiling downloaded grammars)

## Testing Strategy

**Unit Tests:**
- Language detection from extensions
- Grammar manager (bundled vs downloaded)
- Cache operations (read, write, invalidate)

**Integration Tests:**
```rust
#[test]
fn test_parse_javascript() {
    let parser = CodeParser::new(tree_sitter_javascript::language())?;
    let tree = parser.parse_file("test-fixtures/sample.js")?;
    assert!(tree.root_node().child_count() > 0);
}
```

**Test Fixtures:**
- Sample files for each bundled language
- Valid syntax
- Syntax errors (test graceful handling)

## Next Steps

After completing this epic:
1. Proceed to EPIC-003 (Query Pattern Matching) - parse trees ready for queries
2. Integrate with EPIC-004 (Query Library) - test patterns against parsed ASTs
3. EPIC-006 (Performance Optimization) builds on parsing infrastructure

## Related Epics

- **EPIC-001:** Core CLI Foundation (dependency - CLI framework must exist)
- **EPIC-003:** Query Pattern Matching (consumes parsed ASTs)
- **EPIC-004:** Query Library (needs parsed ASTs for pattern execution)
- **EPIC-006:** Performance Optimization (optimizes parsing performance)

## Stories

- [STORY-006] Integrate Tree-sitter FFI for AST Parsing - Dev Complete (8 points)
- [STORY-007] Implement Grammar Bundling System - Backlog (8 points)
- [STORY-008] Implement Grammar Auto-Install System - Backlog (13 points)
- [STORY-009] Implement Smart Context Detection for Auto-Install Behavior - Backlog (5 points)
- [STORY-010] Implement Grammar Management Commands - Backlog (8 points)

**Total: 42 points**

**Progress:** 8/42 points complete (19%)

---

**Epic Owner:** Solo Developer
**Target Completion:** End of Sprint 2 (Week 6)
**Learning Resources:**
- Tree-sitter documentation: https://tree-sitter.github.io/tree-sitter/
- Tree-sitter Rust bindings: https://docs.rs/tree-sitter/
- Unsafe Rust: "The Rustonomicon" (Chapter 1-3)
