# ADR-009: Electron GUI Installer Template for Enterprise Users

**Date**: 2025-01-06
**Status**: Accepted
**Deciders**: User (via constitutional validation review)
**Epic**: EPIC-039
**Story**: STORY-248

## Context

EPIC-039 (Enterprise Installer Modes) introduces multiple installation modes to support different user types:
- CLI Wizard (STORY-247) - Terminal-based step-by-step installation
- GUI Installer (STORY-248) - Graphical point-and-click installation
- Silent/Headless (STORY-249) - CI/CD automation
- Offline Mode (STORY-250) - Air-gapped environments

The GUI Installer (STORY-248) requires a cross-platform graphical framework. This ADR documents the decision to use Electron for the GUI template and the conditions under which it is acceptable.

### Current Allowed NPM Dependencies (dependencies.md)

```
commander, inquirer@8.x, ora@5.x, chalk@4.x
```

The GUI installer requires additional dependencies not currently listed:
- **Electron 28+** - Cross-platform desktop framework
- **electron-builder** - Multi-platform packaging

## Decision

We will add **Electron 28+** and **electron-builder** as **OPTIONAL** dependencies in the NPM installer section of dependencies.md, specifically for the GUI installer template.

### Scope Limitations

**This ADR specifically limits the scope:**

1. **Template Only** - STORY-248 creates a GUI *template*, not a production-ready installer
2. **Optional Feature** - GUI installer is optional; users can use CLI wizard (STORY-247) instead
3. **Separate Directory** - GUI code lives in `installer/gui/`, isolated from core installer
4. **No Runtime Dependency** - Core DevForgeAI framework does NOT require Electron
5. **Enterprise Target** - GUI primarily targets non-technical enterprise users

### Technology Choice: Electron

**Options Considered:**
1. **Electron** - Cross-platform, web technologies (HTML/CSS/JS)
2. **Tauri** - Smaller bundles, Rust-based, newer ecosystem
3. **Qt for Python (PySide6)** - Python-native, large dependency
4. **Tkinter** - Python stdlib, dated appearance
5. **Web-based installer** - Requires browser, network dependency

**Decision: Electron 28+**

**Rationale:**
- Cross-platform support (Windows, macOS, Linux) with single codebase
- Native look and feel via system file dialogs
- Uses web technologies already familiar to developers
- electron-builder provides easy multi-platform packaging
- Largest ecosystem and community support
- Wraps existing Python installer via child_process (same as CLI)

### Directory Structure

```
installer/
├── __init__.py          # Core installer (existing)
├── wizard.py            # CLI wizard (STORY-247)
├── silent.py            # Silent mode (STORY-249)
├── offline.py           # Offline mode (STORY-250)
│
└── gui/                 # NEW: GUI installer template (STORY-248)
    ├── package.json     # Electron dependencies
    ├── main.js          # Electron main process
    ├── preload.js       # Context bridge
    ├── renderer/        # Frontend (HTML/CSS/JS)
    │   ├── index.html
    │   ├── styles.css
    │   └── app.js
    ├── assets/          # Icons, logos
    └── build/           # electron-builder config
```

### Dependency Classification

| Dependency | Version | Type | Required By |
|------------|---------|------|-------------|
| Electron | 28+ | Optional (NPM) | STORY-248 GUI only |
| electron-builder | latest | Optional (NPM, dev) | STORY-248 packaging |

**NOTE:** These are **optional** - core installer works without them.

## Consequences

### Positive
- Enterprise users get familiar point-and-click experience
- Non-technical users can install without terminal knowledge
- Single codebase supports Windows, macOS, Linux
- Reuses existing Python installer logic via IPC
- Template provides starting point for customization

### Negative
- Large bundle size (~150MB per platform)
- Two language ecosystems (Node.js + Python) for GUI mode
- Electron updates require tracking security advisories
- Code signing required for macOS/Windows distribution (not in template scope)

### Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Bundle size too large for some users | CLI wizard (STORY-247) as lightweight alternative |
| Electron security vulnerabilities | Context isolation enabled, nodeIntegration disabled |
| Cross-platform inconsistencies | Platform-specific testing in CI |
| Template becomes outdated | Version-lock Electron, document upgrade path |

## Compliance

### Constitutional Context File Updates Required

1. **dependencies.md** - Add Electron to NPM Optional dependencies
2. **source-tree.md** - Add `installer/gui/` directory structure

### Quality Gates

- GUI installer passes all AC verification tests
- electron-builder produces valid packages for all 3 platforms
- No security vulnerabilities (`npm audit` clean)
- Bundle size < 150MB per platform

## Related

- **EPIC-039**: Enterprise Installer Modes
- **STORY-247**: CLI Wizard Installer (alternative to GUI)
- **STORY-248**: GUI Installer Template (this ADR applies)
- **ADR-004**: NPM Package Distribution (establishes hybrid Node.js + Python pattern)
- **ADR-003**: Framework Markdown-Only Constraint (installer is exception as distribution tool)

## Compliance

This ADR has been recorded in `devforgeai/specs/adrs/` as required by the DevForgeAI framework. Constitutional context files (dependencies.md, source-tree.md) will be updated to reflect this decision.
