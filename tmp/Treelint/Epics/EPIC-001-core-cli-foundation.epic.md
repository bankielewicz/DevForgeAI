# EPIC-001: Core CLI Foundation

---
id: EPIC-001
title: Core CLI Foundation
status: Backlog
created: 2025-11-01
target_sprint: Sprint-1
estimated_points: 21
priority: CRITICAL
---

## Business Goal

Establish the foundational Rust project structure, CLI argument parsing, and core infrastructure that all other epics will build upon.

## Success Metrics

- ✅ Rust project compiles without errors
- ✅ CLI accepts and parses all required arguments via clap
- ✅ File/directory traversal works recursively
- ✅ JSON output format matches DevForgeAI expectations
- ✅ Error handling framework provides helpful messages
- ✅ `treelint --version` displays correct version info

## Features

### Feature 1: Project Setup
- Initialize Cargo workspace
- Configure dependencies (clap, serde, anyhow)
- Set up CI/CD pipeline (GitHub Actions)
- Configure release workflow

### Feature 2: CLI Argument Parsing
- Implement main commands: `analyze`, `query`, `grammar`
- Parse flags: `--pattern`, `--format`, `--auto-install`, `--verbose`
- Implement `--help` text for all commands
- Implement `--version` flag

### Feature 3: File System Operations
- Recursive directory traversal
- File filtering by extension
- Path normalization (cross-platform)
- Error handling for missing/invalid paths

### Feature 4: Output Formatting
- JSON serialization (serde_json)
- Text output formatter (human-readable)
- Exit code handling (0=success, 1=violations, 2=error)
- Stderr for errors, stdout for results

### Feature 5: Error Handling Framework
- Custom error types
- Anyhow error chaining
- Helpful error messages with suggestions
- Graceful degradation

## Requirements Addressed

- **FR-5:** CLI Interface (CRITICAL)
- **NFR-6:** Maintainability (MEDIUM)

## Non-Functional Requirements

- **Performance:** N/A (foundational, no performance bottleneck)
- **Cross-Platform:** Must work on Linux, macOS, Windows
- **Code Quality:** Clear module separation, >80% documentation coverage

## Architecture Considerations

**Module Structure:**
```
src/
├── main.rs          # CLI entry point, argument parsing
├── lib.rs           # Public API for library usage
├── cli/             # CLI-specific code
│   ├── commands.rs  # Command implementations
│   ├── args.rs      # Argument parsing (clap)
│   └── output.rs    # Output formatting
├── fs/              # File system operations
│   ├── traversal.rs # Directory walking
│   └── filters.rs   # File filtering
└── error.rs         # Error types and handling
```

**Key Design Decisions:**
- **Clap v4** for CLI parsing (derive macros for ergonomics)
- **Serde** for JSON serialization
- **Anyhow** for error handling (context propagation)
- Separate CLI layer from core library (enables future PyO3 bindings)

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Beginner Rust confusion with ownership | Medium | Start with simple examples, allocate 2 weeks for learning |
| Cross-platform path handling issues | Low | Use std::path::PathBuf, test on all platforms |
| Clap API complexity | Low | Use derive macros, follow official examples |

## Assumptions

- Rust toolchain (1.75+) installed on development machine
- Familiarity with command-line tools (argument parsing, exit codes)
- JSON output schema can evolve (v1.0 MVP, refine later)

## Dependencies

**Crates:**
- `clap = { version = "4.4", features = ["derive"] }`
- `serde = { version = "1.0", features = ["derive"] }`
- `serde_json = "1.0"`
- `anyhow = "1.0"`
- `walkdir = "2.4"` (directory traversal)

**Development:**
- Rust 1.75+ (stable)
- Cargo

## Next Steps

After completing this epic:
1. Proceed to EPIC-002 (Tree-sitter AST Parsing) - foundation in place
2. Integrate with EPIC-003 (Query Pattern Matching) - CLI can invoke analyzer
3. EPIC-005 (Configuration & UX) builds on CLI framework

## Related Epics

- **EPIC-002:** Tree-sitter AST Parsing (depends on this foundation)
- **EPIC-003:** Query Pattern Matching (depends on this foundation)
- **EPIC-005:** Configuration & UX (extends CLI interface)

## Stories

- [STORY-001] Setup Cargo Workspace with Dependencies and CI/CD - Backlog (3 points)
- [STORY-002] Implement CLI Argument Parsing with clap Derive Macros - Backlog (8 points)
- [STORY-003] Add File System Traversal with walkdir - Backlog (13 points)
- [STORY-004] Implement JSON Output Formatting - Backlog (8 points)
- [STORY-005] Create Error Handling Framework with anyhow - Backlog (8 points)

**Total: 40 points (Epic estimated: 21 points)**

---

**Epic Owner:** Solo Developer
**Target Completion:** End of Sprint 1 (Week 3)
