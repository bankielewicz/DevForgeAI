# ADR-004: NPM Package Distribution for DevForgeAI Installer

**Date**: 2025-11-25
**Status**: Accepted
**Deciders**: User (via /ideate discovery)
**Epic**: EPIC-012, EPIC-013, EPIC-014

## Context

DevForgeAI needs an easy installation mechanism for external projects. The current installer exists as Python scripts in the `installer/` directory but lacks:

1. **Easy distribution** - Users must clone repo or download manually
2. **Version management** - No automated upgrade paths
3. **Wizard experience** - Users must understand file structure
4. **Cross-platform CLI** - No global command available

## Decision

We will distribute the DevForgeAI installer as an **NPM package** with a **Node.js CLI wrapper** that invokes the existing Python installer.

### Distribution Choice: NPM

**Options Considered:**
1. **NPM package** (Node.js ecosystem)
2. **PyPI package** (Python ecosystem)
3. **Homebrew formula** (macOS only)
4. **Shell script installer** (curl | bash pattern)

**Decision: NPM**

**Rationale:**
- Node.js developers are primary target audience for Claude Code projects
- NPM provides global CLI installation (`npm install -g`)
- Package versioning and update mechanism built-in
- Cross-platform support (Windows, macOS, Linux)
- Largest package registry ecosystem

### CLI Framework Choice: Commander.js

**Options Considered:**
1. **Commander.js** - Most popular, simple API
2. **Yargs** - Feature-rich, complex API
3. **Oclif** - Full framework, overkill for installer

**Decision: Commander.js 11+**

**Rationale:**
- Simple API for basic command structure
- Excellent TypeScript support
- Well-documented with large community
- Sufficient for installer use case (not building a complex CLI framework)

### Interactive Prompts: Inquirer.js

**Options Considered:**
1. **Inquirer.js** - Most popular, rich prompt types
2. **Prompts** - Lighter weight, fewer features
3. **Enquirer** - Modern API, less adoption

**Decision: Inquirer.js 9+**

**Rationale:**
- Rich prompt types (list, checkbox, confirm, input)
- Excellent validation support
- Most commonly used with Commander.js
- Mature and well-maintained

### Architecture: Hybrid Node.js + Python

**Options Considered:**
1. **Rewrite installer in Node.js** - Full rewrite
2. **Keep Python, add Node.js wrapper** - Hybrid approach
3. **Pure Python CLI via PyPI** - Python-only

**Decision: Hybrid (Node.js wrapper + Python core)**

**Rationale:**
- Reuses existing, tested Python installer code
- Node.js provides CLI UX layer (prompts, colors, progress)
- Python handles file operations, backup, rollback logic
- Avoids rewriting ~1,500 lines of working Python code
- Both ecosystems leverage their strengths

## Consequences

### Positive
- Easy installation: `npm install -g devforgeai`
- Global `devforgeai` command available immediately
- Version management via npm (updates, rollback to previous version)
- Cross-platform support out of the box
- Reuse existing tested Python installer logic

### Negative
- Requires both Node.js AND Python installed on user's machine
- Two language ecosystems to maintain
- Slightly larger package size (Node.js + Python bundled)
- Python dependency might be optional (fallback to basic mode)

### Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Python not installed on target machine | Make Python optional; basic install works, CLI features disabled |
| Cross-platform path differences | Use `path.join()` and `os.path.join()` consistently |
| NPM publishing unfamiliar | Create test package first, follow NPM provenance guide |

## Related

- **EPIC-012**: NPM Package Distribution
- **EPIC-013**: Interactive Installer & Validation
- **EPIC-014**: Version Management & Lifecycle
- **ADR-003**: Framework Markdown-Only Constraint (core framework remains documentation-only; installer is an exception as a distribution tool)

## Compliance

This ADR has been recorded in `devforgeai/adrs/` as required by the DevForgeAI framework.
