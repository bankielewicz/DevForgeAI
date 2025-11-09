  Recommendation

  🎯 CHOOSE: Option 3 - Minimal Read-Only Config in v1.0

  Answer for Ideation:

  Configuration file support: Minimal read-only config in v1.0

  v1.0 Config Schema (minimal, optional):
  ```toml
  # .treelint.toml (optional file)
  [grammars]
  auto_install = true              # Auto-install missing grammars (default: true)
  cache_dir = "~/.treelint/grammars"  # Grammar cache location (default: ~/.treelint/grammars)

  [output]
  format = "json"                  # Output format: json|text|markdown (default: json)
  verbose = false                  # Show detailed output (default: false)

  Behavior:
  - Config file is OPTIONAL (TreeLint works without it)
  - Sensible defaults if no config present
  - CLI flags override config settings (priority: CLI > Config > Defaults)
  - Simple schema (4 settings only)
  - No validation complexity (all settings have safe defaults)

  Implementation:
  - Use serde + toml crates (standard Rust ecosystem)
  - ~100 lines of code (src/config.rs)
  - 2 days implementation time
  - Minimal learning curve (basic TOML parsing)

  DevForgeAI Integration:
  # DevForgeAI/.treelint.toml (committed to repo)
  [grammars]
  auto_install = true

  [output]
  format = "json"

  Simplifies subagent invocations:
  # With config:
  subprocess.run(['treelint', 'analyze', 'src/'])

  # Without config:
  subprocess.run(['treelint', 'analyze', '--format=json', '--auto-install', 'src/'])

  Future Extension (v1.1+):
  Add settings based on real usage feedback:
  - Custom pattern directories
  - Pattern enable/disable lists
  - Performance tuning options
  - Service mode configuration
  - Advanced output customization

  Why Minimal for v1.0:
  1. Provides essential customization (auto_install, format)
  2. Low complexity (2 days vs 5 days for full config)
  3. Per-project settings (commit .treelint.toml to git)
  4. Learn serde/TOML (valuable Rust skill)
  5. Validate defaults work before adding 20+ settings
  6. Ship v1.0 in 8.5 weeks (only +0.5 week overhead)

  This approach gives DevForgeAI per-project configuration while keeping v1.0 scope manageable and learning-focused.

  ---

  ## Final v1.0 Scope Summary

  With all decisions made:

  **Features:**
  - ✅ Rust CLI with clap
  - ✅ Tree-sitter integration (5 bundled grammars)
  - ✅ Hybrid grammar management (bundle 5, auto-install others)
  - ✅ 12 core query patterns (4+4+3+1)
  - ✅ Performance: Parse + 4 queries in <2s
  - ✅ Auto-install with smart context detection
  - ✅ Minimal config file support (4 settings)
  - ✅ JSON output for DevForgeAI

  **Timeline: 8.5 weeks** (includes Rust learning curve)

  **Complexity: Medium-High** (42-48 points - appropriate for learning project)

  ---

  **This minimal config approach adds valuable customization without significant scope creep!** ⚙️✅