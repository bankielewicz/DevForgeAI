# EPIC-007: Cross-Platform Build & Distribution

---
id: EPIC-007
title: Cross-Platform Build & Distribution
status: Backlog
created: 2025-11-01
target_sprint: Sprint-4
estimated_points: 13
priority: HIGH
---

## Business Goal

Build and distribute TreeLint binaries for all supported platforms (Linux, macOS, Windows) with automated release workflow and installation guides.

## Success Metrics

- ✅ Binaries for 4 platforms: Linux x86_64, macOS x86_64, macOS ARM64, Windows x86_64
- ✅ GitHub Actions CI/CD working (test, build, release)
- ✅ GitHub Releases with binaries on every tag (v1.0.0, v1.0.1, etc.)
- ✅ Published to crates.io (cargo install treelint)
- ✅ Installation documented for all platforms
- ✅ Checksum verification for binary downloads

## Features

### Feature 1: Cross-Platform Compilation

**Purpose:** Build binaries for all platforms from single CI/CD environment

**Platforms:**
1. **Linux x86_64** (x86_64-unknown-linux-gnu)
2. **macOS x86_64** (x86_64-apple-darwin)
3. **macOS ARM64** (aarch64-apple-darwin)
4. **Windows x86_64** (x86_64-pc-windows-gnu)

**Tool:** cargo-cross or GitHub Actions matrix

**Implementation (GitHub Actions):**
```yaml
# .github/workflows/build.yml

name: Build Binaries

on:
  push:
    tags:
      - 'v*'  # Trigger on version tags (v1.0.0, v1.0.1, etc.)

jobs:
  build:
    name: Build ${{ matrix.target }}
    runs-on: ${{ matrix.os }}

    strategy:
      matrix:
        include:
          - os: ubuntu-latest
            target: x86_64-unknown-linux-gnu
            binary: treelint
            artifact: treelint-linux-x86_64

          - os: macos-latest
            target: x86_64-apple-darwin
            binary: treelint
            artifact: treelint-macos-x86_64

          - os: macos-latest
            target: aarch64-apple-darwin
            binary: treelint
            artifact: treelint-macos-aarch64

          - os: windows-latest
            target: x86_64-pc-windows-gnu
            binary: treelint.exe
            artifact: treelint-windows-x86_64.exe

    steps:
      - uses: actions/checkout@v3

      - name: Install Rust
        uses: actions-rs/toolchain@v1
        with:
          toolchain: stable
          target: ${{ matrix.target }}
          override: true

      - name: Build Binary
        run: cargo build --release --target ${{ matrix.target }}

      - name: Strip Binary (Linux/macOS)
        if: runner.os != 'Windows'
        run: strip target/${{ matrix.target }}/release/${{ matrix.binary }}

      - name: Rename Binary
        run: mv target/${{ matrix.target }}/release/${{ matrix.binary }} ${{ matrix.artifact }}

      - name: Generate Checksum
        run: sha256sum ${{ matrix.artifact }} > ${{ matrix.artifact }}.sha256

      - name: Upload Artifact
        uses: actions/upload-artifact@v3
        with:
          name: ${{ matrix.artifact }}
          path: |
            ${{ matrix.artifact }}
            ${{ matrix.artifact }}.sha256
```

---

### Feature 2: GitHub Releases Automation

**Purpose:** Automatically create GitHub releases with binaries when tagged

**Workflow:**
```yaml
# .github/workflows/release.yml

name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    # ... (same as build.yml)

  release:
    needs: build
    runs-on: ubuntu-latest

    steps:
      - name: Download All Artifacts
        uses: actions/download-artifact@v3

      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          files: |
            treelint-linux-x86_64/treelint-linux-x86_64
            treelint-linux-x86_64/treelint-linux-x86_64.sha256
            treelint-macos-x86_64/treelint-macos-x86_64
            treelint-macos-x86_64/treelint-macos-x86_64.sha256
            treelint-macos-aarch64/treelint-macos-aarch64
            treelint-macos-aarch64/treelint-macos-aarch64.sha256
            treelint-windows-x86_64.exe/treelint-windows-x86_64.exe
            treelint-windows-x86_64.exe/treelint-windows-x86_64.exe.sha256
          body: |
            ## TreeLint ${{ github.ref_name }}

            Syntax-aware code analysis CLI tool using tree-sitter.

            ### Installation

            **Linux:**
            ```bash
            curl -L https://github.com/bankielewicz/TreeLint/releases/download/${{ github.ref_name }}/treelint-linux-x86_64 \
              -o /usr/local/bin/treelint
            chmod +x /usr/local/bin/treelint
            ```

            **macOS (Intel):**
            ```bash
            curl -L https://github.com/bankielewicz/TreeLint/releases/download/${{ github.ref_name }}/treelint-macos-x86_64 \
              -o /usr/local/bin/treelint
            chmod +x /usr/local/bin/treelint
            ```

            **macOS (Apple Silicon):**
            ```bash
            curl -L https://github.com/bankielewicz/TreeLint/releases/download/${{ github.ref_name }}/treelint-macos-aarch64 \
              -o /usr/local/bin/treelint
            chmod +x /usr/local/bin/treelint
            ```

            **Windows:**
            Download `treelint-windows-x86_64.exe` and add to PATH.

            **Via cargo:**
            ```bash
            cargo install treelint
            ```

            ### Verify Installation

            ```bash
            treelint --version
            # Output: treelint ${{ github.ref_name }}
            ```

            ### What's New

            See [CHANGELOG.md](https://github.com/bankielewicz/TreeLint/blob/main/CHANGELOG.md) for details.
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

**Release Process:**
```bash
# Local: Create and push tag
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# GitHub Actions:
# 1. Runs tests on all platforms
# 2. Builds binaries for all platforms
# 3. Creates GitHub release
# 4. Uploads binaries and checksums
```

---

### Feature 3: crates.io Publication

**Purpose:** Enable `cargo install treelint` for Rust users

**Cargo.toml Metadata:**
```toml
[package]
name = "treelint"
version = "1.0.0"
edition = "2021"
rust-version = "1.75"
authors = ["Bryan A <doesnotexist@devforgeai.com>"]
description = "Syntax-aware code analysis CLI tool using tree-sitter"
license = "MIT"
repository = "https://github.com/bankielewicz/TreeLint"
homepage = "https://github.com/bankielewicz/TreeLint"
documentation = "https://docs.rs/treelint"
readme = "README.md"
keywords = ["tree-sitter", "code-analysis", "ast", "linting", "static-analysis"]
categories = ["command-line-utilities", "development-tools"]

# Include only necessary files in package
include = [
    "src/**/*",
    "queries/**/*",
    "grammars/**/*",
    "Cargo.toml",
    "Cargo.lock",
    "LICENSE",
    "README.md",
]
```

**Publication Workflow:**
```bash
# Verify package contents
cargo package --list

# Test package builds
cargo package
cargo install --path .

# Publish to crates.io
cargo publish --dry-run  # Test first
cargo publish  # Requires crates.io API token
```

**GitHub Actions (Automated):**
```yaml
# .github/workflows/publish-crate.yml

name: Publish to crates.io

on:
  push:
    tags:
      - 'v*'

jobs:
  publish:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Install Rust
        uses: actions-rs/toolchain@v1
        with:
          toolchain: stable

      - name: Publish to crates.io
        run: cargo publish --token ${{ secrets.CARGO_TOKEN }}
```

---

### Feature 4: Installation Documentation

**Purpose:** Clear installation guides for all platforms and methods

**README.md Installation Section:**
```markdown
## Installation

### Option 1: Download Pre-Built Binary (Recommended)

**Linux:**
```bash
curl -L https://github.com/bankielewicz/TreeLint/releases/latest/download/treelint-linux-x86_64 \
  -o /usr/local/bin/treelint
chmod +x /usr/local/bin/treelint
```

**macOS (Intel):**
```bash
curl -L https://github.com/bankielewicz/TreeLint/releases/latest/download/treelint-macos-x86_64 \
  -o /usr/local/bin/treelint
chmod +x /usr/local/bin/treelint
```

**macOS (Apple Silicon):**
```bash
curl -L https://github.com/bankielewicz/TreeLint/releases/latest/download/treelint-macos-aarch64 \
  -o /usr/local/bin/treelint
chmod +x /usr/local/bin/treelint
```

**Windows:**
1. Download [treelint-windows-x86_64.exe](https://github.com/bankielewicz/TreeLint/releases/latest/download/treelint-windows-x86_64.exe)
2. Rename to `treelint.exe`
3. Add to PATH

**Verify Installation:**
```bash
treelint --version
# Output: treelint 1.0.0
```

### Option 2: Install via Cargo

**Requirements:** Rust 1.75+ installed

```bash
cargo install treelint
```

This compiles from source (takes 2-3 minutes) and installs to `~/.cargo/bin/treelint`.

### Option 3: Build from Source

```bash
git clone https://github.com/bankielewicz/TreeLint.git
cd TreeLint
cargo build --release
sudo mv target/release/treelint /usr/local/bin/
```

### Checksum Verification (Optional)

```bash
# Download checksum
curl -L https://github.com/bankielewicz/TreeLint/releases/latest/download/treelint-linux-x86_64.sha256 \
  -o treelint-linux-x86_64.sha256

# Verify
sha256sum -c treelint-linux-x86_64.sha256
# Output: treelint-linux-x86_64: OK
```
```

---

### Feature 5: CI/CD Testing

**Purpose:** Ensure TreeLint works on all platforms before release

**Test Matrix:**
```yaml
# .github/workflows/ci.yml

name: CI

on: [push, pull_request]

jobs:
  test:
    name: Test on ${{ matrix.os }}
    runs-on: ${{ matrix.os }}

    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]

    steps:
      - uses: actions/checkout@v3

      - name: Install Rust
        uses: actions-rs/toolchain@v1
        with:
          toolchain: stable

      - name: Run Tests
        run: cargo test --all

      - name: Run Clippy
        run: cargo clippy -- -D warnings

      - name: Check Formatting
        run: cargo fmt -- --check

      - name: Build Binary
        run: cargo build --release

      - name: Test Binary
        run: |
          ./target/release/treelint --version
          ./target/release/treelint analyze --pattern=anti-patterns tests/fixtures/
```

**Run on Every Push:**
- Ensures code compiles on all platforms
- Catches platform-specific bugs early
- Validates tests pass on all platforms

---

## Requirements Addressed

- **NFR-2:** Cross-Platform Support (Linux, macOS, Windows) - HIGH

## Non-Functional Requirements

- **Binary Size:** <30MB per platform
- **Build Time:** <10 minutes per platform (CI)
- **Portability:** No runtime dependencies (standalone binaries)

## Architecture Considerations

**Build Configuration:**
```toml
# Cargo.toml

[profile.release]
strip = true        # Remove debug symbols (reduces size 20%)
lto = true          # Link-time optimization (removes unused code)
codegen-units = 1   # Better optimization (slower compile, smaller binary)
opt-level = 3       # Maximum optimization

[profile.dev]
opt-level = 0       # Fast compilation for development
```

**Cross-Compilation Targets:**
```toml
# .cargo/config.toml (optional, for local cross-compilation)

[target.x86_64-unknown-linux-gnu]
linker = "x86_64-linux-gnu-gcc"

[target.aarch64-apple-darwin]
linker = "aarch64-apple-darwin-ld"

[target.x86_64-pc-windows-gnu]
linker = "x86_64-w64-mingw32-gcc"
```

---

## Platform-Specific Considerations

### Linux (x86_64-unknown-linux-gnu)

**Compatibility:**
- glibc 2.31+ (Ubuntu 20.04+, Debian 11+)
- Static linking for portability (or musl target for older systems)

**Build:**
```bash
cargo build --release --target x86_64-unknown-linux-gnu
strip target/x86_64-unknown-linux-gnu/release/treelint
```

**Size:** ~25MB (with 5 bundled grammars)

**Testing:**
- Test on Ubuntu 20.04, 22.04
- Test on Debian 11, 12
- Verify works in Docker (minimal image)

---

### macOS Intel (x86_64-apple-darwin)

**Compatibility:**
- macOS 10.15+ (Catalina and later)

**Build:**
```bash
cargo build --release --target x86_64-apple-darwin
strip target/x86_64-apple-darwin/release/treelint
```

**Size:** ~26MB

**Code Signing (Optional for v1.0):**
```bash
# Sign binary (requires Apple Developer account)
codesign --sign "Developer ID Application: Your Name" treelint
```

**Not required for v1.0** (unsigned binaries work, show warning)

---

### macOS Apple Silicon (aarch64-apple-darwin)

**Compatibility:**
- macOS 11.0+ (Big Sur and later, M1/M2/M3 Macs)

**Build:**
```bash
cargo build --release --target aarch64-apple-darwin
strip target/aarch64-apple-darwin/release/treelint
```

**Size:** ~24MB (ARM binaries slightly smaller)

**Testing:**
- Test on M1/M2/M3 Macs (or GitHub Actions M1 runners)
- Verify Rosetta not used (native ARM binary)

---

### Windows (x86_64-pc-windows-gnu)

**Compatibility:**
- Windows 10+ (64-bit)

**Build:**
```bash
cargo build --release --target x86_64-pc-windows-gnu
strip target/x86_64-pc-windows-gnu/release/treelint.exe
```

**Size:** ~27MB

**Windows Defender:**
- Unsigned binaries may trigger SmartScreen warning
- Document workaround: "More info" → "Run anyway"
- **For v1.1:** Consider code signing

**Path Installation:**
- Document: Add to PATH via System Properties
- Or: Install to directory already in PATH (e.g., C:\Windows\System32)

---

### Feature 6: Release Checklist Automation

**Purpose:** Ensure every release is consistent and complete

**Pre-Release Checklist:**
```bash
# .github/workflows/pre-release.yml

# Run before tagging
- [ ] All tests pass on all platforms
- [ ] Benchmarks meet performance targets
- [ ] No clippy warnings
- [ ] Version bumped in Cargo.toml
- [ ] CHANGELOG.md updated
- [ ] README.md updated (if API changed)
- [ ] Documentation reviewed
```

**Post-Release Checklist:**
- [ ] Binaries uploaded to GitHub Releases
- [ ] crates.io published successfully
- [ ] Binaries tested (download and run --version)
- [ ] Checksums verified
- [ ] Release notes accurate

---

## Distribution Channels

### 1. GitHub Releases (Primary)

**URL:** https://github.com/bankielewicz/TreeLint/releases

**Artifacts per Release:**
- treelint-linux-x86_64 + .sha256
- treelint-macos-x86_64 + .sha256
- treelint-macos-aarch64 + .sha256
- treelint-windows-x86_64.exe + .sha256

**Download Count Tracking:**
- GitHub provides download statistics
- Monitor which platforms are popular

---

### 2. crates.io (Rust Users)

**URL:** https://crates.io/crates/treelint

**Installation:**
```bash
cargo install treelint
```

**Benefits:**
- Compiles from source (always latest Rust toolchain)
- Automatic updates: `cargo install treelint --force`
- Verifiable (source code inspection)

---

### 3. Package Managers (Future v1.1+)

**Homebrew (macOS):**
```bash
brew install treelint
```

**Requires:** Homebrew formula (tap repository)
**Effort:** ~1 day to create formula
**Defer to:** v1.1 (after v1.0 adoption proven)

**apt (Ubuntu/Debian):**
```bash
sudo apt install treelint
```

**Requires:** Debian package (.deb) and PPA hosting
**Effort:** ~2 days
**Defer to:** v1.2

**Chocolatey (Windows):**
```bash
choco install treelint
```

**Requires:** Chocolatey package
**Effort:** ~1 day
**Defer to:** v1.1

---

## DevForgeAI Bundling Strategy

**From repository.md decision:** Standalone repo + smart bundling

**DevForgeAI Installation Script:**
```bash
# .devforgeai/scripts/install-treelint.sh

#!/bin/bash
set -e

CODELENS_VERSION="1.0.0"

# Detect platform
OS=$(uname -s)
ARCH=$(uname -m)

case "$OS-$ARCH" in
    Linux-x86_64)
        BINARY="treelint-linux-x86_64"
        ;;
    Darwin-x86_64)
        BINARY="treelint-macos-x86_64"
        ;;
    Darwin-arm64)
        BINARY="treelint-macos-aarch64"
        ;;
    MINGW*-x86_64|MSYS*-x86_64)
        BINARY="treelint-windows-x86_64.exe"
        ;;
    *)
        echo "Unsupported platform: $OS-$ARCH"
        echo "Install manually: cargo install treelint"
        exit 1
        ;;
esac

echo "Downloading TreeLint $CODELENS_VERSION for $OS-$ARCH..."

curl -L "https://github.com/bankielewicz/TreeLint/releases/download/v${CODELENS_VERSION}/${BINARY}" \
  -o treelint

chmod +x treelint

# Install to /usr/local/bin or ~/.local/bin
if [ -w /usr/local/bin ]; then
    mv treelint /usr/local/bin/
    echo "✓ Installed to /usr/local/bin/treelint"
else
    mkdir -p ~/.local/bin
    mv treelint ~/.local/bin/
    echo "✓ Installed to ~/.local/bin/treelint"
    echo "Ensure ~/.local/bin is in your PATH"
fi

# Verify
treelint --version
echo "✓ TreeLint installed successfully"
```

**DevForgeAI README Update:**
```markdown
## Installing TreeLint (Required for Code Analysis)

TreeLint is used by DevForgeAI for syntax-aware code validation.

**Quick Install:**
```bash
.devforgeai/scripts/install-treelint.sh
```

**Or install manually:**
```bash
cargo install treelint
```

**Verify:**
```bash
treelint --version
```

**Bundled Grammars:** JavaScript, TypeScript, Python, C#, Go, Rust work offline.
**Other Languages:** Auto-install on first use (requires gcc/clang).
```

---

## CI/CD Integration Examples

### GitHub Actions

```yaml
# .github/workflows/qa.yml (in user's project)

name: Code Quality

on: [push, pull_request]

jobs:
  treelint:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Install TreeLint
        run: cargo install treelint

      - name: Cache Grammars
        uses: actions/cache@v3
        with:
          path: ~/.cache/treelint/grammars
          key: treelint-grammars-${{ hashFiles('**/*.rs') }}

      - name: Run Anti-Pattern Analysis
        run: treelint analyze --pattern=anti-patterns src/

      - name: Run Security Analysis
        run: treelint analyze --pattern=security src/

      - name: Run Architecture Validation
        run: treelint analyze --pattern=architecture src/
```

---

### GitLab CI

```yaml
# .gitlab-ci.yml (in user's project)

treelint-analysis:
  image: rust:1.75
  stage: test

  cache:
    paths:
      - ~/.cache/treelint/grammars

  before_script:
    - cargo install treelint

  script:
    - treelint analyze --pattern=anti-patterns src/
    - treelint analyze --pattern=security src/
    - treelint analyze --pattern=architecture src/
```

---

## Versioning Strategy

**Semantic Versioning (SemVer):**
- **MAJOR.MINOR.PATCH** (e.g., 1.0.0)

**Version Bumps:**
- **MAJOR (1.x → 2.x):** Breaking changes (API changes, CLI flag changes)
- **MINOR (1.0 → 1.1):** New features (new patterns, Python library)
- **PATCH (1.0.0 → 1.0.1):** Bug fixes, performance improvements

**v1.0.x Releases:**
- v1.0.0: Initial release (12 patterns, CLI only)
- v1.0.1: Bug fixes (grammar installation issues, error messages)
- v1.0.2: Performance improvements (query optimization)

**v1.1.x Releases:**
- v1.1.0: Add Python library (PyO3 bindings)
- v1.1.1: Python library bug fixes

**v1.2.x Releases:**
- v1.2.0: Add gRPC service mode
- v1.2.1: Service mode bug fixes

---

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Cross-compilation failures | High | Test on all platforms in CI |
| Binary size exceeds 30MB | Medium | Use strip, LTO, profile size |
| Platform-specific bugs | Medium | Comprehensive testing matrix |
| Code signing issues (macOS) | Low | Document unsigned binary warning |

## Assumptions

- GitHub Actions provides all required platforms (Linux, macOS, Windows)
- Binary size will be <30MB after strip and LTO
- Users can accept unsigned binaries (or we get code signing in v1.1)
- crates.io publication will succeed (standard process)

## Dependencies

**Build Tools:**
- Rust 1.75+ (all platforms)
- strip (Linux, macOS) for size reduction
- GitHub Actions runners (CI/CD)

**Development:**
- cargo (build system)
- git (version control)
- GitHub account (releases, Actions)
- crates.io account (publication)

---

## Testing Strategy

**Platform-Specific Tests:**
```rust
#[test]
#[cfg(target_os = "linux")]
fn test_linux_specific() {
    // Test Linux-specific behavior
}

#[test]
#[cfg(target_os = "macos")]
fn test_macos_specific() {
    // Test macOS-specific behavior
}

#[test]
#[cfg(target_os = "windows")]
fn test_windows_specific() {
    // Test Windows-specific behavior
}
```

**Cross-Platform Path Tests:**
```rust
#[test]
fn test_cross_platform_paths() {
    // Ensure PathBuf works on all platforms
    let cache_dir = dirs::cache_dir().unwrap().join("treelint");

    #[cfg(windows)]
    assert!(cache_dir.to_str().unwrap().contains("\\"));

    #[cfg(unix)]
    assert!(cache_dir.to_str().unwrap().contains("/"));
}
```

---

## Release Workflow

### Step 1: Prepare Release (Local)

```bash
# 1. Update version in Cargo.toml
version = "1.0.0"

# 2. Update CHANGELOG.md
## [1.0.0] - 2025-12-15

### Added
- 12 core patterns (anti-patterns, architecture, security, testing)
- 5 bundled grammars (JavaScript, TypeScript, Python, C#, Go, Rust)
- Auto-install for non-bundled grammars
- JSON output format
- .treelint.toml configuration support

# 3. Commit changes
git add Cargo.toml CHANGELOG.md
git commit -m "chore: Prepare v1.0.0 release"

# 4. Create and push tag
git tag -a v1.0.0 -m "Release v1.0.0: Syntax-aware code analysis with 12 core patterns"
git push origin main
git push origin v1.0.0
```

---

### Step 2: Automated Build (GitHub Actions)

**Triggered by tag push:**
1. Run tests on all platforms
2. Build binaries for all platforms
3. Strip debug symbols
4. Generate checksums
5. Create GitHub Release
6. Upload binaries and checksums
7. Publish to crates.io

**Duration:** ~15-20 minutes (parallel builds)

---

### Step 3: Verify Release

```bash
# Download and test each binary
curl -L .../treelint-linux-x86_64 -o treelint-linux
chmod +x treelint-linux
./treelint-linux --version
./treelint-linux analyze --pattern=anti-patterns tests/fixtures/

# Verify checksum
sha256sum treelint-linux
# Compare with .sha256 file

# Test cargo install
cargo install treelint
treelint --version
```

---

### Step 4: Announce Release

**GitHub Release Notes:**
- Summary of features
- Installation instructions
- Breaking changes (if any)
- Known issues
- Contributors (if any)

**Social Media (Optional):**
- Reddit (r/rust)
- Twitter/X
- Hacker News (for major releases)

---

## Next Steps

After completing this epic:
1. Monitor download statistics (which platforms most popular)
2. Gather user feedback on installation process
3. Plan v1.1 release (Python library)

## Related Epics

- **EPIC-001:** Core CLI Foundation (binary that gets distributed)
- **ALL EPICS:** Complete product that gets released

---

**Epic Owner:** Solo Developer
**Target Completion:** End of Sprint 4 (Week 12)
**Deliverables:** 4 platform binaries, GitHub Release, crates.io publication, complete documentation
