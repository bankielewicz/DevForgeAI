# Dependencies - DevForgeAI Framework

**Status**: LOCKED
**Last Updated**: 2025-10-30
**Version**: 1.0

## Framework Dependencies

### Core Platform Dependency

**Claude Code Terminal 1.0+**
- **LOCKED**: Framework requires Claude Code Terminal
- **Version**: 1.0 or higher
- **Rationale**: Framework built on Claude Code's Skills, Subagents, and Slash Commands

### No External Package Dependencies

**CRITICAL**: DevForgeAI framework itself has ZERO external package dependencies.

**Rationale**:
- Framework is documentation-based (Markdown files)
- No code to execute = No packages to install
- Projects using DevForgeAI specify their own dependencies

### Project Dependency Pattern

When devforgeai-architecture skill creates dependencies.md for projects:

**Process**:
1. Use AskUserQuestion for each technology layer
2. Lock approved packages with versions
3. Document "FORBIDDEN" alternatives
4. Add dependency addition protocol

**Example Project dependencies.md**:
```markdown
# Backend Data Access
- Dapper 2.1.28 (LOCKED - NOT Entity Framework)
- FluentMigrator 3.3.2 (LOCKED)

# Frontend State Management  
- Zustand 4.4.1 (LOCKED - NOT Redux/MobX)

# Testing
- xUnit 2.5.0 (LOCKED - NOT NUnit/MSTest)
- NSubstitute 5.1.0 (LOCKED - NOT Moq)
```

## Dependency Addition Protocol

**Framework Constraint**: When ANY framework component needs external functionality:

1. **Check**: Is it core Claude Code functionality? (Yes → Use it, No → Continue)
2. **Evaluate**: Can it be done with Markdown documentation? (Yes → Document it, No → Continue)
3. **Question**: Use AskUserQuestion to get user approval
4. **Document**: Add to this file with rationale
5. **ADR**: Create Architecture Decision Record

## Prohibited Dependencies (Core Framework)

❌ **NO npm packages** for core framework (skills, subagents, commands)
❌ **NO Python packages** for core framework (Markdown documentation only)
❌ **NO .NET packages** for core framework
❌ **NO** executable code dependencies in core framework

**Rationale**: Core framework must work across all language ecosystems without installation.

---

## Installer Dependencies (EPIC-012, EPIC-013, EPIC-014)

**Exception**: The installer is a **distribution tool** (not core framework) and requires dependencies.

### NPM Dependencies (Locked)

**Production Dependencies:**
```json
{
  "commander": "^11.0.0",
  "inquirer": "^8.2.6",
  "ora": "^5.4.1",
  "chalk": "^4.1.2",
  "cli-progress": "^3.12.0"
}
```

**Version Constraints (per ADR-006):**
- `inquirer`: 8.x (Last CommonJS version, 9.x is ESM-only)
- `ora`: 5.x (Last CommonJS version, 6.x+ is ESM-only)
- `chalk`: 4.x (Last CommonJS version, 5.x+ is ESM-only)
- `cli-progress`: 3.x (CommonJS compatible)
- `commander`: 11.x (CommonJS compatible)

**Alternatives FORBIDDEN:**
- ❌ Yargs (use Commander.js only)
- ❌ Prompts (use Inquirer.js only)
- ❌ cli-spinners (use Ora only)
- ❌ colors (use Chalk only)

**Optional GUI Dependencies (EPIC-039, ADR-009):**
```json
{
  "electron": "^28.0.0",
  "electron-builder": "^24.0.0"
}
```

**GUI Dependency Constraints (per ADR-009):**
- `electron`: 28.x+ (LTS version with security patches)
- `electron-builder`: 24.x (Multi-platform packaging)
- **OPTIONAL**: GUI installer is optional; CLI wizard works without Electron
- **SCOPE**: Only for `installer/gui/` directory (STORY-248)
- **NOT REQUIRED**: Core DevForgeAI framework does NOT require Electron

**GUI Alternatives FORBIDDEN:**
- ❌ Tauri (use Electron only - more mature ecosystem)
- ❌ NW.js (use Electron only - better maintained)
- ❌ Qt/PySide6 (use Electron only - cross-platform consistency)

**Dev Dependencies:**
```json
{
  "jest": "^30.0.0",
  "typescript": "^5.0.0"
}
```

**Jest Version Constraint (per ADR-007):**
- `jest`: 30.x required for Node.js 22+ compatibility
- Jest 29.x has initialization hanging issues with Node 22
- See ADR-007 for full rationale

### Python Dependencies (Existing - Locked)

**Core Installer Modules:**
- `installer/install.py` - Main orchestrator
- `installer/backup.py` - Backup/restore
- `installer/rollback.py` - Rollback mechanism
- `installer/merge.py` - CLAUDE.md merge
- `installer/version.py` - Version management
- `installer/validate.py` - Installation validation
- `installer/deploy.py` - File deployment

**DevForgeAI CLI (pip package):**
```
devforgeai-cli
├── devforgeai check-git
├── devforgeai validate-dod
├── devforgeai validate-context
└── devforgeai check-hooks
```

**Python Requirements:**
- Python 3.10+ (LOCKED)
- PyYAML 6.0+ (LOCKED - for configuration file parsing)

### Optional CLI Dependencies (EPIC-018)

**ast-grep-cli** (OPTIONAL - auto-prompted)
- **Version**: >=0.40.0,<1.0.0 (LOCKED)
- **Purpose**: Semantic code analysis engine for security/anti-pattern detection
- **Installation**: `pip install ast-grep-cli` (prompted if missing)
- **Fallback**: Grep-based analysis when unavailable (60-75% vs 90-95% accuracy)
- **Rationale**: AST-based analysis provides superior accuracy for code pattern detection
- **Platform Support**: Linux, macOS, Windows/WSL (via PyPI binary wheels)

**Alternatives FORBIDDEN:**
- ❌ semgrep (use ast-grep-cli only - smaller footprint, MIT license)
- ❌ tree-sitter bindings (use ast-grep-cli abstraction)

### Platform Support

**LOCKED - All platforms must be supported:**
- Windows 10+ (PowerShell, CMD)
- macOS 11+ (Bash, Zsh)
- Linux (Ubuntu, Debian, RHEL, Arch)
- WSL 1/2 (Windows Subsystem for Linux)

**Platform-Specific Handling:**
- Path separators: Use `path.join()` / `os.path.join()` (never hardcode `/` or `\`)
- File permissions: Handle NTFS vs POSIX differences
- Shell execution: Use cross-platform subprocess invocation

---

**REMEMBER**: This dependencies.md is for the framework itself. Projects using DevForgeAI will have their own dependencies.md created by devforgeai-architecture skill.
