# DevForgeAI Build Guide

How to compile, build, and package DevForgeAI CLIs and distribution bundles.

**Version:** 1.0.0
**Last Updated:** 2025-01-14

---

## Overview

DevForgeAI has multiple build targets:

| Target | Output | Command |
|--------|--------|---------|
| Node.js CLI | Global `devforgeai` command | `npm install -g .` |
| Python CLI | Global `devforgeai` validators | `pip install -e .claude/scripts/` |
| Offline Bundle | `bundled/` directory | `bash scripts/build-offline-bundle.sh` |
| npm Package | `devforgeai-x.x.x.tgz` | `npm pack` |
| GUI Installer | Desktop apps (Win/Mac/Linux) | `cd installer/gui && npm run build` |

---

## Building the Node.js CLI

The Node.js CLI provides the installation wizard interface.

### Development Build

```bash
# Install dependencies
npm install

# Install globally (creates devforgeai command)
npm install -g .

# Verify
devforgeai --version
devforgeai --help
```

### What Gets Built

```
devforgeai (global command)
├── Entry: bin/devforgeai.js
├── Core: lib/cli.js
└── Wizard: src/cli/wizard/*.js
    ├── install-wizard.js
    ├── prompt-service.js
    ├── progress-service.js
    ├── output-formatter.js
    └── signal-handler.js
```

### Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| commander | ^11.0.0 | CLI argument parsing |
| inquirer | ^8.2.6 | Interactive prompts |
| ora | 5.4.1 | Spinners |
| chalk | 4.1.2 | Terminal colors |
| cli-progress | ^3.12.0 | Progress bars |

---

## Building the Python CLI

The Python CLI provides validators and phase tracking.

### Development Build (Editable Mode)

```bash
# Install in editable mode (changes reflect immediately)
pip install --break-system-packages -e .claude/scripts/

# Verify
devforgeai validate-dod --help
devforgeai phase-status --help
```

### Production Build (Wheel)

```bash
cd .claude/scripts

# Build wheel file
python setup.py bdist_wheel

# Output: dist/devforgeai_cli-x.x.x-py3-none-any.whl

# Install from wheel
pip install dist/devforgeai_cli-*.whl
```

### What Gets Built

```
devforgeai (CLI commands)
├── validate-dod       # DoD validation
├── check-git          # Git repository check
├── validate-context   # Context file validation
├── check-hooks        # Hook configuration check
├── invoke-hooks       # Hook invocation
├── phase-*            # Phase state commands
│   ├── phase-init
│   ├── phase-check
│   ├── phase-complete
│   ├── phase-status
│   ├── phase-record
│   └── phase-observe
└── ast-grep           # Code scanning
    ├── ast-grep scan
    ├── ast-grep init
    └── ast-grep validate-config
```

---

## Building the Offline Bundle

Creates a complete distribution package for offline/air-gapped installations.

### Build Command

```bash
bash scripts/build-offline-bundle.sh
```

### Output Structure

```
bundled/
├── claude/                   # Framework files (~27 MB)
│   ├── skills/               # 21 skill directories
│   ├── agents/               # 37 agent definitions
│   ├── commands/             # 36 command definitions
│   ├── rules/                # Execution rules
│   ├── memory/               # Knowledge base
│   └── hooks/                # Automation hooks
├── devforgeai/               # Configuration templates
│   ├── specs/context/        # 6 context file templates
│   └── protocols/            # Framework protocols
├── python-cli/
│   └── wheels/               # Python CLI wheel files
├── checksums.json            # SHA256 integrity manifest
├── version.json              # Version metadata
├── CLAUDE.md                 # Installation template
└── README.md                 # Bundle README
```

### Bundle Size

- **Uncompressed:** ~50-100 MB
- **Compressed (tar.gz):** ~20-40 MB
- **Files:** 700+ framework files

### Build Script Details

The `scripts/build-offline-bundle.sh` script:

1. Creates `bundled/` directory structure
2. Copies framework files from `src/claude/` and `src/devforgeai/`
3. Removes development artifacts (`.pyc`, `node_modules`, etc.)
4. Builds Python wheel files
5. Copies version metadata
6. Generates SHA256 checksums (`checksums.json`)
7. Reports bundle size and file count

---

## Creating the npm Package

Package the framework for npm distribution.

### Build Command

```bash
# Build offline bundle first
bash scripts/build-offline-bundle.sh

# Create npm package
npm pack

# Output: devforgeai-1.0.0.tgz
```

### Package Contents

The npm package includes:
- `bin/devforgeai.js` - CLI entry point
- `lib/cli.js` - CLI logic
- `src/cli/wizard/` - Wizard modules
- `bundled/` - Complete framework bundle
- `package.json` - Package metadata

### Publishing to npm

```bash
# Login to npm
npm login

# Publish
npm publish

# Publish pre-release
npm publish --tag beta
```

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed release process.

---

## Building the GUI Installer (Electron)

Creates desktop installers for Windows, macOS, and Linux.

### Setup

```bash
cd installer/gui

# Install dependencies
npm install
```

### Build Commands

```bash
# Build for all platforms
npm run build

# Platform-specific builds
npm run build:win    # Windows (.exe, .msi)
npm run build:mac    # macOS (.dmg, .pkg)
npm run build:linux  # Linux (.deb, .AppImage)
```

### Output

```
installer/gui/dist/
├── DevForgeAI-Setup-1.0.0.exe      # Windows
├── DevForgeAI-1.0.0.dmg            # macOS
├── DevForgeAI-1.0.0.AppImage       # Linux
└── DevForgeAI-1.0.0.deb            # Debian/Ubuntu
```

### Configuration

Build configuration in `installer/gui/build/builder-config.json`:

```json
{
  "appId": "com.devforgeai.installer",
  "productName": "DevForgeAI",
  "win": {
    "target": ["nsis", "msi"]
  },
  "mac": {
    "target": ["dmg", "pkg"]
  },
  "linux": {
    "target": ["AppImage", "deb"]
  }
}
```

---

## Version Management

### Version Files

| File | Purpose |
|------|---------|
| `package.json` | npm package version |
| `src/devforgeai/version.json` | Framework version |
| `bundled/version.json` | Bundle version (generated) |

### Version Bump Process

```bash
# Patch release (1.0.0 → 1.0.1)
npm version patch

# Minor release (1.0.0 → 1.1.0)
npm version minor

# Major release (1.0.0 → 2.0.0)
npm version major

# Update framework version
# Edit: src/devforgeai/version.json
```

### Version Format

```json
{
  "version": "1.0.0",
  "released_at": "2025-01-14T00:00:00Z",
  "schema_version": "1.0"
}
```

---

## Continuous Integration

### GitHub Actions

Build workflows in `.github/workflows/`:

```yaml
# Example: build-and-test.yml
name: Build and Test
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 18
      - run: npm install
      - run: npm test
      - run: bash scripts/build-offline-bundle.sh
```

---

## Troubleshooting

### "Python wheel build failed"

**Solution:**
```bash
# Ensure pip has wheel package
pip install wheel setuptools

# Try building again
cd .claude/scripts
python setup.py bdist_wheel
```

### "npm pack includes too many files"

**Check `.npmignore`** - Ensure development files are excluded:
```
tests/
*.pyc
__pycache__/
.coverage
```

### "Bundle size exceeds limit"

**Clean development artifacts:**
```bash
# Remove from bundled/
find bundled/ -type d -name "__pycache__" -exec rm -rf {} +
find bundled/ -type d -name "node_modules" -exec rm -rf {} +
find bundled/ -type f -name "*.pyc" -delete
```

### "Checksums don't match after modification"

**Regenerate checksums:**
```bash
# Re-run bundle script
bash scripts/build-offline-bundle.sh
```

---

## Build Verification Checklist

Before releasing:

- [ ] `npm test` passes
- [ ] `npm install -g .` works
- [ ] `devforgeai --version` shows correct version
- [ ] `devforgeai install /tmp/test --yes` completes
- [ ] `bash scripts/build-offline-bundle.sh` succeeds
- [ ] Bundle size under 60 MB compressed
- [ ] `npm pack` creates valid package
- [ ] Checksums generated in `bundled/checksums.json`

---

## See Also

- [DEVELOPER-SETUP.md](DEVELOPER-SETUP.md) - Development environment setup
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Release process
- [installer/README.md](../installer/README.md) - Installer framework
- [docs/cli/README.md](cli/README.md) - CLI architecture
