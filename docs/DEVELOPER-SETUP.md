# DevForgeAI Developer Setup Guide

Quick guide for setting up a local development environment to contribute to DevForgeAI.

**Version:** 1.0.0
**Last Updated:** 2025-01-14

---

## Prerequisites

### Required Software

| Software | Minimum Version | Verify Command |
|----------|-----------------|----------------|
| Node.js | 18.0.0 | `node --version` |
| npm | 8.0.0 | `npm --version` |
| Python | 3.8.0 | `python3 --version` |
| pip | 21.0.0 | `pip3 --version` |
| Git | 2.30.0 | `git --version` |

### System Requirements

- **Disk Space:** ~500 MB (includes node_modules and test files)
- **RAM:** 4 GB minimum (for running tests)
- **OS:** Windows (WSL), macOS, or Linux

---

## Quick Setup (5 minutes)

```bash
# 1. Clone the repository
git clone https://github.com/bankielewicz/DevForgeAI.git
cd DevForgeAI

# 2. Install Node.js dependencies
npm install

# 3. Install Python CLI in editable mode
pip install --break-system-packages -e .claude/scripts/

# 4. Verify setup
npm test
devforgeai --version
```

---

## Detailed Setup

### Step 1: Clone Repository

```bash
# HTTPS
git clone https://github.com/bankielewicz/DevForgeAI.git

# SSH (if you have keys configured)
git clone git@github.com:bankielewicz/DevForgeAI.git

cd DevForgeAI
```

### Step 2: Install Node.js CLI

The Node.js CLI provides the installation wizard and user interface.

```bash
# Install dependencies
npm install

# (Optional) Install globally for testing
npm install -g .

# Verify
devforgeai --version
# Output: devforgeai v1.0.0

devforgeai --help
```

**Files involved:**
- `bin/devforgeai.js` - Entry point
- `lib/cli.js` - Core CLI logic
- `src/cli/wizard/` - Interactive wizard modules

### Step 3: Install Python CLI

The Python CLI provides validators, phase tracking, and hook integration.

```bash
# Install in editable/development mode
pip install --break-system-packages -e .claude/scripts/

# Verify
devforgeai validate-dod --help
devforgeai phase-status --help
devforgeai ast-grep --help
```

**Note:** The `--break-system-packages` flag may be needed on newer Python installations that use PEP 668 externally managed environments.

**Files involved:**
- `.claude/scripts/devforgeai_cli/` - Python CLI source
- `.claude/scripts/setup.py` - Package configuration

### Step 4: Run Tests

```bash
# Node.js tests (unit + integration)
npm test

# Python tests (if pytest available)
cd .claude/scripts
pytest tests/ -v

# Coverage report
npm run test:coverage
```

### Step 5: Verify Complete Setup

Run this verification script:

```bash
# Check Node.js CLI
node --version && echo "✓ Node.js OK"
npm --version && echo "✓ npm OK"
devforgeai --version && echo "✓ Node.js CLI OK"

# Check Python CLI
python3 --version && echo "✓ Python OK"
devforgeai validate-dod --help > /dev/null && echo "✓ Python CLI OK"

# Check tests
npm test > /dev/null 2>&1 && echo "✓ Tests pass"
```

Expected output:
```
v18.x.x
✓ Node.js OK
8.x.x
✓ npm OK
devforgeai v1.0.0
✓ Node.js CLI OK
Python 3.x.x
✓ Python OK
✓ Python CLI OK
✓ Tests pass
```

---

## Project Structure

```
DevForgeAI/
├── bin/                      # CLI entry points
│   └── devforgeai.js         # Node.js CLI entry
├── lib/                      # Node.js CLI core
│   └── cli.js
├── src/                      # Source files
│   ├── cli/wizard/           # Installation wizard
│   ├── claude/               # Framework source (for bundling)
│   └── devforgeai/           # Framework source (for bundling)
├── installer/                # Python installer system
│   ├── install.py            # Main installer
│   ├── gui/                  # Electron GUI installer
│   └── tests/                # Installer tests
├── .claude/                  # Operational framework files
│   ├── skills/               # Skill definitions
│   ├── agents/               # Subagent definitions
│   ├── commands/             # Slash commands
│   ├── rules/                # Execution rules
│   └── scripts/              # Python CLI source
├── devforgeai/               # Project specifications
│   └── specs/                # Stories, epics, context
├── docs/                     # Documentation
├── tests/                    # Test suites
├── scripts/                  # Build scripts
└── package.json              # npm configuration
```

---

## Development Workflow

### Making Changes

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make changes** to CLI or framework files

3. **Run tests**
   ```bash
   npm test
   ```

4. **Test locally**
   ```bash
   # Reinstall CLI to test changes
   npm install -g .
   devforgeai --version
   ```

5. **Submit PR** following [CONTRIBUTING.md](../CONTRIBUTING.md)

### Testing CLI Changes

```bash
# After modifying Node.js CLI
npm install -g .
devforgeai install /tmp/test-project --yes

# After modifying Python CLI
pip install -e .claude/scripts/
devforgeai validate-dod path/to/story.md
```

---

## Troubleshooting

### "npm install" fails with permission error

**Solution:**
```bash
# Option 1: Use sudo (not recommended)
sudo npm install -g .

# Option 2: Fix npm permissions
# https://docs.npmjs.com/resolving-eacces-permissions-errors
```

### "pip install" fails with "externally managed environment"

**Solution:**
```bash
# Use --break-system-packages flag
pip install --break-system-packages -e .claude/scripts/

# Or use a virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -e .claude/scripts/
```

### "devforgeai: command not found"

**Solution:**
```bash
# Add npm global bin to PATH
export PATH="$PATH:$(npm config get prefix)/bin"

# Or for Python
export PATH="$PATH:$(python3 -m site --user-base)/bin"
```

### Tests fail with "Python version mismatch"

**Solution:**
```bash
# Check Python version (need 3.8+)
python3 --version

# Install correct version (Ubuntu/Debian)
sudo apt install python3.10

# Use specific version
python3.10 -m pip install -e .claude/scripts/
```

### Node.js version too old

**Solution:**
```bash
# Check version
node --version

# Install Node 18+ via nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 18
nvm use 18
```

---

## IDE Setup (Optional)

### VS Code

Recommended extensions:
- ESLint
- Prettier
- Python
- Markdown All in One

Settings (`.vscode/settings.json`):
```json
{
  "editor.formatOnSave": true,
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true
}
```

### JetBrains (WebStorm/PyCharm)

- Enable ESLint integration
- Configure Python interpreter to project venv
- Enable Markdown support

---

## Next Steps

- Read [BUILD.md](BUILD.md) for compilation/packaging instructions
- Read [CONTRIBUTING.md](../CONTRIBUTING.md) for contribution guidelines
- Review [docs/cli/README.md](cli/README.md) for CLI architecture

---

## Support

- **Issues:** [GitHub Issues](https://github.com/bankielewicz/DevForgeAI/issues)
- **Discussions:** [GitHub Discussions](https://github.com/bankielewicz/DevForgeAI/discussions)
