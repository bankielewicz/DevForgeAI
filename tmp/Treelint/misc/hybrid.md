  Hybrid Strategy (Recommended)

  Option 5: Context-Aware Error Handling

  Smart Behavior Based on Context:

  enum GrammarMissingStrategy {
      AutoInstall,    // CI_AUTO_INSTALL=true or --auto-install flag
      FailFast,       // CI_AUTO_INSTALL=false or --no-auto-install flag
      Interactive,    // TTY available and not in CI
  }

  fn handle_missing_grammar(language: &str, strategy: GrammarMissingStrategy) -> Result<Grammar> {
      match strategy {
          GrammarMissingStrategy::AutoInstall => {
              println!("{} grammar not found. Auto-installing...", language);
              auto_install_with_progress(language)?
          }

          GrammarMissingStrategy::FailFast => {
              eprintln!("ERROR: {} grammar not found", language);
              eprintln!("\nInstall with: treelint grammar install {}", language);
              std::process::exit(1);
          }

          GrammarMissingStrategy::Interactive => {
              print!("Install {} grammar now? (y/n): ", language);
              if confirm_yes() {
                  auto_install_with_progress(language)?
              } else {
                  eprintln!("Analysis aborted. Install manually:");
                  eprintln!("  treelint grammar install {}", language);
                  std::process::exit(1);
              }
          }
      }
  }

  Strategy Detection:
  fn detect_strategy() -> GrammarMissingStrategy {
      // Check environment variable (CI/CD sets this)
      if env::var("CODELENS_AUTO_INSTALL").is_ok() {
          return GrammarMissingStrategy::AutoInstall;
      }

      // Check CLI flag
      if cli.auto_install {
          return GrammarMissingStrategy::AutoInstall;
      }
      if cli.no_auto_install {
          return GrammarMissingStrategy::FailFast;
      }

      // Check if in CI environment
      if env::var("CI").is_ok() {
          return GrammarMissingStrategy::FailFast;  // Don't auto-install in CI by default
      }

      // Check TTY (interactive terminal)
      if atty::is(atty::Stream::Stdin) {
          return GrammarMissingStrategy::Interactive;
      }

      // Default: Auto-install (best UX)
      GrammarMissingStrategy::AutoInstall
  }

  ---
  DevForgeAI Integration Patterns

  Pattern 1: Developer Local Workflow (Auto-Install)

  # Developer's machine (interactive terminal)
  > /dev STORY-001

  # TreeLint detects: TTY available, not in CI
  # Strategy: Auto-install silently with progress

  Kotlin grammar not found. Auto-installing...
  [1/3] Downloading tree-sitter-kotlin...
  [2/3] Compiling (30s)...
  [3/3] Caching...
  ✓ Installed

  # Continues automatically ✅

  ---
  Pattern 2: CI/CD Pipeline (Fail Fast)

  # .github/workflows/qa.yml
  - name: Run Deep QA
    run: |
      treelint analyze --pattern=all src/
    env:
      CI: true  # TreeLint detects CI environment

  # Behavior: Fail fast if grammar missing
  # Rationale: CI should have grammars pre-installed (cached)

  Best Practice in DevForgeAI CI:
  # Install TreeLint + common grammars once
  - name: Setup TreeLint
    uses: actions/cache@v3
    with:
      path: ~/.treelint/grammars
      key: treelint-grammars-${{ hashFiles('**/Cargo.lock') }}

  - name: Pre-install grammars (if cache miss)
    run: |
      if [ ! -d ~/.treelint/grammars/kotlin ]; then
        treelint grammar install kotlin
      fi

  ---
  Pattern 3: Explicit Control (CLI Flags)

  # Force auto-install (override detection)
  treelint analyze --auto-install --pattern=anti-patterns src/

  # Force fail-fast (override detection)
  treelint analyze --no-auto-install --pattern=anti-patterns src/

  # Environment variable (for scripts)
  export CODELENS_AUTO_INSTALL=true
  treelint analyze --pattern=anti-patterns src/

  ---
  Recommendation

  🎯 CHOOSE: Option 3 (Auto-Install Silently) with Smart Context Detection

  Answer for Ideation:

  Error handling for missing grammars: Context-aware auto-install (hybrid strategy)

  Default Behavior: Auto-install silently with progress feedback
  - Detects missing grammar automatically
  - Downloads and compiles if gcc/clang available
  - Shows progress: [1/3] Downloading... [2/3] Compiling... [3/3] Caching...
  - Caches in ~/.treelint/grammars/ for future use
  - No user interaction required

  Context Detection:
  1. CI Environment (CI=true): Fail fast with error
     - Rationale: CI should have grammars pre-installed (cached)
     - Exit code 1, clear error message
     - Prevents long compilation in CI (should use cache)

  2. TTY Available: Auto-install with progress
     - Rationale: Interactive user can see progress
     - One-time delay acceptable (30-60s)
     - Subsequent runs instant (cached)

  3. No TTY (script): Auto-install silently
     - Rationale: Automation scripts need to complete
     - Show progress to logs for debugging

  Override Options:
  - CLI flag: --auto-install (force auto-install)
  - CLI flag: --no-auto-install (force fail-fast)
  - ENV var: CODELENS_AUTO_INSTALL=true/false

  Error Handling if Auto-Install Fails:
  ERROR: Failed to auto-install Kotlin grammar

  Reason: gcc not found (required for compilation)

  Solutions:
  1. Install gcc:
  Ubuntu/Debian: apt-get install build-essential
  macOS: xcode-select --install
  Windows: Install Visual Studio Build Tools
  2. Download pre-compiled grammar (if available):
  treelint grammar download kotlin
  3. Use bundled languages only:
  javascript, typescript, python, csharp, go

  Exit code: 1

  Rationale:
  1. Best UX for DevForgeAI (auto-install in local dev, fail-fast in CI)
  2. No interactive prompts (doesn't block automation)
  3. Clear errors when auto-install fails (actionable guidance)
  4. Respects different execution contexts (local vs CI)
  5. User control via flags (override defaults)

  This strategy ensures DevForgeAI workflows run without intervention while providing helpful guidance when issues
  occur.

  ---
  Implementation Example

  Smart Error Handler

  // src/grammar_handler.rs

  pub struct GrammarHandler {
      bundled: HashSet<&'static str>,
      cache_dir: PathBuf,
      strategy: MissingGrammarStrategy,
  }

  #[derive(Debug, Clone)]
  enum MissingGrammarStrategy {
      AutoInstall { show_progress: bool },
      FailFast,
      Interactive,
  }

  impl GrammarHandler {
      pub fn new() -> Self {
          let strategy = Self::detect_strategy();

          GrammarHandler {
              bundled: hashset!["javascript", "typescript", "python", "csharp", "go"],
              cache_dir: dirs::cache_dir()
                  .unwrap()
                  .join("treelint")
                  .join("grammars"),
              strategy,
          }
      }

      fn detect_strategy() -> MissingGrammarStrategy {
          // Check CLI flags first
          if let Some(flag) = env::var("CODELENS_AUTO_INSTALL").ok() {
              if flag == "true" {
                  return MissingGrammarStrategy::AutoInstall { show_progress: true };
              } else {
                  return MissingGrammarStrategy::FailFast;
              }
          }

          // In CI: Fail fast (don't auto-install)
          if env::var("CI").is_ok() {
              return MissingGrammarStrategy::FailFast;
          }

          // Interactive terminal: Auto-install with progress
          if atty::is(atty::Stream::Stdout) {
              return MissingGrammarStrategy::AutoInstall { show_progress: true };
          }

          // Non-interactive (scripts): Auto-install silently
          MissingGrammarStrategy::AutoInstall { show_progress: false }
      }

      pub fn get_grammar(&mut self, language: &str) -> Result<Language> {
          // 1. Check bundled
          if self.bundled.contains(language) {
              return load_bundled_grammar(language);
          }

          // 2. Check cache
          if let Some(grammar) = self.load_from_cache(language)? {
              return Ok(grammar);
          }

          // 3. Handle missing grammar based on strategy
          match self.strategy {
              MissingGrammarStrategy::AutoInstall { show_progress } => {
                  self.auto_install(language, show_progress)
              }

              MissingGrammarStrategy::FailFast => {
                  self.fail_with_helpful_error(language)
              }

              MissingGrammarStrategy::Interactive => {
                  self.prompt_and_install(language)
              }
          }
      }

      fn auto_install(&mut self, language: &str, show_progress: bool) -> Result<Language> {
          if show_progress {
              println!("{} grammar not found. Auto-installing...", language);
          }

          // Check build tools
          if !self.has_build_tools() {
              bail!(
                  "Cannot auto-install {} grammar: gcc/clang not found\n\n\
                   Install build tools:\n\
                     Ubuntu/Debian: apt-get install build-essential\n\
                     macOS: xcode-select --install\n\
                     Windows: Install Visual Studio Build Tools",
                  language
              );
          }

          // Download
          if show_progress {
              println!("[1/3] Downloading tree-sitter-{}...", language);
          }
          self.download_grammar(language)?;

          // Compile
          if show_progress {
              println!("[2/3] Compiling grammar (this may take 30-60s)...");
          }
          self.compile_grammar(language)?;

          // Cache
          if show_progress {
              println!("[3/3] Caching in {:?}...", self.cache_dir);
              println!("✓ Grammar installed successfully\n");
          }

          // Load from cache
          self.load_from_cache(language)?
              .ok_or_else(|| anyhow!("Failed to load installed grammar"))
      }

      fn fail_with_helpful_error(&self, language: &str) -> Result<Language> {
          let mut error = format!("ERROR: {} grammar not found\n\n", language);

          error.push_str(&format!(
              "{} is not bundled. Install with one of:\n\n",
              language
          ));

          // Option 1: Auto-install
          if self.has_build_tools() {
              error.push_str(&format!(
                  "  Option 1: Auto-install (requires gcc/clang)\n\
                     treelint grammar install {}\n\n",
                  language
              ));
          } else {
              error.push_str(&format!(
                  "  Option 1: Install gcc first, then:\n\
                     treelint grammar install {}\n\n",
                  language
              ));
          }

          // Option 2: Use bundled languages
          error.push_str(&format!(
              "  Option 2: Use bundled languages only:\n\
                 {:?}\n\n",
              self.bundled
          ));

          // Option 3: Request bundling
          error.push_str(&format!(
              "  Option 3: Request {} bundled in next release:\n\
                 https://github.com/user/treelint/issues\n",
              language
          ));

          eprintln!("{}", error);
          std::process::exit(1);
      }
  }

  ---
  Configuration Options

  .treelint.toml

  [grammars]
  # Auto-install behavior
  auto_install = true              # Default: true (auto-install missing grammars)
  show_progress = true             # Default: true (show download/compile progress)
  fail_on_missing = false          # Default: false (true = fail fast instead)

  # Cache settings
  cache_dir = "~/.treelint/grammars"
  cache_ttl_days = 90              # Re-download after 90 days

  # Bundled grammars (read-only)
  bundled = ["javascript", "typescript", "python", "csharp", "go"]

  # CI behavior override
  ci_auto_install = false          # Default: false (fail fast in CI)

  ---
  DevForgeAI Integration Best Practices

  Setup Script for New Users

  # .devforgeai/scripts/setup-treelint.sh

  #!/bin/bash
  set -e

  echo "Setting up TreeLint for DevForgeAI..."

  # 1. Check if TreeLint installed
  if ! command -v treelint &> /dev/null; then
      echo "TreeLint not found. Installing..."
      curl -L https://github.com/user/treelint/releases/download/v1.0.0/treelint-linux \
        -o /usr/local/bin/treelint
      chmod +x /usr/local/bin/treelint
  fi

  # 2. Verify installation
  treelint --version

  # 3. Pre-install common grammars (optional, speeds up first use)
  echo "Pre-installing common grammars..."
  for lang in python javascript typescript csharp go; do
      if [ ! -d ~/.treelint/grammars/$lang ]; then
          treelint grammar install $lang || echo "Warning: Failed to install $lang grammar"
      fi
  done

  echo "✓ TreeLint setup complete!"
  echo ""
  echo "Bundled grammars (work offline):"
  echo "  - JavaScript, TypeScript, Python, C#, Go"
  echo ""
  echo "Other languages will auto-install on first use (requires gcc/clang)"

  ---
  CI/CD Configuration

  # .github/workflows/qa.yml
  name: Deep QA Validation

  on: [push, pull_request]

  jobs:
    qa:
      runs-on: ubuntu-latest

      steps:
        - uses: actions/checkout@v3

        # Cache TreeLint binary and grammars
        - name: Cache TreeLint
          uses: actions/cache@v3
          with:
            path: |
              ~/.cargo/bin/treelint
              ~/.treelint/grammars
            key: treelint-${{ runner.os }}-v1.0.0

        # Install TreeLint if not cached
        - name: Install TreeLint
          run: |
            if ! command -v treelint; then
              cargo install treelint
            fi

        # Pre-install grammars if not cached (prevents auto-install in validation)
        - name: Setup Grammars
          run: |
            if [ ! -d ~/.treelint/grammars/python ]; then
              sudo apt-get update && sudo apt-get install -y build-essential
              treelint grammar install python javascript typescript
            fi

        # Run validation (will use cached grammars, no auto-install delay)
        - name: Run QA
          run: |
            # In CI, auto-install disabled by default (fail fast)
            python .claude/skills/devforgeai-qa/scripts/validate.py
          env:
            CODELENS_AUTO_INSTALL: false  # Fail if grammar missing (should be cached)

  ---
  Final Recommendation

  🎯 CHOOSE: Option 3 with Smart Context Detection

  Answer for Ideation:

  Error handling for missing grammars: Auto-install silently with smart context detection

  Default Behavior (Local Development):
  - Auto-install missing grammars without prompting
  - Show clear progress feedback:
    "Kotlin grammar not found. Auto-installing..."
    "[1/3] Downloading tree-sitter-kotlin from GitHub..."
    "[2/3] Compiling grammar (requires gcc/clang, ~30s)..."
    "[3/3] Caching in ~/.treelint/grammars/..."
    "✓ Installed successfully"
  - Continue analysis automatically
  - Cache for future use (subsequent runs instant)

  CI/CD Behavior:
  - Fail fast if grammar missing (don't auto-install in CI)
  - Exit code 1 with helpful error message
  - Assumes grammars should be pre-installed/cached
  - Prevents unexpected 30-60s compilation in CI

  Override Options:
  - CLI flag: --auto-install (force auto-install)
  - CLI flag: --no-auto-install (force fail-fast)
  - ENV var: CODELENS_AUTO_INSTALL=true/false
  - Config file: auto_install = true/false in .treelint.toml

  Error Handling if Auto-Install Fails:
  ERROR: Failed to auto-install Kotlin grammar

  Cause: gcc not found (required for compilation)

  Install build tools:
    Ubuntu/Debian: apt-get install build-essential
    macOS: xcode-select --install
    Windows: Install Visual Studio Build Tools

  Then retry:
    treelint analyze --pattern=anti-patterns src/

  Or use bundled languages only:
    javascript, typescript, python, csharp, go

  Exit code: 1

  Rationale:
  1. Best UX for local development (auto-install = zero friction)
  2. CI/CD compatible (fail-fast prevents unexpected delays)
  3. DevForgeAI automation-friendly (no interactive prompts)
  4. Clear errors when auto-install fails (actionable guidance)
  5. User control via flags/env vars (override smart detection)
  6. Predictable behavior (context-aware, documented)

  This ensures TreeLint works seamlessly in DevForgeAI workflows while handling edge cases gracefully.

  ---
  This gives you the best of both worlds: automatic operation for smooth UX, but intelligent failure modes for CI/CD
   and error cases! ⚡🎯