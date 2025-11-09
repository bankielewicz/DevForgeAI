# TreeLint Requirements Specification

**Project:** TreeLint - Syntax-Aware Code Analysis CLI Tool
**Version:** 1.0
**Date:** 2025-11-01
**Author:** DevForgeAI Ideation
**Status:** Requirements Complete - Ready for Architecture Phase

---

## Executive Summary

TreeLint is a high-performance CLI tool that provides syntax-aware code analysis using tree-sitter Abstract Syntax Tree (AST) parsing. It addresses DevForgeAI's current limitation of text-based code analysis (grep/regex) which has 20-30% false positive rates due to matching patterns in comments, strings, and unrelated contexts.

**Business Value:**
- **Accuracy Improvement:** <5% false positive rate (vs 20-30% current)
- **Performance:** Parse + run 4 queries in <2 seconds (10K line file)
- **Multi-Language Support:** 40+ languages via tree-sitter grammars
- **Developer Productivity:** Reduce manual code review time by 70%
- **DevForgeAI Integration:** Drop-in replacement for grep-based validation

**Primary Users:**
1. DevForgeAI framework subagents (context-validator, security-auditor, code-reviewer, test-automator, refactoring-specialist)
2. Developers using spec-driven workflows
3. CI/CD pipelines requiring structural code validation

---

## Problem Statement

### Current State
DevForgeAI currently uses grep and regex for code analysis in QA validation workflows. This approach:
- **High False Positives:** 20-30% false positive rate (matches in comments, strings, unrelated code)
- **Language-Agnostic Limitations:** Cannot distinguish between code structure and text
- **Maintenance Burden:** Pattern updates require testing across multiple false-positive scenarios
- **Developer Friction:** Manual verification of flagged violations wastes time

### Desired State
TreeLint provides syntax-aware analysis that:
- **<5% False Positives:** AST-based detection understands code structure
- **Multi-Language Support:** Single tool for JavaScript, Python, C#, Go, Rust, Java, etc.
- **Performance:** <2 seconds for parse + 4 queries on 10K line file
- **Automation-Friendly:** JSON output for CI/CD integration
- **Zero Configuration:** Works immediately with bundled grammars

---

## Project Context

### Project Type
**Greenfield** - New standalone CLI tool

### Repository Strategy
**Hybrid** - Standalone GitHub repository (github.com/user/treelint) with smart bundling in DevForgeAI
- Independent development and versioning
- Broader adoption potential beyond DevForgeAI
- DevForgeAI provides download script (no binaries committed to git)

### Timeline
**10-12 weeks** for v1.0 (CLI with 12 core patterns)
- Includes comprehensive Rust learning (beginner level)
- Thorough testing across 5 bundled languages
- Cross-platform build and documentation

### Complexity Assessment
**Score:** 18/60
**Tier:** Tier 2 - Moderate Application
**Primary Drivers:** High-performance requirements, FFI complexity, beginner Rust learning curve

---

## User Roles & Personas

### Persona 1: DevForgeAI Subagent (Primary)
- **Role:** Automated QA validator
- **Goal:** Detect anti-patterns, architecture violations, security issues with high accuracy
- **Environment:** Invoked via Bash subprocess from Python scripts
- **Constraints:** Must complete in <5 seconds per validation, JSON output required

### Persona 2: Developer (Secondary)
- **Role:** Human code reviewer
- **Goal:** Manually analyze code for violations during development
- **Environment:** Terminal, local machine
- **Constraints:** Needs clear error messages, helpful --help text, human-readable output option

### Persona 3: CI/CD Pipeline (Secondary)
- **Role:** Automated gatekeeper
- **Goal:** Block merges with critical violations, fail fast
- **Environment:** GitHub Actions, Jenkins, etc.
- **Constraints:** Must work in minimal containers, no interactive prompts, exit codes for pass/fail

---

## Functional Requirements

### FR-1: AST Parsing
**Priority:** CRITICAL
**Description:** Parse source code into Abstract Syntax Trees using tree-sitter

**Acceptance Criteria:**
- Parse files in JavaScript, TypeScript, Python, C#, Go, Rust (bundled grammars)
- Support 40+ languages via auto-install
- Handle syntax errors gracefully (partial parsing)
- Cache parsed trees for re-use
- Incremental parsing for modified files

**Out of Scope (v1.0):**
- AST visualization
- Interactive tree exploration
- Custom grammar generation

---

### FR-2: Query Pattern Matching
**Priority:** CRITICAL
**Description:** Execute S-expression queries against AST to detect code patterns

**Acceptance Criteria:**
- Parse and execute tree-sitter query syntax (.scm files)
- Support capture groups (`@variable.name`)
- Support predicates (`#match?`, `#eq?`, `#not-eq?`)
- Support negation and alternation
- Return match locations (file, line, column, code snippet)

**Query Example:**
```scheme
; Detect God Objects (classes >500 lines)
(class_declaration
  name: (identifier) @class.name
  body: (class_body) @body
  (#count-lines @body >500))
```

**Out of Scope (v1.0):**
- Query builder GUI
- Query optimization hints
- Query composition operators

---

### FR-3: Pattern Library
**Priority:** CRITICAL
**Description:** Pre-built query patterns for common anti-patterns, architecture violations, security issues, and testing gaps

**v1.0 Scope: 12 Core Patterns**

**Anti-Patterns (4):**
1. **God Objects** - Classes >500 lines
2. **Direct Instantiation** - `new Service()` in business logic (violates DI)
3. **Magic Numbers** - Hardcoded numeric constants
4. **Long Functions** - Functions >50 lines

**Architecture (4):**
1. **Layer Boundaries** - Domain layer importing Infrastructure
2. **Dependency Injection** - Constructor injection validation
3. **Circular Dependencies** - Module import cycles
4. **Clean Architecture** - Dependency rule enforcement

**Security (3):**
1. **SQL Injection** - String concatenation in SQL queries
2. **Hardcoded Secrets** - API keys, passwords in code
3. **Weak Crypto** - MD5, SHA1 usage

**Testing (1):**
1. **Public Functions** - All public/exported functions (for coverage gap analysis)

**Acceptance Criteria:**
- Each pattern has .scm query file
- Tested against all 5 bundled languages
- Documentation with examples and rationale
- Categorized (anti-patterns/, architecture/, security/, testing/)
- Embedded in binary (no external files required)

**Future Scope (v1.1+):**
- 21 additional patterns (33 total)
- User-contributed patterns
- Pattern customization

---

### FR-4: Grammar Management
**Priority:** HIGH
**Description:** Bundle common grammars and auto-install others on demand

**Bundled Grammars (Ship in Binary):**
1. JavaScript/TypeScript
2. Python
3. C#
4. Go
5. Rust

**Rationale:** These 5 languages cover 90%+ of DevForgeAI projects

**Auto-Install (On-Demand):**
- Download from tree-sitter GitHub organization
- Compile locally using gcc/clang
- Cache in `~/.treelint/grammars/`
- Smart context detection (auto-install in local dev, fail-fast in CI)

**Acceptance Criteria:**
- Bundled grammars work offline
- Auto-install shows progress: "[1/3] Downloading...", "[2/3] Compiling...", "[3/3] Caching..."
- Fail gracefully if gcc/clang missing (helpful error with installation instructions)
- Manual install command: `treelint grammar install <language>`
- List available grammars: `treelint grammar list`

---

### FR-5: CLI Interface
**Priority:** CRITICAL
**Description:** Command-line interface for invoking TreeLint

**Commands:**

```bash
# Analyze with pattern
treelint analyze --pattern=<name> <path>
treelint analyze --pattern=anti-patterns src/

# Run custom query
treelint query <query-file.scm> <path>
treelint query custom-god-objects.scm src/

# Grammar management
treelint grammar list
treelint grammar install <language>

# Version info
treelint --version
```

**Flags:**
- `--format=json|text` - Output format (default: json)
- `--auto-install` - Force auto-install missing grammars
- `--no-auto-install` - Fail fast if grammar missing
- `--verbose` - Show detailed output

**Acceptance Criteria:**
- Clear `--help` text
- JSON output by default (machine-readable)
- Text output option for human consumption
- Exit codes: 0 (success), 1 (violations found), 2 (error)
- Descriptive error messages with actionable suggestions

---

### FR-6: Language Detection
**Priority:** MEDIUM
**Description:** Automatically detect programming language from file extensions

**Acceptance Criteria:**
- Detect language from extension (.js, .py, .cs, .go, .rs)
- Handle ambiguous extensions (.h → C/C++)
- Override via `--language` flag
- Error if language unsupported or grammar missing

---

### FR-7: Configuration File (Optional)
**Priority:** LOW
**Description:** Minimal read-only config file for per-project settings

**Config Schema (.treelint.toml):**
```toml
[grammars]
auto_install = true
cache_dir = "~/.treelint/grammars"

[output]
format = "json"
verbose = false
```

**Acceptance Criteria:**
- Config file is OPTIONAL (sensible defaults without it)
- CLI flags override config settings
- Simple schema (4 settings only)
- Per-project config (commit .treelint.toml to git)

---

## Non-Functional Requirements

### NFR-1: Performance
**Priority:** CRITICAL
**Target:** Parse + 4 queries in <2 seconds (10,000 line file)

**Breakdown:**
- Parse to AST: <700ms
- Execute 4 queries: <1,000ms total (<250ms each)
- Overhead (JSON formatting): <300ms

**Optimization Strategies:**
- Pre-compile queries (lazy_static)
- Parallel query execution (rayon - 4 queries on 4 cores)
- Incremental parsing (tree-sitter native feature)

**Acceptance Criteria:**
- Benchmark suite in `benches/`
- Performance regression tests in CI
- Performance target met on reference hardware (4-core CPU, 8GB RAM)

---

### NFR-2: Cross-Platform Support
**Priority:** HIGH
**Platforms:**
- ✅ Linux x86_64 (Ubuntu 20.04+, Debian 11+)
- ✅ macOS x86_64 (Intel)
- ✅ macOS ARM64 (Apple Silicon)
- ✅ Windows x86_64 (Windows 10+)

**Acceptance Criteria:**
- Single binary per platform (no runtime dependencies)
- Binary size <30MB (includes 5 bundled grammars)
- GitHub Actions CI tests all platforms
- Cross-compilation via `cross-rs`

---

### NFR-3: Accuracy
**Priority:** CRITICAL
**Target:** <5% false positive rate

**Definition:** False positive = violation flagged but not an actual issue

**Measurement:**
- Test against DevForgeAI codebase (known violations + known clean code)
- Manual review of flagged violations
- Compare against grep-based approach (baseline: 20-30% FPR)

**Acceptance Criteria:**
- <5% FPR on test suite (100+ test cases)
- 100% detection of actual violations (no false negatives)
- Documentation explains pattern detection logic

---

### NFR-4: Error Handling
**Priority:** HIGH
**Strategy:** Context-aware auto-install with smart detection

**Behavior:**

**Local Development (Auto-Install):**
- Detect missing grammar
- Auto-install silently with progress feedback
- Continue analysis automatically
- Cache for future use

**CI/CD (Fail-Fast):**
- Fail immediately if grammar missing
- Exit code 1 with clear error message
- Assume grammars should be pre-installed/cached

**Override Options:**
- CLI flag: `--auto-install` / `--no-auto-install`
- ENV var: `CODELENS_AUTO_INSTALL=true/false`
- Config file: `auto_install = true/false`

**Error Messages:**
- Actionable (tell user what to do)
- Include platform-specific instructions
- Reference documentation

---

### NFR-5: Availability
**Priority:** MEDIUM
**Target:** Works offline with bundled grammars

**Acceptance Criteria:**
- Analyze JavaScript, TypeScript, Python, C#, Go, Rust without internet
- Auto-install requires internet (download grammars)
- Cached grammars work offline after first download

---

### NFR-6: Maintainability
**Priority:** MEDIUM
**Requirements:**
- Clear module separation (CLI, core library, patterns, grammars)
- Comprehensive documentation (inline comments, README, user guide)
- Automated tests (unit, integration, performance)
- CI/CD pipeline (test, build, release)

**Acceptance Criteria:**
- Code documentation coverage >80%
- Test coverage >70% (unit tests)
- README with installation, usage, contribution guide
- Architecture decision records (ADRs) for major decisions

---

## Data Model

### Entity 1: Pattern
```rust
pub struct Pattern {
    pub id: String,           // "god-objects"
    pub name: String,         // "God Objects"
    pub category: PatternCategory, // AntiPattern, Architecture, Security, Testing
    pub query: String,        // S-expression query
    pub description: String,  // "Classes with >500 lines"
    pub severity: Severity,   // CRITICAL, HIGH, MEDIUM, LOW
    pub languages: Vec<String>, // ["javascript", "python", "csharp"]
}
```

### Entity 2: Violation
```rust
pub struct Violation {
    pub file: PathBuf,
    pub line: usize,
    pub column: usize,
    pub pattern_id: String,
    pub message: String,
    pub code_snippet: String,
    pub severity: Severity,
}
```

### Entity 3: Grammar
```rust
pub struct Grammar {
    pub language: String,     // "python"
    pub version: String,      // "0.21.0"
    pub source: GrammarSource, // Bundled, Downloaded, Custom
    pub extensions: Vec<String>, // [".py"]
    pub installed: bool,
}
```

---

## Integration Requirements

### INT-1: DevForgeAI Subprocess Integration
**Priority:** CRITICAL
**Method:** Bash subprocess invocation from Python scripts

**Example:**
```python
import subprocess
import json

result = subprocess.run(
    ['treelint', 'analyze', '--pattern=layer-boundaries', '--format=json', 'src/'],
    capture_output=True,
    text=True,
    check=True
)

violations = json.loads(result.stdout)
```

**Acceptance Criteria:**
- JSON output parseable by Python's `json.loads()`
- Exit codes distinguish success/violations/errors
- stderr contains helpful debug information if errors occur

---

### INT-2: CI/CD Integration
**Priority:** HIGH
**Method:** Shell commands in CI/CD pipelines

**Example (GitHub Actions):**
```yaml
- name: Install TreeLint
  run: cargo install treelint

- name: Run Security Checks
  run: treelint analyze --pattern=security src/
  env:
    CODELENS_AUTO_INSTALL: false  # Fail if grammar missing
```

**Acceptance Criteria:**
- Works in minimal Docker containers
- No interactive prompts (fully automated)
- Exit code failures block CI/CD pipeline

---

## Success Criteria

TreeLint v1.0 succeeds when:

- [ ] **Performance:** Parse + 4 queries <2 seconds (10K line file)
- [ ] **Accuracy:** <5% false positive rate on test suite
- [ ] **Multi-Language:** 5 bundled grammars work offline
- [ ] **Auto-Install:** Downloads and compiles grammars on demand
- [ ] **Pattern Library:** 12 core patterns implemented and tested
- [ ] **CLI:** All 5 commands work with clear --help text
- [ ] **Cross-Platform:** Binaries for Linux, macOS (Intel + ARM), Windows
- [ ] **DevForgeAI Integration:** context-validator uses TreeLint successfully
- [ ] **Documentation:** README, user guide, pattern reference complete
- [ ] **Open Source:** Published to GitHub, crates.io

---

## Out of Scope (v1.0)

**Deferred to v1.1:**
- PyO3 Python library (direct import, no subprocess)
- Extended pattern library (20 more patterns)
- Markdown report generation
- Pattern customization via config

**Deferred to v1.2:**
- gRPC service mode (AST caching, incremental parsing)
- Real-time code analysis (watch mode)
- Multi-file analysis (cross-file dependencies)

**Never Planned:**
- GUI or web UI
- Language Server Protocol (LSP) implementation
- Custom grammar generation

---

## Risks & Assumptions

### Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Rust learning takes longer than expected | Medium | High | Allocated 10-12 weeks (thorough timeline), focus on practical examples |
| Cross-language query patterns don't work uniformly | Medium | Medium | Test early (Week 3), document language-specific patterns |
| Performance targets not met | Low | Medium | Benchmark early (Week 6), optimize if needed |
| Grammar auto-install fails on user machines | Medium | Low | Bundled grammars cover 90%, clear error messages |

### Assumptions

1. **Tree-sitter query language sufficiency:** S-expression queries can express all 12 patterns
   - **Validation:** Research existing queries in tree-sitter-queries repo

2. **Performance achievable:** Rust + tree-sitter can meet <2s target
   - **Validation:** Early benchmark (Week 6) with initial pattern

3. **User machines have gcc/clang:** Most dev environments have build tools
   - **Validation:** Bundled grammars cover 90%, auto-install handles edge cases

4. **Pattern accuracy:** AST-based detection reduces false positives to <5%
   - **Validation:** Test against DevForgeAI codebase with known violations

---

## Next Steps

1. **Architecture Phase:** Invoke `devforgeai-architecture` skill to:
   - Create 6 context files (tech-stack.md, source-tree.md, dependencies.md, coding-standards.md, architecture-constraints.md, anti-patterns.md)
   - Document technology decisions (Rust, tree-sitter, clap, serde, etc.)
   - Create ADR for hybrid grammar management strategy

2. **Orchestration Phase:** Invoke `devforgeai-orchestration` skill to:
   - Create Sprint 1 plan
   - Generate user stories from epics
   - Set up story workflow

3. **Development Phase:** Use `/dev` command to implement stories with TDD

---

**Requirements complete. Ready for architecture phase.**
