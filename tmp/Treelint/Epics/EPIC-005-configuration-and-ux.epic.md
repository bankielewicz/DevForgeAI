# EPIC-005: Configuration & UX

---
id: EPIC-005
title: Configuration & UX
status: Backlog
created: 2025-11-01
target_sprint: Sprint-3
estimated_points: 13
priority: HIGH
---

## Business Goal

Provide excellent user experience through clear configuration options, helpful error messages, progress feedback, and comprehensive documentation.

## Success Metrics

- ✅ .treelint.toml config file support (optional, sensible defaults)
- ✅ Clear progress feedback for grammar installation
- ✅ Helpful error messages with actionable suggestions
- ✅ Comprehensive --help text for all commands
- ✅ README and user guide complete
- ✅ 90% of users report "easy to use" (post-v1.0 survey)

## Features

### Feature 1: Configuration File Support

**Purpose:** Allow per-project customization without CLI flags

**Config File:** `.treelint.toml` (optional, placed in project root)

**Schema (Minimal for v1.0):**
```toml
[grammars]
# Auto-install behavior
auto_install = true              # Default: true
cache_dir = "~/.treelint/grammars"  # Default: XDG cache

[output]
# Output formatting
format = "json"                  # Options: json, text
verbose = false                  # Default: false
```

**Features:**
- Config file is **OPTIONAL** (TreeLint works without it)
- Sensible defaults if no config present
- CLI flags override config settings (priority: CLI > Config > Defaults)
- Per-project config (committed to git for team consistency)

**Implementation:**
```rust
// src/config.rs

use serde::Deserialize;
use std::path::Path;

#[derive(Deserialize, Default)]
pub struct Config {
    #[serde(default)]
    pub grammars: GrammarConfig,

    #[serde(default)]
    pub output: OutputConfig,
}

#[derive(Deserialize)]
pub struct GrammarConfig {
    #[serde(default = "default_auto_install")]
    pub auto_install: bool,

    #[serde(default = "default_cache_dir")]
    pub cache_dir: String,
}

fn default_auto_install() -> bool { true }
fn default_cache_dir() -> String {
    dirs::cache_dir()
        .unwrap()
        .join("treelint")
        .join("grammars")
        .display()
        .to_string()
}

impl Config {
    pub fn load() -> Result<Self> {
        let config_path = Path::new(".treelint.toml");

        if !config_path.exists() {
            // No config file, use defaults
            return Ok(Config::default());
        }

        let config_str = fs::read_to_string(config_path)
            .context("Failed to read .treelint.toml")?;

        toml::from_str(&config_str)
            .context("Failed to parse .treelint.toml")
    }
}
```

**Error Handling:**
- If .treelint.toml has syntax errors → Show helpful error with line number
- If unknown settings → Warning (ignore), not error (forward compatibility)

---

### Feature 2: Progress Feedback

**Purpose:** Keep users informed during long operations (grammar installation)

**Grammar Installation Progress:**
```
Kotlin grammar not found. Auto-installing...
[1/3] Downloading tree-sitter-kotlin from GitHub...
      ████████████████████ 100% (1.2 MB)
[2/3] Compiling grammar (requires gcc/clang)...
      ⣾ Compiling... (30s remaining)
[3/3] Caching in ~/.cache/treelint/grammars/...
✓ Grammar installed successfully

Analyzing src/Main.kt...
```

**Implementation:**
```rust
// src/grammars/installer.rs

use indicatif::{ProgressBar, ProgressStyle};

pub fn install_grammar(language: &str) -> Result<Grammar> {
    println!("{} grammar not found. Auto-installing...", language);

    // Step 1: Download
    println!("[1/3] Downloading tree-sitter-{}...", language);
    let pb = ProgressBar::new(0);
    pb.set_style(ProgressStyle::default_bar()
        .template("{bar:40} {percent}% ({bytes}/{total_bytes})")?);

    download_with_progress(url, &pb)?;
    pb.finish_and_clear();

    // Step 2: Compile
    println!("[2/3] Compiling grammar (requires gcc/clang)...");
    let spinner = ProgressBar::new_spinner();
    spinner.set_message("Compiling...");

    compile_grammar(language, &spinner)?;
    spinner.finish_and_clear();

    // Step 3: Cache
    println!("[3/3] Caching in {:?}...", cache_dir);
    cache_grammar(language)?;

    println!("✓ Grammar installed successfully\n");

    load_from_cache(language)
}
```

**Dependencies:**
- `indicatif = "0.17"` (progress bars) - **Add to dependencies.md if approved**

**Alternative (No New Dependency):**
```rust
// Simple progress without library
println!("[1/3] Downloading tree-sitter-{}...", language);
download(url)?;
println!("✓ Downloaded");

println!("[2/3] Compiling grammar...");
compile(language)?;
println!("✓ Compiled");

println!("[3/3] Caching...");
cache(language)?;
println!("✓ Installed successfully");
```

---

### Feature 3: Helpful Error Messages

**Purpose:** Guide users to solutions when errors occur

**Principle:** Every error message must be actionable

**Error Message Template:**
```
ERROR: [What went wrong]

Reason: [Why it failed]

Solutions:
  1. [Most common solution]
  2. [Alternative solution]
  3. [Workaround]

Documentation: [Link to relevant docs]
```

**Example 1: Grammar Not Found**
```
ERROR: Kotlin grammar not found

Reason: Kotlin is not bundled in TreeLint

Bundled languages (work offline):
  - javascript, typescript, python, csharp, go, rust

Solutions:
  1. Install Kotlin grammar:
     treelint grammar install kotlin
     (Requires gcc or clang)

  2. Install build tools first (if needed):
     Ubuntu/Debian: apt-get install build-essential
     macOS: xcode-select --install
     Windows: Install Visual Studio Build Tools

  3. Use bundled languages only

Documentation: https://github.com/bankielewicz/TreeLint#grammar-management

Exit code: 1
```

**Example 2: Build Tools Missing**
```
ERROR: Failed to compile Kotlin grammar

Reason: gcc or clang not found (required for compilation)

Your system needs a C compiler to compile tree-sitter grammars.

Install build tools:
  Ubuntu/Debian:
    sudo apt-get install build-essential

  macOS:
    xcode-select --install

  Windows:
    Install Visual Studio Build Tools
    https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022

After installation, retry:
  treelint grammar install kotlin

Or use bundled languages only:
  javascript, typescript, python, csharp, go, rust

Exit code: 2
```

**Example 3: Invalid Pattern Name**
```
ERROR: Pattern 'god-objets' not found (typo?)

Available patterns:
  Anti-Patterns:
    - god-objects (classes >500 lines)
    - direct-instantiation (DI violations)
    - magic-numbers (hardcoded constants)
    - long-functions (functions >50 lines)

  Architecture:
    - layer-boundaries (clean architecture violations)
    - dependency-injection (DI validation)
    - circular-dependencies (import cycles)
    - clean-architecture (dependency rules)

  Security:
    - sql-injection (string concatenation in SQL)
    - hardcoded-secrets (API keys in code)
    - weak-crypto (MD5, SHA1 usage)

  Testing:
    - public-functions (coverage gap analysis)

Did you mean: god-objects?

Usage:
  treelint analyze --pattern=god-objects src/

Exit code: 2
```

---

### Feature 4: Comprehensive --help Text

**Purpose:** Self-documenting CLI (users don't need external docs for basic usage)

**Top-Level Help:**
```bash
$ treelint --help

TreeLint - Syntax-aware code analysis using tree-sitter

USAGE:
    treelint [OPTIONS] <COMMAND>

COMMANDS:
    analyze    Run pattern analysis on source code
    query      Execute custom tree-sitter query
    grammar    Manage language grammars
    help       Print this message or help for a subcommand

OPTIONS:
    -h, --help       Print help information
    -V, --version    Print version information
    --verbose        Show detailed output

EXAMPLES:
    # Analyze code for anti-patterns
    treelint analyze --pattern=anti-patterns src/

    # Check for security issues
    treelint analyze --pattern=security src/

    # Run custom query
    treelint query custom-pattern.scm src/

    # List available grammars
    treelint grammar list

For more information, visit: https://github.com/bankielewicz/TreeLint
```

**Analyze Command Help:**
```bash
$ treelint analyze --help

Run pattern analysis on source code

USAGE:
    treelint analyze [OPTIONS] --pattern <PATTERN> <PATH>

ARGUMENTS:
    <PATH>    Directory or file to analyze

OPTIONS:
    -p, --pattern <PATTERN>     Pattern or category to run
                                (e.g., anti-patterns, god-objects, security)

    -f, --format <FORMAT>       Output format [default: json]
                                [possible values: json, text]

    --auto-install              Force auto-install missing grammars
    --no-auto-install           Fail if grammar missing (don't auto-install)
    --verbose                   Show detailed output

EXAMPLES:
    # Run all anti-patterns
    treelint analyze --pattern=anti-patterns src/

    # Run specific pattern
    treelint analyze --pattern=god-objects src/

    # Output as text (human-readable)
    treelint analyze --pattern=security src/ --format=text

    # Disable auto-install (fail fast)
    treelint analyze --pattern=anti-patterns src/ --no-auto-install

AVAILABLE PATTERNS:
    Categories:
      anti-patterns, architecture, security, testing

    Individual:
      god-objects, direct-instantiation, magic-numbers, long-functions,
      layer-boundaries, dependency-injection, circular-dependencies,
      clean-architecture, sql-injection, hardcoded-secrets, weak-crypto,
      public-functions
```

---

### Feature 5: Documentation

#### 5.1 README.md

**Sections:**
1. **Introduction** - What is TreeLint, why use it
2. **Installation** - Binary download, cargo install, package managers
3. **Quick Start** - 5-minute tutorial
4. **Usage Guide** - All commands with examples
5. **Pattern Library** - List of 12 patterns with descriptions
6. **Configuration** - .treelint.toml reference
7. **DevForgeAI Integration** - How to integrate with DevForgeAI
8. **Contributing** - How to add patterns or fix bugs
9. **License** - MIT

#### 5.2 User Guide (docs/user-guide.md)

**Sections:**
1. **Getting Started** - Installation and first analysis
2. **Pattern Library Reference** - Detailed pattern documentation
3. **Grammar Management** - Bundled vs auto-install
4. **Configuration Reference** - .treelint.toml complete reference
5. **CI/CD Integration** - GitHub Actions, GitLab CI examples
6. **Troubleshooting** - Common errors and solutions

#### 5.3 Pattern Reference (docs/pattern-reference.md)

**For each of 12 patterns:**
- Description and rationale
- Severity level
- Supported languages
- Detection logic explanation
- Examples (✅ CORRECT vs ❌ FORBIDDEN)
- False positive scenarios (how to handle)

---

## Requirements Addressed

- **FR-7:** Configuration File (LOW priority)
- **NFR-6:** Maintainability (Documentation coverage >80%)

## Non-Functional Requirements

- **Usability:** Users can complete basic analysis in <5 minutes (no reading docs)
- **Documentation Coverage:** >80% of features documented
- **Error Messages:** 100% actionable (tell user what to do next)

## Architecture Considerations

**Config Module:**
```
src/
└── config/
    ├── mod.rs      # Config loading and defaults
    └── schema.rs   # Config struct definitions
```

**Config Loading Precedence:**
1. CLI flags (highest priority)
2. .treelint.toml (per-project)
3. Default values (lowest priority)

**Example Merging:**
```rust
pub fn load_config(cli_args: &Args) -> Result<Config> {
    // 1. Load from file (if exists)
    let mut config = Config::load_from_file()?;

    // 2. Override with CLI flags
    if let Some(format) = cli_args.format {
        config.output.format = format;
    }
    if cli_args.auto_install {
        config.grammars.auto_install = true;
    }
    if cli_args.no_auto_install {
        config.grammars.auto_install = false;
    }

    Ok(config)
}
```

---

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Config file adds complexity | Low | Keep schema minimal (4 settings only) |
| Poor error messages frustrate users | Medium | Test with real users, iterate on messages |
| Documentation becomes outdated | Medium | Document alongside code, not separately |

## Assumptions

- Users will commit .treelint.toml to git (team consistency)
- 4 config settings sufficient for v1.0 (can expand in v1.1)
- TOML format is familiar to Rust developers

## Dependencies

**Crates (Already in dependencies.md):**
- `toml = "0.8"` (config parsing)
- `serde = "1.0"` (deserialization)
- `dirs = "5.0"` (default cache directory)

**Optional (If Progress Bars Desired):**
- `indicatif = "0.17"` (progress bars and spinners)
  - **Requires approval and ADR** if added

**Development:**
- None additional

---

## Testing Strategy

**Config Loading Tests:**
```rust
#[cfg(test)]
mod tests {
    use super::*;
    use tempfile::tempdir;

    #[test]
    fn test_load_config_with_file() {
        let dir = tempdir().unwrap();
        let config_path = dir.path().join(".treelint.toml");

        fs::write(&config_path, r#"
            [grammars]
            auto_install = false

            [output]
            format = "text"
        "#).unwrap();

        env::set_current_dir(&dir).unwrap();
        let config = Config::load().unwrap();

        assert_eq!(config.grammars.auto_install, false);
        assert_eq!(config.output.format, "text");
    }

    #[test]
    fn test_default_config_without_file() {
        let dir = tempdir().unwrap();
        env::set_current_dir(&dir).unwrap();

        let config = Config::load().unwrap();

        // Should use defaults
        assert_eq!(config.grammars.auto_install, true);
        assert_eq!(config.output.format, "json");
    }

    #[test]
    fn test_cli_overrides_config() {
        // Config says auto_install = false
        let config = Config { /* ... */ };

        // CLI says --auto-install
        let cli_args = Args { auto_install: true, /* ... */ };

        let merged = merge_config(config, cli_args);

        // CLI wins
        assert_eq!(merged.grammars.auto_install, true);
    }
}
```

**Error Message Tests:**
```rust
#[test]
fn test_grammar_not_found_error_message() {
    let result = get_grammar("kotlin");

    assert!(result.is_err());
    let error_msg = result.unwrap_err().to_string();

    // Should contain helpful guidance
    assert!(error_msg.contains("Bundled languages"));
    assert!(error_msg.contains("treelint grammar install kotlin"));
    assert!(error_msg.contains("build-essential"));
}
```

---

## Documentation Checklist

**README.md:**
- [ ] Introduction with value proposition
- [ ] Installation instructions (all platforms)
- [ ] Quick start (5-minute tutorial)
- [ ] Usage examples (all commands)
- [ ] Pattern library reference (12 patterns)
- [ ] Configuration reference (.treelint.toml)
- [ ] DevForgeAI integration examples
- [ ] Contributing guide
- [ ] License (MIT)

**docs/user-guide.md:**
- [ ] Detailed usage guide
- [ ] Advanced patterns
- [ ] Troubleshooting section
- [ ] CI/CD integration examples
- [ ] Performance tuning tips

**docs/pattern-reference.md:**
- [ ] All 12 patterns documented
- [ ] Examples for each pattern
- [ ] False positive scenarios
- [ ] How to customize patterns

**Cargo.toml metadata:**
- [ ] description, keywords, categories
- [ ] repository, homepage URLs
- [ ] license

---

## UX Design Principles

### 1. Zero Configuration by Default

Users should be able to run TreeLint immediately:
```bash
# Download binary
curl -L .../treelint-linux -o treelint
chmod +x treelint

# Run immediately (no config needed)
./treelint analyze --pattern=anti-patterns src/
# Works ✓ (uses sensible defaults)
```

---

### 2. Progressive Disclosure

Don't overwhelm users with options:
- Basic usage: `treelint analyze --pattern=anti-patterns src/` (2 args)
- Advanced usage: Add flags as needed (--format, --verbose, --no-auto-install)
- Expert usage: Custom queries, config file

---

### 3. Fail with Guidance

Never fail without telling user what to do:
```
❌ BAD:
ERROR: Grammar not found

✅ GOOD:
ERROR: Kotlin grammar not found

Install with:
  treelint grammar install kotlin

Requires: gcc or clang
Install build tools: [platform-specific instructions]

Or use bundled languages:
  javascript, typescript, python, csharp, go, rust
```

---

### 4. Consistency

All commands follow same patterns:
- `treelint <command> [OPTIONS] <ARGS>`
- --help works for all commands
- Exit codes consistent (0=success, 1=violations, 2=error)
- JSON output format consistent

---

## DevForgeAI Integration Documentation

**In README.md, include DevForgeAI section:**

```markdown
## DevForgeAI Integration

TreeLint integrates with DevForgeAI subagents for automated code quality validation.

### Installation

```bash
# Download TreeLint binary (or cargo install treelint)
curl -L https://github.com/bankielewicz/TreeLint/releases/download/v1.0.0/treelint-linux \
  -o /usr/local/bin/treelint
chmod +x /usr/local/bin/treelint
```

### Usage in Subagents

```python
# .claude/agents/context-validator.md

import subprocess
import json

def validate_layer_boundaries(domain_path: str) -> list[dict]:
    result = subprocess.run(
        [
            'treelint', 'analyze',
            '--pattern=layer-boundaries',
            '--format=json',
            domain_path
        ],
        capture_output=True,
        text=True,
        check=True,
        timeout=30
    )

    violations = json.loads(result.stdout)
    return violations
```

### CI/CD Integration

```yaml
# .github/workflows/qa.yml
- name: Install TreeLint
  run: cargo install treelint

- name: Cache Grammars
  uses: actions/cache@v3
  with:
    path: ~/.cache/treelint/grammars
    key: treelint-grammars-${{ hashFiles('**/*.rs') }}

- name: Run Security Checks
  run: treelint analyze --pattern=security src/
  env:
    CODELENS_AUTO_INSTALL: false  # Fail if grammar missing (should be cached)
```

---

## Next Steps

After completing this epic:
1. User testing with DevForgeAI developers
2. Iterate on error messages based on feedback
3. Gather documentation improvement suggestions

## Related Epics

- **EPIC-001:** Core CLI Foundation (extends CLI with config support)
- **EPIC-002:** Tree-sitter AST Parsing (error messages for grammar issues)
- **EPIC-004:** Query Library (documentation for patterns)

---

**Epic Owner:** Solo Developer
**Target Completion:** End of Sprint 3 (Week 9)
**User Testing:** Week 9-10 (before release)
