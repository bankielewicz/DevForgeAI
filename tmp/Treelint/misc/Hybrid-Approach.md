  🎯 CHOOSE: Option 4 - Hybrid Approach

  Bundle these 5 grammars:

  1. JavaScript (ES6+, JSX, JSON)
  2. TypeScript (TSX included)
  3. Python (2.7, 3.x)
  4. C# (.NET, Blazor)
  5. Go (cloud-native, microservices)

  Why these 5?
  - Cover 90%+ of DevForgeAI projects based on framework-agnostic target
  - Web (JS/TS), Backend (Python, C#, Go)
  - Total size: ~20-25MB (acceptable)

  Auto-install on-demand:
  - Rust, Java, Ruby, PHP, Swift, Kotlin, C, C++, etc.
  - Triggered automatically when analyzing files
  - Cached in ~/.treelint/grammars/

  ---
  Hybrid Implementation Strategy

  // src/grammars/mod.rs
  pub struct GrammarManager {
      bundled: HashMap<&'static str, Language>,
      cache_dir: PathBuf,
  }

  impl GrammarManager {
      pub async fn get_grammar(&self, language: &str) -> Result<Language> {
          // 1. Check bundled (instant)
          if let Some(grammar) = self.bundled.get(language) {
              info!("Using bundled grammar for {}", language);
              return Ok(grammar.clone());
          }

          // 2. Check cache (~/.treelint/grammars/)
          if let Some(grammar) = self.load_from_cache(language)? {
              info!("Using cached grammar for {}", language);
              return Ok(grammar);
          }

          // 3. Auto-download and compile (if possible)
          if self.can_compile() {
              info!("Auto-installing grammar for {}...", language);
              return self.download_and_compile(language).await;
          }

          // 4. Fail with helpful message
          Err(anyhow!(
              "Grammar for {} not available.\n\n\
               Bundled languages: javascript, typescript, python, csharp, go\n\
               Install {} grammar with: treelint grammar install {}\n\n\
               Auto-install requires gcc/clang. Install with:\n\
                 Ubuntu/Debian: apt-get install build-essential\n\
                 macOS: xcode-select --install\n\
                 Windows: Install Visual Studio Build Tools",
              language, language, language
          ))
      }

      fn can_compile(&self) -> bool {
          // Check for gcc, clang, or MSVC
          Command::new("gcc").arg("--version").output().is_ok() ||
          Command::new("clang").arg("--version").output().is_ok() ||
          Command::new("cl").arg("/?").output().is_ok()
      }
  }

  ---
  Configuration Options

  User Control via Config File

  .treelint.toml:
  [grammars]
  # Auto-install behavior
  auto_install = true          # Auto-download missing grammars (default: true)
  require_confirmation = false # Ask before downloading (default: false)
  cache_dir = "~/.treelint/grammars"

  # Bundled grammars (read-only, informational)
  bundled = ["javascript", "typescript", "python", "csharp", "go"]

  # Pre-installed (user-managed)
  installed = ["rust", "java", "kotlin"]

  Override via CLI:
  # Disable auto-install (fail fast)
  treelint analyze --no-auto-install src/

  # Force re-download
  treelint grammar install python --force

  ---
  DevForgeAI Integration Example

  context-validator Subagent Usage

  # .claude/agents/context-validator.md (updated)

  import subprocess
  import json
  from pathlib import Path

  def validate_layer_boundaries(domain_path: str) -> list[dict]:
      """
      Use TreeLint to validate architectural layer boundaries.

      TreeLint will auto-install grammars if needed (first run only).
      Subsequent runs use cached grammars.
      """
      try:
          result = subprocess.run(
              [
                  'treelint', 'query',
                  '--pattern=layer-boundaries',
                  '--format=json',
                  domain_path
              ],
              capture_output=True,
              text=True,
              check=True,
              timeout=30  # Allow time for auto-install on first run
          )

          violations = json.loads(result.stdout)
          return violations

      except subprocess.CalledProcessError as e:
          # Grammar installation might have failed
          if "Grammar" in e.stderr and "not available" in e.stderr:
              # Helpful error for user
              raise ValidationError(
                  f"TreeLint grammar not available.\n{e.stderr}\n\n"
                  f"First-time setup: TreeLint will auto-install grammars.\n"
                  f"Ensure gcc/clang is installed, or pre-install with:\n"
                  f"  treelint grammar install <language>"
              )
          raise

  ---
  Installation Documentation

  DevForgeAI README Addition

  ## Installing TreeLint (Code Analysis Tool)

  TreeLint is used by DevForgeAI for syntax-aware code analysis.

  ### Quick Install

  **Download binary:**
  ```bash
  # Linux
  curl -L https://github.com/user/treelint/releases/download/v1.0.0/treelint-linux \
    -o /usr/local/bin/treelint
  chmod +x /usr/local/bin/treelint

  # macOS
  brew install treelint  # (if available)

  # Windows
  choco install treelint  # (if available)

  # Or via cargo
  cargo install treelint

  Bundled Languages (Work Immediately)

  TreeLint includes grammars for:
  - JavaScript/TypeScript (web projects)
  - Python (data science, scripting)
  - C# (.NET projects)
  - Go (cloud-native projects)
  - Rust (systems programming)

  No setup required for these languages.

  Additional Languages (Auto-Install)

  For other languages (Java, Ruby, PHP, etc.):
  - TreeLint auto-downloads grammars on first use
  - Requires gcc/clang (one-time setup):
  # Ubuntu/Debian
  sudo apt-get install build-essential

  # macOS
  xcode-select --install

  # Windows
  # Install Visual Studio Build Tools

  Verification

  # Check installation
  treelint --version

  # Test with your project language
  treelint analyze --pattern=functions src/

  If grammar auto-install fails, manually install:
  treelint grammar install <language>
  treelint grammar list  # See available grammars

  ---

  ## Complexity Assessment Impact

  ### Hybrid Grammar Management

  **Added Complexity:**
  - Build-time grammar bundling: +3 points
  - Download manager implementation: +4 points
  - Compiler detection logic: +2 points
  - Cache management: +3 points

  **Total Grammar Management Complexity:** +12 points

  **But:**
  - Better UX = Lower support burden
  - 90% projects work instantly = Higher adoption
  - Acceptable trade-off for learning project

  ---

  ## Answer for Ideation Prompt

  ### Add to Your TreeLint Ideation Prompt

  ```markdown
  ## Grammar Management Strategy

  **Approach:** Hybrid (bundled + auto-install)

  **Bundled Grammars (Ship in binary):**
  1. JavaScript/TypeScript (web projects)
  2. Python (scripting, data science)
  3. C# (.NET projects)
  4. Go (cloud-native projects)
  5. Rust (systems programming)

  **Rationale:** These 5 languages cover 90%+ of DevForgeAI projects

  **Auto-Install (On-Demand):**
  - Other languages: Java, Ruby, PHP, Swift, Kotlin, C/C++, etc.
  - Download from tree-sitter GitHub organization
  - Compile locally (requires gcc/clang)
  - Cache in ~/.treelint/grammars/

  **User Experience:**
  ```bash
  # Bundled language (instant)
  treelint analyze --pattern=anti-patterns src/main.py
  # Works immediately ✓

  # Non-bundled language (auto-install once)
  treelint analyze --pattern=anti-patterns src/Main.kt
  # Kotlin grammar not found. Auto-installing...
  # Downloading tree-sitter-kotlin...
  # Compiling... (requires gcc/clang)
  # ✓ Grammar installed successfully
  # Analyzing... ✓

  # Subsequent runs (cached)
  treelint analyze --pattern=anti-patterns src/Main.kt
  # Works immediately ✓ (uses cached grammar)

  Configuration:
  - Auto-install enabled by default
  - Can be disabled: treelint --no-auto-install (fail fast)
  - Manual install option: treelint grammar install <language>

  Binary Size Impact:
  - Base: ~5MB
  - With 5 bundled grammars: ~25MB
  - Acceptable for developer tool in 2025

  CI/CD Compatibility:
  - 90% of projects: Works in minimal containers (bundled grammars)
  - 10% of projects: Requires build-essential (documented in README)